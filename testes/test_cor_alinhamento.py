"""COR-08/A1: alinhamento que otimiza o IoU + dilatacao com dominio.

Sinteticos puros (sem Blender): o otimizador tem de (a) recuperar o
encaixe quando a caixa e ditada por uma protrusao (o "machado fora de
pose" do diagnostico D1), (b) nunca piorar o IoU da afinidade por
caixas, (c) ser deterministico, (d) respeitar as travas anti-zoom
degenerado e (e) devolver None com mascara vazia.
"""
import unittest

import numpy as np

from oficina3d.cor import projecao


def _retangulo(shape, y0, y1, x0, x1):
    m = np.zeros(shape, dtype=bool)
    m[y0:y1, x0:x1] = True
    return m


class TestAlinhamentoOtimizado(unittest.TestCase):
    def test_recupera_protrusao(self):
        # Arte: corpo 50x50 + protrusao curta de 5 (o machado dela).
        arte = _retangulo((128, 128), 30, 80, 40, 90)
        arte[50:60, 90:95] = True
        # Malha: mesmo corpo, protrusao de 12 noutra altura (pose diversa):
        # a caixa da malha e mais larga -> a afinidade por caixas comprime
        # o corpo e o IoU nasce baixo; o otimizador tem de recuperar.
        malha = _retangulo((128, 128), 30, 80, 40, 90)
        malha[35:45, 90:102] = True
        saida = projecao.alinhamento_otimizado(malha, arte)
        self.assertIsNotNone(saida)
        _ax, _bx, _ay, _by, iou0, iou1 = saida
        # CORRECAO 2 (executor, apos segunda falha medida): nem a v1
        # por caixas extremas e "baixa" neste caso - ela tambem alcanca
        # 0,8846 (as caixas robusta e extrema quase coincidem aqui, e a
        # compressao em x e modesta). O maximo teorico do caso e 0,9363
        # = corpo / (corpo + as duas protrusoes disjuntas: 2500/2670) -
        # e o otimizador o atinge EXATAMENTE. Exigir +0,08 sobre 0,8846
        # seria exigir acima do maximo possivel: limiar insatisfazivel
        # por construcao, nao fraqueza do otimizador. O teste passa a
        # afirmar o que o caso realmente prova: nunca piora (nem v1,
        # nem inicial robusto) e atinge o otimo teorico. A recuperacao
        # a partir de uma v1 genuinamente baixa ja e coberta por
        # test_ponta_fina_recupera_iou em test_cor.py.
        ini_v1 = projecao.alinhamento_silhueta(
            projecao.bbox_mascara(arte), projecao.bbox_mascara(malha))
        iou_v1 = projecao.iou_alinhado(malha, arte, *ini_v1)
        self.assertGreaterEqual(iou1, iou_v1)
        self.assertGreaterEqual(iou1, iou0)
        self.assertAlmostEqual(iou1, 2500 / 2670, places=3)
        self.assertGreaterEqual(iou1, 0.85)

    def test_nunca_piora(self):
        # Circulo deslocado e achatado: caixa nao resolve a forma.
        yy, xx = np.mgrid[0:96, 0:96]
        arte = ((xx - 48) / 30.0) ** 2 + ((yy - 48) / 22.0) ** 2 <= 1.0
        malha = ((xx - 43) / 30.0) ** 2 + ((yy - 52) / 22.0) ** 2 <= 1.0
        saida = projecao.alinhamento_otimizado(malha, arte)
        self.assertIsNotNone(saida)
        self.assertGreaterEqual(saida[5], saida[4])
        self.assertGreater(saida[5], 0.9)

    def test_deterministico(self):
        arte = _retangulo((96, 96), 20, 70, 25, 75)
        malha = _retangulo((96, 96), 24, 66, 18, 80)
        a = projecao.alinhamento_otimizado(malha, arte)
        b = projecao.alinhamento_otimizado(malha, arte)
        self.assertEqual(a, b)

    def test_trava_escala_anti_zoom(self):
        # Arte de mascara cheia: sem trava, "amostrar so o centro"
        # maximizaria o IoU destruindo a correspondencia. A escala nao
        # pode se afastar da inicial alem de trava_escala (0,35).
        arte = np.ones((96, 96), dtype=bool)
        malha = _retangulo((96, 96), 33, 63, 33, 63)
        ax0, _bx0, ay0, _by0 = projecao.alinhamento_silhueta(
            projecao.bbox_mascara(arte), projecao.bbox_mascara(malha))
        saida = projecao.alinhamento_otimizado(malha, arte)
        self.assertIsNotNone(saida)
        self.assertLessEqual(saida[0], ax0 * 1.35 + 1e-9)
        self.assertGreaterEqual(saida[0], ax0 / 1.35 - 1e-9)
        self.assertLessEqual(saida[2], ay0 * 1.35 + 1e-9)
        self.assertGreaterEqual(saida[2], ay0 / 1.35 - 1e-9)

    def test_mascara_vazia_retorna_none(self):
        vazia = np.zeros((32, 32), dtype=bool)
        cheia = _retangulo((32, 32), 5, 20, 5, 20)
        self.assertIsNone(projecao.alinhamento_otimizado(vazia, cheia))
        self.assertIsNone(projecao.alinhamento_otimizado(cheia, vazia))

    def test_formatos_diferentes_levantam(self):
        with self.assertRaises(ValueError):
            projecao.alinhamento_otimizado(np.zeros((8, 8), dtype=bool),
                                           np.zeros((9, 8), dtype=bool))


class TestDeformarMascara(unittest.TestCase):
    def test_identidade(self):
        m = _retangulo((32, 32), 5, 20, 7, 25)
        out = projecao.deformar_mascara(m, 1.0, 0.0, 1.0, 0.0)
        self.assertTrue((out == m).all())

    def test_translacao(self):
        m = _retangulo((32, 32), 5, 10, 5, 10)
        out = projecao.deformar_mascara(m, 1.0, 3.0, 1.0, 2.0)
        esperado = _retangulo((32, 32), 7, 12, 8, 13)
        self.assertTrue((out == esperado).all())


class TestDilatarDominio(unittest.TestCase):
    def test_dominio_limita_o_preenchimento(self):
        tex = np.zeros((7, 7, 3))
        tex[3, 3] = [1.0, 0.0, 0.0]
        pin = np.zeros((7, 7), dtype=bool)
        pin[3, 3] = True
        dominio = np.zeros((7, 7), dtype=bool)
        dominio[:, :4] = True  # so a metade esquerda pode ser preenchida
        _t, pin2, n = projecao.dilatar(tex, pin, 10, dominio=dominio)
        self.assertTrue(pin2[:, :4].all())
        self.assertFalse(pin2[:, 4:].any())
        self.assertEqual(n, int(dominio.sum()) - 1)

    def test_sem_dominio_comportamento_v1(self):
        tex = np.zeros((5, 5, 3))
        tex[2, 2] = [1.0, 0.0, 0.0]
        pin = np.zeros((5, 5), dtype=bool)
        pin[2, 2] = True
        _t, pin2, n = projecao.dilatar(tex, pin, 10)
        self.assertTrue(pin2.all())
        self.assertEqual(n, 24)


if __name__ == "__main__":
    unittest.main()
