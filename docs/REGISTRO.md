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

