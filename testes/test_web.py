"""Testes da API web (oficina3d.web.app) com o TestClient do FastAPI.
O app e montado com hosts_locais={"testclient"} (o parametro existe para
testes) e a pasta de jobs temporaria da suite. Nada sobe porta de verdade.
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

from fastapi.testclient import TestClient  # noqa: E402

from oficina3d import motores  # noqa: E402
from oficina3d.web.app import criar_app  # noqa: E402


class TestWeb(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # pedido_local exige: cliente em hosts_locais ("testclient"), Host de
        # loopback (base_url 127.0.0.1) e, nos POSTs, o cabecalho anti-CSRF.
        cls.cliente = TestClient(criar_app(hosts_locais={"testclient"}),
                                 base_url="http://127.0.0.1:8765",
                                 headers={"X-Oficina3D": "1"})

    def test_pagina_inicial(self):
        r = self.cliente.get("/")
        self.assertEqual(r.status_code, 200)
        self.assertIn("text/html", r.headers.get("content-type", ""))

    def test_motores_batem_com_o_modulo(self):
        r = self.cliente.get("/api/motores")
        self.assertEqual(r.status_code, 200)
        dados = r.json()
        esperado = {m["nome"]: m["disponivel"] for m in motores.listar()}
        obtido = {m["nome"]: m["disponivel"] for m in dados}
        self.assertEqual(obtido, esperado)

    def test_saude_responde_ok(self):
        r = self.cliente.get("/api/saude")
        self.assertEqual(r.status_code, 200)
        self.assertIn("saude", r.json())

    def test_criar_sem_imagem_e_422(self):
        r = self.cliente.post("/api/jobs", data={"modo": "livre"})
        self.assertEqual(r.status_code, 422)

    def test_criar_modo_invalido_e_422(self):
        r = self.cliente.post("/api/jobs", data={"modo": "banana"},
                              files={"imagens": ("a.png", png_bytes(), "image/png")})
        self.assertEqual(r.status_code, 422)

    def test_fluxo_criar_ler_cancelar(self):
        r = self.cliente.post("/api/jobs", data={"nome": "web-teste"},
                              files={"imagens": ("frente.png", png_bytes(), "image/png")})
        self.assertEqual(r.status_code, 201, r.text[:300])
        jid = r.json()["id"]
        r = self.cliente.get(f"/api/jobs/{jid}")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["id"], jid)
        r = self.cliente.get("/api/jobs")
        self.assertIn(jid, [j["id"] for j in r.json()])
        r = self.cliente.post(f"/api/jobs/{jid}/cancelar")
        self.assertEqual(r.status_code, 200, r.text[:300])
        r = self.cliente.get(f"/api/jobs/{jid}")
        self.assertEqual(r.json()["estado"], "cancelado")

    def test_job_inexistente_e_404(self):
        r = self.cliente.get("/api/jobs/20260101-000000-nao-existe")
        self.assertEqual(r.status_code, 404)


if __name__ == "__main__":
    unittest.main()
