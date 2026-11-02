"""Terceira coluna historica, congelada no pai da extracao 5384780."""
import ast,hashlib,json,struct,subprocess,time
from pathlib import Path
import psutil
BASE=Path(__file__).resolve().parents[3];OUT=BASE/'evidencias/missao_1h_20261102/parte1_retomada_v2';MAIN=BASE.parent/'Oficina3D/app'
t=time.perf_counter();proc=psutil.Process();cpu=proc.cpu_times()
rev=subprocess.check_output(['git','-C',str(MAIN),'rev-parse','5384780^'],text=True).strip()
raw=subprocess.check_output(['git','-C',str(MAIN),'show',rev+':oficina3d/cor/_blender_vertice.py'])
source=raw.decode('utf-8-sig');tree=ast.parse(source);nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='verificar_glb_vertice'];assert len(nodes)==1
scope={'json':json,'struct':struct};exec(compile(ast.Module(body=nodes,type_ignores=[]),'<verificador_historico_'+rev+'>','exec'),scope)
(OUT/'verificador_historico.py').write_text(ast.get_source_segment(source,nodes[0]),encoding='utf-8')
r=json.loads((OUT/'inventario_final.json').read_text());r['instrumento_historico']={'revisao':rev,'fonte_sha256':hashlib.sha256(raw).hexdigest(),'funcao_sha256':hashlib.sha256(ast.get_source_segment(source,nodes[0]).encode()).hexdigest(),'rotulo':'historico anterior; NAO main atual'}
for row in r['arquivos']+r['dourados_forma']:
 path=Path(row['arquivo']);h=hashlib.sha256()
 with path.open('rb') as f:
  for chunk in iter(lambda:f.read(8*1024**2),b''):h.update(chunk)
 assert h.hexdigest()==row['sha256'],'Arquivo mudou apos inventario'
 row['anterior_historico']=scope['verificar_glb_vertice'](path);row['dict_historico_igual_codex']=row['anterior_historico']==row['codex'];row['aceite_historico_igual_codex']=row['anterior_historico']['ok']==row['codex']['ok']
byhashpath={row['arquivo']:row for row in r['arquivos']};r['fixtures_T2']=[{'fixture':Path(row['arquivo']).parent.parent.name.split('-',2)[2],**byhashpath[row['arquivo']]} for row in r['fixtures_T2']]
r['painel_historico']={'duracao_s':time.perf_counter()-t,'cpu_usuario_s':proc.cpu_times().user-cpu.user,'cpu_sistema_s':proc.cpu_times().system-cpu.system,'pico_ram_bytes':proc.memory_info().peak_wset,'gpu':'nao usada','tokens_gastos':'nao medido'}
(OUT/'inventario_final.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print('REV',rev,'DIVERGENCIAS_DICT',sum(not x['dict_historico_igual_codex'] for x in r['arquivos']),'DIVERGENCIAS_ACEITE',sum(not x['aceite_historico_igual_codex'] for x in r['arquivos']))
