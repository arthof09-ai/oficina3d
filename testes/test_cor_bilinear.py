"""Testes do passo 6 da Frente D (C-COR02): amostragem bilinear em
luz linear nos DOIS caminhos (bake T1 em ``projecao`` e cor de
vertice em ``vertice``).

Pacote julgado, secao 6 - os 3 testes novos:
1. **Gradiente conhecido**: imagem 2x2, amostra no centro -> valor
   bilinear exacto calculado a mao, nos dois caminhos (aqui).
2. **Fronteira preto/branco**: a mistura em linear separa-se da
   mistura em sRGB - endurecido pelo aditamento E-PC1-1 nos testes
   T-MIX-1..3, em ``test_cor_mistura_linear.py``.
3. **Regressao A0 + determinismo**: o centro continua subtraido com
   o bilinear ligado; pesos fixos, sem dependencia de ordem (aqui).

Controlos deste passo: o modo ``amostragem='seco'`` (amostragem
pontual pre-C-COR02) byte-exacto nos dois caminhos, e a paridade das
duas copias da EOTF (``projecao.srgb_para_linear`` ==
``vertice.srgb_para_linear`` - a duplicacao e forcada pelo ciclo de
imports e fica presa por este teste).
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

SRGB_MEIO = 0.7353569830524495  # sRGB(0,5 em linear), calculado a mao
LIN_075 = 0.5225215539683921    # lin(0,75), EOTF sRGB exacta


def _quadro():
    """Quadrado no plano y=0 (x,z em [-1, 1]), normal para a camara
    da frente, UV cheia. Centro na origem; ortho 2."""
    verts = np.array([[-1.0, 0.0, -1.0], [1.0, 0.0, -1.0],
                      [1.0, 0.0, 1.0], [-1.0, 0.0, 1.0]])
    faces = np.array([[0, 1, 2], [0, 2, 3]])
    norm = np.tile(np.array([[0.0, -1.0, 0.0]]), (4, 1))
    fuv = np.array([[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
                    [[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]]])
    return verts, faces, norm, fuv


def _bake_gradiente(amostragem="bilinear"):
    """Cena do gradiente: imagem 2x2 de cantos puros; o override de
    alinhamento poem o texel (1, 1) exactamente no centro da imagem
    (coordenada continua (1, 0; 1, 0) -> pesos 0,5/0,5 nos 4 cantos).
    """
    img = np.array([[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
                    [[0.0, 0.0, 1.0], [1.0, 1.0, 1.0]]])
    vista = {"vista": "frente", "imagem": img,
             "mascara": np.ones((2, 2), dtype=bool),
             "visivel": np.array([True, True]),
             "peso_face": np.array([1.0, 1.0]),
             "alinhamento": (1.0, 0.25, 1.0, 0.25)}
    verts, faces, norm, fuv = _quadro()
    return P.rasterizar_textura(
        verts, faces, norm, fuv, [vista], 4, np.zeros(3),
        (2.0, 2.0, 2.0), 2.0, amostragem=amostragem)


class TestGradienteConhecido(unittest.TestCase):
    def test_gradiente_bake(self):
        tex, pintado, _, _ = _bake_gradiente()
        self.assertTrue(pintado[1, 1])
        # Mistura linear dos 4 cantos = (0,5; 0,5; 0,5); o bake
        # re-codifica -> sRGB(0,5) em cada canal.
        np.testing.assert_allclose(tex[1, 1], [SRGB_MEIO] * 3, atol=1e-9)

    def test_gradiente_vertice(self):
        img = np.array([[[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]],
                        [[0.0, 0.0, 1.0], [1.0, 1.0, 1.0]]])
        vista = {"vista": "frente", "imagem": img,
                 "mascara": np.ones((2, 2), dtype=bool),
                 "visivel": np.array([True])}
        verts = np.zeros((1, 3))
        normais = np.array([[0.0, -1.0, 0.0]])
        with patch.object(V.P, "projetar",
                          return_value=(np.array([1.0]), np.array([1.0]))), \
                patch.object(V.P, "alinhamento_silhueta",
                             return_value=(1.0, 0.0, 1.0, 0.0)):
            cores, fonte, _m, _i = V.amostrar_vertices(
                verts, normais, [vista], np.zeros(3), 1.0)
        self.assertEqual(fonte[0], V.FONTE_VISTA)
        # No vertice NAO ha re-codificacao: fica a mistura linear.
        np.testing.assert_allclose(cores[0], [0.5, 0.5, 0.5], atol=1e-12)


class TestControloSeco(unittest.TestCase):
    def test_seco_bake_byte_exacto(self):
        tex_s, pin_s, _, _ = _bake_gradiente(amostragem="seco")
        tex_b, pin_b, _, _ = _bake_gradiente(amostragem="bilinear")
        # Em "seco", o texel (1, 1) cai no pixel (1, 1) = branco,
        # byte a byte (a linha pontual pre-C-COR02).
        np.testing.assert_array_equal(tex_s[1, 1], np.array([1.0, 1.0, 1.0]))
        np.testing.assert_allclose(tex_b[1, 1], [SRGB_MEIO] * 3, atol=1e-9)
        # Onde se pinta nao muda entre modos (o clip e o mesmo).
        np.testing.assert_array_equal(pin_s, pin_b)
        with self.assertRaises(ValueError):
            _bake_gradiente(amostragem="erro")

    def test_seco_vertice_e_centro_exacto(self):
        img = np.array([[[0.25, 0.25, 0.25], [0.75, 0.75, 0.75]]])
        vista = {"vista": "frente", "imagem": img,
                 "mascara": np.ones((1, 2), dtype=bool),
                 "visivel": np.array([True])}
        verts = np.zeros((1, 3))
        normais = np.array([[0.0, -1.0, 0.0]])

        def correr(px, amostragem):
            with patch.object(V.P, "projetar",
                              return_value=(np.array([px]),
                                            np.array([0.5]))), \
                    patch.object(V.P, "alinhamento_silhueta",
                                 return_value=(1.0, 0.0, 1.0, 0.0)):
                return V.amostrar_vertices(
                    verts, normais, [vista], np.zeros(3), 1.0,
                    amostragem=amostragem)

        # Fora do centro: o seco amostra o pixel (lin(0,75) exacto);
        # o bilinear mistura - os modos separam-se.
        seco = correr(1.25, "seco")
        bilin = correr(1.25, "bilinear")
        np.testing.assert_allclose(seco[0][0], [LIN_075] * 3, atol=1e-12)
        self.assertFalse(np.array_equal(seco[0][0], bilin[0][0]))
        np.testing.assert_array_equal(seco[1], bilin[1])
        # No centro exacto do pixel, o bilinear degenera no pontual:
        # byte-exacto entre modos.
        seco_c = correr(1.5, "seco")
        bilin_c = correr(1.5, "bilinear")
        np.testing.assert_array_equal(seco_c[0], bilin_c[0])
        with self.assertRaises(ValueError):
            correr(1.25, "erro")


class TestA0Determinismo(unittest.TestCase):
    def _triangulo(self):
        verts = np.array([[0.0, -1.0, 0.0], [1.0, -1.0, 0.0],
                          [0.0, -1.0, 1.0]])
        faces = np.array([[0, 1, 2]])
        norm = np.array([[0.0, -1.0, 0.0]] * 3)
        fuv = np.array([[[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]])
        return verts, faces, norm, fuv

    def test_a0_centro_com_bilinear_ligado(self):
        # A mesma cena de faixas do test_cor (COR-08/A0): com o
        # bilinear ligado, a base continua a amostrar a faixa certa
        # (o centro continua subtraido) e as cores das faixas puras
        # sobrevivem byte a byte - a mistura so vive nas fronteiras.
        verts, faces, norm, fuv = self._triangulo()
        img = np.zeros((10, 10, 3))
        img[0:3] = [1.0, 0.0, 0.0]
        img[3:7] = [0.0, 1.0, 0.0]
        img[7:10] = [0.0, 0.0, 1.0]
        vista = {"vista": "frente", "imagem": img,
                 "mascara": np.ones((10, 10), dtype=bool),
                 "visivel": np.array([True]), "peso_face": np.array([1.0])}
        tex, pintado, _, _ = P.rasterizar_textura(
            verts, faces, norm, fuv, [vista], 16,
            np.array([0.0, 0.0, 0.5]), (1.0, 1.0, 1.0), 2.0)
        self.assertTrue(pintado[15, 0])
        self.assertTrue(np.all(tex[15, 0] == np.array([0.0, 0.0, 1.0])))
        self.assertTrue(pintado[0, 0])
        self.assertTrue(np.all(tex[0, 0] == np.array([1.0, 0.0, 0.0])))

    def test_determinismo_e_ordem(self):
        # Duas vistas com facings distintos (0,894 frente / 0,447
        # esquerda, como em test_cor): quem vence e o facing, nao a
        # ordem - e o resultado e byte-identico entre repeticoes e
        # entre ordens, com o bilinear activo (ha texels misturados).
        n = np.array([0.5, -1.0, 0.0])
        n = n / np.linalg.norm(n)
        centro = np.array([0.0, 0.0, 0.5])
        e1 = np.cross(n, np.array([0.0, 0.0, 1.0]))
        e1 = e1 / np.linalg.norm(e1)
        e2 = np.cross(n, e1)
        verts = np.array([centro, centro + e1 * 0.5, centro + e2 * 0.5])
        faces = np.array([[0, 1, 2]])
        norm = np.array([n, n, n])
        fuv = np.array([[[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]])
        faixas = np.zeros((10, 10, 3))
        faixas[0:3] = [1.0, 0.0, 0.0]
        faixas[3:7] = [0.0, 1.0, 0.0]
        faixas[7:10] = [0.0, 0.0, 1.0]
        grad = np.linspace(0.0, 1.0, 100).reshape(10, 10)
        outra = np.stack([grad, grad.T, 1.0 - grad], axis=2)
        vf = {"vista": "frente", "imagem": faixas,
              "mascara": np.ones((10, 10), dtype=bool),
              "visivel": np.array([True]), "peso_face": np.array([0.894])}
        ve = {"vista": "esquerda", "imagem": outra,
              "mascara": np.ones((10, 10), dtype=bool),
              "visivel": np.array([True]), "peso_face": np.array([0.447])}
        resultados = []
        for ordem in ([vf, ve], [ve, vf], [vf, ve]):
            tex, pintado, _, _ = P.rasterizar_textura(
                verts, faces, norm, fuv, ordem, 16, centro,
                (1.0, 1.0, 1.0), 2.0)
            resultados.append((tex, pintado))
        for tex, pintado in resultados[1:]:
            np.testing.assert_array_equal(tex, resultados[0][0])
            np.testing.assert_array_equal(pintado, resultados[0][1])
        tex, pintado = resultados[0]
        self.assertGreater(int(pintado.sum()), 0)
        puras = {tuple(c) for c in
                 ([1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0])}
        self.assertTrue(any(tuple(c) not in puras for c in tex[pintado]))


class TestParidadeConversao(unittest.TestCase):
    def test_as_duas_eotf_coincidem(self):
        g = np.linspace(0.0, 1.0, 257)
        g3 = np.stack([g, g, g], axis=1)
        np.testing.assert_array_equal(P.srgb_para_linear(g3),
                                      V.srgb_para_linear(g3))

    def test_inversa_roundtrip(self):
        g = np.linspace(0.0, 1.0, 257)
        volta = P.linear_para_srgb(P.srgb_para_linear(g))
        np.testing.assert_allclose(volta, g, atol=1e-12)
        # Os extremos sao exactos (bake de cor solida = cor solida).
        self.assertEqual(float(P.linear_para_srgb(np.array([1.0]))[0]), 1.0)
        self.assertEqual(float(P.linear_para_srgb(np.array([0.0]))[0]), 0.0)


if __name__ == "__main__":
    unittest.main()
