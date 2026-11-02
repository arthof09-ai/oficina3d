"""Controle positivo experimental da bateria, SEM patch de producao."""
import io,json,time,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import psutil
import bateria_mistura_gama as B
BASE=Path(__file__).resolve().parents[3];OUT=BASE/'evidencias/missao_1h_20261102/parte2_retomada';OUT.mkdir(parents=True,exist_ok=False)
start=time.perf_counter();proc=psutil.Process();cpu=proc.cpu_times();results={}
original=B.PF.cores_diretas_por_face
# Adaptador de TESTE: decodifica sRGB, usa media real do PF, recodifica.
# Esperados dos testes sao constantes independentes, nao calculados aqui.
def referencia(textura,pintado,texel_face,n_faces):
    linear=B.V.srgb_para_linear(textura)
    cores,tem,cont=original(linear,pintado,texel_face,n_faces)
    encoded=np.where(cores<=.0031308,12.92*cores,1.055*cores**(1/2.4)-.055)
    return encoded,tem,cont

def rodar(label,cls):
    log=io.StringIO();result=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(cls))
    (OUT/(label+'.log')).write_text(log.getvalue(),encoding='utf-8')
    row={'testes':result.testsRun,'falhas':len(result.failures),'erros':len(result.errors),'skips':len(result.skipped)};results[label]=row;return row

def exige(row,falhas):assert row==dict(testes=2,falhas=falhas,erros=0,skips=0),row
exige(rodar('bake_producao_vermelho',B.TestMisturaBake),2)
with patch.object(B.PF,'cores_diretas_por_face',side_effect=referencia):
    exige(rodar('bake_referencia_experimental_linear',B.TestMisturaBake),0)
    with patch.object(B.V,'srgb_para_linear',side_effect=lambda x:np.asarray(x)):
        exige(rodar('bake_mutante_identidade',B.TestMisturaBake),2)
# Mutante explicitamente volta a media em sRGB do PF atual.
with patch.object(B.PF,'cores_diretas_por_face',side_effect=original):
    exige(rodar('bake_mutante_mistura_srgb',B.TestMisturaBake),2)
exige(rodar('vertice_producao',B.TestMisturaVertice),0)
with patch.object(B.V,'srgb_para_linear',side_effect=lambda x:np.asarray(x)):
    exige(rodar('vertice_mutante_identidade',B.TestMisturaVertice),2)
old=B.V.amostrar_bilinear
def mistura_srgb(im,mascara,x,y):
    encoded=np.where(im<=.0031308,12.92*im,1.055*im**(1/2.4)-.055)
    return B.V.srgb_para_linear(old(encoded,mascara,x,y))
with patch.object(B.V,'amostrar_bilinear',side_effect=mistura_srgb):
    exige(rodar('vertice_mutante_mistura_srgb',B.TestMisturaVertice),2)
results['observacoes_bake']=B.OBSERVACOES_BAKE
results['estado']='Bateria diagnosticada; producao bake permanece vermelha; somente referencia experimental passa'
results['painel']={'duracao_s':time.perf_counter()-start,'cpu_usuario_s':proc.cpu_times().user-cpu.user,'cpu_sistema_s':proc.cpu_times().system-cpu.system,'pico_ram_bytes':proc.memory_info().peak_wset,'gpu':'nao usada','tokens_gastos':'nao medido'}
(OUT/'resultado.json').write_text(json.dumps(results,indent=2),encoding='utf-8');print(json.dumps(results,indent=2))
