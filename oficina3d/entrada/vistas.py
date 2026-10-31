"""Etiquetas de vista: leitura pelo nome do arquivo e correção de lados por kit.

Só biblioteca padrão (nada de numpy/Pillow aqui), para que `vista_pelo_nome`
funcione em qualquer Python, inclusive na web e na CLI.

Convenção do contrato (docs/ARQUITETURA.md): `esquerda` = imagem em que o
personagem OLHA PARA A ESQUERDA DA IMAGEM.
"""
from __future__ import annotations

import re
import unicodedata

# Cópia de segurança de config.VISTAS (o config é a fonte de verdade; ver vistas_validas()).
VISTAS_PADRAO = (
    "frente", "costas", "esquerda", "direita",
    "frente-esquerda", "frente-direita", "costas-esquerda", "costas-direita",
    "cima", "detalhe", "referencia-de-cor",
)
# Vistas que vão para preproc\ mas não servem para gerar a forma.
VISTAS_SEM_FORMA = ("detalhe", "referencia-de-cor")

# Palavras -> etiqueta. Tudo já sem acento e em minúsculas.
_FRENTE_COSTAS = {
    "frente": "frente", "front": "frente", "frontal": "frente",
    "costas": "costas", "back": "costas", "tras": "costas", "atras": "costas",
    "traseira": "costas", "traseiro": "costas", "verso": "costas", "rear": "costas",
}
_LADOS = {
    "esquerda": "esquerda", "esquerdo": "esquerda", "esq": "esquerda", "left": "esquerda",
    "direita": "direita", "direito": "direita", "dir": "direita", "right": "direita",
}
_OUTRAS = {
    "cima": "cima", "topo": "cima", "top": "cima", "superior": "cima",
    "detalhe": "detalhe", "detalhes": "detalhe", "detail": "detalhe", "closeup": "detalhe",
    "paleta": "referencia-de-cor", "palette": "referencia-de-cor",
    "swatch": "referencia-de-cor", "swatches": "referencia-de-cor",
}
# "cor"/"cores" sozinhas só valem se não houver outra vista no nome ("orc_frente_cor" = frente).
_COR_FRACA = {"cor", "cores", "color", "colors", "colour", "colours"}
# Palavras grudadas comuns.
_COMPOSTAS = {}
for _fb_txt, _fb in (("frente", "frente"), ("front", "frente"), ("costas", "costas"), ("back", "costas")):
    for _ld_txt, _ld in (("esquerda", "esquerda"), ("esq", "esquerda"), ("left", "esquerda"),
                         ("direita", "direita"), ("dir", "direita"), ("right", "direita")):
        _COMPOSTAS[_fb_txt + _ld_txt] = f"{_fb}-{_ld}"
_COMPOSTAS["referenciadecor"] = "referencia-de-cor"

# Palavras que indicam prancha (várias vistas numa imagem só).
_MARCAS_PRANCHA = {"prancha", "pranchas", "sheet", "turnaround", "turnarounds",
                   "modelsheet", "lineup", "vistas", "views"}

_TROCA_LADO = {
    "esquerda": "direita", "direita": "esquerda",
    "frente-esquerda": "frente-direita", "frente-direita": "frente-esquerda",
    "costas-esquerda": "costas-direita", "costas-direita": "costas-esquerda",
}

# Kits com convenção própria. Achado da v1 (relatório do agente "entrada", conferido abrindo
# as imagens): Orc e Capríleo seguem o contrato; a Besta Cristalina está INVERTIDA
# (`03_ESQUERDA` olha para a direita, `04_DIREITA` olha para a esquerda). Inferência visual:
# o bicho é ambíguo (parece uma cobra). As diagonais 05–08 não foram conferidas na v1;
# aqui elas também são trocadas (PENDENTE: conferir visualmente).
KITS = {
    "besta-cristalina": {
        "inverter_lados": True,
        "padroes": (("besta", "cristalina"),),
        "nota": "kit da Besta Cristalina: esquerda/direita invertidas em relação ao contrato",
    },
    "orc": {"inverter_lados": False, "padroes": (), "nota": "segue o contrato"},
    "caprileo": {"inverter_lados": False, "padroes": (), "nota": "segue o contrato"},
}


def vistas_validas() -> tuple:
    """Etiquetas aceitas: as do config (contrato); se o config não existir, a cópia local."""
    try:
        from .. import config  # oficina3d.config
    except ImportError:
        return VISTAS_PADRAO
    v = getattr(config, "VISTAS", None)
    return tuple(v) if v else VISTAS_PADRAO


def _sem_acento(texto: str) -> str:
    s = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in s if not unicodedata.combining(c)).lower()


def _base(nome_arquivo: str) -> str:
    """Nome sem pastas e sem extensão, sem acento, minúsculo."""
    nome = re.split(r"[\\/]", str(nome_arquivo))[-1]
    nome = re.sub(r"\.[A-Za-z0-9]{1,5}$", "", nome)
    return _sem_acento(nome)


def _palavras(texto: str) -> list[str]:
    return re.findall(r"[a-z]+|[0-9]+", texto)


def _ler_sequencia(tokens: list[str], juntar_invertido: bool) -> list[str]:
    """Lê as vistas de uma lista de palavras, juntando frente/costas + lado em vista composta."""
    res: list[str] = []
    i = 0
    n = len(tokens)
    while i < n:
        t = tokens[i]
        prox = tokens[i + 1] if i + 1 < n else None
        if t in _COMPOSTAS:
            res.append(_COMPOSTAS[t])
        elif t in _FRENTE_COSTAS:
            if prox in _LADOS:
                res.append(f"{_FRENTE_COSTAS[t]}-{_LADOS[prox]}")
                i += 1
            else:
                res.append(_FRENTE_COSTAS[t])
        elif t in _LADOS:
            if juntar_invertido and prox in _FRENTE_COSTAS:   # "left_front" -> frente-esquerda
                res.append(f"{_FRENTE_COSTAS[prox]}-{_LADOS[t]}")
                i += 1
            else:
                res.append(_LADOS[t])
        elif t in _OUTRAS:
            res.append(_OUTRAS[t])
        elif t == "referencia" and "cor" in tokens[i + 1:i + 3]:
            res.append("referencia-de-cor")
            i += 2 if prox == "cor" else 3
            continue
        i += 1
    return res


def vista_pelo_nome(nome_arquivo: str) -> str | None:
    """Etiqueta de vista lida do nome do arquivo, ou None.

    Exemplos: `01_FRENTE_S`→frente, `05_FRENTE_DIREITA_SE`→frente-direita,
    `03_ESQUERDA`→esquerda, `orc_back.png`→costas, `frente-esq`→frente-esquerda,
    `paleta_cores`→referencia-de-cor. Sem acento e sem caixa. Nomes com mais de uma
    vista (pranchas, ex. `prancha_frente_costas`) devolvem None: use `vistas_da_prancha`.
    Não aplica correção de kit (isso é feito em `preparar`).
    """
    if not nome_arquivo:
        return None
    tokens = _palavras(_base(nome_arquivo))
    if not tokens or any(t in _MARCAS_PRANCHA for t in tokens):
        return None
    achadas = _ler_sequencia(tokens, juntar_invertido=True)
    if not achadas and any(t in _COR_FRACA for t in tokens):
        achadas = ["referencia-de-cor"]
    unicas = list(dict.fromkeys(achadas))
    if "detalhe" in unicas:            # "detalhe_frente" = detalhe (não serve para a forma)
        return "detalhe"
    if len(unicas) != 1:
        return None
    vista = unicas[0]
    return vista if vista in vistas_validas() else None


def vistas_da_prancha(nome_arquivo: str) -> list[str] | None:
    """Sequência de vistas escrita no nome de uma prancha, na ordem (esquerda→direita,
    de cima para baixo). Na prancha, `_`/espaço SEPARAM vistas e `-` JUNTA vista composta:
    `prancha_frente_costas_esquerda_direita` → [frente, costas, esquerda, direita];
    `prancha_frente-esquerda_costas-direita` → [frente-esquerda, costas-direita].
    Devolve None se o nome não tiver pelo menos 2 vistas, ou se o nome for de UMA vista só
    sem marca de prancha (ex.: `05_FRENTE_DIREITA_SE` é frente-direita, não 2 vistas).
    """
    if not nome_arquivo:
        return None
    base = _base(nome_arquivo)
    marcada = any(t in _MARCAS_PRANCHA for t in _palavras(base))
    if not marcada and vista_pelo_nome(nome_arquivo) is not None:
        return None
    res: list[str] = []
    for bloco in re.split(r"[^a-z0-9-]+", base):
        if bloco:
            res.extend(_ler_sequencia(_palavras(bloco.replace("-", " ")), juntar_invertido=False))
    validas = vistas_validas()
    res = [v for v in res if v in validas]
    return res if len(res) >= 2 else None


def nome_de_prancha(nome_arquivo: str) -> bool:
    """True se o nome indica prancha (`prancha`, `sheet`, `turnaround`…) ou lista 2+ vistas."""
    if not nome_arquivo:
        return False
    if any(t in _MARCAS_PRANCHA for t in _palavras(_base(nome_arquivo))):
        return True
    return vistas_da_prancha(nome_arquivo) is not None


def trocar_lado(vista: str | None) -> str | None:
    """esquerda↔direita (inclusive nas diagonais). Outras vistas ficam iguais."""
    return _TROCA_LADO.get(vista, vista) if vista else vista


def kit_pelo_texto(*textos) -> str | None:
    """Reconhece um kit conhecido pelo nome do job / dos arquivos (ex.: 'besta_cristalina')."""
    compacto = re.sub(r"[^a-z0-9]", "", _sem_acento(" ".join(str(t) for t in textos if t)))
    for nome_kit, dados in KITS.items():
        for padrao in dados["padroes"]:
            if padrao and all(p in compacto for p in padrao):
                return nome_kit
    return None


def _como_bool(valor):
    """True/False/None ('auto') a partir de bool ou texto."""
    if isinstance(valor, bool):
        return valor
    if valor is None:
        return None
    t = _sem_acento(str(valor)).strip()
    if t in ("1", "sim", "true", "s", "yes"):
        return True
    if t in ("0", "nao", "false", "n", "no"):
        return False
    return None  # "auto" e qualquer outra coisa


def decidir_inversao(job: dict) -> tuple[bool, str | None]:
    """Decide se o job inteiro troca esquerda↔direita.

    `opcoes.inverter_lados`: true | false | "auto" (padrão). Em "auto", inverte se o kit
    (`opcoes.kit`, `job.kit`, ou reconhecido pelo nome do job/arquivos) estiver marcado
    com `inverter_lados` em KITS. Devolve (inverter, aviso_ou_None).
    """
    opcoes = job.get("opcoes") or {}
    escolha = _como_bool(opcoes.get("inverter_lados", "auto"))
    if escolha is True:
        return True, "lados trocados (esquerda↔direita) por opção do job (inverter_lados=true)"
    if escolha is False:
        return False, None
    kit = opcoes.get("kit") or job.get("kit")
    if kit:
        kit = re.sub(r"[^a-z0-9]+", "-", _sem_acento(str(kit))).strip("-")
    if not kit or kit not in KITS:
        arquivos = [i.get("arquivo", "") for i in (job.get("imagens") or []) if isinstance(i, dict)]
        kit = kit_pelo_texto(job.get("nome"), *arquivos) or kit
    dados = KITS.get(kit) if kit else None
    if dados and dados.get("inverter_lados"):
        return True, (f"{dados['nota']}: lados trocados (esquerda↔direita) ao preparar; "
                      "use opcoes.inverter_lados=false para desligar")
    return False, None
