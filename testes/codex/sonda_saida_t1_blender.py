"""Sonda do caminho de gravacao T1: byte sRGB, save_render vs save."""
import bpy,json,sys
from pathlib import Path
p=json.loads(Path(sys.argv[sys.argv.index('--')+1]).read_text(encoding='utf-8'))
out=Path(p['pasta']);out.mkdir(exist_ok=True)
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
img=bpy.data.images.new('sonda_t1',4,4,alpha=True)
color=[137/255,103/255,58/255,1.]
img.pixels.foreach_set(color*16)
report={'ok':True,'view_transform_default':scene.view_settings.view_transform,
 'colorspace_image':img.colorspace_settings.name,'is_float':img.is_float,'entrada_srgb':[137,103,58]}
img.save_render(str(out/'save_render_default.png'))
scene.view_settings.view_transform='Standard'
img.save_render(str(out/'save_render_standard.png'))
img.filepath_raw=str(out/'save.png');img.file_format='PNG';img.save()
Path(p['resultado']).write_text(json.dumps(report,indent=2),encoding='utf-8')
