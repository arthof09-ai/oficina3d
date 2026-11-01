"""O teste de GLB real tem de reprovar o exportador anterior a correcao."""
import io,json,os,subprocess,sys,unittest
from pathlib import Path
APP=Path(__file__).resolve().parents[2];BASE=APP.parent
os.environ.update(OFICINA3D_BASE=str(BASE),OFICINA3D_JOBS=str(BASE/'jobs'),PYTHONDONTWRITEBYTECODE='1',TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path[:0]=[str(APP),str(APP/'testes')]
import oficina3d.cor as cor
from test_cor_colorimetria import TestCorGLBReal
OUT=BASE/'evidencias/t2/contraprova';OUT.mkdir(exist_ok=False)
source=subprocess.check_output(['git','show','0e8746e:oficina3d/cor/_blender_vertice.py'],cwd=APP).decode('utf-8')
old=OUT/'exportador_antigo.py'
old.write_text('import sys\nsys.path.insert(0, '+repr(str(APP))+')\n'+source,encoding='utf-8')
cor.SCRIPT_VERTICE=old
log=io.StringIO()
result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.TestSuite([TestCorGLBReal('test_png_real_exporta_oliva_linear')]))
(OUT/'teste_antigo.log').write_text(log.getvalue(),encoding='utf-8')
r={'executados':result.testsRun,'falhas':len(result.failures),'erros':len(result.errors),'esperado':'1 falha numerica sRGB vs linear; 0 erros de infraestrutura'}
(OUT/'resultado.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(log.getvalue());assert r['falhas']==1 and r['erros']==0
