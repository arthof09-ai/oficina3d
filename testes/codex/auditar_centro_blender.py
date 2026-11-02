"""Prova geometrica independente: dois caminhos T1 discordam no centro."""
import json,math,sys
from pathlib import Path
import numpy as np
APP=Path(__file__).resolve().parents[2];sys.path.insert(0,str(APP))
from oficina3d.cor import _blender_vertice as B,projecao as P
p=json.loads(Path(sys.argv[sys.argv.index('--')+1]).read_text(encoding='utf-8'))
obj=B.importar_glb(p['glb']);verts,_,_=B.extrair_malha(obj)
lo=verts.min(axis=0);hi=verts.max(axis=0);center=(lo+hi)/2;ortho=P.enquadramento(tuple(hi-lo),1024,1024)
_,mask,_=B.ler_imagem(p['imagem']);h,w=mask.shape
px,py=P.projetar(verts,center,'frente',ortho,w,h)
box=(int(math.floor(px.min())),int(math.floor(py.min())),int(math.ceil(px.max())),int(math.ceil(py.max())))
ax,bx,ay,by=P.alinhamento_silhueta(P.bbox_mascara(mask),box)
right,up,_=P.base_camera('frente')
# Formula presente no rasterizador T1, sem chamar rasterizador.
raw_y=(.5-(verts@up)/ortho)*h
difference=ay*(raw_y-py)
result={'ok':True,'centro':center.tolist(),'deslocamento_y_fonte_px_min':float(difference.min()),
 'deslocamento_y_fonte_px_max':float(difference.max()),'formula':'ay * (py_raster_sem_centro - py_projetar_com_centro)',
 'escopo':'Diagnostico somente leitura. Nao aplicado patch, nao medido ganho de correcao.'}
Path(p['resultado']).write_text(json.dumps(result,indent=2),encoding='utf-8')
