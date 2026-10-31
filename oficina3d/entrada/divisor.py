"""Divisor de pranchas: separa uma imagem com várias vistas em partes (numpy + opencv).

Método (o que funcionou na v1, no Capríleo/Orc/Besta):
1. Máscara do alfa (> 10) e componentes conexos.
2. Ficam os componentes "grandes" (>= 8% da área do maior e >= 50% da altura do mais alto);
   o resto são fragmentos (cristal solto, ponta de cauda) e vão para a parte mais próxima.
3. Vistas encostadas/sobrepostas (um componente só): sementes pela distância à borda
   (equivale à erosão progressiva da máscara) e crescimento geodésico das sementes dentro
   da máscara (watershed simplificado). A divisão só vale se cada parte for grande e o
   contato entre partes for estreito (comprimento do contato <= 0,33 da altura da parte;
   0,5 se o componente for muito largo; 0,6 se o usuário disse quantas vistas são).
4. NUNCA corta em quadrantes iguais (caudas e chifres passam das linhas).

A análise é feita numa cópia reduzida (lado <= 768 px) e o resultado volta à resolução
original; o recorte final usa os pixels originais.
"""
from __future__ import annotations

import statistics

from .dependencias import exigir
from .imagem import ALFA_FRACO

ESCALA_ANALISE = 768
FRACAO_AREA_GRANDE = 0.08
FRACAO_ALTURA_GRANDE = 0.50
FRACAO_AREA_PARTE = 0.30
FRACAO_ALTURA_PARTE = 0.50
CONTATO_MAX = 0.33
CONTATO_MAX_LARGA = 0.50
CONTATO_MAX_ETIQUETADA = 0.60
LARGURA_VS_MEDIANA = 1.6
ASPECTO_LARGO = 2.5
SOBREPOSICAO_CAIXAS = 0.5
MAX_PARTES = 12
PROFUNDIDADE_MAX = 4
FRACOES = tuple(round(0.20 + 0.05 * k, 2) for k in range(13))   # 0,20 … 0,80 da distância máxima


def _libs():
    np = exigir("numpy", "dividir pranchas")
    cv2 = exigir("cv2", "dividir pranchas (opcoes.dividir_pranchas)")
    return np, cv2


def _medidas(p) -> dict:
    np, _ = _libs()
    ys, xs = np.nonzero(p)
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    return {"area": int(ys.size), "x0": x0, "x1": x1, "y0": y0, "y1": y1,
            "w": x1 - x0 + 1, "h": y1 - y0 + 1, "cx": float(xs.mean()), "cy": float(ys.mean())}


def _crescer(marcadores, mask, max_iter: int | None = None):
    """Crescimento geodésico (8-vizinhos) dos rótulos dentro da máscara. Devolve int32."""
    np, cv2 = _libs()
    rot = marcadores.astype(np.float32)
    livre = mask & (marcadores == 0)
    k3 = np.ones((3, 3), np.uint8)
    limite = max_iter if max_iter is not None else mask.shape[0] + mask.shape[1]
    for _ in range(limite):
        if not livre.any():
            break
        d = cv2.dilate(rot, k3)
        novo = livre & (d > 0)
        if not novo.any():
            break
        rot[novo] = d[novo]
        livre &= ~novo
    return rot.astype(np.int32)


def _contato(a, b) -> int:
    """Quantos pixels de `a` encostam em `b` (≈ comprimento da fronteira)."""
    np, cv2 = _libs()
    db = cv2.dilate(b.astype(np.uint8), np.ones((3, 3), np.uint8)) > 0
    return int(np.count_nonzero(a & db))


def _fundir_pequenas(partes: list) -> list:
    """Partes pequenas/baixas demais (cabeça, perna, arma) voltam para a vizinha de maior contato."""
    while len(partes) > 1:
        med = [_medidas(p) for p in partes]
        amax = max(m["area"] for m in med)
        hmax = max(m["h"] for m in med)
        pequenas = [i for i, m in enumerate(med)
                    if m["area"] < FRACAO_AREA_PARTE * amax or m["h"] < FRACAO_ALTURA_PARTE * hmax]
        if not pequenas:
            break
        i = min(pequenas, key=lambda k: med[k]["area"])

        def chave(j):
            dist = (med[i]["cx"] - med[j]["cx"]) ** 2 + (med[i]["cy"] - med[j]["cy"]) ** 2
            return (_contato(partes[i], partes[j]), -dist)

        destino = max((j for j in range(len(partes)) if j != i), key=chave)
        partes[destino] = partes[destino] | partes[i]
        del partes[i]
    return partes


def _fundir_contato_largo(partes: list, limite: float) -> list:
    """Duas partes com fronteira longa demais são a MESMA vista: junta (a pior primeiro)."""
    while len(partes) > 1:
        med = [_medidas(p) for p in partes]
        pior = None
        for i in range(len(partes)):
            for j in range(i + 1, len(partes)):
                c = _contato(partes[i], partes[j])
                if c == 0:
                    continue
                dx = abs(med[i]["cx"] - med[j]["cx"])
                dy = abs(med[i]["cy"] - med[j]["cy"])
                base = min(med[i]["h"], med[j]["h"]) if dx >= dy else min(med[i]["w"], med[j]["w"])
                razao = c / max(1, base)
                if razao > limite and (pior is None or razao > pior[0]):
                    pior = (razao, i, j)
        if pior is None:
            break
        _, i, j = pior
        partes[i] = partes[i] | partes[j]
        del partes[j]
    return partes


def _lado_a_lado(partes: list) -> bool:
    """As partes têm de estar lado a lado ou uma sobre a outra (não uma dentro da outra)."""
    med = [_medidas(p) for p in partes]
    for i in range(len(med)):
        for j in range(i + 1, len(med)):
            a, b = med[i], med[j]
            ox = max(0, min(a["x1"], b["x1"]) - max(a["x0"], b["x0"]) + 1) / min(a["w"], b["w"])
            oy = max(0, min(a["y1"], b["y1"]) - max(a["y0"], b["y0"]) + 1) / min(a["h"], b["h"])
            if min(ox, oy) >= SOBREPOSICAO_CAIXAS:
                return False
    return True


def _separar_recorte(sub, limite: float):
    """Tenta separar um componente (já recortado e com borda de zeros). None = não separa."""
    np, cv2 = _libs()
    m8 = sub.astype(np.uint8)
    area = int(m8.sum())
    dist = cv2.distanceTransform(m8, cv2.DIST_L2, 5)
    dmax = float(dist.max())
    if dmax < 3:
        return None
    for fr in FRACOES:
        sementes = (dist > fr * dmax).astype(np.uint8)
        k, lab, st, _ = cv2.connectedComponentsWithStats(sementes, connectivity=8)
        idx = [j for j in range(1, k) if st[j, cv2.CC_STAT_AREA] >= max(4, 0.002 * area)]
        if len(idx) < 2:
            continue
        marc = np.zeros(sub.shape, np.int32)
        for n, j in enumerate(idx, 1):
            marc[lab == j] = n
        rot = _crescer(marc, sub)
        partes = [rot == n for n in range(1, len(idx) + 1)]
        partes = [p for p in partes if p.any()]
        partes = _fundir_pequenas(partes)
        partes = _fundir_contato_largo(partes, limite)
        if len(partes) >= 2 and _lado_a_lado(partes):
            return partes
    return None


def _separar(m, limite: float, profundidade: int = 0) -> list:
    """Separa recursivamente um componente em vistas. Devolve máscaras do tamanho de `m`."""
    np, _ = _libs()
    if profundidade >= PROFUNDIDADE_MAX:
        return [m]
    ys, xs = np.nonzero(m)
    y0, y1, x0, x1 = int(ys.min()), int(ys.max()) + 1, int(xs.min()), int(xs.max()) + 1
    sub = np.pad(m[y0:y1, x0:x1], 1)               # borda de zeros p/ a distância
    res = _separar_recorte(sub, limite)
    if res is None:
        return [m]
    saida = []
    for p in res:
        cheia = np.zeros_like(m)
        cheia[y0:y1, x0:x1] = p[1:-1, 1:-1]
        saida.extend(_separar(cheia, limite, profundidade + 1))
    return saida


def _ordenar(partes: list) -> list:
    """Ordem de leitura: linhas de cima para baixo, e da esquerda para a direita em cada linha."""
    med = [_medidas(p) for p in partes]
    hmed = statistics.median(m["h"] for m in med)
    linhas: list[list[int]] = []
    for i in sorted(range(len(partes)), key=lambda k: med[k]["cy"]):
        if linhas and abs(med[i]["cy"] - med[linhas[-1][0]]["cy"]) < 0.5 * hmed:
            linhas[-1].append(i)
        else:
            linhas.append([i])
    return [partes[i] for linha in linhas for i in sorted(linha, key=lambda k: med[k]["cx"])]


def _partes_na_analise(peq, n_esperado: int | None):
    np, cv2 = _libs()
    k, lab, st, _ = cv2.connectedComponentsWithStats(peq.astype(np.uint8), connectivity=8)
    comps = [(j, int(st[j, cv2.CC_STAT_AREA]), int(st[j, cv2.CC_STAT_WIDTH]),
              int(st[j, cv2.CC_STAT_HEIGHT])) for j in range(1, k)]
    if not comps:
        return [], "vazia"
    amax = max(c[1] for c in comps)
    candidatos = [c for c in comps if c[1] >= FRACAO_AREA_GRANDE * amax]
    hmax = max(c[3] for c in candidatos)
    grandes = [c for c in candidatos if c[3] >= FRACAO_ALTURA_GRANDE * hmax]
    mediana = statistics.median(c[2] for c in grandes)
    partes, usou_sementes = [], False
    for j, _area, w, h in grandes:
        if n_esperado and n_esperado > len(grandes):
            limite = CONTATO_MAX_ETIQUETADA
        elif (len(grandes) >= 2 and w > LARGURA_VS_MEDIANA * mediana) or \
                (len(grandes) == 1 and w > ASPECTO_LARGO * h):
            limite = CONTATO_MAX_LARGA
        else:
            limite = CONTATO_MAX
        sub = _separar(lab == j, limite)
        usou_sementes = usou_sementes or len(sub) > 1
        partes.extend(sub)
    metodo = "componentes" + ("+sementes" if usou_sementes else "")
    return partes, metodo


def _completar(lab, mask, n: int):
    """Pixels da máscara sem rótulo (efeito da redução ou fragmentos soltos) vão para a parte
    mais próxima; migalhas minúsculas ficam de fora (alfa 0)."""
    np, cv2 = _libs()
    if (mask & (lab == 0)).any():
        lab = _crescer(lab, mask, max_iter=8)
    falta = mask & (lab == 0)
    if not falta.any():
        return lab
    k, cc, st, cent = cv2.connectedComponentsWithStats(falta.astype(np.uint8), connectivity=8)
    total = int(np.count_nonzero(mask))
    distancias = [cv2.distanceTransform(np.where(lab == i, 0, 1).astype(np.uint8), cv2.DIST_L2, 3)
                  for i in range(1, n + 1)]
    h, w = mask.shape
    for j in range(1, k):
        if st[j, cv2.CC_STAT_AREA] < max(16, 0.0001 * total):
            continue
        px = min(w - 1, max(0, int(round(cent[j][0]))))
        py = min(h - 1, max(0, int(round(cent[j][1]))))
        destino = 1 + int(np.argmin([d[py, px] for d in distancias]))
        lab[cc == j] = destino
    return lab


def dividir(arr, n_esperado: int | None = None) -> dict:
    """Detecta e separa as vistas de uma prancha RGBA.

    Devolve {"mascaras": [máscaras bool HxW, em ordem de leitura], "metodo": str}.
    Uma imagem com uma vista só devolve 1 máscara (a do objeto inteiro, sem mexer em nada).
    `n_esperado`: quantas vistas o usuário disse que há (etiquetas); afrouxa o critério.
    """
    np, cv2 = _libs()
    mask = arr[..., 3] > ALFA_FRACO
    if not mask.any():
        return {"mascaras": [], "metodo": "vazia"}
    H, W = mask.shape
    fator = min(1.0, ESCALA_ANALISE / float(max(H, W)))
    if fator < 1.0:
        w2, h2 = max(1, int(round(W * fator))), max(1, int(round(H * fator)))
        peq = cv2.resize(mask.astype(np.uint8) * 255, (w2, h2), interpolation=cv2.INTER_AREA) > 127
    else:
        peq = mask
    partes, metodo = _partes_na_analise(peq, n_esperado)
    if len(partes) <= 1:
        return {"mascaras": [mask], "metodo": "unica"}
    if len(partes) > MAX_PARTES:
        return {"mascaras": [mask], "metodo": f"nao-dividida ({len(partes)} partes: demais)"}
    partes = _ordenar(partes)
    lab = np.zeros(peq.shape, np.int32)
    for i, p in enumerate(partes, 1):
        lab[p] = i
    if fator < 1.0:
        ys = np.minimum((np.arange(H) * peq.shape[0] / H).astype(np.int64), peq.shape[0] - 1)
        xs = np.minimum((np.arange(W) * peq.shape[1] / W).astype(np.int64), peq.shape[1] - 1)
        lab = lab[ys[:, None], xs[None, :]]
    lab = np.where(mask, lab, 0).astype(np.int32)
    lab = _completar(lab, mask, len(partes))
    mascaras = [lab == i for i in range(1, len(partes) + 1)]
    mascaras = [m for m in mascaras if m.any()]
    if len(mascaras) <= 1:
        return {"mascaras": [mask], "metodo": "unica"}
    return {"mascaras": mascaras, "metodo": metodo}
