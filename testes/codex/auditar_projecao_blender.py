"""Auditoria A somente-leitura do codigo T1; instrumentacao em memoria."""
import ast,json,sys,inspect
from pathlib import Path
import numpy as np
import bpy
APP=Path(__file__).resolve().parents[2];sys.path.insert(0,str(APP))
from oficina3d.cor import projecao as P
pedido=json.loads(Path(sys.argv[sys.argv.index('--')+1]).read_text(encoding='utf-8'))
out=Path(pedido['saida_textura']).parent
src=APP/'oficina3d/cor/_blender_cor.py'
tree=ast.parse(src.read_text(encoding='utf-8-sig'))
assert isinstance(tree.body[-1],ast.Expr) and isinstance(tree.body[-1].value,ast.Call) and tree.body[-1].value.func.id=='main'
tree.body.pop()
ns={'__file__':str(src),'__name__':'auditoria_t1'}
exec(compile(tree,str(src),'exec'),ns)
source=inspect.getsource(P.rasterizar_textura)
source=source.replace('pintado = np.zeros', '''origem = np.full((tamanho,tamanho,3), -1, dtype=np.int32)
    pintado = np.zeros''')
source=source.replace('tex[ty[g], tx[g]] = cor[g]', """tex[ty[g], tx[g]] = cor[g]
                origem[ty[g], tx[g], 0] = ['frente','costas','esquerda','direita'].index(nome)
                origem[ty[g], tx[g], 1] = ipx[amostra_ok][g]
                origem[ty[g], tx[g], 2] = ipy[amostra_ok][g]""")
source=source.replace('return tex, pintado, melhor, info', """np.save(OUT_A/'proveniencia.npy',origem)
    return tex, pintado, melhor, info""")
scope=dict(P.__dict__,OUT_A=out)
exec(compile(source,str(src),'exec'),scope)
original=scope['rasterizar_textura']
def raster(*args,**kwargs):
    result=original(*args,**kwargs)
    np.savez_compressed(out/'raster.npz',textura=result[0],pintado=result[1])
    return result
P.rasterizar_textura=raster
old=P.dilatar
def dilatar(*args,**kwargs):
    result=old(*args,**kwargs)
    np.save(out/'antes_gravacao.npy',result[0])
    return result
P.dilatar=dilatar
ns['main']()
