"""Download restrito, revisao congelada, sem duplicar bin/safetensors."""
import argparse,hashlib,json,os,shutil,time
from pathlib import Path
BASE=Path(__file__).resolve().parents[3];OUT=BASE/'evidencias/paint_spike';TARGET=BASE/'modelos/paint_spike'
os.environ.update(HF_HOME=str(BASE/'_cache/huggingface'),HF_HUB_CACHE=str(BASE/'_cache/huggingface/hub'),
 HF_HUB_DISABLE_XET='1',HF_HUB_DISABLE_TELEMETRY='1',PYTHONDONTWRITEBYTECODE='1',
 TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'))
import requests
from huggingface_hub import hf_hub_url

def baixar(f,revision):
    target=(TARGET/f['arquivo']).resolve()
    assert target.is_relative_to(TARGET.resolve())
    target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists():return target
    part=target.with_name(target.name+'.part')
    offset=part.stat().st_size if part.exists() else 0
    headers={'Range':f'bytes={offset}-'} if offset else {}
    url=hf_hub_url('tencent/Hunyuan3D-2',f['arquivo'],revision=revision)
    with requests.get(url,headers=headers,stream=True,timeout=(20,60)) as response:
        response.raise_for_status()
        mode='ab' if offset and response.status_code==206 else 'wb'
        with part.open(mode) as stream:
            for chunk in response.iter_content(1024**2):
                if shutil.disk_usage(BASE).free < 6*1024**3:
                    raise OSError('Disco livre abaixo da reserva de 6 GiB')
                stream.write(chunk)
    assert part.stat().st_size==f['bytes']
    if f['lfs']:
        digest=hashlib.sha256()
        with part.open('rb') as stream:
            for chunk in iter(lambda:stream.read(8*1024**2),b''):digest.update(chunk)
        assert digest.hexdigest()==f['lfs']['sha256']
    part.replace(target)
    return target
parser=argparse.ArgumentParser();parser.add_argument('--complemento-bin',action='store_true');args=parser.parse_args()
inventory=json.loads((OUT/'inventario_pesos.json').read_text())
names={f['arquivo'] for f in inventory['arquivos']}
files=[f for f in inventory['arquivos'] if not (f['arquivo'].endswith('.bin') and f['arquivo'][:-4]+'.safetensors' in names)]
if args.complemento_bin:
    files=[f for f in inventory['arquivos'] if f['arquivo']=='hunyuan3d-paint-v2-0/unet/diffusion_pytorch_model.bin']
report_name='download_bin.json' if args.complemento_bin else 'download.json'
report={'revision':inventory['revision'],'bytes_selecionados':sum(f['bytes'] for f in files),
 'livre_antes_bytes':shutil.disk_usage(BASE).free,'destino':str(TARGET),'reserva_bytes':6*1024**3,'arquivos':[],'ok':False}
def save():(OUT/report_name).write_text(json.dumps(report,indent=2),encoding='utf-8')
save()
remaining=sum(f['bytes'] for f in files if not (TARGET/f['arquivo']).exists())
assert shutil.disk_usage(BASE).free>remaining+report['reserva_bytes']
for f in files:
    t=time.perf_counter()
    try:
        path=baixar(f,inventory['revision'])
        h=hashlib.sha256()
        with path.open('rb') as stream:
            for chunk in iter(lambda:stream.read(8*1024**2),b''):h.update(chunk)
        assert path.stat().st_size==f['bytes']
        if f['lfs']:assert h.hexdigest()==f['lfs']['sha256']
        report['arquivos'].append({'arquivo':f['arquivo'],'bytes':path.stat().st_size,'sha256':h.hexdigest(),'tempo_s':time.perf_counter()-t})
        save();print('PESO_OK',f['arquivo'],f['bytes'],flush=True)
    except Exception as exc:
        report['erro']=repr(exc);report['arquivo_falhou']=f['arquivo'];save();raise
report['ok']=True;report['livre_apos_bytes']=shutil.disk_usage(BASE).free;save()
