"""Testes de oficina3d.saude (só leitura) e do modelo da Tarefa Agendada.

Rodar (cwd = app):  py -3.12 -m unittest discover -s testes -p "test_saude.py" -v
Temporários só em <BASE>\\jobs_teste\\ (apagados no fim). Não registra tarefa.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

APP = Path(__file__).resolve().parents[1]
JOBS_TESTE = APP.parent / "jobs_teste"
sys.path.insert(0, str(APP))

from oficina3d import saude, travas  # noqa: E402


class TestDisco(unittest.TestCase):
    def test_espaco(self):
        d = saude.espaco_disco()
        self.assertGreater(d["total_gb"], 0)
        self.assertGreaterEqual(d["livre_gb"], 0)

    def test_disco_ok(self):
        self.assertTrue(saude.disco_ok(limite_gb=0))
        self.assertFalse(saude.disco_ok(limite_gb=10 ** 9))
        with mock.patch.dict(os.environ, {"OFICINA3D_LIMITE_DISCO_GB": str(10 ** 9)}):
            self.assertFalse(saude.disco_ok())
        self.assertFalse(saude.disco_ok(unidade="Q:\\nao\\existe\\"))  # na dúvida, não ok

    def test_alerta_disco_baixo(self):
        with mock.patch.dict(os.environ, {"OFICINA3D_LIMITE_DISCO_GB": str(10 ** 9)}):
            r = saude.saude(medir_drive=False, ler_gpu=False)
        self.assertFalse(r["disco"]["ok"])
        self.assertTrue(any("GB livres" in a for a in r["alertas"]))


class TestTamanhoPasta(unittest.TestCase):
    def setUp(self):
        JOBS_TESTE.mkdir(parents=True, exist_ok=True)
        self.tmp = Path(tempfile.mkdtemp(prefix="g_saude_", dir=JOBS_TESTE))

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_soma(self):
        (self.tmp / "a" / "b").mkdir(parents=True)
        (self.tmp / "x.bin").write_bytes(b"1" * 1000)
        (self.tmp / "a" / "b" / "y.bin").write_bytes(b"2" * 24)
        r = saude.tamanho_pasta(self.tmp)
        self.assertEqual((r["bytes"], r["arquivos"], r["parcial"]), (1024, 2, False))

    def test_inexistente(self):
        r = saude.tamanho_pasta(self.tmp / "nao")
        self.assertFalse(r["existe"])
        self.assertEqual(r["bytes"], 0)

    def test_cache_drive_usa_localappdata(self):
        (self.tmp / "Google" / "DriveFS").mkdir(parents=True)
        (self.tmp / "Google" / "DriveFS" / "c.db").write_bytes(b"0" * 10)
        with mock.patch.dict(os.environ, {"LOCALAPPDATA": str(self.tmp)}):
            r = saude.cache_drive()
        self.assertEqual(r["bytes"], 10)


class TestWindowsUpdate(unittest.TestCase):
    AGORA = datetime(2026, 10, 31, 15, 0, tzinfo=timezone.utc)

    def test_pausado(self):
        v = {"PauseUpdatesExpiryTime": "2026-12-05T15:08:40Z", "PauseQualityUpdatesEndTime": "2026-12-01T00:00:00Z"}
        r = saude.interpretar_windows_update(v, self.AGORA)
        self.assertTrue(r["pausado"])
        self.assertTrue(r["ate"].startswith("2026-12-05"))
        self.assertAlmostEqual(r["dias_restantes"], 35.0, delta=0.1)

    def test_pausa_vencida_ou_ausente(self):
        self.assertFalse(saude.interpretar_windows_update({"PauseUpdatesExpiryTime": "2026-10-01T00:00:00Z"},
                                                          self.AGORA)["pausado"])
        self.assertFalse(saude.interpretar_windows_update({}, self.AGORA)["pausado"])
        self.assertFalse(saude.interpretar_windows_update({"PauseUpdatesExpiryTime": "lixo"}, self.AGORA)["pausado"])

    def test_leitura_real_do_registro(self):
        r = saude.windows_update()
        self.assertIn("pausado", r)
        self.assertIn(r["pausado"], (True, False, None))


class TestSaude(unittest.TestCase):
    def test_saude_completa(self):
        r = saude.saude()
        for chave in ("medido_em", "disco", "gpu", "cache_drive", "travas", "windows_update", "alertas", "ok"):
            self.assertIn(chave, r)
        self.assertEqual(set(r["travas"]), {"gpu", "worker"})
        json.dumps(r)  # serializável

    def test_gpu_com_erro_nao_quebra(self):
        with mock.patch.object(travas, "ler_gpu", side_effect=RuntimeError("sem nvidia-smi")):
            r = saude.saude(medir_drive=False)
        self.assertIn("erro", r["gpu"])
        self.assertFalse(r["ok"])

    def test_cli_json(self):
        p = subprocess.run([sys.executable, "-m", "oficina3d.saude", "--json", "--sem-drive"], cwd=str(APP),
                           capture_output=True, timeout=120, creationflags=0x08000000)
        self.assertEqual(p.returncode, 0, p.stderr.decode("utf-8", "replace"))
        dado = json.loads(p.stdout.decode("utf-8"))
        self.assertIn("disco", dado)
        self.assertNotIn("cache_drive", dado)

    def test_cli_texto(self):
        p = subprocess.run([sys.executable, "-m", "oficina3d.saude", "--sem-drive"], cwd=str(APP),
                           capture_output=True, timeout=120, creationflags=0x08000000)
        self.assertEqual(p.returncode, 0)
        self.assertIn("Disco", p.stdout.decode("utf-8"))


class TestModeloTarefa(unittest.TestCase):
    """Confere o XML da tarefa sem registrar nada."""
    PASTA = APP / "instalacao" / "tarefa_worker"
    NS = {"t": "http://schemas.microsoft.com/windows/2004/02/mit/task"}

    def test_xml(self):
        texto = (self.PASTA / "tarefa_worker.xml").read_text(encoding="utf-8")
        texto = texto.replace("__USUARIO__", "PC\\usuario").replace("__APP__", "C:\\X\\app").replace("__BASE__", "C:\\X")
        raiz = ET.fromstring(texto.encode("utf-8"))
        q = lambda c: raiz.find(c, self.NS)  # noqa: E731
        self.assertEqual(q("t:Triggers/t:LogonTrigger/t:Delay").text, "PT2M")
        self.assertEqual(q("t:Triggers/t:LogonTrigger/t:UserId").text, "PC\\usuario")
        self.assertEqual(q("t:Principals/t:Principal/t:RunLevel").text, "LeastPrivilege")
        self.assertEqual(q("t:Principals/t:Principal/t:LogonType").text, "InteractiveToken")
        self.assertGreaterEqual(int(q("t:Settings/t:Priority").text), 7)
        self.assertIsNotNone(q("t:Settings/t:RestartOnFailure"))
        self.assertIn("pythonw.exe", q("t:Actions/t:Exec/t:Command").text)
        self.assertEqual(q("t:Actions/t:Exec/t:WorkingDirectory").text, "C:\\X\\app")
        self.assertNotIn("__", texto)

    def test_lancador_compila(self):
        compile((self.PASTA / "iniciar_worker.py").read_text(encoding="utf-8"), "iniciar_worker.py", "exec")


if __name__ == "__main__":
    unittest.main()
