"""Etapa `validar` da Oficina 3D (Fase 2, item 1 do plano v2): o GLB abre no Godot como o jogo abriria?

Contrato:

    validar(glb, pasta_saida=None, opcoes=None, progresso=None) -> dict
      grava pasta_saida/validacao.json (se pasta_saida for dada)
      -> {"aprovado": bool, "perfil": str, "regras": [{"id", "ok", "severidade", "valor", "limite", "msg"}],
          "glb": {...contagens lidas do arquivo...}, "godot": {...o que o Godot carregou...} | None,
          "avisos": [...], "pendente": [...]}

Duas réguas independentes, e uma confere a outra:
  1. `glb.resumo`: Python puro lendo o arquivo (magic bytes, chunks, accessors, imagens embutidas);
  2. `godot.carregar`: Godot 4.7.2 --headless carregando por GLTFDocument (o caminho do jogo).

Perfis (`opcoes["perfil"]`):
  - "oficina" (padrão): estrutura; o arquivo é um GLB 2.0 são, o Godot carrega, as duas réguas
    batem nos triângulos, pivô nos pés, imagens embutidas são PNG/JPEG de verdade;
  - "jogo": "oficina" + aceite EXP-01 do plano (< 20 mil triângulos, 1 material, textura no albedo
    de até 1024 px, até 5 MB).
Limites avulsos em `opcoes` sobrescrevem o perfil: max_triangulos, max_materiais, max_mb,
max_textura_px, exigir_albedo.

Severidade "erro" reprova; "aviso" só registra. Ossos e animações são só contados (Fase 3).

PENDENTE (honesto): as 8 capturas de tela do plano. O --headless usa o renderizador dummy e não
desenha nada; renderizar exige abrir uma janela do Godot, o que disputa a tela do dono do PC.
Até haver uma forma sem janela, as capturas visuais são as prévias do Blender do refino/cor.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from . import glb as _glb
from . import godot as _godot

__all__ = ["validar", "PERFIS", "ErroValidacao"]

PERFIS = {
    "oficina": {},
    "jogo": {"max_triangulos": 19999, "max_materiais": 1, "max_mb": 5.0, "max_textura_px": 1024,
             "exigir_albedo": True},
}
TOLERANCIA_PIVO = 0.01  # fração da altura: o ponto mais baixo tem de estar a até 1% de y=0


class ErroValidacao(RuntimeError):
    """Falha do próprio validador (não confundir com um GLB reprovado, que volta aprovado=False)."""


def _avisar(progresso, pct, msg):
    if progresso:
        try:
            progresso(int(pct), msg)
        except Exception:  # noqa: BLE001 — progresso nunca derruba a validação
            pass


def _limites(opcoes: dict) -> tuple[str, dict]:
    perfil = opcoes.get("perfil") or "oficina"
    if perfil not in PERFIS:
        raise ErroValidacao(f"perfil de validação desconhecido: {perfil!r} (use {', '.join(PERFIS)})")
    lim = dict(PERFIS[perfil])
    for k in ("max_triangulos", "max_materiais", "max_mb", "max_textura_px", "exigir_albedo"):
        if opcoes.get(k) is not None:
            lim[k] = opcoes[k]
    return perfil, lim


def _regra(regras, id_, ok, msg, valor=None, limite=None, severidade="erro"):
    regras.append({"id": id_, "ok": bool(ok), "severidade": severidade, "valor": valor,
                   "limite": limite, "msg": msg})


def validar(glb, pasta_saida=None, opcoes: dict | None = None, progresso=None) -> dict:
    opcoes = dict(opcoes or {})
    perfil, lim = _limites(opcoes)
    glb = Path(glb)
    t0 = time.time()
    regras: list[dict] = []
    avisos: list[str] = []
    pendente = ["capturas: o Godot --headless não renderiza; usar as prévias do Blender (ver docstring)"]
    resumo = godot = None

    _avisar(progresso, 5, "lendo o GLB")
    if not glb.is_file():
        _regra(regras, "arquivo_existe", False, f"arquivo não existe: {glb}")
    else:
        try:
            resumo = _glb.resumo(glb)
            _regra(regras, "glb_valido", True, "GLB 2.0 com cabeçalho, chunks e comprimento corretos")
        except _glb.ErroGLB as e:
            _regra(regras, "glb_valido", False, f"GLB inválido: {e}")
        except (KeyError, IndexError, TypeError) as e:
            _regra(regras, "glb_valido", False, f"GLB com referência quebrada no JSON: {e!r}")

    if resumo:
        _regra(regras, "tem_triangulos", resumo["triangulos"] > 0, "a malha tem triângulos",
               resumo["triangulos"], "> 0")
        if resumo["primitivas_nao_triangulo"]:
            _regra(regras, "so_triangulos", False, "primitivas que não são triângulos (linhas/pontos)",
                   resumo["primitivas_nao_triangulo"], 0, "aviso")
        ruins = [i for i in resumo["imagens"] if not i["ok"]]
        _regra(regras, "imagens_embutidas", not ruins,
               f"{len(resumo['imagens'])} imagem(ns) embutida(s), todas PNG/JPEG de verdade (valor = ruins)" if not ruins
               else "; ".join(f"imagem {i['indice']}: {i['info']}" for i in ruins), len(ruins), 0)

        _avisar(progresso, 30, "carregando no Godot (headless)")
        if not _godot.disponivel():
            pendente.append("godot: executável não encontrado; a carga no motor do jogo NÃO foi conferida")
            _regra(regras, "godot_carrega", False, "Godot ausente: carga não conferida", severidade="aviso")
        else:
            try:
                godot = _godot.carregar(glb, timeout_s=int(opcoes.get("timeout_godot_s", 300)))
            except _godot.ErroGodot as e:
                raise ErroValidacao(str(e)) from e
            _regra(regras, "godot_carrega", godot.get("ok") and godot.get("mesh_instances", 0) > 0,
                   "o Godot carregou a cena com malha" if godot.get("ok")
                   else f"o Godot não carregou: {godot.get('erro')}")
            if godot.get("erros_godot"):
                avisos.extend(f"godot: {x}" for x in godot["erros_godot"])

    if resumo and godot and godot.get("ok"):
        _regra(regras, "reguas_batem", resumo["triangulos"] == godot["triangulos"],
               "triângulos iguais no arquivo e no Godot",
               {"arquivo": resumo["triangulos"], "godot": godot["triangulos"]}, "iguais")
        cmin, cmax = godot["caixa_min"], godot["caixa_max"]
        altura = cmax[1] - cmin[1]
        ok_pivo = altura > 0 and abs(cmin[1]) <= TOLERANCIA_PIVO * altura
        _regra(regras, "pivo_nos_pes", ok_pivo, "ponto mais baixo em y=0 (pivô nos pés, Y para cima)",
               round(cmin[1], 5), f"|y_min| <= {TOLERANCIA_PIVO:.0%} da altura ({altura:.4f})")
        if godot.get("superficies_com_uv", 0) < godot.get("superficies", 0):
            _regra(regras, "uv", False, "superfícies sem UV (a textura não teria onde cair)",
                   godot.get("superficies_com_uv"), godot.get("superficies"), "aviso")

    fonte = godot if (godot and godot.get("ok")) else resumo
    if fonte:
        tris = fonte["triangulos"]
        if lim.get("max_triangulos") is not None:
            _regra(regras, "max_triangulos", tris <= lim["max_triangulos"], "orçamento de triângulos",
                   tris, lim["max_triangulos"])
        if lim.get("max_materiais") is not None and resumo:
            _regra(regras, "max_materiais", resumo["materiais"] <= lim["max_materiais"], "materiais",
                   resumo["materiais"], lim["max_materiais"])
        if lim.get("max_mb") is not None and resumo:
            mb = round(resumo["bytes"] / 1e6, 3)
            _regra(regras, "max_mb", mb <= lim["max_mb"], "tamanho do arquivo (MB)", mb, lim["max_mb"])
        if lim.get("exigir_albedo"):
            n_albedo = (godot["superficies_com_albedo"] if (godot and godot.get("ok"))
                        else (resumo or {}).get("materiais_com_albedo", 0))
            _regra(regras, "textura_albedo", n_albedo > 0, "textura de cor no albedo do material",
                   n_albedo, ">= 1")
        if lim.get("max_textura_px") is not None and godot and godot.get("albedo_px"):
            _regra(regras, "max_textura_px", godot["albedo_px"] <= lim["max_textura_px"],
                   "lado da textura de albedo (px)", godot["albedo_px"], lim["max_textura_px"])

    aprovado = bool(regras) and all(r["ok"] for r in regras if r["severidade"] == "erro")
    res = {
        "aprovado": aprovado, "perfil": perfil, "limites": lim, "arquivo": str(glb),
        "regras": regras, "glb": resumo, "godot": godot, "avisos": avisos, "pendente": pendente,
        "tempo_s": round(time.time() - t0, 2),
    }
    if pasta_saida is not None:
        pasta = Path(pasta_saida)
        pasta.mkdir(parents=True, exist_ok=True)
        (pasta / "validacao.json").write_text(json.dumps(res, ensure_ascii=False, indent=2), encoding="utf-8")
        res["arquivo_relatorio"] = str(pasta / "validacao.json")
    _avisar(progresso, 100, "aprovado" if aprovado else "reprovado")
    return res
