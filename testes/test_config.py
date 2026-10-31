"""Testes de oficina3d.config (caminhos, regra do Drive, env_subprocesso sem efeito colateral)."""
import atexit
import os
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

# --- pasta temporária dos testes: SEMPRE dentro de BASE\jobs_teste (antes de importar o config) ---
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

from oficina3d import config  # noqa: E402

if os.path.normcase(str(config.JOBS)) != os.path.normcase(str(TEMP_TESTES)):
    raise RuntimeError(f"config.JOBS ({config.JOBS}) não é a pasta temporária dos testes; recuso rodar")

DRIVE_DESKTOP = r"C:\Users\usuario\Desktop\RPG Assimilação\RPG Assimilação\Oficina3D_v2"


class TestMontar(unittest.TestCase):
    def test_padrao(self):
        c = config.montar({})
        self.assertEqual(c.base, Path(r"C:\Users\txcga\RPG_Local\Oficina3D"))
        self.assertEqual(c.jobs, c.base / "jobs")
        self.assertEqual(c.jobs_teste, c.base / "jobs_teste")
        self.assertEqual(c.locks, c.base / "locks")
        self.assertEqual(c.app, c.base / "app")
        self.assertEqual(c.motores, c.base / "motores")
        for p, nome in ((c.hy3dgen, "hy3dgen"), (c.hf_home, "huggingface"), (c.u2net, "u2net"),
                        (c.tmp, "tmp"), (c.uv_cache, "uv")):
            self.assertEqual(p, c.base / "_cache" / nome)
        self.assertEqual({k: p.name for k, p in c.venvs.items()},
                         {"app": ".venv_app", "hunyuan": ".venv_app", "triposr": ".venv_triposr",
                          "mcp": ".venv_mcp"})
        self.assertEqual(c.ferramentas, Path(r"C:\Users\txcga\RPG_Local\ferramentas"))
        self.assertEqual(c.blender.name.lower(), "blender.exe")
        self.assertIn("console", c.godot.name.lower())

    def test_base_e_jobs_por_variavel(self):
        c = config.montar({"OFICINA3D_BASE": r"D:\Teste\Oficina3D"})
        self.assertEqual(c.base, Path(r"D:\Teste\Oficina3D"))
        self.assertEqual(c.jobs, Path(r"D:\Teste\Oficina3D\jobs"))
        self.assertEqual(c.hf_home, Path(r"D:\Teste\Oficina3D\_cache\huggingface"))
        self.assertEqual(c.venvs["hunyuan"], Path(r"D:\Teste\Oficina3D\.venv_app"))
        self.assertEqual(c.ferramentas, Path(r"D:\Teste\ferramentas"))
        c = config.montar({"OFICINA3D_BASE": r"D:\Teste\Oficina3D", "OFICINA3D_JOBS": '"D:\\Fila\\jobs"'})
        self.assertEqual(c.jobs, Path(r"D:\Fila\jobs"))

    def test_executaveis_por_variavel(self):
        c = config.montar({"OFICINA3D_BLENDER": r"D:\B\blender.exe", "OFICINA3D_GODOT": r"D:\G\godot.exe",
                           "OFICINA3D_UV": r"D:\U\uv.exe"})
        self.assertEqual(c.blender, Path(r"D:\B\blender.exe"))
        self.assertEqual(c.godot, Path(r"D:\G\godot.exe"))
        self.assertEqual(c.uv, Path(r"D:\U\uv.exe"))

    def test_caminho_relativo_recusado(self):
        for var in ("OFICINA3D_BASE", "OFICINA3D_JOBS", "OFICINA3D_BLENDER"):
            with self.assertRaises(config.ErroConfiguracao):
                config.montar({var: r"pasta\relativa"})
        with self.assertRaises(config.ErroConfiguracao):
            config.montar({"OFICINA3D_BASE": r"\sem\unidade"})

    def test_drive_g_proibido(self):
        for env in ({"OFICINA3D_BASE": r"G:\Meu Drive\Oficina3D"},
                    {"OFICINA3D_JOBS": r"G:\Meu Drive\jobs"},
                    {"OFICINA3D_JOBS": r"g:\jobs"}):
            with self.subTest(env=env), self.assertRaises(config.ErroConfiguracao) as cm:
                config.montar(env)
            self.assertIn("Google Drive", str(cm.exception))

    def test_pasta_espelhada_do_drive_proibida(self):
        variantes = (DRIVE_DESKTOP, DRIVE_DESKTOP.lower(), DRIVE_DESKTOP.upper(),
                     unicodedata.normalize("NFD", DRIVE_DESKTOP))
        for caminho in variantes:
            for var in ("OFICINA3D_BASE", "OFICINA3D_JOBS"):
                with self.subTest(var=var, caminho=caminho), self.assertRaises(config.ErroConfiguracao):
                    config.montar({var: caminho})

    def test_caminhos_parecidos_permitidos(self):
        for caminho in (r"C:\Users\usuario\Desktop\Outra Pasta\Oficina3D", r"D:\RPG Assimilação\Oficina3D",
                        r"C:\Users\usuario\RPG_Local\Oficina3D"):
            with self.subTest(caminho=caminho):
                self.assertEqual(config.montar({"OFICINA3D_BASE": caminho}).base, Path(caminho))

    def test_importacao_falha_com_jobs_no_drive(self):
        for var, valor in (("OFICINA3D_JOBS", r"G:\Meu Drive\jobs"), ("OFICINA3D_BASE", DRIVE_DESKTOP)):
            with self.subTest(var=var):
                env = dict(os.environ)
                env[var] = valor
                env["PYTHONIOENCODING"] = "utf-8"
                r = subprocess.run([sys.executable, "-c", "import oficina3d.config"], cwd=str(APP), env=env,
                                   capture_output=True, text=True, encoding="utf-8", timeout=60)
                self.assertNotEqual(r.returncode, 0)
                self.assertIn("ErroConfiguracao", r.stderr)

    def test_sem_disco_e_fixo(self):
        for nome in ("config.py", "job.py"):
            texto = (APP / "oficina3d" / nome).read_text(encoding="utf-8")
            self.assertNotIn("E:\\", texto, nome)
            self.assertNotIn("E:/", texto, nome)


class TestVocabulario(unittest.TestCase):
    def test_motores_e_padroes(self):
        self.assertEqual(set(config.MOTORES), {"hunyuan-mini", "hunyuan-mini-turbo", "hunyuan-mv",
                                               "hunyuan-mv-turbo", "triposr"})
        self.assertEqual(config.MOTOR_PADRAO_MULTIVISTA, "hunyuan-mv-turbo")
        self.assertEqual(config.MOTOR_PADRAO_UMA_VISTA, "hunyuan-mini-turbo")
        self.assertIsNone(config.OPCOES_PADRAO["motor"])
        self.assertEqual(config.PY_APP, config.BASE / ".venv_app" / "Scripts" / "python.exe")
        self.assertEqual(config.PY_HUNYUAN, config.BASE / ".venv_app" / "Scripts" / "python.exe")


class TestEnvSubprocesso(unittest.TestCase):
    def test_sem_efeito_colateral(self):
        antes = dict(os.environ)
        env = config.env_subprocesso(criar_pastas=False)
        self.assertEqual(dict(os.environ), antes)
        self.assertIsNot(env, os.environ)
        self.assertIsInstance(env, dict)
        env["OFICINA3D_TESTE_X"] = "1"
        self.assertNotIn("OFICINA3D_TESTE_X", os.environ)

    def test_variaveis(self):
        env = config.env_subprocesso(criar_pastas=False)
        self.assertEqual(env["PYTORCH_CUDA_ALLOC_CONF"], "expandable_segments:True")
        self.assertEqual(env["HF_HUB_OFFLINE"], "1")
        self.assertEqual(env["HF_HOME"], str(config.CACHE / "huggingface"))
        self.assertEqual(env["HY3DGEN_MODELS"], str(config.CACHE / "hy3dgen"))
        self.assertEqual(env["U2NET_HOME"], str(config.CACHE / "u2net"))
        self.assertEqual(env["UV_CACHE_DIR"], str(config.CACHE / "uv"))
        self.assertEqual(env["TEMP"], str(config.TMP))
        self.assertEqual(env["TMP"], str(config.TMP))
        self.assertTrue(_dentro(Path(env["APPDATA"]), config.CACHE))
        self.assertTrue(_dentro(Path(env["LOCALAPPDATA"]), config.CACHE))
        self.assertNotIn("PYTHONHOME", env)

    def test_opcoes(self):
        env = config.env_subprocesso(offline=False, criar_pastas=False)
        self.assertNotIn("HF_HUB_OFFLINE", env)
        env = config.env_subprocesso(isolar_appdata=False, criar_pastas=False)
        self.assertEqual(env.get("APPDATA"), os.environ.get("APPDATA"))
        env = config.env_subprocesso({"HF_HUB_OFFLINE": "0", "MINHA_VAR": 5}, criar_pastas=False)
        self.assertEqual(env["HF_HUB_OFFLINE"], "0")
        self.assertEqual(env["MINHA_VAR"], "5")

    def test_extra_no_drive_recusado(self):
        for k, v in (("HF_HOME", r"G:\Meu Drive\hf"), ("HY3DGEN_MODELS", DRIVE_DESKTOP + r"\hy3dgen"),
                     ("TEMP", r"G:\tmp")):
            with self.subTest(k=k), self.assertRaises(config.ErroConfiguracao):
                config.env_subprocesso({k: v}, criar_pastas=False)

    def test_verificar_fora_do_drive(self):
        self.assertEqual(config.verificar_fora_do_drive(r"C:\x\y", "teste"), Path(r"C:\x\y"))
        with self.assertRaises(config.ErroConfiguracao):
            config.verificar_fora_do_drive(r"G:\x", "teste")


if __name__ == "__main__":
    unittest.main()
