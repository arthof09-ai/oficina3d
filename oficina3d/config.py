"""Caminhos e ambiente da Oficina 3D v2 neste PC.

Tudo sai de duas variáveis (nada de disco fixo no código):
  OFICINA3D_BASE  pasta raiz (padrão C:\\Users\\txcga\\RPG_Local\\Oficina3D)
  OFICINA3D_JOBS  fila de jobs (padrão BASE\\jobs; os testes usam uma pasta dentro de BASE\\jobs_teste)
Ferramentas externas, sobrescrevíveis: OFICINA3D_FERRAMENTAS, OFICINA3D_BLENDER, OFICINA3D_GODOT, OFICINA3D_UV.

Regra do plano (5.1): pesos, caches, venvs e jobs NUNCA no Google Drive (unidade G: ou a pasta
espelhada "Desktop\\RPG Assimilação"). Se alguma variável apontar para lá, importar este módulo
levanta ErroConfiguracao com a explicação.

Importar este módulo não cria pastas nem altera os.environ. Quem precisa das pastas chama
garantir_pastas(); quem chama subprocessos usa env_subprocesso() (devolve uma cópia).
"""
import os
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PureWindowsPath
from typing import Mapping

BASE_PADRAO = Path(r"C:\Users\txcga\RPG_Local\Oficina3D")

# Pastas da v2 (plano 6.1).
NOMES_VENVS = {"app": ".venv_app", "hunyuan": ".venv_hunyuan", "triposr": ".venv_triposr", "mcp": ".venv_mcp"}
PYTHON_VENVS = "3.10"  # todas criadas pelo uv com Python 3.10


class ErroConfiguracao(ValueError):
    """Configuração inválida (caminho no Drive, caminho relativo...)."""


# ---------------------------------------------------------------------------
# Proteção contra o Google Drive
# ---------------------------------------------------------------------------
def _normalizar(texto: str) -> str:
    return unicodedata.normalize("NFC", texto).casefold()


def _no_drive(caminho: str) -> bool:
    """True se o caminho está na unidade G: ou dentro de ...\\Desktop\\RPG Assimilação\\."""
    for forma in {os.path.abspath(caminho), os.path.realpath(caminho)}:
        p = PureWindowsPath(forma)
        if _normalizar(p.drive) == "g:":
            return True
        partes = [_normalizar(x) for x in p.parts]
        for i in range(len(partes) - 1):
            if partes[i] == "desktop" and partes[i + 1] == _normalizar("RPG Assimilação"):
                return True
    return False


def verificar_fora_do_drive(caminho, rotulo: str) -> Path:
    """Levanta ErroConfiguracao se `caminho` está no Google Drive. Devolve o Path."""
    if _no_drive(str(caminho)):
        raise ErroConfiguracao(
            f"{rotulo} não pode ficar no Google Drive: {caminho}. O Drive em streaming deixa a leitura "
            f"lenta, quebra imports e corrompe arquivos. Use uma pasta local (por exemplo {BASE_PADRAO}); "
            f"regra do plano 5.1: nunca HF_HOME, HY3DGEN_MODELS, venvs ou jobs no G: nem em "
            f"'Desktop\\RPG Assimilação'."
        )
    return Path(caminho)


# ---------------------------------------------------------------------------
# Montagem dos caminhos (função pura: só lê o `environ` recebido e procura executáveis)
# ---------------------------------------------------------------------------
def _var(environ: Mapping[str, str], nome: str) -> str | None:
    v = environ.get(nome)
    if v is None:
        return None
    v = v.strip().strip('"').strip()
    return v or None


def _absoluto(valor: str, nome: str) -> Path:
    p = PureWindowsPath(valor)
    if not (p.drive and p.root):  # exige "C:\..." (ou \\servidor\pasta\...)
        raise ErroConfiguracao(f"{nome} precisa ser um caminho absoluto (com a unidade), recebi: {valor!r}")
    return Path(os.path.normpath(valor))


def _chave_versao(p: Path):
    """Ordena 'Blender 5.10' depois de 'Blender 5.2' (números comparados como números)."""
    return [int(x) if x.isdigit() else x.casefold() for x in re.split(r"(\d+)", str(p))]


def _procurar(raiz: Path, padroes: tuple[str, ...]) -> Path | None:
    achados = []
    if raiz.is_dir():
        for padrao in padroes:
            achados.extend(x for x in raiz.glob(padrao) if x.is_file())
    return max(achados, key=_chave_versao) if achados else None


def _executavel(environ, var: str, candidatos: list, padrao: Path) -> Path:
    """Variável de ambiente > primeiro candidato encontrado > padrão (mesmo que não exista ainda)."""
    v = _var(environ, var)
    if v:
        return _absoluto(v, var)
    for c in candidatos:
        if c is not None:
            return c
    return padrao


@dataclass(frozen=True)
class Caminhos:
    base: Path
    app: Path
    motores: Path
    cache: Path
    tmp: Path
    hf_home: Path
    hy3dgen: Path
    u2net: Path
    uv_cache: Path
    uv_python: Path
    torch_home: Path
    pip_cache: Path
    godot_appdata: Path
    godot_localappdata: Path
    jobs: Path
    jobs_teste: Path
    locks: Path
    venvs: dict
    ferramentas: Path
    blender: Path
    godot: Path
    uv: Path


def montar(environ: Mapping[str, str] | None = None) -> Caminhos:
    """Calcula todos os caminhos a partir de `environ` (padrão: os.environ) e valida a regra do Drive.

    Não cria pastas e não altera nada.
    """
    environ = os.environ if environ is None else environ
    v = _var(environ, "OFICINA3D_BASE")
    base = _absoluto(v, "OFICINA3D_BASE") if v else BASE_PADRAO
    v = _var(environ, "OFICINA3D_JOBS")
    jobs = _absoluto(v, "OFICINA3D_JOBS") if v else base / "jobs"
    cache = base / "_cache"

    v = _var(environ, "OFICINA3D_FERRAMENTAS")
    ferramentas = _absoluto(v, "OFICINA3D_FERRAMENTAS") if v else base.parent / "ferramentas"
    programas = Path(_var(environ, "ProgramFiles") or r"C:\Program Files")

    blender_pf = programas / "Blender Foundation" / "Blender 5.2" / "blender.exe"
    blender = _executavel(environ, "OFICINA3D_BLENDER", [
        _procurar(ferramentas, ("blender.exe", "*/blender.exe", "*/*/blender.exe")),
        _procurar(programas / "Blender Foundation", ("Blender */blender.exe",)),
    ], blender_pf)
    godot = _executavel(environ, "OFICINA3D_GODOT", [
        _procurar(ferramentas, ("Godot*/Godot_v*_console.exe", "*/Godot*/Godot_v*_console.exe")),
    ], ferramentas / "Godot_4.7.2" / "Godot_v4.7.2-stable_win64_console.exe")
    uv = _executavel(environ, "OFICINA3D_UV", [
        _procurar(ferramentas, ("uv/uv.exe", "*/uv/uv.exe")),
    ], ferramentas / "oficina3d" / "uv" / "uv.exe")

    c = Caminhos(
        base=base, app=base / "app", motores=base / "motores", cache=cache,
        tmp=cache / "tmp", hf_home=cache / "huggingface", hy3dgen=cache / "hy3dgen", u2net=cache / "u2net",
        uv_cache=cache / "uv", uv_python=cache / "uv" / "python", torch_home=cache / "torch",
        pip_cache=cache / "pip", godot_appdata=cache / "godot" / "appdata",
        godot_localappdata=cache / "godot" / "localappdata",
        jobs=jobs, jobs_teste=base / "jobs_teste", locks=base / "locks",
        venvs={k: base / n for k, n in NOMES_VENVS.items()},
        ferramentas=ferramentas, blender=blender, godot=godot, uv=uv,
    )
    for rotulo, p in (("OFICINA3D_BASE", c.base), ("OFICINA3D_JOBS", c.jobs), ("_cache", c.cache),
                      ("HF_HOME", c.hf_home), ("HY3DGEN_MODELS", c.hy3dgen), ("U2NET_HOME", c.u2net),
                      ("TEMP", c.tmp), ("UV_CACHE_DIR", c.uv_cache), ("locks", c.locks),
                      ("jobs_teste", c.jobs_teste), ("motores", c.motores),
                      *((f"venv {n}", p) for n, p in c.venvs.items())):
        verificar_fora_do_drive(p, rotulo)
    return c


# ---------------------------------------------------------------------------
# Valores do processo atual (calculados uma vez, na importação)
# ---------------------------------------------------------------------------
_C = montar()

BASE = _C.base
APP = _C.app
JOBS = _C.jobs
JOBS_TESTE = _C.jobs_teste
LOCKS = _C.locks
TRAVA_GPU = LOCKS / "gpu.lock"
TRAVA_WORKER = LOCKS / "worker.lock"
CACHE = _C.cache
TMP = _C.tmp

VENVS = dict(_C.venvs)
PY_APP = VENVS["app"] / "Scripts" / "python.exe"
PY_HUNYUAN = VENVS["hunyuan"] / "Scripts" / "python.exe"
PY_TRIPOSR = VENVS["triposr"] / "Scripts" / "python.exe"
PY_MCP = VENVS["mcp"] / "Scripts" / "python.exe"

FERRAMENTAS = _C.ferramentas
BLENDER = _C.blender
GODOT = _C.godot
UV = _C.uv

MOTORES_DIR = _C.motores
MOTOR_HUNYUAN = MOTORES_DIR / "Hunyuan3D-2GP"
MOTOR_TRIPOSR = MOTORES_DIR / "TripoSR"

# ---------------------------------------------------------------------------
# Vocabulário do contrato
# ---------------------------------------------------------------------------
VISTAS = (
    "frente", "costas", "esquerda", "direita",
    "frente-esquerda", "frente-direita", "costas-esquerda", "costas-direita",
    "cima", "detalhe", "referencia-de-cor",
)
# Vistas usadas para gerar forma (as outras servem de conferência/cor).
VISTAS_MV_HUNYUAN = {"frente": "front", "costas": "back", "esquerda": "left", "direita": "right"}

MODOS = ("livre", "corpo-base", "multivista", "so-refinar")

# Motores aceitos em opcoes.motor (plano 6.3; o hunyuan-full ficou de fora na v2).
MOTORES = ("hunyuan-mini", "hunyuan-mini-turbo", "hunyuan-mv", "hunyuan-mv-turbo", "triposr")
MOTORES_MULTIVISTA = ("hunyuan-mv", "hunyuan-mv-turbo")
MOTOR_PADRAO_UMA_VISTA = "hunyuan-mini-turbo"
MOTOR_PADRAO_MULTIVISTA = "hunyuan-mv-turbo"   # padrão da v2 com 2+ vistas

REMOVER_FUNDO = ("auto", "sim", "nao")

OPCOES_PADRAO = {
    "motor": None,           # None = automático: hunyuan-mv-turbo com 2+ vistas, hunyuan-mini-turbo com 1
    "passos": None,          # None = padrão do motor
    "octree": 256,
    "seed": 1234,
    "sementes": 1,           # quantas sementes tentar na etapa forma (plano 6.2)
    "flashvdm": True,
    "alvo_triangulos": 50000,
    "altura_m": None,        # None = mantém escala normalizada (altura 1,0)
    "simetrizar": False,
    "dividir_pranchas": True,
    "remover_fundo": "auto",
}

# ---------------------------------------------------------------------------
# Ambiente
# ---------------------------------------------------------------------------
# Chaves que apontam para pastas pesadas: conferidas contra a regra do Drive em env_subprocesso.
_CHAVES_PASTA = ("HF_HOME", "HY3DGEN_MODELS", "U2NET_HOME", "TORCH_HOME", "UV_CACHE_DIR",
                 "UV_PYTHON_INSTALL_DIR", "PIP_CACHE_DIR", "TEMP", "TMP")


def _env_proprio(offline: bool = True, isolar_appdata: bool = True) -> dict:
    env = {
        "TEMP": str(TMP), "TMP": str(TMP),
        "PIP_CACHE_DIR": str(_C.pip_cache),
        "HF_HOME": str(_C.hf_home),
        "TORCH_HOME": str(_C.torch_home),
        "HY3DGEN_MODELS": str(_C.hy3dgen),
        "U2NET_HOME": str(_C.u2net),
        "UV_CACHE_DIR": str(_C.uv_cache),
        "UV_PYTHON_INSTALL_DIR": str(_C.uv_python),
        "PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True",
        "HF_HUB_DISABLE_SYMLINKS_WARNING": "1",
        "PYTHONIOENCODING": "utf-8",
        "PYTHONUTF8": "1",
    }
    if offline:
        env["HF_HUB_OFFLINE"] = "1"
    if isolar_appdata:
        # O Godot grava configuração e cache em %APPDATA%/%LOCALAPPDATA%: ficam em _cache\godot.
        env["APPDATA"] = str(_C.godot_appdata)
        env["LOCALAPPDATA"] = str(_C.godot_localappdata)
    return env


def env_subprocesso(extra: dict | None = None, *, offline: bool = True, isolar_appdata: bool = True,
                    criar_pastas: bool = True) -> dict:
    """Ambiente para subprocessos (motores, Blender, Godot, uv): caches e temporários em BASE\\_cache.

    Devolve uma CÓPIA de os.environ com as variáveis da Oficina; não altera os.environ.
    - offline=True: HF_HUB_OFFLINE=1 (nada baixa sem querer). offline=False tira a variável
      (só o instalador de modelos deve usar).
    - isolar_appdata=True: APPDATA/LOCALAPPDATA próprios em _cache\\godot (pedido do Godot headless).
    - criar_pastas=True: cria TEMP e as pastas de APPDATA (o subprocesso falha sem elas).
    - extra: sobrescreve no fim; se apontar HF_HOME, HY3DGEN_MODELS etc. para o Drive, levanta erro.
    """
    env = dict(os.environ)
    env.pop("PYTHONHOME", None)  # PYTHONHOME herdado quebra os Pythons das venvs
    if not offline:
        env.pop("HF_HUB_OFFLINE", None)
    env.update(_env_proprio(offline=offline, isolar_appdata=isolar_appdata))
    if extra:
        env.update({str(k): str(v) for k, v in extra.items()})
    for k in _CHAVES_PASTA:
        if env.get(k):
            verificar_fora_do_drive(env[k], k)
    if criar_pastas:
        TMP.mkdir(parents=True, exist_ok=True)
        if isolar_appdata:
            Path(env["APPDATA"]).mkdir(parents=True, exist_ok=True)
            Path(env["LOCALAPPDATA"]).mkdir(parents=True, exist_ok=True)
    return env


def aplicar_env_local() -> None:
    """Aplica no processo ATUAL as variáveis de cache (para quem carrega modelos dentro do próprio processo).

    Este, sim, tem efeito colateral de propósito: altera os.environ. Não mexe em APPDATA/LOCALAPPDATA
    nem desliga a internet do HF se o processo já definiu HF_HUB_OFFLINE.
    """
    proprio = _env_proprio(offline=True, isolar_appdata=False)
    if "HF_HUB_OFFLINE" in os.environ:
        proprio.pop("HF_HUB_OFFLINE")
    for k in _CHAVES_PASTA:
        if proprio.get(k):
            verificar_fora_do_drive(proprio[k], k)
    TMP.mkdir(parents=True, exist_ok=True)
    os.environ.update(proprio)


def garantir_pastas() -> list[Path]:
    """Cria (se faltarem) as pastas de trabalho da Oficina. Devolve a lista conferida."""
    pastas = [CACHE, TMP, _C.hf_home, _C.hy3dgen, _C.u2net, _C.uv_cache, _C.godot_appdata,
              _C.godot_localappdata, JOBS, JOBS_TESTE, LOCKS, MOTORES_DIR]
    for p in pastas:
        p.mkdir(parents=True, exist_ok=True)
    return pastas
