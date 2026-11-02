"""COR-08/A0: prova CPU do centro, com controle negativo pre-fix."""
import inspect
import unittest

import numpy as np

from oficina3d.cor import projecao as P


def cena():
    verts = np.array([[-.4, -.1, 0.], [.4, -.1, 0.],
                      [.4, -.1, 1.], [-.4, -.1, 1.]])
    faces = np.array([[0, 1, 2], [0, 2, 3]])
    uv = np.array([[[0., 0.], [1., 0.], [1., 1.]],
                   [[0., 0.], [1., 1.], [0., 1.]]])
    h, w = 945, 700  # sintetico: .5/1.1*945 = 429.54545 px
    yy, xx = np.indices((h, w))
    imagem = np.stack([xx / (w - 1), yy / (h - 1), yy * 0.], axis=-1)
    vista = dict(vista="frente", imagem=imagem, mascara=np.ones((h, w), bool),
                 visivel=np.ones(2, bool), peso_face=np.ones(2),
                 alinhamento=(1., 0., 1., 0.))
    return verts, faces, np.tile([0., -1., 0.], (4, 1)), uv, vista


def bake(func=P.rasterizar_textura, deslocamento=None, override=True):
    verts, faces, normais, uv, vista = cena()
    centro = np.array([0., 0., .5])
    if deslocamento is not None:
        verts = verts + deslocamento
        centro = centro + deslocamento
    if not override:
        vista.pop("alinhamento")
    return func(verts, faces, normais, uv, [vista], 32, centro, (.8, .2, 1.), 1.1)


def mutante_sem_centro():
    fonte = inspect.getsource(P.rasterizar_textura)
    alvo = "rel = p3d - np.asarray(centro, dtype=np.float64)"
    if fonte.count(alvo) != 1:
        raise AssertionError("controle negativo precisa ser revisto: ponto da mutacao mudou")
    escopo = dict(vars(P))
    exec(compile(fonte.replace(alvo, "rel = p3d"), "<controle-pre-A0>", "exec"), escopo)
    return escopo["rasterizar_textura"]


class TestCentroPublicado(unittest.TestCase):
    def test_coordenadas_por_texel_contra_formula_independente(self):
        tex, pin, _, _ = bake()
        y, x = np.indices(pin.shape)
        # UV do centro do texel -> quadrilatero 3D, sem chamar projetar().
        world_x = -.4 + .8 * (x + .5) / 32
        world_z = 1. - (y + .5) / 32
        ix = ((world_x / (1.1 * 700 / 945) + .5) * 700).astype(int)
        iy = ((.5 - (world_z - .5) / 1.1) * 945).astype(int)
        self.assertEqual(int(pin.sum()), 1024)
        np.testing.assert_allclose(tex[..., 0], ix / 699, atol=1e-12)
        np.testing.assert_allclose(tex[..., 1], iy / 944, atol=1e-12)
        self.assertGreater(float(tex[pin, 1].max()), .9)

    def test_translacao_conjunta_nao_muda_amostras_bbox_e_override(self):
        for override in (False, True):
            with self.subTest(override=override):
                a = bake(override=override)
                b = bake(deslocamento=np.array([1.25, -2., 3.5]), override=override)
                for i in range(3):
                    np.testing.assert_array_equal(a[i], b[i])

    def test_controle_negativo_discrimina_erro_antigo(self):
        atual, pin, _, _ = bake()
        antigo, pin_antigo, _, _ = bake(mutante_sem_centro())
        np.testing.assert_array_equal(pin, pin_antigo)
        self.assertGreater(float(np.abs(atual - antigo).max()), .4)
        self.assertLess(float(antigo[pin, 1].max()), .5)
        self.assertTrue(np.all(atual[31, :, 1] > .9))
        self.assertTrue(np.all(antigo[31, :, 1] < .5))


if __name__ == "__main__":
    unittest.main()
