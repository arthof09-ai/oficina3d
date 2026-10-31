"""Blender headless: localizar, rodar scripts com pedido JSON e ler o progresso.

Convenção de eixos e vistas (A10 do plano v2; confere com a v1):

- GLB de saída: **Y para cima**, frente do personagem em **+Z** (padrão glTF/Godot).
- No Blender (Z para cima) isso é: frente do personagem em **−Y**.
- Lado ESQUERDO do personagem = **+X** (nos dois sistemas).
- Vista ``esquerda`` = imagem em que o personagem olha para a esquerda da imagem,
  mostrando o lado esquerdo do corpo → câmera em +X olhando para −X.

Ângulo de cada vista: câmera em ``(sen a, −cos a, 0)`` no Blender, olhando o centro.

| vista            | a (graus) | câmera no Blender | câmera no glTF |
|------------------|-----------|-------------------|----------------|
| frente           |     0     | −Y                | +Z             |
| frente-esquerda  |    45     | +X −Y             | +X +Z          |
| esquerda         |    90     | +X                | +X             |
| costas-esquerda  |   135     | +X +Y             | +X −Z          |
| costas           |   180     | +Y                | −Z             |
| costas-direita   |   225     | −X +Y             | −X −Z          |
| direita          |   270     | −X                | −X             |
| frente-direita   |   315     | −X −Y             | −X +Z          |
| cima             |    —      | +Z (olhando para baixo; costas no alto da imagem) | +Y |
"""
from __future__ import annotations

import glob
import json
import math
import os
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

AQUI = Path(__file__).resolve().parent
SCRIPT_REFINO = AQUI / "_blender_refino.py"
SCRIPT_PREVIA = AQUI / "_blender_previa.py"

ANGULOS = {
    "frente": 0, "frente-esquerda": 45, "esquerda": 90, "costas-esquerda": 135,
    "costas": 180, "costas-direita": 225, "direita": 270, "frente-direita": 315,
}
# Prévias entregues em saida\ (v1: frente, frente-direita, direita, costas; v2 soma esquerda).
VISTAS_PREVIA = ("frente", "frente-direita", "direita", "esquerda", "costas")


def direcao_camera(vista: str, sistema: str = "blender") -> tuple[float, float, float]:
    """Vetor unitário do centro do modelo até a câmera (``blender`` Z-up ou ``gltf`` Y-up)."""
    if vista == "cima":
        bx, by, bz = 0.0, 0.0, 1.0
    elif vista in ANGULOS:
        a = math.radians(ANGULOS[vista])
        bx, by, bz = math.sin(a), -math.cos(a), 0.0
    else:
        raise ValueError(f"vista sem câmera definida: {vista!r}")
    bx, by, bz = (round(c, 6) + 0.0 for c in (bx, by, bz))
    if sistema == "blender":
        return bx, by, bz
    if sistema == "gltf":  # Blender (x, y, z) -> glTF (x, z, −y)
        return bx, bz, (-by) + 0.0
    raise ValueError(f"sistema desconhecido: {sistema!r}")


# ----------------------------------------------------------------------------
# Localizar o Blender
# ----------------------------------------------------------------------------
def _config():
    try:
        from oficina3d import config  # noqa: PLC0415 — contrato do Agente A
        return config
    except Exception:  # noqa: BLE001 — config ainda pode não existir/estar quebrado
        return None


def _base_oficina() -> Path:
    cfg = _config()
    for nome in ("BASE", "OFICINA3D_BASE"):
        v = getattr(cfg, nome, None) if cfg else None
        if v:
            return Path(v)
    if os.environ.get("OFICINA3D_BASE"):
        return Path(os.environ["OFICINA3D_BASE"])
    return AQUI.parents[2]  # app\oficina3d\refino -> Oficina3D


def achar_blender() -> Path | None:
    """Ordem: env ``OFICINA3D_BLENDER`` → ``config.BLENDER`` → pastas conhecidas → PATH."""
    candidatos: list[Path] = []
    if os.environ.get("OFICINA3D_BLENDER"):
        candidatos.append(Path(os.environ["OFICINA3D_BLENDER"]))
    cfg = _config()
    if cfg is not None:
        for nome in ("BLENDER", "BLENDER_EXE", "CAMINHO_BLENDER"):
            v = getattr(cfg, nome, None)
            if v:
                candidatos.append(Path(v))
    base = _base_oficina()
    padroes = [
        str(base / "[Ff]erramentas" / "**" / "blender.exe"),
        str(base.parent / "[Ff]erramentas" / "**" / "blender.exe"),
        r"C:\Program Files\Blender Foundation\Blender*\blender.exe",
    ]
    for p in padroes:
        achados = sorted(glob.glob(p, recursive=True), reverse=True)  # versão maior primeiro
        candidatos.extend(Path(a) for a in achados)
    no_path = shutil.which("blender")
    if no_path:
        candidatos.append(Path(no_path))
    for c in candidatos:
        if c.is_file():
            return c
    return None


def env_blender() -> dict:
    cfg = _config()
    env = None
    if cfg is not None and hasattr(cfg, "env_subprocesso"):
        try:
            env = cfg.env_subprocesso()
        except Exception:  # noqa: BLE001
            env = None
    if env is None:
        env = dict(os.environ)
    env.setdefault("PYTHONIOENCODING", "utf-8")
    return env


# ----------------------------------------------------------------------------
# Rodar
# ----------------------------------------------------------------------------
class ErroBlender(RuntimeError):
    pass


def rodar_blender(script: Path, pedido: dict, pasta: Path, nome: str,
                  progresso=None, faixa: tuple[int, int] = (0, 100),
                  timeout_s: float = 900, blender: Path | None = None) -> dict:
    """Roda ``blender -b --factory-startup -P script -- pedido.json``.

    O script imprime ``PROGRESSO <0-100> <msg>`` e grava ``pedido["resultado"]`` (JSON).
    O log completo fica em ``pasta/blender_<nome>.log``.
    """
    blender = blender or achar_blender()
    if blender is None:
        raise ErroBlender("Blender não encontrado (defina OFICINA3D_BLENDER ou config.BLENDER).")
    pasta.mkdir(parents=True, exist_ok=True)
    arq_pedido = pasta / f"pedido_{nome}.json"
    arq_result = pasta / f"resultado_{nome}.json"
    arq_log = pasta / f"blender_{nome}.log"
    if arq_result.exists():
        arq_result.unlink()
    pedido = dict(pedido, resultado=str(arq_result))
    arq_pedido.write_text(json.dumps(pedido, ensure_ascii=False, indent=1), encoding="utf-8")

    cmd = [str(blender), "-b", "--factory-startup", "--python-exit-code", "3",
           "-P", str(script), "--", str(arq_pedido)]
    flags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if sys.platform == "win32" else 0
    t0 = time.perf_counter()
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            env=env_blender(), cwd=str(pasta), creationflags=flags)
    ultimas: list[str] = []
    ini, fim = faixa

    def ler():
        with open(arq_log, "w", encoding="utf-8") as log:
            for bruto in proc.stdout:
                linha = bruto.decode("utf-8", errors="replace").rstrip()
                log.write(linha + "\n")
                ultimas.append(linha)
                del ultimas[:-40]
                if linha.startswith("PROGRESSO ") and progresso:
                    partes = linha.split(" ", 2)
                    try:
                        pct = int(float(partes[1]))
                    except (IndexError, ValueError):
                        continue
                    msg = partes[2] if len(partes) > 2 else ""
                    try:
                        progresso(ini + (fim - ini) * max(0, min(100, pct)) // 100, msg)
                    except Exception:  # noqa: BLE001 — progresso nunca derruba o refino
                        pass

    leitor = threading.Thread(target=ler, daemon=True)
    leitor.start()
    try:
        codigo = proc.wait(timeout=timeout_s)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()
        leitor.join(5)
        if proc.stdout:
            proc.stdout.close()
        raise ErroBlender(f"Blender ({nome}) passou de {timeout_s:.0f} s e foi encerrado. Log: {arq_log}")
    leitor.join(10)
    if proc.stdout:
        proc.stdout.close()
    tempo = time.perf_counter() - t0

    resultado = None
    if arq_result.exists():
        try:
            resultado = json.loads(arq_result.read_text(encoding="utf-8"))
        except ValueError:
            resultado = None
    if codigo != 0 or not resultado or not resultado.get("ok"):
        erro = (resultado or {}).get("erro") or "\n".join(ultimas[-15:])
        raise ErroBlender(f"Blender ({nome}) falhou (código {codigo}): {erro}\nLog: {arq_log}")
    resultado["tempo_blender_s"] = round(tempo, 2)
    return resultado
