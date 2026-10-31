"""Peças comuns do núcleo: Job Object do Windows, PID vivo, GLB válido, config com padrões.

Só biblioteca padrão (o MCP e a web importam o pacote `motores` sem torch).

Job Object (Windows): o processo do motor (e tudo o que ele abrir) entra num Job Object com
JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE. Cancelar = TerminateJobObject (mata a árvore inteira);
se o worker morrer de repente, o Windows fecha o handle e mata a árvore junto, e a GPU não
fica presa por um motor órfão (lição da v1: `taskkill /T` à mão).
"""
from __future__ import annotations

import ctypes
import importlib
import os
import subprocess
import sys
from pathlib import Path

WINDOWS = sys.platform == "win32"


# --------------------------------------------------------------------------- config com padrões

def cfg(nome: str, padrao=None):
    """Lê `oficina3d.config.<nome>` na hora (não no import), com padrão se o contrato ainda não tiver."""
    from .. import config
    return getattr(config, nome, padrao)


def base() -> Path:
    b = cfg("BASE")
    return Path(b) if b else Path(os.environ.get("OFICINA3D_BASE", r"C:\Users\txcga\RPG_Local\Oficina3D"))


def env_motor(extra: dict | None = None) -> dict:
    """Ambiente do subprocesso: config.env_subprocesso() + extras (sem mexer no os.environ)."""
    from .. import config
    try:
        # Motor não é o Godot: não precisa do APPDATA/LOCALAPPDATA isolado.
        env = dict(config.env_subprocesso(isolar_appdata=False))
    except TypeError:
        env = dict(config.env_subprocesso())
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env.setdefault("PYTHONUTF8", "1")
    env["PYTHONUNBUFFERED"] = "1"
    if extra:
        env.update({k: str(v) for k, v in extra.items()})
    return env


def importar_opcional(nome_modulo: str):
    """Importa um módulo de outro agente; devolve None só se ELE não existir (erro interno sobe)."""
    try:
        return importlib.import_module(nome_modulo)
    except ModuleNotFoundError as e:
        if e.name and (nome_modulo == e.name or nome_modulo.startswith(e.name + ".")):
            return None
        raise


# --------------------------------------------------------------------------- GLB

def glb_valido(caminho: Path) -> bool:
    """Confere o cabeçalho binário do glTF 2.0 ('glTF', versão 2, tamanho coerente)."""
    try:
        with open(caminho, "rb") as f:
            cab = f.read(12)
        if len(cab) < 12 or cab[:4] != b"glTF":
            return False
        versao = int.from_bytes(cab[4:8], "little")
        tamanho = int.from_bytes(cab[8:12], "little")
        return versao == 2 and tamanho <= Path(caminho).stat().st_size
    except OSError:
        return False


# --------------------------------------------------------------------------- Windows (ctypes)

if WINDOWS:
    from ctypes import wintypes

    _k32 = ctypes.WinDLL("kernel32", use_last_error=True)

    class _IO_COUNTERS(ctypes.Structure):
        _fields_ = [(n, ctypes.c_ulonglong) for n in (
            "ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
            "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

    class _BASIC_LIMIT(ctypes.Structure):
        _fields_ = [
            ("PerProcessUserTimeLimit", ctypes.c_int64), ("PerJobUserTimeLimit", ctypes.c_int64),
            ("LimitFlags", wintypes.DWORD), ("MinimumWorkingSetSize", ctypes.c_size_t),
            ("MaximumWorkingSetSize", ctypes.c_size_t), ("ActiveProcessLimit", wintypes.DWORD),
            ("Affinity", ctypes.c_size_t), ("PriorityClass", wintypes.DWORD),
            ("SchedulingClass", wintypes.DWORD),
        ]

    class _EXTENDED_LIMIT(ctypes.Structure):
        _fields_ = [
            ("BasicLimitInformation", _BASIC_LIMIT), ("IoInfo", _IO_COUNTERS),
            ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
            ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t),
        ]

    _k32.CreateJobObjectW.restype = wintypes.HANDLE
    _k32.CreateJobObjectW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR]
    _k32.SetInformationJobObject.restype = wintypes.BOOL
    _k32.SetInformationJobObject.argtypes = [wintypes.HANDLE, ctypes.c_int, ctypes.c_void_p, wintypes.DWORD]
    _k32.AssignProcessToJobObject.restype = wintypes.BOOL
    _k32.AssignProcessToJobObject.argtypes = [wintypes.HANDLE, wintypes.HANDLE]
    _k32.TerminateJobObject.restype = wintypes.BOOL
    _k32.TerminateJobObject.argtypes = [wintypes.HANDLE, wintypes.UINT]
    _k32.CloseHandle.restype = wintypes.BOOL
    _k32.CloseHandle.argtypes = [wintypes.HANDLE]
    _k32.OpenProcess.restype = wintypes.HANDLE
    _k32.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    _k32.GetExitCodeProcess.restype = wintypes.BOOL
    _k32.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    _k32.GetProcessTimes.restype = wintypes.BOOL
    _k32.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    _k32.GetCurrentProcess.restype = wintypes.HANDLE

    _JobObjectExtendedLimitInformation = 9
    _KILL_ON_JOB_CLOSE = 0x2000
    _PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    _STILL_ACTIVE = 259
    _ERROR_ACCESS_DENIED = 5


class JobObject:
    """Job Object com KILL_ON_JOB_CLOSE. Fora do Windows vira no-op (encerrar usa kill)."""

    def __init__(self):
        self.handle = None
        if not WINDOWS:
            return
        h = _k32.CreateJobObjectW(None, None)
        if not h:
            raise OSError(ctypes.get_last_error(), "CreateJobObjectW falhou")
        info = _EXTENDED_LIMIT()
        info.BasicLimitInformation.LimitFlags = _KILL_ON_JOB_CLOSE
        if not _k32.SetInformationJobObject(h, _JobObjectExtendedLimitInformation,
                                            ctypes.byref(info), ctypes.sizeof(info)):
            err = ctypes.get_last_error()
            _k32.CloseHandle(h)
            raise OSError(err, "SetInformationJobObject falhou")
        self.handle = h

    def adicionar(self, proc: subprocess.Popen | None = None) -> bool:
        """Coloca o processo (ou o processo atual, se None) no Job Object. Devolve True se deu certo."""
        if not WINDOWS or not self.handle:
            return False
        hproc = _k32.GetCurrentProcess() if proc is None else int(proc._handle)  # noqa: SLF001
        return bool(_k32.AssignProcessToJobObject(self.handle, hproc))

    def encerrar(self, codigo: int = 1) -> None:
        """Mata todos os processos do Job Object (a árvore inteira do motor)."""
        if WINDOWS and self.handle:
            _k32.TerminateJobObject(self.handle, codigo)

    def fechar(self) -> None:
        """Fecha o handle (com KILL_ON_JOB_CLOSE, o que sobrou dentro morre)."""
        if WINDOWS and self.handle:
            _k32.CloseHandle(self.handle)
            self.handle = None

    def __del__(self):
        try:
            self.fechar()
        except Exception:
            pass


_JOB_DO_PROCESSO: JobObject | None = None


def entrar_em_job_object() -> bool:
    """Põe o processo ATUAL (o worker) num Job Object KILL_ON_JOB_CLOSE, uma vez só.

    Os filhos herdam: se o worker morrer, motor e Blender morrem junto. O handle fica vivo
    até o fim do processo (variável global). Job Objects aninhados exigem Windows 8+.
    """
    global _JOB_DO_PROCESSO
    if not WINDOWS:
        return False
    if _JOB_DO_PROCESSO is not None:
        return True
    try:
        jo = JobObject()
        if jo.adicionar(None):
            _JOB_DO_PROCESSO = jo
            return True
        jo.fechar()
    except OSError:
        pass
    return False


def encerrar_arvore(proc: subprocess.Popen, jo: JobObject | None = None) -> None:
    """Mata o processo e os descendentes: Job Object; se não houver, taskkill /T /F."""
    if proc.poll() is not None and jo is None:
        return
    if jo is not None and jo.handle:
        jo.encerrar(1)
    elif WINDOWS:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    else:
        proc.kill()
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()


# --------------------------------------------------------------------------- PID vivo (sem psutil)

def hora_criacao(pid: int) -> int | None:
    """Horário de criação do processo (FILETIME, inteiro) — junto com o PID evita confundir PID reciclado."""
    if not WINDOWS:
        return None
    h = _k32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
    if not h:
        return None
    try:
        c, e, k, u = (wintypes.FILETIME() for _ in range(4))
        if not _k32.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(e), ctypes.byref(k), ctypes.byref(u)):
            return None
        return (c.dwHighDateTime << 32) | c.dwLowDateTime
    finally:
        _k32.CloseHandle(h)


def processo_vivo(pid: int | None, criado: int | None = None) -> bool:
    """True se o PID existe e ainda roda (e, se `criado` vier, se é o MESMO processo)."""
    if not pid or int(pid) <= 0:
        return False
    if not WINDOWS:
        try:
            os.kill(int(pid), 0)
            return True
        except OSError:
            return False
    h = _k32.OpenProcess(_PROCESS_QUERY_LIMITED_INFORMATION, False, int(pid))
    if not h:
        # Sem permissão = existe (processo de outro usuário/elevado); senão, não existe.
        return ctypes.get_last_error() == _ERROR_ACCESS_DENIED
    try:
        codigo = wintypes.DWORD()
        if not _k32.GetExitCodeProcess(h, ctypes.byref(codigo)) or codigo.value != _STILL_ACTIVE:
            return False
    finally:
        _k32.CloseHandle(h)
    if criado is not None:
        atual = hora_criacao(int(pid))
        return atual is None or int(atual) == int(criado)
    return True
