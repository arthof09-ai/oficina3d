"""Remoção de fundo com rembg + u2net (licença livre; NÃO usar RMBG, que é não comercial).

Regras:
- O modelo fica em U2NET_HOME (do config: `_cache\\u2net\\u2net.onnx`).
- Nunca baixa nada: se o u2net.onnx faltar, levanta ModeloAusente com o caminho esperado.
  (o rembg baixaria sozinho pelo pooch; aqui o arquivo é conferido ANTES e a checagem de
  MD5 do rembg é desligada, para que um arquivo existente nunca dispare novo download.)
- Roda na CPU (u2net é leve; a GPU fica para o motor de forma).
"""
from __future__ import annotations

import io
import os
from pathlib import Path

from .dependencias import ModeloAusente, exigir
from .imagem import limpar_alfa

NOME_MODELO = "u2net"
ARQUIVO_MODELO = "u2net.onnx"
TAMANHO_MINIMO = 1_000_000      # o u2net.onnx tem ~176 MB; menos de 1 MB = arquivo quebrado

_sessao = None
_sessao_pasta = None


def pasta_u2net() -> Path:
    """Pasta do u2net segundo o config (U2NET_HOME); variável de ambiente só como reserva."""
    try:
        from .. import config
    except ImportError:
        config = None
    if config is not None:
        valor = getattr(config, "U2NET_HOME", None)
        if valor:
            return Path(valor)
        if hasattr(config, "env_subprocesso"):
            env = config.env_subprocesso()
            if env.get("U2NET_HOME"):
                return Path(env["U2NET_HOME"])
        cache = getattr(config, "CACHE", None)
        if cache:
            return Path(cache) / "u2net"
    if os.environ.get("U2NET_HOME"):
        return Path(os.environ["U2NET_HOME"])
    raise ModeloAusente(
        "Não sei onde fica o u2net: o oficina3d.config não define U2NET_HOME/CACHE "
        "e a variável de ambiente U2NET_HOME não está definida."
    )


def caminho_modelo() -> Path:
    """Caminho do u2net.onnx, conferido. Levanta ModeloAusente se faltar ou estiver quebrado."""
    pasta = pasta_u2net()
    arq = pasta / ARQUIVO_MODELO
    if not arq.is_file():
        raise ModeloAusente(
            f"Modelo de remoção de fundo não encontrado: {arq}. Baixe-o pelo instalador "
            f"(manifesto de modelos, item u2net) — a entrada não baixa nada sozinha. "
            f"Enquanto isso, mande PNG com fundo transparente ou use remover_fundo='nao'."
        )
    tamanho = arq.stat().st_size
    if tamanho < TAMANHO_MINIMO:
        raise ModeloAusente(
            f"O arquivo {arq} parece quebrado ({tamanho} bytes; o u2net tem ~176 MB). "
            f"Baixe de novo pelo instalador e confira o SHA256 do manifesto."
        )
    return arq


def _obter_sessao():
    global _sessao, _sessao_pasta
    modelo = caminho_modelo()                     # confere ANTES de importar o rembg
    if _sessao is not None and _sessao_pasta == modelo.parent:
        return _sessao
    exigir("onnxruntime", "remover o fundo das imagens (rembg)")
    os.environ["U2NET_HOME"] = str(modelo.parent)
    os.environ["MODEL_CHECKSUM_DISABLED"] = "1"   # arquivo existente => o pooch não baixa de novo
    rembg = exigir("rembg", "remover o fundo das imagens")
    try:
        sessao = rembg.new_session(NOME_MODELO, providers=["CPUExecutionProvider"])
    except TypeError:                             # versões antigas sem 'providers'
        sessao = rembg.new_session(NOME_MODELO)
    _sessao, _sessao_pasta = sessao, modelo.parent
    return sessao


def remover_fundo(arr, manter_alfa_original: bool = False):
    """Recorta o objeto com rembg/u2net. `arr` RGBA uint8 -> RGBA uint8 com alfa limpo (<=10 -> 0).

    Se `manter_alfa_original`, o alfa final é o mínimo entre o do rembg e o original
    (útil quando a imagem já tinha alfa, mas com sujeira).
    """
    np = exigir("numpy", "remover o fundo das imagens")
    Image = exigir("PIL.Image", "remover o fundo das imagens")
    sessao = _obter_sessao()
    rembg = exigir("rembg", "remover o fundo das imagens")
    rgb = Image.fromarray(np.ascontiguousarray(arr[..., :3]), "RGB")
    saida = rembg.remove(rgb, session=sessao)
    if isinstance(saida, (bytes, bytearray)):     # algumas versões devolvem bytes ou ndarray
        saida = Image.open(io.BytesIO(saida))
    elif not isinstance(saida, Image.Image):
        saida = Image.fromarray(np.asarray(saida))
    res = np.array(saida.convert("RGBA"), dtype=np.uint8)
    if res.shape[:2] != arr.shape[:2]:
        raise RuntimeError(f"rembg devolveu tamanho diferente: {res.shape[:2]} != {arr.shape[:2]}")
    res[..., :3] = arr[..., :3]                   # cor original; o rembg só decide o alfa
    if manter_alfa_original:
        res[..., 3] = np.minimum(res[..., 3], arr[..., 3])
    return limpar_alfa(res)
