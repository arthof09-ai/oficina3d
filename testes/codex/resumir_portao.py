"""Enriquece inventario por primitivo e confirma fixtures por SHA integral."""
import hashlib,importlib.util,json,struct,subprocess,time
from pathlib import Path
import psutil
BASE=Path(__file__).resolve().parents[3];OUT=BASE/'evidencias/missao_1h_20261102/parte1_retomada_v2';MAIN=BASE.parent/'Oficina3D'
t=time.perf_counter();proc=psutil.Process();cpu=proc.cpu_times()
r=json.loads((OUT/'inventario.json').read_text())
def parse(path):
 with Path(path).open('rb') as f:
  _,_,_,n,_=struct.unpack('<5I',f.read(20));return json.loads(f.read(n))
def shape(doc):
 rows=[]
 for mi,m in enumerate(doc.get('meshes',[])):
  for pi,p in enumerate(m.get('primitives',[])):
   rows.append({'mesh':mi,'primitivo':pi,'atributos':{k:{'accessor':v,**doc['accessors'][v]} for k,v in p.get('attributes',{}).items()},'material':p.get('material')})
 return {'meshes':len(doc.get('meshes',[])),'primitivos':rows,'imagens':doc.get('images',[]),'materiais':doc.get('materials',[])}
for row in r['arquivos']:
 if 'erro' not in row:
  path=Path(row['arquivo']);row['estrutura_detalhada']=shape(parse(path));row['recorte_original_jobs']=path.is_relative_to(MAIN/'jobs') or path.is_relative_to(MAIN/'jobs_teste')
labels=['t2-orc','t2-orc-det','t2-besta','t2-caprileio','t2-orc-triposr','t2-orc-1vista','crit-t2-soforma','crit-t2-cancel']
fixtures=[]
for label in labels:
 matches=[row for row in r['arquivos'] if row.get('recorte_original_jobs') and Path(row['arquivo']).parent.parent.name.endswith('-'+label)]
 assert len(matches)==1,(label,len(matches));row=matches[0];assert row['classe_estrutural']=='T2_puro' and row['codex']['ok'] and row['main']['ok']
 fixtures.append({'fixture':label,**row})
search=subprocess.run(['rg','--files','--hidden','--no-ignore','-g','modelo.glb','G:/'],capture_output=True,text=True,encoding='utf-8',timeout=180)
(OUT/'busca_dourados_drive.json').write_text(json.dumps({'exit_code':search.returncode,'stderr':search.stderr,'candidatos':[s for s in search.stdout.splitlines() if 'provac-besta-s7' in s or 'provac-caprileo-s7' in s]},indent=2),encoding='utf-8')
candidates=[MAIN/'jobs_teste/prova_validar/20261101-173915-prova-validar-jogo/saida/modelo.glb']+[Path(s) for s in search.stdout.splitlines() if 'provac-besta-s7/' in s.replace('\\','/') or 'provac-caprileo-s7/' in s.replace('\\','/')]
expected={'88c30236272510603c74eb99fc7c5ecd90133c8f01494b3f011d80e310e12514':'Orc','ba8d6cd56395ff17f62da25e07fc84001a01f0845f0528242864c974cf6d8621':'Besta','1b92e3b83c0b2e19fac58ccb8260d6ef1335bce655c2a9f8bce655775db791f5':'Caprileo'}
def load(label,path):
 spec=importlib.util.spec_from_file_location(label,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m.verificar_glb_vertice
ours=load('codex_gold',BASE/'app/oficina3d/cor/validacao_vertice.py');main=load('main_gold',MAIN/'app/oficina3d/cor/validacao_vertice.py')
golds=[]
for path in candidates:
 before=path.stat();h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(8*1024**2),b''):h.update(chunk)
 digest=h.hexdigest();assert digest in expected,(str(path),digest)
 doc=parse(path);golds.append({'fixture':expected[digest],'arquivo':str(path),'sha256':digest,'bytes':before.st_size,'estrutura':shape(doc),'codex':ours(path),'main':main(path)})
 assert path.stat().st_mtime_ns==before.st_mtime_ns
assert len(golds)==3
for label,path in [('codex',BASE/'app/oficina3d/cor/validacao_vertice.py'),('main',MAIN/'app/oficina3d/cor/validacao_vertice.py')]:assert hashlib.sha256(path.read_bytes()).hexdigest()==r['instrumentos'][label]['sha256']
r['fixtures_T2']=fixtures;r['dourados_forma']=golds
r['painel_enriquecimento']={'duracao_s':time.perf_counter()-t,'cpu_usuario_s':proc.cpu_times().user-cpu.user,'cpu_sistema_s':proc.cpu_times().system-cpu.system,'pico_ram_bytes':proc.memory_info().peak_wset,'cpu_ram_rg':'nao medidos','tokens_gastos':'nao medido','gpu':'nao usada'}
(OUT/'inventario_final.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
original=[x for x in r['arquivos'] if x.get('recorte_original_jobs')]
print('TOTAL',len(r['arquivos']),'RECORTE',len(original),'OK',sum(x['codex']['ok'] for x in original),'DIV',sum(not x['dicts_iguais'] for x in r['arquivos']))
for x in fixtures:print(x['fixture'],x['sha256'])
for x in golds:print('DOURADO',x['fixture'],x['sha256'],x['codex']['ok'],x['main']['ok'])
