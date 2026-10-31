"""Validações que geram AVISOS (nunca travam o job). Textos em português claro."""
from __future__ import annotations

from .dependencias import exigir
from .imagem import ALFA_FRACO, caixa, estatisticas_alfa, mascara, pct
from .vistas import VISTAS_SEM_FORMA

# Limites (calibrados na v1 com Orc, Capríleo e Besta; reconferir no conjunto dourado da v2).
OPACO_DEMAIS = 0.98        # >= 98% dos pixels opacos = "fundo não removido"
FRACO_DEMAIS = 0.01        # >= 1% dos pixels com alfa 1–10 = "fundo não removido de verdade"
SEMI_DEMAIS = 0.20         # >= 20% do objeto semitransparente = "recorte incerto"
RES_MENOR_LADO = 512       # menor lado do objeto <= 512 px (Besta 739×512 caiu aqui na v1)
RES_MAIOR_LADO = 768       # ou maior lado < 768 px (1024 com margem pede ~860)
BORDA_MIN_PX = 3           # pixels tocando a borda para contar como "cortado"
LIMITE_PERSONAGENS = 0.45  # distância de cor acima disso = personagens diferentes (v1: 0,34 x 0,58)


def diagnostico_fundo(arr, tinha_alfa: bool) -> tuple[bool, str | None]:
    """(alfa_util, motivo). alfa_util=False => precisa remover o fundo (ou vai com ele)."""
    if not tinha_alfa:
        return False, "sem fundo transparente (imagem sem canal alfa)"
    est = estatisticas_alfa(arr)
    if est["opaco"] >= OPACO_DEMAIS:
        return False, f"fundo não removido ({pct(est['opaco'])} opaco)"
    if est["fraco"] >= FRACO_DEMAIS:
        return True, (f"fundo não removido de verdade ({pct(est['fraco'])} dos pixels "
                      f"com alfa 1–10)")
    return True, None


def avisos_recorte(arr, nome: str, checar_borda: bool = True) -> list[str]:
    """Resolução baixa, objeto cortado na borda e recorte semitransparente."""
    np = exigir("numpy", "validar imagens")
    avisos: list[str] = []
    mask = mascara(arr, ALFA_FRACO)
    cx = caixa(mask)
    if cx is None:
        return [f"{nome}: imagem vazia (nada com alfa > 10)"]
    x0, y0, x1, y1 = cx
    w, h = x1 - x0 + 1, y1 - y0 + 1
    if min(w, h) <= RES_MENOR_LADO or max(w, h) < RES_MAIOR_LADO:
        avisos.append(f"{nome}: resolução baixa (objeto com {w}×{h} px; o ideal é >= 768 px "
                      f"no lado maior e > 512 no menor)")
    if checar_borda:
        lados = []
        for rotulo, faixa in (("em cima", mask[0, :]), ("embaixo", mask[-1, :]),
                              ("à esquerda", mask[:, 0]), ("à direita", mask[:, -1])):
            n = int(np.count_nonzero(faixa))
            if n >= BORDA_MIN_PX:
                lados.append(f"{rotulo} ({n} px)")
        if lados:
            avisos.append(f"{nome}: objeto cortado na borda: " + ", ".join(lados))
    semi = estatisticas_alfa(arr)["semi_no_objeto"]
    if semi >= SEMI_DEMAIS:
        avisos.append(f"{nome}: recorte incerto ({pct(semi)} do objeto ficou semitransparente)")
    return avisos


def vistas_repetidas(registros: list[dict]) -> list[str]:
    contagem: dict[str, int] = {}
    for r in registros:
        v = r.get("vista")
        if v and v not in VISTAS_SEM_FORMA:
            contagem[v] = contagem.get(v, 0) + 1
    return [f"vista repetida: '{v}' aparece {n} vezes (os arquivos ganharam sufixo _2, _3…)"
            for v, n in contagem.items() if n > 1]


def assinatura_cor(arr):
    """Histograma RGB 4×4×4 (64 caixas) das áreas opacas, normalizado (soma 1)."""
    np = exigir("numpy", "comparar cores das imagens")
    mask = arr[..., 3] > 128
    if not mask.any():
        return None
    rgb = arr[..., :3][mask].astype(np.int32) // 64          # 0..3 por canal
    idx = rgb[:, 0] * 16 + rgb[:, 1] * 4 + rgb[:, 2]
    hist = np.bincount(idx, minlength=64).astype(np.float64)
    return hist / hist.sum()


def distancia_cor(a, b) -> float:
    """Distância de variação total entre histogramas (0 = iguais, 1 = nada em comum)."""
    return float(0.5 * abs(a - b).sum())


def personagens_diferentes(registros: list[dict], limite: float = LIMITE_PERSONAGENS) -> list[str]:
    """Agrupa as imagens por cor (ligação simples). Mais de 1 grupo => aviso (não bloqueia).

    `registros`: [{"nome": str, "assinatura": array|None, "vista": ...}]
    """
    itens = [r for r in registros if r.get("assinatura") is not None
             and r.get("vista") not in VISTAS_SEM_FORMA]
    if len(itens) < 2:
        return []
    grupo = list(range(len(itens)))

    def raiz(i):
        while grupo[i] != i:
            grupo[i] = grupo[grupo[i]]
            i = grupo[i]
        return i

    for i in range(len(itens)):
        for j in range(i + 1, len(itens)):
            if distancia_cor(itens[i]["assinatura"], itens[j]["assinatura"]) <= limite:
                grupo[raiz(i)] = raiz(j)
    grupos: dict[int, list[str]] = {}
    for i, r in enumerate(itens):
        grupos.setdefault(raiz(i), []).append(r["nome"])
    if len(grupos) < 2:
        return []
    partes = [f"grupo {k}: " + ", ".join(nomes) for k, nomes in enumerate(grupos.values(), 1)]
    return ["as imagens parecem ser de personagens diferentes (pela cor) — confira: "
            + "; ".join(partes)]
