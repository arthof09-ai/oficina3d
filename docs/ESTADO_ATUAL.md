# ESTADO ATUAL - Oficina 3D

**Atualizado:** 01/11/2026, ~01:00 (Muse, CM-000009, apos a Prova C completa e o QUAL-01)
**Fase:** 1 - reconstrucao endurecida. **TODOS os itens executados; aguardando a auditoria final do Critico (a 3a) para o carimbo de PRONTA da Fase 1.** A Fase 2 (textura/cor) NAO comecou: depende do estudo das cartas (QUAL-02) e da decisao de desenho.

## O que esta provado (com evidencia)

- Ambiente, motores e modelos instalados pelo manifesto, com SHA-256 (itens 1-2), e do zero so com o GitHub (rodada R4 - independencia das referencias, DONO-02).
- Worker como servico (tarefa Oficina3D_Worker), web no ar (Oficina3D_Web, http://127.0.0.1:8765), MCP com 9 ferramentas por stdio e por HTTP com token (401 sem ele). Paridade web x MCP provada.
- Os 5 motores com GLB real gerado; refino de ponta a ponta.
- **Prova C COMPLETA (item 3 da definicao de pronta):** Orc, Besta Cristalina e Caprileo, cada um em hunyuan-mv-turbo (4 vistas) e hunyuan-mini-turbo (1 vista), sementes 7 e 42 + repeticao da 7: **determinismo byte-identico nos 3 personagens e nos 2 motores** (sha256 iguais nas repeticoes), forma <= 41,4 s, VRAM <= 6.435 MB, GLB final = 49.750 triangulos em todos. As imagens da Besta e do Caprileo vieram do Drive (indice da auditoria do Codex, relatorio de continuidade v002), com sha256 conferido arquivo a arquivo, e estao em app\testes\dourado\imagens (gitignore: arte do RPG nao vai ao repo publico).
- Rodadas de endurecimento R1-R4 concluidas (ver REGISTRO): restarts do worker explicados, arquivos no Drive, instalacao do zero, travas e retomada de orfao provadas, fila longa 10/10.
- **Perfis de qualidade QUAL-01 NO AR e medidos** (oficina3d/qualidades.py, --qualidade na CLI, opcoes.qualidade em todos os canais): Bronze 24.874 tris/1.250 KB, Prata 49.750/2.332, Ouro 149.250/6.188, Ouro Negro 298.500/10.703, Lenario 497.500/17.431 (forma do Lenario: 1.209.599 tris em 157,2 s; VRAM ~6,4 GB em todos os niveis). O Mestre aprovou visualmente o Orc Lenario ("ficou muito bom").
- Suite de testes: 218 testes OK no .venv_app (204 + 14 do QUAL-01), skipped=1.

## Definicao de pronta da Fase 1 (docs/REVISAO_E_ROTEIRO.md)

Itens 1, 2, 4, 5 e 6 provados; item 3 (Prova C) COMPLETO nos 3 personagens; itens 7 (documentacao honesta e atual) e 8 (veredito do Critico) dependem da auditoria final em andamento.

## Decisoes recentes do Mestre (DECISOES.md)

QUAL-01 (niveis de qualidade), QUAL-02 (forma nao e o app pronto: textura/pintura e a proxima frente; estudar as cartas antes), ANIM-01 (animacao como funcao futura/opcional do app), MET-01 (Critico rigoroso personalizado em toda melhoria), MET-02 (trabalho continuo em segundo plano, agentes para qualidade), MET-03 (portao final: TRES Criticos senior independentes, baterias diferentes), ARMAZ-01 (o que nao esta em uso vai para o Drive; PC do cunhado enxuto), QUAL-03 (bateria de variancia + Critico visual caçando defeitos contra a referencia + retrabalho local como frente do backlog).

## Pendencias conhecidas

1. Auditoria final do Critico sobre a Fase 1 (em convocacao).
2. Bateria de variancia do Lenario (Orc sementes 42/1234/repeticao + Besta e Caprileo) rodando: mede diferenca de qualidade e custo entre execucoes.
3. Defeito visual achado pelo Mestre no Orc Lenario: o machado saiu com laminas multiplas/fundidas (a referencia tem lamina unica). Registrado como primeiro caso da frente de retrabalho local/Critico visual (QUAL-03).
4. Estudo das cartas + backlog de melhorias (QUAL-02) em andamento por agente pesquisador; desenho da Etapa COR sai dele.
5. Guardian do notebook: adiado pelo Mestre (sem o notebook agora).
