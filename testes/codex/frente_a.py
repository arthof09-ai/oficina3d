"""Reproduz COR-05 na copia e captura texels antes da serializacao."""
import hashlib,json,os,shutil,sys
from pathlib import Path
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),
 PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
from oficina3d.refino.previa import rodar_blender
SRC=BASE.parent/'Oficina3D/jobs/20261101-101528-corint-orc-s7'
OUT=BASE/'evidencias/frente_a';IN=OUT/'entrada';IN.mkdir(parents=True,exist_ok=True)
manifest=[]
for src,dst in [(SRC/'cor/modelo_uv.glb',IN/'modelo_uv.glb'),(SRC/'cor/modelo_cor.glb',IN/'modelo_cor.glb'),
 (SRC/'cor/textura.png',IN/'textura.png'),*[(SRC/f'preproc/{v}.png',IN/f'{v}.png') for v in ['frente','costas','esquerda','direita']]]:
    if not dst.exists():shutil.copyfile(src,dst)
    a=hashlib.sha256(src.read_bytes()).hexdigest();assert a==hashlib.sha256(dst.read_bytes()).hexdigest()
    manifest.append({'nome':dst.name,'sha256':a,'bytes':dst.stat().st_size})
(OUT/'entradas.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
pedido=json.loads((SRC/'cor/pedido_cor.json').read_text(encoding='utf-8'))
folder=OUT/'proveniencia';folder.mkdir(exist_ok=True)
pedido.update(glb=str(IN/'modelo_uv.glb'),vistas=[{'vista':v,'arquivo':str(IN/f'{v}.png')} for v in ['frente','costas','esquerda','direita']],
 saida_glb=str(folder/'modelo.glb'),saida_textura=str(folder/'textura.png'),previas=[],pasta_previas=str(folder/'previas'))
if not (folder/'resultado_cor.json').exists():
    res=rodar_blender(APP/'testes/codex/auditar_projecao_blender.py',pedido,folder,'cor',timeout_s=900)
    print(json.dumps(res),flush=True)
