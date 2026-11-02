"""Frente B: mesma referencia, perfis reais preservados e variantes CPU."""
import hashlib,json,os,shutil,sys,time
from pathlib import Path
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),
 PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
from oficina3d.refino.previa import rodar_blender
OUT=BASE/'evidencias/frente_b';OUT.mkdir(exist_ok=True)
SRC=BASE.parent/'Oficina3D/jobs';REF=BASE/'evidencias/t2/entrada_orc'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copiar(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():shutil.copyfile(src,dst)
    assert sha(src)==sha(dst)
    return {'origem_job':src.parent.parent.name,'nome':dst.name,'bytes':dst.stat().st_size,'sha256':sha(dst)}
report={'gpu_inferencia':False,'entradas':[],'casos':{}}
guard=['oficina3d/cor/projecao.py','oficina3d/cor/_blender_cor.py','oficina3d/cor/passo.py','testes/test_cor.py']
report['reservados_sha256']={p:sha(APP/p) for p in guard}
def save():(OUT/'resultado.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
save()
modelos={}
for nivel,job in [('prata','20261101-003057-bateriaq-prata'),('ouro','20261101-003200-bateriaq-ouro'),('lendario','20261101-003542-bateriaq-lendario')]:
    folder=OUT/'entradas'/nivel;folder.mkdir(parents=True,exist_ok=True)
    source=SRC/job/'saida/modelo.glb'
    if not source.exists():
        arc=json.loads((SRC/job/'arquivamento.json').read_text(encoding='utf-8'))
        source=Path(arc['destino'])/'saida/modelo.glb'
    if source.exists():
        report['entradas'].append(copiar(source,folder/'modelo.glb'))
    else:
        report['entradas'].append(copiar(SRC/job/'refino/limpa.glb',folder/'limpa.glb'))
        pedido=json.loads((SRC/job/'refino/pedido_refino.json').read_text(encoding='utf-8'))
        pedido.update(entrada=str(folder/'limpa.glb'),saida_glb=str(folder/'modelo.glb'),salvar_blend=None)
        if not (folder/'modelo.glb').exists():
            report.setdefault('refinos_reproduzidos',{})[nivel]=rodar_blender(APP/'oficina3d/refino/_blender_refino.py',pedido,folder,'refino',timeout_s=600)
    modelos[nivel]=folder/'modelo.glb';save()
# Controle exato da medicao anterior 17.10070598.
modelos['controle']=REF/'modelo_sem_cor.glb'
cases=[(n,'seco',1.0) for n in modelos]
cases += [(n,'bilinear',1.0) for n in ['controle','ouro','lendario']]
cases += [('controle','seco',e) for e in [.5,1.5,2.0]]
for nivel,modo,exp in cases:
    label=f'{nivel}_{modo}_{exp}';folder=OUT/label
    if (folder/'resultado_vertice.json').exists():
        res=json.loads((folder/'resultado_vertice.json').read_text(encoding='utf-8'))
    else:
        folder.mkdir(exist_ok=True)
        pedido={'modo':'glb','glb':str(modelos[nivel]),'previas':[],
          'vistas':[{'vista':v,'arquivo':str(REF/(v+'.png'))} for v in ['frente','costas','esquerda','direita']],
          'saida_glb':str(folder/'modelo.glb'),'pasta_previas':str(folder/'previas'),
          'amostragem':modo,'expoente':exp}
        res=rodar_blender(APP/'testes/codex/variantes_vertice_blender.py',pedido,folder,'vertice',timeout_s=900)
    report['casos'][label]=res;save();print(label,res.get('tempo_s'),res.get('sha256_glb'),flush=True)
    if not (folder/'flat/frente.png').exists():
        rodar_blender(APP/'testes/codex/render_flat_blender.py',
           {'modelos':[{'glb':str(folder/'modelo.glb'),'pasta':str(folder/'flat')}],'vistas':['frente']},
           folder/'render','flat',timeout_s=180)
assert report['reservados_sha256']=={p:sha(APP/p) for p in guard}
save()

