"""Testes de oficina3d.travas (gpu.lock / worker.lock / GPU ocupada).

Rodar (cwd = app, no Python de producao):  ..\.venv_app\Scripts\python.exe -m unittest discover -s testes -p "test_travas.py" -v
Temporários só em <BASE>\\jobs_teste\\ (apagados no fim).
"""
import json
import os
import subprocess
import sys
import tempfile
import shutil
import time
import unittest
from pathlib import Path
from unittest import mock

APP = Path(__file__).resolve().parents[1]
JOBS_TESTE = APP.parent / "jobs_teste"
sys.path.insert(0, str(APP))

from oficina3d import travas  # noqa: E402

FILHO = r"""
import os, sys, time
sys.path.insert(0, sys.argv[1])
from oficina3d import travas
pasta, segurar, registro = sys.argv[2], float(sys.argv[3]), sys.argv[4]
with travas.adquirir_gpu(timeout=60, dono="filho", pasta=pasta):
    with open(registro, "a") as f:
        f.write("E %.6f %d\n" % (time.time(), os.getpid()))
    print("PRONTO", flush=True)
    if segurar < 0:
        while True:
            time.sleep(1)      # fica preso até ser morto
    time.sleep(segurar)
    with open(registro, "a") as f:
        f.write("S %.6f %d\n" % (time.time(), os.getpid()))
print("SOLTOU", flush=True)
"""


def _filho(pasta, segurar, registro):
    return subprocess.Popen([sys.executable, "-c", FILHO, str(APP), str(pasta), str(segurar), str(registro)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                            creationflags=0x08000000)


def _pid_reportado(registro):
    """PID que o proprio filho gravou no registro (o PID real do interprete).

    NAO usar Popen.pid: no venv do uv, sys.executable e um lancador (trampolim)
    cujo PID difere do PID do Python real que segura a trava (P1, auditoria do Critico).
    """
    for ln in Path(registro).read_text().splitlines():
        partes = ln.split()
        if partes and partes[0] == "E" and len(partes) >= 3:
            return int(partes[2])
    raise AssertionError("registro sem linha E com pid")


def _esperar_pronto(p, timeout=30):
    linha = p.stdout.readline().strip()
    if linha != "PRONTO":
        p.kill()
        raise AssertionError(f"filho não pegou a trava: {linha!r} {p.stderr.read()}")


class BaseTemp(unittest.TestCase):
    def setUp(self):
        JOBS_TESTE.mkdir(parents=True, exist_ok=True)
        self.tmp = Path(tempfile.mkdtemp(prefix="g_travas_", dir=JOBS_TESTE))
        self.pasta = self.tmp / "locks"
        self.registro = self.tmp / "registro.txt"
        self.filhos = []

    def tearDown(self):
        for p in self.filhos:
            if p.poll() is None:
                p.kill()
            p.wait(timeout=10)
            for s in (p.stdout, p.stderr):
                if s:
                    s.close()
        shutil.rmtree(self.tmp, ignore_errors=True)


class TestTravaEntreProcessos(BaseTemp):
    def test_dois_processos_disputando(self):
        p = _filho(self.pasta, 2.0, self.registro)
        self.filhos.append(p)
        _esperar_pronto(p)
        pid_filho = _pid_reportado(self.registro)
        est = travas.estado_trava("gpu", self.pasta)
        self.assertTrue(est["ocupada"])
        self.assertEqual(est["dono"]["pid"], pid_filho)
        self.assertTrue(est["dono_vivo"])
        # timeout=0: não espera, falha dizendo quem tem a trava
        with self.assertRaises(travas.TravaOcupada) as ctx:
            with travas.adquirir_gpu(timeout=0, pasta=self.pasta):
                pass
        self.assertEqual(ctx.exception.dono.get("pid"), pid_filho)
        # com timeout: espera o filho soltar e pega
        t0 = time.monotonic()
        with travas.adquirir_gpu(timeout=30, dono="pai", pasta=self.pasta) as info:
            self.assertEqual(info["pid"], os.getpid())
            self.assertNotIn("orfa_anterior", info)  # filho saiu limpo
            self.assertEqual(p.wait(timeout=10), 0)
        self.assertGreater(time.monotonic() - t0, 0.5)
        est = travas.estado_trava("gpu", self.pasta)
        self.assertFalse(est["ocupada"])
        self.assertFalse(est["orfa"])

    def test_exclusao_mutua_varios_processos(self):
        for _ in range(4):
            self.filhos.append(_filho(self.pasta, 0.3, self.registro))
        for p in self.filhos:
            self.assertEqual(p.wait(timeout=60), 0, p.stderr.read())
        eventos = [ln.split() for ln in self.registro.read_text().splitlines()]
        self.assertEqual(len(eventos), 8)
        eventos.sort(key=lambda e: float(e[1]))
        # Sequência tem de ser E S E S ... (nunca dois dentro ao mesmo tempo)
        self.assertEqual([e[0] for e in eventos], ["E", "S"] * 4)

    def test_trava_orfa_de_processo_morto(self):
        p = _filho(self.pasta, -1, self.registro)
        self.filhos.append(p)
        _esperar_pronto(p)
        pid_filho = _pid_reportado(self.registro)
        p.kill()  # "Finalizar tarefa": sem chance de soltar
        p.wait(timeout=10)
        est = travas.estado_trava("gpu", self.pasta)
        self.assertFalse(est["ocupada"])
        self.assertTrue(est["orfa"])
        self.assertFalse(est["dono_vivo"])
        with travas.adquirir_gpu(timeout=0, pasta=self.pasta) as info:
            self.assertEqual(info["orfa_anterior"]["pid"], pid_filho)
        self.assertFalse(travas.estado_trava("gpu", self.pasta)["orfa"])

    def test_registro_velho_com_pid_morto(self):
        # arquivo deixado por um processo que já não existe (ex.: PC desligado no meio)
        q = subprocess.run([sys.executable, "-c", "import os; print(os.getpid())"],
                           capture_output=True, text=True, creationflags=0x08000000)
        pid_morto = int(q.stdout.strip())
        self.pasta.mkdir(parents=True)
        (self.pasta / "worker.lock").write_text(json.dumps({"pid": pid_morto, "criado_em_processo": 1}))
        est = travas.estado_trava("worker", self.pasta)
        self.assertTrue(est["orfa"])
        self.assertFalse(est["dono_vivo"])
        with travas.adquirir_worker(pasta=self.pasta) as info:
            self.assertEqual(info["orfa_anterior"]["pid"], pid_morto)


class TestTravaMesmoProcesso(BaseTemp):
    def test_nao_reentrante(self):
        with travas.adquirir_worker(pasta=self.pasta):
            with self.assertRaises(travas.TravaOcupada):
                with travas.adquirir_worker(pasta=self.pasta):
                    pass
            self.assertTrue(travas.estado_trava("worker", self.pasta)["ocupada"])
        self.assertFalse(travas.estado_trava("worker", self.pasta)["ocupada"])

    def test_gpu_e_worker_independentes(self):
        with travas.adquirir_worker(pasta=self.pasta), travas.adquirir_gpu(timeout=0, pasta=self.pasta):
            e = travas.estado_travas(self.pasta)
            self.assertTrue(e["gpu"]["ocupada"] and e["worker"]["ocupada"])

    def test_solta_em_excecao(self):
        with self.assertRaises(ValueError):
            with travas.adquirir_gpu(timeout=0, pasta=self.pasta):
                raise ValueError("falha no motor")
        with travas.adquirir_gpu(timeout=0, pasta=self.pasta):
            pass

    def test_estado_sem_arquivo(self):
        e = travas.estado_trava("gpu", self.pasta)
        self.assertFalse(e["ocupada"] or e["orfa"])

    def test_pid_reaproveitado(self):
        _, criado = travas._tempo_criacao(os.getpid())
        self.assertTrue(travas.processo_vivo(os.getpid(), criado))
        self.assertFalse(travas.processo_vivo(os.getpid(), (criado or 0) + 12345))
        self.assertFalse(travas.processo_vivo(0))


SAIDA_GPU = "NVIDIA GeForce RTX 4060, 610.88, 8188, 1101, 6856, 5\n"
SAIDA_APPS = ("1864, [Insufficient Permissions], [N/A]\n"
              "3088, C:\\Windows\\explorer.exe, [N/A]\n"
              "4242, C:\\Jogos\\Exemplo\\JogoPesado.exe, 2300\n")


class TestGpu(unittest.TestCase):
    def test_interpretar(self):
        g = travas.interpretar_query_gpu(SAIDA_GPU)
        self.assertEqual(g["vram_total_mb"], 8188)
        self.assertEqual(g["vram_livre_mb"], 6856)
        self.assertEqual(g["uso_pct"], 5)
        apps = travas.interpretar_compute_apps(SAIDA_APPS)
        self.assertEqual(len(apps), 3)
        self.assertIsNone(apps[0]["vram_mb"])
        self.assertEqual(apps[2]["exe"], "jogopesado.exe")
        self.assertEqual(apps[2]["vram_mb"], 2300)

    def _estado(self, gpu, apps=SAIDA_APPS, tela=False, **kw):
        with mock.patch.object(travas, "ler_gpu", return_value=gpu), \
                mock.patch.object(travas, "listar_processos_gpu",
                                  return_value=travas.interpretar_compute_apps(apps)), \
                mock.patch.object(travas, "_tela_cheia", return_value=tela):
            return travas.gpu_ocupada_por_outros(amostras=1, intervalo_s=0, processos_pesados=[], **kw)

    def test_livre(self):
        e = self._estado(travas.interpretar_query_gpu(SAIDA_GPU))
        self.assertFalse(e)
        self.assertEqual(e.motivo, "livre")

    def test_ocupada_por_uso(self):
        g = dict(travas.interpretar_query_gpu(SAIDA_GPU), uso_pct=90)
        e = self._estado(g, limiar_uso_pct=40)
        self.assertTrue(e)
        self.assertIn("uso da GPU", e.motivo)

    def test_ocupada_por_vram(self):
        g = dict(travas.interpretar_query_gpu(SAIDA_GPU), vram_usada_mb=5000)
        self.assertTrue(self._estado(g, limiar_vram_mb=3000))
        self.assertFalse(self._estado(g, limiar_vram_mb=6000))

    def test_ocupada_por_processo_pesado_e_tela_cheia(self):
        g = travas.interpretar_query_gpu(SAIDA_GPU)
        with mock.patch.object(travas, "ler_gpu", return_value=g), \
                mock.patch.object(travas, "listar_processos_gpu",
                                  return_value=travas.interpretar_compute_apps(SAIDA_APPS)), \
                mock.patch.object(travas, "_tela_cheia", return_value=False):
            e = travas.gpu_ocupada_por_outros(amostras=1, processos_pesados=["JogoPesado.exe"])
        self.assertTrue(e)
        self.assertEqual(e.pesados, ["jogopesado.exe"])
        self.assertTrue(self._estado(g, tela=True))
        self.assertFalse(self._estado(g, tela=True, considerar_tela_cheia=False))

    def test_limiar_por_variavel(self):
        g = dict(travas.interpretar_query_gpu(SAIDA_GPU), uso_pct=20)
        with mock.patch.dict(os.environ, {"OFICINA3D_GPU_USO_MAX": "15"}):
            self.assertTrue(self._estado(g))
        with mock.patch.dict(os.environ, {"OFICINA3D_GPU_USO_MAX": "50"}):
            self.assertFalse(self._estado(g))

    def test_falha_de_leitura_e_ocupada(self):
        with mock.patch.object(travas, "ler_gpu", side_effect=RuntimeError("sem driver")):
            e = travas.gpu_ocupada_por_outros(amostras=1)
        self.assertTrue(e)
        self.assertEqual(e.erro, "sem driver")

    def test_esperar_gpu_livre(self):
        livre = travas.EstadoGpu(False, "livre")
        ocupada = travas.EstadoGpu(True, "jogo")
        vistos = []
        with mock.patch.object(travas, "gpu_ocupada_por_outros", side_effect=[ocupada, ocupada, livre]):
            ok = travas.esperar_gpu_livre(verificar_a_cada_s=0.01, ao_esperar=vistos.append)
        self.assertTrue(ok)
        self.assertEqual(len(vistos), 2)
        with mock.patch.object(travas, "gpu_ocupada_por_outros", return_value=ocupada):
            self.assertFalse(travas.esperar_gpu_livre(verificar_a_cada_s=0.01, max_espera_s=0.05))
            self.assertFalse(travas.esperar_gpu_livre(parar=lambda: True))

    @unittest.skipUnless(travas._nvidia_smi(), "nvidia-smi ausente")
    def test_nvidia_smi_real(self):
        g = travas.ler_gpu()
        self.assertGreater(g["vram_total_mb"], 0)
        e = travas.gpu_ocupada_por_outros(amostras=1, intervalo_s=0)
        self.assertIsInstance(e.como_dict(), dict)


if __name__ == "__main__":
    unittest.main()
