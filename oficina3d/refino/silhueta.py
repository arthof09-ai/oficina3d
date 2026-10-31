"""Nota de fidelidade por silhueta (IoU) — Python puro, sem numpy nem Pillow.

Máscaras são listas de linhas (``list[list[int|bool]]``), 1 = objeto, 0 = fundo.
Internamente cada linha vira um inteiro (bitset), o que deixa a busca de alinhamento
rápida mesmo em Python puro (``int.bit_count``).

Régua única (plano v2, E12): todas as notas de todos os motores usam os MESMOS
parâmetros (``REGUA``). Mudou a régua → mude ``REGUA["versao"]``, senão notas
antigas e novas deixam de ser comparáveis.

A nota principal (``nota_iou``) usa só as vistas LATERAIS e de COSTAS: o IoU de
frente sai inflado porque o motor vê a imagem de frente (na v1 o TripoSR "grumoso"
tirou 0,88 de frente e 0,60 de lado).
"""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

REGUA = {
    "versao": "iou-v2.0",
    "limiar_alfa": 10,          # pixel da imagem conta como objeto se alfa > 10 (como na v1)
    "altura_px": 192,           # as duas silhuetas são levadas a esta altura (pés à cabeça)
    "escalas": (0.94, 0.97, 1.0, 1.03, 1.06),   # ajuste fino de escala do modelo
    "desloc_px": 4,             # ajuste fino de translação (± px, em x e em y)
    "margem_px": 8,
}

VISTAS_LATERAIS = ("esquerda", "direita")
VISTA_COSTAS = "costas"
# Vistas para as quais faz sentido comparar silhueta (as 8 direções).
VISTAS_IOU = (
    "frente", "costas", "esquerda", "direita",
    "frente-esquerda", "frente-direita", "costas-esquerda", "costas-direita",
)


# ----------------------------------------------------------------------------
# Operações básicas em máscaras (listas puras)
# ----------------------------------------------------------------------------
def _dimensoes(m) -> tuple[int, int]:
    altura = len(m)
    largura = len(m[0]) if altura else 0
    for linha in m:
        if len(linha) != largura:
            raise ValueError("máscara irregular: linhas com larguras diferentes")
    return largura, altura


def iou(a, b) -> float:
    """IoU (interseção / união) de duas máscaras do MESMO tamanho.

    Duas máscaras vazias dão 0,0 (não há o que comparar; quem chama deve avisar).
    """
    la, ha = _dimensoes(a)
    lb, hb = _dimensoes(b)
    if (la, ha) != (lb, hb):
        raise ValueError(f"máscaras de tamanhos diferentes: {la}x{ha} e {lb}x{hb}")
    inter = uniao = 0
    for linha_a, linha_b in zip(a, b):
        for pa, pb in zip(linha_a, linha_b):
            pa = bool(pa)
            pb = bool(pb)
            inter += pa and pb
            uniao += pa or pb
    return inter / uniao if uniao else 0.0


def caixa(m) -> tuple[int, int, int, int] | None:
    """Caixa envolvente (x0, y0, x1, y1), com x1/y1 exclusivos; None se vazia."""
    xs0, xs1, ys = [], [], []
    for y, linha in enumerate(m):
        idx = [x for x, p in enumerate(linha) if p]
        if idx:
            ys.append(y)
            xs0.append(idx[0])
            xs1.append(idx[-1])
    if not ys:
        return None
    return min(xs0), ys[0], max(xs1) + 1, ys[-1] + 1


def recortar(m):
    """Recorta a máscara na caixa do objeto (lista vazia se não houver objeto)."""
    c = caixa(m)
    if c is None:
        return []
    x0, y0, x1, y1 = c
    return [[1 if p else 0 for p in linha[x0:x1]] for linha in m[y0:y1]]


def redimensionar(m, largura: int, altura: int):
    """Redimensiona por vizinho mais próximo (centro do pixel)."""
    lo, ho = _dimensoes(m)
    if lo == 0 or ho == 0:
        raise ValueError("máscara vazia")
    largura = max(1, int(largura))
    altura = max(1, int(altura))
    xs = [min(lo - 1, int((x + 0.5) * lo / largura)) for x in range(largura)]
    out = []
    for y in range(altura):
        linha = m[min(ho - 1, int((y + 0.5) * ho / altura))]
        out.append([1 if linha[x] else 0 for x in xs])
    return out


def espelhar(m):
    """Espelha na horizontal (esquerda <-> direita da imagem)."""
    return [list(reversed(linha)) for linha in m]


def area(m) -> int:
    return sum(1 for linha in m for p in linha if p)


# ----------------------------------------------------------------------------
# Bitsets: cada linha vira um int (bit x = pixel x)
# ----------------------------------------------------------------------------
def _linha_int(linha) -> int:
    v = 0
    for x, p in enumerate(linha):
        if p:
            v |= 1 << x
    return v


def _contar(v: int) -> int:
    try:
        return v.bit_count()            # Python 3.10+
    except AttributeError:              # pragma: no cover
        return bin(v).count("1")


def _colocar(m_rec, largura_tela: int, altura_tela: int, x0: int, y_base: int) -> list[int]:
    """Põe a máscara recortada numa tela, com o canto esquerdo em x0 e a base em y_base."""
    tela = [0] * altura_tela
    h = len(m_rec)
    for i, linha in enumerate(m_rec):
        y = y_base - h + i
        if 0 <= y < altura_tela:
            v = _linha_int(linha)
            v = v << x0 if x0 >= 0 else v >> -x0
            tela[y] = v & ((1 << largura_tela) - 1)
    return tela


def _iou_bits(ref: list[int], mod: list[int], dx: int, dy: int, mascara_largura: int) -> float:
    inter = uniao = 0
    n = len(ref)
    for y in range(n):
        ys = y - dy
        mv = mod[ys] if 0 <= ys < n else 0
        if mv:
            mv = (mv << dx if dx >= 0 else mv >> -dx) & mascara_largura
        rv = ref[y]
        if rv or mv:
            inter += _contar(rv & mv)
            uniao += _contar(rv | mv)
    return inter / uniao if uniao else 0.0


def iou_alinhado(mascara_ref, mascara_modelo, regua: dict | None = None, espelho: bool = True) -> dict:
    """IoU depois de alinhar a silhueta do modelo à da imagem.

    1. Recorta as duas na caixa do objeto.
    2. Leva as duas à mesma altura (``altura_px``) mantendo a proporção; base (pés)
       alinhada e centros horizontais alinhados.
    3. Busca pequena de escala (``escalas``) e translação (±``desloc_px``) no modelo.

    Retorna ``{"iou", "escala", "dx", "dy", "iou_espelhada", "tela": (larg, alt),
    "ref": bits, "modelo": bits}`` (as duas últimas para a imagem de comparação).
    ``iou_espelhada`` é a mesma busca com o modelo espelhado: se for bem maior que
    ``iou``, a etiqueta esquerda/direita da imagem provavelmente está trocada.
    """
    r = dict(REGUA)
    if regua:
        r.update(regua)
    ref = recortar(mascara_ref)
    mod = recortar(mascara_modelo)
    if not ref or not mod:
        return {"iou": 0.0, "escala": None, "dx": 0, "dy": 0, "iou_espelhada": None,
                "vazia": "imagem" if not ref else "modelo"}

    H = int(r["altura_px"])
    lr, hr = _dimensoes(ref)
    lm, hm = _dimensoes(mod)
    ref_n = redimensionar(ref, round(lr * H / hr), H)
    larg_ref = len(ref_n[0])

    escalas = tuple(r["escalas"])
    d = int(r["desloc_px"])
    margem = int(r["margem_px"])
    s_max = max(escalas)
    larg_mod_max = max(1, round(lm * H * s_max / hm))
    largura = max(larg_ref, larg_mod_max) + 2 * (margem + d)
    altura = round(H * s_max) + 2 * (margem + d)
    y_base = altura - margem - d
    cx = largura // 2
    mascara_largura = (1 << largura) - 1

    ref_bits = _colocar(ref_n, largura, altura, cx - larg_ref // 2, y_base)

    def buscar(mod_rec) -> tuple[float, float, int, int, list[int]]:
        melhor = (-1.0, 1.0, 0, 0, [])
        for s in escalas:
            hm_s = max(1, round(H * s))
            lm_s = max(1, round(lm * hm_s / hm))
            m_n = redimensionar(mod_rec, lm_s, hm_s)
            bits = _colocar(m_n, largura, altura, cx - lm_s // 2, y_base)
            for dy in range(-d, d + 1):
                for dx in range(-d, d + 1):
                    v = _iou_bits(ref_bits, bits, dx, dy, mascara_largura)
                    if v > melhor[0]:
                        melhor = (v, s, dx, dy, bits)
        return melhor

    v, s, dx, dy, bits = buscar(mod)
    v_esp = buscar(espelhar(mod))[0] if espelho else None
    # Bits do modelo já deslocados, para a imagem de comparação.
    mod_final = []
    for y in range(altura):
        ys = y - dy
        mv = bits[ys] if 0 <= ys < altura else 0
        mod_final.append((mv << dx if dx >= 0 else mv >> -dx) & mascara_largura)
    return {"iou": round(v, 4), "escala": s, "dx": dx, "dy": dy,
            "iou_espelhada": round(v_esp, 4) if v_esp is not None else None,
            "tela": (largura, altura), "ref": ref_bits, "modelo": mod_final}


# ----------------------------------------------------------------------------
# Nota (lateral + costas)
# ----------------------------------------------------------------------------
def _media(valores):
    valores = [float(v) for v in valores if v is not None]
    return sum(valores) / len(valores) if valores else None


def nota_iou(silhueta_iou: dict) -> dict:
    """Resume os IoU por vista.

    - ``iou_lateral`` = média de esquerda e direita (as que existirem);
    - ``iou_costas`` = costas;
    - ``nota_iou`` = média de ``iou_lateral`` e ``iou_costas`` (as que existirem);
      None se não houver nem lateral nem costas (a frente sozinha NÃO vira nota).
    """
    lateral = _media(silhueta_iou.get(v) for v in VISTAS_LATERAIS)
    costas = silhueta_iou.get(VISTA_COSTAS)
    nota = _media([lateral, costas])
    arred = lambda x: round(x, 4) if x is not None else None  # noqa: E731
    return {"iou_lateral": arred(lateral), "iou_costas": arred(costas), "nota_iou": arred(nota)}


# ----------------------------------------------------------------------------
# Arquivos: PBM (máscaras vindas do Blender) e PNG (comparação), sem dependências
# ----------------------------------------------------------------------------
def ler_pbm(caminho) -> list[list[int]]:
    """Lê PBM binário (P4) ou texto (P1). 1 = preto = objeto."""
    dados = Path(caminho).read_bytes()
    tokens, pos = [], 0

    def proximo_token():
        nonlocal pos
        while pos < len(dados):
            c = dados[pos:pos + 1]
            if c == b"#":
                while pos < len(dados) and dados[pos:pos + 1] not in (b"\n", b"\r"):
                    pos += 1
            elif c.isspace():
                pos += 1
            else:
                break
        ini = pos
        while pos < len(dados) and not dados[pos:pos + 1].isspace():
            pos += 1
        return dados[ini:pos]

    magico = proximo_token()
    largura = int(proximo_token())
    altura = int(proximo_token())
    if magico == b"P4":
        pos += 1  # um único espaço em branco antes dos dados
        bpl = (largura + 7) // 8
        m = []
        for y in range(altura):
            linha_b = dados[pos + y * bpl: pos + (y + 1) * bpl]
            if len(linha_b) < bpl:
                raise ValueError(f"PBM truncado: {caminho}")
            v = int.from_bytes(linha_b, "big")
            desloc = bpl * 8 - 1
            m.append([(v >> (desloc - x)) & 1 for x in range(largura)])
        return m
    if magico == b"P1":
        bits = [int(c) for c in dados[pos:].decode("ascii") if c in "01"]
        if len(bits) < largura * altura:
            raise ValueError(f"PBM truncado: {caminho}")
        return [bits[y * largura:(y + 1) * largura] for y in range(altura)]
    raise ValueError(f"não é PBM (P1/P4): {caminho}")


def salvar_pbm(m, caminho) -> Path:
    largura, altura = _dimensoes(m)
    bpl = (largura + 7) // 8
    corpo = bytearray()
    for linha in m:
        v = 0
        for x, p in enumerate(linha):
            if p:
                v |= 1 << (bpl * 8 - 1 - x)
        corpo += v.to_bytes(bpl, "big")
    caminho = Path(caminho)
    caminho.write_bytes(f"P4\n{largura} {altura}\n".encode("ascii") + bytes(corpo))
    return caminho


def salvar_png(pixels, caminho, canais: int = 3) -> Path:
    """Grava PNG 8 bits (RGB ou RGBA). ``pixels``: linhas de tuplas (r, g, b[, a])."""
    if canais not in (3, 4):
        raise ValueError("canais deve ser 3 ou 4")
    largura, altura = _dimensoes(pixels)
    bruto = bytearray()
    for linha in pixels:
        bruto.append(0)  # filtro "nenhum"
        for px in linha:
            bruto.extend(int(c) & 255 for c in px[:canais])

    def bloco(tipo: bytes, dados: bytes) -> bytes:
        return (struct.pack(">I", len(dados)) + tipo + dados
                + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF))

    tipo_cor = 2 if canais == 3 else 6
    png = (b"\x89PNG\r\n\x1a\n"
           + bloco(b"IHDR", struct.pack(">IIBBBBB", largura, altura, 8, tipo_cor, 0, 0, 0))
           + bloco(b"IDAT", zlib.compress(bytes(bruto), 6))
           + bloco(b"IEND", b""))
    caminho = Path(caminho)
    caminho.write_bytes(png)
    return caminho


# Cores da imagem de comparação.
COR_AMBOS = (235, 235, 235)
COR_SO_IMAGEM = (60, 120, 255)    # azul: a imagem tem, o modelo não (faltou volume)
COR_SO_MODELO = (240, 70, 50)     # vermelho: o modelo tem, a imagem não (sobrou volume)
COR_FUNDO = (32, 32, 36)


def salvar_comparacao(resultado: dict, caminho, ampliar: int = 2) -> Path | None:
    """Imagem com as duas silhuetas sobrepostas (cores acima). None se não há dados."""
    if "tela" not in resultado:
        return None
    largura, altura = resultado["tela"]
    ref, mod = resultado["ref"], resultado["modelo"]
    linhas = []
    for y in range(altura):
        rv, mv = ref[y], mod[y]
        linha = []
        for x in range(largura):
            r = (rv >> x) & 1
            m = (mv >> x) & 1
            cor = COR_AMBOS if r and m else COR_SO_IMAGEM if r else COR_SO_MODELO if m else COR_FUNDO
            linha.extend([cor] * ampliar)
        linhas.extend([linha] * ampliar)
    return salvar_png(linhas, caminho, 3)


def mascara_de_png(caminho, limiar: int | None = None):
    """Máscara de um PNG RGBA (alfa > limiar) usando Pillow — utilitário opcional.

    O caminho principal do refino NÃO usa isto: o Blender lê as imagens e grava PBM,
    para que a régua seja a mesma com ou sem Pillow instalado.
    """
    from PIL import Image  # import preguiçoso

    limiar = REGUA["limiar_alfa"] if limiar is None else limiar
    with Image.open(caminho) as im:
        alfa = im.convert("RGBA").getchannel("A")
        largura, altura = alfa.size
        dados = list(alfa.getdata())
    return [[1 if dados[y * largura + x] > limiar else 0 for x in range(largura)] for y in range(altura)]
