# Renders de previa identicos para os dois GLBs (Oficina x Blender)
# Angulos: frente, 3/4 (frente+direita elevada), costas. Eevee, mesma luz/camera.
import bpy, os, json, math
from mathutils import Vector

W = r'C:\Users\txcga\RPG_Local\Oficina3D\_cache\tmp\comparativo-blender'
OUT = os.path.join(W, 'saida', 'renders')
os.makedirs(OUT, exist_ok=True)
with open(os.path.join(W, 'saida', 'resultado_blender.json')) as f:
    RB = json.load(f)
ORIENT = RB['orientacao']  # vista -> direcao '+X'/'-X'/'+Y'/'-Y'
DIRS = {'+X': Vector((1, 0, 0)), '-X': Vector((-1, 0, 0)),
        '+Y': Vector((0, 1, 0)), '-Y': Vector((0, -1, 0))}

def log(msg):
    print('[REND] ' + msg, flush=True)

def import_join(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
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

def render_model(tag, glb_path):
    obj = import_join(glb_path)
    scene = bpy.context.scene
    bb = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    xs = [v.x for v in bb]; ys = [v.y for v in bb]; zs = [v.z for v in bb]
    center = Vector(((min(xs)+max(xs))/2, (min(ys)+max(ys))/2, (min(zs)+max(zs))/2))
    radius = max((v - center).length for v in bb)
    scene.render.engine = 'BLENDER_EEVEE'
    try:
        scene.eevee.taa_render_samples = 32
    except Exception:
        pass
    scene.render.resolution_x = 640
    scene.render.resolution_y = 640
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.film_transparent = False
    world = bpy.data.worlds.new('WMundo')
    world.use_nodes = True
    bg = world.node_tree.nodes['Background']
    bg.inputs[0].default_value = (0.10, 0.10, 0.11, 1.0)
    bg.inputs[1].default_value = 0.55
    scene.world = world
    def sun(name, rot, energy):
        d = bpy.data.lights.new(name, 'SUN')
        d.energy = energy
        d.angle = 0.6
        o = bpy.data.objects.new(name, d)
        scene.collection.objects.link(o)
        o.rotation_euler = rot
        return o
    sun('SolChave', (math.radians(50), 0, math.radians(35)), 3.2)
    sun('SolPreench', (math.radians(70), 0, math.radians(-120)), 1.1)
    cam_data = bpy.data.cameras.new('Cam')
    cam_data.sensor_fit = 'HORIZONTAL'
    cam_data.angle = math.radians(33.0)
    cam = bpy.data.objects.new('Cam', cam_data)
    scene.collection.objects.link(cam)
    scene.camera = cam
    dist = radius / math.tan(math.radians(33.0) / 2) * 1.10
    frente = DIRS[ORIENT['frente']]
    costas = DIRS[ORIENT['costas']]
    direita = DIRS[ORIENT['direita']]
    d34 = (frente + direita + Vector((0, 0, 0.55))).normalized()
    views = {
        'frente': (frente + Vector((0, 0, 0.22))).normalized(),
        '34': d34,
        'costas': (costas + Vector((0, 0, 0.22))).normalized(),
    }
    for vn, dv in views.items():
        cam.location = center + dv * dist
        d = center - cam.location
        cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        scene.render.filepath = os.path.join(OUT, tag + '_' + vn + '.png')
        bpy.ops.render.render(write_still=True)
        log(tag + ' ' + vn + ' ok')
    # limpa para o proximo modelo
    bpy.data.objects.remove(obj, do_unlink=True)

render_model('oficina', os.path.join(W, 'entrada', 'oficina_colorido.glb'))
render_model('blender', os.path.join(W, 'saida', 'orc_blender_colorido.glb'))
log('FIM renderizar')
