"""Etapa 11 do worker: arquivar o job concluído no Drive e liberar o disco.

Plano v2, seção 5.1: ao concluir um job, copiar `saida\\` (e o `relatorio.json`)
para `<Drive>\\Oficina3D_v2\\arquivo_jobs\\<id>\\`, conferir o hash e só então
apagar a cópia local. Aprovado (com nota do Mestre) vai na hora; sem nota, depois
de 3 dias.

Garantias:
- NUNCA apaga sem conferir: cada arquivo é relido DO DESTINO e o SHA256 tem de
  bater com o da origem; o manifesto também é relido e conferido.
- Se algo mudou na `saida\\` durante a cópia (arquivo novo, tamanho ou data
  diferente), não apaga.
- Destino não definido (variável OFICINA3D_ARQUIVO) → não arquiva, só avisa.
- Destino inacessível (sem internet, Drive desligado) ou erro de cópia → o job
  fica na fila ("pendente") e é tentado de novo na próxima rodada.
- Retomável: arquivo que já está no destino com o hash certo não é recopiado.

Destino (`destino_raiz`): a pasta `Oficina3D_v2` do Drive (ex.: na unidade G:
em streaming). O app grava em `<destino_raiz>\\arquivo_jobs\\<id>\\`.

Limite conhecido: pelo G: (Drive para computador), reler o destino confere a
cópia que o Drive recebeu; o envio para a nuvem é assíncrono. Para conferir
contra a nuvem, passe `conferir_extra` (ex.: um verificador com `rclone`).
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import shutil
import stat
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable

from oficina3d.travas import caminho_config

log = logging.getLogger("oficina3d.arquivar")

ENV_DESTINO = "OFICINA3D_ARQUIVO"
SUBPASTA = "arquivo_jobs"
MANIFESTO = "manifesto_sha256.json"
RECIBO = "arquivamento.json"      # gravado na pasta local do job
DIAS_SEM_NOTA = 3
_ID_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,80}$")
_BLOCO = 1024 * 1024


# --------------------------------------------------------------------------- utilidades

def sha256_arquivo(caminho: Path) -> str:
    h = hashlib.sha256()
    with open(caminho, "rb") as f:
        while True:
            bloco = f.read(_BLOCO)
            if not bloco:
                break
            h.update(bloco)
    return h.hexdigest()


def _agora() -> datetime:
    return datetime.now().astimezone()


def _registrar_log(job_dir: Path, msg: str) -> None:
    """Uma linha no log.txt do job (além do logging)."""
    try:
        with open(job_dir / "log.txt", "a", encoding="utf-8") as f:
            f.write(f"{_agora().isoformat(timespec='seconds')} [arquivar] {msg}\n")
    except OSError:
        pass


def _ler_json(caminho: Path) -> dict | None:
    try:
        with open(caminho, encoding="utf-8") as f:
            dado = json.load(f)
        return dado if isinstance(dado, dict) else None
    except (OSError, ValueError):
        return None


def destino_padrao() -> Path | None:
    valor = os.environ.get(ENV_DESTINO, "").strip().strip('"')
    return Path(valor) if valor else None


def _copiar_arquivo(origem: Path, destino: Path) -> None:
    """Copia para `<destino>.parcial` e renomeia (não deixa arquivo pela metade com o nome final)."""
    destino.parent.mkdir(parents=True, exist_ok=True)
    parcial = destino.with_name(destino.name + ".parcial")
    shutil.copyfile(origem, parcial)
    os.replace(parcial, destino)


def _gravar_conferido(caminho: Path, dados: bytes) -> bool:
    """Grava `dados` e relê do destino para conferir."""
    parcial = caminho.with_name(caminho.name + ".parcial")
    with open(parcial, "wb") as f:
        f.write(dados)
        f.flush()
        os.fsync(f.fileno())
    os.replace(parcial, caminho)
    return hashlib.sha256(caminho.read_bytes()).digest() == hashlib.sha256(dados).digest()


def _listar(job_dir: Path) -> dict[str, Path]:
    """{caminho relativo com '/' : Path} do que vai para o arquivo: saida\\ + relatorio.json."""
    itens: dict[str, Path] = {}
    saida = job_dir / "saida"
    if saida.is_dir():
        for p in sorted(saida.rglob("*")):
            if p.is_file() and not p.name.endswith(".parcial"):
                itens[p.relative_to(job_dir).as_posix()] = p
    rel = job_dir / "relatorio.json"
    if rel.is_file():
        itens["relatorio.json"] = rel
    return itens


def _assinatura(p: Path) -> tuple[int, int]:
    st = p.stat()
    return st.st_size, st.st_mtime_ns


def _apagar_arvore(pasta: Path) -> None:
    def _forcar(func, caminho, _exc):  # arquivo somente-leitura: tira o atributo e tenta de novo
        os.chmod(caminho, stat.S_IWRITE)
        func(caminho)
    if sys.version_info >= (3, 12):
        shutil.rmtree(pasta, onexc=_forcar)
    else:
        shutil.rmtree(pasta, onerror=_forcar)


def _resultado(estado: str, job_id: str, msg: str, **extra) -> dict:
    r = {"id": job_id, "estado": estado, "msg": msg}
    r.update(extra)
    return r


# --------------------------------------------------------------------------- arquivar um job

def arquivar_job(job_dir: Path | str, destino_raiz: Path | str | None = None, *,
                 apagar_local: bool = True,
                 conferir_extra: Callable[[Path, dict], bool] | None = None) -> dict:
    """Copia `saida\\` + `relatorio.json` do job para `<destino_raiz>\\arquivo_jobs\\<id>\\`,
    confere o SHA256 relendo do destino, grava o manifesto e só então apaga `saida\\`.

    Devolve {"id", "estado", "msg", ...}. Estados:
    - "arquivado": copiado e conferido (e `apagado`: True/False diz se liberou o disco);
    - "sem_destino": OFICINA3D_ARQUIVO não definida e nenhum destino passado (nada feito);
    - "pendente": destino inacessível ou erro de E/S (fica na fila; nada apagado);
    - "erro": hash não bateu ou entrada inválida (nada apagado);
    - "nada": não há o que arquivar (sem `saida\\`).
    Campos extras quando arquivado: "destino" (pasta no Drive; vai como link no
    relatorio do worker), "manifesto", "arquivos", "bytes", "apagado".
    """
    job_dir = Path(job_dir)
    job = _ler_json(job_dir / "job.json") or {}
    job_id = str(job.get("id") or job_dir.name)
    if not _ID_OK.match(job_id):
        return _resultado("erro", job_id, "id do job inválido para usar como pasta")

    raiz = Path(destino_raiz) if destino_raiz else destino_padrao()
    if raiz is None:
        msg = f"{ENV_DESTINO} não definida: job não arquivado (fica no disco)"
        log.warning("%s: %s", job_id, msg)
        return _resultado("sem_destino", job_id, msg)

    itens = _listar(job_dir)
    if not (job_dir / "saida").is_dir() or not itens:
        return _resultado("nada", job_id, "sem saida\\ para arquivar")

    try:
        raiz_ok = raiz.is_dir()
    except OSError:
        raiz_ok = False
    if not raiz_ok:
        msg = f"destino inacessível ({raiz}); fica na fila"
        log.warning("%s: %s", job_id, msg)
        return _resultado("pendente", job_id, msg)

    destino = raiz / SUBPASTA / job_id
    try:
        if destino.resolve().is_relative_to(job_dir.resolve()):
            return _resultado("erro", job_id, "destino dentro da pasta do job")
    except (OSError, ValueError):
        pass

    _registrar_log(job_dir, f"arquivando {len(itens)} arquivo(s) em {destino}")
    entradas: list[dict] = []
    assinaturas: dict[str, tuple[int, int]] = {}
    total = 0
    try:
        destino.mkdir(parents=True, exist_ok=True)
        for rel, origem in itens.items():
            assinaturas[rel] = _assinatura(origem)
            h_origem = sha256_arquivo(origem)
            alvo = destino.joinpath(*rel.split("/"))
            ja_ok = alvo.is_file() and alvo.stat().st_size == assinaturas[rel][0] \
                and sha256_arquivo(alvo) == h_origem
            if not ja_ok:
                _copiar_arquivo(origem, alvo)
                h_destino = sha256_arquivo(alvo)  # relê DO DESTINO
                if h_destino != h_origem:
                    msg = f"SHA256 não bateu em {rel} (origem {h_origem[:12]}…, destino {h_destino[:12]}…); nada apagado"
                    log.error("%s: %s", job_id, msg)
                    _registrar_log(job_dir, msg)
                    return _resultado("erro", job_id, msg, destino=str(destino))
            entradas.append({"caminho": rel, "bytes": assinaturas[rel][0], "sha256": h_origem})
            total += assinaturas[rel][0]

        # Une com um manifesto anterior (retomada após apagamento parcial).
        anterior = _ler_json(destino / MANIFESTO) or {}
        novos = {e["caminho"] for e in entradas}
        for e in anterior.get("arquivos", []) or []:
            if isinstance(e, dict) and e.get("caminho") not in novos \
                    and destino.joinpath(*str(e["caminho"]).split("/")).is_file():
                entradas.append(e)
        entradas.sort(key=lambda e: e["caminho"])
        manifesto = {
            "versao": 1,
            "id": job_id,
            "arquivado_em": _agora().isoformat(timespec="seconds"),
            "algoritmo": "sha256",
            "arquivos": entradas,
            "total_bytes": sum(int(e.get("bytes", 0)) for e in entradas),
        }
        dados = json.dumps(manifesto, ensure_ascii=False, indent=2).encode("utf-8")
        if not _gravar_conferido(destino / MANIFESTO, dados):
            msg = "manifesto gravado não confere ao reler; nada apagado"
            _registrar_log(job_dir, msg)
            return _resultado("erro", job_id, msg, destino=str(destino))
        sha_manifesto = hashlib.sha256(dados).hexdigest()
    except OSError as e:
        msg = f"erro de E/S ao copiar ({e}); fica na fila, nada apagado"
        log.warning("%s: %s", job_id, msg)
        _registrar_log(job_dir, msg)
        return _resultado("pendente", job_id, msg, destino=str(destino))

    if conferir_extra is not None:
        try:
            ok_extra = bool(conferir_extra(destino, manifesto))
        except Exception as e:  # noqa: BLE001
            ok_extra, msg_extra = False, f"conferência extra falhou: {e}"
        else:
            msg_extra = "conferência extra recusou"
        if not ok_extra:
            _registrar_log(job_dir, msg_extra + "; nada apagado")
            return _resultado("pendente", job_id, msg_extra + "; fica na fila, nada apagado",
                              destino=str(destino))

    base = dict(destino=str(destino), manifesto=str(destino / MANIFESTO), sha256_manifesto=sha_manifesto,
                arquivos=len(entradas), bytes=manifesto["total_bytes"])
    if not apagar_local:
        _registrar_log(job_dir, "arquivado e conferido (cópia local mantida)")
        return _resultado("arquivado", job_id, "arquivado e conferido; cópia local mantida",
                          apagado=False, **base)

    # Última conferência antes de apagar: nada mudou na saida\ desde a cópia.
    atuais = _listar(job_dir)
    mudou = set(atuais) != set(itens) or any(
        _assinatura(p) != assinaturas.get(rel) for rel, p in atuais.items())
    if mudou:
        msg = "saida\\ mudou durante o arquivamento; arquivado, mas cópia local mantida"
        log.warning("%s: %s", job_id, msg)
        _registrar_log(job_dir, msg)
        return _resultado("arquivado", job_id, msg, apagado=False, **base)

    recibo = {"id": job_id, "arquivado_em": manifesto["arquivado_em"], "destino": str(destino),
              "manifesto": str(destino / MANIFESTO), "sha256_manifesto": sha_manifesto,
              "arquivos": len(entradas), "bytes": manifesto["total_bytes"]}
    try:
        _gravar_conferido(job_dir / RECIBO, json.dumps(recibo, ensure_ascii=False, indent=2).encode("utf-8"))
        _apagar_arvore(job_dir / "saida")
    except OSError as e:
        msg = f"arquivado e conferido, mas falhou ao apagar saida\\ ({e})"
        log.warning("%s: %s", job_id, msg)
        _registrar_log(job_dir, msg)
        return _resultado("arquivado", job_id, msg, apagado=False, **base)

    _registrar_log(job_dir, f"arquivado e conferido ({len(entradas)} arquivo(s)); saida\\ local apagada")
    return _resultado("arquivado", job_id, "arquivado e conferido; saida\\ local apagada", apagado=True, **base)


# --------------------------------------------------------------------------- política (fila)

def tem_nota(job: dict, job_dir: Path | None = None) -> bool:
    """O Mestre já deu nota? Aceita `nota`/`nota_mestre` preenchidos, `aprovado: true`,
    ou um `nota.json` na pasta do job. (Convenção a alinhar com worker/web.)"""
    for chave in ("nota", "nota_mestre"):
        if job.get(chave) not in (None, "", [], {}):
            return True
    if job.get("aprovado") is True:
        return True
    return bool(job_dir and (job_dir / "nota.json").is_file())


def _parse_data(valor) -> datetime | None:
    if not isinstance(valor, str) or not valor:
        return None
    try:
        d = datetime.fromisoformat(valor.replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.astimezone()


def concluido_em(job: dict, job_dir: Path) -> datetime | None:
    """Quando o job terminou: `concluido_em`, senão o último `historico[].quando`,
    senão a data do `saida\\relatorio.json` (ou da própria `saida\\`)."""
    d = _parse_data(job.get("concluido_em"))
    if d:
        return d
    for item in reversed(job.get("historico") or []):
        if isinstance(item, dict):
            d = _parse_data(item.get("quando"))
            if d:
                return d
    for p in (job_dir / "saida" / "relatorio.json", job_dir / "relatorio.json", job_dir / "saida"):
        if p.exists():
            return datetime.fromtimestamp(p.stat().st_mtime).astimezone()
    return None


def arquivar_pendentes(jobs_dir: Path | str | None = None, destino_raiz: Path | str | None = None, *,
                       agora: datetime | None = None, dias_sem_nota: float = DIAS_SEM_NOTA,
                       urgente: bool = False,
                       conferir_extra: Callable[[Path, dict], bool] | None = None) -> list[dict]:
    """Passa pela fila e arquiva o que já pode ir:
    - job `concluido` com nota do Mestre → na hora;
    - job `concluido` sem nota → depois de `dias_sem_nota` (3) dias;
    - `urgente=True` (disco abaixo de 20 GB) → arquiva os concluídos sem esperar.
    Jobs em outro estado, ou já arquivados (sem `saida\\`), são ignorados.
    Sem destino definido: não arquiva nada e devolve um item "sem_destino" por job elegível.
    """
    jobs_dir = Path(jobs_dir) if jobs_dir else caminho_config("JOBS")
    agora = agora or _agora()
    if agora.tzinfo is None:
        agora = agora.astimezone()
    raiz = Path(destino_raiz) if destino_raiz else destino_padrao()
    resultados: list[dict] = []
    if not jobs_dir.is_dir():
        return resultados

    elegiveis: list[tuple[Path, dict]] = []
    for pasta in sorted(p for p in jobs_dir.iterdir() if p.is_dir()):
        job = _ler_json(pasta / "job.json")
        if not job or job.get("estado") != "concluido" or not (pasta / "saida").is_dir():
            continue
        if tem_nota(job, pasta) or urgente:
            elegiveis.append((pasta, job))
            continue
        fim = concluido_em(job, pasta)
        if fim is not None and agora - fim >= timedelta(days=dias_sem_nota):
            elegiveis.append((pasta, job))

    if raiz is None:
        if elegiveis:
            log.warning("%s não definida: %d job(s) prontos para arquivar ficam no disco",
                        ENV_DESTINO, len(elegiveis))
        return [_resultado("sem_destino", str(j.get("id") or p.name), f"{ENV_DESTINO} não definida")
                for p, j in elegiveis]

    for pasta, _job in elegiveis:
        try:
            resultados.append(arquivar_job(pasta, raiz, conferir_extra=conferir_extra))
        except Exception as e:  # noqa: BLE001 - um job ruim não para a fila
            log.exception("falha inesperada ao arquivar %s", pasta.name)
            resultados.append(_resultado("erro", pasta.name, f"falha inesperada: {e}"))
    return resultados
