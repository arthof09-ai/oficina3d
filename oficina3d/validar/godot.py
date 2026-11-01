"""Chama o Godot headless com _godot_validar.gd e devolve o JSON que ele imprimiu."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from oficina3d import config

SCRIPT = Path(__file__).with_name("_godot_validar.gd")
PREFIXO = "VALIDACAO_JSON "


class ErroGodot(RuntimeError):
    """O Godot não rodou ou não devolveu a linha VALIDACAO_JSON."""


def disponivel() -> bool:
    return Path(config.GODOT).is_file()


def carregar(glb, timeout_s: int = 300) -> dict:
    """Carrega `glb` no Godot (--headless, sem janela) e devolve o dict do script.

    O dict tem "ok": False quando o Godot abriu mas não conseguiu carregar o arquivo
    (o motivo vem em "erro"); levanta ErroGodot só quando o próprio Godot falhou.
    """
    if not disponivel():
        raise ErroGodot(f"Godot não encontrado em {config.GODOT} (defina OFICINA3D_GODOT)")
    cmd = [str(config.GODOT), "--headless", "--script", str(SCRIPT), "--", str(Path(glb).resolve())]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace",
                           timeout=timeout_s, env=config.env_subprocesso(), cwd=str(SCRIPT.parent),
                           creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
    except subprocess.TimeoutExpired as e:
        raise ErroGodot(f"Godot passou de {timeout_s} s carregando {glb}") from e
    linhas = [x for x in (r.stdout or "").splitlines() if x.startswith(PREFIXO)]
    if not linhas:
        fim = "\n".join(((r.stdout or "") + (r.stderr or "")).splitlines()[-15:])
        raise ErroGodot(f"Godot saiu com {r.returncode} sem a linha {PREFIXO.strip()}:\n{fim}")
    dados = json.loads(linhas[-1][len(PREFIXO):])
    dados["codigo_saida"] = r.returncode
    dados["erros_godot"] = [x.strip() for x in (r.stdout + r.stderr).splitlines()
                            if x.lstrip().startswith(("ERROR:", "SCRIPT ERROR:"))][:20]
    return dados
