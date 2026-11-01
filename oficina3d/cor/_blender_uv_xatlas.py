"""Blender headless: T5 - aplicar a UV do xatlas (.npz) e exportar o GLB.

Uso:
    blender -b --factory-startup --python-exit-code 3 -P _blender_uv_xatlas.py -- pedido.json

pedido.json: {glb, npz, saida_glb, resultado}
O .npz vem de oficina3d.uv_xatlas.gerar_uv (vmapping, indices, uvs).
A UV e aplicada por loop: o poligono i do GLB importado corresponde a
face i do .npz (ordem preservada pelo xatlas e pela importacao glTF) e
o loop j do triangulo recebe uvs[indices[i, j]]. A metrica de UV medida
aqui no Blender tem de bater com a medida no .venv_app (ocupacao ~0,61
no Orc Prata); se nao bater, a correspondencia de ordem falhou e o
resultado sai com ok=False em vez de um GLB silenciosamente errado.
"""
import json
import math
import os
import sys
import time
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

import bpy
import numpy as np

APP = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if APP not in sys.path:
    sys.path.insert(0, APP)

from oficina3d.cor import projecao as P  # noqa: E402


def progresso(pct, msg):
    print(f"PROGRESSO {int(pct)} {msg}", flush=True)


def ler_pedido():
    args = sys.argv[sys.argv.index("--") + 1:]
    with open(args[0], encoding="utf-8") as f:
        return json.load(f)


def importar_glb(caminho):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=caminho)
    malhas = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not malhas:
        raise ValueError("GLB sem malha")
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
    me.update()
    uv_layer = me.uv_layers.active
    if uv_layer is None:
        raise ValueError("sem camada UV")
    n = len(me.vertices)
    co = np.empty(n * 3, dtype=np.float64)
    me.vertices.foreach_get("co", co)
    verts = co.reshape(-1, 3)
    faces_uv, areas = [], []
    for poly in me.polygons:
        idx = list(poly.loop_indices)
        if len(idx) != 3:
            raise ValueError(f"poligono nao triangulado: {len(idx)} loops")
        uvs = [uv_layer.data[li].uv for li in idx]
        faces_uv.append([(u[0], u[1]) for u in uvs])
        a, b, c = verts[poly.vertices[0]], verts[poly.vertices[1]], verts[poly.vertices[2]]
        areas.append(float(np.linalg.norm(np.cross(b - a, c - a)) * 0.5))
    faces_uv = np.array(faces_uv, dtype=np.float64)
    areas = np.array(areas, dtype=np.float64)
    met = P.metricas_uv(faces_uv, areas, 512)
    auv = np.abs((faces_uv[:, 1, 0] - faces_uv[:, 0, 0]) * (faces_uv[:, 2, 1] - faces_uv[:, 0, 1])
                 - (faces_uv[:, 2, 0] - faces_uv[:, 0, 0]) * (faces_uv[:, 1, 1] - faces_uv[:, 0, 1])) * 0.5
    texel_face = auv * 1024.0 * 1024.0
    met["uv_area_total"] = round(float(auv.sum()), 5)
    met["texels_por_face_media_1024"] = round(float(texel_face.mean()), 3)
    met["faces_com_menos_de_1_texel_pct"] = round(100.0 * float((texel_face < 1.0).mean()), 2)
    met["triangulos"] = int(len(faces_uv))
    return met


def main():
    pedido = ler_pedido()
    res = {"ok": False}
    t0 = time.perf_counter()
    try:
        progresso(5, "Blender T5: importando o GLB refinado")
        obj = importar_glb(pedido["glb"])
        me = obj.data
        dados = np.load(pedido["npz"])
        indices = dados["indices"].reshape(-1, 3)
        uvs = dados["uvs"]
        if len(me.polygons) != len(indices):
            raise ValueError(f"poligonos {len(me.polygons)} != faces xatlas {len(indices)}")
        for poly in me.polygons:
            if len(poly.vertices) != 3:
                raise ValueError("GLB de entrada nao triangulado")
        progresso(40, "Blender T5: aplicando a UV do xatlas por loop")
        if me.uv_layers.active is None:
            me.uv_layers.new(name="UVMap")
        uv_layer = me.uv_layers.active
        for pi, poly in enumerate(me.polygons):
            for k, li in enumerate(poly.loop_indices):
                u, v = uvs[indices[pi, k]]
                uv_layer.data[li].uv = (float(u), float(v))
        progresso(70, "Blender T5: medindo a UV aplicada")
        res["metricas_uv"] = medir(obj)
        progresso(85, "Blender T5: exportando o GLB com a UV nova")
        obj.data.materials.clear()
        bpy.ops.object.select_all(action="DESELECT")
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.export_scene.gltf(filepath=pedido["saida_glb"], export_format="GLB",
                                  use_selection=True, export_yup=True, export_apply=True,
                                  export_normals=True, export_texcoords=True,
                                  export_materials="NONE", export_animations=False)
        res["tempo_s"] = round(time.perf_counter() - t0, 2)
        res["versao_blender"] = bpy.app.version_string
        res["ok"] = True
        progresso(100, "Blender T5: pronto")
    except Exception as e:  # noqa: BLE001
        res["erro"] = f"{type(e).__name__}: {e}"
        res["traceback"] = traceback.format_exc()
        print(res["traceback"], flush=True)
    with open(pedido["resultado"], "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    if not res["ok"]:
        sys.exit(3)


main()
