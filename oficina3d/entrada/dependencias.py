"""Importação preguiçosa das dependências pesadas, com mensagem clara se faltarem.

Nada aqui instala ou baixa coisa alguma: os pacotes vêm do instalador da Oficina
(`instalacao\\`, venv do app) e o modelo u2net vem do manifesto de modelos.
"""
from __future__ import annotations

import importlib


class DependenciaAusente(ImportError):
    """Falta um pacote Python que esta etapa precisa."""


class ModeloAusente(FileNotFoundError):
    """Falta um arquivo de modelo (ex.: u2net.onnx) no cache da Oficina."""


# módulo importável -> nome do pacote no pip (só para a mensagem)
_PACOTE_PIP = {
    "numpy": "numpy",
    "PIL": "Pillow",
    "PIL.Image": "Pillow",
    "PIL.ImageOps": "Pillow",
    "cv2": "opencv-python-headless (ou opencv-python)",
    "rembg": "rembg",
    "onnxruntime": "onnxruntime",
}


def exigir(modulo: str, para: str):
    """Importa `modulo` ou levanta DependenciaAusente explicando o que falta e para quê."""
    try:
        return importlib.import_module(modulo)
    except ImportError as erro:
        pacote = _PACOTE_PIP.get(modulo, modulo.split(".")[0])
        raise DependenciaAusente(
            f"Falta o pacote '{pacote}' (módulo '{modulo}') no Python do app, necessário para "
            f"{para}. Ele vem no instalador da Oficina 3D (venv do app, pelo lock); "
            f"este módulo não instala nada sozinho. Detalhe: {erro}"
        ) from erro


def disponivel(modulo: str) -> bool:
    """True se o módulo importa (usado para pular testes/recursos opcionais)."""
    try:
        importlib.import_module(modulo)
        return True
    except ImportError:
        return False
