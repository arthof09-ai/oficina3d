"""Jobs da Oficina 3D: uma pasta por pedido, estado em job.json (fonte da verdade)."""
import json
import os
import re
import shutil
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

from .config import JOBS, MODOS, OPCOES_PADRAO, VISTAS

FUSO = timezone(timedelta(hours=-3))
SUBPASTAS = ("entrada", "preproc", "forma", "refino", "saida")


def agora() -> str:
    return datetime.now(FUSO).isoformat(timespec="seconds")


def _slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()[:40] or "job"


def pasta_job(job_id: str) -> Path:
    return JOBS / job_id


def salvar_job(job: dict) -> None:
    """Grava job.json de forma atômica (escreve .tmp e troca)."""
    p = pasta_job(job["id"]) / "job.json"
    tmp = p.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(job, ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, p)


def ler_job(job_id: str) -> dict:
    return json.loads((pasta_job(job_id) / "job.json").read_text(encoding="utf-8"))


def listar_jobs() -> list[dict]:
    """Jobs válidos, do mais antigo para o mais novo."""
    jobs = []
    if JOBS.exists():
        for p in sorted(JOBS.iterdir()):
            f = p / "job.json"
            if f.is_file():
                try:
                    jobs.append(json.loads(f.read_text(encoding="utf-8")))
                except (OSError, json.JSONDecodeError):
                    continue
    return sorted(jobs, key=lambda j: j.get("criado_em", ""))


def registrar(job: dict, etapa: str | None, msg: str, progresso: int | None = None, salvar: bool = True) -> None:
    job["historico"].append({"quando": agora(), "etapa": etapa, "msg": msg})
    if etapa is not None:
        job["etapa"] = etapa
    if progresso is not None:
        job["progresso"] = int(max(0, min(100, progresso)))
    if salvar:
        salvar_job(job)


def criar_job(arquivos: list[tuple[Path, str | None]], modo: str = "livre", opcoes: dict | None = None,
              nome: str | None = None, malha: Path | None = None) -> dict:
    """Cria jobs\\<id>\\ com cópias das imagens (e da malha, no modo so-refinar).

    arquivos: [(caminho_da_imagem, vista ou None)]. Vista None = descobrir depois pelo nome
    (entrada.vista_pelo_nome) ou ficar sem etiqueta.
    """
    if modo not in MODOS:
        raise ValueError(f"modo inválido: {modo} (use {', '.join(MODOS)})")
    if modo == "so-refinar" and malha is None:
        raise ValueError("modo so-refinar precisa de uma malha (.glb/.obj)")
    if modo != "so-refinar" and not arquivos:
        raise ValueError("mande pelo menos uma imagem")
    for _, vista in arquivos:
        if vista is not None and vista not in VISTAS:
            raise ValueError(f"vista inválida: {vista} (use {', '.join(VISTAS)})")

    base_nome = nome or (Path(arquivos[0][0]).stem if arquivos else Path(malha).stem)
    job_id = f"{datetime.now(FUSO):%Y%m%d-%H%M%S}-{_slug(base_nome)}"
    n = 1
    while pasta_job(job_id).exists():
        n += 1
        job_id = f"{job_id.rsplit('_', 1)[0]}_{n}"
    raiz = pasta_job(job_id)
    for s in SUBPASTAS:
        (raiz / s).mkdir(parents=True, exist_ok=True)

    imagens = []
    usados = set()
    for origem, vista in arquivos:
        origem = Path(origem)
        destino = origem.name
        while destino.lower() in usados:
            destino = f"{Path(destino).stem}_{len(usados)}{origem.suffix}"
        usados.add(destino.lower())
        shutil.copy2(origem, raiz / "entrada" / destino)
        imagens.append({"arquivo": f"entrada/{destino}", "vista": vista})

    malha_rel = None
    if malha is not None:
        malha = Path(malha)
        shutil.copy2(malha, raiz / "entrada" / malha.name)
        malha_rel = f"entrada/{malha.name}"

    op = dict(OPCOES_PADRAO)
    op.update({k: v for k, v in (opcoes or {}).items() if v is not None or k in ("passos", "altura_m")})
    job = {
        "id": job_id, "criado_em": agora(), "nome": base_nome, "modo": modo,
        "imagens": imagens, "malha_entrada": malha_rel, "opcoes": op,
        "estado": "pendente", "etapa": None, "progresso": 0, "erro": None, "avisos": [],
        "resultado": None, "historico": [],
    }
    salvar_job(job)
    registrar(job, None, f"job criado ({len(imagens)} imagem(ns), modo {modo}, motor {op['motor']})")
    return job
