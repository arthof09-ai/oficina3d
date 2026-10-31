"""Refino da Oficina 3D: malha crua do motor -> modelo entregável + prévias + nota de silhueta.

Contrato (docs/ARQUITETURA.md):

    refinar(glb_entrada, pasta_trabalho, pasta_saida, opcoes, imagens=None, progresso=None) -> dict
      grava pasta_saida/modelo.glb e pasta_saida/previa_<vista>.png
      -> {"glb": Path, "previas": [Path], "silhueta_iou": {"frente": 0.91, ...},
          "nota_iou": 0.8, "iou_lateral": ..., "iou_costas": ...,
          "metricas": {"triangulos_antes", "triangulos_depois", "fechada", "altura", "pivo": "pes", ...},
          "avisos": [...]}

Passos (como a v1): limpar (duplicados, degenerados, pedaços soltos) -> fechar buracos ->
decimação quadrática até ``alvo_triangulos`` (padrão 50.000) -> normalizar (Y para cima,
frente +Z, altura 1,0 ou ``altura_m``, pivô nos pés) -> simetrizar (opcional) -> UV
automático -> exportar GLB -> reabrir no Blender e renderizar prévias -> IoU de silhueta.

Limpeza/decimação: pymeshlab + trimesh quando instalados (``backend_malha="auto"``),
senão o próprio Blender (bmesh + modificador Decimate). Dependências pesadas são
importadas só quando usadas. Opções extras aceitas em ``opcoes`` (todas opcionais):
``backend_malha`` ("auto" | "pymeshlab" | "blender"), ``uv`` (True), ``salvar_blend`` (False),
``orientacao_entrada`` ("gltf" | "triposr"), ``girar_graus`` (0), ``min_componente_frac``
(0.005), ``max_lados_buraco`` (1000), ``previas`` (lista de vistas), ``timeout_blender_s`` (900).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from . import malha, previa, silhueta

__all__ = ["refinar", "ErroRefino"]

ALVO_PADRAO = 50000


class ErroRefino(RuntimeError):
    """Falha do refino, com mensagem em português."""


def _avisar(progresso, pct, msg):
    if progresso:
        try:
            progresso(int(pct), msg)
        except Exception:  # noqa: BLE001 — progresso nunca derruba o refino
            pass


def _resolver_imagens(imagens, pasta_trabalho: Path, avisos: list) -> list[dict]:
    """Uma imagem por vista (só as 8 direções), com caminho absoluto existente."""
    escolhidas: dict[str, dict] = {}
    for item in imagens or []:
        vista = (item or {}).get("vista")
        arq = (item or {}).get("arquivo")
        if not vista or not arq or vista not in silhueta.VISTAS_IOU:
            continue
        p = Path(arq)
        if not p.is_absolute():
            # Caminho relativo à pasta do job (pasta_trabalho = <job>\refino).
            p = pasta_trabalho.parent / p
        if not p.is_file():
            avisos.append(f"imagem da vista {vista} não encontrada: {p}")
            continue
        if vista in escolhidas:
            avisos.append(f"mais de uma imagem para a vista {vista}; usei a primeira")
            continue
        escolhidas[vista] = {"vista": vista, "arquivo": str(p.resolve())}
    return list(escolhidas.values())


def refinar(glb_entrada, pasta_trabalho, pasta_saida, opcoes: dict | None = None,
            imagens: list[dict] | None = None, progresso=None) -> dict:
    t_inicio = time.perf_counter()
    opcoes = dict(opcoes or {})
    glb_entrada = Path(glb_entrada)
    pasta_trabalho = Path(pasta_trabalho)
    pasta_saida = Path(pasta_saida)
    if not glb_entrada.is_file():
        raise ErroRefino(f"malha de entrada não encontrada: {glb_entrada}")
    pasta_trabalho.mkdir(parents=True, exist_ok=True)
    pasta_saida.mkdir(parents=True, exist_ok=True)

    alvo = int(opcoes.get("alvo_triangulos") or ALVO_PADRAO)
    if alvo < 100:
        raise ErroRefino(f"alvo_triangulos muito baixo: {alvo} (mínimo 100)")
    altura = float(opcoes.get("altura_m") or 1.0)
    if altura <= 0:
        raise ErroRefino(f"altura_m inválida: {altura}")
    timeout = float(opcoes.get("timeout_blender_s") or 900)
    avisos: list[str] = []
    tempos: dict[str, float] = {}

    blender = previa.achar_blender()
    if blender is None:
        raise ErroRefino("Blender não encontrado: o refino precisa dele (defina OFICINA3D_BLENDER "
                         "ou config.BLENDER).")

    # --- 0. medir a entrada (GLB puro, sem dependências) ---
    _avisar(progresso, 0, "Lendo a malha crua")
    tri_antes = None
    if glb_entrada.suffix.lower() == ".glb":
        try:
            tri_antes = malha.info_glb(glb_entrada)["triangulos"]
        except ValueError as e:
            raise ErroRefino(f"GLB de entrada inválido: {e}") from e

    # --- 1. limpeza + decimação com pymeshlab (se houver) ---
    backend = opcoes.get("backend_malha", "auto")
    if backend not in ("auto", "pymeshlab", "blender"):
        raise ErroRefino(f"backend_malha desconhecido: {backend!r}")
    orientacao = opcoes.get("orientacao_entrada", "gltf")
    if orientacao not in ("gltf", "triposr"):
        raise ErroRefino(f"orientacao_entrada desconhecida: {orientacao!r}")
    if orientacao == "triposr" and backend == "auto":
        # O GLB intermediário do trimesh perderia a convenção do OBJ do TripoSR (Z para cima).
        backend = "blender"
    info_pml = None
    entrada_blender = glb_entrada
    if backend in ("auto", "pymeshlab") and glb_entrada.suffix.lower() in (".glb", ".gltf", ".ply", ".stl"):
        if malha.pymeshlab_disponivel():
            _avisar(progresso, 5, "Limpando e reduzindo a malha (pymeshlab)")
            t = time.perf_counter()
            limpa = pasta_trabalho / "limpa.glb"
            try:
                info_pml = malha.limpar_pymeshlab(
                    glb_entrada, limpa, alvo,
                    min_componente_frac=float(opcoes.get("min_componente_frac", 0.005)),
                    max_lados_buraco=int(opcoes.get("max_lados_buraco", 1000)))
                entrada_blender = limpa
            except Exception as e:  # noqa: BLE001 — cai no Blender, com aviso
                avisos.append(f"pymeshlab falhou ({type(e).__name__}: {e}); limpeza feita no Blender")
                info_pml = None
            tempos["pymeshlab"] = round(time.perf_counter() - t, 2)
        elif backend == "pymeshlab":
            raise ErroRefino("backend_malha='pymeshlab' pedido, mas pymeshlab/trimesh/numpy não estão instalados")

    # --- 2. Blender: limpar/fechar/decimar (se preciso), normalizar, UV, exportar ---
    glb_saida = pasta_saida / "modelo.glb"
    pedido_refino = {
        "entrada": str(entrada_blender), "saida_glb": str(glb_saida),
        "alvo_triangulos": alvo, "altura": altura,
        "limpar": info_pml is None,  # pymeshlab já tirou os pedaços soltos
        "simetrizar": bool(opcoes.get("simetrizar", False)),
        "uv": bool(opcoes.get("uv", True)),
        "orientacao": orientacao,
        "girar_graus": float(opcoes.get("girar_graus") or 0),
        "min_componente_frac": float(opcoes.get("min_componente_frac", 0.005)),
        "max_lados_buraco": int(opcoes.get("max_lados_buraco", 1000)),
        "salvar_blend": str(pasta_trabalho / "modelo.blend") if opcoes.get("salvar_blend") else None,
    }
    t = time.perf_counter()
    _avisar(progresso, 10, "Blender: limpando, fechando e reduzindo")
    try:
        r_ref = previa.rodar_blender(previa.SCRIPT_REFINO, pedido_refino, pasta_trabalho, "refino",
                                     progresso, (10, 60), timeout, blender)
    except previa.ErroBlender as e:
        raise ErroRefino(str(e)) from e
    tempos["blender_refino"] = round(time.perf_counter() - t, 2)
    if not glb_saida.is_file():
        raise ErroRefino(f"o Blender terminou mas não gravou {glb_saida}")

    # --- 3. Blender: reabrir, prévias, máscaras ---
    imgs = _resolver_imagens(imagens, pasta_trabalho, avisos)
    vistas_previa = list(opcoes.get("previas") or previa.VISTAS_PREVIA)
    pedido_previa = {
        "glb": str(glb_saida), "pasta_saida": str(pasta_saida), "pasta_trabalho": str(pasta_trabalho),
        "previas": vistas_previa, "mascaras": [i["vista"] for i in imgs], "imagens": imgs,
        "limiar_alfa": silhueta.REGUA["limiar_alfa"], "tam_mascara": 512, "previa_px": [640, 800],
    }
    t = time.perf_counter()
    _avisar(progresso, 65, "Blender: reabrindo o GLB e renderizando prévias")
    try:
        r_prev = previa.rodar_blender(previa.SCRIPT_PREVIA, pedido_previa, pasta_trabalho, "previa",
                                      progresso, (65, 85), timeout, blender)
    except previa.ErroBlender as e:
        raise ErroRefino(str(e)) from e
    tempos["blender_previa"] = round(time.perf_counter() - t, 2)
    avisos.extend(r_prev.get("avisos", []))

    # --- 4. IoU de silhueta ---
    _avisar(progresso, 85, "Comparando silhuetas com as imagens")
    t = time.perf_counter()
    silhueta_iou: dict[str, float] = {}
    detalhe: dict[str, dict] = {}
    for vista, pbm_mod in r_prev.get("mascaras_modelo", {}).items():
        pbm_img = r_prev.get("mascaras_imagem", {}).get(vista)
        if not pbm_img:
            continue
        r = silhueta.iou_alinhado(silhueta.ler_pbm(pbm_img), silhueta.ler_pbm(pbm_mod))
        if r.get("vazia"):
            avisos.append(f"silhueta vazia ({r['vazia']}) na vista {vista}: IoU 0")
        silhueta_iou[vista] = r["iou"]
        comp = silhueta.salvar_comparacao(r, pasta_trabalho / f"silhueta_{vista}.png")
        detalhe[vista] = {k: r.get(k) for k in ("iou", "escala", "dx", "dy", "iou_espelhada")}
        detalhe[vista]["comparacao"] = str(comp) if comp else None
        esp = r.get("iou_espelhada")
        if esp is not None and esp > r["iou"] + 0.05 and vista != "frente" and vista != "costas":
            avisos.append(f"vista {vista}: a silhueta espelhada bate melhor ({esp:.2f} × {r['iou']:.2f}); "
                          "a etiqueta esquerda/direita da imagem pode estar trocada")
    resumo = silhueta.nota_iou(silhueta_iou)
    tempos["silhueta"] = round(time.perf_counter() - t, 2)

    # --- 5. conferir o arquivo final ---
    _avisar(progresso, 95, "Conferindo o arquivo final")
    info_final = malha.info_glb(glb_saida)
    reaberto = r_prev.get("reaberto", {})
    tri_depois = info_final["triangulos"]
    if tri_depois > alvo:
        avisos.append(f"o modelo ficou com {tri_depois} triângulos, acima do alvo {alvo}")
    fechada = bool(reaberto.get("fechada", r_ref.get("fechada")))
    if not fechada:
        avisos.append("a malha final não ficou fechada (arestas abertas: "
                      f"{reaberto.get('arestas_abertas', r_ref.get('arestas_abertas'))})")
    caixa = info_final.get("caixa") or {}
    mn, mx = caixa.get("min", [0, 0, 0]), caixa.get("max", [0, 0, 0])
    altura_medida = round(mx[1] - mn[1], 5)
    pivo = {"x": round((mn[0] + mx[0]) / 2, 5), "y": round(mn[1], 5), "z": round((mn[2] + mx[2]) / 2, 5)}
    tol = max(1e-3, altura * 1e-3)
    pivo_ok = abs(pivo["x"]) <= tol and abs(pivo["y"]) <= tol and abs(pivo["z"]) <= tol
    if not pivo_ok:
        avisos.append(f"pivô fora dos pés: centro da base em {pivo}")
    if abs(altura_medida - altura) > tol:
        avisos.append(f"altura medida {altura_medida} difere da pedida {altura}")
    fechada_tm = malha.fechada_trimesh(glb_saida) if malha.pymeshlab_disponivel() else None

    previas = [Path(p) for p in r_prev.get("previas", []) if Path(p).is_file()]
    faltando = set(vistas_previa) - {p.stem.removeprefix("previa_") for p in previas}
    if faltando:
        avisos.append(f"prévias não geradas: {', '.join(sorted(faltando))}")

    metricas = {
        "backend_malha": "pymeshlab" if info_pml else "blender",
        "triangulos_antes": tri_antes if tri_antes is not None else r_ref.get("triangulos_entrada"),
        "triangulos_depois": tri_depois,
        "vertices_depois": reaberto.get("vertices", info_final["vertices"]),
        "alvo_triangulos": alvo,
        "fechada_antes": (info_pml or {}).get("fechada_antes", r_ref.get("fechada_antes")),
        "fechada": fechada,
        "fechada_trimesh": fechada_tm,
        "arestas_abertas": reaberto.get("arestas_abertas", r_ref.get("arestas_abertas")),
        "componentes_removidos": (info_pml or {}).get("componentes_removidos", r_ref.get("componentes_removidos")),
        "altura": altura_medida,
        "dimensoes": r_ref.get("dimensoes"),
        "pivo": "pes" if pivo_ok else "fora",
        "pivo_centro_base": pivo,
        "eixos": "Y para cima, frente +Z (glTF)",
        "tem_uv": info_final["tem_uv"],
        "simetria": r_ref.get("simetria"),
        "silhueta_iou": silhueta_iou,
        **resumo,
        "regua_iou": silhueta.REGUA["versao"],
        "versao_blender": r_ref.get("versao_blender"),
        "tempos_s": {**tempos, "blender_passos": r_ref.get("tempos_s"),
                     "total": round(time.perf_counter() - t_inicio, 2)},
    }
    resultado = {
        "glb": glb_saida,
        "previas": previas,
        "silhueta_iou": silhueta_iou,
        **resumo,
        "silhueta_detalhe": detalhe,
        "metricas": metricas,
        "avisos": avisos,
    }
    try:
        (pasta_trabalho / "refino.json").write_text(
            json.dumps(resultado, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    except OSError as e:
        avisos.append(f"não consegui gravar refino.json: {e}")
    _avisar(progresso, 100, "Refino concluído")
    return resultado
