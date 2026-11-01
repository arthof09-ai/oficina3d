# Comparativo Oficina3D x Blender nativo - etapa de cor (pintura por projecao)
# Rota 100% Blender: UV propria (Smart UV Project), projecao das 4 vistas
# canonicas por cameras (nos de shader), bake Cycles EMIT para textura.
# Headless: blender -b --python pintar_blender.py
import bpy, os, json, math, time
import numpy as np
from mathutils import Vector

T0 = time.time()
W = r'C:\Users\txcga\RPG_Local\Oficina3D\_cache\tmp\comparativo-blender'
IN_GLB = os.path.join(W, 'entrada', 'modelo_sem_cor.glb')
OUT = os.path.join(W, 'saida')
os.makedirs(OUT, exist_ok=True)
VIEW_NAMES = ['frente', 'costas', 'esquerda', 'direita']
TEX = 1024
RES = {'etapas': {}, 'avisos': []}

def log(msg):
    print('[COMP] ' + msg, flush=True)

def etapa(nome, t):
    RES['etapas'][nome] = round(t, 2)
    log(nome + ': ' + str(round(t, 2)) + 's')

# ---------------------------------------------------------------- setup
def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)

def import_join(path):
    bpy.ops.import_scene.gltf(filepath=path)
    meshes = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    bpy.ops.object.select_all(action='DESELECT')
    for o in meshes:
        o.select_set(True)
    bpy.context.view_layer.objects.active = meshes[0]
    if len(meshes) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
    for o in list(bpy.context.scene.objects):
        if o != obj:
            bpy.data.objects.remove(o, do_unlink=True)
    return obj

def bbox_info(obj):
    bb = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
    center = Vector(((min(xs)+max(xs))/2, (min(ys)+max(ys))/2, (min(zs)+max(zs))/2))
    dims = Vector((max(xs)-min(xs), max(ys)-min(ys), max(zs)-min(zs)))
    radius = max((v - center).length for v in bb)
    return center, dims, radius

def make_cam(scene, name, pos, target, ortho=None, angle=None):
    data = bpy.data.cameras.new(name)
    ob = bpy.data.objects.new(name, data)
    scene.collection.objects.link(ob)
    ob.location = pos
    d = Vector(target) - Vector(pos)
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    if ortho is not None:
        data.type = 'ORTHO'
        data.ortho_scale = ortho
    if angle is not None:
        data.sensor_fit = 'HORIZONTAL'
        data.angle = angle
    return ob

def cycles_setup(scene, samples=1):
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = samples
    scene.cycles.use_denoising = False
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'OPTIX'
        prefs.get_devices()
        for d in prefs.devices:
            d.use = True
        scene.cycles.device = 'GPU'
        log('Cycles: GPU (OPTIX) ativado')
    except Exception as e:
        scene.cycles.device = 'CPU'
        RES['avisos'].append('GPU falhou, CPU usado: ' + str(e))
        log('Cycles: fallback CPU')

# ---------------------------------------------------------------- imagens
def mask_bbox(img, res=None):
    """Retorna (bbox normalizada u0,v0,u1,v1 com v a partir de baixo, mascara)."""
    if res is not None and tuple(img.size) != (res, res):
        img = img.copy()
        img.scale(res, res)
    w, h = img.size
    px = np.empty(w * h * 4, dtype=np.float32)
    img.pixels.foreach_get(px)
    px = px.reshape(h, w, 4)
    a = px[:, :, 3]
    if a.max() - a.min() < 0.05:
        rgb = px[:, :, :3]
        corner = rgb[0, 0]
        mask = np.abs(rgb - corner).sum(axis=2) > 0.15
    else:
        mask = a > 0.5
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return None, mask
    bbox = (xs.min() / w, ys.min() / h, (xs.max() + 1) / w, (ys.max() + 1) / h)
    return bbox, mask

def iou(a, b):
    inter = np.logical_and(a, b).sum()
    union = np.logical_or(a, b).sum()
    return float(inter) / float(union) if union else 0.0

# ---------------------------------------------------------------- principal
reset()
scene = bpy.context.scene
t = time.time()
obj = import_join(IN_GLB)
center, dims, radius = bbox_info(obj)
log('mesh: %d tris, dims %s, centro %s' % (len(obj.data.polygons), tuple(round(d, 3) for d in dims), tuple(round(c, 3) for c in center)))
etapa('import', time.time() - t)

views = {}
for n in VIEW_NAMES:
    im = bpy.data.images.load(os.path.join(W, 'vistas', n + '.png'))
    im.colorspace_settings.name = 'sRGB'
    views[n] = im
    log('vista %s: %dx%d' % (n, im.size[0], im.size[1]))

# ------------------------------------------------- calibracao: orientacao
t = time.time()
cycles_setup(scene, samples=1)
world = bpy.data.worlds.new('WPreto')
world.use_nodes = True
world.node_tree.nodes['Background'].inputs[0].default_value = (0, 0, 0, 1)
world.node_tree.nodes['Background'].inputs[1].default_value = 1.0
scene.world = world
silh_mat = bpy.data.materials.new('SILH')
silh_mat.use_nodes = True
emit = silh_mat.node_tree.nodes.new('ShaderNodeEmission')
emit.inputs[0].default_value = (1, 1, 1, 1)
outn = silh_mat.node_tree.nodes.get('Material Output')
silh_mat.node_tree.links.new(emit.outputs[0], outn.inputs[0])
vl = bpy.context.view_layer
vl.material_override = silh_mat
scene.render.image_settings.file_format = 'PNG'
DIRS = {'+X': Vector((1, 0, 0)), '-X': Vector((-1, 0, 0)),
        '+Y': Vector((0, 1, 0)), '-Y': Vector((0, -1, 0))}
sil = {}
for dn, dv in DIRS.items():
    cam = make_cam(scene, 'Silh' + dn, center + dv * (radius * 4 + 1.0), center,
                   ortho=max(dims) * 1.25)
    scene.camera = cam
    scene.render.resolution_x = 192
    scene.render.resolution_y = 192
    scene.render.resolution_percentage = 100
    p = os.path.join(OUT, 'silh_' + dn.replace('+', 'p').replace('-', 'm') + '.png')
    scene.render.filepath = p
    bpy.ops.render.render(write_still=True)
    im = bpy.data.images.load(p)
    _, m = mask_bbox(im)
    sil[dn] = m
    bpy.data.images.remove(im)
    bpy.data.objects.remove(cam, do_unlink=True)
ref_masks = {}
for n in VIEW_NAMES:
    _, m = mask_bbox(views[n], res=192)
    ref_masks[n] = m
ious = {dn: {n: iou(sil[dn], ref_masks[n]) for n in VIEW_NAMES} for dn in DIRS}
log('IoU silhuetas: ' + json.dumps({k: {n: round(v, 3) for n, v in d.items()} for k, d in ious.items()}))
OPP = {'+X': '-X', '-X': '+X', '+Y': '-Y', '-Y': '+Y'}
best = None
for fd in DIRS:
    cd = OPP[fd]
    rest = [d for d in DIRS if d not in (fd, cd)]
    s1 = ious[rest[0]]['esquerda'] + ious[rest[1]]['direita']
    s2 = ious[rest[1]]['esquerda'] + ious[rest[0]]['direita']
    if s1 >= s2:
        assign = {rest[0]: 'esquerda', rest[1]: 'direita'}
        ss = s1
    else:
        assign = {rest[1]: 'esquerda', rest[0]: 'direita'}
        ss = s2
    total = ious[fd]['frente'] + ious[cd]['costas'] + ss
    if best is None or total > best:
        best = total
        best_map = {fd: 'frente', cd: 'costas'}
        best_map[rest[0]] = assign[rest[0]]
        best_map[rest[1]] = assign[rest[1]]
orient = {v: k for k, v in best_map.items()}  # vista -> direcao
ovr_path = os.path.join(OUT, 'orient_override.json')
if os.path.exists(ovr_path):
    with open(ovr_path) as f:
        orient = json.load(f)
    RES['avisos'].append('orientacao substituida por orient_override.json')
    log('orientacao substituida pelo override: ' + json.dumps(orient))
RES['orientacao'] = orient
RES['iou_silhueta'] = {n: round(ious[orient[n]][n], 3) for n in VIEW_NAMES}
log('orientacao (vista->direcao da camera): ' + json.dumps(orient))
log('IoU escolhidos: ' + json.dumps(RES['iou_silhueta']))
vl.material_override = None
etapa('calibracao_orientacao', time.time() - t)

# ------------------------------------------------- UV propria do Blender
t = time.time()
uv_mode = 'existente'
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
try:
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.uv.smart_project(angle_limit=math.radians(66.0), island_margin=0.003,
                             correct_aspect=True)
    bpy.ops.object.mode_set(mode='OBJECT')
    uv_mode = 'smart_project'
except Exception as e:
    RES['avisos'].append('smart_project falhou: ' + str(e))
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass
RES['uv'] = uv_mode
log('UV: ' + uv_mode)
etapa('uv', time.time() - t)

# ------------------------------------------------- cameras + ajuste fino
t = time.time()
verts = np.empty(len(obj.data.vertices) * 3, dtype=np.float64)
obj.data.vertices.foreach_get('co', verts)
verts = verts.reshape(-1, 3)
if len(verts) > 40000:
    verts = verts[::3]
mw = np.array(obj.matrix_world)
verts_w = verts @ mw[:3, :3].T + mw[:3, 3]
scene.render.resolution_x = 512
scene.render.resolution_y = 512
scene.render.resolution_percentage = 100
proj_cams = {}
fit_info = {}
for n in VIEW_NAMES:
    dv = DIRS[orient[n]]
    tgt, _ = mask_bbox(views[n])
    dist = radius * 4.5
    off = Vector((0.0, 0.0, 0.0))
    cam = make_cam(scene, 'Proj_' + n, center + dv * dist, center, angle=math.radians(32.0))
    bpy.context.view_layer.update()
    tanx = math.tan(cam.data.angle_x / 2.0)
    tany = math.tan(cam.data.angle_y / 2.0)
    right = Vector(cam.matrix_world.col[0][:3]).normalized()
    up = Vector(cam.matrix_world.col[1][:3]).normalized()
    cur = None
    for it in range(6):
        pos = center + dv * dist + off
        cam.location = pos
        bpy.context.view_layer.update()
        Minv = np.array(cam.matrix_world.inverted())
        pc = verts_w @ Minv[:3, :3].T + Minv[:3, 3]
        front = pc[:, 2] < -0.05
        pf = pc[front]
        u = 0.5 + 0.5 * (pf[:, 0] / (-pf[:, 2])) / tanx
        v = 0.5 + 0.5 * (pf[:, 1] / (-pf[:, 2])) / tany
        cur = (u.min(), v.min(), u.max(), v.max())
        cw, ch = cur[2] - cur[0], cur[3] - cur[1]
        tw, th = tgt[2] - tgt[0], tgt[3] - tgt[1]
        r = math.sqrt((cw / tw) * (ch / th))
        dist *= r
        eu = (cur[0] + cur[2]) / 2 - (tgt[0] + tgt[2]) / 2
        ev = (cur[1] + cur[3]) / 2 - (tgt[1] + tgt[3]) / 2
        off = off + right * (eu * 2 * dist * tanx) + up * (ev * 2 * dist * tany)
    cam.location = center + dv * dist + off
    bpy.context.view_layer.update()
    # empty gemea da camera para o no Texture Coordinate
    emp = bpy.data.objects.new('ProjObj_' + n, None)
    scene.collection.objects.link(emp)
    emp.location = cam.location
    emp.rotation_euler = cam.rotation_euler
    proj_cams[n] = (cam, emp, tanx, tany)
    inter = (max(0.0, min(cur[2], tgt[2]) - max(cur[0], tgt[0])) *
             max(0.0, min(cur[3], tgt[3]) - max(cur[1], tgt[1])))
    union = (cur[2] - cur[0]) * (cur[3] - cur[1]) + (tgt[2] - tgt[0]) * (tgt[3] - tgt[1]) - inter
    fit_info[n] = {'bbox_proj': [round(x, 3) for x in cur],
                   'bbox_alvo': [round(x, 3) for x in tgt],
                   'iou_bbox': round(inter / union, 3) if union > 0 else 0.0,
                   'dist': round(dist, 3)}
    log('fit %s: iou_bbox=%.3f dist=%.2f' % (n, fit_info[n]['iou_bbox'], dist))
RES['ajuste_cameras'] = fit_info
etapa('ajuste_cameras', time.time() - t)

# --------------------------------------- visibilidade por vista (raycast)
# Sem teste de oclusao, a projecao pinta ATRAVES do modelo (a imagem da
# frente mancha superficies escondidas). Raycast BVH do proprio Blender:
# para cada face e cada camera, visivel = o raio da face ate a camera nao
# bate em outra face antes. Gravado como atributo FLOAT por face.
t = time.time()
from mathutils.bvhtree import BVHTree
dg = bpy.context.evaluated_depsgraph_get()
bvh = BVHTree.FromObject(obj, dg)
vis_frac = {}
for n in VIEW_NAMES:
    cam, emp, tanx, tany = proj_cams[n]
    P = cam.matrix_world.translation
    attr = obj.data.attributes.new('vis_' + n, 'FLOAT', 'FACE')
    vals = np.zeros(len(obj.data.polygons), dtype=np.float32)
    nm = obj.matrix_world.to_3x3()
    for i, pol in enumerate(obj.data.polygons):
        c = obj.matrix_world @ pol.center
        pn = (nm @ pol.normal).normalized()
        origem = c + pn * 0.003
        d = P - c
        dist = d.length
        loc, nrm, idx, hdist = bvh.ray_cast(origem, d.normalized())
        if idx is None or idx == i or hdist >= dist - 0.01:
            vals[i] = 1.0
    attr.data.foreach_set('value', vals)
    vis_frac[n] = round(float(vals.mean()) * 100, 1)
    log('visibilidade %s: %.1f%% das faces' % (n, vis_frac[n]))
RES['visibilidade_faces_pct'] = vis_frac
etapa('visibilidade_raycast', time.time() - t)

# ------------------------------------------------- material de projecao
def N(nt, tipo, x=0.0, y=0.0, **kw):
    nd = nt.nodes.new(tipo)
    nd.location = (x, y)
    for k, v in kw.items():
        setattr(nd, k, v)
    return nd

def math1(nt, op, a, b, x, y):
    """a: socket ou valor; b: valor numerico (segunda entrada)."""
    nd = N(nt, 'ShaderNodeMath', x, y, operation=op)
    if hasattr(a, 'name') or hasattr(a, 'type'):
        nt.links.new(a, nd.inputs[0])
    else:
        nd.inputs[0].default_value = float(a)
    nd.inputs[1].default_value = float(b)
    return nd.outputs[0]

def build_paint_material():
    mat = bpy.data.materials.new('ProjecaoBlender')
    mat.use_nodes = True
    nt = mat.node_tree
    nt.nodes.clear()
    out = N(nt, 'ShaderNodeOutputMaterial', 1400, 0)
    geo = N(nt, 'ShaderNodeNewGeometry', -1200, -600)
    sum_rgb = None
    sum_w = None
    for i, n in enumerate(VIEW_NAMES):
        cam, emp, tanx, tany = proj_cams[n]
        y0 = 500 - i * 320
        tc = N(nt, 'ShaderNodeTexCoord', -1200, y0)
        tc.object = emp
        sep = N(nt, 'ShaderNodeSeparateXYZ', -1000, y0)
        nt.links.new(tc.outputs['Object'], sep.inputs[0])
        depth = math1(nt, 'MULTIPLY', sep.outputs[2], -1.0, -800, y0 - 60)
        den_h = math1(nt, 'MULTIPLY', depth, 2.0 * tanx, -800, y0)
        den_v = math1(nt, 'MULTIPLY', depth, 2.0 * tany, -800, y0 - 120)
        # divisao perspectiva: X/den_h e Y/den_v (nodos DIVIDE com dois sockets ligados)
        du = N(nt, 'ShaderNodeMath', -620, y0, operation='DIVIDE')
        nt.links.new(sep.outputs[0], du.inputs[0])
        nt.links.new(den_h, du.inputs[1])
        dv = N(nt, 'ShaderNodeMath', -620, y0 - 120, operation='DIVIDE')
        nt.links.new(sep.outputs[1], dv.inputs[0])
        nt.links.new(den_v, dv.inputs[1])
        u2 = math1(nt, 'ADD', math1(nt, 'MULTIPLY', du.outputs[0], 0.5, -460, y0), 0.5, -300, y0)
        v2 = math1(nt, 'ADD', math1(nt, 'MULTIPLY', dv.outputs[0], 0.5, -460, y0 - 120), 0.5, -300, y0 - 120)
        comb = N(nt, 'ShaderNodeCombineXYZ', -140, y0)
        nt.links.new(u2, comb.inputs[0])
        nt.links.new(v2, comb.inputs[1])
        comb.inputs[2].default_value = 0.0
        tex = N(nt, 'ShaderNodeTexImage', 40, y0)
        tex.image = views[n]
        tex.extension = 'CLIP'
        nt.links.new(comb.outputs[0], tex.inputs[0])
        # frustum: 0<u<1, 0<v<1, depth>0.02
        f1 = math1(nt, 'GREATER_THAN', u2, 0.0, 40, y0 - 200)
        f2 = math1(nt, 'LESS_THAN', u2, 1.0, 40, y0 - 260)
        f3 = math1(nt, 'GREATER_THAN', v2, 0.0, 40, y0 - 320)
        f4 = math1(nt, 'LESS_THAN', v2, 1.0, 40, y0 - 380)
        f5 = math1(nt, 'GREATER_THAN', depth, 0.02, 40, y0 - 440)
        frus = N(nt, 'ShaderNodeMath', 220, y0 - 200, operation='MULTIPLY')
        nt.links.new(f1, frus.inputs[0])
        nt.links.new(f2, frus.inputs[1])
        frus2 = N(nt, 'ShaderNodeMath', 380, y0 - 200, operation='MULTIPLY')
        nt.links.new(frus.outputs[0], frus2.inputs[0])
        nt.links.new(f3, frus2.inputs[1])
        frus3 = N(nt, 'ShaderNodeMath', 540, y0 - 200, operation='MULTIPLY')
        nt.links.new(frus2.outputs[0], frus3.inputs[0])
        nt.links.new(f4, frus3.inputs[1])
        frus4 = N(nt, 'ShaderNodeMath', 700, y0 - 200, operation='MULTIPLY')
        nt.links.new(frus3.outputs[0], frus4.inputs[0])
        nt.links.new(f5, frus4.inputs[1])
        frustum = frus4.outputs[0]
        # facing: dot(N, normalize(camPos - Pos))
        campos = N(nt, 'ShaderNodeCombineXYZ', -1200, y0 - 500)
        cp = cam.matrix_world.translation
        campos.inputs[0].default_value = cp.x
        campos.inputs[1].default_value = cp.y
        campos.inputs[2].default_value = cp.z
        sub = N(nt, 'ShaderNodeVectorMath', -1000, y0 - 500, operation='SUBTRACT')
        nt.links.new(campos.outputs[0], sub.inputs[0])
        nt.links.new(geo.outputs['Position'], sub.inputs[1])
        nrm = N(nt, 'ShaderNodeVectorMath', -820, y0 - 500, operation='NORMALIZE')
        nt.links.new(sub.outputs[0], nrm.inputs[0])
        dot = N(nt, 'ShaderNodeVectorMath', -640, y0 - 500, operation='DOT_PRODUCT')
        nt.links.new(geo.outputs['Normal'], dot.inputs[0])
        nt.links.new(nrm.outputs[0], dot.inputs[1])
        fac = math1(nt, 'POWER', math1(nt, 'MAXIMUM', dot.outputs['Value'], 0.0, -460, y0 - 500), 1.5, -300, y0 - 500)
        w1 = N(nt, 'ShaderNodeMath', -120, y0 - 500, operation='MULTIPLY')
        nt.links.new(fac, w1.inputs[0])
        nt.links.new(tex.outputs['Alpha'], w1.inputs[1])
        w2 = N(nt, 'ShaderNodeMath', 40, y0 - 500, operation='MULTIPLY')
        nt.links.new(w1.outputs[0], w2.inputs[0])
        nt.links.new(frustum, w2.inputs[1])
        attr = N(nt, 'ShaderNodeAttribute', 200, y0 - 560)
        attr.attribute_name = 'vis_' + n
        w3 = N(nt, 'ShaderNodeMath', 360, y0 - 500, operation='MULTIPLY')
        nt.links.new(w2.outputs[0], w3.inputs[0])
        nt.links.new(attr.outputs['Fac'], w3.inputs[1])
        weight = w3.outputs[0]
        # cor ponderada
        wc = N(nt, 'ShaderNodeCombineXYZ', 220, y0 - 60)
        nt.links.new(weight, wc.inputs[0])
        nt.links.new(weight, wc.inputs[1])
        nt.links.new(weight, wc.inputs[2])
        mulc = N(nt, 'ShaderNodeVectorMath', 380, y0 - 60, operation='MULTIPLY')
        nt.links.new(tex.outputs['Color'], mulc.inputs[0])
        nt.links.new(wc.outputs[0], mulc.inputs[1])
        if sum_rgb is None:
            sum_rgb = mulc.outputs[0]
            sum_w = weight
        else:
            add_rgb = N(nt, 'ShaderNodeVectorMath', 700 + i * 40, 200, operation='ADD')
            nt.links.new(sum_rgb, add_rgb.inputs[0])
            nt.links.new(mulc.outputs[0], add_rgb.inputs[1])
            sum_rgb = add_rgb.outputs[0]
            add_w = N(nt, 'ShaderNodeMath', 700 + i * 40, 100, operation='ADD')
            nt.links.new(sum_w, add_w.inputs[0])
            nt.links.new(weight, add_w.inputs[1])
            sum_w = add_w.outputs[0]
    # normalizacao + fallback
    maxw = math1(nt, 'MAXIMUM', sum_w, 0.001, 900, 100)
    inv = N(nt, 'ShaderNodeMath', 1020, 100, operation='DIVIDE')
    inv.inputs[0].default_value = 1.0
    nt.links.new(maxw, inv.inputs[1])
    col = N(nt, 'ShaderNodeVectorMath', 900, 220, operation='SCALE')
    nt.links.new(sum_rgb, col.inputs[0])
    nt.links.new(inv.outputs[0], col.inputs['Scale'])
    sel = math1(nt, 'GREATER_THAN', sum_w, 0.002, 1020, 220)
    mix = N(nt, 'ShaderNodeMixRGB', 1180, 220)
    mix.blend_type = 'MIX'
    nt.links.new(sel, mix.inputs[0])
    mix.inputs[1].default_value = (0.04, 0.04, 0.045, 1.0)
    nt.links.new(col.outputs[0], mix.inputs[2])
    emit = N(nt, 'ShaderNodeEmission', 1180, 60)
    nt.links.new(mix.outputs[0], emit.inputs[0])
    emit.inputs[1].default_value = 1.0
    nt.links.new(emit.outputs[0], out.inputs[0])
    # saida alternativa de cobertura (para o segundo bake)
    covc = math1(nt, 'MINIMUM', sum_w, 1.0, 900, -60)
    covrgb = N(nt, 'ShaderNodeCombineColor', 1020, -60)
    covrgb.mode = 'RGB'
    nt.links.new(covc, covrgb.inputs[0])
    nt.links.new(covc, covrgb.inputs[1])
    nt.links.new(covc, covrgb.inputs[2])
    return mat, emit, covrgb

def bake_emit(mat, img, clear=(0.0, 0.0, 0.0, 1.0)):
    nt = mat.node_tree
    tgt = None
    for nd in nt.nodes:
        if nd.type == 'TEX_IMAGE' and nd.image == img:
            tgt = nd
    if tgt is None:
        tgt = nt.nodes.new('ShaderNodeTexImage')
        tgt.image = img
        tgt.location = (600, -400)
    for nd in nt.nodes:
        nd.select = False
    tgt.select = True
    nt.nodes.active = tgt
    scene = bpy.context.scene
    scene.render.bake.margin = 6
    scene.render.bake.use_clear = True
    try:
        scene.render.bake.clear_color = clear
    except Exception as e:
        RES['avisos'].append('clear_color indisponivel: ' + str(e))
    bpy.ops.object.bake(type='EMIT')

t = time.time()
mat, emit_node, cov_node = build_paint_material()
obj.data.materials.clear()
obj.data.materials.append(mat)
bpy.context.view_layer.objects.active = obj
obj.select_set(True)
scene.cycles.samples = 4

img_cor = bpy.data.images.new('TEXTURA_BLENDER', TEX, TEX, alpha=False)
img_cor.filepath_raw = os.path.join(OUT, 'textura_blender.png')
img_cor.file_format = 'PNG'
bake_emit(mat, img_cor)
img_cor.save()
log('bake de cor concluido')
etapa('bake_cor', time.time() - t)

# cobertura: troca a emissao para o no de cobertura e bake de novo
t = time.time()
img_cov = bpy.data.images.new('COBERTURA', TEX, TEX, alpha=False)
img_cov.filepath_raw = os.path.join(OUT, 'cobertura_blender.png')
img_cov.file_format = 'PNG'
out_node = [nd for nd in mat.node_tree.nodes if nd.type == 'OUTPUT_MATERIAL'][0]
emit_cov = mat.node_tree.nodes.new('ShaderNodeEmission')
emit_cov.location = (1180, -160)
mat.node_tree.links.new(cov_node.outputs[0], emit_cov.inputs[0])
emit_cov.inputs[1].default_value = 1.0
mat.node_tree.links.new(emit_cov.outputs[0], out_node.inputs[0])
bake_emit(mat, img_cov)
img_cov.save()
# mascara de ilhas UV: emissao branca constante
img_msk = bpy.data.images.new('MASCARA_UV', TEX, TEX, alpha=False)
emit_cov.inputs[0].default_value = (1, 1, 1, 1)
# desliga o link da cobertura: valor default branco ja vale porque o link sera removido
for lk in list(emit_cov.inputs[0].links):
    mat.node_tree.links.remove(lk)
bake_emit(mat, img_msk)
wpx = np.empty(TEX * TEX * 4, dtype=np.float32)
img_msk.pixels.foreach_get(wpx)
mask = wpx.reshape(TEX, TEX, 4)[:, :, 0] > 0.5
cpx = np.empty(TEX * TEX * 4, dtype=np.float32)
img_cov.pixels.foreach_get(cpx)
cov = cpx.reshape(TEX, TEX, 4)[:, :, 0]
cob = float(((cov > 0.05) & mask).sum()) / float(mask.sum()) if mask.sum() else 0.0
RES['cobertura_direta_pct'] = round(cob * 100, 2)
RES['texels_uv_pct'] = round(float(mask.mean()) * 100, 2)
log('cobertura direta da projecao: %.2f%% dos texels UV' % (cob * 100))
etapa('bake_cobertura', time.time() - t)

# ------------------------------------------------- material final + export
t = time.time()
matf = bpy.data.materials.new('PinturaBlender')
matf.use_nodes = True
ntf = matf.node_tree
bsdf = ntf.nodes.get('Principled BSDF')
bsdf.inputs['Roughness'].default_value = 0.9
texn = ntf.nodes.new('ShaderNodeTexImage')
texn.image = img_cor
texn.location = (-300, 200)
ntf.links.new(texn.outputs['Color'], bsdf.inputs['Base Color'])
obj.data.materials.clear()
obj.data.materials.append(matf)
img_cor.pack()
glb_out = os.path.join(OUT, 'orc_blender_colorido.glb')
bpy.ops.export_scene.gltf(filepath=glb_out, export_format='GLB')
RES['glb_blender_bytes'] = os.path.getsize(glb_out)
log('GLB exportado: %d bytes' % RES['glb_blender_bytes'])
etapa('export_glb', time.time() - t)

RES['tempo_total_s'] = round(time.time() - T0, 2)
RES['textura_px'] = TEX
with open(os.path.join(OUT, 'resultado_blender.json'), 'w') as f:
    json.dump(RES, f, indent=1, ensure_ascii=False)
log('FIM pintar_blender - total %.1fs' % (time.time() - T0))
