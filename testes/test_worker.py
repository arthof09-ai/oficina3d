"""Testes de oficina3d.worker: fila (pendentes/proximo), retomada de orfaos,
escolha do motor e o minimo de disco livre. Jobs de verdade (criar_job) numa
pasta temporaria em jobs_teste; nenhum job real e processado (sem GPU).
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

def png_bytes(w: int = 32, h: int = 32) -> bytes:
    """PNG valido minimo (gerado em codigo; nada de arte do RPG)."""
    import struct
    import zlib
    linha = b"\x00" + b"\x80\x40\x20\xff" * w
    bruto = linha * h

    def pedaco(tipo: bytes, dados: bytes) -> bytes:
        return (struct.pack(">I", len(dados)) + tipo + dados
                + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + pedaco(b"IHDR", ihdr)
            + pedaco(b"IDAT", zlib.compress(bruto)) + pedaco(b"IEND", b""))

from oficina3d import config  # noqa: E402

if os.path.normcase(str(config.JOBS)) != os.path.normcase(str(TEMP_TESTES)):
    raise RuntimeError(f"config.JOBS ({config.JOBS}) nao e a pasta temporaria dos testes; recuso rodar")

from oficina3d import job, worker  # noqa: E402


class CasoWorker(unittest.TestCase):
    def img(self, nome="img.png") -> Path:
        p = TEMP_TESTES / "fixtures_worker" / nome
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(png_bytes())
        return p

    def criar(self, nome="teste-worker"):
        return job.criar_job([(self.img(), "frente")], nome=nome)["id"]

    def mudar(self, jid, **campos):
        def alterar(d):
            d.update(campos)
            return d
        return job.atualizar_job(jid, alterar)


class TestFila(CasoWorker):
    def test_pendentes_so_traz_pendentes(self):
        a = self.criar("fila-a")
        b = self.criar("fila-b")
        c = self.criar("fila-c")
        self.mudar(b, estado="concluido")
        pend = worker.pendentes()
        self.assertIn(a, pend)
        self.assertIn(c, pend)
        self.assertNotIn(b, pend)

    def test_proximo_pendente_respeita_permitidos(self):
        a = self.criar("prox-a")
        b = self.criar("prox-b")
        self.assertEqual(worker.proximo_pendente({b}), b)
        self.assertIsNone(worker.proximo_pendente({"id-que-nao-existe"}))
        self.assertIn(worker.proximo_pendente({a, b}), (a, b))

    def test_contrato_da_fila(self):
        # a pasta e compartilhada com os outros testes: so o contrato, nao o conteudo
        pend = worker.pendentes()
        self.assertIsInstance(pend, list)
        self.assertTrue(all(isinstance(x, str) for x in pend))


class TestOrfaos(CasoWorker):
    def test_orfao_sem_worker_volta_para_fila(self):
        jid = self.criar("orfao-1")
        self.mudar(jid, estado="processando", worker={})
        mexidos = worker.retomar_orfaos()
        self.assertIn(jid, mexidos)
        j = job.ler_job(jid)
        self.assertEqual(j["estado"], "pendente")
        self.assertEqual(j["retomadas"], 1)
        self.assertIsNone(j["erro"])

    def test_orfao_estourado_vira_erro(self):
        jid = self.criar("orfao-2")
        self.mudar(jid, estado="processando", worker={}, retomadas=worker.MAX_RETOMADAS)
        worker.retomar_orfaos()
        j = job.ler_job(jid)
        self.assertEqual(j["estado"], "erro")
        self.assertIn("caiu", j["erro"])

    def test_concluido_nao_e_tocado(self):
        jid = self.criar("orfao-3")
        self.mudar(jid, estado="concluido")
        self.assertNotIn(jid, worker.retomar_orfaos())
        self.assertEqual(job.ler_job(jid)["estado"], "concluido")


class TestMotorDoJob(CasoWorker):
    def test_motor_explicito_vence(self):
        jb = {"imagens": [{"vista": "frente"}, {"vista": "costas"}], "modo": "livre"}
        self.assertEqual(worker._motor_do_job(jb, {"motor": "triposr"}), "triposr")

    def test_padrao_multivista_e_uma_vista(self):
        duas = {"imagens": [{"vista": "frente"}, {"vista": "costas"}], "modo": "livre"}
        uma = {"imagens": [{"vista": "frente"}], "modo": "livre"}
        self.assertEqual(worker._motor_do_job(duas, {}), "hunyuan-mv-turbo")
        self.assertEqual(worker._motor_do_job(uma, {}), "hunyuan-mini-turbo")


class TestLivreMin(unittest.TestCase):
    def test_env_valido_invalido_e_ausente(self):
        antigo = os.environ.get("OFICINA3D_LIVRE_MIN_GB")
        try:
            os.environ["OFICINA3D_LIVRE_MIN_GB"] = "7.5"
            self.assertEqual(worker._livre_min_gb(), 7.5)
            os.environ["OFICINA3D_LIVRE_MIN_GB"] = "abc"
            self.assertEqual(worker._livre_min_gb(), worker.LIVRE_MIN_GB_PADRAO)
            del os.environ["OFICINA3D_LIVRE_MIN_GB"]
            self.assertEqual(worker._livre_min_gb(), worker.LIVRE_MIN_GB_PADRAO)
        finally:
            if antigo is None:
                os.environ.pop("OFICINA3D_LIVRE_MIN_GB", None)
            else:
                os.environ["OFICINA3D_LIVRE_MIN_GB"] = antigo


if __name__ == "__main__":
    unittest.main()
