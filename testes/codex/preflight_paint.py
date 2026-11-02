"""Preflight de import Paint antes de baixar pesos e ocupar a GPU."""
import json,os,sys,time,traceback
from pathlib import Path
BASE=Path(__file__).resolve().parents[3];ENGINE=BASE/'motores/Hunyuan3D-2GP'
os.environ.update(HF_HOME=str(BASE/'_cache/huggingface'),HF_HUB_CACHE=str(BASE/'_cache/huggingface/hub'),
 TRANSFORMERS_CACHE=str(BASE/'_cache/huggingface/hub'),TORCH_HOME=str(BASE/'_cache/torch'),
 HF_MODULES_CACHE=str(BASE/'_cache/huggingface/modules'),PYTHONDONTWRITEBYTECODE='1',
 TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'),HF_HUB_OFFLINE='1')
sys.path[:0]=[str(ENGINE),str(ENGINE/'hy3dgen/texgen/custom_rasterizer'),str(ENGINE/'hy3dgen/texgen/differentiable_renderer')]
t=time.perf_counter()
try:
 import torch
 from hy3dgen.texgen import Hunyuan3DPaintPipeline
 from mmgp import offload
 result={'ok':True,'tempo_s':time.perf_counter()-t}
except Exception as exc:
 result={'ok':False,'erro':repr(exc),'traceback':traceback.format_exc(),'tempo_s':time.perf_counter()-t}
(BASE/'evidencias/paint_spike/preflight.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2));sys.exit(0 if result['ok'] else 1)
