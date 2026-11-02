"""Launcher: trava Windows principal em rb, telemetria 1 Hz, limite 45 min."""
import argparse,json,msvcrt,os,subprocess,sys,time
from pathlib import Path
import psutil
BASE=Path(__file__).resolve().parents[3];APP=BASE/'app';OUT=BASE/'evidencias/paint_spike'
parser=argparse.ArgumentParser();parser.add_argument('--run',required=True);parser.add_argument('--perfil',type=int,default=5)
args=parser.parse_args()
folder=(OUT/args.run).resolve();assert folder.is_relative_to(OUT.resolve())
folder.mkdir(exist_ok=False)
report={'ok':False,'perfil':args.perfil,'trava':'Windows byte 1<<30; handle rb; sem escrever metadados na principal'}
def save():(folder/'supervisao.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
assert json.loads((OUT/'download.json').read_text())['ok'],'Pesos incompletos'
lock=BASE.parent/'Oficina3D/locks/gpu.lock'
with lock.open('rb',buffering=0) as handle:
 handle.seek(1<<30)
 try:msvcrt.locking(handle.fileno(),msvcrt.LK_NBLCK,1)
 except OSError:
  report['bloqueio']='GPU ocupada por trava principal';save();sys.exit(2)
 child=None
 try:
  sample=subprocess.check_output(['nvidia-smi','--query-gpu=utilization.gpu,memory.used,memory.total','--format=csv,noheader,nounits'],text=True)
  use,mem,total=[float(x.strip()) for x in sample.splitlines()[0].split(',')]
  report['gpu_inicial']={'uso_pct':use,'vram_mb':mem,'total_mb':total}
  if use>=30 or mem>=3000:
   report['bloqueio']='GPU ocupada por outro uso conforme limites do projeto';save();sys.exit(2)
  env=dict(os.environ,CODEX_GPU_LOCK_HELD='1',PYTHONDONTWRITEBYTECODE='1',PYTHONUTF8='1',
   TEMP=str(BASE/'_cache/tmp'),TMP=str(BASE/'_cache/tmp'),OMP_NUM_THREADS='4')
  t=time.perf_counter();samples=[];reason=None
  with (folder/'worker.log').open('w',encoding='utf-8') as log:
   child=subprocess.Popen([str(BASE/'.venv_paint/Scripts/python.exe'),'-B',str(APP/'testes/codex/paint_worker.py'),
       '--pasta',str(folder),'--perfil',str(args.perfil)],cwd=folder,env=env,stdout=log,stderr=subprocess.STDOUT)
   process=psutil.Process(child.pid)
   while child.poll() is None:
    stamp=time.perf_counter()
    try:
     gpu=subprocess.check_output(['nvidia-smi','--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True,timeout=5)
     memory,util=[float(x.strip()) for x in gpu.splitlines()[0].split(',')]
     rss=sum(p.memory_info().rss for p in [process]+process.children(recursive=True) if p.is_running())
     samples.append({'s':stamp-t,'vram_mb':memory,'gpu_pct':util,'ram_processo_bytes':rss})
     with (folder/'telemetria.jsonl').open('a') as f:f.write(json.dumps(samples[-1])+'\n')
     if memory>8188:reason='VRAM > 8188 MB'
     if stamp-t>2700:reason='Tempo > 45 min'
     if reason:child.kill();break
    except psutil.NoSuchProcess:break
    time.sleep(max(0.,1-(time.perf_counter()-stamp)))
   code=child.wait()
  report.update(exit_code=code,parede_s=time.perf_counter()-t,limite_violado=reason,
    pico_vram_mb=max((s['vram_mb'] for s in samples),default=None),
    pico_ram_bytes=max((s['ram_processo_bytes'] for s in samples),default=None),amostras=len(samples))
  result=json.loads((folder/'resultado.json').read_text()) if (folder/'resultado.json').exists() else {}
  report['ok']=code==0 and result.get('ok',False) and not reason
  report['resultado_worker']=result;save()
 finally:
  if child is not None and child.poll() is None:child.kill();child.wait()
  handle.seek(1<<30);msvcrt.locking(handle.fileno(),msvcrt.LK_UNLCK,1)
print(json.dumps(report,indent=2))
sys.exit(0 if report['ok'] else 1)
