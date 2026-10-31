"""Leitura/gravação de imagens e medidas do canal alfa (numpy + Pillow, importados aqui dentro)."""
from __future__ import annotations

from pathlib import Path

from .dependencias import exigir

ALFA_FRACO = 10          # alfa <= 10 conta como fundo (achado da v1 no Capríleo)
EXTENSOES = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def _np():
    return exigir("numpy", "preparar imagens (entrada)")


def _pil():
    return exigir("PIL.Image", "abrir e gravar imagens (entrada)")


def abrir_rgba(caminho: Path):
    """Abre qualquer imagem como array RGBA uint8 (H, W, 4).

    Devolve (array, tinha_alfa). Aplica a rotação do EXIF (fotos de celular).
    """
    np = _np()
    Image = _pil()
    ImageOps = exigir("PIL.ImageOps", "abrir imagens (entrada)")
    with Image.open(caminho) as im:
        im.load()
        tinha_alfa = im.mode in ("RGBA", "LA", "PA", "RGBa", "La") or "transparency" in im.info
        try:
            im = ImageOps.exif_transpose(im)
        except Exception:      # EXIF quebrado não impede o uso da imagem
            pass
        if im.mode in ("I;16", "I;16B", "I;16L", "I"):
            im = im.convert("I").point(lambda v: v * (1 / 256)).convert("L")
        rgba = im.convert("RGBA")
        arr = np.array(rgba, dtype=np.uint8)
    return arr, bool(tinha_alfa)


def salvar_png(arr, caminho: Path) -> None:
    Image = _pil()
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    Image.fromarray(arr, "RGBA").save(caminho, format="PNG", optimize=False)


def mascara(arr, limite: int = ALFA_FRACO):
    """Máscara booleana do objeto (alfa > limite)."""
    return arr[..., 3] > limite


def caixa(mask):
    """(x0, y0, x1, y1) inclusivos da máscara, ou None se vazia."""
    np = _np()
    linhas = np.flatnonzero(mask.any(axis=1))
    colunas = np.flatnonzero(mask.any(axis=0))
    if linhas.size == 0 or colunas.size == 0:
        return None
    return int(colunas[0]), int(linhas[0]), int(colunas[-1]), int(linhas[-1])


def estatisticas_alfa(arr) -> dict:
    """Frações de pixels por faixa de alfa."""
    np = _np()
    a = arr[..., 3]
    total = float(a.size) or 1.0
    objeto = a > ALFA_FRACO
    n_obj = int(np.count_nonzero(objeto))
    return {
        "opaco": float(np.count_nonzero(a >= 250)) / total,
        "transparente": float(np.count_nonzero(a <= ALFA_FRACO)) / total,
        "fraco": float(np.count_nonzero((a >= 1) & (a <= ALFA_FRACO))) / total,
        "objeto": n_obj / total,
        # parte do OBJETO que ficou semitransparente (recorte incerto do rembg)
        "semi_no_objeto": (float(np.count_nonzero(objeto & (a < 200))) / n_obj) if n_obj else 0.0,
    }


def limpar_alfa(arr, limite: int = ALFA_FRACO):
    """Alfa <= limite vira 0 e o RGB dos pixels transparentes vira 0 (fundo limpo). Devolve cópia."""
    out = arr.copy()
    fundo = out[..., 3] <= limite
    out[fundo] = 0
    return out


def pct(fracao: float) -> str:
    """0.579 -> '57,9%'."""
    return f"{fracao * 100:.1f}".replace(".", ",") + "%"
