"""Completa Gate 0 apos resolver dependencias; preserva resultado inicial."""
import hashlib,importlib,importlib.machinery,json,os,sys,time
from pathlib import Path
BASE=Path(__file__).resolve().parents[3];OUT=BASE/'evidencias/gate0_tentativa2'
assert Path(sys.prefix).resolve()==(BASE/'.venv_paint').resolve()
report={'ok':False,'gpu_inferencia':False,'imports':[]}
original=json.loads((OUT/'resultado.json').read_text())
report['builds_ok']=all(row['exit_code']==0 for row in original['tentativas'] if row['nome'].endswith('_build'))
import torch  # registra diretorio de DLLs antes de carregar extensao PyTorch no Windows
for name,folder,native in [('custom_rasterizer','custom_rasterizer',False),
 ('custom_rasterizer_kernel','custom_rasterizer',True),('mesh_processor','differentiable_renderer',True)]:
 sys.path.insert(0,str(BASE/'motores/Hunyuan3D-2GP/hy3dgen/texgen'/folder))
 t=time.perf_counter()
 try:
  mod=importlib.import_module(name);path=Path(mod.__file__)
  if native:assert any(str(path).endswith(s) for s in importlib.machinery.EXTENSION_SUFFIXES)
  row={'nome':name,'ok':True,'tempo_s':time.perf_counter()-t,'arquivo':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 except Exception as exc:row={'nome':name,'ok':False,'erro':repr(exc)}
 report['imports'].append(row)
report['ok']=report['builds_ok'] and all(r['ok'] for r in report['imports'])
(OUT/'resultado_final.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(0 if report['ok'] else 1)
