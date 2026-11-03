"""Testes da P1.1 - pesos territoriais em ``projecao.rasterizar_textura``.

Triangulo com normal inclinada entre frente e esquerda (facing frente
0,8; esquerda 0,6): sem fator, a frente vence; com o fator territorial
da face apontando para a esquerda (autoridade) e pedágio 0,5 na frente,
a esquerda vence - e ``info["vencedor"]`` registra quem venceu.
"""
import inspect
import sys
import unittest
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d.cor import projecao  # noqa: E402


def _caso():
    n = np.array([0.6, -0.8, 0.0])
    n = n / np.linalg.norm(n)
    centro = np.array([0.0, 0.0, 0.5])
    e1 = np.cross(n, np.array([0.0, 0.0, 1.0]))
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(n, e1)
    verts = np.array([centro, centro + e1 * 0.5, centro + e2 * 0.5])
    faces = np.array([[0, 1, 2]])
    norm = np.array([n, n, n])
    fuv = np.array([[[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]])
    vermelha = np.zeros((10, 10, 3))
    vermelha[:] = [1.0, 0.0, 0.0]
    azul = np.zeros((10, 10, 3))
    azul[:] = [0.0, 0.0, 1.0]
    vf = {"vista": "frente", "imagem": vermelha,
          "mascara": np.ones((10, 10), dtype=bool),
          "visivel": np.array([True]), "peso_face": np.array([0.8])}
    ve = {"vista": "esquerda", "imagem": azul,
          "mascara": np.ones((10, 10), dtype=bool),
          "visivel": np.array([True]), "peso_face": np.array([0.6])}
    return verts, faces, norm, fuv, [vf, ve], centro


class TestPesosTerritoriais(unittest.TestCase):
    def test_sem_fator_frente_vence_e_sem_vencedor(self):
        verts, faces, norm, fuv, vistas, centro = _caso()
        tex, pintado, _m, info = projecao.rasterizar_textura(
            verts, faces, norm, fuv, vistas, 16, centro, (1.0, 1.0, 1.0), 2.0)
        self.assertGreater(int(pintado.sum()), 0)
        self.assertTrue(np.all(tex[pintado] == np.array([1.0, 0.0, 0.0])))
        self.assertNotIn("vencedor", info)

    def test_fator_identidade_e_bit_a_bit_igual(self):
        verts, faces, norm, fuv, vistas, centro = _caso()
        base = projecao.rasterizar_textura(
            verts, faces, norm, fuv, vistas, 16, centro, (1.0, 1.0, 1.0), 2.0)
        fator = np.ones((1, 2), dtype=np.float32)
        com = projecao.rasterizar_textura(
            verts, faces, norm, fuv, vistas, 16, centro, (1.0, 1.0, 1.0), 2.0,
            fator_face_vista=fator)
        self.assertTrue((base[0] == com[0]).all())
        self.assertTrue((base[1] == com[1]).all())
        self.assertTrue((base[2] == com[2]).all())

    def test_pedagio_inverte_vencedor_e_registra_vencedor(self):
        verts, faces, norm, fuv, vistas, centro = _caso()
        # Colunas na ordem da lista [frente, esquerda]; territorio da
        # face = esquerda: frente paga 0,5, esquerda paga 1,0.
        # Efetivos: frente 0,8*0,5=0,4 < esquerda 0,6*1,0=0,6.
        fator = np.array([[0.5, 1.0]], dtype=np.float32)
        tex, pintado, _m, info = projecao.rasterizar_textura(
            verts, faces, norm, fuv, vistas, 16, centro, (1.0, 1.0, 1.0), 2.0,
            fator_face_vista=fator)
        self.assertGreater(int(pintado.sum()), 0)
        self.assertTrue(np.all(tex[pintado] == np.array([0.0, 0.0, 1.0])))
        self.assertIn("vencedor", info)
        self.assertTrue((info["vencedor"][pintado] == 1).all())

    def test_c_p1_5_amostragem_antes_do_fator_e_posicional_intacta(self):
        # C-P1-5: fator_face_vista fica DEPOIS de amostragem na
        # assinatura (cauda so por palavra-chave): um chamador que
        # passe amostragem POSICIONALMENTE nao pode cair no fator.
        params = list(inspect.signature(
            projecao.rasterizar_textura).parameters)
        self.assertLess(params.index("amostragem"),
                        params.index("fator_face_vista"))
        verts, faces, norm, fuv, vistas, centro = _caso()
        fator = np.array([[0.5, 1.0]], dtype=np.float32)
        tex, pintado, _m, info = projecao.rasterizar_textura(
            verts, faces, norm, fuv, vistas, 16, centro, (1.0, 1.0, 1.0),
            2.0, "seco", fator_face_vista=fator)
        self.assertGreater(int(pintado.sum()), 0)
        self.assertTrue(np.all(tex[pintado] == np.array([0.0, 0.0, 1.0])))
        self.assertTrue((info["vencedor"][pintado] == 1).all())


if __name__ == "__main__":
    unittest.main()
