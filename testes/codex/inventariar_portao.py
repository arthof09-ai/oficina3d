"""Inventario somente leitura. Nao certifica diferenciacao entre instrumentos iguais."""
import ast,hashlib,importlib.util,json,os,struct,subprocess,time
from pathlib import Path
import psutil
BASE=Path(__file__).resolve().parents[3];OUT=BASE/'evidencias/missao_1h_20261102/parte1_retomada_v2'
OUT.mkdir(parents=True,exist_ok=False)
t=time.perf_counter();proc=psutil.Process();cpu=proc.cpu_times()
roots=['C:/','G:/'];paths=[];discovery=[]
for root in roots:
 start=time.perf_counter()
 with (OUT/('busca_'+root[0]+'.log')).open('w',encoding='utf-8') as errors:
  result=subprocess.run(['rg','--files','--hidden','--no-ignore','-g','modelo_cor.glb',root],stdout=subprocess.PIPE,stderr=errors,text=True,encoding="utf-8",timeout=600)
 found=result.stdout.splitlines();paths.extend(found);discovery.append({'raiz':root,'exit_code':result.returncode,'arquivos':len(found),'duracao_s':time.perf_counter()-start,'erros_log':'busca_'+root[0]+'.log'})
 (OUT/'descoberta.json').write_text(json.dumps(discovery,indent=2),encoding='utf-8');print('BUSCA',discovery[-1],flush=True)
(OUT/'caminhos.json').write_text(json.dumps(paths,indent=2),encoding='utf-8')
def load(label,path):
 spec=importlib.util.spec_from_file_location(label,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m.verificar_glb_vertice
ours=BASE/'app/oficina3d/cor/validacao_vertice.py';main=BASE.parent/'Oficina3D/app/oficina3d/cor/validacao_vertice.py'
functions=[load('codex_snapshot',ours),load('main_snapshot',main)]
report={'instrumentos':{},'descoberta':discovery,'arquivos':[],'nao_certifica_candidato_distinto':True}
for label,path in [('codex',ours),('main',main)]:report['instrumentos'][label]={'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sha256_ast':hashlib.sha256(ast.dump(ast.parse(path.read_text(encoding='utf-8-sig'))).encode()).hexdigest()}
for i,name in enumerate(sorted(set(paths))):
 path=Path(name);row={'arquivo':name}
 try:
  st=path.stat();h=hashlib.sha256()
  with path.open('rb') as stream:
   header=stream.read(20);magic,version,total,size,kind=struct.unpack('<5I',header);assert magic==0x46546c67 and kind==0x4e4f534a and total==st.st_size
   doc=json.loads(stream.read(size).decode('utf-8'));stream.seek(0)
   for chunk in iter(lambda:stream.read(8*1024**2),b''):h.update(chunk)
  primitives=[p for m in doc.get('meshes',[]) for p in m.get('primitives',[])]
  images=doc.get('images',[]);materials=doc.get('materials',[])
  row.update(sha256=h.hexdigest(),bytes=st.st_size,primitivos=len(primitives),atributos=[sorted(p.get('attributes',{})) for p in primitives],color_0_em_todos=bool(primitives) and all('COLOR_0' in p.get('attributes',{}) for p in primitives),imagens=len(images),imagens_embutidas=sum('bufferView' in im for im in images),materiais=len(materials),materiais_referenciados=[p.get('material') for p in primitives])
  row['classe_estrutural']='T2_puro' if row['color_0_em_todos'] and not images else ('texturizado' if images else 'sem_COLOR_0_ou_misto')
  row['codex']=functions[0](path);row['main']=functions[1](path);row['dicts_iguais']=row['codex']==row['main'];row['aceite_igual']=row['codex']['ok']==row['main']['ok']
  assert path.stat().st_size==st.st_size and path.stat().st_mtime_ns==st.st_mtime_ns,'Arquivo mudou durante leitura'
 except Exception as exc:row['erro']=repr(exc)
 report['arquivos'].append(row)
 (OUT/'inventario.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
 print(i+1,len(paths),row.get('classe_estrutural'),name,flush=True)
report['painel']={'duracao_s':time.perf_counter()-t,'cpu_usuario_s':proc.cpu_times().user-cpu.user,'cpu_sistema_s':proc.cpu_times().system-cpu.system,'pico_ram_processo_bytes':proc.memory_info().peak_wset,'cpu_ram_busca_rg':'nao medidos','tokens_gastos':'nao medido','gpu':'nao usada'}
(OUT/'inventario.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
