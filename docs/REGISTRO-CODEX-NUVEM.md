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

1. Em cópia/branch de integração, conferir base e os hashes do manifesto.
   Trazer o commit desta Frente 2 por cherry-pick, ou seu diff seletivo;
   não reaplicar os commits antigos inteiros, que carregam documentação caduca.
2. Ordem lógica já resolvida no pacote: C-COR01 → C-GUARD01 (inclui módulo
   novo e import do verificador) → C-COR02 → testes da Frente C/sabotagens.
   Os três estão num único commit coerente para não deixar import quebrado.
3. Rodar as 52 verificações acima e a suíte completa no ambiente do PC.
   Fora desta rodada, liberar os dois testes de exportação real e validar
   oliva, ausência de dupla conversão, todos os primitivos e controle `seco`.
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
  As asserções e os testes originais permanecem intactos.
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
