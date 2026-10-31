"""API HTTP e página da Oficina 3D (FastAPI). Só cria e acompanha jobs; quem processa é o worker.

Rotas:
  GET  /                                  página (static/index.html)
  GET  /static/...                        css/js da página e static/vendor/ (model-viewer, offline)
  GET  /api/config                        vistas, modos, motores, limites
  GET  /api/motores                       motores.listar() + tempo estimado do contrato
  GET  /api/jobs                          resumo de todos (mais novo primeiro)
  POST /api/jobs                          multipart: imagens[] + vistas[] (paralela) + modo, motor, passos,
                                          alvo_triangulos, simetrizar, nome, malha (so-refinar)
  GET  /api/jobs/{id}                     job.json completo
  POST /api/jobs/{id}/cancelar            só pendente/processando
  POST /api/jobs/{id}/nota                {"nota": 0-10, "comentario": "..."} -> job.json["nota_mestre"]
  GET  /api/jobs/{id}/arquivos            lista os arquivos do job
  GET  /api/jobs/{id}/arquivo/{caminho}   um arquivo de dentro da pasta do job (nada fora dela)
  GET  /api/jobs/{id}/zip                 saida\\ zipada
  GET  /api/galeria                       jobs concluídos com prévia, GLB e nota
  GET  /api/saude                         GPU, disco, worker (mesma função do MCP)

Segurança (oficina3d.mcp.seguranca + web.regras): só 127.0.0.1; pedido não local exige token; POST exige
X-Oficina3D: 1 e Origin igual ao Host; id validado; caminhos resolvidos e presos à pasta do job; tipo real
dos uploads pelos primeiros bytes; 40 MB por arquivo; cabeçalhos CSP/nosniff.
"""
import io
import os
import shutil
import urllib.parse
import uuid
import zipfile
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse, Response

from . import VERSAO, regras
from ..mcp import seguranca as seg
from ..mcp.seguranca import ErroSeguranca

PASTA_STATIC = Path(__file__).resolve().parent / "static"
LIMITE_ZIP = 300 * 1024 * 1024
BLOCO = 1024 * 1024

# Tempo estimado (contrato e medidas da v1 na GTX 1660 SUPER; a medir na v2).
TEMPOS = {
    "hunyuan-mini": "~3,6 min (v1)",
    "hunyuan-mini-turbo": "~4 min (v1)",
    "hunyuan-mv": "~35 min com 4 vistas (v1)",
    "hunyuan-mv-turbo": "~6 min com 4 vistas (v1)",
    "triposr": "~1 min (v1)",
}


def _http(status: int, msg: str):
    return HTTPException(status_code=status, detail=msg)


def criar_app(config_mod=None, jobs_mod=None, hosts_locais=None, token=None, saude_fn=None) -> FastAPI:
    """Monta o app. Os parâmetros servem aos testes (módulos falsos, host do TestClient, token fixo)."""
    if config_mod is None:
        from .. import config as config_mod
    if jobs_mod is None:
        from .. import job as jobs_mod
    cfg, jobs = config_mod, jobs_mod
    locais = frozenset(hosts_locais) if hosts_locais else seg.HOSTS_LOOPBACK
    vistas_validas = tuple(getattr(cfg, "VISTAS", ()))
    modos_validos = tuple(getattr(cfg, "MODOS", ()))

    def pasta_jobs() -> Path:
        return Path(cfg.JOBS).resolve()

    def pasta_tmp() -> Path:
        return Path(getattr(cfg, "TMP", Path(cfg.BASE) / "_cache" / "tmp"))

    def pasta_locks() -> Path:
        return Path(getattr(cfg, "LOCKS", Path(cfg.BASE) / "locks"))

    app = FastAPI(title="Oficina 3D", version=VERSAO,
                  description="API local da Oficina 3D (só 127.0.0.1). Ver docs/USO_PARA_IAS.md.")

    # ------------------------------------------------------------ porteiro (token, CSRF, tamanho, cabeçalhos)
    def _cabecalhos(resp: Response, sem_cache: bool) -> Response:
        for k, v in regras.CABECALHOS_SEGURANCA.items():
            resp.headers.setdefault(k, v)
        if sem_cache:
            resp.headers["Cache-Control"] = "no-cache"
        return resp

    @app.middleware("http")
    async def porteiro(request: Request, call_next):
        cab = {k.lower(): v for k, v in request.headers.items()}
        cliente = request.client.host if request.client else None
        local = seg.pedido_local(cliente, cab, locais)
        token_cfg = None
        if not local:
            token_cfg = token if token is not None else seg.ler_token(pasta_locks())
            q = request.query_params.get("token")
            if request.method == "GET" and request.url.path == "/" and q is not None:
                if seg.token_confere(q, token_cfg):
                    # troca o token da URL por um cookie HttpOnly e tira o token da barra de endereço
                    resp = RedirectResponse("/", status_code=303)
                    https = (cab.get("x-forwarded-proto") or request.url.scheme) == "https"
                    resp.set_cookie(regras.COOKIE_TOKEN, q, httponly=True, samesite="strict", secure=https,
                                    max_age=7 * 24 * 3600)
                    return _cabecalhos(resp, True)
        status, motivo = regras.decidir_acesso(local, cab, request.method, token_cfg,
                                               request.cookies.get(regras.COOKIE_TOKEN))
        if status:
            return _cabecalhos(JSONResponse({"detail": motivo}, status_code=status), True)
        resp = await call_next(request)
        p = request.url.path
        return _cabecalhos(resp, p == "/" or p.startswith("/static/") or p.startswith("/api/"))

    # ------------------------------------------------------------ utilidades
    def job_seguro(job_id: str):
        try:
            seg.validar_id(job_id)
            raiz = Path(jobs.pasta_job(job_id)).resolve()
        except ValueError as e:
            raise _http(400, str(e))
        if not seg._dentro(raiz, pasta_jobs()) or raiz == pasta_jobs():
            raise _http(400, "pasta do job fora da pasta de jobs")
        try:
            j = jobs.ler_job(job_id)
        except FileNotFoundError:
            raise _http(404, f"job não encontrado: {job_id}")
        except ValueError as e:
            raise _http(500, str(e))
        return j, raiz

    def alterar(job_id: str, func) -> dict:
        if hasattr(jobs, "atualizar_job"):
            return jobs.atualizar_job(job_id, func)   # trava do job + job.salvar_job
        j = jobs.ler_job(job_id)
        novo = func(j)
        j = novo if novo is not None else j
        jobs.salvar_job(j)
        return j

    def vista_pelo_nome(nome: str):
        try:
            from ..entrada import vista_pelo_nome as f
        except Exception:
            try:
                from ..entrada.vistas import vista_pelo_nome as f
            except Exception:
                return None
        try:
            v = f(nome)
            return v if v in vistas_validas else None
        except Exception:
            return None

    async def salvar_upload(up: UploadFile, pasta: Path, tipos, usados: set) -> Path:
        """Grava o upload em blocos, com limite de 40 MB, e confere o tipo real pelos primeiros bytes."""
        parcial = pasta / f"_{uuid.uuid4().hex}.part"
        total, cabeca = 0, b""
        with open(parcial, "wb") as f:
            while True:
                bloco = await up.read(BLOCO)
                if not bloco:
                    break
                total += len(bloco)
                if total > seg.LIMITE_BYTES:
                    raise _http(413, f"{up.filename}: arquivo grande demais (limite {seg.LIMITE_BYTES // 2**20} MB)")
                if len(cabeca) < 4096:
                    cabeca += bloco[:4096 - len(cabeca)]
                f.write(bloco)
        if total == 0:
            raise _http(422, f"{up.filename}: arquivo vazio")
        tipo = seg.tipo_por_assinatura(cabeca)
        if tipo not in tipos:
            raise _http(422, f"{up.filename}: tipo não aceito (aceitos: {', '.join(sorted(tipos))})")
        nome = seg.nome_seguro(up.filename, tipo, padrao="imagem")
        destino, n = pasta / nome, 1
        while destino.name.lower() in usados:
            n += 1
            destino = pasta / f"{Path(nome).stem}_{n}{Path(nome).suffix}"
        usados.add(destino.name.lower())
        os.replace(parcial, destino)
        return destino

    def inteiro(nome: str, valor: str, lo: int, hi: int):
        if valor is None or str(valor).strip() == "":
            return None
        try:
            v = int(str(valor).strip())
        except ValueError:
            raise _http(422, f"{nome}: precisa ser número inteiro")
        if not lo <= v <= hi:
            raise _http(422, f"{nome}: entre {lo} e {hi}")
        return v

    # ------------------------------------------------------------ página
    @app.get("/", include_in_schema=False)
    def pagina():
        return FileResponse(PASTA_STATIC / "index.html", media_type="text/html; charset=utf-8")

    from fastapi.staticfiles import StaticFiles
    app.mount("/static", StaticFiles(directory=str(PASTA_STATIC)), name="static")

    # ------------------------------------------------------------ API
    @app.get("/api/config")
    def api_config():
        return {"versao": VERSAO, "vistas": list(vistas_validas), "modos": list(modos_validos),
                "motores": list(getattr(cfg, "MOTORES", ())),
                "motor_padrao_uma_vista": getattr(cfg, "MOTOR_PADRAO_UMA_VISTA", None),
                "motor_padrao_multivista": getattr(cfg, "MOTOR_PADRAO_MULTIVISTA", None),
                "max_imagens": seg.MAX_IMAGENS, "limite_mb": seg.LIMITE_BYTES // 2**20,
                "nota_min": regras.NOTA_MIN, "nota_max": regras.NOTA_MAX}

    @app.get("/api/motores")
    def api_motores():
        try:
            from .. import motores
            lista = [dict(m) for m in motores.listar()]
        except Exception:
            lista = [{"nome": n, "descricao": "", "aceita_multivista": n in getattr(cfg, "MOTORES_MULTIVISTA", ()),
                      "disponivel": None} for n in getattr(cfg, "MOTORES", ())]
        for m in lista:
            m.setdefault("tempo_estimado", TEMPOS.get(m.get("nome")))
        return lista

    @app.get("/api/jobs")
    def api_jobs():
        return [regras.resumo_job(j) for j in jobs.listar_jobs()][::-1]

    @app.post("/api/jobs", status_code=201)
    async def api_criar(imagens: Optional[List[UploadFile]] = File(None),
                        vistas: Optional[List[str]] = Form(None),
                        modo: str = Form("livre"), motor: str = Form(""), passos: str = Form(""),
                        alvo_triangulos: str = Form(""), simetrizar: str = Form(""), nome: str = Form(""),
                        malha: Optional[UploadFile] = File(None)):
        imagens = [u for u in (imagens or []) if u is not None and u.filename]
        vistas = list(vistas or [])
        if modo not in modos_validos:
            raise _http(422, f"modo inválido: {modo}")
        if len(imagens) > seg.MAX_IMAGENS:
            raise _http(422, f"no máximo {seg.MAX_IMAGENS} imagens")
        if vistas and len(vistas) != len(imagens):
            raise _http(422, "'vistas' precisa ter um item por imagem (vazio = descobrir pelo nome)")
        for v in vistas:
            if v and v not in vistas_validas:
                raise _http(422, f"vista inválida: {v}")
        tem_malha = malha is not None and bool(malha.filename)
        if modo == "so-refinar" and not tem_malha:
            raise _http(422, "o modo so-refinar precisa de uma malha (.glb/.obj)")
        if tem_malha and modo != "so-refinar":
            raise _http(422, "malha só vale no modo so-refinar")
        if modo != "so-refinar" and not imagens:
            raise _http(422, "mande pelo menos uma imagem")
        nome = (nome or "").strip()
        if len(nome) > 60:
            raise _http(422, "nome: até 60 caracteres")
        opcoes = {"simetrizar": str(simetrizar).strip().lower() in ("1", "true", "sim", "on")}
        if motor.strip():
            if getattr(cfg, "MOTORES", None) and motor.strip() not in cfg.MOTORES:
                raise _http(422, f"motor desconhecido: {motor}")
            opcoes["motor"] = motor.strip()
        v = inteiro("passos", passos, 1, 100)
        if v is not None:
            opcoes["passos"] = v
        v = inteiro("alvo_triangulos", alvo_triangulos, 1000, 1_000_000)
        if v is not None:
            opcoes["alvo_triangulos"] = v

        tmp = pasta_tmp() / f"upload_{uuid.uuid4().hex[:12]}"
        tmp.mkdir(parents=True, exist_ok=False)
        try:
            usados: set = set()
            arquivos = []
            for i, up in enumerate(imagens):
                p = await salvar_upload(up, tmp, seg.TIPOS_IMAGEM, usados)
                vista = (vistas[i] if vistas else "") or vista_pelo_nome(up.filename or "")
                arquivos.append((p, vista or None))
            malha_p = await salvar_upload(malha, tmp, seg.TIPOS_MALHA, usados) if tem_malha else None
            try:
                j = jobs.criar_job(arquivos, modo=modo, opcoes=opcoes, nome=nome or None, malha=malha_p)
            except ValueError as e:
                raise _http(422, str(e))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        return regras.resumo_job(j)

    @app.get("/api/jobs/{job_id}")
    def api_job(job_id: str):
        j, _ = job_seguro(job_id)
        return j

    @app.post("/api/jobs/{job_id}/cancelar")
    def api_cancelar(job_id: str):
        job_seguro(job_id)
        recusado = {}

        def cancelar(j):
            if j.get("estado") not in ("pendente", "processando"):
                recusado["estado"] = j.get("estado")
                return None
            j["estado"] = "cancelado"
            jobs.registrar(j, None, "cancelado pela página", salvar=False)
            return None

        try:
            alterar(job_id, cancelar)
        except TimeoutError as e:
            raise _http(409, str(e))
        if recusado:
            raise _http(409, f"só cancela pendente/processando (estado: {recusado['estado']})")
        return {"id": job_id, "estado": "cancelado", "cancelado": True}

    @app.post("/api/jobs/{job_id}/nota")
    async def api_nota(job_id: str, request: Request):
        job_seguro(job_id)
        try:
            corpo = await request.json()
        except Exception:
            raise _http(422, "mande JSON: {\"nota\": 0-10, \"comentario\": \"...\"}")
        if not isinstance(corpo, dict):
            raise _http(422, "mande um objeto JSON")
        try:
            nota = regras.validar_nota(corpo.get("nota"), corpo.get("comentario"))
        except ErroSeguranca as e:
            raise _http(422, str(e))
        quando = jobs.agora() if hasattr(jobs, "agora") else None
        nota["quando"] = quando

        def gravar(j):
            j["nota_mestre"] = nota
            msg = "nota do Mestre: " + (f"{nota['nota']}/10" if nota["nota"] is not None else "comentário")
            jobs.registrar(j, None, msg, salvar=False)
            return None

        try:
            alterar(job_id, gravar)
        except TimeoutError as e:
            raise _http(409, str(e))
        return {"id": job_id, "nota_mestre": nota}

    @app.get("/api/jobs/{job_id}/arquivos")
    def api_arquivos(job_id: str):
        _, raiz = job_seguro(job_id)
        lista = []
        for p in sorted(raiz.rglob("*")):
            if not p.is_file() or p.name.endswith((".tmp", ".lock", ".part")):
                continue
            real = p.resolve()
            if not seg._dentro(real, raiz):
                continue   # link que sai da pasta: nem aparece
            lista.append({"caminho": p.relative_to(raiz).as_posix(), "bytes": p.stat().st_size})
        return lista

    @app.get("/api/jobs/{job_id}/arquivo/{caminho:path}")
    def api_arquivo(job_id: str, caminho: str):
        _, raiz = job_seguro(job_id)
        try:
            p = seg.caminho_dentro(raiz, caminho)
        except ErroSeguranca as e:
            raise _http(404 if "não encontrado" in str(e) else 400, str(e))
        if not p.is_file():
            raise _http(404, "não é um arquivo")
        mime, inline = regras.tipo_para_servir(p.name)
        disp = "inline" if inline else "attachment"
        return FileResponse(p, media_type=mime, headers={
            "Content-Disposition": f"{disp}; filename*=UTF-8''{urllib.parse.quote(p.name)}"})

    @app.get("/api/jobs/{job_id}/zip")
    def api_zip(job_id: str):
        _, raiz = job_seguro(job_id)
        saida = raiz / "saida"
        arquivos = [p for p in sorted(saida.rglob("*")) if p.is_file() and seg._dentro(p.resolve(), raiz)] \
            if saida.is_dir() else []
        if not arquivos:
            raise _http(404, "a pasta saida está vazia")
        if sum(p.stat().st_size for p in arquivos) > LIMITE_ZIP:
            raise _http(413, "saida grande demais para zipar pela página; copie a pasta direto")
        buf = io.BytesIO()
        with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
            for p in arquivos:
                z.write(p, f"{job_id}/{p.relative_to(saida).as_posix()}")
        return Response(buf.getvalue(), media_type="application/zip", headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{urllib.parse.quote(job_id)}.zip"})

    @app.get("/api/galeria")
    def api_galeria():
        itens = []
        for j in reversed(jobs.listar_jobs()):
            if j.get("estado") != "concluido" or not j.get("resultado"):
                continue
            r = regras.resumo_job(j)
            itens.append({"id": r["id"], "nome": r["nome"], "criado_em": r["criado_em"], "motor": r["motor"],
                          "glb": r["resultado"]["glb"], "previas": r["resultado"]["previas"],
                          "nota_mestre": r["nota_mestre"]})
        return itens

    @app.get("/api/saude")
    def api_saude():
        if saude_fn is not None:
            return saude_fn()
        from ..mcp import servidor
        s = servidor.saude()
        s["versao_web"] = VERSAO
        return s

    return app
