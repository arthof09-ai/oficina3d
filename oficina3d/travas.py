"""Travas entre processos (gpu.lock, worker.lock) e leitura da GPU.

Plano v2, E9: a GPU é coordenada por um `gpu.lock` exclusivo (runners, testes e
worker), e não por "olhar o nvidia-smi". Este módulo também diz se OUTRO
programa (um jogo, por exemplo) está usando a GPU, para o worker pausar: o PC
é de outra pessoa e a Oficina não pode atrapalhar.

Como a trava funciona (Windows):
- o arquivo `BASE\\locks\\<nome>.lock` é aberto e um byte bem além do fim do
  arquivo é travado com `msvcrt.locking` (LockFile do Windows). A trava é do
  sistema operacional: se o processo morrer (até por "Finalizar tarefa"), o
  Windows a solta sozinho. Não existe trava presa para sempre.
- o conteúdo do arquivo (byte 0 em diante, fora da região travada) guarda quem
  tem a trava: PID, horário de criação do processo, desde quando e uma
  descrição. Serve para diagnóstico (`saude`) e para detectar
  trava órfã: registro presente + trava livre = o dono morreu sem soltar.
- PID + horário de criação evitam confundir um PID reaproveitado pelo Windows.

Uso:
    from oficina3d import travas
    with travas.adquirir_worker():              # um worker só por vez
        while True:
            if travas.gpu_ocupada_por_outros():
                ...  # pausa
            with travas.adquirir_gpu(timeout=600, dono="job 2026..."):
                ...  # roda o motor

Observação: a trava NÃO é reentrante. No mesmo processo, pedir a mesma trava
duas vezes falha (o segundo pedido espera/estoura o timeout).
"""
from __future__ import annotations

import ctypes
import json
import logging
import os
import shutil
import statistics
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import asdict, dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Callable, Iterator

log = logging.getLogger("oficina3d.travas")

_WINDOWS = sys.platform == "win32"
if _WINDOWS:
    import msvcrt
else:  # pragma: no cover - o app roda no Windows; isto é só para não quebrar em outro SO
    import fcntl

# Byte travado: bem além do conteúdo, para leitores poderem ler o registro.
_OFFSET_TRAVA = 1 << 30
_CREATE_NO_WINDOW = 0x08000000
_INTERVALO_TENTATIVA_S = 0.25


# --------------------------------------------------------------------------- caminhos

def caminho_config(nome: str) -> Path:
    """Lê um caminho de `oficina3d.config` (BASE, JOBS, LOCKS, CACHE), com reserva.

    O config.py é de outro agente; se ainda não existir ou não tiver o nome,
    usa as variáveis OFICINA3D_BASE / OFICINA3D_JOBS ou a pasta acima de `app\\`.
    """
    try:
        from oficina3d import config  # noqa: WPS433 (import tardio de propósito)
        valor = getattr(config, nome, None)
        if valor:
            return Path(valor)
    except Exception:  # config ausente ou com erro: segue com a reserva
        pass
    base_env = os.environ.get("OFICINA3D_BASE")
    base = Path(base_env) if base_env else Path(__file__).resolve().parents[2]
    if nome == "BASE":
        return base
    if nome == "JOBS":
        return Path(os.environ.get("OFICINA3D_JOBS") or base / "jobs")
    if nome == "LOCKS":
        return caminho_config("BASE") / "locks"
    if nome == "CACHE":
        return caminho_config("BASE") / "_cache"
    raise KeyError(nome)


def pasta_travas() -> Path:
    return caminho_config("LOCKS")


# --------------------------------------------------------------------------- processos (ctypes, sem psutil)

def _tempo_criacao(pid: int) -> tuple[bool, int | None]:
    """(vivo, horário de criação em FILETIME) do processo `pid`.

    Sem permissão para abrir o processo (de outro usuário) → vivo=True, None.
    """
    if pid <= 0:
        return False, None
    if not _WINDOWS:  # pragma: no cover
        try:
            os.kill(pid, 0)
            return True, None
        except OSError:
            return False, None
    k32 = ctypes.WinDLL("kernel32", use_last_error=True)
    k32.OpenProcess.restype = ctypes.c_void_p
    k32.OpenProcess.argtypes = [ctypes.c_uint32, ctypes.c_int, ctypes.c_uint32]
    k32.CloseHandle.argtypes = [ctypes.c_void_p]
    k32.GetExitCodeProcess.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32)]
    k32.GetProcessTimes.argtypes = [ctypes.c_void_p] + [ctypes.POINTER(ctypes.c_uint64)] * 4
    PROCESS_QUERY_LIMITED_INFORMATION = 0x1000
    STILL_ACTIVE = 259
    h = k32.OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, 0, pid)
    if not h:
        erro = ctypes.get_last_error()
        return (erro == 5), None  # 5 = acesso negado: existe, mas não é nosso
    try:
        codigo = ctypes.c_uint32()
        if k32.GetExitCodeProcess(h, ctypes.byref(codigo)) and codigo.value != STILL_ACTIVE:
            return False, None
        c, e, k, u = (ctypes.c_uint64() for _ in range(4))
        if k32.GetProcessTimes(h, ctypes.byref(c), ctypes.byref(e), ctypes.byref(k), ctypes.byref(u)):
            return True, int(c.value)
        return True, None
    finally:
        k32.CloseHandle(h)


def processo_vivo(pid: int, criado_em: int | None = None) -> bool:
    """True se o PID existe E (quando informado) tem o mesmo horário de criação."""
    vivo, criado = _tempo_criacao(int(pid))
    if not vivo:
        return False
    if criado_em is not None and criado is not None and int(criado_em) != criado:
        return False  # PID reaproveitado por outro processo
    return True


# --------------------------------------------------------------------------- trava

class TravaOcupada(Exception):
    """A trava está com outro processo (e o timeout acabou)."""

    def __init__(self, nome: str, dono: dict | None):
        self.nome = nome
        self.dono = dono or {}
        quem = f"PID {self.dono.get('pid')}" if self.dono.get("pid") else "outro processo"
        desc = f" ({self.dono['dono']})" if self.dono.get("dono") else ""
        super().__init__(f"trava '{nome}' ocupada por {quem}{desc}")


def _ler_registro(caminho: Path) -> dict | None:
    try:
        bruto = caminho.read_bytes()
    except OSError:
        return None
    bruto = bruto.split(b"\0", 1)[0].strip()
    if not bruto:
        return None
    try:
        dado = json.loads(bruto.decode("utf-8"))
        return dado if isinstance(dado, dict) else None
    except (ValueError, UnicodeDecodeError):
        return {"ilegivel": True}


class Trava:
    """Trava exclusiva entre processos sobre `<pasta>\\<nome>.lock`."""

    def __init__(self, nome: str, pasta: Path | str | None = None):
        self.nome = nome
        self.pasta = Path(pasta) if pasta else pasta_travas()
        self.caminho = self.pasta / f"{nome}.lock"
        self._arq = None
        self.info: dict = {}

    # -- baixo nível
    def _abrir(self):
        self.pasta.mkdir(parents=True, exist_ok=True)
        flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOINHERIT", 0)
        fd = os.open(self.caminho, flags, 0o644)
        return os.fdopen(fd, "r+b", buffering=0)

    @staticmethod
    def _travar(arq) -> bool:
        arq.seek(_OFFSET_TRAVA)
        try:
            if _WINDOWS:
                msvcrt.locking(arq.fileno(), msvcrt.LK_NBLCK, 1)
            else:  # pragma: no cover
                fcntl.flock(arq.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except OSError:
            return False

    @staticmethod
    def _destravar(arq) -> None:
        arq.seek(_OFFSET_TRAVA)
        if _WINDOWS:
            msvcrt.locking(arq.fileno(), msvcrt.LK_UNLCK, 1)
        else:  # pragma: no cover
            fcntl.flock(arq.fileno(), fcntl.LOCK_UN)

    # -- API
    @property
    def presa(self) -> bool:
        return self._arq is not None

    def adquirir(self, timeout: float | None = None, dono: str = "") -> dict:
        """Pega a trava. timeout=None espera para sempre; 0 tenta só uma vez (com
        uma tolerância curta de ~0,5 s). Estourou → TravaOcupada."""
        if self._arq is not None:
            raise RuntimeError(f"trava '{self.nome}' já está presa por este objeto")
        limite = None if timeout is None else time.monotonic() + max(0.5, float(timeout))
        arq = self._abrir()
        try:
            while True:
                if self._travar(arq):
                    break
                if limite is not None and time.monotonic() >= limite:
                    raise TravaOcupada(self.nome, _ler_registro(self.caminho))
                time.sleep(_INTERVALO_TENTATIVA_S)
        except BaseException:
            arq.close()
            raise
        # Temos a trava. Registro anterior presente = dono morreu sem soltar (órfã).
        anterior = _ler_registro(self.caminho)
        orfa = None
        if anterior:
            orfa = anterior
            log.warning("trava '%s' órfã (PID %s morreu sem soltar); assumida pelo PID %s",
                        self.nome, anterior.get("pid"), os.getpid())
        _, criado = _tempo_criacao(os.getpid())
        self.info = {
            "nome": self.nome,
            "pid": os.getpid(),
            "criado_em_processo": criado,
            "desde": datetime.now().astimezone().isoformat(timespec="seconds"),
            "dono": dono,
        }
        dados = json.dumps(self.info, ensure_ascii=False).encode("utf-8")
        arq.seek(0)
        arq.truncate()
        arq.write(dados)
        try:
            os.fsync(arq.fileno())
        except OSError:
            pass
        self._arq = arq
        if orfa:
            self.info = dict(self.info, orfa_anterior=orfa)
        return self.info

    def soltar(self) -> None:
        arq, self._arq = self._arq, None
        if arq is None:
            return
        try:
            arq.seek(0)
            arq.truncate()  # registro vazio = saída limpa (não é órfã)
        except OSError:
            pass
        try:
            self._destravar(arq)
        except OSError:
            pass
        finally:
            arq.close()

    def __enter__(self) -> dict:
        return self.adquirir()

    def __exit__(self, *exc) -> None:
        self.soltar()


@contextmanager
def adquirir_gpu(timeout: float | None = None, dono: str = "",
                 pasta: Path | str | None = None) -> Iterator[dict]:
    """Context manager do gpu.lock. Espera até `timeout` segundos (None = sempre)."""
    t = Trava("gpu", pasta)
    info = t.adquirir(timeout=timeout, dono=dono)
    try:
        yield info
    finally:
        t.soltar()


@contextmanager
def adquirir_worker(timeout: float | None = 0, dono: str = "worker",
                    pasta: Path | str | None = None) -> Iterator[dict]:
    """Context manager do worker.lock: garante um worker só. Por padrão não espera
    (outro worker rodando → TravaOcupada na hora)."""
    t = Trava("worker", pasta)
    info = t.adquirir(timeout=timeout, dono=dono)
    try:
        yield info
    finally:
        t.soltar()


def estado_trava(nome: str, pasta: Path | str | None = None) -> dict:
    """Diz se a trava está livre, ocupada (e por quem) ou órfã. Não espera.

    Atenção: para testar, toma a trava por um instante quando ela está livre.
    """
    t = Trava(nome, pasta)
    registro = _ler_registro(t.caminho) if t.caminho.exists() else None
    estado = {"nome": nome, "caminho": str(t.caminho), "ocupada": False, "orfa": False, "dono": registro}
    if not t.caminho.exists():
        return estado
    try:
        arq = t._abrir()
    except OSError as e:
        estado["erro"] = str(e)
        return estado
    try:
        if t._travar(arq):
            t._destravar(arq)
            if registro:
                estado["orfa"] = True
                pid = registro.get("pid")
                estado["dono_vivo"] = bool(pid) and processo_vivo(pid, registro.get("criado_em_processo"))
        else:
            estado["ocupada"] = True
            pid = (registro or {}).get("pid")
            if pid:
                estado["dono_vivo"] = processo_vivo(pid, registro.get("criado_em_processo"))
    finally:
        arq.close()
    return estado


def estado_travas(pasta: Path | str | None = None) -> dict:
    return {n: estado_trava(n, pasta) for n in ("gpu", "worker")}


# --------------------------------------------------------------------------- GPU (nvidia-smi)

def _nvidia_smi() -> str | None:
    achado = shutil.which("nvidia-smi")
    if achado:
        return achado
    padrao = Path(os.environ.get("SystemRoot", r"C:\Windows")) / "System32" / "nvidia-smi.exe"
    return str(padrao) if padrao.exists() else None


def _rodar_smi(args: list[str], timeout: float = 15) -> str:
    exe = _nvidia_smi()
    if not exe:
        raise RuntimeError("nvidia-smi não encontrado")
    r = subprocess.run([exe, *args], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", timeout=timeout,
                       creationflags=_CREATE_NO_WINDOW if _WINDOWS else 0)
    if r.returncode != 0:
        raise RuntimeError(f"nvidia-smi saiu com {r.returncode}: {(r.stderr or r.stdout).strip()[:200]}")
    return r.stdout


def _num(texto: str) -> float | None:
    texto = texto.strip()
    try:
        return float(texto)
    except ValueError:
        return None  # "[N/A]", "[Insufficient Permissions]"...


def interpretar_query_gpu(saida: str) -> dict:
    """Primeira GPU de `--query-gpu=name,driver_version,memory.total,memory.used,
    memory.free,utilization.gpu --format=csv,noheader,nounits`."""
    for linha in saida.splitlines():
        partes = [p.strip() for p in linha.split(",")]
        if len(partes) >= 6:
            nome = ",".join(partes[:-5]).strip()
            drv, tot, usada, livre, uso = partes[-5:]
            return {"nome": nome, "driver": drv, "vram_total_mb": _num(tot),
                    "vram_usada_mb": _num(usada), "vram_livre_mb": _num(livre), "uso_pct": _num(uso)}
    raise RuntimeError("saída do nvidia-smi sem linha de GPU")


def interpretar_compute_apps(saida: str) -> list[dict]:
    """Linhas de `--query-compute-apps=pid,process_name,used_memory`.
    No Windows (WDDM) a memória por processo costuma vir como [N/A] → None."""
    procs = []
    for linha in saida.splitlines():
        partes = linha.split(",")
        if len(partes) < 3:
            continue
        try:
            pid = int(partes[0].strip())
        except ValueError:
            continue
        caminho = ",".join(partes[1:-1]).strip()
        procs.append({"pid": pid, "processo": caminho,
                      "exe": os.path.basename(caminho.replace("\\", "/")).lower(),
                      "vram_mb": _num(partes[-1])})
    return procs


def ler_gpu() -> dict:
    """Nome, driver, VRAM total/usada/livre (MiB) e uso (%) da primeira GPU."""
    return interpretar_query_gpu(_rodar_smi([
        "--query-gpu=name,driver_version,memory.total,memory.used,memory.free,utilization.gpu",
        "--format=csv,noheader,nounits"]))


def listar_processos_gpu() -> list[dict]:
    return interpretar_compute_apps(_rodar_smi([
        "--query-compute-apps=pid,process_name,used_memory", "--format=csv,noheader,nounits"]))


def _tela_cheia() -> bool | None:
    """True se há app em tela cheia (jogo D3D, apresentação, "ocupado").
    Usa SHQueryUserNotificationState (shell32). None se não deu para saber."""
    if not _WINDOWS:  # pragma: no cover
        return None
    try:
        estado = ctypes.c_int(0)
        hr = ctypes.windll.shell32.SHQueryUserNotificationState(ctypes.byref(estado))
        if hr != 0:
            return None
        # 2 = QUNS_BUSY (tela cheia), 3 = QUNS_RUNNING_D3D_FULL_SCREEN, 4 = QUNS_PRESENTATION_MODE
        return estado.value in (2, 3, 4)
    except Exception:
        return None


def _env_float(nome: str, padrao: float) -> float:
    try:
        return float(os.environ.get(nome, "") or padrao)
    except ValueError:
        return padrao


@dataclass
class EstadoGpu:
    """Resultado de `gpu_ocupada_por_outros()`. Vale como bool (`if estado:` = ocupada)."""
    ocupada: bool
    motivo: str
    uso_pct: float | None = None
    vram_usada_mb: float | None = None
    vram_total_mb: float | None = None
    vram_livre_mb: float | None = None
    tela_cheia: bool | None = None
    pesados: list[str] = field(default_factory=list)
    processos: list[dict] = field(default_factory=list)
    limiares: dict = field(default_factory=dict)
    erro: str | None = None

    def __bool__(self) -> bool:
        return bool(self.ocupada)

    def como_dict(self) -> dict:
        return asdict(self)


def gpu_ocupada_por_outros(limiar_uso_pct: float | None = None,
                           limiar_vram_mb: float | None = None,
                           processos_pesados: list[str] | None = None,
                           amostras: int = 3, intervalo_s: float = 1.0,
                           ignorar_pids: set[int] | None = None,
                           considerar_tela_cheia: bool = True) -> EstadoGpu:
    """Diz se OUTRO programa está usando a GPU a ponto de o worker dever pausar.

    Chamar ENTRE jobs (antes de pegar o gpu.lock): com o nosso motor rodando, o
    uso e a VRAM medidos incluem o próprio motor (o Windows não separa a VRAM
    por processo; vem [N/A]).

    Ocupada se qualquer um:
    - não deu para ler a GPU (fail-closed: na dúvida, não atrapalha);
    - há app em tela cheia (jogo/apresentação), se `considerar_tela_cheia`;
    - roda um processo da lista de pesados (nomes de .exe; padrão vem de
      OFICINA3D_PROCESSOS_PESADOS, separados por ';');
    - uso da GPU (mediana das amostras) >= limiar_uso_pct
      (padrão OFICINA3D_GPU_USO_MAX, 30%);
    - VRAM usada >= limiar_vram_mb (padrão OFICINA3D_GPU_VRAM_MAX_MB, 3000 MiB;
      a área de trabalho comum usa ~1,1 GB na 4060).
    """
    lim_uso = limiar_uso_pct if limiar_uso_pct is not None else _env_float("OFICINA3D_GPU_USO_MAX", 30)
    lim_vram = limiar_vram_mb if limiar_vram_mb is not None else _env_float("OFICINA3D_GPU_VRAM_MAX_MB", 3000)
    if processos_pesados is None:
        processos_pesados = [p for p in os.environ.get("OFICINA3D_PROCESSOS_PESADOS", "").split(";") if p.strip()]
    pesados_alvo = {p.strip().lower() for p in processos_pesados}
    ignorar = set(ignorar_pids or ()) | {os.getpid()}
    limiares = {"uso_pct": lim_uso, "vram_mb": lim_vram, "pesados": sorted(pesados_alvo)}

    usos: list[float] = []
    ultimo: dict = {}
    try:
        for i in range(max(1, int(amostras))):
            if i:
                time.sleep(intervalo_s)
            ultimo = ler_gpu()
            if ultimo.get("uso_pct") is not None:
                usos.append(ultimo["uso_pct"])
        procs = [p for p in listar_processos_gpu() if p["pid"] not in ignorar]
    except Exception as e:  # noqa: BLE001
        return EstadoGpu(True, "não consegui ler a GPU (nvidia-smi); por segurança, considerada ocupada",
                         limiares=limiares, erro=str(e))

    uso = statistics.median(usos) if usos else None
    est = EstadoGpu(False, "livre", uso_pct=uso, vram_usada_mb=ultimo.get("vram_usada_mb"),
                    vram_total_mb=ultimo.get("vram_total_mb"), vram_livre_mb=ultimo.get("vram_livre_mb"),
                    processos=procs, limiares=limiares)
    est.pesados = sorted({p["exe"] for p in procs if p["exe"] in pesados_alvo})
    if considerar_tela_cheia:
        est.tela_cheia = _tela_cheia()

    motivos = []
    if est.tela_cheia:
        motivos.append("app em tela cheia (jogo ou apresentação)")
    if est.pesados:
        motivos.append("processo pesado rodando: " + ", ".join(est.pesados))
    if uso is not None and uso >= lim_uso:
        motivos.append(f"uso da GPU {uso:.0f}% >= {lim_uso:.0f}%")
    if est.vram_usada_mb is not None and est.vram_usada_mb >= lim_vram:
        motivos.append(f"VRAM usada {est.vram_usada_mb:.0f} MiB >= {lim_vram:.0f} MiB")
    if motivos:
        est.ocupada = True
        est.motivo = "; ".join(motivos)
    return est


def esperar_gpu_livre(parar: Callable[[], bool] | None = None,
                      verificar_a_cada_s: float = 60.0,
                      max_espera_s: float | None = None,
                      ao_esperar: Callable[[EstadoGpu], None] | None = None,
                      **limiares) -> bool:
    """Bloqueia enquanto outro programa usa a GPU. True = livre; False = `parar()`
    pediu para sair ou estourou `max_espera_s`. `ao_esperar(estado)` é chamado a
    cada verificação ocupada (para o worker registrar "pausado: <motivo>")."""
    inicio = time.monotonic()
    while True:
        if parar and parar():
            return False
        estado = gpu_ocupada_por_outros(**limiares)
        if not estado:
            return True
        if ao_esperar:
            ao_esperar(estado)
        if max_espera_s is not None and time.monotonic() - inicio >= max_espera_s:
            return False
        fim = time.monotonic() + verificar_a_cada_s
        while time.monotonic() < fim:
            if parar and parar():
                return False
            time.sleep(min(1.0, verificar_a_cada_s))
