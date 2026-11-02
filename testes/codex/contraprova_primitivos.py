"""Contraprova dos dois ataques novos contra o verificador anterior."""
import ast,json,os,struct,subprocess,sys,unittest
from pathlib import Path
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),
 PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path[:0]=[str(APP),str(APP/'testes')]
import test_cor_guardas as T
old=subprocess.check_output(['git','show','7511a68:oficina3d/cor/_blender_vertice.py'],cwd=APP).decode('utf-8')
tree=ast.parse(old)
node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verificar_glb_vertice')
scope={'json':json,'struct':struct}
exec(compile(ast.Module(body=[node],type_ignores=[]),'<verificador_7511a68>','exec'),scope)
T.verificar_glb_vertice=scope['verificar_glb_vertice']
suite=unittest.TestSuite(T.TestDefesaColor0(n) for n in [
 'test_troca_de_acessores_entre_primitivos','test_reordenacao_valida_e_contagem_deslocada'])
result=unittest.TextTestRunner(verbosity=2).run(suite)
assert result.testsRun==2 and len(result.failures)==2 and not result.errors
print('CONTRAPROVA: 2 falhas numericas esperadas, zero erros de infraestrutura')
