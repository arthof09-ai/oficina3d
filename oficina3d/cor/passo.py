"""Etapa `cor` da fila de jobs (integracao T1+T5, COR-05).

Encadeia, dentro de um job, exatamente a cadeia ja provada fora da fila
(T5 + D-T5-1, ver docs/REGISTRO.md):

    1. ``oficina3d.uv_xatlas.gerar_uv`` sobre o GLB refinado -> ``cor/uv.npz``
       (padding 8 em 2048, o padrao D-T5-1);
    2. ``cor/_blender_uv_xatlas.py`` via ``refino.previa.rodar_blender`` ->
       ``cor/modelo_uv.glb``, com a guarda de ocupacao ligada
       (``ocupacao_esperada`` + tolerancia, e a checagem duplicada aqui);
    3. ``cor.rodar_cor`` (bake T1) sobre o GLB com UV nova ->
       ``cor/modelo_cor.glb`` + ``cor/textura.png`` + ``cor/previas/``.

Regras da v1 (COR-05, reversiveis, registradas para auditoria):

- O passo usa SO as 4 vistas canonicas (frente/costas/esquerda/direita).
  Diagonais, cima e outras etiquetas presentes no job sao IGNORADAS
  (registradas em ``vistas_ignoradas``) e nao entram no bake: o caminho
  provado e o de 4 vistas, e ampliar o conjunto exige nova prova.
- Sem nenhuma vista canonica utilizavel, o passo FALHA (ValueError) em
  vez de entregar um modelo sem cor em silencio. A etapa e opcional no
  job (opcao ``cor``, padrao False); quando o usuario a liga, a falta
  de insumo e erro do job, nao fallback silencioso.
- A S2-3 (suspeita de troca esquerda/direita nas imagens da Besta)
  NAO e resolvida aqui: o bake usa as etiquetas do job como estao.
  A prova desta tranche usa o Orc, fora do alcance da S2-3.
- Nada aqui muda o refino nem a forma: o GLB refinado continua intacto
  em ``saida/modelo_sem_cor.glb`` quando a cor roda (o worker copia o
  colorido para ``saida/modelo.glb``); sem ``cor``, o worker nao toca
  em nada novo.

``selecionar_vistas`` e pura (testavel sem Blender nem GPU); o resto
orquestra os dois lados ja provados (``.venv_app`` + Blender headless).
"""
from __future__ import annotations

from pathlib import Path

AQUI = Path(__file__).resolve().parent
SCRIPT_UV = AQUI / "_blender_uv_xatlas.py"

VISTAS_COR = ("frente", "costas", "esquerda", "direita")
TOLERANCIA_OCUPACAO = 0.02
TAMANHO_TEXTURA = 1024
DILATACAO = 256
TIMEOUT_UV_S = 900
TIMEOUT_BAKE_S = 1800


def _rel(job_dir: Path, caminho) -> str:
    """Caminho relativo a pasta do job quando possivel (senao, absoluto)."""
    p = Path(caminho)
    try:
        return p.resolve().relative_to(job_dir.resolve()).as_posix()
    except (ValueError, OSError):
        return str(p)


def selecionar_vistas(imagens, job_dir=None):
    """Separa as vistas canonicas utilizaveis pelo bake.

    ``imagens``: entradas do job (``{"arquivo", "vista"}``), vindas do
    preproc quando houver etapa de entrada, ou da criacao do job no
    modo so-refinar. ``arquivo`` pode ser relativo a ``job_dir``.

    Devolve ``(vistas, ausentes, ignoradas)``: ``vistas`` e a lista
    ``[{"vista", "arquivo"}]`` na ordem de VISTAS_COR (primeira ocorrencia
    vence em caso de duplicata); ``ausentes`` sao as canonicas sem imagem;
    ``ignoradas`` sao as etiquetas presentes que o bake v1 nao usa.
    Levanta ValueError sem nenhuma vista canonica, ou com arquivo
    ausente/ilegivel para uma vista canonica.
    """
    por_vista: dict[str, str] = {}
    ignoradas: list[str] = []
    for im in imagens or []:
        vista = (im or {}).get("vista")
        if vista is None:
            continue
        if vista not in VISTAS_COR:
            if vista not in ignoradas:
                ignoradas.append(vista)
            continue
        if vista in por_vista:
            continue
        p = Path((im or {}).get("arquivo") or "")
        if job_dir is not None and not p.is_absolute():
            p = Path(job_dir) / p
        if not p.is_file():
            raise ValueError(f"vista {vista!r}: imagem nao encontrada: {p}")
        por_vista[vista] = str(p)
    vistas = [{"vista": v, "arquivo": por_vista[v]} for v in VISTAS_COR if v in por_vista]
    if not vistas:
        raise ValueError("etapa cor sem nenhuma vista canonica "
                         "(frente/costas/esquerda/direita) nas imagens do job")
    ausentes = [v for v in VISTAS_COR if v not in por_vista]
    return vistas, ausentes, ignoradas


def rodar_passo_cor(job_dir, glb_refinado, imagens, pasta_cor=None, progresso=None):
    """Roda UV xatlas + bake COR; devolve o resumo da etapa (JSONavel).

    ``progresso`` segue o contrato ``progresso(pct, msg)`` do worker
    (pode ser None). Erros do Blender chegam como ErroBlender; falta de
    insumo, como ValueError; divergencia de ocupacao, como RuntimeError.
    """
    from oficina3d import uv_xatlas  # noqa: PLC0415 - import pesado so quando a etapa roda
    from oficina3d.cor import rodar_cor  # noqa: PLC0415
    from oficina3d.refino import previa  # noqa: PLC0415

    job_dir = Path(job_dir)
    glb_refinado = Path(glb_refinado)
    if not glb_refinado.is_file():
        raise ValueError(f"etapa cor: GLB refinado nao encontrado: {glb_refinado}")
    pasta_cor = Path(pasta_cor) if pasta_cor is not None else job_dir / "cor"
    pasta_cor.mkdir(parents=True, exist_ok=True)

    vistas, ausentes, ignoradas = selecionar_vistas(imagens, job_dir)

    def avisar(pct, msg):
        if progresso is not None:
            progresso(pct, msg)

    avisar(5, "cor: gerando UV xatlas")

    def _progresso_uv(pct, msg):
        # Mapeia o progresso interno da UV (0-100) para a janela 5-30
        # da etapa cor; cada chamada passa pelo _Progresso do worker,
        # que confere o cancelamento no disco (D-COR05-1).
        avisar(5 + (int(pct) * 25) // 100, f"cor: UV xatlas {msg}")

    met_uv = uv_xatlas.gerar_uv(glb_refinado, pasta_cor / "uv.npz", progresso=_progresso_uv)
    avisar(30, f"cor: UV xatlas pronta (ocupacao {met_uv.get('ocupacao')})")

    modelo_uv = pasta_cor / "modelo_uv.glb"
    pedido_uv = {"glb": str(glb_refinado), "npz": str(pasta_cor / "uv.npz"),
                 "saida_glb": str(modelo_uv),
                 "ocupacao_esperada": met_uv["ocupacao"],
                 "tolerancia_ocupacao": TOLERANCIA_OCUPACAO}
    res_uv = previa.rodar_blender(SCRIPT_UV, pedido_uv, pasta_cor, "uv_xatlas",
                                  progresso=progresso, timeout_s=TIMEOUT_UV_S)
    if not modelo_uv.is_file():
        raise RuntimeError(f"etapa cor: Blender UV nao entregou {modelo_uv}")
    ocup_blender = (res_uv.get("metricas_uv") or {}).get("ocupacao")
    if ocup_blender is None or abs(float(ocup_blender) - float(met_uv["ocupacao"])) > TOLERANCIA_OCUPACAO:
        raise RuntimeError(f"etapa cor: ocupacao Blender {ocup_blender} diverge da "
                           f"xatlas {met_uv['ocupacao']} (tol {TOLERANCIA_OCUPACAO})")
    avisar(60, "cor: UV aplicada no Blender")

    pasta_previas = pasta_cor / "previas"
    modelo_cor = pasta_cor / "modelo_cor.glb"
    textura = pasta_cor / "textura.png"
    pedido_cor = {"modo": "glb", "glb": str(modelo_uv), "tamanho": TAMANHO_TEXTURA,
                  "dilatacao": DILATACAO, "vistas": vistas,
                  "saida_glb": str(modelo_cor), "saida_textura": str(textura),
                  "pasta_previas": str(pasta_previas),
                  "previas": [v["vista"] for v in vistas]}
    res_cor = rodar_cor(pedido_cor, pasta_cor, progresso=progresso, timeout_s=TIMEOUT_BAKE_S)
    if not modelo_cor.is_file() or not textura.is_file():
        raise RuntimeError("etapa cor: bake nao entregou modelo_cor.glb + textura.png")
    avisar(100, "cor: bake pronto")

    previas = [_rel(job_dir, p) for p in (res_cor.get("previas") or [])]
    return {"vistas_usadas": [v["vista"] for v in vistas],
            "vistas_ausentes": ausentes,
            "vistas_ignoradas": ignoradas,
            "metricas_uv": met_uv,
            "resultado_uv": res_uv,
            "resultado_cor": res_cor,
            "arquivos": {"uv_npz": _rel(job_dir, pasta_cor / "uv.npz"),
                         "modelo_uv": _rel(job_dir, modelo_uv),
                         "modelo_cor": _rel(job_dir, modelo_cor),
                         "textura": _rel(job_dir, textura),
                         "previas": previas}}
