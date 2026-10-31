"""Motores de forma (imagem(ns) -> malha crua) da Oficina 3D.

Contrato (docs/ARQUITETURA.md):
    listar() -> list[dict]          nome, descricao, aceita_multivista, disponivel (+ motivo, passos_padrao, ...)
    gerar(nome, imagens, opcoes, pasta, progresso=None) -> {"glb": Path, "metricas": {...}, "avisos": [...]}

Cada motor roda num SUBPROCESSO com o Python do venv dele (o processo morre no fim e devolve
toda a VRAM/RAM; versões de torch/transformers não brigam). Protocolo com o runner:
    entrada  : pasta/pedido_motor.json     (motor, imagens absolutas, opções, saída)
    saída    : pasta/resultado_motor.json  ({"ok": true, "glb": ..., "metricas": {...}} ou {"ok": false, "erro": ...})
    log      : pasta/motor.log             (stdout + stderr do runner, bytes crus)
    progresso: linhas "PROGRESSO <0-100> <mensagem>" no stdout (podem vir coladas na barra do tqdm).

Segurança da GPU:
  * `oficina3d.travas.adquirir_gpu()` (Agente G) em volta do subprocesso — um motor por vez no PC;
  * o subprocesso entra num Job Object (KILL_ON_JOB_CLOSE): cancelar/timeout mata a árvore inteira.

Cancelamento: se o callback `progresso` levantar exceção (ex.: o worker viu o job cancelado),
o subprocesso é encerrado e a exceção sobe para quem chamou. O callback é chamado também a cada
~3 s sem linha nova (batimento), para o worker poder conferir o cancelamento durante a carga.
"""
from __future__ import annotations

import contextlib
import json
import os
import queue
import re
import shutil
import subprocess
import threading
import time
from pathlib import Path
from typing import Callable

from . import base

PASTA_RUNNERS = Path(__file__).resolve().parent
RE_PROGRESSO = re.compile(r"PROGRESSO\s+(\d{1,3})\s*([^\r\n]*)")
INTERVALO_BATIMENTO_S = 3.0
TEMPO_MAX_PADRAO_S = 7200          # 2 h: o 2mv normal levou 38 min na 1660S
VISTAS_MV_PADRAO = {"frente": "front", "costas": "back", "esquerda": "left", "direita": "right"}

Progresso = Callable[[int, str], None]


class ErroMotor(RuntimeError):
    """Falha do motor (subprocesso), com o fim do motor.log na mensagem."""


# --------------------------------------------------------------------------- catálogo
# "repo"/"subpasta": pesos do Hunyuan (HY3DGEN_MODELS\<repo>\<subpasta>\model.fp16.safetensors
# ou cache do Hugging Face). "vae_turbo": VAE que o enable_flashvdm(replace_vae=True) carrega.
MOTORES: dict[str, dict] = {
    "hunyuan-mv-turbo": {
        "descricao": "Hunyuan3D-2mv turbo (1,1B destilado), 5 passos + FlashVDM, 2-4 vistas "
                     "frente/costas/esquerda/direita (PADRÃO multivista; v1: 6 min na 1660S)",
        "tipo": "hunyuan", "repo": "tencent/Hunyuan3D-2mv", "subpasta": "hunyuan3d-dit-v2-mv-turbo",
        "vae_turbo": ("tencent/Hunyuan3D-2", "hunyuan3d-vae-v2-0-turbo"),
        "passos": 5, "aceita_multivista": True, "vistas_recomendadas": (2, 4), "forcar_flashvdm": True,
        "licenca": "Tencent Hunyuan Community (uso liberado, inclusive no resultado final — RF-03 final, 31/10/2026)",
    },
    "hunyuan-mini-turbo": {
        "descricao": "Hunyuan3D-2mini turbo (0,6B destilado), 5 passos + FlashVDM, 1 imagem "
                     "(PADRÃO 1 vista; v1: ~4 min na 1660S)",
        "tipo": "hunyuan", "repo": "tencent/Hunyuan3D-2mini", "subpasta": "hunyuan3d-dit-v2-mini-turbo",
        "vae_turbo": ("tencent/Hunyuan3D-2mini", "hunyuan3d-vae-v2-mini-turbo"),
        "passos": 5, "aceita_multivista": False, "forcar_flashvdm": True,
        "licenca": "Tencent Hunyuan Community (uso liberado, inclusive no resultado final — RF-03 final, 31/10/2026)",
    },
    "hunyuan-mini": {
        "descricao": "Hunyuan3D-2mini (0,6B), 30 passos, 1 imagem (v1: ~3,6 min com FlashVDM na 1660S)",
        "tipo": "hunyuan", "repo": "tencent/Hunyuan3D-2mini", "subpasta": "hunyuan3d-dit-v2-mini",
        "vae_turbo": ("tencent/Hunyuan3D-2mini", "hunyuan3d-vae-v2-mini-turbo"),
        "passos": 30, "aceita_multivista": False,
        "licenca": "Tencent Hunyuan Community (uso liberado, inclusive no resultado final — RF-03 final, 31/10/2026)",
    },
    "hunyuan-mv": {
        "descricao": "Hunyuan3D-2mv (1,1B), 30 passos, 1-4 vistas frente/costas/esquerda/direita "
                     "(lento: ~38 min com 4 vistas na 1660S)",
        "tipo": "hunyuan", "repo": "tencent/Hunyuan3D-2mv", "subpasta": "hunyuan3d-dit-v2-mv",
        "vae_turbo": ("tencent/Hunyuan3D-2", "hunyuan3d-vae-v2-0-turbo"),
        "passos": 30, "aceita_multivista": True, "vistas_recomendadas": (2, 4),
        "licenca": "Tencent Hunyuan Community (uso liberado, inclusive no resultado final — RF-03 final, 31/10/2026)",
    },
    "triposr": {
        "descricao": "TripoSR (MIT), 1 imagem, com cor de vértice (~1 min, forma simples)",
        "tipo": "triposr", "passos": None, "aceita_multivista": False,
        "licenca": "MIT",
    },
}

PADRAO_1_VISTA = "hunyuan-mini-turbo"
PADRAO_MULTIVISTA = "hunyuan-mv-turbo"


# --------------------------------------------------------------------------- caminhos de cada tipo

def _python_do_tipo(tipo: str) -> Path:
    b = base.base()
    if tipo == "hunyuan":
        return Path(base.cfg("PY_HUNYUAN") or b / ".venv_hunyuan" / "Scripts" / "python.exe")
    if tipo == "triposr":
        return Path(base.cfg("PY_TRIPOSR") or b / ".venv_triposr" / "Scripts" / "python.exe")
    raise ValueError(f"tipo de motor sem Python conhecido: {tipo}")


def _repo_do_tipo(tipo: str) -> Path:
    b = base.base()
    if tipo == "hunyuan":
        return Path(base.cfg("MOTOR_HUNYUAN") or b / "motores" / "Hunyuan3D-2GP")
    if tipo == "triposr":
        return Path(base.cfg("MOTOR_TRIPOSR") or b / "motores" / "TripoSR")
    raise ValueError(f"tipo de motor sem repositório conhecido: {tipo}")


def _caminhos(spec: dict) -> dict:
    """python, runner e cwd do motor (o catálogo pode trazer os três prontos, ex.: motor falso dos testes)."""
    tipo = spec.get("tipo")
    python = Path(spec["python"]) if spec.get("python") else _python_do_tipo(tipo)
    runner = Path(spec["runner"]) if spec.get("runner") else PASTA_RUNNERS / f"_runner_{tipo}.py"
    cwd = Path(spec["cwd"]) if spec.get("cwd") else _repo_do_tipo(tipo)
    return {"python": python, "runner": runner, "cwd": cwd}


def _pastas_modelos() -> tuple[Path | None, Path | None]:
    """(HY3DGEN_MODELS, HF_HOME) como o subprocesso vai ver."""
    try:
        env = base.env_motor()
    except Exception:
        env = dict(os.environ)
    hy = env.get("HY3DGEN_MODELS")
    hf = env.get("HF_HOME")
    return (Path(hy) if hy else None, Path(hf) if hf else None)


def _achar_peso(repo: str, caminho_rel: str) -> Path | None:
    """Acha `<repo>/<caminho_rel>` em HY3DGEN_MODELS ou no cache do Hugging Face (hub/models--a--b/snapshots/*)."""
    hy, hf = _pastas_modelos()
    if hy:
        p = hy / Path(repo) / Path(caminho_rel)
        if p.is_file():
            return p
    if hf:
        snaps = hf / "hub" / ("models--" + repo.replace("/", "--")) / "snapshots"
        if snaps.is_dir():
            for s in sorted(snaps.iterdir(), reverse=True):
                p = s / Path(caminho_rel)
                if p.is_file():
                    return p
    return None


def _pesos_necessarios(spec: dict, flashvdm: bool) -> list[tuple[str, str]]:
    """Lista de (repo, arquivo relativo) que o motor precisa; motor falso usa spec['pesos'] (caminhos)."""
    tipo = spec.get("tipo")
    if tipo == "hunyuan":
        # config.yaml TAMBEM e obrigatorio: sem ele o motor morre ao carregar
        # (prova viva do hunyuan-mini em 31/10/2026 — o verificador nao cobrava
        # e o motor constava "disponivel" sem conseguir rodar).
        req = [(spec["repo"], f"{spec['subpasta']}/model.fp16.safetensors"),
               (spec["repo"], f"{spec['subpasta']}/config.yaml")]
        if flashvdm and spec.get("vae_turbo"):
            r, s = spec["vae_turbo"]
            req.append((r, f"{s}/model.fp16.safetensors"))
        return req
    if tipo == "triposr":
        return [("stabilityai/TripoSR", "model.ckpt"), ("stabilityai/TripoSR", "config.yaml")]
    return []


def _usa_flashvdm(spec: dict, opcoes: dict | None) -> bool:
    if spec.get("tipo") != "hunyuan":
        return False
    if spec.get("forcar_flashvdm"):
        return True
    v = (opcoes or {}).get("flashvdm")
    return True if v is None else bool(v)


def _verificar(spec: dict, flashvdm: bool) -> tuple[bool, str]:
    """(disponivel, motivo). Disponível = Python do venv, runner, repositório e pesos presentes."""
    try:
        c = _caminhos(spec)
    except ValueError as e:
        return False, str(e)
    if not c["python"].is_file():
        return False, f"Python do motor não encontrado: {c['python']}"
    if not c["runner"].is_file():
        return False, f"runner não encontrado: {c['runner']}"
    if not c["cwd"].is_dir():
        return False, f"pasta do motor não encontrada: {c['cwd']}"
    faltam = [p for p in spec.get("pesos", []) if not Path(p).exists()]
    faltam += [f"{r}/{a}" for r, a in _pesos_necessarios(spec, flashvdm) if _achar_peso(r, a) is None]
    if faltam:
        return False, "pesos ausentes: " + ", ".join(str(f) for f in faltam)
    return True, ""


# --------------------------------------------------------------------------- API pública

def listar() -> list[dict]:
    """Motores conhecidos, com `disponivel` (venv + pesos presentes) e `motivo` quando não estiver."""
    saida = []
    for nome, spec in MOTORES.items():
        ok, motivo = _verificar(spec, _usa_flashvdm(spec, None))
        vr = spec.get("vistas_recomendadas")
        saida.append({
            "nome": nome,
            "descricao": spec.get("descricao", ""),
            "aceita_multivista": bool(spec.get("aceita_multivista")),
            "disponivel": ok,
            "motivo": motivo,
            "passos_padrao": spec.get("passos"),
            "flashvdm": _usa_flashvdm(spec, None),
            "vistas": f"{vr[0]}-{vr[1]}" if vr else "1",
            "licenca": spec.get("licenca", ""),
            "padrao": nome in (PADRAO_1_VISTA, PADRAO_MULTIVISTA),
        })
    return saida


def _mapa_mv() -> dict:
    return dict(base.cfg("VISTAS_MV_HUNYUAN") or VISTAS_MV_PADRAO)


def _escolher_imagens(spec: dict, imagens: list[dict]) -> tuple[list[dict], list[str]]:
    """Imagens que o motor vai receber ({"caminho", "vista", "vista_motor"}) + avisos."""
    avisos: list[str] = []
    lista = []
    for im in imagens or []:
        caminho = Path(im.get("arquivo") or im.get("caminho") or "")
        if not caminho.is_absolute():
            raise ValueError(f"motores.gerar precisa de caminhos ABSOLUTOS: {caminho}")
        if not caminho.is_file():
            raise FileNotFoundError(f"imagem não encontrada: {caminho}")
        lista.append({"caminho": str(caminho), "vista": im.get("vista")})
    if not lista:
        raise ValueError("nenhuma imagem para o motor")

    if spec.get("aceita_multivista"):
        mapa = _mapa_mv()
        if len(lista) == 1 and not lista[0]["vista"]:
            lista[0]["vista"] = "frente"
        escolhidas, usadas = [], set()
        for im in lista:
            vm = mapa.get(im["vista"] or "")
            if vm and vm not in usadas:
                usadas.add(vm)
                escolhidas.append({**im, "vista_motor": vm})
        ignoradas = [im["vista"] or Path(im["caminho"]).name for im in lista
                     if not any(e["caminho"] == im["caminho"] for e in escolhidas)]
        if ignoradas:
            avisos.append("vistas que o motor multivista não usa (servem para refino/cor): " + ", ".join(ignoradas))
        if not escolhidas:
            raise ValueError("motor multivista precisa de pelo menos uma vista frente/costas/esquerda/direita")
        vr = spec.get("vistas_recomendadas")
        if vr and len(escolhidas) < vr[0]:
            avisos.append(f"só {len(escolhidas)} vista(s) para o motor multivista (recomendado {vr[0]}-{vr[1]})")
        return escolhidas, avisos

    frente = [im for im in lista if im["vista"] == "frente"]
    escolhida = frente[0] if frente else lista[0]
    if not frente and len(lista) > 1:
        avisos.append(f"nenhuma vista 'frente'; o motor de 1 imagem usou {Path(escolhida['caminho']).name}")
    if len(lista) > 1:
        avisos.append(f"motor de 1 imagem: {len(lista) - 1} imagem(ns) extra(s) não entram na forma")
    return [{**escolhida, "vista_motor": "frente"}], avisos


def _montar_pedido(nome: str, spec: dict, imagens: list[dict], opcoes: dict, pasta: Path) -> tuple[dict, list[str]]:
    escolhidas, avisos = _escolher_imagens(spec, imagens)
    op = dict(opcoes or {})
    flashvdm = _usa_flashvdm(spec, op)
    if (spec.get("tipo") == "hunyuan" and flashvdm and not spec.get("forcar_flashvdm")
            and spec.get("vae_turbo") and _achar_peso(spec["vae_turbo"][0], f"{spec['vae_turbo'][1]}/model.fp16.safetensors") is None):
        flashvdm = False
        avisos.append("FlashVDM desligado: VAE turbo ausente (fica bem mais lento)")
    pedido = {
        "motor": nome,
        "tipo": spec.get("tipo"),
        "imagens": escolhidas,
        "saida_glb": str(pasta / "forma.glb"),
        "resultado": str(pasta / "resultado_motor.json"),
        "repo_motor": str(_caminhos(spec)["cwd"]),
        "passos": int(op.get("passos") or spec.get("passos") or 0) or None,
        "seed": int(op["seed"]) if op.get("seed") is not None else 1234,
        "octree": int(op.get("octree") or 256),
    }
    if spec.get("tipo") == "hunyuan":
        pedido.update({
            "repo": spec["repo"], "subpasta": spec["subpasta"],
            "multivista": bool(spec.get("aceita_multivista")),
            "flashvdm": flashvdm, "mc_algo": op.get("mc_algo") or "mc",   # 'dmc' exige o diso (compilar)
            "perfil_mmgp": int(op.get("perfil_mmgp") or 4),
            "orcamento_mb": int(op.get("orcamento_mb") or 2200),
            "chunks": int(op.get("chunks") or 8000),
            "guidance": float(op.get("guidance") or 5.0),
        })
    elif spec.get("tipo") == "triposr":
        pedido.update({
            "pesos": op.get("pesos_triposr") or "stabilityai/TripoSR",
            "mc_resolucao": int(op.get("mc_resolucao") or 256),
            "chunk": int(op.get("chunk_triposr") or 8192),
            "proporcao_frente": float(op.get("proporcao_frente") or 0.85),
        })
    else:
        # motor falso/experimental: repassa as opções do job tal como vieram
        pedido["opcoes"] = op
    return pedido, avisos


def _travas():
    return base.importar_opcional("oficina3d.travas")


def _trava_gpu(spec: dict, nome: str):
    """Context manager do gpu.lock (Agente G; espera a GPU ficar livre). Sem o módulo: segue sem trava."""
    if not spec.get("usa_gpu", True):
        return contextlib.nullcontext()
    t = _travas()
    if t is None or not hasattr(t, "adquirir_gpu"):
        return contextlib.nullcontext()
    return t.adquirir_gpu(timeout=None, dono=f"motor {nome} (PID {os.getpid()})")


class _AmostradorVram(threading.Thread):
    """Régua única de VRAM (E12): pico de memory.used do nvidia-smi durante o motor."""

    def __init__(self, intervalo: float = 1.0):
        super().__init__(daemon=True)
        self.exe = shutil.which("nvidia-smi")
        self.intervalo = intervalo
        self.parar = threading.Event()
        self.base_mb: int | None = None
        self.pico_mb: int | None = None

    def _ler(self) -> int | None:
        try:
            r = subprocess.run([self.exe, "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                               capture_output=True, text=True, timeout=10,
                               creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))
            return int(r.stdout.strip().splitlines()[0])
        except Exception:
            return None

    def run(self):
        if not self.exe:
            return
        self.base_mb = self._ler()
        while not self.parar.is_set():
            v = self._ler()
            if v is not None:
                self.pico_mb = v if self.pico_mb is None else max(self.pico_mb, v)
            self.parar.wait(self.intervalo)


def _ler_saida(proc: subprocess.Popen, log_f, fila: "queue.Queue") -> None:
    """Thread: copia stdout+stderr crus para motor.log e manda (pct, msg) de cada PROGRESSO para a fila."""
    resto = b""
    try:
        for bloco in iter(lambda: proc.stdout.read1(4096), b""):
            log_f.write(bloco)
            log_f.flush()
            resto += bloco
            partes = re.split(rb"[\r\n]", resto)
            resto = partes.pop()
            for linha in partes:
                _empurrar(linha, fila)
        if resto:
            _empurrar(resto, fila)
    finally:
        fila.put(None)


def _empurrar(linha: bytes, fila: "queue.Queue") -> None:
    texto = linha.decode("utf-8", errors="replace")
    for m in RE_PROGRESSO.finditer(texto):
        fila.put((max(0, min(100, int(m.group(1)))), m.group(2).strip()))


def _fim_do_log(log: Path, n: int = 15) -> str:
    try:
        texto = log.read_bytes()[-8000:].decode("utf-8", errors="replace")
    except OSError:
        return ""
    linhas = [ln.strip() for ln in re.split(r"[\r\n]+", texto) if ln.strip()]
    return "\n".join(linhas[-n:])


def gerar(nome: str, imagens: list[dict], opcoes: dict, pasta: Path, progresso: Progresso | None = None) -> dict:
    """Gera `pasta/forma.glb` com o motor `nome`. Imagens com caminhos ABSOLUTOS ({"arquivo"|"caminho", "vista"}).

    Devolve {"glb": Path, "metricas": {tempo_s, vram_pico_mb, triangulos, vertices, fechada, ...}, "avisos": [...]}.
    Opções extras aceitas (além das do job): tempo_max_s, perfil_mmgp, orcamento_mb, chunks, guidance,
    mc_algo (Hunyuan); mc_resolucao, chunk_triposr, proporcao_frente (TripoSR); medir_vram (bool).
    """
    if nome not in MOTORES:
        raise ValueError(f"motor desconhecido: {nome} (conhecidos: {', '.join(MOTORES)})")
    spec = MOTORES[nome]
    op = dict(opcoes or {})
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)

    pedido, avisos = _montar_pedido(nome, spec, imagens, op, pasta)
    ok, motivo = _verificar(spec, bool(pedido.get("flashvdm")))
    if not ok:
        raise ErroMotor(f"motor {nome} indisponível: {motivo}")
    c = _caminhos(spec)

    arq_pedido = pasta / "pedido_motor.json"
    arq_resultado = Path(pedido["resultado"])
    arq_glb = Path(pedido["saida_glb"])
    log = pasta / "motor.log"
    for velho in (arq_resultado, arq_glb):
        if velho.exists():
            velho.unlink()
    arq_pedido.write_text(json.dumps(pedido, ensure_ascii=False, indent=2), encoding="utf-8")

    env = base.env_motor({"HF_HUB_OFFLINE": "1", **(spec.get("env") or {})})
    tempo_max = float(op.get("tempo_max_s") or spec.get("tempo_max_s") or TEMPO_MAX_PADRAO_S)
    medir = op.get("medir_vram", spec.get("usa_gpu", True))
    amostrador = _AmostradorVram() if medir else None

    def avisar(pct: int, msg: str) -> None:
        if progresso is not None:
            progresso(pct, msg)

    with _trava_gpu(spec, nome), open(log, "ab") as log_f:
        log_f.write(f"\n=== motor {nome} | {time.strftime('%Y-%m-%d %H:%M:%S')} | {c['python']} {c['runner'].name}\n".encode("utf-8"))
        log_f.flush()
        avisar(0, f"iniciando motor {nome}")
        if amostrador:
            amostrador.start()
        t0 = time.time()
        proc = subprocess.Popen(
            [str(c["python"]), "-u", str(c["runner"]), str(arq_pedido)],
            cwd=str(c["cwd"]), env=env, stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        jo = None
        try:
            jo = base.JobObject()
            if not jo.adicionar(proc):
                jo.fechar()
                jo = None
        except OSError:
            jo = None
        fila: queue.Queue = queue.Queue()
        leitor = threading.Thread(target=_ler_saida, args=(proc, log_f, fila), daemon=True)
        leitor.start()
        ult = (0, f"iniciando motor {nome}")
        ult_aviso = time.time()
        try:
            terminou_leitura = False
            saiu_em = None
            while not terminou_leitura:
                try:
                    item = fila.get(timeout=0.5)
                except queue.Empty:
                    item = False
                if item is None:
                    terminou_leitura = True
                elif item:
                    ult = item
                    ult_aviso = time.time()
                    avisar(*item)
                if time.time() - ult_aviso >= INTERVALO_BATIMENTO_S:
                    ult_aviso = time.time()
                    avisar(*ult)          # batimento: deixa o worker conferir o cancelamento
                if time.time() - t0 > tempo_max:
                    raise ErroMotor(f"motor {nome} passou do tempo máximo ({tempo_max:.0f} s) e foi encerrado")
                if not terminou_leitura and proc.poll() is not None:
                    # O runner saiu, mas um neto pode segurar o pipe aberto: espera 5 s e mata a sobra.
                    saiu_em = saiu_em or time.time()
                    if time.time() - saiu_em > 5:
                        if jo is not None:
                            jo.encerrar(0)
                        leitor.join(timeout=5)
                        break
            proc.wait()
        except BaseException:
            base.encerrar_arvore(proc, jo)
            leitor.join(timeout=5)
            raise
        finally:
            if amostrador:
                amostrador.parar.set()
            if jo is not None:
                jo.fechar()   # KILL_ON_JOB_CLOSE: netos que sobraram morrem aqui
        tempo_processo = time.time() - t0
        log_f.write(f"\n=== fim: código {proc.returncode}, {tempo_processo:.1f} s\n".encode("utf-8"))

    resultado = None
    if arq_resultado.is_file():
        try:
            resultado = json.loads(arq_resultado.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            resultado = None
    if not resultado or not resultado.get("ok"):
        erro = (resultado or {}).get("erro") or f"o motor saiu com código {proc.returncode} sem resultado"
        raise ErroMotor(f"{nome}: {erro}\n--- fim do motor.log ---\n{_fim_do_log(log)}")
    if not base.glb_valido(arq_glb):
        raise ErroMotor(f"{nome}: forma.glb ausente ou inválido (cabeçalho glTF)\n{_fim_do_log(log)}")

    metricas = dict(resultado.get("metricas") or {})
    metricas.setdefault("tempo_s", round(tempo_processo, 1))
    metricas["tempo_processo_s"] = round(tempo_processo, 1)
    if "vram_pico_mb" in metricas:
        metricas["vram_pico_torch_mb"] = metricas.pop("vram_pico_mb")
    metricas["vram_pico_mb"] = amostrador.pico_mb if amostrador else None
    metricas["vram_base_mb"] = amostrador.base_mb if amostrador else None
    metricas["vram_regua"] = "nvidia-smi memory.used (GPU inteira)"
    if metricas["vram_pico_mb"] is None:
        metricas["vram_pico_mb"] = metricas.get("vram_pico_torch_mb")
        metricas["vram_regua"] = "torch.cuda.max_memory_allocated (nvidia-smi indisponível)"
    metricas["bytes_glb"] = arq_glb.stat().st_size
    avisos += list(resultado.get("avisos") or [])
    avisar(100, "forma pronta")
    return {"glb": arq_glb, "metricas": metricas, "avisos": avisos, "motor": nome}
