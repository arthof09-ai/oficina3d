"""Saúde do PC para a Oficina 3D (ferramenta `saude` do MCP e do worker).

Só LÊ: espaço no disco, VRAM, tamanho do cache do Drive, travas e se o Windows
Update está pausado. Não muda nada no Windows.

    python -m oficina3d.saude          resumo em texto
    python -m oficina3d.saude --json   o mesmo dict em JSON (para MCP/web)

Regra do plano v2 (5.1): com menos de 20 GB livres no C: o worker pausa,
arquiva e avisa → `disco_ok()`.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from oficina3d import travas
from oficina3d.travas import caminho_config

LIMITE_DISCO_GB_PADRAO = 20.0
_GB = 1024 ** 3
_CHAVE_WU = r"SOFTWARE\Microsoft\WindowsUpdate\UX\Settings"
_VALORES_WU = ("PauseUpdatesExpiryTime", "PauseFeatureUpdatesEndTime", "PauseQualityUpdatesEndTime",
               "PauseUpdatesStartTime")


def limite_disco_gb() -> float:
    try:
        return float(os.environ.get("OFICINA3D_LIMITE_DISCO_GB", "") or LIMITE_DISCO_GB_PADRAO)
    except ValueError:
        return LIMITE_DISCO_GB_PADRAO


def _unidade_padrao() -> str:
    unidade = os.path.splitdrive(str(caminho_config("BASE")))[0] or "C:"
    return unidade + "\\"


# --------------------------------------------------------------------------- disco

def espaco_disco(unidade: str | None = None) -> dict:
    unidade = unidade or _unidade_padrao()
    u = shutil.disk_usage(unidade)
    return {"unidade": unidade, "total_gb": round(u.total / _GB, 2),
            "usado_gb": round(u.used / _GB, 2), "livre_gb": round(u.free / _GB, 2)}


def disco_ok(limite_gb: float | None = None, unidade: str | None = None) -> bool:
    """True se há pelo menos `limite_gb` (padrão 20, ou OFICINA3D_LIMITE_DISCO_GB) livres.
    Se não der para medir, devolve False (na dúvida, o worker pausa)."""
    limite = limite_gb if limite_gb is not None else limite_disco_gb()
    try:
        return espaco_disco(unidade)["livre_gb"] >= limite
    except OSError:
        return False


# --------------------------------------------------------------------------- cache do Drive

def tamanho_pasta(pasta: Path | str, limite_s: float = 30.0) -> dict:
    """Soma os arquivos da pasta (sem seguir links/junções). Para depois de
    `limite_s` segundos e marca `parcial`."""
    pasta = Path(pasta)
    res = {"caminho": str(pasta), "existe": pasta.is_dir(), "bytes": 0, "gb": 0.0,
           "arquivos": 0, "parcial": False, "erros": 0}
    if not res["existe"]:
        return res
    fim = time.monotonic() + limite_s
    pilha = [str(pasta)]
    while pilha:
        if time.monotonic() > fim:
            res["parcial"] = True
            break
        atual = pilha.pop()
        try:
            with os.scandir(atual) as it:
                for e in it:
                    try:
                        if e.is_symlink():
                            continue
                        if e.is_dir(follow_symlinks=False):
                            # junções do Windows também são pontos de nova análise: pular
                            if getattr(e.stat(follow_symlinks=False), "st_file_attributes", 0) & 0x400:
                                continue
                            pilha.append(e.path)
                        elif e.is_file(follow_symlinks=False):
                            res["bytes"] += e.stat(follow_symlinks=False).st_size
                            res["arquivos"] += 1
                    except OSError:
                        res["erros"] += 1
        except OSError:
            res["erros"] += 1
    res["gb"] = round(res["bytes"] / _GB, 3)
    return res


def cache_drive(limite_s: float = 30.0) -> dict:
    """Tamanho de %LOCALAPPDATA%\\Google\\DriveFS (cache do Drive para computador). Só mede."""
    local = os.environ.get("LOCALAPPDATA")
    if not local:
        return {"caminho": None, "existe": False, "erro": "LOCALAPPDATA não definida"}
    return tamanho_pasta(Path(local) / "Google" / "DriveFS", limite_s=limite_s)


# --------------------------------------------------------------------------- Windows Update

def interpretar_windows_update(valores: dict, agora: datetime | None = None) -> dict:
    """Decide se está pausado a partir dos valores do registro (datas ISO em UTC)."""
    agora = agora or datetime.now(timezone.utc)
    if agora.tzinfo is None:
        agora = agora.replace(tzinfo=timezone.utc)
    fins = []
    for chave in ("PauseUpdatesExpiryTime", "PauseFeatureUpdatesEndTime", "PauseQualityUpdatesEndTime"):
        v = valores.get(chave)
        if isinstance(v, str) and v.strip():
            try:
                d = datetime.fromisoformat(v.strip().replace("Z", "+00:00"))
                fins.append(d if d.tzinfo else d.replace(tzinfo=timezone.utc))
            except ValueError:
                continue
    if not fins:
        return {"pausado": False, "ate": None, "valores": valores}
    ate = max(fins)
    return {"pausado": ate > agora, "ate": ate.isoformat(), "dias_restantes": round((ate - agora).total_seconds() / 86400, 1),
            "valores": valores}


def windows_update() -> dict:
    """Lê (só leitura) HKLM\\SOFTWARE\\Microsoft\\WindowsUpdate\\UX\\Settings."""
    try:
        import winreg
    except ImportError:  # pragma: no cover
        return {"pausado": None, "erro": "winreg indisponível (não é Windows)"}
    valores = {}
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, _CHAVE_WU, 0, winreg.KEY_READ) as k:
            for nome in _VALORES_WU:
                try:
                    valores[nome] = winreg.QueryValueEx(k, nome)[0]
                except FileNotFoundError:
                    pass
    except OSError as e:
        return {"pausado": None, "erro": f"não consegui ler o registro: {e}"}
    return interpretar_windows_update(valores)


# --------------------------------------------------------------------------- tudo junto

def saude(medir_drive: bool = True, ler_gpu: bool = True) -> dict:
    """Retrato do PC para o worker/MCP. Nunca levanta exceção: cada parte tem `erro` se falhar."""
    alertas: list[str] = []
    limite = limite_disco_gb()
    r: dict = {"medido_em": datetime.now().astimezone().isoformat(timespec="seconds")}

    try:
        d = espaco_disco()
        d["limite_gb"] = limite
        d["ok"] = d["livre_gb"] >= limite
        if not d["ok"]:
            alertas.append(f"disco {d['unidade']} com {d['livre_gb']:.1f} GB livres (< {limite:.0f} GB): "
                           "pausar o worker e arquivar")
    except OSError as e:
        d = {"erro": str(e), "ok": False, "limite_gb": limite}
        alertas.append("não consegui medir o disco")
    r["disco"] = d

    if ler_gpu:
        try:
            g = travas.ler_gpu()
            outros = travas.gpu_ocupada_por_outros(amostras=1, intervalo_s=0)
            g["ocupada_por_outros"] = outros.ocupada
            g["motivo"] = outros.motivo
            if outros.ocupada:
                alertas.append(f"GPU em uso por outro programa: {outros.motivo}")
        except Exception as e:  # noqa: BLE001
            g = {"erro": str(e)}
            alertas.append("não consegui ler a GPU (nvidia-smi)")
        r["gpu"] = g

    if medir_drive:
        r["cache_drive"] = cache_drive()

    try:
        r["travas"] = travas.estado_travas()
        for nome, t in r["travas"].items():
            if t.get("orfa"):
                alertas.append(f"trava {nome} órfã (PID {(t.get('dono') or {}).get('pid')} morreu sem soltar)")
    except Exception as e:  # noqa: BLE001
        r["travas"] = {"erro": str(e)}

    r["windows_update"] = windows_update()
    if r["windows_update"].get("pausado") is False:
        alertas.append("Windows Update não está pausado")

    r["alertas"] = alertas
    r["ok"] = not alertas
    return r


def _resumo(r: dict) -> str:
    linhas = [f"Saúde da Oficina 3D ({r['medido_em']})"]
    d = r.get("disco", {})
    if "livre_gb" in d:
        linhas.append(f"- Disco {d['unidade']}: {d['livre_gb']:.1f} GB livres de {d['total_gb']:.1f} GB "
                      f"(limite {d['limite_gb']:.0f} GB) {'OK' if d['ok'] else 'BAIXO'}")
    g = r.get("gpu")
    if g:
        if "erro" in g:
            linhas.append(f"- GPU: erro: {g['erro']}")
        else:
            linhas.append(f"- GPU {g.get('nome')}: VRAM livre {g.get('vram_livre_mb')} de {g.get('vram_total_mb')} MiB, "
                          f"uso {g.get('uso_pct')}%; {'ocupada por outros' if g.get('ocupada_por_outros') else 'livre'}")
    c = r.get("cache_drive")
    if c:
        linhas.append(f"- Cache do Drive: {c.get('gb', 0):.2f} GB" + (" (parcial)" if c.get("parcial") else "")
                      if c.get("existe") else "- Cache do Drive: não encontrado")
    for nome, t in (r.get("travas") or {}).items():
        if isinstance(t, dict):
            situacao = "ocupada" if t.get("ocupada") else ("órfã" if t.get("orfa") else "livre")
            pid = (t.get("dono") or {}).get("pid") if t.get("ocupada") else None
            linhas.append(f"- Trava {nome}: {situacao}" + (f" (PID {pid})" if pid else ""))
    wu = r.get("windows_update", {})
    linhas.append("- Windows Update: " + ("pausado até " + str(wu.get("ate")) if wu.get("pausado")
                                         else ("NÃO pausado" if wu.get("pausado") is False else f"? {wu.get('erro')}")))
    for a in r.get("alertas", []):
        linhas.append(f"! {a}")
    return "\n".join(linhas)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m oficina3d.saude", description="Saúde do PC para a Oficina 3D (só leitura).")
    p.add_argument("--json", action="store_true", help="saída em JSON")
    p.add_argument("--sem-drive", action="store_true", help="não medir o cache do Drive")
    args = p.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass
    r = saude(medir_drive=not args.sem_drive)
    print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else _resumo(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
