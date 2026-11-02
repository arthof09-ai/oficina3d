"""Runner CPU sem Blender/GPU: logs, contagens e recursos medidos, sem estimar.

Uso: python -B testes/auditoria_nuvem.py ROTULO [modulo.unittest ...]
Sem modulos: unittest discover de testes/test_*.py. Evidencias publicas so textuais.
"""
import contextlib
import ctypes
from ctypes import wintypes
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def pico_memoria_bytes():
    if sys.platform != "win32":
        return None

    class Counters(ctypes.Structure):
        _fields_ = [("cb", wintypes.DWORD), ("PageFaultCount", wintypes.DWORD),
                    *[(n, ctypes.c_size_t) for n in (
                        "PeakWorkingSetSize", "WorkingSetSize", "QuotaPeakPagedPoolUsage",
                        "QuotaPagedPoolUsage", "QuotaPeakNonPagedPoolUsage", "QuotaNonPagedPoolUsage",
                        "PagefileUsage", "PeakPagefileUsage")]]

    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.GetCurrentProcess.restype = wintypes.HANDLE
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
    c = Counters()
    c.cb = ctypes.sizeof(c)
    if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(c), c.cb):
        return None
    return c.PeakWorkingSetSize


def main():
    label = sys.argv[1]
    if not label.replace("-", "").replace("_", "").isalnum():
        raise ValueError("rotulo invalido")
    branch = subprocess.check_output(["git", "branch", "--show-current"], cwd=ROOT, text=True).strip()
    if branch != "codex/auditoria-sem-pc":
        raise RuntimeError(f"branch fora da missao: {branch}")
    out = ROOT / "docs" / "evidencias-nuvem"
    out.mkdir(exist_ok=True)
    wall, cpu = time.perf_counter(), time.process_time()
    with tempfile.TemporaryDirectory(prefix="oficina-nuvem-") as tmp:
        jobs_teste = Path(tmp) / "jobs_teste"
        jobs_teste.mkdir()
        jobs = jobs_teste / "unittest_nuvem"
        jobs.mkdir()
        for key, value in {"OFICINA3D_BASE": tmp, "OFICINA3D_JOBS": str(jobs),
                           "OFICINA3D_JOBS_TESTE": str(jobs_teste),
                           "OFICINA3D_AUDITORIA_SEM_PC": "1",
                           "HF_HOME": str(Path(tmp) / "hf"), "TORCH_HOME": str(Path(tmp) / "torch")}.items():
            os.environ[key] = value
        with (out / f"{label}.txt").open("w", encoding="utf-8") as log:
            with contextlib.redirect_stdout(log), contextlib.redirect_stderr(log):
                loader = unittest.TestLoader()
                # A missao proibe Blender mesmo se houver uma instalacao local.
                # Faz os testes de integracao declararem skip antes de descobrir a suite.
                from oficina3d.refino import previa
                previa.achar_blender = lambda: None
                suite = (loader.loadTestsFromNames(sys.argv[2:]) if len(sys.argv) > 2
                         else loader.discover(str(ROOT / "testes")))
                # Tres modulos legados fixam APP.parent/jobs_teste, ignorando env.
                # Redireciona apenas sua raiz de temporarios, sem mudar assercoes.
                for module in tuple(sys.modules.values()):
                    file = getattr(module, "__file__", None)
                    if file and Path(file).resolve().parent == ROOT / "testes":
                        if hasattr(module, "JOBS_TESTE"):
                            module.JOBS_TESTE = jobs_teste
                result = unittest.TextTestRunner(stream=log, verbosity=2).run(suite)
    versions = {}
    for name in ("numpy", "Pillow", "trimesh", "fastapi", "httpx", "mcp", "scipy", "xatlas", "psutil"):
        try:
            versions[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            versions[name] = "ausente"
    data = {"rotulo": label, "branch": branch,
            "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "comando": ["python", "-B", "testes/auditoria_nuvem.py", *sys.argv[1:]],
            "python": platform.python_version(), "plataforma": platform.platform(), "versoes": versions,
            "testes_executados": result.testsRun,
            "passaram": result.testsRun - len(result.skipped) - len(result.failures) - len(result.errors),
            "falhas": len(result.failures), "erros": len(result.errors),
            "skips": [{"teste": str(t), "motivo": reason} for t, reason in result.skipped],
            "falhas_ids": [str(t) for t, _ in result.failures], "erros_ids": [str(t) for t, _ in result.errors],
            "parede_s": round(time.perf_counter() - wall, 6),
            "cpu_processo_s": round(time.process_time() - cpu, 6),
            "pico_working_set_processo_bytes": pico_memoria_bytes(),
            "gpu": "nao usada", "vram": "nao medido", "blender": "nao executado",
            "jobs_reais_e_qualidade_visual": "nao medido",
            "nota_recursos": "CPU e memoria do processo runner; nao incluem processos filhos; pico desde inicio do processo"}
    (out / f"{label}.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
