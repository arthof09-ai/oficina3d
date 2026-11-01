# REGISTRO: diário da Oficina 3D v2 (CUNHADO-PC)
Regra: nunca apagar entradas; só acrescentar. Cada entrada: data/hora, o que fez, comando, resultado, evidência.

---

## 31/10/2026 ~11:45 — Início da sessão
- Prompt de entrada lido: `docs\PROMPT_ENTRADA_CLAUDE_CUNHADO_PC_OFICINA3D_v2.md`.
- Caminho real da pasta do plano (o prompt omite um nível): `C:\Users\txcga\Desktop\RPG Assimilação\RPG Assimilação\00 — Comece aqui\PC_Gusta_Oficina3D\OFICINA3D_v2_PLANO\`.
- Lidos: `RELATORIO_CENTRAL_E_PLANO_OFICINA3D_v2.md`, `analise_B_PC_CUNHADO.md`, `MANIFESTO_DOWNLOADS_OFICINA3D_v1.json`.

## 31/10/2026 ~11:50 — Medidas iniciais
- `hostname` → `PCdaNasa`.
- `nvidia-smi` → RTX 4060, driver 610.88, 8188 MiB total, 1098 MiB usados, 6859 MiB livres, 2% de uso. Processos com GPU: só aplicativos de desktop do dono do PC (lista omitida no repositório público).
- `Get-PSDrive C` → 46,2 GB livres. `G:` já existe ("Google Drive"), contém só `Meu Drive.lnk` → aponta para `C:\Users\txcga\Desktop\RPG Assimilação` (modo espelho).
- Pasta espelhada `Desktop\RPG Assimilação` = 6,9 GB.
- `RPG_Local\oficina3d_ia` = 26,3 GB (TripoSG 12,6; PartCrafter 10,2; DetailGen3D 3,4; python 0,1).
- `python --version` → 3.12.10; `py.exe` presente; `uv` ausente.
- Windows Update: chaves `PauseUpdatesExpiryTime` etc. vazias → **não pausado**.
- `gh auth status` → logado como arthof09-ai, escopo `repo`.

## 31/10/2026 ~11:55 — Repositório e pastas
- `gh repo create arthof09-ai/oficina3d --private --clone` (em `C:\Users\txcga\RPG_Local\Oficina3D`) → `https://github.com/arthof09-ai/oficina3d`; pasta renomeada para `app`.
- Criadas `motores`, `_cache`, `jobs`, `jobs_teste`, `locks` em `C:\Users\txcga\RPG_Local\Oficina3D`.
- Copiados para `app\docs\`: ARQUITETURA.md, USO_PARA_IAS.md, o prompt de entrada; para `app\docs\v1_recuperado\`: config.py, job.py, servidor_mcp.py, scripts de instalação, compat\torchmcubes; para `app\instalacao\`: o manifesto de downloads.
- Criados os arquivos de continuidade (ESTADO_ATUAL, REGISTRO, DECISOES, ERROS, COMANDOS_QUE_FUNCIONARAM.ps1, PROMPT_RETOMADA, SAUDE_FASE0.json).
- Commit `9661c68` em `main`, push OK. Evidência: `git ls-remote https://github.com/arthof09-ai/oficina3d.git main` → `9661c68fda6d...`; `gh api repos/arthof09-ai/oficina3d --jq .private` → `true`. VERIFICADO.

## 31/10/2026 ~12:00 — Drive: Oficina3D_v2 e item 0.1
- Criado `C:\Users\txcga\Desktop\RPG Assimilação\RPG Assimilação\Oficina3D_v2\` com `arquivo_jobs`, `referencias`, `aprovados`, `REGISTRO`, `modelos_guardados`, `instaladores`, `backups` (ainda no espelho; depois do streaming fica em `G:\Meu Drive\RPG Assimilação\Oficina3D_v2\`).
- `docs\*` (sem `v1_recuperado`) + manifesto copiados para `Oficina3D_v2\REGISTRO\`.
- Item 0.1 (Drive "atualizado"): **PENDENTE**. `%LOCALAPPDATA%\Google\DriveFS\Logs\drive_fs.txt` mostra o Drive em atividade (uploads dos arquivos novos, downloads vindos de outro PC) e erros de "Retrying operation" / `FAILED_PRECONDITION` às 14:56Z. Não dá para garantir "atualizado" pelo log: precisa de uma pessoa olhar o ícone do Drive.
- Item 0.2 (trocar para streaming): **PENDENTE**, precisa de cliques na tela (sem computer use nesta sessão).

## 31/10/2026 ~12:15 — Repositório público (pedido do Mestre)
- Mestre: "Quero o repositório público" e "Pode trabalhar com mais de um agente, mas registre tudo para uma possível sucessão".
- Tirados dos docs: o e-mail pessoal (prompt de entrada) e a lista de programas do cunhado (REGISTRO, SAUDE_FASE0). Conferido por busca: sem `gmail`/nomes de programas.
- Histórico refeito: branch órfã com a árvore limpa → force-push em `main` → `gh repo edit --visibility public`. Ver DECISOES GIT-02 a GIT-04.
- (ver entrada seguinte)
- Drive conferido de novo: `G:\Meu Drive` não existe; G:\ ainda só tem `Meu Drive.lnk` → **continua em espelho**. Por isso nada de download/instalação ainda; sigo com código (Fase 1, item 1), que não depende do Drive.

## 31/10/2026 ~12:30 — Agentes
- Checkpoint `8810d37`; abertos Agente A (config/job) e B (instalador/manifesto), em segundo plano.
- Mestre: "Divida o seu trabalho com outros agentes, quanto mais melhor" (DECISOES AG-02). Checkpoint `c4296bc`; abertos C (núcleo), D (entrada), E (refino), F (web+MCP), G (travas/arquivar/saúde). Donos dos arquivos: tabela no ESTADO_ATUAL.
- Os relatórios de cada agente serão colados abaixo quando chegarem, com SHA256 dos arquivos.

## 31/10/2026 ~12:38 — Sessão interrompida pelo limite de uso (registro do Muse)
- A sessão do Claude atingiu o limite ("You've hit your session limit") com as notificações dos agentes ainda chegando. Os relatórios dos agentes **não** foram colados aqui e nada do código deles foi commitado. O limite semanal da conta vai até qui 05/11, 14:00.
- Continuação assumida pelo Muse (DECISOES EXEC-01).

## 31/10/2026 ~12:26 — Itens 0.2 e 0.4 resolvidos pelo Muse (remoto)
- Drive trocado de espelho para **streaming**: `G:\Meu Drive` ativo com o conteúdo da conta; a pasta do Desktop segue como pasta de origem da sincronização (nada apagado). Antes disso o app do Drive mostrava "1 erro" de upload — era um arquivo do próprio Muse, sem relação com a Oficina, que ficou só no computador por decisão informada.
- **Windows Update pausado por 5 semanas** (até 05/12/2026), conferido de volta no registro do Windows.
- Item 0.3 liberado: o Claude foi avisado com "Drive pronto" na sessão dele.

## 31/10/2026 ~14:35 — Decisões do Mestre (item 0.6)
- ZIP-01 aprovado; RF-03 final (Hunyuan livre); NET-01 final (Tailscale no celular adiado); USO-01 final (sem horário fixo; janela livre até dom 01/11 à noite). Ver DECISOES.

## 31/10/2026 14:37–15:05 — ZIP-01 executado pelo Muse
- `PartCrafter.zip`: 7.491.118.361 bytes; `7z t` OK; MD5 `7BF9163230357929E1B9C52F94D16CCD`; SHA256 `3332C55A72404397932F7EE163279DB867A8AEA14F682AE1A260493E125D191A`.
- `DetailGen3D.zip`: 3.429.846.267 bytes; `7z t` OK; MD5 `3F78B7B71BA1B34FDE7EE016CC9B3872`; SHA256 `C2B0568E707F39C9C7D4FF568807308A3FFE709EBC1413F71AF4AC3CC4B48FA2`.
- Cópias em `Oficina3D_v2\modelos_guardados\`; `md5Checksum` da nuvem conferido igual ao local **antes** de apagar.
- Originais locais e zips de staging apagados; pasta de staging removida. TripoSG intocado. No conjunto das limpezas do dia (inclui Downloads, com aprovação do dono do PC), o C: foi de 46,1 para **70,1 GB livres**.

## 31/10/2026 ~15:10 — Auditoria da sessão pelo Muse
- Transcrição completa da sessão lida e cruzada com PC, GitHub e Drive: relatos conferidos (repo público por GIT-02, a pedido do Mestre; medidas batem).
- Código dos agentes A–G conferido arquivo por arquivo: presente, sem revisão e sem commit. Faltam `test_worker.py`, `test_cli.py` (C), `test_entrada.py` (D), `test_web.py`, `test_mcp.py` (F) e `instalacao\LISTA_INSTALACAO_FASE1.md` (B). Detalhes no ESTADO_ATUAL.

## 31/10/2026 ~15:25 — Fase 0 fechada
- Medidas que faltavam: CUDA UMD **13.3** (nvidia-smi); SSD **NVMe NX-512 2280, 477 GB** (Get-PhysicalDisk respondeu via SSH); rede **~95 Mbps** de download (curl, speed.cloudflare.com).
- `SAUDE_FASE0.json` reescrito com o cenário pós-streaming (aceite da Fase 0). Docs atualizados copiados para `Oficina3D_v2\REGISTRO\`.

## 31/10/2026 ~15:27 — Revisão do código dos agentes (Muse)
- Suíte rodada na pasta `app`: `py -3.12 -m unittest discover -s testes -v` → **152 testes em 25,2 s: OK (skipped=1), exit 0**. O skip é o backend opcional de refino (Blender + pymeshlab), que depende da instalação da Fase 1.
- Nenhuma correção de código foi necessária. Dívida registrada no ESTADO_ATUAL: 5 arquivos de teste faltantes (C, D, F) e a `LISTA_INSTALACAO_FASE1.md` (B) — não bloqueiam a instalação.
- Commit de checkpoint do pacote `oficina3d\`, `testes\`, `instalacao\` e `docs\mcp_exemplo.json` (o `.gitignore` já barra pycache, venvs, pesos e imagens).

## [2026-10-31 18:24 -03] Fase 1, itens 1 e 2: instalacao executada

- Quem: Muse (continuacao autorizada pelo Mestre em 31/10 18:22).
- Plano do instalador conferido antes de executar (guarda anti-Drive OK; 70,00 GiB livres; previsto 20,64 GiB; minimo de 20 GiB respeitado).
- Executado pelo instalador do projeto: uv 0.13.6 achado no PATH do usuario; Python 3.10 instalado pelo uv; 3 venvs criados com torch 2.5.1+cu124 (app, triposr, mcp); clones Hunyuan3D-2GP@f2456e0 e TripoSR@107cefd; patch triposr_bake_texture aplicado (git apply --check antes); 13 modelos baixados (11,42 GB) com SHA-256 conferido um a um; manifesto atualizado com bytes/SHA medidos; locks dos 3 venvs gravados.
- Testes de import da primeira rodada: .venv_triposr OK (IMPORT OK 2.5.1+cu124, CUDA True, transformers 4.35.0, torchmcubes resolvido pelo compat do projeto); .venv_mcp OK (mcp 2.3.0); .venv_app FALHOU: ModuleNotFoundError: No module named 'setuptools' (cadeia: optimum.quanto -> torch.utils.cpp_extension -> import setuptools).

## [2026-10-31 18:45 -03] Correcao do .venv_app: setuptools + wheel

- Causa: o venv criado pelo uv nasce sem setuptools; o app.txt nao o listava.
- Correcao aplicada: setuptools 84.2.1 e wheel 0.48.0 instalados no .venv_app; `setuptools` e `wheel` adicionados a `instalacao/requisitos/app.txt` (com comentario da causa) para instalacoes futuras; lock `requirements_venv_app.lock` re-congelado.
- Reteste com o mesmo comando do instalador: **IMPORT OK 2.5.1+cu124 True 4.49.0 0.39.0** (torch, CUDA disponivel, transformers, diffusers).
- Estado: **itens 1 e 2 da Fase 1 CONCLUIDOS** (ambiente, motores e modelos prontos e provados por import). Proximos: item 4 (worker + gpu.lock + jobs_teste), item 5 (web/MCP no ar) e item 6 (bateria dourada).

## [2026-10-31 19:44 -03] EXEC-02: autorizacao total + metodo de trabalho

- O Mestre concedeu autorizacao total ao Muse DENTRO do projeto Oficina3D (ver DECISOES, EXEC-02): decidir pelo melhor do projeto, fazer e baixar o que precisar, registrando todas as duvidas, problemas, decisoes e solucoes, e trabalhando sempre com um agente Critico rigoroso e baterias de testes.
- Primeira aplicacao: o registro da tarefa do worker (item 4 da Fase 1), que estava pausado desde 18:50 aguardando esta confirmacao, foi executado com o script do proprio projeto.

## [2026-10-31 18:47-18:57 -03] PROBLEMA: PC sem alcancar o github.com (push pendente)

- Sintoma: `git push` falha com "Failed to connect to github.com:443" (timeouts de 21-33 s), 8 tentativas automaticas esgotadas. Outros destinos funcionaram no mesmo periodo (Hugging Face a ~200 Mbps, PyPI, indice do PyTorch).
- Impacto: nenhum no codigo (commit 6839839 esta salvo local; o remoto ja tinha tudo ate 6762003). Apenas a sincronizacao esta pendente.
- Estado: em diagnostico (DNS x rota) pelo Muse; solucao e resultado serao registrados aqui.

### Atualizacao do diagnostico [2026-10-31 19:57 -03]

- O problema NAO e so o GitHub: testes as 19:52-19:57 mostram a conexao TCP 443 falhando para TODOS os destinos provados (github.com, api.github.com, ssh.github.com, huggingface.co, pypi.org, www.google.com), com DNS lento e algumas respostas estranhas do resolvedor local (github.com e api.github.com resolvendo para a faixa 4.228.31.x). Ate 18:38 a mesma rede baixava a ~200 Mbps; a degradacao comecou entre 18:42 e 18:47.
- O acesso do Muse ao PC (Tailscale/SSH) segue normal: o defeito esta na saida comum do PC/provedor, nao no projeto.
- DECISAO do Muse (EXEC-02): o trabalho local da Fase 1 SEGUE (worker, jobs, web, MCP e bateria dourada nao precisam de internet — os modelos ja sao locais). Para a sincronizacao, fica armada uma tarefa automatica no PC que tenta o `git push` a cada 15 min e se desliga sozinha no primeiro sucesso; o resultado fica registrado aqui.

## [2026-10-31 19:45-20:02 -03] Item 4 (worker no ar) + INFRA-01 (Hunyuan no .venv_app)

- Worker: tarefa `Oficina3D_Worker` registrada com o script do proprio projeto (registrar_tarefa.cmd) e iniciada; log confirma o lancador subindo `python -m oficina3d.worker` as 19:45:49; processos vivos conferidos.
- PROBLEMA encontrado na checagem viva `cli motores`: os motores Hunyuan apareciam INDISPONIVEIS — o config esperava um `.venv_hunyuan` que o instalador nao criou (a pilha Hunyuan foi instalada no `.venv_app`). Os testes unitarios nao pegavam (fronteira dos motores e simulada neles).
- SOLUCAO (DECISOES: INFRA-01): `NOMES_VENVS` passou a apontar `hunyuan` -> `.venv_app`; docstring do runner e 3 assercoes de `test_config.py` ajustadas. Verificacao: suite completa **152 testes OK** e `cli motores` agora mostra **mv-turbo, mini-turbo e triposr DISPONIVEIS**.
- PROBLEMA registrado (pendente): os motores NAO-turbo `hunyuan-mini` e `hunyuan-mv` (30 passos) estao sem os pesos completos (o manifesto so baixou as variantes turbo). DECISAO (EXEC-02 + ordem de qualidade do Mestre, 19:52): baixar tambem os pesos full dos dois motores quando a internet do PC voltar, para a Oficina ficar completa — pesos estimados em ~8,7 GB no total; conferir a lista exata pelo manifesto antes de baixar.
- Ordem do Mestre (19:52): revisar tudo que falta, definir o que e a Oficina "pronta", e depois da conclusao rodar rodadas de aprimoramento — qualidade acima de economia. Revisao formal entra em `docs/REVISAO_E_ROTEIRO.md`.

## [2026-10-31 19:59-20:15 -03] Auditoria do Critico n. 1 + correcao do P1 (trava x PID)

- O agente Critico entregou a auditoria independente (relatorio completo em `docs/CRITICO-fase1-auditoria-1.md`): itens 1 (venvs), 2 (modelos, amostra 5/13 = 93% dos bytes, SHA identico), 3 (motores nos commits + patch) e 4 (worker) APROVADOS com evidencia propria. Durante a auditoria, o job de fumaca `20261031-195500-fumaca-mv-turbo` concluiu ponta a ponta em **64,5 s** (forma em 43,1 s; VRAM de pico 6.417 MB) — a fila funciona de verdade.
- **P1 (grave): a suite estava VERMELHA no interpretador de producao.** No `py -3.12` eram 152 OK (1 skip); no `.venv_app` (o Python que o worker usa) havia 2 falhas em `test_travas.TestTravaEntreProcessos`: o teste comparava o PID gravado na trava com `Popen.pid`, mas no venv do uv o executavel e um lancador (trampolim) cujo PID difere do PID do Python real.
- Auditoria de producao do Muse sobre o P1: `travas.py` e consistente (quem segura a trava grava o proprio `os.getpid()` + horario de criacao do processo); `motores` roda os runners sob JobObject do Windows com morte da arvore inteira (seguro contra o trampolim); o worker nao depende de `Popen.pid`. Conclusao: o defeito era da ASSUNCAO do teste, nao do codigo de producao.
- CORRECAO aplicada em `testes/test_travas.py`: o processo filho grava o proprio PID no registro de eventos e os testes comparam a trava com ESSE pid (nunca com `Popen.pid`); docstring do arquivo atualizada. Resultado: **suite inteira no `.venv_app`: 152 testes, OK, 0 skips** (o teste de pymeshlab, que no 3.12 era pulado, roda e passa no venv).
- **P2 (metodo): a regua oficial de testes do projeto passa a ser o interpretador de producao (`.venv_app`)**, nao o Python do sistema.
- **P3 (rede): hipotese do Critico para o github.com inalcancavel:** o resolvedor local devolve IP de faixa errada para github.com (4.228.31.x) e consultas a DNS publicos dao timeout; ha um adaptador **Windscribe WireGuard** no PC — provavel interceptacao de DNS da VPN, quebrada entre 18:38 e 18:47. O `MusePushSync` segue tentando a cada 15 min; o repo local esta integro e a frente do remoto (nada perdido).
- **P4 esclarecido:** a reinicializacao do worker as 19:54:38 foi do Muse (parar/subir a tarefa) para o worker carregar a correcao INFRA-01 — causa registrada aqui, como o Critico cobrou.
- P5 (arquivamento de jobs concluidos desligado: falta `OFICINA3D_ARQUIVO` no ambiente), P6 (5 testes que faltam + LISTA do agente B) e P7 (bateria dourada precisa de imagens de entrada em tamanho adequado) aceitos como proximos trabalhos, nesta ordem de execucao: P5, item 5 (web/MCP), P6, item 6 (bateria dourada).

## [2026-10-31 20:05-20:20 -03] P5 resolvido + item 4 FECHADO + bug do numpy (TripoSR)

- **INCIDENTE (espelho no Drive desatualizado):** as copias de REGISTRO/DECISOES/ESTADO na pasta `Oficina3D_v2\REGISTRO` do Drive estavam paradas nas versoes de 15:28. Causa: os espelhos feitos pelo Muse desde 18:5x usavam o caminho `G:\Meu Drive\RPG Assimilacao\...` SEM o til do nome real (`RPG Assimilação`); o erro do Copy-Item nao aparecia nas saidas capturadas e os espelhos falharam em silencio. CORRECAO: espelho refeito resolvendo a pasta por curinga e **conferido por MD5** (os 3 arquivos identicos local x Drive). LICao registrada: espelho so vale com conferencia de hash/tempo; nunca confiar em copia silenciosa.
- **P5 (arquivamento):** o worker ja chamava `arquivar_job`, mas `OFICINA3D_ARQUIVO` nao existia no ambiente. CORRECAO: `instalacao\env.cmd` e `instalacao\env.ps1` agora definem a variavel resolvendo a pasta do Drive por curinga (arquivos seguem 100% ASCII; o lancador executa o env.cmd de verdade). Worker reiniciado as 20:05:57.
- **BUG REAL (achado pelo job de prova):** o TripoSR quebrava em producao — `AttributeError: ptp was removed from ndarray (NumPy 2.0)`, dentro do **trimesh 4.0.5** (`util.allclose`), na hora de aplicar a transformacao na malha (o job chegava a 75%). Os testes de import nao pegavam: so aparece rodando o motor. DECISAO: o venv do TripoSR e da era do motor — `numpy==1.26.4` fixado em `requisitos/triposr.txt` (com o motivo), instalado e lock re-congelado. O `.venv_app` segue no numpy 2.2.6 (a pilha Hunyuan e compativel — provado no job mv-turbo).
- **PROVA:** job `20261031-200949-fumaca-arquivo-2` (triposr): **concluido 100%**, `saida\modelo.glb` (1.125.516 B) + 5 previas + relatorio; e **arquivado no Drive** em `arquivo_jobs\<id>` com `manifesto_sha256.json` e tamanhos identicos.
- **Item 4 da Fase 1 FECHADO** (worker como tarefa + fila real + gpu.lock em uso + arquivamento). Restam da Fase 1: item 5 (web/MCP no ar) e item 6 (bateria dourada), alem da divida P6 (testes que faltam + LISTA).

## [2026-10-31 20:14-20:16 -03] P3 RESOLVIDO: era o tunel da VPN Windscribe

- Autorizacao do Mestre (20:14): desligar a VPN do PC.
- Diagnostico confirmado antes de desligar: adaptador `WindscribeWireguard` ativo com DNS proprio do tunel (10.255.255.1) e servicos `WindscribeService` + tunel WireGuard rodando; o DNS do Wi-Fi (8.8.8.8) estava limpo.
- Acao: parados o servico do tunel e o `WindscribeService` e encerrado o app Windscribe (reversivel: abrir o app religa). Nada mais foi tocado (o adaptador Radmin VPN, sem DNS, ficou como estava).
- Prova: com o tunel fora, o MESMO IP que o DNS devolve para github.com passou a responder — `https://github.com` = **HTTP 200**. Ou seja: o endereco estava certo; o tunel e que engolia as conexoes (blackhole) desde ~18:42-18:47. Hipotese do Critico (P3) confirmada na essencia: era a VPN.
- Sincronizacao: o push rodou na hora — **remoto = 969e2f7** (5 commits: 6839839, 03cf44a, 44afc03, c3615a3, 969e2f7), conferido pela API do GitHub; a tarefa `MusePushSync` se desligou sozinha apos o sucesso, como desenhado.
- Efeito colateral bom: com a internet de volta, o download dos pesos full (hunyuan-mini/mv nao-turbo) volta a ser possivel — entra na fila deste fim de semana.

## [2026-10-31 20:18-20:35 -03] Item 5 CONCLUIDO (web + MCP) e achado GIT-01

- **Tarefa `Oficina3D_Web`** criada (pasta nova `instalacao/tarefa_web/`, espelho da do worker): sobe no logon e mantem a pagina em http://127.0.0.1:8765. Endpoints provados ao vivo: `/api/saude` (ok, disco/GPU/worker), `/api/motores`, `/api/jobs`, `/` (HTTP 200).
- **Defeito real achado e corrigido no lancador:** a web MORRIA em ~3 s sob `pythonw.exe` (o `__main__` da web e o uvicorn escrevem em `sys.stderr`, que nao existe no pythonw). Em console (python.exe) subia perfeita. Correcao no `iniciar_web.py`: usar **python.exe** com `CREATE_NO_WINDOW` e saida para `_cache/logs/web_server.log`. (O worker NAO tem esse problema: foi desenhado para pythonw e segue nele.)
- **Incidente (erro do Muse, registrado):** o diagnostico da web encerrou por engano os processos do worker (filtro de processos recentes amplo demais). O worker foi religado em seguida (20:20:47) e confirmado vivo pela propria `/api/saude` (pid + trava conferem). Sem perda: a fila estava vazia.
- **MCP provado com cliente real (stdio):** servidor `oficina3d` v2.0.0, **9 ferramentas** (o plano falava 8; a extra e `iniciar_worker`). Criado o **`.mcp.json` na BASE** com os caminhos reais deste PC (o USO dizia que o Claude Code ja estava configurado, mas o arquivo nao existia).
- **PROVA B do Critico: APROVADA.** Paridade total web x MCP: mesmos 5 motores com a mesma disponibilidade e os mesmos 3 jobs (a resposta do MCP vem em blocos, um item por bloco — cliente precisa juntar todos).
- **GIT-01 (grave, corrigido):** a regra `motores/` do `.gitignore` escondia do git o pacote **`oficina3d/motores/` inteiro** (4 arquivos: `__init__.py`, `base.py`, `_runner_hunyuan.py`, `_runner_triposr.py`) — o repositorio no GitHub NAO tinha a camada de motores. A regra mirava os clones externos, que ficam na BASE (fora do repo) e nem precisavam dela. Regra ancorada para a raiz (`/motores/`) com comentario, e os 4 arquivos entraram no git neste commit.
- Derivas de documentacao corrigidas: modulo `oficina3d.servidor_mcp` -> `oficina3d.mcp` no USO (3 pontos) + nota no topo do USO com a BASE e os venvs reais deste PC; textos dos motores nao dizem mais "RF-03: so rascunho" (4 licencas + 1 descricao) — RF-03 final liberou o uso.
- Suite completa no interpretador de producao apos tudo: **verde (exit 0)**.

## [2026-10-31 20:29-20:44 -03] Pesos completos baixados (5/5 motores) e divida P6 paga

- **Motores completos:** com a internet de volta, baixados os DiTs full (30 passos) do `hunyuan-mini` e do `hunyuan-mv` para o cache HF. `cli motores` agora mostra **os 5 motores disponiveis**. Disco C: com 45,1 GiB livres apos os downloads.
- **P6 PAGA — os 5 arquivos de teste que faltavam, escritos pelo Muse:**
  - `testes/test_worker.py` (11 testes): fila (pendentes/proximo com permitidos), retomada de orfaos (volta para a fila; estourou MAX_RETOMADAS=2 vira erro; concluido intocado), escolha do motor (explicito vence; padrao mv-turbo com 2+ vistas e mini-turbo com 1) e `_livre_min_gb` (env valido/invalido/ausente).
  - `testes/test_entrada.py` (13): validacao com arrays sinteticos — diagnostico de fundo (sem alfa/tudo opaco/limpo), avisos de recorte (vazia, resolucao baixa, boa sem avisos, cortada na borda), assinatura/distancia de cor (0 consigo, 1 entre vermelho e azul), personagens diferentes e vistas repetidas.
  - `testes/test_cli.py` (10): `separar_vista` (com/sem vista, `C:\\` do Windows nao e vista, sufixo desconhecido nao e vista), parser ligado aos comandos certos e comandos sem GPU (motores=0, status de job real=0, inexistente=1).
  - `testes/test_web.py` (7): TestClient com `hosts_locais={"testclient"}` + Host de loopback + cabecalho anti-CSRF (sem isso o porteiro responde 403 a tudo — comportamento correto dele); pagina 200, motores identicos aos do modulo, saude, 422 sem imagem e com modo invalido, fluxo criar->ler->cancelar e 404.
  - `testes/test_mcp.py` (6+1): ferramentas chamadas direto (o modulo funciona sem o pacote mcp); listar motores/jobs, status, recusas de id malformado/inexistente, cancelar exigindo confirmacao; e, **so no `.venv_mcp`** (onde o pacote existe), o registro do servidor — nos outros venvs esse teste pula, como desenhado.
- **LISTA_INSTALACAO_FASE1.md** (a outra metade da P6, divida do agente B): em `instalacao/` — runtime, os 3 venvs com versoes conferidas, clones e commits, os 13+2 modelos, env, tarefas e como conferir em 1 minuto.
- **Suite completa no interpretador de producao: 199 testes, OK** (152 antigos + 47 novos; 1 skip desenhado, o do registro MCP fora do venv_mcp — la ele roda e passa: 7/7).

## [2026-10-31 20:50 -03] REVISAO_E_ROTEIRO.md entregue; Prova C bloqueada pelas imagens douradas

- Escrito `docs/REVISAO_E_ROTEIRO.md` (pedido do Mestre das 19:52): a definicao de "pronta" em 8 itens com prova, as lacunas honestas, as rodadas de melhoria R1-R5 com criterio de saida, os riscos permanentes e a tabela de status das ressalvas do Critico (P1-P6 resolvidos; P7 aberto).
- **Bloqueio da Prova C (item 6):** as imagens douradas do Orc, Caprileo e Besta NAO estao neste PC nem no Drive (buscadas em toda a BASE, em `Oficina3D_v2` — pastas `referencias` e `aprovados` vazias — e em `03 - Modelos 3D`). Eram material da v1, noutra maquina. A bateria esta desenhada e a pasta `testes/dourado/` aceita as imagens assim que o Mestre indicar onde estao (ou enviar). Sem elas, qualquer "dourado" substituto seria invencao — nao farei.

## [2026-10-31 20:46-20:57 -03] R2 comeca: o motor mini completo quebrou, foi corrigido e provou

- **Diretriz nova registrada:** DONO-01 em DECISOES (o app e do Mestre; motores embutidos; referencias de estudo serao excluidas no fim — com os limites tecnicos e de licenca escritos).
- **Falha real (a R2 cumprindo o papel):** o primeiro job do `hunyuan-mini` completo (30 passos) morreu na etapa forma: faltava `hunyuan3d-dit-v2-mini/config.yaml`. Causas: (1) meu download dirigido baixou so o `.safetensors` de cada motor novo; (2) **o verificador de disponibilidade nao cobrava o config.yaml** (para o TripoSR ele cobrava!) — o motor constava "disponivel" sem conseguir rodar.
- **Correcoes:** baixados os `config.yaml` dos dois motores novos; `_pesos_necessarios` agora exige safetensors **e** config.yaml para todo Hunyuan; criado `testes/test_motores.py` (5 testes) com a regressao.
- **Prova:** job `20261031-205245-prova-mini-full-2` **concluido 100%** — GLB de 1.134 KB + 5 previas + relatorio, arquivado. O `hunyuan-mini` completo esta vivo de verdade (nao so "disponivel").
- Na fila a seguir: a prova do `hunyuan-mv` completo (4 vistas) e um job de refino ponta a ponta usando esse GLB.

## [2026-10-31 20:59-21:02 -03] R2 CONCLUIDA: os 5 motores tem prova viva + refino + MCP HTTP

- **hunyuan-mv completo:** job `20261031-205559-prova-mv-full` concluido 100% (4 vistas, 30 passos, GLB de 1.096 KB, com o refino do proprio pipeline).
- **Refino ponta a ponta:** job `20261031-205600-prova-refino` (modo so-refinar sobre o GLB do mini completo) concluido 100% (GLB de 1.134 KB).
- **hunyuan-mini-turbo:** job `20261031-210013-prova-mini-turbo` concluido 100% (GLB de 1.108 KB). **Com isso, os 5 motores tem pelo menos 1 GLB real gerado nesta maquina** — o item 2 da definicao de "pronta" (REVISAO_E_ROTEIRO) virou verdade.
- **MCP por HTTP provado:** criado o token em `BASE\locks\oficina3d_token.txt` (gerado no PC; o valor nunca saiu de la; a pasta locks e ignorada pelo git). Servidor de prova na 8766: sem token = **401**; com `Authorization: Bearer` = initialize 200 com sessao, `tools/list` com as **9 ferramentas** e `tools/call listar_motores` respondendo. Servidor da prova encerrado no fim (o modo de uso segue sendo o stdio; o HTTP fica disponivel quando alguem precisar, com o token ja criado).
- Lacunas correspondentes da REVISAO marcadas como resolvidas no proprio documento.

## [2026-10-31 21:04-21:22 -03] R3 CONCLUIDA: queda, GPU ocupada e fila longa — tudo provado ao vivo

- **Queda do worker no meio do job:** job `r3-orfao` (hunyuan-mv, 4 vistas) teve o worker morto a força durante o processamento. Cadeia completa observada: (1) o runner morreu junto (JobObject com tree-kill — nenhum processo fantasma segurando a GPU); (2) o lancador registrou a queda e religou o worker em ~30 s; (3) o worker novo retomou o orfao (`retomadas=1`) e o job **terminou 100%**. Observacao honesta: a retomada reprocessa a forma do zero (nao reaproveita a etapa parcial) — correto, so nao e economico; fica como otimizacao futura anotada.
- **GPU ocupada por outro programa (USO-01 ao vivo):** com um processo segurando 6 GB de VRAM, o job `r3-gpu-ocupada` ficou **pendente** esperando (o worker nao forcou a entrada); quando o processo soltou a GPU, o job processou e concluiu sozinho.
- **Fila longa sem intervencao:** 8 jobs enfileirados de uma vez (6 triposr + 2 mini-turbo, atras dos dois exercicios acima): **10/10 concluidos** na sequencia, sem nenhum toque humano.
- Com a R3, a definicao de "pronta" da REVISAO fica faltando: Prova C (bloqueada nas imagens douradas), a instalacao do zero (R4) e a auditoria final do Critico.

## [2026-10-31 21:20-21:31 -03] R4 acha um defeito de verdade: o lock do TripoSR nao instalava do zero

- **A rodada R4 (instalacao do zero a partir do GitHub) FALHOU na etapa (d)** — e era para falhar mesmo, se houvesse defeito: o `requirements_venv_triposr.lock` pedia `opencv-python-headless==5.0.0.93` (que exige numpy>=2 nos metadados) junto com `numpy==1.26.4` (o fix de 31/10): **resolucao impossivel**. A combinacao RODAVA na maquina (o freeze foi feito depois do ajuste manual), mas nao INSTALA do zero. Sem a R4, ninguem saberia.
- **Correcao:** `opencv-python-headless==4.10.0.84` fixado em `requisitos/triposr.txt` (com o motivo), instalado no venv vivo (cv2 4.10.0 + numpy 1.26.4) e lock re-congelado. **Prova:** job triposr `20261031-212903-prova-opencv410` concluido e arquivado com a combinacao nova.
- O clone da R4 foi atualizado com este commit e a instalacao retomada.

## [2026-10-31 21:19-21:47 -03] R4 CONCLUIDA: a Oficina se instala do zero so com o repositorio

- Clone novo do GitHub (HEAD 6274089 na clonagem; 106 arquivos, pacote `oficina3d/motores` presente — o GIT-01 provado de fora para dentro) numa BASE limpa `Oficina3D_R4`, e o instalador oficial rodou as etapas (a)-(g): guarda e espaco ok, uv/Python 3.10, os 3 venvs (com o lock do TripoSR ja corrigido), clones nos commits fixos + patch, os 13 modelos com SHA-256 em 7,5 min e **IMPORT OK nos 3 venvs**.
- **Job de prova na base limpa:** `20261031-214423-r4-prova` (triposr) **concluido**, GLB de 1.099 KB gerado pela instalacao nova, sem tocar na instalacao principal.
- **Ligacao com a DONO-02:** esta instalacao nunca leu `modelos_guardados`, codigo v1 nem material de estudo — e a prova viva de que **o app funciona sem precisar das referencias**, que ficam preservadas para a auditoria dos Comestres, como o Mestre corrigiu.
- A BASE de teste `Oficina3D_R4` (26,8 GB) foi apagada ao final da prova para devolver o espaco ao disco (a evidencia fica neste registro e nos logs citados).

## [2026-10-31 22:43-23:05 -03] Auditoria n. 2 do Critico: NAO PRONTA + correcoes N1/N2/N3 + Prova C do Orc

- **Veredito do Critico (relatorio em `docs/CRITICO-fase1-auditoria-2.md`): NAO PRONTA** pela definicao de 8 itens — nucleo tecnico provado (1, 2, 4, 5, 6; ele rodou a suite, 2 jobs proprios e um cliente MCP proprio), item 3 bloqueado por insumo (imagens douradas), itens 7/8 nao provados por documentacao desatualizada.
- **N1 (GRAVE, erro do Muse):** no ciclo R2, o commit 8030d4b sobrescreveu `testes/test_motores.py` e apagou 19 dos 24 testes (TestPedido, TestGerarFalso — incluindo cancelamento, tree-kill e JobObject — e TestBase), e o REGISTRO da epoca descreveu o arquivo como "criado (5 testes)". A suite real tinha caido para 180. **Correcao:** arquivo restaurado do commit pai e fundido com os 5 testes novos (TestPesosNecessarios + TestListarFormatoPublico): 29 testes no arquivo. A fusao expos 1 falha: `test_disponivel_quando_venv_e_pesos_existem` (antigo) nao criava o config.yaml que a correcao de 31/10 passou a exigir — fixture atualizada com o motivo comentado. **Suite final no `.venv_app`: 204 testes, OK (skipped=1).**
- **N2 (MEDIO):** a web rodava desde as 20:20, anterior ao ajuste RF-03, e servia "so rascunho" em `/api/motores`. **Correcao:** tarefa `Oficina3D_Web` reiniciada; resposta conferida com o texto final da licenca.
- **N3 (BAIXO):** `ESTADO_ATUAL.md` reescrito com o estado real (estava parado nas ~20:20, listando dividas ja pagas).
- **As imagens douradas do ORC chegaram (envio do Mestre, 22:52):** pacotes `CODEX_DOWNLOAD_NOVO_03/04` com as 8 vistas do Orc do kit de 27/10 (4 cardinais 1280x1820 + 4 diagonais) e o machado/ataques. As 4 cardinais foram instaladas em `testes\dourado\imagens\` (gitignored). Junto vieram o PLANO fundador e o BRIEF do corpo-base em T-pose (as imagens de T-pose nunca foram geradas; seguem como opcao do Mestre).
- **PROVA C — fatia do Orc (mv-turbo) APROVADA:** jobs `20261031-225432-provac-orc-s7`, `...-225544-provac-orc-s42` e `...-225703-provac-orc-s7b`, todos concluidos e arquivados: forma em 37,1/38,9/37,9 s (criterio <= 180 s), VRAM de pico 6.411/6.411/6.435 MB (<= 8.188), GLB final de 49.750 triangulos nos tres (<= 50 mil; forma bruta de 760.690 e 928.382), e **s7b com SHA-256 identico ao s7** (determinismo por semente provado). A fatia do mini-turbo entrou em medicao em seguida; Caprileo e Besta seguem bloqueados pelas imagens (estao no kit do notebook).

- **Adendo (23:06) — fatia mini-turbo do Orc tambem APROVADA:** jobs `20261031-230121-provac-orc-mini-s7`, `...-230214-provac-orc-mini-s42` e `...-230306-provac-orc-mini-s7b` concluidos: forma em 31,2/29,3/29,1 s, VRAM de pico 5.358/5.356/5.358 MB, GLB final de 49.750 triangulos, e s7b com SHA-256 identico ao s7. **A fatia do Orc da Prova C esta completa nos dois motores; a bateria so aguarda Caprileo e Besta.**

## [2026-10-31 23:08 -03] Adendo do Critico: correcoes CONFEREM; falta so o item 3

- O Critico re-verificou com evidencia propria (relatorio em `docs/CRITICO-fase1-auditoria-2-adendo.md`): **N1 CONFERE** (suite rodada por ele: 204 testes OK; 29 no test_motores com as 5 classes; commit 49e89e4 = GitHub), **N2 CONFERE** (web ao vivo com a licenca final, CLI batendo), **N3 CONFERE COM RESSALVA MENOR** (ESTADO fiel; restavam 2 mencoes a "199 testes" na REVISAO e 1 frase superada no ESTADO — corrigidas neste ciclo) e **Prova C do Orc CONFERE integral** (hashes e parse dele: determinismo nos dois motores, 49.750 triangulos, VRAM max. 6.435 MB, forma max. 41,4 s).
- **Veredito atualizado: NAO PRONTA por um unico item** — o item 3, que so fecha com as imagens do Caprileo e da Besta Cristalina (kit de 27/10, no notebook) rodando a mesma bateria. O item 8 depende dele. De engenharia, nada falta.


## 01/11/2026, ~00:50-01:00 - Muse (CM-000009): Prova C COMPLETA, QUAL-01 no ar e novas diretivas

- **Imagens douradas recuperadas do Drive** pelo indice da auditoria do Codex (relatorio de continuidade v002, enviado pelo Mestre): Besta Cristalina (768x512) e Caprileo (~700x700), 4 cardinais de cada, **sha256 conferindo com o indice em 8/8**, instaladas em app\testes\dourado\imagens.
- **Prova C FECHADA:** Besta (mv forma <=37,7 s, VRAM <=6.415 MB; mini <=34,1 s; determinismo sha ba8d6cd5.../0dbf7062... repetidos) e Caprileo (mv <=38,8 s, <=6.411 MB; mini <=33,6 s; sha 1b92e3b8.../742df2bd... repetidos); GLB final 49.750 tris em todos os 12 jobs. Somados ao Orc, os 3 personagens passam na bateria inteira.
- **QUAL-01 implementado e medido** (ver ESTADO): 5 perfis com os nomes das classificacoes do RPG; 14 testes novos (suite 218 OK); tabela de custo por nivel no ESTADO_ATUAL.
- **Diretivas novas registradas em DECISOES:** QUAL-02, ANIM-01, MET-01, MET-02 (com trabalho programado de melhoria continua a cada 90 min), MET-03, ARMAZ-01, QUAL-03.
- **Critico visual (primeira passada, Muse):** o Mestre achou e a analise das previas CONFIRMA: o machado do Orc Lenario tem laminas multiplas/fundidas; a referencia tem lamina unica larga. Rosto ainda suave. Silhueta e proporcoes fieis. Caso inaugural da frente de retrabalho local.
- Bateria de variancia do Lenario disparada (varq): Orc sementes 42/1234/repeticao da 7, Besta e Caprileo na semente 7.

## 01/11/2026, ~01:12 - Muse (CM-000009): correcoes da auditoria no 3 do Critico (C3-1 a C3-3)

- **C3-1 (GRAVE, meu erro):** o codigo do QUAL-01 (qualidades.py, test_qualidades.py e os trechos de cli/config/job) tinha ficado FORA do git - funcionalidade no ar e testada, mas nao commitada. Corrigido nesta entrada: add + commit + push dos 5 arquivos, arvore conferida limpa e local == remoto. Reincidencia da classe GIT-01: a licao registrada e commitar o codigo ANTES de anunciar a funcionalidade.
- **C3-2 (MEDIO, meu erro):** faltava a linha QUAL-01 em DECISOES.md (o ESTADO a citava como registrada). Linha incluida com a data real da ordem e a nota da formalizacao tardia. A lista de diretivas da entrada anterior fica corrigida por esta: QUAL-01..03, ANIM-01, MET-01..03, ARMAZ-01.
- **C3-3 (BAIXO):** com o commit feito e a linha registrada, a afirmacao do item 6 no ESTADO volta a ter lastro; a conferencia curta e dirigida do Critico decide o carimbo.
- Espelho do REGISTRO no Drive (G:) segue pendente: nesta noite a pasta G: nao esta lendo (0 bytes/ausente nas leituras); GitHub e a copia local sao o lastro ate o Drive voltar.

## 01/11/2026, ~01:10 - Critico senior: **FASE 1 PRONTA**

- A conferencia curta e dirigida (adendo da auditoria no 3) conferiu C3-1, C3-2 e C3-3 com evidencia propria no git: os itens 6, 7 e 8 da definicao de pronta passam. Somados aos itens 1-5 provados na auditoria no 3 (suite 218, Prova C integral 18/18 com determinismo nas 6 combinacoes, 5 motores, worker/web/MCP vivos, trabalhos arquivados), **a Fase 1 da Oficina3D esta PRONTA** - palavra do Critico, nao do executor.
- Relatorios: docs/CRITICO-fase1-auditoria-3.md e docs/CRITICO-fase1-auditoria-3-adendo.md.
- Isto NAO e o app pronto (QUAL-02): faltam textura/pintura e as demais frentes do backlog, e no fim de TUDO o portao MET-03 (tres Criticos senior, baterias diferentes).

## 01/11/2026, ~01:16 - Muse (CM-000009): estudo das cartas entregue + variancia do Lenario

- **Estudo de melhorias protocolado:** docs/ESTUDO_MELHORIAS.md (478 linhas): inventario fonte a fonte (plano, brief, IBX-178/179/187 com os pareceres do Claude no dossie CM-000008, relatorio central v2, docs vivos, auditorias 1-3, continuidade v002, pesquisa web de 01/11), backlog priorizado P-0/T1-T6/F1-F4/P1-P3 (cada item com ganho, custo, risco, prova de aceite e bateria do Critico), desenho da Etapa COR, protocolo do Critico Visual (secao 7) e rotas de retrabalho local (secao 8), viabilidade da animacao futura (secao 4).
- **Recomendacao da Etapa COR:** projecao das vistas canonicas com bake no Blender como caminho PADRAO (a arte do proprio RPG no modelo, deterministica, custo zero de GPU); Flow como plano B; Hunyuan Paint como plano C opcional (spike T3: a pesquisa mostrou perfis de offload ~6 GB no 2GP). Prioridades: T1 projecao, T2 cor de vertice (parar de descartar a cor que o TripoSR ja entrega), T5 UV, P-0 corpo-base, T3 spike do Paint.
- **Variancia do Lenario (QUAL-03):** Orc s7 = 17.431 KB / forma 1.209.599 tris / 157,2 s; repeticao da s7 BYTE-IDENTICA (sha 7d53a89d...); s42 = 17.232 KB; s1234 = 17.226 KB (forma 1.154.952 tris / 157,1 s). Custo estavel (~157 s, ~6,4 GB) e arquivos variando ~1% entre sementes. Besta Lenario s7: forma 1.102.030 tris / 155,7 s / 17.032 KB. Caprileo Lenario em conclusao ao fechar esta entrada.

## 01/11/2026, ~01:20 - Muse (CM-000009): variancia do Lenario FECHADA

- Caprileo Lenario s7 concluido: forma 1.096.124 tris em 156,1 s, VRAM 6.410 MB, GLB 17.006 KB, final 497.500 tris. A bateria de variancia (QUAL-03) esta completa: Orc (s7 identica na repeticao; s42 e s1234 com custo estavel ~157 s e arquivos ~17,2-17,4 MB), Besta (155,7 s; 17.032 KB) e Caprileo (156,1 s; 17.006 KB) - o nivel Lenario e consistente em custo nos 3 personagens.

## [2026-10-31 23:50 -03] Claude (sessão do CUNHADO-PC) volta do limite de uso
- Os 7 agentes A–G abertos às ~12:30 morreram todos no limite de uso (HTTP 429, "session limit", ~13:00). O trabalho parcial deles já foi integrado pelo Muse no commit `6762003` e evoluído depois. **Decisão: NÃO retomar esses agentes**: eles voltariam com o contexto das 13:00 e sobrescreveriam o código mais novo (o mesmo tipo de erro do N1).
- Conferido ao vivo: `git status` limpo e igual a `origin/main` (`d83335d`); worker e web rodando (tarefas `Oficina3D_Worker`/`Oficina3D_Web`); GPU parada (1105 MiB, 2%); C: 70+ GB livres; `PartCrafter.zip` (7.491.118.361 B) e `DetailGen3D.zip` (3.429.846.267 B) presentes em `G:\Meu Drive\RPG Assimilação\Oficina3D_v2\modelos_guardados\`.
- Procura no Drive (`G:\Meu Drive`, recursiva, nomes `*capr*`, `*besta*`, `*KIT_TESTE*`, 129 s): **o kit dourado do Capríleo e da Besta Cristalina NÃO está no Drive.** Achadas só 5 referências novas em `05 — Imagens e referências\Referências visuais\2026-10-31_RPG_besta-*.jp*g` (enviadas às 23:45; "besta lendária"/"besta do vazio"). **Não usadas** como insumo da Prova C: não são o kit de 27/10 com as vistas nomeadas, e trocar o insumo mudaria a bateria.
- Item 3 continua **PENDENTE**: esperando o Mestre enviar o kit do Capríleo e da Besta Cristalina.

## 01/11/2026, ~02:05 - Muse (CM-000009): diretrizes REF-01, APR-01, CORPO-01 e REG-01 + APRENDIZADO_E_FLUXO criado

- **REF-01 (ordem do Mestre, 01:54):** frente permanente de referencias registrada em DECISOES - recriar seres vivos do RPG da arte existente (personagens em PNG, T-pose com pernas um pouco afastadas + angulos do mesmo personagem; monstros na pose adequada a modelagem), SEM mudar caracteristicas; arsenal de cobaias para testes reais do app; Critico em todas as fases. Lote 1 (Orc) executado nesta mesma tranche, em entrada propria.
- **APR-01 (01:54):** criado docs/APRENDIZADO_E_FLUXO.md - fluxograma geral do trabalho, protocolo REG-01, protocolo de antecipacao (checklist pre-Critico), diario de licoes semeado com os casos reais (N1, C3-1, C3-2/C3-3, machado do Orc Lenario, helpers-SSH via STDIN, /tmp da VM apagado em restart, espelho do Drive com hash, decimacao x motor) e a regra de escalada do Critico (cada bateria nova adiciona >= 1 verificacao nova, registrada na propria bateria).
- **CORPO-01 (01:56):** prioridade reordenada - construir o CORPO (Etapa COR primeiro); testes validam cada parte nova ao nascer, sem multiplicar testes sobre o esqueleto aprovado.
- **REG-01 (01:57):** plano valido = o escrito nos documentos. Esta tranche ja nasce sob o protocolo: comecou relendo ESTADO/DECISOES/ESTUDO dos arquivos e termina com o plano atualizado por escrito.
- **ESTADO_ATUAL atualizado nesta tranche:** cabecalho (Fase 1 PRONTA), secao da definicao de pronta corrigida (os 8 itens conferidos na auditoria 3 + adendo) e "Pendencias conhecidas" substituida por "Proximos passos" com o estado real (COR primeiro; REF-01 em andamento; APR-01 criado; machado como caso inaugural do retrabalho local; guardiao do notebook adiado; portao MET-03 so no fim de tudo).

## 01/11/2026, ~02:15 - Muse (CM-000009): REF-01 lote 1 (Orc) gerado e instalado - aguarda o Critico Visual

- **Fonte:** testes/dourado/imagens/orc_frente.png (1280x1820, RGBA, sha256 30c0f83d3ede10fd...) - a arte dourada do Orc. Geracao pelo gerador de imagem do proprio Muse (a rota mais economica em tokens: sem orquestrar outra IA), 3 geracoes neste lote.
- **Divergencia consciente:** o BRIEF de 27/10 pedia corpo-base SEM armadura; a ordem REF-01 do Mestre manda NAO mudar as caracteristicas. Vale a ordem nova: Orc como ele e, so muda a pose; o machado fica fora da pose.
- **Entregues** (em app/testes/referencias/, FORA do git - .gitignore linha 22, *.png; git check-ignore conferido nos 3; copias locais em ~/workspace/oficina-audit/referencias/):
  - orc_tpose.png - 1328x1904, 1.614.418 B, sha256 1a82f46a2b9d911f... - Orc em T-pose, fundo cinza-claro uniforme, corpo inteiro com margem.
  - orc_angulos.png - 2544x960, 2.654.580 B, sha256 2f1103055d63fb71... - folha de angulos (frente, 3/4 e perfis).
  - orc_costas_ref.png - 1328x1904, 2.095.521 B, sha256 7b523cad0e669072... - vista de costas avulsa, gerada porque a folha nao trouxe as costas.
- **Leitura honesta do executor (antecipacao, APR-01; quem julga e o Critico):** (detalhe na secao 6 do APRENDIZADO_E_FLUXO)
  - T-pose: identidade e equipamento fieis; bracos ~20-25 graus abaixo da horizontal ("T" relaxada), dedos macios/parcialmente fundidos, tecido vermelho da cintura tocando as coxas por dentro.
  - Folha: FALTOU a vista de costas pedida e um perfil saiu quase duplicado (MIS - o desvio mais grave do lote); a consistencia cruzada das vistas presentes e boa.
  - Costas avulsa: coerente no conjunto, mas a peca de lobo saiu no ombro ESPELHADO em relacao a fonte (SYM); bolsinhas no cinto sao completacao nao pedida (EXT leve).
  - Estilo gerado mais liso que a textura da arte-fonte; cores e desenho fieis. NENHUMA imagem foi aprovada pelo executor: sao insumo de teste aguardando o Critico Visual e a palavra do Mestre.
- **Proximo passo (plano escrito):** Critico Visual do lote 1 (bateria na secao 6 do APRENDIZADO_E_FLUXO); em paralelo de prioridade, a Etapa COR (CORPO-01); lote 2 da REF-01 = Besta Cristalina.

## 01/11/2026 - Critico Visual senior (independente): REF-01 lote 1 (Orc) - LOTE REPROVADO no criterio de aceite

- **Relatorio completo:** docs/CRITICO-ref01-lote1.md (bateria da secao 6 do APRENDIZADO_E_FLUXO item a item, com evidencia visual e medicoes; tabela de defeitos D1-D14 na taxonomia do protocolo).
- **Vereditos por imagem:** orc_tpose.png REPROVADA (D1 MIS S2 - massa de pele do ombro direito perdida); orc_angulos.png REPROVADA (D7 MIS S2 - folha sem a vista de costas); orc_costas_ref.png REPROVADA (D10 SYM S2 - personagem INTEIRO espelhado: lobo E ombreira de espinhos trocados de lado).
- **Correcoes as confissoes do executor:** (1) angulo dos bracos MEDIDO por regressao sobre a silhueta: ~30 graus abaixo da horizontal (31,6/29,9), nao 20-25; (2) a afirmacao "ombreira no lado certo" nas costas foi REFUTADA - o espelhamento e do personagem inteiro; (3) bolsinha EXT tambem existe na folha (D9), nao so nas costas avulsas.
- **Escalada APR-01 desta bateria (verificacao nova):** amostragem quantitativa de paleta por classe de cor (mediana RGB de pele verde e de tecido vermelho, fonte x geradas) - paleta FIEL (vermelho delta 3 na T-pose; pele delta 41 = levemente mais clara; folha delta 17; costas delta 10); o desvio de estilo do lote e de TEXTURA (grao), nao de cor. Medicao geometrica de pose tambem incorporada a bateria.
- **Retrabalho exigido (especificacao no relatorio):** T-pose v2 com pele do ombro direito restaurada, bracos a 90 graus e dedos separados; folha de angulos abandonada em favor de vistas AVULSAS; costas v2 com ancoras de lado explicitas, sem bolsinhas e com a alca diagonal. Todos os defeitos ABERTOS; a palavra final de fidelidade e do Mestre.

## 2026-11-01 (madrugada) - REF-01 lote 1: RETRABALHO v2 executado
- Executor: Muse (agente principal), seguindo a especificacao do CRITICO-ref01-lote1. Geradas a partir das fontes douradas (frente sha256 30c0f83d..., costas sha256 256c8a2f...) e instaladas em testes/referencias/ (fora do git, como manda a regra): orc_tpose_v2.png (sha256 26da22e2...), orc_costas_v2.png (sha256 09890d74...), orc_tresquartos_v2.png (sha256 7c9d9465...).
- O que cada uma ataca: T-pose v2 = D1 (pele dos ombros no pedido), D2 (bracos a 90 graus, T rigorosa) e D3 (maos abertas, dedos separados); costas v2 = D10 (ancoras explicitas: lobo a ESQUERDA da imagem, ombreira de espinhos a DIREITA), D11 (cinto sem bolsinhas), D12 (alca diagonal presente), sem machado; folha abandonada (D7/D8) - vistas avulsas, com o 3/4 como vista nova do conjunto.
- Leitura de antecipacao do executor (o julgamento e do Critico): costas v2 e 3/4 conferem com todas as ancoras e com a fonte; na T-pose v2, bracos e dedos estao corrigidos, mas a massa de pele do ombro direito segue MAIS FINA que a da fonte (a ombreira assenta quase sobre o ombro nu) - D1 possivelmente reduzido, nao necessariamente fechado; o Critico mede.
- Estado: aguardando a rodada 2 do Critico Visual (bateria escalada, APR-01). Defeitos D1-D14 seguem ABERTOS ate o veredito.

## 01/11/2026, ~02:40 - Critico Visual senior (rodada 2, independente): REF-01 lote 1 v2 - LOTE APROVADO

- **Relatorio completo:** docs/CRITICO-ref01-lote1-v2.md (bateria da secao 6 do APRENDIZADO_E_FLUXO adaptada as vistas avulsas + verificacoes herdadas + verificacoes novas da escalada APR-01, com zooms e script de medicao arquivados com o executor em hidden_files/critico-v2/).
- **Vereditos por imagem:** orc_tpose_v2.png APROVADA (com ressalvas D5 e D15); orc_costas_v2.png APROVADA (sem ressalva de lado); orc_tresquartos_v2.png APROVADA (sem ressalva). **LOTE APROVADO no criterio de aceite (nenhum defeito S1/S2 de fidelidade).** As tres vistas entram no arsenal de referencias do Orc como insumo de modelagem. A palavra final de fidelidade artistica e do Mestre.
- **Medicoes decisivas:** bracos da T-pose v2 a 3,18/1,88 grau abaixo da horizontal (v1: ~30) - D2 FECHADO; dedos contados com zoom, 5 + 5 separados e articulados - D3 FECHADO; massa de pele no ombro direito do personagem presente - D1 FECHADO; auditoria de lado 16/16 ancoras APROVADAS (lobo, ombreira, 2 braceletes, capa, pes, alca diagonal, ausencia de bolsinhas) nas costas v2 e no 3/4 v2 - D10/D11/D12/D13 FECHADOS; folha defeituosa abandonada - D7/D8/D9 FECHADOS por superacao; D6 FECHADO (maos grandes como na fonte).
- **Tabela D1-D14 apos a rodada 2:** FECHADOS D1, D2, D3, D6, D7, D8, D9, D10, D11, D12, D13; REDUZIDOS D4 (S3 -> S4, painel do saiote entre as pernas, faces internas legiveis) e D14 (S4, textura mais lisa que a fonte); D5 MANTEM S3 (pele da T-pose v2 mais clara: delta 49 no peito, 60 na imagem inteira; vermelho fiel, deltas <= 19; pele fiel na 3/4, delta 16, e nas costas, delta 20 por regiao).
- **Defeito novo:** D15 (DEF S4) - palmas da T-pose v2 voltadas para a frente, nao para baixo; sem impacto de modelagem, mas vira convencao explicita nos pedidos dos proximos lotes (licao L-09 no APRENDIZADO_E_FLUXO).
- **Escalada APR-01 desta bateria (verificacoes novas):** (a) contagem de dedos por mao com zoom; (b) simetria espelhada medida da silhueta (IoU mascara x espelho = 0,809; extensoes 653 px de cada lado); (c) auditoria de ancoras de lado, ancora por ancora, nas costas v2 E no 3/4 v2.
- **Pendencias nomeadas (nao bloqueiam o uso):** D5 (S3) - para TOM DE PELE, a autoridade continua sendo a frente canonica, nao a T-pose v2; D15 (S4) - convencao de palmas; D4/D14 (S4) - cosmeticos.
- **Correcao ao executor:** a antecipacao dizia que a massa de pele do ombro direito seguia "mais fina que a da fonte" e que D1 estava "possivelmente reduzido" - o Critico mediu e FECHOU D1 (massa espessa presente, como na fonte). A antecipacao subestimou a correcao; o veredito do Critico vale.
- **Fechamento da etapa:** REF-01 lote 1 (Orc) FECHADO. Proximo sujeito do arsenal: Besta Cristalina (lote 2). Em paralelo de prioridade, a Etapa COR (CORPO-01): levantamento desta tranche confirma Blender 5.2 instalado e infra headless reutilizavel (refino/_blender_refino.py e previa/_blender_previa.py com cameras ortograficas calibradas nos 8 angulos) para o T1.
- **Registro previo desta tranche (antes do veredito):** entrada do retrabalho v2 commitada e pushada como a079791 apos diff conferido (estava pendente sem commit - licao C3-1 aplicada antes de convocar o Critico); hashes SHA-256 das 3 vistas v2 e das 2 fontes conferidos integralmente; Drive G: voltou a ler (43,6 GB livres), destravando o espelho desta etapa.
- **Espelho no Drive (ARMAZ-01, apos o veredito):** REGISTRO.md, ESTADO_ATUAL.md e CRITICO-ref01-lote1-v2.md copiados para Oficina3D_v2/REGISTRO no Drive (G:) e conferidos por SHA-256 na volta: REGISTRO 7A7A20D6..., CRITICO 9CC14ADC..., ESTADO EE713478... - os tres identicos a origem. O espelho desta etapa esta validado (nas tranches anteriores o G: nao lia; nesta voltou a ler).

## 01/11/2026, ~04:30 - Muse (CM-000009): Etapa COR, T1-mecanismo executado (aguarda Critico)

- **Escopo desta tranche (CORPO-01):** construir o mecanismo do T1 (projecao das vistas canonicas com bake), nao o T1 completo: a integracao como etapa da fila de jobs fica como proximo passo, apos o veredito do Critico. Codigo novo em `app/oficina3d/cor/` (padrao do refino): `projecao.py` (matematica pura: cameras iguais as de `refino/previa.py`, peso por facing, rasterizacao por triangulo UV, dilatacao, metricas de UV), `_blender_cor.py` (headless: BVH para oclusao, bake, GLB com material + textura embutida, previas Workbench TEXTURE) e `__init__.py` (`rodar_cor` via `previa.rodar_blender`); testes em `app/testes/test_cor.py` (15 testes, todos em matematica pura).
- **Decisoes de desenho v1 (COR-01, em DECISOES):** alinhamento por silhueta (caixa da mascara da arte mapeada por afinidade sobre a caixa da malha projetada; IoU residual medido); facing minimo 0,05; dilatacao v1 = cor vizinha mais proxima, padrao 256 passes (cobre o interior das zonas cegas; o que restar sem cor e reportado, nunca escondido); se a malha nao tem UV, o bake gera Smart UV (mesmos parametros do refino) e reporta `uv_gerada_no_bake`; textura padrao 1024 px.
- **Prova sintetica (bateria T1 item 7) - PASSOU:** cubo com Smart UV + 4 vistas de cor solida (frente=vermelho, costas=azul, esquerda=verde, direita=amarelo). Resultado: 4/4 faces laterais com a cor EXATA da sua vista (tolerancia 0,05; 2 amostras por face), IoU de silhueta 1,0 nas 4 vistas, GLB com 1 imagem embutida e material com textura, previas renderizadas (frente vermelha solida confere o caminho Workbench TEXTURE). Tempo 1,5 s. SHA-256 textura 32cc0955097d03fc61629e152395e14cb2bf7176ecae1ace64ba40217e625c8e; GLB 328610b7e11f27f261470ae2f98fdef5cb250677ba2fd3f55fd43abfc0af6931. Zonas cegas do cubo (topo/base, 33,33%) comportam-se como o previsto.
- **Prova real - Orc dourado (Prata, 49.750 tris):** entrada = `jobs/20261031-225432-provac-orc-s7/saida/modelo.glb` (o GLB refinado com UV; o `refino/limpa.glb` e a entrada do refino via pymeshlab e NAO tem UV - erro de entrada achado e corrigido nesta tranche). Vistas canonicas frente/costas/esquerda/direita de `testes/dourado/imagens/`. Tempo 24,7 s. SHA-256 textura 93c14cc6d4fc274f414fb3dc835e98314904358125a4ea3514ec93a36e0eb212; GLB fe73cf889b32f86152e16caff68dc4b0491bbfb61d852ffc6106305120a8c3bd (hashes conferidos nos arquivos baixados). IoU de silhueta pos-alinhamento: frente 0,7947, costas 0,7241, esquerda 0,793, direita 0,7872. Faces visiveis por vista: 8.789 / 11.135 / 8.426 / 7.503.
- **Cobertura e o gargalo T5 (achado central):** texels UV 42.494; pintados direto so 8.513 (20,03%); cegos antes da dilatacao 33.981 (79,97%); apos 256 passes, 0 sem cor. Metricas de UV (Smart UV do refino): distorcao media 0,10051, ocupacao rasterizada 0,03983, 8.098 ilhas, margem minima 8 px (em 1024). Verificacao independente (decode do GLB, sem Blender): area UV total = 0,0432 (4,32% do quadrado UV, bbox 0..1) - ou seja, ~1 texel por face em 1024 px. Conclusao do executor: o mecanismo funciona, mas a UV atual NAO sustenta detalhe - o T5 (UV de qualidade, menos ilhas, mais ocupacao) e o proximo gargalo, antes de qualquer julgamento de fidelidade fina.
- **Determinismo (bateria T1 item 5) - PROVADO:** 2 runs do Orc com o mesmo pedido deram SHA-256 identicos da textura e do GLB.
- **Suite completa no .venv_app do PC:** 233 testes OK, 0 falhas, 0 erros, skipped=1 (218 anteriores + 15 novos do test_cor). Runner dedicado `jobs_teste/cor_t1/run_suite.py` (a tarefa com cmd.exe falhou 2x por cwd/citacao - licao registrada).
- **Bugs achados e corrigidos nesta tranche:** (1) no Blender 5.2, `BVHTree.ray_cast` sem acerto devolve `(None, None, None, None)`, nao `None` - o teste de oclusao quebrava; (2) cubo sintetico sem `transform_apply`: vertices locais vs BVH em mundo deslocavam o enquadramento e a oclusao; (3) entrada errada (`limpa.glb` sem UV) + fallback Smart UV no bake.
- **Leitura do executor (antecipacao; quem julga e o Critico):** nas 4 previas, o Orc e reconhecivel (silhueta, pose, verde da pele, vermelho do tecido, armadura escura), mas a textura sai fragmentada em "confete" de cores, sem detalhe legivel, com grandes areas pretas nas laterais (dilatacao a partir de vizinhos escuros) e uma mancha branca no antebraco da vista de frente. Itens da bateria T1 ainda pendentes: adversarial com a Besta (menor resolucao) e com vista faltante (item 6), e a integracao a fila. Nada disso e apresentado como "T1 concluido": o que fecha nesta tranche, se o Critico aprovar, e o T1-mecanismo.
- **Estado:** codigo + testes + docs desta tranche commitados e pushados antes de convocar o Critico (licao C3-1). Critico senior com bateria T1 + escalada APR-01 convocado apos o commit; veredito pendente. Espelho no Drive (ARMAZ-01) apos o veredito.

## 01/11/2026, ~04:50 - Critico senior (independente): T1-mecanismo APROVADO

- **Relatorio completo:** docs/CRITICO-t1-mecanismo-relatorio.md (bateria T1 item a item + escalada APR-01, com medicoes proprias). **Veredito: APROVA o T1-mecanismo** (nao o T1 completo, nao a fidelidade de detalhe do Orc, nao o determinismo como provado de forma independente na primeira versao).
- **O que o Critico confirmou por conta propria:** sintético 4/4 cores exatas; SHAs da textura Orc (93c14cc6...eb212) e do GLB (fe73cf88...8c3bd) conferidos por sha256sum; GLB decodificado sem Blender (TEXCOORD_0, 1 imagem PNG embutida, material com textura, 49.750 tris); area UV confirmada em 4,324% (media 0,91 texel/face, 61,7% das faces com <1 texel) - a fragmentacao do Orc e explicada pela UV, nao por erro de projecao; nenhum atravessamento detectado (prova forte = controle sintetico; teste-espelho do Orc fraco pela sobreposicao de paletas, declarado como tal); nenhuma alegacao numerica verificavel errada; nenhum defeito de codigo que invalide os resultados (ray_cast, transform_apply e fallback examinados e corretos). Nenhum defeito S1.
- **Defeitos e pendencias (classificacao do Critico):** S2 - D1 fidelidade de detalhe ausente no Orc (rosto/peitoral ilegiveis, laterais piores; bloqueia qualquer "T1 pronto" ate o T5), D2 adversarial pendente (Besta em menor resolucao, vista faltante). S3 - D3 trilha de determinismo insuficiente, D4 teste mal nomeado, D5 IoU sintetico vacuo, D6 lacunas de teste, D7 costura nao avaliavel nesta UV. S4 - D8 (iou vazia, verificacao GLB so materials[0], fallback sem prova, oclusao por centroide, empate de facing), D9 (limites da auditoria), D10 (previas Workbench sombreadas: fidelidade futura amostra a textura, nao a previa).
- **Correcoes executadas nesta mesma tranche (pos-veredito):** D3 FECHADO com re-prova guardada - 2 runs novos do Orc (artefatos `jobs_teste/cor_t1/orc/resultado_detA.json` e `resultado_detB.json`, copias em hidden_files/orc-determinismo/): ambos com SHA textura 93c14cc6... e GLB fe73cf88..., identicos aos runs anteriores, inclusive com o `_blender_cor.py` atualizado (a mudanca foi so na verificacao do GLB, nao no bake). D4 FECHADO - teste renomeado para `test_empate_mantem_primeira_fonte` + teste verdadeiro `test_maior_facing_vence_entre_vistas` (normal inclinada 0,894 frente x 0,447 esquerda, vence nos dois pedidos). D6 FECHADO - 5 testes novos (mascara rejeita, UV degenerada, borda da dilatacao, distorcao != 0, alinhamento com aspectos distintos). D8 PARCIAL - `iou` com uniao vazia agora retorna 0,0 (com teste) e `verificar_glb_texturizado` olha qualquer material com textura; fallback Smart UV segue sem prova de execucao (pendencia de prova). D5 - correcao de leitura registrada aqui: o IoU sintetico 1,0 NAO prova acordo de silhueta (mascara solida estica qualquer geometria para 1,0); a prova sintetica valida e a cor exata.
- **Pendencias registradas (nao bloqueiam o mecanismo):** D1 (resolve-se com o T5), D2 (adversarial do T1-completo), D7 (costura volta a ser testavel com UV de qualidade), D8 resto (oclusao por centroide, empate de facing), D9/D10 (notas de auditoria e de metodo para as proximas baterias).
- **Fechamento da etapa:** T1-mecanismo FECHADO com aprovacao do Critico. Suite apos as correcoes: 240 testes OK no .venv_app (218 + 22 do test_cor), 0 falhas, skipped=1, log em jobs_teste/cor_t1/suite.log. Proximo passo obrigatorio antes do T1-completo (ordem do Critico, aceita): T5 (UV de qualidade) + D2. Espelho no Drive (ARMAZ-01) apos este commit.

- **Espelho no Drive (ARMAZ-01, apos o veredito):** REGISTRO.md, ESTADO_ATUAL.md e CRITICO-t1-mecanismo-relatorio.md copiados para Oficina3D_v2/REGISTRO no Drive (G:) e conferidos por SHA-256 na volta (prefixos de 8 digitos iguais nos 3 arquivos: REGISTRO 6D48DB97, ESTADO B52F78D1, CRITICO 0FCFD335). O espelho desta etapa esta validado.
## 01/11/2026, ~06:00 - Muse (CM-000009): Etapa COR, T5 - UV de qualidade com xatlas (aguarda Critico)

- **Escopo desta tranche (CORPO-01, ordem do Critico do T1-mecanismo):** o gargalo medido no T1 era a UV: o Smart UV do refino fragmenta o Orc Prata em 8.098 ilhas que ocupam 4,32% do quadrado UV (~0,91 texel/face em 1024 px). O T5 troca a UV, nao a projecao. Codigo novo commitado e pushado como ac8c15a antes de convocar o Critico (licao C3-1): `app/oficina3d/uv_xatlas.py` (lado .venv_app: trimesh + xatlas -> .npz com vmapping/indices/uvs) e `app/oficina3d/cor/_blender_uv_xatlas.py` (Blender: aplica o .npz como UV por loop e exporta o GLB com a UV nova); testes em `app/testes/test_uv_xatlas.py` (4 testes, OK no .venv_app).
- **Experimento, rodada 1 - 7 estrategias no mesmo Orc Prata (artefatos em `jobs_teste/cor_t5/`, fora do git):** smart66 (linha de base, reproduzida exatamente: distorcao 0,10051, ocupacao 0,03983, 8.098 ilhas, 0,911 texel/face, 61,68% das faces com <1 texel); smart89 (pior em tudo: ocupacao 0,01361, distorcao 0,25529, 13.525 ilhas); smart66_pack (ocupacao 0,07831, distorcao inalterada 0,10051); smart66_avg_pack (ocupacao 0,07356, distorcao 0,07005); unwrap_conformal (ocupacao 0,17489, distorcao 0,57613); unwrap_angle (ocupacao 0,17675, distorcao 0,48249); lightmap_pack (erro de API: `pref_context` nao existe nessa forma no Blender 5.2 - estrategia descartada sem conclusao). Conclusao da rodada 1: `pack_islands` nao reescala as ilhas (so rearranja), e o unwrap do Blender nao resolve: ocupa 4x mais que o Smart UV ao custo de 5x mais distorcao.
- **Experimento, rodada 2 - controle sem costuras + spike xatlas:** o controle (limpar todas as costuras antes do unwrap) devolveu metricas IDENTICAS as do unwrap com costuras ate a 5a casa (conformal 0,57613/0,17489, angle 0,48249/0,17675, ilhas 8.098 nos dois) - a hipotese "o importador glTF marca as costuras do Smart UV e o unwrap as reutiliza" NAO se sustenta neste controle; o numero de ilhas travado em 8.098 em todas as estrategias Blender segue NAO EXPLICADO e foi entregue ao Critico como anomalia aberta (nao afeta a decisao T5, que nao depende do Blender). O spike xatlas (trimesh + xatlas no .venv_app, que ja tinha o pacote instalado): distorcao 0,08787 (MENOR que o Smart UV), ocupacao 0,61398 (15,4x a linha de base), 6.578 ilhas, 12,937 texels/face, 0,33% das faces com <1 texel, 26,6 s incluindo o carregamento do GLB. Ressalva: margem minima 1 px em 512 px (4 px em 2048) - ABAIXO da regua sugerida pelo estudo (>=8 px em 2048); a dilatacao de 256 passes do bake e o que hoje segura o vazamento nas costuras, e o Critico foi chamado a julgar esse risco.
- **Prova completa T5 (runner `jobs_teste/cor_t5/run_t5.py`, via tarefa agendada):** (1) xatlas no GLB refinado -> `orc_xatlas/uv.npz`; (2) Blender aplica a UV -> `orc_xatlas/modelo_uv.glb` com metricas medidas NO Blender IDENTICAS ao spike (ocupacao 0,61398, distorcao 0,08787) - a correspondencia de ordem das faces entre trimesh e Blender esta PROVADA por essa igualdade, nao assumida; (3) bake COR do T1 sobre o GLB com UV nova -> `orc_xatlas/modelo_cor.glb`, `textura.png` (SHA 794ced3d...), `previas/` com as 4 vistas. Resultado do bake: IoUs IDENTICOS ao bake Smart UV (frente 0,7947, costas 0,7241, esquerda 0,793, direita 0,7872) e mesmas contagens de faces visiveis - a geometria nao mudou; texels pintados direto 121.567 (antes 8.513, 14,3x); texels UV 643.613 (antes 42.494); cegos antes da dilatacao 81,11% (antes 79,97% - a fracao cega quase nao caiu porque a area UV cresceu 15x junto com o pintado; o ganho esta na resolucao por face, nao na fracao coberta); 0 texels sem cor apos a dilatacao; tempo 23,87 s.
- **Leitura do executor (antecipacao; quem julga e o Critico):** comparacao A/B das previas frente (Smart UV em `cor_t1/orc/previas/` x xatlas em `cor_t5/orc_xatlas/previas/`): a xatlas ELIMINA os defeitos mais visiveis do bake anterior (grandes areas pretas nas laterais, mancha branca no antebraco) e as pernas/pele de lobo leem melhor, mas o torso continua em mosaico de manchas deslocadas. A T5 fecha o gargalo de RESOLUCAO (0,91 -> 12,94 texels/face); a fidelidade de detalhe D1 segue ABERTA, e o gargalo visivel agora e outro: alinhamento por silhueta (afinidade) + divergencia entre a geometria gerada e a arte de referencia. Nenhuma alegacao de "detalhe fiel" e feita nesta tranche.
- **Bugs e licoes desta tranche:** (1) `np.load` de .npz mantem o arquivo aberto - no Windows, o TemporaryDirectory do teste falhava ao apagar o .npz (PermissionError WinError 32); corrigido fechando com `with np.load(...) as dados` (teste 4/4 OK apos a correcao). (2) Tarefa agendada com trigger Once + Start-ScheduledTask dispara DUAS vezes (a primeira rodada do experimento sobrescreveu o resultado parcial da segunda) - regra nova: tarefa de run unico usa Start-ScheduledTask SEM trigger, ou trigger sem Start, nunca os dois. (3) `echo "..."` no bash expande `$variavel` antes do PowerShell ver o comando - variaveis PowerShell em chamadas via helper exigem aspas simples externas.
- **Veredito do Critico senior (01/11/2026, relatorio em docs/CRITICO-t5-relatorio.md): T5 APROVADA como passo de UV.** Nenhum defeito S1. O Critico confirmou por conta propria (decode proprio do GLB, sem Blender): metricas do `modelo_uv.glb` identicas as alegadas (distorcao 0,08787, ocupacao 0,61398, 6.578 ilhas, 12,937 texels/face, 0,33% com <1 texel); identidade geometrica PROVADA sem ressalva (49.750 faces identicas na ordem e como multiconjunto, diferenca maxima de posicao 0,0; UV por face casa com o .npz sob flip V com erro maximo 2,98e-08); determinismo do passo xatlas PROVADO (3 reexecucoes, arrays .npz bit a bit identicos); suite 244 testes OK, 0 falhas, skipped=1, contagem arquivo a arquivo; nenhum defeito de codigo que invalide os resultados. A/B de previas confirma as alegacoes do executor por regiao (mancha branca do braco esquerdo sumiu; quase-preto frente 27,75% vs 33,03% no Smart, direita 31,13% vs 37,51%; costas/esquerda em empate tecnico, sem massas pretas solidas) e confirma que o torso segue em mosaico - D1 segue aberto, com o gargalo isolado (alinhamento + geometria-vs-arte). Amostragem da textura (D10): peito frente mediano [104,70,50], mesma familia quente da arte canonica; sem troca grosseira de regiao; contraste entre faces vizinhas 2,3 (Smart, borrado) -> 28,9 (xatlas).
- **Defeitos e pendencias (classificacao do Critico):** S2 - D-T5-1 margem 1 px em 2048 vs regua >=8 px (falha por 8x; a dilatacao de 256 passes compensa visualmente no nivel base mas mascara o problema, e sob mipmapping vira halo - pendencia OBRIGATORIA antes do T1-completo); D-T5-2 guarda de ocupacao ausente no script Blender (vivia so no runner) - FECHADA nesta mesma tranche apos o veredito (ver abaixo); D1 herdado do T1 (fidelidade de detalhe ausente - bloqueia qualquer "T1 pronto"). S3 - flip V nao documentado no contrato .npz↔GLB (documentado nesta tranche nos dois modulos); vertices nao preservados pelo Blender (63.948 -> 64.044 -> 64.093; correspondencia e por face/loop, nunca por vertice); multi-geometria silenciosa no lado Blender (join sem checar ordem; sem impacto no GLB atual de 1 geometria); margem do bake 2 @512 vs spike 1 @512 (metodo, nao dado); coincidencia das 8.098 ilhas nao-explicada. S4 - silhuetas xatlas/Smart diferem <=0,3% (limiar de mascara); lightmap_pack fora do escopo. Limites declarados pelo Critico: IoUs do bake e tempo 23,87 s conferidos no arquivo, nao reexecutados (mas consistentes: texels 121.567 = 14,3x os 8.513 do Smart, igual a razao de texels/face 14,2x); hashes conferidos: textura 794ced3d... e modelo_cor.glb 7730405e... iguais aos alegados; modelo_uv.glb 3c3a73db... (novo, para registro).
- **Anomalia do controle sem costuras - EXPLICADA pelo Critico (sonda Blender 5.2.3, ok=True):** o GLB importado tem 0 costuras em 100.809 arestas (o importador glTF nao cria flags de costura); limpar costuras foi 0->0 (braco-controle vacuo); unwrap com/sem limpeza produziu UVs bit a bit identicas (diferenca maxima 0,0). Nao afeta a T5 (que nao usa costuras nem unwrap). Segue NAO-EXPLICADO por que unwrap e Smart dao exatamente 8.098 ilhas - registrado como nao-explicado, sem inventar causa.
- **Correcao pos-veredito (D-T5-2 FECHADO):** `_blender_uv_xatlas.py` agora aceita `ocupacao_esperada` (+ `tolerancia_ocupacao`, padrao 0,02) no pedido e falha (ok=False, exit 3) quando a ocupacao medida diverge; `uv_xatlas.py` e o script Blender documentam o flip V (`v_glb = 1 - v_npz`). Prova nos dois sentidos via tarefa agendada `Oficina3D_T5Guard` (sem trigger, so Start; removida apos o uso): com esperada 0,61398 passou (medida 0,61398); com esperada 0,10 falhou como esperado (ValueError, exit 3). O runner `run_t5.py` ja comparava a ocupacao; a guarda agora vive tambem no script, como a docstring prometia.
- **Estado:** codigo da T5 commitado e pushado como ac8c15a antes do Critico; correcao D-T5-2 + este registro + relatorio do Critico seguem em commit apos o veredito. T5 FECHADA como passo de UV. Proximo passo obrigatorio antes do T1-completo (ordem aceita): D-T5-1 (margem) + D2 (adversarial).
- **Espelho no Drive (ARMAZ-01, apos o veredito):** REGISTRO.md, ESTADO_ATUAL.md e CRITICO-t5-relatorio.md copiados para Oficina3D_v2/REGISTRO no Drive (G:) e conferidos por SHA-256 na volta (prefixos de 8 digitos iguais nos 3 arquivos: REGISTRO 65CBC0D7, ESTADO D1F84F55, CRITICO C6D8B77E). O espelho desta etapa esta validado.

## 01/11/2026, ~07:34 - Muse (CM-000009): Etapa COR, D-T5-1 - gutter real na UV xatlas (aguarda Critico)

- **Escopo (ordem do Critico T5, aceita):** a margem minima entre ilhas estava
  abaixo da regua (>= 8 px em 2048). O padrao anterior (padding 0) media
  1 px em 512 e em 1024. A correcao e padding real no empacotamento xatlas.
- **Experimento 1 - varredura de padding no Orc Prata**
  (`jobs_teste/cor_margem/resultado_exp.json`, tarefa Oficina3D_MargemExp):
  baseline reproduzida exatamente (ocupacao 0,61398, distorcao 0,08787,
  6.578 ilhas, 12,937 texels/face, margem 1@512 e 1@1024); padding 8@2048:
  margem 2@512, 4@1024 e **9@2048 (medicao direta) - REGUA CUMPRIDA**,
  ocupacao 0,23332, texels/face 4,92, distorcao 0,07446, ilhas 6.578
  (inalteradas); padding 12: margem 5@1024, ocupacao 0,161, texels 3,39;
  padding 16: margem 6@1024, ocupacao 0,117, texels 2,46.
- **Achado central (custo geometrico do gutter):** com 6.578 ilhas pequenas,
  o gutter de 8 px em 2048 custa mais area UV que as proprias ilhas
  (perimetro total x gutter); o empacotador reduz a escala para caber:
  ocupacao 0,614 -> 0,233. A troca e real e foi medida, nao assumida. O
  numero de ilhas nao muda e a distorcao nao piora (0,0745 vs 0,0879). Em
  1024 (textura do bake), 4,92 texels/face segue 5,4x acima do Smart UV
  (0,91). Em bake 2048, a mesma UV daria ~19,7 texels/face - registrado
  como dado, nao como mudanca de padrao (o bake segue em 1024).
- **Experimento 2 - max_cost do charting** (`resultado_exp2.json`, tarefa
  Oficina3D_MargemExp2): max_cost 4: 5.365 ilhas, ocupacao 0,253, texels
  5,33, distorcao 0,0720; max_cost 8: 4.575 ilhas, ocupacao 0,268, texels
  5,65, distorcao 0,0742; max_cost 16: 4.475 ilhas, ocupacao 0,270, texels
  5,69, distorcao 0,0756. **NAO ADOTADO:** ganho modesto (+15% de densidade
  no max_cost 8) ao custo de mudar o charting provado na T5, com risco nao
  medido de distorcao LOCAL (a media nao se move, mas a media nao ve
  estiramento local). Fica registrado como otimizacao futura, com numeros,
  para o Critico julgar.
- **Equivalencia de implementacao** (`resultado_cmp.json`, tarefa
  Oficina3D_MargemCmp): a API Atlas com padding 0 e resolucao 0 e BIT A BIT
  identica a conveniencia parametrize no Orc Prata (vmapping, indices e uvs
  com maxdiff 0,0) - a troca de implementacao em `parametrizar()` e neutra;
  so o padding muda o resultado.
- **Codigo** (commitado e pushado antes do Critico - licao C3-1):
  `oficina3d/uv_xatlas.py` passa a usar a API Atlas com PADDING_PX_PADRAO=8
  e RESOLUCAO_PADRAO=2048, guarda atlas_count==1 (o bake assume uma unica
  textura) e registra padding/resolucao/max_cost nas metricas do gerar_uv.
  Testes novos em `testes/test_uv_xatlas.py` (classe TestUvMargemD_T5_1):
  margem do cubo com o padrao em 2048 >= 8 (medido 15); gap sintetico de
  0,01 UV medido 6 px em 512 (valida o METODO, D-T5-6); gerar_uv registra
  padding 8 e resolucao 2048. Suite: **247 testes OK, skipped=1**
  (240 do T1 + 4 da T5 + 3 novos da D-T5-1).
- **Prova completa** (`jobs_teste/cor_margem/prova/`, tarefa
  Oficina3D_MargemProva, `resultado_prova.json`): (0) determinismo do
  gerar_uv novo - 2 runs com .npz bit a bit identicos (vmapping, indices,
  uvs) e metricas iguais; (1) Blender aplica a UV - metricas IDENTICAS ao
  lado xatlas (ocupacao 0,23287, distorcao 0,07446, ilhas 6.578, margem 2@512,
  texels 4,92), guarda de ocupacao passa (esperada = medida = 0,23287);
  (2) bake COR - IoUs IDENTICOS aos da T5 nas 4 vistas (frente 0,7947,
  costas 0,7241, esquerda 0,793, direita 0,7872) e mesmas faces visiveis -
  a geometria nao mudou; faces pintadas levemente menores (8.723/10.916/
  8.299/7.424 vs 8.778/11.100/8.397/7.498 - efeito esperado da menor
  densidade: menos faces capturam um centro de texel); cobertura: texels
  UV 244.649 (antes 643.613), pintados direto 46.343 (antes 121.567, 38,1%
  = a razao de ocupacao 0,233/0,614), cegos 81,06% (antes 81,11% - a fracao
  cega nao mudou), 0 texels sem cor apos a dilatacao; (3) margens em 2048
  com o MESMO metodo nos dois artefatos (D-T5-6 unificado): **.npz 9 px e
  GLB exportado 9 px** - regua cumprida nos dois; area UV do GLB 0,23341 =
  .npz; 49.750 faces. SHAs: textura 5660c824..., modelo_cor 9aa12f8e...,
  modelo_uv 64782391....
- **Determinismo ponta a ponta do caminho novo** (`det_resultado.json`,
  tarefa Oficina3D_MargemDet): refazer Blender + bake com o mesmo .npz
  devolve os 3 SHAs IDENTICOS (textura, modelo_cor, modelo_uv). O primeiro
  det "falhou" por um artefato do proprio script: o nome da imagem
  embutida no GLB vem do nome do arquivo de saida ("textura" vs
  "textura_det" = +4 bytes) - com os mesmos nomes de arquivo, tudo bate.
  Licao L-21. As previas das rodadas 2 e 3 sao pixel-identicas (0 px
  diferentes na frente) com SHA diferente - metadado PNG do Blender;
  comparacao de previas e por pixels, nao por SHA (licao L-22).
- **Bugs da prova (da prova, nao do passo):** (1) a v1 do run_prova
  comparava `tempo_s` nas metricas e reprovou um passo bit a bit identico
  (licao L-20: determinismo nunca compara relogio); (2) o trimesh nao le
  UV de GLB sem textura (modelo_uv.glb vira ColorVisuals) - a margem do
  GLB foi medida no modelo_cor.glb, cuja UV e a mesma (area UV bate com o
  .npz; o bake nao altera UVs).
- **Leitura do executor (antecipacao; quem julga e o Critico):** A/B das 4
  previas (nova x T5): nenhuma regressao visual - sem massas pretas novas,
  sem mancha branca, mesmas familias de cor; o torso segue em mosaico
  (D1 segue ABERTO, como esperado: o gargalo continua sendo alinhamento +
  geometria-vs-arte, nao densidade). O detalhe fino sai um pouco mais
  macio que na T5, coerente com 4,92 vs 12,94 texels/face - preco medido
  do gutter, nao defeito novo.
- **Estado:** codigo + testes + prova commitados e pushados antes de
  convocar o Critico. D-T5-1 FECHADA como correcao se o Critico aprovar.
  Proximo: D2 (adversarial) + D7 (costura) com a UV nova, depois
  integracao a fila. Espelho no Drive apos o veredito.

## 01/11/2026, ~08:01 - Critico senior (independente): D-T5-1 APROVADA

- **Relatorio completo:** docs/CRITICO-dt51-relatorio.md (SHA-256 BE2B9AF5...,
  conferido apos o scp; scripts e brutos em jobs_teste/critico_dt51/, fora
  do git). **Veredito: APROVA a D-T5-1 como correcao.** Nenhum defeito S1
  ou S2 introduzido pela D-T5-1. D-T5-1 FECHADA.
- **O que o Critico provou por conta propria:** margem pelo metodo do
  executor reproduzida (2@512, 4@1024, **9@2048** - regua >= 8 cumprida) e
  por metodo proprio euclidiano (menor distancia centro-a-centro entre
  bordas de ilhas diferentes = **10,0 px @2048**, com prova de otimalidade
  -> 9 texels vazios reais; a brecha diagonal do metodo linha/coluna nao
  afeta este resultado); determinismo re-executado bit a bit identico ao
  uv_a.npz; metricas reproduzidas (distorcao 0,07446, ocupacao 0,23287@512
  / 0,23332@1024, 6.578 ilhas, 4,92 texels/face, 2,49% < 1 texel); SHAs
  recalculados e iguais (textura 5660c824..., modelo_cor 9aa12f8e...,
  modelo_uv 64782391...); geometria intacta (49.750 faces, ordem
  preservada); UV do GLB exata (modelo_cor.glb casa com o .npz com maxdiff
  2,98e-08); suite rodada por ele (247 testes OK, skipped=1, 33,359 s);
  IoUs conferidos em arquivo (0,7947 / 0,7241 / 0,793 / 0,7872) - o bake
  nao foi re-executado em Blender (limite declarado, como na T5).
- **Escalada APR-01 (verificacoes novas desta bateria):** (1) margem
  euclidiana (acima); (2) distorcao LOCAL: a UV nova e melhor que a T5 em
  todos os percentis (p95 0,275 vs 0,359; p99 0,541 vs 0,627; max 5,01 vs
  12,64; faces com razao >2: 0,070% vs 0,147%) - nenhum estiramento local
  escondido; (3) halo por blocos mistos (teste direto da razao da D-T5-1):
  UV nova = **0 blocos mistos em 2x2 (mip 512) e 4x4 (mip 256)**; T5 = 40
  blocos @2x2 e **5.680 blocos @4x4 (32.292 texels, 22,8% com desvio >30)**
  - o gutter elimina a mistura entre ilhas nos dois primeiros mips;
  (4) faces que perderam tinta: **771 faces perderam todo texel** (0,31%
  da area 3D - so faces miudas, cobertas pela dilatacao), 28 ganharam, 100
  nunca tiveram; faces com exatamente 1 texel saltaram de 319 para 3.468
  (preco a vigiar no T1-completo).
- **Defeitos (classificacao do Critico):** S3 - (a) nota de flip no
  docstring de uv_xatlas.py incompleta (faltava dizer que o caminho do
  bake cancela o flip no modelo_cor.glb) - **CORRIGIDA nesta tranche**
  (docstring atualizado; quem decodificar o modelo_cor.glb NAO aplica o
  flip, quem decodificar o modelo_uv.glb aplica); (b) fragilidade dos
  3.468 faces de 1 texel - vigilancia no T1-completo, sem nova queda de
  densidade sem re-medir; (c) limitacao do metodo de margem linha/coluna
  no codigo - fechada para esta UV pela prova euclidiana, mas baterias
  futuras devem inclui-la como padrao. S4 - resultado_cor.json em prova/
  conferido: e o bake da rodada 3 (faces pintadas 8.723/10.916/8.299/
  7.424); 5 faces degeneradas (iguais na T5 e na nova, sem efeito).
- **Falso alarme do Critico, registrado como licao (nao defeito do
  projeto):** a primeira comparacao de UV do GLB aplicou o flip ao
  modelo_cor.glb e deu maxdiff 1,0; o arquivo passou por DOIS round-trips
  glTF e o flip se cancela - sem flip, casa exato (2,98e-08) na nova e na
  T5. Virou a licao L-23 do diario.
- **Julgamento do preco (ocupacao 0,233): ACEITAVEL, com numeros:** margem
  cumprida por dois metodos; halo eliminado nos mips 512/256; densidade
  restante 5,4x o Smart UV; distorcao local melhorou; max_cost 8 so
  recuperaria +14,9% (5,653 texels/face) ao custo de trocar o charting
  provado - desproporcional. O gutter de 8 px em 2048 e a correcao certa,
  no tamanho certo.
- **Estado:** D-T5-1 FECHADA. Proximo: D2 (adversarial) + D7 (costura) com
  a UV nova, depois integracao a fila. Espelho no Drive validado: REGISTRO 96FFD62D, ESTADO F8E3A2CD, CRITICO 821BD6C9, VERIFICACAO 0AC21EF0 (SHA-256 conferidos na volta, G:).
- **Espelho no Drive (ARMAZ-01, apos o veredito):** REGISTRO.md, ESTADO_ATUAL.md e CRITICO-dt51-relatorio.md copiados para Oficina3D_v2/REGISTRO no Drive (G:) e conferidos por SHA-256 na volta (iguais aos 3 arquivos: REGISTRO 74B414E7, ESTADO 427966BC, CRITICO BE2B9AF5). O espelho desta etapa esta validado.

## 01/11/2026, ~09:00 - D2 + D7 FECHADOS (Etapa COR, apos correcoes do Critico)

- **Prova** (`jobs_teste/cor_d2d7/`, tarefa Oficina3D_D2D7,
  `resultado_prova.json`, PROVA_OK): Besta Cristalina, GLB refinado do
  job provac-besta-s7, UV nova D-T5-1 (padding 8 em 2048) - ocupacao
  0,34946, distorcao 0,08918, 2.419 ilhas, margem 11 px em 2048,
  7,37 texels/face em 1024. Tres bakes COR (dilatacao 256): base 1024
  4 vistas (IoU frente 0,7231, costas 0,7758, esquerda 0,3631,
  direita 0,4085; texels_uv 366.673, direto 140.964, cegos 61,56%,
  sem_cor 0); adv512 (512 px, 4 vistas: IoUs IDENTICOS a base,
  texels_uv 91.610 = 0,2498 da base, sem_cor 0); adv3v (1024 px, 3
  vistas, SEM costas: por_vista com 3 chaves - a ausencia da vista
  esta registrada no proprio resumo, nao e silenciosa; IoUs e faces
  pintadas das 3 vistas restantes IDENTICOS a base; direto 120.658
  (-14,4%), cegos 67,09%, sem_cor 0). SHAs: textura_base 842b461d...,
  textura_adv512 0f0d520a..., textura_adv3v fd856d16....
  Ressalva registrada: IoUs laterais baixos (0,36/0,41) contra
  frente/costas (0,72/0,78) - padrao compativel com a suspeita antiga
  de etiquetas esquerda/direita trocadas nas imagens da Besta (S2-3,
  abaixo); nao contamina D2/D7.
- **Olho do executor (antes do Critico):** previas base frente/costas
  (Workbench, sombreadas - D10, nao provam cor): Besta reconhecivel,
  superficie em mosaico, manchas cinza/magenta - fragmentacao visivel,
  coerente com a metrica D7, sem isolar uma linha de costura. A metrica
  e a prova primaria; a previa e indicio, nao veredito.
- **Veredito do Critico senior (REPROVA o fechamento NESTA tranche,**
  **docs/CRITICO-d2d7-relatorio.md, SHA-256 821BD6C9...):** a medicao
  entregue tinha DOIS erros, e o fenomeno medido estava certo:
  (S2-1) `classificar_arestas` nao soldava vertices por posicao - o
  GLB duplica vertices (split por normal/UV): costura 4.017 de 13.758
  reais, 37.456 "bordas" falsas numa malha fechada; (S2-2) o D2
  sem-costas aplicou `direcao_camera("costas")` (frame Blender, +Y)
  crua as normais glTF e mediu topo/base, nao costas/frente - a
  "separacao fraca" era artefato do eixo errado. O Critico provou por
  conta propria: com solda, costura 13.758 / interna 60.867 / borda 0;
  no eixo correto, D2 sem-costas separa forte (ver republicacao).
  D2-A (512) APROVADO nos numeros. Bake NAO afetado pelo bug de frame
  (dentro do Blender, vetor e normais vivem no mesmo frame). S3-3
  margem 2 vs 11 RESOLVIDA como definicional (512 vs 2048 px); faltavam
  os hashes do GLB de entrada e do .npz. S2-3 (troca esq/dir) segue
  ABERTA e ORTOGONAL: bloqueia a textura base, nao D2/D7. Escalada
  APR-01 desta bateria: reimplementacao independente da costura,
  proxy x media rasterizada, localizacao das piores costuras,
  controle x alvo no sem-costas, cobertura rasterizada independente.
- **Correcoes aplicadas (commit aa2758c, push conferido):**
  `oficina3d/cor/costura.py` solda vertices por posicao (tolerancia
  1e-6) em `classificar_arestas` (parametro `verts`, obrigatorio para
  malha vinda de GLB), ganha `piores_costuras` e nota de frame na
  docstring (licoes L-24/L-25); `testes/test_cor_costura.py` ganha o
  teste de vertice duplicado (o caso que deixou o bug passar) e o
  teste de piores costuras. Testes novos: 7/7 OK; suite completa apos
  a correcao: 252 OK, skipped=1 (log em jobs_teste/cor_d2d7/suite.log).
- **Republicacao SEM novo bake** (`resultado_republicacao.json`,
  REPUBLICACAO_OK; tarefa Oficina3D_D2D7Rep): sobre os MESMOS
  artefatos, com solda e frame corrigido - D7 soldada base: costura
  n=13.758, media 93,49, mediana 77,22, p90 199,86, 78,08% > 30,
  59,90% > 60; interna n=60.867, media 36,20, mediana 13,96, p90
  107,19, 36,61% > 30; classificadas 74.625 (= 3F/2, malha fechada),
  borda 0; adv3v: costura 96,42 / interna 33,65. Solda: 47.476 ->
  24.805 vertices unicos. D2 sem-costas corrigido (glTF, costas =
  (0,0,-1), conversao Blender->glTF (x,y,z)->(x,z,-y)): limiar 0,5,
  alvo 28,23 / 24,01% > 30 vs controle 7,05 / 5,86%; limiar 0,9, alvo
  18,96 / 18,03% vs controle 8,41 / 7,07% - separacao FORTE (o caso ja
  era forte; era a regua que media o eixo errado). Hashes agora
  registrados: glb_refinado_entrada ba8d6cd5..., uv_npz e8b76f32...
  (S3-3 parte de hashes FECHADA). Piores 20 costuras: 325,68-337,17
  (top 1: faces 10776/10979, ponto medio glTF
  [-0.325465, 0.160957, -0.638934]).
- **Previa flat/unlit (ressalva da D7, tarefa Oficina3D_D2D7Flat,**
  **FLAT_OK):** `previas_flat/previa_flat_costura.png` (regiao da pior
  costura) e `previa_flat_frente.png`, material Emission com a
  textura, sem luzes (script `_blender_flat.py`; dois bugs do script
  corrigidos na tranche: cena vazia sem World; motor EEVEE e
  `BLENDER_EEVEE`, nao `_NEXT`). Olho do executor: frente flat mostra
  a fragmentacao na propria textura (sem sombreamento); a regiao da
  pior costura mostra saltos abruptos entre facetas - sem marcacao
  individual, a costura isolada nao e isolavel a olho no meio das
  demais descontinuidades do cristal (limitacao de leitura, registrada
  pelo verificador, nao bloqueio).
- **Verificacao independente (docs/CRITICO-d2d7-verificacao.md,**
  **SHA-256 0AC21EF0...):** reimplementacao propria (parse binario do
  GLB, sem trimesh, sem costura.py) reproduz TODOS os numeros
  corrigidos a casa decimal (D7 soldada, D2 -Z nos dois limiares,
  solda 24.805); o teste de vertice duplicado FALHA no codigo antigo
  (17462aa, TypeError sem o parametro `verts`, e por assercao contra
  stub sem solda) - o teste pega o bug, nao so a assinatura;
  `suite.log` confere 252 OK. Divergencia explicada: top 3 tem empate
  exato em 336,02 (duas costuras) - ordem ambigua, top 1 identico.
  **Veredito final: D2 - FECHADO. D7 - FECHADO.**
- **Estado:** D2 e D7 FECHADOS. Proximo: (c) integracao do `cor` como
  etapa opcional da fila de jobs; depois (d) T2. Pendencias que ficam:
  S2-3 (troca esq/dir, bloqueia a textura base), S3-2 (sem_cor 0 sem
  mascara entregue), S4-2 (resultado_cor.json nativo do bake nao
  entregue), D1 (fidelidade de detalhe do Orc, segue ABERTA). Tarefas
  agendadas da tranche removidas apos o uso (Oficina3D_D2D7,
  D2D7Suite, D2D7Rep, D2D7Flat). Espelho no Drive validado: REGISTRO 96FFD62D, ESTADO F8E3A2CD, CRITICO 821BD6C9, VERIFICACAO 0AC21EF0 (SHA-256 conferidos na volta, G:).

- 2026-11-01 ~09:07 - ESTUDO T3 (Hunyuan Paint) protocolado em docs/ESTUDO_T3_PAINT.md: veredito = spike pratico unico com regua pre-registrada (venv isolado; Orc Prata; perfil mmgp 5->4; aceite: VRAM <= 8188 MB, <= 45 min, SSIM frontal nao pior que o T1, zero OOM). O Paint usa 1 vista e inventa as demais: nao substitui a projecao (T1); papel possivel = Plano C (zonas cegas). Spike entra na fila do backlog.

- 2026-11-01 ~09:1x - REF-01 lote 2 (Besta Cristalina): geracao concluida pelo executor, a partir das fontes douradas (besta_frente/costas/esquerda/direita, 768x512). 3 vistas avulsas instaladas em testes/referencias/ (gitignored; git check-ignore conferido), com copias locais em ~/workspace/oficina-audit/referencias/: besta_diag_esq.png (SHA-256 029259abb429de65...), besta_diag_dir.png (8640c324b45b624c...), besta_topo.png (b35caa6427be50597...) - hashes PC == local conferidos pelo Critico. Pose canonica enrolada (monstro: sem T-pose). Antecipacao do executor: diag_dir a mais forte, porem rasa; diag_esq com bracos segmentados, cristal das costas menor, dentinhos na boca e ambiguidade de lado declarada; topo regenerado 1x (v1 obliqua alta), cabeca ainda elevada. Registro desta geracao ficou PENDENTE na hora (arvore suja: tranche D2/D7 em andamento) e se protocola neste ato, junto do veredito.

- 2026-11-01 ~09:1x - REF-01 lote 2: VEREDITO do Critico Visual senior (docs/CRITICO-ref01-lote2.md) - LOTE REPROVADO no criterio de aceite. besta_diag_dir.png APROVADA (ressalva B7 S3: angulo raso, quase-frente) - entra no arsenal. besta_diag_esq.png REPROVADA: B1 SYM S2 (lateralizacao invertida contra o conjunto canonico: ponta da cauda em x=885/1000, centroide de cristais 0,557, metade esquerda 38,7% contra 56,1% da frente) + B3/B4/B5 (S3: bracos com articulacoes esfericas; franja da boca virando presas; placa de cristal frontal ausente, cobertura de cristal 21,3% contra 32-36% canonicos). besta_topo.png REPROVADA como vista de topo: B2 DEF/MIS S2 (obliqua alta ~40-55 graus, boca 100% frontal - a planta segue faltando no conjunto) + B6 (S3: antebraco direito em espiral). Paleta fiel nas 3 vistas (deltas 9-25 por classe); nenhum defeito S1; nenhum elemento inventado. Escalada APR-01 da rodada: DUAS verificacoes novas (teste de atribuicao das diagonais e teste de pureza da planta) - foram elas que mediram B1 e B2. Retrabalho especificado na secao 6 do relatorio; licao L-26 e item de checklist lancados em APRENDIZADO_E_FLUXO.md.

- 2026-11-01 ~09:1x - REF-01 lote 2: retrabalho (diag_esq v2 + topo v2) EM ANDAMENTO pelo agente principal, pela especificacao da secao 6 do relatorio do Critico; diag_dir aprovada ja utilizavel.

- 2026-11-01 ~09:1x - REF-01 lote 2: RETRABALHO gerado pelo executor, pela especificacao da secao 6 do relatorio do Critico (rodada 1). 2 vistas avulsas novas instaladas em testes/referencias/ (gitignored; git check-ignore conferido), copias locais em ~/workspace/oficina-audit/referencias/: besta_diag_esq_v2.png (SHA-256 cea0262ef59b31c0...) e besta_topo_v2.png (208906f0c6788918...) - hashes PC == local conferidos pelo Critico da rodada 2. A besta_diag_dir.png aprovada fica como membro do conjunto. Autotestes geometricos do executor (protocolo L-26): diag_esq_v2 com ponta da cauda x~27/1000, centroide de cristais 0,475 (52,5% a esquerda), placa de cristal frontal presente, cobertura de cristal 29,0% (classificador do executor) e margem esquerda 2,7%; topo_v2 com a boca reduzida a fenda fina (nao le frontal), cauda a direita x=964, cobertura 28,9% declarada e antebracos retos abertos lateralmente.

- 2026-11-01 ~09:2x - REF-01 lote 2: VEREDITO do Critico Visual senior, RODADA 2 do retrabalho (docs/CRITICO-ref01-lote2-v2.md) - **LOTE 2 FECHADO/APROVADO**. besta_diag_esq_v2.png APROVADA: B1 FECHADO por medida (ponta da cauda x~24/1000 pela mascara; centroide de cristais 0,483; metade esquerda 51,2% - familia frontal, contra 0,557/38,7% da v1); B3 FECHADO (comparativo de 4 paineis: o segmento arredondado unico do braco e o canonico - a v1 tinha bola dupla e bracos abertos); B4 FECHADO (franja da boca curta/fina/irregular como a fonte); B5 FECHADO (placa frontal presente; cobertura de cristal no piso canonico em 3 classificadores: 29,1/31,8/25,8, contra 20,0-24,0 da v1). besta_topo_v2.png APROVADA como vista de topo: B2 FECHADO (domo de escamas + fenda fina escornada; o perimetro da boca NAO le frontal - planta verdadeira); B6 FECHADO (antebracos retos com placa, sem espiral). TODOS os autotestes do executor confirmados na substancia (8/8). Escalada APR-01 da rodada: verificacao nova de COERENCIA INTERNA DO CONJUNTO (as 3 vistas como rotacoes de UMA criatura, ancora por ancora entre elas) + diversidade angular medida do par de diagonais. Achados novos: B10 DEF S3 (maos do topo_v2 em roseta radial contradizem o feixe alongado das fontes e das diagonais) e B11 TXT S3 (tom do topo_v2: cristal delta 32 mais saturado, pele delta 28 mais clara; a frente canonica segue como autoridade de cor); B7 (S3) estendido ao par de diagonais (correlacao 0,778 e centroides gemeos 0,485/0,483 - diversidade angular baixa; pendencia nomeada); B9 (S4) margens de 2,0-2,5% persistem, nada cortado. Nenhum defeito S1/S2 restante. Conjunto final da Besta: 4 cardeais canonicos + diag_dir + diag_esq_v2 + topo_v2. **Proximo sujeito da fila REF-01: Caprileo (lote 3).** Licao L-27 lancada em APRENDIZADO_E_FLUXO.md.


## 2026-11-01 — Pesquisa de texturizacao do ChatGPT protocolada; novo spike T7 (UltraTex)

- Origem: o Mestre entregou ao Muse uma nova pesquisa do ChatGPT (textura/pintura da Oficina) com a ordem de continuar trabalhando em varias frentes. Analise completa em `docs/ESTUDO_T7_PESQUISA_TEXTURA.md`.
- Decisao de fila (registrada pelo Muse sob EXEC-02): o spike **T7 (UltraTex Modular)** entra na Etapa COR **a frente do T3 (Hunyuan Paint)** — o UltraTex consome as referencias canonicas multivista do projeto, enquanto o Paint inventaria as vistas a partir de uma imagem; a regua pre-registrada do T7 (Gate 0 de disco, VRAM, tempo, SSIM por regiao, aceite total ou arquivamento) esta no estudo.
- Divergencia registrada: VRAM do Paint — repo oficial 2.1 recomenda 21 GB; fork 2GP mira ~6 GB com relatos de OOM. O T3 mantem o Gate 0 e fica atras do T7.
- Destinos secundarios: Eyek = leitura comparativa do T1; Yedp = candidato da frente de retrabalho local; SUPRA-Tex e StableGen = observacao.
- Verificacao factual das afirmacoes da pesquisa: em curso por agente dedicado no momento deste registro; o spike so executa depois dela.


## 2026-11-01 — Verificacao da pesquisa de textura protocolada; Yedp retirada do plano

- Relatorio de verificacao (fontes primarias, trechos literais) em `docs/VERIFICACAO_PESQUISA_TEXTURA.md`; resolucao item a item lancada como adendo em `docs/ESTUDO_T7_PESQUISA_TEXTURA.md` e correcao no backlog de `docs/ESTUDO_MELHORIAS.md`.
- Confirmados: UltraTex (GPL-3.0; 15-18 min em 8 GB literais no README; referencias proprias guiam a cor — geracao condicionada, nao projecao literal), Paint 2.1 oficial = 21 GB de VRAM para textura (literal), SUPRA-Tex (48 GB/Linux, release 19/10/2026), InstaMAT Pioneer (< US$ 100 mil, atribuicao obrigatoria), Open Painter (Blender 5.2+, GPL-3.0).
- **Correcao:** Yedp UV Painter NAO foi localizada em fonte primaria alguma — retirada como candidata; fica so o registro da mencao nao verificada. Eyek e Comfy BlenderTools: funcoes reais, licenca nao declarada — vedados como dependencia ate registro de licenca.
- Spike T7 segue liberado para quando o laco o alcancar, com o Gate 0 de disco medindo o que o README nao declara, e com a ressalva BFL (modelo-base FLUX.2 nao comercial) pesando em qualquer decisao futura de adocao.


## 2026-11-01 — Integracao do `cor` a fila de jobs (COR-05, item (c) da Etapa COR)

- **Escopo (CORPO-01):** ligar o mecanismo T1+T5 ja provado fora da fila como etapa opcional do worker, entre o refino e o exportar. Nao e melhoria de fidelidade: a D1 (fidelidade de detalhe do Orc) segue ABERTA e ortogonal, como nas tranches T1/T5/D2/D7.
- **Desenho (COR-05, DECISOES):** (1) opcao `cor`, bool, padrao False (opt-in; `config.OPCOES_PADRAO`, validacao explicita em `job.OPCOES_BOOL`, flag `--cor` na CLI); web/MCP NAO expoem a opcao nesta tranche (seguem o padrao do QUAL-01 na pratica: CLI + worker) - exposicao web/MCP fica como pendencia nomeada. (2) Etapa `cor` nas FAIXAS do worker: refino 80-95, cor 95-98, exportar 98-100; sem `cor`, o caminho do job nao muda (nenhuma etapa nova, nenhum arquivo novo). (3) O passo (`oficina3d/cor/passo.py`, novo) encadeia EXATAMENTE a cadeia provada na T5/D-T5-1: `uv_xatlas.gerar_uv` (padding 8 em 2048) -> Blender aplica a UV (guarda de ocupacao ligada, tolerancia 0,02, checagem duplicada no passo) -> `cor.rodar_cor` (bake 1024, dilatacao 256). (4) O passo usa SO as 4 vistas canonicas; diagonais/cima presentes sao IGNORADAS e registradas (o caminho provado e o de 4 vistas; ampliar exige nova prova). (5) Sem nenhuma vista canonica, o passo FALHA (ValueError -> erro do job na etapa `cor`): opt-in sem insumo e erro, nunca fallback silencioso para modelo sem cor. (6) A S2-3 (troca esq/dir nas imagens da Besta) NAO e resolvida aqui: o bake usa as etiquetas do job como estao; a prova usa o Orc, fora do alcance da S2-3. (7) O GLB refinado e preservado em `saida/modelo_sem_cor.glb` e o colorido ocupa `saida/modelo.glb` (SHA igual ao de `cor/modelo_cor.glb`); o relatorio registra `glb_sem_cor`. Ressalva de leitura: `etapas["refino"]["glb"]` continua apontando para `saida/modelo.glb` (caminho estavel da etapa), cujo conteudo apos a cor e o GLB colorido - quem quiser o refinado original le `saida/modelo_sem_cor.glb` (SHA-256 5467f25e...). Melhoria documental pendente (sem urgencia): registrar `glb_refinado_preservado` com SHA em `etapas["cor"]`.
- **Codigo (commit desta tranche):** novo `oficina3d/cor/passo.py` (`selecionar_vistas` pura + `rodar_passo_cor`); `worker.py` (FAIXAS + etapa `cor` + `glb_sem_cor` + previas da cor no resultado); `config.py` (opcao `cor`); `job.py` (validacao bool); `cli.py` (`--cor`); novo `testes/test_cor_passo.py` (9 testes: selecao de vistas, opcao, faixas, flag da CLI).
- **Suite (tarefa Oficina3D_CorIntSuite, removida apos o uso):** 263 testes, 0 falhas, 0 erros, skipped=1, ok=True (log em `jobs_teste/cor_integracao/suite.log`). Contagem conferida arquivo a arquivo (17 modulos, soma 263; `test_cor_passo` = 9). Ressalva honesta: a suite anterior (D2/D7) marcava 252, ou seja, +11 no total contra +9 novos desta tranche - os +2 NAO foram atribuidos por inspecao de codigo (nenhum teste commitado desde aa2758c em `testes/`; nenhuma geracao dinamica de testes encontrada em `test_config.py`/`test_job.py`): fica como pendencia explicita para o Critico explicar (ou aceitar como baseline 254 pre-tranche).
- **Troca de codigo do worker vivo (licao de operacao):** o worker em loop desde 31/10 21:05 (PID 25544) tinha o codigo antigo carregado; criar o job de prova antes de reinicia-lo teria rodado SEM a etapa cor. Procedimento executado com a fila vazia (pendentes = []): kill do PID 25544, supervisor (`iniciar_worker.py`) relancou o worker (PID 31976, 01/11 10:14:19) com o codigo novo - confirmado por `worker_ativo()` + FAIXAS com `cor`. Licao candidata ao diario: deploy de worker = reiniciar o processo em loop; job criado nao herda codigo novo sozinho. (O venv correto e `Oficina3D\.venv_app`, na RAIZ do projeto - `app\.venv_app` nao existe; a primeira tarefa da suite falhou por isso, codigo 0x80070002, antes da correcao.)
- **Job de prova (fila real, worker novo):** `20261101-101528-corint-orc-s7` - Orc, 4 vistas canonicas douradas, `--qualidade prata --seed 7 --cor`, motor hunyuan-mv-turbo automatico. CONCLUIDO em 264,1 s (tempos: entrada 3,4; forma 59,6; refino 25,3; cor 175,6; exportar 0,005; arquivar 0,4). Forma: 425.626 triangulos, 57,4 s, VRAM pico 6.455 MB. Refino: 425.626 -> 49.750 triangulos (Prata), malha fechada, pivo nos pes, silhueta IoU 0,76-0,81. Cor: UV xatlas ocupacao 0,20152 (Blender: 0,20152, identica), 8.844 ilhas; bake IoU por vista frente 0,7929 / costas 0,7237 / esquerda 0,7885 / direita 0,7827; cobertura: 211.268 texels UV, 41.070 diretos, 170.198 cegos antes da dilatacao (80,56%), sem_cor 0 apos a dilatacao. SHAs: textura ebd744a9..., modelo colorido 0f838538... (= `saida/modelo.glb`, copia conferida); refinado preservado 5467f25e.... Verificacao do GLB final pelo bake: 1 imagem, 1 material com textura. Arquivado pelo gancho do worker em `Oficina3D_v2\arquivo_jobs\20261101-101528-corint-orc-s7` (Drive, copia conferida; local mantido). Previas da cor: `cor/previas/previa_cor_{frente,costas,esquerda,direita}.png` (9 previas no resultado: 5 do refino + 4 da cor).
- **Comparacao com a D-T5-1 (nao e byte-reproducao, e isso e esperado):** a textura e o modelo colorido da prova NAO tem os SHAs da D-T5-1 (textura 5660c824..., modelo 9aa12f8e...), porque a FORMA difere: o job provac usava octree 256 sem perfil de qualidade, e a prova usa o perfil Prata (octree 192, perfil mmgp 4) - a forma crua tambem difere (19db803f... vs 9987f90b...). A comparacao valida e por faixa: os IoUs da prova (0,72-0,79) ficam na faixa do bake T1 do Orc (0,72-0,79), com laterais (0,78-0,79) bem acima do bake da Besta (0,36/0,41) - sujeitos diferentes, sem surpresa. O determinismo da Prova C nao e contestado: ele valia para mesmas opcoes; aqui as opcoes mudaram.
- **Olho do executor (antes do Critico; previas frente/costas lidas):** Orc reconhecivel (silhueta, pose, peca de lobo, armadura, tecido vermelho), sem areas pretas (dilatacao + sem_cor 0 funcionaram), MAS a textura segue em mosaico/"confete" - o rosto sai como mancha escura e o detalhe fino nao e legivel. E a limitacao conhecida (D1 ABERTA: 8.844 ilhas + divergencia geometria-vs-arte), nao regressao da integracao: a etapa entrega o pipeline, nao a fidelidade. O Critico julga se a integracao fecha com a D1 aberta (criterio proposto: pipeline valido + saidas validas + metricas registradas + sem regressao; D1 segue como pendencia nomeada, nao como bloqueio desta etapa).
- **Pendencias que ficam:** S2-3 (troca esq/dir, bloqueia a textura base da Besta, nao a integracao); S3-2 (sem_cor 0 sem mascara entregue); S4-2 (resultado_cor.json nativo do bake nao entregue - o relatorio do job o embute em `etapas["cor"]`); D1 (fidelidade, ABERTA); delta +2 da suite (acima); exposicao da opcao `cor` na web/MCP; campo `glb_refinado_preservado` com SHA em `etapas["cor"]` (documental). Tarefas agendadas da tranche removidas apos o uso (Oficina3D_CorIntSuite). Espelho no Drive dos docs: A FAZER apos o veredito do Critico (junto do relatorio dele), com SHA conferido na volta - o lastro ate la e PC + GitHub.
- **Estado:** (c) integracao do `cor` EXECUTADA (codigo + testes + job de prova), aguardando veredito do Critico senior - NAO autoaprovada. Proximo: (d) T2 apos o veredito; T7 (UltraTex) segue como spike a frente do T3, para quando o laco o alcancar.


## 2026-11-01 — COR-05 FECHADA: veredito do Critico senior

- **Veredito (docs/CRITICO-cor-integracao-relatorio.md, SHA-256 CDC4F5B877C5F4763384195DA9BA5852AAB5E534124A40C0818D3B4C26009021): FECHADO (integracao)** - com pendencias S3/S4 nomeadas abaixo. Nenhum defeito S1/S2 novo. Escopo exato do FECHADO: fecha a fiacao CLI -> worker -> passo -> exportar -> arquivo; NAO fecha a fidelidade da cor (D1 segue ABERTA; qualquer leitura de "cor pronta/fiel" a partir deste veredito seria falsa).
- **Julgamento do Critico sobre a D1 aberta (concorda com o criterio do executor):** a D1 e anterior a COR-05 e nao mudou de natureza nem de magnitude com a integracao (IoUs do bake 0,7237-0,7929 na faixa do T1 0,72-0,79; mesmo carater visual em mosaico); reprovar a integracao pela D1 puniria a tranche errada e travaria o corpo (CORPO-01). Guarda registrada: o FECHADO segue junto da D1 aberta em ESTADO_ATUAL e no backlog.
- **Re-medicoes do Critico (nada aceito sem re-medir):** parse binario proprio do GLB final (sem trimesh, sem costura.py): 1 mesh, 49.750 triangulos, TEXCOORD_0 presente (71.336 VEC2), 1 imagem PNG (349.459 B), 1 material "cor" com baseColorTexture; `saida/modelo.glb` byte-identico a `cor/modelo_cor.glb` (SHA 0f838538...) e diferente de `saida/modelo_sem_cor.glb` (SHA 5467f25e..., 49.750 tris, 0 imagens, 0 materiais). Ressalva medida (nao defeito): a imagem embutida no GLB (349.459 B) nao e byte-identica a `cor/textura.png` (349.022 B) - o Blender re-codifica o PNG na exportacao; ancoras distintas, nao confundir. Tempos: soma das etapas 264,305 -> total 264,3 s (o "264,1 s" do historico e outro relogio). Cobertura: 41.070 + 170.198 = 211.268 texels; 80,56% cegos antes da dilatacao. UV: ocupacao xatlas = Blender = 0,20152.
- **Correcoes do Critico a secao anterior deste REGISTRO (registradas aqui, nao apagadas la):** (1) o delta +2 da suite ESTA EXPLICADO e a ressalva anterior esta SUPERADA: o `suite.log` da D2/D7 (252 testes) era da arvore 17462aa (01/11 08:31:30), onde `test_cor_costura` tinha 5 testes; o commit aa2758c (08:45:57, posterior ao log) acrescentou exatamente 2 testes (5 -> 7); baseline correto pre-tranche = 254, nao 252; 254 + 9 = 263. Nenhum teste fantasma, nenhum perdido. (2) Tempo total: 264,3 s (soma) vs 264,1 s (relogio do processamento) - ambos certos. (3) Worker novo: inicio 10:14:18 (supervisor + processo), nao 10:14:19. (4) "perfil mmgp 4" nao e distintivo da Prata (o provac tambem o tem); o delta distintivo e qualidade/octree (null/256 -> prata/192). (5) Vertices entre estagios 65.274 (refino) -> 71.195 (xatlas) -> 71.289 (resultado_cor) -> 71.336 (GLB final), sem explicacao registrada (observacao, nao defeito). (6) Os IoUs 0,76-0,81 citados na secao anterior sao os do REFINO, nao do bake (bake: 0,72-0,79).
- **Defeitos do Critico (nenhum bloqueia):** D-COR05-1 (S3) janela de cancelamento: `gerar_uv` (~97,5 s) nao emite callback de progresso, logo o flag de cancelamento so surte efeito quando o Blender UV comeca a reportar (atraso de ate ~100 s, sem publicacao parcial); acao: emitir progresso/verificar o flag dentro de `gerar_uv` e antes das copias finais, na proxima tranche que tocar o passo/worker. D-COR05-2 (S3) nenhum job sem-`--cor` sob o worker novo (nao-regressao provada por diff + job pre-integracao, nao por execucao); acao: rodar 1 job sem-cor sob o worker atual e registrar antes de declarar a nao-regressao como provada por execucao. D-COR05-3 (S4) falta `glb_refinado_preservado` com SHA em `etapas["cor"]` (SHA completo hoje so no manifesto do Drive); acao: incluir o campo na proxima tranche que tocar o worker. D-COR05-4 (S4) divergencias documentais corrigidas acima + ESTADO com suite 247 (corrigido nesta tranche para 263).
- **Prova de nao-regressao (Critico):** sem `cor`, `modelo_final` e o mesmo valor do codigo antigo; `previas` soma lista vazia; `glb_sem_cor` so com `cor`; job pre-integracao `20261031-225432-provac-orc-s7` sem chave `cor`, sem etapa `cor`, sem `glb_sem_cor`. Unica mudanca para jobs sem-cor: faixa de progresso do refino (80-98 -> 80-95), cosmetica.
- **Troca do worker vivo (Critico):** supervisor registra queda do PID 25544 em 10:13:18 (kill) e relancamento em 10:14:18; processo vivo PID 31976 (CreationDate 10:14:18); `job.json` registra worker PID 31976, inicio 10:15:31 - o job de prova rodou sob o worker novo. Fila vazia na troca: zero jobs fora de (concluido, erro, cancelado); nenhum orfao; nenhum job afetado.
- **Verificacao nova exigida para a proxima bateria (escalada APR-01):** reexecucao deterministica ponta a ponta da etapa `cor` (mesmas opcoes da prova; SHAs textura ebd744a9... e modelo 0f838538... devem reproduzir; divergencia = S2, com decomposicao por sub-passo UV vs bake). Secundarias: (i) job sem-`--cor` sob o worker novo (fecha D-COR05-2 por execucao); (ii) job `--cor` sem vista canonica pela fila real (deve terminar `erro` na etapa `cor`); (iii) validador glTF independente (ex.: `gltf-validator`) alem do parse proprio.
- **Estado:** (c) integracao do `cor` FECHADA com veredito do Critico. Proximo: (d) T2 cor de vertice como rede de seguranca + D-COR05-1/2/3/4; T7 (UltraTex) segue como spike a frente do T3, para quando o laco o alcancar.

- **Espelho no Drive (fechamento desta tranche):** REGISTRO, ESTADO_ATUAL, DECISOES, APRENDIZADO_E_FLUXO e o relatorio do Critico copiados para `Oficina3D_v2\REGISTRO` (via G: transmitido) e conferidos por SHA-256 na volta: REGISTRO 8F06E4B7B3EE, ESTADO_ATUAL 60C31AD2FE58, DECISOES E6E489987F24, APRENDIZADO_E_FLUXO 23606EFE5FFF, CRITICO-cor-integracao-relatorio CDC4F5B877C5 (prefixos de 12 hex; todos iguais PC = Drive). O relatorio do Critico ja estava espelhado com o mesmo hash (espelho feito pelo proprio Critico); os 4 docs foram atualizados nesta tranche.


## 2026-11-01 — D-COR05 FECHADA: veredito do Critico senior (fechamento documental desta tranche)

- **Veredito (docs/CRITICO-dc05-relatorio.md, SHA-256 DC96449CFE9A40B82CD88732652AB7B004B4064CE008F443C58631A02EF3F31B): D-COR05 FECHADA — D1 segue ABERTA e ortogonal.** Tranche julgada: pendencias D-COR05-1/2/3/4 da integracao COR-05, commit julgado `0449f9c` ("D-COR05: janela de cancelamento na UV, campo glb_refinado_preservado, testes (jobs de prova pendentes)"), diff contra `61c3a37` lido linha a linha. Nenhum defeito S1/S2/S3 novo. Guarda explicita do Critico, registrada aqui junto do FECHADO: a reexecucao reproduz byte a byte o mesmo bake da prova (IoUs 0,7237-0,7929, mesmo carater em mosaico) — a D1 nao melhorou nem piorou; qualquer leitura de "cor pronta/fiel" a partir deste veredito seria falsa.
- **Metodo do Critico (nada aceito sem re-medir):** diff do commit; reexecucao propria do modulo `test_cor_passo`; discovery propria com contagem por modulo; suite completa reexecutada em duas metades; parse binario proprio dos GLBs (struct + JSON, sem trimesh, sem `costura.py`); hashes refeitos na maquina dele pos-scp; comparacao byte a byte de TODOS os artefatos do job de determinismo contra a prova, com decomposicao de chunks PNG e comparacao pixel a pixel; leitura de `job.json`, `relatorio.json`/`relatorio_parcial.json`, `log.txt` e `resultado_*.json` dos 3 jobs; codigo do worker/passo lido, nao resumido.
- **Jobs de prova (fila real, worker novo PID 33284, inicio 2026-11-01T11:06:42-03:00):** `20261101-110658-dc05-semcor-orc-s7` (sem `--cor`); `20261101-110659-dc05-cor-det-orc-s7` (reexecucao deterministica da prova COR-05); `20261101-110659-dc05-cor-semvista-besta` (`--cor` sem vista canonica). Prova de referencia: `20261101-101528-corint-orc-s7` (worker antigo PID 31976).
- **D-COR05-1 (janela de cancelamento na UV) — FECHADO.** `uv_xatlas.gerar_uv` ganhou `progresso` (0/20/30/80/90/100); `cor/passo.py` mapeia para a janela 5-30 pela formula `5 + (pct*25)//100`; `worker.py` re-checa o cancelamento apos o retorno do passo e ANTES das copias finais para `saida/`. Aritmetica conferida pelo Critico linha por linha no `log.txt` do determinismo (0→5% gerando, 0→5% carregando, 20→10% carregado, 30→12% parametrizando, 80→25% pronta apos ~84 s, 90→27% metricas, 100→30% .npz, 30% pronta). Janela residual medida: 12% as 11:09:01 → 25% as 11:10:25 = **84 s** de chamada nativa nao interrompivel; UV total 97 s. Testes reexecutados pelo Critico: `test_cor_passo` = 13 OK (9 antigos + 3 `TestGerarUvProgresso` + 1 `TestSha256Worker`), incluindo "progresso que levanta em >=80 nao grava .npz" e monotonicidade.
- **D-COR05-2 (job sem `--cor` sob o worker novo) — FECHADO.** Job sem-cor: `estado=concluido`, `worker.pid=33284`, `opcoes.cor=false`, `tempo_total_s=58,5`; etapas = entrada, forma, refino, arquivar (sem `cor`); `job.json: resultado` sem `glb_sem_cor`, com as 5 previas do refino e sem previas da cor. A nao-regressao, antes provada so por diff + job pre-integracao, agora esta provada por execucao sob o worker novo.
- **D-COR05-3 (campo `glb_refinado_preservado`) — FECHADO.** No `relatorio.json` do determinismo, `etapas["cor"]["glb_refinado_preservado"] = {"arquivo": "saida/modelo_sem_cor.glb", "sha256": "5467f25e900cf9ab43b84ccbaecc4b42d81deab4cfe0887c9a33447769b41d00"}`; SHA re-medido pelo Critico no arquivo baixado, identico ao campo. Contraste que prova a novidade: o `relatorio.json` da prova COR-05 (worker antigo) NAO tem o campo.
- **D-COR05-4 (divergencias documentais) — FECHADO, item a item.** (a) 264,1 vs 264,3: `log.txt` marca "concluido em 264.1 s" (relogio do processamento, na linha do exportar, antes do arquivar); `relatorio.json: tempos_s` soma 264,305 → total 264,3; dois relogios, ambos corretos (mesmo padrao no determinismo: soma 232,806 → total 232,8). (b) Worker COR-05: `job.json` da prova, `worker.pid=31976`, filetime 2026-11-01T13:14:18.834 UTC = 10:14:18-03:00, nao 10:14:19. (c) Vertices 65.274→71.195→71.289→71.336, com recontagem propria do Critico (parser binario): `saida/modelo_sem_cor.glb` 65.274 vertices / 23.771 posicoes unicas / 49.750 faces; `cor/uv.npz` 71.195; `cor/modelo_uv.glb` 71.289 / 23.771 / 49.750; final 71.336 / 23.771 / 49.750 — geometria inalterada, so duplicacao em costuras (+5.921 xatlas, +94 round-trip Blender UV, +47 export do bake). (d) "perfil mmgp 4": provac tem `perfil_mmgp=4`, `octree=256`, sem `qualidade`; determinismo tem `perfil_mmgp=4`, `octree=192`, `qualidade=prata` — o delta distintivo e qualidade/octree. (e) ESTADO com suite 263: a correcao 247→263 da tranche anterior esta no arquivo; apos a D-COR05 o numero correto passa a 267 (atualizado neste fechamento).
- **Verificacao principal (reexecucao deterministica da etapa cor) — PASSOU.** Job determinismo: `concluido`, `worker.pid=33284`, `tempo_total_s=232,8`, mesmas opcoes da prova. Byte-identicos a prova: `cor/textura.png` (EBD744A9FE1BD0FB1B73334EFB1EACBB0B147E4F9B2FF714AED5A2C213D2139D), `cor/modelo_cor.glb` e `saida/modelo.glb` (0F8385380B22F86894355E6E944FC74CE910EF3A3B60D56EF341BFB57E9BF48C), `saida/modelo_sem_cor.glb` (5467F25E...69B41D00), `cor/uv.npz` (42097d3b...) e `cor/modelo_uv.glb` (9a5c1203...). Previas: as 4 da cor e as 5 do refino tem o mesmo tamanho em bytes mas SHA diferente — decomposicao dos chunks PNG: `IDAT` identico em todos; a unica diferenca esta nos chunks `tEXt` do Blender (`Date` 10:19:54 na prova vs 11:11:55 no determinismo; `RenderTime` 0.45 vs 0.50 s). Decodificacao pixel a pixel das 9 previas: **0 pixels diferentes** (512.000 pixels cada). Conclusao: determinismo total no conteudo; comparacoes futuras de previas do Blender devem comparar `IDAT`/pixels, nao bytes brutos (licao L-32). Metricas identicas a prova: ocupacao 0,20152, 8.844 ilhas, distorcao 0,0671, IoUs 0,7929/0,7237/0,7885/0,7827, cobertura 211.268 texels (41.070 diretos, 170.198 cegos = 80,56%, 0 sem cor apos dilatacao), 49.750 triangulos.
- **Verificacao secundaria (ii) (job `--cor` sem vista canonica) — PASSOU.** Job sem-vista (Besta `topo_v2`, vista "cima", prata, seed 7, `--cor`): `estado=erro`, `etapa=cor`, erro exato `cor: etapa cor sem nenhuma vista canonica (frente/costas/esquerda/direita) nas imagens do job`; sem pasta `cor/`, sem `modelo_cor`, sem `relatorio.json` final — so `relatorio_parcial.json`. Sobre o `saida/modelo.glb` presente no job em erro: comportamento pre-existente documentado, nao vazamento da cor — o refino grava ele mesmo `saida/modelo.glb` (a cor nunca rodou); ressalva S4: num job em erro, ele e indistinguivel por nome de um final; so `job.json: estado` + `relatorio_parcial.json` vs `relatorio.json` distinguem.
- **Suite de testes — 267 OK, reconciliada pelo Critico.** Executor: `jobs_teste/cor_dc05/suite.log` → `Ran 267 tests, OK (skipped=1)` (ressalva honesta herdada da tranche executora: o `status.txt` da tarefa agendada da suite NAO foi escrito por quoting do comando final, LastTaskResult 1 — a evidencia e o proprio `suite.log`, nao o status; tarefa removida apos o uso). Critico: discovery propria TOTAL 267, por modulo identica a bateria anterior exceto `test_cor_passo` 9→13 (+4); reexecucao propria: `test_cor_passo` 13 OK, metade A 131 OK, metade B 136 OK (skipped=1); 131+136 = 267; 263+4 = 267, reconciliacao exata. O skipped=1 e o mesmo das suites anteriores (trava assumida em `test_motores`, pre-existente). Nota de operacao do Critico: a primeira tentativa de suite completa em segundo plano morreu sem saida (logs vazios); a verificacao foi refeita nas duas metades; os rascunhos da auditoria foram removidos do PC ao fim, deixando a arvore como encontrada, exceto este relatorio.
- **Escalada APR-01 desta bateria (verificacoes novas, ausentes na anterior):** (1) comparacao byte a byte de TODOS os artefatos do determinismo contra a prova (inclui `uv.npz`, `modelo_uv.glb` e as 9 previas, com decomposicao de chunks PNG e comparacao pixel a pixel — foi ela que explicou a divergencia de bytes das previas); (2) proveniencia do worker nos 3 jobs + fila vazia ao fim (`worker.pid=33284` nos 3, criado 11:06:42-03:00; ultimo job modificado as 11:12:53; a auditoria nao criou jobs, nao commitou e nao tocou em arquivo fora do relatorio); (3) tentativa do validador glTF independente (`gltf-validator`): fontes oficiais buscadas (KhronosGroup/glTF-Validator); distribuido via npm/build Dart, **nenhum binario standalone oficial para Windows localizado nas releases** — nao instalado nem executado (instalar pacotes no PC do cunhado extrapolaria o escopo da auditoria); nao bloqueia (validacao estrutural coberta pelo parser binario proprio + cadeia Blender); pendencia segue aberta como sugestao; (4) recontagem independente da cadeia de vertices incluindo o `.npz` (uvs 71.195 medidos no arquivo).
- **Ressalvas S4 (nao bloqueiam):** S4-1 docstring de `gerar_uv` diz "chamada nativa (~97 s)" — medido: nativa 84 s, total 97 s; corrigir o numero numa proxima passada pelo arquivo. S4-2 `saida/modelo.glb` do refino em jobs em erro (acima). S4-3 cancelamento real em job vivo nao exercido (mecanismo provado por codigo + teste unitario). S4-4 validador glTF independente pendente (acima).
- **Conferencia do executor neste fechamento (antes de escrever):** relidos do PC os arquivos do projeto (ESTADO_ATUAL, REGISTRO, APRENDIZADO_E_FLUXO, DECISOES) e o relatorio do Critico; re-medidos nesta tranche: `jobs_teste/cor_dc05/suite.log` = `Ran 267 tests, OK (skipped=1)`; estados dos 3 jobs dc05 (`concluido`/`concluido`/`erro`, todos `worker.pid=33284`); SHA-256 da textura do determinismo = EBD744A9...213D2139D, identico ao do Critico; SHA-256 do relatorio do Critico = DC96449C...F31B, identico a medicao no PC. Worker vivo conferido (PID 33284, lock desde 11:06:42-03:00); nenhum job novo criado por este fechamento (tranche so documental — nao se duplica prova ja feita).
- **Pendencias que ficam (nao sao defeitos desta tranche):** D1 (fidelidade de detalhe do Orc) ABERTA e ortogonal; **T2 (cor de vertice) = proximo passo**, rede de seguranca da Etapa COR; exposicao web/MCP da opcao `cor` (desde a COR-05, CLI + worker apenas); S2-3 (troca esq/dir nas imagens da Besta), S3-2 (sem_cor 0 sem mascara entregue), S4-2 do bake (resultado nativo) — herdadas, inalteradas; validador glTF independente (sugestao). Arquivo alheio notado e NAO tocado: `docs/CRITICO-ref01-lote3.md` (nao rastreado; possivelmente trabalho concorrente de outra IA no PC).
- **Estado:** (c) integracao do `cor` FECHADA; D-COR05 FECHADA com veredito do Critico. Proximo: (d) T2 cor de vertice. T7 (UltraTex) segue como spike a frente do T3, para quando o laco o alcancar. Portao final MET-03: so depois de TODAS as frentes concluidas.

- **Espelho no Drive (fechamento desta tranche):** ESTADO_ATUAL, REGISTRO, APRENDIZADO_E_FLUXO, DECISOES e o relatorio do Critico copiados para `Oficina3D_v2\REGISTRO` (via G: transmitido) e conferidos por SHA-256 na volta: ESTADO_ATUAL 4D16857C269C, REGISTRO 41024C77D4AF (versao copiada; esta linha de espelho foi acrescentada depois da copia, pelo que o REGISTRO commitado difere dela so por esta linha), APRENDIZADO_E_FLUXO 6C622DF53817, DECISOES F552DCDB4680, CRITICO-dc05-relatorio DC96449CFE9A (prefixos de 12 hex; todos iguais PC = Drive). PC + GitHub seguem como lastro junto do espelho.


## 2026-11-01 - T2 cor de vertice (COR-07): desenho, autoauditoria e execucao

- **Escopo (CORPO-01 + ESTUDO_MELHORIAS, secao T2):** o modo `vertice` da etapa COR - nivel Bronze e rede de seguranca da cor: (i) preservar a cor que o TripoSR ja gera (hoje o refino a descarta - MEDIDO nesta tranche com inspetor proprio de GLB: `jobs/20261031-210907-r3-gpu-ocupada/forma/forma.glb` tem COLOR_0 em 30.452 vertices, media RGB 181/162/143 (uint8), dp 6-9 por canal; a `saida/modelo.glb` do mesmo job tem so POSITION/NORMAL/TEXCOORD_0, sem COLOR_0 e sem material); (ii) amostragem das vistas canonicas sobre os vertices para qualquer motor, sem UV nem textura, com tempo adicional muito menor que o bake (a medir na prova).
- **Desenho (COR-07 em DECISOES.md):** opcao `cor_modo` em {projecao, vertice}, padrao projecao; `--cor-modo` na CLI implica `--cor`; o passo `rodar_passo_vertice` roda `cor/_blender_vertice.py` (amostragem por vertice, mesmas cameras/alinhamento/facing do T1, oclusao BVH por vertice); fontes em prioridade vista > forma (transferencia pela superficie mais proxima, alinhamento reconstruido das invariantes do refino e autochecado por distancia mediana - acima de 5% da altura, recusa registrada) > propagacao por arestas; vertice sem fonte sai preto e CONTADO; GLB verificado por parse no passo (COLOR_0 completo, 0 imagens, material) - sem COLOR_0, FALHA; relatorio declara `modo_cor` + `rotulo = "rascunho"` e o worker emite o aviso correspondente.
- **Autoauditoria APR-02 (o executor cacou e corrigiu ANTES do Critico):** (1) o export do Blender pode nao gravar COLOR_0 se o atributo nao for o ativo/render ou se o material nao o referenciar -> mitigacao em camadas: atributo "Color" novo (anteriores removidos), active/render setados, no ShaderNodeVertexColor no material, `export_vertex_colors=True` com fallback, e verificacao por parse dentro do proprio script (falha = exit 3, nunca entrega silenciosa); (2) o sintetico do T1 (cubo) nao serve a vertices - normais de canto sao medias diagonais e nenhum vertice tem facing > 0,99 -> o sintetico do T2 usa ESFERA UV (normais radiais) e checa a cor no vertice voltado a cada camera; os polos exercitam a propagacao; (3) a primeira cena dos testes unitarios era degenerada (vertices coplanares) e reproduziu a regra do T1 (caixa projetada degenerada levanta ValueError) -> cena com extensao vertical explicita; o modulo mantem o comportamento do bake (erro declarado, nao silencio); (4) o refino nao registra a transformacao que aplica - a transferencia da forma reconstrói o alinhamento das invariantes registradas (altura = altura_m, pivo nos pes) e se AUTOVERIFICA por distancia mediana antes de pintar 1 vertice sequer (sem isso, pintaria a cor certa no lugar errado em silencio); (5) colisao de nome: o desenho nasceu rotulado "COR-06" nos comentarios e foi renomeado para COR-07 ao conferir DECISOES (COR-06 = fechamento D-COR05) - grep conferido nos 8 arquivos tocados (10 ocorrencias, todas desta tranche); (6) clip de pixel (como no bake) esticaria a cor da borda sobre vertices fora do quadro -> no vertice, fora do quadro NAO pinta (diferenca registrada no docstring de `cor/vertice.py`); (7) erro de sintaxe no proprio arquivo de testes (colchete faltando) pego na compilacao antes de rodar - registrado para nao fingir que nao houve.
- **Codigo (commit desta tranche):** novos `oficina3d/cor/vertice.py` (puro) e `oficina3d/cor/_blender_vertice.py`; `cor/passo.py` (`rodar_passo_vertice` + `_forma_tem_color0`); `cor/__init__.py` (`rodar_vertice`); `config.py` (`MODOS_COR` + opcao `cor_modo`); `job.py` (validacao de `cor_modo`); `worker.py` (despacho por modo, mensagens e aviso de rascunho); `cli.py` (`--cor-modo`); novo `testes/test_cor_vertice.py` (18 testes: amostragem, mescla, propagacao, baricentricas, passo com runner mockado, opcao, CLI, despacho do worker).
- **Testes rapidos (pre-suite, .venv_app):** `test_cor_vertice` + `test_cor_passo` = 31 testes OK (18 novos + 13 herdados).
- **Estado:** T2 EXECUTADA (codigo + testes unitarios). Pendente nesta tranche: suite completa, sintetico no Blender, jobs de prova na fila real (3 personagens + TripoSR + determinismo + regressao) e veredito do Critico senior - NAO autoaprovada.


## 2026-11-01 — REF-01 lote 3 FECHADO (Capríleo): C1 fechado por renomeação

- **Geração (rodada ~09:54–10:10):** 3 vistas avulsas a partir das 4 fontes douradas
  (`testes/dourado/imagens/caprileo_{frente,costas,esquerda,direita}.png`): `caprileo_diag_tras_esq.png`
  (1600x1600), `caprileo_diag_tras_dir.png` (1920x1280) e `caprileo_topo.png` (1600x1600), instaladas em
  `testes/referencias/` com hashes PC == local e fora do git (gitignored).
- **Veredito da rodada 1 (docs/CRITICO-ref01-lote3.md): LOTE REPROVADO por um único defeito S2 — C1 (SYM):**
  os rótulos das duas diagonais traseiras estavam trocados (o arquivo `esq` continha a vista traseira-direita e
  vice-versa, provado por 5 âncoras: cabeça, cauda, flanco, motivo do chifre próximo e correlação com os perfis).
  O topo foi APROVADO como planta verdadeira na mesma rodada. Retrabalho especificado: só renomear, sem regenerar.
- **Retrabalho (rodada ~11:00, árvore limpa, HEAD 61c3a37):** troca simultânea dos nomes nos DOIS lados
  (PC `testes/referencias/` + cópias locais) via nome temporário, sem sobrescrita direta. Hashes por conteúdo
  intactos e idênticos PC = local. Mapeamento NOVO, por nome: `caprileo_diag_tras_esq.png` =
  `46CBE2B9B645163909A6EB6AC745EB8B9D0694717122FDEDFC8348D10D1EF07A` (1955953 B);
  `caprileo_diag_tras_dir.png` = `EFD00A7D77E0830F609025A12307F6F00485032BB86D91F7496FE02EE59FA180` (2065375 B);
  `caprileo_topo.png` = `F09270071BDEA23CD587DA96EE4B52BF4BB29B3204D47CA369AA4BA3C238B634` (inalterado).
  Nenhum arquivo temporário restante; `git check-ignore` confirma os PNGs fora do git.
- **Re-verificação C1 (checklist da seção 7 do relatório da rodada 1):** executor, com os olhos, nos arquivos
  renomeados — `diag_tras_esq`: cabeça à esquerda + chifre próximo com segundo anel pequeno e fechado + cauda à
  direita (3/3); `diag_tras_dir`: cabeça à direita + chifre próximo em gancho aberto em "C" + cauda à esquerda
  (3/3). Crítico Visual sênior de fechamento, independente (docs/CRITICO-ref01-lote3-fechamento.md), confirmou
  os mesmos 3/3 itens nos dois arquivos e os três hashes acima no local e no PC (via `Get-FileHash`).
  **C1 FECHADO; LOTE 3 FECHADO.**
- **Registro adiado duas vezes pela regra anti-colisão** (árvore suja com tranches da frente principal) e concluído
  nesta rodada com a árvore limpa (HEAD 8ce9860, antes de qualquer escrita): instalados docs/CRITICO-ref01-lote3.md
  e docs/CRITICO-ref01-lote3-fechamento.md junto destas edições. Os arquivos guardados da rodada anterior
  (pc_docs_lote3, base ~11:00) NÃO foram subidos como estavam — as tranches D-COR05 e COR-07/T2 avançaram os docs
  desde então; as edições foram reaplicadas sobre os docs frescos, com âncoras conferidas, para não sobrescrever
  o trabalho da frente principal.
- **Conjunto final do Capríleo no arsenal:** 4 cardeais canônicos + `diag_tras_esq` + `diag_tras_dir`
  (corretamente rotuladas) + `topo`. Pendências nomeadas que NÃO bloqueiam: C2 (S3, pernas espraiadas do topo —
  modelar a articulação pelos perfis/costas, nunca pelo topo), C3 (S3, espirais dos chifres do topo mais fechadas,
  "caracol" — modelar o número de voltas pelos perfis), C4 (S3, diagonais rasas, próximas dos perfis — futura
  diagonal profunda ~45° opcional), C5 (S4, margens das bases 2,3–3,7%, abaixo dos 5% pedidos, nada cortado).
- **Convenção de nomes registrada:** `diag_tras_esq/dir` = lado do animal visível (= lado da câmera) na vista traseira.
- **Verificação nova do fechamento (escalada APR-01): consistência de rótulos no conjunto.** Varredura do Crítico de
  fechamento em `~/workspace/oficina-audit/**/*.md` e em `app\docs\*.md` no PC: nenhum documento do projeto citava
  os nomes das diagonais (só menções genéricas ao Capríleo); o relatório da rodada 1 é documento histórico datado
  que descreve o mapeamento pré-troca e é complementado por esta entrada com o mapeamento novo. Zooms de evidência
  em `zooms_lote3/` foram renomeados localmente acompanhando a troca (`esq_*` ↔ `dir_*`) — conferido pelo executor
  com os próprios olhos nesta rodada (`esq_cabeca_chifres.png` mostra cabeça à esquerda e chifre próximo com
  segundo anel fechado, conteúdo de vista traseira-esquerda, coerente com o nome). Os brutos
  `media-generation-caprileo-diag-tras-*` mantêm os nomes originais do pedido de geração (artefatos intermediários,
  fora do arsenal) — quem reconstituir o lote a partir deles precisa saber da troca.
- **Autoauditoria adversarial do executor (APR-02, antes de submeter):** (1) recusou subir os arquivos guardados da
  rodada anterior sem conferir o diff — o diff mostrou que eles sobrescreveriam D-COR05 e COR-07/T2; (2) re-mediu
  os hashes no PC e no local nesta rodada em vez de copiar os da rodada anterior; (3) verificou a renomeação dos
  zooms com os próprios olhos em vez de aceitar a afirmação do rascunho; (4) corrigiu a posição da linha de
  escalada na tabela (após D-COR05, não após COR-05) para manter a cronologia.
  (5) detectou colisão de numeração (L-30 já ocupado pelo cancelamento em chamada nativa da D-COR05 e L-33
  pela APR-02) e renumerou a lição nova para L-34 antes de subir.
- **Próximo sujeito da fila REF-01:** diagonais do Orc; depois, a classificação das 5 bestas novas de 31/10.


## 2026-11-01 - T2 cor de vertice (COR-07): execucao medida e provas (fechamento do executor; aguarda Critico)

Codigo no commit 8ce9860 (push conferido: HEAD = origin/main, arvore limpa). Worker reiniciado para carregar o codigo novo (PID 33284 -> 31856, 12:47:35, fila vazia na troca; o supervisor levou ~4 min no backoff - registrado no log da tarefa).

- **Suite:** 285 testes, 0 falhas, 0 erros, 1 skipped, 27,5 s (267 da D-COR05 + 18 novos do T2; reconciliacao exata).
- **Sintetico no Blender** (esfera 64x32, 1.986 vertices): as 4 vistas com a cor esperada EXATA nos vertices de facing > 0,99 (9 amostras por vista); cobertura vista 99,9% + propagacao 0,1% (os polos), sem_cor 0; exportacao verificada por parse do GLB (COLOR_0 2.143 == POSITION 2.143, 0 imagens, 1 material); passo Blender 0,78 s.
- **Autoauditoria, item 8 (pos-sintetico):** a primeira versao da verificacao interna do GLB exigia COLOR_0 == n. de vertices da MALHA do Blender e reprovou o sintetico (2.143 exportados x 1.986 da malha): o exportador duplica vertices nas costuras - o mesmo fenomeno medido na D-COR05 (65.274 -> 71.336). Verificacao corrigida para a invariante real do formato (COLOR_0 == POSITION no mesmo primitivo) ANTES de qualquer job real; sintetico aprovado na reexecucao. A verificacao continua sendo saida dura (exit 3) se o COLOR_0 vier incompleto ou ausente.

Provas reais pela fila (worker novo; os 8 jobs concluidos):

- **J1 `20261101-124814-t2-orc`** (hunyuan-mv, prata, seed 7, vertice): passo de cor no Blender 2,57 s (contra 175,6 s do passo de projecao na prova COR-05); cobertura vista 47,54% / propagacao 34,72% / sem_cor 17,74%; GLB final com COLOR_0 em 65.469 vertices exportados, 99,4% nao-brancos, media RGB (0,361; 0,243; 0,192); SHA da saida 949E3CF7...
- **J2 determinismo:** job identico (`t2-orc-det`) -> saida BYTE-IDENTICA (mesmo SHA 949E3CF7...).
- **J3 besta:** passo 2,05 s; vista 58,53% / propagacao 30,76% / sem_cor 10,71%; 97,0% nao-brancos; media (0,398; 0,142; 0,349) - o roxo dos cristais.
- **J4 caprileio:** passo 1,93 s; vista 70,08% / propagacao 20,49% / sem_cor 9,42%; 99,9% nao-brancos.
- **J5 orc triposr, so frente (a parte (i) do backlog):** transferencia da forma ACEITA com distancia mediana de 0,00018 da altura (limite 0,05); fontes: vista 27,51% / **FORMA 72,49%** / sem_cor 0 - a cor que o TripoSR gera e o refino descartava agora chega ao modelo final, com cobertura total.
- **J6 sem cor:** saida SHA 5467F25E... == ancora da D-COR05 (caminho sem cor intocado pelo T2).
- **J7 projecao:** textura EBD744A9... e modelo 0F838538... BYTE-IDENTICOS as ancoras da COR-05 (sem regressao no modo padrao sob o codigo novo).
- **J8 so a vista frente (adversarial):** concluido com declaracao completa - os avisos do job nomeiam as 3 vistas ausentes; cobertura vista 25,80% / propagacao 43,13% / sem_cor 31,07% declarada em `cobertura`.
- **Rotulo de rascunho:** aviso presente em todos os jobs de vertice; job de projecao (J7) sem avisos.
- **sem_cor:** fracao de vertices sem fonte, exportada preta e DECLARADA por job; nas previas de superficie inspecionadas (frente e costas do J1) nao aparece mancha preta - consistente com geometria interna/oculta das malhas Hunyuan; a Critica pode medir por componentes.
- **Previas** baixadas para a VM do executor (pasta da auditoria do T2): orc nos 4 angulos, besta frente, caprileio frente, triposr frente e costas - superficie visivel colorida por inteiro nas tres personagens e no triposr.

Pendencias nomeadas apos a execucao: (1) exposicao web/MCP da opcao `cor_modo` (herdada da COR-05); (2) D1 (fidelidade da cor no modo projecao) segue ABERTA e ortogonal - o modo vertice e rascunho por desenho (COR-07); (3) veredito do Critico senior sob a carta CRITICO-PADRAO (duas baterias: padrao + personalizada do T2) - esta secao e o fechamento do EXECUTOR; "pronto" so com o veredito dele.


## 2026-11-01 - T2 (COR-07): veredito do Critico senior - MECANISMO APROVADO (9,0/10); rascunho aprovado como rascunho

Relatorio integral: docs/CRITICO-t2-relatorio.md (SHA-256 3DF49D3BDA2F86D329014D0F17270547994FAC3054B85CD535DAB019162AAA2B; commit 20e75bd + emenda 0a40c8d com o veredito visual do Mestre). O Critico re-mediu tudo a partir das fontes (parser GLB proprio em todos os primitivos; suite reexecutada por ele: 285 testes, 0 falhas, skipped=1, 26,2 s; o passo do J1 reproduzido por ele com o MESMO SHA-256; alinhamento refeito por KDTree; 3 jobs vivos proprios pela fila real) e rodou as duas baterias da carta CRITICO-PADRAO: a padrao (a-j) e uma personalizada com 5 verificacoes novas em relacao as tranches anteriores (sabotagem da autochecagem de alinhamento; rede de seguranca com ZERO vistas; reproducao do passo por terceiro; composicao geometrica do sem_cor; cancelamento vivo durante a cor de vertice).

- **MECANISMO: APROVADO, nota 9,0/10.** Nenhum defeito S1/S2. Todas as medicoes do fechamento do executor conferiram na tabela de conferencia dele (suite, sintetico, J1-J8, ancoras da COR-05 byte-exatas, tempos: job de vertice 92,5 s x 233,0 s da projecao).
- **QUALIDADE VISUAL: APROVADO COMO RASCUNHO - e so como rascunho.** Veredito do Mestre (01/11, ~13:29, ao ver a previa da frente do Orc em cor de vertice): "Melhorou um pouco, mas ta longe do ideal" - cor final NAO aprovada em nenhum modo; D1 segue ABERTA e ortogonal.
- **Rede de seguranca provada pelo Critico com zero vistas:** job so-forma TripoSR concluiu com a forma pintando 100% (27.421 vertices); job Hunyuan sem vistas errou na etapa cor com a mensagem desenhada. **Cancelamento vivo** durante a cor de vertice: honrado antes de publicar (fecha, para o modo vertice, a ressalva herdada da D-COR05).
- **sem_cor do J1 medido por ele:** faces 100% pretas = 7,68% da area; pixels quase-pretos nas previas = 0,03-0,07% - a leitura "majoritariamente interno/oculto" se sustenta; no J8 (1 vista) o preto aparece nas costas (21,02% da area) e esta declarado, como desenhado.

Pendencias nomeadas (nenhuma bloqueia o fechamento; entram na fila da Etapa COR):

- **D-T2-1 (S3):** a autochecagem de alinhamento ACEITOU uma forma sabotada com o eixo X esticado 2x (mediana 0,02101 < 0,05 - a mediana e insensivel a deformacao anisotropica). No fluxo real a forma transferida e sempre a do proprio job, por isso S3 e nao S2. Correcao exigida ANTES de a transferencia ser tratada como guarda para formas de origem externa ao job: acrescentar razao por eixo das caixas e/ou percentil p90 a autochecagem, registrando a nova regua na COR-07. Ate la, proibido citar a transferencia como guarda contra "forma errada" sem esta ressalva.
- **D-T2-2 (S4):** o relatorio da etapa `cor` no modo projecao nao declara `modo_cor`/`rotulo` (o modo so aparece nas opcoes do job) - assimetria de coerencia; no vertice a declaracao e completa.
- **D-T2-3 (S4):** aviso do worker menciona "bake v1" tambem no modo vertice (texto velho; no vertice nao ha bake).
- **D-T2-4 (S4, latente):** `verificar_glb_vertice` inspeciona so o primeiro primitivo do primeiro mesh - inalcancavel hoje (a importacao unifica os objetos; a prova multi-objeto do Critico saiu com 1 primitivo); defesa em profundidade futura: iterar todos os primitivos de todos os meshes.
- **Herdadas e inalteradas:** D1 ABERTA; exposicao web/MCP de `cor`/`cor_modo` pendente desde a COR-05; S2-3 (troca esquerda/direita nas imagens da Besta) aberta.
- **Espelho no Drive (fechamento formal do T2 + registro da COR-08):** ESTADO_ATUAL, REGISTRO, ESTUDO_MELHORIAS e ESTUDO_D1_FIDELIDADE atualizados em `Oficina3D_v2\REGISTRO` via conector e conferidos por MD5 na volta (Drive = PC; 7/7 com CRITICO-t2-relatorio, DECISOES e APRENDIZADO_E_FLUXO, que ja estavam identicos). SHA-256 (prefixos de 12 hex): ESTADO_ATUAL 3E44D47C8A8A, REGISTRO 450572584E41 (versao espelhada; o REGISTRO commitado difere dela so por esta linha de espelho), ESTUDO_MELHORIAS 3C640E62F597, ESTUDO_D1_FIDELIDADE 467D866EB198, CRITICO-t2-relatorio 3DF49D3BDA2F. Com isso a T2 (COR-07) esta FECHADA em todas as vias (repo, GitHub e Drive); proximo passo declarado no ESTADO: COR-08 como prioridade da fidelidade de cor; T7 (UltraTex) segue como spike a frente do T3.


## 2026-11-01 - T2 (COR-07) FECHADA formalmente + COR-08 registrada (frente de fidelidade da cor, ataque a D1)

- **Fechamento formal do T2:** o veredito do Critico senior (entrada anterior) e o ESTADO_ATUAL ja declaravam o fechamento; esta rodada completou a papelada no escopo exato do veredito (L-33: mecanismo x visual separados). Numeros da tranche: suite 285 testes (reexecutada pelo Critico: 0 falhas, skipped=1); passo de cor de vertice 1,93-2,57 s contra 175,6 s do passo de projecao; determinismo byte-identico J1 = J2 (SHA 949E3CF7...) reproduzido pelo proprio Critico; regressao zero (ancoras da COR-05 byte-exatas sob o codigo novo: textura EBD744A9..., modelo 0F838538..., refinado 5467F25E...).
- **Destino da D-T2-1 (S3): TRANCHE FUTURA, como manda o veredito** ("correcao exigida antes de a transferencia ser tratada como rede de seguranca para formas de origem externa ao job"; a S3 nao bloqueia o fechamento). Registrada como item nomeado no backlog (ESTUDO_MELHORIAS, secao T2) junto de D-T2-2/3/4 (S4), com o motivo e a correcao exigida (razao por eixo das caixas e/ou p90; nova regua registrada na COR-07). Nao foi improvisada neste fechamento: e mudanca de codigo do passo de vertice e exige nova prova de sabotagem + re-verificacao do Critico.
- **COR-08 registrada no backlog (ESTUDO_MELHORIAS)** como a frente de fidelidade da cor e prioridade da Etapa COR apos o T2; estudo completo copiado para **docs/ESTUDO_D1_FIDELIDADE.md** (30.549 B) e ponteiro no ESTADO_ATUAL. Diagnostico medido: IoU de silhueta 0,72-0,79 por vista; cobertura direta ~19-20% dos texels; ~81% da textura por dilatacao UV (o confete); 4,247 texels/face na prova a 1024; salto de costura medio 93,49 x 36,20 interno. Alavancas em ordem: A1 alinhamento que otimiza o IoU (alvo >= 0,88/vista), A2 bake em 2048 com o gutter da D-T5-1, A3 preenchimento por adjacencia 3D no lugar da dilatacao UV + licao do comparativo Blender (mistura ponderada com oclusao, sem dilatacao agressiva). Prova desenhada sobre o job-ancora da COR-05, com aceite visual separado do de mecanismo.

## 2026-11-01 - D-T2 FECHADA: pendencias do veredito T2 (D-T2-1/2/3/4) com veredito do Critico senior

Relatorio integral: docs/CRITICO-dt2-relatorio.md (SHA-256 05527A062D7076E72485F8CDB58F6E565943FA5EC4AAA6D3169C49E99A856027). Veredito: **MECANISMO APROVADO 9,5/10, nenhum defeito S1/S2; QUALIDADE VISUAL NAO JULGADA** (nenhum resultado visual novo nesta tranche: nenhum modelo, textura ou previa nova para o Mestre ver; a D1 segue ABERTA e intocada). A S3 do T2 (D-T2-1) esta FECHADA.

**Execucao (executor, caminho real do Blender, par legitimo TripoSR Orc do job 20261101-131410-crit-t2-soforma):** a regra nova de aceite da transferencia da cor da forma (`oficina3d.cor.vertice.avaliar_alinhamento_forma`, chamada em `oficina3d/cor/_blender_vertice.py:transferir_forma`) soma mediana + p90 das distancias (fracao da altura) + razao por eixo das caixas (forma mapeada / refinado), limites mediana 0,05, p90 0,10, caixa [0,80, 1,25]. Medicoes: legitimo mediana 0,00056 / p90 0,0013 / caixas x 1,00098 / y 1,00184 / z 1,0 -> aceito, 27.421/27.421 vertices pela forma; X2 mediana 0,02022 / p90 0,08138 / caixa X 2,002 -> RECUSADO pela caixa (a regra antiga aceitava: mediana < 0,05); X0,5 mediana 0,04348 / p90 0,12702 / caixa X 0,500 -> RECUSADO pelo p90; X1,15 mediana 0,00721 / p90 0,02362 / caixa X 1,151 -> aceito (controle: a faixa nao e gatilho sensivel). O p90 0,10 NAO pega o X2 sozinho: a caixa e a guarda primaria contra esticamento, o p90 e guarda secundaria contra deformacoes que preservam a caixa. Caso so-forma recusado falha com 'nenhuma fonte pintou vertice algum' (falha segura e declarada, nao modelo sem cor em silencio).

**Bateria do Critico (mais rigorosa que a do T2; 10 verificacoes novas registradas no relatorio dele):** reproducao propria do X2 (numeros identicos); sabotagens em Y (Y2 recusada pela caixa; Y0,5 recusada pela caixa com p90 0,09779 < 0,10, provando que a caixa e necessaria mesmo onde o p90 falha); sabotagem em Z (Z2 recusada; a escala pela altura a mostra como compressao X/Y); caso misto (4 vistas + forma X2: conclui pelas vistas, vista 20.034 / forma 0 / propagacao 5.450 / sem_cor 1.937, recusa declarada); arestas do verificador (sem meshes -> ok=False; 3 primitivos com o terceiro sem COLOR_0 -> ok=False); D-T2-2 fora do mock (passo de projecao real, so CPU, sobre o refinado existente: `modo_cor=projecao`, `rotulo=padrao`, modelo_cor.glb 1.643.868 B + textura.png 513.019 B + 4 previas); suite conferida arquivo a arquivo (294 = soma dos metodos); bordas da regra (razao 0,80 aceita; mediana 0,05 e p90 0,10 exatos aceitos; amostra vazia recusada). Suite do executor no fechamento: **296 testes OK, skipped=1** (294 + 2 novos da S4-2).

**Correcao de artefato (exigencia 5 do Critico):** o `resumo_passo.json` alegado na ordem de servico NAO existe - o probe do executor quebrou no caso X2 (o erro do passo, esperado, nao era tolerado naquele script) antes de gravar o resumo. Os numeros do legitimo/X2 vivem em `probe-dt2/probe.log` e nos `resultado_vertice.json` de cada job (`probe-dt2/job_legit`, `job_x2`, `job_x05`, `job_x115`); o resumo dos casos tolerados vive em `probe-dt2/resumo_passo2.json`; as provas do Critico vivem em `probe-dt2-crit/`. A proxima auditoria nao deve procurar um `resumo_passo.json` que nao ha.

**Ressalvas S4 do Critico, corrigidas neste fechamento (nenhuma bloqueadora):** S4-1 - `verificar_glb_vertice` com acessor COLOR_0 invalido dava `IndexError`; agora primitivo malformado conta como sem cor (prova S41: acessor 9999, sem POSITION, acessor sem count e sem meshes -> ok=False sem excecao; normal -> ok=True). S4-2 - `avaliar_alinhamento_forma` aceitava dict parcial; agora exige x/y/z (dict incompleto -> recusa com motivo proprio) + `_aviso_vistas_ignoradas` usa `.get` (nao quebra sem a chave); 2 testes novos. S4-3 - DECISOES COR-07 atualizada para a regra D-T2-1 (linha D-T2 propria). S4-4 - docstring 'bake v1' de `selecionar_vistas` trocada por 'passo de cor' (a mencao restante em `worker.py` e historico do texto antigo, na docstring do proprio helper).

**LIMITE DA GUARDA (frase exigida pelo Critico, item f):** a regra nova pega deformacao global anisotropica; NAO atesta identidade da forma (uma forma de outro personagem com as mesmas proporcoes passaria) nem deformacao local pequena. Sem esta frase, a guarda nao deve ser citada no futuro como algo que ela nao e. Dentro do fluxo real (forma do proprio job), a guarda cumpre o papel.

**Pendencias apos o fechamento:** D1 ABERTA (proximo passo: COR-08, frente de fidelidade da cor); S2-3 (troca esq/dir da Besta) ABERTA e bloqueando a textura base; exposicao web/MCP de `cor`/`cor_modo` pendente desde a COR-05; T7 (UltraTex) segue como spike a frente do T3.
- **Espelho no Drive (fechamento D-T2):** ESTADO_ATUAL, REGISTRO, DECISOES, APRENDIZADO_E_FLUXO e CRITICO-dt2-relatorio atualizados em `Oficina3D_v2\REGISTRO` via G: e conferidos por SHA-256 na volta (Drive = PC; 5/5). A copia espelhada do REGISTRO difere desta versao commitada so por esta linha de espelho.

## 2026-11-01 — REF-01 lote 4 parcial (diagonais traseiras do Orc): tras_dir APROVADA, tras_esq REPROVADA

- **Geração (rodada anterior, ~14:0x):** 4 diagonais do Orc a partir das fontes reais (frente/costas canônicas +
  `orc_tresquartos_v2.png` aprovada no lote 1), dentro do teto de 4 imagens por rodada. Convenções das lições:
  tom verde-oliva da frente canônica (D5), palmas para baixo (D15), zero bolsinhas (D9/D11), sem machado
  (como a tresquartos aprovada), corpo inteiro sem corte.
- **AUTOAUDITORIA adversarial do executor (APR-02, antes do Crítico):** o par FRONTAL foi reprovado pelo próprio
  executor — SYM S2, espelhamento (cabeça-de-lobo à esquerda de quem olha numa vista frontal, impossível sem
  espelho) — e NÃO foi instalado no PC nem submetido ao Crítico. SHAs dos reprovados, guardados só como registro
  do erro: frente-dir 3936A192…, frente-esq 6214C6B1…. Arquivo da autoauditoria:
  `oficina-audit/autoauditoria-orc-diag-tras.md`. A tresquartos_v2 aprovada já cobre a diagonal frontal DIREITA
  (ombreira proeminente à esquerda de quem olha); falta, portanto, só a diagonal frontal ESQUERDA.
- **Veredito do Crítico Visual sênior (docs/CRITICO-ref01-lote4-tras.md), só o par traseiro: tras_dir APROVADA;
  tras_esq REPROVADA; LOTE 4 parcial (traseiras) REPROVADO.** Sem defeitos S1.
- **Defeito único com força de reprovação — SYM-4.1 S2: a "esq" é a diagonal direita duplicada.** Provas medidas
  pelo Crítico: rosto em perfil à direita nas duas; pé em perfil à direita nas duas; assimetria da faixa inferior
  no mesmo sentido (tras_dir 1,78; tras_esq 1,75; costas retas 1,02 — uma esquerda genuína exigiria ~0,56); IoU
  entre as silhuetas 0,915, maior que a semelhança de cada uma com as costas retas (0,765/0,779). Diversidade
  lateral zero, não apenas baixa. Cada traseira isolada passava nas âncoras de costas — o defeito só aparece no PAR.
- **DEF-4.2 S4 (não bloqueia):** tom de pele levemente mais escuro/saturado que `costas_v2` (saturação +0,05,
  direção oposta ao D5); saiote vermelho conforme (Δ ≤ 3). Suspeitas da autoauditoria resolvidas: pés/mãos e alça
  dorsal fechados a favor das imagens; alça descer para o mesmo lado na frente e nas costas é convenção já
  consagrada pela autoridade, não defeito deste lote.
- **Arquivos:** `orc_diag_tras_dir.png` (SHA ACB515D2…B7372250B, 2.277.440 B) APROVADA — entra no arsenal do Orc
  como diagonal traseira direita. `orc_diag_tras_esq.png` (SHA 6D0B0B35…37A6CA26413, 2.128.241 B) REPROVADA e
  PERMANECE por enquanto em `testes/referencias/` no PC por causa do bloqueio anti-colisão desta rodada anterior —
  está REPROVADA e NÃO deve ser usada como referência; na próxima rodada ela deve ser SUBSTITUÍDA pela refeita
  (nunca mantida ao lado dela, conforme o relatório do Crítico).
- **Registro adiado uma vez pela regra anti-colisão** (árvore suja com a tranche da frente principal, HEAD 4b8384e)
  e concluído nesta rodada com a árvore limpa (HEAD c75cdd3, antes de qualquer escrita): instalado
  docs/CRITICO-ref01-lote4-tras.md junto destas edições. A numeração da lição nova foi confirmada nesta rodada
  (L-38: L-33 é a nota APR-02 e L-34 a L-37 já estavam ocupadas; o rascunho anterior dizia "L-29, a confirmar").
- **Retrabalho especificado pelo Crítico (tras_esq — próxima rodada):** NÃO espelhar `tras_dir` no editor (falso
  esquerdo com textura do dorso invertida). Gerar de novo do lado oposto: câmera na retaguarda ESQUERDA (lado da
  cabeça-de-lobo); rosto em perfil parcial apontando para a ESQUERDA; cabeça-de-lobo proeminente em primeiro
  plano à esquerda; ombreira recuada à direita; pé viewer-ESQUERDO em perfil apontando para a esquerda;
  pé viewer-direito traseiro; alça com fivela central descendo para o quadril viewer-ESQUERDO; caveira grande do
  cinto à ESQUERDA; capa proeminente à esquerda abaixo da cintura até meia-canela; zero bolsinhas, zero machado,
  corpo inteiro, fundo cinza-claro, tom oliva de `costas_v2`. Critério de aceite numérico do novo par: IoU com
  `tras_dir` < 0,85 E razão dir/esq da faixa inferior < 0,7 E pé em perfil no lado esquerdo — os três. A refeita
  volta ao Crítico antes de ser instalada como definitiva.
- **Retrabalho especificado pelo executor (frontal esquerda — próxima rodada):** pedido com instrução anti-espelho
  explícita ("a cabeça-de-lobo, que fica no ombro ESQUERDO dele, tem que aparecer à DIREITA da imagem; a ombreira
  de espinhos, no ombro DIREITO dele, à ESQUERDA da imagem; NÃO espelhar"). Orçamento da próxima rodada:
  2 imagens (tras_esq refeita + frontal esquerda), dentro do teto de 4.
- **Verificações novas do Crítico (escalada APR-01, seção 6):** N1 pureza do 3/4 traseiro; N2 diversidade angular
  MEDIDA do par (os três critérios obrigatórios); N3 tom medido por amostragem anatômica com filtro oliva.
  Registradas no checklist pré-Crítico e na lição L-38.

## 2026-11-01 - LIC-01 registrada: licenças não bloqueiam as frentes técnicas (decisão do Mestre)

- **Decisão do Mestre (01/11, 14:19), literal:** "Não precisa se preocupar com nenhuma licença, pode deixar que depois eu vou resolver isso." Registrada como **LIC-01** em DECISOES.md.
- **Efeito:** os fatos de licença do estudo de reuso × recriação (`docs/ESTUDO_REUSO_RECRIACAO.md`, copiado nesta rodada) — FLUX.2 sob BFL não-comercial, LoRAs/decoder do UltraTex com concessão não estabelecida, UltraTex/StableGen GPL-3.0, adaptador do SUPRA-Tex sob licença de pesquisa, Eyek/Comfy BlenderTools sem licença publicada — passam a ser INFORMAÇÃO registrada, não bloqueador: spikes, testes e estudos seguem sem trava de licença.
- **Limites da decisão:** adoção comercial de qualquer peça fica para quando o Mestre resolver as licenças; os fatos continuam registrados no estudo e no Gate 0 do T7; a DONO-01 (independência técnica) permanece valendo por mérito próprio.
