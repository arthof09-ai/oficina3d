"""Reproducao independente D-T2: forma legitima, eixos e fonte mista."""
import json,os,sys,hashlib
from pathlib import Path
import shutil,time
import trimesh
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
from oficina3d.cor.passo import rodar_passo_vertice
from oficina3d.cor.vertice import avaliar_alinhamento_forma
OUT=BASE/'evidencias/dt2';OUT.mkdir(exist_ok=False)
source=BASE.parent/'Oficina3D/jobs/20261101-131410-crit-t2-soforma'
for name,src in [('forma.glb',source/'entrada/forma.glb'),('refinado.glb',source/'saida/modelo_sem_cor.glb')]:
    shutil.copyfile(src,OUT/name)
report={'entradas':{n:hashlib.sha256((OUT/n).read_bytes()).hexdigest() for n in ['forma.glb','refinado.glb']},'casos':{}}
def save():(OUT/'resultado.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
for label,axis,factor,mixed in [('legitimo',None,1,False),('X2',0,2,False),('X05',0,.5,False),('Y2',2,2,False),('Z2',1,2,False),('X2_misto',0,2,True)]:
    folder=OUT/label;folder.mkdir()
    forma=OUT/'forma.glb'
    if axis is not None:
        mesh=trimesh.load(forma,force='mesh',process=False)
        mesh.vertices[:,axis]*=factor
        forma=folder/'forma.glb';mesh.export(forma)
    vistas=[{'vista':v,'arquivo':str(BASE/f'evidencias/t2/entrada_orc/{v}.png')} for v in ['frente','costas','esquerda','direita']] if mixed else []
    start=time.perf_counter()
    try:
        res=rodar_passo_vertice(folder,OUT/'refinado.glb',vistas,glb_forma=forma)
        row={'concluiu':True,'forma':res['resultado_vertice']['forma_transferencia'],'cobertura':res['cobertura_vertices']}
    except Exception as exc:
        result=json.loads((folder/'cor/resultado_vertice.json').read_text(encoding='utf-8'))
        row={'concluiu':False,'erro':result.get('erro'),'forma':result.get('forma_transferencia')}
    row['parede_s']=round(time.perf_counter()-start,4)
    report['casos'][label]=row;save();print(label,json.dumps(row),flush=True)
report['casos_guarda']={}
for name,dist in [('nan',[float('nan')]),('negativo',[-.1]),('vazio',[])]:
    val=avaliar_alinhamento_forma(dist,{'x':1.,'y':1.,'z':1.})
    report['casos_guarda'][name]={'aceita':val[0],'motivo':val[1]}
save()
