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

## EM ANDAMENTO
- Agente A: `oficina3d\config.py` + `oficina3d\job.py` corrigidos (seção 6.5 do plano) + testes `testes\test_config.py`, `testes\test_job.py`.
- Agente B: `instalacao\manifesto_modelos.json`, `instalacao\baixar_modelos.py`, `instalacao\instalar.ps1`, `instalacao\env.ps1`/`env.cmd`, patch do TripoSR em `instalacao\patches\`. Só escreve; **não roda download nem instalação**.

## PENDENTE
- Item 0: Drive espelho → streaming; itens 0.3 a 0.6.
- Pausar Windows Update (cliques na tela).
- Velocidade de rede, tipo do SSD.
- Fase 1 itens 2 a 6 (dependem do Drive em streaming e de espaço).

## Próximo comando exato
1. Se os agentes terminaram: conferir os relatórios deles colados no `docs\REGISTRO.md`; se não estiverem lá, rodar `git -C C:\Users\txcga\RPG_Local\Oficina3D\app status` e revisar os arquivos novos.
2. Quando o Mestre disser "Drive pronto": `Get-ChildItem "G:\Meu Drive\RPG Assimilação" | Select-Object Name` e seguir o item 0.3 do prompt de entrada.

## Processos rodando agora
- Agentes A e B (subagentes do Claude Code, sem PID próprio). Se a sessão cair, eles morrem: refazer pela descrição acima, partindo do que estiver no disco (`git status`).

## Bloqueios e perguntas ao Mestre
1. Trocar o Drive para streaming (cliques). 2. Pausar Windows Update (cliques). 3. Posso zipar PartCrafter + DetailGen3D para `modelos_guardados\` e apagar o local (~13,6 GB)? 4. RF-03 / Tailscale / horários da GPU (padrões em uso).

## Espaço livre no C:
46,2 GB (31/10/2026, 12:10).
