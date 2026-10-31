"""Jobs da Oficina 3D: uma pasta por pedido, estado em job.json (fonte da verdade).

Correções da v2 (plano 6.5):
- id sempre no formato AAAAMMDD-HHMMSS-nome (RE_ID), conferido em toda função que recebe id
  (bloqueia "..\\", barras e caminhos);
- a pasta do job é reservada com mkdir(exist_ok=False) em laço (dois processos nunca pegam o mesmo id);
- trava por job (job.lock, criado com O_CREAT|O_EXCL, com timeout) e escrita atômica do job.json
  (grava um .tmp e troca com os.replace);
- opções conferidas (motor conhecido, faixas, tipos) e imagens conferidas (existe, é PNG/JPEG/WEBP de
  verdade, até 40 MB e 8192 px de lado); funciona com ou sem Pillow;
- se criar_job falhar no meio, a pasta criada é apagada;
- motor automático: hunyuan-mv-turbo com 2+ vistas, hunyuan-mini-turbo com 1.

A pasta dos jobs é lida de config.JOBS na hora de cada chamada (os testes trocam esse valor).
"""
import json
import math
import os
import re
import secrets
import shutil
import struct
import threading
import time
import unicodedata
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Callable

from . import config

FUSO = timezone(timedelta(hours=-3))
SUBPASTAS = ("entrada", "preproc", "forma", "refino", "saida")
ESTADOS = ("pendente", "processando", "concluido", "erro", "cancelado")

RE_ID = re.compile(r"[0-9]{8}-[0-9]{6}-[a-z0-9-]{1,40}")
TAM_SLUG = 40

# Limites das entradas
LIMITE_BYTES_IMAGEM = 40 * 1024 * 1024
LADO_MAX = 8192
LADO_MIN = 16
MAX_IMAGENS = 16
LIMITE_BYTES_MALHA = 300 * 1024 * 1024
EXTENSOES_MALHA = (".glb", ".obj")
EXTENSOES_IMAGEM = {"PNG": (".png",), "JPEG": (".jpg", ".jpeg"), "WEBP": (".webp",)}

# Faixas das opções (inclusive nas duas pontas)
FAIXAS_INT = {
    "passos": (1, 100),
    "octree": (64, 512),
    "seed": (0, 2**32 - 1),
    "sementes": (1, 8),
    "alvo_triangulos": (1_000, 1_000_000),
}
FAIXAS_REAL = {"altura_m": (0.01, 100.0)}
OPCOES_BOOL = ("flashvdm", "simetrizar", "dividir_pranchas")

# Trava por job
NOME_TRAVA = "job.lock"
TIMEOUT_TRAVA_S = 10.0
TRAVA_VELHA_S = 120.0   # trava mais velha que isso (ou de processo morto) é considerada abandonada


class TravaOcupada(TimeoutError):
    """Outro processo segurou a trava do job por mais tempo que o timeout."""


# ---------------------------------------------------------------------------
# Básico
# ---------------------------------------------------------------------------
def agora() -> str:
    return datetime.now(FUSO).isoformat(timespec="seconds")


def _carimbo() -> str:
    return datetime.now(FUSO).strftime("%Y%m%d-%H%M%S")


def _slug(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()[:TAM_SLUG].strip("-") or "job"


def validar_id(job_id) -> str:
    """Devolve o id se ele está no formato AAAAMMDD-HHMMSS-nome; senão levanta ValueError."""
    if not isinstance(job_id, str) or not RE_ID.fullmatch(job_id):
        raise ValueError(f"id de job inválido: {job_id!r} (formato AAAAMMDD-HHMMSS-nome; "
                         f"nome só com a-z, 0-9 e '-', até {TAM_SLUG} letras)")
    return job_id


def pasta_job(job_id: str) -> Path:
    return Path(config.JOBS) / validar_id(job_id)


def _repetir(func, tentativas: int = 60, espera: float = 0.05):
    """No Windows, ler/trocar um arquivo que outro processo está abrindo dá PermissionError por instantes."""
    for i in range(tentativas):
        try:
            return func()
        except PermissionError:
            if i == tentativas - 1:
                raise
            time.sleep(espera)


# ---------------------------------------------------------------------------
# Trava por job (job.lock)
# ---------------------------------------------------------------------------
_local = threading.local()


def _mantidas() -> dict:
    d = getattr(_local, "travas", None)
    if d is None:
        d = _local.travas = {}
    return d


def _pid_vivo(pid: int) -> bool:
    if pid <= 0:
        return False
    if os.name == "nt":
        # os.kill(pid, 0) no Windows MATA o processo; por isso a consulta é pela API.
        import ctypes
        from ctypes import wintypes
        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        k32.OpenProcess.restype = wintypes.HANDLE
        k32.OpenProcess.argtypes = (wintypes.DWORD, wintypes.BOOL, wintypes.DWORD)
        k32.GetExitCodeProcess.argtypes = (wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD))
        k32.CloseHandle.argtypes = (wintypes.HANDLE,)
        h = k32.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return ctypes.get_last_error() == 5  # acesso negado: o processo existe
        try:
            codigo = wintypes.DWORD()
            if not k32.GetExitCodeProcess(h, ctypes.byref(codigo)):
                return True
            return codigo.value == 259  # STILL_ACTIVE
        finally:
            k32.CloseHandle(h)
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _ler_trava(caminho: Path) -> str | None:
    try:
        return caminho.read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return None


def _trava_velha(caminho: Path, conteudo: str) -> bool:
    partes = conteudo.split()
    if partes and partes[0].isdigit() and not _pid_vivo(int(partes[0])):
        return True
    try:
        return time.time() - caminho.stat().st_mtime > TRAVA_VELHA_S
    except OSError:
        return False


def _quebrar_trava(caminho: Path, visto: str) -> None:
    """Tira uma trava abandonada sem correr o risco de apagar uma trava nova de outro processo."""
    lixo = caminho.with_name(f"{caminho.name}.velha.{secrets.token_hex(4)}")
    try:
        os.rename(caminho, lixo)
    except OSError:
        return
    if _ler_trava(lixo) != visto:  # outro processo já tinha trocado a trava: devolve
        try:
            os.rename(lixo, caminho)
            return
        except OSError:
            pass
    try:
        os.remove(lixo)
    except OSError:
        pass


def _adquirir(caminho: Path, timeout: float, job_id: str) -> str:
    token = secrets.token_hex(8)
    conteudo = f"{os.getpid()} {token} {agora()}".encode("utf-8")
    limite = time.monotonic() + max(0.0, timeout)
    while True:
        try:
            fd = os.open(caminho, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0))
        except FileExistsError:
            visto = _ler_trava(caminho)
            if visto is not None and _trava_velha(caminho, visto):
                _quebrar_trava(caminho, visto)
        except PermissionError:
            pass  # Windows: a trava anterior está sendo apagada neste instante
        else:
            with os.fdopen(fd, "wb") as f:
                f.write(conteudo)
            return token
        if time.monotonic() >= limite:
            dono = (_ler_trava(caminho) or "?").strip()
            raise TravaOcupada(f"job {job_id} travado por outro processo há mais de {timeout:g} s (trava: {dono})")
        time.sleep(0.02 + secrets.randbelow(30) / 1000)


def _liberar(caminho: Path, token: str) -> None:
    conteudo = _ler_trava(caminho)
    if not conteudo or conteudo.split()[1:2] != [token]:
        return  # não é mais nossa (foi quebrada por velhice) ou já sumiu
    try:
        _repetir(lambda: os.remove(caminho), tentativas=20)
    except FileNotFoundError:
        pass


@contextmanager
def trava_job(job_id: str, timeout: float | None = None):
    """Segura a trava do job (reentrante na mesma thread). Use só para operações curtas.

        with trava_job(id):
            j = ler_job(id); ...; salvar_job(j)
    """
    pasta = pasta_job(job_id)
    caminho = pasta / NOME_TRAVA
    chave = os.path.normcase(str(caminho))
    mantidas = _mantidas()
    if chave in mantidas:
        mantidas[chave] += 1
        try:
            yield caminho
        finally:
            mantidas[chave] -= 1
        return
    if not pasta.is_dir():
        raise FileNotFoundError(f"job não encontrado: {job_id}")
    token = _adquirir(caminho, TIMEOUT_TRAVA_S if timeout is None else timeout, job_id)
    mantidas[chave] = 1
    try:
        yield caminho
    finally:
        del mantidas[chave]
        _liberar(caminho, token)


# ---------------------------------------------------------------------------
# Leitura e gravação do job.json
# ---------------------------------------------------------------------------
def _gravar_atomico(destino: Path, texto: str) -> None:
    tmp = destino.with_name(f"{destino.name}.{os.getpid()}.{secrets.token_hex(4)}.tmp")
    try:
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(texto)
            f.flush()
            os.fsync(f.fileno())
        _repetir(lambda: os.replace(tmp, destino))
    except BaseException:
        try:
            os.remove(tmp)
        except OSError:
            pass
        raise


def salvar_job(job: dict) -> None:
    """Grava job.json de forma atômica (escreve .tmp e troca), com a trava do job."""
    if not isinstance(job, dict):
        raise TypeError("job precisa ser um dict")
    job_id = validar_id(job.get("id"))
    texto = json.dumps(job, ensure_ascii=False, indent=2)  # falha aqui (tipo estranho) não deixa lixo
    with trava_job(job_id):
        _gravar_atomico(pasta_job(job_id) / "job.json", texto)


def ler_job(job_id: str) -> dict:
    p = pasta_job(job_id) / "job.json"
    try:
        texto = _repetir(lambda: p.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise FileNotFoundError(f"job não encontrado: {job_id}") from None
    try:
        job = json.loads(texto)
    except json.JSONDecodeError as e:
        raise ValueError(f"job.json corrompido em {job_id}: {e}") from None
    if not isinstance(job, dict) or job.get("id") != job_id:
        raise ValueError(f"job.json de {job_id} não corresponde ao id da pasta")
    return job


def listar_jobs() -> list[dict]:
    """Jobs válidos, do mais antigo para o mais novo (pastas com nome fora do formato são ignoradas)."""
    raiz = Path(config.JOBS)
    jobs = []
    if raiz.is_dir():
        for p in raiz.iterdir():
            if not RE_ID.fullmatch(p.name) or not p.is_dir():
                continue
            try:
                jobs.append(ler_job(p.name))
            except (OSError, ValueError):
                continue
    return sorted(jobs, key=lambda j: (str(j.get("criado_em", "")), j["id"]))


def registrar(job: dict, etapa: str | None, msg: str, progresso: int | None = None, salvar: bool = True) -> None:
    job.setdefault("historico", []).append({"quando": agora(), "etapa": etapa, "msg": msg})
    if etapa is not None:
        job["etapa"] = etapa
    if progresso is not None:
        job["progresso"] = int(max(0, min(100, progresso)))
    if salvar:
        salvar_job(job)


def atualizar_job(job_id: str, alterar: Callable[[dict], dict | None], timeout: float | None = None) -> dict:
    """Lê, altera e grava o job com a trava segura do começo ao fim (sem corrida entre worker, web e MCP).

    `alterar` recebe o dict e o modifica (ou devolve um novo). Devolve o job gravado.
    """
    with trava_job(job_id, timeout=timeout):
        job = ler_job(job_id)
        novo = alterar(job)
        if novo is not None:
            job = novo
        if job.get("id") != job_id:
            raise ValueError("atualizar_job não pode trocar o id do job")
        salvar_job(job)
        return job


# ---------------------------------------------------------------------------
# Conferência das entradas
# ---------------------------------------------------------------------------
def _pillow():
    """Módulo PIL.Image, se o Pillow estiver instalado neste Python; senão None."""
    try:
        from PIL import Image
    except Exception:
        return None
    return Image


def _formato_pela_assinatura(cab: bytes) -> str | None:
    if cab.startswith(b"\x89PNG\r\n\x1a\n"):
        return "PNG"
    if cab.startswith(b"\xff\xd8\xff"):
        return "JPEG"
    if len(cab) >= 12 and cab[:4] == b"RIFF" and cab[8:12] == b"WEBP":
        return "WEBP"
    return None


def _dimensoes_png(d: bytes):
    if len(d) < 24 or d[12:16] != b"IHDR" or d.rfind(b"IEND") < 0:
        return None  # sem IHDR ou truncado (sem IEND)
    return struct.unpack(">II", d[16:24])


_SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


def _dimensoes_jpeg(d: bytes):
    i, n = 2, len(d)
    while i < n:
        if d[i] != 0xFF:
            return None
        while i < n and d[i] == 0xFF:
            i += 1
        if i >= n:
            return None
        m = d[i]
        i += 1
        if m in (0x01, 0xD8) or 0xD0 <= m <= 0xD7:
            continue
        if m in (0xD9, 0xDA) or i + 2 > n:
            return None  # acabou (ou começaram os dados) sem achar o SOF
        tam = struct.unpack(">H", d[i:i + 2])[0]
        if m in _SOF:
            if i + 7 > n:
                return None
            h, w = struct.unpack(">HH", d[i + 3:i + 7])
            return w, h
        i += tam
    return None


def _dimensoes_webp(d: bytes):
    pedaco = d[12:16]
    if pedaco == b"VP8 " and len(d) >= 30 and d[23:26] == b"\x9d\x01\x2a":
        w, h = struct.unpack("<HH", d[26:30])
        return w & 0x3FFF, h & 0x3FFF
    if pedaco == b"VP8L" and len(d) >= 25 and d[20] == 0x2F:
        b = int.from_bytes(d[21:25], "little")
        return (b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1
    if pedaco == b"VP8X" and len(d) >= 30:
        return int.from_bytes(d[24:27], "little") + 1, int.from_bytes(d[27:30], "little") + 1
    return None


_DIMENSOES = {"PNG": _dimensoes_png, "JPEG": _dimensoes_jpeg, "WEBP": _dimensoes_webp}


def conferir_imagem(caminho) -> dict:
    """Confere que o arquivo existe, é PNG/JPEG/WEBP de verdade e tem tamanho aceitável.

    Usa o Pillow se estiver instalado; senão lê a assinatura e o cabeçalho na mão.
    Devolve {"formato", "largura", "altura", "bytes"}; levanta ValueError com o motivo.
    """
    p = Path(caminho)
    if not p.is_file():
        raise ValueError(f"imagem não encontrada: {p}")
    tam = p.stat().st_size
    if tam == 0:
        raise ValueError(f"imagem vazia: {p}")
    if tam > LIMITE_BYTES_IMAGEM:
        raise ValueError(f"imagem grande demais ({tam / 2**20:.1f} MB; limite {LIMITE_BYTES_IMAGEM / 2**20:.0f} MB): {p}")
    with open(p, "rb") as f:
        cab = f.read(32)
    formato = _formato_pela_assinatura(cab)
    if formato is None:
        raise ValueError(f"não é imagem PNG, JPEG nem WEBP: {p}")

    Image = _pillow()
    if Image is not None:
        try:
            with Image.open(p) as im:
                fmt_pil = "JPEG" if im.format == "MPO" else im.format
                w, h = im.size
                im.verify()
        except Exception as e:
            raise ValueError(f"imagem ilegível ({type(e).__name__}: {e}): {p}") from None
        if fmt_pil != formato:
            raise ValueError(f"formato confuso ({formato} pela assinatura, {fmt_pil} pelo Pillow): {p}")
    else:
        dims = _DIMENSOES[formato](p.read_bytes())
        if dims is None:
            raise ValueError(f"cabeçalho {formato} ilegível ou arquivo truncado: {p}")
        w, h = dims

    if min(w, h) < LADO_MIN:
        raise ValueError(f"imagem pequena demais ({w}x{h}; mínimo {LADO_MIN} px de lado): {p}")
    if max(w, h) > LADO_MAX:
        raise ValueError(f"imagem grande demais ({w}x{h}; máximo {LADO_MAX} px de lado): {p}")
    return {"formato": formato, "largura": int(w), "altura": int(h), "bytes": tam}


def conferir_malha(caminho) -> dict:
    """Confere a malha do modo so-refinar (.glb ou .obj, até LIMITE_BYTES_MALHA)."""
    p = Path(caminho)
    if not p.is_file():
        raise ValueError(f"malha não encontrada: {p}")
    ext = p.suffix.lower()
    if ext not in EXTENSOES_MALHA:
        raise ValueError(f"malha precisa ser {' ou '.join(EXTENSOES_MALHA)}: {p}")
    tam = p.stat().st_size
    if tam == 0 or tam > LIMITE_BYTES_MALHA:
        raise ValueError(f"malha vazia ou grande demais ({tam / 2**20:.1f} MB; "
                         f"limite {LIMITE_BYTES_MALHA / 2**20:.0f} MB): {p}")
    if ext == ".glb":
        with open(p, "rb") as f:
            if f.read(4) != b"glTF":
                raise ValueError(f"não é um .glb válido (falta a assinatura glTF): {p}")
    return {"formato": ext[1:], "bytes": tam}


# ---------------------------------------------------------------------------
# Opções
# ---------------------------------------------------------------------------
def _inteiro(k: str, v) -> int:
    if isinstance(v, bool) or not isinstance(v, (int, float)) or (isinstance(v, float) and not v.is_integer()):
        raise ValueError(f"opção {k} precisa ser número inteiro, recebi {v!r}")
    v = int(v)
    lo, hi = FAIXAS_INT[k]
    if not lo <= v <= hi:
        raise ValueError(f"opção {k} fora da faixa {lo}–{hi}: {v}")
    return v


def _real(k: str, v) -> float:
    if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
        raise ValueError(f"opção {k} precisa ser número, recebi {v!r}")
    lo, hi = FAIXAS_REAL[k]
    if not lo <= v <= hi:
        raise ValueError(f"opção {k} fora da faixa {lo}–{hi}: {v}")
    return float(v)


def _validar_opcao(k: str, v):
    if k == "motor":
        if v not in config.MOTORES:
            raise ValueError(f"motor desconhecido: {v!r} (use {', '.join(config.MOTORES)})")
        return v
    if k in FAIXAS_INT:
        return _inteiro(k, v)
    if k in FAIXAS_REAL:
        return _real(k, v)
    if k in OPCOES_BOOL:
        if not isinstance(v, bool):
            raise ValueError(f"opção {k} precisa ser true/false, recebi {v!r}")
        return v
    if k == "remover_fundo":
        if isinstance(v, bool):
            return "sim" if v else "nao"
        if v not in config.REMOVER_FUNDO:
            raise ValueError(f"remover_fundo inválido: {v!r} (use {', '.join(config.REMOVER_FUNDO)})")
        return v
    # Opção nova acrescentada em config.OPCOES_PADRAO sem regra aqui: aceita se o tipo bate com o padrão.
    padrao = config.OPCOES_PADRAO[k]
    if padrao is not None and type(v) is not type(padrao):
        raise ValueError(f"opção {k} precisa ser {type(padrao).__name__}, recebi {v!r}")
    return v


def motor_padrao(modo: str, vistas) -> str:
    """Motor automático da v2: hunyuan-mv-turbo com 2+ vistas de forma, hunyuan-mini-turbo com 1.

    Conta as vistas frente/costas/esquerda/direita distintas, mais as imagens sem vista (o nome do
    arquivo ainda vai dizer qual é). No modo multivista é sempre o mv-turbo (pode vir uma prancha só).
    """
    vistas = list(vistas)
    if modo == "multivista":
        return config.MOTOR_PADRAO_MULTIVISTA
    n = len({v for v in vistas if v in config.VISTAS_MV_HUNYUAN}) + sum(1 for v in vistas if v is None)
    return config.MOTOR_PADRAO_MULTIVISTA if n >= 2 else config.MOTOR_PADRAO_UMA_VISTA


def validar_opcoes(opcoes: dict | None = None, modo: str = "livre", vistas=()) -> tuple[dict, list[str]]:
    """Junta as opções com OPCOES_PADRAO, conferindo nomes, tipos e faixas.

    None numa opção = usar o padrão (motor None = automático). Devolve (opcoes, avisos).
    """
    if opcoes is None:
        opcoes = {}
    if not isinstance(opcoes, dict):
        raise ValueError("opcoes precisa ser um dicionário")
    desconhecidas = sorted(set(opcoes) - set(config.OPCOES_PADRAO))
    if desconhecidas:
        raise ValueError(f"opção desconhecida: {', '.join(map(str, desconhecidas))} "
                         f"(válidas: {', '.join(config.OPCOES_PADRAO)})")
    op = dict(config.OPCOES_PADRAO)
    for k, v in opcoes.items():
        if v is not None:
            op[k] = _validar_opcao(k, v)
    vistas = list(vistas)
    avisos = []
    if op["motor"] is None:
        op["motor"] = motor_padrao(modo, vistas)
    elif op["motor"] not in config.MOTORES_MULTIVISTA:
        n_mv = len({v for v in vistas if v in config.VISTAS_MV_HUNYUAN})
        if n_mv >= 2:
            avisos.append(f"o motor {op['motor']} usa uma imagem só; as outras vistas servem de conferência")
    repetidas = sorted({v for v in vistas if v is not None and vistas.count(v) > 1})
    if repetidas:
        avisos.append(f"vista repetida: {', '.join(repetidas)}")
    return op, avisos


# ---------------------------------------------------------------------------
# Criação
# ---------------------------------------------------------------------------
_RESERVADOS = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)), *(f"LPT{i}" for i in range(1, 10))}


def _nome_seguro(nome: str, extensoes: tuple[str, ...]) -> str:
    """Nome de arquivo seguro para o Windows; a extensão sai da lista (a primeira se a original não serve)."""
    p = Path(nome)
    base = re.sub(r"[^\w\-]+", "_", unicodedata.normalize("NFC", p.stem)).strip("_ ")[:80] or "arquivo"
    if base.upper() in _RESERVADOS:
        base = "_" + base
    ext = p.suffix.lower()
    return base + (ext if ext in extensoes else extensoes[0])


def _nome_unico(nome: str, usados: set) -> str:
    base, ext = os.path.splitext(nome)
    candidato, k = nome, 2
    while candidato.lower() in usados:
        candidato = f"{base}_{k}{ext}"
        k += 1
    usados.add(candidato.lower())
    return candidato


def _reservar_pasta(raiz: Path, base_nome: str) -> tuple[str, Path]:
    """Cria a pasta do job com mkdir(exist_ok=False): se outro processo pegou o id, tenta o próximo."""
    slug = _slug(base_nome)
    carimbo = _carimbo()
    for n in range(1, 1000):
        sufixo = "" if n == 1 else f"-{n}"
        job_id = validar_id(f"{carimbo}-{(slug[:TAM_SLUG - len(sufixo)].rstrip('-') or 'job')}{sufixo}")
        pasta = raiz / job_id
        try:
            pasta.mkdir(exist_ok=False)
        except FileExistsError:
            continue
        return job_id, pasta
    raise RuntimeError(f"não consegui reservar um id livre para {slug!r} em {raiz}")


def _apagar_pasta(pasta: Path) -> None:
    for _ in range(10):
        shutil.rmtree(pasta, ignore_errors=True)
        if not pasta.exists():
            return
        time.sleep(0.1)


def criar_job(arquivos: list[tuple[Path, str | None]], modo: str = "livre", opcoes: dict | None = None,
              nome: str | None = None, malha: Path | None = None) -> dict:
    """Cria jobs\\<id>\\ com cópias das imagens (e da malha, no modo so-refinar).

    arquivos: [(caminho_da_imagem, vista ou None)]. Vista None = descobrir depois pelo nome
    (entrada.vista_pelo_nome) ou ficar sem etiqueta.
    Tudo é conferido ANTES de criar a pasta; se algo falhar depois disso, a pasta é apagada.
    """
    if modo not in config.MODOS:
        raise ValueError(f"modo inválido: {modo!r} (use {', '.join(config.MODOS)})")
    arquivos = list(arquivos or [])
    if modo == "so-refinar" and malha is None:
        raise ValueError("modo so-refinar precisa de uma malha (.glb/.obj)")
    if modo != "so-refinar" and not arquivos:
        raise ValueError("mande pelo menos uma imagem")
    if len(arquivos) > MAX_IMAGENS:
        raise ValueError(f"imagens demais ({len(arquivos)}; máximo {MAX_IMAGENS})")
    if nome is not None and (not isinstance(nome, str) or not nome.strip()):
        raise ValueError("nome do job vazio")

    entradas = []
    for item in arquivos:
        try:
            origem, vista = item
        except (TypeError, ValueError):
            raise ValueError("cada item de arquivos é (caminho, vista ou None)") from None
        if vista is not None and vista not in config.VISTAS:
            raise ValueError(f"vista inválida: {vista!r} (use {', '.join(config.VISTAS)})")
        entradas.append((Path(origem), vista, conferir_imagem(origem)))
    if malha is not None:
        malha = Path(malha)
        conferir_malha(malha)
    vistas = [v for _, v, _ in entradas]
    op, avisos = validar_opcoes(opcoes, modo, vistas)
    motor_auto = (opcoes or {}).get("motor") is None
    base_nome = nome.strip() if nome else (entradas[0][0].stem if entradas else malha.stem)

    raiz_jobs = config.verificar_fora_do_drive(Path(config.JOBS), "OFICINA3D_JOBS")
    raiz_jobs.mkdir(parents=True, exist_ok=True)
    job_id, raiz = _reservar_pasta(raiz_jobs, base_nome)
    try:
        for s in SUBPASTAS:
            (raiz / s).mkdir()
        usados = set()
        imagens = []
        for origem, vista, info in entradas:
            destino = _nome_unico(_nome_seguro(origem.name, EXTENSOES_IMAGEM[info["formato"]]), usados)
            shutil.copy2(origem, raiz / "entrada" / destino)
            copia = conferir_imagem(raiz / "entrada" / destino)
            if copia["bytes"] != info["bytes"] or copia["formato"] != info["formato"]:
                raise OSError(f"a imagem mudou durante a cópia: {origem}")
            imagens.append({"arquivo": f"entrada/{destino}", "vista": vista})

        malha_rel = None
        if malha is not None:
            destino = _nome_unico(_nome_seguro(malha.name, (malha.suffix.lower(),)), usados)
            shutil.copy2(malha, raiz / "entrada" / destino)
            conferir_malha(raiz / "entrada" / destino)
            malha_rel = f"entrada/{destino}"

        job = {
            "id": job_id, "criado_em": agora(), "nome": base_nome, "modo": modo,
            "imagens": imagens, "malha_entrada": malha_rel, "opcoes": op,
            "estado": "pendente", "etapa": None, "progresso": 0, "erro": None, "avisos": avisos,
            "resultado": None, "historico": [],
        }
        escolha = " (automático)" if motor_auto else ""
        with trava_job(job_id):
            registrar(job, None, f"job criado ({len(imagens)} imagem(ns), modo {modo}, motor {op['motor']}{escolha})")
        return job
    except BaseException:
        _apagar_pasta(raiz)
        raise
