"""Regras de segurança comuns ao servidor MCP e à página web da Oficina 3D.

Só biblioteca padrão (roda no .venv_mcp, no .venv do app e nos testes sem nada instalado).
Princípio: **fail-closed** — em qualquer dúvida, recusa.

Conteúdo:
- validar_id ............ id de job no formato do contrato (nada de "..\\", barras, letras de unidade)
- caminho_dentro ........ caminho RELATIVO que tem de ficar dentro de uma pasta (arquivos de um job)
- caminho_permitido ..... caminho ABSOLUTO local que tem de ficar dentro das pastas permitidas
- tipo_por_assinatura ... tipo real do arquivo pelos primeiros bytes (PNG/JPG/WebP/GLB/OBJ)
- decodificar_base64 .... base64 com limite de 40 MB (conferido ANTES de decodificar) e tipo conferido
- ler_token / token_confere / extrair_token ... token do HTTP (arquivo em BASE\\locks\\ ou OFICINA3D_TOKEN)
- pedido_local / origem_confere ............... decide se um pedido HTTP veio mesmo deste PC
- ler_trava_worker / processo_confere ......... PID do worker conferido pelo psutil + horário de criação
- MiddlewareToken ....... ASGI puro: exige token em todo pedido HTTP (usado no MCP por HTTP)
"""
from __future__ import annotations

import base64
import binascii
import hmac
import json
import os
import re
from pathlib import Path, PurePosixPath

# ---------------------------------------------------------------- limites
LIMITE_BYTES = 40 * 1024 * 1024          # 40 MB por arquivo (imagem, malha ou resultado em base64)
MAX_IMAGENS = 12
TOKEN_MIN = 32                            # caracteres mínimos de um token aceitável
NOME_ARQUIVO_TOKEN = "oficina3d_token.txt"  # em BASE\locks\ (fora do git)
VAR_TOKEN = "OFICINA3D_TOKEN"

TIPOS_IMAGEM = frozenset({"png", "jpg", "webp"})
TIPOS_MALHA = frozenset({"glb", "obj"})
EXTENSAO = {"png": ".png", "jpg": ".jpg", "webp": ".webp", "glb": ".glb", "obj": ".obj"}

# Formato do id (plano 6.5): AAAAMMDD-HHMMSS-slug. Aceita também o sufixo "_N" de colisão da v1.
RE_ID = re.compile(r"^[0-9]{8}-[0-9]{6}-[a-z0-9-]{1,40}(?:_[0-9]{1,4})?$")

HOSTS_LOOPBACK = frozenset({"127.0.0.1", "::1", "localhost"})
CABECALHOS_PROXY = ("x-forwarded-for", "x-forwarded-host", "x-real-ip", "forwarded", "cf-connecting-ip",
                    "tailscale-user-login", "x-original-forwarded-for")


class ErroSeguranca(ValueError):
    """Pedido recusado por uma regra de segurança (mensagem em português, segura para devolver)."""


# ---------------------------------------------------------------- id de job
def validar_id(job_id) -> str:
    """Devolve o id se for válido; senão levanta ErroSeguranca."""
    if not isinstance(job_id, str) or not RE_ID.fullmatch(job_id):
        raise ErroSeguranca("id de job inválido (formato esperado: AAAAMMDD-HHMMSS-nome)")
    return job_id


# ---------------------------------------------------------------- caminhos
def _dentro(p: Path, raiz: Path) -> bool:
    """p está dentro de raiz (ou é a própria raiz)? Comparação sem diferença de maiúsculas no Windows."""
    a = Path(os.path.normcase(str(p)))
    b = Path(os.path.normcase(str(raiz)))
    return a == b or a.is_relative_to(b)


def caminho_dentro(raiz: Path, relativo: str, *, deve_existir: bool = True) -> Path:
    """Resolve `relativo` (estilo URL, com "/") dentro de `raiz` e garante que não escapa dela.

    Recusa: vazio, NUL, "\\", ":" (unidade ou fluxo alternativo NTFS), absoluto, "..", partes vazias,
    partes terminadas em ponto/espaço (o Windows as apaga) e qualquer coisa que, resolvida, saia da raiz
    (inclusive por link simbólico ou nome reservado como NUL/CON).
    """
    if not isinstance(relativo, str) or not relativo or len(relativo) > 400:
        raise ErroSeguranca("caminho vazio ou longo demais")
    if "\x00" in relativo or "\\" in relativo or ":" in relativo:
        raise ErroSeguranca("caminho com caractere proibido")
    pp = PurePosixPath(relativo)
    if pp.is_absolute() or relativo.startswith("/"):
        raise ErroSeguranca("caminho absoluto não é aceito aqui")
    partes = relativo.split("/")
    for parte in partes:
        if parte in ("", ".", "..") or parte != parte.rstrip(". "):
            raise ErroSeguranca("caminho com parte proibida")
    raiz_r = Path(raiz).resolve()
    alvo = raiz_r.joinpath(*partes).resolve()
    if not _dentro(alvo, raiz_r) or alvo == raiz_r:
        raise ErroSeguranca("caminho fora da pasta permitida")
    if deve_existir and not alvo.exists():
        raise ErroSeguranca("arquivo não encontrado")
    return alvo


def caminho_permitido(caminho, raizes) -> Path:
    """Caminho ABSOLUTO de um arquivo deste PC; só vale se, resolvido, ficar dentro de uma das `raizes`.

    Recusa caminhos de rede (UNC), relativos, com NUL, inexistentes e que não sejam arquivo.
    """
    if not isinstance(caminho, (str, os.PathLike)):
        raise ErroSeguranca("caminho inválido")
    texto = os.fspath(caminho)
    if not texto or "\x00" in texto or len(texto) > 1000:
        raise ErroSeguranca("caminho inválido")
    if texto.startswith(("\\\\", "//")):
        raise ErroSeguranca("caminho de rede (UNC) não é aceito")
    p = Path(texto)
    if not p.is_absolute():
        raise ErroSeguranca("use caminho absoluto")
    try:
        real = p.resolve(strict=True)
    except (OSError, RuntimeError):
        raise ErroSeguranca(f"arquivo não encontrado: {texto}") from None
    permitidas = [Path(r).resolve() for r in raizes if r]
    if not any(_dentro(real, r) for r in permitidas):
        raise ErroSeguranca("caminho fora das pastas permitidas (" + "; ".join(str(r) for r in permitidas) + ")")
    if not real.is_file():
        raise ErroSeguranca("o caminho não é um arquivo")
    return real


# ---------------------------------------------------------------- tipo real do arquivo
def tipo_por_assinatura(cabeca: bytes) -> str | None:
    """Tipo pelo conteúdo (magic bytes), nunca pela extensão. None = desconhecido."""
    if cabeca.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if cabeca.startswith(b"\xff\xd8\xff"):
        return "jpg"
    if len(cabeca) >= 12 and cabeca[:4] == b"RIFF" and cabeca[8:12] == b"WEBP":
        return "webp"
    if cabeca.startswith(b"glTF"):
        return "glb"
    if _parece_obj(cabeca):
        return "obj"
    return None


def _parece_obj(cabeca: bytes) -> bool:
    """OBJ é texto: sem byte nulo, decodifica como UTF-8/ASCII e tem linhas típicas (v, vn, vt, f, o, g, #)."""
    if not cabeca or b"\x00" in cabeca:
        return False
    try:
        texto = cabeca.decode("utf-8")
    except UnicodeDecodeError:
        # o corte em 4 KB pode partir um caractere de vários bytes no fim
        try:
            texto = cabeca[:-3].decode("utf-8")
        except UnicodeDecodeError:
            return False
    tem_vertice = False
    for linha in texto.splitlines()[:200]:
        s = linha.strip()
        if not s or s.startswith("#"):
            continue
        chave = s.split(None, 1)[0]
        if chave in ("v", "vn", "vt", "f", "o", "g", "s", "mtllib", "usemtl", "l", "vp"):
            tem_vertice = tem_vertice or chave == "v"
            continue
        return False
    return tem_vertice


def conferir_arquivo(p: Path, tipos, limite: int = LIMITE_BYTES) -> str:
    """Confere tamanho (≤ limite, > 0) e tipo real de um arquivo local. Devolve o tipo."""
    tamanho = p.stat().st_size
    if tamanho <= 0:
        raise ErroSeguranca(f"arquivo vazio: {p.name}")
    if tamanho > limite:
        raise ErroSeguranca(f"arquivo grande demais: {p.name} ({tamanho / 2**20:.1f} MB; limite {limite / 2**20:.0f} MB)")
    with open(p, "rb") as f:
        tipo = tipo_por_assinatura(f.read(4096))
    if tipo not in tipos:
        raise ErroSeguranca(f"tipo de arquivo não aceito: {p.name} (aceitos: {', '.join(sorted(tipos))})")
    return tipo


_RE_DATA_URL = re.compile(r"^data:[\w.+/-]+;base64,", re.IGNORECASE)


def decodificar_base64(texto, tipos, limite: int = LIMITE_BYTES) -> tuple[bytes, str]:
    """Decodifica base64 (aceita prefixo data:...;base64,). O tamanho é conferido ANTES de decodificar."""
    if not isinstance(texto, str) or not texto:
        raise ErroSeguranca("base64 vazio ou inválido")
    texto = _RE_DATA_URL.sub("", texto, count=1)
    # limite pelo tamanho do texto: 4 caracteres -> 3 bytes, com folga para quebras de linha MIME (76 + CRLF)
    max_chars = ((limite + 2) // 3) * 4
    if len(texto) > max_chars * 78 // 76 + 16:
        raise ErroSeguranca(f"arquivo grande demais (limite {limite / 2**20:.0f} MB)")
    limpo = re.sub(r"\s+", "", texto)
    try:
        dados = base64.b64decode(limpo, validate=True)
    except (binascii.Error, ValueError):
        raise ErroSeguranca("base64 inválido") from None
    if not dados:
        raise ErroSeguranca("base64 vazio")
    if len(dados) > limite:
        raise ErroSeguranca(f"arquivo grande demais (limite {limite / 2**20:.0f} MB)")
    tipo = tipo_por_assinatura(dados[:4096])
    if tipo not in tipos:
        raise ErroSeguranca(f"tipo de arquivo não aceito (aceitos: {', '.join(sorted(tipos))})")
    return dados, tipo


def nome_seguro(nome, tipo: str, padrao: str = "imagem") -> str:
    """Nome de arquivo limpo (sem pastas, só [A-Za-z0-9_-]) com a extensão do TIPO REAL."""
    base = Path(str(nome or "")).name if nome else ""
    radical = base.rsplit(".", 1)[0] if "." in base else base
    radical = re.sub(r"[^A-Za-z0-9_-]+", "_", radical).strip("_-")[:60] or padrao
    if radical.upper() in {"CON", "PRN", "AUX", "NUL"} or re.fullmatch(r"(?i)(COM|LPT)[0-9]", radical):
        radical = f"_{radical}"
    return radical + EXTENSAO[tipo]


# ---------------------------------------------------------------- token
def _decodificar_texto(dados: bytes) -> str:
    """Lê o arquivo do token aceitando UTF-8 (com ou sem BOM) e UTF-16 (o '>' do PowerShell 5.1 grava UTF-16)."""
    if dados.startswith((b"\xff\xfe", b"\xfe\xff")):
        return dados.decode("utf-16")
    return dados.decode("utf-8-sig")


def ler_token(pasta_locks: Path | None, env=None) -> str | None:
    """Token do HTTP: variável OFICINA3D_TOKEN (prioridade) ou BASE\\locks\\oficina3d_token.txt.

    Devolve None se não houver token aceitável (curto demais também conta como "não há") —
    e quem chama tem de RECUSAR o acesso nesse caso.
    """
    env = os.environ if env is None else env
    candidato = (env.get(VAR_TOKEN) or "").strip()
    if not candidato and pasta_locks is not None:
        arq = Path(pasta_locks) / NOME_ARQUIVO_TOKEN
        try:
            candidato = _decodificar_texto(arq.read_bytes()).strip()
        except (OSError, UnicodeDecodeError):
            candidato = ""
    if len(candidato) < TOKEN_MIN or any(c.isspace() for c in candidato):
        return None
    return candidato


def token_confere(recebido, esperado) -> bool:
    """Comparação em tempo constante. Sem token configurado -> sempre False (fail-closed)."""
    if not esperado or not isinstance(recebido, str) or not recebido:
        return False
    return hmac.compare_digest(recebido.encode("utf-8"), esperado.encode("utf-8"))


def extrair_token(cabecalhos) -> str | None:
    """Token de "Authorization: Bearer <t>" ou "X-Oficina3D-Token: <t>". `cabecalhos`: dict com chaves minúsculas."""
    aut = (cabecalhos.get("authorization") or "").strip()
    if aut[:7].lower() == "bearer ":
        return aut[7:].strip() or None
    t = (cabecalhos.get("x-oficina3d-token") or "").strip()
    return t or None


# ---------------------------------------------------------------- pedido local x remoto
def _hostname(host_header: str) -> str:
    h = (host_header or "").strip().lower()
    if h.startswith("["):                       # [::1]:8765
        return h[1:h.find("]")] if "]" in h else h
    return h.rsplit(":", 1)[0] if h.count(":") == 1 else h


def pedido_local(cliente_host, cabecalhos, hosts_locais=HOSTS_LOOPBACK) -> bool:
    """O pedido veio MESMO deste PC, direto do navegador/cliente local?

    Exige as três coisas: conexão de 127.0.0.1/::1; nenhum cabeçalho de proxy/túnel (um túnel local,
    como Tailscale/Cloudflare, chega pelo 127.0.0.1 mas acrescenta esses cabeçalhos); e cabeçalho Host
    apontando para o próprio PC (barra o "DNS rebinding"). Qualquer outra coisa = remoto = exige token.
    """
    if not cliente_host or cliente_host not in hosts_locais:
        return False
    if any(cabecalhos.get(c) for c in CABECALHOS_PROXY):
        return False
    return _hostname(cabecalhos.get("host", "")) in (HOSTS_LOOPBACK | set(hosts_locais))


def origem_confere(cabecalhos) -> bool:
    """Para POST/PUT/DELETE: se o navegador mandou Origin, ela tem de ser o próprio servidor (contra CSRF)."""
    origem = (cabecalhos.get("origin") or "").strip().lower()
    if not origem:
        return True
    if origem == "null":
        return False
    sem_esquema = origem.split("://", 1)[-1]
    return sem_esquema == (cabecalhos.get("host") or "").strip().lower()


# ---------------------------------------------------------------- PID do worker
FILETIME_PARA_EPOCH_S = 11644473600  # segundos entre 1601-01-01 (FILETIME do Windows) e 1970-01-01


def filetime_para_epoch(ft) -> float:
    """FILETIME (intervalos de 100 ns desde 1601) -> segundos desde 1970 (a régua do psutil.create_time)."""
    return int(ft) / 10_000_000 - FILETIME_PARA_EPOCH_S


def ler_trava_worker(arquivo: Path) -> dict | None:
    """Lê o registro da trava do worker.

    Formatos aceitos:
    - v2 (oficina3d.travas, agente G): JSON {"pid": ..., "criado_em_processo": <FILETIME>, ...};
      arquivo vazio = o worker saiu limpo;
    - JSON {"pid": ..., "create_time": <segundos desde 1970>};
    - texto "PID [create_time]" (v1: só o PID).
    Devolve {"pid": int, "create_time": float|None (segundos desde 1970), "mtime": float} ou None se não
    existir / estiver vazio. Levanta ErroSeguranca se existir mas estiver ilegível (quem chama trata como
    "não sei").
    """
    try:
        bruto = Path(arquivo).read_bytes()
        mtime = Path(arquivo).stat().st_mtime
    except FileNotFoundError:
        return None
    except OSError:
        raise ErroSeguranca("trava do worker existe mas não pôde ser lida") from None
    try:
        texto = _decodificar_texto(bruto).split("\x00", 1)[0].strip()
    except UnicodeDecodeError:
        raise ErroSeguranca("trava do worker com conteúdo inválido") from None
    if not texto:
        return None
    try:
        d = json.loads(texto)
    except ValueError:
        d = None
    try:
        if d is None:                       # texto "PID [create_time]"
            partes = texto.split()
            pid = partes[0]
            ct = float(partes[1]) if len(partes) > 1 else None
        elif isinstance(d, dict):
            pid = d.get("pid")
            if d.get("create_time") is not None:
                ct = float(d["create_time"])
            elif d.get("criado_em_processo") is not None:
                ct = filetime_para_epoch(d["criado_em_processo"])
            else:
                ct = None
        else:
            raise TypeError
        if isinstance(pid, bool):
            raise TypeError
        pid = int(pid)
    except (TypeError, ValueError, IndexError):
        raise ErroSeguranca("trava do worker com conteúdo inválido") from None
    if pid <= 0:
        raise ErroSeguranca("trava do worker com PID inválido")
    return {"pid": pid, "create_time": ct, "mtime": mtime}


def _psutil():
    try:
        import psutil  # import preguiçoso: só quando precisa conferir PID
        return psutil
    except ImportError:
        return None


def processo_confere(pid: int, create_time: float | None, mtime_trava: float | None,
                     psutil_mod=None, tolerancia: float = 2.0) -> bool | None:
    """O processo `pid` é o worker que gravou a trava? True/False, ou None = não dá para saber.

    Nada de "PID por substring" (v1: tasklist + `str(pid) in saída`). Usa psutil e o horário de criação:
    - com create_time gravado na trava: o processo tem de ter sido criado nesse horário (± tolerância);
    - sem ele: o processo tem de ser MAIS VELHO que a trava (um PID reaproveitado nasceu depois dela).
    E o executável tem de ser um Python.
    """
    ps = psutil_mod if psutil_mod is not None else _psutil()
    if ps is None:
        return None
    try:
        proc = ps.Process(int(pid))
        criado = float(proc.create_time())
        nome = (proc.name() or "").lower()
    except ps.NoSuchProcess:
        return False
    except ps.AccessDenied:
        return None
    except Exception:
        return None
    if "python" not in nome:
        return False
    if create_time is not None:
        return abs(criado - float(create_time)) <= tolerancia
    if mtime_trava is not None:
        return criado <= float(mtime_trava) + tolerancia
    return None


def situacao_worker(arquivos_trava, psutil_mod=None) -> dict:
    """{"vivo": True|False|None, "pid": ..., "motivo": "..."} olhando as travas na ordem dada."""
    for arq in arquivos_trava:
        try:
            t = ler_trava_worker(arq)
        except ErroSeguranca as e:
            return {"vivo": None, "pid": None, "motivo": str(e), "trava": str(arq)}
        if t is None:
            continue
        ok = processo_confere(t["pid"], t["create_time"], t["mtime"], psutil_mod=psutil_mod)
        motivo = {True: "processo confere (PID + horário de criação)",
                  False: "trava velha: o PID não existe mais ou é de outro processo",
                  None: "não deu para conferir o PID (psutil ausente ou acesso negado)"}[ok]
        return {"vivo": ok, "pid": t["pid"], "motivo": motivo, "trava": str(arq)}
    return {"vivo": False, "pid": None, "motivo": "sem trava do worker"}


# ---------------------------------------------------------------- ASGI: token obrigatório
class MiddlewareToken:
    """Envolve um app ASGI e exige token em TODO pedido HTTP. Sem token configurado: recusa tudo.

    Usado no MCP por HTTP (streamable-http). Pedidos que não são "http" (ex.: lifespan) passam direto.
    """

    def __init__(self, app, token: str | None):
        self.app = app
        self.token = token

    async def __call__(self, scope, receive, send):
        if scope.get("type") != "http":
            return await self.app(scope, receive, send)
        cab = {k.decode("latin-1").lower(): v.decode("latin-1") for k, v in scope.get("headers") or []}
        if not self.token:
            return await _responder(send, 503, "servidor sem token configurado: acesso HTTP recusado")
        if not token_confere(extrair_token(cab), self.token):
            return await _responder(send, 401, "token ausente ou errado")
        return await self.app(scope, receive, send)


async def _responder(send, status: int, msg: str):
    corpo = json.dumps({"erro": msg}, ensure_ascii=False).encode("utf-8")
    cab = [(b"content-type", b"application/json; charset=utf-8"), (b"content-length", str(len(corpo)).encode())]
    if status == 401:
        cab.append((b"www-authenticate", b'Bearer realm="oficina3d"'))
    await send({"type": "http.response.start", "status": status, "headers": cab})
    await send({"type": "http.response.body", "body": corpo})
