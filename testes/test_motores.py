"""Testes do pacote oficina3d.motores (sem GPU, sem torch).

Rodar (cwd = app\\):  py -3.12 -m unittest discover -s testes -p "test_motores.py" -v

Usa um MOTOR FALSO: um script Python (gravado na pasta temporária do teste) que segue o mesmo
protocolo dos runners de verdade — lê pedido_motor.json, imprime "PROGRESSO <n> <msg>" (algumas
coladas na barra do tqdm), grava um GLB mínimo e resultado_motor.json.
Tudo acontece em BASE\\jobs_teste\\nucleo-*; a pasta é apagada no fim. A fila real (jobs\\) nunca é tocada.

Este arquivo também serve de apoio para test_worker.py e test_cli.py (AmbienteNucleo, png_rgba...).
"""
from __future__ import annotations

import json
import os
import secrets
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import zlib
from pathlib import Path
from unittest import mock

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d import config, motores  # noqa: E402
from oficina3d.motores import base  # noqa: E402

RAIZ_TESTES = Path(config.JOBS_TESTE)

RUNNER_FALSO = r'''
"""Motor FALSO dos testes do núcleo: mesmo protocolo dos runners reais, sem GPU."""
import json, os, struct, subprocess, sys, time

p = json.load(open(sys.argv[1], encoding="utf-8"))
op = p.get("opcoes") or {}
modo = op.get("modo_falso") or os.environ.get("MODO_FALSO") or "ok"
pasta = os.path.dirname(p["resultado"])

def prog(pct, msg):
    sys.stdout.write(f"PROGRESSO {pct} {msg}\n"); sys.stdout.flush()

def gravar(caminho, dados):
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f)

def glb(caminho):
    js = json.dumps({"asset": {"version": "2.0"}}).encode()
    js += b" " * (-len(js) % 4)
    corpo = struct.pack("<II", len(js), 0x4E4F534A) + js
    with open(caminho, "wb") as f:
        f.write(b"glTF" + struct.pack("<II", 2, 12 + len(corpo)) + corpo)

pids = {"filho": os.getpid()}
prog(1, "carregando bibliotecas")
if modo == "neto":
    neto = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(120)"])
    pids["neto"] = neto.pid
gravar(os.path.join(pasta, "pids_falso.json"), pids)

if modo in ("neto", "silencioso"):
    time.sleep(120)
elif modo == "lento":
    for i in range(600):
        prog(10 + i % 80, f"difusao {i}")
        time.sleep(0.1)
elif modo == "erro":
    gravar(p["resultado"], {"ok": False, "erro": "falha simulada do motor"})
    sys.exit(1)
elif modo == "sem_resultado":
    print("Traceback simulado: CUDA out of memory", flush=True)
    sys.exit(3)
else:
    # Barra do tqdm (stderr, com \r) misturada com o PROGRESSO, inclusive colada sem separador.
    sys.stderr.write("Diffusion Sampling::  33%|###       | 1/3 [00:01<00:02]\r"); sys.stderr.flush()
    sys.stdout.write("\rDiffusion Sampling::  33%|###   | 1/3\rPROGRESSO 33 difusao 1/3\n"); sys.stdout.flush()
    sys.stdout.write("Diffusion Sampling::  66%|######| 2/3PROGRESSO 66 difusao 2/3\n"); sys.stdout.flush()
    prog(90, "gravando forma.glb")
    glb(p["saida_glb"])
    gravar(os.path.join(pasta, "eco_pedido.json"), p)
    gravar(p["resultado"], {"ok": True, "glb": p["saida_glb"], "avisos": ["aviso do motor falso"],
                            "metricas": {"triangulos": 12, "vertices": 8, "fechada": True, "tempo_s": 0.1,
                                         "vram_pico_torch_mb": 0, "eixo_cima": "Y"}})
    prog(100, "pronto")
'''


# --------------------------------------------------------------------------- apoio comum

def png_rgba(caminho: Path, lado: int = 64, cor=(200, 60, 40, 255)) -> Path:
    """PNG RGBA válido, só com a biblioteca padrão."""
    linhas = b"".join(b"\x00" + bytes(cor) * lado for _ in range(lado))

    def chunk(tipo: bytes, dados: bytes) -> bytes:
        return struct.pack(">I", len(dados)) + tipo + dados + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF)

    dados = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", lado, lado, 8, 6, 0, 0, 0))
             + chunk(b"IDAT", zlib.compress(linhas)) + chunk(b"IEND", b""))
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(dados)
    return caminho


def glb_minimo(caminho: Path) -> Path:
    js = json.dumps({"asset": {"version": "2.0"}}).encode()
    js += b" " * (-len(js) % 4)
    corpo = struct.pack("<II", len(js), 0x4E4F534A) + js
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_bytes(b"glTF" + struct.pack("<II", 2, 12 + len(corpo)) + corpo)
    return caminho


def pid_morto() -> int:
    """PID de um processo que já terminou (para simular worker caído)."""
    p = subprocess.Popen([sys.executable, "-c", "pass"])
    p.wait()
    return p.pid


def esperar_ate(cond, limite: float = 20.0, passo: float = 0.05) -> bool:
    fim = time.time() + limite
    while time.time() < fim:
        if cond():
            return True
        time.sleep(passo)
    return cond()


class AmbienteNucleo:
    """Pasta temporária em jobs_teste\\ + config.JOBS/LOCKS/TMP apontando para ela + motor 'falso'."""

    def __init__(self, caso: unittest.TestCase, nome: str):
        self.caso = caso
        self.raiz = RAIZ_TESTES / f"nucleo-{nome}-{os.getpid()}-{secrets.token_hex(3)}"
        self.jobs = self.raiz / "jobs"
        self.locks = self.raiz / "locks"
        self.tmp = self.raiz / "tmp"
        self.dados = self.raiz / "dados"
        for p in (self.jobs, self.locks, self.tmp, self.dados):
            p.mkdir(parents=True, exist_ok=True)
        self.runner = self.raiz / "runner_falso.py"
        self.runner.write_text(RUNNER_FALSO, encoding="utf-8")
        self.spec = {
            "descricao": "motor falso dos testes", "tipo": "falso", "python": sys.executable,
            "runner": str(self.runner), "cwd": str(self.raiz), "passos": 3,
            "aceita_multivista": False, "usa_gpu": False, "env": {"MODO_FALSO": "ok"},
        }
        self._patches = [
            mock.patch.object(config, "JOBS", self.jobs),
            mock.patch.object(config, "LOCKS", self.locks),
            mock.patch.object(config, "TMP", self.tmp),
            mock.patch.object(config, "MOTORES", tuple(config.MOTORES) + ("falso",)),
            mock.patch.dict(motores.MOTORES, {"falso": self.spec}),
            mock.patch.dict(os.environ, {"OFICINA3D_IGNORAR_GPU_OCUPADA": "1", "OFICINA3D_LIVRE_MIN_GB": "0"}),
        ]
        os.environ.pop("OFICINA3D_ARQUIVO", None)
        for p in self._patches:
            p.start()
        os.environ.pop("OFICINA3D_ARQUIVO", None)
        # Proteção da lição E4 da v1: os testes NUNCA podem mexer na fila real.
        assert Path(config.JOBS).resolve().is_relative_to(RAIZ_TESTES.resolve()), config.JOBS
        caso.addCleanup(self.fechar)

    def modo_falso(self, modo: str) -> None:
        self.spec["env"] = {"MODO_FALSO": modo}

    def fechar(self) -> None:
        for p in reversed(self._patches):
            p.stop()
        for _ in range(40):
            shutil.rmtree(self.raiz, ignore_errors=True)
            if not self.raiz.exists():
                break
            time.sleep(0.25)


def tearDownModule():  # noqa: N802
    # Sobras de execuções interrompidas deste processo (pastas nucleo-* com o nosso PID).
    for p in RAIZ_TESTES.glob(f"nucleo-*-{os.getpid()}-*"):
        shutil.rmtree(p, ignore_errors=True)


# --------------------------------------------------------------------------- testes

class TestListar(unittest.TestCase):
    def setUp(self):
        self.amb = AmbienteNucleo(self, "listar")

    def test_catalogo_do_plano(self):
        nomes = [m["nome"] for m in motores.listar()]
        for n in ("hunyuan-mini-turbo", "hunyuan-mv-turbo", "hunyuan-mini", "hunyuan-mv", "triposr"):
            self.assertIn(n, nomes)
        self.assertNotIn("hunyuan-full", nomes)  # fora na v2 (plano 5)
        for n in config.MOTORES:
            if n != "falso":
                self.assertIn(n, motores.MOTORES, "config.MOTORES e motores.MOTORES precisam bater")

    def test_campos_e_motivo(self):
        for m in motores.listar():
            for chave in ("nome", "descricao", "aceita_multivista", "disponivel", "motivo", "passos_padrao"):
                self.assertIn(chave, m)
            if not m["disponivel"]:
                self.assertTrue(m["motivo"], m["nome"])
        mv = {m["nome"]: m for m in motores.listar()}
        self.assertTrue(mv["hunyuan-mv-turbo"]["aceita_multivista"])
        self.assertTrue(mv["hunyuan-mv-turbo"]["flashvdm"])
        self.assertEqual(mv["hunyuan-mv-turbo"]["vistas"], "2-4")
        self.assertFalse(mv["triposr"]["aceita_multivista"])
        self.assertTrue(mv["falso"]["disponivel"], mv["falso"]["motivo"])

    def test_disponivel_quando_venv_e_pesos_existem(self):
        hy, hf = self.amb.raiz / "hy3dgen", self.amb.raiz / "hf"
        repo_motor = self.amb.raiz / "Hunyuan3D-2GP"
        repo_motor.mkdir()
        with mock.patch.object(motores, "_pastas_modelos", return_value=(hy, hf)), \
                mock.patch.object(config, "PY_HUNYUAN", Path(sys.executable)), \
                mock.patch.object(config, "MOTOR_HUNYUAN", repo_motor):
            m = {x["nome"]: x for x in motores.listar()}["hunyuan-mini-turbo"]
            self.assertFalse(m["disponivel"])
            self.assertIn("hunyuan3d-dit-v2-mini-turbo", m["motivo"])
            # DiT no HY3DGEN_MODELS; VAE turbo no cache do Hugging Face (as duas formas que o hy3dgen usa)
            dit = hy / "tencent" / "Hunyuan3D-2mini" / "hunyuan3d-dit-v2-mini-turbo" / "model.fp16.safetensors"
            dit.parent.mkdir(parents=True)
            dit.write_bytes(b"x")
            m = {x["nome"]: x for x in motores.listar()}["hunyuan-mini-turbo"]
            self.assertFalse(m["disponivel"])
            self.assertIn("vae-v2-mini-turbo", m["motivo"])
            vae = (hf / "hub" / "models--tencent--Hunyuan3D-2mini" / "snapshots" / "abc123"
                   / "hunyuan3d-vae-v2-mini-turbo" / "model.fp16.safetensors")
            vae.parent.mkdir(parents=True)
            vae.write_bytes(b"x")
            m = {x["nome"]: x for x in motores.listar()}["hunyuan-mini-turbo"]
            self.assertTrue(m["disponivel"], m["motivo"])


class TestPedido(unittest.TestCase):
    def setUp(self):
        self.amb = AmbienteNucleo(self, "pedido")
        self.imgs = {v: png_rgba(self.amb.dados / f"{v}.png") for v in
                     ("frente", "costas", "esquerda", "direita", "frente-direita")}

    def _lista(self, *vistas):
        return [{"arquivo": str(self.imgs[v]), "vista": v} for v in vistas]

    def test_multivista_mapeia_vistas_e_forca_flashvdm(self):
        spec = motores.MOTORES["hunyuan-mv-turbo"]
        ped, avisos = motores._montar_pedido("hunyuan-mv-turbo", spec,
                                             self._lista("frente", "costas", "esquerda", "direita", "frente-direita"),
                                             {"flashvdm": False, "seed": 7}, self.amb.raiz)
        self.assertEqual([i["vista_motor"] for i in ped["imagens"]], ["front", "back", "left", "right"])
        self.assertTrue(ped["flashvdm"], "mv-turbo sempre com FlashVDM")
        self.assertTrue(ped["multivista"])
        self.assertEqual(ped["passos"], 5)
        self.assertEqual(ped["seed"], 7)
        self.assertEqual(ped["mc_algo"], "mc")
        self.assertTrue(any("frente-direita" in a for a in avisos))

    def test_multivista_com_uma_vista_avisa(self):
        spec = motores.MOTORES["hunyuan-mv-turbo"]
        ped, avisos = motores._montar_pedido("hunyuan-mv-turbo", spec, self._lista("frente"), {}, self.amb.raiz)
        self.assertEqual(len(ped["imagens"]), 1)
        self.assertTrue(any("recomendado 2-4" in a for a in avisos))

    def test_uma_vista_escolhe_frente(self):
        spec = motores.MOTORES["hunyuan-mini-turbo"]
        ped, avisos = motores._montar_pedido("hunyuan-mini-turbo", spec, self._lista("costas", "frente"),
                                             {"passos": None}, self.amb.raiz)
        self.assertEqual(len(ped["imagens"]), 1)
        self.assertEqual(Path(ped["imagens"][0]["caminho"]).name, "frente.png")
        self.assertEqual(ped["passos"], 5)
        self.assertFalse(ped["multivista"])
        self.assertTrue(avisos)

    def test_flashvdm_desliga_sem_vae_turbo_em_motor_nao_turbo(self):
        spec = motores.MOTORES["hunyuan-mini"]
        with mock.patch.object(motores, "_achar_peso", return_value=None):
            ped, avisos = motores._montar_pedido("hunyuan-mini", spec, self._lista("frente"), {"flashvdm": True},
                                                 self.amb.raiz)
        self.assertFalse(ped["flashvdm"])
        self.assertTrue(any("FlashVDM desligado" in a for a in avisos))
        with mock.patch.object(motores, "_achar_peso", return_value=Path(sys.executable)):
            ped, _ = motores._montar_pedido("hunyuan-mini", spec, self._lista("frente"), {}, self.amb.raiz)
        self.assertTrue(ped["flashvdm"])
        self.assertEqual(ped["passos"], 30)

    def test_triposr(self):
        ped, _ = motores._montar_pedido("triposr", motores.MOTORES["triposr"], self._lista("frente"),
                                        {"seed": 1}, self.amb.raiz)
        self.assertEqual(ped["tipo"], "triposr")
        self.assertEqual(ped["mc_resolucao"], 256)
        self.assertTrue(ped["saida_glb"].endswith("forma.glb"))

    def test_caminho_relativo_e_inexistente(self):
        spec = motores.MOTORES["hunyuan-mini-turbo"]
        with self.assertRaises(ValueError):
            motores._montar_pedido("x", spec, [{"arquivo": "preproc/frente.png", "vista": "frente"}], {}, self.amb.raiz)
        with self.assertRaises(FileNotFoundError):
            motores._montar_pedido("x", spec, [{"arquivo": str(self.amb.dados / "nao.png"), "vista": "frente"}],
                                   {}, self.amb.raiz)

    def test_motor_desconhecido(self):
        with self.assertRaises(ValueError):
            motores.gerar("hunyuan-full", self._lista("frente"), {}, self.amb.raiz / "forma")

    def test_indisponivel_da_erro_claro(self):
        with mock.patch.object(config, "PY_TRIPOSR", self.amb.raiz / "nao_existe" / "python.exe"):
            with self.assertRaises(motores.ErroMotor) as cm:
                motores.gerar("triposr", self._lista("frente"), {}, self.amb.raiz / "forma")
        self.assertIn("indisponível", str(cm.exception))


class TestGerarFalso(unittest.TestCase):
    def setUp(self):
        self.amb = AmbienteNucleo(self, "gerar")
        self.img = png_rgba(self.amb.dados / "frente.png")
        self.pasta = self.amb.raiz / "job" / "forma"

    def _gerar(self, modo="ok", progresso=None, **op):
        return motores.gerar("falso", [{"arquivo": str(self.img), "vista": "frente"}],
                             {"modo_falso": modo, "seed": 42, **op}, self.pasta, progresso=progresso)

    def test_ok_progresso_glb_metricas(self):
        visto = []
        r = self._gerar(progresso=lambda p, m: visto.append((p, m)))
        self.assertEqual(r["glb"], self.pasta / "forma.glb")
        self.assertTrue(base.glb_valido(r["glb"]))
        pcts = [p for p, _ in visto]
        for esperado in (1, 33, 66, 90, 100):
            self.assertIn(esperado, pcts, visto)
        self.assertIn((66, "difusao 2/3"), visto, "PROGRESSO colado na barra do tqdm")
        m = r["metricas"]
        for chave in ("tempo_s", "vram_pico_mb", "triangulos", "vertices", "fechada", "tempo_processo_s"):
            self.assertIn(chave, m)
        self.assertEqual(m["triangulos"], 12)
        self.assertIn("aviso do motor falso", r["avisos"])
        self.assertTrue((self.pasta / "motor.log").is_file())
        log = (self.pasta / "motor.log").read_bytes()
        self.assertIn(b"Diffusion Sampling", log)
        eco = json.loads((self.pasta / "eco_pedido.json").read_text(encoding="utf-8"))
        self.assertTrue(Path(eco["imagens"][0]["caminho"]).is_absolute())
        self.assertEqual(eco["seed"], 42)
        self.assertEqual(eco["opcoes"]["modo_falso"], "ok")

    def test_ambiente_do_subprocesso(self):
        env = base.env_motor({"HF_HUB_OFFLINE": "1"})
        self.assertEqual(env["HF_HUB_OFFLINE"], "1")
        self.assertEqual(env["PYTHONUNBUFFERED"], "1")
        self.assertEqual(Path(env["TEMP"]), self.amb.tmp)
        self.assertIn("HY3DGEN_MODELS", env)

    def test_erro_do_motor(self):
        with self.assertRaises(motores.ErroMotor) as cm:
            self._gerar("erro")
        self.assertIn("falha simulada do motor", str(cm.exception))

    def test_saiu_sem_resultado_mostra_fim_do_log(self):
        with self.assertRaises(motores.ErroMotor) as cm:
            self._gerar("sem_resultado")
        self.assertIn("código 3", str(cm.exception))
        self.assertIn("CUDA out of memory", str(cm.exception))

    def test_cancelar_pelo_callback_mata_filho_e_neto(self):
        class Parar(Exception):
            pass

        pids_arq = self.pasta / "pids_falso.json"

        def progresso(p, m):
            if pids_arq.exists() and "neto" in pids_arq.read_text(encoding="utf-8"):
                raise Parar()

        with mock.patch.object(motores, "INTERVALO_BATIMENTO_S", 0.2):
            t0 = time.time()
            with self.assertRaises(Parar):
                self._gerar("neto", progresso=progresso)
        self.assertLess(time.time() - t0, 30)
        pids = json.loads(pids_arq.read_text(encoding="utf-8"))
        self.assertTrue(esperar_ate(lambda: not base.processo_vivo(pids["filho"]), 10), "filho vivo")
        self.assertTrue(esperar_ate(lambda: not base.processo_vivo(pids["neto"]), 10), "neto vivo (Job Object)")

    def test_tempo_maximo(self):
        with self.assertRaises(motores.ErroMotor) as cm:
            self._gerar("silencioso", tempo_max_s=1.5)
        self.assertIn("tempo máximo", str(cm.exception))
        pids = json.loads((self.pasta / "pids_falso.json").read_text(encoding="utf-8"))
        self.assertTrue(esperar_ate(lambda: not base.processo_vivo(pids["filho"]), 10))

    def test_batimento_chama_progresso_sem_linha_nova(self):
        chamadas = []

        class Parar(Exception):
            pass

        def progresso(p, m):
            chamadas.append(time.time())
            if len(chamadas) >= 4:
                raise Parar()

        with mock.patch.object(motores, "INTERVALO_BATIMENTO_S", 0.2), self.assertRaises(Parar):
            self._gerar("silencioso", progresso=progresso)

    def test_usa_gpu_lock_do_agente_g(self):
        self.amb.spec["usa_gpu"] = True
        falso = mock.MagicMock()
        with mock.patch.object(motores, "_travas", return_value=falso):
            self._gerar(medir_vram=False)
        falso.adquirir_gpu.assert_called_once()
        self.assertIn("falso", falso.adquirir_gpu.call_args.kwargs.get("dono", ""))

    def test_gpu_lock_real_fica_em_locks_do_teste(self):
        self.amb.spec["usa_gpu"] = True
        self._gerar(medir_vram=False)
        self.assertTrue((self.amb.locks / "gpu.lock").exists())


class TestBase(unittest.TestCase):
    def test_glb_valido(self):
        with tempfile.TemporaryDirectory(dir=RAIZ_TESTES) as d:
            g = glb_minimo(Path(d) / "a.glb")
            self.assertTrue(base.glb_valido(g))
            ruim = Path(d) / "b.glb"
            ruim.write_bytes(b"v 0 0 0\n")
            self.assertFalse(base.glb_valido(ruim))
            self.assertFalse(base.glb_valido(Path(d) / "nao.glb"))

    def test_processo_vivo(self):
        self.assertTrue(base.processo_vivo(os.getpid(), base.hora_criacao(os.getpid())))
        self.assertFalse(base.processo_vivo(pid_morto()))
        self.assertFalse(base.processo_vivo(0))
        if base.WINDOWS:
            self.assertFalse(base.processo_vivo(os.getpid(), base.hora_criacao(os.getpid()) + 1),
                             "PID reciclado (horário de criação diferente) não conta como vivo")

    @unittest.skipUnless(base.WINDOWS, "Job Object só no Windows")
    def test_job_object_mata_ao_fechar(self):
        p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
        jo = base.JobObject()
        self.assertTrue(jo.adicionar(p))
        jo.fechar()
        p.wait(timeout=10)
        self.assertIsNotNone(p.returncode)

    @unittest.skipUnless(base.WINDOWS, "Job Object só no Windows")
    def test_worker_morre_e_motor_morre_junto(self):
        # Um "worker" entra no Job Object, abre um "motor" e morre de repente (os._exit).
        codigo = (
            "import os, subprocess, sys, time\n"
            f"sys.path.insert(0, {str(APP)!r})\n"
            "from oficina3d.motores import base\n"
            "assert base.entrar_em_job_object()\n"
            "m = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\n"
            "print(m.pid, flush=True)\n"
            "time.sleep(0.5)\n"
            "os._exit(9)\n"
        )
        r = subprocess.run([sys.executable, "-c", codigo], capture_output=True, text=True, timeout=60, cwd=str(APP))
        self.assertEqual(r.returncode, 9, r.stderr)
        pid_motor = int(r.stdout.strip().splitlines()[-1])
        self.assertTrue(esperar_ate(lambda: not base.processo_vivo(pid_motor), 10), "motor sobreviveu ao worker")


if __name__ == "__main__":
    unittest.main()
