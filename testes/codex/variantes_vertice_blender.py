"""Experimento B: variantes em memoria; nao altera defaults do aplicativo."""
import inspect
import ast
import subprocess
import json
from pathlib import Path
import sys
import numpy as np
APP = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(APP))
from oficina3d.cor import _blender_vertice as B
from oficina3d.cor import vertice as V

def bilinear(imagem, mascara, x, y):
    # Centros de pixels em i+0.5; renormalizar evita misturar fundo transparente.
    x = np.clip(x - .5, 0, imagem.shape[1]-1)
    y = np.clip(y - .5, 0, imagem.shape[0]-1)
    x0 = np.floor(x).astype(int); y0 = np.floor(y).astype(int)
    x1 = np.minimum(x0+1, imagem.shape[1]-1)
    y1 = np.minimum(y0+1, imagem.shape[0]-1)
    dx=x-x0; dy=y-y0
    total=np.zeros(len(x)); rgb=np.zeros((len(x),3))
    for xx,yy,w in [(x0,y0,(1-dx)*(1-dy)),(x1,y0,dx*(1-dy)),
                    (x0,y1,(1-dx)*dy),(x1,y1,dx*dy)]:
        w=w*mascara[yy,xx];total+=w;rgb+=w[:,None]*imagem[yy,xx]
    return rgb/np.maximum(total[:,None],1e-15)

def instalar(modo, expoente):
    baseline=subprocess.check_output(['git','show','53e845c:oficina3d/cor/vertice.py'],cwd=APP).decode('utf-8')
    node=next(n for n in ast.parse(baseline).body if isinstance(n,ast.FunctionDef) and n.name=='amostrar_vertices')
    source=ast.get_source_segment(baseline,node)
    source=source.replace('ganha = facing[idx] > melhor[idx]',
        'ganha = facing[idx] ** EXP > melhor[idx]')
    source=source.replace('melhor[sel] = facing[sel]', 'melhor[sel] = facing[sel] ** EXP')
    if modo=='bilinear':
        source=source.replace('imagem[ipy[sel], ipx[sel]]',
            'bilinear(imagem, mascara, ax*px_all[sel]+bx, ay*py_all[sel]+by)')
    ns=dict(V.__dict__,EXP=expoente,bilinear=bilinear)
    exec(compile(source,__file__,'exec'),ns)
    V.amostrar_vertices=lambda *args, **kwargs: ns['amostrar_vertices'](*args)

if __name__=='__main__':
    pedido=B.ler_pedido()
    instalar(pedido.get('amostragem','seco'),pedido.get('expoente',1.0))
    B.main()
