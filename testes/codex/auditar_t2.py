"""Reproduz as entradas exatas do T2 e sonda tons intermediarios, sem GPU pesada."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import time

APP = Path(__file__).resolve().parents[2]
BASE = APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE), OFICINA3D_JOBS=str(BASE/'jobs'),
                  PYTHONDONTWRITEBYTECODE='1', TEMP=str(BASE/'_cache/tmp'), TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0, str(APP))
from oficina3d.cor.passo import rodar_passo_vertice
from oficina3d.refino.previa import rodar_blender
from PIL import Image

parser=argparse.ArgumentParser()
parser.add_argument('--fase',choices=['antes','depois'],required=True)
fase=parser.parse_args().fase

SOURCE = BASE.parent/'Oficina3D/jobs/20261101-124814-t2-orc'
OUT = BASE/'evidencias/t2'
INPUT = OUT/'entrada_orc'
INPUT.mkdir(parents=True, exist_ok=True)
manifest=[]
for src, dest in [(SOURCE/'saida/modelo_sem_cor.glb',INPUT/'modelo_sem_cor.glb'),
                  *[(SOURCE/f'preproc/{v}.png',INPUT/f'{v}.png') for v in ['frente','costas','esquerda','direita']]]:
    a=hashlib.sha256(src.read_bytes()).hexdigest()
    if not dest.exists():
        shutil.copyfile(src,dest)
    b=hashlib.sha256(dest.read_bytes()).hexdigest()
    assert a==b, 'Insumo mudou; preservar evidencia existente e usar nova pasta'
    manifest.append(dict(nome=dest.name,bytes=dest.stat().st_size,sha256=b))
(OUT/'entradas.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
report={}
for label in [fase+'_A',fase+'_B']:
    folder=OUT/label
    folder.mkdir(exist_ok=False)
    start=time.perf_counter()
    res=rodar_passo_vertice(folder,INPUT/'modelo_sem_cor.glb',
                          [{'vista':v,'arquivo':str(INPUT/f'{v}.png')} for v in ['frente','costas','esquerda','direita']])
    (folder/'passo.json').write_text(json.dumps(res,indent=2),encoding='utf-8')
    report[label]={'parede_s':round(time.perf_counter()-start,4),
                   'resultado':res['resultado_vertice']}
    (OUT/('reproducao_'+fase+'.json')).write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(label, report[label]['parede_s'],res['resultado_vertice']['sha256_glb'],flush=True)
Image.new('RGBA',(16,16),(137,103,58,255)).save(OUT/'oliva.png')
r=rodar_blender(APP/'testes/codex/probe_gamma_blender.py',{'imagem':str(OUT/'oliva.png')},OUT/('gamma_'+fase),'gamma')
print('SONDA',json.dumps(r),flush=True)
