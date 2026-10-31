"""Lancador da pagina web da Oficina 3D para a Tarefa Agendada (sem janela).

Espelho do lancador do worker (instalacao\tarefa_worker\iniciar_worker.py):
1. carrega o `instalacao\\env.cmd` (roda `cmd /c call env.cmd && set` escondido
   e copia o ambiente resultante);
2. se a porta 8765 ja responde, sai sem fazer nada (a web ja esta no ar);
3. roda `.venv_app\\Scripts\\pythonw.exe -m oficina3d.web` com cwd = app,
   prioridade abaixo do normal e sem janela;
4. se a web cair (codigo != 0), espera e reinicia (30 s, 1, 2, 4... ate
   10 min); mais de 5 quedas em 1 hora -> desiste e sai com erro.
Log em `<BASE>\\_cache\\logs\\tarefa_web.log` (local, nunca no Drive).

Criado pelo Muse em 31/10/2026 (Fase 1, item 5), seguindo o padrao do worker.
"""
from __future__ import annotations

import os
import socket
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

APP = Path(__file__).resolve().parents[2]
BASE = APP.parent
ENV_CMD = APP / "instalacao" / "env.cmd"
PYTHON = BASE / ".venv_app" / "Scripts" / "python.exe"
LOG_SERVIDOR = BASE / "_cache" / "logs" / "web_server.log"
LOG = BASE / "_cache" / "logs" / "tarefa_web.log"
PORTA = 8765

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
        registrar(f"AVISO: {ENV_CMD} nao existe; seguindo com o ambiente atual")
        return env
    try:
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


def web_ja_no_ar() -> bool:
    try:
        with socket.create_connection(("127.0.0.1", PORTA), timeout=2):
            return True
    except OSError:
        return False


def main() -> int:
    exe = PYTHON if PYTHON.is_file() else Path(sys.executable)
    quedas: list[float] = []
    espera = 30.0
    while True:
        if web_ja_no_ar():
            registrar("web ja esta no ar (porta 8765 responde); nada a fazer")
            return 0
        env = carregar_env_cmd()
        registrar(f"iniciando web: {exe} -m oficina3d.web (cwd {APP})")
        try:
            # python.exe (NAO pythonw): o __main__ da web e o uvicorn escrevem em
            # sys.stderr, que nao existe no pythonw (a web morria em ~3 s, codigo 1).
            # CREATE_NO_WINDOW esconde o console; a saida vai para web_server.log.
            LOG_SERVIDOR.parent.mkdir(parents=True, exist_ok=True)
            logf = open(LOG_SERVIDOR, "ab")
            try:
                p = subprocess.Popen([str(exe), "-m", "oficina3d.web"], cwd=str(APP), env=env,
                                     stdout=logf, stderr=subprocess.STDOUT,
                                     creationflags=CREATE_NO_WINDOW | BELOW_NORMAL_PRIORITY_CLASS)
            finally:
                logf.close()
            codigo = p.wait()
        except OSError as e:
            registrar(f"ERRO ao iniciar a web: {e}")
            codigo = -1
        if codigo == 0:
            registrar("web terminou normalmente")
            return 0
        agora = time.monotonic()
        quedas = [t for t in quedas if agora - t < 3600] + [agora]
        registrar(f"web caiu (codigo {codigo}); queda {len(quedas)} na ultima hora")
        if len(quedas) > MAX_QUEDAS_POR_HORA:
            registrar("muitas quedas seguidas; desistindo (a tarefa tenta de novo no proximo logon)")
            return 1
        time.sleep(espera)
        espera = min(espera * 2, 600.0)


if __name__ == "__main__":
    sys.exit(main())
