"""Testes do D-H0 (oficina3d.diagnostico_dh0). Sem arte do RPG: mascaras
sinteticas + a tabela de coordenadas medida (diagnostico_dh0_dados.json).

Rodar (cwd = app):  py -3.12 -m unittest discover -s testes -p "test_diagnostico_dh0.py" -v
A geometria sobre as imagens reais (medir_vistas) NAO e testada aqui:
as imagens sao gitignored (arte do RPG) e nao existem num clone limpo;
ela foi executada e registrada no relatorio docs/DIAGNOSTICO-dh0-relatorio.md.
"""
from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d import diagnostico_dh0 as dh0  # noqa: E402


class TestMascaraIoUPerfil(unittest.TestCase):
    def test_bbox_da_mascara(self):
        m = np.zeros((10, 12), dtype=bool)
        m[2:5, 3:8] = True
        self.assertEqual(dh0.bbox_da_mascara(m), (3, 2, 7, 4))

    def test_iou_identidade_e_disjunto(self):
        a = np.zeros((8, 8), dtype=bool)
        a[1:5, 1:5] = True
        self.assertEqual(dh0.iou(a, a), 1.0)
        b = np.zeros((8, 8), dtype=bool)
        b[6:8, 6:8] = True
        self.assertEqual(dh0.iou(a, b), 0.0)

    def test_iou_espelhado_de_lados_simetricos(self):
        # Silhueta simetrica: espelhar nao muda o IoU (caso controle do
        # par esquerda x direita espelhado do D-H0).
        a = np.zeros((10, 10), dtype=bool)
        a[2:8, 2:8] = True
        self.assertEqual(dh0.iou(a, np.fliplr(a)), 1.0)

    def test_perfil_largura(self):
        m = np.zeros((100, 40), dtype=bool)
        m[:, 10:30] = True
        perfil = dh0.perfil_largura(m, (0, 0, 39, 99), faixas=100)
        self.assertEqual(len(perfil), 100)
        self.assertTrue(all(abs(v - 0.5) < 1e-9 for v in perfil))


class TestTabelaDeMarcos(unittest.TestCase):
    def setUp(self):
        self.dados = dh0.carregar_dados()
        self.por_marco, self.faixas = dh0.faixas_dos_marcos(self.dados)

    def test_tabela_tem_as_4_vistas_com_sha(self):
        self.assertEqual(set(self.dados["vistas"]), set(dh0.VISTAS))
        for vista, entrada in self.dados["vistas"].items():
            self.assertRegex(entrada["sha256"], r"^[0-9a-f]{64}$", vista)
            self.assertEqual(set(entrada["marcos"]),
                             {"topknot", "buckle", "skull", "redtip", "knee"})

    def test_faixas_recomputadas_iguais_as_publicadas(self):
        for marco, esperado in self.dados["valores_esperados"].items():
            self.assertAlmostEqual(self.faixas[marco], esperado, places=3,
                                   msg=marco)

    def test_tronco_sem_bandeira_regua_005(self):
        # Nenhum marco de tronco ultrapassa a regua pre-registrada.
        for marco in dh0.MARCOS_TRONCO:
            self.assertLess(self.faixas[marco], dh0.REGUA_FAIXA, marco)

    def test_joelho_com_bandeira_de_pose_registrada(self):
        # A faixa dos joelhos EXCEDE a regua: as vistas nao partilham
        # uma unica pose de pernas (documentado no relatorio, nao
        # escondido por uma media).
        self.assertGreater(self.faixas["knee"], dh0.REGUA_FAIXA)

    def test_cranio_a_direita_da_fivela_nas_4_vistas(self):
        # REGRA FINAL do Orc (reconciliacao REF-01 lote 4): o cranio
        # fica sempre a DIREITA do losango em coordenadas de imagem,
        # em qualquer vista -- nao se testa espelhamento fisico.
        for vista, entrada in self.dados["vistas"].items():
            buckle = entrada["marcos"]["buckle"][0]
            skull = entrada["marcos"]["skull"][0]
            xc_buckle = (buckle[0] + buckle[2]) / 2
            xc_skull = (skull[0] + skull[2]) / 2
            self.assertGreater(xc_skull, xc_buckle, vista)


if __name__ == "__main__":
    unittest.main()
