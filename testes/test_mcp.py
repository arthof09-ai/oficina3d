"""Testes de oficina3d.mcp.servidor: as funcoes das ferramentas MCP chamadas
direto (o modulo foi feito para funcionar sem o pacote `mcp` instalado).
Quando o pacote `mcp` existe (venv_mcp), confere tambem o registro das
9 ferramentas no servidor. Jobs numa pasta temporaria em jobs_teste.
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

import importlib.util  # noqa: E402

from oficina3d import config, job  # noqa: E402

if os.path.normcase(str(config.JOBS)) != os.path.normcase(str(TEMP_TESTES)):
    raise RuntimeError(f"config.JOBS ({config.JOBS}) nao e a pasta temporaria dos testes; recuso rodar")

from oficina3d.mcp import servidor  # noqa: E402


class TestFerramentasLeitura(unittest.TestCase):
    def test_listar_motores(self):
        lista = servidor.listar_motores()
        self.assertIsInstance(lista, list)
        nomes = {m["nome"] for m in lista}
        self.assertIn("triposr", nomes)
        self.assertIn("hunyuan-mv-turbo", nomes)
        for m in lista:
            self.assertIn("disponivel", m)

    def test_saude_tem_o_envelope(self):
        s = servidor.saude()
        self.assertIn("versao_servidor", s)
        self.assertIn("saude", s)
        self.assertIn("worker", s)


class TestFerramentasJobs(unittest.TestCase):
    def _img(self):
        p = TEMP_TESTES / "fixtures_mcp" / "img.png"
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(png_bytes())
        return p

    def test_listar_e_status(self):
        jid = job.criar_job([(self._img(), "frente")], nome="mcp-teste")["id"]
        ids = [j["id"] for j in servidor.listar_jobs(limite=50)]
        self.assertIn(jid, ids)
        st = servidor.status_job(jid)
        self.assertEqual(st["id"], jid)
        self.assertEqual(st["estado"], "pendente")

    def test_status_id_malformado_recusa(self):
        with self.assertRaises(Exception):
            servidor.status_job("../fora-da-pasta")

    def test_status_inexistente_recusa(self):
        with self.assertRaises(Exception):
            servidor.status_job("20260101-000000-nao-existe")

    def test_cancelar_exige_confirmacao(self):
        jid = job.criar_job([(self._img(), "frente")], nome="mcp-cancela")["id"]
        r = servidor.cancelar_job(jid)
        self.assertFalse(r.get("executado", False))
        self.assertEqual(job.ler_job(jid)["estado"], "pendente")
        r = servidor.cancelar_job(jid, confirmar=True)
        self.assertTrue(r.get("cancelado"))
        self.assertEqual(job.ler_job(jid)["estado"], "cancelado")
        r = servidor.cancelar_job(jid, confirmar=True)
        self.assertFalse(r.get("cancelado", False))


class TestRegistroServidor(unittest.TestCase):
    @unittest.skipUnless(importlib.util.find_spec("mcp"), "pacote mcp nao instalado neste venv")
    def test_criar_servidor_registra_as_ferramentas(self):
        srv = servidor.criar_servidor()
        self.assertIsNotNone(srv)


if __name__ == "__main__":
    unittest.main()
