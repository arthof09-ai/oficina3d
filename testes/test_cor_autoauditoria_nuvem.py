"""APR-02: limites das entregas Codex e contraprovas contra a base nova."""
import ast
from pathlib import Path
import unittest

import numpy as np

from oficina3d.cor import preenchimento as PF, vertice as V
from testes.publicado_nuvem import fonte, ROOT


class TestAutoauditoria(unittest.TestCase):
    def test_expoente_positivo_nao_muda_vencedor_nem_empate(self):
        # Reproduz a operacao do experimento B: expoente aplicado somente
        # na comparacao/armazenamento, depois da mascara, visibilidade e cutoff.
        pesos = np.array([[.8, .6, .8], [.1, .9, .2], [.5, .5, .5]])
        for exp in (.5, 1., 1.5, 2.):
            np.testing.assert_array_equal(np.argmax(pesos ** exp, axis=1), [0, 1, 0])
        # Nao e knob em producao. Nao generalizar para exp<=0 ou blending.
        arvore = ast.parse((ROOT / "oficina3d/cor/_blender_vertice.py").read_text(encoding="utf-8"))
        strings = [n.value for n in ast.walk(arvore) if isinstance(n, ast.Constant) and isinstance(n.value, str)]
        self.assertNotIn("expoente", strings)

    def test_media_linear_da_cor_de_vertice_nao_e_media_srgb_do_bake(self):
        # Evita declarar que C-COR01 fecha o S2 do bake A3.
        linear = V.srgb_para_linear(np.array([.25, .75])).mean()
        srgb = np.array([.25, .75]).mean()
        self.assertAlmostEqual(srgb, .5)
        self.assertGreater(abs(linear - V.srgb_para_linear(srgb)), .05)
        publicado = fonte("oficina3d/cor/_blender_cor.py")
        self.assertNotIn("srgb_para_linear", publicado)

    def test_mapa_de_vistas_diretas_nao_explica_preenchimento_a3(self):
        # Duas faces vizinhas; a segunda nao tem amostra direta de vista.
        cores = np.array([[.2, .4, .6], [0., 0., 0.]])
        final, anel, alcancavel = PF.difundir([[1], [0]], cores, np.array([True, False]))
        tex = np.array([[[.2, .4, .6], [0., 0., 0.]]])
        pin = np.array([[True, False]])
        _, pin_final, preenchidos = PF.aplicar_preenchimento(tex, pin, np.array([[0, 1]]), final, alcancavel)
        self.assertEqual(int(pin.sum()), 1)
        self.assertEqual(int(pin_final.sum()), 2)
        self.assertEqual(int(preenchidos.sum()), 1)
        self.assertEqual(anel.tolist(), [0, 1])
        # Um mapa salvo dentro de rasterizar_textura cobre apenas o direto.
        mapa_vista_direta = np.array([[0, -1]])
        self.assertEqual(int((mapa_vista_direta >= 0).sum()), 1)

    def test_codigo_do_bake_cor08_s2_permanece_byte_identico(self):
        for arquivo in ("oficina3d/cor/projecao.py", "oficina3d/cor/_blender_cor.py",
                        "oficina3d/cor/preenchimento.py", "oficina3d/cor/passo.py"):
            with self.subTest(arquivo=arquivo):
                atual = (ROOT / arquivo).read_text(encoding="utf-8")
                self.assertEqual(atual, fonte(arquivo))


if __name__ == "__main__":
    unittest.main()
