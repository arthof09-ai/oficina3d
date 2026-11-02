"""Leitura do GLB em Python puro (sem trimesh, sem numpy): cabeçalho, chunks e contagens.

É a primeira régua do validador: não depende do Godot e roda em qualquer Python.
Confere os "magic bytes" do plano (GLB 'glTF' versão 2, comprimento batendo com o arquivo,
chunk JSON e BIN), conta triângulos/vértices pelos accessors e confere as imagens embutidas
(PNG/JPEG de verdade, não só a extensão).
"""
from __future__ import annotations

import json
import struct
from pathlib import Path

MAGIC_GLB = b"glTF"
CHUNK_JSON = 0x4E4F534A
CHUNK_BIN = 0x004E4942
MAGIC_IMAGENS = {"image/png": b"\x89PNG\r\n\x1a\n", "image/jpeg": b"\xff\xd8\xff"}
MODO_TRIANGULOS = 4


class ErroGLB(ValueError):
    """Arquivo que não é um GLB válido, com a explicação em português."""


def ler(caminho) -> tuple[dict, bytes]:
    """Devolve (json_do_gltf, bytes_do_chunk_bin). Levanta ErroGLB se o arquivo não for GLB 2.0."""
    dados = Path(caminho).read_bytes()
    if len(dados) < 20:
        raise ErroGLB(f"arquivo pequeno demais para ser GLB ({len(dados)} bytes)")
    magic, versao, comprimento = struct.unpack_from("<4sII", dados, 0)
    if magic != MAGIC_GLB:
        raise ErroGLB(f"magic errado: {magic!r} (esperado b'glTF')")
    if versao != 2:
        raise ErroGLB(f"versão do GLB {versao} (esperado 2)")
    if comprimento != len(dados):
        raise ErroGLB(f"comprimento do cabeçalho {comprimento} != tamanho do arquivo {len(dados)}")
    pos, gltf, binario = 12, None, b""
    while pos + 8 <= len(dados):
        tam, tipo = struct.unpack_from("<II", dados, pos)
        corpo = dados[pos + 8: pos + 8 + tam]
        if len(corpo) != tam:
            raise ErroGLB(f"chunk em {pos} truncado ({len(corpo)} de {tam} bytes)")
        if tipo == CHUNK_JSON and gltf is None:
            try:
                gltf = json.loads(corpo.decode("utf-8").rstrip(" \x00"))
            except (UnicodeDecodeError, json.JSONDecodeError) as e:
                raise ErroGLB(f"chunk JSON ilegível: {e}") from e
        elif tipo == CHUNK_BIN and not binario:
            binario = corpo
        pos += 8 + tam
    if gltf is None:
        raise ErroGLB("sem chunk JSON")
    return gltf, binario


def _imagem_ok(gltf: dict, binario: bytes, img: dict) -> tuple[bool, str]:
    if "bufferView" not in img:
        return False, "imagem externa (uri) num GLB: o jogo não acharia o arquivo"
    vista = gltf.get("bufferViews", [])[img["bufferView"]]
    ini = vista.get("byteOffset", 0)
    cabeca = binario[ini: ini + 8]
    tipo = img.get("mimeType", "")
    esperado = MAGIC_IMAGENS.get(tipo)
    if esperado is None:
        return False, f"mimeType {tipo!r} não suportado (use PNG ou JPEG)"
    if not cabeca.startswith(esperado):
        return False, f"bytes não batem com {tipo}"
    return True, tipo


def resumo(caminho) -> dict:
    """Contagens do GLB lidas do próprio arquivo (independentes do Godot)."""
    gltf, binario = ler(caminho)
    acc = gltf.get("accessors", [])
    tris = verts = prims_nao_tri = 0
    caixa_min, caixa_max = None, None
    com_uv = com_cor = com_pesos = 0
    for malha in gltf.get("meshes", []):
        for p in malha.get("primitives", []):
            at = p.get("attributes", {})
            if p.get("mode", MODO_TRIANGULOS) != MODO_TRIANGULOS:
                prims_nao_tri += 1
                continue
            npos = acc[at["POSITION"]]["count"] if "POSITION" in at else 0
            verts += npos
            tris += (acc[p["indices"]]["count"] if "indices" in p else npos) // 3
            com_uv += "TEXCOORD_0" in at
            com_cor += "COLOR_0" in at
            com_pesos += "JOINTS_0" in at and "WEIGHTS_0" in at
            a = acc[at["POSITION"]] if "POSITION" in at else {}
            if "min" in a and "max" in a:  # min/max são obrigatórios no POSITION pela especificação
                caixa_min = a["min"] if caixa_min is None else [min(x, y) for x, y in zip(caixa_min, a["min"])]
                caixa_max = a["max"] if caixa_max is None else [max(x, y) for x, y in zip(caixa_max, a["max"])]
    imagens = []
    for i, img in enumerate(gltf.get("images", [])):
        ok, info = _imagem_ok(gltf, binario, img)
        imagens.append({"indice": i, "ok": ok, "info": info})
    albedo = sum(1 for m in gltf.get("materials", [])
                 if "baseColorTexture" in m.get("pbrMetallicRoughness", {}))
    return {
        "versao_gltf": gltf.get("asset", {}).get("version"),
        "gerador": gltf.get("asset", {}).get("generator"),
        "malhas": len(gltf.get("meshes", [])),
        "primitivas_nao_triangulo": prims_nao_tri,
        "triangulos": tris,
        "vertices": verts,
        "materiais": len(gltf.get("materials", [])),
        "materiais_com_albedo": albedo,
        "texturas": len(gltf.get("textures", [])),
        "imagens": imagens,
        "primitivas_com_uv": com_uv,
        "primitivas_com_cor_vertice": com_cor,
        "primitivas_com_pesos": com_pesos,
        "skins": len(gltf.get("skins", [])),
        "ossos": sum(len(s.get("joints", [])) for s in gltf.get("skins", [])),
        "animacoes": [a.get("name", f"anim_{i}") for i, a in enumerate(gltf.get("animations", []))],
        "caixa_min": caixa_min,
        "caixa_max": caixa_max,
        "bytes": Path(caminho).stat().st_size,
    }
