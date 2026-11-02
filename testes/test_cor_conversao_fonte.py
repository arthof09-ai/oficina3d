"""Testes do C-COR01 (Frente D, passo 4): conversao sRGB -> linear
POR FONTE na etapa de cor de vertice (pacote de execucao da Frente D,
secao 4, testes D-5 escritos COM o codigo).

Desenho julgado: a cor da VISTA (fonte sRGB - o PNG lido por
``ler_imagem`` entrega byte/255, sem linearizar na carga; portao D-3 do
passo 3, medido dentro do Blender) e convertida na amostragem, em
``amostrar_vertices``. A cor da FORMA (COLOR_0 do GLB de origem) ja e
linear por especificacao glTF e NUNCA e convertida - converter os dois
lados criaria o defeito simetrico. A propagacao media valores ja no
mesmo espaco (linear). Nenhuma conversao acontece na carga.

Os tres testes discriminam porque usam tons medios: nos canais 0/1 da
bateria sintetica antiga, sRGB e linear coincidem e nada disto se ve.
"""
import sys
import unittest
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d.cor import projecao as P, vertice as V  # noqa: E402

# EOTF sRGB exacta, calculada a mao (float64):
# lin(c) = c/12.92 se c <= 0.04045, senao ((c+0.055)/1.055)**2.4
LIN_025 = 0.05087608817155679   # lin(0.25)
LIN_050 = 0.21404114048223255   # lin(0.5)
LIN_075 = 0.5225215539683921    # lin(0.75)


def _cena():
    # Mesma cena dos testes do T2: 4 vertices voltados para as vistas
    # canonicas + polos de cima e de baixo (extensao vertical da caixa).
    centro = np.array([0.0, 0.0, 1.0])
    verts, normais = [], []
    for nome in ("frente", "costas", "esquerda", "direita"):
        d = np.array(P.direcao_camera(nome))
        verts.append(centro + d)
        normais.append(d)
    for d in (np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0])):
        verts.append(centro + d)
        normais.append(d)
    return np.array(verts), np.array(normais), centro


def _vista_solida(nome, tom, n=6):
    img = np.full((100, 100, 3), float(tom), dtype=np.float64)
    return {"vista": nome, "imagem": img,
            "mascara": np.ones((100, 100), dtype=bool),
            "visivel": np.ones(n, dtype=bool)}


class TestConversaoPorFonteD5(unittest.TestCase):
    def test_d5_1_meio_tom_discriminante(self):
        # Vista sintetica com cinza 0,5 (sRGB): o COLOR_0 tem de sair
        # LINEAR (~0,214), nao 0,5. E o teste que reprova o codigo
        # pre-C-COR01 e aprova o corrigido.
        verts, normais, centro = _cena()
        ortho = P.enquadramento((2.0, 2.0, 2.0), 100, 100)
        cores, fonte, _m, _i = V.amostrar_vertices(
            verts, normais, [_vista_solida("frente", 0.5)], centro, ortho)
        self.assertEqual(fonte[0], V.FONTE_VISTA)
        np.testing.assert_allclose(cores[0], (LIN_050,) * 3, atol=1e-9)
        # Referencias do helper puro (a constante julgada da tranche):
        self.assertEqual(float(V.srgb_para_linear(0.0)), 0.0)
        self.assertEqual(float(V.srgb_para_linear(1.0)), 1.0)
        np.testing.assert_allclose(float(V.srgb_para_linear(0.25)), LIN_025, atol=1e-12)
        np.testing.assert_allclose(float(V.srgb_para_linear(0.5)), LIN_050, atol=1e-12)
        np.testing.assert_allclose(float(V.srgb_para_linear(0.75)), LIN_075, atol=1e-12)
        np.testing.assert_allclose(float(V.srgb_para_linear(0.04045)),
                                   0.04045 / 12.92, atol=1e-12)
        np.testing.assert_allclose(
            V.srgb_para_linear(np.array([0.25, 0.5, 0.75])),
            (LIN_025, LIN_050, LIN_075), atol=1e-12)

    def test_d5_2_forma_nao_convertida(self):
        # Vertice pintado so pela forma mantem o valor do COLOR_0 de
        # entrada BYTE A BYTE (igualdade exacta): guarda contra a
        # conversao global/simmetrica. Um valor de forma 0,5 tem de
        # ficar 0,5 - se a forma fosse convertida, sairia 0,214.
        cores = np.zeros((3, 3))
        fonte = np.array([V.FONTE_VISTA, V.FONTE_NENHUMA, V.FONTE_NENHUMA],
                         dtype=np.int8)
        cores[0] = (1.0, 0.0, 0.0)
        forma = np.array([
            [0.0, 1.0, 0.0],
            [0.21586050011389926, 0.3333333333333333, 0.7171717171717171],
            [0.04045, 0.9999999999999999, 0.12345678901234568],
        ])
        n = V.mesclar_forma(cores, fonte, forma)
        self.assertEqual(n, 2)
        np.testing.assert_array_equal(cores[1], forma[1])
        np.testing.assert_array_equal(cores[2], forma[2])
        np.testing.assert_array_equal(cores[0], (1.0, 0.0, 0.0))
        # Ponta a ponta: sem nenhuma vista, amostragem + mescla deixam
        # a cor da forma intacta em todos os vertices.
        verts, normais, centro = _cena()
        ortho = P.enquadramento((2.0, 2.0, 2.0), 100, 100)
        cores2, fonte2, _m, _i = V.amostrar_vertices(
            verts, normais, [], centro, ortho)
        forma2 = np.tile(np.array([0.21586050011389926, 0.5, 0.04045]), (6, 1))
        V.mesclar_forma(cores2, fonte2, forma2)
        np.testing.assert_array_equal(cores2, forma2)

    def test_d5_3_propagacao_espaco_unico(self):
        # Vizinhos vista + forma propagam SEM salto de espaco: a media
        # e calculada sobre valores ja em linear (a vista convertida na
        # amostragem; a forma crua, porque ja e linear).
        verts, normais, centro = _cena()
        ortho = P.enquadramento((2.0, 2.0, 2.0), 100, 100)
        cores, fonte, _m, _i = V.amostrar_vertices(
            verts, normais, [_vista_solida("frente", 0.5)], centro, ortho)
        np.testing.assert_allclose(cores[0], (LIN_050,) * 3, atol=1e-9)
        # Vertice 1 coberto pela forma com 0,3 (valor linear de COLOR_0;
        # a mescla byte a byte esta provada no D-5/2 - aqui o estado e
        # montado directo para isolar a propagacao).
        cores[1] = (0.3, 0.3, 0.3)
        fonte[1] = V.FONTE_FORMA
        faces = np.array([[0, 1, 4]])
        n, _passes = V.preencher_por_vizinhos(cores, fonte, faces)
        self.assertEqual(n, 1)
        self.assertEqual(fonte[4], V.FONTE_PROPAGACAO)
        esperado = (LIN_050 + 0.3) / 2.0  # 0.25702057024111624, em linear
        np.testing.assert_allclose(cores[4], (esperado,) * 3, atol=1e-9)


if __name__ == "__main__":
    unittest.main()
