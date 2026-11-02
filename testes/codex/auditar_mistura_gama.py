"""Autoauditoria explicita, resultados completos e recursos do processo CPU."""
import hashlib,io,json,sys,time,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import psutil
import bateria_mistura_gama as B
OUT=Path(__file__).resolve().parents[3]/'evidencias/missao_1h_20261102/parte2';OUT.mkdir(parents=True,exist_ok=True)
start=time.perf_counter();proc=psutil.Process();cpu=proc.cpu_times();results={}
def rodar(label,cls):
    stream=io.StringIO();r=unittest.TextTestRunner(stream=stream,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    (OUT/(label+'.log')).write_text(stream.getvalue(),encoding='utf-8')
    row={'testes':r.testsRun,'falhas':len(r.failures),'erros':len(r.errors),'skips':len(r.skipped)};results[label]=row;return row
normal=rodar('vertice_real',B.TestMisturaVertice)
with patch.object(B.V,'srgb_para_linear',side_effect=lambda x:np.asarray(x)):
    identidade=rodar('mutante_identidade',B.TestMisturaVertice)
original=B.V.amostrar_bilinear
# Mutante: re-encode, mistura em sRGB, decodifica. Imita erro que
# converter apenas na entrada/saida nao resolve.
def mistura_srgb(im,mascara,x,y):
    encoded=np.where(im<=.0031308,12.92*im,1.055*np.power(im,1/2.4)-.055)
    return B.V.srgb_para_linear(original(encoded,mascara,x,y))
with patch.object(B.V,'amostrar_bilinear',side_effect=mistura_srgb):
    srgb=rodar('mutante_mistura_srgb',B.TestMisturaVertice)
bake=rodar('bake_real',B.TestMisturaBake)
assert normal==dict(testes=2,falhas=0,erros=0,skips=0)
for row in [identidade,srgb,bake]:assert row==dict(testes=2,falhas=2,erros=0,skips=0)
results['estado']='PARADA: defeito novo medido no bake; tranche incompleta, sem patch de producao'
results['medicao_bake']=B.OBSERVACOES_BAKE
results['painel']={'duracao_s':time.perf_counter()-start,'cpu_usuario_s':proc.cpu_times().user-cpu.user,'cpu_sistema_s':proc.cpu_times().system-cpu.system,'pico_ram_bytes':proc.memory_info().peak_wset,'gpu':'nao usada','tokens_gastos':'nao medido'}
(OUT/'resultado.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results,indent=2))
