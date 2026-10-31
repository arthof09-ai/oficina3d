"""Malha: leitura/escrita mínima de GLB em Python puro + limpeza/decimação com pymeshlab.

- ``info_glb``: conta triângulos/vértices e mede a caixa envolvente de um GLB sem
  dependências (serve para "antes" e para conferir o arquivo final).
- ``escrever_glb``: grava um GLB simples (posições + índices). Usado nos testes e
  como saída intermediária quando não há trimesh.
- ``limpar_pymeshlab``: caminho da v1 (trimesh + pymeshlab): tira duplicados, faces
  nulas, pedaços soltos pequenos, arestas não-manifold; fecha buracos; decimação
  quadrática até o alvo. trimesh, pymeshlab e numpy são importados só aqui dentro.

Eixos: GLB/glTF é Y para cima e a frente do personagem fica em +Z.
"""
from __future__ import annotations

import json
import math
import struct
import time
from pathlib import Path

_MAGICO = 0x46546C67  # "glTF"
_JSON = 0x4E4F534A
_BIN = 0x004E4942

_COMPONENTES = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4, "MAT4": 16}


# ----------------------------------------------------------------------------
# GLB puro
# ----------------------------------------------------------------------------
def _ler_json_glb(caminho) -> dict:
    caminho = Path(caminho)
    with open(caminho, "rb") as f:
        cab = f.read(12)
        if len(cab) < 12:
            raise ValueError(f"GLB curto demais: {caminho}")
        magico, versao, _total = struct.unpack("<III", cab)
        if magico != _MAGICO:
            raise ValueError(f"não é um GLB (assinatura errada): {caminho}")
        if versao != 2:
            raise ValueError(f"GLB versão {versao} não suportada (só 2): {caminho}")
        tam, tipo = struct.unpack("<II", f.read(8))
        if tipo != _JSON:
            raise ValueError(f"GLB sem bloco JSON: {caminho}")
        return json.loads(f.read(tam).decode("utf-8"))


def _mat_mult(a, b):
    # matrizes 4x4 em listas de linhas
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]


def _mat_no(no: dict):
    if "matrix" in no:
        m = no["matrix"]  # coluna-maior
        return [[m[c * 4 + r] for c in range(4)] for r in range(4)]
    tx, ty, tz = no.get("translation", (0.0, 0.0, 0.0))
    qx, qy, qz, qw = no.get("rotation", (0.0, 0.0, 0.0, 1.0))
    sx, sy, sz = no.get("scale", (1.0, 1.0, 1.0))
    r = [
        [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
        [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
        [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)],
    ]
    return [
        [r[0][0] * sx, r[0][1] * sy, r[0][2] * sz, tx],
        [r[1][0] * sx, r[1][1] * sy, r[1][2] * sz, ty],
        [r[2][0] * sx, r[2][1] * sy, r[2][2] * sz, tz],
        [0.0, 0.0, 0.0, 1.0],
    ]


def info_glb(caminho) -> dict:
    """Triângulos, vértices e caixa envolvente (em coordenadas glTF: Y para cima).

    A caixa vem do min/max do atributo POSITION (obrigatório no glTF), transformado
    pelos nós; é exata para malhas sem rotação nos nós e conservadora nos outros casos.
    """
    g = _ler_json_glb(caminho)
    acessores = g.get("accessors", [])
    malhas = g.get("meshes", [])
    nos = g.get("nodes", [])
    ident = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]

    instancias = []  # (indice_malha, matriz_mundo)

    def visitar(i, pai):
        no = nos[i]
        m = _mat_mult(pai, _mat_no(no))
        if "mesh" in no:
            instancias.append((no["mesh"], m))
        for f in no.get("children", []):
            visitar(f, m)

    cenas = g.get("scenes") or []
    if cenas:
        for raiz in cenas[g.get("scene", 0)].get("nodes", []):
            visitar(raiz, ident)
    if not instancias:  # GLB sem cena: conta cada malha uma vez
        instancias = [(i, ident) for i in range(len(malhas))]

    tri = vert = 0
    tem_uv = False
    lo = [math.inf] * 3
    hi = [-math.inf] * 3
    for im, mat in instancias:
        for prim in malhas[im].get("primitives", []):
            modo = prim.get("mode", 4)
            attrs = prim.get("attributes", {})
            tem_uv = tem_uv or "TEXCOORD_0" in attrs
            pos = acessores[attrs["POSITION"]] if "POSITION" in attrs else None
            nv = pos["count"] if pos else 0
            n = acessores[prim["indices"]]["count"] if "indices" in prim else nv
            if modo == 4:
                tri += n // 3
            elif modo in (5, 6):
                tri += max(0, n - 2)
            vert += nv
            if pos and "min" in pos and "max" in pos:
                mn, mx = pos["min"], pos["max"]
                for cx in (mn[0], mx[0]):
                    for cy in (mn[1], mx[1]):
                        for cz in (mn[2], mx[2]):
                            p = [sum(mat[r][c] * v for c, v in enumerate((cx, cy, cz, 1.0))) for r in range(3)]
                            for k in range(3):
                                lo[k] = min(lo[k], p[k])
                                hi[k] = max(hi[k], p[k])
    caixa = None
    if lo[0] != math.inf:
        caixa = {"min": [round(v, 6) for v in lo], "max": [round(v, 6) for v in hi]}
    return {"triangulos": tri, "vertices": vert, "malhas": len(malhas),
            "instancias": len(instancias), "tem_uv": tem_uv, "caixa": caixa}


def escrever_glb(vertices, faces, caminho) -> Path:
    """GLB mínimo: uma malha, posições float32 e índices uint32 (Y para cima)."""
    vertices = [tuple(float(c) for c in v) for v in vertices]
    faces = [tuple(int(i) for i in f) for f in faces]
    if not vertices or not faces:
        raise ValueError("malha vazia")
    pos = struct.pack(f"<{len(vertices) * 3}f", *(c for v in vertices for c in v))
    idx = struct.pack(f"<{len(faces) * 3}I", *(i for f in faces for i in f))
    pad = (-len(pos)) % 4
    bin_ = pos + b"\x00" * pad + idx
    bin_ += b"\x00" * ((-len(bin_)) % 4)
    mn = [min(v[k] for v in vertices) for k in range(3)]
    mx = [max(v[k] for v in vertices) for k in range(3)]
    g = {
        "asset": {"version": "2.0", "generator": "oficina3d.refino"},
        "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0, "name": "malha"}],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0}, "indices": 1, "mode": 4}]}],
        "buffers": [{"byteLength": len(bin_)}],
        "bufferViews": [
            {"buffer": 0, "byteOffset": 0, "byteLength": len(pos), "target": 34962},
            {"buffer": 0, "byteOffset": len(pos) + pad, "byteLength": len(idx), "target": 34963},
        ],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": len(vertices), "type": "VEC3",
             "min": mn, "max": mx},
            {"bufferView": 1, "componentType": 5125, "count": len(faces) * 3, "type": "SCALAR"},
        ],
    }
    js = json.dumps(g, separators=(",", ":")).encode("utf-8")
    js += b" " * ((-len(js)) % 4)
    total = 12 + 8 + len(js) + 8 + len(bin_)
    caminho = Path(caminho)
    with open(caminho, "wb") as f:
        f.write(struct.pack("<III", _MAGICO, 2, total))
        f.write(struct.pack("<II", len(js), _JSON) + js)
        f.write(struct.pack("<II", len(bin_), _BIN) + bin_)
    return caminho


# ----------------------------------------------------------------------------
# Caminho trimesh + pymeshlab (opcional; .venv_app)
# ----------------------------------------------------------------------------
def pymeshlab_disponivel() -> bool:
    import importlib.util as u
    return all(u.find_spec(m) is not None for m in ("numpy", "trimesh", "pymeshlab"))


def _filtro(ms, nomes: tuple[str, ...], **kw):
    """Chama o primeiro filtro que existir (os nomes mudaram entre versões do pymeshlab)."""
    for nome in nomes:
        f = getattr(ms, nome, None)
        if f is not None:
            return f(**kw)
    raise AttributeError(f"pymeshlab sem nenhum destes filtros: {', '.join(nomes)}")


def _topologia(ms) -> dict:
    try:
        t = _filtro(ms, ("get_topological_measures", "compute_topological_measures"))
    except Exception:  # noqa: BLE001 — medida opcional
        return {}
    return {k: t.get(k) for k in ("connected_components_number", "boundary_edges",
                                  "non_two_manifold_edges", "is_mesh_two_manifold") if t and k in t}


def limpar_pymeshlab(entrada, saida, alvo_triangulos: int = 50000,
                     min_componente_frac: float = 0.005, max_lados_buraco: int = 1000) -> dict:
    """Limpa, fecha buracos e decima com pymeshlab; grava ``saida`` (GLB, Y para cima).

    Levanta exceção se faltar biblioteca ou algum filtro — quem chama cai no Blender.
    """
    import numpy as np  # imports preguiçosos (dependências pesadas)
    import pymeshlab
    import trimesh

    t0 = time.perf_counter()
    tm = trimesh.load(str(entrada), force="mesh", process=False)
    if tm is None or len(tm.faces) == 0:
        raise ValueError(f"malha vazia: {entrada}")
    tri_antes = int(len(tm.faces))
    tm.merge_vertices()
    fechada_antes = bool(tm.is_watertight)

    ms = pymeshlab.MeshSet()
    ms.add_mesh(pymeshlab.Mesh(vertex_matrix=np.asarray(tm.vertices, dtype=np.float64),
                               face_matrix=np.asarray(tm.faces, dtype=np.int32)))
    topo_antes = _topologia(ms)
    _filtro(ms, ("meshing_remove_duplicate_vertices", "remove_duplicate_vertices"))
    _filtro(ms, ("meshing_remove_duplicate_faces", "remove_duplicate_faces"))
    _filtro(ms, ("meshing_remove_null_faces", "remove_zero_area_faces"))
    _filtro(ms, ("meshing_remove_unreferenced_vertices", "remove_unreferenced_vertices"))
    n = ms.current_mesh().face_number()
    _filtro(ms, ("meshing_remove_connected_component_by_face_number",
                 "remove_isolated_pieces_wrt_face_num"),
            mincomponentsize=max(10, int(n * min_componente_frac)))
    _filtro(ms, ("meshing_repair_non_manifold_edges", "repair_non_manifold_edges_by_removing_faces"))
    _filtro(ms, ("meshing_close_holes", "close_holes"), maxholesize=int(max_lados_buraco))
    t_limpa = time.perf_counter()

    alvo = int(alvo_triangulos)
    if ms.current_mesh().face_number() > alvo:
        # Um pouco abaixo do alvo: fechar buracos depois pode acrescentar faces.
        _filtro(ms, ("meshing_decimation_quadric_edge_collapse",
                     "simplification_quadric_edge_collapse_decimation"),
                targetfacenum=int(alvo * 0.995), preservenormal=True, preservetopology=True,
                optimalplacement=True, planarquadric=True, autoclean=True)
    _filtro(ms, ("meshing_close_holes", "close_holes"), maxholesize=int(max_lados_buraco))
    _filtro(ms, ("meshing_remove_unreferenced_vertices", "remove_unreferenced_vertices"))
    t_dec = time.perf_counter()

    m = ms.current_mesh()
    final = trimesh.Trimesh(vertices=m.vertex_matrix(), faces=m.face_matrix(), process=False)
    final.merge_vertices()
    trimesh.repair.fix_normals(final)
    Path(saida).parent.mkdir(parents=True, exist_ok=True)
    final.export(str(saida))
    topo_depois = _topologia(ms)
    comp_antes = topo_antes.get("connected_components_number")
    comp_depois = topo_depois.get("connected_components_number")
    return {
        "backend": "pymeshlab",
        "triangulos_antes": tri_antes,
        "triangulos_limpa": int(len(final.faces)),
        "fechada_antes": fechada_antes,
        "fechada_limpa": bool(final.is_watertight),
        "componentes_antes": comp_antes,
        "componentes_removidos": (comp_antes - comp_depois) if comp_antes and comp_depois else None,
        "tempo_limpeza_s": round(t_limpa - t0, 2),
        "tempo_decimacao_s": round(t_dec - t_limpa, 2),
    }


def fechada_trimesh(caminho) -> bool | None:
    """Confere com trimesh se o GLB final é fechado (None se trimesh não existe).

    O exportador glTF separa vértices nas costuras de UV; por isso unimos por posição.
    """
    try:
        import trimesh
    except ImportError:
        return None
    m = trimesh.load(str(caminho), force="mesh", process=False)
    m.merge_vertices(merge_tex=True, merge_norm=True)
    return bool(m.is_watertight)
