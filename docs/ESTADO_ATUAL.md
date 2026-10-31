# ESTADO ATUAL: Oficina 3D v2 (CUNHADO-PC)
**Atualizado em:** 31/10/2026, ~15:25 (horário do PC)
**Quem escreveu:** Muse (IA remota do Mestre), continuando a sessão do Claude Code local — que parou no limite de uso semanal (volta qui 05/11, 14:00). Auditoria completa da sessão em 31/10 ~15:10: tudo que o Claude relatou confere no PC, no GitHub e no Drive.

## Fase e passo
- **Fase 0 CONCLUÍDA.** Os itens que dependiam de tela foram resolvidos pelo Muse em 31/10: Drive em streaming (item 0.2/5 do plano), Windows Update pausado por 5 semanas (item 0.4) e as decisões do item 0.6 tomadas pelo Mestre (ver DECISOES: ZIP-01, RF-03 final, NET-01 final, USO-01 final). Medidas que faltavam coletadas (CUDA, SSD, rede) e `SAUDE_FASE0.json` reescrito — aceite da fase cumprido.
- **Fase 1, item 1 (código):** os 7 agentes (AG-02) terminaram de escrever; o código está no disco **sem revisão e sem commit**. Revisão + testes em andamento pelo Muse.
- Janela de trabalho: PC livre até domingo 01/11 à noite (USO-01 final).

## VERIFICADO
- Repositório **público** `https://github.com/arthof09-ai/oficina3d` (GIT-02), clonado em `C:\Users\txcga\RPG_Local\Oficina3D\app`. HEAD `c4296bc` = remoto.
- Pastas: `C:\Users\txcga\RPG_Local\Oficina3D\{app,motores,_cache,jobs,jobs_teste,locks}`.
- Contrato v1 em `app\docs\`; código recuperado da v1 em `app\docs\v1_recuperado\`.
- Drive em **streaming**: `G:\Meu Drive\RPG Assimilação\Oficina3D_v2\` com 7 subpastas; `REGISTRO\` com cópia dos docs. A pasta do Desktop segue como pasta de origem da sincronização (não mexida).
- Windows Update pausado até 05/12/2026 (conferido no registro do Windows).
- Medidas completas em `docs\SAUDE_FASE0.json`: RTX 4060 (CUDA UMD 13.3, ~7,0 GB VRAM livre), SSD NVMe 477 GB, C: com 70,1 GB livres, rede ~95 Mbps.
- **ZIP-01 executado:** PartCrafter e DetailGen3D zipados em `modelos_guardados\` (teste de integridade OK; MD5 da nuvem = MD5 local) e os originais locais apagados. TripoSG intocado (12,57 GB em `oficina3d_ia\`).

## EM ANDAMENTO: revisão do código dos 7 agentes (decisão AG-02 do Mestre)
Nenhum agente commitou. Estado conferido arquivo por arquivo pelo Muse:
| Agente | Arquivos | Estado |
|---|---|---|
| A | `oficina3d\config.py`, `job.py`; `testes\test_config.py`, `test_job.py` | completo |
| B | `instalacao\*` (manifesto, baixar_modelos.py, instalar.ps1/.cmd, env, patches, compat, requisitos) | falta `LISTA_INSTALACAO_FASE1.md` |
| C (núcleo) | `oficina3d\motores\*`, `worker.py`, `cli.py`; testes | faltam `test_worker.py` e `test_cli.py` |
| D (entrada) | `oficina3d\entrada\*`; teste | falta `test_entrada.py` |
| E (refino) | `oficina3d\refino\*`; `testes\test_refino.py` | completo |
| F (web+MCP) | `oficina3d\web\*`, `oficina3d\mcp\*`; testes; `docs\mcp_exemplo.json` | faltam `test_web.py` e `test_mcp.py` |
| G (robustez) | `oficina3d\travas.py`, `arquivar.py`, `saude.py`; `instalacao\tarefa_worker\*`; 3 testes | completo |

## PENDENTE
- Revisão: rodar os 7 testes existentes, corrigir quebras, decidir sobre os 5 testes que faltam e a LISTA do agente B; commit de checkpoint.
- Fase 1 item 1 (instalação): `uv` ainda ausente — instalar, `uv python install 3.10`, criar os venvs e instalar pelo manifesto (`instalacao\instalar.ps1`).
- Fase 1 item 2: clonar Hunyuan3D-2GP e TripoSR nos commits fixados, aplicar patches, baixar modelos com SHA.
- Fase 1 itens 3 a 6, na ordem do plano.

## Próximo comando exato
1. Rodar a suíte: `python -m pytest testes` (ou `python -m unittest discover -s testes`) na pasta `app`; registrar o resultado no REGISTRO.
2. Commit + push do checkpoint do código dos agentes; seguir para a instalação do `uv`.

## Processos rodando agora
- Nenhum agente do Claude (a sessão caiu com o limite). Quem executa agora é o Muse, por SSH, até o Mestre dizer o contrário ou o Claude voltar (qui 05/11).

## Bloqueios e perguntas ao Mestre
- Nenhuma. As 4 perguntas da versão anterior foram respondidas em 31/10 (ver DECISOES).
