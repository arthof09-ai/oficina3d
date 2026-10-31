"""Servidor MCP da Oficina 3D (v2): deixa Claude, ChatGPT/Codex e outras IAs usarem o app como ferramenta.

Roda no ambiente separado .venv_mcp (pacote `mcp==2.3.0`, onde FastMCP virou `MCPServer`, em
`mcp.server.mcpserver`). Só usa as partes leves do app (config, job, motores.listar, saude).

    <BASE>\\.venv_mcp\\Scripts\\python.exe -m oficina3d.mcp                       (stdio)
    <BASE>\\.venv_mcp\\Scripts\\python.exe -m oficina3d.mcp --http --porta 8766   (HTTP local, COM token)

(cwd = app\\, ou PYTHONPATH apontando para app\\. Não ponha app\\oficina3d\\ no PYTHONPATH: o nome deste
pacote, `mcp`, esconderia a biblioteca `mcp`.)

Correções em relação à v1 (servidor_mcp.py), plano 6.4/6.5:
- PID do worker conferido pelo psutil + horário de criação (seguranca.processo_confere), import preguiçoso;
- iniciar_worker idempotente (worker vivo -> não abre outro; trava de partida contra duas chamadas seguidas;
  "não sei se está vivo" -> recusa);
- base64 com limite de 40 MB (conferido antes de decodificar) e tipo conferido pelos primeiros bytes;
- caminhos locais só dentro das pastas permitidas (resolve() + is_relative_to);
- nada de E:\\ fixo (pastas vêm de oficina3d.config, que lê OFICINA3D_BASE/OFICINA3D_JOBS);
- HTTP só com token (arquivo BASE\\locks\\oficina3d_token.txt ou OFICINA3D_TOKEN), comparação em tempo
  constante, sem token -> o HTTP nem sobe;
- prepare-only + confirmar=true nas ações que executam (submeter_job, cancelar_job, iniciar_worker);
- id de job validado em todas as ferramentas.
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import os
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

from . import seguranca as seg
from .seguranca import ErroSeguranca

VERSAO = "2.0.0"
PORTA_HTTP = 8766
HOST = "127.0.0.1"  # fixo: nada exposto à rede (acesso de fora só por túnel com token — decisão do Mestre)
LIMITE_TOTAL_BASE64 = 160 * 1024 * 1024
VALIDADE_TRAVA_PARTIDA_S = 90

# Do contrato (ARQUITETURA.md). Usados só se oficina3d.config não tiver as constantes.
VISTAS_PADRAO = ("frente", "costas", "esquerda", "direita", "frente-esquerda", "frente-direita",
                 "costas-esquerda", "costas-direita", "cima", "detalhe", "referencia-de-cor")
MODOS_PADRAO = ("livre", "corpo-base", "multivista", "so-refinar")

INSTRUCOES = (
    "Oficina 3D: gera modelo 3D (GLB) a partir de imagem(ns) de personagem/criatura/objeto, numa GPU só. "
    "Fluxo: listar_motores -> submeter_job (imagens PNG com fundo transparente, cada uma com a vista: frente, "
    "costas, esquerda, direita...) -> status_job até 'concluido' -> obter_resultado (caminhos) ou "
    "baixar_resultado_base64 (para quem não está neste PC). Ações que executam (submeter_job, cancelar_job, "
    "iniciar_worker) primeiro devolvem o PLANO; para executar, chame de novo com os mesmos argumentos e "
    "confirmar=true. Um job por vez na GPU; o worker precisa estar rodando (iniciar_worker). "
    "'esquerda' = imagem em que o personagem olha para a esquerda da imagem. Caminhos locais só valem dentro "
    "das pastas permitidas (ver saude)."
)


# =============================================================== acesso preguiçoso ao app
# (os testes trocam estas funções por versões falsas; o servidor importa o app só quando precisa)
def _config():
    from .. import config
    return config


def _jobs():
    from .. import job
    return job


def _pastas() -> dict:
    c = _config()
    base = Path(c.BASE)
    return {
        "base": base,
        "app": Path(getattr(c, "APP", base / "app")),
        "jobs": Path(getattr(c, "JOBS", base / "jobs")),
        "locks": Path(getattr(c, "LOCKS", base / "locks")),
        "tmp": Path(getattr(c, "TMP", base / "_cache" / "tmp")),
    }


def pastas_permitidas() -> list[Path]:
    """Onde caminhos locais podem apontar: BASE\\entradas, a pasta de jobs (para reaproveitar resultados no
    modo so-refinar) e o que estiver em config.PASTAS_PERMITIDAS ou na variável OFICINA3D_PASTAS_PERMITIDAS
    (separadas por ';'). Só caminhos absolutos contam."""
    p = _pastas()
    raizes = [p["base"] / "entradas", p["jobs"]]
    raizes += [Path(x) for x in getattr(_config(), "PASTAS_PERMITIDAS", ()) or ()]
    extra = os.environ.get("OFICINA3D_PASTAS_PERMITIDAS", "")
    raizes += [Path(x.strip()) for x in extra.split(os.pathsep) if x.strip()]
    return [r for r in raizes if r.is_absolute()]


def _vistas() -> tuple:
    return tuple(getattr(_config(), "VISTAS", VISTAS_PADRAO))


def _modos() -> tuple:
    return tuple(getattr(_config(), "MODOS", MODOS_PADRAO))


def _travas_worker() -> list[Path]:
    """Onde o worker grava a trava: config.TRAVA_WORKER (v2: BASE\\locks\\worker.lock); jobs\\.worker.lock (v1)."""
    p = _pastas()
    v2 = Path(getattr(_config(), "TRAVA_WORKER", p["locks"] / "worker.lock"))
    return [v2, p["jobs"] / ".worker.lock"]


def situacao_worker() -> dict:
    w = seg.situacao_worker(_travas_worker())
    partida = _pastas()["locks"] / "iniciando_worker.lock"
    try:
        if w["vivo"] is not True and time.time() - partida.stat().st_mtime < VALIDADE_TRAVA_PARTIDA_S:
            w["iniciando"] = True
    except OSError:
        pass
    return w


def _job_seguro(job_id) -> tuple[dict, Path]:
    """Valida o id, confere que a pasta fica dentro da pasta de jobs e lê o job.json."""
    seg.validar_id(job_id)
    jobs = _jobs()
    raiz_jobs = _pastas()["jobs"].resolve()
    raiz = Path(jobs.pasta_job(job_id)).resolve()
    if not seg._dentro(raiz, raiz_jobs) or raiz == raiz_jobs:
        raise ErroSeguranca("pasta do job fora da pasta de jobs")
    try:
        j = jobs.ler_job(job_id)
    except FileNotFoundError:
        raise ErroSeguranca(f"job não encontrado: {job_id}") from None
    return j, raiz


def alterar_job(job_id: str, alterar) -> dict:
    """Lê, altera e grava o job.json com a trava do job (job.atualizar_job); sem ela, lê e salva na hora."""
    jobs = _jobs()
    seg.validar_id(job_id)
    if hasattr(jobs, "atualizar_job"):
        return jobs.atualizar_job(job_id, alterar)
    j = jobs.ler_job(job_id)
    novo = alterar(j)
    j = novo if novo is not None else j
    jobs.salvar_job(j)
    return j


def _resumo(j: dict) -> dict:
    r = {k: j.get(k) for k in ("id", "nome", "modo", "estado", "etapa", "progresso", "erro", "avisos", "criado_em")}
    r["motor"] = (j.get("opcoes") or {}).get("motor")
    return r


def _rel_seguro(raiz: Path, rel) -> Path | None:
    """Caminho relativo vindo do job.json -> absoluto, só se ficar dentro da pasta do job."""
    if not rel:
        return None
    try:
        return seg.caminho_dentro(raiz, str(rel).replace("\\", "/"), deve_existir=False)
    except ErroSeguranca:
        return None


def _motores_disponiveis() -> list[dict] | None:
    try:
        from .. import motores
        return list(motores.listar())
    except Exception:
        return None


def _trava_partida(arq: Path, validade: float = VALIDADE_TRAVA_PARTIDA_S) -> bool:
    """Cria a trava de partida de forma exclusiva (O_EXCL). False = outra chamada já está ligando o worker."""
    arq.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(2):
        try:
            fd = os.open(str(arq), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                if time.time() - arq.stat().st_mtime > validade:
                    arq.unlink()
                    continue
            except OSError:
                pass
            return False
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(f"{os.getpid()} {time.time():.3f}\n")
        return True
    return False


# =============================================================== ferramentas
def listar_motores() -> list[dict]:
    """Lista os motores de forma deste PC (nome, descrição, se aceita várias vistas, se está pronto)."""
    m = _motores_disponiveis()
    if m is None:
        return [{"erro": "não consegui listar os motores (pacote oficina3d.motores indisponível)"}]
    return m


def submeter_job(imagens: list[dict], modo: str = "livre", motor: str | None = None, nome: str | None = None,
                 alvo_triangulos: int | None = None, simetrizar: bool = False, passos: int | None = None,
                 malha: str | None = None, confirmar: bool = False) -> dict:
    """Cria um pedido de modelo 3D. SEM confirmar=true só confere tudo e devolve o plano (nada é criado).

    imagens: lista de {"caminho": "<caminho absoluto dentro das pastas permitidas>", "vista": "frente"} ou
             {"base64": "<png/jpg/webp em base64, até 40 MB>", "nome": "frente.png", "vista": "frente"}.
             vista pode faltar (é deduzida pelo nome do arquivo, ex.: 01_FRENTE). Até 12 imagens.
    modo: livre | corpo-base | multivista | so-refinar.  motor: ver listar_motores.
    malha: caminho de .glb/.obj (só no modo so-refinar), dentro das pastas permitidas.
    Devolve o plano (confirmar=false) ou o id do job (confirmar=true); acompanhe com status_job.
    """
    modos, vistas = _modos(), _vistas()
    if modo not in modos:
        raise ErroSeguranca(f"modo inválido: {modo} (use {', '.join(modos)})")
    if not isinstance(imagens, list) or len(imagens) > seg.MAX_IMAGENS:
        raise ErroSeguranca(f"imagens: mande uma lista com no máximo {seg.MAX_IMAGENS}")
    if modo != "so-refinar" and not imagens:
        raise ErroSeguranca("mande pelo menos uma imagem")
    if modo == "so-refinar" and not malha:
        raise ErroSeguranca("o modo so-refinar precisa de 'malha'")
    if malha and modo != "so-refinar":
        raise ErroSeguranca("'malha' só vale no modo so-refinar")
    if nome is not None and (not isinstance(nome, str) or len(nome) > 60):
        raise ErroSeguranca("nome: texto de até 60 caracteres")

    opcoes: dict = {"simetrizar": bool(simetrizar)}
    if motor:
        if not isinstance(motor, str) or not re.fullmatch(r"[a-z0-9-]{1,40}", motor):
            raise ErroSeguranca("motor inválido")
        conhecidos = getattr(_config(), "MOTORES", None)
        if conhecidos is None:
            lista = _motores_disponiveis()
            conhecidos = None if lista is None else {m.get("nome") for m in lista if isinstance(m, dict)}
        if conhecidos is not None and motor not in conhecidos:
            raise ErroSeguranca(f"motor desconhecido: {motor} (ver listar_motores)")
        opcoes["motor"] = motor
    if alvo_triangulos is not None:
        if isinstance(alvo_triangulos, bool) or not isinstance(alvo_triangulos, int) \
                or not 1000 <= alvo_triangulos <= 1_000_000:
            raise ErroSeguranca("alvo_triangulos: inteiro entre 1000 e 1000000")
        opcoes["alvo_triangulos"] = alvo_triangulos
    if passos is not None:
        if isinstance(passos, bool) or not isinstance(passos, int) or not 1 <= passos <= 100:
            raise ErroSeguranca("passos: inteiro entre 1 e 100")
        opcoes["passos"] = passos

    raizes = pastas_permitidas()
    preparadas: list[tuple] = []       # ("caminho", Path, vista) | ("base64", bytes, nome, vista)
    plano_imgs: list[dict] = []
    total_b64 = 0
    for i, im in enumerate(imagens):
        if not isinstance(im, dict):
            raise ErroSeguranca(f"imagem {i + 1}: use um objeto com 'caminho' ou 'base64'")
        vista = im.get("vista") or None
        if vista is not None and vista not in vistas:
            raise ErroSeguranca(f"imagem {i + 1}: vista inválida: {vista} (use {', '.join(vistas)})")
        if im.get("caminho") and im.get("base64"):
            raise ErroSeguranca(f"imagem {i + 1}: use 'caminho' OU 'base64', não os dois")
        if im.get("caminho"):
            p = seg.caminho_permitido(im["caminho"], raizes)
            tipo = seg.conferir_arquivo(p, seg.TIPOS_IMAGEM)
            preparadas.append(("caminho", p, vista))
            plano_imgs.append({"origem": str(p), "tipo": tipo, "bytes": p.stat().st_size, "vista": vista})
        elif im.get("base64"):
            dados, tipo = seg.decodificar_base64(im["base64"], seg.TIPOS_IMAGEM)
            total_b64 += len(dados)
            if total_b64 > LIMITE_TOTAL_BASE64:
                raise ErroSeguranca(f"base64 somado passa de {LIMITE_TOTAL_BASE64 // 2**20} MB")
            nome_arq = seg.nome_seguro(im.get("nome") or f"imagem_{i + 1}", tipo, padrao=f"imagem_{i + 1}")
            preparadas.append(("base64", dados, nome_arq, vista))
            plano_imgs.append({"origem": f"base64 ({nome_arq})", "tipo": tipo, "bytes": len(dados), "vista": vista,
                               "sha256": hashlib.sha256(dados).hexdigest()})
        else:
            raise ErroSeguranca(f"imagem {i + 1}: precisa de 'caminho' ou 'base64'")

    malha_p = None
    if malha:
        malha_p = seg.caminho_permitido(malha, raizes)
        # caminho local: vale o limite de malha do job.py (malha crua pode passar de 40 MB)
        seg.conferir_arquivo(malha_p, seg.TIPOS_MALHA,
                             limite=int(getattr(_jobs(), "LIMITE_BYTES_MALHA", seg.LIMITE_BYTES)))

    plano = {"modo": modo, "nome": nome, "opcoes": opcoes, "imagens": plano_imgs,
             "malha": str(malha_p) if malha_p else None}
    if not confirmar:
        return {"executado": False, "plano": plano,
                "proximo_passo": "confira o plano e chame submeter_job de novo com os mesmos argumentos e confirmar=true"}

    tmp = _pastas()["tmp"] / f"mcp_{uuid.uuid4().hex[:12]}"
    tmp.mkdir(parents=True, exist_ok=False)
    try:
        arquivos = []
        for item in preparadas:
            if item[0] == "caminho":
                arquivos.append((item[1], item[2]))
            else:
                _, dados, nome_arq, vista = item
                destino = tmp / nome_arq
                n = 1
                while destino.exists():
                    n += 1
                    destino = tmp / f"{Path(nome_arq).stem}_{n}{Path(nome_arq).suffix}"
                destino.write_bytes(dados)
                arquivos.append((destino, vista))
        j = _jobs().criar_job(arquivos, modo=modo, opcoes=opcoes, nome=nome, malha=malha_p)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    w = situacao_worker()
    return {"executado": True, "id": j["id"], "estado": j.get("estado"), "motor": (j.get("opcoes") or {}).get("motor"),
            "worker_vivo": w["vivo"],
            "aviso": None if w["vivo"] else "o worker não está rodando: chame iniciar_worker"}


def status_job(id: str) -> dict:
    """Estado de um job: pendente | processando | concluido | erro | cancelado, etapa, progresso (0-100), avisos."""
    j, _ = _job_seguro(id)
    r = _resumo(j)
    r["ultimas_mensagens"] = (j.get("historico") or [])[-5:]
    if j.get("nota_mestre"):
        r["nota_mestre"] = j["nota_mestre"]
    return r


def listar_jobs(limite: int = 20) -> list[dict]:
    """Os jobs mais recentes (resumo), do mais novo para o mais velho. limite: 1 a 200."""
    limite = max(1, min(200, int(limite)))
    return [_resumo(j) for j in _jobs().listar_jobs()[-limite:]][::-1]


def obter_resultado(id: str) -> dict:
    """Resultado de um job concluído: caminhos absolutos do modelo.glb, malha crua, prévias, relatório e a
    nota de fidelidade por silhueta (IoU por vista, 0-1)."""
    j, raiz = _job_seguro(id)
    if j.get("estado") != "concluido" or not j.get("resultado"):
        return {"id": id, "estado": j.get("estado"), "erro": j.get("erro"), "pronto": False}
    res = j["resultado"]

    def absol(rel):
        p = _rel_seguro(raiz, rel)
        return str(p) if p else None

    saida = {"id": id, "pronto": True, "glb": absol(res.get("glb")), "glb_cru": absol(res.get("glb_cru")),
             "previas": [x for x in (absol(p) for p in res.get("previas") or []) if x],
             "relatorio": absol(res.get("relatorio")), "avisos": j.get("avisos", []),
             "nota_mestre": j.get("nota_mestre")}
    rel_p = _rel_seguro(raiz, res.get("relatorio"))
    if rel_p and rel_p.is_file() and rel_p.stat().st_size <= seg.LIMITE_BYTES:
        try:
            import json
            rel = json.loads(rel_p.read_text(encoding="utf-8"))
            ref = rel.get("refino") or (rel.get("etapas") or {}).get("refino") or {}
            saida["silhueta_iou"] = ref.get("silhueta_iou")
            saida["metricas_refino"] = ref.get("metricas")
        except Exception:
            pass
    return saida


def baixar_resultado_base64(id: str, arquivo: str = "glb") -> dict:
    """Devolve um arquivo do resultado em base64 (para clientes que não estão neste PC). Até 40 MB.

    arquivo: "glb" (saida/modelo.glb), "glb_cru" (forma/forma.glb), "relatorio", "previa:<vista>"
             (ex.: previa:frente) ou um caminho relativo dentro de saida/ ou forma/ (ex.: saida/previa_costas.png).
    """
    j, raiz = _job_seguro(id)
    res = j.get("resultado") or {}
    if arquivo in ("glb", "glb_cru", "relatorio"):
        rel = res.get(arquivo) or {"glb": "saida/modelo.glb", "glb_cru": "forma/forma.glb",
                                   "relatorio": "saida/relatorio.json"}[arquivo]
    elif isinstance(arquivo, str) and arquivo.startswith("previa:"):
        vista = arquivo.split(":", 1)[1]
        if vista not in _vistas():
            raise ErroSeguranca("vista inválida")
        rel = f"saida/previa_{vista}.png"
    else:
        rel = str(arquivo)
    if rel.replace("\\", "/").split("/", 1)[0] not in ("saida", "forma"):
        raise ErroSeguranca("só arquivos de saida/ ou forma/")
    p = seg.caminho_dentro(raiz, rel.replace("\\", "/"))
    if not p.is_file():
        raise ErroSeguranca("não é um arquivo")
    tamanho = p.stat().st_size
    if tamanho > seg.LIMITE_BYTES:
        raise ErroSeguranca(f"arquivo grande demais para base64 ({tamanho / 2**20:.1f} MB; limite 40 MB)")
    dados = p.read_bytes()
    tipo = seg.tipo_por_assinatura(dados[:4096])
    mime = {"glb": "model/gltf-binary", "png": "image/png", "jpg": "image/jpeg", "webp": "image/webp",
            "obj": "text/plain"}.get(tipo)
    if mime is None and p.suffix.lower() == ".json":
        mime = "application/json"
    if mime is None:
        raise ErroSeguranca("tipo de arquivo não liberado para download")
    import base64
    return {"id": id, "arquivo": p.relative_to(raiz).as_posix(), "nome": p.name, "tipo_mime": mime,
            "bytes": tamanho, "sha256": hashlib.sha256(dados).hexdigest(),
            "base64": base64.b64encode(dados).decode("ascii")}


def cancelar_job(id: str, confirmar: bool = False) -> dict:
    """Cancela um job pendente ou em processamento. Sem confirmar=true só mostra o que seria feito."""
    j, _ = _job_seguro(id)
    if j.get("estado") not in ("pendente", "processando"):
        return {"id": id, "estado": j.get("estado"), "cancelado": False, "motivo": "só cancela pendente/processando"}
    if not confirmar:
        return {"executado": False, "id": id, "estado": j.get("estado"), "nome": j.get("nome"),
                "proximo_passo": "chame cancelar_job de novo com confirmar=true"}
    mudou = {}

    def cancelar(jj: dict):
        if jj.get("estado") not in ("pendente", "processando"):
            mudou["estado"] = jj.get("estado")
            return None
        jj["estado"] = "cancelado"
        _jobs().registrar(jj, None, "cancelado pelo servidor MCP", salvar=False)
        return None

    alterar_job(id, cancelar)  # relê e grava com a trava do job (o worker pode ter mudado o estado)
    if mudou:
        return {"id": id, "estado": mudou["estado"], "cancelado": False, "motivo": "o estado mudou"}
    return {"executado": True, "id": id, "estado": "cancelado", "cancelado": True}


def iniciar_worker(confirmar: bool = False) -> dict:
    """Liga o worker (processa a fila, um job por vez na GPU), se ainda não estiver rodando.

    Idempotente: se já estiver vivo (ou ligando), não abre outro. Sem confirmar=true só mostra o plano.
    """
    w = situacao_worker()
    if w["vivo"] is True:
        return {"ja_estava_rodando": True, **w}
    if w.get("iniciando"):
        return {"ja_estava_iniciando": True, **w}
    if w["vivo"] is None:
        return {"iniciado": False, "recusado": True,
                "motivo": "não consegui conferir se o worker está vivo (" + w["motivo"] + "); não abro outro",
                **{k: v for k, v in w.items() if k != "motivo"}}
    c, p = _config(), _pastas()
    py = Path(getattr(c, "PY_APP", ""))
    if not py.is_file():
        return {"iniciado": False, "recusado": True, "motivo": f"Python do app não encontrado: {py}"}
    log = p["jobs"] / "worker.log"
    comando = [str(py), "-m", "oficina3d.worker"]
    if not confirmar:
        return {"executado": False, "plano": {"comando": comando, "cwd": str(p["app"]), "log": str(log)},
                "situacao": w, "proximo_passo": "chame iniciar_worker de novo com confirmar=true"}
    if not _trava_partida(p["locks"] / "iniciando_worker.lock"):
        return {"ja_estava_iniciando": True, **situacao_worker()}
    flags = (0x00000008 | 0x00000200) if os.name == "nt" else 0  # DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP
    env = c.env_subprocesso() if hasattr(c, "env_subprocesso") else dict(os.environ)
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "ab") as f:   # o filho herda o descritor; o pai fecha o dele (a v1 vazava)
        proc = subprocess.Popen(comando, cwd=str(p["app"]), env=env, stdin=subprocess.DEVNULL, stdout=f,
                                stderr=subprocess.STDOUT, creationflags=flags, close_fds=True)
    return {"executado": True, "iniciado": True, "pid": proc.pid, "log": str(log)}


def saude() -> dict:
    """Situação do PC: GPU, espaço livre no disco da Oficina, worker vivo, pastas permitidas, token do HTTP."""
    p = _pastas()
    saida: dict = {"versao_servidor": VERSAO}
    try:
        from .. import saude as modulo_saude   # agente G; usado se existir
        for nome_f in ("resumo", "coletar", "medir", "saude"):
            f = getattr(modulo_saude, nome_f, None)
            if callable(f):
                r = f()
                if isinstance(r, dict):
                    saida["saude"] = r
                break
    except Exception as e:
        saida["saude_modulo"] = f"indisponível ({type(e).__name__})"
    if "saude" not in saida:
        try:
            saida["disco_livre_gb"] = round(shutil.disk_usage(p["base"].anchor or str(p["base"])).free / 2**30, 1)
        except OSError as e:
            saida["disco_livre_gb"] = f"indisponível ({e})"
        try:
            saida["gpu"] = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.used,memory.total,utilization.gpu,temperature.gpu",
                 "--format=csv,noheader"], capture_output=True, text=True, timeout=8).stdout.strip()
        except Exception as e:
            saida["gpu"] = f"indisponível ({type(e).__name__})"
    saida["worker"] = situacao_worker()
    saida["pastas_permitidas"] = [str(r) for r in pastas_permitidas()]
    saida["token_http_configurado"] = seg.ler_token(p["locks"]) is not None
    return saida


FERRAMENTAS = (listar_motores, submeter_job, status_job, listar_jobs, obter_resultado, cancelar_job,
               iniciar_worker, saude, baixar_resultado_base64)


# =============================================================== servidor
def criar_servidor():
    """Cria o MCPServer (mcp 2.x). Import preguiçoso: o resto do módulo funciona sem o pacote mcp."""
    try:
        from mcp.server.mcpserver import MCPServer
        s = MCPServer(name="oficina3d", title="Oficina 3D", instructions=INSTRUCOES, version=VERSAO)
    except ImportError:  # mcp 1.x (não é o fixado; só para não quebrar se alguém instalar errado)
        from mcp.server.fastmcp import FastMCP
        s = FastMCP(name="oficina3d", instructions=INSTRUCOES)
    for f in FERRAMENTAS:
        s.tool()(f)
    return s


def app_http_protegido(servidor, token: str):
    """App ASGI do streamable-http envolvido pelo MiddlewareToken. Se não der para envolver, recusa."""
    fabrica = getattr(servidor, "streamable_http_app", None)
    if fabrica is None:
        raise RuntimeError("esta versão do mcp não tem streamable_http_app(); HTTP recusado (sem token não sobe)")
    params = inspect.signature(fabrica).parameters
    kwargs = {k: v for k, v in {"host": HOST, "streamable_http_path": "/mcp"}.items() if k in params}
    return seg.MiddlewareToken(fabrica(**kwargs), token)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Servidor MCP da Oficina 3D")
    ap.add_argument("--http", action="store_true", help="HTTP local (streamable-http, só 127.0.0.1, exige token)")
    ap.add_argument("--porta", type=int, default=PORTA_HTTP)
    a = ap.parse_args(argv)
    if not a.http:
        criar_servidor().run()
        return 0
    token = seg.ler_token(_pastas()["locks"])
    if not token:
        print(f"Recusado: HTTP exige token. Grave um token (>= {seg.TOKEN_MIN} caracteres) em "
              f"{_pastas()['locks'] / seg.NOME_ARQUIVO_TOKEN} ou na variável {seg.VAR_TOKEN}.", file=sys.stderr)
        return 2
    import uvicorn
    app = app_http_protegido(criar_servidor(), token)
    print(f"MCP HTTP em http://{HOST}:{a.porta}/mcp (cabeçalho Authorization: Bearer <token>)", file=sys.stderr)
    uvicorn.run(app, host=HOST, port=a.porta, log_level="warning")
    return 0


if __name__ == "__main__":
    sys.exit(main())
