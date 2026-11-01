"""Perfis de qualidade da Oficina 3D (diretriz QUAL-01 do Mestre, 01/11/2026).

Cinco niveis de qualidade com os nomes das classificacoes do RPG
Assimilacao: Bronze, Prata, Ouro, Ouro Negro e Lendario. A ideia do
Mestre: resposta rapida tem valor (Bronze/Prata servem de rascunho),
mas qualidade manda -- os niveis altos gastam mais tempo e memoria
para entregar uma malha melhor.

O perfil NAO e um motor: e um pacote de parametros (passos, octree,
alvo de triangulos) mais a CLASSE de motor sugerida:
- "leve":     o caminho mais rapido (triposr com 1 vista; turbo com 2+);
- "turbo":    os motores turbo, no automatico padrao;
- "completo": os motores cheios (hunyuan-mini/mv, sem turbo).

Opcao explicita do usuario SEMPRE vence o perfil: o perfil so preenche
o que ficou em None. O custo medido de cada nivel (tempo, VRAM,
triangulos, tamanho do GLB) fica registrado no REGISTRO do projeto.
"""
from __future__ import annotations

from . import config

# slug -> rotulo de exibicao (tematica do RPG) e parametros.
PERFIS = {
    "bronze": {
        "rotulo": "Bronze", "classe": "leve",
        "passos": None, "octree": 128, "alvo_triangulos": 25_000,
    },
    "prata": {
        "rotulo": "Prata", "classe": "turbo",
        "passos": None, "octree": 192, "alvo_triangulos": 50_000,
    },
    "ouro": {
        "rotulo": "Ouro", "classe": "turbo",
        "passos": None, "octree": 256, "alvo_triangulos": 150_000,
    },
    "ouro-negro": {
        "rotulo": "Ouro Negro", "classe": "completo",
        "passos": 30, "octree": 320, "alvo_triangulos": 300_000,
    },
    "lendario": {
        "rotulo": "Lend\u00e1rio", "classe": "completo",
        "passos": 50, "octree": 384, "alvo_triangulos": 500_000,
    },
}

NOMES = tuple(PERFIS)
ROTULOS = {slug: p["rotulo"] for slug, p in PERFIS.items()}


def _multivista(modo, vistas) -> bool:
    """Mesma conta do motor_padrao de job.py, sem importar job (ciclo)."""
    if modo == "multivista":
        return True
    n = len({v for v in vistas if v in config.VISTAS_MV_HUNYUAN})
    n += sum(1 for v in vistas if v is None)
    return n >= 2


def motor_sugerido(classe: str, modo: str, vistas) -> str | None:
    """Motor que a classe do perfil sugere; None = deixar o automatico."""
    if classe == "leve":
        return None if _multivista(modo, vistas) else "triposr"
    if classe == "completo":
        return "hunyuan-mv" if _multivista(modo, vistas) else "hunyuan-mini"
    return None  # turbo: o automatico padrao ja escolhe os turbo


def aplicar(opcoes: dict, modo: str = "livre", vistas=()) -> dict:
    """Devolve uma copia das opcoes brutas com os defaults do perfil.

    So preenche chaves ausentes ou None (a escolha explicita vence).
    Levanta ValueError para slug desconhecido.
    """
    slug = opcoes.get("qualidade")
    if slug is None:
        return dict(opcoes)
    if slug not in PERFIS:
        raise ValueError(
            f"qualidade desconhecida: {slug!r} (use {', '.join(PERFIS)})")
    perfil = PERFIS[slug]
    op = dict(opcoes)
    for chave in ("passos", "octree", "alvo_triangulos"):
        if op.get(chave) is None and perfil[chave] is not None:
            op[chave] = perfil[chave]
    if op.get("motor") is None:
        sugerido = motor_sugerido(perfil["classe"], modo, vistas)
        if sugerido is not None:
            op["motor"] = sugerido
    return op
