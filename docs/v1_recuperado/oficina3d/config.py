"""Caminhos e ambiente da Oficina 3D neste PC. Tudo no disco E:."""
import os
from pathlib import Path

BASE = Path(r"E:\RPG_Assimilacao\Oficina3D")
APP = BASE / "app"
JOBS = BASE / "jobs"
CACHE = BASE / "_cache"
TMP = CACHE / "tmp"

PY_APP = BASE / ".venv" / "Scripts" / "python.exe"
PY_TRIPOSR = BASE / ".venv_triposr" / "Scripts" / "python.exe"
BLENDER = BASE / "Ferramentas" / "Blender" / "blender-5.2.3-windows-x64" / "blender.exe"
GODOT = BASE / "Ferramentas" / "Godot" / "Godot_v4.7.2-stable_win64_console.exe"

MOTOR_HUNYUAN = BASE / "motores" / "Hunyuan3D-2GP"
MOTOR_TRIPOSR = BASE / "motores" / "TripoSR"

VISTAS = (
    "frente", "costas", "esquerda", "direita",
    "frente-esquerda", "frente-direita", "costas-esquerda", "costas-direita",
    "cima", "detalhe", "referencia-de-cor",
)
# Vistas usadas para gerar forma (as outras servem de conferência/cor).
VISTAS_MV_HUNYUAN = {"frente": "front", "costas": "back", "esquerda": "left", "direita": "right"}

MODOS = ("livre", "corpo-base", "multivista", "so-refinar")

OPCOES_PADRAO = {
    "motor": "hunyuan-mini-turbo",
    "passos": None,          # None = padrão do motor
    "octree": 256,
    "seed": 1234,
    "flashvdm": True,
    "alvo_triangulos": 50000,
    "altura_m": None,        # None = mantém escala normalizada (altura 1,0)
    "simetrizar": False,
    "dividir_pranchas": True,
    "remover_fundo": "auto",
}


def env_subprocesso(extra: dict | None = None) -> dict:
    """Ambiente para subprocessos: caches e temporários no E:."""
    TMP.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env.update({
        "TEMP": str(TMP), "TMP": str(TMP),
        "PIP_CACHE_DIR": str(CACHE / "pip"),
        "HF_HOME": str(CACHE / "huggingface"),
        "TORCH_HOME": str(CACHE / "torch"),
        "HY3DGEN_MODELS": str(CACHE / "hy3dgen"),
        "U2NET_HOME": str(CACHE / "u2net"),
        "HF_HUB_DISABLE_SYMLINKS_WARNING": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1",
    })
    if extra:
        env.update(extra)
    return env


def aplicar_env_local():
    """Aplica o mesmo ambiente no processo atual (para quem importa modelos direto)."""
    os.environ.update({k: v for k, v in env_subprocesso().items() if k not in os.environ or k in (
        "TEMP", "TMP", "PIP_CACHE_DIR", "HF_HOME", "TORCH_HOME", "HY3DGEN_MODELS", "U2NET_HOME")})
