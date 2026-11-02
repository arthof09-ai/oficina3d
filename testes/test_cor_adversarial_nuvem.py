"""Provas de limites/defeitos na base PUBLICADA congelada, nao requisitos futuros.

Estes testes documentam contracasos; nao obrigam o codigo integrado a manter bugs.
"""
import unittest

import numpy as np

from oficina3d.cor import preenchimento as PF
from testes.publicado_nuvem import modulo
from testes.test_cor_centro_nuvem import cena


class TestPipelinePublicado(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.p = modulo("oficina3d/cor/projecao.py")

    def executar(self, vistas, normais=None):
        verts, faces, norm, uv, _ = cena()
        return self.p.rasterizar_textura(verts, faces, norm if normais is None else normais,
                                        uv, vistas, 32, np.array([0., 0., .5]), (.8, .2, 1.), 1.1)

    def test_n01_faces_contadas_sem_um_texel_aceito(self):
        *_, vista = cena()
        vista["mascara"][:] = False
        vista["mascara"][0, 0] = True  # mascara nao vazia, fora de todas as amostras
        _, pin, _, info = self.executar([vista])
        self.assertEqual(int(pin.sum()), 0)
        self.assertEqual(info["texels_por_vista"]["frente"], 0)
        self.assertEqual(info["faces_pintadas_por_vista"]["frente"], 2)

    def test_n02_contagens_de_vistas_nao_sao_proveniencia_final(self):
        *_, frente = cena()
        frente["imagem"][:] = [1., 0., 0.]
        esquerda = {**frente, "vista": "esquerda", "imagem": np.zeros_like(frente["imagem"])}
        esquerda["imagem"][:] = [0., 0., 1.]
        normais = np.tile([.8, -.6, 0.], (4, 1))
        tex, pin, _, info = self.executar([frente, esquerda], normais)
        self.assertEqual(int(pin.sum()), 1024)
        np.testing.assert_array_equal(tex[pin], np.tile([0., 0., 1.], (1024, 1)))
        self.assertEqual(info["texels_por_vista"], {"frente": 1024, "esquerda": 1024})
        tex2, pin2, _, info2 = self.executar([esquerda, frente], normais)
        np.testing.assert_array_equal(tex, tex2)
        np.testing.assert_array_equal(pin, pin2)
        self.assertEqual(info2["texels_por_vista"], {"esquerda": 1024, "frente": 0})

    def test_n03_fora_do_quadro_vira_fonte_direta_por_clip(self):
        *_, vista = cena()
        vista["alinhamento"] = (1., 10000., 1., 0.)
        vista["imagem"][:] = 0.
        vista["imagem"][:, -1] = [1., 0., 0.]
        tex, pin, _, info = self.executar([vista])
        self.assertEqual(int(pin.sum()), 1024)
        self.assertEqual(info["texels_por_vista"]["frente"], 1024)
        np.testing.assert_array_equal(tex[pin], np.tile([1., 0., 0.], (1024, 1)))

    def test_n04_trava_de_aspecto_e_relativa_ao_inicial(self):
        m = np.zeros((64, 64), bool)
        a = m.copy()
        m[10:30, 10:20] = True
        a[10:30, 20:40] = True
        ax, _, ay, _, info = self.p.otimizar_alinhamento(m, a, (2., 0., 1., 0.))
        self.assertEqual(info["iou_final"], 1.)
        self.assertEqual(ax / ay, 2.)
        self.assertEqual(info["escala_x"] / info["escala_y"], 1.)

    def test_s2_linear_ja_conhecido_media_srgb_quantificada(self):
        tex = np.array([[[0., 0., 0.], [1., 1., 1.]]])
        cor, tem, contagem = PF.cores_diretas_por_face(tex, np.ones((1, 2), bool),
                                                    np.zeros((1, 2), int), 1)
        np.testing.assert_array_equal(cor, [[.5, .5, .5]])
        self.assertTrue(tem[0])
        self.assertEqual(contagem[0], 2)
        esperado = 1.055 * .5 ** (1 / 2.4) - .055
        self.assertAlmostEqual(esperado, .7353569830524495)
        self.assertAlmostEqual((esperado - cor[0, 0]) * 255, 60.0160306784, places=7)


if __name__ == "__main__":
    unittest.main()
