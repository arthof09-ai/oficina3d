"""Renders Emission e regua fixa do Paint; sem Workbench."""
import json,os,sys
from pathlib import Path
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),PYTHONDONTWRITEBYTECODE='1',
 TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
from oficina3d.refino.previa import rodar_blender
from metricas_frentes import medir
from glb_evidencia import ler_glb
OUT=BASE/'evidencias/paint_spike'
label=sys.argv[1];folder=OUT/label
views=['frente'] if '--frente' in sys.argv else ['frente','frente-esquerda','esquerda','costas-esquerda','costas','costas-direita','direita','frente-direita']
rodar_blender(APP/'testes/codex/render_flat_blender.py',
 {'modelos':[{'glb':str(folder/'modelo.glb'),'pasta':str(folder/'flat'),'textura':True}],'vistas':views},folder/'render','flat')
r=medir({'COR05':BASE/'evidencias/frente_a/flat/frente.png',label:folder/'flat/frente.png'},folder/'metricas.json')
_,prims=ler_glb(folder/'modelo.glb')
r['artefato']={'triangulos':sum(len(p['indices'])//3 for p in prims),'vertices_exportados':sum(len(p['POSITION']) for p in prims),
 'bytes_glb':(folder/'modelo.glb').stat().st_size,'bytes_textura':(folder/'textura.png').stat().st_size}
(folder/'metricas.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps(r,indent=2))
