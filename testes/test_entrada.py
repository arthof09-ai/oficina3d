"""Testes de oficina3d.entrada.validacao: os avisos de qualidade de imagem
(fundo, recorte/resolucao, vistas repetidas, personagens diferentes).
Arrays sinteticos com numpy; nenhuma imagem do RPG.
"""
import atexit
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

# --- pasta temporaria dos testes: SEMPRE dentro de BASE\\jobs_teste (mesmo padrao dos outros testes) ---
_BASE_TESTE = Path(os.environ.get("OFICINA3D_BASE") or r"C:\Users\txcga\RPG_Local\Oficina3D")
RAIZ_TESTE = _BASE_TESTE / "jobs_teste"


def _dentro(filho: Path, pai: Path) -> bool:
    f = os.path.normcase(os.path.abspath(filho))
    p = os.path.normcase(os.path.abspath(pai))
    return f.startswith(p + os.sep)


def _pasta_temporaria_dos_testes() -> Path:
    atual = os.environ.get("OFICINA3D_JOBS")
    if atual and _dentro(Path(atual), RAIZ_TESTE) and Path(atual).name.startswith("unittest_"):
        return Path(atual)
    RAIZ_TESTE.mkdir(exist_ok=True)
    p = Path(tempfile.mkdtemp(prefix="unittest_", dir=RAIZ_TESTE))
    os.environ["OFICINA3D_JOBS"] = str(p)
    atexit.register(shutil.rmtree, p, True)
    return p


TEMP_TESTES = _pasta_temporaria_dos_testes()

import numpy as np  # noqa: E402

from oficina3d.entrada import validacao as v  # noqa: E402


def rgba(w, h, cor=(200, 30, 30), alfa=255, fundo_alfa=0):
    """Quadro com fundo de um alfa e um objeto retangular centrado de outro."""
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[..., 3] = fundo_alfa
    y0, y1 = h // 4, 3 * h // 4
    x0, x1 = w // 4, 3 * w // 4
    arr[y0:y1, x0:x1] = (*cor, alfa)
    return arr


def solido(w, h, cor):
    arr = np.zeros((h, w, 4), dtype=np.uint8)
    arr[..., 0], arr[..., 1], arr[..., 2], arr[..., 3] = (*cor, 255)
    return arr


class TestDiagnosticoFundo(unittest.TestCase):
    def test_sem_canal_alfa(self):
        util, motivo = v.diagnostico_fundo(rgba(64, 64), False)
        self.assertFalse(util)
        self.assertIn("sem canal alfa", motivo)

    def test_tudo_opaco_e_fundo_nao_removido(self):
        arr = solido(64, 64, (10, 10, 10))
        util, motivo = v.diagnostico_fundo(arr, True)
        self.assertFalse(util)
        self.assertIn("fundo não removido", motivo)

    def test_alfa_limpo_ok(self):
        util, motivo = v.diagnostico_fundo(rgba(64, 64), True)
        self.assertTrue(util)
        self.assertIsNone(motivo)


class TestAvisosRecorte(unittest.TestCase):
    def test_imagem_vazia(self):
        arr = np.zeros((50, 50, 4), dtype=np.uint8)
        avisos = v.avisos_recorte(arr, "vazia.png")
        self.assertEqual(len(avisos), 1)
        self.assertIn("imagem vazia", avisos[0])

    def test_resolucao_baixa(self):
        avisos = v.avisos_recorte(rgba(200, 200), "pequena.png")
        self.assertTrue(any("resolução baixa" in a for a in avisos), avisos)

    def test_resolucao_boa_sem_avisos(self):
        avisos = v.avisos_recorte(rgba(1600, 1600), "grande.png")
        self.assertEqual(avisos, [], avisos)

    def test_objeto_cortado_na_borda(self):
        arr = np.zeros((400, 400, 4), dtype=np.uint8)
        arr[0:200, 100:300] = (50, 60, 70, 255)  # toca a borda de cima
        avisos = v.avisos_recorte(arr, "cortada.png")
        self.assertTrue(any("cortado na borda" in a for a in avisos), avisos)


class TestCores(unittest.TestCase):
    def test_assinatura_e_distancia(self):
        verm = v.assinatura_cor(solido(40, 40, (255, 0, 0)))
        azul = v.assinatura_cor(solido(40, 40, (0, 0, 255)))
        self.assertIsNotNone(verm)
        self.assertAlmostEqual(float(verm.sum()), 1.0, places=6)
        self.assertEqual(v.distancia_cor(verm, verm), 0.0)
        self.assertEqual(v.distancia_cor(verm, azul), 1.0)

    def test_sem_pixels_opacos_sem_assinatura(self):
        arr = np.zeros((20, 20, 4), dtype=np.uint8)
        self.assertIsNone(v.assinatura_cor(arr))

    def test_personagens_diferentes_detecta(self):
        regs = [
            {"nome": "a.png", "vista": "frente", "assinatura": v.assinatura_cor(solido(40, 40, (255, 0, 0)))},
            {"nome": "b.png", "vista": "costas", "assinatura": v.assinatura_cor(solido(40, 40, (0, 0, 255)))},
        ]
        avisos = v.personagens_diferentes(regs)
        self.assertEqual(len(avisos), 1)
        self.assertIn("personagens diferentes", avisos[0])

    def test_mesmo_personagem_sem_aviso(self):
        s = v.assinatura_cor(solido(40, 40, (255, 0, 0)))
        regs = [{"nome": "a.png", "vista": "frente", "assinatura": s},
                {"nome": "b.png", "vista": "costas", "assinatura": s}]
        self.assertEqual(v.personagens_diferentes(regs), [])


class TestVistasRepetidas(unittest.TestCase):
    def test_repetida_avisa(self):
        regs = [{"vista": "frente"}, {"vista": "frente"}, {"vista": "costas"}]
        avisos = v.vistas_repetidas(regs)
        self.assertEqual(len(avisos), 1)
        self.assertIn("'frente' aparece 2 vezes", avisos[0])

    def test_distintas_sem_aviso(self):
        regs = [{"vista": "frente"}, {"vista": "costas"}, {"vista": None}]
        self.assertEqual(v.vistas_repetidas(regs), [])


if __name__ == "__main__":
    unittest.main()
