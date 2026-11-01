# Crítico sênior — D-COR05: pendências da integração COR-05

- **Tranche julgada:** D-COR05 (pendências D-COR05-1/2/3/4 da integração COR-05).
- **Commit julgado:** `0449f9c` ("D-COR05: janela de cancelamento na UV, campo glb_refinado_preservado, testes (jobs de prova pendentes)"), diff contra `61c3a37` lido linha a linha. `main == origin/main == 0449f9cd98a6ee136eb1801b48dd4ce6e11a242a`, árvore limpa (`git status` vazio).
- **Jobs de prova (fila real, worker novo PID 33284, início 2026-11-01T11:06:42-03:00):**
  - `20261101-110658-dc05-semcor-orc-s7` (sem `--cor`);
  - `20261101-110659-dc05-cor-det-orc-s7` (reexecução determinística da prova COR-05);
  - `20261101-110659-dc05-cor-semvista-besta` (`--cor` sem vista canônica).
- **Prova de referência:** `20261101-101528-corint-orc-s7` (worker antigo PID 31976).
- **Método:** nenhum número do executor foi aceito sem re-medição. Diff do commit; reexecução própria do módulo `test_cor_passo`; discovery própria com contagem por módulo; suíte completa reexecutada por mim em duas metades; parse binário próprio dos GLBs (`struct` + JSON, sem trimesh, sem `costura.py`); hashes refeitos na minha máquina pós-scp; comparação byte a byte de TODOS os artefatos do job de determinismo contra a prova, com decomposição de chunks PNG e comparação pixel a pixel; leitura de `job.json`, `relatorio.json`/`relatorio_parcial.json`, `log.txt` e `resultado_*.json` dos 3 jobs; código do worker/passo lido, não resumido.
- **Data do veredito:** 01/11/2026, ~11:20–11:40 (horário de Brasília).

## VEREDITO: D-COR05 FECHADA — D1 segue ABERTA e ortogonal

Os quatro itens fecham, a reexecução determinística reproduz a prova, e a verificação secundária falha exatamente como o desenho manda. **Nenhum defeito S1/S2/S3 novo.** As ressalvas abaixo são S4 e não bloqueiam.

**Guarda explícita (leitura obrigatória):** este FECHADO fecha as pendências de integração da COR-05. **A D1 (fidelidade de detalhe do Orc) segue ABERTA** — a reexecução reproduz byte a byte o mesmo bake da prova (IoUs 0,7237–0,7929, mesmo caráter em mosaico), ou seja, a D1 não melhorou nem piorou; qualquer leitura de "cor pronta/fiel" a partir deste veredito seria falsa.

## Julgamento por item

### D-COR05-1 (janela de cancelamento na UV) — FECHADO

- Diff confirma o desenho: `uv_xatlas.gerar_uv` ganhou `progresso` com chamadas em 0/20/30/80/90/100; `cor/passo.py` mapeia para a janela 5–30 pela fórmula `5 + (pct*25)//100`; `worker.py` re-checa o cancelamento após o retorno do passo e ANTES das cópias finais para `saida/`.
- Aritmética conferida contra o `log.txt` do job de determinismo, linha por linha: 0→5% ("gerando UV xatlas"), 0→5% ("carregando GLB"), 20→10% ("GLB carregado"), 30→12% ("parametrizando"), 80→25% ("parametrização pronta"), 90→27% ("métricas prontas"), 100→30% (".npz gravado"), 30% ("UV pronta, ocupação 0.20152"). Exatamente as 8 linhas afirmadas, nas horas afirmadas.
- Janela residual medida: 12% às 11:09:01 → 25% às 11:10:25 = **84 s** de chamada nativa não interrompível; UV total 11:09:01→11:10:38 = 97 s. A limitação declarada é honesta quanto à natureza (não interrompível no meio; o cancelamento aborta logo após o retorno, antes de gravar o `.npz` e antes das cópias finais). Ressalva S4: o docstring diz "chamada nativa (~97 s)" — 97 s é o `gerar_uv` total, não a chamada nativa (84 s). Corrigir o número no docstring numa próxima passada pelo arquivo; o fato funcional (janela residual = chamada nativa) está correto.
- Testes reexecutados por mim no `.venv_app`: `test_cor_passo` = **13 testes, OK** (9 antigos + 3 `TestGerarUvProgresso` + 1 `TestSha256Worker`), incluindo "progresso que levanta em >=80 não grava .npz" e monotonicidade 0/30/80/100.
- Observação S4 (não é defeito): o cancelamento real em job vivo não foi exercido nesta tranche (o teste simula a exceção; o `_Progresso` que lê o disco é código pré-existente e inalterado). O mecanismo está provado por código + teste unitário; um teste vivo de cancelamento fica como sugestão, não como pendência bloqueadora.

### D-COR05-2 (job sem `--cor` sob o worker novo) — FECHADO

- Job `20261101-110658-dc05-semcor-orc-s7`: `estado=concluido`, `worker.pid=33284`, `opcoes.cor=false`, `tempo_total_s=58,5` (afirmado 58,5 s — exato).
- `relatorio.json`: etapas = entrada, forma, refino, arquivar (sem `cor`); `job.json: resultado` sem `glb_sem_cor`, com as 5 prévias do refino e sem prévias da cor. A não-regressão, antes provada só por diff + job pré-integração, agora está provada por execução sob o worker novo.

### D-COR05-3 (campo `glb_refinado_preservado`) — FECHADO

- No `relatorio.json` do job de determinismo, `etapas["cor"]["glb_refinado_preservado"] = {"arquivo": "saida/modelo_sem_cor.glb", "sha256": "5467f25e900cf9ab43b84ccbaecc4b42d81deab4cfe0887c9a33447769b41d00"}`.
- SHA re-medido por mim no arquivo baixado: **idêntico** ao campo. Contraste que prova a novidade: o `relatorio.json` da prova COR-05 (worker antigo) NÃO tem o campo — ele só existe a partir do worker da D-COR05.

### D-COR05-4 (divergências documentais) — FECHADO, item a item

- **(a) 264,1 vs 264,3 — FECHADO.** Re-medido na prova: `log.txt` marca "=== concluído em 264.1 s" (relógio do processamento, na linha do exportar, antes do arquivar); `relatorio.json: tempos_s` = entrada 3,4 + forma 59,6 + refino 25,3 + cor 175,6 + exportar 0,005 + arquivar 0,4 = **264,305 → tempo_total_s 264,3**. Dois relógios, dois pontos de medição, ambos corretos. O mesmo padrão se repete no job de determinismo (soma 232,806 → total 232,8).
- **(b) Início do worker COR-05 — FECHADO.** `job.json` da prova: `worker.pid=31976`, `worker.criado` (filetime) = 2026-11-01T13:14:18.834 UTC = **10:14:18-03:00**, não 10:14:19. Exato.
- **(c) Vértices 65.274→71.195→71.289→71.336 — FECHADO, com recontagem própria.** Parser binário próprio (sem trimesh, sem `costura.py`):

  | Artefato (job de determinismo) | Vértices | Posições únicas | Faces |
  |---|---|---|---|
  | `saida/modelo_sem_cor.glb` (refino) | 65.274 | 23.771 | 49.750 |
  | `cor/uv.npz` (`uvs`) | 71.195 | — | 49.750 |
  | `cor/modelo_uv.glb` (UV aplicada) | 71.289 | 23.771 | 49.750 |
  | `saida/modelo.glb` / `cor/modelo_cor.glb` (final) | 71.336 | 23.771 | 49.750 |

  Posições únicas idênticas (23.771) nos 3 GLBs e faces constantes (49.750): a geometria não mudou, só a duplicação em costuras. Deltas: +5.921 (costuras do xatlas), +94 (round-trip Blender da UV), +47 (export do bake). Explicação completa e medida.
- **(d) "perfil mmgp 4" — FECHADO.** Re-medido no job provac (`20261031-225432-provac-orc-s7`): `perfil_mmgp=4`, `octree=256`, sem chave `qualidade`. No job de determinismo: `perfil_mmgp=4`, `octree=192`, `qualidade=prata`. O mmgp 4 não distingue a Prata; o delta distintivo é qualidade/octree (null/256 → prata/192). Exato.
- **(e) ESTADO com suíte 263 — FECHADO.** `docs/ESTADO_ATUAL.md`, linha 14: "Suite de testes: 263 testes OK ... (baseline 254 pre-tranche + 9 novos da COR-05), skipped=1". A correção 247→263 da tranche anterior está no arquivo. **Acompanhamento (não é defeito desta tranche):** após a D-COR05 o número correto passa a ser 267 (ver seção da suíte); o ESTADO deve subir 263→267 na atualização de fechamento do executor, junto do espelho no Drive deste relatório.

### Verificação principal (reexecução determinística da etapa cor) — PASSOU

Job `20261101-110659-dc05-cor-det-orc-s7`: `concluido`, `worker.pid=33284`, `tempo_total_s=232,8` (afirmado 232,8 s — exato), mesmas opções da prova (Orc, 4 vistas douradas, prata, seed 7, `--cor`).

- **Byte-idênticos à prova** (`cmp` limpo + SHA-256 refeito): `cor/textura.png` (**EBD744A9…213D2139D**), `cor/modelo_cor.glb` e `saida/modelo.glb` (**0F838538…B57E9BF48C**), `saida/modelo_sem_cor.glb` (**5467F25E…69B41D00**), `cor/uv.npz` (SHA `42097d3b8dcbe3d4…`) e `cor/modelo_uv.glb` (SHA `9a5c1203bb41ddf8…`).
- **Prévias — pixel-idênticas, byte-diferentes só em metadado (achado da escalada, não defeito):** as 4 prévias da cor e as 5 do refino têm o mesmo tamanho em bytes mas SHA diferente. Decomposição dos chunks PNG: `IDAT` **idêntico** em todos os casos; a única diferença está nos chunks `tEXt` do Blender — `Date` (10:19:54 na prova vs 11:11:55 no determinismo) e `RenderTime` (0.45 vs 0.50 s). Decodificação pixel a pixel das 9 prévias: **0 pixels diferentes em todas** (cada uma com 512.000 pixels); `IDAT` idêntico nas 9. Conclusão: o determinismo é total no conteúdo; comparações futuras de prévias do Blender devem comparar `IDAT`/pixels, não bytes brutos — lição a registrar no diário.
- **Métricas idênticas à prova** (`resultado_cor.json` vs prova: só mudam caminhos e `tempo_s` 61,61 vs 61,26; `resultado_uv_xatlas.json`: só `tempo_s` 14,48 vs 14,97): ocupação 0,20152 (xatlas = Blender), 8.844 ilhas, distorção 0,0671, IoUs frente 0,7929 / costas 0,7237 / esquerda 0,7885 / direita 0,7827, cobertura 211.268 texels (41.070 diretos, 170.198 cegos = 80,56%, 0 sem cor após dilatação), 49.750 triângulos, `vertices=71.289` no resultado do passo (o 71.336 do GLB final vem do export do bake — ver item (c)).
- **Linhas de progresso UV** presentes no `log.txt` do determinismo (e ausentes na prova, que só tinha 5%→30%): 5% gerando, 5% carregando, 10% carregado, 12% parametrizando, 25% pronta após 84 s, 27% métricas, 30% `.npz`, 30% pronta.

### Verificação secundária (ii) (job `--cor` sem vista canônica) — PASSOU

Job `20261101-110659-dc05-cor-semvista-besta` (Besta `topo_v2`, vista "cima", prata, seed 7, `--cor`, `worker.pid=33284`): `estado=erro`, `etapa=cor`, erro exato `cor: etapa cor sem nenhuma vista canonica (frente/costas/esquerda/direita) nas imagens do job` (também no traceback do `log.txt`: `ErroEtapa` na linha do worker que envolve o `ValueError` do passo). Sem pasta `cor/`, sem `modelo_cor`, sem `relatorio.json` final — só `relatorio_parcial.json` (etapas entrada/forma/refino; tempos 12,5/34,5/7,6) e `resultado=null`.

- **Sobre o `saida/modelo.glb` presente no job em erro — comportamento pré-existente documentado, não vazamento da cor.** Verificado no código: o refino grava ele mesmo `saida/modelo.glb` (o `refinar` recebe `saida/` como pasta de saída; o export do Blender difere do `refino/limpa.glb` — SHAs `666BD656…` vs `59531B08…` no job sem-vista). A cor nunca rodou, logo nada da cor foi publicado. Ressalva S4: num job em erro, o `saida/modelo.glb` do refino é indistinguível por nome de um final; só `job.json: estado` + `relatorio_parcial.json` vs `relatorio.json` distinguem. Vale um registro no REGISTRO (ou uma nota futura no worker); não é defeito desta tranche e não muda o veredito.

## Escalada APR-01 (bateria mais rigorosa que a anterior)

Verificações novas desta bateria, ausentes na anterior:

1. **Comparação byte a byte de TODOS os artefatos do determinismo contra a prova** (não só textura/modelo): inclui `uv.npz`, `modelo_uv.glb` e as 9 prévias, com decomposição de chunks PNG e comparação pixel a pixel — foi ela que explicou a divergência de bytes das prévias (metadado `tEXt` do Blender, não conteúdo).
2. **Proveniência do worker nos 3 jobs + fila vazia ao fim:** `job.json: worker.pid=33284` nos 3 jobs (criado 11:06:42-03:00, mesmo filetime nos 3); último job modificado às 11:12:53; nenhum job novo criado por esta auditoria (a auditoria não criou jobs, não commitou e não tocou em nenhum arquivo fora deste relatório).
3. **Tentativa do validador glTF independente (`gltf-validator`):** buscadas as fontes oficiais (KhronosGroup/glTF-Validator). O validador é distribuído via npm (`npm install gltf-validator`) / build Dart a partir do fonte — **nenhum binário standalone oficial para Windows foi localizado nas releases**; por isso não foi instalado nem executado. Instalar pacotes no PC do cunhado extrapolaria o escopo desta auditoria (só este relatório é escrito). **Não bloqueia:** a validação estrutural está coberta pelo parser binário próprio (containers, acessores, índices, materiais/textura) e pela cadeia Blender (que importou e re-exportou o GLB). A pendência do validador independente segue aberta como sugestão, não como bloqueio.
4. **Recontagem independente da cadeia de vértices incluindo o `.npz`** (uvs 71.195 medidos no arquivo, não citados do relatório do passo).

## Suíte de testes — 267 OK, reconciliada por mim

- Executor: `jobs_teste/cor_dc05/suite.log` → `Ran 267 tests, OK (skipped=1)`.
- Minha discovery própria (`.venv_app`, `TestLoader.discover` + carga por módulo): **TOTAL 267**; por módulo, idêntica à bateria anterior exceto `test_cor_passo` 9→13 (+4: 3 de progresso UV + 1 de SHA). Soma: 14+11+15+22+7+13+13+36+7+29+14+30+15+18+7+7+9 = 267. **263+4=267, reconciliação exata.**
- Minha reexecução: módulo `test_cor_passo` = 13 OK; metade A (8 módulos) = **131 OK**; metade B (9 módulos) = **136 OK (skipped=1)**. 131+136 = 267. O skipped=1 é o mesmo das suítes anteriores (em `test_motores`/travas, com as mensagens habituais de trava assumida — comportamento pré-existente dos testes, não novidade).
- Nota de operação: a primeira tentativa de suíte completa em segundo plano no PC morreu sem saída (logs vazios); a verificação foi refeita nas duas metades acima, dentro do limite das sessões SSH. Os logs/rascunhos dessa auditoria (`critico_conta.py`, `critico_dc05_*.log`) foram removidos do PC ao fim, deixando a árvore como encontrada, exceto este relatório.

## Defeitos novos e pendências

**Nenhum defeito S1/S2/S3.** Ressalvas S4 (não bloqueiam):

- **S4-1:** docstring de `gerar_uv` diz "chamada nativa (~97 s)"; medido: nativa 84 s, total 97 s. Corrigir o número numa próxima passada pelo arquivo.
- **S4-2:** `saida/modelo.glb` do refino existe também em jobs em erro (pré-existente; ver seção secundária). Documentar no REGISTRO.
- **S4-3:** cancelamento real em job vivo não exercido (mecanismo provado por código + teste unitário).
- **S4-4:** validador glTF independente segue pendente (tentativa registrada acima; não bloqueia).

**Pendências que ficam (não são defeitos desta tranche):**

- **D1 (fidelidade de detalhe do Orc) — ABERTA e ortogonal**, como acima.
- **T2 (cor de vértice) — próximo passo**, rede de segurança da Etapa COR, conforme o roteiro.
- **Exposição web/MCP da opção `cor`** — pendente desde a COR-05 (CLI + worker apenas).
- S2-3 (troca esq/dir nas imagens da Besta), S3-2 (sem_cor 0 sem máscara entregue), S4-2 (resultado do bake nativo) — herdadas, inalteradas por esta tranche.
- Fechamento documental do executor: ESTADO 263→267, espelho no Drive deste relatório (com SHA conferido), e registro da lição das prévias (comparar `IDAT`/pixels, não bytes brutos) no diário do `APRENDIZADO_E_FLUXO.md`.

## Arquivos desta auditoria

- Este relatório: `app/docs/CRITICO-dc05-relatorio.md` (PC; SHA-256 conferido após o upload — ver abaixo).
- Rascunhos da auditoria na minha máquina (não no PC, não entregues ao usuário): `~/workspace/dc05-audit/` (artefatos baixados, scripts de contagem e de verificação).
