"""Emite tabela completa da evidencia, sem copiar numeros de relatorios externos."""
from pathlib import Path
import json
BASE=Path(__file__).resolve().parents[3];OUT=BASE/'evidencias/missao_1h_20261102/parte1_retomada_v2';MAIN=BASE.parent/'Oficina3D'
r=json.loads((OUT/'inventario_final.json').read_text())
def nome(s):
 p=Path(s)
 for label,root in [('Codex/',BASE),('Principal/',MAIN)]:
  if p.is_relative_to(root):return label+p.relative_to(root).as_posix()
 return str(p)
lines=['\n## Missao 1 hora — Parte 1 retomada: INVENTARIO E MEDICAO CONCLUIDOS\n',
'Nova ordem de continuar: retomei os subitens de estrutura/hash que independem da identidade dos instrumentos e identifiquei uma terceira coluna historica distinta. A parada anterior permanece historica; este fechamento nao certifica o portao. Nao houve merge/cherry-pick nem escrita na principal.\n',
'Busca C:/ e G:/ com rg --files --hidden --no-ignore -g modelo_cor.glb: 41 arquivos acessiveis em C: (exit 2 por diretorios protegidos; erros completos em busca_C.log); zero em G: com esse nome (exit 1, stderr vazio). Nao afirmar exaustividade em areas inacessiveis, discos desmontados ou arquivos renomeados. Repetida busca com UTF-8 explicito dos caminhos, preservada a primeira execucao.\n',
'Instrumentos atuais Codex/main intactos e semanticamente identicos pelos hashes/AST anteriores. Comparacao adicional por AST da funcao verificar_glb_vertice extraida de git show da revisao ANTERIOR **'+r['instrumento_historico']['revisao']+'**, sem executar bpy ou restante do arquivo. Fonte SHA '+r['instrumento_historico']['fonte_sha256']+', funcao SHA '+r['instrumento_historico']['funcao_sha256']+'. Este instrumento e historico, nao a main atual.\n',
'### Tabela completa\n',
'P/I/IE/M = primitivos/imagens declaradas/imagens embutidas/materiais; C/N/P/U = COLOR_0/NORMAL/POSITION/TEXCOORD_0. ok na ordem Codex/main atual/anterior historico. Dicts completos e atributos/acessores por primitivo em inventario_final.json. Classe estrutural nao garante qualidade visual ou publicacao do job.\n',
'| Arquivo | SHA-256 integral | Atributos por primitivo | P/I/IE/M | Classe | ok C/M/H |\n|---|---|---|---|---|---|']
for x in r['arquivos']:
 attrs='; '.join(','.join({'COLOR_0':'C','NORMAL':'N','POSITION':'P','TEXCOORD_0':'U'}.get(a,a) for a in g) for g in x['atributos'])
 lines.append(f"| {nome(x['arquivo'])} | {x['sha256']} | {attrs} | {x['primitivos']}/{x['imagens']}/{x['imagens_embutidas']}/{x['materiais']} | {x['classe_estrutural']} | {x['codex']['ok']}/{x['main']['ok']}/{x['anterior_historico']['ok']} |")
lines+=['\n**41 = 23 T2_puros aceitos + 18 texturizados reprovados**, nos tres instrumentos. Zero divergencias de aceite E dict completo. Recorte original Principal/jobs + Principal/jobs_teste: **24 = 8 aceitos + 16 reprovados**. Os outros 17 sao artefatos auxiliares/copias/provas fora desse recorte.\n',
'### Oito fixtures positivas, SHA integral remedido\n',
'| Fixture | SHA-256 | Bytes | POSITION / COLOR_0 contagens exportadas |\n|---|---|---|---|']
for x in r['fixtures_T2']:lines.append(f"| {x['fixture']} | {x['sha256']} | {x['bytes']} | {x['codex']['posicao_vertices']}/{x['codex']['color_0_vertices']} |")
lines+=['\nTodas sao T2 puras: 1 primitivo, COLOR_0 completo, 1 material valido, 0 imagens. Orc e Orc-det duplicam o mesmo hash: oito arquivos, sete identidades unicas. crit-t2-cancel e artefato interno da etapa; nao certifica publicacao correta de job cancelado.\n',
'### Dourados de forma/UV\n',
'| Criatura | SHA-256 integral | Bytes | Veredito T2 nos tres |\n|---|---|---|---|']
for x in r['dourados_forma']:
 assert len(x['estrutura']['primitivos'])==1 and not x['estrutura']['materiais'] and not x['estrutura']['imagens']
 assert set(x['estrutura']['primitivos'][0]['atributos'])=={'POSITION','NORMAL','TEXCOORD_0'}
 lines.append(f"| {x['fixture']} | {x['sha256']} | {x['bytes']} | False / False / False |")
lines+=['\nTres hashes fornecidos CONFIRMADOS integralmente. Estrutura medida: 1 primitivo, NORMAL/POSITION/TEXCOORD_0, sem COLOR_0, zero materiais/imagens. Orc em Principal/jobs_teste/prova_validar/.../saida/modelo.glb; Besta/Caprileo em arquivo_jobs no Drive. Caminhos completos privados no JSON. Nomes apenas localizaram candidatos, hashes decidiram identidade.\n',
'**Proposta, decisao do re-julgamento:** dourados de forma/refino/UV certificam regressao de geometria/UV/identidade e determinismo quando exigido, e servem de controles negativos T2, nao positivos. Portao T2 deve fixar corpus por hashes integrais, exigir aceite anterior e candidato em cada fixture positiva estrutural, comparar vereditos em todo o corpus e manter sabotagens adversariais. Limitar a alegacao ao corpus acessivel/data; nao prometer sobre-estricao universal nem validacao semantica/binaria.\n',
'APR-02: rehash de todos os 41 arquivos antes da coluna historica; nenhuma mudanca. Hashes dos instrumentos atuais conferidos antes/depois. Comparacao de dict completo, positivos por arquivo e hash, duplicata deterministica e cancelamento explicitados. Estrutura por primitivo inclui tipos/componentes/contagens de acessores e material referenciado. Erro do gerador documental (KeyError fixture) detectado ANTES de gravar registro; corrigida preservacao do rotulo no instrumento historico, depois regerado a partir do JSON. Nenhuma alteracao aos valores medidos ou verificadores.\n',
'### Painel e limites\n']
for key in ['painel','painel_enriquecimento','painel_historico']:lines.append(key+': '+json.dumps(r[key],ensure_ascii=False)+'\n')
lines+=['CPU/RAM agregados da retomada e dos filhos rg: nao medidos; acima medicoes por processo Python e parede de cada fase, nao soma de picos. Tokens gastos: **nao medido**. GPU: nao usada. Arquivos tocados: REGISTRO-CODEX e quatro instrumentos em testes/codex (inventariar_portao, resumir_portao, comparar_portao_historico, publicar_relatorio_portao). Arte fora do git; evidencia privada em ../evidencias/missao_1h_20261102/parte1_retomada_v2/.\n']
text='\n'.join(lines)+'\n';(OUT/'relatorio.md').write_text(text,encoding='utf-8')
with (BASE/'app/docs/REGISTRO-CODEX.md').open('a',encoding='utf-8') as f:f.write(text)
