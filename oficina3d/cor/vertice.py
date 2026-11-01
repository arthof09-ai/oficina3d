"""Etapa COR (T2): cor de vertice - matematica pura (sem bpy).

Nivel rapido e rede de seguranca da Etapa COR (docs/ESTUDO_MELHORIAS.md,
secao T2; desenho em docs/DECISOES.md, COR-07):

- cada vertice da malha refinada e pintado pela vista canonica de maior
  facing que o enxerga (mesmas cameras, mesmo alinhamento por silhueta e
  mesmo FACING_MIN do bake T1 - ``oficina3d.cor.projecao``);
- vertice que nenhuma vista pinta pode herdar a cor da FORMA (o COLOR_0
  que motores como o TripoSR ja geram e que o refino descarta - T2 item
  (i)); a transferencia geometrica (superficie mais proxima) acontece no
  script do Blender, este modulo so faz a MESCLA por prioridade;
- o que sobrar e preenchido por propagacao sobre as arestas da malha
  (dilatacao em grafo, passes com snapshot, ordem deterministica);
- o que nem a propagacao alcancar (componente sem nenhuma fonte) fica
  SEM cor e e CONTADO no resumo - nunca escondido.

Fontes (``fonte`` por vertice): 0 = nenhuma, 1 = vista, 2 = forma,
3 = propagacao. Prioridade estrita: vista > forma > propagacao.

Diferenca registrada contra o bake T1: la o pixel amostrado e limitado
por clip a borda da imagem; aqui, vertice projetado FORA do quadro da
vista nao pinta por ela (clip pintaria a cor da borda esticada sobre a
silhueta - num vertice, o erro fica visivel como mancha; fora do quadro
ele simplesmente nao e fonte).
"""
from __future__ import annotations

import math

import numpy as np

from oficina3d.cor import projecao as P

FONTE_NENHUMA = 0
FONTE_VISTA = 1
FONTE_FORMA = 2
FONTE_PROPAGACAO = 3


def amostrar_vertices(verts: np.ndarray, normais: np.ndarray, vistas: list[dict],
                      centro: np.ndarray, ortho_scale: float):
    """Pinta vertices por projecao das vistas. Retorna (cores, fonte, melhor, info).

    ``vistas``: lista de dicts com ``vista`` (nome), ``imagem`` (HxWx3 float
    0..1, linha 0 = topo), ``mascara`` (HxW bool) e ``visivel`` (N,) bool
    (oclusao pre-calculada por quem chama - no Blender, via BVH). A ordem
    da lista e a ordem de desempate (a primeira vista vence facing igual),
    como em ``projecao.rasterizar_textura``.
    """
    verts = np.asarray(verts, dtype=np.float64)
    normais = np.asarray(normais, dtype=np.float64)
    n = len(verts)
    cores = np.zeros((n, 3), dtype=np.float64)
    fonte = np.zeros(n, dtype=np.int8)
    melhor = np.zeros(n, dtype=np.float64)
    nn = np.linalg.norm(normais, axis=1)
    nn_safe = np.where(nn == 0, 1.0, nn)
    unit = normais / nn_safe[:, None]
    info = {"vertices_por_vista": {}}
    for v in vistas:
        nome = v["vista"]
        imagem = v["imagem"]
        mascara = v["mascara"]
        visivel = np.asarray(v["visivel"], dtype=bool)
        hi, wi = mascara.shape
        dcam = np.array(P.direcao_camera(nome), dtype=np.float64)
        facing = np.clip(unit @ dcam, 0.0, 1.0)
        px_all, py_all = P.projetar(verts, centro, nome, ortho_scale, wi, hi)
        bbox_m = (int(math.floor(px_all.min())), int(math.floor(py_all.min())),
                  int(math.ceil(px_all.max())), int(math.ceil(py_all.max())))
        bbox_a = P.bbox_mascara(mascara)
        if bbox_a is None:
            info["vertices_por_vista"][nome] = 0
            continue
        ax, bx, ay, by = P.alinhamento_silhueta(bbox_a, bbox_m)
        ipx = np.floor(ax * px_all + bx).astype(int)
        ipy = np.floor(ay * py_all + by).astype(int)
        dentro = (ipx >= 0) & (ipx < wi) & (ipy >= 0) & (ipy < hi)
        cand = visivel & (facing > P.FACING_MIN) & dentro
        if cand.any():
            idx = np.nonzero(cand)[0]
            ok = mascara[ipy[idx], ipx[idx]]
            idx = idx[ok]
            ganha = facing[idx] > melhor[idx]
            sel = idx[ganha]
            if len(sel):
                melhor[sel] = facing[sel]
                cores[sel] = imagem[ipy[sel], ipx[sel]]
                fonte[sel] = FONTE_VISTA
            info["vertices_por_vista"][nome] = int(len(sel))
        else:
            info["vertices_por_vista"][nome] = 0
    return cores, fonte, melhor, info


def mesclar_forma(cores: np.ndarray, fonte: np.ndarray, cores_forma):
    """Preenche vertices sem fonte com a cor transferida da forma.

    ``cores_forma``: (N,3) float ou None (None = forma sem cor utilizavel).
    Retorna quantos vertices foram preenchidos. Nao sobrescreve vista.
    """
    if cores_forma is None:
        return 0
    cores_forma = np.asarray(cores_forma, dtype=np.float64)
    alvo = fonte == FONTE_NENHUMA
    n = int(alvo.sum())
    if n:
        cores[alvo] = cores_forma[alvo]
        fonte[alvo] = FONTE_FORMA
    return n


def _adjacencia(faces: np.ndarray, n: int) -> list[list[int]]:
    viz: list[set] = [set() for _ in range(n)]
    for a, b, c in np.asarray(faces, dtype=int):
        viz[a].update((b, c))
        viz[b].update((a, c))
        viz[c].update((a, b))
    return [sorted(s) for s in viz]


def preencher_por_vizinhos(cores: np.ndarray, fonte: np.ndarray, faces: np.ndarray,
                           max_passes: int | None = None):
    """Dilatacao em grafo: preenche vertices sem fonte com a media dos
    vizinhos ja pintados, em passes com snapshot (o passe inteiro le o
    estado do inicio do passe - deterministico e sem vies de ordem).

    Retorna (n_preenchidos, passes_usados). Vertices de componentes sem
    nenhuma fonte nao sao alcancados: ficam FONTE_NENHUMA e cabem ao
    chamador conta-los e reporta-los.
    """
    n = len(cores)
    if max_passes is None:
        max_passes = n  # pior caso: uma cadeia de n vertices
    viz = _adjacencia(faces, n)
    preenchidos = 0
    passes = 0
    for _ in range(int(max_passes)):
        base_fonte = fonte.copy()
        base_cores = cores.copy()
        novos = []
        for vi in range(n):
            if base_fonte[vi] != FONTE_NENHUMA:
                continue
            pintados = [u for u in viz[vi] if base_fonte[u] != FONTE_NENHUMA]
            if pintados:
                novos.append((vi, base_cores[pintados].mean(axis=0)))
        if not novos:
            break
        passes += 1
        for vi, cor in novos:
            cores[vi] = cor
            fonte[vi] = FONTE_PROPAGACAO
        preenchidos += len(novos)
        if not (fonte == FONTE_NENHUMA).any():
            break
    return preenchidos, passes


def baricentricas_3d(p, a, b, c):
    """Pesos baricentricos de ``p`` no triangulo (a, b, c) 3D.

    Usado na transferencia da cor da forma: ``p`` e o ponto da superficie
    da forma mais proximo do vertice refinado. Retorna (w0, w1, w2) ou
    None se o triangulo e degenerado.
    """
    p = np.asarray(p, dtype=np.float64)
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    c = np.asarray(c, dtype=np.float64)
    v0 = b - a
    v1 = c - a
    v2 = p - a
    d00 = float(v0 @ v0)
    d01 = float(v0 @ v1)
    d11 = float(v1 @ v1)
    d20 = float(v2 @ v0)
    d21 = float(v2 @ v1)
    den = d00 * d11 - d01 * d01
    if abs(den) < 1e-14:
        return None
    w1 = (d11 * d20 - d01 * d21) / den
    w2 = (d00 * d21 - d01 * d20) / den
    return (1.0 - w1 - w2, w1, w2)


def resumo_cobertura(fonte: np.ndarray) -> dict:
    """Contagens por fonte (a soma confere com o total de vertices)."""
    fonte = np.asarray(fonte)
    total = int(len(fonte))
    cont = {
        "vista": int((fonte == FONTE_VISTA).sum()),
        "forma": int((fonte == FONTE_FORMA).sum()),
        "propagacao": int((fonte == FONTE_PROPAGACAO).sum()),
        "sem_cor": int((fonte == FONTE_NENHUMA).sum()),
    }
    pct = {k: (round(100.0 * v / total, 2) if total else 0.0) for k, v in cont.items()}
    return {"total_vertices": total, "por_fonte": cont, "pct": pct}

# --- Regra de aceite do alinhamento forma x refinado (D-T2-1) -------------
# A autochecagem antiga usava SO a distancia mediana (COR-07): o Critico
# do T2 mostrou que ela ACEITA uma forma sabotada com o eixo X esticado
# 2x (mediana 0,02101 < 0,05 - a mediana e insensivel a deformacao
# anisotropica). A regra nova soma duas guardas, ambas medidas na mesma
# amostra de distancias e nas caixas ja alinhadas:
#   * percentil p90 das distancias (fracao da altura): pega a cauda que
#     a mediana ignora - deformacao global empurra o p90, nao so a
#     mediana;
#   * razao por eixo das caixas (forma mapeada / refinado): pega o
#     esticamento direto, mesmo quando as distancias pontuais ficam
#     baixas (superficie 2D: ponto deslocado lateralmente continua perto
#     de ALGUMA parte da superficie).
# Limites medidos na tranche D-T2 (par legitimo TripoSR Orc, job
# crit-t2-soforma, vs sabotagem X2 do Critico): legitimo = mediana
# 0,00056, p90 0,0013, caixas <= 1,00184 (margem > 70x no p90 e > 20% na
# caixa); sabotado X2 = mediana 0,02022 (PASSAVA na regra antiga),
# p90 0,08138, caixa X 2,002 (recusado pela caixa). O p90 0,10 NAO pega
# o X2 sozinho: a caixa e a guarda primaria contra esticamento, o p90
# e guarda secundaria contra deformacoes que preservam a caixa.
# Limite conhecido, nao defeito escondido: deformacao LOCAL pequena
# (ex.: so um braco esticado) passa pelas tres guardas - a regra pega
# deformacao global anisotropica, que e o caso do Critico. A razao do
# eixo Z e ~1 por construcao (a escala e pela altura) e nao conta como
# guarda: ela esta na tabela por completude, nao por cobertura.
LIMITE_ALINHAMENTO_MEDIANA_FRAC = 0.05
LIMITE_ALINHAMENTO_P90_FRAC = 0.10
FAIXA_RAZAO_CAIXA = (0.80, 1.25)


def avaliar_alinhamento_forma(distancias_frac_altura, razoes_caixa):
    """Decide se a cor da forma pode ser transferida (regra D-T2-1).

    ``distancias_frac_altura``: distancias amostra -> superficie da forma
    alinhada, como fracao da altura do refinado. ``razoes_caixa``: dict
    {eixo: extensao_forma_mapeada / extensao_refinado} (eixos "x", "y",
    "z" - os tres SAO obrigatorios; dict incompleto e recusado, S4-2).
    Devolve (aceita, motivo, metricas): motivo vazio quando
    aceita; metricas traz mediana, p90 e razoes (arredondados) para o
    relatorio do job. A decisao usa os valores sem arredondar.
    """
    dists = np.asarray(list(distancias_frac_altura or []), dtype=np.float64)
    razoes = dict(razoes_caixa or {})
    med = float(np.median(dists)) if len(dists) else None
    p90 = float(np.percentile(dists, 90)) if len(dists) else None
    metricas = {
        "dist_mediana_frac_altura": round(med, 5) if med is not None else None,
        "dist_p90_frac_altura": round(p90, 5) if p90 is not None else None,
        "razao_caixa": {k: round(float(v), 5) for k, v in razoes.items()},
    }
    if not len(dists):
        return False, "alinhamento forma x refinado sem amostra de distancia", metricas
    faltam = [e for e in ("x", "y", "z") if e not in razoes]
    if faltam:
        return False, ("alinhamento forma x refinado sem razoes de caixa dos "
                       f"eixos: {','.join(faltam)}"), metricas
    if med > LIMITE_ALINHAMENTO_MEDIANA_FRAC:
        return False, "alinhamento forma x refinado nao sadio (distancia mediana alta)", metricas
    if p90 > LIMITE_ALINHAMENTO_P90_FRAC:
        return False, "alinhamento forma x refinado nao sadio (percentil p90 alto)", metricas
    lo, hi = FAIXA_RAZAO_CAIXA
    for eixo, razao in razoes.items():
        if not (lo <= float(razao) <= hi):
            return False, (f"alinhamento forma x refinado nao sadio "
                           f"(caixa do eixo {eixo} fora da faixa: {float(razao):.3f})"), metricas
    return True, "", metricas
