"""Testes T-MIX (aditamento E-PC1-1 a Frente D): mistura em luz linear
de dois tons medios distintos.

A bateria antiga nao misturava dois tons medios em nenhum teste: a
mistura ingenua em sRGB de 0,25 + 0,75 da 0,500000 e a correcta em
linear da 0,286699 - uma regressao dessa classe passava por tudo.

Este ficheiro e a casa julgada dos T-MIX-1...3 (E-PC1-1, secao 4).
Por despacho da integracao, o T-MIX-2 (caminho do VERTICE) executa ja
no passo 4, com o codigo que ele vigia (o C-COR01 cria a conversao na
amostragem; a mistura do caminho de vertice acontece na propagacao, que
media os vizinhos ja convertidos). O T-MIX-1 (bake) e o T-MIX-3
(pesos 0,25/0,75) entram no passo 6, neste mesmo ficheiro.
"""
import sys
import unittest
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d.cor import projecao as P, vertice as V  # noqa: E402

LIN_025 = 0.05087608817155679   # lin(0.25), EOTF sRGB exacta
LIN_075 = 0.5225215539683921    # lin(0.75)
TMIX2_ESPERADO = 0.2866988210699744  # (lin(0.25) + lin(0.75)) / 2


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


if __name__ == "__main__":
    unittest.main()
