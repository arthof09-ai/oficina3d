"""Leitura de codigo da base publica congelada, sem checkout e sem importar bpy."""
import ast
from pathlib import Path
import subprocess
import types

BASE = "5cd092d37bddf36a2d888404936d4c9f394528c4"
ROOT = Path(__file__).resolve().parents[1]


def fonte(arquivo):
    return subprocess.check_output(["git", "show", f"{BASE}:{arquivo}"], cwd=ROOT).decode("utf-8")


def modulo(arquivo):
    mod = types.ModuleType("publicado_nuvem")
    exec(compile(fonte(arquivo), f"{BASE}:{arquivo}", "exec"), vars(mod))
    return mod


def funcao(codigo, nome, escopo):
    tree = ast.parse(codigo)
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == nome)
    exec(compile(ast.Module(body=[node], type_ignores=[]), "<funcao-isolada-CPU>", "exec"), escopo)
    return escopo[nome]
