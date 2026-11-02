"""COR-08 publicada: producao real, instrumentacao e contraprova A0 em memoria."""
import hashlib,json,os,shutil,sys
from pathlib import Path
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
from oficina3d.refino.previa import rodar_blender
MAIN=BASE.parent/'Oficina3D';OUT=BASE/'evidencias/cor08_composicao';IN=OUT/'entradas';IN.mkdir(parents=True,exist_ok=True)
req=json.loads((MAIN/'jobs_teste/cor08-critico/cor08rep/pedido_cor.json').read_text())
manifest=[]
for src,name in [(Path(req['glb']),'modelo_uv.glb')]+[(Path(v['arquivo']),v['vista']+'.png') for v in req['vistas']]:
 dst=IN/name
 if not dst.exists():shutil.copyfile(src,dst)
 digest=hashlib.sha256(src.read_bytes()).hexdigest();assert digest==hashlib.sha256(dst.read_bytes()).hexdigest()
 manifest.append({'nome':name,'sha256':digest,'bytes':dst.stat().st_size})
(OUT/'entradas.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
for label in ['producao','instrumentado','contraprova_absoluto']:
 folder=OUT/label
 if (folder/'resultado_cor.json').exists():
  assert json.loads((folder/'resultado_cor.json').read_text())['ok'];continue
 folder.mkdir(exist_ok=True)
 pedido=dict(req,glb=str(IN/'modelo_uv.glb'),vistas=[{'vista':v,'arquivo':str(IN/f'{v}.png')} for v in ['frente','costas','esquerda','direita']],saida_glb=str(folder/'modelo.glb'),saida_textura=str(folder/'textura.png'),previas=[],pasta_previas=str(folder/'previas'),resultado=str(folder/'resultado_cor.json'),codex_centro_audit=label!='producao',codex_absoluto=label=='contraprova_absoluto')
 script=APP/('oficina3d/cor/_blender_cor.py' if label=='producao' else 'testes/codex/auditar_projecao_blender.py')
 res=rodar_blender(script,pedido,folder,'cor',timeout_s=900)
 print(label,json.dumps(res),flush=True)
 assert res['ok']
