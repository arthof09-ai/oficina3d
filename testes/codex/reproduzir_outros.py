"""Regressao da mesma correcao nos outros dois sujeitos dourados."""
import hashlib,json,os,shutil,sys,time
from pathlib import Path
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
import oficina3d.cor as cor
from oficina3d.cor.passo import rodar_passo_vertice
from glb_evidencia import geometria_sha
OUT=BASE/'evidencias/t2/outros';OUT.mkdir(exist_ok=False)
current=cor.SCRIPT_VERTICE;old=BASE/'evidencias/t2/contraprova/exportador_antigo.py'
report={}
for sujeito,job in [('besta','20261101-124815-t2-besta'),('caprileo','20261101-124815-t2-caprileio')]:
    src=BASE.parent/'Oficina3D/jobs'/job
    entry=OUT/sujeito/'entrada';entry.mkdir(parents=True)
    files=[('modelo_sem_cor.glb',src/'saida/modelo_sem_cor.glb')]+[(v+'.png',src/f'preproc/{v}.png') for v in ['frente','costas','esquerda','direita']]
    manifest={}
    for name,path in files:
        shutil.copyfile(path,entry/name);manifest[name]=hashlib.sha256((entry/name).read_bytes()).hexdigest()
    report[sujeito]={'entradas':manifest,'runs':{}}
    for fase,script in [('antes',old),('depois',current)]:
        cor.SCRIPT_VERTICE=script
        folder=OUT/sujeito/fase;folder.mkdir()
        res=rodar_passo_vertice(folder,entry/'modelo_sem_cor.glb',[{'vista':v,'arquivo':str(entry/f'{v}.png')} for v in ['frente','costas','esquerda','direita']])
        (folder/'passo.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
        report[sujeito]['runs'][fase]={'tempo_s':res['resultado_vertice']['tempo_s'],'sha256_glb':res['resultado_vertice']['sha256_glb'],'geometria_sha256':geometria_sha(folder/'cor/modelo_cor.glb'),'cobertura':res['cobertura_vertices']}
        (OUT/'resultado.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
        print(sujeito,fase,json.dumps(report[sujeito]['runs'][fase]),flush=True)
cor.SCRIPT_VERTICE=current
