"""Confere producao contra experimento, determinismo e geometria, apos B."""
import hashlib,json,os,sys
from pathlib import Path
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),
 PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
from oficina3d.cor import rodar_vertice
from oficina3d.refino.previa import rodar_blender
from glb_evidencia import geometria_sha
OUT=BASE/'evidencias/frente_b';REF=BASE/'evidencias/t2/entrada_orc'
report={}
for nivel in ['controle','ouro','controle_repeticao']:
    original='controle' if nivel.startswith('controle') else nivel
    entrada=REF/'modelo_sem_cor.glb' if original=='controle' else OUT/f'entradas/{original}/modelo.glb'
    folder=OUT/('producao_'+nivel);folder.mkdir(exist_ok=True)
    req={'modo':'glb','glb':str(entrada),'previas':[],'saida_glb':str(folder/'modelo.glb'),'pasta_previas':str(folder/'previas'),
     'vistas':[{'vista':v,'arquivo':str(REF/f'{v}.png')} for v in ['frente','costas','esquerda','direita']]}
    res=rodar_vertice(req,folder)
    experimental=OUT/f'{original}_bilinear_1.0/modelo.glb'
    assert (folder/'modelo.glb').read_bytes()==experimental.read_bytes()
    assert geometria_sha(folder/'modelo.glb')==geometria_sha(OUT/f'{original}_seco_1.0/modelo.glb')
    report[nivel]={'resultado':res,'geometria_sha256':geometria_sha(folder/'modelo.glb'),
      'bytes':(folder/'modelo.glb').stat().st_size,'identico_experimento':True}
    if nivel=='ouro':
        rodar_blender(APP/'testes/codex/render_flat_blender.py',{'modelos':[{'glb':str(folder/'modelo.glb'),'pasta':str(folder/'flat')}],
         'vistas':['frente','frente-esquerda','esquerda','costas-esquerda','costas','costas-direita','direita','frente-direita']},folder/'render','flat')
(OUT/'producao.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps({k:{'tempo_s':v['resultado']['tempo_s'],'sha256':v['resultado']['sha256_glb'],'bytes':v['bytes']} for k,v in report.items()},indent=2))
