"""T5 - UV de qualidade com xatlas (lado .venv_app, sem Blender).

O Smart UV do refino fragmenta a malha em ~8 mil ilhas que ocupam 4,3% do
quadrado UV (~0,9 texel/face em 1024 px): o bake do T1 sai em "confete".
O xatlas parametriza a mesma malha com ocupacao ~61% e distorcao menor
que o Smart UV (medido no Orc Prata, 49.750 tris - ver REGISTRO T5).

Fluxo: ``gerar_uv`` le o GLB refinado com trimesh, parametriza com
xatlas e grava um .npz (vmapping, indices, uvs). O script Blender
``cor/_blender_uv_xatlas.py`` aplica esse .npz como UV por loop e
exporta o GLB com a UV nova - o bake do T1 le esse GLB sem mudanca.

O .npz e o contrato entre os dois lados: vmapping mapeia cada vertice
novo para o vertice original, indices (nfaces x 3) apontam para uvs, e
uvs tem um par por vertice novo (costuras duplicam vertices, como deve
ser). A ordem das faces e preservada pelo xatlas, e o script Blender
verifica isso medindo as metricas de UV no GLB exportado.
Nota de flip V (S3, Critico T5): o round-trip glTF inverte V
(v_glb = 1 - v_npz, medido com erro maximo 2,98e-08); quem comparar UVs
do GLB exportado com este .npz fora do Blender tem de aplicar o flip.
Dentro do Blender o bake usa as loop UVs lidas do GLB importado, logo
o flip nao afeta o bake; a correspondencia e por face/loop, nunca por
vertice (o Blender muda a contagem de vertices ao importar/exportar).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np


def carregar_malha_glb(caminho: str | Path) -> tuple[np.ndarray, np.ndarray]:
    """(vertices, faces) do GLB; exige malha unica (o caso do GLB refinado)."""
    import trimesh

    cena = trimesh.load(str(caminho), force="mesh")
    if hasattr(cena, "geometry"):
        geometrias = list(cena.geometry.values())
        if len(geometrias) != 1:
            raise ValueError(f"GLB com {len(geometrias)} geometrias; esperado 1")
        malha = geometrias[0]
    else:
        malha = cena
    return np.asarray(malha.vertices, dtype=np.float64), np.asarray(malha.faces, dtype=int)


def parametrizar(vertices: np.ndarray, faces: np.ndarray):
    """(vmapping, indices, uvs) do xatlas, na ordem das faces de entrada."""
    import xatlas

    vmapping, indices, uvs = xatlas.parametrize(vertices, faces)
    return (np.asarray(vmapping), np.asarray(indices).reshape(-1, 3),
            np.asarray(uvs, dtype=np.float64))


def metricas(faces_uv: np.ndarray, areas_3d: np.ndarray) -> dict:
    """As metricas do T1 (projecao.metricas_uv em 512 px) + extras em 1024."""
    from oficina3d.cor import projecao as P

    met = P.metricas_uv(faces_uv, areas_3d, 512)
    auv = np.abs((faces_uv[:, 1, 0] - faces_uv[:, 0, 0]) * (faces_uv[:, 2, 1] - faces_uv[:, 0, 1])
                 - (faces_uv[:, 2, 0] - faces_uv[:, 0, 0]) * (faces_uv[:, 1, 1] - faces_uv[:, 0, 1])) * 0.5
    texel_face = auv * 1024.0 * 1024.0
    met["uv_area_total"] = round(float(auv.sum()), 5)
    met["uv_bbox"] = [round(float(faces_uv[..., 0].min()), 4), round(float(faces_uv[..., 0].max()), 4),
                      round(float(faces_uv[..., 1].min()), 4), round(float(faces_uv[..., 1].max()), 4)]
    met["texels_por_face_media_1024"] = round(float(texel_face.mean()), 3)
    met["faces_com_menos_de_1_texel_pct"] = round(100.0 * float((texel_face < 1.0).mean()), 2)
    met["triangulos"] = int(len(faces_uv))
    return met


def gerar_uv(caminho_glb: str | Path, caminho_npz: str | Path) -> dict:
    """Parametriza o GLB e grava o .npz; devolve metricas + contagens."""
    t0 = time.perf_counter()
    verts, faces = carregar_malha_glb(caminho_glb)
    vmapping, indices, uvs = parametrizar(verts, faces)
    faces_uv = uvs[indices]
    a, b, c = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
    areas = np.linalg.norm(np.cross(b - a, c - a), axis=1) * 0.5
    met = metricas(faces_uv, areas)
    met["tempo_s"] = round(time.perf_counter() - t0, 2)
    met["vertices_originais"] = int(len(verts))
    met["vertices_com_costura"] = int(len(uvs))
    Path(caminho_npz).parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(caminho_npz, vmapping=vmapping.astype(np.int64),
                        indices=indices.astype(np.int64), uvs=uvs.astype(np.float32))
    return met


if __name__ == "__main__":
    import sys

    glb, npz = sys.argv[1], sys.argv[2]
    res = gerar_uv(glb, npz)
    print(json.dumps(res, indent=1))
    if len(sys.argv) > 3:
        Path(sys.argv[3]).write_text(json.dumps(res, indent=1), encoding="utf-8")
