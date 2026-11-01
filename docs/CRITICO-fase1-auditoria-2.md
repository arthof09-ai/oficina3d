# CRÍTICO — Auditoria independente nº 2 da Oficina3D (rodada final da Fase 1)

- **Data/hora da auditoria:** 2026-10-31, 22:44–23:02 (America/Sao_Paulo, relógio do PCDANASA)
- **Auditor:** Agente Crítico oficial do projeto (EXEC-02), atuando de forma independente
- **Objeto:** as alegações do construtor (Muse) de que resolveu P1–P6 da auditoria nº 1 e concluiu as rodadas R2, R3 e R4 — auditadas contra a definição de "pronta" de `docs\REVISAO_E_ROTEIRO.md` (8 itens)
- **Método:** evidência própria, gerada pelo auditor ao vivo no PCDANASA: suíte executada pelo auditor no interpretador de produção, 2 jobs reais submetidos pelo auditor (triposr + hunyuan-mini-turbo), hashes SHA-256 recalculados pelo auditor, cliente MCP real escrito pelo auditor, histórico git dissecado commit a commit. Nada foi aceito a partir de relatórios de terceiros.
- **Regra cumprida:** o Crítico não corrigiu nada; julga e aponta. Correções são do construtor.

---

## VEREDITO GERAL

**NÃO PRONTA** — pela definição de "pronta" do próprio projeto (os 8 itens verdade ao mesmo tempo). O núcleo técnico está **provado com evidência minha**: suíte verde na régua certa, 5 motores com GLB real, arquivo no Drive byte-idêntico, repositório íntegro e idêntico ao GitHub, worker/web/MCP no ar. Mas três coisas impedem o carimbo:

1. **Item 3 (Prova C) segue BLOQUEADO** — as imagens douradas não existem nesta máquina nem no Drive (atestado por mim, item 7 abaixo). Sem elas, a bateria de aceite da Fase 1 não pode rodar. Bloqueio de insumo externo (Mestre), não de engenharia.
2. **Defeito novo GRAVE (N1):** o commit da R2 **apagou 19 dos 24 testes do motor** ao "criar" um arquivo que já existia — e o REGISTRO descreveu a reescrita como criação. A suíte real tem **180 testes, não 199** como os documentos ainda afirmam.
3. **Item 7 (documentação sem deriva) não provado:** o ESTADO_ATUAL parou às ~20:20 e não conhece R2, R3, R4 nem DONO-02.

Se o Mestre aceitar a Prova C como bloqueio externo pendente, o estado de engenharia é "pronta com ressalvas N1–N3". Pelo texto da definição, o veredito formal é NÃO PRONTA.

| Item da definição de "pronta" | Veredito |
|---|---|
| 1. Suíte verde na régua certa (.venv_app) | ✅ PROVADO (180 testes — ver N1) |
| 2. 5 motores com prova viva | ✅ PROVADO |
| 3. Prova C (bateria dourada) | ⛔ BLOQUEADO (insumo ausente) |
| 4. Paridade das portas (CLI/web/MCP) | ✅ PROVADO COM RESSALVA (N2) |
| 5. Arquivo no Drive provado | ✅ PROVADO |
| 6. Repositório completo / instalação do zero | ✅ PROVADO (R4 atestada por artefatos — ver limite) |
| 7. Documentação sem deriva | ❌ NÃO PROVADO (N3 + número de testes) |
| 8. Crítico aprovou a rodada final | ❌ NÃO PROVADO (consequência deste veredito) |

---

## ITEM 1 — Suíte verde na régua certa ✅ PROVADO (com o alerta N1)

Executada por mim, via tarefa agendada, no interpretador de produção
(`BASE\.venv_app\Scripts\python.exe -m unittest discover -s testes`, cwd=`app`, env do projeto):

- **Ran 180 tests in 18.459s — OK (skipped=1), EXIT=0.** Início 22:45:09, fim 22:45:28 (log `_cache\logs\critico2_suite.txt`).
- O skip único é o desenhado: registro do servidor MCP fora do `.venv_mcp` (lá ele roda).
- Os testes de trava que falhavam na auditoria nº 1 passam: `test_travas.py` tem 18 testes, todos dentro da suíte verde; o log da suíte mostra inclusive as mensagens de trava órfã sendo assumida por outro PID (o mecanismo exercitado de verdade).
- **Porém o número oficial está errado:** REGISTRO, ESTADO_ATUAL e REVISAO afirmam **199 testes**. A contagem real, por arquivo, medida por mim com o loader do unittest: arquivar 14, cli 11, config 15, entrada 13, job 36, mcp 7, motores 5, refino 30, saude 15, travas 18, web 7, worker 9 = **180**. A divergência é o defeito N1.

## ITEM 2 — Os 5 motores com prova viva ✅ PROVADO

- `cli motores` executado por mim: **os 5 motores "sim"** (disponível), exit=0.
- Jobs citados no REGISTRO, conferidos por mim em disco (job.json + GLB na saída), todos `concluido`: fumaca-mv-turbo (mv-turbo), fumaca-arquivo-2 (triposr), prova-mini-full-2 (hunyuan-mini, GLB 1.134 KB), prova-mv-full (hunyuan-mv, 1.096 KB), prova-refino, prova-mini-turbo (1.108 KB), prova-opencv410. O primeiro mini-full (`20261031-204609`) está `estado=erro` sem GLB — a falha da R2 está honestamente preservada em disco.
- **Jobs meus, submetidos nesta auditoria** pela CLI, processados pelo worker sem intervenção: `20261031-224729-critico2-triposr` → concluído 100%, GLB 1.099 KB; `20261031-224730-critico2-turbo` (hunyuan-mini-turbo) → concluído 100%, GLB 1.108 KB.
- Validação de GLB por mim (trimesh no .venv_app): ambos abrem como Scene; o do turbo tem **1 geometria, 49.750 triângulos, 26.098 vértices** — malha real, dentro do teto de 50 mil.

## ITEM 3 — Prova C (bateria dourada) ⛔ BLOQUEADO

Atesto a ausência nos locais esperados, sem inventar substitutos:

- `app\testes\dourado` **não existe**.
- Drive `Oficina3D_v2\referencias`: existe, **0 arquivos**. `Oficina3D_v2\aprovados`: existe, **0 arquivos**.
- Logo Orc/Capríleo/Besta em tamanho útil não estão acessíveis nesta máquina. O bloqueio é o P7 da auditoria nº 1, ainda aberto. A bateria não pode ser aprovada nem reprovada: está bloqueada por insumo do Mestre.

## ITEM 4 — Paridade das portas ✅ PROVADO COM RESSALVA (N2)

- Tarefas `Oficina3D_Worker` e `Oficina3D_Web`: ambas **Running**. `GET http://127.0.0.1:8765/api/saude` → **HTTP 200** com dados vivos (medido 22:45:09, GPU RTX 4060, disco 44,66 GB livres).
- Cantos da web conferidos por mim: `GET /` → 200; job inexistente → **404**; `POST /api/jobs` sem o cabeçalho anti-CSRF → **403** (o porteiro funciona como desenhado).
- **Cliente MCP real, escrito por mim** (stdio, `.venv_mcp`, configuração do `.mcp.json` da BASE): servidor responde com **9 ferramentas** (listar_motores, submeter_job, status_job, listar_jobs, obter_resultado, cancelar_job, iniciar_worker, saude, baixar_resultado_base64); `listar_motores` e `listar_jobs` respondem dados reais — inclusive os meus 2 jobs, com os mesmos ids/estados da API web no mesmo instante.
- CLI: meus 2 jobs entraram pela CLI e concluíram pelo worker — a porta CLI está provada de ponta a ponta. A porta "pasta" não foi exercitada separadamente (usa o mesmo núcleo `job.json` das demais).
- **Ressalva (N2):** a paridade de *conteúdo* do catálogo de motores está quebrada neste momento — a web serve textos antigos de licença ("RF-03: só rascunho") que o MCP/CLI não servem mais. Detalhes em N2. Ids, estados e disponibilidade coincidem; o texto jurídico, não.

## ITEM 5 — Arquivo no Drive provado ✅ PROVADO

Prova de ida e volta com hashes calculados por mim (job `20261031-200949-fumaca-arquivo-2`):

- SHA-256 do GLB local: `AB877E778A6FF30EB34A686E32F2F42128B40D878E052B15ED09B3E51362F4DC`
- SHA-256 da cópia em `arquivo_jobs` no Drive: **idêntico**.
- `manifesto_sha256.json` do arquivo: `saida/modelo.glb`, 1.125.516 bytes, sha256 `ab877e77...f4dc` — **confere com os dois**.
- Cópia byte-idêntica ⇒ um job restaurado de lá abre igual (identidade de bytes).
- Escala: **16 jobs** arquivados em `arquivo_jobs`; e os **meus 2 jobs desta auditoria também foram arquivados** (pastas presentes no Drive) — o arquivamento não é um caso ensaiado, é o comportamento corrente (P5 resolvido em produção).

## ITEM 6 — Repositório completo ✅ PROVADO

- `git status`: árvore **limpa**; HEAD local = `e2f44a11249d04c17551cf639f922395c6c9d897`.
- API do GitHub consultada por mim: `main` remoto = **o mesmo hash** — paridade local×remoto total (P3 morto). Repositório público, como decidido (GIT-02).
- **GIT-01 conferido:** `git ls-files oficina3d/motores` → os 4 arquivos (`__init__.py`, `base.py`, `_runner_hunyuan.py`, `_runner_triposr.py`) versionados. Como local e remoto são o mesmo commit, a árvore do GitHub é idêntica por construção.
- **Correção R4 conferida no fonte:** `instalacao\requisitos\triposr.txt` fixa `opencv-python-headless==4.10.0.84` (com o motivo escrito) e `numpy==1.26.4`; o lock `requirements_venv_triposr.lock` é coerente (mesmas versões). O defeito original (lock insatisfazível) não existe mais no repositório.
- **R4 (instalação do zero):** a BASE de teste foi apagada como o REGISTRO declara (conferi: `Oficina3D_R4` não existe; C: com ~44,7 GB livres). O log do job da base limpa (`_cache\logs\r4_job.txt`, 4.252 B) existe na BASE principal. **Limite declarado:** eu não reexecutei a instalação do zero (custaria ~21 GB e ~25 min para repetir uma prova cujo defeito ela deveria achar — e achou — já foi corrigido e verificado no fonte); atesto a R4 pelos artefatos e pela correção verificada, não por reexecução.

## ITEM 7 — Documentação sem deriva ❌ NÃO PROVADO

- ✅ O que confere: USO sem nenhuma ocorrência de `servidor_mcp` (0 — a correção do nome do módulo é real); DECISOES contém a linha **DONO-02** (31/10, referências preservadas, exigência = independência); REGISTRO bate com o disco em todos os jobs que amostrei (incl. a falha do mini-full e `retomadas=1` do órfão da R3).
- ❌ **ESTADO_ATUAL está parado:** cabeçalho "Atualizado em 31/10/2026, ~20:20"; **zero** ocorrências de R2, R3, R4 ou DONO no documento; a seção PENDENTE ainda lista como pendentes a dívida P6 (paga) e os itens 4/5 (concluídos), e "Próximos passos" aponta trabalho já feito. Quem retomar pelo ESTADO_ATUAL recebe um retrato de ~1,5 h atrás — exatamente a deriva que o item 7 proíbe.
- ❌ O número "199 testes" persiste em ESTADO_ATUAL e REVISAO_E_ROTEIRO — falso no HEAD (180), ver N1.

## ITEM 8 — Aprovação do Crítico ❌ NÃO PROVADO

Esta auditoria é a rodada final prevista. Pelos itens 3 (bloqueado) e 7 (não provado) e pelo defeito N1, o Crítico **não aprova** a Oficina como "pronta" nesta rodada. Aprova, com evidência, o núcleo técnico (itens 1, 2, 4, 5, 6).

---

## STATUS DAS RESSALVAS P1–P8 DA AUDITORIA Nº 1

| item | status nesta auditoria | evidência (minha) |
|---|---|---|
| P1 (grave) suíte vermelha no venv / PID do trampolim | ✅ RESOLVIDO | Suíte 180/180 verde no `.venv_app`; travas exercitadas; drill vivo da R3 conferido em disco (órfão retomado e concluído) |
| P2 régua medida no interpretador errado | ✅ RESOLVIDO | A régua oficial é o `.venv_app`; foi nela que medi |
| P3 github.com inalcançável / push pendente | ✅ RESOLVIDO | HEAD local == GitHub (`e2f44a1`), árvore limpa, API respondendo |
| P4 restart do worker sem causa no log | ✅ RESOLVIDO | Causa registrada no REGISTRO **e** o lançador agora instrumenta: log mostra `21:04:34 worker caiu (código 4294967295); queda 1 na última hora` e o reinício às 21:05:04 (drill da R3) |
| P5 job concluído não arquivava | ✅ RESOLVIDO | 16 jobs em `arquivo_jobs` + hashes conferidos + meus 2 jobs arquivados |
| P6 dívida de testes + LISTA | ⚠️ PAGO COM R
...[truncated 4093 chars]