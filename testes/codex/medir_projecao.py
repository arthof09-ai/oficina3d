"""Compara PNG externo/embutido com texels fonte e gera prova flat T1."""
import hashlib,io,json,os,struct,sys
from pathlib import Path
import numpy as np
from PIL import Image
from skimage.color import rgb2lab,deltaE_ciede2000
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),
 PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
from oficina3d.refino.previa import rodar_blender
from metricas_frentes import medir
OUT=BASE/'evidencias/frente_a';RUN=OUT/'proveniencia';IN=OUT/'entrada'
data=(IN/'modelo_cor.glb').read_bytes();n=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+n])
binary=data[28+n:];bv=doc['bufferViews'][doc['images'][0]['bufferView']]
embed=binary[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']]
(OUT/'embutida.png').write_bytes(embed)
raw=np.load(RUN/'antes_gravacao.npy');origin=np.load(RUN/'proveniencia.npy')
external=np.array(Image.open(IN/'textura.png').convert('RGB'))
embedded=np.array(Image.open(io.BytesIO(embed)).convert('RGB'))
report={'hashes':{name:hashlib.sha256((IN/name).read_bytes()).hexdigest() for name in ['modelo_cor.glb','textura.png']},
 'reproducao_textura_identica':(IN/'textura.png').read_bytes()==(RUN/'textura.png').read_bytes(),
 'reproducao_glb_identico':(IN/'modelo_cor.glb').read_bytes()==(RUN/'modelo.glb').read_bytes(),
 'externa_embutida_pixels_iguais':bool(np.array_equal(external,embedded)),
 'erro_byte_externa_vs_raw_max':float(np.abs(external.astype(float)-np.rint(raw*255)).max()),
 'erro_byte_embutida_vs_raw_max':float(np.abs(embedded.astype(float)-np.rint(raw*255)).max()),
 'regioes_texels':{}}
ref=np.array(Image.open(IN/'frente.png').convert('RGBA'))
bbox=Image.open(IN/'frente.png').getchannel('A').getbbox()
for nome,(a,b,c,d) in {'rosto':(.40,.07,.62,.21),'peito':(.30,.26,.70,.43),'pernas':(.25,.64,.86,.94)}.items():
    x0=round(bbox[0]+a*(bbox[2]-bbox[0]));x1=round(bbox[0]+c*(bbox[2]-bbox[0]))
    y0=round(bbox[1]+b*(bbox[3]-bbox[1]));y1=round(bbox[1]+d*(bbox[3]-bbox[1]))
    mask=(origin[...,0]==0)&(origin[...,1]>=x0)&(origin[...,1]<x1)&(origin[...,2]>=y0)&(origin[...,2]<y1)
    if not mask.any():
        report['regioes_texels'][nome]={'n':0,'motivo':'Nenhum texel vencedor vem desta ROI frontal; nao estimar erro sem amostras.'}
        continue
    source=ref[origin[mask,2],origin[mask,1],:3]
    row={'n':int(mask.sum()),'bbox_fonte':[x0,y0,x1,y1],
      'erro_raw_vs_fonte_max':float(np.abs(raw[mask]*255-source).max())}
    for label,arr in [('externa',external),('embutida',embedded)]:
        row[label]={'deltaE2000_medio':float(deltaE_ciede2000(rgb2lab(source/255.),rgb2lab(arr[mask]/255.)).mean()),
          'erro_byte_max':int(np.abs(arr[mask].astype(int)-source.astype(int)).max())}
    report['regioes_texels'][nome]=row
(OUT/'texels.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2),flush=True)
if not (OUT/'flat/frente.png').exists():
    rodar_blender(APP/'testes/codex/render_flat_blender.py',
        {'modelos':[{'glb':str(IN/'modelo_cor.glb'),'pasta':str(OUT/'flat'),'textura':True}],
         'vistas':['frente']},OUT/'render','flat')
r=medir({'COR05':OUT/'flat/frente.png'},OUT/'metricas_flat.json')
print(json.dumps(r,indent=2))
