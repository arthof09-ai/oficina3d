"""Worker da Oficina 3D: pega jobs pendentes da fila e processa UM POR VEZ (a GPU é uma só).

    python -m oficina3d.worker               # loop contínuo (varre a fila a cada ~2 s)
    python -m oficina3d.worker --uma-vez     # só os pendentes que JÁ existiam ao começar, e sai
    python -m oficina3d.worker --job ID      # só esse job (se estiver pendente), e sai

Etapas (docs/ARQUITETURA.md + plano v2 6.2):
    1. entrada  (0–10%)   oficina3d.entrada.preparar        (pulada no modo so-refinar)
    2. forma    (10–80%)  oficina3d.motores.gerar -> forma\\forma.glb   (gpu.lock dentro do gerar)
    3. refino   (80–98%)  oficina3d.refino.refinar -> saida\\
    4. exportar (98–100%) saida\\relatorio.json = job + métricas de todas as etapas
    11. arquivar (gancho) oficina3d.arquivar.arquivar_job(job_dir, apagar_local=False): cópia conferida
        no Drive; quem apaga a cópia local depois é arquivar_pendentes() (política de 3 dias / nota).
Falha numa etapa -> estado="erro", erro com a mensagem, traceback no log.txt, nada apagado.

Robustez (plano v2: A12, E9, E10):
  * worker.lock: `oficina3d.travas.adquirir_worker()` (trava do SO; morre junto com o processo);
  * o worker entra num Job Object do Windows: se ele morrer, motor e Blender morrem junto;
  * job órfão (estado "processando" sem worker vivo) volta para "pendente" ao subir o worker
    (no máximo MAX_RETOMADAS vezes; depois vira "erro" para não entrar em laço);
  * cancelamento: o job.json do disco é conferido a cada ~3 s durante o motor e antes de cada gravação
    (o worker nunca sobrescreve um "cancelado" gravado pelo cli/web/MCP);
  * a pasta da fila vem só de config.JOBS (OFICINA3D_JOBS); os testes usam jobs_teste\\.
"""
from __future__ import annotations

import argparse
import contextlib
import importlib
import json
import os
import shutil
import sys
import time
import traceback
from pathlib import Path

from . import config, job, motores
from .motores import base

FAIXAS = {"entrada": (0, 10), "forma": (10, 80), "refino": (80, 98), "exportar": (98, 100), "arquivar": (100, 100)}
INTERVALO_CANCEL_S = 3.0
INTERVALO_SALVAR_S = 2.0
INTERVALO_HISTORICO_S = 30.0
INTERVALO_ARQUIVAR_S = 600.0
MAX_RETOMADAS = 2
LIVRE_MIN_GB_PADRAO = 20.0      # plano 5.1: com menos de 20 GB livres o worker pausa
ESTADOS_FINAIS = ("concluido", "erro", "cancelado")


class JobCancelado(Exception):
    """O job foi marcado como cancelado no disco (cli, web ou MCP)."""


class ErroEtapa(RuntimeError):
    def __init__(self, etapa: str, msg: str):
        super().__init__(msg)
        self.etapa = etapa


# --------------------------------------------------------------------------- utilidades

def _pasta_jobs() -> Path:
    return Path(config.JOBS)


def _log(job_dir: Path, msg: str) -> None:
    try:
        with open(job_dir / "log.txt", "a", encoding="utf-8") as f:
            f.write(f"[{job.agora()}] {msg}\n")
    except OSError:
        pass


def _cancelado_no_disco(job_id: str) -> bool:
    try:
        return job.ler_job(job_id).get("estado") == "cancelado"
    except (OSError, ValueError):
        return False


def _salvar(jb: dict) -> None:
    """Grava o job com a trava dele; se o disco diz "cancelado", não sobrescreve (levanta JobCancelado).

    Campos que só existem no disco (ex.: nota do Mestre gravada pela web) são preservados.
    """
    with job.trava_job(jb["id"]):
        try:
            disco = job.ler_job(jb["id"])
        except (OSError, ValueError):
            disco = {}
        if disco.get("estado") == "cancelado" and jb.get("estado") != "cancelado":
            raise JobCancelado()
        job.salvar_job({**disco, **jb})


def _registrar(jb: dict, etapa: str | None, msg: str, progresso: int | None = None) -> None:
    job.registrar(jb, etapa, msg, progresso=progresso, salvar=False)
    _salvar(jb)


def _modulo(nome: str, funcao: str):
    """Função `funcao` de oficina3d.<nome> (módulo de outro agente), com erro claro se faltar."""
    try:
        mod = importlib.import_module(f"oficina3d.{nome}")
    except ModuleNotFoundError as e:
        if e.name in (f"oficina3d.{nome}", None) or "halted" in str(e):
            raise ErroEtapa(nome, f"módulo {nome} ainda não disponível") from e
        raise ErroEtapa(nome, f"módulo {nome} não carregou (falta {e.name}): {e}") from e
    f = getattr(mod, funcao, None)
    if not callable(f):
        raise ErroEtapa(nome, f"módulo {nome} ainda não disponível (sem {funcao}())")
    return f


def _rel(job_dir: Path, caminho) -> str | None:
    if caminho is None:
        return None
    p = Path(caminho)
    try:
        return p.resolve().relative_to(job_dir.resolve()).as_posix()
    except ValueError:
        return str(p)


def _abs(job_dir: Path, imagens: list[dict] | None) -> list[dict]:
    """Imagens com caminhos absolutos (o contrato dos motores e do refino pede assim)."""
    saida = []
    for im in imagens or []:
        p = Path(im["arquivo"])
        saida.append({**im, "arquivo": str(p if p.is_absolute() else (job_dir / p))})
    return saida


def _jsonavel(obj):
    if isinstance(obj, dict):
        return {str(k): _jsonavel(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple, set)):
        return [_jsonavel(v) for v in obj]
    if isinstance(obj, Path):
        return str(obj)
    if hasattr(obj, "item"):  # escalares do numpy
        try:
            return obj.item()
        except Exception:
            pass
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)


class _Progresso:
    """Callback progresso(pct, msg) de uma etapa -> progresso global do job (com limite de gravações).

    Também confere o cancelamento no disco a cada INTERVALO_CANCEL_S (levanta JobCancelado).
    """

    def __init__(self, jb: dict, job_dir: Path, etapa: str):
        self.job, self.job_dir, self.etapa = jb, job_dir, etapa
        self.ini, self.fim = FAIXAS[etapa]
        self.ult_salvar = 0.0
        self.ult_hist = 0.0
        self.ult_cancel = time.time()
        self.ult_msg = None

    def __call__(self, pct, msg: str = "") -> None:
        agora_t = time.time()
        if agora_t - self.ult_cancel >= INTERVALO_CANCEL_S:
            self.ult_cancel = agora_t
            if _cancelado_no_disco(self.job["id"]):
                raise JobCancelado()
        try:
            pct = max(0, min(100, int(pct)))
        except (TypeError, ValueError):
            pct = 0
        glob = int(self.ini + (self.fim - self.ini) * pct / 100)
        msg = (msg or "").strip()
        nova = bool(msg) and msg != self.ult_msg
        if nova:
            _log(self.job_dir, f"{self.etapa}: {pct}% {msg}")
        self.job["progresso"] = max(int(self.job.get("progresso") or 0), glob)
        if nova and agora_t - self.ult_hist >= INTERVALO_HISTORICO_S:
            self.ult_hist = agora_t
            job.registrar(self.job, self.etapa, f"{msg} ({pct}%)", salvar=False)
        self.ult_msg = msg or self.ult_msg
        if agora_t - self.ult_salvar >= INTERVALO_SALVAR_S:
            self.ult_salvar = agora_t
            _salvar(self.job)


def _verificar_cancelado(jb: dict) -> None:
    if _cancelado_no_disco(jb["id"]):
        raise JobCancelado()


def _gravar_relatorio(job_dir: Path, jb: dict, etapas: dict, tempos: dict, parcial: bool = False) -> Path:
    destino = job_dir / "saida" / ("relatorio_parcial.json" if parcial else "relatorio.json")
    destino.parent.mkdir(parents=True, exist_ok=True)
    rel = {"gerado_em": job.agora(), "job": jb, "etapas": etapas, "tempos_s": tempos,
           "tempo_total_s": round(sum(tempos.values()), 1)}
    tmp = destino.with_name(destino.name + ".tmp")
    tmp.write_text(json.dumps(_jsonavel(rel), ensure_ascii=False, indent=2), encoding="utf-8")
    os.replace(tmp, destino)
    return destino


def _identidade_worker() -> dict:
    return {"pid": os.getpid(), "criado": base.hora_criacao(os.getpid()), "inicio": job.agora()}


def _motor_do_job(jb: dict, op: dict) -> str:
    if op.get("motor"):
        return op["motor"]
    vistas = [im.get("vista") for im in jb.get("imagens") or []]
    return job.motor_padrao(jb.get("modo", "livre"), vistas)


# --------------------------------------------------------------------------- processamento

def processar_job(job_id: str) -> dict:
    """Processa um job do começo ao fim. Devolve o job final (estado concluido/erro/cancelado).

    Não pega a trava do worker (quem chama em paralelo é responsável); loop() pega.
    """
    job_dir = job.pasta_job(job_id)
    jb = job.ler_job(job_id)
    if jb.get("estado") in ("cancelado", "concluido"):
        return jb
    modo = jb.get("modo", "livre")
    op = dict(config.OPCOES_PADRAO)
    op.update({k: v for k, v in (jb.get("opcoes") or {}).items() if v is not None})
    op["motor"] = _motor_do_job(jb, op)
    jb.setdefault("avisos", [])
    jb.setdefault("historico", [])
    for s in job.SUBPASTAS:
        (job_dir / s).mkdir(parents=True, exist_ok=True)

    jb.update({"estado": "processando", "erro": None, "progresso": 0, "resultado": None,
               "worker": _identidade_worker()})
    _log(job_dir, f"=== início do processamento (modo {modo}, motor {op['motor']}) PID {os.getpid()}")
    etapas: dict = {}
    tempos: dict = {}
    etapa_atual = None
    t_job = time.time()
    try:
        _registrar(jb, None, f"processamento iniciado (worker PID {os.getpid()})", progresso=0)

        # 1. entrada ---------------------------------------------------------
        imagens_motor: list[dict] = _abs(job_dir, jb.get("imagens"))
        if modo != "so-refinar":
            etapa_atual = "entrada"
            _verificar_cancelado(jb)
            preparar = _modulo("entrada", "preparar")
            _registrar(jb, "entrada", "preparando imagens", progresso=FAIXAS["entrada"][0])
            t = time.time()
            res = preparar(job_dir, jb, progresso=_Progresso(jb, job_dir, "entrada"))
            tempos["entrada"] = round(time.time() - t, 1)
            etapas["entrada"] = res
            jb["avisos"].extend(res.get("avisos") or [])
            if not res.get("imagens"):
                raise ErroEtapa("entrada", "a entrada não devolveu nenhuma imagem pronta")
            jb["imagens_preproc"] = res["imagens"]
            imagens_motor = _abs(job_dir, res["imagens"])

            # 2. forma -------------------------------------------------------
            etapa_atual = "forma"
            _verificar_cancelado(jb)
            if int(op.get("sementes") or 1) > 1:
                jb["avisos"].append("sementes > 1 ainda não implementado no worker; gerei só com a seed do job")
            _registrar(jb, "forma", f"gerando forma com {op['motor']}", progresso=FAIXAS["forma"][0])
            t = time.time()
            res = motores.gerar(op["motor"], imagens_motor, op, job_dir / "forma",
                                progresso=_Progresso(jb, job_dir, "forma"))
            tempos["forma"] = round(time.time() - t, 1)
            etapas["forma"] = res
            jb["avisos"].extend(res.get("avisos") or [])
            glb_cru = Path(res["glb"])
            m = res.get("metricas") or {}
            _registrar(jb, "forma", f"forma pronta: {m.get('triangulos')} triângulos, "
                                    f"{m.get('tempo_s')} s, VRAM pico {m.get('vram_pico_mb')} MB",
                       progresso=FAIXAS["forma"][1])
        else:
            etapa_atual = "forma"
            if not jb.get("malha_entrada"):
                raise ErroEtapa("forma", "modo so-refinar sem malha_entrada")
            glb_cru = job_dir / jb["malha_entrada"]
            if not glb_cru.is_file():
                raise ErroEtapa("forma", f"malha de entrada não encontrada: {jb['malha_entrada']}")
            _registrar(jb, None, "modo so-refinar: entrada e forma puladas", progresso=FAIXAS["forma"][1])

        # 3. refino ----------------------------------------------------------
        etapa_atual = "refino"
        _verificar_cancelado(jb)
        refinar = _modulo("refino", "refinar")
        _registrar(jb, "refino", "refinando a malha", progresso=FAIXAS["refino"][0])
        t = time.time()
        res = refinar(glb_cru, job_dir / "refino", job_dir / "saida", op,
                      imagens=imagens_motor, progresso=_Progresso(jb, job_dir, "refino"))
        tempos["refino"] = round(time.time() - t, 1)
        etapas["refino"] = res
        jb["avisos"].extend(res.get("avisos") or [])
        _verificar_cancelado(jb)

        # 4. exportar --------------------------------------------------------
        etapa_atual = "exportar"
        t = time.time()
        modelo = Path(res.get("glb") or job_dir / "saida" / "modelo.glb")
        if not base.glb_valido(modelo):
            raise ErroEtapa("exportar", f"o refino não entregou um GLB válido: {_rel(job_dir, modelo)}")
        jb["resultado"] = {
            "glb": _rel(job_dir, modelo),
            "glb_cru": _rel(job_dir, glb_cru),
            "previas": [_rel(job_dir, p) for p in res.get("previas") or []],
            "relatorio": "saida/relatorio.json",
        }
        jb["progresso"] = 100
        jb["estado"] = "concluido"
        jb["concluido_em"] = job.agora()
        tempos["exportar"] = round(time.time() - t, 3)
        _gravar_relatorio(job_dir, jb, etapas, tempos)
        job.registrar(jb, "exportar", f"concluído em {time.time() - t_job:.1f} s", salvar=False)
        _salvar(jb)
        _log(job_dir, f"=== concluído em {time.time() - t_job:.1f} s")

        # 11. arquivar (gancho; falha aqui não desfaz o job concluído) -----
        _arquivar(jb, job_dir, etapas, tempos)
    except JobCancelado:
        try:
            jb = {**jb, **job.ler_job(job_id)}
        except (OSError, ValueError):
            pass
        jb["estado"] = "cancelado"
        job.registrar(jb, etapa_atual, f"cancelado durante a etapa {etapa_atual or 'inicial'}", salvar=False)
        job.salvar_job(jb)
        _log(job_dir, f"=== cancelado na etapa {etapa_atual}")
    except Exception as e:  # noqa: BLE001 — qualquer falha vira estado "erro" legível
        etapa = getattr(e, "etapa", None) or etapa_atual or "inicial"
        _log(job_dir, f"ERRO na etapa {etapa}: {type(e).__name__}: {e}\n{traceback.format_exc()}")
        msg = str(e).strip().splitlines()[0] if str(e).strip() else type(e).__name__
        jb["estado"] = "erro"
        jb["erro"] = f"{etapa}: {msg}"[:500]
        try:
            job.registrar(jb, etapa, f"erro: {msg}"[:300], salvar=False)
            _salvar(jb)
        except JobCancelado:
            pass
        try:
            _gravar_relatorio(job_dir, jb, etapas, tempos, parcial=True)
        except Exception:  # noqa: BLE001
            pass
    return job.ler_job(job_id)


def _arquivar(jb: dict, job_dir: Path, etapas: dict, tempos: dict) -> None:
    """Etapa `arquivar` (Agente G): cópia conferida para o Drive, SEM apagar a cópia local.

    Sem o módulo, ou sem destino (OFICINA3D_ARQUIVO), só registra um aviso. Nunca muda o estado
    "concluido" do job.
    """
    try:
        mod = base.importar_opcional("oficina3d.arquivar")
    except Exception as e:  # noqa: BLE001
        mod = None
        jb["avisos"].append(f"arquivar: módulo com erro de importação ({e})")
    if mod is None or not hasattr(mod, "arquivar_job"):
        _log(job_dir, "arquivar: módulo oficina3d.arquivar ainda não disponível; etapa pulada")
        return
    t = time.time()
    try:
        r = mod.arquivar_job(job_dir, apagar_local=False)
    except Exception as e:  # noqa: BLE001
        r = {"estado": "erro", "msg": f"{type(e).__name__}: {e}"}
        _log(job_dir, f"arquivar falhou: {traceback.format_exc()}")
    tempos["arquivar"] = round(time.time() - t, 1)
    r = _jsonavel(r or {})
    etapas["arquivar"] = r
    estado = r.get("estado")
    jb.setdefault("resultado", {})["arquivo"] = {k: r.get(k) for k in ("estado", "destino", "msg") if k in r}
    if estado == "arquivado":
        job.registrar(jb, "arquivar", f"cópia conferida no Drive: {r.get('destino')}", salvar=False)
    else:
        jb["avisos"].append(f"arquivar ({estado}): {r.get('msg')}")
        job.registrar(jb, "arquivar", f"não arquivado ({estado}): {r.get('msg')}", salvar=False)
    try:
        _salvar(jb)
        if (job_dir / "saida").is_dir():
            _gravar_relatorio(job_dir, jb, etapas, tempos)   # leva o link do arquivo no relatório
    except JobCancelado:
        pass


# --------------------------------------------------------------------------- fila

def _travas():
    return base.importar_opcional("oficina3d.travas")


def _trava_worker():
    """worker.lock do Agente G (trava do SO). Sem o módulo: trava simples em JOBS\\.worker.lock."""
    t = _travas()
    if t is not None and hasattr(t, "adquirir_worker"):
        return t.adquirir_worker(timeout=0, dono=f"worker PID {os.getpid()}")
    return _trava_worker_local()


@contextlib.contextmanager
def _trava_worker_local():
    caminho = _pasta_jobs() / ".worker.lock"
    caminho.parent.mkdir(parents=True, exist_ok=True)
    eu = {"pid": os.getpid(), "criado": base.hora_criacao(os.getpid()), "desde": job.agora()}
    for _ in range(2):
        try:
            fd = os.open(caminho, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        except FileExistsError:
            try:
                dono = json.loads(caminho.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                dono = {}
            if base.processo_vivo(dono.get("pid"), dono.get("criado")):
                raise RuntimeError(f"outro worker já está rodando (PID {dono.get('pid')})")
            caminho.unlink(missing_ok=True)   # trava velha: dono morreu
            continue
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(eu, f)
        break
    else:
        raise RuntimeError("não consegui criar a trava do worker")
    try:
        yield eu
    finally:
        caminho.unlink(missing_ok=True)


def worker_ativo() -> dict | None:
    """Dono do worker.lock se houver worker vivo; senão None (para cli/web)."""
    t = _travas()
    if t is not None and hasattr(t, "estado_trava"):
        e = t.estado_trava("worker")
        return e.get("dono") if e.get("ocupada") else None
    caminho = _pasta_jobs() / ".worker.lock"
    try:
        dono = json.loads(caminho.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return dono if base.processo_vivo(dono.get("pid"), dono.get("criado")) else None


def retomar_orfaos() -> list[str]:
    """Jobs "processando" sem worker vivo voltam para "pendente" (até MAX_RETOMADAS vezes).

    Chamar só com o worker.lock na mão (então nenhum outro worker está vivo). Um job cujo
    processo dono (campo "worker") ainda vive é deixado em paz (alguém chamou processar_job direto).
    """
    mexidos = []
    for j in job.listar_jobs():
        if j.get("estado") != "processando":
            continue
        w = j.get("worker") or {}
        if w.get("pid") and w.get("pid") != os.getpid() and base.processo_vivo(w.get("pid"), w.get("criado")):
            continue

        def alterar(d: dict):
            if d.get("estado") != "processando":
                return None
            n = int(d.get("retomadas") or 0) + 1
            d["retomadas"] = n
            if n > MAX_RETOMADAS:
                d["estado"] = "erro"
                d["erro"] = (f"{d.get('etapa') or 'inicial'}: o worker caiu {n} vezes neste job; "
                             f"não retomo sozinho (reenvie se quiser)")
                job.registrar(d, d.get("etapa"), d["erro"], salvar=False)
            else:
                d.update({"estado": "pendente", "progresso": 0, "erro": None})
                job.registrar(d, None, f"worker anterior caiu na etapa {d.get('etapa') or 'inicial'}; "
                                       f"job volta para a fila (retomada {n} de {MAX_RETOMADAS})", salvar=False)
                d["etapa"] = None
            return d

        try:
            job.atualizar_job(j["id"], alterar)
            mexidos.append(j["id"])
            _log(job.pasta_job(j["id"]), "=== job órfão encontrado pelo worker (retomada)")
        except (OSError, ValueError, TimeoutError):
            continue
    return mexidos


def pendentes() -> list[str]:
    """Ids pendentes, do mais antigo para o mais novo."""
    return [j["id"] for j in job.listar_jobs() if j.get("estado") == "pendente"]


def proximo_pendente(permitidos: set[str] | None = None) -> str | None:
    for jid in pendentes():
        if permitidos is None or jid in permitidos:
            return jid
    return None


def _espaco_livre_gb() -> float:
    alvo = _pasta_jobs()
    while not alvo.exists() and alvo.parent != alvo:
        alvo = alvo.parent
    return shutil.disk_usage(alvo).free / 2**30


def _livre_min_gb() -> float:
    try:
        return float(os.environ.get("OFICINA3D_LIVRE_MIN_GB") or LIVRE_MIN_GB_PADRAO)
    except ValueError:
        return LIVRE_MIN_GB_PADRAO


def _arquivar_fila(urgente: bool = False) -> None:
    """Política do plano 5.1 (Agente G): aprovado na hora, sem nota após 3 dias, tudo se o disco apertar."""
    try:
        mod = base.importar_opcional("oficina3d.arquivar")
        if mod is not None and hasattr(mod, "arquivar_pendentes"):
            for r in mod.arquivar_pendentes(_pasta_jobs(), urgente=urgente) or []:
                if r.get("estado") not in ("sem_destino", "nada"):
                    print(f"arquivar {r.get('id')}: {r.get('estado')} — {r.get('msg')}", flush=True)
    except Exception as e:  # noqa: BLE001
        print(f"arquivar a fila falhou: {e}", flush=True)


def _gpu_livre(uma_vez: bool) -> bool:
    """Espera outro programa (jogo etc.) largar a GPU antes do próximo job (USO-01). True = pode seguir.

    Desligue com OFICINA3D_IGNORAR_GPU_OCUPADA=1 (ex.: testes, ou o Mestre quer forçar).
    """
    if os.environ.get("OFICINA3D_IGNORAR_GPU_OCUPADA") == "1":
        return True
    t = _travas()
    if t is None or not hasattr(t, "esperar_gpu_livre"):
        return True

    def ao_esperar(estado):
        print(f"GPU ocupada por outro programa: {getattr(estado, 'motivo', estado)}; aguardando", flush=True)

    return bool(t.esperar_gpu_livre(verificar_a_cada_s=60.0, max_espera_s=0 if uma_vez else None,
                                    ao_esperar=ao_esperar))


def loop(uma_vez: bool = False, intervalo: float = 2.0, apenas: list[str] | None = None) -> int:
    """Processa a fila, um job por vez. Devolve o código de saída (0 = ok, 2 = outro worker rodando).

    uma_vez: só os pendentes que já existiam ao começar; apenas: só esses ids (e sai).
    """
    with contextlib.ExitStack() as pilha:
        try:
            pilha.enter_context(_trava_worker())
        except Exception as e:  # noqa: BLE001 — TravaOcupada do Agente G ou trava local
            print(f"worker não iniciado: {e}", flush=True)
            return 2
        if base.entrar_em_job_object():
            print("worker no Job Object: se ele cair, o motor cai junto", flush=True)
        for jid in retomar_orfaos():
            print(f"job órfão retomado: {jid}", flush=True)

        if apenas:
            for jid in apenas:
                job.validar_id(jid)
            alvo = set(apenas)
            for jid in apenas:
                try:
                    estado = job.ler_job(jid).get("estado")
                except (OSError, ValueError) as e:
                    print(f"{jid}: {e}", flush=True)
                    alvo.discard(jid)
                    continue
                if estado != "pendente":
                    print(f"{jid}: está '{estado}', não 'pendente'; nada a fazer", flush=True)
                    alvo.discard(jid)
        elif uma_vez:
            alvo = set(pendentes())
        else:
            alvo = None
        sair_quando_vazio = uma_vez or bool(apenas)
        ult_arquivar = 0.0
        avisou_disco = False
        while True:
            livre = _espaco_livre_gb()
            if livre < _livre_min_gb():
                if not avisou_disco:
                    print(f"pausado: só {livre:.1f} GB livres (mínimo {_livre_min_gb():.0f} GB); arquivando", flush=True)
                    avisou_disco = True
                _arquivar_fila(urgente=True)
                if sair_quando_vazio:
                    return 3
                time.sleep(max(intervalo, 1.0) * 30)
                continue
            avisou_disco = False
            jid = proximo_pendente(alvo)
            if jid is None:
                if sair_quando_vazio:
                    break
                if time.time() - ult_arquivar >= INTERVALO_ARQUIVAR_S:
                    ult_arquivar = time.time()
                    _arquivar_fila()
                time.sleep(intervalo)
                continue
            if not _gpu_livre(sair_quando_vazio):
                if sair_quando_vazio:
                    print("GPU ocupada por outro programa; saindo sem processar", flush=True)
                    return 4
                continue
            print(f"processando {jid}", flush=True)
            final = processar_job(jid)
            print(f"{jid}: {final.get('estado')}" + (f" — {final.get('erro')}" if final.get("erro") else ""), flush=True)
            if alvo is not None:
                alvo.discard(jid)
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m oficina3d.worker", description="Worker da fila da Oficina 3D")
    ap.add_argument("--uma-vez", action="store_true", help="processa só os pendentes que já existem e sai")
    ap.add_argument("--job", action="append", metavar="ID", help="processa só este job (pode repetir) e sai")
    ap.add_argument("--intervalo", type=float, default=2.0, help="segundos entre varreduras da fila")
    a = ap.parse_args(argv)
    try:
        return loop(uma_vez=a.uma_vez, intervalo=a.intervalo, apenas=a.job)
    except KeyboardInterrupt:
        print("worker interrompido (Ctrl+C); o job em andamento volta para a fila no próximo worker", flush=True)
        return 130
    except ValueError as e:
        print(f"erro: {e}", flush=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
