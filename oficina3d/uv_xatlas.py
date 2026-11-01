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
(v_glb = 1 - v_npz, medido com erro maximo 2,98e-08); quem decodificar o modelo_uv.glb (UM round-trip) tem de aplicar
o flip para comparar com este .npz; quem decodificar o modelo_cor.glb
(DOIS round-trips: npz -> modelo_uv.glb -> modelo_cor.glb) NAO deve
aplicar o flip, porque ele se cancela - as UVs do modelo_cor.glb casam
com o .npz direto (maxdiff 2,98e-08, medido pelo Critico D-T5-1).
Dentro do Blender o bake usa as loop UVs lidas do GLB importado, logo
o flip nao afeta o bake; a correspondencia e por face/loop, nunca por
vertice (o Blender muda a contagem de vertices ao importar/exportar).

Gutter real (D-T5-1, Critico T5): o empacotamento usa padding real em
texels na resolucao dada, de modo que a menor faixa vazia entre ilhas
mede >= 8 px em 2048 (regua do Critico T5; o padrao anterior, padding 0,
media 1 px em 512 e em 1024 - abaixo da regua, com halo sob mipmapping).
Custo medido no Orc Prata (ver REGISTRO D-T5-1): com 6.578 ilhas, o
gutter de 8 px em 2048 encolhe as ilhas (ocupacao 0,614 -> 0,233,
12,94 -> 4,92 texels/face em 1024) - o empacotador reduz a escala para
caber o perimetro total com gutter. A margem medida no Orc com o padrao
novo e 9 px em 2048 (direto) e 4 px em 1024. O numero de ilhas nao muda
(o gutter nao funde nem divide ilhas) e a distorcao nao piora.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

# Padrao D-T5-1: gutter de 8 texels numa resolucao de 2048 -> faixa vazia
# minima >= 8 px em 2048 (medido: 9 px no Orc Prata). Mudar o padrao exige
# re-medir a margem no Orc e atualizar este comentario com os numeros.
PADDING_PX_PADRAO = 8
RESOLUCAO_PADRAO = 2048


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


def parametrizar(vertices: np.ndarray, faces: np.ndarray, padding_px: int = PADDING_PX_PADRAO,
                 resolucao: int = RESOLUCAO_PADRAO, max_cost: float = 2.0):
    """(vmapping, indices, uvs) do xatlas, na ordem das faces de entrada.

    Usa a API Atlas (bit a bit identica a conveniencia parametrize no
    Orc Prata - prova em jobs_teste/cor_margem/resultado_cmp.json) para
    poder fixar o padding do empacotamento. ``padding_px`` sao texels na
    ``resolucao`` dada; ``max_cost`` e o custo maximo de crescimento das
    ilhas (2.0 = padrao do xatlas, o mesmo da T5). Exige um unico atlas:
    o bake do T1 assume uma unica textura.
    """
    import xatlas

    atlas = xatlas.Atlas()
    atlas.add_mesh(np.asarray(vertices, dtype=np.float32),
                   np.asarray(faces, dtype=np.uint32))
    chart = xatlas.ChartOptions()
    chart.max_cost = max_cost
    pack = xatlas.PackOptions()
    pack.padding = padding_px
    pack.resolution = resolucao
    atlas.generate(chart, pack)
    if atlas.atlas_count != 1:
        raise ValueError(f"xatlas gerou {atlas.atlas_count} atlas; esperado 1")
    vmapping, indices, uvs = atlas.get_mesh(0)
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


def gerar_uv(caminho_glb: str | Path, caminho_npz: str | Path,
             padding_px: int = PADDING_PX_PADRAO, resolucao: int = RESOLUCAO_PADRAO,
             max_cost: float = 2.0, progresso=None) -> dict:
    """Parametriza o GLB e grava o .npz; devolve metricas + contagens.

    ``progresso`` (opcional) segue o contrato ``progresso(pct, msg)``
    com pct 0-100 dentro deste passo; e chamado antes de carregar (0),
    apos carregar (20), antes de parametrizar (30), logo apos a
    parametrizacao retornar (80), apos as metricas (90) e apos gravar
    o .npz (100). Se ele levantar (o worker levanta JobCancelado
    quando o job foi cancelado no disco), a excecao propaga ANTES de
    gravar o .npz: um cancelamento pedido durante a parametrizacao
    aborta antes de qualquer saida, sem publicar nada parcial.

    Limitacao honesta (D-COR05-1): a chamada nativa ``atlas.generate``
    (~97 s no Orc Prata) e um unico bloqueio e nao pode ser
    interrompida no meio; a janela residual de cancelamento e
    exatamente essa chamada. Antes dela, o ultimo ponto de checagem
    era o ``avisar(5)`` do passo; depois dela, o ponto 80 acima.
    """
    t0 = time.perf_counter()

    def avisar(pct, msg):
        if progresso is not None:
            progresso(pct, msg)

    avisar(0, "uv: carregando GLB")
    verts, faces = carregar_malha_glb(caminho_glb)
    avisar(20, "uv: GLB carregado")
    avisar(30, "uv: parametrizando (xatlas)")
    vmapping, indices, uvs = parametrizar(verts, faces, padding_px, resolucao, max_cost)
    avisar(80, "uv: parametrizacao pronta")
    faces_uv = uvs[indices]
    a, b, c = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
    areas = np.linalg.norm(np.cross(b - a, c - a), axis=1) * 0.5
    met = metricas(faces_uv, areas)
    avisar(90, "uv: metricas prontas")
    met["tempo_s"] = round(time.perf_counter() - t0, 2)
    met["vertices_originais"] = int(len(verts))
    met["vertices_com_costura"] = int(len(uvs))
    met["padding_px"] = int(padding_px)
    met["resolucao"] = int(resolucao)
    met["max_cost"] = float(max_cost)
    Path(caminho_npz).parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(caminho_npz, vmapping=vmapping.astype(np.int64),
                        indices=indices.astype(np.int64), uvs=uvs.astype(np.float32))
    avisar(100, "uv: .npz gravado")
    return met


if __name__ == "__main__":
    import sys

    glb, npz = sys.argv[1], sys.argv[2]
    res = gerar_uv(glb, npz)
    print(json.dumps(res, indent=1))
    if len(sys.argv) > 3:
        Path(sys.argv[3]).write_text(json.dumps(res, indent=1), encoding="utf-8")
