# REGISTRO-CODEX-NUVEM — 02/11/2026

Missão: `MISSAO.md` recebido na raiz. Trabalho exclusivo em
`codex/auditoria-sem-pc`, base pública `5cd092d37bddf36a2d888404936d4c9f394528c4`.
`git fetch origin` concluiu; `origin/main` continua nessa base. Não se alterou
`main`, não houve force-push, acesso ao PCDANASA, uso de arte privada, job GPU
ou execução do Blender. Tudo desta rodada fica neste registro e nas evidências
textuais versionadas. Nenhuma rota paga ou pesquisa externa foi executada.

## Método, limites e desvios

- Inspeção inicial: branch já correta, HEAD na base pedida, única entrada não
  rastreada `MISSAO.md` (arquivo do usuário, preservado e fora dos commits).
  `rg --files -g AGENTS.md` não encontrou instruções adicionais na árvore;
  também não foram encontrados AGENTS.md nos diretórios ancestrais consultados.
- Fonte dos patches: objetos Git da branch **pública**
  `origin/codex/melhoria-paralela`, sem mudar para ela. Nenhum arquivo do PC foi
  consultado. Base/SHAs e diffs, em vez de memória, definem a comparação.
- **Desvio de execução:** ao inventariar essa branch pública, li também seu
  `docs/REGISTRO-CODEX.md` via `git show`. A missão manda não usar o registro
  antigo. Não foi acesso ao PC, mas foi leitura indevida diante dessa instrução.
  O arquivo não foi copiado, reconciliado nem usado como prova desta rodada.
  Resultados abaixo exigem código público, testes novos ou documentos da base.
- Autoauditoria é do executor; não constitui veredito de Crítico independente
  nem aprovação visual do Mestre. Nenhum resultado visual novo foi produzido.
- Interpretador inicial: Python 3.12.14 do runtime local; NumPy 2.3.5,
  Pillow 12.3.0; sem bpy, scipy, trimesh, FastAPI, httpx ou MCP inicialmente.
  Difere do ambiente do PC: números de tempo não são comparáveis entre máquinas.

## Frente 1 — centro na COR-08/S2: FECHADA em CPU

**Veredito: CORRIGIDO explicitamente pela COR-08/A0 (`27704b1`), não absorvido
pelo alinhamento e não persistente na base publicada.**

Prova de código: `oficina3d/cor/projecao.py:118` subtrai `centro` em
`projetar`; `:510` faz `rel = p3d - np.asarray(centro, dtype=np.float64)`
no bake, antes da mesma projeção. O diff do commit `27704b1` mostra a troca de
`qx = p3d @ direita; qy = p3d @ cima` por essa subtração.
O commit `22b9d5c` trata o salvamento Standard, sem desfazer a A0.
O teste publicado `test_amostragem_usa_centro_faixas` já cobre o erro.

Prova nova: `testes/test_cor_centro_nuvem.py` compara os **1.024 texels** de um
quadrilátero com uma fórmula independente de UV → 3D → pixel, usa imagem
retangular com gradiente que codifica coordenadas, e verifica invariância à
translação conjunta da malha e do centro nos caminhos bbox e override.
Controle negativo recompila somente a função em memória, removendo a subtração:
a cobertura continua 1.024, mas a faixa inferior amostra a metade superior;
erro máximo de canal >0,4. Nenhum código de produção foi alterado nesta frente.

O deslocamento antigo obedece a `Δy_arte = -ay * (centro·cima)/ortho * altura`.
No sintético explicitamente escolhido (altura 945, centro z=0,5, ortho=1,1,
ay=1), dá **−429,54545 px**, arredondado −429,5. Isso ilustra a fórmula;
**não** reproduz nem autentica os parâmetros ou o mapa de proveniência do
antigo job do Orc. O limite histórico y=511 e a ausência de amostras frontais
nas pernas não podem ser afirmados para a COR-08 sem seus artefatos.

Execução: `python -B testes/auditoria_nuvem.py frente1
testes.test_cor_centro_nuvem testes.test_cor` — **36 executados, 36 passaram,
0 falhas, 0 erros, 0 skips** (3 novos + 33 existentes).
Lista completa: `docs/evidencias-nuvem/frente1.txt`; painel medido:
`docs/evidencias-nuvem/frente1.json`.

| Medida desta execução CPU | Valor |
|---|---:|
| Tempo de parede | 86,757012 s |
| CPU do processo | 27,96875 s |
| Pico working set do processo desde início | 78.675.968 bytes |
| GPU | não usada |
| VRAM / consumo de energia | não medido |
| IoU/cobertura/cores do Orc real, SSIM, DeltaE, PNG×GLB | não medido |

O runner usa diretório temporário para BASE/jobs/caches e registra versões,
IDs de falhas/skips e recursos reais. A suíte completa inicial foi iniciada
separadamente; seu resultado será registrado na frente de integração.

**Para a volta do PC:** executar dois bakes da âncora COR-08 correta
(`cor08rep`, não o job antigo 1024), conferir hashes de entradas, exportar mapa
texel→face→vista→pixel e medir regiões inferiores, determinismo, textura×GLB e
render flat. Qualidade visual e fidelidade continuam pendentes; não reaplicar
um patch de centro que já entrou.

## Frente 2 — Frente D v2: PRONTO PARA INTEGRAR (código + provas CPU)

Pacote montado seletivamente sobre COR-08/S2. Não se fez merge da branch antiga.
`testes/preparar_frente_d_nuvem.py` extrai somente sete arquivos do commit público
`31c2d883e9351b11dcbac6896c5b1f266e619f7e`; antes da escrita verifica que os
dois arquivos de produção já existentes são idênticos entre `0e8746e` e
`5cd092d` e que a cópia de trabalho ainda corresponde à base. Assim, nenhum
delta da COR-08/S2 foi substituído. Manifesto SHA-256 de origem/integrado:
`docs/evidencias-nuvem/integracao-manifesto.json`.

| Mudança / origem pública | Arquivos de produção | Provas nesta rodada |
|---|---|---|
| C-COR01, `7511a68`: decodificar imagem byte sRGB para linear no modo vértice; float e forma já lineares preservados | `cor/vertice.py`, `cor/_blender_vertice.py` | `test_cor_colorimetria.TestCurvaCor` (2) e `test_cor_integracao_nuvem.test_c_cor01…` |
| C-GUARD01, `53e845c` + sabotagens `80c48d0`: recusar NaN/distâncias inválidas; validar COLOR_0 por primitivo | mesmos dois + `cor/validacao_vertice.py` novo | `test_cor_guardas` (12), mais duas contraprovas antes/depois |
| C-COR02, `4836e6f`: bilinear linear com centros i+0,5, máscara renormalizada e controle `seco` | `cor/vertice.py`, `cor/_blender_vertice.py` | `test_cor_amostragem` (4) e contraprova integrada |

Os caminhos de produção da tabela são relativos a `oficina3d/`.
Também entram `testes/test_cor_colorimetria.py`, `test_cor_amostragem.py`,
`test_cor_guardas.py`, leitor puro `testes/codex/glb_evidencia.py` e seu
`__init__.py`. Do teste antigo de colorimetria só foram adaptados o import do
leitor e o skip explícito de Blender nesta rodada. Nada de scripts que leem
jobs do PC ou executam experimentos GPU foi importado. Os demais arquivos
novos da frente são o preparador, o runner, `publicado_nuvem.py` e
`test_cor_integracao_nuvem.py`, mais evidências textuais.

### Antes/depois realmente medido em CPU

`test_cor_integracao_nuvem.py` carrega o código de `5cd092d` por `git show`,
sem checkout. Funções que dependem de bpy são extraídas por AST e recebem
somente a API de pixels simulada; não se finge uma exportação real.

| Contracaso controlado | Publicado `5cd092d` | Integrado |
|---|---:|---:|
| Imagem byte com canal sRGB 0,5 → leitor de vértice | 0,5 tratado como linear | 0,21404114048223255 linear |
| Imagem float com canal 0,5 | 0,5 | 0,5 (sem dupla conversão) |
| Centro do tabuleiro 2×2, amostra de vértice | RGB 0/0/0 (`seco`) | RGB 0,5/0,5/0,5 (bilinear); mesma fonte |
| Distância NaN, caixas 1/1/1 | aceita | recusa |
| Dois primitivos POSITION 3/3, COLOR_0 2/4 | aceita somas 6=6 | recusa, 2 primitivos inválidos |

Quatro contraprovas passaram, 0 falhas/erros/skips: `frente2-contraprovas.txt`
e `.json` (10,670741 s parede; 2,328125 s CPU; pico 43.806.720 bytes).
A bateria integrada `frente2-puro` terminou com **52 executados: 50 passaram,
2 skips, 0 falhas, 0 erros**. Abrange os cinco módulos
`test_cor_amostragem`, `test_cor_colorimetria`, `test_cor_guardas`,
`test_cor_vertice` e `test_cor_integracao_nuvem`; todos os nomes estão no `.txt`.
Skips: exportação real PNG→GLB e forma já linear→GLB, porque Blender é
expressamente excluído nesta missão. Tempo unittest 11,127 s;
parede 92,421240 s; CPU 5,390625 s; pico working set 90.243.072 bytes.
O tempo de parede inclui importação e infraestrutura; não é tempo de bake.
GPU não usada; VRAM, energia, métricas visuais e desempenho do PC: não medido.

### Integração mecânica na volta do PC

1. Receber esta branch na cópia do PC e conferir base/hashes do manifesto.
   Validar nela: o runner desta rodada recusa outro nome de branch. Para a
   integração pelo orquestrador, transportar os commits fechados na ordem,
   com esta Frente 2 fornecendo o código; não reaplicar os commits antigos
   inteiros, que carregam documentação caduca.
2. Ordem lógica já resolvida no pacote: C-COR01 → C-GUARD01 (inclui módulo
   novo e import do verificador) → C-COR02 → testes da Frente C/sabotagens.
   Os três estão num único commit coerente para não deixar import quebrado.
3. Rodar as 52 verificações acima e a suíte completa no ambiente do PC.
   Para testes reais fora desta rodada, usar unittest diretamente, com
   `OFICINA3D_AUDITORIA_SEM_PC` ausente e temporários apontados a jobs_teste:
   `python -B -m unittest discover -s testes -v`. O runner `auditoria_nuvem.py`
   sempre desabilita Blender por desenho, mesmo no PC. Validar exportação
   de oliva, ausência de dupla conversão, todos os primitivos e controle `seco`.
4. Reexecutar bakes/cores duas vezes sobre entradas preservadas com hash,
   comparar geometria/normais/UV/índices, máscaras, cobertura e determinismo.
   Medir renders flat por região e submeter qualidade ao Mestre/Crítico.
   Os números antigos de DeltaE/SSIM não são aceite desta base.

Conflitos esperados: **zero de conteúdo contra a base exata `5cd092d`** nos
arquivos existentes, comprovado pela igualdade acima; sobre avanços futuros,
concentrados em `vertice.py` e `_blender_vertice.py`. Preservar a correção
Standard de `_blender_cor.py`, o centro em `projecao.py`, A1/A3 e os testes
novos da principal. Não aplicar C-COR01 ao bake por simples cópia: o bake tem
contrato de textura sRGB e sua pendência S2-linear requer desenho próprio.
`validacao_vertice` valida estrutura JSON, não offsets/payload binário,
identidade semântica de modelos ou conformidade glTF completa.

### Suíte ampla: tentativas, infraestrutura e bloqueio nativo

- Primeira descoberta, antes de instalar dependências: **337 executados,
  292 passaram, 39 erros, 6 skips, 0 falhas**; parede 186,169598 s,
  CPU 48,656250 s, pico 92.168.192 bytes. Evidência preservada em
  `baseline-completa.json/.txt`. Os erros incluem dependências ausentes e
  raízes temporárias fora da pasta inicialmente gravável; não foram mascarados.
- Criado `.venv_auditoria` com herança de pacotes do runtime, somente nesta
  cópia. Instaladas dependências gratuitas de CPU, sem modelos/torch/CUDA.
  A primeira tentativa de pip foi bloqueada pela rede do sandbox; a repetição
  autorizada concluiu. Versões efetivas constam dos JSONs. Não se alteraram
  requisitos do app nem o ambiente do PC.
- O runner passou a definir `OFICINA3D_JOBS_TESTE`, redireciona apenas a raiz
  `JOBS_TESTE` de módulos legados e desabilita a descoberta de Blender.
  Nessa etapa, as asserções originais não foram alteradas; os ajustes
  posteriores de duas fixtures de processo estão registrados no item 4.
- Duas tentativas amplas encerraram ao entrar no primeiro teste nativo de UV,
  sem resumo unittest/JSON final. `integracao-completa.txt` é log **incompleto**,
  não uma suíte aprovada. A repetição `frente2` foi interrompida pela troca do
  ambiente/permissões e deixou arquivo vazio; não tem contagem utilizável.
- Sonda independente `testes/sonda_xatlas_nuvem.py`: tetraedro, NumPy 2.3.5,
  xatlas 0.0.11, CPython 3.12.14; **access violation 0xC0000005** em
  `Atlas.add_mesh`, antes de `generate`, exit 3221225477; 27,856659 s parede.
  `xatlas-isolado.json` guarda stdout e faulthandler. CPU/pico do filho:
  não medido. Isso prova falha desta combinação local, não defeito da COR-08
  nem falha no PC. A contraprova com NumPy fixado e o resultado amplo final
  serão fechados na seção de autoauditoria.

Registro Git: a primeira gravação de índice foi barrada pelo sandbox; após
autorização, o primeiro commit falhou por identidade ausente. Resolvido usando
`git -c user.name=Codex -c user.email=codex@users.noreply.github.com commit`,
sem alterar configuração global. Frente 1 ficou no commit `d11449a`.

## Frente 3 — auditoria adversarial: FECHADA como diagnóstico reproduzível

Código auditado: projeção/amostragem, preparação de vistas e salvamento em
`_blender_cor.py`, mapa texel→face, médias e BFS/dilatação em
`preenchimento.py`, sempre contra `5cd092d`. Não foi feita pesquisa externa.
Achados abaixo são contracasos provados desta rodada; não se atribui ocorrência
ao Orc real sem seus artefatos, nem se afirma que ninguém os observou antes.

| ID / classificação | Prova mínima CPU e leitura da base publicada | Consequência e encaminhamento |
|---|---|---|
| N01 — S3, contagem falsa de faces pintadas | `projecao.py:495` incrementa `faces_ok` antes de máscara, facing por texel e vencedor; `:533` publica como `faces_pintadas_por_vista`. Máscara com um único pixel fora das amostras: **0 texels pintados, 2 faces reportadas pintadas** | O campo conta faces candidatas rasterizáveis. Corrigir nome ou contar faces com escrita aceita; não usá-lo para atestar cobertura/proveniência. |
| N02 — S3, telemetria de texels dependente da ordem | `projecao.py:526–534` soma vitórias intermediárias, sem retirar a fonte anterior quando há sobrescrita. Frente facing 0,6, esquerda 0,8: textura final idêntica nas duas ordens, toda azul, **1.024 texels**; frente→esquerda reporta **1.024+1.024=2.048**, ordem inversa **0+1.024=1.024** | Esses campos são eventos de escrita, não contribuição final de cada vista. Não somá-los como cobertura nem chamar de mapa de proveniência. Manter eventos explicitamente nomeados e adicionar contagem final por mapa de dono/vista. |
| N03 — S3 condicional, fonte direta fora do quadro | `projecao.py:516–519` aplica `clip` antes de testar máscara, sem rejeição das coordenadas contínuas fora da imagem. Override x+10.000, borda vermelha válida: **1.024 texels diretos vermelhos**, embora nenhuma projeção esteja dentro do quadro | Com arte recortada/alinhamento extrapolado e primeiro/último pixel opaco, a borda vira fonte esticada. O comportamento já é reconhecido por contraste no docstring de `vertice.py`; aqui recebe prova isolada no bake. Rejeitar fora do quadro antes do clip em futura mudança separada, com re-baseline; efeito real no Orc não medido. |
| N04 — S3 documental, trava de aspecto relativa | `projecao.py:331` aceita IoU≥0,999 sem busca; `:369` limita **sx/sy relativo ao inicial**. Caso inicial ax=2, ay=1 já com IoU=1 retorna **ax/ay=2**, enquanto `info.escala_x/escala_y=1`. `docs/REGISTRO.md:877` descreve `|ax/ay−1|≤0,15` | A alegação de trava absoluta não vale. O docstring técnico usa sx/sy; o registro executivo usa ax/ay. Corrigir a leitura para “variação de aspecto relativa ao bbox inicial”; uma trava absoluta exigiria decisão e teste próprios. |

Os IDs de teste correspondentes são `test_n01…` a `test_n04…` em
`testes/test_cor_adversarial_nuvem.py`. Eles carregam o **snapshot congelado**
do Git: documentam o defeito publicado e não obrigam código futuro a conservar
o comportamento. Nenhuma dessas quatro mudanças de produção foi aplicada
silenciosamente ao pacote de integração. São pendências nomeadas, com a
correção e o limite de evidência explícitos.

**S2-linear já conhecido, não contado como achado novo:**
`preenchimento.py:91` tira média no espaço recebido, e `_blender_cor.py`
continua recebendo RGB byte sem decodificação. Dois texels preto/branco dão
**0,5 sRGB**; média em luz linear reencodificada daria
**0,7353569830524495**, diferença **60,0160306784/255** no contracaso de alto
contraste. O quinto teste quantifica essa operação; não mede o erro médio do
Orc, nem demonstra que todo preenchimento se desvia em 60 níveis.
C-COR01 é do modo vértice e não fecha esse S2 do bake. Standard corrige
salvamento; não converte retroativamente a aritmética de médias.

**Outros limites verificados por leitura, sem promover suspeita a defeito novo:**
a oclusão de `_blender_cor.py:400–412` é por centroide da face e não um z-buffer
por texel; a BFS opera no grafo soldado, sem semântica de regiões do corpo.
Não se mediram aqui falsos visíveis nem vazamento semântico na âncora.
O parâmetro `dim` não usado dentro da rasterização não foi anunciado como
novo controle de qualidade. Não há `expoente` de facing exposto no pipeline
de produção auditado; a análise do antigo experimento fica no item 4.

Execução: `python -B testes/auditoria_nuvem.py frente3
testes.test_cor_adversarial_nuvem` — **5 executados, 5 passaram,
0 falhas, 0 erros, 0 skips**. `frente3.txt/.json`: parede **15,341488 s**,
CPU **2,546875 s**, pico **111.095.808 bytes**. GPU/Blender não usados;
VRAM, energia, frequência/impacto dos defeitos no Orc real, SSIM/DeltaE:
**não medido**. Prioridade sugerida de trabalho futuro: tornar telemetria
inequívoca (N01/N02), tratar extrapolação com re-baseline (N03), corrigir a
descrição da trava (N04). Isso é diagnóstico/proposta, não novo job comandado.

Frente 2 fechada no commit `c2828ab`; este registro não declara aprovação
visual nem aprovação independente de qualquer uma das frentes.

## Frente 4 — autoauditoria APR-02 sobre COR-08/S2

Fontes das entregas antigas: **código público**, sem voltar a consultar o
registro antigo proibido, no commit `31c2d883e9351b11dcbac6896c5b1f266e619f7e`:
`testes/codex/frente_a.py`, `auditar_projecao_blender.py`, `frente_b.py`,
`variantes_vertice_blender.py`, `validar_frente_b.py` e testes de cor/guardas.
Confronto com `5cd092d`, com as funções de produção integradas e com os
documentos publicados desta base. Não se inferiu existência ou conteúdo de
evidências privadas apontadas por esses scripts.

| Entrega/alegação anterior | Situação nesta base | Fonte e contraprova atual |
|---|---|---|
| A: deslocamento do centro no bake | **Caducou como defeito presente.** COR-08/A0 corrigiu explicitamente. Não reaplicar patch | Frente 1: teste por 1.024 texels + translação + mutante pre-A0; diff `27704b1` |
| A: PNG salvo com AgX diverge do GLB | **Caducou como diagnóstico do caminho atual de salvamento.** S2 usa Standard. Identidade real PNG×GLB nesta rodada não medida | `_blender_cor.py:546–547`, dois testes estáticos publicados de ordem/unicidade do `save_render`; não substituem sonda Blender |
| A: reutilização do mapa de vista/pixel para auditar a textura nova | **Limitada às fontes diretas.** Instrumentação antiga salva dentro de `rasterizar_textura`; A3 depois cria cores em faces cegas, mais halo | Teste novo com 2 texels: 1 direto → 2 coloridos, sendo 1 por A3; mapa direto ainda tem só 1 fonte. Exigir mapa face/semente/anel para a auditoria completa |
| A: âncora COR-05 e números de cobertura/UV usados como baseline corrente | **Caducaram.** A0/A1/A2/A3 mudam projeção, resolução e preenchimento; o script A ainda aponta o job antigo | `frente_a.py` público aponta `20261101-101528-corint-orc-s7`; docstring `projecao.py:30–36` declara a âncora superada. Não se reaproveitam SHAs/percentuais antigos como medição da COR-08 |
| B: C-COR01 continua necessário no modo vértice | **Confirmado em CPU.** A base publicada ainda lê byte sRGB como linear | Leitor isolado por AST antes/depois: 0,5 → 0,21404114; float 0,5 preservado. Exportação real segue pendente |
| B: C-COR02 bilinear e controle seco continuam aplicáveis | **Confirmado em CPU.** Fontes/facing preservados no contracaso; cor interpolada muda conforme esperado | 4 testes de amostragem + contraprova tabuleiro integrada; modos bilinear/seco e máscara testados |
| B: diagnóstico anterior de placebo no expoente de facing | **Confirmado para a operação antiga.** Potência positiva é monótona; o experimento aplica o expoente só à comparação/armazenamento após o cutoff e não à mescla | `variantes_vertice_blender.py:30–34`; teste com expoentes 0,5/1/1,5/2 preserva vencedor e empate. Não generalizar para expoente≤0 nem mistura ponderada; não existe knob `expoente` em produção |
| B: métricas regionais/Prata–Ouro–Lendário, identidade geométrica e SHAs dos runs antigos | **Não revalidados.** Dependem de malhas, imagens, renders e ambiente do PC | Scripts públicos apontam jobs/evidências externas e precisam de Blender. Nenhum novo DeltaE/SSIM, ranking de qualidade, SHA de GLB ou custo por personagem foi medido aqui |
| C: NaN pode passar e somas COLOR_0 podem esconder primitivo inválido na principal | **Confirmado na base nova e corrigido no pacote.** COR-08/S2 não tocaram os arquivos de vértice | NaN aceito→recusado; POSITION 3/3 × COLOR_0 2/4 aceito→recusado; índices, tipos, normalização, materiais e arquivos truncados nos 12 testes de guardas |
| C: alcance da guarda estrutural | **Continua limitado.** O pacote valida JSON/contagens/tipos por primitivo, sem atestar payload binário ou identidade | Contrato explícito de `validacao_vertice.py`; fixtures de estrutura não são exportações reais. Mesmas contagens entre partes não provam que as cores pertencem semanticamente àquelas partes |
| Escopo dos patches perante a fidelidade de cor do bake | **Restrito ao modo vértice.** O modo vértice e o bake têm contratos diferentes; S2-linear permanece aberto | Teste novo de médias e ausência de decode no bake; quatro arquivos do bake devem continuar idênticos a `5cd092d` |

`testes/test_cor_autoauditoria_nuvem.py` acrescenta quatro verificações:
expoente e ausência de knob de produção; diferença entre médias lineares do
vértice e médias sRGB do bake; limitação do mapa direto diante da A3;
identidade integral dos arquivos `projecao.py`, `_blender_cor.py`,
`preenchimento.py` e `passo.py` contra a base pública.

### Autoauditoria da própria rodada e encerramento do bloqueio xatlas

- Desvio de leitura do registro antigo já declarado na abertura; não foi
  escondido nem convertido em fonte de números novos.
- A baseline inicial teve **293 métodos aprovados**, contados das linhas
  `... ok` do log, e não os 292 calculados pelo primeiro runner. O total
  unittest continua **337 métodos executados**, 6 skips e 39 registros de
  erro, incluindo **1 erro de setUpClass**, que não incrementa `testsRun`.
  Portanto 293 + 6 + 38 erros de método = 337; o erro da classe é adicional.
  O JSON original foi preservado. O runner final conta aprovações em
  `addSuccess`, sem subtrair erros de classe/subtestes do total de métodos.
- Não houve resumo nas tentativas mortas no xatlas: não receberam contagem
  inventada de testes aprovados. O log parcial e o arquivo vazio da tentativa
  interrompida permanecem identificados como tal.
- A sonda nativa repetiu **o mesmo access violation em `Atlas.add_mesh`**
  com NumPy **2.2.6** (13,069337 s) e **1.26.4** (16,413513 s), além do
  primeiro teste com 2.3.5. Todos com CPython 3.12.14 e xatlas 0.0.11.
  Evidências: `xatlas-numpy226.json`, `xatlas-numpy126.json`,
  `xatlas-isolado.json`. **Trocar NumPy não resolveu; causa raiz não
  identificada.** Não há prova de que seja defeito de ABI, instrução de CPU,
  sandbox ou código da Oficina3D; tampouco de que ocorra no Python 3.10 do PC.
- NumPy 1.26.4 tornou o SciPy 1.18.1 local incompatível pelos requisitos
  declarados pelo pip. Foi instalado **SciPy 1.15.3**, versão fixada pelo app
  e compatível, somente no venv da rodada. O ambiente final usa NumPy 1.26.4;
  **não é réplica do PC** (que declara NumPy 2.2.6/Python 3.10). Nenhum arquivo
  de dependências do projeto foi alterado.
- Bloqueio contornado de forma explícita no runner com
  `OFICINA3D_NUVEM_SEM_XATLAS=1`: pulam só os **9 testes nativos** (3 de
  progresso UV, 4 de `TestUvXatlas`, 2 de margem/parametrização). O teste
  de gap entre quadrados puramente NumPy continua rodando. Blender é
  excluído da descoberta e de suas classes mesmo se instalado localmente.
  Nada foi removido da suíte, e as asserções originais não foram afrouxadas.

O resultado final da suíte, o painel completo e as pendências de retorno do PC
estão registrados no fechamento abaixo.

### Falha da fixture de timeout encontrada na suíte ampla

A primeira execução ampla que conseguiu terminar (agora preservada como
`suite-com-timeout.json/.txt`) teve **388 executados, 363 aprovações,
24 skips, 1 erro, 0 falhas**; parede **194,037273 s**, CPU **33,578125 s**,
pico **171.937.792 bytes**. O erro foi em
`test_motores.TestGerarFalso.test_tempo_maximo`: o motor já havia levantado o
erro de tempo máximo esperado, mas o teste tentou ler um arquivo de PID que
o filho poderia ainda não ter escrito antes do timeout de 1,5 s.

Corrigida somente essa fixture em `testes/test_motores.py:391`: o teste
envolve o `Popen` real para capturar PID/horário de criação no **pai**, exige
processo iniciado, `poll()` finalizado e PID não vivo após o timeout. Assim
verifica a morte do processo mesmo quando o filho não chegou a inicializar.
O timeout continua 1,5 s; nenhuma função do motor foi modificada e não se
eliminou a asserção de encerramento. Não foi uma falha de produção comprovada.

Contraprova isolada: **1 executado, 1 aprovado, 0 falhas/erros/skips**;
`timeout-corrigido.json/.txt`, unittest **2,126 s**, parede **8,309081 s**,
CPU **0,750000 s**, pico **35.446.784 bytes**. Uma nova corrida completa foi
necessária para verificar essa correção; a tentativa com erro foi preservada.

Na repetição seguinte surgiu uma falha distinta, preservada em
`suite-com-trava.json/.txt`: **388 executados, 363 aprovações, 24 skips,
1 falha, 0 erros**; parede **203,819797 s**, CPU **30,812500 s**, pico
**172.560.384 bytes**. `test_trava_orfa_de_processo_morto` chamava `p.kill()`
no PID do lançador do venv, embora o próprio arquivo já alertasse que esse PID
pode diferir do intérprete que segura a trava. Matar o lançador não prova a
morte do dono da trava; o teste podia encontrar a trava legitimamente ocupada.

Corrigida somente a fixture em `testes/test_travas.py`: matar por SIGTERM o
PID registrado pelo próprio filho (TerminateProcess no Windows), esperar o
lançador e manter as verificações de órfã, dono morto e recuperação da trava.
No teste de timeout, preservou-se também a verificação do PID real do runner
quando o arquivo chegou a ser escrito integralmente; se o timeout impede o
registro, verifica-se o processo capturado no pai. Os demais testes existentes
de encerramento de filho/neto continuam cobrindo a árvore de processos.
Nenhum código de produção de motores/travas foi alterado.

Contraprova conjunta das duas fixtures finais: **2 executados, 2 aprovados,
0 falhas/erros/skips**; `fixtures-processos.json/.txt`, parede
**13,091503 s**, CPU **1,140625 s**, pico **35.098.624 bytes**.
Nova corrida ampla iniciada para conferir o conjunto com ambas as correções.

### Fechamento da Frente 4 e da missão — CPU

**Frente 4 FECHADA no escopo autorizado, com pendências de PC declaradas.**
Quatro testes específicos de autoauditoria passaram, sem falhas/erros/skips:
`frente4.json/.txt`; parede **8,346381 s**, CPU **1,203125 s**, pico
**43.601.920 bytes**. A corrida ampla final terminou com **388 métodos
executados: 364 aprovados, 24 skips, 0 falhas, 0 erros**.
Nomes de todos os testes: `suite-final.txt`; motivos individuais dos skips,
versões e recursos: `suite-final.json`. Nenhum resultado das tentativas
anteriores foi substituído por uma declaração de sucesso.

| Painel final do Mestre | Medição |
|---|---:|
| Tempo unittest da suíte | 144,228 s |
| Tempo de parede do runner | 182,000646 s |
| CPU do processo runner | 36,046875 s |
| Pico working set do processo desde início | 172.077.056 bytes |
| GPU / Blender | não usados |
| VRAM / energia / recursos dos filhos | não medido |
| Inferência, bake real, SSIM/DeltaE, qualidade visual | não medido |

Os **24 skips** se decompõem em **10 de Blender**, **9 de xatlas nativo**,
**3 de Godot ausente**, **1 de MCP ausente** e **1 de consulta nvidia-smi
ausente**. Não se deduziu inexistência de GPU a partir da ausência do comando.
O teste sintético puro de margem UV passou. Motores executados pela suíte são
scripts falsos de CPU, não inferências nem jobs reais da fila.

Reprodução da corrida restrita, nesta branch e no ambiente documentado:

```powershell
$env:OFICINA3D_NUVEM_SEM_XATLAS = '1'
.\.venv_auditoria\Scripts\python.exe -X utf8 -B testes/auditoria_nuvem.py reproducao-final
.\.venv_auditoria\Scripts\python.exe -X utf8 -B testes/fechar_auditoria_nuvem.py
```

O segundo comando verifica a evidência original `suite-final.json`, além dos
hashes e da árvore atual; não é um substituto da execução de testes.
`ambiente-final.txt` é o freeze **local** do venv com herança de pacotes,
não um lock autossuficiente: os JSONs também registram pacotes herdados,
como Pillow 12.3.0. Não houve alteração do requirements do projeto.

**Verificação final mecânica:** `testes/fechar_auditoria_nuvem.py` concluiu;
**88 fontes Python compiladas sem executá-las**, manifesto da integração
conferido, quatro arquivos do bake idênticos à base, `main` ainda em
`5cd092d37bddf36a2d888404936d4c9f394528c4`, mudanças só textuais e `MISSAO.md`
preservado fora do índice. Evidência: `fechamento.json`. `git diff --check`
sem erro. A compilação emite um SyntaxWarning preexistente de escape no
docstring de `test_travas.py`; isso não foi contado como teste nem ocultado.
Checagem de processos dos testes de trava após as contraprovas: nenhum
filho remanescente encontrado (lista vazia).

**Entrega por frente:** 1 = `d11449a` (centro já corrigido, prova negativa);
2 = `c2828ab` (pacote integrado C-COR01/C-COR02/C-GUARD01 + testes);
3 = `2995ad0` (quatro contracasos/limites publicados + S2 conhecido medido);
4 = commit desta seção (autoauditoria, fixture de processos e fechamento).
Um commit por frente, sem commits na main e sem force-push.

**Pendências para a volta do PC, sem execução nesta rodada:**

1. Rodar os testes nativos de xatlas no Python/venv do PC e investigar a
   combinação local CPython 3.12/xatlas que aborta; causa raiz continua aberta.
2. Executar os dois testes de exportação real de vértice e a suíte com Blender,
   Godot/MCP quando disponíveis. Só o PC pode confirmar o contrato real de
   leitura/exportação da versão dele e a não regressão dos GLBs.
3. Recuperar a âncora correta COR-08/S2 com hashes, repetir o bake, medir
   cobertura/proveniência por região, PNG×GLB, geometria, determinismo e
   custo real. Não usar job antigo 1024 nem números antigos como medidas novas.
4. Tratar N01/N02 de telemetria, decidir o ajuste de fora-do-quadro N03 e
   corrigir a leitura documental N04 em tranche separada. Quantificar/decidir
   o S2-pipeline-linear do bake, que permanece aberto.
5. Reavaliar fidelidade com renders flat e julgamento independente/Mestre.
   A missão de CPU não fecha D1 nem substitui aprovação visual.

Nenhuma dessas pendências foi simulada como concluída. Nenhuma pesquisa,
rota paga, modelo baixado, alteração de serviço/worker ou job GPU foi iniciado.

**Disponibilização remota:** o pré-teste não interativo
`git -c credential.interactive=false push --dry-run origin
HEAD:refs/heads/codex/auditoria-sem-pc` falhou por credenciais ausentes
(`Cannot prompt because user interactivity has been disabled` / `unable to
get password from user`). Era dry-run; nenhum estado remoto foi alterado.
Os quatro commits ficam completos na branch local; a publicação por Git CLI
fica pendente de autenticação do proprietário, sem pedir nem registrar senha.
O bloqueio não impediu os quatro itens da missão, os testes e os commits locais.
