# Crítico sênior — tranche D-T2 (fechamento das pendências do veredito T2)

- **Tranche julgada:** D-T2 — fechamento de D-T2-1 (S3), D-T2-2, D-T2-3 e D-T2-4 (S4) do
  veredito do T2 (COR-07).
- **Árvore julgada:** `C:\Users\txcga\RPG_Local\Oficina3D\app`, HEAD `4b8384e`, mais as
  alterações NÃO commitadas da tranche D-T2 (diff lido linha a linha):
  `oficina3d/cor/vertice.py`, `oficina3d/cor/_blender_vertice.py`,
  `oficina3d/cor/passo.py`, `oficina3d/worker.py`, `testes/test_cor_vertice.py`,
  `testes/test_cor_passo.py` (6 arquivos, +230/−18). Nada foi commitado nem enviado
  por este Crítico; nada do `probe-dt2` do executor foi apagado ou alterado; nenhum
  job da fila foi tocado; o worker em loop não foi perturbado.
- **Método:** nenhum número do executor foi aceito sem re-medição. Sabotagens próprias
  (script Blender próprio, `probe-dt2-crit/sabotar_crit.py`, eixo e fator por argumento —
  não reutilizado o script do executor); passos de vértice reais próprios no `.venv_app`
  (Blender 5.2.3 LTS); GLBs sintéticos próprios para as arestas do verificador (edição
  só do chunk JSON de um GLB real); passo de projeção real (UV xatlas + bake no Blender,
  só CPU); reexecução integral da suíte; contagem de testes arquivo a arquivo; leitura
  integral do diff. Provas do Crítico em `C:\Users\txcga\RPG_Local\Oficina3D\probe-dt2-crit\`
  (tarefas próprias `Oficina3D_CritDT2*`, todas removidas após o uso).
- **Data do veredito:** 01/11/2026, ~14:15–15:00 (horário de Brasília).

## VEREDITO (dividido por escopo, L-33)

- **MECANISMO: APROVADO — nota 9,5/10.** Nenhum defeito S1/S2. A pendência S3 do T2
  (D-T2-1) está FECHADA: a regra nova (mediana + p90 + razão de caixa por eixo) recusa
  todas as sabotagens globais testadas, incluindo as que a regra antiga aceitava, e
  aceita o par legítimo com margens amplas. Restam quatro ressalvas S4 (abaixo), nenhuma
  bloqueadora: duas de robustez de código fora do caminho real e duas documentais que o
  executor deve corrigir no fechamento (os documentos ele atualiza depois deste veredito,
  por desenho da tranche — a lista do que corrigir está em "Correções exigidas no
  fechamento").
- **QUALIDADE VISUAL: NÃO JULGADA NESTA TRANCHE.** Esta tranche NÃO tem resultado
  visual novo: nenhum modelo, textura ou prévia nova foi produzido para o Mestre ver
  (o passo de projeção real rodado aqui foi prova de mecanismo, sobre o refinado e as
  vistas já existentes, e suas prévias não foram submetidas a julgamento visual).
  Nenhuma aprovação visual está em jogo nesta tranche nem deve ser inferida deste
  veredito. A D1 (fidelidade da cor do modo projeção) segue ABERTA e intocada, como no T2.

## Tabela de conferência — alegação do executor × minha medição

Par legítimo de referência em todos os casos: forma TripoSR Orc do job
`20261101-131410-crit-t2-soforma` (`entrada/forma.glb` + `saida/modelo_sem_cor.glb`).

| Alegação do executor | Minha medição independente | Confere? |
|---|---|---|
| Legítimo: mediana 0,00056 / p90 0,0013 / caixas ≤ 1,00184 → aceito | Meu run próprio (job_legit): mediana **0,00056**, p90 **0,0013**, caixas x **1,00098** / y **1,00184** / z **1,0**, aceito, forma **27.421/27.421 (100%)**, `modo_cor=vertice`, `rotulo=rascunho` | ✔ exato |
| X2: mediana 0,02022 / p90 0,08138 / caixa X 2,002 → RECUSADO pela caixa (regra antiga aceitava) | Minha sabotagem própria X2 (script próprio, fator 2,0 em X): mediana **0,02022**, p90 **0,08138**, caixa X **2,00197**, motivo **"caixa do eixo x fora da faixa: 2,002"**, passo falha com "nenhuma fonte pintou vertice algum" (comportamento esperado: só-forma recusada) | ✔ exato, motivo da caixa confirmado |
| X0,5: mediana 0,04348 / p90 0,12702 / caixa X 0,500 → RECUSADO pelo p90 | Relido em `probe-dt2/resumo_passo2.json` + `job_x05/cor/resultado_vertice.json`: **0,04348 / 0,12702 / 0,50049**, motivo **p90 alto** (a checagem de p90 vem antes da caixa no código, portanto o motivo registrado é o p90 mesmo com a caixa também fora) | ✔ (relido, não reexecutado — ver nota) |
| X1,15: mediana 0,00721 / p90 0,02362 / caixa X 1,151 → aceito (controle) | Relido em `resumo_passo2.json` + `job_x115`: **0,00721 / 0,02362 / 1,15113**, aceito, 27.421 vértices | ✔ (relido, não reexecutado) |
| D-T2-2: `rodar_passo_cor` declara `modo_cor="projecao"`, `rotulo="padrao"` | Código lido (`passo.py:163-166`) + run REAL (não mock): UV xatlas + bake no Blender sobre o refinado do job soforma + 4 vistas canônicas do Orc em `app/testes/dourado/imagens` → retorno com `modo_cor="projecao"`, `rotulo="padrao"`, motivo "bake T1 (projecao das vistas canonicas)", 4 vistas usadas, 0 ausentes, 0 ignoradas; arquivos entregues `modelo_cor.glb` (1.643.868 B) + `textura.png` (513.019 B) + 4 prévias | ✔ exato, fora do mock |
| D-T2-3: aviso virou `_aviso_vistas_ignoradas`; vértice diz "passo vertice (sem bake)", projeção diz "bake" | Código lido (`worker.py`); testes do executor reexecutados na suíte (vértice contém "passo vertice" e não "bake v1"; projeção contém "bake"); nenhum "bake v1" restante no texto do aviso (só na docstring do próprio `_aviso_...`, que explica o texto antigo, e na docstring de `selecionar_vistas` — ver S4-4) | ✔ |
| D-T2-4: `verificar_glb_vertice` exige TODOS os primitivos de TODOS os meshes | Código lido + provas do executor relidas (`resumo_verificar.json`: 1 primitivo ok=True; 2 primitivos com 1 sem COLOR_0 ok=False, `primitivos_sem_cor=1`; 2 com COLOR_0 ok=True) + minhas arestas próprias (abaixo) | ✔ |
| Suíte: 294 testes OK, skipped=1, no `.venv_app` (285 + 9 novos) | Minha reexecução integral: **Ran 294 tests in 25,324s — OK (skipped=1)**; soma arquivo a arquivo dos métodos `def test_` = **294** (arquivo a arquivo: arquivar 14, cli 11, config 15, cor 22, cor_costura 7, cor_passo 14, cor_vertice 26, entrada 13, job 36, mcp 7, motores 29, qualidades 14, refino 30, saude 15, travas 18, uv_xatlas 7, web 7, worker 9); `test_cor_vertice` 26 = 18 do T2 + 8 novos, `test_cor_passo` 14 = 13 + 1 novo — os 9 novos conferem | ✔ exato |

Nota sobre a lacuna do artefato do executor: o `probe-dt2/resumo_passo.json` alegado
na ordem de serviço **não existe no disco** — o `probe_passo.py` do executor quebrou no
caso X2 (o erro do passo, esperado, não era tolerado naquele script) antes de gravar o
resumo, de modo que os números do legítimo/X2 vivem no `probe.log` e nos
`resultado_vertice.json` de cada job, não no resumo. Não é defeito do produto (o
comportamento do passo no X2 é o correto), mas a lista de artefatos da tranche estava
imprecisa — e é por isso que este relatório registra X0,5/X1,15 como "relidos" e
X2/legítimo como "reexecutados por mim": a reprodução própria cobre a lacuna.

## Bateria padrão (Carta do Crítico)

- **(a) Verdade das fontes:** todas as alegações centrais reproduziram (tabela acima),
  com a ressalva do artefato ausente registrada acima. Diff lido linha a linha; nenhum
  número foi aceito de resumo alheio sem fonte primária.
- **(b) Código / casos-limite:** regra nova lida em `vertice.py` (`avaliar_alinhamento_forma`:
  mediana > 0,05 → recusa; p90 > 0,10 → recusa; razão fora de [0,80, 1,25] → recusa;
  amostra vazia → recusa). Bordas medidas por mim: razão 0,80 aceita; mediana 0,05 e
  p90 0,10 exatos aceitos (comparações estritas `>`, intervalo fechado — coerente com o
  documentado); amostra vazia recusada. Limite declarado no próprio comentário do código
  (deformação LOCAL pequena passa pelas três guardas) é honesto e fora do escopo da
  D-T2-1, que era a deformação global anisotrópica do T2 — não é defeito escondido.
- **(c) Interface × spec:** `rodar_passo_cor` agora declara modo/rótulo como o vértice;
  nada mais na interface mudou; web/MCP seguem sem expor `cor_modo` (pendência herdada,
  já declarada no T2, não é defeito novo).
- **(d) Matemática:** somas de cobertura conferem nos meus runs (misto: 20.034 + 0 + 5.450
  + 1.937 = 27.421; legítimo: 27.421 forma = total); razões de caixa conferem com os
  fatores de sabotagem aplicados (2,0 → 2,00197; 0,5 → 0,50049; Z2 → X/Y 0,50).
- **(e) Integridade de estado:** determinismo não foi re-testado nesta tranche (não é
  objeto da D-T2; o código de transferência não tocou o caminho determinístico do T2);
  refinado preservado nos meus jobs (o passo de vértice não reescreve o refinado).
- **(f) Abuso / papéis:** a regra nova NÃO pode ser citada como guarda contra formas de
  origem externa arbitrária além do que ela mede: ela pega deformação global
  anisotrópica, não deformação local nem troca de identidade (uma forma de outro
  personagem com as mesmas proporções passaria). O comentário do código diz isso
  indiretamente ("a regra pega deformacao global anisotropica, que e o caso do
  Critico"); o fechamento documental deve dizer com todas as letras que a guarda não
  atesta identidade da forma — ver "Correções exigidas no fechamento". Dentro do fluxo
  real (forma do próprio job), a guarda cumpre o papel.
- **(g) Visual × referências:** NÃO JULGADA (ver veredito). As prévias do passo de
  projeção real não foram inspecionadas como julgamento visual e não contam como prova
  de qualidade de cor.
- **(h) Coerência interna:** código coerente entre si (`transferir_forma` registra
  `regua_alinhamento` com os três limites; `info` carrega mediana/p90/caixas; motivo
  registra a guarda que recusou). Divergências documentais: ver S4-3 e S4-4.
- **(i) Regressão:** âncoras do T2 não foram re-testadas byte a byte aqui (o diff não
  toca o caminho de bake nem de refino, e a suíte integral passou); defeitos herdados
  do T2: D-T2-1 FECHADA, D-T2-2/3/4 FECHADAS com as ressalvas S4 abaixo; D1 segue ABERTA.
- **(j) Desempenho:** passo de vértice próprio ~2 s de Blender por caso (mesma ordem do
  T2); passo de projeção real completo em uma tarefa agendada (UV + bake, minutos, sem
  medição de tempo publicada aqui porque o relógio da tarefa não foi o objeto).

## Bateria personalizada (desenho — superfícies de risco desta entrega)

Desenhada sobre o risco específico desta tranche: o executor poderia ter "fechado" a S3
com uma guarda que só pega o caso X do T2, ou com testes que só exercem a função nova
isolada. Por isso cada verificação nova mira um eixo que a bateria do T2 não cobria.

**Verificações NOVAS em relação à bateria do T2 (escalada APR-01):**

1. **Reprodução própria da sabotagem X2** (item 2 da ordem): minha forma sabotada, meu
   run do passo — não lido o resumo do executor. Resultado: recusa pela caixa, números
   idênticos aos dele (tabela).
2. **Sabotagem no eixo Y — Y2 e Y0,5** (item 3, NOVO): a regra pega esticamento em Y
   como pega em X? Y2: mediana 0,01995 / p90 0,0686 / caixa Y **2,00368** → RECUSADO
   pela caixa (a regra antiga aceitaria: mediana < 0,05). Y0,5: mediana 0,03277 /
   p90 **0,09779** (< 0,10, ou seja, o p90 NÃO pegaria este caso) / caixa Y **0,50092**
   → RECUSADO pela caixa. Simetria X/Y confirmada; e o Y0,5 prova que a caixa é
   necessária mesmo onde o p90 falha — a redundância das guardas é real, não decorativa.
3. **Caso misto: 4 vistas canônicas + forma sabotada X2** (item 4, NOVO): o passo
   CONCLUI pelas vistas (`ok_passo` verdadeiro, 4 vistas usadas), declara a forma
   RECUSADA com o motivo da caixa (não silenciosamente ignorada) e NÃO pinta lixo da
   forma: cobertura vista 20.034 (73,06%), **forma 0 (0,0%)**, propagação 5.450 (19,88%),
   sem_cor 1.937 (7,06%). O caso que faltava no T2 (só-forma que erra + legítimo) está
   coberto: a rede de segurança degrada com declaração, não com lixo silencioso.
4. **Arestas do `verificar_glb_vertice`** (item 5, NOVO): GLB sem meshes → `ok=False`,
   sem exceção (`primitivos=0`); mesh sem primitivos → `ok=False`, sem exceção; GLB com
   **3 primitivos onde só o TERCEIRO não tem COLOR_0** → `ok=False`,
   `primitivos_sem_cor=1` (a correção cobre o último, não só o segundo); controle com
   3 primitivos todos com COLOR_0 → `ok=True` (72 = 72 vértices).
5. **D-T2-2 fora do mock** (item 6, NOVO): `rodar_passo_cor` de verdade, só CPU, sobre
   o refinado existente + vistas canônicas do Orc em `testes/dourado/imagens` →
   `modo_cor="projecao"`, `rotulo="padrao"` no retorno real (tabela).
6. **Suíte conferida arquivo a arquivo** (item 7, NOVO): soma dos métodos de teste por
   arquivo = 294, igual ao `Ran 294` da minha reexecução (tabela).
7. **Bordas da regra nova** (extra): razão 0,80 aceita; mediana 0,05 e p90 0,10 exatos
   aceitos; amostra vazia recusada (código + medição, não só teste do executor).
8. **Sabotagem no eixo Z — Z2** (extra): a escala uniforme pela altura normaliza o Z,
   então o Z2 aparece como compressão X/Y: escala aplicada 0,50327, caixas X 0,50049 /
   Y 0,50092, mediana 0,07758 / p90 0,14608 → RECUSADO (pela mediana primeiro, com a
   caixa também fora — captura redundante). Nenhum eixo escapa da regra.
9. **Robustez do verificador contra acessor inválido** (extra): virou S4-1.
10. **Dicionário de razões parcial em `avaliar_alinhamento_forma`** (extra): virou S4-2.

## Defeitos

**Nenhum defeito S1/S2.**

### S4-1 — `verificar_glb_vertice` quebra com `IndexError` em acessor COLOR_0 inválido

- **Evidência:** GLB sintético meu com `COLOR_0 = 9999` (fora da lista de acessores)
  → `IndexError: list index out of range`, em vez de `ok=False`. Reproduzível em
  `probe-dt2-crit/crit_verificar.json` (caso `acessor_invalido`).
- **Por que é só S4:** no caminho real a entrada do verificador é a saída do próprio
  passo (sempre bem formada); um acessor inválido não ocorre ali. Mas a função promete
  verificar e, diante de GLB quebrado, quebra em vez de reprovar — a defesa em
  profundidade que a D-T2-4 instalou fica furada exatamente no caso quebrado.
- **Correção sugerida:** tratar índice de acessor fora da lista como
  `primitivos_sem_cor += 1` (ou `ok=False` direto), sem mudar o comportamento nos
  casos bem formados.

### S4-2 — `avaliar_alinhamento_forma` confia na completude do dicionário de razões

- **Evidência:** chamada direta com `{"x": 1.0}` (eixos Y/Z ausentes) e distâncias boas
  → **aceita** (`True, ''`). O eixo ausente simplesmente não é checado.
- **Por que é só S4:** o único chamador real (`transferir_forma`) sempre passa os três
  eixos (`x`, `y`, `z`), e a docstring da função descreve o dict com os três eixos —
  o caminho real está coberto. Mas a função é a guarda de segurança: aceitar um dict
  incompleto sem reclamar é o mesmo padrão de "guarda que não guarda" que a D-T2-1
  acabou de corrigir, em versão menor.
- **Correção sugerida:** exigir as chaves `x`, `y`, `z` (dict incompleto → recusa com
  motivo próprio). Observação vizinha, mesmo espírito, sem classificação própria: o
  helper `_aviso_vistas_ignoradas` indexa `res_cor["vistas_ignoradas"]` diretamente —
  seguro no caminho real (o chamador só o chama quando a chave existe e é não-vazia),
  mas quebraria com `KeyError` em uso direto sem a chave.

### S4-3 — Documental: `DECISOES.md` (COR-07) ainda descreve a regra antiga

- **Evidência:** `docs/DECISOES.md:50`, item (3) do T2, diz "autochecagem por distancia
  mediana (recusa registrada acima de 5% da altura)" — a regra nova (mediana + p90 +
  caixa por eixo) não está lá. Por desenho da tranche os documentos são atualizados
  depois deste veredito, então isto é lista de fechamento, não reprovação do código:
  o executor DEVE atualizar o item COR-07 para a regra D-T2-1, com os três limites e o
  motivo de cada guarda.
- **Correção exigida no fechamento** (junto com o resto da lista abaixo).

### S4-4 — Documental: docstring de `selecionar_vistas` ainda diz "bake v1"

- **Evidência:** `oficina3d/cor/passo.py:69` — "as etiquetas presentes que o bake v1
  nao usa". A D-T2-3 corrigiu o texto do aviso do worker, mas esta docstring (que vale
  também para o modo vértice, onde não há bake) manteve o termo. Trocar por formulação
  neutra ("que o passo de cor não usa") no fechamento.

## Correções exigidas no fechamento (pelo executor, antes do commit final)

1. Atualizar `docs/DECISOES.md` (COR-07) para a regra D-T2-1 completa (S4-3).
2. Atualizar `docs/ESTADO_ATUAL.md` e `docs/REGISTRO.md` com o fechamento da D-T2
   (status do backlog: D-T2-1/2/3/4 fechadas; próximo passo segue o roteiro).
3. Corrigir a docstring "bake v1" em `selecionar_vistas` (S4-4). Opcional, recomendado:
   S4-1 (acessor inválido → reprova, não exceção) e S4-2 (exigir x/y/z) — se o executor
   optar por deixá-los para uma tranche futura, devem entrar no backlog como pendências
   nomeadas, não sumir.
4. Dizer com todas as letras, no REGISTRO do fechamento, o limite da guarda (f): ela
   pega deformação global anisotrópica; NÃO atesta identidade da forma (uma forma de
   outro personagem com as mesmas proporções passaria) nem deformação local pequena.
   Sem essa frase, a guarda pode ser citada no futuro como algo que ela não é.
5. Registrar no REGISTRO que o `resumo_passo.json` alegado não existe (o probe do
   executor quebrou no X2 antes de gravar) e que os números vivem no `probe.log` e nos
   `resultado_vertice.json` — para a próxima auditoria não procurar um arquivo que não
   há.

## Limites declarados desta auditoria (P3)

- O veredito aprova o **mecanismo** da D-T2; **qualidade visual não foi julgada** e a
  D1 segue aberta.
- X0,5 e X1,15 foram **relidos** (resumo + resultado do job do executor), não
  reexecutados por mim; X2, Y2, Y0,5, Z2, legítimo e misto foram **reexecutados por mim**
  com sabotagens próprias.
- A reprodução byte a byte das âncoras do T2 não foi refeita aqui (fora do objeto da
  D-T2; suíte integral passou e o diff não toca bake/refino).
- Nenhuma tarefa agendada minha restou no PC (`Oficina3D_CritDT2*` todas removidas);
  meus probes vivem em `probe-dt2-crit/` (fora do repo `app`, exceto este relatório,
  que é arquivo novo e segue fora do git até o executor commitar).
