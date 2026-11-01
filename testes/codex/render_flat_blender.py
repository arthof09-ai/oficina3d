"""Renders de evidencia: Emission, Standard, Cycles CPU, mesmas cameras."""
import bpy
import json
import math
from pathlib import Path
import sys
import time
from mathutils import Vector
APP=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(APP))
from oficina3d.cor._blender_vertice import importar_glb, apontar_camera
p=json.loads(Path(sys.argv[sys.argv.index('--')+1]).read_text(encoding='utf-8'))
t=time.perf_counter();frames=[]
for entrada in p['modelos']:
    obj=importar_glb(entrada['glb']);scene=bpy.context.scene
    attr=obj.data.color_attributes.active_color or obj.data.color_attributes[0]
    mat=bpy.data.materials.new('prova_unlit');mat.use_nodes=True
    ns=mat.node_tree.nodes;ns.clear()
    vertex=ns.new('ShaderNodeVertexColor');vertex.layer_name=attr.name
    emit=ns.new('ShaderNodeEmission');out=ns.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(vertex.outputs['Color'],emit.inputs['Color'])
    mat.node_tree.links.new(emit.outputs[0],out.inputs['Surface'])
    obj.data.materials.clear();obj.data.materials.append(mat)
    coords=[obj.matrix_world@v.co for v in obj.data.vertices]
    lo=Vector(tuple(min(v[i] for v in coords) for i in range(3)))
    hi=Vector(tuple(max(v[i] for v in coords) for i in range(3)))
    dim=hi-lo;center=(lo+hi)/2;radius=max(dim)*3
    cd=bpy.data.cameras.new('camera_prova');cd.type='ORTHO'
    cam=bpy.data.objects.new('camera_prova',cd);scene.collection.objects.link(cam);scene.camera=cam
    cd.ortho_scale=max(dim.z,math.hypot(dim.x,dim.y)*800/640)*1.1
    cd.clip_start=max(dim)*0.01;cd.clip_end=radius*4
    scene.render.engine='CYCLES';scene.cycles.device='CPU';scene.cycles.samples=1
    scene.render.threads_mode='FIXED';scene.render.threads=4
    scene.render.resolution_x=640;scene.render.resolution_y=800;scene.render.resolution_percentage=100
    scene.render.film_transparent=True;scene.render.image_settings.file_format='PNG'
    scene.render.image_settings.color_mode='RGBA';scene.view_settings.view_transform='Standard'
    scene.view_settings.look='None';scene.view_settings.exposure=0;scene.view_settings.gamma=1
    scene.render.dither_intensity=0
    folder=Path(entrada['pasta']);folder.mkdir(parents=True,exist_ok=True)
    for view in p['vistas']:
        apontar_camera(cam,view,center,radius)
        target=folder/(view+'.png');scene.render.filepath=str(target)
        bpy.ops.render.render(write_still=True)
        frames.append(str(target))
Path(p['resultado']).write_text(json.dumps({'ok':True,'frames':frames,'tempo_s':time.perf_counter()-t,
    'render':'Cycles CPU / Emission / Standard / exposure=0 / gamma=1 / samples=1'},indent=2),encoding='utf-8')
