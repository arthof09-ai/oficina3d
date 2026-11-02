"""Inferencia Paint isolada; so executar via executar_spike_paint.py (trava)."""
import argparse,hashlib,json,os,sys,time,traceback
from pathlib import Path
BASE=Path(__file__).resolve().parents[3];ENGINE=BASE/'motores/Hunyuan3D-2GP'
parser=argparse.ArgumentParser();parser.add_argument('--pasta',required=True);parser.add_argument('--perfil',type=int,default=5)
args=parser.parse_args();out=Path(args.pasta).resolve()
assert out.is_relative_to((BASE/'evidencias/paint_spike').resolve())
assert os.environ.get('CODEX_GPU_LOCK_HELD')=='1','Usar launcher com trava principal'
os.environ.update(HF_HOME=str(BASE/'_cache/huggingface'),HF_HUB_CACHE=str(BASE/'_cache/huggingface/hub'),
 HF_MODULES_CACHE=str(BASE/'_cache/huggingface/modules'),TORCH_HOME=str(BASE/'_cache/torch'),
 TORCH_EXTENSIONS_DIR=str(BASE/'_cache/torch_extensions'),XDG_CACHE_HOME=str(BASE/'_cache'),
 HF_HUB_OFFLINE='1',HF_HUB_DISABLE_TELEMETRY='1',PYTHONDONTWRITEBYTECODE='1',
 TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
sys.path[:0]=[str(ENGINE),str(ENGINE/'hy3dgen/texgen/custom_rasterizer'),str(ENGINE/'hy3dgen/texgen/differentiable_renderer')]
t=time.perf_counter();report={'ok':False,'perfil':args.perfil,'seed_delight':42,'seed_multiview':0,'passos_delight':50,'passos_multiview':30}
def save():(out/'resultado.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
try:
 import torch,trimesh
 from PIL import Image
 from hy3dgen.texgen.pipelines import Hunyuan3DPaintPipeline,Hunyuan3DTexGenConfig
 from mmgp import offload
 weights=BASE/'modelos/paint_spike'
 # Diffusers 0.39 exige opt-in ate para o custom_pipeline LOCAL do fork.
 # Escopo estrito: modelo e codigo ja inspecionados nesta copia; rede offline.
 from hy3dgen.texgen.utils import multiview_utils as MV
 factory=MV.DiffusionPipeline
 class LocalPaintLoader:
  @staticmethod
  def from_pretrained(path,**kwargs):
   assert Path(path).resolve()==(weights/'hunyuan3d-paint-v2-0').resolve()
   assert Path(kwargs['custom_pipeline']).resolve()==(ENGINE/'hy3dgen/texgen/hunyuanpaint').resolve()
   return factory.from_pretrained(path,trust_remote_code=True,local_files_only=True,**kwargs)
 MV.DiffusionPipeline=LocalPaintLoader
 report['loader']='opt-in apenas custom_pipeline local inspecionado; offline'
 report['codigo_local_sha256']={str(p.relative_to(BASE)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [
  ENGINE/'hy3dgen/texgen/hunyuanpaint/pipeline.py',
  ENGINE/'hy3dgen/texgen/hunyuanpaint/unet/modules.py',
  weights/'hunyuan3d-paint-v2-0/unet/modules.py']}

 report['etapa']='carregar_modelos';save()
 pipe=Hunyuan3DPaintPipeline(Hunyuan3DTexGenConfig(str(weights/'hunyuan3d-delight-v2-0'),str(weights/'hunyuan3d-paint-v2-0')))
 models=offload.extract_models('texgen_worker',pipe)
 report['modelos_offload']=list(models);save()
 pipe.models['multiview_model'].pipeline.vae.use_slicing=True
 kwargs={'budgets':{'*':2200}}
 # Sem modelo de forma: perfil 4 fixa os modelos do proprio Paint conforme mmgp.
 offload.profile(models,profile_no=args.perfil,verboseLevel=1,**kwargs)
 source=BASE/'evidencias/t2/entrada_orc'
 mesh=trimesh.load(str(source/'modelo_sem_cor.glb'),force='mesh',process=False)
 image=Image.open(source/'frente.png').convert('RGBA')
 report['entrada_triangulos']=len(mesh.faces)
 report['entrada_sha256']=hashlib.sha256((source/'modelo_sem_cor.glb').read_bytes()).hexdigest()
 report['imagem_sha256']=hashlib.sha256((source/'frente.png').read_bytes()).hexdigest()
 report['carregamento_s']=time.perf_counter()-t;report['etapa']='pintar';save()
 paint_start=time.perf_counter()
 mesh=pipe(mesh,image=image)
 report['pintura_s']=time.perf_counter()-paint_start
 mesh.export(str(out/'modelo.glb'))
 material=mesh.visual.material
 texture=getattr(material,'baseColorTexture',None)
 if texture is None:texture=getattr(material,'image',None)
 if texture is None:raise RuntimeError('Saida Paint sem imagem de textura')
 texture.save(out/'textura.png')
 report['sha256_glb']=hashlib.sha256((out/'modelo.glb').read_bytes()).hexdigest()
 report['sha256_textura']=hashlib.sha256((out/'textura.png').read_bytes()).hexdigest()
 report['ok']=True;report['etapa']='concluido'
except Exception as exc:
 report['erro']=repr(exc);report['traceback']=traceback.format_exc()
 print(report['traceback'],flush=True)
finally:
 report['parede_s']=time.perf_counter()-t;save()
sys.exit(0 if report['ok'] else 1)
