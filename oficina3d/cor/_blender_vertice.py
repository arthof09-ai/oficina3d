"""Blender headless: Etapa COR (T2) - cor de vertice (rascunho/rede de
seguranca da Etapa COR; desenho em docs/DECISOES.md, COR-07).

Uso (chamado por oficina3d.cor.vertice.rodar_vertice, mesmo padrao do
bake T1): blender -b --factory-startup --python-exit-code 3 -P
_blender_vertice.py -- pedido.json

pedido.json:
    modo: "glb" | "sintetico"
    glb: caminho do GLB refinado (modo "glb")
    glb_forma: caminho do GLB da forma (opcional; so vem quando a forma
        tem COLOR_0 - ex.: TripoSR - e serve de fonte secundaria)
    vistas: [{"vista", "arquivo"}] (modo "glb"; pode ser lista vazia
        quando a unica fonte e a forma)
    saida_glb, pasta_previas, previas: ["frente", ...]

Fontes de cor, em prioridade estrita (matematica em
``oficina3d.cor.vertice``): (1) vistas canonicas por projecao sobre os
vertices (oclusao por BVH, facing minimo, alinhamento por silhueta -
o mesmo do T1); (2) cor da forma transferida pela superficie mais
proxima (com autochecagem de alinhamento D-T2-1: mediana + p90 das
distancias + razao por eixo das caixas; fora da regua, a fonte e
RECUSADA e o motivo fica no resultado); (3) propagacao pela malha. Vertice sem nenhuma fonte sai
preto e CONTADO em cobertura.sem_cor - nunca escondido.

Saida: GLB com COLOR_0 e material "cor" (Principled com no de cor de
vertice), SEM imagem/textura; a presenca de COLOR_0 no arquivo
exportado e verificada por parse do JSON do GLB - sem COLOR_0, o passo
FALHA (exit 3) em vez de entregar um modelo branco/preto em silencio.
Previas Workbench com cor de vertice (color_type VERTEX). Imprime
"PROGRESSO <pct> <msg>".
"""
import hashlib
import json
import math
import os
import sys
import time
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

import bpy
import numpy as np
from mathutils import Vector
from mathutils.bvhtree import BVHTree

# O script mora em app/oficina3d/cor/ -> app fica 2 niveis acima.
APP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if APP not in sys.path:
    sys.path.insert(0, APP)

from oficina3d.cor import projecao as P  # noqa: E402
from oficina3d.cor import vertice as V  # noqa: E402
from oficina3d.cor.validacao_vertice import verificar_glb_vertice  # noqa: E402

ANGULOS = P.ANGULOS
CORES_SINTETICO = {"frente": (1.0, 0.0, 0.0), "costas": (0.0, 0.0, 1.0),
                   "esquerda": (0.0, 1.0, 0.0), "direita": (1.0, 1.0, 0.0)}
LIMITE_FORMA_VERTS = 2_000_000
# Legado (COR-07): a decisao de aceite vive em V.avaliar_alinhamento_forma
# (D-T2-1); esta constante e so o limite antigo da mediana, mantida para
# nao quebrar import externo.
LIMITE_ALINHAMENTO_FRAC = 0.05


def progresso(pct, msg):
    print(f"PROGRESSO {int(pct)} {msg}", flush=True)


def ler_pedido():
    args = sys.argv[sys.argv.index("--") + 1:]
    with open(args[0], encoding="utf-8") as f:
        return json.load(f)


def sha256_arquivo(caminho):
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        for bloco in iter(lambda: f.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def importar_glb(caminho):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=caminho)
    malhas = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not malhas:
        raise ValueError("o GLB nao tem nenhuma malha")
    bpy.ops.object.select_all(action="DESELECT")
    for o in malhas:
        o.select_set(True)
    bpy.context.view_layer.objects.active = malhas[0]
    if len(malhas) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def importar_glb_adicional(caminho):
    """Importa um segundo GLB SEM resetar a cena; devolve o objeto unico."""
    antes = set(bpy.context.scene.objects)
    bpy.ops.import_scene.gltf(filepath=caminho)
    novos = [o for o in bpy.context.scene.objects if o not in antes and o.type == "MESH"]
    if not novos:
        raise ValueError("o GLB da forma nao tem nenhuma malha")
    bpy.ops.object.select_all(action="DESELECT")
    for o in novos:
        o.select_set(True)
    bpy.context.view_layer.objects.active = novos[0]
    if len(novos) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def criar_esfera():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, radius=1.0,
                                         location=(0.0, 0.0, 1.0))
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.shade_smooth()
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def extrair_malha(obj):
    """(verts, faces, normais_vert) - sem UV (cor de vertice nao usa UV)."""
    me = obj.data
    me.update()
    try:
        me.calc_normals()
    except Exception:  # noqa: BLE001
        pass
    n = len(me.vertices)
    co = np.empty(n * 3, dtype=np.float64)
    me.vertices.foreach_get("co", co)
    verts = co.reshape(-1, 3)
    nm = np.empty(n * 3, dtype=np.float64)
    me.vertices.foreach_get("normal", nm)
    normais = nm.reshape(-1, 3)
    faces = []
    for poly in me.polygons:
        for k in range(1, len(poly.vertices) - 1):
            faces.append([poly.vertices[0], poly.vertices[k], poly.vertices[k + 1]])
    return verts, np.array(faces, dtype=int), normais


def ler_imagem(caminho, limiar_alfa=10.0):
    """(RGB linear HxWx3, mascara HxW bool, origem), linha 0 = topo.

    PNG/JPEG canonicos: bpy retorna os canais sRGB sem decodificar.
    Imagens float (ex.: EXR) ja fornecem luz linear. A mascara continua
    calculada nos pixels originais para preservar o contrato de fundo.
    """
    img = bpy.data.images.load(caminho, check_existing=False)
    try:
        w, h = img.size
        if w == 0 or h == 0:
            raise ValueError(f"imagem vazia ou ilegivel: {caminho}")
        canais = img.channels
        px = np.empty(w * h * canais, dtype=np.float32)
        img.pixels.foreach_get(px)
        px = px.reshape(h, w, canais)[::-1]
        if canais == 4 and float(px[..., 3].min()) < 0.999:
            masc = px[..., 3] * 255.0 > limiar_alfa
            origem = "alfa"
        else:
            rgb = px[..., :3]
            borda = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
            fundo = np.median(borda, axis=0)
            masc = np.abs(rgb - fundo).max(axis=2) * 255.0 > 40
            origem = "fundo"
        rgb = px[..., :3].astype(np.float64)
        if not img.is_float:
            rgb = V.srgb_para_linear(rgb)
        return rgb, masc, origem
    finally:
        bpy.data.images.remove(img)


def visibilidade_vertices(bvh, verts, normais, centro, vista, raio, diag):
    """(N,) bool: vertice enxergado pela camera da vista (BVH, mesmo
    criterio do bake T1 para as faces: origem deslocada pela normal,
    acerto alem da camera nao oclui)."""
    dcam = np.array(P.direcao_camera(vista), dtype=np.float64)
    nn = np.linalg.norm(normais, axis=1)
    facing = np.zeros(len(verts), dtype=np.float64)
    ok_n = nn > 0
    facing[ok_n] = (normais[ok_n] / nn[ok_n, None]) @ dcam
    cam = Vector(tuple(np.array(centro) + dcam * raio))
    dvec = Vector(tuple(dcam))
    vis = np.zeros(len(verts), dtype=bool)
    eps = diag * 1e-4
    tol = diag * 1e-3
    for vi in range(len(verts)):
        if facing[vi] <= P.FACING_MIN:
            continue
        v = verts[vi]
        origem = Vector(tuple(v + (normais[vi] / nn[vi]) * eps))
        dist_cam = float(np.linalg.norm(np.array(cam) - v))
        hit = bvh.ray_cast(origem, dvec, dist_cam)
        # Blender 5.2: sem acerto, ray_cast devolve (None, None, None, None).
        if hit is None or hit[0] is None:
            vis[vi] = True
        elif hit[3] is not None and hit[3] >= dist_cam - tol:
            vis[vi] = True
    return vis


def cores_da_forma(obj_forma):
    """(verts, faces, cores_por_vertice ou None) da malha da forma."""
    me = obj_forma.data
    me.update()
    n = len(me.vertices)
    co = np.empty(n * 3, dtype=np.float64)
    me.vertices.foreach_get("co", co)
    verts = co.reshape(-1, 3)
    faces = []
    for poly in me.polygons:
        for k in range(1, len(poly.vertices) - 1):
            faces.append([poly.vertices[0], poly.vertices[k], poly.vertices[k + 1]])
    faces = np.array(faces, dtype=int)
    if len(me.color_attributes) == 0:
        return verts, faces, None
    attr = me.color_attributes.active_color or me.color_attributes[0]
    if attr.domain == "POINT":
        arr = np.empty(n * 4, dtype=np.float32)
        attr.data.foreach_get("color", arr)
        return verts, faces, arr.reshape(-1, 4)[:, :3].astype(np.float64)
    # Dominio CORNER (por loop): media dos loops de cada vertice.
    n_loops = len(me.loops)
    arr = np.empty(n_loops * 4, dtype=np.float32)
    attr.data.foreach_get("color", arr)
    arr = arr.reshape(-1, 4)[:, :3].astype(np.float64)
    soma = np.zeros((n, 3), dtype=np.float64)
    conta = np.zeros(n, dtype=np.float64)
    donos = np.array([l.vertex_index for l in me.loops], dtype=int)
    np.add.at(soma, donos, arr)
    np.add.at(conta, donos, 1.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        cores = np.where(conta[:, None] > 0, soma / np.maximum(conta, 1.0)[:, None], 0.0)
    return verts, faces, cores


def transferir_forma(obj_forma, verts_ref, fonte, dim_ref):
    """Amostra a cor da forma nos vertices ainda sem fonte.

    Alinhamento: escala uniforme pela altura (a invariante do refino:
    altura = altura_m, pivo nos pes) + centros X/Y da caixa + base Z.
    Autochecagem (regra D-T2-1, em oficina3d.cor.vertice):
    mediana + p90 das distancias (amostra) entre vertices refinados e
    a superficie da forma alinhada + razao por eixo das caixas; fora
    da regua, a fonte e recusada. Retorna (cores_forma ou None, info).
    """
    fv, ff, fc = cores_da_forma(obj_forma)
    info = {"presente": fc is not None, "aceita": False}
    if fc is None:
        info["motivo"] = "forma sem COLOR_0 legivel no Blender"
        return None, info
    if len(fv) > LIMITE_FORMA_VERTS:
        info["motivo"] = f"forma com {len(fv)} vertices acima do limite {LIMITE_FORMA_VERTS}"
        return None, info
    lo_f, hi_f = fv.min(axis=0), fv.max(axis=0)
    lo_r, hi_r = verts_ref.min(axis=0), verts_ref.max(axis=0)
    alt_f = float(hi_f[2] - lo_f[2]) or 1.0
    alt_r = float(hi_r[2] - lo_r[2]) or 1.0
    s = alt_r / alt_f
    desl = np.array([(lo_r[0] + hi_r[0]) / 2 - s * (lo_f[0] + hi_f[0]) / 2,
                     (lo_r[1] + hi_r[1]) / 2 - s * (lo_f[1] + hi_f[1]) / 2,
                     lo_r[2] - s * lo_f[2]])
    fv_map = fv * s + desl
    bvh = BVHTree.FromPolygons([Vector(tuple(v)) for v in fv_map],
                               [tuple(int(i) for i in f) for f in ff])
    alvo = np.nonzero(fonte == V.FONTE_NENHUMA)[0]
    amostra = alvo[::max(1, len(alvo) // 1500)][:1500] if len(alvo) else \
        np.arange(0, len(verts_ref), max(1, len(verts_ref) // 1500))[:1500]
    dists = []
    for vi in amostra:
        hit = bvh.find_nearest(Vector(tuple(verts_ref[vi])))
        if hit is not None and hit[3] is not None:
            dists.append(float(hit[3]))
    ext_f = fv_map.max(axis=0) - fv_map.min(axis=0)
    ext_r = hi_r - lo_r
    razoes = {}
    for i, eixo in enumerate("xyz"):
        razoes[eixo] = float(ext_f[i] / ext_r[i]) if ext_r[i] else float("inf")
    dists_frac = [d / alt_r for d in dists]
    aceita, motivo, metricas = V.avaliar_alinhamento_forma(dists_frac, razoes)
    info.update(metricas)
    info["escala_aplicada"] = round(float(s), 5)
    info["regua_alinhamento"] = {
        "mediana_max_frac_altura": V.LIMITE_ALINHAMENTO_MEDIANA_FRAC,
        "p90_max_frac_altura": V.LIMITE_ALINHAMENTO_P90_FRAC,
        "razao_caixa_faixa": list(V.FAIXA_RAZAO_CAIXA)}
    if not aceita:
        info["motivo"] = motivo
        return None, info
    info["aceita"] = True
    cores_forma = np.zeros((len(verts_ref), 3), dtype=np.float64)
    for vi in alvo:
        hit = bvh.find_nearest(Vector(tuple(verts_ref[vi])))
        if hit is None or hit[0] is None or hit[2] is None:
            continue
        loc, _nrm, fi, _dist = hit
        tri = ff[int(fi)]
        w = V.baricentricas_3d(np.array(loc), fv_map[tri[0]], fv_map[tri[1]], fv_map[tri[2]])
        if w is None:
            continue
        cores_forma[vi] = w[0] * fc[tri[0]] + w[1] * fc[tri[1]] + w[2] * fc[tri[2]]
    return cores_forma, info


def apontar_camera(cam, vista, centro, raio):
    if vista == "cima":
        cam.location = Vector((centro.x, centro.y, centro.z + raio))
        cam.rotation_euler = (0.0, 0.0, 0.0)
        return
    a = math.radians(ANGULOS[vista])
    d = Vector((math.sin(a), -math.cos(a), 0.0))
    cam.location = centro + d * raio
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()


def renderizar_previas(obj, vistas, pasta, centro, dim, raio):
    cena = bpy.context.scene
    cena.render.engine = "BLENDER_WORKBENCH"
    try:
        cena.view_settings.view_transform = "Standard"
    except Exception:  # noqa: BLE001
        pass
    cena.world = bpy.data.worlds.new("fundo_vertice")
    cena.world.color = (0.2, 0.2, 0.22)
    dados = bpy.data.cameras.new("cam_vertice")
    dados.type = "ORTHO"
    cam = bpy.data.objects.new("cam_vertice", dados)
    cena.collection.objects.link(cam)
    cena.camera = cam
    cam.data.clip_start = max(dim) * 0.01
    cam.data.clip_end = raio * 4
    largura, altura = 640, 800
    cena.render.resolution_x, cena.render.resolution_y = largura, altura
    cena.render.resolution_percentage = 100
    cena.render.film_transparent = False
    cena.display.shading.light = "STUDIO"
    try:
        cena.display.shading.color_type = "VERTEX"
    except Exception:  # noqa: BLE001 - Workbench sem VERTEX nesta versao
        cena.display.shading.color_type = "MATERIAL"
    try:
        cena.display.shading.show_cavity = False
    except Exception:  # noqa: BLE001
        pass
    try:
        cena.render.image_settings.file_format = "PNG"
        cena.render.image_settings.color_mode = "RGB"
    except Exception:  # noqa: BLE001
        pass
    saidas = []
    for vista in vistas:
        apontar_camera(cam, vista, centro, raio)
        horiz = math.hypot(dim.x, dim.y)
        cam.data.ortho_scale = max(dim.z, horiz * (altura / largura)) * 1.1
        caminho = os.path.join(pasta, f"previa_cor_{vista}.png")
        cena.render.filepath = caminho
        bpy.ops.render.render(write_still=True)
        saidas.append(caminho)
    return saidas


def main():
    pedido = ler_pedido()
    res = {"ok": False}
    t0 = time.perf_counter()
    try:
        os.makedirs(pedido["pasta_previas"], exist_ok=True)
        progresso(3, "Blender VERTICE: preparando a malha")
        sintetico = pedido.get("modo") == "sintetico"
        if sintetico:
            obj = criar_esfera()
            entradas = [(nome, None) for nome in ("frente", "costas", "esquerda", "direita")]
        else:
            obj = importar_glb(pedido["glb"])
            entradas = [(v["vista"], v["arquivo"]) for v in pedido.get("vistas") or []]
        verts, faces, normais = extrair_malha(obj)
        lo = verts.min(axis=0)
        hi = verts.max(axis=0)
        dim_v = Vector((hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))
        centro = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))
        dim = (float(dim_v.x), float(dim_v.y), float(dim_v.z))
        maior = max(dim) or 1.0
        raio = maior * 3
        ortho = P.enquadramento(dim, 1024, 1024)
        diag = float(np.linalg.norm(hi - lo)) or 1.0
        res.update(triangulos=int(len(faces)), vertices=int(len(verts)),
                   dimensoes_blender=[round(float(v), 5) for v in dim_v])

        progresso(18, "Blender VERTICE: construindo BVH para oclusao")
        deps = bpy.context.evaluated_depsgraph_get()
        bvh = BVHTree.FromObject(obj, deps)

        vistas_prontas = []
        por_vista = {}
        for vista, arquivo in entradas:
            progresso(25, f"Blender VERTICE: vista {vista}")
            if arquivo is None:
                h = w = 256
                rgb = np.zeros((h, w, 3), dtype=np.float64)
                rgb[:] = CORES_SINTETICO[vista]
                masc = np.ones((h, w), dtype=bool)
                origem = "sintetico"
            else:
                rgb, masc, origem = ler_imagem(arquivo)
            vis = visibilidade_vertices(bvh, verts, normais, np.array(centro), vista, raio, diag)
            vistas_prontas.append({"vista": vista, "imagem": rgb, "mascara": masc, "visivel": vis})
            por_vista[vista] = {"origem_mascara": origem,
                                "vertices_visiveis": int(vis.sum())}
            progresso(45, f"Blender VERTICE: vista {vista} pronta ({int(vis.sum())} vertices visiveis)")

        progresso(55, "Blender VERTICE: amostrando as vistas nos vertices")
        cores, fonte, _melhor, info_amostra = V.amostrar_vertices(
            verts, normais, vistas_prontas, np.array(centro), ortho)
        for vista in por_vista:
            por_vista[vista]["vertices_pintados"] = int(
                info_amostra["vertices_por_vista"].get(vista, 0))
        res["por_vista"] = por_vista
        res["espaco_cor"] = {"atributo": "linear", "imagens_byte": "sRGB decodificado",
                             "imagens_float": "linear", "forma": "linear preservado"}

        # Fonte 2: cor da forma (TripoSR etc.), se o passo a declarou.
        info_forma = {"presente": False, "aceita": False}
        if pedido.get("glb_forma") and not sintetico:
            progresso(65, "Blender VERTICE: transferindo a cor da forma")
            obj_forma = importar_glb_adicional(pedido["glb_forma"])
            try:
                cores_forma, info_forma = transferir_forma(obj_forma, verts, fonte, dim)
            finally:
                bpy.data.objects.remove(obj_forma, do_unlink=True)
            if cores_forma is not None:
                n_forma = V.mesclar_forma(cores, fonte, cores_forma)
                info_forma["vertices_preenchidos"] = int(n_forma)
        res["forma_transferencia"] = info_forma

        progresso(75, "Blender VERTICE: propagando pelas arestas")
        n_prop, passes = V.preencher_por_vizinhos(cores, fonte, faces)
        res["propagacao"] = {"vertices": int(n_prop), "passes": int(passes)}
        res["cobertura"] = V.resumo_cobertura(fonte)
        if res["cobertura"]["por_fonte"]["vista"] + res["cobertura"]["por_fonte"]["forma"] == 0:
            raise RuntimeError("nenhuma fonte pintou vertice algum "
                               "(sem vista util e sem cor da forma)")

        # Checagem do sintetico (esfera): o vertice voltado para cada
        # camera (facing > 0,99) tem de sair com a cor exata da vista.
        if sintetico:
            check = {}
            unit = normais / np.maximum(np.linalg.norm(normais, axis=1, keepdims=True), 1e-12)
            for nome_vista, esperada in CORES_SINTETICO.items():
                dcam = np.array(P.direcao_camera(nome_vista))
                sel = np.nonzero((unit @ dcam) > 0.99)[0]
                if len(sel):
                    obtida = cores[sel].mean(axis=0)
                    check[nome_vista] = {
                        "esperada": [round(float(v), 3) for v in esperada],
                        "obtida": [round(float(v), 3) for v in obtida],
                        "amostras": int(len(sel)),
                        "ok": bool(np.all(np.abs(obtida - np.array(esperada)) < 0.05)),
                    }
                else:
                    check[nome_vista] = {"amostras": 0, "ok": False}
            res["sintetico"] = check

        progresso(85, "Blender VERTICE: escrevendo COLOR_0 e exportando")
        me = obj.data
        for attr in list(me.color_attributes):
            me.color_attributes.remove(attr)
        attr = me.color_attributes.new(name="Color", type="FLOAT_COLOR", domain="POINT")
        rgba = np.zeros((len(verts), 4), dtype=np.float32)
        rgba[:, :3] = cores.astype(np.float32)
        rgba[:, 3] = 1.0
        attr.data.foreach_set("color", rgba.ravel())
        for prop in ("active_color", "render_color"):
            try:
                setattr(me.color_attributes, prop, attr)
            except Exception:  # noqa: BLE001 - versao sem a propriedade
                pass
        mat = bpy.data.materials.new("cor")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        no_vc = mat.node_tree.nodes.new("ShaderNodeVertexColor")
        no_vc.layer_name = "Color"
        mat.node_tree.links.new(no_vc.outputs["Color"], bsdf.inputs["Base Color"])
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        export_kwargs = dict(filepath=pedido["saida_glb"], export_format="GLB",
                             use_selection=True, export_yup=True, export_apply=True,
                             export_normals=True, export_texcoords=True,
                             export_materials="EXPORT", export_animations=False)
        try:
            bpy.ops.export_scene.gltf(export_vertex_colors=True, **export_kwargs)
        except TypeError:
            bpy.ops.export_scene.gltf(**export_kwargs)
        verif = verificar_glb_vertice(pedido["saida_glb"])
        res["glb_verificacao"] = verif
        if not verif["ok"]:
            raise RuntimeError(f"GLB exportado sem COLOR_0 completo: {verif}")
        res["sha256_glb"] = sha256_arquivo(pedido["saida_glb"])

        progresso(93, "Blender VERTICE: previas com cor de vertice")
        res["previas"] = renderizar_previas(
            obj, list(pedido.get("previas", ["frente", "direita", "esquerda", "costas"])),
            pedido["pasta_previas"], centro, dim_v, raio)
        res["tempo_s"] = round(time.perf_counter() - t0, 2)
        res["versao_blender"] = bpy.app.version_string
        res["ok"] = True
        progresso(100, "Blender VERTICE: pronto")
    except Exception as e:  # noqa: BLE001
        res["erro"] = f"{type(e).__name__}: {e}"
        res["traceback"] = traceback.format_exc()
        print(res["traceback"], flush=True)
    with open(pedido["resultado"], "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    if not res["ok"]:
        sys.exit(3)


if __name__ == "__main__":
    main()
