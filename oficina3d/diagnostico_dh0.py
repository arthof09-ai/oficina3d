"""D-H0: consistencia cruzada 2D das 4 vistas canonicas do Orc (P0, C-05).

Instrumento do diagnostico de raiz da D1, exigido pelo Critico do estudo
de raiz (docs/CRITICO-estudo-raiz-d1.md, C-05): antes de atribuir a
discordancia medida por D-H4.2 a registro (H1) ou a juncao (H4), verifica
se as proprias referencias concordam ENTRE SI.

O que este modulo faz (sem arte do RPG: so matematica + uma tabela de
coordenadas medida):
- mascara de primeiro plano pelo canal alfa, bbox, perfil de largura por
  faixa de altura, IoU de silhueta bbox-alinhada (esticado e preservando
  a razao de aspecto), sensibilidade do IoU ao limiar de alfa;
- normalizacao dos marcos medidos (tabela em
  ``diagnostico_dh0_dados.json``, caixas 0-1000 lidas por grounding com
  grade de referencial) para y em fracao da altura do bbox, e faixas
  (max-min) por marco entre as 4 vistas.

Regras de leitura registradas (pre-registradas antes de medir):
- faixa > 0,05 num marco de tronco = bandeira de inconsistencia;
  faixa > 0,10 = severa. O D-H0 atribui causa, nao aprova/reprova a D1.
- IoU frente x costas NAO prova inconsistencia: vistas opostas de um
  ser com capa grande nas costas e machado lateral tem assimetria
  legitima (capa visivel so por tras; machado na mao direita aparece
  a esquerda na frente e a direita nas costas). O IoU oposto e
  reportado, mas o juiz do D-H0 sao os marcos verticais e o IoU
  espelhado dos pares laterais.
- Lado horizontal do kit NAO se julga por espelhamento fisico: a REGRA
  FINAL do Orc (reconciliacao REF-01 lote 4, secao 5) manda o cranio
  sempre a DIREITA do losango em coordenadas de imagem, em qualquer
  vista. O teste e "cranio a direita da fivela em todas", nao espelho.
- Limiar de alfa 254 e INVALIDO nestas imagens: o platô de alfa do
  primeiro plano fica em 252-253 em 3 das 4 vistas (costas: 254-255);
  a sensibilidade usa os limiares 1, 128 e 200.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image

VISTAS = ("frente", "costas", "esquerda", "direita")
LIMIARES_SENSIBILIDADE = (1, 128, 200)
REGUA_FAIXA = 0.05
REGUA_SEVERA = 0.10
MARCOS_TRONCO = ("topknot", "buckle", "skull", "redtip")

AQUI = Path(__file__).resolve().parent


def carregar_dados(caminho=None):
    """Tabela de marcos medida (caixas 0-1000 + bbox em px + SHAs)."""
    caminho = Path(caminho) if caminho else AQUI / "diagnostico_dh0_dados.json"
    return json.loads(caminho.read_text(encoding="utf-8"))


def mascara_alfa(caminho, limiar=128):
    """Primeiro plano = alfa >= limiar (PNG RGBA com fundo transparente)."""
    im = np.array(Image.open(caminho).convert("RGBA"))
    return im[:, :, 3] >= limiar


def bbox_da_mascara(mask):
    """(x0, y0, x1, y1) inclusivos do primeiro plano."""
    ys, xs = np.where(mask)
    return (int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max()))


def recorta_redimensiona(mask, bb, tamanho=256, preservar_aspecto=False):
    """Recorte do bbox redimensionado para tamanho x tamanho (bool)."""
    x0, y0, x1, y1 = bb
    rec = mask[y0:y1 + 1, x0:x1 + 1]
    img = Image.fromarray((rec * 255).astype(np.uint8))
    if preservar_aspecto:
        h, w = rec.shape
        s = tamanho / max(h, w)
        nw, nh = max(1, round(w * s)), max(1, round(h * s))
        img = img.resize((nw, nh), Image.NEAREST)
        tela = Image.new("L", (tamanho, tamanho), 0)
        tela.paste(img, ((tamanho - nw) // 2, (tamanho - nh) // 2))
        img = tela
    else:
        img = img.resize((tamanho, tamanho), Image.NEAREST)
    return np.array(img) > 0


def iou(a, b):
    """IoU de duas mascaras booleanas do mesmo formato."""
    inter = np.logical_and(a, b).sum()
    uniao = np.logical_or(a, b).sum()
    return float(inter / uniao) if uniao else 0.0


def perfil_largura(mask, bb, faixas=100):
    """Largura ocupada por faixa de altura, em fracao da largura do bbox."""
    x0, y0, x1, y1 = bb
    rec = mask[y0:y1 + 1, x0:x1 + 1]
    h, w = rec.shape
    return [float(rec[i * h // faixas:(i + 1) * h // faixas].any(axis=0).sum() / w)
            for i in range(faixas)]


def normalizar_marco(bbox_px, y_1000, altura_imagem):
    """y (0-1000) -> fracao da altura do bbox (0 = topo, 1 = base)."""
    _, topo, _, base = bbox_px
    return ((y_1000 / 1000.0 * altura_imagem) - topo) / (base - topo)


def faixas_dos_marcos(dados):
    """{marco: {vista: y_norm}} + {marco: faixa} a partir da tabela."""
    altura = dados["altura_imagem"]
    por_marco = {}
    for marco in ("topknot", "buckle", "skull", "redtip", "knee"):
        valores = {}
        for vista in VISTAS:
            entrada = dados["vistas"][vista]
            bb = tuple(entrada["bbox_px"])
            # Cada caixa: [x_min, y_min, x_max, y_max] em 0-1000; o marco
            # usa o CENTRO vertical da caixa (topknot: centro tambem, para
            # todas as vistas usarem a mesma convencao).
            caixas = entrada["marcos"][marco]
            centros = [(c[1] + c[3]) / 2 for c in caixas]
            if marco == "knee":
                valores[vista] = [round(normalizar_marco(bb, c, altura), 4)
                                  for c in centros]
            else:
                valores[vista] = round(
                    normalizar_marco(bb, centros[0], altura), 4)
        por_marco[marco] = valores
    faixas = {}
    for marco, valores in por_marco.items():
        todos = [v for lista in valores.values()
                 for v in (lista if isinstance(lista, list) else [lista])]
        faixas[marco] = round(max(todos) - min(todos), 4)
    return por_marco, faixas


def medir_vistas(pasta_imagens, dados=None):
    """Geometria completa das 4 vistas (exige as imagens; fora dos testes)."""
    dados = dados or carregar_dados()
    pasta = Path(pasta_imagens)
    resultado = {"vistas": {}, "iou": {}, "sensibilidade_limiar": {}}
    mascaras = {}
    for vista in VISTAS:
        caminho = pasta / f"orc_{vista}.png"
        m = mascara_alfa(caminho, 128)
        bb = bbox_da_mascara(m)
        x0, y0, x1, y1 = bb
        resultado["vistas"][vista] = {
            "bbox": list(bb),
            "bbox_largura": x1 - x0 + 1,
            "bbox_altura": y1 - y0 + 1,
            "razao_largura_altura": round((x1 - x0 + 1) / (y1 - y0 + 1), 4),
            "ocupacao_bbox": round(float(m[y0:y1 + 1, x0:x1 + 1].mean()), 4),
            "perfil_largura_100": [round(v, 4) for v in perfil_largura(m, bb)],
        }
        mascaras[vista] = (m, bb)
    for (a, b), espelhar in [(("frente", "costas"), False),
                             (("esquerda", "direita"), False),
                             (("esquerda", "direita"), True)]:
        for modo, preservar in [("esticado", False), ("aspecto", True)]:
            ma = recorta_redimensiona(mascaras[a][0], mascaras[a][1],
                                      preservar_aspecto=preservar)
            mb = recorta_redimensiona(mascaras[b][0], mascaras[b][1],
                                      preservar_aspecto=preservar)
            if espelhar:
                mb = np.fliplr(mb)
            chave = f"{a}_x_{b}{'_espelhado' if espelhar else ''}_{modo}"
            resultado["iou"][chave] = round(iou(ma, mb), 4)
    for limiar in LIMIARES_SENSIBILIDADE:
        ms = {v: mascara_alfa(pasta / f"orc_{v}.png", limiar) for v in VISTAS}
        bbs = {v: bbox_da_mascara(ms[v]) for v in VISTAS}
        fa = recorta_redimensiona(ms["frente"], bbs["frente"])
        fb = recorta_redimensiona(ms["costas"], bbs["costas"])
        resultado["sensibilidade_limiar"][str(limiar)] = round(iou(fa, fb), 4)
    por_marco, faixas = faixas_dos_marcos(dados)
    resultado["marcos_y_norm"] = por_marco
    resultado["marcos_faixa"] = faixas
    return resultado


if __name__ == "__main__":  # pragma: no cover - CLI de diagnostico
    import sys
    print(json.dumps(medir_vistas(sys.argv[1]), indent=2, ensure_ascii=False))
