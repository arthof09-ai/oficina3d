"""Testes dos perfis de qualidade (QUAL-01): Bronze, Prata, Ouro,
Ouro Negro e Lendario -- as classificacoes do RPG como niveis de
qualidade da modelagem. O perfil preenche defaults; a opcao explicita
do usuario sempre vence."""
import sys
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d import job, qualidades  # noqa: E402

QUATRO = ["frente", "costas", "esquerda", "direita"]
UMA = ["frente"]


class TestPerfis(unittest.TestCase):
    def test_cinco_niveis_na_ordem_do_rpg(self):
        self.assertEqual(qualidades.NOMES,
                         ("bronze", "prata", "ouro", "ouro-negro", "lendario"))
        self.assertEqual([qualidades.ROTULOS[s] for s in qualidades.NOMES],
                         ["Bronze", "Prata", "Ouro", "Ouro Negro", "Lend\u00e1rio"])

    def test_parametros_dentro_das_faixas_do_job(self):
        for slug, p in qualidades.PERFIS.items():
            with self.subTest(slug=slug):
                self.assertTrue(64 <= p["octree"] <= 512)
                self.assertTrue(1_000 <= p["alvo_triangulos"] <= 1_000_000)
                if p["passos"] is not None:
                    self.assertTrue(1 <= p["passos"] <= 100)

    def test_custo_sobe_com_o_nivel(self):
        alvos = [qualidades.PERFIS[s]["alvo_triangulos"] for s in qualidades.NOMES]
        octs = [qualidades.PERFIS[s]["octree"] for s in qualidades.NOMES]
        self.assertEqual(alvos, sorted(alvos))
        self.assertEqual(octs, sorted(octs))


class TestAplicar(unittest.TestCase):
    def test_sem_qualidade_nao_muda_nada(self):
        op = {"motor": None, "octree": None}
        self.assertEqual(qualidades.aplicar(op, "livre", QUATRO), op)

    def test_slug_desconhecido_levanta(self):
        with self.assertRaises(ValueError):
            qualidades.aplicar({"qualidade": "diamante"}, "livre", QUATRO)

    def test_bronze_uma_vista_sugere_triposr(self):
        op = qualidades.aplicar({"qualidade": "bronze"}, "livre", UMA)
        self.assertEqual(op["motor"], "triposr")
        self.assertEqual(op["octree"], 128)
        self.assertEqual(op["alvo_triangulos"], 25_000)

    def test_bronze_multivista_deixa_o_automatico(self):
        op = qualidades.aplicar({"qualidade": "bronze"}, "livre", QUATRO)
        self.assertIsNone(op.get("motor"))

    def test_completo_multivista_e_hunyuan_mv(self):
        op = qualidades.aplicar({"qualidade": "lendario"}, "livre", QUATRO)
        self.assertEqual(op["motor"], "hunyuan-mv")
        self.assertEqual(op["passos"], 50)
        self.assertEqual(op["octree"], 384)
        self.assertEqual(op["alvo_triangulos"], 500_000)

    def test_completo_uma_vista_e_hunyuan_mini(self):
        op = qualidades.aplicar({"qualidade": "ouro-negro"}, "livre", UMA)
        self.assertEqual(op["motor"], "hunyuan-mini")
        self.assertEqual(op["passos"], 30)

    def test_turbo_nao_forca_motor_nem_passos(self):
        op = qualidades.aplicar({"qualidade": "ouro"}, "livre", QUATRO)
        self.assertIsNone(op.get("motor"))
        self.assertIsNone(op.get("passos"))
        self.assertEqual(op["alvo_triangulos"], 150_000)

    def test_opcao_explicita_vence_o_perfil(self):
        op = qualidades.aplicar(
            {"qualidade": "lendario", "octree": 200, "motor": "hunyuan-mv-turbo"},
            "livre", QUATRO)
        self.assertEqual(op["octree"], 200)
        self.assertEqual(op["motor"], "hunyuan-mv-turbo")
        self.assertEqual(op["alvo_triangulos"], 500_000)  # o resto do perfil fica


class TestValidarOpcoes(unittest.TestCase):
    def test_lendario_ponta_a_ponta(self):
        op, _ = job.validar_opcoes({"qualidade": "lendario"}, "livre", QUATRO)
        self.assertEqual(op["qualidade"], "lendario")
        self.assertEqual(op["motor"], "hunyuan-mv")
        self.assertEqual(op["passos"], 50)
        self.assertEqual(op["octree"], 384)
        self.assertEqual(op["alvo_triangulos"], 500_000)

    def test_prata_mantem_automatico_turbo(self):
        op, _ = job.validar_opcoes({"qualidade": "prata"}, "livre", QUATRO)
        self.assertEqual(op["motor"], "hunyuan-mv-turbo")
        self.assertEqual(op["alvo_triangulos"], 50_000)

    def test_qualidade_invalida_levanta(self):
        with self.assertRaises(ValueError):
            job.validar_opcoes({"qualidade": "diamante"}, "livre", QUATRO)


if __name__ == "__main__":
    unittest.main()
