"""Blender: verifica o contrato real de pixels da imagem versus atributo linear."""
import bpy
import json
from pathlib import Path
import sys
p=json.loads(Path(sys.argv[sys.argv.index('--')+1]).read_text(encoding='utf-8'))
img=bpy.data.images.load(p['imagem'],check_existing=False)
rgb=list(img.pixels[:3])
bpy.ops.mesh.primitive_plane_add()
a=bpy.context.object.data.color_attributes.new(name='Color',type='FLOAT_COLOR',domain='POINT')
a.data[0].color=(*rgb,1)
r={'ok':True,'blender':bpy.app.version_string,'image_colorspace':img.colorspace_settings.name,
   'pixels_rgb':rgb,'attribute_linear':list(a.data[0].color[:3]),
   'attribute_srgb':list(a.data[0].color_srgb[:3]),'referencia_srgb':[137/255,103/255,58/255]}
Path(p['resultado']).write_text(json.dumps(r,indent=2),encoding='utf-8')
