"""Testes da integracao `cor` (COR-05): selecao de vistas do passo, opcao
`cor` na fila e faixas de progresso do worker. Nada aqui toca GPU nem
Blender: o passo real (xatlas + bake) e provado pelo job de prova.
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

from oficina3d import cli, config, job, worker  # noqa: E402
from oficina3d.cor import passo  # noqa: E402

if os.path.normcase(str(config.JOBS)) != os.path.normcase(str(TEMP_TESTES)):
    raise RuntimeError(f"config.JOBS ({config.JOBS}) nao e a pasta temporaria dos testes; recuso rodar")


def _imgs(tmp: Path, vistas):
    """Imagens falsas (arquivos vazios bastam: selecionar_vistas so exige existir)."""
    out = []
    for v in vistas:
        p = tmp / f"{v}.png"
        p.write_bytes(b"")
        out.append({"arquivo": str(p), "vista": v})
    return out


class TestSelecionarVistas(unittest.TestCase):
    def test_canonicas_em_ordem_duplicata_vence_primeira_e_diagonal_ignorada(self):
        tmp = TEMP_TESTES / "cor_vistas"
        tmp.mkdir(exist_ok=True)
        imgs = _imgs(tmp, ["costas", "frente", "frente-esquerda"])
        dup = tmp / "frente2.png"
        dup.write_bytes(b"")
        imgs.append({"arquivo": str(dup), "vista": "frente"})
        vistas, ausentes, ignoradas = passo.selecionar_vistas(imgs)
        self.assertEqual([v["vista"] for v in vistas], ["frente", "costas"])
        self.assertEqual(vistas[0]["arquivo"], str(tmp / "frente.png"))
        self.assertEqual(ausentes, ["esquerda", "direita"])
        self.assertEqual(ignoradas, ["frente-esquerda"])

    def test_sem_canonica_levanta(self):
        tmp = TEMP_TESTES / "cor_vistas2"
        tmp.mkdir(exist_ok=True)
        with self.assertRaises(ValueError):
            passo.selecionar_vistas(_imgs(tmp, ["frente-esquerda", "cima"]))

    def test_sem_imagem_levanta(self):
        with self.assertRaises(ValueError):
            passo.selecionar_vistas([])

    def test_arquivo_canonico_ausente_levanta(self):
        with self.assertRaises(ValueError):
            passo.selecionar_vistas([{"arquivo": "nao-existe.png", "vista": "frente"}])

    def test_arquivo_relativo_resolve_no_job_dir(self):
        tmp = TEMP_TESTES / "cor_vistas3"
        tmp.mkdir(exist_ok=True)
        (tmp / "frente.png").write_bytes(b"")
        vistas, _, _ = passo.selecionar_vistas(
            [{"arquivo": "frente.png", "vista": "frente"}], job_dir=tmp)
        self.assertEqual(vistas[0]["arquivo"], str(tmp / "frente.png"))


class TestOpcaoCor(unittest.TestCase):
    def test_padrao_desligado_e_true_valido(self):
        op, _ = job.validar_opcoes({}, "livre", ["frente"])
        self.assertIs(op["cor"], False)
        op, _ = job.validar_opcoes({"cor": True}, "livre", ["frente"])
        self.assertIs(op["cor"], True)

    def test_texto_rejeitado(self):
        with self.assertRaises(ValueError):
            job.validar_opcoes({"cor": "sim"}, "livre", ["frente"])


class TestFaixasCor(unittest.TestCase):
    def test_faixas_ordenadas_e_cor_entre_refino_e_exportar(self):
        f = worker.FAIXAS
        self.assertEqual(f["refino"][1], f["cor"][0])
        self.assertEqual(f["cor"][1], f["exportar"][0])
        self.assertEqual(f["entrada"][0], 0)
        self.assertEqual(f["exportar"][1], 100)
        for ini, fim in f.values():
            self.assertLessEqual(0, ini)
            self.assertLessEqual(ini, fim)
            self.assertLessEqual(fim, 100)


class TestCliCor(unittest.TestCase):
    def test_flag_cor_no_enviar(self):
        a = cli.montar_parser().parse_args(
            ["enviar", "--cor", "--imagem", "a.png:frente"])
        self.assertTrue(a.cor)
        b = cli.montar_parser().parse_args(["enviar", "--imagem", "a.png:frente"])
        self.assertFalse(b.cor)


if __name__ == "__main__":
    unittest.main()
