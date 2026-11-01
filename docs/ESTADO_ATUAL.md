# ESTADO ATUAL - Oficina 3D

**Atualizado:** 01/11/2026, ~04:30 (Muse, CM-000009, Etapa COR: T1-mecanismo executado - sintetico exato + Orc dourado com textura, determinismo provado, suite 233 OK; aguarda veredito do Critico senior; gargalo T5 medido: UV Smart UV cobre so 4,32% do quadrado)
**Fase 1 PRONTA** (veredito do Critico senior, auditoria no 3 + adendo, 01/11 ~01:10). O app hoje e o ESQUELETO (CORPO-01): a prioridade agora e CONSTRUIR o corpo que falta - Etapa COR (cor/textura) primeiro, depois retrabalho local e as demais frentes do backlog; testes validam cada parte nova quando ela nasce.

## O que esta provado (com evidencia)

- Ambiente, motores e modelos instalados pelo manifesto, com SHA-256 (itens 1-2), e do zero so com o GitHub (rodada R4 - independencia das referencias, DONO-02).
- Worker como servico (tarefa Oficina3D_Worker), web no ar (Oficina3D_Web, http://127.0.0.1:8765), MCP com 9 ferramentas por stdio e por HTTP com token (401 sem ele). Paridade web x MCP provada.
- Os 5 motores com GLB real gerado; refino de ponta a ponta.
- **Prova C COMPLETA (item 3 da definicao de pronta):** Orc, Besta Cristalina e Caprileo, cada um em hunyuan-mv-turbo (4 vistas) e hunyuan-mini-turbo (1 vista), sementes 7 e 42 + repeticao da 7: **determinismo byte-identico nos 3 personagens e nos 2 motores** (sha256 iguais nas repeticoes), forma <= 41,4 s, VRAM <= 6.435 MB, GLB final = 49.750 triangulos em todos. As imagens da Besta e do Caprileo vieram do Drive (indice da auditoria do Codex, relatorio de continuidade v002), com sha256 conferido arquivo a arquivo, e estao em app\testes\dourado\imagens (gitignore: arte do RPG nao vai ao repo publico).
- Rodadas de endurecimento R1-R4 concluidas (ver REGISTRO): restarts do worker explicados, arquivos no Drive, instalacao do zero, travas e retomada de orfao provadas, fila longa 10/10.
- **Perfis de qualidade QUAL-01 NO AR e medidos** (oficina3d/qualidades.py, --qualidade na CLI, opcoes.qualidade em todos os canais): Bronze 24.874 tris/1.250 KB, Prata 49.750/2.332, Ouro 149.250/6.188, Ouro Negro 298.500/10.703, Lenario 497.500/17.431 (forma do Lenario: 1.209.599 tris em 157,2 s; VRAM ~6,4 GB em todos os niveis). O Mestre aprovou visualmente o Orc Lenario ("ficou muito bom").
- Suite de testes: 233 testes OK no .venv_app (218 + 15 novos da Etapa COR), skipped=1.
- **T1-mecanismo (Etapa COR, 01/11 ~04:30, aguarda Critico):** `oficina3d/cor/` - projecao das vistas canonicas com peso por facing + oclusao por BVH + dilatacao, bake para textura 1024 e GLB com material. Sintetico: 4/4 cores exatas, IoU 1,0. Orc Prata dourado: textura SHA-256 93c14cc6..., GLB fe73cf88..., determinismo em 2 runs, IoU 0,72-0,79, cobertura direta 20,03% (resto por dilatacao). Limitacao medida: UV Smart UV do refino tem 8.098 ilhas e cobre 4,32% do quadrado (~1 texel/face) - a qualidade do Orc sai fragmentada; T5 (UV de qualidade) e o proximo gargalo. Integracao a fila de jobs pendente apos o veredito.

## Definicao de pronta da Fase 1 (docs/REVISAO_E_ROTEIRO.md)

Todos os 8 itens conferidos com evidencia pelo Critico (auditoria no 3 + adendo): **FASE 1 PRONTA**. O portao MET-03 (tres Criticos senior, baterias diferentes) acontece so no fim de TODAS as frentes, nao agora.

## Decisoes recentes do Mestre (DECISOES.md)

QUAL-01 (niveis de qualidade), QUAL-02 (forma nao e o app pronto: textura/pintura e a proxima frente; estudar as cartas antes), ANIM-01 (animacao como funcao futura/opcional do app), MET-01 (Critico rigoroso personalizado em toda melhoria), MET-02 (trabalho continuo em segundo plano, agentes para qualidade), MET-03 (portao final: TRES Criticos senior independentes, baterias diferentes), ARMAZ-01 (o que nao esta em uso vai para o Drive; PC do cunhado enxuto), QUAL-03 (bateria de variancia + Critico visual cacando defeitos contra a referencia + retrabalho local como frente do backlog). Diretrizes de 01/11 ~01:54-01:57: REF-01 (arsenal de referencias vivas para testes reais), APR-01 (autoaperfeicoamento: fluxograma + diario de licoes + antecipacao, com o Critico cada vez mais rigoroso), CORPO-01 (testes servem ao corpo: construir as partes que faltam, cor primeiro) e REG-01 (nunca confiar na memoria: o plano valido e o escrito nos documentos).

## Proximos passos (atualizado em 01/11/2026, por REG-01)

1. **Etapa COR (prioridade 1, CORPO-01):** T1-mecanismo executado e aguardando o Critico (ver REGISTRO 01/11 ~04:30). Proximos passos, em ordem: (a) veredito do Critico + correcoes; (b) T5 - UV de qualidade (o Smart UV atual cobre 4,32%: xatlas ou novos parametros Smart UV, com as metricas de UV como juiz); (c) integracao do `cor` como etapa opcional da fila de jobs; (d) T2 cor de vertice como rede de seguranca; (e) adversarial T1 item 6 (Besta em menor resolucao, vista faltante). T3 (Paint) continua como spike opcional, depois do T1 aprovado.
2. **REF-01 lote 1 FECHADO (Orc):** Critico Visual rodada 2 APROVOU as 3 vistas v2 (orc_tpose_v2, orc_costas_v2, orc_tresquartos_v2) em testes/referencias/ - D1/D2/D3/D10 fechados, nenhum S1/S2 restante; ressalvas registradas: D5 (S3, pele da T-pose mais clara - a frente canonica e a autoridade de tom de pele) e D15 (S4, palmas para a frente - convencao a explicitar nos proximos pedidos). Folha de angulos abandonada em favor de vistas avulsas. Proximo: lote 2 = Besta Cristalina; fila: Caprileo e o acervo do indice do Drive.
3. **Retrabalho local (QUAL-03):** caso inaugural = machado do Orc Lenario (laminas multiplas/fundidas; a referencia tem lamina unica) - rotas R1/R4 do estudo (secao 8).
4. **APR-01 (criado):** docs/APRENDIZADO_E_FLUXO.md - fluxograma geral, protocolo de antecipacao, diario de licoes e regra de escalada do Critico; atualizar a cada tranche (REG-01).
5. Guardian do notebook: adiado pelo Mestre (sem o notebook agora).
6. Portao final MET-03: so depois de TODAS as frentes concluidas.
