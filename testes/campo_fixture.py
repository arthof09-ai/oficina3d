"""Fixture da cerca (6) de T-COR-3 (PACOTE-T-COR-3 SS3.1): corpo
sintetico por arrays, sem Blender, partilhado pelos testes
(``test_cor_campo.py``) e pelo gerador da medicao de divergencia
(``gerar_medicao_campo.py``) - uma so fixture, duas consumidoras.

Textura T = 64. Tres componentes:

- **A faixa:** 5 quadrados em cadeia ao longo de x (vertices
  duplicados por quadrado, estilo GLB - a solda e por posicao),
  z = 0 para x <= 2 e z = (x-2)*0,5 para x >= 2 (uma dobra a meio).
  Cada quadrado = 2 triangulos (faces 0..9); o grafo dual e a cadeia
  Q0-Q1-Q2-Q3-Q4. Ilhas UV: {Q0, Q1} na ilha A (contigua), {Q2}
  sozinho na ilha B, {Q3, Q4} na ilha C (contigua) - as arestas duais
  Q1-Q2 e Q2-Q3 atravessam costuras de ilha. Pintura: todos os
  texeis de Q0 com X = (1, 0, 0) e todos os de Q4 com ``cor_q4``
  (por omissao Y = (0, 0, 1)); Q1, Q2, Q3 inteiramente cegos e
  alcancaveis.
- **A componente desligada:** um quadrado afastado em 3D, ilha
  propria COLADA na grelha a ilha A (colunas de texeis vizinhas -
  e esta vizinhanca UV deliberada que da dentes ao mutante M-d:
  um acoplamento que ignore a restricao de mesma face/componente
  importa o verde Z para a faixa). Um triangulo pintado
  Z = (0, 1, 0) (face 10), o outro cego (face 11).
- **A componente inalcancavel:** um quadrado, ilha propria, nenhum
  texel pintado (faces 12, 13) - testa a exclusao de SS1.3.

A variante de fronteira intermedia (descarga de Metodo C-1 no
julgamento do pacote) constroi-se com ``cor_q4=(0.5, 0.25, 0.75)``:
a medicao da divergencia corre nas duas, para exercitar P1 e nao
so P2. As leituras (a)-(g) de SS3.2 correm so na fixture base.
"""
import hashlib

import numpy as np

from oficina3d.cor import preenchimento as PF

TAMANHO = 64
COR_X = (1.0, 0.0, 0.0)
COR_Y = (0.0, 0.0, 1.0)
COR_Z = (0.0, 1.0, 0.0)
COR_Q4_INTERMEDIA = (0.5, 0.25, 0.75)

# Celulas UV (u0, v0, u1, v1) por quadrado da faixa e componentes.
_UV_FAIXA = [
    (0.0, 0.5, 0.25, 0.75),      # Q0 - ilha A
    (0.25, 0.5, 0.5, 0.75),      # Q1 - ilha A
    (0.75, 0.0, 1.0, 0.25),      # Q2 - ilha B, sozinho (longe das outras)
    (0.0, 0.0625, 0.25, 0.3125),  # Q3 - ilha C
    (0.25, 0.0625, 0.5, 0.3125),  # Q4 - ilha C
]
_UV_DESLIGADA = (0.5, 0.5, 0.75, 0.75)   # colada a ilha A na grelha
_UV_INALCANCAVEL = (0.0, 0.75, 0.25, 1.0)


def _z(x):
    return 0.0 if x <= 2 else (x - 2) * 0.5


def _quadrado(verts, faces, faces_uv, cantos3d, celula_uv):
    """Acrescenta um quadrado (2 triangulos, vertices proprios)."""
    bl, br, tr, tl = cantos3d
    base = len(verts)
    verts.extend([bl, br, tr, tl])
    u0, v0, u1, v1 = celula_uv
    # Triangulo 0: BL, BR, TR. Triangulo 1: BL, TR, TL.
    faces.append([base + 0, base + 1, base + 2])
    faces_uv.append([(u0, v0), (u1, v0), (u1, v1)])
    faces.append([base + 0, base + 2, base + 3])
    faces_uv.append([(u0, v0), (u1, v1), (u0, v1)])


def construir_fixture(cor_q4=COR_Y):
    """Constroi a fixture; ``cor_q4`` e a cor pintada em Q4 (a
    variante intermedia passa COR_Q4_INTERMEDIA). Devolve um dict
    com os arrays de construcao e os grupos de faces nomeados."""
    verts, faces, faces_uv = [], [], []
    for i in range(5):
        x0, x1 = float(i), float(i + 1)
        cantos = [(x0, 0.0, _z(x0)), (x1, 0.0, _z(x1)),
                  (x1, 1.0, _z(x1)), (x0, 1.0, _z(x0))]
        _quadrado(verts, faces, faces_uv, cantos, _UV_FAIXA[i])
    # Componente desligada (longe em 3D; ilha colada a A na grelha).
    _quadrado(verts, faces, faces_uv,
              [(10.0, 0.0, 5.0), (11.0, 0.0, 5.0),
               (11.0, 1.0, 5.0), (10.0, 1.0, 5.0)], _UV_DESLIGADA)
    # Componente inalcancavel.
    _quadrado(verts, faces, faces_uv,
              [(20.0, 0.0, 5.0), (21.0, 0.0, 5.0),
               (21.0, 1.0, 5.0), (20.0, 1.0, 5.0)], _UV_INALCANCAVEL)
    verts = np.array(verts, dtype=np.float64)
    faces = np.array(faces, dtype=int)
    faces_uv = np.array(faces_uv, dtype=np.float64)
    texel_face = PF.mapa_texel_face(faces_uv, TAMANHO)
    textura = np.zeros((TAMANHO, TAMANHO, 3), dtype=np.float64)
    pintado = np.zeros((TAMANHO, TAMANHO), dtype=bool)
    grupos = {"Q0": (0, 1), "Q1": (2, 3), "Q2": (4, 5),
              "Q3": (6, 7), "Q4": (8, 9)}
    for nome, cor in (("Q0", COR_X), ("Q4", tuple(cor_q4))):
        for f in grupos[nome]:
            sel = texel_face == f
            textura[sel] = cor
            pintado[sel] = True
    sel = texel_face == 10  # triangulo pintado da componente desligada
    textura[sel] = COR_Z
    pintado[sel] = True
    return {"verts": verts, "faces": faces, "faces_uv": faces_uv,
            "texel_face": texel_face, "textura": textura,
            "pintado": pintado, "tamanho": TAMANHO, "grupos": grupos,
            "faces_faixa": tuple(range(10)),
            "face_pintada_desligada": 10, "face_cega_desligada": 11,
            "faces_inalcancavel": (12, 13), "cor_q4": tuple(cor_q4)}


def produtos_preenchimento(fx):
    """Os produtos de ``preenchimento.py`` sobre a fixture (os que o
    campo consome): (cores, tem_cor, contagem, adjacencia,
    cores_final, anel, alcancavel)."""
    cores, tem_cor, contagem = PF.cores_diretas_por_face(
        fx["textura"], fx["pintado"], fx["texel_face"], len(fx["faces"]))
    adj = PF.adjacencia_faces(fx["faces"], fx["verts"])
    cores_final, anel, alcancavel = PF.difundir(adj, cores, tem_cor)
    return cores, tem_cor, contagem, adj, cores_final, anel, alcancavel


def hash_fixture(fx):
    """Hash SHA-256 dos arrays de construcao da fixture (SS3.3)."""
    h = hashlib.sha256()
    for chave in ("verts", "faces", "faces_uv", "texel_face",
                  "textura", "pintado"):
        a = np.ascontiguousarray(fx[chave])
        h.update(chave.encode("ascii"))
        h.update(str(a.dtype).encode("ascii"))
        h.update(np.array(a.shape, dtype=np.int64).tobytes())
        h.update(a.tobytes())
    return h.hexdigest()
