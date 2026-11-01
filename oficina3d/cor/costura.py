"""Medicao de costura (D7) e de cor por face para a Etapa COR.

Pergunta D7: nas bordas entre ilhas da UV (costuras do chart), a cor
renderizada salta mais do que nas bordas internas as ilhas? Se sim, a
costura e visivel no modelo; se nao, a projecao + dilatacao a esconde.

Metodo (puro numpy, sem Blender):
- Cada face recebe uma cor = mediana de 4 amostras da textura (centroide
  da UV + 3 pontos a 1/4 do caminho ate cada vertice). A mediana resiste
  a uma amostra cair no gutter.
- Uma aresta 3D compartilhada por 2 faces e "costura" quando as duas
  faces NAO compartilham o segmento UV (as coordenadas UV dos vertices
  3D em comum diferem alem da tolerancia). Aresta interna compartilha.
- Descontinuidade = distancia euclidiana RGB entre as cores das faces
  vizinhas, separada em costura x interna, com media, mediana, p90 e a
  fracao acima de 30 e de 60 (limiares de salto visivel; 30 = salto
  perceptivel, 60 = salto forte).

Sobre o flip V (licao L-23): a amostragem usa UM mapeamento fixo
(linha = (1 - v) * (H - 1)) para TODAS as texturas comparadas, que
compartilham a mesma UV. A distancia entre duas texturas, e a distancia
costura x interna dentro de uma textura, nao dependem de o mapeamento
estar "certo" no sentido glTF: o mesmo texel e amostrado nos dois lados
da comparacao. Nao se afirma aqui qual flip o glTF espera.

Sobre a cor por face: e um PROXY (4 amostras por face), nao a media
exata dos texels do triangulo. Faces pequenas (poucos texels) tornam o
proxy ruidoso; por isso a leitura e sempre em distribuicao (mediana,
p90, fracoes), nunca numa unica aresta.
"""

from __future__ import annotations

import numpy as np

LIMIAR_VISIVEL = 30.0
LIMIAR_FORTE = 60.0
TOL_UV = 1e-6


def amostras_face(faces_uv: np.ndarray) -> np.ndarray:
    """(F, 3, 2) UV -> (F, 4, 2): centroide + 3 pontos quarto-a-vertice."""
    faces_uv = np.asarray(faces_uv, dtype=np.float64)
    centroide = faces_uv.mean(axis=1)
    pontos = [centroide]
    for k in range(3):
        pontos.append(0.75 * centroide + 0.25 * faces_uv[:, k, :])
    return np.stack(pontos, axis=1)


def cores_por_face(faces_uv: np.ndarray, textura: np.ndarray) -> np.ndarray:
    """Cor mediana por face a partir da textura (H, W, 3|4) uint8.

    Retorna (F, 3) float. Textura RGBA: usa so RGB.
    """
    textura = np.asarray(textura)
    if textura.ndim != 3 or textura.shape[2] not in (3, 4):
        raise ValueError("textura esperada (H, W, 3|4), veio %s" % (textura.shape,))
    h, w = textura.shape[0], textura.shape[1]
    rgb = textura[:, :, :3].astype(np.float64)
    pts = amostras_face(faces_uv)
    col = np.clip(np.rint(pts[:, :, 0] * (w - 1)).astype(int), 0, w - 1)
    lin = np.clip(np.rint((1.0 - pts[:, :, 1]) * (h - 1)).astype(int), 0, h - 1)
    amostras = rgb[lin, col]  # (F, 4, 3)
    return np.median(amostras, axis=1)


def _pares_adjacentes(faces: np.ndarray):
    """Aresta 3D (min, max) -> lista de indices de faces que a usam."""
    faces = np.asarray(faces, dtype=int)
    arestas: dict = {}
    for fi in range(len(faces)):
        tri = faces[fi]
        for a, b in ((tri[0], tri[1]), (tri[1], tri[2]), (tri[2], tri[0])):
            chave = (min(a, b), max(a, b))
            arestas.setdefault(chave, []).append(fi)
    return arestas


def classificar_arestas(faces: np.ndarray, faces_uv: np.ndarray, tol: float = TOL_UV):
    """Classifica cada aresta compartilhada por exatamente 2 faces.

    Retorna (pares, n_borda, n_nao_manifold): pares = lista de
    (f1, f2, e_costura). Aresta de borda (1 face) nao e defeito nem
    nao-manifold: e contada a parte. So aresta com > 2 faces e
    nao-manifold. Nenhuma das duas entra nas estatisticas de salto.
    """
    faces = np.asarray(faces, dtype=int)
    faces_uv = np.asarray(faces_uv, dtype=np.float64)
    arestas = _pares_adjacentes(faces)
    pares = []
    n_borda = 0
    n_nao_manifold = 0
    for (va, vb), incidentes in arestas.items():
        if len(incidentes) == 1:
            n_borda += 1
            continue
        if len(incidentes) != 2:
            n_nao_manifold += 1
            continue
        f1, f2 = incidentes
        # Coordenadas UV de va e vb em cada face.
        def uv_de(face_idx, vertice):
            tri = faces[face_idx]
            for k in range(3):
                if tri[k] == vertice:
                    return faces_uv[face_idx, k]
            raise ValueError("vertice fora da face")
        uv1a, uv1b = uv_de(f1, va), uv_de(f1, vb)
        uv2a, uv2b = uv_de(f2, va), uv_de(f2, vb)
        e_costura = bool(np.max(np.abs(uv1a - uv2a)) > tol
                         or np.max(np.abs(uv1b - uv2b)) > tol)
        pares.append((f1, f2, e_costura))
    return pares, n_borda, n_nao_manifold


def _estatisticas(distancias: np.ndarray) -> dict:
    d = np.asarray(distancias, dtype=np.float64)
    if len(d) == 0:
        return {"n": 0, "media": None, "mediana": None, "p90": None,
                "pct_acima_30": None, "pct_acima_60": None, "max": None}
    return {"n": int(len(d)), "media": round(float(d.mean()), 2),
            "mediana": round(float(np.median(d)), 2),
            "p90": round(float(np.percentile(d, 90)), 2),
            "pct_acima_30": round(float((d > LIMIAR_VISIVEL).mean() * 100), 2),
            "pct_acima_60": round(float((d > LIMIAR_FORTE).mean() * 100), 2),
            "max": round(float(d.max()), 2)}


def descontinuidade(faces: np.ndarray, faces_uv: np.ndarray,
                    cores: np.ndarray) -> dict:
    """Estatisticas de salto de cor: costura x interna as ilhas."""
    pares, n_borda, n_nao_manifold = classificar_arestas(faces, faces_uv)
    cores = np.asarray(cores, dtype=np.float64)
    dist_costura = []
    dist_interna = []
    for f1, f2, e_costura in pares:
        dist = float(np.linalg.norm(cores[f1] - cores[f2]))
        (dist_costura if e_costura else dist_interna).append(dist)
    return {"costura": _estatisticas(np.array(dist_costura)),
            "interna": _estatisticas(np.array(dist_interna)),
            "arestas_classificadas": len(pares),
            "arestas_borda": n_borda,
            "arestas_nao_manifold": n_nao_manifold}


def distancia_cor_por_direcao(normais: np.ndarray, cores_a: np.ndarray,
                             cores_b: np.ndarray, direcao: np.ndarray,
                             limiar: float = 0.5) -> dict:
    """Distancia de cor entre duas texturas, por grupo de faces.

    Grupo "alvo": faces com dot(normal, direcao) > limiar (faces que
    olham para aquela direcao); grupo "controle": dot < -limiar.
    Serve a D2: no bake sem a vista das costas, as faces das costas
    (alvo) devem mudar e as da frente (controle) devem ficar paradas.
    """
    normais = np.asarray(normais, dtype=np.float64)
    direcao = np.asarray(direcao, dtype=np.float64)
    direcao = direcao / (np.linalg.norm(direcao) or 1.0)
    normas = np.linalg.norm(normais, axis=1, keepdims=True)
    normas[normas == 0] = 1.0
    pontos = (normais / normas) @ direcao
    dist = np.linalg.norm(np.asarray(cores_a, dtype=np.float64)
                          - np.asarray(cores_b, dtype=np.float64), axis=1)
    out = {}
    for nome, mascara in (("alvo", pontos > limiar), ("controle", pontos < -limiar)):
        d = dist[mascara]
        out[nome] = {"n": int(len(d)),
                     "media": round(float(d.mean()), 2) if len(d) else None,
                     "mediana": round(float(np.median(d)), 2) if len(d) else None,
                     "pct_acima_30": round(float((d > LIMIAR_VISIVEL).mean() * 100), 2) if len(d) else None}
    return out
