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


class TestGerarUvProgresso(unittest.TestCase):
    """D-COR05-1: gerar_uv emite progresso e aborta antes de gravar o .npz."""

    def _cubo_glb(self, tmp):
        import trimesh
        p = tmp / "cubo.glb"
        trimesh.creation.box(extents=(1.0, 1.0, 1.0)).export(str(p))
        return p

    def test_progresso_chamado_nas_fronteiras_e_monotonico(self):
        from oficina3d import uv_xatlas
        tmp = TEMP_TESTES / "cor_uv_prog"
        tmp.mkdir(exist_ok=True)
        chamadas = []
        met = uv_xatlas.gerar_uv(self._cubo_glb(tmp), tmp / "uv.npz",
                                 progresso=lambda pct, msg: chamadas.append((pct, msg)))
        self.assertEqual(met["triangulos"], 12)
        pcts = [c[0] for c in chamadas]
        self.assertEqual(pcts[0], 0)
        self.assertEqual(pcts[-1], 100)
        self.assertIn(30, pcts)
        self.assertIn(80, pcts)
        self.assertEqual(pcts, sorted(pcts))
        self.assertTrue((tmp / "uv.npz").is_file())

    def test_progresso_que_levanta_em_80_nao_grava_npz(self):
        from oficina3d import uv_xatlas
        tmp = TEMP_TESTES / "cor_uv_cancel"
        tmp.mkdir(exist_ok=True)

        def _cancela(pct, msg):
            if pct >= 80:
                raise RuntimeError("cancelado simulado")

        with self.assertRaises(RuntimeError):
            uv_xatlas.gerar_uv(self._cubo_glb(tmp), tmp / "uv.npz", progresso=_cancela)
        self.assertFalse((tmp / "uv.npz").exists())

    def test_sem_progresso_mantem_comportamento(self):
        from oficina3d import uv_xatlas
        tmp = TEMP_TESTES / "cor_uv_semprog"
        tmp.mkdir(exist_ok=True)
        met = uv_xatlas.gerar_uv(self._cubo_glb(tmp), tmp / "uv.npz")
        self.assertEqual(met["triangulos"], 12)
        self.assertTrue((tmp / "uv.npz").is_file())


class TestSha256Worker(unittest.TestCase):
    """D-COR05-3: o helper de SHA usado no campo glb_refinado_preservado."""

    def test_sha256_de_conteudo_conhecido(self):
        import hashlib
        tmp = TEMP_TESTES / "cor_sha"
        tmp.mkdir(exist_ok=True)
        p = tmp / "a.bin"
        p.write_bytes(b"oficina3d-dc05")
        self.assertEqual(worker._sha256(p), hashlib.sha256(b"oficina3d-dc05").hexdigest())


if __name__ == "__main__":
    unittest.main()
