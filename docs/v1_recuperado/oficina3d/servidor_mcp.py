"""Servidor MCP da Oficina 3D: deixa Claude, ChatGPT/Codex e outras IAs usarem o app como ferramenta.

Roda no ambiente separado .venv_mcp (o pacote `mcp` 2.x pede versões de pydantic/starlette
diferentes das do Hunyuan). Só usa as partes leves do app (job, config, motores.listar).

    E:\\RPG_Assimilacao\\Oficina3D\\.venv_mcp\\Scripts\\python.exe -m oficina3d.servidor_mcp            (stdio)
    ... -m oficina3d.servidor_mcp --http --porta 8766                                                       (HTTP local)
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import uuid
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from . import config
from . import job as jobs

INSTRUCOES = (
    "Oficina 3D: gera modelo 3D (GLB) a partir de imagem(ns) de personagem/criatura/objeto, roda numa GTX 1660 "
    "SUPER 6 GB. Fluxo: listar_motores -> submeter_job (imagens PNG com fundo transparente, cada uma com a vista: "
    "frente, costas, esquerda, direita...) -> status_job até 'concluido' -> obter_resultado (caminho do modelo.glb, "
    "prévias, nota de silhueta). Um job por vez na GPU; o worker precisa estar rodando (iniciar_worker). "
    "'esquerda' = imagem em que o personagem olha para a esquerda da imagem."
)

servidor = MCPServer(name="oficina3d", title="Oficina 3D", instructions=INSTRUCOES, version="0.1.0")


def _worker_vivo() -> dict:
    trava = config.JOBS / ".worker.lock"
    if not trava.exists():
        return {"vivo": False, "pid": None}
    try:
        pid = int(trava.read_text(encoding="utf-8").split()[0])
    except (ValueError, IndexError, OSError):
        return {"vivo": False, "pid": None}
    r = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True)
    return {"vivo": str(pid) in r.stdout, "pid": pid}


def _resumo(j: dict) -> dict:
    return {k: j.get(k) for k in ("id", "nome", "modo", "estado", "etapa", "progresso", "erro", "avisos", "criado_em")} | {
        "motor": j.get("opcoes", {}).get("motor")}


@servidor.tool()
def listar_motores() -> list[dict]:
    """Lista os motores de forma disponíveis neste PC (nome, descrição, se aceita várias vistas, se está pronto)."""
    try:
        from . import motores
        return motores.listar()
    except Exception as e:  # o pacote motores é leve, mas não pode derrubar o servidor
        return [{"erro": f"não consegui listar os motores: {e}"}]


@servidor.tool()
def submeter_job(imagens: list[dict], modo: str = "livre", motor: str | None = None, nome: str | None = None,
                 alvo_triangulos: int | None = None, simetrizar: bool = False, passos: int | None = None,
                 malha: str | None = None) -> dict:
    """Cria um pedido de modelo 3D.

    imagens: lista de objetos {"caminho": "E:\\\\...\\\\frente.png", "vista": "frente"} ou
             {"base64": "<png em base64>", "nome": "frente.png", "vista": "frente"} (para quem não está neste PC).
             vista pode faltar (é deduzida pelo nome do arquivo, ex.: 01_FRENTE).
    modo: livre | corpo-base | multivista | so-refinar.  motor: ver listar_motores (padrão hunyuan-mini-turbo;
    para várias vistas use hunyuan-mv-turbo).  malha: caminho de .glb/.obj (só no modo so-refinar).
    Devolve o id do job; acompanhe com status_job.
    """
    tmp = config.TMP / f"mcp_{uuid.uuid4().hex[:10]}"
    tmp.mkdir(parents=True, exist_ok=True)
    try:
        arquivos = []
        for i, im in enumerate(imagens):
            if im.get("caminho"):
                p = Path(im["caminho"])
                if not p.is_file():
                    raise ValueError(f"imagem não encontrada: {p}")
            elif im.get("base64"):
                p = tmp / Path(im.get("nome") or f"imagem_{i}.png").name
                p.write_bytes(base64.b64decode(im["base64"]))
            else:
                raise ValueError("cada imagem precisa de 'caminho' ou 'base64'")
            arquivos.append((p, im.get("vista") or None))
        opcoes = {"simetrizar": simetrizar}
        if motor:
            opcoes["motor"] = motor
        if alvo_triangulos:
            opcoes["alvo_triangulos"] = int(alvo_triangulos)
        if passos:
            opcoes["passos"] = int(passos)
        j = jobs.criar_job(arquivos, modo=modo, opcoes=opcoes, nome=nome, malha=Path(malha) if malha else None)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    w = _worker_vivo()
    return {"id": j["id"], "estado": j["estado"], "motor": j["opcoes"]["motor"], "worker_vivo": w["vivo"],
            "aviso": None if w["vivo"] else "o worker não está rodando: chame iniciar_worker"}


@servidor.tool()
def status_job(id: str) -> dict:
    """Estado de um job: pendente | processando | concluido | erro | cancelado, etapa, progresso (0-100), avisos."""
    j = jobs.ler_job(id)
    r = _resumo(j)
    r["ultimas_mensagens"] = j.get("historico", [])[-5:]
    return r


@servidor.tool()
def listar_jobs(limite: int = 20) -> list[dict]:
    """Os jobs mais recentes (resumo)."""
    return [_resumo(j) for j in jobs.listar_jobs()[-limite:]][::-1]


@servidor.tool()
def obter_resultado(id: str) -> dict:
    """Resultado de um job concluído: caminhos absolutos do modelo.glb, malha crua, prévias, relatório e a nota
    de fidelidade por silhueta (IoU por vista, 0-1)."""
    j = jobs.ler_job(id)
    if j.get("estado") != "concluido" or not j.get("resultado"):
        return {"id": id, "estado": j.get("estado"), "erro": j.get("erro"), "pronto": False}
    raiz = jobs.pasta_job(id)
    res = j["resultado"]
    absol = lambda rel: str((raiz / rel).resolve()) if rel else None  # noqa: E731
    saida = {"id": id, "pronto": True, "glb": absol(res.get("glb")), "glb_cru": absol(res.get("glb_cru")),
             "previas": [absol(p) for p in res.get("previas", [])], "relatorio": absol(res.get("relatorio")),
             "avisos": j.get("avisos", [])}
    try:
        rel = json.loads((raiz / res["relatorio"]).read_text(encoding="utf-8"))
        ref = rel.get("refino") or rel.get("etapas", {}).get("refino") or {}
        saida["silhueta_iou"] = ref.get("silhueta_iou")
        saida["metricas_refino"] = ref.get("metricas")
    except Exception:
        pass
    return saida


@servidor.tool()
def cancelar_job(id: str) -> dict:
    """Cancela um job pendente ou em processamento."""
    j = jobs.ler_job(id)
    if j["estado"] not in ("pendente", "processando"):
        return {"id": id, "estado": j["estado"], "cancelado": False}
    j["estado"] = "cancelado"
    jobs.registrar(j, None, "cancelado pelo servidor MCP")
    return {"id": id, "estado": "cancelado", "cancelado": True}


@servidor.tool()
def iniciar_worker() -> dict:
    """Liga o worker (processa a fila, um job por vez na GPU), se ainda não estiver rodando."""
    w = _worker_vivo()
    if w["vivo"]:
        return {"ja_estava_rodando": True, **w}
    log = open(config.BASE / "jobs" / "worker.log", "ab")
    flags = 0x00000008 | 0x00000200  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    p = subprocess.Popen([str(config.PY_APP), "-m", "oficina3d.worker"], cwd=str(config.APP),
                         env=config.env_subprocesso(), stdout=log, stderr=log, creationflags=flags)
    return {"iniciado": True, "pid": p.pid, "log": str(config.BASE / "jobs" / "worker.log")}


@servidor.tool()
def saude() -> dict:
    """Situação do PC: GPU, espaço livre no disco E: e se o worker está vivo."""
    livre = shutil.disk_usage("E:\\").free / 2**30
    try:
        gpu = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu",
                              "--format=csv,noheader"], capture_output=True, text=True, timeout=8).stdout.strip()
    except Exception as e:
        gpu = f"indisponível ({e})"
    return {"gpu": gpu, "disco_e_livre_gb": round(livre, 1), "worker": _worker_vivo()}


def main():
    ap = argparse.ArgumentParser(description="Servidor MCP da Oficina 3D")
    ap.add_argument("--http", action="store_true", help="HTTP local (streamable-http) em vez de stdio")
    ap.add_argument("--porta", type=int, default=8766)
    a = ap.parse_args()
    os.chdir(config.APP)
    if a.http:
        servidor.run(transport="streamable-http", host="127.0.0.1", port=a.porta)
    else:
        servidor.run()


if __name__ == "__main__":
    sys.exit(main())
