"""Auditoria do bake COR-08: hashes, fonte real por texel e contraprova A0."""
import hashlib,io,json,os,struct,sys
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path.insert(0,str(APP))
from oficina3d.refino.previa import rodar_blender
from metricas_frentes import medir
from glb_evidencia import ler_glb
from oficina3d.cor.projecao import _baricentricas
OUT=BASE/'evidencias/cor08_composicao'
# Faixa inferior geometrica (35% da altura), nao segmentacao semantica das pernas.
doc,prims=ler_glb(OUT/'entradas/modelo_uv.glb')
for node in doc.get('nodes',[]):
    assert 'matrix' not in node and 'rotation' not in node and 'translation' not in node and 'scale' not in node, 'Tratar transformacao de node antes de medir faixa'
T=2048;surface=np.full((T,T),np.nan)
for prim in prims:
    verts=prim['POSITION'].astype(float);uv=prim['TEXCOORD_0'].astype(float)*T
    for tri in prim['indices'].reshape(-1,3):
        pts=uv[tri];x0=max(0,int(np.floor(pts[:,0].min())));x1=min(T,int(np.ceil(pts[:,0].max()))+1);y0=max(0,int(np.floor(pts[:,1].min())));y1=min(T,int(np.ceil(pts[:,1].max()))+1)
        if x1<=x0 or y1<=y0:continue
        xs,ys=np.meshgrid(np.arange(x0,x1),np.arange(y0,y1));result=_baricentricas(pts,xs.ravel()+.5,ys.ravel()+.5)
        if result is None:continue
        inside,w0,w1,w2=result
        h=w0*verts[tri[0],1]+w1*verts[tri[1],1]+w2*verts[tri[2],1]
        surface[ys.ravel()[inside],xs.ravel()[inside]]=h[inside]
lo=min(p['POSITION'][:,1].min() for p in prims);hi=max(p['POSITION'][:,1].max() for p in prims)
lower=surface<=lo+.35*(hi-lo)
report={};expected=[.8177,.7774,.8065,.7957]
for label in ['producao','instrumentado','contraprova_absoluto']:
 folder=OUT/label;r=json.loads((folder/'resultado_cor.json').read_text());assert r['ok']
 row={'resultado':r,'sha256_glb':hashlib.sha256((folder/'modelo.glb').read_bytes()).hexdigest(),'sha256_png':hashlib.sha256((folder/'textura.png').read_bytes()).hexdigest()}
 assert [r['por_vista'][v]['iou_bake_256'] for v in ['frente','costas','esquerda','direita']]==expected
 if label!='producao':
  origin=np.load(folder/'proveniencia.npy')
  direct=origin[...,0]>=0;row['texels_diretos_fora_mapa_superficie']=int((direct&~np.isfinite(surface)).sum())
  assert row['texels_diretos_fora_mapa_superficie']==0
  row['erro_coordenadas_px']=json.loads((folder/'erro_coordenadas.json').read_text())
  row['fonte_por_vista']={v:{'texels':int((origin[...,0]==i).sum()),'y_min':int(origin[...,2][origin[...,0]==i].min()),'y_max':int(origin[...,2][origin[...,0]==i].max())} for i,v in enumerate(['frente','costas','esquerda','direita'])}
  bbox=Image.open(OUT/'entradas/frente.png').getchannel('A').getbbox();row['regioes_fonte_frontal']={}
  for nome,(a,b,c,d) in {'rosto':(.40,.07,.62,.21),'peito':(.30,.26,.70,.43),'pernas':(.25,.64,.86,.94)}.items():
   x0=round(bbox[0]+a*(bbox[2]-bbox[0]));x1=round(bbox[0]+c*(bbox[2]-bbox[0]));y0=round(bbox[1]+b*(bbox[3]-bbox[1]));y1=round(bbox[1]+d*(bbox[3]-bbox[1]))
   mask=(origin[...,0]==0)&(origin[...,1]>=x0)&(origin[...,1]<x1)&(origin[...,2]>=y0)&(origin[...,2]<y1)
   row['regioes_fonte_frontal'][nome]={'n':int(mask.sum()),'bbox_fonte':[x0,y0,x1,y1],'n_na_faixa_inferior_35pct':int((mask&lower).sum())}
  row['fonte_frontal_na_faixa_inferior_35pct']=int(((origin[...,0]==0)&lower).sum())
  row['dimensoes_fonte_frontal']=Image.open(OUT/'entradas/frente.png').size
 if label=='producao':
  data=(folder/'modelo.glb').read_bytes();n=struct.unpack_from('<I',data,12)[0];doc=json.loads(data[20:20+n]);binary=data[28+n:];bv=doc['bufferViews'][doc['images'][0]['bufferView']]
  embedded=np.array(Image.open(io.BytesIO(binary[bv.get('byteOffset',0):bv.get('byteOffset',0)+bv['byteLength']])).convert('RGB'));external=np.array(Image.open(folder/'textura.png').convert('RGB'))
  row['externa_embutida_erro_max_bytes']=int(np.abs(external.astype(int)-embedded.astype(int)).max());assert row['externa_embutida_erro_max_bytes']==0
 report[label]=row
assert report['producao']['sha256_glb']=='a8e793b267db27c2a06669dbb925c91b8863a99ec4f43f558c880a1d10a09b9a'
assert report['producao']['sha256_glb']==report['instrumentado']['sha256_glb']
assert report['producao']['sha256_png']==report['instrumentado']['sha256_png']
assert max(report['instrumentado']['erro_coordenadas_px'].values())==0
assert min(report['contraprova_absoluto']['erro_coordenadas_px'].values())>400
assert report['instrumentado']['regioes_fonte_frontal']['pernas']['n']>0
assert report['contraprova_absoluto']['regioes_fonte_frontal']['pernas']['n']==0
(OUT/'auditoria_centro.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
models=[{'glb':str(OUT/label/'modelo.glb'),'pasta':str(OUT/label/'flat'),'textura':True} for label in ['producao','contraprova_absoluto']]
if not all((Path(m['pasta'])/'frente.png').exists() for m in models):
    rodar_blender(APP/'testes/codex/render_flat_blender.py',{'modelos':models,'vistas':['frente']},OUT/'render_t1','flat')
labels=['contraprova_absoluto','producao','main_prata','c01_prata','c02_prata','c02_ouro']
paths={label:OUT/label/'flat/frente.png' for label in labels}
metrics=medir(paths,OUT/'metricas_composicao.json')
board=Image.new('RGB',(320*len(paths),460),(30,32,36))
for i,(label,path) in enumerate(paths.items()):
 im=Image.open(path).convert('RGBA');im.thumbnail((320,400));board.paste(im,(i*320,40),im.getchannel('A'));draw=ImageDraw.Draw(board);draw.text((i*320+5,5),label,fill='white');draw.text((i*320+5,425),'Face DE %.5f'%metrics['casos'][label]['rosto']['deltaE2000_media'],fill='white')
board.save(OUT/'painel_composicao.png')
print(json.dumps({k:{'sha256_glb':v['sha256_glb'],'erro':v.get('erro_coordenadas_px'),'fontes':v.get('fonte_por_vista'),'regioes':v.get('regioes_fonte_frontal')} for k,v in report.items()},indent=2))
