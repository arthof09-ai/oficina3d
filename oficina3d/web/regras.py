"""Regras da página web que não dependem do FastAPI (testáveis só com a biblioteca padrão).

- decidir_acesso: pedido local (127.0.0.1 de verdade) passa; qualquer outro precisa de token
  (Authorization: Bearer, X-Oficina3D-Token ou o cookie criado por "/?token=..."); sem token configurado,
  remoto é recusado. POST/PUT/DELETE exigem o cabeçalho X-Oficina3D: 1 e Origin igual ao Host (CSRF).
- validar_nota: nota do Mestre (0 a 10) + comentário curto.
- tipo_para_servir: tipo MIME e se o arquivo pode abrir no navegador (inline) ou só baixar.
- resumo_job: o que a fila e a galeria mostram.
"""
from __future__ import annotations

import re

from ..mcp import seguranca as seg

COOKIE_TOKEN = "oficina3d_token"
CABECALHO_CSRF = "x-oficina3d"
METODOS_SEGUROS = frozenset({"GET", "HEAD", "OPTIONS"})
LIMITE_PEDIDO = (seg.MAX_IMAGENS + 1) * seg.LIMITE_BYTES + 1024 * 1024   # 12 imagens + 1 malha + folga
NOTA_MIN, NOTA_MAX = 0, 10
COMENTARIO_MAX = 2000

CSP = ("default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; "
       "img-src 'self' data: blob:; connect-src 'self' data: blob:; worker-src 'self' blob:; "
       "object-src 'none'; base-uri 'none'; form-action 'self'; frame-ancestors 'none'")
CABECALHOS_SEGURANCA = {
    "Content-Security-Policy": CSP,
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "no-referrer",
    "X-Frame-Options": "DENY",
    "Cross-Origin-Opener-Policy": "same-origin",
}


def decidir_acesso(local: bool, cabecalhos, metodo: str, token_configurado: str | None,
                   cookie_token: str | None = None) -> tuple[int, str | None]:
    """(0, None) = pode seguir; senão (status HTTP, motivo). `cabecalhos`: dict com chaves minúsculas."""
    if not local:
        if not token_configurado:
            return 403, "acesso de fora deste PC exige token, e nenhum token está configurado"
        recebido = seg.extrair_token(cabecalhos) or cookie_token
        if not seg.token_confere(recebido, token_configurado):
            return 401, "token ausente ou errado"
    if metodo.upper() not in METODOS_SEGUROS:
        if (cabecalhos.get(CABECALHO_CSRF) or "").strip() != "1":
            return 403, "pedido sem o cabeçalho X-Oficina3D (proteção contra CSRF)"
        if not seg.origem_confere(cabecalhos):
            return 403, "a origem do pedido não confere com este servidor"
    cl = cabecalhos.get("content-length")
    if cl:
        try:
            if int(cl) > LIMITE_PEDIDO:
                return 413, f"pedido grande demais (limite {LIMITE_PEDIDO // 2**20} MB)"
        except ValueError:
            return 400, "Content-Length inválido"
    return 0, None


_RE_CONTROLE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def validar_nota(nota, comentario) -> dict:
    """Confere a nota do Mestre. nota: inteiro 0–10 ou None; comentário: texto até 2000 caracteres.
    Pelo menos um dos dois. Levanta ErroSeguranca (ValueError) com o motivo."""
    if nota is not None and nota != "":
        if isinstance(nota, bool):
            raise seg.ErroSeguranca("nota: inteiro de 0 a 10")
        try:
            n = int(nota)
        except (TypeError, ValueError):
            raise seg.ErroSeguranca("nota: inteiro de 0 a 10") from None
        if isinstance(nota, float) and not nota.is_integer():
            raise seg.ErroSeguranca("nota: inteiro de 0 a 10")
        if not NOTA_MIN <= n <= NOTA_MAX:
            raise seg.ErroSeguranca("nota: inteiro de 0 a 10")
    else:
        n = None
    if comentario is None:
        c = ""
    elif isinstance(comentario, str):
        c = _RE_CONTROLE.sub("", comentario).strip()
    else:
        raise seg.ErroSeguranca("comentário precisa ser texto")
    if len(c) > COMENTARIO_MAX:
        raise seg.ErroSeguranca(f"comentário longo demais (máximo {COMENTARIO_MAX} caracteres)")
    if n is None and not c:
        raise seg.ErroSeguranca("mande a nota (0 a 10) ou um comentário")
    return {"nota": n, "comentario": c}


_MIME = {
    ".png": ("image/png", True), ".jpg": ("image/jpeg", True), ".jpeg": ("image/jpeg", True),
    ".webp": ("image/webp", True), ".glb": ("model/gltf-binary", True),
    ".json": ("application/json; charset=utf-8", True), ".txt": ("text/plain; charset=utf-8", True),
    ".log": ("text/plain; charset=utf-8", True), ".obj": ("text/plain; charset=utf-8", False),
}


def tipo_para_servir(nome: str) -> tuple[str, bool]:
    """(tipo MIME, inline?). HTML/SVG/JS e desconhecidos saem como download (octet-stream), nunca abrem."""
    ext = ("." + nome.rsplit(".", 1)[-1].lower()) if "." in nome else ""
    return _MIME.get(ext, ("application/octet-stream", False))


def resumo_job(j: dict) -> dict:
    r = {k: j.get(k) for k in ("id", "nome", "modo", "estado", "etapa", "progresso", "erro", "avisos", "criado_em")}
    r["motor"] = (j.get("opcoes") or {}).get("motor")
    res = j.get("resultado") or {}
    r["resultado"] = {"glb": res.get("glb"), "glb_cru": res.get("glb_cru"), "previas": list(res.get("previas") or []),
                      "relatorio": res.get("relatorio")} if res else None
    r["nota_mestre"] = j.get("nota_mestre")
    return r
