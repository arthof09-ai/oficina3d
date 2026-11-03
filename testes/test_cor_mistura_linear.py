"""Testes T-MIX (aditamento E-PC1-1 a Frente D): mistura em luz linear
de dois tons medios distintos.

A bateria antiga nao misturava dois tons medios em nenhum teste: a
mistura ingenua em sRGB de 0,25 + 0,75 da 0,500000 e a correcta em
linear da 0,286699 - uma regressao dessa classe passava por tudo.

Este ficheiro e a casa julgada dos T-MIX-1...3 (E-PC1-1, secao 4).
Por despacho da integracao, o T-MIX-2 (caminho do VERTICE) executou
no passo 4, com o codigo que ele vigia (o C-COR01 cria a conversao na
amostragem; a mistura do caminho de vertice acontece na propagacao, que
media os vizinhos ja convertidos). O T-MIX-1 (bake) e o T-MIX-3
(pesos 0,25/0,75) entraram no passo 6, neste mesmo ficheiro - o
aditamento E-PC1-1 fecha aqui, com os tres testes executados e as
tres sabotagens de fecho corridas em copias descartaveis (registo no
relatorio do passo 6).
"""
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d.cor import projecao as P, vertice as V  # noqa: E402

LIN_025 = 0.05087608817155679   # lin(0.25), EOTF sRGB exacta
LIN_075 = 0.5225215539683921    # lin(0.75)
TMIX2_ESPERADO = 0.2866988210699744  # (lin(0.25) + lin(0.75)) / 2
TMIX1_ESPERADO = 0.5718735140718357  # bake: enc((lin(.25)+lin(.75))/2)
TMIX3_ESPERADO = 0.40461018751918326  # vertice: .25*lin(.25)+.75*lin(.75)
TMIX3_ENC = 0.6686320581212071        # bake R: enc(TMIX3_ESPERADO)
TMIX3_ENC_TROCADO = 0.44770228728154887  # bake G: enc(.75*lin(.25)+.25*lin(.75))


def _cena():
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


class TestMisturaLinearVertice(unittest.TestCase):
    def test_tmix2_dois_contribuintes_ponto_medio(self):
        # Dois contribuintes de vistas distintas (0,25 na frente,
        # 0,75 nas costas) pintam os vizinhos do vertice do polo; a
        # propagacao media os dois JA EM LINEAR -> 0,286699.
        # Ingenuo (misturar em sRGB): 0,500000. Converter depois de
        # misturar: lin(0,5) = 0,214041. Ambos teem de falhar aqui -
        # as sabotagens S-PC1-1/2/3 provam os dentes (registo do passo).
        verts, normais, centro = _cena()
        ortho = P.enquadramento((2.0, 2.0, 2.0), 100, 100)
        vistas = [_vista_solida("frente", 0.25), _vista_solida("costas", 0.75)]
        cores, fonte, _m, _i = V.amostrar_vertices(
            verts, normais, vistas, centro, ortho)
        self.assertEqual(fonte[0], V.FONTE_VISTA)
        self.assertEqual(fonte[1], V.FONTE_VISTA)
        np.testing.assert_allclose(cores[0], (LIN_025,) * 3, atol=1e-9)
        np.testing.assert_allclose(cores[1], (LIN_075,) * 3, atol=1e-9)
        faces = np.array([[0, 1, 4]])
        V.preencher_por_vizinhos(cores, fonte, faces)
        self.assertEqual(fonte[4], V.FONTE_PROPAGACAO)
        np.testing.assert_allclose(cores[4], (TMIX2_ESPERADO,) * 3, atol=1e-9)


def _quadro():
    """Quadrado no plano y=0 (x,z em [-1, 1]), normal para a camara
    da frente, UV cheia (a mesma cena de test_cor_bilinear)."""
    verts = np.array([[-1.0, 0.0, -1.0], [1.0, 0.0, -1.0],
                      [1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]])
    faces = np.array([[0, 1, 2], [0, 2, 3]])
    norm = np.tile(np.array([[0.0, -1.0, 0.0]]), (4, 1))
    fuv = np.array([[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
                    [[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]]])
    return verts, faces, norm, fuv


class TestMisturaLinearBake(unittest.TestCase):
    """T-MIX-1 (E-PC1-1, secao 4): mistura no BAKE, pares por canal.

    Imagem 1x2: pixel 0 = (0,25; 0,75; 0,5), pixel 1 = (0,75; 0,25;
    0,5) - R e G tem gradientes OPOSTOS sobre o mesmo par {0,25;
    0,75} (uma mistura que so prove um canal falha no outro) e B =
    0,5 nos dois pixels (controlo: sai 0,5). O override (1; 0,125;
    1; 0) poem a amostra do texel (ty=1, tx=1) em cx = 1,0 - entre
    os centros dos dois pixels (0,5 e 1,5), pesos 0,5/0,5 - e a do
    texel (ty=1, tx=2) em cx = 1,25 (pesos 0,25/0,75).
    """

    def _bake(self):
        img = np.array([[[0.25, 0.75, 0.5], [0.75, 0.25, 0.5]]])
        vista = {"vista": "frente", "imagem": img,
                 "mascara": np.ones((1, 2), dtype=bool),
                 "visivel": np.array([True, True]),
                 "peso_face": np.array([1.0, 1.0]),
                 "alinhamento": (1.0, 0.125, 1.0, 0.0)}
        verts, faces, norm, fuv = _quadro()
        return P.rasterizar_textura(
            verts, faces, norm, fuv, [vista], 4, np.zeros(3),
            (2.0, 2.0, 2.0), 2.0)

    def test_tmix1_bake_pesos_iguais(self):
        tex, pintado, _, _ = self._bake()
        self.assertTrue(pintado[1, 1])
        # R e G: enc((lin(0,25)+lin(0,75))/2) = 0,571874; B: 0,5.
        np.testing.assert_allclose(
            tex[1, 1], [TMIX1_ESPERADO, TMIX1_ESPERADO, 0.5], atol=1e-9)

    def test_tmix1_bake_pesos_025_075(self):
        # O mesmo par com pesos 0,25/0,75 (amostra em cx = 1,25):
        # R sai enc(0,404610) e G o valor de pesos TROCADOS
        # enc(0,168787) - uma transposicao de pesos troca R por G e
        # falha os dois canais ao mesmo tempo.
        tex, pintado, _, _ = self._bake()
        self.assertTrue(pintado[1, 2])
        np.testing.assert_allclose(
            tex[1, 2], [TMIX3_ENC, TMIX3_ENC_TROCADO, 0.5], atol=1e-9)


class TestMisturaLinearPesosVertice(unittest.TestCase):
    """T-MIX-3 (E-PC1-1, secao 4): pesos 0,25/0,75 no VERTICE.

    Amostrar a 1,25 (entre os centros 0,5 e 1,5) sobre o par
    (0,25; 0,75) devolve 0,25*lin(0,25) + 0,75*lin(0,75) =
    0,404610 em linear. Uma transposicao de pesos devolveria
    0,168787 - o teste distingue os dois (distancia 0,236).
    """

    def test_tmix3_pesos_025_075(self):
        img = np.array([[[0.25, 0.25, 0.25], [0.75, 0.75, 0.75]]])
        vista = {"vista": "frente", "imagem": img,
                 "mascara": np.ones((1, 2), dtype=bool),
                 "visivel": np.array([True])}
        verts = np.zeros((1, 3))
        normais = np.array([[0.0, -1.0, 0.0]])
        with patch.object(P, "projetar",
                          return_value=(np.array([1.25]),
                                        np.array([0.5]))),                 patch.object(P, "alinhamento_silhueta",
                             return_value=(1.0, 0.0, 1.0, 0.0)):
            cores, fonte, _m, _i = V.amostrar_vertices(
                verts, normais, [vista], np.zeros(3), 1.0)
        self.assertEqual(fonte[0], V.FONTE_VISTA)
        np.testing.assert_allclose(cores[0], [TMIX3_ESPERADO] * 3,
                                   atol=1e-9)


if __name__ == "__main__":
    unittest.main()
