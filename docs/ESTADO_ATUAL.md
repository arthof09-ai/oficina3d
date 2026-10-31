# ESTADO ATUAL: Oficina 3D v2 (CUNHADO-PC)
**Atualizado em:** 31/10/2026, ~12:20 (horário do PC)
**Quem escreveu:** Claude Code no CUNHADO-PC (hostname `PCdaNasa`)

## Fase e passo
- Fase 0, item 0 **bloqueado** (troca do Drive para streaming precisa de cliques na tela).
- Em paralelo, Fase 1 item 1 (código, sem download): 2 agentes rodando (ver "Processos").

## VERIFICADO
- Repositório **público** `https://github.com/arthof09-ai/oficina3d`, clonado em `C:\Users\txcga\RPG_Local\Oficina3D\app`. Histórico refeito sem e-mail pessoal (commit `e16460d`). `gh api repos/arthof09-ai/oficina3d --jq .visibility` → `public`.
- Pastas: `C:\Users\txcga\RPG_Local\Oficina3D\{app,motores,_cache,jobs,jobs_teste,locks}`.
- Contrato v1 em `app\docs\`; código recuperado da v1 em `app\docs\v1_recuperado\`.
- Drive (ainda espelho): `C:\Users\txcga\Desktop\RPG Assimilação\RPG Assimilação\Oficina3D_v2\` com 7 subpastas; `REGISTRO\` com cópia dos docs.
- Medidas iniciais em `docs\SAUDE_FASE0.json`.

## EM ANDAMENTO: 7 agentes (decisão AG-02 do Mestre). Nenhum commita; nenhum baixa/instala.
| Agente | Dono dos arquivos (dentro de `app\`) | Fonte |
|---|---|---|
| A | `oficina3d\__init__.py`, `config.py`, `job.py`; `testes\test_config.py`, `test_job.py` | plano 6.5 + v1_recuperado |
| B | `instalacao\*` (manifesto_modelos.json, baixar_modelos.py, instalar.ps1/.cmd, env.ps1/.cmd, patches\, compat\, LISTA_INSTALACAO_FASE1.md) | manifesto + transcrição |
| C (núcleo) | `oficina3d\motores\*`, `worker.py`, `cli.py`; `testes\test_motores.py`, `test_worker.py`, `test_cli.py` | transcrição (agente núcleo da v1) |
| D (entrada) | `oficina3d\entrada\*`; `testes\test_entrada.py` | transcrição (agente entrada) |
| E (refino) | `oficina3d\refino\*`; `testes\test_refino.py` | transcrição (agente refino) |
| F (web+MCP) | `oficina3d\web\*`, `oficina3d\mcp\*`; `testes\test_web.py`, `test_mcp.py` | transcrição (agente web) + servidor_mcp.py v1 + plano 6.4/6.5 |
| G (robustez) | `oficina3d\travas.py` (gpu.lock, worker.lock), `oficina3d\arquivar.py`, `oficina3d\saude.py`; `instalacao\tarefa_worker\*`; `testes\test_travas.py`, `test_arquivar.py`, `test_saude.py` | plano 5.1, 6.2, Fase 1 item 4 |
Se a sessão cair: os agentes morrem. Rodar `git -C C:\Users\txcga\RPG_Local\Oficina3D\app status`, ver que arquivos de cada dono existem e reabrir só os que faltam, com a mesma descrição.

## PENDENTE
- Item 0: Drive espelho → streaming; itens 0.3 a 0.6.
- Pausar Windows Update (cliques na tela).
- Velocidade de rede, tipo do SSD.
- Fase 1 itens 2 a 6 (dependem do Drive em streaming e de espaço).

## Próximo comando exato
1. Se os agentes terminaram: conferir os relatórios deles colados no `docs\REGISTRO.md`; se não estiverem lá, rodar `git -C C:\Users\txcga\RPG_Local\Oficina3D\app status` e revisar os arquivos novos.
2. Quando o Mestre disser "Drive pronto": `Get-ChildItem "G:\Meu Drive\RPG Assimilação" | Select-Object Name` e seguir o item 0.3 do prompt de entrada.

## Processos rodando agora
- Agentes A a G (subagentes do Claude Code, sem PID próprio; ver tabela acima). Se a sessão cair, eles morrem: refazer pela descrição acima, partindo do que estiver no disco (`git status`).

## Bloqueios e perguntas ao Mestre
1. Trocar o Drive para streaming (cliques). 2. Pausar Windows Update (cliques). 3. Posso zipar PartCrafter + DetailGen3D para `modelos_guardados\` e apagar o local (~13,6 GB)? 4. RF-03 / Tailscale / horários da GPU (padrões em uso).

## Espaço livre no C:
46,2 GB (31/10/2026, 12:10).
