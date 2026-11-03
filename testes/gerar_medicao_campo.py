"""Gerador da medicao vinculativa da divergencia de espaco de cor do
campo (PACOTE-T-COR-3 SS3.3; descarga de Metodo C-1 no julgamento do
pacote: a medicao corre nas DUAS variantes da fixture).

Sobre a fixture da cerca (6), o campo corre duas vezes, com grafo,
acoplamento, resolvedor, tolerancia e fronteira identicos:

- corrida **L** - o mecanismo do pacote (conversoes em P1/P2, luz
  linear), via ``aplicar_campo``;
- corrida **S** - o mesmo campo computado em sRGB (P1/P2 omitidos),
  composta aqui a partir das pecas do modulo - a corrida S existe SO
  para esta medicao: nao e um modo do job, nao entra em
  ``campo_difusao`` como caminho de producao, nenhum braco a usa.

Mede-se, sobre as incognitas da fixture (o territorio cego da faixa
Q1-Q3 e o triangulo cego da componente desligada - o conjunto de
SS3.2(a)), nos valores COMO ESCRITOS na textura pelas duas corridas:
Delta(t) = max sobre os canais de |L(t) - S(t)|. Publica-se a
distribuicao inteira: n, mediana, p95 (``numpy.percentile``,
interpolacao linear), maximo e o array de Delta ordenado, ao lado do
hash dos arrays de construcao da fixture de cada variante.

SEM LIMIAR - declarado (SS3.3): nenhum valor aprova nem chumba coisa
nenhuma; a medicao e obrigacao de publicacao, nao portao.

Variantes: ``binaria`` (a fixture de SS3.1, fronteira em {0,1} por
canal - P1 e a identidade e Delta mede so o efeito de P2) e
``intermedia`` (Q4 pintado com (0.5, 0.25, 0.75) - P1 exercitado, a
divergencia mede os dois pontos de conversao). Escreve
``testes/campo_divergencia.json``.

Uso: python testes/gerar_medicao_campo.py   (cwd indiferente)
"""
import json
import sys
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))
AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import campo_fixture as FX  # noqa: E402
from oficina3d.cor import campo_difusao as CD  # noqa: E402

SAIDA = AQUI / "campo_divergencia.json"


def _corrida_s(fx, produtos):
    """A corrida S (em sRGB): mesmas estruturas e resolvedor, com as
    conversoes omitidas (identidade nos dois pontos)."""
    _cores, _tem, _cont, _adj, cores_final, _anel, alc = produtos
    estruturas = CD.construir_acoplamento(
        fx["texel_face"], fx["pintado"], fx["faces"], fx["faces_uv"],
        fx["verts"], alc)
    x, _parcial = CD.resolver_campo(
        estruturas, fx["textura"], cores_final,
        converter_entrada=lambda v: np.asarray(v, dtype=np.float64))
    tex, _pin, aplicada = CD.escrever_campo(
        fx["textura"], fx["pintado"], estruturas, x,
        converter_saida=lambda v: np.asarray(v, dtype=np.float64))
    return tex, aplicada


def _medir(fx):
    produtos = FX.produtos_preenchimento(fx)
    _c, _t, _ct, _a, cores_final, _an, alc = produtos
    tex_l, _pin, aplicada, _rel = CD.aplicar_campo(
        fx["textura"], fx["pintado"], fx["texel_face"], fx["faces"],
        fx["faces_uv"], fx["verts"], alc, cores_final)
    tex_s, aplicada_s = _corrida_s(fx, produtos)
    assert (aplicada == aplicada_s).all(), \
        "as duas corridas divergem no conjunto de incognitas"
    delta = np.abs(tex_l[aplicada] - tex_s[aplicada]).max(axis=1)
    delta_ord = np.sort(delta)
    return {"fixture_sha256": FX.hash_fixture(fx),
            "n": int(len(delta_ord)),
            "mediana": float(np.percentile(delta_ord, 50)),
            "p95": float(np.percentile(delta_ord, 95)),
            "maximo": float(delta_ord.max()) if len(delta_ord) else 0.0,
            "delta": [float(v) for v in delta_ord]}


def main():
    doc = {
        "medicao": "divergencia de espaco de cor do campo (L linear x "
                   "S sRGB), PACOTE-T-COR-3 SS3.3 + descarga C-1 de "
                   "Metodo; sem limiar - obrigacao de publicacao",
        "variantes": {
            "binaria": _medir(FX.construir_fixture()),
            "intermedia": _medir(FX.construir_fixture(
                cor_q4=FX.COR_Q4_INTERMEDIA)),
        },
    }
    SAIDA.write_text(json.dumps(doc, indent=1, ensure_ascii=False),
                     encoding="utf-8")
    for nome, bloco in doc["variantes"].items():
        print("%s: n=%d mediana=%.6f p95=%.6f maximo=%.6f fixture=%s"
              % (nome, bloco["n"], bloco["mediana"], bloco["p95"],
                 bloco["maximo"], bloco["fixture_sha256"][:12]))
    print("escrito:", SAIDA)


if __name__ == "__main__":
    main()
