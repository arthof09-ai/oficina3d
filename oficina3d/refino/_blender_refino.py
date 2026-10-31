"""Blender headless: limpar, fechar, decimar, normalizar, simetrizar, UV e exportar GLB.

Uso (chamado por oficina3d.refino.previa.rodar_blender):
    blender -b --factory-startup --python-exit-code 3 -P _blender_refino.py -- pedido.json

pedido.json:
    entrada, saida_glb, resultado, alvo_triangulos, altura, limpar (bool), simetrizar (bool),
    uv (bool), orientacao ("gltf" | "triposr"), girar_graus, min_componente_frac,
    max_lados_buraco, salvar_blend (caminho ou null)

Saída: GLB Y para cima, frente +Z (no Blender: Z para cima, frente −Y), altura
``altura``, pivô nos pés (origem no centro da base), centrado em X e na profundidade.
Imprime "PROGRESSO <pct> <msg>" e grava o resultado (JSON) com as métricas.
"""
import json
import math
import sys
import time
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001
    pass

import bmesh
import bpy
from mathutils import Matrix


def progresso(pct, msg):
    print(f"PROGRESSO {int(pct)} {msg}", flush=True)


def ler_pedido():
    args = sys.argv[sys.argv.index("--") + 1:]
    with open(args[0], encoding="utf-8") as f:
        return json.load(f)


# ----------------------------------------------------------------------------
def importar(caminho, orientacao):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    baixo = caminho.lower()
    if baixo.endswith((".glb", ".gltf")):
        bpy.ops.import_scene.gltf(filepath=caminho)
    elif baixo.endswith(".obj"):
        if orientacao == "triposr":  # OBJ do TripoSR: Z para cima, frente +X
            bpy.ops.wm.obj_import(filepath=caminho, forward_axis="Y", up_axis="Z")
        else:
            bpy.ops.wm.obj_import(filepath=caminho)
    elif baixo.endswith(".ply"):
        bpy.ops.wm.ply_import(filepath=caminho)
    elif baixo.endswith(".stl"):
        bpy.ops.wm.stl_import(filepath=caminho)
    else:
        raise ValueError(f"formato de malha não suportado: {caminho}")

    malhas = [o for o in bpy.context.scene.objects if o.type == "MESH"]
    if not malhas:
        raise ValueError("o arquivo não tem nenhuma malha")
    bpy.ops.object.select_all(action="DESELECT")
    for o in malhas:
        o.select_set(True)
    bpy.context.view_layer.objects.active = malhas[0]
    if len(malhas) > 1:
        bpy.ops.object.join()
    obj = bpy.context.view_layer.objects.active
    bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
    for o in list(bpy.context.scene.objects):
        if o is not obj:
            bpy.data.objects.remove(o, do_unlink=True)
    if orientacao == "triposr":
        obj.rotation_euler.z += math.radians(-90)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    # Formas e modificadores herdados não interessam ao refino.
    if obj.data.shape_keys:
        obj.shape_key_clear()
    obj.modifiers.clear()
    obj.name = "modelo"
    obj.data.name = "modelo"
    return obj


def diagonal(me):
    if not me.vertices:
        return 1.0
    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    zs = [v.co.z for v in me.vertices]
    return max(1e-9, math.dist((min(xs), min(ys), min(zs)), (max(xs), max(ys), max(zs))))


def contar_triangulos(me):
    return sum(len(p.vertices) - 2 for p in me.polygons)


def topologia(bm):
    """Arestas abertas (1 face) e não-manifold (>2 faces)."""
    abertas = nao_manifold = 0
    for e in bm.edges:
        n = len(e.link_faces)
        if n == 1:
            abertas += 1
        elif n > 2:
            nao_manifold += 1
    return abertas, nao_manifold


def fechada_de(me, dist):
    """Fechada = toda aresta tem exatamente 2 faces (depois de unir vértices coincidentes)."""
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
    soltas = sum(1 for e in bm.edges if not e.link_faces)
    abertas, nao_manifold = topologia(bm)
    bm.free()
    return (abertas == 0 and nao_manifold == 0 and soltas == 0 and len(me.polygons) > 0), abertas, nao_manifold


def ilhas(bm):
    """Componentes conexos (por arestas) — lista de listas de faces."""
    pai = list(range(len(bm.verts)))

    def raiz(i):
        while pai[i] != i:
            pai[i] = pai[pai[i]]
            i = pai[i]
        return i

    bm.verts.index_update()
    for e in bm.edges:
        a, b = raiz(e.verts[0].index), raiz(e.verts[1].index)
        if a != b:
            pai[a] = b
    grupos = {}
    for f in bm.faces:
        grupos.setdefault(raiz(f.verts[0].index), []).append(f)
    return list(grupos.values())


def limpar_bmesh(me, dist, min_componente_frac, max_lados, remover_pedacos=True):
    """Duplicados, degenerados, soltos, pedaços pequenos, não-manifold e buracos."""
    bm = bmesh.new()
    bm.from_mesh(me)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=dist)
    bmesh.ops.dissolve_degenerate(bm, edges=bm.edges, dist=dist * 0.1)
    removidos = 0
    if remover_pedacos:
        grupos = ilhas(bm)
        total = len(bm.faces)
        minimo = max(1, int(total * min_componente_frac))
        if len(grupos) > 1:
            maior = max(len(g) for g in grupos)
            pequenos = [g for g in grupos if len(g) < minimo and len(g) < maior]
            for g in pequenos:
                bmesh.ops.delete(bm, geom=g, context="FACES")
            removidos = len(pequenos)
    # Arestas com mais de 2 faces: apaga as faces envolvidas e deixa o fechamento refazer.
    ruins = {f for e in bm.edges if len(e.link_faces) > 2 for f in e.link_faces}
    if ruins:
        bmesh.ops.delete(bm, geom=list(ruins), context="FACES")
    soltos_v = [v for v in bm.verts if not v.link_faces]
    if soltos_v:
        bmesh.ops.delete(bm, geom=soltos_v, context="VERTS")
    soltas_e = [e for e in bm.edges if not e.link_faces]
    if soltas_e:
        bmesh.ops.delete(bm, geom=soltas_e, context="EDGES")
    abertas = [e for e in bm.edges if len(e.link_faces) == 1]
    if abertas:
        bmesh.ops.holes_fill(bm, edges=abertas, sides=int(max_lados))
    bmesh.ops.triangulate(bm, faces=bm.faces)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    me.update()
    return removidos, len(ruins)


def decimar(obj, alvo):
    """Decimação por colapso de arestas (quádrica) até no máximo ``alvo`` triângulos."""
    for _ in range(4):
        tri = contar_triangulos(obj.data)
        if tri <= alvo:
            break
        mod = obj.modifiers.new("decimar", "DECIMATE")
        mod.decimate_type = "COLLAPSE"
        mod.ratio = max(1e-4, (alvo * 0.995) / tri)
        mod.use_collapse_triangulate = True
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)


def normalizar(obj, altura):
    """Centro da base na origem (pivô nos pés), altura = ``altura``."""
    me = obj.data
    xs = [v.co.x for v in me.vertices]
    ys = [v.co.y for v in me.vertices]
    zs = [v.co.z for v in me.vertices]
    dz = max(zs) - min(zs)
    if dz <= 0:
        raise ValueError("malha sem altura (plana no eixo vertical)")
    s = altura / dz
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    me.transform(Matrix.Diagonal((s, s, s, 1.0)) @ Matrix.Translation((-cx, -cy, -min(zs))))
    me.update()
    obj.location = (0, 0, 0)
    obj.rotation_euler = (0, 0, 0)
    obj.scale = (1, 1, 1)
    return s


def simetrizar(obj, dist):
    """Espelha em X o lado mais completo (mais área) sobre o outro."""
    me = obj.data
    area_pos = sum(p.area for p in me.polygons if p.center.x > 0)
    area_neg = sum(p.area for p in me.polygons if p.center.x < 0)
    direcao = "POSITIVE_X" if area_pos >= area_neg else "NEGATIVE_X"
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.symmetrize(direction=direcao, threshold=dist)
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.mesh.quads_convert_to_tris()
    bpy.ops.object.mode_set(mode="OBJECT")
    return direcao


def uv_automatico(obj):
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.mode_set(mode="EDIT")
    bpy.ops.mesh.select_all(action="SELECT")
    bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.003)
    bpy.ops.object.mode_set(mode="OBJECT")


def exportar(obj, caminho, uv):
    obj.data.materials.clear()
    bpy.ops.object.select_all(action="DESELECT")
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    kw = dict(filepath=caminho, export_format="GLB", use_selection=True, export_yup=True,
              export_apply=True, export_normals=True, export_texcoords=bool(uv),
              export_materials="NONE", export_animations=False)
    try:
        bpy.ops.export_scene.gltf(**kw)
    except TypeError:  # opção renomeada em alguma versão: exporta com o mínimo
        bpy.ops.export_scene.gltf(filepath=caminho, export_format="GLB", use_selection=True)


# ----------------------------------------------------------------------------
def main():
    pedido = ler_pedido()
    res = {"ok": False}
    tempos = {}
    try:
        t = time.perf_counter()
        progresso(2, "Blender: importando a malha")
        obj = importar(pedido["entrada"], pedido.get("orientacao", "gltf"))
        if pedido.get("girar_graus"):
            obj.data.transform(Matrix.Rotation(math.radians(float(pedido["girar_graus"])), 4, "Z"))
        me = obj.data
        dist = diagonal(me) * 1e-6
        res["triangulos_entrada"] = contar_triangulos(me)
        res["vertices_entrada"] = len(me.vertices)
        fechada0, abertas0, nm0 = fechada_de(me, dist)
        res.update(fechada_antes=fechada0, arestas_abertas_antes=abertas0, arestas_nao_manifold_antes=nm0)
        tempos["importar"] = round(time.perf_counter() - t, 2)

        t = time.perf_counter()
        progresso(15, "Blender: limpando e fechando buracos")
        rem, nm_rem = limpar_bmesh(me, dist, float(pedido.get("min_componente_frac", 0.005)),
                                   int(pedido.get("max_lados_buraco", 1000)),
                                   remover_pedacos=bool(pedido.get("limpar", True)))
        res["componentes_removidos"] = rem
        res["faces_nao_manifold_removidas"] = nm_rem
        tempos["limpar"] = round(time.perf_counter() - t, 2)

        t = time.perf_counter()
        alvo = int(pedido.get("alvo_triangulos", 50000))
        progresso(35, f"Blender: reduzindo para até {alvo} triângulos")
        decimar(obj, alvo)
        # Decimação pode abrir algum buraco: fecha de novo sem tirar pedaços.
        limpar_bmesh(me, dist, 0.0, int(pedido.get("max_lados_buraco", 1000)), remover_pedacos=False)
        decimar(obj, alvo)
        tempos["decimar"] = round(time.perf_counter() - t, 2)

        t = time.perf_counter()
        progresso(55, "Blender: normalizando (pivô nos pés, Y para cima, frente +Z)")
        altura = float(pedido.get("altura") or 1.0)
        res["escala_aplicada"] = normalizar(obj, altura)
        if pedido.get("simetrizar"):
            progresso(60, "Blender: simetrizando em X")
            res["simetria"] = simetrizar(obj, diagonal(me) * 1e-4)
            # O espelho pode criar faces (costura no plano X=0): fecha e reduz de novo.
            limpar_bmesh(me, diagonal(me) * 1e-6, 0.0, int(pedido.get("max_lados_buraco", 1000)),
                         remover_pedacos=False)
            decimar(obj, alvo)
            normalizar(obj, altura)
        tempos["normalizar"] = round(time.perf_counter() - t, 2)

        me.shade_smooth() if hasattr(me, "shade_smooth") else None
        if pedido.get("uv", True):
            t = time.perf_counter()
            progresso(70, "Blender: UV automático (Smart UV Project)")
            uv_automatico(obj)
            tempos["uv"] = round(time.perf_counter() - t, 2)

        dist = diagonal(me) * 1e-6
        fechada, abertas, nm = fechada_de(me, dist)
        xs = [v.co.x for v in me.vertices]
        ys = [v.co.y for v in me.vertices]
        zs = [v.co.z for v in me.vertices]
        res.update(
            triangulos_depois=contar_triangulos(me), vertices_depois=len(me.vertices),
            fechada=fechada, arestas_abertas=abertas, arestas_nao_manifold=nm,
            # dimensões em glTF: largura (X), altura (Y), profundidade (Z)
            dimensoes={"largura": round(max(xs) - min(xs), 5), "altura": round(max(zs) - min(zs), 5),
                       "profundidade": round(max(ys) - min(ys), 5)},
            base_z=round(min(zs), 6),
            centro_base=[round((min(xs) + max(xs)) / 2, 6), round((min(ys) + max(ys)) / 2, 6)],
            tem_uv=bool(me.uv_layers),
        )

        t = time.perf_counter()
        progresso(85, "Blender: exportando o GLB")
        exportar(obj, pedido["saida_glb"], pedido.get("uv", True))
        if pedido.get("salvar_blend"):
            bpy.ops.wm.save_as_mainfile(filepath=pedido["salvar_blend"], compress=True)
        tempos["exportar"] = round(time.perf_counter() - t, 2)
        res["tempos_s"] = tempos
        res["versao_blender"] = bpy.app.version_string
        res["ok"] = True
        progresso(100, "Blender: refino pronto")
    except Exception as e:  # noqa: BLE001
        res["erro"] = f"{type(e).__name__}: {e}"
        res["traceback"] = traceback.format_exc()
        print(res["traceback"], flush=True)
    with open(pedido["resultado"], "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    if not res["ok"]:
        sys.exit(3)


main()
