"""Linha de comando da Oficina 3D (rodar com o Python do app, cwd = app\\).

    python -m oficina3d.cli enviar --imagem arq[:vista] ... [--malha x.glb] --modo livre --motor hunyuan-mini-turbo
                                   [--passos N] [--octree N] [--seed N] [--alvo-triangulos N] [--altura-m X]
                                   [--sem-flashvdm] [--simetrizar] [--nome x] [--esperar]
    python -m oficina3d.cli status [id]
    python -m oficina3d.cli baixar id destino
    python -m oficina3d.cli motores
    python -m oficina3d.cli worker [--uma-vez] [--job ID]
    python -m oficina3d.cli cancelar id

Vista ausente em --imagem: tenta oficina3d.entrada.vista_pelo_nome (se o módulo existir); senão None.
A vista vai depois do ÚLTIMO ':' e só conta se for uma vista conhecida (C:\\pasta\\x.png continua inteiro).
"""
from __future__ import annotations

import argparse
import shutil
import sys
import time
from pathlib import Path

from . import config, job, motores, qualidades

ESTADOS_FINAIS = ("concluido", "erro", "cancelado")


def _saida_utf8() -> None:
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError):
            pass


def _tabela(linhas: list[list[str]], cab: list[str]) -> str:
    larg = [max(len(str(x)) for x in col) for col in zip(cab, *linhas)] if linhas else [len(c) for c in cab]
    fmt = "  ".join(f"{{:<{w}}}" for w in larg)
    out = [fmt.format(*cab), fmt.format(*("-" * w for w in larg))]
    out += [fmt.format(*(str(x) for x in ln)) for ln in linhas]
    return "\n".join(out)


def separar_vista(texto: str) -> tuple[Path, str | None]:
    """'arq.png:frente' -> (arq.png, 'frente'); 'C:\\x\\arq.png' -> (C:\\x\\arq.png, None)."""
    if ":" in texto:
        caminho, vista = texto.rsplit(":", 1)
        if vista in config.VISTAS:
            return Path(caminho), vista
    return Path(texto), None


def _vista_pelo_nome(nome: str) -> str | None:
    for modulo in ("oficina3d.entrada", "oficina3d.entrada.vistas"):
        try:
            mod = __import__(modulo, fromlist=["vista_pelo_nome"])
        except Exception:  # noqa: BLE001 — módulo de outro agente ausente ou com dependência faltando
            continue
        f = getattr(mod, "vista_pelo_nome", None)
        if callable(f):
            try:
                return f(nome)
            except Exception:  # noqa: BLE001
                return None
    return None


# --------------------------------------------------------------------------- comandos

def cmd_enviar(a) -> int:
    arquivos = []
    for item in a.imagem or []:
        caminho, vista = separar_vista(item)
        if vista is None:
            vista = _vista_pelo_nome(caminho.name)
        arquivos.append((caminho, vista))
    opcoes = {
        "motor": a.motor, "passos": a.passos, "octree": a.octree, "seed": a.seed,
        "qualidade": a.qualidade,
        "alvo_triangulos": a.alvo_triangulos, "altura_m": a.altura_m,
    }
    if a.sem_flashvdm:
        opcoes["flashvdm"] = False
    if a.simetrizar:
        opcoes["simetrizar"] = True
    if a.cor:
        opcoes["cor"] = True
    if a.cor_modo:
        opcoes["cor"] = True
        opcoes["cor_modo"] = a.cor_modo
    if a.motor and a.motor not in motores.MOTORES:
        print(f"erro: motor desconhecido: {a.motor} (use: {', '.join(motores.MOTORES)})", file=sys.stderr)
        return 1
    try:
        jb = job.criar_job(arquivos, modo=a.modo, opcoes=opcoes, nome=a.nome,
                           malha=Path(a.malha) if a.malha else None)
    except (ValueError, OSError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1
    print(f"job criado: {jb['id']}")
    if jb.get("imagens"):
        print("  imagens: " + ", ".join(f"{im['arquivo']} ({im.get('vista') or 'sem vista'})" for im in jb["imagens"]))
    print(f"  modo {jb['modo']}, motor {jb['opcoes'].get('motor')}")
    for av in jb.get("avisos") or []:
        print(f"  aviso: {av}")
    disp = {m["nome"]: m for m in motores.listar()}
    m = disp.get(jb["opcoes"].get("motor"))
    if m and not m["disponivel"] and jb["modo"] != "so-refinar":
        print(f"  aviso: motor indisponível agora ({m['motivo']})")
    if a.esperar:
        return esperar(jb["id"])
    return 0


def esperar(job_id: str, intervalo: float = 2.0, limite_s: float | None = None) -> int:
    """Mostra o progresso até o job terminar. 0 = concluído; 1 = erro/cancelado."""
    from . import worker
    if worker.worker_ativo() is None:
        print("  (nenhum worker rodando: abra outro terminal com `python -m oficina3d.cli worker`)")
    ult = None
    t0 = time.time()
    while True:
        jb = job.ler_job(job_id)
        linha = (jb.get("estado"), jb.get("etapa"), jb.get("progresso"))
        if linha != ult:
            ult = linha
            hist = (jb.get("historico") or [{}])[-1].get("msg", "")
            print(f"  {jb['estado']:<11} {str(jb.get('etapa') or '-'):<9} {int(jb.get('progresso') or 0):>3}%  {hist}", flush=True)
        if jb.get("estado") in ESTADOS_FINAIS:
            if jb.get("erro"):
                print(f"  erro: {jb['erro']}")
            return 0 if jb["estado"] == "concluido" else 1
        if limite_s is not None and time.time() - t0 > limite_s:
            return 1
        time.sleep(intervalo)


def cmd_status(a) -> int:
    if a.id:
        try:
            jb = job.ler_job(a.id)
        except (OSError, ValueError) as e:
            print(f"erro: {e}", file=sys.stderr)
            return 1
        print(f"id:        {jb['id']}")
        print(f"nome:      {jb.get('nome')}   modo: {jb.get('modo')}   motor: {(jb.get('opcoes') or {}).get('motor')}")
        print(f"estado:    {jb.get('estado')}   etapa: {jb.get('etapa') or '-'}   progresso: {jb.get('progresso')}%")
        if jb.get("erro"):
            print(f"erro:      {jb['erro']}")
        for av in jb.get("avisos") or []:
            print(f"aviso:     {av}")
        res = jb.get("resultado") or {}
        if res:
            print(f"modelo:    {res.get('glb')}   (cru: {res.get('glb_cru')})")
            if res.get("previas"):
                print(f"prévias:   {', '.join(res['previas'])}")
            if res.get("arquivo"):
                print(f"arquivo:   {res['arquivo'].get('estado')} {res['arquivo'].get('destino') or ''}")
        print(f"pasta:     {job.pasta_job(jb['id'])}")
        print("histórico (últimos 8):")
        for h in (jb.get("historico") or [])[-8:]:
            print(f"  {h.get('quando')}  {str(h.get('etapa') or '-'):<9} {h.get('msg')}")
        return 0
    jobs = job.listar_jobs()
    if not jobs:
        print(f"nenhum job em {config.JOBS}")
        return 0
    linhas = [[j["id"], j.get("estado"), j.get("etapa") or "-", f"{int(j.get('progresso') or 0)}%",
               (j.get("opcoes") or {}).get("motor") or "-", (j.get("erro") or "")[:60]] for j in jobs]
    print(_tabela(linhas, ["id", "estado", "etapa", "prog", "motor", "erro"]))
    return 0


def cmd_baixar(a) -> int:
    try:
        jb = job.ler_job(a.id)
    except (OSError, ValueError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1
    if jb.get("estado") != "concluido":
        print(f"erro: job {a.id} está '{jb.get('estado')}', não 'concluido'", file=sys.stderr)
        return 1
    origem = job.pasta_job(a.id) / "saida"
    if not origem.is_dir():
        arq = (jb.get("resultado") or {}).get("arquivo") or {}
        onde = f" (arquivado em {arq.get('destino')})" if arq.get("destino") else ""
        print(f"erro: a saida\\ local não existe mais{onde}", file=sys.stderr)
        return 1
    destino = Path(a.destino)
    destino.mkdir(parents=True, exist_ok=True)
    copiados = []
    for p in sorted(origem.rglob("*")):
        if p.is_file():
            alvo = destino / p.relative_to(origem)
            alvo.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, alvo)
            copiados.append(alvo)
    print(f"{len(copiados)} arquivo(s) copiado(s) para {destino}")
    for c in copiados:
        print(f"  {c.name}")
    return 0


def cmd_motores(a) -> int:
    linhas = [[m["nome"] + (" *" if m.get("padrao") else ""), "sim" if m["disponivel"] else "não",
               "sim" if m["aceita_multivista"] else "não", m.get("passos_padrao") or "-", m["descricao"]]
              for m in motores.listar()]
    print(_tabela(linhas, ["motor", "disponível", "multivista", "passos", "descrição"]))
    print("* = padrão (1 vista / multivista)")
    for m in motores.listar():
        if not m["disponivel"]:
            print(f"  {m['nome']}: {m['motivo']}")
    return 0


def cmd_worker(a) -> int:
    from . import worker
    return worker.loop(uma_vez=a.uma_vez, apenas=a.job)


def cmd_cancelar(a) -> int:
    def alterar(d: dict):
        if d.get("estado") not in ("pendente", "processando"):
            raise ValueError(f"job está '{d.get('estado')}': só dá para cancelar pendente ou processando")
        d["estado"] = "cancelado"
        job.registrar(d, d.get("etapa"), "cancelado pelo cli", salvar=False)
        return d
    try:
        job.atualizar_job(a.id, alterar)
    except (OSError, ValueError, TimeoutError) as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1
    print(f"job {a.id} cancelado (o worker para o motor em até ~3 s)")
    return 0


def montar_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="python -m oficina3d.cli", description="Oficina 3D: imagem(ns) -> malha 3D")
    sub = ap.add_subparsers(dest="comando", required=True)

    e = sub.add_parser("enviar", help="cria um job na fila")
    e.add_argument("--imagem", action="append", metavar="ARQ[:VISTA]", help="imagem (repetível); vista opcional")
    e.add_argument("--malha", help="malha .glb/.obj (modo so-refinar)")
    e.add_argument("--modo", default="livre", choices=config.MODOS)
    e.add_argument("--motor", default=None, help="padrão: automático (mv-turbo com 2+ vistas, mini-turbo com 1)")
    e.add_argument("--passos", type=int)
    e.add_argument("--octree", type=int)
    e.add_argument("--seed", type=int)
    e.add_argument("--alvo-triangulos", type=int, dest="alvo_triangulos")
    e.add_argument("--altura-m", type=float, dest="altura_m")
    e.add_argument("--sem-flashvdm", action="store_true", dest="sem_flashvdm")
    e.add_argument("--simetrizar", action="store_true")
    e.add_argument("--cor", action="store_true",
                   help="pinta a malha apos o refino (UV xatlas + bake T1; etapa opcional COR-05)")
    e.add_argument("--cor-modo", default=None, choices=config.MODOS_COR,
                   help="modo da etapa cor (COR-07): projecao = bake T1 (padrao); "
                        "vertice = cor de vertice T2 (rascunho); implica --cor")
    e.add_argument("--qualidade", default=None, choices=qualidades.NOMES,
                   help="perfil de qualidade QUAL-01 (bronze, prata, ouro, ouro-negro, lendario)")
    e.add_argument("--nome")
    e.add_argument("--esperar", action="store_true", help="acompanha o progresso até terminar")
    e.set_defaults(func=cmd_enviar)

    s = sub.add_parser("status", help="lista os jobs ou mostra um")
    s.add_argument("id", nargs="?")
    s.set_defaults(func=cmd_status)

    b = sub.add_parser("baixar", help="copia saida\\ de um job concluído")
    b.add_argument("id")
    b.add_argument("destino")
    b.set_defaults(func=cmd_baixar)

    m = sub.add_parser("motores", help="lista os motores e se estão disponíveis")
    m.set_defaults(func=cmd_motores)

    w = sub.add_parser("worker", help="roda o worker (processa a fila)")
    w.add_argument("--uma-vez", action="store_true", dest="uma_vez")
    w.add_argument("--job", action="append", metavar="ID")
    w.set_defaults(func=cmd_worker)

    c = sub.add_parser("cancelar", help="cancela um job pendente ou em processamento")
    c.add_argument("id")
    c.set_defaults(func=cmd_cancelar)
    return ap


def main(argv=None) -> int:
    _saida_utf8()
    a = montar_parser().parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
