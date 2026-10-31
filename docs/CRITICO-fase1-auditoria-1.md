# CRÍTICO — Auditoria independente nº 1 da Fase 1 da Oficina3D

- **Data/hora da auditoria:** 2026-10-31, 19:46–20:00 (America/Sao_Paulo, relógio do PCDANASA)
- **Auditor:** Agente Crítico oficial do projeto (EXEC-02), atuando de forma independente
- **Objeto:** tudo o que o agente principal (Muse) executou/registrou na Fase 1, itens 1–2, mais worker (item 4 parcial)
- **Método:** evidência própria, colhida ao vivo no PCDANASA via SSH — imports executados pelo auditor, hashes recalculados pelo auditor, suíte executada pelo auditor em DOIS interpretadores. Nada foi aceito a partir de relatórios de terceiros.
- **Regra cumprida:** o Crítico não corrigiu nada; julga e aponta. Correções são do agente principal.

---

## VEREDITO GERAL

**APROVADO COM RESSALVAS GRAVES.** A instalação (itens 1–2) é real, íntegra e conferida byte a byte na amostra — nisso o relato do agente principal é exato. Porém a auditoria encontrou um **defeito estrutural que o relato não viu**: a suíte de testes **não** é verde no interpretador de produção (`.venv_app`): há **2 falhas reais** nos testes de trava entre processos, com causa raiz provada em experimento controlado (shim de PID do venv criado pelo uv). O checkpoint "152 testes OK" só é verdade no Python 3.12 do sistema, que **não** é o interpretador que o worker usa.

| Item | Veredito |
|---|---|
| 1. Venvs importam + versões × locks | ✅ APROVADO |
| 2. Modelos: tamanho + SHA-256 × manifesto (amostra de 5/13, incl. os 2 maiores) | ✅ APROVADO |
| 3. Motores nos commits fixos + patch do TripoSR | ✅ APROVADO |
| 4. Tarefa Oficina3D_Worker + worker vivo | ✅ APROVADO (com observação O1) |
| 5. Suíte de testes | ⚠️ REPROVADO PARCIAL — verde no interpretador errado; 2 falhas no de produção |
| 6. Rede/GitHub (push) | ❌ REPROVADO (ambiente) — github.com inalcançável do PC; commits seguros localmente |

---

## ITEM 1 — Venvs: imports e versões × locks ✅ APROVADO

Executado pelo auditor, um import real em cada venv (não o teste do instalador):

- **`.venv_app`** (cwd neutro): `import torch, transformers, diffusers, mmgp, trimesh, pymeshlab, fastapi, rembg, huggingface_hub` → **IMPORT OK**; torch **2.5.1+cu124**; `torch.cuda.is_available()` = **True**; GPU detectada: **NVIDIA GeForce RTX 4060**; transformers **4.49.0**; diffusers **0.39.0**.
- **`.venv_triposr`** (cwd = motores\TripoSR): `import torch, torchmcubes, transformers, trimesh, onnxruntime, moderngl, xatlas; from tsr.system import TSR` → **IMPORT OK**; torch 2.5.1+cu124; CUDA True; transformers **4.35.0**; `torchmcubes.__file__` = `app\instalacao\compat\torchmcubes\__init__.py` (o shim do projeto, como desenhado — a extensão compilada que a NVIDIA/ambiente não fornece foi substituída pela compatibilidade do projeto, e isso está explícito e testado).
- **`.venv_mcp`**: `from mcp.server.mcpserver import MCPServer` → **IMPORT OK mcp 2.3.0**; psutil 7.2.2.

**Cruzamento com os locks** (`instalacao\requirements_*.lock`): torch==2.5.1+cu124, torchvision==0.20.1+cu124, transformers==4.49.0 (app) / 4.35.0 (triposr), diffusers==0.39.0, mcp==2.3.0 — **todos idênticos ao instalado**. O lock do app contém `setuptools==84.2.1` e `wheel==0.48.0`, confirmando que a correção do defeito encontrado na instalação foi incorporada ao lock (e, conforme o REGISTRO, ao `requisitos\app.txt`).

## ITEM 2 — Modelos × manifesto (amostra) ✅ APROVADO

Amostra de **5 dos 13** arquivos (38% dos arquivos; **10,61 dos 11,42 GB = 93% dos bytes**), incluindo obrigatoriamente os 2 maiores. Tamanho e SHA-256 recalculados pelo auditor no PC:

| Arquivo | Bytes (manifesto = medido) | SHA-256 | Resultado |
|---|---|---|---|
| hy-mv-turbo-dit (4,93 GB) | 4930777530 = 4930777530 | `172d7a98...4afa574e45` | ✅ idêntico |
| hy-mini-turbo-dit (3,82 GB) | 3822584202 = 3822584202 | `bdbcef30...e04e03c247bc4` | ✅ idêntico |
| triposr-ckpt (1,68 GB) | 1677246742 = 1677246742 | `429e2c6b...2ffcd970ee` | ✅ idêntico |
| hy-vae-v2-0-turbo | 407410402 = 407410402 | `66b7af69...2837af9e4ce31cb4` | ✅ idêntico |
| u2net.onnx | 175997641 = 175997641 | `8d10d2f3...a728a912b491` | ✅ idêntico |

O ckpt do TripoSR vive no cache HF como blob cujo próprio nome é o SHA-256 esperado — consistência adicional. Os totais do manifesto (13 arquivos, 11.421.432.606 B medidos, 0 sem SHA) são coerentes com a soma dos itens.

## ITEM 3 — Motores: commits e patch ✅ APROVADO

- `motores\Hunyuan3D-2GP`: `git rev-parse HEAD` = **f2456e036a86a4b1d9f58e2379fe7ab0fe9b68b0** (o f2456e0 do plano); árvore limpa.
- `motores\TripoSR`: HEAD = **107cefdc244c39106fa830359024f6a2f1c78871** (o 107cefd do plano); `git status` mostra exatamente **1 modificação local**: `tsr/bake_texture.py`; `git diff --stat` = 1 arquivo, 3 inserções, 2 remoções — **o patch `triposr_bake_texture.patch` está aplicado** e nada mais foi tocado.

## ITEM 4 — Worker: tarefa, processo, lock ✅ APROVADO (obs. O1)

- Tarefa **Oficina3D_Worker** registrada: estado **Running**; ação = `.venv_app\Scripts\pythonw.exe instalacao\tarefa_worker\iniciar_worker.py`; gatilho **LogonTrigger** habilitado; última execução 31/10 19:45:49, resultado 267009 (0x41301 = tarefa em execução — coerente).
- Processos vivos no momento da auditoria: o lançador (`iniciar_worker.py`, via shim do venv) e o worker real `-m oficina3d.worker`.
- `locks\worker.lock` presente (140 B, 19:45:50).
- Log `_cache\logs\tarefa_worker.log` registra a subida às 19:45:49.
- **Evidência funcional (além do escopo mínimo):** durante a auditoria, um job real (`20261031-195500-fumaca-mv-turbo`, 4 vistas, motor hunyuan-mv-turbo, seed 1234) foi processado de ponta a ponta pelo worker: `estado=concluido`, `progresso=100`, forma gerada em 43,1 s (165.944 triângulos brutos, pico de VRAM 6.417 MB), refino + exportação, conclusão em **64,5 s** totais. A fila funciona de verdade, não só no papel.

**O1 (observação):** o log do lançador mostra **duas subidas** do worker (19:45:49 e 19:54:38) — houve um reinício ~9 min após a subida, sem registro de causa no log. O job das 19:55 foi processado pelo worker já reiniciado (PID 28044). Ver problema P4.

## ITEM 5 — Suíte de testes ⚠️ REPROVADO PARCIAL

O agente principal relatou "152 testes OK, 1 skip legítimo". A auditoria executou a suíte **duas vezes, em dois interpretadores**, com resultados diferentes — e a diferença é o achado mais importante desta auditoria:

### 5a. No Python 3.12 do sistema (`py -3.12 -m unittest discover -s testes`)
- **Ran 152 tests in 20.083s — OK (skipped=1), exit=0.** O número do agente principal **confere exatamente**.
- O skip é `test_refino.TestRefinarPymeshlab.test_backend_pymeshlab` ("precisa de Blender + numpy/trimesh/pymeshlab"). Causa: `pymeshlab_disponivel()` inspeciona o interpretador corrente (`importlib.util.find_spec`), e o Python 3.12 do sistema **não tem** pymeshlab — ele mora no `.venv_app`. Ou seja: sob o 3.12, o skip é esperado e não some nunca, exista ou não instalação.

### 5b. No interpretador de PRODUÇÃO (`.venv_app\Scripts\python.exe`, Python 3.10)
- **Ran 152 tests in 19.460s — FAILED (failures=2), exit=1.**
- O teste do backend pymeshlab **rodou e passou** (`test_backend_pymeshlab ... ok`) — a instalação real é exercitada e aprovada aqui.
- **2 falhas**, ambas em `test_travas.TestTravaEntreProcessos`:
  - `test_dois_processos_disputando`: `AssertionError: 25092 != 20780`
  - `test_trava_orfa_de_processo_morto`: `AssertionError: 22384 != 29528`
  Os valores são **PIDs**: o teste spawna um processo e espera que o PID gravado na trava seja o PID do processo spawnado.

### Causa raiz — PROVADA em experimento controlado do auditor
Os venvs criados pelo **uv** no Windows usam um **lançador-shim**: o `python.exe` do venv é um trampolim que executa o interpretador real (`_cache\uv_python\cpython-3.10\python.exe`) como processo filho, **com outro PID**. Experimento (mesmo comando, dois interpretadores):

```
.venv_app : Popen.pid = 10444 | filho os.getpid() = 30204  -> DIFERENTES (shim confirmado)
py -3.12  : Popen.pid = 4684  | filho os.getpid() = 4684   -> IGUAIS
```

A própria lista de processos do worker exibe o fenômeno (shim PID 33552 → worker real PID 24816).

### Por que isto é GRAVE e não "só um teste chato"
- Os testes que falham são justamente os da **trava entre processos** (`oficina3d.travas`) — o mecanismo que impede dois processos de disputarem a GPU e que detecta trava órfã de processo morto. Se o código de produção grava/confere PIDs obtidos via `Popen`/`sys.executable` sob o venv, ele pode estar comparando **o PID do shim com o PID do processo real** — ou seja, o defeito que o teste expõe pode existir **em produção**, não só no teste: detecção de órfã e de disputa operando sobre a identidade errada de processo.
- O veredito "suíte verde" do checkpoint `6762003` foi medido no interpretador que **não** é o de produção. A régua correta daqui pra frente: **a suíte oficial roda no `.venv_app`** (é ele que executa worker, CLI e motores), e nela a suíte está **vermelha: 150/152**.

## ITEM 6 — Rede/GitHub: push falhando ❌ REPROVADO (ambiente)

Verificação própria do auditor (não é transcrição do relato):
- `git status` no `app`: árvore **limpa**, `main` **ahead 2** de `origin/main` — os commits `6839839` (itens 1–2) e `03cf44a` (EXEC-02) existem **só localmente**. Remoto parado em `6762003` (confirmado também pela API do GitHub a partir da VM do auditor).
- `Resolve-DnsName github.com` no PC → **4.228.31.150**; `api.github.com` → **4.228.31.149**. Os endereços reais do GitHub são da faixa **140.82.112.0/20** — o PC está recebendo endereço que **não é do GitHub**.
- Consultas diretas a resolvedores públicos (8.8.8.8 e 1.1.1.1) a partir do PC: **timeout** — o DNS externo está interceptado/bloqueado no caminho.
- Conexão TCP a github.com:443: **pendura** até estourar (blackhole), compatível com IP de sinkhole/filtro.
- A placa de rede lista um adaptador **Windscribe WireGuard** (VPN) com DNS próprio (10.255.255.1), além do Wi-Fi com DNS 8.8.8.8/8.8.4.4.
- **Hipótese do Crítico (rotulada como hipótese):** a resolução de nomes do PC está sendo interceptada — o suspeito principal é a camada de VPN/filtro (Windscribe) ou interceptação de DNS na rede local — devolvendo IPs de bloqueio para `*.github.com`. Não é falha do projeto nem do git: clones e pushes funcionaram mais cedo no mesmo dia (até ~18:38) e downloads de Hugging Face/PyPI fluíram a ~200 Mbps no mesmo período; a quebra é específica de rota/DNS para o GitHub e começou entre 18:38 e 18:47.
- **Risco:** enquanto durar, o "commit+push ao fim de cada tarefa" do plano está quebrado; a guarda dupla (Drive + GitHub) fica manca. Nada se perde (working tree limpa, commits locais íntegros), mas **a divergência local×remoto precisa ser monitorada** — hoje são 2 commits.

---

## PROBLEMAS, RISCOS E LACUNAS (consolidado)

- **P1 — GRAVE. Suíte vermelha no interpretador de produção.** 2 falhas em `test_travas.TestTravaEntreProcessos` sob `.venv_app` (150/152), por incompatibilidade de identidade de PID causada pelo shim do venv do uv. Risco de o mesmo desencontro de PID existir no código de produção de travas (trava órfã/disputa), não só nos testes. **Exige:** correção que torne a identidade de processo robusta sob o venv (ou padronização da suíte no venv + ajuste dos testes/código) e reexecução completa no `.venv_app` antes de qualquer "Fase 1 concluída".
- **P2 — GRAVE (processo). Régua de aceite medida no interpretador errado.** O checkpoint do código (152 OK) usou o Python 3.12 do sistema. Daqui pra frente, resultado de suíte só vale se vier do `.venv_app` (produção). O skip "legítimo" do backend pymeshlab era, na verdade, sintoma dessa troca de interpretador: no venv ele roda e passa.
- **P3 — MÉDIO (ambiente). github.com inalcançável do PC** (DNS devolvendo IP estranho; resolvedores externos em timeout; TCP blackhole). Push impossível desde ~18:47; 2 commits só locais. **Exige:** diagnóstico de rede (VPN Windscribe é a suspeita nº 1) e, resolvido, push imediato + confirmação de `ahead 0`. Não é defeito do projeto.
- **P4 — MÉDIO. Worker reiniciou sem causa registrada** (subidas às 19:45:49 e 19:54:38 no log do lançador, sem linha de erro/queda). O supervisor reinicia em queda (até 5×/h) — se houve queda, o motivo não ficou registrado em `tarefa_worker.log`. **Exige:** logar o motivo de cada reinício (código de saída do worker) — sem isso, instabilidade futura é invisível. (E, dado P1, vale conferir se o reinício tem relação com PID/lock.)
- **P5 — BAIXO. Job concluído não arquiva:** o job de fumaça terminou `concluido`, mas o arquivamento ficou `sem destino` porque `OFICINA3D_ARQUIVO` não está definida no ambiente da tarefa — resultado fica só no disco local, fora do fluxo de arquivo do projeto (Drive `arquivo_jobs`). Decisão/configuração pendente, não defeito de código.
- **P6 — BAIXO (já conhecido, revalidado). Dívida de testes herdada dos agentes:** faltam `test_worker.py`, `test_cli.py`, `test_entrada.py`, `test_web.py`, `test_mcp.py` e a `LISTA_INSTALACAO_FASE1.md` do agente B. Com P1/P2, a escrita desses testes deve mirar o `.venv_app`. Em especial **web e MCP não têm NENHUM teste automatizado** — a prova do item 5 da Fase 1 será manual até existirem.
- **P7 — OBSERVAÇÃO. Entradas do job de fumaça eram imagens muito pequenas** (objeto de ~49×241 px; o pré-processamento ampliou só 2× e emitiu 8 avisos de resolução). O job provou o encanamento, **não** a qualidade — a bateria dourada (abaixo) precisa usar as imagens de referência em resolução adequada, senão mede o pipeline com entrada inválida.
- **P8 — OBSERVAÇÃO. Higiene da auditoria:** processos destacados via `Start-Process` a partir da sessão SSH morrem com ela (dois jobs do próprio auditor morreram assim às 19:50); o meio confiável de executar trabalhos longos no PC é **tarefa agendada** — foi o método usado nas execuções válidas. Registrar para as próximas auditorias.

---

## BATERIA DE TESTES RIGOROSA — PRÓXIMAS PROVAS DA FASE 1

Regras gerais da bateria: (i) toda prova roda com o PC **ocioso** (sem outro uso de GPU; o cunhado está fora até dom 01/11 à noite — janela válida); (ii) toda prova grava em `docs\REGISTRO.md`: comando exato, interpretador, tempos, VRAM de pico, artefatos e hashes; (iii) nenhuma prova é "passou de olho": cada critério é binário e mensurável; (iv) a suíte unitária oficial passa a ser a do `.venv_app`.

### Prova A — Job de fumaça na fila do worker (item 4, fechamento)
- **Objetivo:** provar enfileirar → processar → concluir sem intervenção, ponta a ponta, pelo caminho que outra IA usaria.
- **Método:** com o worker já rodando pela tarefa, submeter 1 job via CLI do `.venv_app` (`python -m oficina3d.cli enviar --imagem <frente.png:frente> --motor triposr --esperar`) usando imagem de referência ≥1024 px; acompanhar `cli status` até o fim.
- **Aprovação (todos):** job termina `estado=concluido`; `saida\modelo.glb` existe e abre em `trimesh` (malha não vazia, >0 triângulos); `saida\relatorio.json` presente; tempo total registrado; nenhum erro no `log.txt` do job; worker segue vivo depois do job.
- **Registrar:** id do job, tempos por etapa (histórico do job.json), VRAM de pico, tamanho do GLB.

### Prova B — Web (FastAPI) e MCP no ar (item 5)
- **Objetivo:** as duas portas de entrada sobem, respondem e enxergam a mesma fila.
- **Método:** subir `python -m oficina3d.web` (127.0.0.1:8765) e o servidor MCP (`.venv_mcp`, stdio e/ou `--http --porta 8766`) a partir dos venvs certos; da web: `GET /docs`, `GET /api/...` de saúde e de motores; submeter 1 job triposr pela API e 1 pela ferramenta MCP `submeter_job`; consultar `status_job`/`listar_jobs` no MCP e o mesmo job na API.
- **Aprovação (todos):** web responde 200 em `/docs` e no endpoint de saúde; lista de motores idêntica nas duas superfícies; os 2 jobs aparecem nas duas superfícies com o mesmo id/estado; ambos concluem; `saude` do MCP responde sem erro. Qualquer divergência entre API e MCP reprova.
- **Registrar:** comandos de subida, respostas (status HTTP/JSON resumido), ids dos jobs, tempos.

### Prova C — Bateria dourada (item 6, aceite da Fase 1)
Matriz do plano: **{Orc, Capríleo, Besta} × {mv-turbo (4 vistas), mini-turbo (1 vista)} × {seed A, seed B}**, PC ocioso.

- **Objetivo:** provar qualidade e desempenho do caminho principal: o Orc de 4 vistas no mv-turbo em **≤ 3 min** é a meta histórica da fase; os demais medem consistência.
- **Método:** para cada célula: submeter o job pela fila (worker), cronometrar do `processamento iniciado` ao `concluido` no histórico do job.json; coletar do `relatorio.json`: triângulos finais, VRAM de pico, prévias geradas; validar cada GLB (abre, malha fechada/não vazia, triângulos ≤ teto do projeto de 50 mil na saída refinada); renderizar/conferir as 5 prévias.
- **Aprovação (binário, por célula e no conjunto):**
  1. **Orc × mv-turbo: tempo total ≤ 180 s** nas 2 seeds (é O critério da fase);
  2. 12/12 jobs `concluido`, 0 erros;
  3. 12/12 GLBs válidos e dentro do teto de triângulos da saída;
  4. VRAM de pico ≤ 8.188 MB (RTX 4060) sem estouro em nenhuma célula;
  5. Mesma seed ⇒ mesmo resultado: repetir 1 célula (Orc/mv/seed A) e exigir GLB byte-idêntico ou, se o motor não for determinístico nesse nível, relatorio.json com mesmos parâmetros e triângulos iguais — o comportamento observado vira o registrado (sem maquiar);
  6. Prévias presentes e visualmente íntegras (sem malha explodida) nas 12 células.
- **Registrar:** tabela completa da matriz (tempos, triângulos, VRAM, tamanhos), hashes SHA-256 dos 12 GLBs, e o veredito célula a célula no REGISTRO + espelho no Drive.

### Prova D — Regressão obrigatória pós-correção do P1 (nova, criada por esta auditoria)
- **Objetivo:** fechar o defeito da trava sob o venv.
- **Método:** após a correção do agente principal, rodar a suíte **inteira no `.venv_app`** e, em seguida, a prova de estresse: 2 processos disputando a trava de GPU de verdade + matar o dono da trava e exigir que a trava órfã seja detectada e liberada.
- **Aprovação:** suíte 152/152 (ou 152 + novos testes, 0 falhas, 0 skips indevidos) no `.venv_app`; estresse com disputa resolvida a favor de um só processo; órfã liberada em tempo registrado.
- **Registrar:** saída completa da suíte, PIDs envolvidos, tempos de detecção da órfã.

---

## CONCLUSÃO DO CRÍTICO

A instalação da Fase 1 é **sólida e honestamente relatada** nos itens materiais (venvs, modelos, motores, worker) — a conferência independente reproduziu cada número. O que o relato não tinha como ver — porque mediu com o interpretador errado — é que **a trava entre processos não está provada no ambiente real**, e há 2 falhas de teste apontando para um desencontro de PID que pode ser de produção. Some-se a rede do PC rejeitando o GitHub (ambiente, não projeto) e o retrato correto é: **itens 1, 2 e 4 aprovados; item 3 (código) aprovado apenas sob a régua antiga — sob a régua certa, reprovado até a correção do P1 e a Prova D; item 5 e 6 pelas Provas B e C.**

Assinado: Agente Crítico — Auditoria nº 1, 2026-10-31.
Evidências brutas no PC: `_cache\logs\critico_hash.txt`, `_cache\logs\critico_testes.txt` (3.12), `_cache\logs\critico_testes_venv.txt` (venv), `_cache\logs\tarefa_worker.log`.
