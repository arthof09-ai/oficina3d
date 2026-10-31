"""Blender headless: importa uma malha e renderiza 3 vistas (frente, 3/4, lado).

Uso: blender -b --factory-startup -P render_previa.py -- <malha.glb|.obj> <prefixo_saida> [triposr]
Gera <prefixo>_frente.png, <prefixo>_34.png, <prefixo>_lado.png.
"triposr": o OBJ do TripoSR vem com Z para cima e frente para +X; e usa texture.png ao lado.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

args = sys.argv[sys.argv.index("--") + 1:]
malha, prefixo = args[0], args[1]
triposr = len(args) > 2 and args[2] == "triposr"

bpy.ops.wm.read_factory_settings(use_empty=True)
if malha.lower().endswith(".obj"):
    if triposr:
        bpy.ops.wm.obj_import(filepath=malha, forward_axis="Y", up_axis="Z")
    else:
        bpy.ops.wm.obj_import(filepath=malha)
else:
    bpy.ops.import_scene.gltf(filepath=malha)

objs = [o for o in bpy.context.scene.objects if o.type == "MESH"]
bpy.ops.object.select_all(action="DESELECT")
for o in objs:
    o.select_set(True)
bpy.context.view_layer.objects.active = objs[0]
if len(objs) > 1:
    bpy.ops.object.join()
obj = bpy.context.view_layer.objects.active
bpy.ops.object.parent_clear(type="CLEAR_KEEP_TRANSFORM")
if triposr:
    obj.rotation_euler.z += math.radians(-90)
bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="BOUNDS")
obj.location = (0, 0, 0)

textura = os.path.join(os.path.dirname(malha), "texture.png")
cena = bpy.context.scene
cena.render.engine = "BLENDER_WORKBENCH"
cena.display.shading.light = "STUDIO"
cena.display.shading.show_cavity = True
cena.display.shading.color_type = "MATERIAL"
if triposr and os.path.exists(textura) and obj.data.uv_layers:
    mat = bpy.data.materials.new("textura")
    mat.use_nodes = True
    no = mat.node_tree.nodes.new("ShaderNodeTexImage")
    no.image = bpy.data.images.load(textura)
    mat.node_tree.links.new(no.outputs["Color"], mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"])
    obj.data.materials.clear()
    obj.data.materials.append(mat)
    cena.display.shading.color_type = "TEXTURE"
cena.render.resolution_x, cena.render.resolution_y = 700, 900
cena.world = bpy.data.worlds.new("fundo")
cena.world.color = (0.2, 0.2, 0.22)

dim = obj.dimensions
raio = max(dim) * 3
cam_dados = bpy.data.cameras.new("cam")
cam_dados.type = "ORTHO"
cam_dados.ortho_scale = max(dim) * 1.1
cam = bpy.data.objects.new("cam", cam_dados)
cena.collection.objects.link(cam)
cena.camera = cam
alvo = bpy.data.objects.new("alvo", None)
cena.collection.objects.link(alvo)
rastreio = cam.constraints.new("TRACK_TO")
rastreio.target = alvo

for nome, ang in (("frente", 0), ("34", 45), ("lado", 90)):
    a = math.radians(ang)
    cam.location = Vector((raio * math.sin(a), -raio * math.cos(a), dim.z * 0.05))
    cena.render.filepath = f"{prefixo}_{nome}.png"
    bpy.ops.render.render(write_still=True)
    print("PREVIA_OK", cena.render.filepath)
print("DIMENSOES", tuple(round(d, 3) for d in dim))
