# Crítico sênior — COR-05: integração do `cor` à fila de jobs

- **Tranche julgada:** COR-05, item (c) da Etapa COR.
- **Commit:** `e3a4ca41ab53eff8e19d3c1a9b391219de9604fe` — "COR-05: integracao do cor a fila de jobs (etapa opcional pos-refino) + job de prova Orc Prata (aguarda Critico)".
- **Job de prova:** `20261101-101528-corint-orc-s7` (Orc, 4 vistas douradas, `--qualidade prata --seed 7 --cor`).
- **Método:** nenhum número do executor foi aceito sem re-medição. GLB re-parseado por parser binário próprio (struct + JSON, sem trimesh, sem `costura.py`); hashes refeitos no PC (`Get-FileHash`) e na minha máquina (sha256sum pós-scp); suíte recontada por discovery própria e reexecutada no `.venv_app`; diff do commit lido linha a linha; código do worker e do passo lido, não resumido; 4 prévias da cor inspecionadas visualmente contra a frente dourada do Orc.
- **Data do veredito:** 01/11/2026, ~10:30–11:00 (horário de Brasília).

## VEREDITO: FECHADO (integração) — com pendências S3/S4 nomeadas abaixo

A integração do `cor` à fila **fecha**: o pipeline funciona de ponta a ponta via fila real (job concluído sob o worker novo, com etapa `cor` entre refino e exportar), o GLB final é válido e texturizado (provado por parse próprio), as métricas têm lastro (hashes conferidos em 3 lugares: job, manifesto do Drive e minha medição), o caminho sem-cor está preservado por código, o commit não contém arte do RPG nem segredos, e **não há nenhuma pendência S1/S2 nova**.

**Escopo exato do FECHADO:** fecha a *integração* (fiação CLI → worker → passo → exportar → arquivo). NÃO fecha a fidelidade da cor: a **D1 segue ABERTA** e este veredito não pode ser lido como "o Orc colorido está fiel". Nenhum defeito S3/S4 abaixo bloqueia o fechamento pelo critério de aceite; todos viram pendências nomeadas.

## Julgamento explícito sobre a D1 aberta (item 9, critério do executor)

**Concordo com o critério do executor: a D1 aberta NÃO bloqueia esta etapa — e o critério está correto, não apenas tolerável.** Razões: (1) a D1 é anterior à COR-05 e não mudou de natureza nem de magnitude com a integração — os IoUs do bake da prova (0,7237–0,7929) caem na mesma faixa do bake T1 do Orc (0,72–0,79), e o caráter visual (mosaico) é o mesmo dos bakes T1/T5; (2) o objeto desta tranche é a fiação, não a fidelidade, exatamente como T1, T5, D-T5-1 e D2/D7 fecharam com a D1 aberta; (3) reprovar a integração pela D1 puniria a tranche errada e travaria o corpo (CORPO-01) por um problema que pertence às frentes de fidelidade (T2/T3/T7 e retrabalho). **Guarda:** o FECHADO deve continuar registrado junto da D1 aberta em ESTADO_ATUAL e no backlog; qualquer leitura pública de "cor pronta/fiel" a partir deste veredito seria falsa.

## Itens da bateria, um a um

### 1. Parse binário próprio do GLB final — PASSOU

Parser próprio (`struct`, sem trimesh, sem `costura.py`) aplicado aos 3 GLBs baixados por scp:

| Arquivo | Bytes | Meshes/prims | Triângulos (índices ÷ 3) | TEXCOORD_0 | Imagens | Materiais |
|---|---|---|---|---|---|---|
| `saida/modelo.glb` | 3.230.584 | 1/1 | **49.750** (149.250 índices) | sim, 71.336 VEC2 | **1** (PNG, 349.459 B) | **1** ("cor", `baseColorTexture: 0`) |
| `cor/modelo_cor.glb` | 3.230.584 | 1/1 | 49.750 | sim, 71.336 | 1 | 1 ("cor") |
| `saida/modelo_sem_cor.glb` | 2.388.272 | 1/1 | 49.750 | sim, 65.274 (UV do refino) | 0 | 0 |

- `saida/modelo.glb` **byte-idêntico** a `cor/modelo_cor.glb` (`cmp` limpo; SHA-256 `0f8385380b22f86894355e6e944fc74ce910ef3a3b60d56ef341bfb57e9bf48c` nos dois, medido no PC e na minha máquina).
- `saida/modelo.glb` **diferente** de `saida/modelo_sem_cor.glb` (SHA `5467f25e900cf9ab43b84ccbaecc4b42d81deab4cfe0887c9a33447769b41d00`, medido nos dois lados).
- Precisão contra a alegação do bake ("1 imagem, 1 material com textura"): **confirmada por via independente**.
- Ressalva medida (não é defeito): a imagem embutida no GLB (349.459 B, SHA `8d5e9939…`) **não é byte-idêntica** a `cor/textura.png` (349.022 B, SHA `ebd744a9…`) — o Blender re-codifica o PNG na exportação. A âncora do bake é o arquivo `cor/textura.png`; a do modelo é o GLB. Não confundir as duas.
- Observação (vira S4, D-COR05-4): vértices 65.274 (refino) → 71.195 (xatlas com costura) → 71.289 (`resultado_cor`) → 71.336 (GLB final, medido). Triângulos estáveis em 49.750 e dimensões idênticas (0,6794 × 0,69656 × 1,0); a divergência de vértices entre estágios não está explicada nos docs.

### 2. Delta +2 da suíte (252 → 263 contra 9 testes novos) — EXPLICADO, NÃO É DEFEITO

Discovery própria (`.venv_app`, `unittest.defaultTestLoader.discover("testes")`), idêntica à do executor:

| Módulo | Testes | Módulo | Testes |
|---|---|---|---|
| test_arquivar | 14 | test_qualidades | 14 |
| test_cli | 11 | test_refino | 30 |
| test_config | 15 | test_saude | 15 |
| test_cor | 22 | test_travas | 18 |
| test_cor_costura | 7 | test_uv_xatlas | 7 |
| **test_cor_passo** | **9** | test_web | 7 |
| test_entrada | 13 | test_worker | 9 |
| test_job | 36 | **TOTAL** | **263** |
| test_mcp | 7 | | |
| test_motores | 29 | | |

17 módulos, soma 263 — e a contagem por `def test_` coincide módulo a módulo com a discovery (nenhuma geração dinâmica, herança ou `load_tests` inflando o número; os `subTest` de `test_config.py`/`test_job.py`/`test_qualidades.py` não alteram `testsRun`).

Reconciliação exata, com carimbo de tempo:

- O `suite.log` da D2/D7 (252 testes) foi gravado em **01/11 08:31:30**, sobre a árvore do commit `17462aa` (08:31:48), onde `test_cor_costura` tinha **5** testes → total 252.
- O commit `aa2758c` (01/11 **08:45:57**, posterior ao log) acrescentou exatamente **2** testes a `test_cor_costura` (5 → 7): `test_vertice_duplicado_sem_solda_vira_borda_e_com_solda_classifica` e `test_piores_costuras_ordena_e_da_ponto_medio`.
- A COR-05 acrescentou **9** (`test_cor_passo`).
- **252 + 2 + 9 = 263. Delta totalmente explicado.** A ressalva do REGISTRO ("+2 NÃO atribuídos; nenhum teste commitado desde aa2758c") inverteu a direção: os +2 vieram *do* `aa2758c` em relação à baseline defasada de 252, não depois dele. O baseline correto pré-tranche é **254**, não 252. Correção documental devida (S4, D-COR05-4). Nenhum teste fantasma, nenhum teste perdido.

### 3. Não-regressão para jobs SEM `--cor` — PASSOU POR CÓDIGO + JOB PRÉ-INTEGRAÇÃO, com ressalva S3

Leitura do diff de `worker.py` (linhas da etapa `cor` + exportar):

- Sem `cor`, `modelo_final = Path(res.get("glb") …)` é exatamente o valor que o código antigo usava em `modelo = …`; o exportar valida e publica o mesmo GLB; `previas` soma `cor_previas` ausente (lista vazia); `glb_sem_cor` só é registrado `if op.get("cor")`; nenhum arquivo novo é tocado. **Artefatos byte-idênticos ao caminho antigo.**
- A única mudança que atinge jobs sem-cor é cosmética: a faixa de progresso do refino (80–98 → 80–95) — muda percentuais exibidos, não o GLB.
- `config.OPCOES_PADRAO["cor"] = False`, validação bool em `job.OPCOES_BOOL`, flag `--cor` opt-in na CLI. Default seguro.
- Prova pré-integração: o job `20261031-225432-provac-orc-s7` (concluído 31/10 22:55, worker antigo PID 25544) tem `opcoes` sem chave `cor`, `etapas = entrada, forma, refino, arquivar` (sem `cor`), `resultado` com 5 prévias e **sem** `glb_sem_cor` nem prévias da cor.
- **Ressalva (D-COR05-2, S3):** nenhum job SEM `--cor` rodou sob o worker novo (PID 31976) — o único job pós-reinício é o de prova, COM cor. A não-regressão está provada por diff + job pré-integração, não por job vivo pós-integração. A confirmação viva (1 job sem-cor sob o worker novo) fica como pendência da próxima tranche; não bloqueia o fechamento, mas o veredito "sem regressão" deve ser lido com essa qualificação.

### 4. Reexecução dos 9 testes novos + SUITE_RESULT — PASSOU

- Reexecução própria no `.venv_app`: `python -m unittest testes.test_cor_passo -v` → **9 testes, OK** (5 de `TestSelecionarVistas`, 2 de `TestOpcaoCor`, 1 de `TestFaixasCor`, 1 de `TestCliCor`), sem GPU/Blender.
- `jobs_teste/cor_integracao/suite.log`: `Ran 263 tests in 24.573s — OK (skipped=1)` e `SUITE_RESULT tests=263 failures=0 errors=0 skipped=1 ok=True` — **idêntico à minha discovery (263)**. Zero divergência.
- O skipped=1 é o mesmo das suítes anteriores (não investigado aqui; não é novidade desta tranche).

### 5. Commit `e3a4ca4` — PASSOU

Arquivos (9, nenhum binário): `docs/DECISOES.md`, `docs/ESTADO_ATUAL.md`, `docs/REGISTRO.md`, `oficina3d/cli.py`, `oficina3d/config.py`, `oficina3d/cor/passo.py` (novo), `oficina3d/job.py`, `oficina3d/worker.py`, `testes/test_cor_passo.py` (novo).

- **Zero** PNG/GLB ou outro binário no diff; zero ocorrências, no diff inteiro, de IPs da tailnet (`100.64.`, `100.66.`, `100.97.`), tokens (`ghp_`, `sk-`, `token`) ou e-mails pessoais (`gmail`, `hotmail`, `BEGIN … KEY`). O e-mail do autor é o `noreply` do GitHub (metadado do commit, padrão do projeto).
- Diff do worker no caminho sem-cor: além da faixa de progresso (item 3), **nenhuma alteração de comportamento** — a etapa `cor` é estritamente condicional a `op.get("cor")`, e o exportar sem-cor executa o mesmo código de antes.

### 6. Semântica de falha e cancelamento — PASSOU, com janela S3

Lido em `oficina3d/cor/passo.py`, `oficina3d/worker.py`:

- **Sem vista canônica → erro do job, não skip:** `selecionar_vistas` levanta `ValueError` (nenhuma canônica, arquivo canônico ausente, GLB refinado ausente); o worker converte em `ErroEtapa("cor", …)` (worker.py, `except ValueError`) e o handler externo (`except Exception`) marca `estado="erro"`, grava traceback em `log.txt` e relatório parcial — nada apagado, nenhum modelo sem-cor passado por colorido. Confirmado nos 4 testes de `TestSelecionarVistas` que cobrem esses caminhos.
- **Falha no Blender → erro do job:** `ErroBlender` de `rodar_blender`/`rodar_cor` e `RuntimeError` (UV não entregue, ocupação divergente além de 0,02, bake sem `modelo_cor.glb`+`textura.png`) caem no mesmo handler externo → `estado="erro"`. Nenhum caminho de fallback silencioso existe no passo (a única tolerância é a guarda de ocupação, que *falha* quando divergente).
- **Cancelamento — respeitado, com uma janela (D-COR05-1, S3):** `_verificar_cancelado` é chamado imediatamente antes da etapa `cor`, e `_Progresso` verifica o flag no disco a cada callback (intervalo 3 s). Os callbacks *existem* durante o Blender (o `log.txt` do job mostra 18%/25%/45%/55%/75%/85%/93%/100% durante o bake). **Mas** `uv_xatlas.gerar_uv` roda ~97,5 s (`metricas_uv.tempo_s = 97,49`) entre `avisar(5)` e `avisar(30)`, sem nenhum callback — um pedido de cancelamento nessa janela só surte efeito quando o Blender UV começa a reportar. Efeito limitado: atraso de até ~100 s, sem publicação parcial (as cópias para `saida/` só acontecem após o retorno do passo). A janela das cópias finais em si (milissegundos, sem nova verificação antes do exportar) tem o mesmo caráter. Não é skip silencioso nem corrupção; é latência de cancelamento. Vira pendência S3, não bloqueio.

### 7. "Forma difere por opções, não por não-determinismo" — CONFIRMADO

| | provac `20261031-225432-provac-orc-s7` | prova COR-05 `20261101-101528-corint-orc-s7` |
|---|---|---|
| Motor / seed / passos / perfil_mmgp | hunyuan-mv-turbo / 7 / 5 / 4 | hunyuan-mv-turbo / 7 / 5 / 4 |
| Qualidade / octree / alvo_tris | null / 256 / 50.000 | prata / 192 / 50.000 |
| Forma (triângulos) | 760.690 | 425.626 |
| Forma SHA-256 (medido por mim) | `9987f90b…` | `19db803f…` |
| Refino | 760.690 → 49.750 | 425.626 → 49.750 |

Mesmo motor, mesma seed, mesmos passos — o que muda é a opção (qualidade null→prata ⇒ octree 256→192), e a forma crua muda junto, com SHAs conferidos nos dois lados e iguais aos citados no REGISTRO. O determinismo da Prova C (mesmas opções ⇒ bytes idênticos) não é contestado por este par, porque as opções não são as mesmas. Precisão: o REGISTRO cita "perfil mmgp 4" como distintivo da prova Prata, mas o provac também registra `perfil_mmgp=4`; o delta distintivo real é `qualidade`/`octree` (S4, D-COR05-4).

### 8. Armadilha documental (`etapas["refino"]["glb"]` → conteúdo colorido) — CONFIRMADO, NÃO BLOQUEIA

- Confirmado: `etapas["refino"]["glb"]` aponta para `…/saida/modelo.glb`, cujo conteúdo após a cor é o GLB colorido (SHA `0f838538…`, medido). Quem ler só esse campo concluirá, errado, que o refino "entregou" o modelo colorido.
- A receita de reconstrução **está documentada** no REGISTRO (entrada COR-05, item 7 + ressalva): o refinado original se lê em `saida/modelo_sem_cor.glb`, e `resultado.glb_sem_cor` registra o caminho. O SHA completo do refinado (`5467f25e900cf9ab43b84ccbaecc4b42d81deab4cfe0887c9a33447769b41d00`) existe e foi conferido por mim — mas **só no manifesto do Drive** (`arquivo_jobs/…/manifesto_sha256.json`: 8 arquivos, 8.266.236 bytes, conferido) e na minha medição; no REGISTRO ele aparece truncado ("5467f25e…") e **não** existe em `etapas["cor"]` nem no `relatorio.json` do job.
- **Julgamento: a falta do campo `glb_refinado_preservado` com SHA em `etapas["cor"]` NÃO bloqueia o fechamento** (D-COR05-3, S4). Motivos: o refinado está preservado em caminho estável, registrado em `resultado`, arquivado com manifesto conferido e re-medido por mim — a reconstrução é possível hoje, sem ambiguidade, por 3 vias independentes. O campo é melhoria documental devida na próxima tranche que tocar o worker, não condição de validade do GLB nem da prova.

### 9. Olho crítico nas 4 prévias da cor vs. frente dourada — D1 RE-CONFIRMADA, SEM DEFEITO NOVO

Método: as 4 `cor/previas/previa_cor_*.png` baixadas e inspecionadas contra `app/testes/dourado/imagens/orc_frente.png` (Orc: pele verde, listras vermelhas de guerra, dreadlocks, pele de lobo no ombro, tanga vermelha central, machado de lâmina única).

O que se vê (4/4 vistas):

- **Silhueta e pose reconhecíveis** (humanóide volumoso, braços ao lado do corpo, pernas afastadas); sem áreas pretas vazias — o `sem_cor 0` após dilatação se confirma visualmente: os escuros são textura escura, não buracos. A dilatação funcionou.
- **TXT (mosaico/"confete") — generalizado, 4/4 vistas:** a superfície inteira é retalhada em fragmentos marrons/pretos/vermelhos/tan; nenhuma região plana de cor (pele, couro, metal) se sustenta. É exatamente a D1 já aberta, não um artefato novo da integração.
- **FACE (frente) — rosto ilegível:** a face sai como mancha escura, sem olhos, presas, pintura vermelha ou dreadlocks legíveis. D1, não defeito novo.
- **Fidelidade de cor (parte da D1):** o verde da pele da referência praticamente não se transfere (a pele sai marrom/tan); o vermelho aparece em retalhos (tanga/faixas) mas sem as listras de guerra legíveis; a pele de lobo é apenas sugerida na perna inferior direita da frente, não no ombro — divergência geometria-vs-arte, o segundo componente declarado da D1.
- **Sem evidência nova de troca esq/dir no Orc** (a S2-3 é suspeita sobre a Besta, fora do alcance desta prova) e sem defeito de geometria novo atribuível à cor (machado/braços são da forma, pré-cor).
- Cobertura numérica coerente com o visual: 211.268 texels UV, só 41.070 diretos (19,4%), 170.198 cegos antes da dilatação (80,56%) — a textura é, em sua maior parte, dilatada, não projetada. Isso *explica* o mosaico; não o absolve, mas o ancora na D1.

**Conclusão do item 9:** a integração pode FECHAR com a D1 aberta (ver "Julgamento explícito" acima). Nenhum defeito visual novo é imputado à COR-05.

### 10. Troca do worker vivo — CONFIRMADA, nenhum job afetado

- Supervisor (`_cache/logs/tarefa_worker.log`): worker antigo (PID 25544, desde 31/10 21:05) "caiu (código 4294967295)" em **01/11 10:13:18** (kill, exit -1); relançamento em **10:14:18**.
- Processo vivo agora: PID **31976**, `CreationDate` 01/11 10:14:18, CPU 232 s (compatível com ter rodado o job de 264 s) — é o worker real (`uv_python pythonw -m oficina3d.worker`), filho do lançador PID 33612 (`-m oficina3d.worker`, CPU ~0, também de 10:14:18), sob o supervisor PID 2016 (`iniciar_worker.py`, desde 31/10 20:20). O `job.json` registra `worker.pid = 31976`, `inicio = 10:15:31` — **o job de prova rodou sob o worker novo, com o código novo**. (O REGISTRO diz 10:14:19; o valor exato medido é 10:14:18 — diferença de 1 s, S4.)
- **Fila vazia no momento da troca:** varredura de todos os `jobs/*/job.json` — zero jobs em estado fora de (concluído, erro, cancelado); nenhum job criado entre 01:13 (`varq-caprileo-s7`, concluído) e o de prova (10:15); o de prova é o job mais recente da fila. **Nenhum job órfão, nenhum job afetado pela reinicialização.** O procedimento do executor (matar com fila vazia, supervisor relançando) está corroborado pelos logs, não apenas afirmado.

## Verificações aritméticas laterais (todas conferem)

- Tempos do job: entrada 3,4 + forma 59,6 + refino 25,3 + cor 175,6 + exportar 0,005 + arquivar 0,4 = 264,305 → `tempo_total_s = 264,3` no `relatorio.json`; o `log.txt`/histórico diz "concluído em 264,1 s" (outro relógio, do início do processamento). Diferença de 0,2 s, S4 (D-COR05-4).
- Cobertura: 41.070 + 170.198 = 211.268 texels; 170.198 / 211.268 = 80,56% ✓.
- UV: ocupação xatlas 0,20152 = ocupação medida no Blender 0,20152 (guarda 0,02, checagem duplicada passou) ✓; texels/face 4,247 em 1024, coerente com a queda de ocupação (T5: 12,94 a 0,614) ✓.
- IoUs do bake: frente 0,7929 / costas 0,7237 / esquerda 0,7885 / direita 0,7827 — todos reproduzidos de `resultado_cor.json` ✓. (Os IoUs 0,76–0,81 citados no REGISTRO são os do *refino*, não do bake — não confundir.)

## Defeitos (numerados, com severidade)

**Escala:** S1 = bloqueia / corrompe / vaza; S2 = degrada função central ou prova; S3 = limitação real, contornável, vira pendência; S4 = documental/cosmético.

- **D-COR05-1 (S3) — Janela sem verificação de cancelamento durante a UV xatlas.** `gerar_uv` (~97,5 s) não emite callback de progresso, logo `_Progresso` não verifica o flag de cancelamento nesse intervalo; o mesmo vale, em milissegundos, para as cópias finais (sem nova verificação antes do exportar). Efeito: latência de cancelamento, sem publicação parcial. *Ação:* emitir progresso (ou verificar o flag) dentro de `gerar_uv` / antes das cópias, na próxima tranche que tocar o passo/worker.
- **D-COR05-2 (S3) — Nenhum job sem-`--cor` sob o worker novo.** Não-regressão sem-cor provada por diff + job pré-integração (item 3), não por job vivo pós-integração. *Ação:* rodar 1 job sem-cor sob o worker atual e registrar o SHA/estado antes de declarar a não-regressão como provada por execução.
- **D-COR05-3 (S4) — Falta `glb_refinado_preservado` com SHA em `etapas["cor"]`.** O SHA completo do refinado só existe no manifesto do Drive; o REGISTRO o cita truncado. Não bloqueia (item 8). *Ação:* incluir o campo no worker na próxima tranche que o tocar.
- **D-COR05-4 (S4) — Divergências numéricas/documentais menores, sem explicação registrada.** (a) 264,1 s vs 264,3 s de tempo total; (b) início do worker 10:14:19 (REGISTRO) vs 10:14:18 (supervisor + processo); (c) vértices 65.274 → 71.195 → 71.289 → 71.336 entre estágios, sem nota; (d) "perfil mmgp 4" citado como distintivo da Prata quando o provac também o tem (o delta é qualidade/octree); (e) ESTADO_ATUAL ainda diz "suíte: 247 testes" (defasado; o correto é 263) e a ressalva do REGISTRO sobre o +2 precisa ser corrigida para a explicação do item 2. *Ação:* corrigir na próxima atualização de docs; nenhum afeta o veredito.
- **D-COR05-5 (RESOLVIDA — não é defeito) — Delta +2 da suíte.** Explicação completa no item 2 (252 da árvore `17462aa` + 2 do `aa2758c` + 9 da COR-05 = 263). A pendência declarada pelo executor está fechada por este relatório.

## Pendências pré-existentes que seguem ABERTAS (não são desta tranche, não bloqueiam)

- **D1** (fidelidade de detalhe do Orc — mosaico + rosto ilegível) — ABERTA, re-confirmada nas 4 vistas.
- **S2-3** (suspeita de troca esq/dir nas imagens da Besta) — ABERTA; fora do alcance da prova com Orc; o bake usa as etiquetas do job como estão.
- **S3-2** (sem_cor 0 sem máscara entregue), **S4-2** (`resultado_cor.json` nativo do bake não entregue — o relatório do job o embute em `etapas["cor"]`) — ABERTAS.
- **Exposição web/MCP da opção `cor`** — pendência de produto declarada (CLI + worker apenas nesta tranche).
- **Portão final MET-03** (três Críticos sênior, baterias diferentes) — só no fim de TODAS as frentes, não agora.

## Verificação nova para a próxima bateria (escalada APR-01)

Além desta bateria (que já acrescentou o parse binário próprio do GLB, a reconciliação commit-a-commit do delta da suíte e a prova de não-regressão por diff + job pré-integração), a próxima bateria do Crítico deve acrescentar, como verificação obrigatória e inédita:

> **Reexecução determinística ponta a ponta da etapa `cor`:** rodar novamente, via fila, um job com as *mesmas* opções da prova (`--qualidade prata --seed 7 --cor`, mesmas 4 vistas) e comparar byte a byte os SHAs de `cor/textura.png`, `cor/modelo_cor.glb` e `saida/modelo.glb` com os desta prova (`ebd744a9…`, `0f838538…`). A Prova C provou determinismo da *forma*; o determinismo da *cor* (xatlas + bake) nunca foi provado por reexecução — e uma etapa que não reproduz seus bytes não pode ser chamada de pronta, por mais que a primeira execução tenha sido válida. Se os SHAs divergirem, a divergência vira defeito S2 da próxima tranche, com decomposição por sub-passo (UV vs bake).

Verificações secundárias escaladas para a mesma próxima bateria (não substituem a principal): (i) job sem-`--cor` sob o worker novo (fecha D-COR05-2 por execução); (ii) job com `--cor` e sem vista canônica enviado pela fila real (deve terminar em `erro` na etapa `cor`, provando o item 6 por execução e não só por leitura); (iii) validação do GLB final por um validador glTF independente (ex.: `gltf-validator`), além do parse próprio.

## Lastro

- Job: `Oficina3D/jobs/20261101-101528-corint-orc-s7/` (`job.json`, `saida/relatorio.json`, `cor/resultado_cor.json`, `cor/resultado_uv_xatlas.json`, `log.txt`).
- Suíte: `Oficina3D/jobs_teste/cor_integracao/suite.log` + `count_tests.py` (discovery própria); suíte anterior: `Oficina3D/jobs_teste/cor_d2d7/suite.log` (252, 01/11 08:31:30).
- Arquivo no Drive: `Oficina3D_v2/arquivo_jobs/20261101-101528-corint-orc-s7/manifesto_sha256.json` (8 arquivos, 8.266.236 bytes, conferido).
- Parser próprio do Crítico: `/tmp/critico-cor05/parse_glb.py` (máquina do Muse; não commitado, não faz parte do projeto).
- Este relatório: `app/docs/CRITICO-cor-integracao-relatorio.md` no PC (não commitado, por ordem da tarefa).
