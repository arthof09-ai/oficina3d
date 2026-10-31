"""Baixa os modelos da Oficina 3D v2 a partir do manifesto_modelos.json.

Onde roda: no .venv_app (Python 3.10, tem huggingface_hub<1.0). Exemplo:
    %OFICINA3D_BASE%\\.venv_app\\Scripts\\python.exe baixar_modelos.py
Planejar sem baixar (só biblioteca padrão, qualquer Python >= 3.8, não grava nada):
    py -3.12 baixar_modelos.py --so-planejar

O que faz:
- trava em <BASE>\\locks\\download.lock (criação exclusiva, O_EXCL); um download por vez;
- retomável: pula o arquivo que já está com bytes e SHA256 certos; download direto usa <arquivo>.part
  com Range; o hf_hub_download retoma sozinho (.incomplete em <local_dir>\\.cache\\huggingface);
- confere bytes, SHA256 (e md5, se o manifesto tiver) antes de dar o arquivo por bom;
- quando o manifesto tinha sha256/bytes null, grava o valor medido de volta (gravação atômica);
- log em <BASE>\\_cache\\logs\\download_<AAAAMMDD>.log;
- PARA se o disco ficar com menos de --min-livre-gb (padrão 20 GiB) livres depois do download previsto;
- recusa qualquer destino em G:\\, no Google Drive ou em "Desktop\\RPG Assimilação".

Modos do manifesto:
- hf_local: hf_hub_download(local_dir=...) se o huggingface_hub existir; senão HTTP direto do
  https://huggingface.co/<repo>/resolve/<revisao>/<caminho> com .part;
- hf_cache: hf_hub_download(cache_dir=<BASE>\\_cache\\huggingface\\hub) (exige huggingface_hub);
- url: HTTP direto com .part.

Códigos de saída: 0 ok; 1 erro; 2 espaço insuficiente; 3 lock ocupado; 4 caminho proibido.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import shutil
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
MANIFESTO_PADRAO = AQUI / "manifesto_modelos.json"
GIB = 1024 ** 3
BLOCO = 8 * 1024 * 1024
URL_HF = "https://huggingface.co/{repo}/resolve/{rev}/{caminho}"
PROIBIDOS = ("\\desktop\\rpg assimila", "google drive", "googledrive", "\\meu drive", "\\my drive")


class Fatal(Exception):
    def __init__(self, msg: str, codigo: int = 1):
        super().__init__(msg)
        self.codigo = codigo


# ---------------------------------------------------------------- utilidades

class Log:
    def __init__(self, arquivo: Path | None):
        self.arquivo = arquivo

    def __call__(self, msg: str) -> None:
        linha = f"{_dt.datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
        print(linha, flush=True)
        if self.arquivo:
            with open(self.arquivo, "a", encoding="utf-8") as f:
                f.write(linha + "\n")


def gib(n: float) -> str:
    return f"{n / GIB:.2f} GiB"


def base_padrao() -> Path:
    env = os.environ.get("OFICINA3D_BASE")
    # app\instalacao\baixar_modelos.py -> parents[1] = BASE
    return Path(env) if env else AQUI.parents[1]


def conferir_caminho(p: Path, rotulo: str) -> None:
    """Fail-closed: nada pode ser gravado em G:, no Drive ou no espelho antigo do Desktop."""
    try:
        resolvido = p.resolve()  # segue junções/links já existentes
    except OSError:
        resolvido = p.absolute()
    for s in {str(p.absolute()), str(resolvido)}:
        s = s.replace("/", "\\").casefold()
        if s.startswith("g:") or s.startswith("\\\\?\\g:") or any(x in s for x in PROIBIDOS):
            raise Fatal(f"caminho proibido para {rotulo}: {p} (G:/Drive/Desktop\\RPG Assimilação)", 4)


def caminho_no_repo(item: dict) -> str:
    return f"{item['subpasta']}/{item['arquivo']}" if item.get("subpasta") else item["arquivo"]


def sha256_md5(p: Path, quer_md5: bool) -> tuple[str, str | None]:
    h = hashlib.sha256()
    m = hashlib.md5() if quer_md5 else None
    with open(p, "rb") as f:
        while True:
            b = f.read(16 * 1024 * 1024)
            if not b:
                break
            h.update(b)
            if m:
                m.update(b)
    return h.hexdigest(), (m.hexdigest() if m else None)


def tamanho_previsto(item: dict) -> int:
    return int(item.get("bytes") or item.get("bytes_estimado") or 0)


# ---------------------------------------------------------------- manifesto

def ler_manifesto(p: Path) -> dict:
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def recalcular_totais(man: dict) -> None:
    itens = man["itens"]
    conhecidos = sum(int(i["bytes"]) for i in itens if i.get("bytes"))
    estimados = sum(int(i.get("bytes_estimado") or 0) for i in itens if not i.get("bytes"))
    total = conhecidos + estimados
    man["totais"] = {
        "arquivos": len(itens),
        "bytes_medidos": conhecidos,
        "bytes_estimados_dos_sem_medida": estimados,
        "total_bytes": total,
        "total_gb_decimal": round(total / 1e9, 2),
        "total_gib": round(total / GIB, 2),
        "sem_sha256": sum(1 for i in itens if not i.get("sha256")),
        "nota": "GB decimal = 10^9 B; GiB = 2^30 B (é o 'GB' que o Explorador do Windows mostra).",
    }


def gravar_manifesto(p: Path, man: dict) -> None:
    recalcular_totais(man)
    tmp = p.with_name(p.name + ".tmp")
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(man, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp, p)


# ---------------------------------------------------------------- lock

def _pid_vivo(pid: int) -> bool | None:
    if os.name != "nt":
        try:
            os.kill(pid, 0)
            return True
        except OSError:
            return False
    try:
        import ctypes
        k = ctypes.windll.kernel32
        h = k.OpenProcess(0x1000, False, pid)  # PROCESS_QUERY_LIMITED_INFORMATION
        if not h:
            return False
        codigo = ctypes.c_ulong()
        k.GetExitCodeProcess(h, ctypes.byref(codigo))
        k.CloseHandle(h)
        return codigo.value == 259  # STILL_ACTIVE
    except Exception:
        return None


class Trava:
    def __init__(self, caminho: Path, limpar_orfao: bool):
        self.caminho = caminho
        self.limpar_orfao = limpar_orfao
        self.ok = False

    def __enter__(self):
        self.caminho.parent.mkdir(parents=True, exist_ok=True)
        for tentativa in (1, 2):
            try:
                fd = os.open(self.caminho, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except FileExistsError:
                try:
                    info = json.loads(self.caminho.read_text(encoding="utf-8"))
                except Exception:
                    info = {}
                pid = int(info.get("pid") or 0)
                vivo = _pid_vivo(pid) if pid else None
                if vivo is False and self.limpar_orfao and tentativa == 1:
                    self.caminho.unlink()
                    continue
                dica = ("o processo dono NÃO está rodando: use --limpar-lock-orfao ou apague o arquivo"
                        if vivo is False else "outro download está rodando (ou não deu para conferir)")
                raise Fatal(f"lock ocupado: {self.caminho} {info} -> {dica}", 3)
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                json.dump({"pid": os.getpid(), "inicio": _dt.datetime.now().isoformat(timespec="seconds"),
                           "script": "baixar_modelos.py"}, f)
            self.ok = True
            return self
        raise Fatal("não consegui criar o lock", 3)

    def __exit__(self, *exc):
        if self.ok:
            try:
                self.caminho.unlink()
            except OSError:
                pass


# ---------------------------------------------------------------- estado dos arquivos

def achar_no_cache_hf(base: Path, item: dict) -> Path | None:
    hub = base / item["destino"] / "hub"
    pasta = hub / ("models--" + item["repo"].replace("/", "--")) / "snapshots"
    if not pasta.is_dir():
        return None
    for snap in sorted(pasta.iterdir()):
        p = snap / Path(caminho_no_repo(item))
        if p.is_file():
            return p
    return None


def local_do_item(base: Path, item: dict) -> Path | None:
    if item["modo"] == "hf_cache":
        return achar_no_cache_hf(base, item)
    return base / item["destino"]


def parcial(base: Path, item: dict) -> int:
    if item["modo"] == "hf_cache":
        return 0
    p = base / item["destino"]
    part = p.with_name(p.name + ".part")
    return part.stat().st_size if part.is_file() else 0


def conferir(p: Path, item: dict, log: Log, pesado: bool = True) -> tuple[bool, str, dict]:
    """Devolve (ok, motivo, medidas). Com pesado=False só olha bytes (para o plano)."""
    n = p.stat().st_size
    medidas = {"bytes": n}
    if item.get("bytes") and n != int(item["bytes"]):
        return False, f"bytes {n} != {item['bytes']}", medidas
    if not pesado:
        return True, "bytes ok (sha não conferido no plano)", medidas
    t = time.time()
    sha, md5 = sha256_md5(p, bool(item.get("md5")))
    medidas["sha256"] = sha
    log(f"  sha256 {sha} ({time.time() - t:.0f}s)")
    if item.get("sha256") and sha.lower() != item["sha256"].lower():
        return False, f"sha256 {sha} != {item['sha256']}", medidas
    if item.get("md5") and md5 and md5.lower() != item["md5"].lower():
        return False, f"md5 {md5} != {item['md5']}", medidas
    return True, "ok", medidas


# ---------------------------------------------------------------- download

def baixar_http(url: str, destino: Path, esperado: int | None, log: Log, tentativas: int = 4) -> Path:
    destino.parent.mkdir(parents=True, exist_ok=True)
    part = destino.with_name(destino.name + ".part")
    for t in range(1, tentativas + 1):
        ja = part.stat().st_size if part.exists() else 0
        if esperado and ja > esperado:
            log(f"  .part maior que o esperado ({ja} > {esperado}); recomeçando")
            part.unlink()
            ja = 0
        if esperado and ja == esperado:
            return part
        cab = {"User-Agent": "oficina3d-baixar-modelos/2"}
        if ja:
            cab["Range"] = f"bytes={ja}-"
        try:
            req = urllib.request.Request(url, headers=cab)
            with urllib.request.urlopen(req, timeout=60) as r:
                if ja and r.status != 206:
                    log("  servidor ignorou o Range; recomeçando do zero")
                    ja = 0
                modo = "ab" if ja else "wb"
                total = ja + int(r.headers.get("Content-Length") or 0)
                proximo_aviso = ja + 512 * 1024 * 1024
                t0, n0 = time.time(), ja
                with open(part, modo) as f:
                    while True:
                        b = r.read(BLOCO)
                        if not b:
                            break
                        f.write(b)
                        ja += len(b)
                        if ja >= proximo_aviso:
                            vel = (ja - n0) / max(time.time() - t0, 0.001) / 2**20
                            log(f"  {gib(ja)} de {gib(total)} ({vel:.0f} MiB/s)")
                            proximo_aviso += 512 * 1024 * 1024
            return part
        except urllib.error.HTTPError as e:
            if e.code == 416 and ja:  # Range além do fim: o .part já está completo
                return part
            log(f"  HTTP {e.code} na tentativa {t}: {e}")
            if 400 <= e.code < 500 and e.code not in (408, 429):
                raise Fatal(f"HTTP {e.code} em {url}")
        except (urllib.error.URLError, OSError, TimeoutError) as e:
            log(f"  falha de rede na tentativa {t}: {e}")
        time.sleep(min(60, 5 * t))
    raise Fatal(f"download não terminou após {tentativas} tentativas: {url}")


def baixar_item(base: Path, item: dict, usar_hf: bool, log: Log) -> Path:
    modo = item["modo"]
    caminho = caminho_no_repo(item)
    if modo == "url":
        part = baixar_http(item["url"], base / item["destino"], item.get("bytes"), log)
        return part
    if modo == "hf_cache":
        if not usar_hf:
            raise Fatal(f"{item['id']}: modo hf_cache exige huggingface_hub (rode no .venv_app)")
        from huggingface_hub import hf_hub_download
        return Path(hf_hub_download(repo_id=item["repo"], filename=caminho, revision=item.get("revisao") or "main",
                                    cache_dir=str(base / item["destino"] / "hub")))
    if modo == "hf_local":
        destino = base / item["destino"]
        sufixo = Path(caminho)
        if Path(item["destino"]).parts[-len(sufixo.parts):] != sufixo.parts:
            raise Fatal(f"{item['id']}: destino não termina em {caminho}")
        if usar_hf:
            from huggingface_hub import hf_hub_download
            raiz = destino
            for _ in sufixo.parts:
                raiz = raiz.parent
            return Path(hf_hub_download(repo_id=item["repo"], filename=caminho,
                                        revision=item.get("revisao") or "main", local_dir=str(raiz)))
        url = URL_HF.format(repo=item["repo"], rev=item.get("revisao") or "main", caminho=caminho)
        return baixar_http(url, destino, item.get("bytes"), log)
    raise Fatal(f"{item['id']}: modo desconhecido {modo}")


# ---------------------------------------------------------------- principal

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Baixa os modelos da Oficina 3D pelo manifesto.")
    ap.add_argument("--manifesto", type=Path, default=MANIFESTO_PADRAO)
    ap.add_argument("--base", type=Path, default=None, help="OFICINA3D_BASE (padrão: env ou 2 pastas acima)")
    ap.add_argument("--so-planejar", action="store_true", help="só imprime o que baixaria e o total; não grava nada")
    ap.add_argument("--min-livre-gb", type=float, default=20.0, help="GiB livres exigidos depois do download")
    ap.add_argument("--prioridade-max", type=int, default=99, help="só itens com prioridade <= N")
    ap.add_argument("--ids", nargs="*", default=None, help="só estes ids do manifesto")
    ap.add_argument("--sem-hf", action="store_true", help="não usar huggingface_hub (HTTP direto com .part)")
    ap.add_argument("--limpar-lock-orfao", action="store_true", help="apaga o lock se o PID dono já morreu")
    a = ap.parse_args(argv)

    base = (a.base or base_padrao()).absolute()
    planejar = a.so_planejar
    log = Log(None)
    try:
        conferir_caminho(base, "OFICINA3D_BASE")
        for var in ("HF_HOME", "HY3DGEN_MODELS", "U2NET_HOME"):
            if os.environ.get(var):
                conferir_caminho(Path(os.environ[var]), var)
        man = ler_manifesto(a.manifesto)
        itens = [i for i in man["itens"] if int(i.get("prioridade", 1)) <= a.prioridade_max
                 and (a.ids is None or i["id"] in a.ids)]
        itens.sort(key=lambda i: int(i.get("prioridade", 1)))  # sort estável: mantém a ordem do manifesto
        for i in itens:
            conferir_caminho(base / i["destino"], i["id"])

        usar_hf = False
        if not a.sem_hf:
            try:
                import huggingface_hub  # noqa: F401
                usar_hf = True
            except ImportError:
                usar_hf = False

        # ---- plano (não grava nada)
        pend_total = 0
        linhas = []
        for i in itens:
            p = local_do_item(base, i)
            if p and p.is_file():
                ok, motivo, _ = conferir(p, i, log, pesado=False)
                estado = "PRESENTE" if ok else f"DIVERGENTE ({motivo})"
                falta = 0 if ok else tamanho_previsto(i)
            else:
                ja = parcial(base, i)
                falta = max(0, tamanho_previsto(i) - ja)
                estado = "BAIXAR" + (f" (retoma, {gib(ja)} no .part)" if ja else "")
            pend_total += falta
            linhas.append(f"  [{i.get('prioridade', 1)}] {i['id']:<26} {tamanho_previsto(i) / 1e9:7.3f} GB  {estado}")
        livre = shutil.disk_usage(base.anchor or str(base)).free
        depois = livre - pend_total
        todos = sum(tamanho_previsto(i) for i in itens)
        print(f"Manifesto: {a.manifesto}")
        print(f"BASE: {base}   huggingface_hub: {'sim' if usar_hf else 'não'}")
        print("\n".join(linhas))
        print(f"Total do conjunto: {todos:,} B = {todos / 1e9:.2f} GB = {gib(todos)}")
        print(f"A baixar agora:    {pend_total:,} B = {pend_total / 1e9:.2f} GB = {gib(pend_total)}")
        print(f"Livre no {base.anchor}: {gib(livre)}; depois do download: {gib(depois)} (mínimo {a.min_livre_gb:g} GiB)")
        espaco_ok = depois / GIB >= a.min_livre_gb
        if planejar:
            if not espaco_ok:
                print("PARARIA: espaço insuficiente.")
                return 2
            if not usar_hf and any(i["modo"] == "hf_cache" for i in itens):
                print("AVISO: sem huggingface_hub neste Python; a execução real precisa rodar no .venv_app.")
            print("Plano apenas (--so-planejar): nada foi gravado.")
            return 0
        if not espaco_ok:
            raise Fatal(f"espaço insuficiente: ficariam {gib(depois)} livres (< {a.min_livre_gb:g} GiB)", 2)

        # ---- execução
        logs = base / "_cache" / "logs"
        logs.mkdir(parents=True, exist_ok=True)
        log = Log(logs / f"download_{_dt.date.today():%Y%m%d}.log")
        os.environ.setdefault("HF_HOME", str(base / "_cache" / "huggingface"))
        os.environ.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")
        os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
        with Trava(base / "locks" / "download.lock", a.limpar_lock_orfao):
            log(f"INICIO base={base} itens={len(itens)} a_baixar={pend_total:,} B hf={usar_hf}")
            t_geral = time.time()
            for i in itens:
                log(f"-- {i['id']} ({i.get('repo') or i.get('url')}: {caminho_no_repo(i)})")
                p = local_do_item(base, i)
                if p and p.is_file():
                    ok, motivo, med = conferir(p, i, log)
                    if ok:
                        log("  já presente e conferido: pula")
                        _registrar(a.manifesto, man, i, med, log)
                        continue
                    raise Fatal(f"{i['id']}: arquivo existente DIVERGENTE ({motivo}) em {p}. "
                                "Confira e apague/renomeie à mão; não sobrescrevo.")
                t = time.time()
                obtido = baixar_item(base, i, usar_hf, log)
                ok, motivo, med = conferir(obtido, i, log)
                if not ok:
                    ruim = obtido.with_name(obtido.name + ".divergente")
                    os.replace(obtido, ruim)
                    raise Fatal(f"{i['id']}: download não confere ({motivo}); guardado em {ruim}")
                if obtido.name.endswith(".part"):
                    final = obtido.with_name(obtido.name[:-5])
                    os.replace(obtido, final)
                    obtido = final
                log(f"  OK {med['bytes']:,} B em {time.time() - t:.0f}s -> {obtido}")
                _registrar(a.manifesto, man, i, med, log)
            log(f"FIM ok em {(time.time() - t_geral) / 60:.1f} min")
        return 0
    except Fatal as e:
        log(f"ERRO: {e}")
        return e.codigo
    except KeyboardInterrupt:
        log("INTERROMPIDO: rode de novo para retomar")
        return 1


def _registrar(caminho_man: Path, man: dict, item: dict, medidas: dict, log: Log) -> None:
    """Grava bytes/sha256 medidos no manifesto quando lá estavam null."""
    mudou = False
    if not item.get("bytes") and medidas.get("bytes"):
        item["bytes"] = medidas["bytes"]
        item.pop("bytes_estimado", None)
        mudou = True
    if not item.get("sha256") and medidas.get("sha256"):
        item["sha256"] = medidas["sha256"]
        item["sha256_medido_em"] = _dt.date.today().isoformat()
        mudou = True
    if mudou:
        gravar_manifesto(caminho_man, man)
        log(f"  manifesto atualizado ({item['id']}: bytes/sha256 medidos)")


if __name__ == "__main__":
    sys.exit(main())
