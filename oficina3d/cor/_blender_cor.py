"""Blender headless: Etapa COR (T1) - projecao das vistas canonicas com bake.

Uso (chamado por oficina3d.cor.rodar_cor, mesmo padrao do refino):
    blender -b --factory-startup --python-exit-code 3 -P _blender_cor.py -- pedido.json

pedido.json:
    modo: "glb" | "sintetico"
    glb: caminho do GLB refinado (modo "glb")
    vistas: [{"vista", "arquivo"}]  (modo "glb"; ex.: frente/costas/esquerda/direita)
    saida_glb, saida_textura, resultado, pasta_previas,
    tamanho (px da textura, padrao 1024), dilatacao (passes max, padrao 256),
    previas: ["frente", "direita", ...] (render Workbench com textura)

Modo "sintetico": cubo com Smart UV + 4 vistas de cor solida (frente=vermelho,
costas=azul, esquerda=verde, direita=amarelo). Prova o mecanismo (bateria T1
item 7): cada face lateral tem de sair com a cor exata da sua vista no polo.

Saida: GLB com material Principled + textura de albedo embutida, textura PNG,
previas com textura (Workbench, cor TEXTURE) e resultado JSON com metricas:
UV (distorcao, ocupacao, ilhas, margem), por vista (IoU de silhueta, faces
visiveis, texels), cobertura total, zonas cegas e percentual por dilatacao.
Imprime "PROGRESSO <pct> <msg>".
"""
import hashlib
import json
import math
import os
import struct
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

ANGULOS = P.ANGULOS
CORES_SINTETICO = {"frente": (1.0, 0.0, 0.0), "costas": (0.0, 0.0, 1.0),
                   "esquerda": (0.0, 1.0, 0.0), "direita": (1.0, 1.0, 0.0)}


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


def criar_cubo():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.mesh.primitive_cube_add(size=2.0, location=(0.0, 0.0, 1.0))
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.003)
    bpy.ops.object.mode_set(mode="OBJECT")
    # Sem o apply, os vertices lidos de me.vertices ficam em coords locais
    # (cubo centrado em z=0) enquanto o BVH trabalha em coords de mundo
    # (z=1): o teste de oclusao e o enquadramento sairiam deslocados.
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    return obj


def uv_garantida(obj):
    """Devolve (uv_layer, gerada_aqui). Sem UV, gera Smart UV (mesmos parametros do refino).

    A etapa COR nao pode depender de o GLB de entrada ja ter UV: o caminho
    pymeshlab do refino (limpa.glb) nao gera UV; so a saida do Blender tem.
    Gerar aqui mantem o bake autocontido e e reportado no resultado.
    """
    me = obj.data
    if me.uv_layers.active is not None:
        return me.uv_layers.active, False
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.003)
    bpy.ops.object.mode_set(mode="OBJECT")
    return me.uv_layers.active, True


def extrair_malha(obj):
    """(verts, faces, normais_vert, faces_uv, areas_3d, normais_face, tri_poli, uv_gerada)."""
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
    uv_layer, uv_gerada = uv_garantida(obj)
    faces, faces_uv, areas, normais_face, tri_poli = [], [], [], [], []
    for pi, poly in enumerate(me.polygons):
        idx = list(poly.loop_indices)
        if len(idx) < 3:
            continue
        for k in range(1, len(idx) - 1):
            tri = [poly.vertices[0], poly.vertices[k], poly.vertices[k + 1]]
            uvs = [uv_layer.data[li].uv for li in (idx[0], idx[k], idx[k + 1])]
            faces.append(tri)
            faces_uv.append([(u[0], u[1]) for u in uvs])
            a, b, c = verts[tri[0]], verts[tri[1]], verts[tri[2]]
            areas.append(float(np.linalg.norm(np.cross(b - a, c - a)) * 0.5))
            normais_face.append(tuple(poly.normal))
            tri_poli.append(pi)
    return (verts, np.array(faces, dtype=int), normais,
            np.array(faces_uv, dtype=np.float64), np.array(areas, dtype=np.float64),
            np.array(normais_face, dtype=np.float64), np.array(tri_poli, dtype=int),
            uv_gerada)


def ler_imagem(caminho, limiar_alfa=10.0):
    """(rgb HxWx3 float 0..1 linha 0 = topo, mascara HxW bool, origem)."""
    img = bpy.data.images.load(caminho, check_existing=False)
    try:
        w, h = img.size
        if w == 0 or h == 0:
            raise ValueError(f"imagem vazia ou ilegiven: {caminho}")
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
        return px[..., :3].astype(np.float64), masc, origem
    finally:
        bpy.data.images.remove(img)


def iou_malha_vs_arte(verts, faces, centro, vista, ortho_scale, mascara_arte):
    """IoU@256 entre a silhueta da malha e a da arte, APOS o alinhamento v1.

    A malha e projetada, sua mascara e deformada pela mesma afinidade
    (caixa-da-mascara-da-arte sobre caixa-da-mascara-da-malha) usada no bake,
    e o IoU e medido contra a mascara da arte reduzida para 256 px. Mede o
    acordo de silhueta que o bake realmente enxerga, nao o enquadramento cru.
    """
    hi, wi = mascara_arte.shape
    out_w = 256
    out_h = max(8, int(round(256 * hi / wi)))
    px, py = P.projetar(verts, centro, vista, ortho_scale, out_w, out_h)
    pts = np.stack([px, py], axis=1)
    masc_malha = P.rasterizar_mascara_2d(pts, faces, out_w, out_h)
    iy = np.linspace(0, hi - 1, out_h).astype(int)
    ix = np.linspace(0, wi - 1, out_w).astype(int)
    masc_arte = mascara_arte[np.ix_(iy, ix)]
    bbox_m = P.bbox_mascara(masc_malha)
    bbox_a = P.bbox_mascara(masc_arte)
    if bbox_m is None or bbox_a is None:
        return 0.0
    ax, bx, ay, by = P.alinhamento_silhueta(bbox_a, bbox_m)
    xs, ys = np.meshgrid(np.arange(out_w), np.arange(out_h))
    mx = ((xs - bx) / ax).astype(int)
    my = ((ys - by) / ay).astype(int)
    dentro = (mx >= 0) & (mx < out_w) & (my >= 0) & (my < out_h)
    alinhada = np.zeros((out_h, out_w), dtype=bool)
    alinhada[dentro] = masc_malha[my[dentro], mx[dentro]]
    return P.iou(alinhada, masc_arte)


def verificar_glb_texturizado(caminho):
    """Confere no JSON do GLB: imagens embutidas + textura no material."""
    with open(caminho, "rb") as f:
        cab = f.read(12)
        magico, versao, _total = struct.unpack("<III", cab)
        if magico != 0x46546C67:
            raise ValueError("saida nao e GLB")
        tam, tipo = struct.unpack("<II", f.read(8))
        if tipo != 0x4E4F534A:
            raise ValueError("GLB sem bloco JSON")
        g = json.loads(f.read(tam).decode("utf-8"))
    imagens = g.get("images", [])
    mats = g.get("materials", [])
    # Qualquer material com textura conta (antes: so materials[0] - D8).
    tem = any("baseColorTexture" in m.get("pbrMetallicRoughness", {}) for m in mats)
    return {"imagens_no_glb": len(imagens), "material_com_textura": bool(tem),
            "materiais": len(mats)}


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
    cena.world = bpy.data.worlds.new("fundo_cor")
    cena.world.color = (0.2, 0.2, 0.22)
    dados = bpy.data.cameras.new("cam_cor")
    dados.type = "ORTHO"
    cam = bpy.data.objects.new("cam_cor", dados)
    cena.collection.objects.link(cam)
    cena.camera = cam
    cam.data.clip_start = max(dim) * 0.01
    cam.data.clip_end = raio * 4
    largura, altura = 640, 800
    cena.render.resolution_x, cena.render.resolution_y = largura, altura
    cena.render.resolution_percentage = 100
    cena.render.film_transparent = False
    cena.display.shading.light = "STUDIO"
    cena.display.shading.color_type = "TEXTURE"
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
        tamanho = int(pedido.get("tamanho", 1024))
        # Dilatacao v1 = "cor vizinha mais proxima": passes bastantes para
        # preencher o interior das zonas cegas, nao so as costuras. Cada passe
        # e 1 px (numpy, barato); 256 cobre regioes cegas de ate ~256 px de
        # largura em textura 1024. O que restar sem cor apos o limite e
        # reportado em texels_uv_sem_cor_apos_dilatacao, nunca escondido.
        dilatacao = int(pedido.get("dilatacao", 256))
        os.makedirs(pedido["pasta_previas"], exist_ok=True)
        progresso(3, "Blender COR: preparando a malha")
        if pedido.get("modo") == "sintetico":
            obj = criar_cubo()
            entradas = [(nome, None) for nome in ("frente", "costas", "esquerda", "direita")]
        else:
            obj = importar_glb(pedido["glb"])
            entradas = [(v["vista"], v["arquivo"]) for v in pedido["vistas"]]
        verts, faces, normais, faces_uv, areas_3d, normais_face, tri_poli, uv_gerada = extrair_malha(obj)
        res["uv_gerada_no_bake"] = bool(uv_gerada)
        lo = verts.min(axis=0)
        hi = verts.max(axis=0)
        dim_v = Vector((hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))
        centro = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))
        dim = (float(dim_v.x), float(dim_v.y), float(dim_v.z))
        maior = max(dim) or 1.0
        raio = maior * 3
        ortho = P.enquadramento(dim, 1024, 1024)
        res.update(triangulos=int(len(faces)), vertices=int(len(verts)),
                   dimensoes_blender=[round(float(v), 5) for v in dim_v])

        progresso(10, "Blender COR: metricas de UV (T5)")
        met_uv = P.metricas_uv(faces_uv, areas_3d, 512)
        if met_uv["margem_min_px"] is not None:
            met_uv["margem_min_px"] = int(round(met_uv["margem_min_px"] * tamanho / 512))
        met_uv["medido_em_px"] = 512
        res["metricas_uv"] = met_uv

        # BVH para o teste de profundidade (oclusao).
        progresso(18, "Blender COR: construindo BVH para oclusao")
        deps = bpy.context.evaluated_depsgraph_get()
        bvh = BVHTree.FromObject(obj, deps)
        diag = float(np.linalg.norm(hi - lo)) or 1.0

        vistas_prontas = []
        por_vista = {}
        for vista, arquivo in entradas:
            progresso(25, f"Blender COR: vista {vista}")
            if arquivo is None:
                h = w = 256
                rgb = np.zeros((h, w, 3), dtype=np.float64)
                rgb[:] = CORES_SINTETICO[vista]
                masc = np.ones((h, w), dtype=bool)
                origem = "sintetico"
            else:
                rgb, masc, origem = ler_imagem(arquivo)
                h, w = masc.shape
            dcam = np.array(P.direcao_camera(vista), dtype=np.float64)
            facing_face = np.clip(normais_face @ dcam, 0.0, 1.0)
            visivel = np.zeros(len(faces), dtype=bool)
            for fi in range(len(faces)):
                if facing_face[fi] <= P.FACING_MIN:
                    continue
                tri = faces[fi]
                centroide = verts[tri].mean(axis=0)
                normal = normais_face[fi]
                origem_raio = Vector(tuple(centroide + normal * diag * 1e-4))
                dist_cam = float(np.linalg.norm((np.array(centro) + dcam * raio) - centroide))
                hit = bvh.ray_cast(origem_raio, Vector(tuple(dcam)), dist_cam)
                # Blender 5.2: sem acerto, ray_cast devolve (None, None, None, None),
                # nao None. Acerto alem da camera (ou sem distancia) nao oclui.
                if hit is None or hit[0] is None:
                    visivel[fi] = True
                elif hit[3] is not None and hit[3] >= dist_cam - diag * 1e-3:
                    visivel[fi] = True
            vistas_prontas.append({"vista": vista, "imagem": rgb, "mascara": masc,
                                   "visivel": visivel, "peso_face": facing_face})
            iou_v = iou_malha_vs_arte(verts, faces, np.array(centro), vista, ortho, masc)
            por_vista[vista] = {"origem_mascara": origem,
                                "faces_visiveis": int(visivel.sum()),
                                "faces_totais": int(len(faces)),
                                "iou_silhueta_256": round(float(iou_v), 4)}
            progresso(45, f"Blender COR: vista {vista} pronta ({int(visivel.sum())} faces visiveis)")

        progresso(55, "Blender COR: rasterizando a textura por projecao")
        tex, pintado, _melhor, info_bake = P.rasterizar_textura(
            verts, faces, normais, faces_uv, vistas_prontas, tamanho,
            np.array(centro), dim, ortho)
        # Cobertura: fracao da AREA UV pintada (texels dentro de triangulos UV).
        masc_uv = P.rasterizar_mascara_2d(
            P._uv_para_pixels(faces_uv, tamanho).reshape(-1, 2),
            P._faces_index(len(faces_uv)), tamanho, tamanho)
        area_uv_texels = int(masc_uv.sum())
        pintados_uv = int((pintado & masc_uv).sum())
        cegos_antes = area_uv_texels - pintados_uv
        progresso(75, "Blender COR: dilatando costuras e zonas cegas")
        tex, pintado_final, n_dilat = P.dilatar(tex, pintado, dilatacao)
        # Texels UV ainda sem cor apos a dilatacao (ilhas isoladas alem do alcance).
        sem_cor = int((masc_uv & ~pintado_final).sum())
        for vista in por_vista:
            por_vista[vista]["texels"] = int(info_bake["texels_por_vista"].get(vista, 0))
            por_vista[vista]["faces_pintadas"] = int(info_bake["faces_pintadas_por_vista"].get(vista, 0))
        res["por_vista"] = por_vista
        res["cobertura"] = {
            "texels_uv": area_uv_texels,
            "texels_pintados_direto": pintados_uv,
            "texels_cegos_antes_dilatacao": cegos_antes,
            "cegos_pct": round(100.0 * cegos_antes / max(1, area_uv_texels), 2),
            "texels_por_dilatacao": int(n_dilat),
            "texels_uv_sem_cor_apos_dilatacao": sem_cor,
        }

        # Checagem do sintetico: cor no centroide UV de cada face lateral.
        if pedido.get("modo") == "sintetico":
            sintetico = {}
            normais_poli = {}
            me = obj.data
            for pi, poly in enumerate(me.polygons):
                normais_poli[pi] = np.array(poly.normal)
            for nome_vista, esperada in CORES_SINTETICO.items():
                dcam = np.array(P.direcao_camera(nome_vista))
                amostras = []
                for fi in range(len(faces)):
                    nrm = normais_poli[int(tri_poli[fi])]
                    if float(nrm @ dcam) > 0.99:
                        cuv = faces_uv[fi].mean(axis=0)
                        tx = min(tamanho - 1, max(0, int(cuv[0] * tamanho)))
                        ty = min(tamanho - 1, max(0, int((1.0 - cuv[1]) * tamanho)))
                        amostras.append(tex[ty, tx])
                if amostras:
                    obtida = np.mean(amostras, axis=0)
                    sintetico[nome_vista] = {
                        "esperada": [round(float(v), 3) for v in esperada],
                        "obtida": [round(float(v), 3) for v in obtida],
                        "amostras": len(amostras),
                        "ok": bool(np.all(np.abs(obtida - np.array(esperada)) < 0.05)),
                    }
            res["sintetico"] = sintetico

        progresso(85, "Blender COR: escrevendo textura e GLB com material")
        rgba = np.zeros((tamanho, tamanho, 4), dtype=np.float32)
        rgba[..., :3] = tex[::-1].astype(np.float32)  # Blender: linha 0 = base
        rgba[..., 3] = 1.0
        img = bpy.data.images.new("cor", tamanho, tamanho, alpha=True)
        img.filepath_raw = pedido["saida_textura"]
        img.file_format = "PNG"
        img.pixels.foreach_set(rgba.ravel())
        img.save_render(pedido["saida_textura"])
        mat = bpy.data.materials.new("cor")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        no_tex = mat.node_tree.nodes.new("ShaderNodeTexImage")
        no_tex.image = img
        mat.node_tree.links.new(no_tex.outputs["Color"], bsdf.inputs["Base Color"])
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.export_scene.gltf(filepath=pedido["saida_glb"], export_format="GLB",
                                  use_selection=True, export_yup=True, export_apply=True,
                                  export_normals=True, export_texcoords=True,
                                  export_materials="EXPORT", export_animations=False)
        res["glb_verificacao"] = verificar_glb_texturizado(pedido["saida_glb"])
        res["sha256_textura"] = sha256_arquivo(pedido["saida_textura"])
        res["sha256_glb"] = sha256_arquivo(pedido["saida_glb"])
        res["tamanho_textura_px"] = tamanho

        progresso(93, "Blender COR: previas com textura")
        res["previas"] = renderizar_previas(
            obj, list(pedido.get("previas", ["frente", "direita", "esquerda", "costas"])),
            pedido["pasta_previas"], centro, dim_v, raio)
        res["tempo_s"] = round(time.perf_counter() - t0, 2)
        res["versao_blender"] = bpy.app.version_string
        res["ok"] = True
        progresso(100, "Blender COR: pronto")
    except Exception as e:  # noqa: BLE001
        res["erro"] = f"{type(e).__name__}: {e}"
        res["traceback"] = traceback.format_exc()
        print(res["traceback"], flush=True)
    with open(pedido["resultado"], "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    if not res["ok"]:
        sys.exit(3)


main()
