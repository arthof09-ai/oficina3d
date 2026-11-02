"""Defesa estrutural do COLOR_0 exportado; nao substitui validador glTF completo."""
from __future__ import annotations

import json
import struct
from pathlib import Path


def verificar_glb_vertice(caminho):
    """Exige COLOR_0 completo em CADA primitivo e material referenciado.

    Checa cabecalho/JSON, indices, tipos e contagens dos acessores. Nao
    valida offsets/conteudo binario, cenas ou extensoes arbitrarias.
    Entrada malformada reprova com ok=False, sem excecao de parse.
    As contagens agregadas sao informativas, nunca a regra de aceite:
    deficit num primitivo nao pode ser compensado por excesso em outro.
    """
    result = {"color_0": False, "color_0_vertices": 0, "posicao_vertices": 0,
              "primitivos": 0, "primitivos_sem_cor": 0,
              "imagens_no_glb": 0, "materiais": 0, "ok": False}
    try:
        path = Path(caminho)
        with path.open("rb") as f:
            magic, version, total = struct.unpack("<III", f.read(12))
            if magic != 0x46546C67 or version != 2 or total != path.stat().st_size:
                raise ValueError("cabecalho GLB invalido")
            size, kind = struct.unpack("<II", f.read(8))
            if kind != 0x4E4F534A or size > total - 20 or size % 4:
                raise ValueError("bloco JSON invalido")
            doc = json.loads(f.read(size).decode("utf-8"))
        if not isinstance(doc, dict):
            raise ValueError("raiz JSON nao e objeto")
        meshes = doc.get("meshes", [])
        accessors = doc.get("accessors", [])
        materials = doc.get("materials", [])
        images = doc.get("images", [])
        if not all(isinstance(x, list) for x in (meshes, accessors, materials, images)):
            raise ValueError("colecao GLB invalida")
        prims = []
        for mesh in meshes:
            if not isinstance(mesh, dict) or not isinstance(mesh.get("primitives"), list):
                raise ValueError("mesh malformado")
            # Um mesh vazio tambem e invalido, mesmo com outros meshes bons.
            if not mesh["primitives"]:
                raise ValueError("mesh sem primitivos")
            prims.extend(mesh["primitives"])
        result.update(primitivos=len(prims), imagens_no_glb=len(images), materiais=len(materials))
        materials_ok = True

        def index_ok(index, sequence):
            return type(index) is int and 0 <= index < len(sequence)

        for prim in prims:
            if not isinstance(prim, dict):
                result["primitivos_sem_cor"] += 1
                materials_ok = False
                continue
            material = prim.get("material")
            materials_ok &= index_ok(material, materials) and isinstance(materials[material], dict)
            attrs = prim.get("attributes")
            if not isinstance(attrs, dict) or not all(index_ok(attrs.get(k), accessors) for k in ("POSITION", "COLOR_0")):
                result["primitivos_sem_cor"] += 1
                continue
            pos, color = accessors[attrs["POSITION"]], accessors[attrs["COLOR_0"]]
            if not isinstance(pos, dict) or not isinstance(color, dict):
                result["primitivos_sem_cor"] += 1
                continue
            np, nc = pos.get("count"), color.get("count")
            counts_ok = type(np) is int and type(nc) is int and np > 0 and nc > 0
            if counts_ok:
                result["posicao_vertices"] += np
                result["color_0_vertices"] += nc
            color_type_ok = color.get("componentType") == 5126 or (
                color.get("componentType") in (5121, 5123) and color.get("normalized") is True)
            if not (counts_ok and np == nc and pos.get("type") == "VEC3"
                    and pos.get("componentType") == 5126 and color.get("type") in ("VEC3", "VEC4")
                    and color_type_ok):
                result["primitivos_sem_cor"] += 1
        result["color_0"] = bool(prims) and result["primitivos_sem_cor"] == 0
        result["ok"] = result["color_0"] and materials_ok and not images
    except (OSError, ValueError, TypeError, struct.error) as exc:
        result["erro"] = str(exc)
    return result
