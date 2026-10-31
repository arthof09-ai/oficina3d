"""Lançador do worker para a Tarefa Agendada (roda com pythonw.exe, sem janela).

O Agendador de Tarefas não sabe carregar variáveis de ambiente, então este
script:
1. carrega o `instalacao\\env.cmd` (roda `cmd /c call env.cmd && set` escondido
   e copia o ambiente resultante);
2. se já há um worker rodando (worker.lock ocupado), sai sem fazer nada;
3. roda `.venv_app\\Scripts\\pythonw.exe -m oficina3d.worker` com cwd = app,
   prioridade abaixo do normal e sem janela;
4. se o worker cair (código != 0), espera e reinicia (30 s, 1, 2, 4... até
   10 min); mais de 5 quedas em 1 hora → desiste e sai com erro.
Log em `<BASE>\\_cache\\logs\\tarefa_worker.log` (local, nunca no Drive).
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
BASE = APP.parent
ENV_CMD = APP / "instalacao" / "env.cmd"
PYTHONW = BASE / ".venv_app" / "Scripts" / "pythonw.exe"
LOG = BASE / "_cache" / "logs" / "tarefa_worker.log"

CREATE_NO_WINDOW = 0x08000000
BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
MAX_QUEDAS_POR_HORA = 5


def registrar(msg: str) -> None:
    try:
        LOG.parent.mkdir(parents=True, exist_ok=True)
        if LOG.exists() and LOG.stat().st_size > 1_000_000:
            os.replace(LOG, LOG.with_suffix(".log.1"))
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat(timespec='seconds')} {msg}\n")
    except OSError:
        pass


def carregar_env_cmd() -> dict:
    """Ambiente depois de `call env.cmd` (sem abrir janela)."""
    env = dict(os.environ)
    if not ENV_CMD.is_file():
        registrar(f"AVISO: {ENV_CMD} não existe; seguindo com o ambiente atual")
        return env
    try:
        # Linha de comando em texto (não lista): o cmd tira as aspas de fora do /c.
        r = subprocess.run(
            f'cmd.exe /d /u /c "call "{ENV_CMD}" >nul 2>&1 && set"',
            capture_output=True, cwd=str(APP), timeout=60, creationflags=CREATE_NO_WINDOW)
    except (OSError, subprocess.TimeoutExpired) as e:
        registrar(f"AVISO: falhou ao carregar env.cmd ({e}); seguindo com o ambiente atual")
        return env
    if r.returncode != 0:
        registrar(f"AVISO: env.cmd saiu com {r.returncode}; seguindo com o ambiente atual")
        return env
    novo = {}
    for linha in r.stdout.decode("utf-16-le", errors="replace").splitlines():
        if "=" in linha and not linha.startswith("="):
            k, v = linha.split("=", 1)
            novo[k] = v
    return novo or env


def worker_ja_rodando() -> bool:
    sys.path.insert(0, str(APP))
    try:
        from oficina3d import travas
        return bool(travas.estado_trava("worker").get("ocupada"))
    except Exception as e:  # noqa: BLE001
        registrar(f"AVISO: não consegui olhar o worker.lock ({e})")
        return False
    finally:
        sys.path.remove(str(APP))


def main() -> int:
    exe = PYTHONW if PYTHONW.is_file() else Path(sys.executable)
    quedas: list[float] = []
    espera = 30.0
    while True:
        if worker_ja_rodando():
            registrar("worker já está rodando (worker.lock ocupado); nada a fazer")
            return 0
        env = carregar_env_cmd()
        registrar(f"iniciando worker: {exe} -m oficina3d.worker (cwd {APP})")
        try:
            p = subprocess.Popen([str(exe), "-m", "oficina3d.worker"], cwd=str(APP), env=env,
                                 creationflags=CREATE_NO_WINDOW | BELOW_NORMAL_PRIORITY_CLASS)
            codigo = p.wait()
        except OSError as e:
            registrar(f"ERRO ao iniciar o worker: {e}")
            codigo = -1
        if codigo == 0:
            registrar("worker terminou normalmente")
            return 0
        agora = time.monotonic()
        quedas = [t for t in quedas if agora - t < 3600] + [agora]
        registrar(f"worker caiu (código {codigo}); queda {len(quedas)} na última hora")
        if len(quedas) > MAX_QUEDAS_POR_HORA:
            registrar("muitas quedas seguidas; desistindo (a tarefa tenta de novo no próximo logon)")
            return 1
        time.sleep(espera)
        espera = min(espera * 2, 600.0)


if __name__ == "__main__":
    sys.exit(main())
