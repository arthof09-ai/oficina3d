"""Blender headless: reabre o GLB final, renderiza prévias e máscaras de silhueta.

Uso (chamado por oficina3d.refino.previa.rodar_blender):
    blender -b --factory-startup --python-exit-code 3 -P _blender_previa.py -- pedido.json

pedido.json:
    glb, resultado, pasta_saida, pasta_trabalho,
    previas: ["frente", ...]           -> pasta_saida/previa_<vista>.png (Workbench, fundo cinza-escuro)
    mascaras: ["esquerda", ...]        -> pasta_trabalho/mascara_modelo_<vista>.pbm
    imagens: [{"vista", "arquivo"}]    -> pasta_trabalho/mascara_imagem_<vista>.pbm (alfa > limiar)
    limiar_alfa, tam_mascara, previa_px: [largura, altura]

Reabrir o GLB aqui é de propósito: confere que o arquivo entregue abre e mede de novo
triângulos, caixa e se é fechado (critério de aceite da v1: "reabre no Blender").
Câmeras ortográficas; ângulos documentados em previa.py (esquerda = câmera em +X).
"""
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

import bmesh
import bpy
import numpy as np
from mathutils import Vector

ANGULOS = {
    "frente": 0, "frente-esquerda": 45, "esquerda": 90, "costas-esquerda": 135,
    "costas": 180, "costas-direita": 225, "direita": 270, "frente-direita": 315,
}


def progresso(pct, msg):
    print(f"PROGRESSO {int(pct)} {msg}", flush=True)


def ler_pedido():
    args = sys.argv[sys.argv.index("--") + 1:]
    with open(args[0], encoding="utf-8") as f:
        return json.load(f)


def reabrir(glb):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    malhas = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not malhas:
        raise ValueError("o GLB reaberto não tem malha")
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


def medir(obj):
    me = obj.data
    n = len(me.vertices)
    co = np.empty(n * 3, dtype=np.float64)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    lo, hi = co.min(axis=0), co.max(axis=0)
    diag = float(np.linalg.norm(hi - lo)) or 1.0
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=diag * 1e-6)
    abertas = sum(1 for e in bm.edges if len(e.link_faces) == 1)
    nao_manifold = sum(1 for e in bm.edges if len(e.link_faces) > 2)
    bm.free()
    return {
        "triangulos": sum(len(p.vertices) - 2 for p in me.polygons),
        "vertices": n,
        "fechada": abertas == 0 and nao_manifold == 0 and len(me.polygons) > 0,
        "arestas_abertas": abertas, "arestas_nao_manifold": nao_manifold,
        "min_blender": [round(float(v), 6) for v in lo],
        "max_blender": [round(float(v), 6) for v in hi],
        "tem_uv": bool(me.uv_layers),
    }, lo, hi


def preparar_camera(cena):
    dados = bpy.data.cameras.new("cam")
    dados.type = "ORTHO"
    cam = bpy.data.objects.new("cam", dados)
    cena.collection.objects.link(cam)
    cena.camera = cam
    return cam


def apontar(cam, vista, centro, raio):
    if vista == "cima":
        cam.location = Vector((centro.x, centro.y, centro.z + raio))
        cam.rotation_euler = (0.0, 0.0, 0.0)  # olha −Z; alto da imagem = +Y (costas)
        return
    a = math.radians(ANGULOS[vista])
    d = Vector((math.sin(a), -math.cos(a), 0.0))
    cam.location = centro + d * raio
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()


def ajustar_formato(cena, modo):
    s = cena.render.image_settings
    try:
        s.file_format = "PNG"
    except Exception:  # noqa: BLE001
        pass
    try:
        s.color_mode = modo
    except Exception:  # noqa: BLE001
        pass


def mascara_de_imagem(caminho, limiar):
    """Máscara (numpy bool, linha 0 = topo) a partir do alfa; sem alfa, pelo fundo."""
    img = bpy.data.images.load(caminho, check_existing=False)
    try:
        w, h = img.size
        if w == 0 or h == 0:
            raise ValueError(f"imagem vazia ou ilegível: {caminho}")
        canais = img.channels
        px = np.empty(w * h * canais, dtype=np.float32)
        img.pixels.foreach_get(px)
        px = px.reshape(h, w, canais)[::-1]  # Blender guarda de baixo para cima
        if canais == 4 and float(px[..., 3].min()) < 0.999:
            m = px[..., 3] * 255.0 > limiar
            origem = "alfa"
        else:
            # Sem transparência: fundo = cor mediana das bordas; objeto = o que difere.
            rgb = px[..., :3]
            borda = np.concatenate([rgb[0], rgb[-1], rgb[:, 0], rgb[:, -1]])
            fundo = np.median(borda, axis=0)
            m = np.abs(rgb - fundo).max(axis=2) * 255.0 > 40
            origem = "fundo"
        return m, origem
    finally:
        bpy.data.images.remove(img)


def salvar_pbm(m, caminho):
    h, w = m.shape
    dados = np.packbits(m.astype(np.uint8), axis=1)
    with open(caminho, "wb") as f:
        f.write(f"P4\n{w} {h}\n".encode("ascii"))
        f.write(dados.tobytes())


def main():
    pedido = ler_pedido()
    res = {"ok": False, "previas": [], "mascaras_modelo": {}, "mascaras_imagem": {}, "avisos": []}
    try:
        t0 = time.perf_counter()
        progresso(5, "Blender: reabrindo o GLB")
        obj = reabrir(pedido["glb"])
        res["reaberto"], lo, hi = medir(obj)
        centro = Vector(((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2))
        dim = Vector((hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))
        maior = max(dim) or 1.0
        raio = maior * 3

        cena = bpy.context.scene
        cena.render.engine = "BLENDER_WORKBENCH"
        try:
            cena.view_settings.view_transform = "Standard"
        except Exception:  # noqa: BLE001
            pass
        cena.world = bpy.data.worlds.new("fundo")
        cena.world.color = (0.2, 0.2, 0.22)
        cam = preparar_camera(cena)
        cam.data.clip_start = maior * 0.01
        cam.data.clip_end = raio * 4
        obj.data.materials.clear()

        # --- prévias ---
        largura, altura = pedido.get("previa_px", [640, 800])
        cena.render.resolution_x, cena.render.resolution_y = int(largura), int(altura)
        cena.render.resolution_percentage = 100
        cena.render.film_transparent = False
        cena.display.shading.light = "STUDIO"
        cena.display.shading.color_type = "SINGLE"
        cena.display.shading.single_color = (0.72, 0.7, 0.66)
        cena.display.shading.show_cavity = True
        ajustar_formato(cena, "RGB")
        previas = list(pedido.get("previas", []))
        for i, vista in enumerate(previas):
            apontar(cam, vista, centro, raio)
            horiz = math.hypot(dim.x, dim.y)  # pior caso entre as vistas giradas
            # ortho_scale cobre o maior lado do quadro (aqui, a altura).
            escala_v = dim.z
            escala_h = horiz * (altura / largura)
            cam.data.ortho_scale = max(escala_v, escala_h) * 1.1
            caminho = os.path.join(pedido["pasta_saida"], f"previa_{vista}.png")
            cena.render.filepath = caminho
            bpy.ops.render.render(write_still=True)
            res["previas"].append(caminho)
            progresso(10 + 50 * (i + 1) // max(1, len(previas)), f"Blender: prévia {vista}")

        # --- máscaras do modelo ---
        lado = int(pedido.get("tam_mascara", 512))
        cena.render.resolution_x = cena.render.resolution_y = lado
        cena.render.film_transparent = True
        cena.display.shading.light = "FLAT"
        cena.display.shading.color_type = "SINGLE"
        cena.display.shading.single_color = (1.0, 1.0, 1.0)
        cena.display.shading.show_cavity = False
        try:
            cena.display.render_aa = "OFF"
        except Exception:  # noqa: BLE001
            pass
        ajustar_formato(cena, "RGBA")
        cam.data.ortho_scale = maior * 1.15
        mascaras = list(pedido.get("mascaras", []))
        limiar = float(pedido.get("limiar_alfa", 10))
        for i, vista in enumerate(mascaras):
            apontar(cam, vista, centro, raio)
            png = os.path.join(pedido["pasta_trabalho"], f"render_mascara_{vista}.png")
            cena.render.filepath = png
            bpy.ops.render.render(write_still=True)
            m, _ = mascara_de_imagem(png, limiar)
            pbm = os.path.join(pedido["pasta_trabalho"], f"mascara_modelo_{vista}.pbm")
            salvar_pbm(m, pbm)
            res["mascaras_modelo"][vista] = pbm
            progresso(60 + 25 * (i + 1) // max(1, len(mascaras)), f"Blender: máscara {vista}")

        # --- máscaras das imagens de entrada ---
        for item in pedido.get("imagens", []):
            vista, arq = item["vista"], item["arquivo"]
            try:
                m, origem = mascara_de_imagem(arq, limiar)
            except Exception as e:  # noqa: BLE001
                res["avisos"].append(f"não consegui ler a imagem da vista {vista}: {e}")
                continue
            if origem != "alfa":
                res["avisos"].append(f"imagem da vista {vista} sem transparência: fundo estimado pelas bordas")
            pbm = os.path.join(pedido["pasta_trabalho"], f"mascara_imagem_{vista}.pbm")
            salvar_pbm(m, pbm)
            res["mascaras_imagem"][vista] = pbm
        progresso(100, "Blender: prévias e máscaras prontas")
        res["tempo_s"] = round(time.perf_counter() - t0, 2)
        res["ok"] = True
    except Exception as e:  # noqa: BLE001
        res["erro"] = f"{type(e).__name__}: {e}"
        res["traceback"] = traceback.format_exc()
        print(res["traceback"], flush=True)
    with open(pedido["resultado"], "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    if not res["ok"]:
        sys.exit(3)


main()
