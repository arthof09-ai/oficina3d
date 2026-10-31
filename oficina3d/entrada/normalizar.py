"""Normalização para o motor: RGBA, recorte no objeto, margem ~8%, quadrado transparente 1024²."""
from __future__ import annotations

from .dependencias import exigir
from .imagem import ALFA_FRACO, caixa, limpar_alfa, mascara

LADO = 1024
MARGEM = 0.08            # de cada lado, em fração do quadro
AMPLIACAO_MAXIMA = 2.0   # não inventar detalhe: imagens pequenas sobem no máximo 2x


def recortar(arr, mask, margem_px: int = 0):
    """Zera o alfa fora de `mask` e recorta na caixa da máscara (+ margem, sem sair da imagem)."""
    np = exigir("numpy", "recortar imagens")
    cx = caixa(mask)
    if cx is None:
        return None
    x0, y0, x1, y1 = cx
    h, w = mask.shape
    x0, y0 = max(0, x0 - margem_px), max(0, y0 - margem_px)
    x1, y1 = min(w - 1, x1 + margem_px), min(h - 1, y1 + margem_px)
    parte = arr[y0:y1 + 1, x0:x1 + 1].copy()
    fora = ~mask[y0:y1 + 1, x0:x1 + 1]
    parte[fora] = 0
    return np.ascontiguousarray(parte)


def normalizar(arr, lado: int = LADO, margem: float = MARGEM,
               ampliacao_maxima: float = AMPLIACAO_MAXIMA):
    """Devolve (array lado×lado RGBA, info).

    info = {"escala": float, "ampliacao_limitada": bool, "objeto_px": [w, h] no quadro final,
            "objeto_origem_px": [w, h]}.
    Redimensiona com alfa pré-multiplicado (sem halo escuro/claro na borda).
    """
    np = exigir("numpy", "normalizar imagens")
    Image = exigir("PIL.Image", "normalizar imagens")
    cx = caixa(mascara(arr, ALFA_FRACO))
    if cx is None:
        raise ValueError("imagem vazia: nenhum pixel com alfa > 10")
    x0, y0, x1, y1 = cx
    recorte = arr[y0:y1 + 1, x0:x1 + 1]
    h, w = recorte.shape[:2]
    util = lado * (1.0 - 2.0 * margem)
    escala = util / float(max(w, h))
    limitada = False
    if escala > ampliacao_maxima:
        escala, limitada = ampliacao_maxima, True
    nw = max(1, min(lado, int(round(w * escala))))
    nh = max(1, min(lado, int(round(h * escala))))
    im = Image.fromarray(np.ascontiguousarray(recorte), "RGBA")
    if (nw, nh) != (w, h):
        filtro = getattr(Image, "Resampling", Image).LANCZOS
        im = im.convert("RGBa").resize((nw, nh), filtro).convert("RGBA")
    quadro = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    quadro.paste(im, ((lado - nw) // 2, (lado - nh) // 2))
    out = limpar_alfa(np.array(quadro, dtype=np.uint8))
    info = {"escala": round(escala, 4), "ampliacao_limitada": limitada,
            "objeto_px": [nw, nh], "objeto_origem_px": [w, h]}
    return out, info
