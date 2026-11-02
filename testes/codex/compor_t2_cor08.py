"""Compoe T2 sobre COR-08, comparando a main congelada e as duas correcoes."""
import hashlib,json,os,sys,subprocess
from pathlib import Path
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
from oficina3d.cor import rodar_vertice
from oficina3d.refino.previa import rodar_blender
from glb_evidencia import geometria_sha
from metricas_frentes import medir
OUT=BASE/'evidencias/cor08_composicao';REF=BASE/'evidencias/t2/entrada_orc'
# Carrega os DOIS modulos T2 da main congelada para nao contaminar baseline com default bilinear.
baseline=OUT/'baseline_main_blender.py'
v=subprocess.check_output(['git','show','b6074f3:oficina3d/cor/vertice.py'],cwd=APP).decode('utf-8-sig')
b=subprocess.check_output(['git','show','b6074f3:oficina3d/cor/_blender_vertice.py'],cwd=APP).decode('utf-8-sig')
baseline.write_text('import sys,types\nfrom pathlib import Path\nsys.path.insert(0,'+repr(str(APP))+')\nimport oficina3d.cor as C\nv=types.ModuleType("oficina3d.cor.vertice")\nv.__package__="oficina3d.cor"\nexec(compile('+repr(v)+',"baseline_vertice.py","exec"),v.__dict__)\nC.vertice=v\nsys.modules["oficina3d.cor.vertice"]=v\nexec(compile('+repr(b)+',"baseline_blender_vertice.py","exec"),{"__file__":'+repr(str(APP/'oficina3d/cor/_blender_vertice.py'))+',"__name__":"__main__"})\n',encoding='utf-8')
report={};models=[]
for label,mode in [('main_prata',None),('c01_prata','seco'),('c02_prata','bilinear'),('c02_ouro','bilinear')]:
 folder=OUT/label;folder.mkdir(exist_ok=True)
 model=BASE/'evidencias/frente_b/entradas/ouro/modelo.glb' if label.endswith('ouro') else REF/'modelo_sem_cor.glb'
 req={'modo':'glb','glb':str(model),'vistas':[{'vista':v,'arquivo':str(REF/f'{v}.png')} for v in ['frente','costas','esquerda','direita']], 'previas':[],'pasta_previas':str(folder/'previas'),'saida_glb':str(folder/'modelo.glb')}
 if mode:req['amostragem']=mode
 if (folder/'resultado_vertice.json').exists():res=json.loads((folder/'resultado_vertice.json').read_text())
 else:res=rodar_blender(baseline,req,folder,'vertice') if mode is None else rodar_vertice(req,folder)
 assert res['ok'];report[label]={'resultado':res,'geometria_sha':geometria_sha(folder/'modelo.glb'),'sha256':hashlib.sha256((folder/'modelo.glb').read_bytes()).hexdigest(),'bytes':(folder/'modelo.glb').stat().st_size}
 models.append({'glb':str(folder/'modelo.glb'),'pasta':str(folder/'flat')})
 print(label,report[label]['sha256'],flush=True)
(OUT/'t2_composicao.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
rodar_blender(APP/'testes/codex/render_flat_blender.py',{'modelos':models,'vistas':['frente']},OUT/'render_t2','flat')
print(json.dumps(medir({label:OUT/label/'flat/frente.png' for label in report},OUT/'t2_metricas.json'),indent=2))
