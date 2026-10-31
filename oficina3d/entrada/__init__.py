"""Etapa ENTRADA da Oficina 3D: prepara as imagens do job para o motor de forma.

Contrato (docs/ARQUITETURA.md):
    preparar(job_dir, job, progresso=None) -> {"imagens": [...], "avisos": [...],
                                               "pranchas_divididas": [...]}
    vista_pelo_nome(nome_arquivo) -> str | None

O que faz, por imagem do job (`entrada/...`):
1. abre como RGBA; descobre a vista (do job ou pelo nome do arquivo);
2. fundo (`opcoes.remover_fundo`: "auto" | "sim" | "nao"): "auto" só remove (rembg + u2net,
   CPU) quando não há alfa útil; alfa fraco (<= 10) sempre vira 0;
3. validações que viram AVISOS (nunca travam): fundo não removido, resolução baixa,
   objeto cortado na borda, recorte incerto, vistas repetidas, personagens diferentes;
4. divisor de pranchas (`opcoes.dividir_pranchas`); etiquetas das partes por
   `vistas_partes` na imagem do job ou pelo nome (`prancha_frente_costas_esquerda_direita`);
5. correção de lados por kit (`opcoes.inverter_lados`: true | false | "auto"; a Besta
   Cristalina vem invertida — ver vistas.KITS);
6. normaliza para 1024² RGBA (margem ~8%, no máximo 2× de ampliação) em `preproc/<vista>.png`.

numpy, Pillow, opencv e rembg só são importados quando preciso (mensagem clara se faltarem).
"""
from __future__ import annotations

import json
import time
from pathlib import Path

from . import divisor, fundo, imagem, normalizar, validacao
from .dependencias import DependenciaAusente, ModeloAusente, exigir
from .vistas import (KITS, VISTAS_SEM_FORMA, decidir_inversao, nome_de_prancha, trocar_lado,
                     vista_pelo_nome, vistas_da_prancha, vistas_validas)

__all__ = [
    "preparar", "vista_pelo_nome", "vistas_da_prancha", "trocar_lado", "decidir_inversao",
    "KITS", "DependenciaAusente", "ModeloAusente",
]

ARQUIVO_RESUMO = "preparo.json"


def _opcao_fundo(valor) -> str:
    if valor is True:
        return "sim"
    if valor is False:
        return "nao"
    t = str(valor or "auto").strip().lower().replace("ã", "a")
    return t if t in ("auto", "sim", "nao") else "auto"


def _opcao_bool(valor, padrao: bool) -> bool:
    if isinstance(valor, bool):
        return valor
    if valor is None:
        return padrao
    t = str(valor).strip().lower().replace("ã", "a")
    if t in ("1", "sim", "true", "s", "yes"):
        return True
    if t in ("0", "nao", "false", "n", "no"):
        return False
    return padrao


def _dentro(caminho: Path, base: Path) -> bool:
    try:
        caminho.resolve().relative_to(base.resolve())
        return True
    except ValueError:
        return False


def _limpar_preproc(pasta: Path) -> None:
    """Apaga só o que esta etapa mesma grava (PNGs e o resumo), nada mais."""
    for p in pasta.glob("*.png"):
        p.unlink()
    resumo = pasta / ARQUIVO_RESUMO
    if resumo.exists():
        resumo.unlink()


class _Nomes:
    """Nomes de saída: <vista>.png, <vista>_2.png… e img_<n>.png para as sem vista."""

    def __init__(self):
        self.usados: dict[str, int] = {}
        self.sem_vista = 0

    def novo(self, vista: str | None) -> str:
        if not vista:
            self.sem_vista += 1
            return f"img_{self.sem_vista}.png"
        n = self.usados.get(vista, 0) + 1
        self.usados[vista] = n
        return f"{vista}.png" if n == 1 else f"{vista}_{n}.png"


def _etiquetas_validas(etiquetas, validas) -> list | None:
    if not etiquetas or not isinstance(etiquetas, (list, tuple)):
        return None
    lista = [str(e).strip().lower() if e else None for e in etiquetas]
    return lista if all(e in validas for e in lista) else None


def preparar(job_dir, job: dict, progresso=None) -> dict:
    """Prepara as imagens do job em `preproc/`. Ver a docstring do módulo.

    Devolve {"imagens": [{"arquivo": "preproc/frente.png", "vista": "frente",
    "usar_na_forma": True, "origem": "entrada/01_FRENTE_S.png", "tamanho": [1024, 1024], ...}],
    "avisos": [...], "pranchas_divididas": [{"origem": ..., "partes": [...], "vistas": [...],
    "metodo": ...}]}. Caminhos relativos à pasta do job.
    Levanta DependenciaAusente/ModeloAusente (com mensagem clara) se faltar pacote ou o u2net,
    e ValueError se nenhuma imagem do job puder ser usada.
    """
    inicio = time.time()
    job_dir = Path(job_dir)
    opcoes = dict(job.get("opcoes") or {})
    modo_fundo = _opcao_fundo(opcoes.get("remover_fundo", "auto"))
    dividir_ligado = _opcao_bool(opcoes.get("dividir_pranchas", True), True)
    validas = vistas_validas()

    avisos: list[str] = []
    pranchas: list[dict] = []
    saida: list[dict] = []
    cores: list[dict] = []

    def avisar(msg: str) -> None:
        if msg and msg not in avisos:
            avisos.append(msg)

    def prog(pct: float, msg: str) -> None:
        if progresso is not None:
            progresso(max(0, min(100, int(pct))), msg)

    itens = [i for i in (job.get("imagens") or []) if isinstance(i, dict) and i.get("arquivo")]
    if not itens:
        return {"imagens": [], "avisos": ["o job não tem imagens"], "pranchas_divididas": []}

    exigir("numpy", "preparar imagens (entrada)")
    exigir("PIL.Image", "preparar imagens (entrada)")
    pasta = job_dir / "preproc"
    pasta.mkdir(parents=True, exist_ok=True)
    _limpar_preproc(pasta)

    inverter_job, aviso_inv = decidir_inversao(job)
    avisar(aviso_inv)
    nomes = _Nomes()
    total = len(itens)

    for n, item in enumerate(itens):
        rel = str(item["arquivo"]).replace("\\", "/")
        nome = Path(rel).name
        base_pct = 100.0 * n / total
        prog(base_pct, f"preparando {nome} ({n + 1}/{total})")
        caminho = job_dir / rel
        if not _dentro(caminho, job_dir):
            avisar(f"{nome}: caminho fora da pasta do job; ignorada")
            continue
        if not caminho.is_file():
            avisar(f"{nome}: arquivo não encontrado; ignorada")
            continue
        if caminho.suffix.lower() not in imagem.EXTENSOES:
            avisar(f"{nome}: não é imagem ({caminho.suffix}); ignorada")
            continue
        try:
            arr, tinha_alfa = imagem.abrir_rgba(caminho)
        except DependenciaAusente:
            raise
        except Exception as erro:  # arquivo corrompido etc.: aviso, segue com as outras
            avisar(f"{nome}: não abriu como imagem ({erro}); ignorada")
            continue

        # --- vista da imagem inteira
        vista = item.get("vista")
        fonte = "job"
        if vista and vista not in validas:
            avisar(f"{nome}: vista '{vista}' desconhecida; etiqueta ignorada")
            vista = None
        if not vista:
            vista = vista_pelo_nome(nome)
            fonte = "nome" if vista else None
        inverter = _opcao_bool(item.get("inverter_lados"), inverter_job)
        sem_forma = vista in VISTAS_SEM_FORMA

        # --- fundo
        util, motivo = validacao.diagnostico_fundo(arr, tinha_alfa)
        removeu = False
        if modo_fundo == "sim" or (modo_fundo == "auto" and not util and not sem_forma):
            prog(base_pct, f"removendo fundo de {nome} (rembg)")
            arr = fundo.remover_fundo(arr, manter_alfa_original=tinha_alfa and util)
            removeu = True
            avisar(f"{nome}: {motivo}; fundo removido com rembg (u2net)" if motivo
                   else f"{nome}: fundo removido com rembg (u2net), por opção")
        else:
            if not util and not sem_forma:
                avisar(f"{nome}: {motivo}; remover_fundo='nao': vai com o fundo")
            elif motivo and util:
                avisar(f"{nome}: {motivo}; alfa fraco limpo (<= 10 vira 0)")
            arr = imagem.limpar_alfa(arr)
        com_objeto = util or removeu

        if not sem_forma:
            for a in validacao.avisos_recorte(arr, nome, checar_borda=com_objeto):
                avisar(a)

        # --- prancha?
        etiquetas = _etiquetas_validas(item.get("vistas_partes"), validas)
        if item.get("vistas_partes") and etiquetas is None:
            avisar(f"{nome}: 'vistas_partes' tem etiqueta inválida; ignorado")
        if etiquetas is None:
            etiquetas = vistas_da_prancha(nome)
        pode_dividir = dividir_ligado and (not vista or bool(etiquetas) or nome_de_prancha(nome))
        mascaras, metodo = None, None
        if com_objeto and not sem_forma:
            try:
                prog(base_pct, f"procurando vistas em {nome}")
                res = divisor.dividir(arr, n_esperado=len(etiquetas) if etiquetas else None)
            except DependenciaAusente:
                if pode_dividir:
                    raise
                res = None   # só detecção para aviso; sem opencv, pula
            achadas = len(res["mascaras"]) if res else 1
            if achadas > 1:
                if not dividir_ligado:
                    avisar(f"{nome}: parece uma prancha com {achadas} vistas; "
                           f"dividir_pranchas=false: vai inteira")
                elif not pode_dividir:
                    avisar(f"{nome}: parece ter {achadas} vistas, mas veio etiquetada como "
                           f"'{vista}' e não foi dividida (para dividir, passe 'vistas_partes')")
                else:
                    mascaras, metodo = res["mascaras"], res["metodo"]

        if mascaras:
            if etiquetas and len(etiquetas) == len(mascaras):
                vistas_pecas = list(etiquetas)
            else:
                vistas_pecas = [None] * len(mascaras)
                if etiquetas:
                    avisar(f"{nome}: as etiquetas da prancha ({len(etiquetas)}) não batem com as "
                           f"{len(mascaras)} partes achadas; partes ficaram sem vista")
                else:
                    avisar(f"{nome}: prancha dividida em {len(mascaras)} partes sem etiqueta: "
                           f"diga as vistas em 'vistas_partes' (da esquerda para a direita, de "
                           f"cima para baixo) ou no nome (ex.: prancha_frente_costas_esquerda_direita)")
            pecas = [(normalizar.recortar(arr, m), vistas_pecas[k], k + 1, "prancha" if vistas_pecas[k] else None)
                     for k, m in enumerate(mascaras)]
        else:
            pecas = [(arr, vista, None, fonte)]

        novas: list[dict] = []
        for arr_p, vista_p, parte, fonte_p in pecas:
            rotulo = f"{nome} (parte {parte})" if parte else nome
            if arr_p is None:
                avisar(f"{rotulo}: vazia depois do recorte; ignorada")
                continue
            vista_original = vista_p
            if inverter:
                vista_p = trocar_lado(vista_p)
            try:
                final, info = normalizar.normalizar(arr_p)
            except ValueError:
                avisar(f"{rotulo}: vazia (nada com alfa > 10); ignorada")
                continue
            if info["ampliacao_limitada"]:
                w, h = info["objeto_px"]
                avisar(f"{rotulo}: imagem pequena: ampliada só {normalizar.AMPLIACAO_MAXIMA:g}× "
                       f"(o objeto ocupa {w}×{h} px do quadro de {normalizar.LADO})")
            arquivo = nomes.novo(vista_p)
            imagem.salvar_png(final, pasta / arquivo)
            reg = {"arquivo": f"preproc/{arquivo}", "vista": vista_p,
                   "usar_na_forma": vista_p not in VISTAS_SEM_FORMA,
                   "origem": rel, "tamanho": [int(final.shape[1]), int(final.shape[0])],
                   "fonte_vista": fonte_p}
            if parte:
                reg["parte"] = parte
            if vista_p != vista_original:
                reg["lado_invertido"] = True
                reg["vista_antes_da_correcao"] = vista_original
            if not vista_p:
                avisar(f"{rotulo}: sem vista (nem no job nem no nome); foi como {arquivo}")
            novas.append(reg)
            cores.append({"nome": rotulo, "assinatura": validacao.assinatura_cor(final),
                          "vista": vista_p})
        saida.extend(novas)
        if mascaras:
            pranchas.append({"origem": rel, "partes": [r["arquivo"] for r in novas],
                             "vistas": [r["vista"] for r in novas], "metodo": metodo})

    for a in validacao.vistas_repetidas(saida):
        avisar(a)
    for a in validacao.personagens_diferentes(cores):
        avisar(a)

    if not saida:
        raise ValueError("nenhuma imagem do job pôde ser usada: " + "; ".join(avisos))

    resultado = {"imagens": saida, "avisos": avisos, "pranchas_divididas": pranchas}
    resumo = dict(resultado)
    resumo.update({"opcoes_usadas": {"remover_fundo": modo_fundo, "dividir_pranchas": dividir_ligado,
                                     "inverter_lados": inverter_job},
                   "tempo_s": round(time.time() - inicio, 2)})
    (pasta / ARQUIVO_RESUMO).write_text(json.dumps(resumo, ensure_ascii=False, indent=2),
                                        encoding="utf-8")
    prog(100, f"entrada pronta: {len(saida)} imagem(ns)")
    return resultado
