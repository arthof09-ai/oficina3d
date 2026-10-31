"""Testes de oficina3d.cli: separar_vista, o parser e os comandos que nao
tocam a GPU (motores, status, cancelar). Saida capturada em memoria.
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

import argparse  # noqa: E402
import contextlib  # noqa: E402
import io  # noqa: E402

from oficina3d import cli, config, job  # noqa: E402

if os.path.normcase(str(config.JOBS)) != os.path.normcase(str(TEMP_TESTES)):
    raise RuntimeError(f"config.JOBS ({config.JOBS}) nao e a pasta temporaria dos testes; recuso rodar")


def capturar(fn, *args, **kw):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
        codigo = fn(*args, **kw)
    return codigo, buf.getvalue()


class TestSepararVista(unittest.TestCase):
    def test_com_vista(self):
        caminho, vista = cli.separar_vista("foto.png:frente")
        self.assertEqual(caminho, Path("foto.png"))
        self.assertEqual(vista, "frente")

    def test_sem_vista(self):
        caminho, vista = cli.separar_vista("foto.png")
        self.assertEqual(caminho, Path("foto.png"))
        self.assertIsNone(vista)

    def test_dois_pontos_do_windows_nao_e_vista(self):
        caminho, vista = cli.separar_vista(r"C:\imagens\foto.png")
        self.assertEqual(caminho, Path(r"C:\imagens\foto.png"))
        self.assertIsNone(vista)

    def test_sufixo_desconhecido_nao_e_vista(self):
        caminho, vista = cli.separar_vista("foto.png:banana")
        self.assertEqual(caminho, Path("foto.png:banana"))
        self.assertIsNone(vista)


class TestParser(unittest.TestCase):
    def test_comandos_ligados(self):
        casos = {
            ("motores",): cli.cmd_motores,
            ("status",): cli.cmd_status,
            ("worker",): cli.cmd_worker,
            ("cancelar", "algum-id"): cli.cmd_cancelar,
            ("baixar", "algum-id", "destino"): cli.cmd_baixar,
            ("enviar",): cli.cmd_enviar,
        }
        for argv, func in casos.items():
            a = cli.montar_parser().parse_args(list(argv))
            self.assertIs(a.func, func, argv)

    def test_enviar_opcoes(self):
        a = cli.montar_parser().parse_args(
            ["enviar", "--imagem", "a.png:frente", "--imagem", "b.png", "--seed", "7", "--nome", "Orc"])
        self.assertEqual(a.imagem, ["a.png:frente", "b.png"])
        self.assertEqual(a.seed, 7)
        self.assertEqual(a.modo, "livre")

    def test_sem_comando_da_erro(self):
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                cli.montar_parser().parse_args([])


class TestComandos(unittest.TestCase):
    def _img(self):
        p = TEMP_TESTES / "fixtures_cli" / "img.png"
        p.parent.mkdir(exist_ok=True)
        p.write_bytes(png_bytes())
        return p

    def test_motores_retorna_zero(self):
        codigo, saida = capturar(cli.cmd_motores, argparse.Namespace())
        self.assertEqual(codigo, 0)
        self.assertIn("motor", saida)
        self.assertIn("triposr", saida)

    def test_status_de_job_real_e_inexistente(self):
        jid = job.criar_job([(self._img(), "frente")], nome="cli-teste")["id"]
        codigo, saida = capturar(cli.cmd_status, argparse.Namespace(id=jid))
        self.assertEqual(codigo, 0)
        self.assertIn(jid, saida)
        self.assertIn("pendente", saida)
        codigo, _ = capturar(cli.cmd_status, argparse.Namespace(id="20260101-000000-nao-existe"))
        self.assertEqual(codigo, 1)

    def test_status_lista_sem_id(self):
        codigo, _ = capturar(cli.cmd_status, argparse.Namespace(id=None))
        self.assertEqual(codigo, 0)

    def test_main_motores(self):
        codigo, saida = capturar(cli.main, ["motores"])
        self.assertEqual(codigo, 0)


if __name__ == "__main__":
    unittest.main()
