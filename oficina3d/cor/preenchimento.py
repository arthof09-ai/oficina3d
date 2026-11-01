"""Preenchimento 3D da Etapa COR (COR-08, alavanca A3).

Problema (diagnostico D1, causa C3): ~81% dos texels da textura nascem
sem fonte projetada. A v1 os preenchia por DILATACAO EM ESPACO UV
(``projecao.dilatar``): o texel cego herdava a cor do texel pintado mais
perto NA TEXTURA - e vizinho de UV nao e vizinho no corpo. Com milhares
de ilhas, a cor saltava de uma parte do corpo para outra sem relacao
(a mancha branca do antebraco veio de ilhas claras de pelo): e o
"confete" que o Mestre ve.

Solucao A3: o texel cego herda a cor da FACE VIZINHA NO CORPO.
- ``mapa_texel_face`` diz a qual face cada texel da textura pertence;
- ``cores_diretas_por_face`` resume a cor projetada de cada face
  (media dos seus texels diretos);
- ``adjacencia_faces`` monta o grafo dual da malha com a SOLDA por
  posicao de ``cor/costura.py`` (obrigatoria em malha de GLB, L-24);
- ``difundir`` propaga a cor das faces com fonte para as faces cegas
  por BFS multi-fonte deterministica (anel = distancia em arestas);
- ``aplicar_preenchimento`` pinta os texels cegos com a cor difundida
  da sua propria face.

A dilatacao UV sobrevive so como ultimo recurso, restrita a uma faixa
em torno da UV (costuras/margens e faces sem nenhuma fonte alcancavel):
e o papel legitimo dela (anti-halo), nao solucao de preenchimento.

Proveniencia (auditoria v2): cada texel da area UV sai classificado em
direto / preenchimento_3d / dilatacao / sem_cor. Por construcao, 100%
do preenchimento_3d vem da mesma componente 3D conexa da face (a BFS
so atravessa arestas soldadas) - e essa a classe de defeito eliminada.

Determinismo: ordem de faces crescente em tudo (mapa, BFS, vizinhos);
nenhuma fonte de aleatoriedade. Convergencia registrada com o T2: a
difusao por faces e a mesma ideia da propagacao por vizinhanca de
``cor/vertice.py`` (la, por vertice; aqui, por face) - nao construir
uma terceira via.
"""
from __future__ import annotations

from collections import deque

import numpy as np

from oficina3d.cor import costura as _costura
from oficina3d.cor.projecao import _baricentricas, _uv_para_pixels


def mapa_texel_face(faces_uv: np.ndarray, tamanho: int) -> np.ndarray:
    """(T, T) int32: indice da face dona de cada texel, -1 fora de faces.

    Rasteriza os triangulos UV na ordem das faces; em sobreposicao de UV
    (parametrizacao invalida para bake), a face de indice MAIOR vence -
    regra fixa, igual a da imagem de ids de ``projecao._margem_ilhas``.
    """
    mapa = np.full((tamanho, tamanho), -1, dtype=np.int32)
    pts = _uv_para_pixels(np.asarray(faces_uv, dtype=np.float64), tamanho)
    for fi in range(len(pts)):
        p = pts[fi]
        x0 = max(0, int(np.floor(p[:, 0].min())))
        x1 = min(tamanho, int(np.ceil(p[:, 0].max())) + 1)
        y0 = max(0, int(np.floor(p[:, 1].min())))
        y1 = min(tamanho, int(np.ceil(p[:, 1].max())) + 1)
        if x1 <= x0 or y1 <= y0:
            continue
        xs, ys = np.meshgrid(np.arange(x0, x1), np.arange(y0, y1))
        res = _baricentricas(p, xs.ravel().astype(np.float64) + 0.5,
                             ys.ravel().astype(np.float64) + 0.5)
        if res is None:
            continue
        yy, xx = np.nonzero(res[0].reshape(ys.shape))
        mapa[y0 + yy, x0 + xx] = fi
    return mapa


def cores_diretas_por_face(textura: np.ndarray, pintado: np.ndarray,
                           texel_face: np.ndarray, n_faces: int):
    """Cor media dos texels DIRETOS de cada face.

    Retorna (cores (F,3) float, tem_cor (F,) bool, contagem (F,) int).
    Face sem nenhum texel direto: tem_cor False e cor 0 (nao usar).
    """
    textura = np.asarray(textura, dtype=np.float64)
    sel = pintado & (texel_face >= 0)
    idx = texel_face[sel].astype(np.int64)
    contagem = np.bincount(idx, minlength=n_faces)
    cores = np.zeros((n_faces, 3), dtype=np.float64)
    if len(idx):
        for c in range(3):
            cores[:, c] = np.bincount(idx, weights=textura[sel][:, c],
                                      minlength=n_faces)
    tem = contagem > 0
    cores[tem] = cores[tem] / contagem[tem, None]
    return cores, tem, contagem


def adjacencia_faces(faces: np.ndarray, verts: np.ndarray) -> list:
    """Grafo dual: vizinhos por aresta 3D compartilhada, com solda (L-24).

    Reusa a solda por posicao e o mapa de arestas de ``cor/costura.py``.
    Aresta nao-manifold (3+ faces) liga todas as faces incidentes entre
    si. Cada lista de vizinhos sai ordenada (determinismo da BFS).
    """
    faces_soldadas = _costura._faces_soldadas(faces, verts)
    arestas = _costura._pares_adjacentes(faces_soldadas)
    viz: list[set] = [set() for _ in range(len(faces))]
    for incidentes in arestas.values():
        for a in incidentes:
            for b in incidentes:
                if a != b:
                    viz[a].add(b)
    return [np.array(sorted(v), dtype=int) for v in viz]


def difundir(adjacencia: list, cores: np.ndarray, tem_cor: np.ndarray):
    """BFS multi-fonte: faces cegas herdam a cor da fonte mais perto.

    Retorna (cores_final (F,3), anel (F,) int, alcancavel (F,) bool).
    Fontes (tem_cor) tem anel 0 e sao sua propria fonte. A ordem da fila
    e a dos indices crescentes e os vizinhos sao visitados em ordem
    crescente: a primeira descoberta vence - resultado deterministico.
    Face fora de qualquer componente com fonte: alcancavel False,
    anel -1, cor 0 (o chamador decide o recurso - dilatacao UV).
    """
    n = len(adjacencia)
    cores = np.asarray(cores, dtype=np.float64)
    anel = np.full(n, -1, dtype=int)
    fonte = np.full(n, -1, dtype=int)
    fila = deque()
    for f in range(n):
        if tem_cor[f]:
            anel[f] = 0
            fonte[f] = f
            fila.append(f)
    while fila:
        atual = fila.popleft()
        for viz in adjacencia[atual]:
            v = int(viz)
            if anel[v] == -1:
                anel[v] = anel[atual] + 1
                fonte[v] = fonte[atual]
                fila.append(v)
    alcancavel = anel >= 0
    cores_final = np.zeros((n, 3), dtype=np.float64)
    cores_final[alcancavel] = cores[fonte[alcancavel]]
    return cores_final, anel, alcancavel


def aplicar_preenchimento(textura: np.ndarray, pintado: np.ndarray,
                          texel_face: np.ndarray, cores_final: np.ndarray,
                          alcancavel: np.ndarray):
    """Pinta texels cegos com a cor difundida da SUA face.

    Retorna (textura, pintado, mascara_aplicada): a mascara marca os
    texels preenchidos por esta via (a proveniencia da auditoria v2).
    Texels fora de qualquer face ou de face inalcancavel nao sao
    tocados - ficam para a dilatacao restrita.
    """
    tex = np.array(textura, dtype=np.float64, copy=True)
    pin = pintado.copy()
    seguro = np.where(texel_face >= 0, texel_face, 0)
    aplicada = (~pin) & (texel_face >= 0) & alcancavel[seguro]
    if aplicada.any():
        tex[aplicada] = cores_final[seguro[aplicada]]
        pin[aplicada] = True
    return tex, pin, aplicada


def dominio_dilatacao_restrita(masc_uv: np.ndarray, texel_face: np.ndarray,
                               alcancavel: np.ndarray, passes: int = 8) -> np.ndarray:
    """Dominio da dilatacao restrita anti-halo (COR-08/A3).

    Base = area UV expandida por ``passes`` px (padrao 8 = o gutter da
    D-T5-1 em 2048: cobre a faixa entre ilhas sem atravessar o quadrado).
    Dela se SUBTRAEM os texels de faces inalcancaveis (componente 3D sem
    nenhuma fonte direta): preencher uma componente isolada por dilatacao
    UV seria importar cor de outra parte do corpo - exatamente o defeito
    que a A3 elimina. Esses texels ficam sem_cor e CONTADOS, nunca
    preenchidos em silencio.
    """
    base = expandir_mascara(masc_uv, passes)
    seguro = np.where(texel_face >= 0, texel_face, 0)
    fora = (texel_face >= 0) & ~alcancavel[seguro]
    return base & ~fora


def expandir_mascara(mascara: np.ndarray, passes: int) -> np.ndarray:
    """Expande uma mascara bool por ``passes`` px (4-vizinhos, sem wrap).

    Uso: a faixa em torno da UV que delimita o dominio da dilatacao
    restrita (anti-halo de costura), os mesmos guardas de borda de
    ``projecao.dilatar``.
    """
    m = mascara.copy()
    for _ in range(int(passes)):
        novo = m.copy()
        for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            desloc = np.roll(m, shift=(dy, dx), axis=(0, 1))
            if dy == -1:
                desloc[-1, :] = False
            elif dy == 1:
                desloc[0, :] = False
            if dx == -1:
                desloc[:, -1] = False
            elif dx == 1:
                desloc[:, 0] = False
            novo |= desloc
        if (novo == m).all():
            break
        m = novo
    return m
