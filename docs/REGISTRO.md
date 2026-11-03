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

## [2026-11-01 17:10-17:45 -03] Claude: Fase 2 item 1, etapa `validar` (Godot headless)
- Mestre: "Pode" (resposta ao pedido de começar a Fase 2). O Muse já estava na Etapa COR (COR-08 em voo, sem commit); escolhi a frente **validar**, que não toca `oficina3d/cor`. Pedido do Muse (17:40): commitar separado, sem os arquivos de cor. Feito: `git add` só dos caminhos da validação.
- **Novo pacote `oficina3d/validar/`**: `glb.py` (régua 1: leitor de GLB em Python puro, magic/versão/comprimento/chunks, triângulos pelos accessors, imagens embutidas conferidas por magic bytes), `_godot_validar.gd` + `godot.py` (régua 2: Godot 4.7.2 `--headless` carregando por `GLTFDocument`, o caminho do jogo; sem janela), `__init__.py` (regras e perfis `oficina`/`jogo`; o `jogo` é o aceite EXP-01: <20 mil tris, 1 material, albedo <=1024 px, <=5 MB), `__main__.py` (`python -m oficina3d.validar arq.glb [--perfil jogo]`; saída 0/1/2).
- **Ligado ao worker** como etapa 3c (depois de refino/cor, antes de exportar): opções novas `validar` (True) e `validar_perfil` ("oficina") em `config.OPCOES_PADRAO`, regra em `job._validar_opcao`. Reprovado ou validador quebrado = **aviso**, nunca erro do job. Grava `saida/validacao.json` e `resultado.validacao`.
- **Dois achados ao vivo** (ver ERROS): (1) no `--headless` a malha vem como `ImporterMeshInstance3D` (o script conta as duas formas e tira a caixa dos vértices); (2) o modo padrão de imagem do `GLTFState` (1, extrair texturas) **derruba o Godot 4.7.2** (0xC0000005) num GLB com textura; o validador usa o modo 3 (embutir sem compressão).
- **Testes:** `testes/test_validar.py`, 18 testes (GLBs montados byte a byte, com e sem PNG). Prova de mutação: voltando o modo de imagem para 1, `test_textura_nao_derruba_o_godot` dá ERROR; restaurado. **Suíte inteira no `.venv_app`: 341 testes, OK (skipped=1)**, incluindo os testes de cor ainda sem commit do Muse.
- **Validação manual** (CLI) em GLBs reais: modelo sem cor de 24.874 tris → `oficina` APROVADO, `jogo` REPROVADO (tris, albedo); `jobs_teste\cor08\cor08\modelo_cor.glb` → `jogo` REPROVADO (49.750 tris; 5,979 MB; albedo 2048 px), resto ok.
- **Prova viva pelo worker** (fila de TESTE, sem GPU): job `20261101-173915-prova-validar-jogo` em `jobs_teste\prova_validar` (`so-refinar` sobre `jobs\20261031-225432-provac-orc-s7\forma\forma.glb`, `validar_perfil=jogo`) → **concluído**; refino 23,9 s, validar 1,91 s; réguas batem (49.750 = 49.750), pivô y=0,0, 2,173 MB; reprovado em `max_triangulos` e `textura_albedo` (correto: sem `--cor`), virou aviso. SHA-256: `validacao.json` A9F5532F…2C124A92, `modelo.glb` 88C30236…E310E12514.
- **PENDENTE:** as 8 capturas de tela do plano (o `--headless` não renderiza; renderizar abre janela e disputa a tela do dono do PC); a etapa ainda não aparece nas opções da web/MCP/CLI (só via `opcoes`); o worker em serviço (do Muse) só passa a validar depois de ser reiniciado. Não reiniciei: é processo do Muse.
- SHA-256 (16 primeiros) dos arquivos novos: glb.py D1832E105AED7241, godot.py 55248F3DC5B30896, _godot_validar.gd 25C1E505800586D0, __init__.py D8F6F21B7C5247E4, __main__.py 5307F9414503F53E, test_validar.py EF0FBB22B715DA0A.


## 2026-11-01 — COR-08 FECHADA (Etapa COR, ataque a D1: A0+A1+A2+A3) — veredito do Critico senior

- **Reconciliacao desta rodada (REG-01 / anti-colisao):** esta execucao encontrou a arvore suja com DUAS tranches (COR-08 do Muse + validar do Claude) e NAO duplicou nenhuma delas. Durante a rodada, o Claude commitou o validar sozinho (29ebaa9, VAL-01, a pedido do Muse as 17:40: commitar separado, sem os arquivos de cor); a partir dai a arvore suja passou a conter SOMENTE a COR-08, e esta rodada fechou o registro dela. O codigo da COR-08 nao foi reescrito aqui: ele ja estava pronto e criticado; o trabalho desta rodada foi conferir, registrar e commitar.
- **O que a COR-08 muda (estudo docs/ESTUDO_D1_FIDELIDADE.md, alavancas A0-A3):** A0 — caixa robusta a partir da mascara rasterizada (nao dos vertices; o machado fora de pose nao manda nos extremos); A1 — `otimizar_alinhamento` em `oficina3d/cor/projecao.py`: busca deterministica (grade grossa->fina) maximizando o IoU a 256 px, escala uniforme primeiro e afim com trava de aspecto |ax/ay-1| <= 0,15; A2 — bake em 2048 (TAMANHO_TEXTURA 1024 -> 2048), casado com o gutter da D-T5-1; A3 — `oficina3d/cor/preenchimento.py`: preenchimento 3D das zonas cegas por difusao BFS sobre o grafo dual com solda por posicao (a dilatacao UV sobrevive so como halo fora da UV, 8 px). `passo.py` nao fixa os controles (S3-COR08-4, abaixo).
- **Numeros (re-medidos pelo Critico, docs/CRITICO-cor08-relatorio.md; nao re-medidos por esta rodada de registro):** IoUs bake COR-08 frente 0,8177 / costas 0,7774 / esquerda 0,8065 / direita 0,7957, contra baseline bbox 0,7941 / 0,7232 / 0,7925 / 0,7892; cobertura direta 420.713/845.063 = 49,79% (baseline 48,08%); ablacao A0 a 1024: 19,44% -> 48,12% (prova de que a A0, nao a resolucao, explica o salto — o diff do caminho de projecao entre a COR-05 e a base da COR-08 e vazio); textura SHA-256 c7302ee16f41a8f12577546223d509a906986fada1d3f39b61af1a35f4af989a; GLB a8e793b267db27c2a06669dbb925c91b8863a99ec4f43f558c880a1d10a09b9a; determinismo PROVADO em 3 bakes (det do executor + reproducao independente do Critico, mesmos SHAs); faces com fonte 24.590, preenchidas 25.160, sem fonte alcancavel 0, anel medio 3,18 (max 21); proveniencia v2: 845.063 texels UV recomputados, diff 0; halo 2.709.638, diff 0; nenhum texel DENTRO da UV recebeu cor de dilatacao UV no modo 3d.
- **Suite:** o Critico re-executou o discovery no .venv_app: **323 testes OK, skipped=1** (test_cor 31, test_cor_alinhamento 10, test_cor_preenchimento 8, resto reconciliado por modulo). Com o validar do Claude, a suite combinada e **341 OK, skipped=1** (323 + 18), medida no commit 29ebaa9.
- **AUTOAUDITORIA (APR-02, confrontada pelo Critico, secao 8 do relatorio):** nao havia documento de autoauditoria no repo na hora da critica (a tranche ainda nao tinha atualizado REGISTRO/ESTADO — esperado pre-commit; este registro supre a lacuna). Os 3 defeitos alegados pelo executor foram CONFIRMADOS pelo Critico: (1) `dilatar` sem o parametro `dominio` (corrigido; teste novo o exerce); (2) A3 existia mas nao estava ligada ao bake (hoje ligada, controle `preenchimento` com default "3d"); (3) limiar +0,08 insatisfazivel em `test_recupera_protrusao` (prova analitica propria do Critico: maximo exato 0,93632959 = 2500/2670; o teste hoje afirma o que o caso realmente prova). Correcao honesta, nao mascara.
- **VEREDITO — MECANISMO: APROVADO 8,5/10.** A0-A3 funcionam como alegado. Desconto: o S2 do caminho de salvamento (pre-existente, nao regressao da COR-08) + S3 de nomenclatura/documentacao.
- **VEREDITO — QUALIDADE VISUAL: APROVADA 7,0/10, COM RESSALVA EXPLICITA.** Nenhum gatilho do padrao do olho do Mestre disparou: sem confete generalizado, rosto legivel nas 4 vistas em que aparece, regioes de cor se sustentam (pele verde, pano vermelho, pelo, armadura, osso); a COR-08 e um pouco mais limpa que a baseline. **A ressalva faz parte do veredito e nao pode ser omitida ao cita-lo: esta aprovacao visual NAO e aprovacao de fidelidade a arte** — o modelo continua longe da arte canonica em detalhe fino, e o gap e de pose/geometria, nao so de alinhamento. Nunca citar esta secao como "a cor foi aprovada" sem a ressalva (L-33).
- **D1: ABERTA (confirmado, nao refutado).** Nenhuma vista atinge a regua >= 0,88 do estudo D1; maximo medido: frente 0,8177. O proximo ataque precisa mirar o que o IoU nao alcanca: a diferenca de pose/proporcao entre arte e malha (A8 segue estacionada como contingencia; nenhuma afinidade fecha proporcao divergente).
- **Pendencias abertas nomeadas (do veredito; nenhuma bloqueia o commit do mecanismo, todas bloqueiam alguma afirmacao futura):**
  - **S2-COR08-1 (sRGB x LINEAR — PROXIMO PASSO, antes de qualquer afirmacao de fidelidade via `textura.png`):** a arte e lida sem decodificacao sRGB (bytes crus tratados como lineares), as medias sao tiradas em espaco sRGB, e o `save_render` sob o default AgX mapeia branco 255 -> 197 (-23%): o `textura.png` entregue e AgX(textura do GLB), nao a textura entregue (diff media global 5,57/255 na COR-08; so 15,5% dos texels UV identicos entre os dois arquivos). O GLB entregue e fiel aos bytes da arte nos texels diretos. **Correcao provada pelo Critico: fixar `cena.view_settings.view_transform = "Standard"` antes do `save_render` em `_blender_cor.py` (sonda: Standard = identidade byte a byte) + teste de regressao. NAO usar "Raw": a sonda mediu Raw = curva de potencia 2.2 (0,5 -> 55), ou seja, escurece.** Ate o fix, quem seguir a D10 ("amostrar a textura") deve amostrar o GLB, nao o `textura.png`.
  - S3-COR08-2: campo `texels_por_dilatacao_restrita` mente no modo `uv` (carrega o total da dilatacao irrestrita); renomear/separar.
  - S3-COR08-3: argumento da ablacao via IoU e vazio (IoU@256 e invariante ao tamanho da textura); e os IoUs da ancora "0,7237-0,7929" nao tem lastro no `resultado_cor.json` da ancora (la, `iou_bake_256 = None`) — a citacao fica corrigida neste registro: os IoUs da ancora sao do diagnostico de silhueta do estudo D1, nao de um IoU de bake medido.
  - S3-COR08-4: `passo.py` nao fixa `alinhamento` nem `preenchimento` no `pedido_cor` (a fila depende dos defaults de `_blender_cor.py`); fixar as chaves.
  - S4-COR08-5: `margem_min_px` medida numa grade 512 e escalada (4 @1024 e 8 @2048 sao A MESMA margem); reportar normalizado ou renomear.
  - S4-COR08-6: `dominio_dilatacao_restrita` exclui os texels das faces inalcancaveis, mas NAO a faixa de 8 px ao redor delas (o halo continua pintado; sem impacto visual direto, pois esta fora de qualquer triangulo) — documentar com essas palavras.
- **Limites registrados pelo Critico (nao inventados):** renders flat/unlit independentes falharam 3x (quirk do harness de importacao no Blender 5.2, nao defeito da tranche; evidencia visual = previas do proprio bake + analise numerica direta); verificacao per-texel da fonte BFS coberta indiretamente (recomendacao: o bake passar a salvar o mapa texel-face e a mascara de proveniencia como artefatos do job); tempos de bake variam (47,8 s na reproducao do Critico vs 54,35 s do executor) — os SHAs nao variam.
- **Licoes novas:** L-39 (sRGB/AgX no salvamento), L-40 (IoU invariante a resolucao + nome de campo que mente) — ver APRENDIZADO_E_FLUXO.md.
- **Espelho no Drive (fechamento COR-08):** ESTADO_ATUAL, REGISTRO, DECISOES, APRENDIZADO_E_FLUXO e CRITICO-cor08-relatorio atualizados em `Oficina3D_v2\REGISTRO` via G: e conferidos por SHA-256 na volta (Drive = PC; 5/5).

## 2026-11-01 — S2-COR08-1 DESDOBRADO (salvamento FECHADO; pipeline linear ABERTA) — veredito do Critico senior

- **Reconciliacao desta rodada (REG-01 / anti-colisao):** a execucao comecou com a leitura inicial do executor dizendo HEAD 29ebaa9 — leitura ERRADA, corrigida aqui: o topo ja era 27704b1 (COR-08, 18:13) desde antes da execucao. A brief do Critico repetiu o 29ebaa9 (e o Critico citou 26b6a13, registrado por ele como S4-3, sem impacto). Durante a execucao, o topo de main avancou para 26b6a13 (docs: observacao do Mestre 18:59, hipotese de raiz da D1, H1/H2/H3), que so toca docs/ESTADO_ATUAL.md (+12) e nao toca o codigo desta tranche. O commit desta tranche vai sobre 26b6a13; o push publica os dois (26b6a13 estava ahead of origin by 1). Nenhuma duplicacao: a tranche S2 nao foi reescrita por ninguem.
- **O fix:** `oficina3d/cor/_blender_cor.py:546` — `bpy.context.scene.view_settings.view_transform = "Standard"` na linha imediatamente anterior ao `img.save_render` (547), dentro de `main()`, sem try/except de proposito (se a cena nao aceitar Standard, o bake falha alto em vez de entregar textura falsificada). `testes/test_cor.py`: classe `TestSaveRenderStandard` (2 testes: ordem Standard→save dentro de main() + caminho unico de save_render no app).
- **Provas do executor (jobs_teste/s2cor08-1, via tarefa agendada pythonw, invisivel):** a primeira tentativa com processo destacado via Start-Process morreu com a sessao SSH (sem status, sem stderr) — relancada via tarefa agendada, que foi removida apos o uso (L-41). Bake sintetico (cubo, cores puras): textura vs PNG do GLB 100% identicos, diff 0; cores puras exatas (vermelho 8084, verde 11645, azul 10965, amarelo 15130). Reproducao COR-08 (Orc Prata, ancora COR-05, 2048, otimizado, 3d): GLB SHA-256 IDENTICO ao da COR-08 (`a8e793b2...`, exportacao verbatim, nao tocada pelo fix); textura SHA-256 MUDOU (`c7302ee1...` -> `e4056741...`); textura vs GLB 100% identicos, diff 0 (na COR-08 eram 15,5%). Suite: **343 testes OK, skipped=1, 28,42 s** no .venv_app (a primeira corrida guardada no status.json era pre-correcao do Path e dizia FAILED — ver S3-1).
- **AUTOAUDITORIA (APR-02, confrontada pelo Critico — os 4 itens procedentes):** (i) `main()` nao tem variavel `cena` — fix ingenuo daria NameError; o fix usa `bpy.context.scene` (padrao de `renderizar_previas`); (ii) teste inicial comparava string com `/` e falhava no Windows (`\`) — corrigido para objetos Path, `test_cor.py` 33/33; (iii) prova destacada morta com a sessao SSH — relancada via tarefa pythonw; (iv) driver da prova lia chaves erradas (`iou_bake_256` no topo, `texels_diretos`) e gravava nulls — os nomes reais sao `por_vista.<vista>.iou_bake_256` e `cobertura.texels_pintados_direto`; nenhuma alegacao de SHA/pixel dependia deles.
- **VEREDITO — MECANISMO: APROVADO 9,0/10** (docs/CRITICO-s2cor08-1-relatorio.md). **QUALIDADE VISUAL: NAO julgada nesta tranche** (nenhuma alegacao nova; as previas do bake novo sao pixel-identicas as da COR-08 — prova AUSENCIA DE MUDANCA visual, nao aprovacao de qualidade; o visual 7,0/10 com ressalva da COR-08 segue inalterado).
- **VEREDITO — S2-COR08-1: DESDOBRADO (decisao do Critico, registrada aqui).** O S2 como escrito e "caminho de salvamento + medias em espaco sRGB" (carga sem decodificacao sRGB + `cores_diretas_por_face` tirando media de bytes sRGB). O fix corrige SO o salvamento — e a propria COR-08 prescreve o fix do salvamento + regressao como "correcao provada", classificando o erro das medias como "parte do S2" mas "nao quantificado como bloqueador isolado". Logo: **S2-salvamento FECHADO** (falsificacao 255->197 eliminada e provada); **S2-pipeline-linear ABERTA como pendencia nova nomeada** (afeta os VALORES pintados; erro pequeno para cores proximas, maior para alto contraste, ainda nao quantificado). Fechar o S2 integral aqui enterraria a metade das medias em silencio. Consequencia: nenhuma publicacao pode dizer "fidelidade de cor resolvida", nem a D1 pode ser dada como fechada em fidelidade de cor, ate essa pendencia ser quantificada ou decidida pelo Mestre.
- **Verificacoes NOVAS do Critico (alem da bateria da COR-08):** N1 controle negativo pre-fix (GLB identico, textura vs GLB so 30,08%, diff_max 110, ZERO cores puras — a prova discrimina); N2 mutacao do teste (5 variantes: base OK, 4 falsas FALHAM — nao e tautologico quanto a local, ordem e sobrescrita); N3 diff vazio de `resultado_cor.json` novo vs `cor08rep` (IoUs, cobertura 420713/845063, dilatacao 2709638, tudo identico; so a textura mudou); N4 previas 4/4 pixel-identicas, IDAT igual (o fix nao tocou as previas); N5 varredura do app (unico save_render e o do fix; nenhum codigo le textura.png esperando AgX); N6 suite re-executada (343 OK, 28,26 s); N7 proveniencia das ancoras (SHAs conferem com `cor08rep`); N8 curva AgX re-medida no par antigo (15,554%, diff_max 64, media RGB 5,58 — igual a COR-08).
- **Armadilha desarmada (L-42):** a primeira comparacao do Critico usou `jobs/20261101-101528-corint-orc-s7/cor/` como "COR-08" e divergiu — aquele diretorio guarda um bake ANTIGO a 1024 (o proprio codigo o chama de baseline superada, `textura ebd744a9...`). A baseline correta da COR-08 e `jobs_teste/cor08-critico/cor08rep/` (2048). Quem re-checar deve usar `cor08rep`, nao o diretorio do job.
- **Defeitos do Critico e correcoes (condicoes, nao reprovacao):** S3-1 status.json contraditorio (bloco suite velho) — ANOTADO com a corrida final, original preservado; S3-2 driver com chaves erradas — CORRIGIDO para os nomes reais (+ docstring em raw, fim do SyntaxWarning); S4-1/S4-2 rigidez do teste (grafia exata; fatia ate o EOF) — DOCUMENTADA na docstring do teste (opcao "documentar"). Nenhum defeito S1/S2 no fix, no teste ou no mecanismo.
- **Limites registrados pelo Critico (nao inventados):** a figura "15,5%" da COR-08 foi re-medida como 15,554% sobre a imagem inteira do par antigo (o relatorio a descreve sobre texels UV — ressalva de dominio, nao divergencia); contagens da suite por arquivo nao re-extraidas (total 343 conferido).
- **Pendencias apos o fechamento:** S2-pipeline-linear ABERTA (nova); S3-COR08-2/3/4; S4-COR08-5/6. **PROXIMO PASSO (ordem do Mestre 18:59, secao Observacao do ESTADO): diagnostico de raiz da D1 (H1/H2/H3) ANTES de novas tranches de cor; o diagnostico reordena o ataque.** S3/S4 seguem nomeados para apos o diagnostico.
- **Espelho no Drive (fechamento S2-COR08-1):** ESTADO_ATUAL, REGISTRO, APRENDIZADO_E_FLUXO, ESTUDO_MELHORIAS e CRITICO-s2cor08-1-relatorio atualizados em `Oficina3D_v2\REGISTRO` via G: e conferidos por SHA-256 na volta (Drive = PC; 5/5; prefixos de 12 hex: ESTADO_ATUAL 266992A854C3, REGISTRO 24882232768D, APRENDIZADO_E_FLUXO 871ADCB56347, ESTUDO_MELHORIAS B324126D4EB9, CRITICO-s2cor08-1-relatorio 0B469D2A3F44; DECISOES.md ja identica, sem alteracao nesta tranche). O REGISTRO commitado difere do espelhado so por esta linha de espelho.

## 2026-11-01 — REF-01 lote 4 FECHADO nas traseiras (reconciliação de três Críticos) + frontal direita aberta

- **Histórico do atraso (anti-colisão, 3 adiamentos):** o retrabalho foi julgado
  em 01/11 ~15:2x (Crítico 1), o conflito entre Críticos em ~16:07 (Crítico 2) e
  a reconciliação por ordem do Mestre em ~16:41 (terceiro Crítico) — e em todas
  as rodadas seguintes a árvore do PC estava suja pela frente principal
  (tranche COR-08, HEAD `0e8746e`; depois `27704b1` com a tranche S2-COR08-1 em
  curso em 01/11 ~19:0x, o que adiou a aplicação mais uma vez). Pela regra
  anti-colisão da frente REF-01, NENHUMA escrita foi feita no repo nessas
  rodadas. [Aplicacao: rodada REF-01 agendada 01/11/2026 19:54, arvore limpa confirmada antes de qualquer escrita (git status vazio), HEAD f4942ae; S2-COR08-1 ja fechado no commit 22b9d5c.]
- **Instalação (testes/referencias/, gitignored — arte do RPG nunca entra no
  git, conferido com `git check-ignore`):** `orc_diag_tras_esq.png` SUBSTITUÍDA
  pela refeita aprovada — SHA-256 PC após a cópia =
  `ad57447a31c9743b9d40967a0824d0fee3d85848c84d3b2665d6ce59c95c618e`
  (2.274.898 B), idêntico ao local e ao da reconciliação. A reprovada
  `6D0B0B35…37A6CA26413` NÃO existe mais no PC como referência (não há duas
  "esquerdas"); o conteúdo reprovado segue preservado só no bruto local do
  executor. `orc_diag_tras_dir.png` conferida intacta após a troca:
  `ACB515D2…B7372250B`. **NÃO instalada** `orc_diag_frente_esq.png`
  (reprovada por duplicidade; fica só local, como registro do erro).
- **Vereditos finais (relatórios integrais em docs/, sem apagar nenhum):**
  `docs/CRITICO-ref01-lote4-retrabalho.md` (Crítico 1),
  `docs/CRITICO-ref01-lote4-v2.md` (Crítico 2 — registro-resumo fiel; o texto
  integral do handoff ~16:07 não ficou preservado em arquivo, e isso está
  declarado no cabeçalho do próprio documento, sem tabelas recriadas) e
  `docs/CRITICO-ref01-lote4-reconciliacao.md` (terceiro Crítico, ordem do
  Mestre) — este último PREVALECE.
- **Crítico 1 (retrabalho):** refeita APROVADA — N2 nos três critérios por
  medição independente (IoU com `tras_dir` 0,732 < 0,85; faixa 0,521 contra
  1,774 da direita, sentidos invertidos; pé em perfil em lados opostos);
  N1 passa; N3 passa (saiote Δ=(1,4,3) contra a frente canônica). **ESP-4.1 /
  ESP-4.2 — dois itens da especificação anterior provados ERRADOS contra as
  fontes (corrigir o item, não a imagem):** item 5 (alça descendo para o
  quadril viewer-esquerdo) — nas costas a diagonal é superior-esquerda →
  inferior-direita, descendo para o quadril viewer-direito, como em
  `costas_v2`/`tras_dir`; item 6 (caveira grande à esquerda) — o conjunto
  caveira+argolas+pingente está à DIREITA em TODAS as cinco vistas existentes.
  **Frente esquerda REPROVADA como entrada nova — DUP-4.3 S2:** é a
  `tresquartos_v2` re-renderizada (IoU 0,960, todas as âncoras iguais).
  Verificações novas: N4 (lateralização por vista cruzada) e N5 (novidade
  angular: IoU > 0,90 contra vista aprovada = duplicata).
- **Crítico 2 (v2):** refeita REPROVADA (SYM-5.1 alça não espelhada + SYM-5.2
  caveira à direita, regra nova NV-1 "exigir inversão entre frente e
  costas"); frente esquerda APROVADA (S3 giro fraco ~20°) sem mencionar a
  duplicidade; `tras_dir` mantida "com o desvio anotado" pelo mesmo traço —
  incoerência interna. Verificações novas dele: NV-1, NV-2 (solos, > 0,04 =
  pé fora do solo), NV-3 (fundo + margens).
- **Reconciliação (terceiro Crítico, re-medição própria com 3 limiares de
  fundo + grade impressa de 0,1):** Crítico 1 acertou os DOIS vereditos; Crítico
  2 acertou os FATOS e errou todas as decisões. Números do reconciliador:
  IoU refeita × `tras_dir` 0,734 (0,730–0,738); faixa 0,580 × 1,601 (invertida);
  grade da caveira: frente 0,57 / costas 0,56 / refeita 0,64 — sempre à direita
  (o 0,76 do Crítico 2 erra por +0,12); IoU frente_esq × `tresquartos_v2`
  0,962 (DUP-4.3 confirmado). **REGRA FINAL (§5 da reconciliação, uma frase):**
  em qualquer vista nova do Orc, o kit fixo ao corpo se desenha exatamente
  como nas vistas aprovadas da mesma família — caveira grande sempre à
  DIREITA do losango em coordenadas de imagem e alça sempre na diagonal
  superior-esquerda → inferior-direita — mudando de lado apenas os sinais da
  câmera (lobo, ombreira, perfil do rosto, pé em perfil). Fundamento corrigido
  do ESP-4.1: a física NÃO governa este arsenal (cinto como anel rígido
  exigiria a caveira em φ≈+50° na frente e φ≈220° nas costas — impossível;
  faixa contínua exigiria diagonais opostas frente×costas, que o próprio
  cânone viola); quem governa é o cânone. NV-1 RETIRADA (substituída por N7);
  POS-5.1 reclassificado S4 (Δ sola 0,054 = profundidade da postura; a
  `tras_dir` aprovada tem 0,039); CAP-5.1 confirmado S4. **LOTE 4: traseiras
  FECHADAS; frontal permanece aberta só na vaga direita.**
- **Correção de nomenclatura (vale sobre a nota do lote 4 parcial):** a
  `tresquartos_v2` É a diagonal frontal ESQUERDA do arsenal (lobo à direita de
  quem olha, lado esquerdo próximo) — a nota anterior a chamava de frontal
  direita, o que estava errado. A vaga aberta no par frontal é a diagonal
  frontal DIREITA, com especificação exata no §7 da reconciliação (câmera na
  frente-direita; ombreira proeminente à esquerda de quem olha; rosto em 3/4
  para a esquerda; pé viewer-esquerdo em perfil para a esquerda; kit PELA
  REGRA, sem espelhar; aceite N5 < 0,85 contra `tresquartos_v2` E contra a
  frente).
- **AUTOAUDITORIA do executor nesta rodada de aplicação (APR-02):** conferi
  com os meus olhos a refeita antes de instalar — lobo proeminente à
  esquerda, rosto em perfil para a esquerda, pé viewer-esquerdo em perfil
  para a esquerda, pé viewer-direito traseiro com sola visível e um pouco
  mais alto (S4 de profundidade, não flutuação), capa proeminente à esquerda
  abaixo da cintura, losango central, caveira grande à direita do losango,
  alça na diagonal superior-esquerda → inferior-direita, zero bolsinhas,
  zero machado, corpo inteiro, fundo cinza-claro liso, tom oliva. Nenhum
  defeito novo achado por mim; os restantes são os S4 já registrados
  (POS-5.1, CAP-5.1, saturação de um braço) e a vaga da frontal direita.
  Não autoaprovei nada: a instalação executa o veredito final da
  reconciliação, não um juízo meu.
- **Frontal direita — situação ao fechar esta rodada (NÃO é lote concluído,
  NÃO vai ao Mestre como entrega):** 7 tentativas geradas em duas rodadas
  anteriores (3 + 4), TODAS reprovadas na autoauditoria adversarial do
  executor, nenhuma submetida ao Crítico nem instalada — viés sistemático do
  gerador 7/7 (rosto à direita, lobo proeminente à direita, pé em perfil à
  direita, quando a vaga exige o oposto). Próxima rodada REF-01: NÃO repetir
  variação de fraseado sobre frente/T-pose (espaço varrido); decidir entre
  edição controlada, âncora nas traseiras, consulta de processo ao Crítico,
  ou decisão do Mestre — ver as autoauditorias
  `autoauditoria-orc-diag-frente-dir.md` e `autoauditoria-orc-diag-frente-dir-r2.md`.
  Depois da frontal direita: classificação das 5 bestas novas de 31/10.
- **Commit desta rodada (só documentos):** instalar os 3 relatórios em
  `docs/` + esta entrada + ESTADO_ATUAL + APRENDIZADO_E_FLUXO (L-43, N4–N8).
  A imagem instalada é gitignored e não entra no commit — como manda a regra
  da frente (arte do RPG nunca no git).

## Adocao das pesquisas - P0 CONCLUIDO e pacotes P1-P5 preparados (01/11/2026, noite)

Por ordem do Mestre (01/11 20:01, bloco ADOCAO DAS PESQUISAS no ESTADO), 10 agentes trabalharam em paralelo na producao local dos pacotes da fila P0-P5, a partir de docs/ESTUDO-RAIZ-D1-SOLUCOES.md e docs/ESTUDO-ROTAS-MODELAGEM-PINTURA.md (com as correcoes de docs/CRITICO-estudo-raiz-d1.md). Producao local na VM do Muse em ~/workspace/oficina-audit/adocao/, indice INDICE-ADOCAO.md. TODAS as 10 frentes ENTREGUES; cada pacote so vira tranche executavel com o seu Critico senior proprio.

P0 - DIAGNOSTICO COMPLETO (laudos entregues, medicoes proprias):
- D-H0 (d-h0-concordancia.md, 8.575 B, SHA-256 6F0F804A...): as 4 referencias concordam no tronco e no kit (regra do kit 4/4); a discordancia mora na postura das pernas e na capa (compromisso conhecido); enquadramento varia 5,7%. Rota A liberada sem regenerar referencias.
- H2 residual (h2-residual.md, 7.088 B, SHA-256 3AD5B900...): duplicacao REFUTADA por medicao completa (1 componente, 0 duplicadas, 0 degeneradas, watertight); autointersecao residual CONFIRMADA em escala pequena (37 pares, 71 faces = 0,14%, pernas/tronco/cintura); 2 faces internas persistentes. Conduta: nao tocar na ancora; mitigar na pintura; eliminar por construcao na retopologia.
- D-H4 (d-h4-instrumentos.md, 8.838 B, SHA-256 655CF1EB...): salto de cor por classe de aresta - interna 50,73; fronteira de vista 71,19; costura UV 106,00; fronteira PURA de vista 49,07, igual a interna (a borda dominante e a costura do atlas, nao a vista). Disputa de pintura: 114.370 texels (27,18% dos diretos), discordancia media 109,46, uniforme entre pares - a H4 mora DENTRO das zonas de sobreposicao, nao nas bordas entre faces.
- Territorios, base da P1 (p1-territorios.md, 13.385 B, SHA-256 96ACF143...): replica do bake validada exata (IoU das 4 vistas identico; -1 texel em 845.063); 53,0% das faces com autoridade de vista; 47,01% cegas; fronteira = 39,94% da area; preenchimento com barreiras custa media 3,24 (livre 3,18), teto 21, e cria 254 faces orfas que exigem politica explicita (proposta registrada: onda livre com proveniencia contada, nunca silenciosa). Mapa em adocao/p1/territorios_orc.npz - consumir por hash, nao recalcular por job.

P1: pacote de territorios PRONTO (acima). A execucao (pesos territoriais mirando os texels em disputa + preenchimento com barreiras + politica das orfas) e a PROXIMA tranche, com Critico senior proprio.
P2: DESENHO PRONTO (p2-waechter-desenho.md, 23.509 B, SHA-256 21F22C87...): rotulagem v0 deterministica + ICM (v1 MRF condicional), nivelamento global, Poisson em faixa sobre a malha; fatias P2.0-P2.4 atras de flags; aguarda a forma-ancora definitiva (C-11) e o seu Critico.
P3: painel PRONTO e TESTADO com o braco 0 = COR-08 (p3-painel.md, 11.522 B, SHA-256 372E3E88...): regua validada (IoU medido do render repete o pipeline com diferenca <= 0,003); cobertura direta 49,78%; proveniencia anel medio 3,18, max 21; placar de assinatura do braco 0 = 5/12 PARCIAL (validacao do instrumento, nao-cego). Achado de procedimento: os renders salvos do Critico da COR-08 sao clay (sem cor) - o SSIM oficial de cada braco exige o render flat do harness (renderizar_flat.py). Identidade do braco A CONFIRMADA (identidade-mv-turbo.md, 5.484 B, SHA-256 0B0DEA03...): mv-turbo = Hunyuan3D-2mv Turbo oficial, slots nomeados ja existem no codigo. Braco B PRONTO para executar (braco-b-pacote.md, 16.963 B, SHA-256 8ED4CF02...): o TripoSG NAO estava instalado nem baixado (correcao ao estudo de rotas); checklist de instalacao em 5 passos; VRAM ">8 GB" no limite dos 8.188 MB da 4060 - a primeira execucao e a medicao decisiva.
P4: sem artefato dedicado nesta leva (depende de P0/P3) - desenho no bloco ADOCAO do ESTADO.
P5: prontidao do T7 PRONTA (t7-prontidao.md, 15.496 B, SHA-256 40466FCB...): rotulo corrigido (pacote ComfyUI de comunidade, nao o framework oficial; numeros previos = alegacao a medir); checklist executavel de 8 fases com SHA-256 dos 7 pesos como portao; roda em paralelo sob a trava de GPU. Braco T3 (Paint 2.0 via fork 2GP) sem artefato novo nesta leva.

Proximo passo: executar a P1 a partir do pacote de territorios, com autoauditoria adversarial registrada antes de submeter e Critico senior proprio (mecanismo x qualidade visual separados, L-33); painel de metricas do Mestre em toda tranche de modelagem/pintura.

## 2026-11-01 — REF-01 rodada 3 da frontal direita do Orc + consulta de processo ao Crítico (NÃO é lote concluído, NÃO vai ao Mestre)

- **Anti-colisão:** árvore do PC conferida LIMPA antes de qualquer escrita
  (HEAD `6d93280`, `git status --porcelain` vazio). A aplicação do Adendo 3
  (lote 4) já estava feita na rodada 19:54; esta rodada trata SÓ da vaga da
  diagonal frontal DIREITA.
- **Decisão de rota (cumprindo a autoauditoria r2):** NÃO foi variação de
  fraseado — foi a hipótese (b) da r2, âncora nas TRASEIRAS. As 7 tentativas
  anteriores usaram frente/tresquartos/T-pose (família frontal, onde mora o
  viés); nesta rodada a fonte principal é a traseira aprovada
  `orc_diag_tras_esq_refeita.png` (SHA `ad57447a…c95c618e`, conferido igual
  ao da reconciliação e ao instalado no PC), sozinha (t1, t3) ou com a frente
  canônica como autoridade do kit (t2, t4). Teto da rodada: 4 imagens.
- **Tentativas (autoauditoria adversarial registrada em
  `autoauditoria-orc-diag-frente-dir-r3.md`, local do executor; nenhuma
  instalada no PC, nenhuma submetida como candidata):**

  | # | SHA-256 integral | IoU × tresquartos_v2 (25/35/45) | IoU × frente (25/35/45) | Julgamento |
  |---|---|---|---|---|
  | r3-t1 | `74ecb708…f9b418` | 0,780 / 0,773 / 0,767 ✓ | 0,646 / 0,622 / 0,598 ✓ | REPROVADA: passa N5, falha rosto (direita), pés (esq. frontal / dir. perfil direita) e lobo (proeminente à direita) |
  | r3-t2 | `42510537…f9fa2355285eca` | 0,756 / 0,749 / 0,743 ✓ | 0,699 / 0,673 / 0,647 ✓ | REPROVADA como candidata — MELHOR EM 11: passa rosto (3/4 esquerda), pés (esq. perfil esquerda, dir. frontal), kit §5 e N5 completo (6/6 vistas, 3/3 limiares, máx. 0,756); falha SÓ metade do item 1: lobo à direita mas grande e proeminente, 0% de oclusão, em vez de recuado atrás da linha do ombro |
  | r3-t3 | `80f5f1d09bf85279edf522004ff19abd50dddf4d24af8b988aa286b3365355e4` | 0,765 / 0,757 / 0,750 ✓ | 0,647 / 0,621 / 0,596 ✓ | REPROVADA: passa N5, falha rosto, pés e lobo como a t1 |
  | r3-t4 | `ec9a52ae…ac1a034caf23c8` | 0,856 / 0,848 / 0,840 ✗ instável | 0,672 / 0,646 / 0,619 ✓ | REPROVADA: falha rosto, pés, lobo e N5 instável (cruza 0,85 entre limiares) |

  r3-t2 contra as demais vistas aprovadas (25/35/45): costas_v2
  0,755/0,749/0,745 ✓; tras_dir 0,722/0,714/0,710 ✓; tras_esq_refeita
  0,731/0,724/0,720 ✓; tpose_v2 0,422/0,420/0,416 ✓. Método: script
  `iou_ref01.py` (máscara por distância ao fundo, bbox, grade 500×500
  NEAREST), guardado com a autoauditoria. Zooms de conferência da t2:
  lobo grande à frente da capa, focinho para a direita; pé esquerdo em
  perfil para a esquerda com sola visível; pé direito frontal.
- **Verificação nova N9 (APR-01, proposta do executor, ADOTADA pela
  consulta — ver abaixo):** N5 exige IoU < 0,85 no MÁXIMO dos três limiares
  (25/35/45), contra TODAS as vistas aprovadas. A r3-t4 é a prova do furo
  da regra antiga: passaria só no limiar 35 (0,848) sendo composição da
  família da diagonal esquerda.
- **Consulta de processo ao Crítico Visual sênior independente
  (docs/CONSULTA-ref01-frente-dir-r3.md, integral no repo; NÃO é veredito
  de candidatura, NÃO instala nada, NÃO reporta ao Mestre):** primeira
  tentativa da consulta perdida por reinício do daemon (sem resultado);
  reemitida integralmente e concluída com relatório gravado. O Crítico
  releu a reconciliação (§5/§7/§8, N6), as autoauditorias r2/r3, viu as
  imagens com os próprios olhos e re-mediu tudo com o mesmo script:
  - Q1 — leitura do executor sobre a t2 CONFIRMADA nos 4 subitens (rosto,
    pés, kit §5, N5 18/18 medições, máx. 0,756, diferença 0,000 em todas as
    células publicadas pelo executor); rivais t1/t3 também conferidas
    (N5 passa, rosto/pés falham).
  - Q2 — lobo da t2: FALHA do item 1 do §7, segunda metade, **S2**
    (impede a entrada como está, exige retrabalho; não é S1 porque é
    localizado e remediável, nem S3/S4 porque viola item explícito e o
    sinal de câmera que justifica a vista). Oclusão medida: 0% — nenhuma
    parte cortada pela linha do ombro/capa; nas referências de "recuado"
    (`costas_v2`, `tras_dir`) só focinho e uma orelha espiam. Item 5
    confirmado na t2 (tubo de osso no quadril esquerdo NÃO é bolsinha);
    ombreira esquerda passa; olhar do lobo para a direita (orc para a
    esquerda) registrado como S4 de coerência a re-checar, não como falha
    autônoma.
  - Q3 — edição controlada da t2: **SIM, com 6 condições exatas** (região
    só x > 0,65, y < 0,35; original preservado, editado com nome/hash
    novos; oclusão parcial REAL do lobo + fusão com tronco/capa + lobo
    preservado como lobo; re-verificação TOTAL do §7 por Crítico
    independente; N5/N9 no editado contra as 6 vistas; nenhum defeito
    novo na região; UMA única tentativa de edição, sem loop de remendo).
    Vetados: flip puro, só reduzir a cabeça sem oclusão, tocar rosto/pés/
    cinto para "compensar". O editado será NOVO candidato, julgado do
    zero — nada do que a t2 passou é herdado se a ferramenta re-renderizar
    a imagem inteira.
  - Q4 (condicional) — se a edição falhar: declarar a vaga intratável por
    geração/edição e pedir decisão do Mestre (a: aceitar a lacuna; b:
    edição manual externa sob as mesmas condições; c: exceção documentada
    — DESACONSELHADA pelo Crítico). Vetado: mais uma variação de prompt,
    usar t1/t4 como base, gerar sem lobo para "adicionar depois".
  - Q5 — N9: **ADOTADA** (redação: "máximo dos três limiares"), com teste
    N7 cumprido (par aprovado mais próximo do limiar, `tras_dir` ×
    `costas_v2`, 0,832–0,841 na faixa — nenhuma aprovada reprovada pela
    regra nova). N10 proposta (auditoria de região da edição) fica para o
    Crítico da rodada da edição decidir.
- **Achado incidental de higiene (consulta, §0; corrigido aqui):** no
  diretório local do executor, `orc_diag_tras_esq.png` tem o MESMO hash da
  refeita (`ad57447a…`) — sob esse nome já não se distingue a original
  reprovada. A original NÃO está perdida: sobrevive como bruto do gerador
  (`media-generation-orc-diag-tras-esq-0-dd1f2a94…png`, SHA
  `6D0B0B35…37A6CA26413`). Sem efeito nas conclusões (a autoridade vigente
  é a refeita, e foi contra ela que se mediu).
- **AUTOAUDITORIA do executor nesta rodada (APR-02):** conferi as 4 com os
  meus olhos (inteiras + zooms da t2) antes de qualquer submissão; a t2
  foi reprovada por mim como candidata apesar de ser a melhor em 11 —
  parcial não vai ao Crítico como candidata, pela regra das rodadas
  anteriores. Defeito achado por mim e NÃO corrigido aqui (de propósito,
  por ser decisão de processo): o lobo da t2 — levado à consulta em vez
  de "ajeitado" por conta própria. Nenhum defeito novo nas demais; a t4
  quase-duplicata foi pega pela N9, não pelo olho.
- **Próximo passo (ordem de processo, não lote concluído):** tentativa
  ÚNICA de edição controlada da t2 sob as 6 condições da consulta, com
  autoauditoria adversarial + Crítico Visual independente julgando o
  editado do zero (N10 a decidir por ele). Se a edição falhar, o pedido
  de decisão vai ao Mestre nos termos do §4 da consulta. Depois da
  frontal direita: classificação das 5 bestas novas de 31/10.
- **Commit desta rodada (só documentos):** esta entrada + ESTADO_ATUAL +
  APRENDIZADO_E_FLUXO (N9, N10 proposta, L-44) + relatório integral da
  consulta em `docs/CONSULTA-ref01-frente-dir-r3.md`. Nenhuma imagem
  instalada no PC nesta rodada (a t2 segue só local; a arte do RPG nunca
  entra no git).

### 2026-11-01 (noite) - REF-01 lote 4, frontal direita: DECISAO do Critico (CM-000009-I0003) sobre a rota da tentativa unica de edicao

Ordem do Mestre (01/11/2026 22:44): "Use o Comestre critico e escolha a melhor opcao para o app, registre tudo". A decisao e do Critico CM-000009-I0003 (instancia de Critica/Auditoria do CM-000009, vinculada ao Auditor CM-000003); o documento integral esta em decisao-critico-rota.md (pasta local ref01-frontal-direita do workspace do Muse).

DECISAO EM DUAS CAMADAS:

1. NO MERITO: a melhor rota para gastar uma tentativa ainda nao gasta e a A1 - inpainting local mascarado sobre a r3-t2 (FLUX Fill ou SDXL-inpaint via ComfyUI; mascara parcial preservando focinho, olho e orelha frontal do lobo como ancoras). Fundamento estrutural verificado pelo Critico: e o unico mecanismo em que "o resto nao muda" e propriedade do metodo (pixel identico fora da mascara), sustentando as condicoes 1 e 5 da consulta por construcao, e nao por obediencia probabilistica de gerador - o mesmo gerador que levou 11 tentativas para obedecer a um sinal de camera. Chance do estudo (50-65%) aceita como faixa, com a correcao de que ela vale para a execucao, nao para a entrega ponta-a-ponta (o setup no ambiente real nao estava precificado).

2. NO ESTADO REAL: a tentativa unica JA FOI GASTA. As 22:30 de 01/11/2026 - 14 minutos antes da ordem do Mestre - a frente REF-01 executou a edicao da r3-t2 pela rota A2 (ferramenta de imagem da casa, edicao por instrucao), sob a autorizacao generica da consulta de processo (ramo expresso para ferramenta sem edicao regional controlada). Arquivo produzido: media-generation-orc-diag-frente-dir-r3-t2-edit-0-bf78200e-2942-4ab5-b41f-a537b5479673.png, SHA-256 01fd9c27396790e2785473f55c884c7fdbb3741885fe019bcff2dab2482b20f9, sob julgamento do Critico Visual independente do ciclo REF-01 desde ~22:36. Pela condicao 6 da consulta e pela exclusividade A1 x A2 (as duas decididas ANTES de gastar), ESSA edicao e a tentativa unica. Ordenar a A1 agora criaria duas "tentativas unicas" concorrentes - defeito de processo.

CONDICOES VINCULANTES DA DECISAO (alem das 6 da consulta, reafirmadas):
- Se o Critico do ciclo aprovar o editado na bateria completa (paragrafo 7 integral + N9 com tabela + N10), a vaga fecha com ele; a A1 NAO e executada.
- Se reprovar em qualquer item S1/S2, a tentativa esta consumida: A1, A3 pelo executor, B2 e C ficam CONGELADAS para esta vaga; declara-se a vaga intratavavel por geracao/edicao e escala-se ao Mestre com as opcoes G: (a) aceitar a lacuna; (b) retoque manual humano so na regiao do lobo, sob as mesmas condicoes; (c) excecao documentada - com o parecer contrario do Critico registrado (o modelador le a imagem, nao a anotacao). A A1 so retorna como decisao expressa do Mestre nessa escalada, nunca por iniciativa de agente.
- N10 ADOTADA para este julgamento (a consulta a propos ao Critico da rodada da edicao): regiao tocada e proveniencia declaradas, antes/depois; como a A2 re-renderiza a imagem inteira, o editado e julgado como geracao nova integral - nada do que a r3-t2 passou e herdado.
- Quem julga a candidatura e o Critico Visual independente do ciclo REF-01, com remedicao propria. A leitura visual preliminar do Critico decisor (lobo fundido a pele, rosto/kit/pes aparentemente preservados) NAO e veredito e nao substitui essa remedicao.
- Painel de metricas do job de edicao obrigatorio no registro do desfecho (ferramenta, duracao, hashes de entrada/saida); tokens da plataforma nao sao expostos pela ferramenta - declarar "nao medido", nunca estimar.
- Escopo de qualquer aprovacao declarado (L-33): conformidade medida ao paragrafo 7 e ao processo; a palavra final de fidelidade artistica e do Mestre.

VERIFICACAO PROPRIA DO CRITICO DECISOR (fontes, nao relatorios): r3-t2 conferida a olho e por hash (SHA-256 425105374b3cd2c38019121049364fda0aa65162ab193ad048f9fa2355285eca) - passa rosto, pes, kit (paragrafo 5) e item 5; o defeito do lobo confirmado (cabeca inteira a frente da capa, oclusao 0%, onde o item 1 exige parcialidade) - classificacao S2 da consulta correta. Tratamento-alvo confirmado a olho em tras_dir (lobo quase todo atras da capa; so focinho e borda espiam). Probabilidades do estudo julgadas uma a uma na decisao integral: A1 50-65% aceita com correcoes; A2 25-40% era prior generico - a amostra realizada das 22:30 nao exibiu os dois modos de falha centrais previstos (rosto nao reverteu; o lobo nao foi apenas encolhido, foi fundido/ocluido pela pele, a olho), e o desfecho da A2 sera o medido no julgamento, nao o prior; B1, B2, C, D, E e F com faixas e rejeicoes aceitas e congeladas pela condicao 6.

ESTADO DA VAGA: frontal direita continua ABERTA ate o veredito do Critico do ciclo sobre o editado das 22:30.

### 2026-11-01 (noite) - REF-01 lote 4, frontal direita: DESFECHO - veredito do Critico Visual sobre a edicao unica da r3-t2: REPROVADO

Desfecho da decisao do Critico CM-000009-I0003 registrada neste repo (commit 5cd092d). O Critico Visual senior independente do ciclo REF-01 julgou a edicao unica da r3-t2 (executada as 22:30 de 01/11/2026 pela frente REF-01, rota A2, ferramenta de imagem da casa) e REPROVOU. O editado esta DESCARTADO: nao entra no arsenal e NAO foi instalado em testes\referencias. Relatorio integral do veredito: pendente-critico-ref01-frente-dir-editada.md (pasta local oficina-audit do workspace do Muse). Autoauditoria do executor: autoauditoria-orc-diag-frente-dir-r3-editada.md.

MOTIVO MEDIDO (defeito unico, S2): falha o subcriterio (ii) do paragrafo 3 da consulta de processo (CONSULTA-ref01-frente-dir-r3.md) - fusao da silhueta do lobo com tronco/capa, sem leitura de sujeito em primeiro plano. No editado, a cabeca do lobo continua em perfil completo e nitido contra o fundo a direita: cadeia facial completa (olho amarelo, focinho, nariz e mandibula) com contorno frontal livre, e a caixa da cabeca tem a mesma area da base pelo mesmo metodo de medicao (0,0240 nos dois arquivos) - a cabeca nao encolheu; so a parte de tras foi coberta. Os outros dois subcriterios PASSAM: (i) oclusao posterior real (contagem de orelhas 2 -> 1; nuca sob a pele da capa) e (iii) o lobo continua sendo o lobo. A consulta exige os tres subcriterios sem excecao; logo, o item 1b do paragrafo 7 falha. Severidade S2: defeito localizado no quadrante superior direito, sem corrupcao de identidade, sem elemento inventado ou omitido. Nenhum outro item do paragrafo 7 regrediu: 1a, 2, 3, 4 (kit pela REGRA do paragrafo 5) e 5 foram julgados do zero no editado e passam.

MEDICAO QUE PASSOU: N5/N9 PASSA - IoU maximo 0,762 em 18 medicoes (limiares 25/35/45 contra as 6 vistas aprovadas; maximo contra tresquartos_v2 e costas_v2 no limiar 25), abaixo de 0,85 em todos. Os numeros do executor foram remedidos pelo Critico com diferenca 0,000 em todas as celulas.

RE-RENDERIZACAO TOTAL CONFIRMADA (auditoria de regiao, N10): a comparacao pixel a pixel editado x t2 mostra, FORA da regiao declarada (x > 0,65, y < 0,35), diferenca media 10,0 e 8,34% dos pixels com diferenca > 30 (dentro da regiao: media 13,78 e 14,84%). A ferramenta re-renderizou a imagem inteira; o editado foi julgado como geracao nova integral, sem herdar nada da t2 - o tratamento que a N10, adotada na decisao, manda.

VERIFICACOES DESTA RODADA: N10 (auditoria de regiao) ADOTADA; N11 (oclusao em dois planos) ADOTADA como criterio permanente - e o candidato FALHA nela (plano (a) cobertura posterior passa; plano (b) continuidade de silhueta falha); N12 (teste do perfil completo - verificacao nova desta rodada, APR-01) APLICADA: o editado FALHA (cadeia facial completa = cabeca em primeiro plano, nao focinho espiando); as autoridades tras_dir e costas_v2 PASSAM na N12. Licoes novas registradas pelo Critico no relatorio do veredito: L-REC-01 ("cobrir a traseira nao recua a cabeca" - o teste de fusao se le no contorno frontal, focinho/mandibula), L-REC-02 (tamanho da cabeca se mede, nao se estima) e L-REC-03 (auditoria de regiao obrigatoria para editados).

HASHES: base r3-t2 (orc_diag_frente_dir_r3_t2.png), SHA-256 425105374b3cd2c38019121049364fda0aa65162ab193ad048f9fa2355285eca - INTACTA, nunca sobrescrita; segue guardada como base reprovada, NAO como referencia. Editado: media-generation-orc-diag-frente-dir-r3-t2-edit-0-bf78200e-2942-4ab5-b41f-a537b5479673.png, SHA-256 01fd9c27396790e2785473f55c884c7fdbb3741885fe019bcff2dab2482b20f9, 1328x1904 - descartado.

CONSEQUENCIA (condicoes vinculantes da decisao registrada): a tentativa unica esta CONSUMIDA. Ficam CONGELADAS para esta vaga as rotas A1, A3 (pelo executor), B2 e C. A vaga da diagonal frontal direita fica declarada INTRATAVEL por geracao/edicao direta (11 tentativas de geracao + 1 edicao esgotadas). Escala-se ao Mestre com as opcoes G: (a) aceitar a lacuna; (b) retoque manual humano so na regiao do lobo, sob as mesmas condicoes do paragrafo 3 da consulta; (c) excecao documentada - com o parecer contrario do Critico registrado (o modelador le a imagem, nao a anotacao). A pergunta ja foi apresentada ao Mestre no chat e aguarda a escolha dele; este registro NAO pressupoe a escolha. A A1 so retorna como decisao expressa do Mestre nessa escalada, nunca por iniciativa de agente. Enquanto nao ha decisao, o arsenal do Orc segue com as 6 vistas aprovadas.

PAINEL DE METRICAS DO JOB DE EDICAO (exigido pela decisao): ferramenta = media.generate_image (ferramenta de imagem da casa, edicao por instrucao); executor = frente REF-01, rodada de 01/11/2026, edicao executada ~22:30 (rota A2); entrada = r3-t2 (SHA-256 425105374b3cd2c38019121049364fda0aa65162ab193ad048f9fa2355285eca), com orc_costas_v2.png apenas como referencia de "lobo recuado"; regiao declarada = quadrante superior direito (x > 0,65, y < 0,35); saida = arquivo editado (SHA-256 integral no paragrafo de hashes acima), 1328x1904; duracao do job: nao medido (a ferramenta nao o expoe); tokens: nao medido (a ferramenta nao os expoe) - nunca estimar; capacidade do computador (VRAM/RAM/CPU): nao medido (o job roda na plataforma da ferramenta, nao no PC do projeto).

NOTA DE REGISTRO TARDIO: este desfecho so e registrado agora porque (1) a rodada do ciclo REF-01 encontrou a arvore do repo SUJA (HEAD bfb200f; docs/APRENDIZADO_E_FLUXO.md modificado e docs/CONSULTA-ref01-frente-dir-r3.md nao rastreado, conferido 3 vezes entre 22:27 e 22:40, com outra frente no meio de tranche) e, por anti-colisao, nada escreveu no repo naquela rodada; e (2) em seguida o PC ficou inacessivel (desligado/inacessivel desde ~22:51 de 01/11/2026). Pacote preparado por CM-000009-I0007 (Registro/Continuidade, instancia do CM-000009 vinculada ao Historiador CM-000007), pronto para aplicacao em uma operacao quando o PC voltar: merge sobre o HEAD vigente, com verificacao de marcadores, sem sobrescrever arquivo inteiro.

### 2026-11-02 - REF-01 lote 4, frontal direita: DESFECHO DECIDIDO por delegacao - retoque manual humano na regiao do lobo (opcao 2)

DELEGACAO: em 2026-11-02 01:01 (-03), o Mestre delegou expressamente esta escolha ao Comestre Critico: "Deixo o Comestre critico decidir isso" - entre as tres opcoes da escalada do paragrafo 4 da consulta de processo (CONSULTA-ref01-frente-dir-r3.md): (1) aceitar a lacuna; (2) retoque manual por artista humano so na regiao do lobo, sob as condicoes do paragrafo 3 da consulta; (3) excecao documentada sobre a base r3-t2. A decisao e do Critico CM-000009-I0003 (instancia de Critica/Auditoria do CM-000009, vinculada ao Auditor CM-000003). O ato de contratar o artista continua sendo do Mestre; esta decisao fixa a rota e as condicoes tecnicas, nao presume gasto nem contratacao.

DECISAO: OPCAO (2) - RETOQUE MANUAL POR ARTISTA HUMANO, so na regiao do lobo, sobre copia da base r3-t2 intacta (SHA-256 425105374b3cd2c38019121049364fda0aa65162ab193ad048f9fa2355285eca), sob as condicoes C-D1 a C-D9 abaixo. A vaga NAO fecha por lacuna declarada nem por excecao: fica aberta com destino decidido, aguardando o retoque; ate la - e se o Mestre declarar que nao o fara - vale o arsenal atual integro (6 vistas aprovadas + tresquartos_v2), sem nenhum arquivo reprovado instalado.

FUNDAMENTO (medido, nao opiniao): o defeito da vaga e um elemento so, numa regiao so (quadrante superior direito), sobre a melhor base ja medida - a t2 passa rosto, pes, kit, inventario e N5/N9; a edicao unica falhou o subcriterio (ii) do paragrafo 3 por medicao (cadeia facial completa em primeiro plano; caixa da cabeca com area identica a da base, 0,0240 nos dois arquivos; oclusao posterior real, mas sem fusao). A pintura humana sobre a copia da t2 e a unica rota restante que preserva byte a byte o que a base ja provou, e e a de maior chance individual segundo o estudo de rotas (I0002, rotas A3/G-b). A excecao (3) foi rejeitada porque instalaria um sinal de lado contraditorio medido (oclusao 0% onde o item 1 do paragrafo 7 exige recuo parcial; IoU maximo da t2 de 0,756 contra a tresquartos_v2) e porque anotacao nao protege quem modela - o modelador le a imagem, nao a anotacao (parecer ja registrado na consulta e no veredito do ciclo). A lacuna (1) foi rejeitada como declaracao porque nao ganha nada sobre o estado padrao da opcao (2): enquanto nao ha retoque aprovado, o arsenal E a configuracao da lacuna, integro; declara-la so fecharia para sempre a unica rota de conclusao com chance alta, condenando o quadrante frontal-direito do Orc (kit e lobo) a interpolacao permanente das vizinhas.

CONDICOES VINCULANTES DA DECISAO:
- C-D1 Base travada: trabalho sobre COPIA da t2; a base nunca e sobrescrita; o retocado recebe nome e SHA-256 proprios.
- C-D2 Regiao travada: so muda o quadrante superior direito (cabeca do lobo + pele da capa adjacente, aprox. x > 0,65, y < 0,35); diferenca ZERO fora da regiao, verificada por auditoria de regiao (N10); pixel alterado fora da regiao descarta o arquivo (nesta rota nao ha julgamento como geracao nova - geracao esta congelada).
- C-D3 Criterio do lobo: os tres subcriterios do paragrafo 3 da consulta, simultaneos e sem excecao - (i) oclusao posterior real; (ii) fusao da silhueta, sem cadeia facial completa legivel em primeiro plano (N12); (iii) continua sendo o mesmo lobo. N11 tem de passar nos dois planos. Autoridades de tratamento: orc_diag_tras_dir.png e orc_costas_v2.png.
- C-D4 Vetos: proibido espelhar; encolher a cabeca sem oclusao; apagar o lobo; tocar rosto, pes ou kit para compensar.
- C-D5 Material ao artista: copia da t2, tras_dir, costas_v2, frente (ancora de kit/tom) e os tres subcriterios por escrito. NAO se entrega o editado descartado (SHA-256 01fd9c27396790e2785473f55c884c7fdbb3741885fe019bcff2dab2482b20f9) como ponto de partida - ele e re-renderizacao integral, nao pintura sobre a base.
- C-D6 Proveniencia e painel: entrega registra ferramenta de pintura, declaracao do que foi pintado, arquivo de trabalho (camadas, se houver) arquivado, hashes de entrada e saida e painel de metricas do job (tempo/tokens "nao medido" onde nao expostos - nunca estimados).
- C-D7 Julgamento: o retocado e candidato NOVO, julgado do zero pelo Critico Visual independente do ciclo REF-01 (paragrafo 7 integral + tabela N5/N9 + N10 + N11 + N12), com autoauditoria adversarial previa de quem coordenar a encomenda (APR-02). Tentativa julgada UNICA, sem loop de remendo: falha em item S1/S2 descarta o arquivo, e qualquer passo seguinte (segunda tentativa humana, descongelar A1, declarar lacuna, excecao) exige decisao expressa NOVA do Mestre.
- C-D8 Estado e saida: ate retoque aprovado, nada muda no arsenal; a t2 segue guardada como base reprovada e o editado como descartado - nenhum dos dois e instalado em testes\referencias. Se o Mestre declarar que nao encomendara o retoque, a frente registra a opcao (1) como fechamento final da vaga, sem processo novo.
- C-D9 Escopo (L-33): esta decisao trata da rota de desfecho e suas condicoes; nao aprova imagem nenhuma, nao declara a vaga fechada e nao trata de fidelidade artistica final, que e do Mestre sobre o candidato julgado.

EFEITO NA FILA REF-01: a vaga sai de "aguardando decisao do Mestre" para "DECIDIDA - aguarda retoque humano sob C-D1 a C-D9 (default: arsenal atual)". A fila NAO espera pela vaga: os proximos sujeitos seguem em paralelo na ordem registrada (classificacao das 5 bestas de 31/10: Tartaruga-Mundo, Demonio de Lava, Dragao-Serpente do Raio, Besta do Vazio, Sombra da Tempestade). Congelamentos intactos: A1, A3 pelo executor, B2 e C seguem congeladas para esta vaga; nenhuma geracao ou edicao nova da frontal direita esta autorizada por esta decisao; a A1 so retorna por decisao expressa do Mestre - que ele NAO tomou (ele delegou a escolha entre (1)/(2)/(3), e a escolha foi (2)).

NOTA DE INTEGRIDADE: a copia local de decisao-critico-rota.md esta truncada no disco (termina no meio do paragrafo 2); as condicoes vinculantes daquela decisao foram recuperadas na integra deste pacote a partir de registro-decisao.txt (texto aplicado no repo, commit 5cd092d) e das notas de conferencia do I0007. Pendencia para a volta do PC: restaurar o texto integral de decisao-critico-rota.md a partir da copia do repo.

### 2026-11-02 - REF-01, rodada das 15:54: aplicacao dos pacotes pendentes do desfecho da frontal direita (so documentos)

Aplicados por merge (acrescimo, sem sobrescrita) os dois pacotes preparados quando o PC estava inacessivel: (1) registro-desfecho.txt (CM-000009-I0007) - veredito REPROVADO do Critico Visual do ciclo sobre a edicao unica da r3-t2; (2) registro-decisao-delegada.txt (CM-000009-I0003) - decisao delegada do Mestre (02/11 01:01): opcao (2), retoque manual humano so na regiao do lobo, sob C-D1 a C-D9. Arvore conferida LIMPA antes da escrita (HEAD 5cd092d, sem outra frente no meio de tranche); commit so de documentos + push, com a arvore conferida limpa depois.
Instalado o relatorio integral do veredito em docs/CRITICO-ref01-frente-dir-editada.md (fonte local: oficina-audit/pendente-critico-ref01-frente-dir-editada.md); a autoauditoria do executor segue arquivada no workspace local (oficina-audit/autoauditoria-orc-diag-frente-dir-r3-editada.md) e referenciada no veredito. Atualizados: DECISOES.md (linha REF-01-FRDIR), APRENDIZADO_E_FLUXO.md (tabela de escalada, N10/N11 ADOTADAS, N12 APLICADA, L-REC-01 a L-REC-03, checklist pre-Critico e fila) e ESTADO_ATUAL.md (cabecalho + adendos + nota na fila). O PNG editado (SHA-256 01fd9c27...b20f9) NAO foi instalado em testes\referencias (reprovado); a base r3-t2 segue guardada como base reprovada, nao como referencia.
Estado da vaga apos esta rodada: DECIDIDA - aguarda retoque humano (ato de contratar do Mestre); enquanto isso vale o arsenal atual (6 vistas aprovadas + tresquartos_v2). A fila REF-01 NAO espera: proximo sujeito = classificacao das 5 bestas novas de 31/10 (ordem: Tartaruga-Mundo, Demonio de Lava, Dragao-Serpente do Raio, Besta do Vazio, Sombra da Tempestade). Espelho no Drive: ver linha seguinte a este commit (se indisponivel, registrado como pendente).

- **Espelho no Drive (fechamento desta rodada):** REGISTRO, ESTADO_ATUAL, DECISOES, APRENDIZADO_E_FLUXO e CRITICO-ref01-frente-dir-editada.md copiados para `Oficina3D_v2\REGISTRO` (via G:) e conferidos por SHA-256 na volta: REGISTRO 57BEFA79798A, ESTADO_ATUAL A448E95D9FB6, DECISOES 9B20B9E58085, APRENDIZADO_E_FLUXO BF89A908C67F, CRITICO-ref01-frente-dir-editada 88A2167EEC01 (prefixos de 12 hex; todos iguais PC = Drive). O REGISTRO commitado difere do espelhado so por esta linha de espelho.

### 2026-11-02 - FRENTE D: ABERTURA da tranche (pre-condicoes 0.1 a 0.7 verificadas no acto)

ABERTURA executada por I0004 (CM-000009) sob despacho do Coordenador, apos a ordem do Mestre de 2026-11-02 19:08 ("Faca o que for necessario e registre, lembresse de nao incomodar meu cunhado"): execucao so na camada invisivel (SSH + jobs destacados em fundo, prioridade baixa), sem GUI. Rota UNICA da tranche: pacote Frente D v2 julgado (auditoria sem-PC, PRONTO COM RESSALVAS), na ordem integral: pre-condicoes -> C-GUARD01 -> PORTAO DURO da sonda de meio-tom no Blender -> C-COR01 -> C-COR02 -> composicao medida e julgada em branch de integracao -> main. A rota v1 da copia do Codex (cherry-pick 7511a68 -> 53e845c) e INSUMO NAO EXECUTAVEL (reclassificada no adendo de liberacao, correcao do bloqueador R-01).

DECLARACAO (passo 0.1, CC-09) - registada ANTES de qualquer integracao, com o texto do Anexo A do pacote de execucao:

> **DECLARAÇÃO — Substituição dos itens 4–5 da fila "Nova ordem noturna" da linha do Codex no PC (decisão do Coordenador, registrada em 2026-11-02, antes da integração da Frente D na main).**
> Os itens 4 ("compor C-COR01/C-COR02 sobre a base nova") e 5 ("PRONTO PARA INTEGRAR v2") da fila preservada no `REGISTRO-CODEX.md` (registrada em 01/11/2026, 22:43) ficam **SUBSTITUÍDOS** pela integração executada na árvore principal sob o pacote Frente D v2 julgado (ordem: C-GUARD01 → sonda de meio-tom → C-COR01 → C-COR02 → composição medida em branch de integração), com os patches **re-ancorados** na base publicada actual. A composição na cópia **não** deve ser executada: fazê-la produziria uma segunda composição divergente da mesma correcção, sobre base pré-COR-08. Os commits `7511a68` e `53e845c` (e os da Frente B, `4836e6f`) permanecem como **insumo de leitura** da integração — os seus números serão reconfirmados sobre a baseline pós-S2 `e4056741…` e o resultado registrado na main. Os itens 1 (Frente E), 2, 3 e 6 da fila **não** são objecto desta declaração, salvo o registo de que o merge da main nesta cópia **não** é pré-passo da integração na main. Nada nesta declaração apaga ou altera o registro da linha do Codex: a fila original permanece registrada como ficou na queda, com esta substituição anexada.

O par substituido e, exactamente, COMPOSICAO (item 4) + PRONTO v2 (item 5) - conforme a correcao C-01 do Critico de Processo sobre a CC-09. Comunicacao a linha do Codex: nota deixada na caixa de ajuda do PC (_muse_rc\ajuda, junto ao guardiao) em 2026-11-02, arquivo comunicacao-2026-11-02-frente-d-substituicao-itens-4-5.txt, alem desta entrada. Itens 2, 3 e 6 da fila dele NAO sao pre-passos desta integracao (CC-08/D-2): merge da branch dele na main esta PROIBIDO; cherry-pick esta PROIBIDO em qualquer ordem.

DESAMBIGUACAO DOS DOIS "v2" (vale neste REGISTRO e doravante): "pacote Frente D v2 julgado" = o pacote da auditoria sem-PC (pacote-frente-d-v2.md), a rota desta tranche. "PRONTO PARA INTEGRAR v2" / "Frente D v2" no REGISTRO-CODEX (linha do Codex) = o pacote de integracao preparado na copia dele - documento distinto, insumo de leitura. Neste REGISTRO, "v2" sem qualificacao le-se o julgado.

PROVA DE BASE (passo 0.2): HEAD = c27f91f6590d718e00de02a853e8d4fd011a43a3 (linhagem 5cd092d -> e31dc28 -> c27f91f). git diff 5cd092d..c27f91f --stat lista SO documentos (docs/APRENDIZADO_E_FLUXO.md, docs/CRITICO-ref01-frente-dir-editada.md, docs/DECISOES.md, docs/ESTADO_ATUAL.md, docs/REGISTRO.md). Diff commitado por ficheiro nomeado = VAZIO nos 8/8 ficheiros que a tranche toca ou le como ancora (blob git identico nas duas pontas): oficina3d/cor/projecao.py 26d63bc4a9, oficina3d/cor/vertice.py ca1ffcacce, oficina3d/cor/_blender_cor.py 1aa9e94cec, oficina3d/cor/_blender_vertice.py c441f731d0, oficina3d/cor/preenchimento.py c8c8d280c2, oficina3d/cor/passo.py e798f5630e, testes/test_cor.py 7b67de2ac7, testes/test_cor_vertice.py 241f1735e7.

ARVORE RE-DECLARADA (substitui a pre-condicao "arvore limpa", invalida desde 2026-11-02 16:37): a arvore de trabalho esta SUJA com exactamente os 9 ficheiros da Secao 0 do adendo de liberacao (meia-tranche P1 da execucao desgarrada 6641b22b, parada as ~16:40), RE-MEDIDOS nesta abertura e IDENTICOS ao inventario (tamanho e mtime): M oficina3d/cor/projecao.py 33320 B 16:37:08; M oficina3d/cor/preenchimento.py 13067 B 16:37:09; M oficina3d/cor/_blender_cor.py 35880 B 16:37:10; M oficina3d/cor/passo.py 13389 B 16:37:11; M oficina3d/cor/__init__.py 2452 B 16:37:12; ?? oficina3d/cor/mapa_territorios.py 6764 B 16:37:13; ?? testes/test_cor_territorios.py 6022 B 16:37:14; ?? testes/test_cor_preenchimento_barreira.py 9460 B 16:37:15; ?? testes/test_cor_pesos.py 3433 B 16:37:16. PRESERVADOS intactos: nada de checkout/stash/clean. Julga-los e o primeiro acto da tranche P1 (CC-17), nao desta abertura. A regua D-1 (passo 1) mede a base COMO ELA ESTA, com estes 9 presentes.

PONTO C-5 / SS0.5 FECHADO NA ABERTURA (passo 0.3, D-8/CC-13-i): busca executada - (i) o pacote v2 (correcao C-5 do Critico) ja registava: a afirmacao "o congelamento dos quatro arquivos esta CANCELADO desde a COR-08" NAO tem fonte localizada nos documentos do projeto (docs do repo, pacotes de adopcao P1/P2, pre-audit O2); (ii) nesta abertura, git grep "congel" nos docs da main devolveu so usos nao relacionados (rotas REF-01 congeladas, ancoras, locks re-congelados) - nenhum registo do congelamento dos quatro arquivos (projecao.py, _blender_cor.py, passo.py, test_cor.py) nem do seu cancelamento nas fontes da main; (iii) unica mencao localizada: REGISTRO-CODEX.md:223, registo da LINHA DO CODEX ("congelamento dos quatro arquivos oficialmente cancelado pelo Mestre") - registo da outra linha, grau [ele], nao e documento do projeto da main. ESTADO EXPRESSO: o congelamento dos quatro arquivos nao esta documentado nas fontes do projeto da main, nem o seu cancelamento; a autorizacao operante para esta tranche tocar nesses arquivos e o portao de multiplos Criticos de 2026-11-02 sobre o pacote julgado (condicoes CC-01 a CC-38 do adendo de liberacao). Ponto fechado ANTES de qualquer toque em projecao.py (o primeiro toque possivel e o passo 6, C-COR02).

TRAVA DE GPU (passo 0.4, CC-02): locks/gpu.lock PRESENTE, 0 bytes (sem dono registado no conteudo), criado 2026-10-31 19:55:04, modificado 2026-11-01 12:59:09 (pre-queda). Nenhum processo Blender/Godot activo a abertura. Esta abertura e CPU (suite): a trava NAO foi removida nem tocada; corridas de GPU da tranche registam o estado antes, nos termos da CC-02, e vale uma so tranche de GPU de cada vez entre as duas linhas.

PRESERVACAO PRE-QUEDA (passo 0.6, CC-05): copia Oficina3D-codex medida a abertura: HEAD 5e682ab, git status LIMPO (0 linhas; testes/codex/medir_paint.py presente e ignorado pelo git) - esta tranche nao escreve nela; os diffs do Codex entram por leitura dos commits dele. _muse_rc/adocao_apply: listagem conferida (17 ficheiros, todos de 2026-11-01), so-leitura mantida, nada modificado.

DISCO (passo 0.7, CC-01): C: livre na abertura = 28.034.301.952 B (26,11 GiB), muito acima do piso de aborto de 4 GiB. (A referencia da fase de validacao era 16,15 GB; o ganho vem da limpeza de disco concluida e verificada hoje, +11,14 GiB liquidos medidos.)

PASSO 1 (D-1) corre a seguir, nesta mesma abertura; a regua congelada da suite entra em entrada propria, logo a seguir a esta.

- Assinatura: Coordenador CM-000009 (decisao), via executor I0004, 2026-11-02.

### 2026-11-02 - FRENTE D, PASSO 1 (D-1/CC-07): REGUA DE PARTIDA CONGELADA - suite da base como ela esta

ARVORE CONGELADA (declaracao exacta): repo app, branch main, HEAD c27f91f6590d718e00de02a853e8d4fd011a43a3 + arvore de trabalho com os 9 ficheiros extraviados da Secao 0 do adendo (listados na entrada de abertura desta tranche, re-medidos identicos ao inventario) + docs/REGISTRO.md com as entradas desta abertura. E ESTA a base que a regua mede - nao uma arvore limpa imaginada.

AMBIENTE E COMANDO: interpretador do projeto C:\Users\txcga\RPG_Local\Oficina3D\.venv_app\Scripts\python.exe (Python 3.10.22 [MSC v.1944 64 bit (AMD64)]; fastapi 0.162.0 conferido no acto); comando python -m unittest discover -s testes -t . -v, cwd = app; job destacado invisivel (WMI), prioridade BelowNormal; 44 s de parede no lancador, 39,756 s internos da suite.

PLACAR CONGELADO: 376 executados = 371 ok + 3 FAIL + 2 skipped + 0 erros. Decomposicao: ficheiros da main (22 ficheiros) = 352 testes: 351 ok + 1 skipped, ZERO falhas e ZERO erros - a base publicada esta verde na integra. Ficheiros extraviados (3) = 24 testes: 20 ok + 3 FAIL + 1 skipped. As 3 falhas sao TODAS dos testes novos da meia-tranche P1 extraviada, contra a implementacao tambem extraviada: estado registado, merito reservado ao julgamento da tranche P1 (CC-17). Nada foi corrigido nesta abertura.

FALHAS NOMEADAS (nascem na regua; qualquer regressao posterior mede-se contra esta lista, nao contra "zero falhas" imaginado):
1. testes.test_cor_preenchimento_barreira.TestDifundirBarreira.test_u12_ponte_cega_nao_entrega_em_territorio_alheio - FAIL (assertFalse(alc[3]) -> np.True_ is not false).
2. testes.test_cor_preenchimento_barreira.TestDifundirBarreira.test_u14_fonte_cega_so_entrega_em_faces_cegas - FAIL (assertFalse(alc[1]) -> np.True_ is not false).
3. testes.test_cor_territorios.TestMapaTerritorios.test_u8_fator_disputa_no_interior_e_piso - FAIL (assertEqual(float(fator[1, 0]), 0.6) -> 0.6000000238418579 != 0.6: igualdade exacta sobre valor float32).

SKIPS NOMEADOS: testes.test_mcp.TestRegistroServidor.test_criar_servidor_registra_as_ferramentas ("pacote mcp nao instalado neste venv"); testes.test_cor_preenchimento_barreira.TestParidadeLaudoU20.test_u20_paridade_com_npz_do_ancora ("sem OFICINA3D_P1_PROVA (prova do job-ancora)").

CONTAGENS POR FICHEIRO (executados = ok/falhas/skips): test_arquivar 14 = 14/0/0; test_cli 11 = 11/0/0; test_config 15 = 15/0/0; test_cor 33 = 33/0/0; test_cor_alinhamento 10 = 10/0/0; test_cor_costura 7 = 7/0/0; test_cor_passo 14 = 14/0/0; test_cor_pesos [EXTRAVIADO] 3 = 3/0/0; test_cor_preenchimento 8 = 8/0/0; test_cor_preenchimento_barreira [EXTRAVIADO] 9 = 6/2/1; test_cor_territorios [EXTRAVIADO] 12 = 11/1/0; test_cor_vertice 28 = 28/0/0; test_diagnostico_dh0 9 = 9/0/0; test_entrada 13 = 13/0/0; test_job 36 = 36/0/0; test_mcp 7 = 6/0/1; test_motores 29 = 29/0/0; test_qualidades 14 = 14/0/0; test_refino 30 = 30/0/0; test_saude 15 = 15/0/0; test_travas 18 = 18/0/0; test_uv_xatlas 7 = 7/0/0; test_validar 18 = 18/0/0; test_web 7 = 7/0/0; test_worker 9 = 9/0/0.

LOG INTEGRAL DA REGUA: Oficina3D\_muse_rc\frente_d\suite_d1b.log (32.548 B, SHA-256 b76cb9c5fea81d723b2cf82df83193fbdb09be4a07c3570fbfe05051698f7647). A suite nao deixou rasto na arvore (git status pos-suite = os 9 extraviados + a documentacao desta abertura).

NOTA DE METODO (tentativa 1, registada para nao se repetir): a primeira corrida desta abertura usou o Python do sistema (3.12.10, sem as dependencias do projeto): correu 242 testes com 16 erros (12 de importacao de modulos - ex.: fastapi ausente - e 4 erros em test_cor_passo), todos artefacto do ambiente; NAO e regua. Log preservado em Oficina3D\_muse_rc\frente_d\suite_d1.log (38.989 B, SHA-256 f3ea3b2a90b29d9c57a5ce831b285ebae284e7f79869830f97a2b61219b4bb58). Na corrida valida, test_cor_passo passa 14/14.

DISCO (pontos de medicao, CC-01): abertura 28.034.301.952 B (26,11 GiB); antes da suite 27.745.812.480 B (25,84 GiB); depois da suite 27.565.080.576 B (25,67 GiB) - sempre muito acima do piso de aborto de 4 GiB.

PROPOSTA REGISTADA (NAO aplicada; qualquer emenda segue a disciplina do pacote e e julgada antes do passo 2): o achado PC-1 da analise julgada ao Codex do PC - a bateria de cor e cega a MISTURA de dois tons medios distintos (a mistura ingenua em sRGB de 0,25 + 0,75 da 0,5; a correcta em luz linear e 0,2867) e nenhum teste actual mistura dois tons medios - fica como candidata a emenda da bateria do C-GUARD01 no passo 2 (teste de mistura em linear com tons medios distintos, alem das sabotagens ja desenhadas no pacote).

ESTADO DA TRANCHE: abertura CONCLUIDA (pre-condicoes 0.1 a 0.7 + passo 1). O passo 2 (C-GUARD01) NAO foi executado nesta abertura - aguarda despacho seguinte, com esta regua como partida.

- I0004 (CM-000009), 2026-11-02.

### 2026-11-02 - FRENTE D, PASSO 2 (C-GUARD01): BATERIA DE GUARDAS, CONTRAPROVA D-4 VALIDA, FECHO FC-2 - E DEFEITO ESCALADO NA GUARDA PUBLICADA (compensacao entre primitivos aceite)

Executor I0004 (CM-000009), sob despacho do Muse principal e ordem do Mestre de 02/11 19:08 (fazer o necessario e registar, sem incomodar o cunhado: camada invisivel apenas - SSH e jobs destacados de prioridade baixa; nada de GUI). Pre-condicao da arvore re-verificada no acto: HEAD c27f91f + os 9 ficheiros extraviados + os 2 documentos da abertura, com snapshot byte+SHA-256 dos ficheiros lidos e tocados. Os 9 extraviados e o seu merito (P1/CC-17) ficaram INTOCADOS e os 3 FAIL da regua NAO foram resolvidos - permanecem para o julgamento da tranche P1. gpu.lock intocada (passo de CPU).

BATERIA ESCRITA (so testes; ZERO codigo de producao tocado): ficheiro NOVO testes/test_cor_guard.py (5.489 B, SHA-256 945b13c656442e844346d41874ca62678e1f6cdd3727394aa867f193c032d992), classe TestVerificarGlbVerticeGuard, 4 testes + 5 sub-testes - as sabotagens julgadas do pacote re-miradas ao verificador actual verificar_glb_vertice (oficina3d/cor/_blender_vertice.py:314): (0) controlo de 2 primitivos completos aceite (primitivos=2, primitivos_sem_cor=0, contagens 6/6); (i) 2.o primitivo sem COLOR_0 reprova; (ii) primitivo malformado reprova SEM excepcao (3 variantes: acessor fora da lista, acessor sem contagem, POSITION ausente); (iii) COLOR_0 com contagem diferente de POSITION reprova (maior e menor). Arnes: o script do Blender nao e importavel na suite CPU (importa bpy/mathutils e executa main() na importacao, linha 588) - a funcao e carregada por extraccao AST do fonte real (parse + compilar so o FunctionDef, com json/struct no namespace): corre o codigo exacto publicado sem executar o script. Corrida isolada no .venv_app (Python 3.10.22): 4/4 OK (log Oficina3D\_muse_rc\frente_d\bateria_guard_passo2.log, SHA-256 519b495ecbda081b1c55479d325f218c04467772e4f4cfbb680558ccd7de140d).

CONTRAPROVA D-4 - VALIDA, NAO CADUCADA. Verificador pre-D-T2-4 extraido do blob 0008e796d0ab285b49703784a49feb52a5efab1f (pai de 6aecfe9) para Oficina3D\_muse_rc\frente_d\_blender_vertice_pre_dt24.py (23.502 B, SHA-256 ee58dfa08a6a12dfa84f3b1fac0fced5841ef4fdc4e8adcd619bb83c631b5355; confirmado a leitura: so le meshes[0].primitives[0]). Corredor Oficina3D\_muse_rc\frente_d\contraprova_d4.py (SHA-256 ed5bf4748b0b1a71ce33dc80efabcc971bc5dfced3ed300bd4afbc24c382bde3); log contraprova_d4.log, SHA-256 33a588deb5f1ae97ecef51fd0f957a2b54c0049dae3da1e58bce412845edb083. Medido: controlo aceite nos dois verificadores; sabotagens (i) e (iii) ACEITES pelo pre-D-T2-4 (ok=True - ele nao ve o 2.o primitivo) e REPROVADAS pelo actual (ok=False) = as 2 falhas esperadas no codigo antigo; a variante (ii) e igualmente invisivel ao antigo (aceite la, reprovada ca). O D-T2-4 corrigiu presenca e malformacao em todos os primitivos.

DEFEITO ESCALADO (PARADA do pacote aplicada; NAO corrigido neste passo - decisao aguarda julgamento): a sonda da familia da compensacao - as guardas fortes das linhas do Codex (notebook e PC, byte-identicas entre si), re-ancoradas como sonda fora da arvore - mediu que o verificador ACTUAL ACEITA (ok=True) as tres formas de violacao da igualdade POR primitivo: compensacao directa (primitivo 1 com COLOR_0 2/posicao 3 e primitivo 2 com COLOR_0 4/posicao 3; agregado 6=6), troca de acessores COLOR_0 entre primitivos de tamanhos diferentes (agregado 8=8) e reordenacao com contagem deslocada entre primitivos (agregado 8=8). Causa unica, lida do codigo: a igualdade de contagens e imposta so sobre as SOMAS de todos os primitivos (ok = ... conta_cor == conta_pos ...), embora a docstring da funcao prometa a invariante por primitivo ("a mesma contagem de POSITION no mesmo primitivo"). Registo de ironia tecnica: o verificador pre-D-T2-4 reprovava as tres formas por acidente (comparava so o 1.o primitivo, onde a compensacao nasce desigual) - a agregacao introduzida pelo D-T2-4 fechou o defeito de presenca e abriu este. Prova preservada (corredor + log com SHAs acima); a bateria commitada NAO inclui testes vermelhos desta familia, para nao corromper a atribuicao de falhas da regua (a mesma logica do julgamento E-PC1-1 para os T-MIX). Casa candidata do endurecimento (a julgar): imposicao da igualdade por primitivo no verificador, na linha da extraccao validacao_vertice.py julgada nas linhas do Codex - micro-passo proprio com julgamento, fora deste passo. Ate la, o C-GUARD01 fecha COM esta ressalva expressa: a guarda publicada tem um buraco provado.

FECHO FC-2 (contra a regua D-1): suite completa corrida em job destacado invisivel, mesmo comando e ambiente da regua (log Oficina3D\_muse_rc\frente_d\suite_passo2.log, SHA-256 722c3fefdfeb8392e18bfad6db086621af797bb70048cc5cd683367d67b2108c): 380 executados = 375 ok + 3 FAIL + 2 skipped + 0 erros (33,2 s). Regua: 376 = 371 + 3 + 2. O delta e SO a bateria nova (+4, toda verde); os 3 FAIL sao exactamente os mesmos da regua, com os mesmos nomes e a mesma assercao (test_u12 e test_u14 de test_cor_preenchimento_barreira; test_u8 de test_cor_territorios, 0.6000000238418579 != 0.6); os 2 skipped sao os mesmos. Criterio de aceite do passo CUMPRIDO: so somaram testes, nenhuma falha nova. FC-3 (absorcao das guardas das linhas Codex): absorvidas como desenho e como sonda neste passo; a absorcao como codigo commitado depende do julgamento do defeito escalado - fica registado, sem absorcao silenciosa.

ADITAMENTO E-PC1-1 (julgado ENTRA COM CONDICOES pelo Critico dedicado da emenda PC-1; texto da Sec. 5 do julgamento, registado aqui como especificacao anexada ao passo 2 - NAO executado neste passo):

1. (a) Os testes T-MIX-1..3 sao especificacao obrigatoria da Frente D (gama na MISTURA), tao vinculativa como o resto do pacote. (b) Eles NAO entram na bateria executavel do passo 2 nem sao escritos nele; a sua execucao e o seu fecho sao do passo 4 (C-COR01), nos termos do item 2. (c) A sonda dura (passo 3) ja cobre a semantica do pixel em meio-tom; a mistura e o segundo furo gama, distinto, e nao substitui a sonda. (d) As etiquetas T-MIX-1..3 ficam reservadas desde ja; nenhum outro teste pode usa-las.

2. Bateria do passo 4 (sobre o C-COR01 commitado; constantes do contra-teste independente do Critico da emenda, tolerancia <= 1e-6 relativos): T-MIX-1 (bake; via API, Orc, 2 vistas, meio-tom): texel da costura/regiao de mistura de duas vistas com valores-fonte 0.25 e 0.75 mistura-se EM LINEAR: saida esperada sRGB(LIN) ~= 0.571874; a saida ingenua 0.500000 reprova o teste. T-MIX-2 (vertice; unitario CPU, sem Blender): mistura de dois texels-fonte 0.25/0.75 pesos 0.5/0.5 produz 0.286699 e NAO 0.500000. T-MIX-3 (vertice; pesos fora do meio): mistura 0.25/0.75 com pesos 0.25/0.75 produz 0.404610 e NAO 0.625000 (o ingenuo ponderado). Ambiente do T-MIX-2/3: se a implementacao deixar a funcao de mistura pura inacessivel a CPU, a bateria cai TODA para a API/Blender - nunca metade/metade. Sabotagens do passo 6 (fecho da emenda): S-PC1-1 (reverter SO a conversao no ramo da media -> T-MIX-1/2 caem); S-PC1-2 (conversao espuria no ramo da forma mascara -> a bateria pre-existente de forma/mascara cai); S-PC1-3 (mistura ingenua plantada -> T-MIX-2 cai com 0.500000). A entrada de REGISTRO do passo 4 tem de declarar expressamente que o seu teste de meio-tom (leitura de pixel, vista unica) NAO e cobertura de mistura - a cobertura de mistura e T-MIX-1..3 e fecha no passo 4 (T-MIX-1..3) e no passo 6 (sabotagens).

3. Constantes de referencia (recomputadas pelo Critico da emenda, fechadas): lin(0.25) = 0.050876; lin(0.75) = 0.522522; mistura linear 0.5/0.5 = 0.286699; codificacao sRGB de 0.286699 = 0.571874; mistura ponderada 0.25/0.75 = 0.404610; ingenuo ponderado = 0.625000; lin(0.5) = 0.214041.

4. Ficheiro da bateria de mistura: ficheiro NOVO testes/test_cor_mistura_linear.py. NUNCA escrever nos ficheiros da meia-tranche extraviada (test_cor_preenchimento_barreira.py, test_cor_territorios.py, test_cor_pesos.py): esses ficheiros tem dono de julgamento proprio (tranche P1/CC-17) e a bateria de mistura nao pode nascer refem dele.

CLAUSULA EXPRESSA (do julgamento): FC-2 NAO COBRE MISTURA. Nenhum fecho do passo 2 pode ser lido como cobertura gama da mistura; essa cobertura so existe quando T-MIX-1..3 passarem (passo 4) e as sabotagens S-PC1-1..3 forem reprovadas (passo 6).

DISCO (pontos de medicao, CC-01): antes do passo 27.730.796.544 B (25,83 GiB); antes da suite 27.737.456.640 B (25,84 GiB); depois da suite 27.735.678.976 B (25,84 GiB) - sempre muito acima do piso de aborto de 4 GiB.

ESTADO DA TRANCHE: passo 2 CONCLUIDO (bateria + contraprova D-4 + fecho FC-2), COM o defeito da compensacao ESCALADO para julgamento e o aditamento E-PC1-1 registado como especificacao. O passo 3 (portao da sonda meio-tom, D-3) NAO foi executado - aguarda despacho seguinte. Um rebote do portao para julgamento e desfecho legitimo (D-3); e a Frente D nao pode ser declarada com a guarda completa enquanto o defeito escalado nao for julgado e fechado.

- I0004 (CM-000009), 2026-11-02.

## FRENTE D - TRANCHE 2b (ENDURECIMENTO DO VERIFICADOR) - PARADA NO PORTAO CD-3 (2026-11-02, noite)

Executor I0004 (CM-000009), sob o julgamento julgamento-endurecimento-verificador.md (PRONTO COM CONDICOES CD-1 a CD-7) e o seu texto de despacho (SS7). Base: HEAD a5feab4 + 9 extraviados preservados; regua FC-2 = 380 executados (375 ok + 3 FAIL extraviados + 2 skipped). Camada invisivel; gpu.lock intocada; disco sempre >25,8 GiB livres. Relatorio integral da tranche: frente-d-tranche2b-2026-11-02.md (hidden_files do goal da Oficina).

SNAPSHOT (antes de tocar): _blender_vertice.py 25.315 B, SHA-256 b7b7dacb56bec1bb...; os 9 extraviados byte-identicos ao snapshot final do passo 2 (prefixos FB9D44C1, 1B785652, 5BC89FB4, CC4DD88A, 73D208FD, AFD75403, 4A8585A4, 8003D58F, 5F0867DB).

CD-1 - TABELA DE DIVERGENCIAS (actual a5feab4 x candidato validacao_vertice.py da fonte julgada, SHA 1c8871d6ea157487...), conferida clausula a clausula contra os fontes; decisao do julgamento: adoptam-se TODAS as clausulas do candidato, condicionadas ao CD-3:
1. Igualdade de contagens: actual so AGREGADA (somas) x candidato POR PRIMITIVO - O DEFEITO (compensacao passa no actual).
2. Regra de aceite: actual = tem and soma_cor == soma_pos and imagens == 0 and materiais >= 1 (global) x candidato = color_0 and materials_ok and not imagens, com violacao contada por primitivo.
3. Presenca COLOR_0/POSITION: actual via try (KeyError/IndexError/TypeError/AttributeError) x candidato via indices validados e atributos dict - desfecho equivalente, mecanismo diverso.
4. Validade de contagens: actual nenhuma (bool soma 1; negativo subtrai; 0 soma 0) x candidato type(count) is int e count > 0 - clausula D-b (fecha prim vazio 0/0).
5. Tipos de acessor: actual NAO verificados x candidato POSITION VEC3/5126; COLOR_0 VEC3/VEC4 5126 ou 5121/5123 normalizado (ubyte nao normalizada passa no actual e reprova no candidato).
6. Regra de material: actual nenhuma por primitivo (basta >= 1 material no documento; ausente ou 999 nunca dereferenciado) x candidato indice int valido + material dict, por primitivo - clausula D-a (fecha o segundo buraco: material=999 aceite).
7. Indices de acessor: actual sem validacao (-1 le o ultimo; True le o acessor 1) x candidato type int e 0 <= indice < len.
8. Mesh vazio/estrutura: actual ignora mesh sem primitives em silencio x candidato invalida mesh sem primitivos; raiz dict; colecoes listas.
9. Cabecalho GLB: actual so o magic x candidato magic + version == 2 + total == tamanho do ficheiro + bloco JSON size <= total-20 e %4 == 0.
10. Contrato de erro: actual LEVANTA (struct.error/ValueError fora do try por primitivo; ficheiro vazio levanta) x candidato NUNCA levanta (dict ok=False + chave erro) - clausula D-c, externamente equivalente no unico chamador.
11. Semantica de primitivos_sem_cor: actual conta so primitivos ilegiveis x candidato conta QUALQUER violacao por primitivo - ALARGAMENTO declarado (e a chave que os registos historicos citam).
12. Somas agregadas: actual soma contagens de todos os primitivos legiveis x candidato soma so primitivos com contagens validas; somas informativas nos dois, nunca regra de aceite.

CD-2 - CONTRAPROVA PRE-CORRECCAO (corrida no PC, .venv_app; logs em _muse_rc/frente_d/passo2b/ com SHA registados no relatorio): bateria TestDefesaColor0 (9 metodos) da fonte julgada, byte-identica (SHA D789132D9CB66022...), contra o verificador ACTUAL por extraccao AST: 2 ok + 6 metodos em FAIL + 1 metodo em ERRO (levanta) = desfecho exigido da SS3.2 do julgamento CUMPRIDO: falham compensacao, troca de acessores, metade deslocada da reordenacao (traceback na linha 72, a metade valida passou), malformado na variante material (e nas variantes tipo_cor/sem_normalizar, clausula 5), e arquivo-quebrado LEVANTA struct.error em _blender_vertice.py:338; passam os controlos nomeados (controle, metade valida da reordenacao, ubyte normalizada). Falhas adicionais previstas pela tabela CD-1 (a SS3.2 nao enumerava estes dois metodos): indices negativos/bool (subTestes -1 e True; clausula 7) e mesh vazio ignorado (clausula 8). Contra o CANDIDATO em rascunho: Ran 9 tests - OK (a bateria nasce verde sobre o modulo). Contra o PRE-D-T2-4 (informativo): 11 falhas + 7 erros - nenhum dos dois verificadores historicos satisfaz a bateria estrita; linhagem registada.

CD-3 - PORTAO DOS DOURADOS: **PARADA** (desfecho pre-decidido do julgamento: dourado reprovado = parar, preservar o diagnostico por clausula e voltar a julgamento; proibido relaxar clausulas na execucao).
Localizacao por SHA-256 (nunca por nome presumido): a varredura integral de BASE/jobs (149 GLBs, 782.431.500 B) NAO encontrou nenhum dos 3 - as saidas dos jobs provac foram ARQUIVADAS para o Drive em 2026-11-01 (arquivamento.json de cada job; a pasta saida ja nao existe no job local). Localizados: ORC em jobs_teste/prova_validar/20261101-173915-prova-validar-jogo/saida/modelo.glb, SHA-256 88c30236272510603c74eb99fc7c5ecd90133c8f01494b3f011d80e310e12514 (integral, exacto); BESTA em <Drive>/Oficina3D_v2/arquivo_jobs/20261101-003424-provac-besta-s7/saida/modelo.glb, SHA-256 ba8d6cd56395ff17f62da25e07fc84001a01f0845f0528242864c974cf6d8621; CAPRILEO em <Drive>/Oficina3D_v2/arquivo_jobs/20261101-004549-provac-caprileo-s7/saida/modelo.glb, SHA-256 1b92e3b83c0b2e19fac58ccb8260d6ef1335bce655c2a9f8bce655775db791f5 (prefixos registados conferem; integrais agora medidos).
Resultado (dicts completos em _muse_rc/frente_d/passo2b/dourados_resultado.json): os 3 reprovam no CANDIDATO (ok=False) - e reprovam IDENTICAMENTE no verificador ACTUAL (ok=False), divergencia separada registada como o julgamento mandava (esperava-se ok=True nos 3 no actual).
Diagnostico por clausula (parse independente do chunk JSON dos 3 ficheiros, identico nos tres): 1 primitivo com atributos {NORMAL, POSITION, TEXCOORD_0} - SEM COLOR_0; material AUSENTE no primitivo; 0 materiais e 0 imagens no documento. Clausulas que reprovam: presenca de COLOR_0 por primitivo (primitivos_sem_cor=1 nos dois verificadores) e regra de material (candidato: material por primitivo valido; actual: materiais >= 1 global, com materiais=0). Leitura: os ficheiros registados como dourados sao os modelos REFINADOS da etapa de forma/refino (o "modelo.glb (refinado)" do relatorio T5) - artefactos ANTERIORES a etapa de vertice, sem cor de vertice nem material. Nenhum verificador correcto da etapa de vertice os pode aceitar; o portao, com estas fixtures, e insatisfazivel por construcao - NAO por sobre-estricao do candidato (o actual, mais permissivo, reprova igual).
Medicao auxiliar para o re-julgamento (NAO substitui o portao): os dois verificadores sobre as 24 saidas reais modelo_cor.glb presentes no disco (jobs + jobs_teste) concordam em TODOS os ficheiros (0 divergencias): 8 ok nos dois - exactamente as saidas puras da etapa de vertice T2 (t2-orc, t2-orc-det, t2-besta, t2-caprileio, t2-orc-triposr, t2-orc-1vista, crit-t2-soforma, crit-t2-cancel) - e 16 reprovadas nos dois (linhagem texturizada com imagem embebida e variantes de integracao/projecao; reprovacao por desenho nos dois verificadores). Ou seja: sobre o corpus real presente, as clausulas estritas do candidato nao reprovam nenhuma exportacao que o verificador actual aceite.

ESTADO DA TRANCHE: PARADA no passo 4 do despacho (portao CD-3), ANTES de qualquer escrita na arvore: extraccao NAO executada, baterias NAO commitadas, _blender_vertice.py byte-intacto (SHA b7b7dacb...), zero producao tocada, nenhum commit desta tranche. A ressalva do FC-2 continua de pe (a guarda publicada tem o buraco provado da compensacao). FC-2b NAO correu. PERGUNTA PARA O RE-JULGAMENTO (decisao do juiz, nao do executor): o portao de nao-sobre-estricao deve ser re-desenhado sobre saidas reais da etapa de vertice (candidatas medidas: as 8 saidas T2 acima, que incluem as tres criaturas), mantendo os hashes registados como fixtures da bateria de FORMA/UV (o papel que de facto cumprem), ou o desenho muda de outra maneira? Os passos 5 a 10 do despacho ficam suspensos ate la. O passo 3 da Frente D (portao D-3) segue intacto, a aguardar despacho, atras desta tranche.

- I0004 (CM-000009), 2026-11-02.

## FRENTE D - TRANCHE 2b (RETOMA SOB O RE-JULGAMENTO DO PORTAO) - CD-3b, EXTRACCAO E FECHO FC-2b (2026-11-02, noite)

Executor I0004 (CM-000009), sob rejulgamento-portao-dourados.md (veredito RETOMA COM O PORTAO REDESENHADO, condicoes RJ-1 a RJ-7) e o aditamento de despacho da sua SS7; julgamento original julgamento-endurecimento-verificador.md (CD-1 a CD-7). Base: HEAD a5feab4 + appends da PARADA por commitar (absorvidos no commit unico desta tranche) + 9 extraviados preservados byte-identicos ao snapshot; regua FC-2 = 380 executados. Camada invisivel; gpu.lock intocada (0 B, mtime 2026-11-01 12:59:09); disco 25,79 GiB livres no fecho. Relatorio integral: frente-d-tranche2b-retoma-2026-11-02.md (hidden_files do goal da Oficina).

INVARIANTE DE RETOMA: os rascunhos guardados foram re-medidos por SHA-256 ANTES de qualquer corrida, nas duas copias (local julgada e rascunho no PC, identicas): modulo candidato 1c8871d6ea157487810757c6fa25649e22caa0bcddbf24b3b6eff7f40913c802; bateria d789132d9cb660229226d6c7a9516572b653196e58d20826abba95934fd7f77a. CD-1 (tabela de divergencias) e CD-2 (contraprova no desfecho exigido) estao cumpridos e registados na entrada da PARADA - nao se repetem.

PORTAO CD-3b (substitui o CD-3): corredor proprio sobre o corpus ENUMERADO de modelo_cor.glb - disco (jobs + jobs_teste) = 24 ficheiros; arquivo de jobs no Drive montado = 0 ficheiros (a enumeracao RJ-7 nao encontrou saidas da etapa de vertice no arquivo; a concordancia cobre os 24). Corpus identico ao da medicao da PARADA, provado ficheiro a ficheiro: os 16 ficheiros listados no diagnostico da PARADA estao todos no corpus e com dicts de veredicto identicos nos dois verificadores; a contagem da PARADA (24, cand_ok 8, actual_ok 8) reproduz-se ao digito.
(a) Conjunto positivo por ENUMERACAO = {ficheiros do disco que o verificador ACTUAL aceita} = exactamente as 8 saidas puras da etapa de vertice T2 medidas na PARADA. Desfecho: CANDIDATO 8/8 ok=True; ACTUAL 8/8 ok=True (controlo). Tabela de fixtures (RJ-1) - a identidade de cada fixture e o seu SHA-256; estrutura comum (parse registado por fixture): 1 mesh, 1 primitivo com atributos {COLOR_0, NORMAL, POSITION, TEXCOORD_0}, material=0 valido (1 material no documento), POSITION e COLOR_0 VEC3/5126 com contagens iguais por primitivo, 0 imagens, 5 acessores:
1. jobs/20261101-124814-t2-orc/cor/modelo_cor.glb - SHA-256 949e3cf7009b8e23e63474fc395d45226acb2ec63342e2a419b3996b7c9c2f3a - 3.180.412 B - 65.469 vertices - producao (orc, uma das tres criaturas)
2. jobs/20261101-124814-t2-orc-det/cor/modelo_cor.glb - SHA-256 949e3cf7009b8e23e63474fc395d45226acb2ec63342e2a419b3996b7c9c2f3a - 3.180.412 B - 65.469 - producao; bytes identicos aos da fixture 1 (rerun deterministico: duas fixtures, um so hash)
3. jobs/20261101-124815-t2-besta/cor/modelo_cor.glb - SHA-256 39f81010c581721e0c398dfa871e432dddaed1fe03540c4e7a1303a1409b6d03 - 2.424.932 B - 48.299 - producao (besta)
4. jobs/20261101-124815-t2-caprileio/cor/modelo_cor.glb - SHA-256 3798f623fef2aa079857a1890c6a1b572d3e2a0fac9229b6a91fd4f508fa7c82 - 2.248.668 B - 44.293 - producao (caprileio)
5. jobs/20261101-124826-t2-orc-triposr/cor/modelo_cor.glb - SHA-256 0005907cb1f92519170d5fb04c17cb3199c1cb99a66a8a69124fb5e96d0c3522 - 2.488.120 B - 49.735 - producao
6. jobs/20261101-124827-t2-orc-1vista/cor/modelo_cor.glb - SHA-256 121240020a2bb1e520c321aae170415f46e0435f4caa603a1af4b9b0fb9faf73 - 2.026.864 B - 39.252 - producao
7. jobs/20261101-131410-crit-t2-soforma/cor/modelo_cor.glb - SHA-256 1f62f63821dfe73933eff83c8a0cc319820bcdba0de75cc49a73ef8c2370656a - 1.361.224 B - 27.516 - corrida de critico
8. jobs/20261101-131719-crit-t2-cancel/cor/modelo_cor.glb - SHA-256 6372ca058c7c4c342ad6cd081b6578a0f0fa3324671c72ba27be94f71aa217d2 - 2.488.120 B - 49.735 - corrida de critico
Mistura declarada (RJ-1): 6 de producao + 2 de corrida de critico; as saidas de producao das tres criaturas estao no conjunto (fixtures 1, 3 e 4). A lista FECHA nestas 8 linhas: um ficheiro futuro da etapa, mesmo aceite pelos dois verificadores, NAO entra no conjunto positivo sem aditamento julgado.
(b) Concordancia: candidato = actual, veredicto a veredicto, nos 24/24 ficheiros - 0 divergencias. Os 16 reprovados sao-no nos dois, por desenho (linhagem texturizada com imagem embebida e variantes de integracao/projecao). 0 divergencias = nenhum produto do corpus dependia do buraco da compensacao.

CONFERENCIA INDEPENDENTE (RJ-5): a tabela da Parte 1 do Codex do PC NAO tinha pousado a data do fecho - medido antes do commit: REGISTRO-CODEX.md na copia dele inalterado (58.520 B, mtime 2026-11-02 16:47:27), HEAD dele 5e682ab, arvore dele limpa. O fecho assentou na medicao independente substituta prevista no re-julgamento: parse proprio com corredor distinto (o metodo do diagnostico da PARADA) derivou o veredicto do invariante sem importar nenhum dos verificadores - 8 positivos, conjunto por SHA identico, 0 divergencias contra os dois verificadores em todo o corpus. A conferencia com a tabela do Codex fica PENDENTE DE REGISTO POSTERIOR (nao dispensada): quando ela pousar, confere-se contra a tabela RJ-1 desta entrada; divergencia em qualquer fixture reabre a pendencia do FC-2b.

EXTRACCAO E BATERIAS: criado oficina3d/cor/validacao_vertice.py com os bytes exactos da fonte julgada (4.170 B, SHA-256 1c8871d6ea157487...). Em oficina3d/cor/_blender_vertice.py saiu a definicao local e entrou o import pelo mecanismo existente (from oficina3d.cor.validacao_vertice import verificar_glb_vertice, junto aos imports P/V): diff de exactamente 2 hunks (+1 linha de import; -59 linhas da definicao); o chamador (verif = verificar_glb_vertice(...)) ficou byte-intacto; novo SHA-256 do ficheiro 4BE6AD1C4C04F6CA.... testes/test_cor_guardas.py committado SO com a classe TestDefesaColor0 (9 metodos nomeados); a classe TestDistanciasValidas fica FORA - mira avaliar_alinhamento_forma, outro alvo, declarado nao absorvido. testes/test_cor_guard.py re-mirado de extraccao AST para import do modulo (contagem inalterada: 4 testes), com UM ajuste declarado: a assercao de primitivos_sem_cor no teste de contagem divergente passa de 0 para 1 - e a clausula 11 da tabela CD-1 (no verificador extraido a divergencia de contagem por primitivo CONTA; no agregado antigo contava 0 e a reprovacao vinha so da soma), comentado no proprio teste. Corrida dirigida das duas baterias na arvore: 13 testes OK.
FUMO BLENDER (CD-4): Blender 5.2.3 LTS headless, etapa de vertice em modo sintetico, saida so para _muse_rc/frente_d/retoma/fumo/ (nunca sobre producao/dourados): exit 0; resultado ok=True com glb_verificacao.ok=true - dict do modulo extraido (2.143 vertices exportados da esfera de 1.986, primitivos_sem_cor=0, imagens_no_glb=0, materiais=1); checagem sintetica de cor 4/4 vistas ok. O import resolve no runtime real e o portao de entrega chama o modulo extraido.

FECHO FC-2b (CD-5): suite completa no PC (.venv_app, python -m unittest discover -s testes -t .): 389 executados = 384 ok + 3 FAIL + 2 skipped + 0 erros. Os 3 FAIL sao IDENTICOS em nome e assercao aos da regua FC-2 (conferidos bloco a bloco contra o log da suite do passo 2): test_u12_ponte_cega_nao_entrega_em_territorio_alheio (AssertionError: np.True_ is not false); test_u14_fonte_cega_so_entrega_em_faces_cegas (AssertionError: np.True_ is not false); test_u8_fator_disputa_no_interior_e_piso (AssertionError: 0.6000000238418579 != 0.6) - os testes da meia-tranche extraviada, cujo merito e da P1/CC-17: nem resolvidos nem escondidos. Delta contra a regua 380: +9 (a classe absorvida) e +0 pela re-miragem, como desenhado.
DESCARGA DA RESSALVA DO FC-2: a pendencia que a ressalva do FC-2 abriu (a guarda publicada tinha o buraco da compensacao provado) esta DESCAREGADA por este FC-2b, por esta nota que para ele aponta. A entrada do FC-2 NAO foi tocada - fechou com a sua ressalva, que e facto historico.

DECLARACAO DA GUARDA (redaccao autorizada pelo re-julgamento, SS4.3): "C-GUARD01 completo no invariante prometido: COLOR_0 presente e completo por primitivo (presenca, igualdade de contagem com POSITION, validade estrutural dos acessores e do material referenciado) em todos os primitivos de todos os meshes. A bateria de sabotagem e a contraprova estao registadas (FC-2 + FC-2b); a nao-sobre-estricao esta provada sobre o corpus enumerado registado no FC-2b (portao CD-3b: conjunto positivo por enumeracao + concordancia total com o verificador anterior)." Limites permanentes, que viajam com a declaracao: (i) a guarda e ESTRUTURAL, NAO SEMANTICA - uma troca de acessores entre primitivos de igual contagem e indetectavel por construcao; (ii) a mistura de tons (E-PC1-1) continua NAO coberta - o fecho dela e dos passos 4/6; (iii) o verificador irmao da etapa de textura (verificar_glb_texturizado, _blender_cor.py) NAO foi auditado por esta tranche; (iv) a prova de nao-sobre-estricao cobre o corpus enumerado e registado nesta entrada (disco + arquivo do Drive a data) - NAO e uma prova sobre exportacoes da etapa que ja nao existam em nenhum dos dois sitios.

ERRATA (RJ-3) - PAPEL DOS 3 HASHES "DOURADOS": os hashes 88c30236272510603c74eb99fc7c5ecd90133c8f01494b3f011d80e310e12514 (Orc), ba8d6cd56395ff17f62da25e07fc84001a01f0845f0528242864c974cf6d8621 (Besta) e 1b92e3b83c0b2e19fac58ccb8260d6ef1335bce655c2a9f8bce655775db791f5 (Caprileio) sao fixtures da BATERIA DOURADA DA ETAPA DE FORMA (Prova C: forma/refino/UV) - modelos refinados sem COLOR_0 nem material, anteriores a etapa de vertice. Onde o registo os citava como portao da etapa de vertice/cor (expectativa da SS3.3 do julgamento do endurecimento), leia-se esta errata: esse papel esta revogado; o portao da etapa de vertice e o CD-3b registado acima. As entradas historicas NAO foram reescritas - a correcao faz-se por esta errata, por append.

LICAO NOVA: a regra aprovada pelo re-julgamento (SS6) - fixture de portao pertence a etapa que o portao certifica; fixture entra em desenho de portao por parse estrutural registado, nunca por citacao - regista-se no APRENDIZADO_E_FLUXO como L-45. Nota de numeracao: o re-julgamento propos o rotulo "L-44", mas L-44 ja estava ocupado neste projecto (licao da ancora nas traseiras, REF-01, 02/11/2026); o texto da regra e integral, so o rotulo ajustou ao diario.

ESTADO: tranche 2b FECHADA (FC-2b). O passo 3 da Frente D (portao duro D-3, sonda de meio-tom) segue intacto e por despachar, atras desta tranche. Pendencia de registo posterior: a conferencia com a tabela do Codex do PC (ver CONFERENCIA acima).

- I0004 (CM-000009), 2026-11-02.

FRENTE D - PASSO 3: PORTAO DURO D-3 (SONDA DE MEIO-TOM NO BLENDER) - EXECUTADO E FECHADO 2026-11-02

PRE-CONDICOES MEDIDAS NO ACTO: HEAD main 53847808fb152a1bafb1627e88db69134e08b2dc (= fecho da tranche 2b, FC-2b); arvore com exactamente os 9 extraviados da meia-tranche P1 (5 M: cor/__init__.py, cor/_blender_cor.py, cor/passo.py, cor/preenchimento.py, cor/projecao.py; 4 ??: cor/mapa_territorios.py, testes/test_cor_pesos.py, testes/test_cor_preenchimento_barreira.py, testes/test_cor_territorios.py), preservados e intocados em todo o passo; gpu.lock presente, 0 B, mtime 2026-11-01T12:59:09 (pre-queda), sem dono - estado registado antes e depois, INALTERADO; nenhum processo Blender/Godot no arranque nem no fim; disco C: livre 27.577.442.304 B (25,68 GiB) na abertura e 27.561.971.712 B (25,66 GiB) no fecho (delta -15.470.592 B). Corrida leve (pacote SS0.5/CC-03): fundo, job WMI destacado, prioridade BelowNormal, camada invisivel; trabalho todo em _muse_rc/frente_d/passo3 (fora da arvore de producao); Blender 5.2.3 LTS.

PERGUNTA DO PORTAO (pacote SS3; adendo CC-11): na carga de um PNG sRGB pela etapa de vertice, img.pixels devolve valores CODIFICADOS ou JA LINEARIZADOS? A bateria sintetica publicada nao decide (canais so 0/1, onde as hipoteses coincidem - NP1/A2). Hipoteses calculadas em float64 (EOTF sRGB exacta) para os tres tons da sonda: byte 64 - entrada 0,2509803922; A (sem conversao) 0,2509803922; B (linearizado) 0,0512694584. Byte 128 - entrada 0,5019607843; A 0,5019607843; B 0,2158605001. Byte 191 - entrada 0,7490196078; A 0,7490196078; B 0,5209955732. (Referencia do pacote para o cinza 0,5 exacto: lin(0,5) = 0,214041.)

METODO - so codigo de producao no caminho de leitura e de pintura:
(1) PIXEL LIDO: script descartavel sonda_pixels.py (SHA-256 f8226be0dc7714dcd12aed4294b7b55a1320edb65b233d5c8022fe7d56722131) extrai a funcao ler_imagem BYTE A BYTE (AST; fonte de 23 linhas, SHA-256 f84416b419983855c5ea74bb61553c884316db6fb8319fec114bfc690b4a6332) do ficheiro de producao oficina3d/cor/_blender_vertice.py (SHA-256 4be6ad1c4c04f6ca54a46c80c332f967133627a40ec2da537a5a57e65172da2a - o ficheiro pos-extraccao da tranche 2b) e chama-a DUAS vezes por tom sobre PNGs uniformes 64x64; em paralelo, carga directa bpy.data.images.load + foreach_get, com o colorspace que o Blender atribui a imagem: "sRGB" (canais 4, alfa 1,0, alpha_mode STRAIGHT).
(2) COLOR_0 EXPORTADO: o proprio _blender_vertice.py de producao, invocado como a app o invoca (blender -b --factory-startup --python-exit-code 3 -P _blender_vertice.py -- pedido.json), modo glb, malha-esfera r=1 (fixture gerada por gen_esfera.py, SHA-256 df6ae4c6940d8351b67f388711e35f0b3b721b86f97b3048f70d24c9bf3f3545), UMA vista "frente" com PNG 1024x1024 do tom uniforme com moldura preta de 8 px (a mascara de fundo cobre o interior inteiro: cada vertice visivel e pintado SO por essa vista; amostrar_vertices copia imagem[ipy, ipx] sem nenhuma conversao). O tom 050 correu DUAS vezes (reprodutibilidade da cadeia inteira). Fixtures PNG por escritor proprio (zlib, RGB 8 bits, sem alfa): uniforme_025 SHA-256 09199f650e4e2a2208d7cf41a09fbf74f11941077d428e04cdfb3687e19b1feb; uniforme_050 161468955b147ebb1e4a5cde41bedb23fd6292d8d62fe6311880910715a1d82e; uniforme_075 682d13371a6e9592717cbd3dbdbe3dcdb48bef8cce03e03278f106be9172c825; moldura_025 4e88ad500405c8aa65a9db707a7c9a5acb65a29973a70ca1e6fbcaad4d70d890; moldura_050 723e932ab3d5f9ba77d8d5347ebf9d5c4e1adad63ab2a4395043ea4d7a4a69be; moldura_075 2e8f534442bc44df1ce32ee26b0ecd429cc5aec9faab81d92838e7d2bc52176f.

LEITURAS BRUTAS - pixel lido (uniforme em cada imagem: min = max = media, nos 3 canais):
- byte 64: 0,250980406999588 - leitura de producao 1, leitura de producao 2 e carga directa, identicas.
- byte 128: 0,501960813999176 - idem, identicas.
- byte 191: 0,7490196228027344 - idem, identicas.
Ou seja: o valor devolvido e byte/255 em float32 (desvio a hipotese A <= 3,0e-08, puro arredondamento float32). Distancias a hipotese B: 0,200 / 0,286 / 0,228. Reprodutibilidade total (3 tons x 2 leituras de producao + carga directa). Resultado integral: _muse_rc/frente_d/passo3/resultado_pixels.json (SHA-256 da596085c24ceba3755671ae21d8d974adae046ebc0a34ea51caf7fc2b097412).

CADEIA COMPLETA - COLOR_0 exportado (4 corridas de producao, todas ok=True e com glb_verificacao.ok=true da guarda extraida): a vista frente pintou 921 vertices directamente em cada corrida; a propagacao preencheu os restantes 1.222 com o mesmo valor uniforme; sem_cor = 0. O GLB exportado tem UM SO valor de COLOR_0 em todos os 2.143 vertices, igual ao pixel lido: 025 -> 0,250980406999588; 050 -> 0,501960813999176; 075 -> 0,7490196228027344 (calote frontal - normal exportada z > 0,99, n = 9 vertices pintados directamente pela vista: o mesmo valor). SHA-256 das saidas: saida_025 f9865388645f1907a0389af076c9cf3cb88dadf98739249b154e7daa10d08519; saida_050 abc81117f195aa48295959ed096585a121b483fd280ec9cc4f8748c5d3394145; saida_075 aa90e731b93c9e11b6f411b32597e861b7b5931004f18ea5ea68aba559b1df7a. A repeticao do 050 (saida_050rep.glb) saiu BYTE-IDENTICA a saida_050.glb (mesmo SHA-256) - a cadeia e determinista ponta a ponta.

DESFECHO DO PORTAO (na forma do pacote SS3): PIXEL LIDO = VALOR CODIFICADO sRGB (0,50196 no cinza "0,5"; SEM linearizacao na carga). A semantica que as docstrings do pacote do Codex afirmavam esta agora MEDIDA dentro do Blender 5.2.3, sobre o caminho de producao. Consequencia fixada para o passo 4: o C-COR01 ENTRA COMO DESENHADO (conversao por fonte na amostragem; a cor da forma NAO converte; conversao na carga continua proibida - converteria duas vezes apos o passo 4 e quebraria o T1, que e sRGB de ponta a ponta). Regista-se ainda a quantificacao do defeito que o passo 4 corrige: com entrada codificada 0,50196, o COLOR_0 exportado sai hoje 0,50196 em vez do linear 0,21586 - e o desenho desta sonda fica como medicao de aceite reutilizavel do passo 4 (esperado pos-C-COR01, com a mesma fixture: COLOR_0 ~= 0,21586). NENHUMA linha de C-COR01 foi escrita neste passo; os testes T-MIX do aditamento E-PC1-1 nao foram implementados nem tocados (sao dos passos 4/6).

DESVIOS DECLARADOS: (D-1) o lancador rodar_sonda.ps1 (SHA-256 b35683be0bca60eac2e8af3f01d4aa99b9b0f29c8039649dd8127eab0ef9384f) nao capturou os codigos de saida dos 6 processos Blender (status.txt e FIM.txt com os codigos vazios); a validade das corridas assenta nos artefactos - resultados JSON com ok=True, GLBs exportados e verificados pela guarda, logs - e nao nos codigos. (D-2) a malha importada pela producao tem 2.143 vertices contra 1.986 da fixture gerada (divisao de vertices nas costuras UV pela importacao glTF): facto medido, sem impacto no portao. (D-3) stderr das corridas de producao com DeprecationWarning pre-existente (Material.use_nodes, _blender_vertice.py:488) - nao e desta sonda.

PAINEL DE MEDICAO (regra 19:06): tempo interno de cada corrida de producao 0,28-0,29 s; janela total do job destacado 6 s (20:30:36 a 20:30:42); artefactos da sonda ~0,6 MB em _muse_rc/frente_d/passo3; VRAM/RAM/CPU de pico NAO MEDIDOS (headless, sem render) - declarados nao medidos, nao estimados. Tokens: nao medido (a sonda nao expoe contagem).

ESTADO: passo 3 FECHADO, com o desfecho registado. O passo 4 (C-COR01) aguarda despacho - entra como desenhado, sob o aditamento E-PC1-1 (testes T-MIX nos passos 4/6). Regua vigente inalterada: 389 (suite nao correu neste passo - medicao, zero toque em codigo). A copia do Codex nao foi tocada por este passo.

- I0004 (CM-000009), 2026-11-02.

FRENTE D - PASSO 4: C-COR01 (CONVERSAO sRGB->linear POR FONTE NA COR DE VERTICE) - EXECUTADO E FECHADO 2026-11-02

AMBITO E TERRENO: passo 4 do pacote de execucao da Frente D (seccao 4, D-5), sob o aditamento E-PC1-1 (julgamento da emenda PC-1). O terreno foi fixado pelo portao D-3 (passo 3, FECHADO): img.pixels devolve o valor CODIFICADO sRGB - o C-COR01 entra como desenhado. Pre-condicoes medidas no acto: HEAD f3dd68f6a5222ec5b21274a89c4db0145988b7d9 (main); arvore = exactamente os 9 ficheiros extraviados da meia-tranche P1 (merito P1/CC-17 intocado); snapshot do unico ficheiro de producao tocado: oficina3d/cor/vertice.py com 11.753 B, SHA-256 4b50fdfb49d3395f8a20b6bca2e2024d9cff0ae497cbf4cbcfcaae2fad6a7881; gpu.lock presente, 0 B, mtime 2026-11-01T12:59:09 (pre-queda, intocada - verificada antes e depois); nenhum processo Blender no arranque; disco C: livre na abertura 27.739.693.056 B. Camada invisivel: SSH + job destacado WMI (PID 33728), prioridade BelowNormal, Blender so headless; a copia do Codex e a vez dele no app nao foram tocadas.

O CODIGO (diff limitado ao desenho julgado - vertice.py + testes novos): (1) helper puro srgb_para_linear em oficina3d/cor/vertice.py (EOTF sRGB exacta: c/12.92 se c <= 0.04045, senao ((c+0.055)/1.055)**2.4; escalar ou array, float64); (2) conversao aplicada AS CORES DE VISTA em amostrar_vertices, NA AMOSTRAGEM: cores[sel] = srgb_para_linear(imagem[ipy[sel], ipx[sel]]); (3) docstrings do modulo e da funcao passam a declarar o contrato de espaco (a imagem entra codificada sRGB; as cores saem em luz linear). A cor da FORMA nao e convertida (entra por mesclar_forma, intocada; o COLOR_0 do GLB ja e linear por especificacao) e a propagacao nao muda de sitio: passa a mediar valores ja em linear. NENHUMA conversao na carga: ler_imagem intocado nos dois scripts - _blender_vertice.py e _blender_cor.py fora do diff (no fecho, o unico ficheiro de producao modificado e vertice.py). vertice.py depois: 13.107 B, SHA-256 ca67dd1ee2c21b4164252b162c928f28262d0a5c3956deba6f97617518431de7. ABSORCAO (CC-08: diff re-ancorado, sem transporte de commits): a formula do helper e a das duas implementacoes julgadas das linhas Codex (PC e notebook - identicas entre si e contra a especificacao); o PONTO de aplicacao e o do pacote julgado (na amostragem, no modulo puro), nao o das copias, que convertiam a imagem inteira no script do Blender - la, o diff sairia de vertice.py, desvio ao criterio de aceite deste passo.

BATERIA D-5 (escrita COM o codigo; testes/test_cor_conversao_fonte.py, SHA-256 b0413e23e2eac4045eae94787417e6d60dc366111af6c5dcd5795572137b7948): 3/3 ok na app real (.venv_app). D-5/1, meio-tom discriminante: vista sintetica com cinza 0,5 -> o vertice sai com 0,21404114048223255 (linear), nao 0,5; referencias do helper no mesmo teste (lin(0,25) = 0,05087608817155679; lin(0,5) = 0,21404114048223255; lin(0,75) = 0,5225215539683921; extremos 0 -> 0 e 1 -> 1; joelho 0,04045 -> c/12.92). D-5/2, forma nao convertida: mesclar_forma entrega a cor da forma BYTE A BYTE (igualdade exacta, incluindo um valor de forma 0,5 que fica 0,5), tambem ponta a ponta (sem vistas, amostragem + mescla deixam a forma intacta). D-5/3, propagacao em espaco unico: vizinho de vista (0,5 -> 0,21404114048223255) e vizinho de forma (0,3 cru) propagam para 0,25702057024111624 - a media calculada em linear.

ADITAMENTO E-PC1-1 - NOTA DO SS3 (registo expresso, como o aditamento manda): "o teste de meio-tom discriminante deste passo (0,5 -> 0,214) prova a conversao sobre um contribuinte; NAO e cobertura de mistura - a cobertura de mistura e E-PC1-1, no passo 6." E o registo da antecipacao: por despacho da integracao, o T-MIX-2 (caminho do vertice) foi ANTECIPADO e executado neste passo 4, no ficheiro julgado testes/test_cor_mistura_linear.py (SHA-256 25e7b0ad60952e6f48c73df6cd390f98c0d080b9c47a92f722e733856012c144), porque o comportamento que ele vigia nasce aqui (a mistura do caminho de vertice acontece na propagacao, sobre vizinhos ja convertidos); o T-MIX-1 (bake) e o T-MIX-3 (pesos) ficam para o passo 6, no mesmo ficheiro. T-MIX-2: dois contribuintes (frente 0,25; costas 0,75) pintam os vizinhos do vertice do polo e a propagacao media-os ja em linear -> 0,28669882106997435 (esperado do aditamento: 0,286699). 1/1 ok na app real.

SABOTAGENS DO ADITAMENTO (corridas uma a uma, em copias descartaveis em _muse_rc/frente_d/passo4/sab_*; nunca commitadas; valores obtidos medidos por sonda propria sobre os mesmos cenarios, porque os testes param na primeira assercao): S-PC1-1 (srgb_para_linear := identidade): o T-MIX-2 cai, com o ponto medio obtido 0,500000; D-5/1 e D-5/3 tambem caem (vista crua 0,5; propagado 0,4). S-PC1-2 (mistura em sRGB - sem conversao na amostragem): o T-MIX-2 cai, com 0,500000; D-5/1 e D-5/3 caem. S-PC1-3 (converter depois de misturar): o T-MIX-2 cai, com 0,21404114048223255 (= lin(0,5), o valor previsto no aditamento); D-5/1 e D-5/3 caem (propagado 0,13286832155381795 = lin(0,4)). REFORCO extra-aditamento: sabotagem da forma convertida em mesclar_forma -> o D-5/2 cai (a linha da forma sai convertida: [0,038263, 0,090842, 0,472833] contra o desejado [0,215861, 0,333333, 0,717172]) - os dentes contra o defeito simetrico (a PARADA do pacote SS4) ficam provados. Nenhuma sabotagem deixou de fazer falhar o teste que a vigia: neste criterio, o passo fecha.

MEDICAO DE ACEITE (o desenho da sonda do passo 3, reutilizado): mesma fixture (esfera + vista frente com o PNG moldura_050.png, SHA-256 723e932ab3d5f9ba77d8d5347ebf9d5c4e1adad63ab2a4395043ea4d7a4a69be), mesmo script de producao, modo glb, sobre o codigo novo. Resultado da producao: ok=True; 921 vertices pintados pela vista, 1.222 por propagacao, sem_cor = 0; a verificacao do GLB pela guarda publicada (validacao_vertice) devolve ok=true. COLOR_0 exportado, lido por parse independente do GLB: UM SO valor em todos os 2.143 vertices e na calote frontal (n = 9): 0,2158605307340622 por canal. Antes do C-COR01 (passo 3, mesma fixture): 0,501960813999176. Alvo float64: lin(128/255) = 0,21586050011389926; o desvio medido e 3,06e-8 - a quantizacao float32 do formato, digito a digito no representavel. SHA-256 do GLB pos-passo: 8905b49b491e6b9cba781657795e15b883013bcddf2ccfb390d5d8c3e74eb446 (o do passo 3 era abc81117f195aa48295959ed096585a121b483fd280ec9cc4f8748c5d3394145 - muda porque a cor mudou; a malha e a mesma: 3.968 triangulos, 2.143 vertices). O numero [ele] do rosto (28,38 -> 17,10) NAO se reconfirma aqui: a reconfirmacao e no passo 7, sobre bake real e baseline pos-S2.

PLACAR CONTRA A REGUA: suite completa (.venv_app, discover) = 393 executados = 388 ok + 3 FAIL + 2 skipped + 0 erros, contra a regua 389 (384 ok + 3 FAIL + 2 skipped + 0 erros). O delta e exactamente a bateria nova, nomeada: +3 (D-5/1, D-5/2, D-5/3) e +1 (T-MIX-2), todos verdes. Os 3 FAIL sao os mesmos da regua em nome E assercao (u12 e u14 de test_cor_preenchimento_barreira: "np.True_ is not false"; u8 de test_cor_territorios: "0.6000000238418579 != 0.6") - merito da meia-tranche extraviada, reservado a P1 (CC-17), intocado. No diff de conjuntos de testes executados (regua -> passo 4), nenhum teste da regua desapareceu. A bateria dos passos 2/2b (guardas do verificador) continua verde dentro da suite.

DESVIOS DECLARADOS: (D-1) o lancador nao capturou o codigo de saida do processo Blender do aceite (exit vazio no status.txt/FIM.txt - o mesmo quirk registado no passo 3); a validade assenta nos artefactos (resultado_prod_050.json com ok=True, GLB exportado e lido por parse independente, verificacao da guarda publicada). (D-2) a antecipacao do T-MIX-2, do passo 6 para o passo 4, por despacho - registada acima; o criterio de fecho do aditamento fica parcialmente antecipado (T-MIX-2 e as suas sabotagens) e o restante (T-MIX-1/3) continua devido no passo 6.

PAINEL DE MEDICAO (regra 19:06): job destacado total 40 s (20:43:22 a 20:44:02); suite 35,374 s; testes novos 0,065 s + 0,056 s; tempo interno da corrida de producao do aceite 0,3 s; disco C: 27.739.693.056 B na abertura -> 27.744.006.144 B no fecho; VRAM/RAM/CPU de pico nao medidos (headless, sem render) - declarados nao medidos, nao estimados. Tokens: nao medido.

ESTADO: passo 4 FECHADO. A etapa de vertice passa a entregar COLOR_0 em luz linear (a vista converte exactamente uma vez, na amostragem; a forma atravessa crua; a propagacao media em linear), com a guarda publicada a validar a saida. O passo 5 nao existe como passo proprio (pacote SS5); o passo 6 (C-COR02, com T-MIX-1/3) aguarda despacho. Ficam abertos, declarados: C-COR03 (residuo S2 do preenchimento, quantificacao pendente), A1 (clip de borda do bake T1 - intocado por este passo) e a reconfirmacao do numero do rosto no passo 7.

- I0004 (CM-000009), 2026-11-02.

FRENTE D - PASSO 6: C-COR02 (AMOSTRAGEM BILINEAR EM LUZ LINEAR, BAKE + VERTICE) E FECHO DO ADITAMENTO E-PC1-1 (T-MIX-1/3) - EXECUTADO E FECHADO 2026-11-02

AMBITO E TERRENO: passo 6 do pacote de execucao da Frente D (seccao 6, C-COR02; fecho FB-2 do adendo CC na parte de mecanismo) e fecho do aditamento E-PC1-1 (julgamento da emenda PC-1, seccao 5): executam-se e fecham-se neste passo o T-MIX-1 (bake) e o T-MIX-3 (pesos 0,25/0,75), com as 3 sabotagens de fecho correndo uma a uma. Pre-condicoes medidas no acto: HEAD 95a7012ef83163eef004de73c689f6b34335ed66 (main, fecho do passo 4); arvore = exactamente os 9 ficheiros extraviados da meia-tranche P1 (merito P1/CC-17 intocado); snapshots dos ficheiros de producao tocados: oficina3d/cor/vertice.py com 13.107 B, SHA-256 ca67dd1ee2c21b4164252b162c928f28262d0a5c3956deba6f97617518431de7; oficina3d/cor/projecao.py na versao da arvore (HEAD + extraviados) com 33.320 B, SHA-256 fb9d44c1264946c4bbd693e34b666a95681652704cf5ee38fa25c6848f09c6a9 (blob HEAD: 32.229 B, SHA-256 26d63bc4...); gpu.lock presente, 0 B, mtime 2026-11-01T12:59:09 (pre-queda, intocada - verificada antes e depois); disco C: livre na abertura 27.739.770.880 B. Camada invisivel: SSH + jobs destacados WMI, prioridade BelowNormal, sem Blender (passo sem GPU); a copia do Codex e a vez dele no app nao foram tocadas. CITACAO EXPRESSA (pacote SS0.5/CC-13(i), item fechado na abertura): o congelamento dos quatro arquivos (projecao.py, _blender_cor.py, passo.py, test_cor.py) NAO esta documentado nas fontes da main, nem o seu cancelamento; a autorizacao operante deste passo e o portao de multiplos Criticos de 2026-11-02 sobre o pacote julgado (condicoes CC-01 a CC-38).

O CODIGO (diff limitado ao desenho julgado): (1) oficina3d/cor/vertice.py (13.107 -> 15.552 B, SHA-256 57ba0a6491233f0c8dbd6d8146510b24dbd0f36d68fa840a8779a790fc60607c; CRLF preservado): helper amostrar_bilinear(imagem, mascara, x, y) - centros de pixel em i+0,5, pesos (1-dx)(1-dy) e simetricos, vizinhos convertidos com o srgb_para_linear do passo 4 DENTRO do helper (converter cada fonte, depois misturar), mascara a renormalizar os pesos, clip a borda herdado do helper julgado; amostrar_vertices ganha o parametro keyword-only amostragem="bilinear" ("seco" executa a linha pontual literal anterior; outro valor levanta ValueError). (2) oficina3d/cor/projecao.py (versao da arvore 33.320 -> 37.415 B, SHA-256 10987b2cb123711ebe857f44d2d4169f422b26ed515ee3c3b2a56552b538e03f; LF preservado): seccao propria com as mesmas tres funcoes - a EOTF fica DUPLICADA (vertice importa projecao; o inverso fecharia um ciclo) e a paridade das duas copias fica presa por teste - e rasterizar_textura ganha amostragem="bilinear" como ULTIMO parametro (depois de fator_face_vista), com o ramo bilinear a re-codificar para sRGB antes de escrever em tex (a textura continua declarada sRGB); em "seco", executa a linha pontual literal anterior. Os indices ipx/ipy/amostra_ok calculam-se EXACTAMENTE como antes nos dois modos: o clip de borda (achado A1) fica INTOCADO, por desenho e por proibicao expressa deste passo - C-COR02 NAO e correccao do A1, cuja tranche propria nao esta autorizada. _blender_cor.py e _blender_vertice.py fora do diff: os chamadores usam o default (bilinear). COMMIT de projecao.py por plumbing (hash-object + update-index --cacheinfo): o blob committado e HEAD + so os hunks deste passo, construido e verificado localmente (o diff entre a versao construida sobre HEAD e a versao da arvore e exactamente os blocos extraviados, nem uma linha mais); depois do commit, git diff HEAD -- projecao.py volta a mostrar so o diff extraviado (25 insercoes/4 remocoes), com a meia-tranche preservada na arvore, fora do commit. ABSORCAO (CC-08: diff re-ancorado, sem transporte de commits): a semantica (centros em i+0,5, pesos, renormalizacao pela mascara, clip a borda, controlo "seco") e a das duas implementacoes julgadas das linhas Codex (PC e notebook), que a sintese julgada considerou correctas contra a especificacao; o desenho segue o pacote - conversao na amostragem, nos modulos puros, NAO a conversao da imagem inteira a montante das copias.

BATERIA DO PASSO (11 testes novos, todos verdes na app real): testes/test_cor_bilinear.py (novo, 10.565 B, SHA-256 8996fa9fe4679cfc1ec7ad654a33c8dc0bbf70f2dc3ddf68ed12367cb6403f9e): gradiente conhecido 2x2 com amostra no centro nos DOIS caminhos (bake -> sRGB(0,5 em linear) = 0,7353569830524495 por canal; vertice -> 0,5 em linear, sem re-codificacao); controlo "seco" nos dois caminhos (no bake, o texel cai no pixel byte a byte; no vertice, o pixel exacto fora do centro e a degeneracao byte-exacta no centro do pixel; modo invalido levanta ValueError nos dois); regressao A0 com o bilinear ligado (a cena de faixas do COR-08 amostra as faixas certas: o centro continua subtraido); determinismo e independencia de ordem (duas vistas com facings 0,894/0,447: resultado byte-identico entre repeticoes e entre ordens, com texeis misturados presentes); paridade das duas EOTF e roundtrip da codificacao com extremos exactos. testes/test_cor_mistura_linear.py (estendido: 25e7b0ad... -> 7.459 B, SHA-256 33450d383370deae50c168e0316723930ebd98ba6a4431696fda3e78a8dff079; CRLF preservado): T-MIX-1 em dois metodos (pesos iguais: o texel sai (0,571874; 0,571874; 0,5); pesos 0,25/0,75: R = enc(0,404610) = 0,668632 e G = o valor de pesos trocados enc(0,168787) = 0,447702 - uma transposicao de pesos troca R por G e falha os dois canais) e T-MIX-3 no vertice (amostra a 1,25 sobre o par (0,25; 0,75) -> 0,40461018751918326). Valores medidos por sonda sobre o codigo sao: T-MIX-2 (vertice) 0,2866988210699744; T-MIX-3 0,40461018751918326; T-MIX-1, texel (1,1) = (0,5718735140718358; 0,5718735140718358; 0,5000000000000001) e texel (1,2) = (0,6686320581212072; 0,4477022872815489; 0,5000000000000001) - contra os esperados julgados 0,571874 / 0,404610 / 0,286699.

SABOTAGENS DO ADITAMENTO (corridas uma a uma, em copias descartaveis em _muse_rc/frente_d/passo6/sab1..3, por apendice de redefinicao - a ultima definicao vence; nunca commitadas; valores obtidos medidos por sonda propria sobre os mesmos cenarios, porque os testes param na primeira assercao): S-PC1-1 (conversao identidade nos dois modulos): caem T-MIX-1 (os 2 metodos), T-MIX-2 e T-MIX-3 (4/4) - sonda: vertice 0,500000 e 0,625; bake (0,735357; 0,735357; 0,735357) no texel de pesos iguais e (enc(0,625); enc(0,375); enc(0,5)) no de pesos. S-PC1-2 (mistura em sRGB - o bilinear mistura os valores codificados e devolve a media crua como linear): caem os mesmos 4/4, com a sonda identica a S-PC1-1 nos valores (nos dois caminhos, o resultado e a media crua). S-PC1-3 (converter depois de misturar): caem T-MIX-1 (os 2 metodos) e T-MIX-3 (3/4) - sonda: vertice no ponto medio 0,21404114048223255 (= lin(0,5), o valor previsto no aditamento), T-MIX-3 com 0,34851019523975124 (= lin(0,625)); bake (0,500000; 0,500000; 0,500000) e (0,625; 0,375; 0,5). A UNICA combinacao teste x sabotagem que nao falha e T-MIX-2 x S-PC1-3, por construcao: a mistura do T-MIX-2 vive na PROPAGACAO sobre amostras de centro de pixel, onde converter-depois e converter-antes coincidem; a corrupcao da costura nova fica provada e apanhada no mesmo caminho pelo T-MIX-3 (amostra entre pixeis) e medida directamente pela sonda (0,214041 no ponto medio). Nenhuma sabotagem deixou de fazer falhar a bateria: neste criterio, o passo fecha e o aditamento E-PC1-1 fica com os tres T-MIX executados e fechados (T-MIX-2 no passo 4; T-MIX-1/3 neste).

CONTROLO "SECO" BYTE-EXACTO (prova descartavel _muse_rc/frente_d/passo6/prova_seco.py, cenas aleatorias com seed 42, o codigo novo em modo "seco" contra o codigo anterior guardado em raiz_anterior): vertice - cores/fonte/melhor/info identicos byte a byte; bake - tex/pintado/melhor identicos byte a byte. Em modo bilinear, fonte/melhor/pintado ficam identicos e so os valores amostrados mudam (14 de 40 vertices; 215 texeis da cena): o bilinear muda valores, nunca decisoes.

FECHO FB-2 (adendo CC): o C-COR02 fica fechado neste passo na parte de MECANISMO (implementacao nos dois caminhos + bateria julgada + sabotagens + controlo seco byte-exacto). A re-medicao da curva DeltaE sobre a ancora pos-S2 e4056741 pertence ao passo 7.2 do pacote (composicao medida em branch de integracao) - NAO foi forcada neste passo, que nao chama GPU nem bake de producao; declara-lo aqui misturaria series. ROTACAO DE BASELINE (pacote SS6/CC-13(iii)) - DECLARADA: com o bilinear, a textura pos-S2 e4056741... deixa de ser a saida esperada do bake; a nova baseline nasce no passo 7, com as reguas D1 re-medidas e explicadas numero a numero. AVISO PC-5 (julgado), registado sem embelezar: o ganho causal do C-COR02 e pequeno (DeltaE Prata -0,007, Ouro -0,32 nas reguas do Codex) - isto e correccao de mecanismo, nao promessa de melhoria visivel.

PLACAR CONTRA A REGUA: suite completa (.venv_app, discover) = 404 executados = 399 ok + 3 FAIL + 2 skipped + 0 erros, contra a regua 393 (388 ok + 3 FAIL + 2 skipped + 0 erros). O delta e exactamente a bateria nova, nomeada: +8 (test_cor_bilinear) e +3 (T-MIX-1 x2 e T-MIX-3 em test_cor_mistura_linear), todos verdes. Os 3 FAIL sao os mesmos da regua em nome E assercao (u12 e u14 de test_cor_preenchimento_barreira: "np.True_ is not false"; u8 de test_cor_territorios: "0.6000000238418579 != 0.6") - merito da meia-tranche extraviada, reservado a P1 (CC-17), intocado. As baterias dos passos 2/2b/4 (guardas do verificador, D-5, T-MIX-2) continuam verdes dentro da suite. REGUA NOVA: 404.

DESVIOS DECLARADOS: (D-1) A codificacao canonica sRGB devolve 0,9999999999999999 para o linear 1,0 em float64 (1.055 - 0.055 nao e 1 em binario): a primeira corrida da bateria alvo falhou 5 testes antigos do bake, todos de cores solidas/faixas com igualdade exacta, com o caminho do vertice inteiro verde. Corrigido dentro do passo em linear_para_srgb: o ramo da potencia sai como p + 0.055*(p - 1), identico em reais a 1.055*p - 0.055 e exacto no extremo (o T-MIX-1 muda 1e-16, dentro da tolerancia julgada; nenhum artefacto julgado fixa a forma float da codificacao, porque as implementacoes de referencia nao re-codificam). Segunda corrida: 78/78. (D-2) A combinacao T-MIX-2 x S-PC1-3 nao falha, por construcao (ver SABOTAGENS): a sabotagem e apanhada no mesmo caminho pelo T-MIX-3 e medida pela sonda no valor julgado - declarado, nao varrido. (D-3) A primeira versao da cena do gradiente dos testes novos trazia a UV da segunda face do quadrado trocada (o vertice C com a UV de B): 2 testes do bake cairam com a amostra deslocada para a linha errada da imagem - erro da cena de teste, NAO do codigo de producao (o T-MIX-1, com imagem de 1 linha, passava e escondia-o); corrigida a cena: 89/89 na bateria alvo. (D-4) O lancador nao captura codigos de saida (quirk conhecido dos passos anteriores); a validade assenta nos logs SUMARIO e nos artefactos medidos.

PAINEL DE MEDICAO (regra 19:06): suite completa 30,455 s; baterias alvo 2,0-2,1 s por corrida; sabotagens ~0,1 s cada; sonda <1 s; prova do seco <5 s; disco C: 27.739.770.880 B na abertura -> 27.549.470.720 B no fecho (a diferenca sao as copias descartaveis e artefactos do passo em _muse_rc/frente_d/passo6); gpu.lock intocada (0 B, mtime 2026-11-01T12:59:09); VRAM/RAM/CPU de pico nao medidos (passo sem GPU, sem render) - declarados nao medidos, nao estimados. Tokens: nao medido.

ESTADO: passo 6 FECHADO. Os dois caminhos de cor (bake T1 e vertice) amostram em luz linear, com o controlo "seco" byte-exacto disponivel nos dois; o aditamento E-PC1-1 esta fechado (T-MIX-1/2/3 executados, sabotagens medidas uma a uma). O passo 7 (composicao medida em branch de integracao, com a curva DeltaE do FB-2 e a nova baseline) NAO foi avancado - aguarda despacho. Ficam abertos, declarados: C-COR03 (residuo S2 do preenchimento, quantificacao pendente), A1 (clip de borda do bake T1 - intocado por este passo; tranche propria nao autorizada) e a qualidade visual (olho do Mestre, L-33).

- I0004 (CM-000009), 2026-11-02.

FRENTE D - PASSO 7: COMPOSICAO MEDIDA EM BRANCH DE INTEGRACAO (D-7) - EXECUTADO 2026-11-02; JULGAMENTO (PASSO 8) PENDENTE

AMBITO E TERRENO: passo 7 do pacote de execucao da Frente D (seccao 7, composicao/D-7 do adendo CC-14): a composicao C-GUARD01 (verificador por primitivo, passo 2b) + C-COR01 (conversao sRGB->linear, passo 4) + C-COR02 (amostragem bilinear em luz linear, passo 6) prova-se integrada sobre a bateria dourada real, em branch de integracao, ANTES de qualquer integracao na main. Branch: integracao/frente-d, criada de 03fc6f8 (HEAD da main na abertura); worktree irmao app-integracao-fd, limpo (0 linhas) na criacao - os 9 ficheiros extraviados da meia-tranche P1 NAO entram na branch (merito P1/CC-17) e a arvore da main ficou intacta com as suas 9 linhas durante todo o passo. Pre-condicoes medidas no acto: PC ocioso ha 26.727 s; GPU 0 %/732 MiB; nenhum processo Blender/Godot; gpu.lock 0 B, mtime 2026-11-01T12:59:09 (verificada antes e depois de cada corrida, intocada); disco C: livre na abertura 27.549.814.784 B; copia do Codex na abertura: arvore limpa, HEAD 626229b (registado para confronto no fecho; esta tranche nao lhe toca). Camada invisivel: SSH + jobs destacados WMI, Blender headless. Artefactos do passo em _muse_rc/frente_d/passo7 (bakes, vertice, renders, fixtures, scripts, resultados). O ESTADO_ATUAL.md NAO e actualizado neste passo, por desenho (so depois do julgamento do passo 8).

FB-5 (suite completa na branch, contada do zero): 380 executados = 379 ok + 0 FAIL + 1 skipped + 0 erros (discover, .venv_app, 30,983 s). Delta contra a regua 404 da main atribuido ficheiro a ficheiro: os 3 ficheiros de teste extraviados (ausentes da branch limpa) somam exactamente 24 testes - test_cor_territorios.py 12 + test_cor_preenchimento_barreira.py 9 + test_cor_pesos.py 3 - e neles vivem os 3 FAIL da regua (u8, u12, u14) e 1 dos 2 skips (skipTest condicional a OFICINA3D_P1_PROVA, no ficheiro da barreira). A composicao nao parte nenhum teste: placar da branch = regua menos extraviados, sem outro delta.

FB-2 (curva DeltaE completa, D-6; fecha o C-COR02 na linha principal): instrumento proprio (medir_regua_b.py) = replica fiel da regua congelada da Entrega 2 da linha Codex (referencia alinhada; mascara fixa por erosao 3 iter.; ROIs absolutas rosto/peito/pernas; DeltaE CIEDE2000 + SSIM sobre a mascara), validado ao digito sobre os 3 flats guardados dele (flat_depois rosto 17,100705980028597; controle_bilinear 17,093654915697115; ouro_bilinear 14,249079238497838 - reproduzidos exactamente). A cadeia de render foi validada ao digito antes (o GLB controle_bilinear_1.0 dele, renderizado pelos ajudantes de producao da branch, mediu 17,093654915697115). Etapa de vertice de producao da branch sobre as vistas entrada_orc e os modelos de forma dos 3 niveis (vindos do arquivo Drive, SHA-256 conferidos um a um contra os registos: Prata 5467f25e..., Ouro 8738b9c7..., Lendario 7d53a89d...): os GLBs compostos de Prata e Ouro sairam BYTE-IDENTICOS aos da linha Codex (Prata SHA-256 44d6d066e136bcb0048f83a0f8a001048a1120a177a3a66496343630de56ad1e, 3.180.412 B; Ouro 0b6bfdbc43399580420921566f0d4e9148144a1b39aca0dab1e24caade0eac7a, 8.053.592 B; Lendario dca7dde9f589377cacfe590214870f01196325938176a1514072aa83eb5d4d29, 22.332.120 B) e a guarda publicada validou os 3 em producao (glb_verificacao.ok = true). CURVA MEDIDA vs serie [ele]: rosto DeltaE Prata 17,093654915697115 (SSIM 0,14569420034549613), Ouro 14,249079238497838 (SSIM 0,2698980121346872), Lendario 18,25964095325913 (SSIM 0,06324545291031718; fora_silhueta rosto 52, pernas 12) - reproducao DIGITO A DIGITO da curva completa, incluindo a forma nao monotonicca e os valores de peito/pernas (Prata 14,731745548857026/12,958736029607202; Ouro 11,931728105115406/10,688905298617138; Lendario 11,99924804099039/12,46758175450921). FB-2 FECHADO: o mecanismo composto produz exactamente os numeros julgados. (Regua de mecanismo; a qualidade visual continua NAO aprovada - L-33.)

DETERMINISMO E NOVA BASELINE: 3 bakes puros de producao do job ancora pos-S2 (pedido do s2cor08-1: GLB jobs/20261101-101528-corint-orc-s7/cor/modelo_uv.glb, vistas douradas, tamanho 2048, dilatacao 256, alinhamento otimizado, preenchimento 3d), tempos internos 111,43/111,17/112,38 s: textura SHA-256 IDENTICA nos 3 = f198a2a7d44d20a89f620a228187c142fc3b62af7f39bc7e2bd5804e3d2873b7; GLB SHA-256 identico nos 3 = 9dd670848def907f94a4716dfc9c978719c3cad7a32c36bff666243ff645decc. O bake instrumentado (ver FA-429) saiu com os MESMOS SHA - a instrumentacao mede producao, provado por byte. NOVA BASELINE DA FRENTE D, registada: textura f198a2a7d44d20a89f620a228187c142fc3b62af7f39bc7e2bd5804e3d2873b7 (a rotacao declarada no passo 6 cumpre-se: e4056741... deixa de ser a saida esperada do bake da ancora).

FA-429-4 (consistencia com as reguas publicadas): IoU bake do bake reproduzido = frente 0,8177, costas 0,7774, esquerda 0,8065, direita 0,7957 - divergencia 0,000 contra F5 (tolerancia 0,003); cobertura directa 420.713/845.063 texels, exacta - o bilinear nao mudou nenhuma decisao de amostragem (pintado identico ao pos-S2), como previsto no desenho. Consistencia interna da proveniencia: vencedores por vista 116.435 (frente) + 116.391 (costas) + 92.715 (esquerda) + 95.172 (direita) = 420.713 = total directo; os texels_por_vista do resultado (147.604/144.811/92.715/95.172) contam vitorias intermedias (achado N02 da linha Codex, confirmado aqui: esquerda/direita, as ultimas, coincidem; frente/costas acumulam re-vitorias).

FA-429-2 (proveniencia no bake real): instrumento = adaptacao do auditar_projecao_blender da linha Codex ao codigo da branch (ganchos re-ancorados nas linhas cx/cy do C-COR02; executa o main() de producao com rasterizar_textura instrumentada em memoria; ficheiros de producao nunca tocados). Vista frontal (imagem 1280x1820; caixa-alfa da figura y em [165..1658]): texels vencedores da frontal com pixel-fonte y em [165..1581] e x em [187..1133] - a proveniencia cobre a ALTURA TODA da figura, do topo da cabeca as pernas. Regioes-fonte frontais (fraccoes da caixa-alfa, definicao do instrumento dele): rosto n=5.048, peito n=12.830, PERNAS n=20.278 (> 0: as pernas TEM amostras directas da frontal no bake real). Faixa inferior geometrica (35 % da altura 3D, nao segmentacao semantica): 259.665 texels de superficie, dos quais 130.502 com amostra directa de alguma vista e 32.821 com amostra directa da FRONTAL; os 20.278 texels da regiao das pernas caem 100 % dentro da faixa. FA-429-2 FECHADO.

FA-429-3 (o teste decisivo do deslocamento): erro de coordenadas entre o caminho de amostragem e projetar(), medido no bake instrumentado sobre o codigo composto = 0,0 px nas 4 vistas. Contraprova em memoria (amostragem absoluta, o defeito pre-COR-08, sem tocar ficheiros): erro 698,55 a 715,30 px por vista, proveniencia frontal limitada a y em [165..869], regiao das pernas n=0, total directo 167.568. Decisao na forma julgada: deslocamento ~0 + pernas com amostras frontais > 0 = ABSORVIDO/CORRIGIDO, confirmado no bake real da composicao. FA-429-3 FECHADO.

ORC ANTES/DEPOIS NAS DUAS REGUAS (pacote SS7.3): mecanismo - os numeros acima (curva DeltaE do vertice reproduzida; IoU/cobertura do bake exactos; proveniencia corrigida). Visual - previas Workbench do bake da composicao em _muse_rc/frente_d/passo7/bake1/previas (frente/costas/esquerda/direita); o "antes" sao as previas do s2cor08-1. NENHUMA frase desta tranche aprova qualidade visual: ela segue NAO aprovada, a aguardar o olho do Mestre (L-33). D1 (IoU por vista >= 0,88) continua aberto: os IoU medidos sao os da baseline (0,8177/0,7774/0,8065/0,7957) - a Frente D nao prometia move-los.

DESVIOS DECLARADOS: (D-1) Os dois primeiros lancamentos do job de vertice pararam na validacao do render por causas do guião do executor, nunca do pipeline: pedidos JSON com BOM (Set-Content -Encoding UTF8 do PowerShell 5.1) rejeitados pelo json do Blender - corrigido com escrita UTF-8 sem BOM; e caminho errado do GLB de validacao (app\evidencias em vez de evidencias na raiz da copia dele). (D-2) A _blender_vertice da main executa main() no import (sem guarda __main__; a copia do Codex tem a guarda): o render de evidencia carrega importar_glb/apontar_camera por AST, sem a chamada final - mesma tecnica do instrumento T1. (D-3) Orientacao do mapa de superficie da faixa inferior: a proveniencia indexa linhas da textura (ty = (1-v)*T no espaco UV do Blender) e o TEXCOORD_0 do GLB ja traz o V invertido pelo exportador glTF; a orientacao alinhada e a das linhas v*T sobre o GLB (a do medir_cor08 dele), provada por coerencia geometrica (regiao das pernas 100 % dentro da faixa; taxa directa da faixa 50,3 % ~ taxa global 49,78 %). A orientacao invertida, como controlo, daria frontal na faixa = 4.844 e directos 23.303 - fica registada para conferencia do Critico do passo 8. (D-4) CPU de pico nao medido nas corridas (o contador TotalProcessorTime devolveu 0 no contexto destacado; declarado, nao estimado).

PAINEL DE MEDICAO (regra 19:06): bakes puros - duracao parede 112,64/112,74/114,66 s, RAM de pico 982.261.760 / 1.120.202.752 / 1.065.697.280 B, VRAM de pico 726-733 MiB (nivel do ambiente de trabalho; utilizacao GPU <= 7 %, previas Workbench), saidas por bake: GLB 5.964.448 B, textura 3.083.321 B, 4 previas ~0,62-0,65 MB; bake instrumentado 120,84 s / contraprova 118,88 s (RAM ~1,07 GB). Etapa de vertice: Prata 4,1 s parede (1,91 s internos), RAM 398.356.480 B, 49.750 triangulos; Ouro 6,17 s (5,04 s), RAM 518.205.440 B, 149.250 triangulos; Lendario 24,56 s (23,51 s), RAM 871.940.096 B, 497.500 triangulos. Suite da branch 30,983 s. Disco C: 27.549.814.784 B na abertura -> 27.274.584.064 B no fecho do job de bakes (artefactos do passo em _muse_rc). gpu.lock intocada (0 B, mtime 2026-11-01T12:59:09). CPU: nao medido (D-4). Tokens: nao medido.

ESTADO: passo 7 EXECUTADO - a composicao esta MEDIDA na branch integracao/frente-d, com FB-2, FB-5 e FA-429-2/3/4 fechados e a nova baseline registada. A main NAO recebeu nada neste passo. O passo 8 (julgamento da tranche, com bateria de Critico propria) NAO foi avancado - aguarda despacho. Ficam abertos, declarados: C-COR03 (residuo S2 do preenchimento; quantificacao pendente, tranche propria), A1 (clip de borda do bake T1; tranche propria nao autorizada), qualidade visual (olho do Mestre, L-33) e D1 (IoU >= 0,88 por vista).

- I0004 (CM-000009), 2026-11-02.

FRENTE D - PASSO 9 (BATERIA DE FECHO, pacote SS9.1 + condicoes C9-1 a C9-5 do julgamento do passo 8): EXECUTADO E FECHADO nos termos do veredicto do passo 8 - mecanismo PRONTO COM RESSALVAS (R-1 a R-3); qualidade visual NAO JULGADA (olho do Mestre; nao e portao deste passo).

INTEGRACAO (C9-1): merge documental da branch integracao/frente-d na main por fast-forward 03fc6f8..5279f60 (so docs/REGISTRO.md, +26 linhas - a entrada do passo 7); REGISTRO pos-merge 286.469 B, SHA-256 7CC61E9DA26412BFCA84D2BF58097CC99EF73778ADCCFB58EE22200EF1B280F0 - byte-identico ao registado na branch. ESTADO_ATUAL actualizado neste fecho (adendos dos passos 7, 8 e 9: veredicto do passo 8, descarga da conferencia FC-2b, nova baseline) e DECISOES com a linha datada FRENTE-D - tudo antes do commit final, como o pacote manda (REG-01).

SUITE FINAL (C9-2 / SS9.1.1): corrida pos-merge, contada do zero, na arvore da main (venv do projeto, unittest discover): Ran 404 tests in 30.497s - 404 = 399 ok + 3 FAIL + 2 skipped + 0 erros. Os 3 FAIL sao os extraviados de merito P1, nome e assercao identicos aos da regua (test_u12_ponte_cega_nao_entrega_em_territorio_alheio, test_u14_fonte_cega_so_entrega_em_faces_cegas, test_u8_fator_disputa_no_interior_e_piso). Zero falhas novas. Log espelhado no Drive (suite_final.log, MD5 df78e71467b28dc07aca0f967d14031e, provado pela listagem).

BAKES DA ANCORA (C9-3 / SS9.1.2): ancora pos-S2 correcta (pedido de jobs_teste/s2cor08-1/orc; entradas conferidas ANTES por SHA-256 integral - pedido-base EBA1093A4E13B230..., GLB de entrada 9A5C1203BB41DDF8... (2.879.252 B), vistas douradas frente 30C0F83D... / costas 256C8A2F... / esquerda 769E600D... / direita 4F4775E2...; parametros 2048/256/otimizado/3d). 2 bakes puros de producao sobre o codigo da main: bake1 (110,59 s de parede; 108,25 s internos; RAM de pico 1.014.124.544 B; VRAM de pico 729 MiB; utilizacao GPU 0%) e bake2 (110,75 s; RAM de pico 1.120.153.600 B; VRAM de pico 765 MiB; utilizacao 1%) - AMBOS byte-identicos a NOVA BASELINE: textura F198A2A7D44D20A89F620A228187C142FC3B62AF7F39BC7E2BD5804E3D2873B7 (3.083.321 B), GLB 9DD670848DEF907F94A4716DFC9C978719C3CAD7A32C36BFF666243FF645DECC (5.964.448 B; 49.750 triangulos; 71.289 vertices; Blender 5.2.3 LTS; ok=true com a guarda glb_verificacao presente). Bake instrumentado (116,65 s; RAM de pico 1.076.391.936 B) byte-identico ao bake1 - a instrumentacao mede producao: mapa texel->vista->pixel-fonte exportado (passo9/instr/proveniencia.npy, 50.331.776 B, SHA-256 B2BD951C1A28D1F10A660BBB7C1F0224D0851272A309242E5FD98DFFE34CC216) e erro de coordenadas amostragem x projetar() = 0,0 px nas 4 vistas. Medicoes do mapa: cobertura directa 420.713/845.063 texels, exacta; vencedores por vista frente 116.435 / costas 116.391 / esquerda 92.715 / direita 95.172 (soma 420.713); proveniencia frontal cobre a altura toda (pixel-fonte y 165..1581 sobre figura y 165..1658); faixa inferior geometrica (35%): 259.665 texels de superficie, 130.502 com amostra directa de alguma vista, 32.821 com amostra directa da frontal; regioes-fonte frontais rosto 5.048 / peito 12.830 / pernas 20.278 (100% dentro da faixa inferior). Textura x GLB conferidos: imagem embutida x textura.png externa, erro maximo absoluto 0 bytes (confere=true). IoU do bake (iou_bake_256): frente 0,8177 / costas 0,7774 / esquerda 0,8065 / direita 0,7957 - divergencia 0,000 contra a serie da baseline (registo, nao veredicto de D1). Render flat de fecho arquivado (Cycles CPU/Emission/Standard, 640x800, 21,01 s, exit 0) em _muse_rc/frente_d/passo9/renders/flat_fecho (frente 494.230 B SHA CD68ECA1...; costas 477.323 B A978AC25...; esquerda 449.571 B FF103B2E...; direita 448.756 B E507B696...) e espelhado no Drive - com o par antes/depois do passo 7, e a pasta do olho do Mestre. CPU das corridas: o contador devolveu 0 no contexto destacado - nao medido (fenomeno ja declarado no passo 7, D-4/R-3). Tokens: nao medido.

DETERMINISMO (SS9.1.3): os 2 bakes na main sao identicos entre si e a baseline, e somam-se aos 3 bakes identicos do passo 7 na branch; regista-se expressamente, na forma da SS9.1.3, que a prova da branch vale por identidade de blobs - pos-merge a branch e a propria main (HEAD 5279f60) e os SHA da baseline sao os citados.

REMEDICOES DE FECHO (SS9.1.4): FC-2 (passo 2) fechada; FC-2b (tranche 2b retoma) fechada, com a conferencia posterior DESCARREGADA (tabela independente do Codex do PC, branch codex/melhoria-paralela @ 626229b: as 8 fixtures conferidas por SHA integral, 7 identidades unicas, 0 divergencias contra o conjunto CD-3b - nota da linha principal conferencia-fc2b-codex-2026-11-02.md; o passo 7 listava esta pendencia como aberta por desactualizacao do guiao, o passo 8 corrigiu-a e este fecho regista o desfecho no ESTADO, C9-1); FB-2 e FB-5 (passo 7) fechadas; FA-429-2/3/4 (passo 7) fechadas e reconfirmadas nas medicoes deste fecho. Nenhuma remedição pendente.

ESPELHO NO DRIVE (C9-4 / SS9.1.5): provado PELA LISTAGEM do destino (pasta REGISTRO do Drive), nunca pelo log de upload - 9/9 ficheiros com tamanho e MD5 identicos aos locais: passo9-render-flat-frente.png (494.230 B, MD5 08d7f2f4b4aea153deeb50e2c11f3aae), passo9-render-flat-costas.png (477.323 B, 61ee632b58d8986f7ecf47af46e3613f), passo9-render-flat-esquerda.png (449.571 B, 94db6779e54c3c670e40b216e2a81d30), passo9-render-flat-direita.png (448.756 B, a51031403cd91f7772a9413c449ea21d), passo9-entradas.json (5b0ad7337d1e834fddd58356ac2fa22a), passo9-resumo-bakes.json (d50aa05868b93323afadb90ada123b9a), passo9-fa429-fecho.json (6808e72141ffa6a69fd400e738de976a), passo9-textura-glb-check.json (c79b4337651bf559001c5b14cb347fec), suite_final.log (df78e71467b28dc07aca0f967d14031e). Os tres documentos finais (REGISTRO/ESTADO/DECISOES) espelham-se dos bytes commitados neste fecho, com a mesma prova pela listagem registada no relatorio do passo 9.

PAINEL CONSOLIDADO DA TRANCHE (C9-5 / SS9.1.6) - duracoes e uso medidos por passo; "nao medido" onde nao houve medicao, nunca estimado; tokens nao medidos em toda a tranche:
- Abertura (0.1-0.7) + D-1: suite da base 44 s de parede (39,756 s internos); CPU; disco de abertura da frente 28.034.301.952 B livres.
- Passo 2 (C-GUARD01): bateria nova 4/4 OK; suite de fecho FC-2 = 380 executados; sem GPU; disco 27.730.796.544 -> 27.732.336.640 B.
- Tranche 2b (PARADA): medicoes CPU (contraprovas CD-1/CD-2 sobre copias); zero escrita na arvore; disco 27.728.646.144 -> 27.725.557.760 B.
- Tranche 2b retoma (FC-2b): suite completa 389 executados; fumo Blender sintetico exit 0 (saida.glb 119.340 B); disco -> 27.585.445.888 B.
- Passo 3 (sonda D-3): job total 6 s; corridas de producao 0,28-0,29 s cada (tempo interno); artefactos ~0,6 MB; VRAM/RAM/CPU de pico nao medidos (headless, sem render); disco 27.577.442.304 -> 27.561.971.712 B.
- Passo 4 (C-COR01): job destacado total 40 s; suite 35,374 s; testes novos 0,065 s + 0,056 s; producao do aceite 0,3 s (interno); VRAM/RAM/CPU de pico nao medidos (headless, sem render); disco 27.739.693.056 -> 27.744.006.144 B.
- Passo 6 (C-COR02): suite completa 30,455 s; baterias alvo 2,0-2,1 s/corrida; sabotagens ~0,1 s cada; sondas <1 s; VRAM/RAM/CPU de pico nao medidos (sem GPU, sem render); disco 27.739.770.880 -> 27.549.470.720 B.
- Passo 7 (composicao): vertice Prata 4,1 s de parede (1,91 s internos), RAM de pico 398.356.480 B, 49.750 triangulos, GLB 3.180.412 B; Ouro 6,17 s (5,04 s), RAM 518.205.440 B, 149.250 triangulos, GLB 8.053.592 B; Lendario 24,56 s (23,51 s), RAM 871.940.096 B, 497.500 triangulos, GLB 22.332.120 B. Bakes puros 112,64/112,74/114,66 s de parede, RAM de pico 982.261.760/1.120.202.752/1.065.697.280 B, VRAM de pico 726-733 MiB (nivel do ambiente de trabalho; utilizacao GPU <= 7% nas previas), saidas por bake GLB 5.964.448 B + textura 3.083.321 B (malha ancora 49.750 triangulos); bake instrumentado 120,84 s; contraprova 118,88 s (RAM ~1,07 GB); suite da branch 30,983 s; CPU nao medido (contador a 0 no contexto destacado, D-4).
- Passo 8 (julgamento): suite do Critico corrida por ele no PC, 30.450 s (regua 404 reproduzida); re-medicoes proprias registadas no julgamento; nenhuma escrita no projeto por ele.
- Passo 9 (este fecho): suite final 30,497 s; bakes 110,59/110,75 s de parede, RAM de pico 1.014.124.544/1.120.153.600 B, VRAM de pico 729/765 MiB, utilizacao GPU 0-1%; bake instrumentado 116,65 s, RAM de pico 1.076.391.936 B, VRAM 720 MiB; render flat 21,01 s; CPU nao medido (contador a 0 no contexto destacado, como no passo 7).

DISCO FINAL (SS9.1.7): C: livre no fecho = 27.196.502.016 B, contra 28.034.301.952 B da abertura da frente (passo 0.7) - diferenca liquida medida de 837.799.936 B ao longo de toda a tranche (artefactos de trabalho em _muse_rc dos passos + actividade concorrente na maquina; os deltas por passo estao registados acima e nas entradas de cada passo). O piso de aborto de 4 GiB (CC-01) nunca foi aproximado; gpu.lock intocada do principio ao fim (0 B, mtime 2026-11-01T12:59:09).

COPIA DO CODEX (SS9.1.8): git status dela LIMPO e HEAD 626229bfe1921cddc003b583f5e83ea064343522 na abertura e no fecho deste passo - identica ao fecho do passo 7; esta linha nao lhe tocou (so leitura).

ESTADO: a Frente D esta EXECUTADA ate ao passo 9 sob o veredicto do passo 8: mecanismo PRONTO COM RESSALVAS (R-1: celula cega T-MIX-2 x S-PC1-3, nomeada e medida por sonda no valor julgado; R-2: rota da composicao vs letra da CC-14, registada - a composicao foi medida antes de qualquer consumo a jusante e julgada antes da bateria de fecho; R-3: CPU nao medido nos paineis do passo 7 e deste fecho); qualidade visual NAO JULGADA - aguarda o olho do Mestre sobre o render flat deste fecho e o par antes/depois do passo 7. Ficam ABERTOS, declarados e nunca varridos (pacote SS9.2): C-COR03 (medias do preenchimento em sRGB - a S2-pipeline-linear NAO esta fechada; quantificacao devida em tranche propria), A1 (clip de borda no bake T1, intacto por desenho; magnitude em producao NP5 por medir; tranche propria nao autorizada), D1 (IoU por vista 0,8177/0,7774/0,8065/0,7957 < 0,88), FA-2 (confirmacao cruzada DeltaE textura embutida x PNG externo; adiavel, nao bloqueia) e a qualidade visual. Limites que viajam com a guarda: ela e estrutural, nao semantica (troca de acessores entre primitivos de igual contagem e indetectavel por construcao); verificar_glb_texturizado nao foi auditado por esta tranche. Os 9 ficheiros extraviados seguem byte-intactos na arvore (SHA-256 reconferidos neste fecho: preenchimento 1B785652..., _blender_cor 5BC89FB4..., passo CC4DD88A..., __init__ 73D208FD..., mapa_territorios AFD75403..., test_cor_territorios 4A8585A4..., test_cor_preenchimento_barreira 8003D58F..., test_cor_pesos 5F0867DB...; projecao no estado de fecho do passo 6, 10987B2C...), fora de todos os commits da frente - o merito e da tranche P1 (CC-17).

- I0004 (CM-000009), 2026-11-02.

FRENTE P1 - TRANCHE T-P1-0 (CORRECCOES DOS 3 TESTES EXTRAVIADOS, C-P1-1 a C-P1-3 do julgamento CC-17): EXECUTADA - os 3 FAIL eram defeitos de teste (0 de producao); producao INTOCADA por SHA; sem commit (adocao re-serializada = T-P1-1/T-P1-2, C-P1-6).



AUTORIDADE E ABERTURA: julgamento de merito da meia-tranche extraviada (I0003, frente P1, CC-17): veredicto (a) ADOPTAR como base da P1 com correccoes C-P1-1...C-P1-6; esta tranche aplica SO C-P1-1...C-P1-3 (ficheiros de teste). Abertura medida no PC: HEAD 29cee7b8588a9848617d99d7453bb88e9505dcbc; git status = exactamente as 9 linhas extraviadas (5 M + 4 ??); SHA-256 dos 9 = ancoras do julgamento, digito a digito (preenchimento 1B785652..., _blender_cor 5BC89FB4..., passo CC4DD88A..., __init__ 73D208FD..., mapa_territorios AFD75403..., projecao 10987B2C..., test_cor_territorios 4A8585A4..., test_cor_preenchimento_barreira 8003D58F..., test_cor_pesos 5F0867DB...); PC ocioso ha 31.581 s a abertura. Reproducao pre-correccao no PC (venv do projecto): 24 testes extraviados = FAILED (failures=3, skipped=1) - os 3 FAIL da regua, confirmados no ambiente real.



CORRECCOES (so 2 ficheiros de teste mudam; test_cor_pesos intocado): C-P1-1 (test_cor_territorios, U8): as duas assercoes passam a igualdade exacta NO DOMINIO f32 da matriz (fator == np.float32(0.6)), sem tolerancia; errata de uma linha registada ao plano de testes julgado (U8: "== piso, exacto no dominio f32 da matriz"). C-P1-2 (test_cor_preenchimento_barreira, U12): assercoes reescritas para o estado final julgado - alc[3] verdadeiro, classe[3] == ORFA, anel[3] == 3, onda[2] == 0 acrescentado, e a propriedade de seguranca explicita: onda[3] == ONDA_LIVRE (!= 0 - B nunca recebe a onda de A). C-P1-3 (U14, simetrica): classe[1] == ORFA, onda[1] == ONDA_LIVRE, onda[1] != -1 (a face territorial nao recebe a onda cega); acrescentado classe[2] == BARREIRA. U17 e os restantes testes dos dois ficheiros intocados (diff conferido linha a linha).



PROVA DE DENTES POR MUTACAO (em COPIA da arvore fora do repo, apagada no fim; controlo sem mutacao: 24 testes OK (skipped=1)): M-PISO (piso efectivo trocado para 0,5 em mapa_territorios, na copia) - o U8 corrigido FALHA (np.float32(0.5) != np.float32(0.6)); ficheiro de territorios sob o mutante: 12 testes, 1 failure (so o U8). M-PAREDE (condicao de parede removida em difundir_barreira, na copia) - o U12 corrigido FALHA (classe[3] = 1 BARREIRA != 2 ORFA: a onda de A atravessa e entrega em B) e o U14 corrigido FALHA (classe[1] = 1 != 2); ficheiro de barreira sob o mutante: 9 testes, 4 failures + 1 skipped. Cada teste corrigido apanha o seu mutante - as correccoes nao afrouxaram nada.



REGUA NO PC (suite completa, arvore real, venv do projecto, unittest discover): Ran 404 tests in 34.600s - OK (skipped=2) = 402 ok + 0 FAIL + 2 skipped + 0 erros. Os 3 testes corrigidos aparecem ok por nome. Skips nomeados: U20 (sem OFICINA3D_P1_PROVA - prova do job-ancora, pertence a T-P1-1) e test_mcp::test_criar_servidor_registra_as_ferramentas (pacote mcp nao instalado neste venv) - ambos pre-existentes e declarados, nenhum novo.



INTEGRIDADE DE FECHO: HEAD intacto (29cee7b...); os 6 ficheiros de PRODUCAO extraviados com SHA-256 identicos aos da abertura (ancoras acima); test_cor_pesos identico (5F0867DB...); novas ancoras dos ficheiros corrigidos: test_cor_territorios 910B9BC5B144EE1F... e test_cor_preenchimento_barreira B1DE6170D9883651...; git status = as mesmas 9 linhas dos extraviados (+ este append ao REGISTRO, sem commit, como a tranche manda). FICA ABERTO, fora desta tranche por desenho: C-P1-4 (guarda da disputa v3) e C-P1-5 (posicao de fator_face_vista) - tranche P1.1 (T-P1-2); U20 e a ablacao no ancora - T-P1-1; C-COR03/PN-01 intocado e nao decidido (fronteira do julgamento, seccao 4). Relatorio proprio: hidden_files/p1-t0-correccoes-testes-2026-11-02.md (workspace do Muse).



- I0004 (CM-000009), 2026-11-02.


FRENTE P1 - TRANCHE T-P1-1 (ADOPCAO DA FATIA P1.2 - PREENCHIMENTO COM BARREIRAS, C-P1-6): EXECUTADA - commit b552a87 na main; U20 exacto no artefacto real; ablacao A2 x A0 no job-ancora com a sessao a reproduzir a baseline da Frente D byte a byte; R1-R7 medidos. Julgamento da serie B (Critico dedicado) a seguir - nenhum job de producao pode pedir a fatia (barreiras ou pesos) antes de ele fechar: a fatia so entra por flag explicita no pedido e o worker nao passa o campo.



AUTORIDADE E ABERTURA: julgamento CC-17 (adocao re-serializada P1.2 -> P1.1) + fecho da T-P1-0. Abertura medida: HEAD 29cee7b8588a9848617d99d7453bb88e9505dcbc; status = as 9 linhas extraviadas + o append da T-P1-0 neste REGISTRO (por commitar); ancoras dos 9 ficheiros = julgamento/T-P1-0, digito a digito (testes ja nas ancoras novas da T-P1-0: territorios 910B9BC5..., barreira B1DE6170...); PC ocioso ha 32.142 s. Insumos congelados por hash: GLB-ancora 9A5C1203BB41DDF8... (2.879.252 B), mapa territorios_orc.npz EECD9A36... (glb_sha256 interno = o da ancora), pedido-base s2cor08-1/orc EBA1093A....



U20 (guardiao de paridade; OFICINA3D_P1_PROVA = pasta com territorios_orc.npz + modelo_uv.glb, copias conferidas por hash): o modulo de barreira corre OK com o U20 A CORRER (9 testes, nenhum skip): (anel, onda) da onda de barreiras == anel_bake_barreira/onda_bake_barreira do .npz EXACTAMENTE sobre o grafo real; orfas = 254; anel medio sobre a classe BARREIRA = 3,24 (places=2); anel max = 21. A porta de producao reproduz o laudo no artefacto real - a leitura de fidelidade do julgamento fica de pe.



ABLACAO A2 x A0 (4 bakes puros de producao, _blender_cor.py da arvore; pedidos = o do ancora pos-S2 com saidas redireccionadas; A2/A2' com territorios {ativo: true, mapa, barreiras: true} e SEM a chave pesos; gpu.lock detido durante os bakes e reposto a 0 B): A0 textura f198a2a7... / GLB 9dd67084... = A BASELINE DA FRENTE D BYTE A BYTE (R16 na forma mais forte) e A0 == A0' identicos (determinismo); numeros da sessao = laudo (diretos 420.713; fontes 24.590; preenchidas 25.160; anel livre 3,18/21; IoU por vista 0,8177/0,7774/0,8065/0,7957). A2 == A2' byte-identicos (textura c53b165c..., GLB ba1e8b17...). Diagnostico A2: aplicado=true, sha_npz conferido, pesos_ativos=false registado (nunca herdado em silencio), carga do mapa 0,06 s, texels_disputa_antes_npz 42.715 e fieis_antes 377.997 (as classes do laudo reproduzem); faces por classe: fonte 24.590 / barreira 24.906 / orfa_livre 254 / sem_fonte 0; proveniencia v3 de preenchimento em duas camadas, declarado: barreira 402.132 texels, livre (orfas) 2.901 texels, direto_fiel/disputa nulos com o motivo "fatia de pesos desligada".



REGUAS R1-R7 (plano julgado, seccao 3.1): R1 anel medio da barreira 3,24 <= 3,3 (esperado 3,24) OK; R2 anel maximo da barreira 21 <= 21 OK; R3 orfas = 254 exactas OK; R4 cobertura final identica a A0 (845.063 texels UV; sem_cor 0 em ambos; preenchimento_3d 424.350 texels em ambos) OK; R5 salto medio da classe com preenchimento (instrumento D-H4.1 do pacote de adopcao, mesma serie pos-Frente D, classes da reconstrucao validada): A0 73,6242 -> A2 73,6170 - CAI na direccao obrigatoria, magnitude -0,0072 registada sem meta inventada (nas 895 arestas da classe que mudaram, a media cai -0,35; estratificado por banda de fronteira da face preenchida: banda 0 +0,12, banda 1 +0,02, banda 2 -0,15, banda >=3 -0,27); R6 texels diretos byte-identicos a A0: 0 diferencas sobre a mascara de diretos do laudo (420.712 texels) - a mascara texel_* do .npz esta na orientacao interna do pipeline (flip vertical face ao PNG salvo): sem o flip medem-se 6.520 falsos positivos, com o flip 0; diferencas totais A0 x A2 = 62.256 texels, todas fora dos diretos; R7 nenhuma outra classe piora alem de +5%: interna +0,06% (52,70 -> 52,73), fronteira pura +0,45% (50,64 -> 50,87), costura UV -0,26% (108,86 -> 108,58) OK.



B4 (quem paga a barreira - medicao do executor para a serie B): dos arrays do .npz, 585 faces pioram com a barreira e o total extra PELA FORMULA DO PROPRIO LAUDO (adocao/p1/territorios.py:603 - soma de anel_barreira com orfas a 0, menos anel_livre) = +680 exactos (regua da bateria: <= 748); a conta liquida alternativa (orfa ao seu anel livre real) = +1.304 - as duas contas registadas, a leitura e do Critico. 14 faces pioram mais de +6 aneis, com registo nominal (livre -> barreira): territorio 1 (costas): 16125 (1->12), 16127 (2->11), 16129 (2->10), 16723 (1->11), 16726 (1->10), 16734 (2->9), 43671 (1->8), 44171 (3->10), 44187 (2->11); territorio 0 (frente): 45728 (2->9), 46132 (1->11), 46133 (1->10), 46137 (1->9), 46144 (1->8). N-O2-P1b (medicao nova da bateria, sem aceite/reprova nesta tranche): nas 24.906 faces BARREIRA, a vista vencedora majoritaria da face-fonte == rotulo geometrico propagado pela onda em 23.566 faces (94,62%); nas ORFAS o rotulo e o da onda livre por construcao (fontes maioritarias: esquerda 99, costas 65, direita 67, frente 23). B5: faces sem fonte alcancavel = 0 e texels dentro da UV pintados por dilatacao = 0 (a dilatacao segue 100% halo: 2.709.638 texels fora da UV, igual a A0).



ADOPCAO (C-P1-6, commits por fatia com divisao por plumbing): commit b552a87f6505f8a309433bba00844c4ad4dc7298 na main (6 ficheiros, +600/-7): preenchimento.py inteiro; testes/test_cor_preenchimento_barreira.py inteiro; passo.py inteiro (repasse opcional, default desligado); __init__.py inteiro (docstring - descreve tambem a matriz de fatores da P1.1, que entra na T-P1-2); mapa_territorios.py PARCIAL (so carga + validacao; fator_territorial/fator_para_pedido ficam por commitar); _blender_cor.py PARCIAL (sem o calculo do fator e sem o parametro fator_face_vista na chamada - conferido na arvore commitada: 0 ocorrencias de fator_territorial/fator_face_vista=fator_pedido e 0 "def fator" no mapa). CONDICAO ESCRITA: nenhum job de producao pode pedir a fatia de pesos antes de o julgamento da P1.1 (T-P1-2) fechar; nesta arvore o caminho de pesos esta fisicamente incompleto (sem fator e sem parametro) e a proveniencia v3 declara "fatia de pesos desligada" quando ele nao corre. Apos o commit, as versoes completas foram restauradas na arvore e reconfirmadas por SHA (mapa AFD75403..., _blender_cor 5BC89FB4...): o resto da fatia P1.1 segue por commitar e byte-intacto (projecao 10987B2C..., test_cor_territorios 910B9BC5..., test_cor_pesos 5F0867DB...).



SUITES POS-ADOPCAO (venv do projecto, unittest discover): (A) arvore de trabalho, sem env: Ran 404 tests - OK (skipped=2) = 402 ok + 0 FAIL + 2 skipped (a regua de fecho da T-P1-0, mantida sobre a arvore pos-commit); (B) arvore de trabalho, COM OFICINA3D_P1_PROVA: Ran 404 tests - OK (skipped=1) = 403 ok + 0 FAIL + 1 skipped (o U20 corre e passa dentro da suite completa; o skip restante e o test_mcp pre-existente); (C) WORKTREE LIMPO do HEAD b552a87: Ran 389 tests - OK (skipped=2) = 387 ok + 0 FAIL + 2 skipped - a arvore commitada e auto-consistente sem os restos da P1.1 (389 = 404 - 12 testes de territorios - 3 de pesos; worktree removido no fim).



PAINEL (medido): tempo interno dos bakes 41,56 s (A0) / 41,47 s (A0') / 42,20 s (A2) / 43,21 s (A2') - o acrescimo de A2 sobre A0 e +1,5% (carga do mapa 0,06 s incluida); pico de VRAM 762 MiB e pico de working set do processo Blender 1.127,9 MB (amostrador proprio a cada 2 s durante os 4 bakes, 165 amostras); triangulos 49.750 (inalterados); textura A2 3.081.704 B e GLB A2 5.962.828 B (A0: 3.083.321 B / 5.964.448 B); tokens: nao se aplica (motor local); CPU: nao medido (contador a 0 no contexto destacado - fenomeno declarado da Frente D).



FICA ABERTO: o julgamento da serie B sobre esta entrega (Critico senior dedicado da P1) - a adopcao fica sob o veredicto dele; a T-P1-2 (adocao da P1.1: C-P1-4 guarda (terr_tex >= 0) na disputa v3, C-P1-5 posicao de fator_face_vista, commits do resto da fatia, varredura de calibracao, ablacao A1 x A0 e composicao A3, sabotagens e veredicto visual separado no fecho da P1); C-COR03/PN-01 intocado e nao decidido (as reguas de cor desta tranche sao da serie pos-Frente D e ficam datadas se a correccao C-COR03 aterrar depois, como o julgamento declarou). Relatorio proprio: hidden_files/p1-t1-adocao-p12-2026-11-02.md (workspace do Muse).



- I0004 (CM-000009), 2026-11-02.


---

## 2026-11-02 (noite) — P1 / T-P1-2: adopção da fatia P1.1 (pesos territoriais) e FECHO da frente P1

Executor I0004 sob CM-000009, sob o julgamento CC-17 e o julgamento da série B sobre a T-P1-1 (PRONTO COM RESSALVAS; emendas E1–E5, condições C-B1…C-B5). Relatório integral: `hidden_files/p1-t2-adocao-p11-fecho-2026-11-02.md` no goal da Oficina (pasta de trabalho do Muse).

**E1/C-B5 (abertura):** a semântica fecha — leitura de código + bake de ensaio: com `"pesos"` no pedido, `pesos_ativos: true` ⟺ fator calculado e passado à rasterização (disputa 42.715 → 42.001 e fiéis 377.997 → 378.712 no ensaio a piso 0,6/d_ref 0,03); sem `"pesos"`, `false` e contagens nulas (T-P1-1).

**Correcções:** C-P1-4 — a contagem de disputa da proveniência v3 ganha a guarda `(terr_tex >= 0)` do laudo; C-P1-5 — `fator_face_vista` passa para depois de `amostragem` em `projecao.rasterizar_textura` (grep: nenhum chamador posicional afectado). E3 — a v3 itemiza `preenchimento_sobre_faces_fonte` (provado em produção no A2: 19.317; as classes fecham: 402.132 + 2.901 + 19.317 = 424.350). Cada correcção com teste que morde em mutação (M-GUARDA e M-ORDEM falham como exigido; controlo limpo verde).

**Calibração (grelha julgada 3×3, critério pré-registado por SHA antes dos bakes):** a meta de desenho de R8 (redução ≥ 25% → ≤ 32.036) **não é atingida por nenhum ponto** — o melhor é −2,85% (0,50/0,015). A régua julgada de R8 (disputa < 42.715, definição do laudo) cumpre-se em todos. Selecção pelos portões R9–R13 e pelo desempate pré-registado: **piso = 0,75, d_ref = 0,03** (disputa L 42.226, −1,14%; fiéis L 378.486, +489; discordância residual 110,3261 < 110,3512 de A0; % > 60 residual 68,3445% < 68,3809%). (0,50; 0,060) produz um bake byte-idêntico ao escolhido — vencedores coincidentes na grelha discreta de distâncias.

**Ablações:** A0 = A0′ = baseline da Frente D byte a byte (`f198a2a7…`/`9dd67084…`); A1 = bake da calibração escolhida; A2 fresco = A2 da T-P1-1 byte a byte; **A3 = A3′ byte-idênticos** (`2a83cbe6…`/`42d7ea69…`), com a composição a fechar (disputa de A3 = a de A1; anel de A3 = o de A2, 3,24/21; classes de A3 = as de A2). Sabotagens: S1 mapa permutado — sem melhoria falsa (disputa L 42.667 ≈ baseline; pela contabilidade do pipeline, disputa 165.967 e órfãs 13.114 — as fatias respondem ao conteúdo do mapa); S2/S6 recusas `MapaIncompativel` por SHA antes de pintar; S3 consistência de classes — recomputação independente = JSON do bake, e a classe forçada faz a verificação falhar; S5 recusa de piso 0,05 pela faixa vetada. Halo (E2, instrumento declarado): 1.262 cruzamentos em A0 = A1 = A2 = A3 (domínios pintados idênticos; absoluto diverge dos 1.469 da série B pelo proxy de halo, declarado no relatório).

**FECHO DA FRENTE P1 (consolidado):** o preço da barreira é **+1.304 anéis líquidos** (conta líquida, C-B2 — nunca +680, que é só a prova de fidelidade à previsão da bateria); 585 faces pagam; as 14 faces nomeadas na T-P1-1 (território 1/costas, onda 1: 16125, 16127, 16129, 16723, 16726, 16734, 43671, 44171, 44187; território 0/frente, onda 0: 45728, 46132, 46133, 46137, 46144 — em todas, a onda que entrega é a do próprio território) ficam como **custo aceite do mecanismo**, não defeito a corrigir nesta frente. Leitura vinculada de R5 (C-B3): o salto com_preenchimento moveu-se na direcção desenhada onde o mecanismo actua (A3 73,6153 vs A0 73,6242; bandas profundas da T-P1-1), **sem** afirmação de melhoria material da costura global (Δ ≈ 0,01%); a subida da classe fronteira_vista (+0,80% em A3) fica registada ao lado. **C-B1:** até este fecho, nenhum job de produção pediu `"pesos"` nem `"territorios"` — as fatias só correram em bakes de prova sobre o âncora; a flag de uso de produção fica **desligada por omissão no código** (o trabalhador não passa o campo) e assim permanece até decisão expressa em contrário. E4: PN-01/C-COR03 **não aterrou** nesta tranche (branch do Codex parada em `626229b`); as réguas de cor da P1 são da série pós-Frente D e ficam datadas se C-COR03 aterrar depois, como julgado.

Painel (bakes da tranche): tempo 41,47–43,04 s por bake; VRAM pico 762 MiB e RAM (WS Blender) pico ≈ 974 MB medidos na fila 1 e no ensaio E1 — na fila 2 o amostrador saiu vazio (parou no `sampler.stop` da fila 1): VRAM/RAM da fila 2 **não medidos**, declarados; triângulos 49.750; texturas ≈ 3,08 MB; GLBs ≈ 5,96 MB; CPU **não medido**. Suítes e commits na secção seguinte do relatório integral.


---

## 2026-11-03 — P1: veredicto visual do Mestre sobre o par A0×A3 (fecho integral da frente)

**Veredicto visual do Mestre sobre o par A0×A3 (2026-11-03):** apresentado o par (frente e costas aproximado, antes A0 × depois A3), o Mestre declarou **não ter percebido diferença ao seu olho** («não vi diferença») e **aceitou o fecho** porque os Críticos aprovaram e mediram a melhoria («já que os críticos aprovaram e viram que realmente ficou melhor e progrediu, beleza, tranquilo»). Regista-se como **ACEITE por confiança na medição** — não como aprovação visual de melhoria percebida. Com este acto, a Frente P1 está **integralmente fechada** (mecanismo julgado PRONTO COM RESSALVAS + veredicto do Mestre inscrito).


---

## 2026-11-03 — T-COR: abertura da tranche de correcção da cor do Orc (T-COR-0) e diagnóstico medido (T-COR-1) entregue, a julgamento

Executor I0004 sob CM-000009, pacote citável «DESENHO-CORRECCAO-COR-ORC + ERRATA-CORRECCAO-COR-ORC». Relatório integral: `oficina-audit/tcor/RELATORIO-T-COR-1.md` no workspace do Muse (21.764 B, SHA-256 `16e73c2e…`); acto gémeo no índice do tribunal, §23 (assento E-R1).

**T-COR-0 (abertura, camada invisível):** pré-voo — HEAD `af2dc969…`, árvore limpa, C: livre 26.305.806.336 B, PC ocioso há ~17,7 h, `gpu.lock` pela trava da casa. **A0 reproduzido byte a byte**: textura `f198a2a7…` e GLB `9dd67084…` (baseline da Frente D), contadores do laudo todos iguais; painel do bake 45,52 s · VRAM de pico 800 MiB. Facto lido: o `pedido_cor.json` do job âncora é o bake v1 de 1024 (`ebd744a9…`), não a configuração da baseline (2048). Árvore principal limpa no fim; nenhum byte da pipeline alterado.

**Fila (declaração E-R1, inscrita também no índice §23.2):** a ordem anterior («o próximo na fila de placa é P-02 ≡ MP-T1») lê-se como ordem entre braços do tribunal; a T-COR é trabalho da linha principal sob o mesmo `gpu.lock`, e os seus blocos curtos de placa (T-COR-4) correm antes da corrida completa da MP-T1.

**T-COR-1 (diagnóstico medido, só medição):** adenda pré-diagnóstico selada antes dos números (`62540655…`); veredictos pelos limiares pré-registados: **H-A CAI · H-B CAI · H-C ENFRAQUECE · H-D CAI · H-E CONFIRMA · H-F ENFRAQUECE** (ressalva: o modo de média da produção é indecidível pela réplica — a proveniência por face da produção difere da réplica nas bordas; a exigência `proveniencia_v3` viaja para T-COR-2). Achado central: o salto de cor mora entre ilhas do atlas (0,2248 ≈ 5,5× o controlo). Baselines do portão inscritas (M-DET; M-LISO 50,22%; M-COST). Estado: relatório **a julgamento dedicado** (Método + Regras/Fila); T-COR-2 não existe até ao julgamento; nenhuma correcção foi escolhida nem implementada.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — T-COR: adopção expressa da ordem da fila (descarga da C-1)

**Adopção expressa (descarga da C-1 do julgamento Regras/Fila de T-COR-1, `699f1478…`):** a ordem da fila fica **ADOPTADA** nos termos da proposta §7 do desenho — o slot de GPU de T-COR-4 (bakes curtos da correcção da cor) corre **ANTES** da corrida completa da MP-T1 ≡ P-02; a leitura do §22 do índice do tribunal («next = P-02 ≡ MP-T1») vale como ordem **entre braços do tribunal**. **Sem adopção alternativa.** Assento gémeo no índice do tribunal, §23.5. A entrada anterior desta tranche inscreveu a ordem tal como declarada (declaração E-R1); esta fornece a palavra expressa de adopção que a condição C-1 exige, antes de T-COR-4 abrir.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — T-COR: adenda T-COR-2 julgada (PRONTO COM RESSALVAS ×2) e registada — descargas E-R3, C-M6 e fecho da C-1

A **adenda T-COR-2** (`oficina-audit/tcor/ADENDA-T-COR-2.md`, 27.371 B, SHA-256 `af83444a…`) — **escolha K2, re-fundada em H-E** (difusão do campo de cor sobre o grafo dual do corpo; directos invariantes, L-5) e passo novo **T-COR-2.5** (despejo `proveniencia_v3`, com interruptores de morte V4 e forquilha de atribuição) — foi **julgada PRONTO COM RESSALVAS pelas duas lentes**: Método (`c18c9186…`; condições C-T2-M1…C-T2-M4) e Regras/Fila (`f30de535…`; condições C2-1 e C2-2). Acto principal no índice do tribunal, **§24**; mapa completo: as condições dos julgamentos de T-COR-1 ficam todas descarregadas em pleno.

**Com a adenda regista-se a errata C-T2-M3** (`ERRATA-T-COR-2.md`, `f4a3f0fa…`): reconcilia a perna L-2 de §4 da adenda (Δcost-S ≤ 0,1574 e R_S ≤ 3,86) com a letra de §5.2.3 do desenho («R ≤ 1,5», lida contra o controlo antigo) — **nenhum número nem limiar muda**; a leitura válida do par é a da folha.

**Descargas neste acto (C2-2):** (i) **errata C-M6 registada** (`ERRATA-T-COR-1.md`, `47d94d22…`) — reconcilia a §11 do relatório T-COR-1; impacto numérico zero; (ii) **inscrição bilateral E-R3 no assento do PN-01** (índice do tribunal, §5(ii)): o caminho (ii) de §7 foi o seguido — a medição própria D-F de T-COR-1 inscreve-se como **contribuição medida**; o destino do PN-01/T4 do Codex lê-se **confirmação independente ainda devida** (K3 não foi escolhida; o locus C-COR03 fica com o PN-01/T4, com o tamanho de D-F como contribuição); (iii) **C-1 fechada**: descarregada na §23.5 do índice e na entrada gémea anterior deste REGISTRO (commit `f330a187…`), supersedendo o «em curso» do §7 da adenda.

**Estado:** **T-COR-2.5 autorizado a correr** (com a C-T2-M2 a governar o seu V4 e a C2-1 a fixar o conteúdo do seu relatório); **T-COR-3 só depois** de a forquilha de §3 da adenda cair no ramo «prosseguir».

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Motor Próprio: pacote de execução da melhoria do motor novo julgado (PRONTO COM RESSALVAS ×2), errata registada e leitura governante da fila adoptada

Por ordem do Mestre («Então melhore», 2026-11-03 08:57), o **pacote de execução** do desenho de melhoria do motor novo foi julgado: `PACOTE-MELHORIA-EXECUCAO.md` (37.047 B, SHA-256 `0e6a0fdd…`) operacionaliza «DESENHO-MELHORIA-MOTOR-NOVO + ERRATA-MELHORIA-MOTOR-NOVO» em cinco pacotes de construção (**PKG-1** preparação · **PKG-2** saída · **PKG-3** runner/painel/grelha · **PKG-4** perfis · **PKG-5** determinismo), com o mapa (a) já na VM / (b) só depois de a MP-T1 medir a base / (c) fora da tranche. Julgamentos: **Método** (`f566949e…`) **PRONTO COM RESSALVAS**, condições C-1…C-8; **Regras/Fila** (`d73f122a…`) **PRONTO COM RESSALVAS**, condições CR-1…CR-3. A **errata** (`ERRATA-PACOTE-MELHORIA.md`, 24.083 B, `df42d3d9…`) descarrega C-1…C-8 em especificação, sem editar o pacote; a unidade citável passa a ser o par **«PACOTE-MELHORIA-EXECUCAO + ERRATA-PACOTE-MELHORIA»**.

**Descargas de registo neste acto:** **CR-1** — fica adoptada a leitura governante: construir infra-estrutura de prova na VM **não** é executar candidato; a estreia de qualquer candidato continua a ser a MP-T1 sob a fila CE-6. **CR-3** — pacote e julgamentos registados antes de qualquer pacote abrir. **CR-2 fica condição viva:** o relatório de fecho de cada pacote prova staging e clone byte-idênticos (manifesto antes×depois). A construção pode abrir, **PKG-1 primeiro**; a fila da GPU não se mexe. Acto principal no índice do tribunal, **§25**.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Motor Próprio: mapa de paridade julgado (PRONTO COM RESSALVAS ×2) e errata registada — «MAPA-PARIDADE + ERRATA-MAPA-PARIDADE» é o guia governante das melhorias

O **mapa de paridade** do motor novo (`MAPA-PARIDADE.md`, 17.750 B, `d7766556…`; corpo `aaa31737…`) — estudo teórico sobre fontes primárias, sem corrida nenhuma alegada — foi julgado **PRONTO COM RESSALVAS** pelas duas lentes: **Método** (`468221b3…`), com a condição **C-M1 GRAVE**: a frase «nenhum consumidor usa as cores de vértice do TripoSR» é **falsa** — o COLOR_0 do TripoSR é a fonte 2 do passo T2 da pintura da casa e a única fonte no caminho de zero vistas canónicas; **Regras** (`9f6161de…`). A **errata** (`ERRATA-MAPA-PARIDADE.md`, 22.406 B, `c2418acc…`) descarrega C-M1…C-M6, C-R1, C-R2, C-R4 e a perna de inscrição de C-R3, sem editar o mapa.

**Quadro final corrigido (o que vale):** a fronteira estrutural é **uma só raiz — F-01/F-02** (entrada multivista e a sua face, as costas canónicas); a única dívida de treino é a **destilação (F-03)**, que só se fecha com programa próprio sob a cadeia C-07 (outputs Hunyuan proibidos como treino, §5.b); **F-07** (offload de VRAM) é condicional e fencada à medição CE-4 da MP-T1; falha nova **F-11** — granularidade da resolução de extracção (o emprestado tem botão contínuo; o nosso só profundidades inteiras). IoU, tempo e pico de VRAM do motor novo continuam **não medidos** (provas: MP-T1; determinismo e perfis: MP-T2). Com este registo, **«MAPA-PARIDADE + ERRATA-MAPA-PARIDADE» é o guia governante** das melhorias do motor novo. Acto principal no índice do tribunal, **§26**.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Motor Próprio: PKG-1 FECHADO — correcção executada e confirmada sem condições

O **PKG-1** (preparação de entrada da casa) fechou. A ronda de correcção (`RELATORIO-PKG-1-CORRECCAO.md`, 11.575 B, `b2aa8898…`; `preparacao.py` corrigido, 17.587 B, `f05047ba…`) descarregou **CM-1 [GRAVE]** — a truncagem intermédia da fórmula de preenchimento, aplicada nos dois ramos a partir do código oficial staged (caso nomeado 115×100 → (11, 18), onde a casa dava (11, 19); sonda: 0/22.500 divergências na grelha, contra 25,47% da fórmula velha) —, **CM-2** (selecção da componente por **área poligonal do contorno**, a medida do oficial, sem OpenCV) e **CM-3** (documental). Bateria da ronda: controlo **8/8 verde**, mutantes **8/8 vermelhos no alvo** (M7 vermelho só em tb13, devolvendo [11, 19]). A confirmação (`JULGAMENTO-PKG-1-CORRECCAO-METODO.md`, 12.664 B, `eb0b89e2…`) é **CONFIRMA A DESCARGA de tudo, sem condições novas**, com prova própria do crítico (grelha 173×173: 0/29.929 divergências).

**Forma de citação da CR-2 (descarga da C-1 de Regras):** staging (82 ficheiros) e clone (289) idênticos ao manifesto antes×depois nas duas rondas — os quatro manifestos são byte-idênticos entre si (49.473 B, `eb36c42c…`); para os **3 pesos ≥64 MiB**, o facto provado é «idênticos por **tamanho exacto + mtime em nanossegundos**» — a forma curta «byte-idêntico» **não** se usa para eles. Com a **errata-da-errata** (`ERRATA-DA-ERRATA-PACOTE.md`, 17.918 B, `a01b8aef…`), a perna (3) da delimitação caiu: as divergências de entrada vivas são **duas** — (1) o modelo de fundo (rembg+U2Net da casa vs. RMBG-1.4 do oficial; substituição CE-2) e (2) o filtro do tecto (LANCZOS vs. INTER_AREA), **não medida** até à MP-T2; a cadeia citável do pacote, para matéria do PKG-1, passa a **três termos**: «PACOTE-MELHORIA-EXECUCAO + ERRATA-PACOTE-MELHORIA + ERRATA-DA-ERRATA-PACOTE». Declarado não exercido: a inferência real rembg+U2Net — estreia na abertura da MP-T1. **PKG-1 FECHADO.** Acto principal no índice do tribunal, **§27**.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Tribunal P3: régua D-H0 V3 CERTIFICADA pelo Supremo Tribunal RPGional — a V3 é a régua oficial

O Comestre Juiz certificou a régua **D-H0 V3** (`CERTIFICACAO-DH0-V3.md`, 20.080 B, `7c759228…`), sobre a bateria corrida pelo condutor I0008 (`BATERIA-DH0-V3-RELATORIO.md`, 28.988 B, `f0d35048…`) e julgada **PRONTO COM RESSALVAS** pelas duas lentes (Método `348f3836…`; Regras `7b38f8a2…`) — condições só de inscrição, todas descarregadas no próprio acto. Portões: **núcleo CERTIFICADO** · **espelhos CERTIFICADO** (na sua linha de âmbito) · **mínimos CERTIFICADO** · **distância NÃO CERTIFICADO**, na forma citável exacta: «ramo distância: não certificado — medido e reprovado». A partir de 2026-11-03, a **V3 é a régua oficial**; a V2 fica época fechada (série D-H0/V2), sem mistura de números entre séries. Adjudicação do item 5: o valor que governa para IoU_esp do conjunto nulo é **0,658628**; o 0,546320 impresso no §D.5 do selo fica **NÃO CITÁVEL** — o selo não se emenda; a correcção vive no acto e neste registo. Leituras de sujeito da bateria (não são matriz): **Orc CERTIFICÁVEL · Capríleo PARCIAL (perfis) · Besta INDETERMINADO**. Certificar a régua não certifica matriz nem sujeito nenhum, nem decide rota da DECISÃO P3. Actos seguintes ordenados — (a) re-corrida de P-00 sob a V3, (b) julgamento de publicação, (c) re-inscrição composta de PN-09 — nenhum feito por este acto. Acto principal no índice do tribunal, **§28**.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Tribunal P3: matriz P-00 sob a V3 PUBLICADA e PN-09 re-inscrita com fundamento composto

A matriz **P-00 da série D-H0/V3** (`p00-v3/P00-V3-MATRIZ.md`, 28.835 B, `f048730a…`) foi **publicada** pelo acto do Juiz (`ACTO-PUBLICACAO-P00-V3.md`, 28.425 B, `741287e0…`), julgada **PUBLICA COM RESSALVAS** pelas duas lentes (Regras `a6b3fb1d…`; Método `b342ac53…`, que recomputou 45/45 células exactas) — todas as condições descarregadas no acto. **Publicada, não certificada:** os braços práticos lêem os sinais da série V3 desde 2026-11-03; a matriz da série V2 fica época fechada para P-00. Veredictos publicados (com os cinco qualificadores do acto-mãe): **Orc — CERTIFICÁVEL**, identidade **AFIRMATIVA**; **Capríleo — PARCIAL (perfis)**, com o par frente×costas **RECUSADO** (IoU_dir 0,2580, margem −0,1920 D−), identidade **AFIRMATIVA**; **Besta — INDETERMINADO**, identidade só na forma bipartida «**proveniência AFIRMATIVA, coerência INDETERMINADA**». As condições **(4)** linha de lateralidade entre três leitores e **(5)** Anexo S de §6.1-V3 ficam **PENDENTES NÃO EXERCITADAS**: toda a citação da matriz carrega a cláusula «publicada, não certificada — condições (4)/(5) de §6.1-V3 pendentes», e nenhum uso sob a V3 pode depender da linha de lateralidade nem do Anexo S até à adenda de completamento.

**§5.4 (pronúncia lavrada):** a leitura INDETERMINADO da Besta é a **primeira** escalação — **contador = 1**; nenhuma revisão de calibração é devida por acumulação (dispara à segunda escalação de qualquer conjunto) e a revisão **não fica descarregada** por esta publicação — fica armada. **PN-09 re-inscrita com fundamento composto:** (i) INDETERMINADO sob a V3 + (ii) recusa sob a V2 + (iii) concorrência independente T-14 (mede a malha, não depende da régua); a entrada originária não se apaga. Nenhuma decisão sobre o conjunto foi tomada; re-entrada só por conjunto corrigido via **REF-01 aprovado pelo Mestre** → re-corrida → adenda à matriz. Acto principal no índice do tribunal, **§29**.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Tribunal P3: campanha de ataque à régua V3 julgada — certificação CONFIRMADA COM RESTRIÇÕES, adenda de uso em vigor, programa V4 ordenado

Por ordem expressa do Mestre (2026-11-03, 11:16), **10 críticos atacantes** com lentes dedicadas + **1 bateria de estresse** atacaram a régua V3 certificada e a matriz P-00 publicada. Julgamento final: `JULGAMENTO-CAMPANHA-V3.md` (41.774 B, `45f4fadb…`). **Facto enquadrante: nenhum ataque virou um veredicto certificado nos conjuntos exercitados.** Por lente: **Reprodutibilidade SOBREVIVE limpa** (13/13 corridas hostis idênticas); Gramática, Degeneradas, Fronteiras, Mínimos, Mutação, Divergência e Plantas **sobrevivem com feridas**; **Espelhos CAIU** na leitura larga (o portão F×B(a) prefere a configuração espelhada nos 3/3 sujeitos de ouro, +17,4/+39,3/+23,6 p.p.; a forja `direita := espelho(esquerda)` certifica em 4/4; um conjunto meio-Orc/meio-Capríleo lê CERTIFICÁVEL) — a linha fica confirmada **só na sua letra** (espelho lateral único pela assinatura (b2)); **Distância CAIU na linha** (a não-certificação vivia só em prosa: conjuntos de distância liam CERTIFICÁVEL pelo caminho de produção).

**Decisão do Juiz:** a certificação **aguenta, RESTRITA**, na forma citável lavrada no índice (§30.2), sempre com os cinco qualificadores do acto-mãe — citar a certificação sem a cláusula da campanha é defeito de citação. Instrumentos: **errata** `ERRATA-CAMPANHA-V3.md` (5.902 B, `8f615a29…`; itens E-1…E-8 — não toca código nem números certificados); **Adenda de Uso V3-ATAQUE-01** (`ADENDA-USO-V3-ATAQUE-01.md`, 5.619 B, `34f2d93e…`; itens U-1…U-6) **em vigor desde o julgamento** — entre eles, o ramo distância fica **proibido como entrada** de qualquer corrida sob a série V3 até à V4; e **programa V4 ordenado** (V4-1…V4-11; ciclo completo de versão nova; os corpora da campanha são regressão obrigatória da bateria da V4). A **matriz P-00/V3 continua a valer** sob a adenda: verificação retroactiva executada **sem surpresas** (`p00-v3/NOTA-ADENDA-CAMPANHA.md`, 12.681 B, `e713bfae…`) — teste de espelho píxel-exacto **negativo (0/48)**, proveniência fresca **12/12 = manifesto T-08**, ramo **alfa ×12**. **Não ordenado:** tocar um byte da V3, re-correr P-00 sob a V3, decidir o conjunto da Besta ou qualquer rota da DECISÃO P3. A pronúncia de §5.4 fica intacta (contador = 1; a campanha não é a revisão de calibração). Fases 0–2 do programa executadas neste acto; o ciclo da V4 (Fase 3) fica por executar. Acto principal no índice do tribunal, **§30**.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Motor Próprio: PKG-2 FECHADO — errata da citação CR-2 e descargas expressas

O **PKG-2** (saída: contrato de dois artefactos e ligação da limpeza) fechou. Entrega: `RELATORIO-PKG-2.md` (22.659 B, `a1f28ee7…`), `saida.py` (`606f4bb1…`); julgamentos **PRONTO COM RESSALVAS ×2** (Método `fde1d31a…`; Regras `2cc00144…`), convergentes num defeito da §4 do relatório: **três linhas META que não existem** (nomes, tamanhos e mtimes inventados) — a prova mecânica por baixo estava certa (manifestos antes/depois byte-idênticos: 371 linhas = 368 por SHA-256 integral + 3 META, 49.473 B, `eb36c42c…`). Descarga: a **`ERRATA-PKG-2.md`** (7.102 B, `53aaf8fb…`) declara as linhas da §4 **NÃO-CITÁVEIS** e inscreve as verdadeiras (a citação da matéria da §4 passa a «RELATORIO-PKG-2 + ERRATA-PKG-2»):

- `TripoSG/image_encoder_dinov2/model.safetensors` — 1.217.522.888 B · mtime_ns 1793702935631229264
- `TripoSG/transformer/diffusion_pytorch_model.safetensors` — 5.758.280.104 B · mtime_ns 1793702888135228347
- `TripoSG/vae/diffusion_pytorch_model.safetensors` — 970.685.468 B · mtime_ns 1793702969153229911

**C-2 descarregada por inscrição expressa do registador:** o fundamento do estado «não exercitado» de T-C2-3 (ΔIoU) fica admitido com efeito de fecho — o adaptador malha→máscara é entregável do PKG-3; no fecho do PKG-3 o estado terá de ser exercitado ou re-fundamentado. **D-2 descarregada por declaração expressa:** a cadeia citável do PKG-2 é a de **dois termos** («PACOTE-MELHORIA-EXECUCAO + ERRATA-PACOTE-MELHORIA»); a forma de três termos da errata-da-errata vincula só matéria do PKG-1. **PKG-2 FECHADO**, sem nova bateria. Acto principal no índice do tribunal, **§31**.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Motor Próprio: PKG-3 FECHADO — ΔIoU exercitado e condição C-1 corrigida e confirmada

O **PKG-3** (runner, painel e grelha) fechou. Entrega: `RELATORIO-PKG-3.md` (24.691 B, `bd96df7f…`) — corrida sintética completa com **stub declarado** (Entrada do PKG-1 → runner → Saída do PKG-2), adaptador malha→máscara, painel CE-5 de 24 campos e grelha R-1; bateria: controlo **8/8 verde**, mutantes **8/8 vermelhos no alvo**; CR-2 provada (manifestos `eb36c42c…`, idênticos aos do fecho do PKG-2). **ΔIoU de T-C2-3 EXERCITADO** — a sede transitada do PKG-2 fica descarregada **por exercício**: par de diferença conhecida com IoU 0,7500 e **ΔIoU 0,2500 exacto** nas três implementações da pilha D-H0; par idêntico com ΔIoU = 0. Julgamentos: **Regras PRONTO, sem condições** (`b84cddef…`) — primeiro fecho limpo nesta lente nesta linhagem; **Método PRONTO COM RESSALVAS** (`b44d2787…`), condição única **C-1 [MENOR]** (a fase do registo de falha saía «corrida» para `InstrumentacaoAusente`, classe de pré-voo).

A ronda de correcção (`RELATORIO-CORRECCAO-PKG-3.md`, 8.530 B, `627c19a0…`) corrigiu o runner (`1e5ce78d…`) e a bateria (`41b61d81…`; mutante novo MD5 vermelho exactamente na afirmação nova): re-corrida com controlo 8/8 e mutantes **9/9**; a confirmação (`JULGAMENTO-CORRECCAO-PKG-3-METODO.md`, 8.446 B, `38e3a614…`) é **CONFIRMA A DESCARGA**, com a observação O-1 inscrita como extensão: a forma conjunta **«RELATORIO-PKG-3 + RELATORIO-CORRECCAO-PKG-3»** cobre também as linhas de prosa de `painel.json` (`5ca099db…`) e `relatorio_limpa.json` (`ec7f5009…`) da §1 do relatório julgado. **PKG-3 FECHADO.** Transita como não exercitado: corrida real = MP-T1 (fila do PC, atrás do T-COR-4, CE-6); inscrição formal da grelha R-1 = fecho da MP-T1; campo (iii) da saída; rembg real; adaptador em malhas reais. Acto principal no índice do tribunal, **§32**.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Motor Próprio: PKG-4 FECHADO — duas rondas de correcção confirmadas

O **PKG-4** (perfis como configuração) fechou. Entrega: `RELATORIO-PKG-4.md` (14.616 B, `366b79de…`) — 8 ficheiros de perfil com exactamente os **11 campos** do esquema C-8; `perfis.py` com registo fechado de nomes e `perfil_oficial` como único perfil-omissão; bateria T-P-1 (omissões lidas por AST da cópia staged: **11/11 campos, 0 divergências**) + T-P-2 (**11/11**) + 5 mutantes vermelhos no alvo; CR-2 provada (manifestos `eb36c42c…`). Julgamentos **PRONTO COM RESSALVAS ×2**: Método (`bd2996e3…`) — **C-1** (valores não-finitos passavam: `guidance_scale: Infinity` validava) e **C-2** (buraco de cobertura no caminho «ficheiro ilegível»), mais a observação O-1 (partilha de objectos-lista em `validar_perfil` — viaja para a integração da MP-T1); Regras (`81e0e783…`) — **C-1 documental** (a decisão 1 dizia que o eixo de experiência vive no `REGISTO`; cada entrada tem só `{"omissao": bool}`).

**Ronda 1** (`RELATORIO-CORRECCAO-PKG-4.md`, 16.568 B, `97a09b21…`): guarda de finitude, casos novos t2i/t2j/t2k e mutantes MP5/MP6 vermelhos no alvo; re-corrida T-P-2 **14/14**, mutantes **7/7**; a C-1 de Regras descarregou-se por **declaração expressa** («o registo guarda nome e estatuto de omissão; o eixo vive no nome do perfil»). Confirmações: Método (`5cd6af98…`) **CONFIRMA** C-1/C-2 mas levanta condição nova **C-3** — a guarda chamava `math.isfinite` também sobre `int` e um inteiro gigante (>~309 dígitos) rebentava com `OverflowError` cru, classe que o julgado aceitava; Regras (`c95a67e6…`) **CONFIRMA** a descarga documental, com **O-1**: ficam inscritas **duas extensões** da forma conjunta «RELATORIO-PKG-4 + RELATORIO-CORRECCAO-PKG-4» — à **decisão 1** e à **frase do fecho** do relatório julgado (§7, linhas 238–241). **Ronda 2** (`RELATORIO-CORRECCAO-2-PKG-4.md`, 14.051 B, `f7995871…`): `int` não-bool é finito por construção e não passa por `isfinite`; `perfis.py` final 9.394 B (`5923e9e3…`); caso novo t2l vermelho contra a forma da ronda 1 com o `OverflowError` exacto; re-corrida T-P-2 **15/15**, mutantes 7/7; confirmação (`a434d879…`) **CONFIRMA A DESCARGA** da C-3 — e fica inscrita a forma conjunta de **três termos** «RELATORIO-PKG-4 + RELATORIO-CORRECCAO-PKG-4 + RELATORIO-CORRECCAO-2-PKG-4» para as linhas de `perfis.py`/`bateria.py`/`resultados.json` da §1 do julgado. **PKG-4 FECHADO.** Transita: corrida real com qualquer perfil = MP-T1 (atrás do T-COR-4, CE-6); adopção de perfis = MP-T2 sob R-4; integração do runner ao registo = MP-T1; utilidade de determinismo/seed = **PKG-5**.

**Nota de estado do índice (para o próximo gémeo):** o índice do tribunal vai em **§§1–33** (300.240 B, SHA-256 `1ff45a0c…`); a **§34 ainda não existe** — o fecho do **PKG-5 está em correcção**; o seu gémeo escreve-se quando a §34 for inscrita no índice. Com esta entrada, `docs/REGISTRO.md` volta a acompanhar o índice por inteiro.

- I0007 (CM-000009), 2026-11-03.

---

## 2026-11-03 — Tribunal P3: P-00/V3 COMPLETADA — acto de completamento lavrado (condições (4)/(5) descarregadas)

As duas condições que a publicação da matriz P-00/V3 deixara pendentes — (4) lateralidade a três leitores e (5) Anexo S — foram **exercitadas e descarregadas**. Exercício: `RELATORIO-COMPLETAMENTO-P00-V3.md` (26.740 B, `ef612ab8…`) — três leitores independentes leram às cegas as 28 células de lateralidade e um medidor único correu o Anexo S; a coordenação recomputou tudo (39 valores, 0 divergências; corpus 12/12); face à divergência medida numa célula, a missão aplicou o ramo pré-registado **STOP** e não propôs adenda. Julgamentos ×2: **Regras** (`81549e15…`) = relatório CONFORME, acto lavrável na forma exacta do seu §7 sob C-R1…C-R4 (a condição (4) é **por sujeito**); **Método** (`40485598…`) = CONFIRMADO na substância, com **C-1 [MAIOR]** (o limiar de `centro` não está definido na letra governante), C-2 (a disputa imprime-se por inteiro), C-3/C-4. O acto: **`ADENDA-COMPLETAMENTO-P00-V3.md`** (16.191 B, `e214a0cb…`; corpo 15.732 B, `09eb67e9…`) — **adenda à matriz** `P00-V3-MATRIZ.md` (`f048730a…`, byte-idêntica, reconferida — não é matriz nova nem a edita), lavrada ao abrigo do §3 do acto de publicação (`741287e0…`).

**(4) descarregada por sujeito, em três formas distintas.** **Orc — forma certificante:** 20/20 células iguais ao registo V2 (10 informativas unânimes + 10 convencionadas coincidentes). **Capríleo — forma exercitada-coincidente:** 4/4 células coincidentes com o registo, sem predicar unanimidade. **Besta — só a forma impressa de E-V3-5:** frente {`centro`, `direita`, `direita`} «em disputa (2–1)», maioria `direita` = registo V2 (confirma por maioria; **não certifica**); costas {`centro`, `esquerda`, `centro`} «em disputa (2–1)», maioria `centro` **contra** o registo V2 `esquerda`; linha do par F×B «não certificada na célula cabeça»; (b2) «não atribuído»; **a palavra «certificada» fica barrada para a lateralidade desse par em qualquer citação**, e as duas células lêem-se a jusante como sem testemunho. A disputa imprime-se por inteiro no acto (C-2); matriz e registo V2 não foram corrigidos.

**(5) descarregada, com as respostas escritas das duas lentes (C-R1)** — inscritas no acto uma a uma, **sem as fundir**: **Regras** rejeita S-ORC-1…4 e S-CAP-1…4 como equivalentes a sinal e **aceita S-BES-1 como evidência que viaja com PN-09** (precedente da série V2); **Método** rejeita **as 9** como sinal, S-BES-1 incluída (ambiguidade já registada na série V2; fica como registo). Nenhuma suspeita fica por responder.

**Cláusula de citação nova (C-R4):** a antiga («publicada, não certificada — condições (4)/(5) de §6.1-V3 pendentes») **expira** e é substituída por: «**matriz P-00 publicada sob a régua D-H0 V3 certificada (acto de publicação de 2026-11-03), com completamento lavrado em 2026-11-03 — (4) descarregada: Orc e Capríleo na forma certificante; Besta na forma impressa de E-V3-5 (par F×B não certificado na célula cabeça); (5) descarregada com respostas escritas — sob a Adenda de Uso V3-ATAQUE-01 (julgamento da campanha de ataque, 2026-11-03)**». A cláusula antiga **não se apaga** do acto de publicação (época fechada). A restrição de uso do §3 do acto de publicação **dissolve-se**, **excepto** qualquer uso dependente das células Besta/cabeça, que permanecem sem testemunho; a Adenda de Uso V3-ATAQUE-01 continua em vigor (U-1…U-6).

**Declarações expressas (C-R2) e dívida:** este completamento **NÃO é** a revisão de calibração de §5.4 — o contador de escalações **permanece 1** e a revisão continua armada. **PN-09 inalterado:** a Besta continua INDETERMINADO e fora dos braços medidos; a disputa e a S-BES-1 arquivam-se como **evidência PN-09**; re-entrada só por REF-01. **Dívida nomeada D-COMP-1** (= C-1 [MAIOR] de Método): o limiar de `centro` não está definido na letra governante (sem banda, sem eixo, sem fracção); define-se em sede de desenho (errata/ciclo V4) **antes** de qualquer nova corrida a três leitores — **a célula não se re-corre para a resolver por repetição**. Acto principal no índice do tribunal, **§34**.

**Nota de estado do índice (para o próximo gémeo):** o índice do tribunal vai em **§§1–34** (306.811 B, SHA-256 `e84cdae4…`); a **§35 ainda não existe** — será o **fecho do PKG-5** (Motor Próprio); o seu gémeo escreve-se quando a §35 for inscrita no índice. Com esta entrada, `docs/REGISTRO.md` volta a acompanhar o índice por inteiro.

- I0005 (CM-000009), 2026-11-03.
