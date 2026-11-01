# ESTADO ATUAL - Oficina 3D

**Atualizado:** 01/11/2026, ~10:30 (Muse, CM-000009, Etapa COR: integracao a fila EXECUTADA - job de prova Orc Prata concluido com cor (264,1 s, IoUs 0,72-0,79, textura SHA ebd744a9...); aguarda veredito do Critico; proximo: T2)
**Fase 1 PRONTA** (veredito do Critico senior, auditoria no 3 + adendo, 01/11 ~01:10). O app hoje e o ESQUELETO (CORPO-01): a prioridade agora e CONSTRUIR o corpo que falta - Etapa COR (cor/textura) primeiro, depois retrabalho local e as demais frentes do backlog; testes validam cada parte nova quando ela nasce.

## O que esta provado (com evidencia)

- Ambiente, motores e modelos instalados pelo manifesto, com SHA-256 (itens 1-2), e do zero so com o GitHub (rodada R4 - independencia das referencias, DONO-02).
- Worker como servico (tarefa Oficina3D_Worker), web no ar (Oficina3D_Web, http://127.0.0.1:8765), MCP com 9 ferramentas por stdio e por HTTP com token (401 sem ele). Paridade web x MCP provada.
- Os 5 motores com GLB real gerado; refino de ponta a ponta.
- **Prova C COMPLETA (item 3 da definicao de pronta):** Orc, Besta Cristalina e Caprileo, cada um em hunyuan-mv-turbo (4 vistas) e hunyuan-mini-turbo (1 vista), sementes 7 e 42 + repeticao da 7: **determinismo byte-identico nos 3 personagens e nos 2 motores** (sha256 iguais nas repeticoes), forma <= 41,4 s, VRAM <= 6.435 MB, GLB final = 49.750 triangulos em todos. As imagens da Besta e do Caprileo vieram do Drive (indice da auditoria do Codex, relatorio de continuidade v002), com sha256 conferido arquivo a arquivo, e estao em app\testes\dourado\imagens (gitignore: arte do RPG nao vai ao repo publico).
- Rodadas de endurecimento R1-R4 concluidas (ver REGISTRO): restarts do worker explicados, arquivos no Drive, instalacao do zero, travas e retomada de orfao provadas, fila longa 10/10.
- **Perfis de qualidade QUAL-01 NO AR e medidos** (oficina3d/qualidades.py, --qualidade na CLI, opcoes.qualidade em todos os canais): Bronze 24.874 tris/1.250 KB, Prata 49.750/2.332, Ouro 149.250/6.188, Ouro Negro 298.500/10.703, Lenario 497.500/17.431 (forma do Lenario: 1.209.599 tris em 157,2 s; VRAM ~6,4 GB em todos os niveis). O Mestre aprovou visualmente o Orc Lenario ("ficou muito bom").
- Suite de testes: 247 testes OK no .venv_app (240 do T1 + 4 da T5 + 3 novos da D-T5-1), skipped=1.
- **T1-mecanismo APROVADO pelo Critico senior (Etapa COR, 01/11 ~04:50, relatorio em docs/CRITICO-t1-mecanismo-relatorio.md):** `oficina3d/cor/` - projecao das vistas canonicas com peso por facing + oclusao por BVH + dilatacao, bake para textura 1024 e GLB com material. Sintetico: 4/4 cores exatas (o IoU 1,0 sintetico NAO prova silhueta - mascara solida; a prova valida e a cor). Orc Prata dourado: textura SHA-256 93c14cc6..., GLB fe73cf88..., determinismo re-provado com 2 artefatos guardados (detA/detB), IoU 0,72-0,79, cobertura direta 20,03% (resto por dilatacao). Limitacao medida e confirmada pelo Critico: UV Smart UV do refino tem 8.098 ilhas e cobre 4,32% do quadrado (~1 texel/face) - a qualidade do Orc sai fragmentada; T5 (UV de qualidade) e o proximo gargalo. Correcoes pos-veredito: D3, D4, D6 fechados; D8 parcial. Pendencias: D1 (resolve com T5), D2 (adversarial), D7 (costura com UV nova). Integracao a fila de jobs apos o T5.
- **T5 APROVADA pelo Critico senior como passo de UV (Etapa COR, 01/11 ~06:30, relatorio em docs/CRITICO-t5-relatorio.md):** `oficina3d/uv_xatlas.py` (trimesh + xatlas -> .npz) + `cor/_blender_uv_xatlas.py` (aplica a UV por loop no Blender, com guarda de ocupacao). Orc Prata: ocupacao 0,61398 (Smart UV: 0,03983), distorcao 0,08787 (Smart: 0,10051), 6.578 ilhas, 12,937 texels/face (Smart: 0,911), 0,33% das faces com <1 texel (Smart: 61,68%). Geometria PROVADA identica (49.750 faces, diferenca maxima de posicao 0,0); determinismo do passo xatlas PROVADO (3 reexecucoes, arrays bit a bit identicos); bake COR sobre a UV nova com IoUs identicos ao bake Smart UV e texels diretos 121.567 (antes 8.513), textura SHA-256 794ced3d..., GLB 7730405e... (modelo com UV: 3c3a73db...). A/B de previas confirma a melhora (fim das areas pretas e da mancha branca) e confirma que o torso segue em mosaico: D1 (fidelidade de detalhe) segue ABERTO, e o gargalo visivel agora e o alinhamento por silhueta + divergencia geometria-vs-arte. Pendencias S2 do Critico: D-T5-1 margem 1 px em 2048 (regua >=8 px) - obrigatoria antes do T1-completo; D-T5-2 guarda de ocupacao no script Blender - FECHADA nesta mesma tranche (prova nos dois sentidos: passa com 0,61398, falha com exit 3 e ValueError com 0,10). Anomalia do controle sem costuras EXPLICADA pelo Critico (importador glTF cria 0 costuras; limpar 0->0 e vacuo); coincidencia das 8.098 ilhas no Blender segue nao-explicada e nao afeta a T5.
- **D-T5-1 FECHADA (Etapa COR, 01/11, APROVADA pelo Critico senior - relatorio em docs/CRITICO-dt51-relatorio.md):** `oficina3d/uv_xatlas.py` com gutter real (padding 8 em 2048, padrao novo do `parametrizar`); Orc Prata: margem 9 px em 2048 no .npz e no GLB exportado (mesmo metodo), ocupacao 0,233 (antes 0,614), 4,92 texels/face em 1024 (antes 12,94; segue 5,4x acima do Smart UV), distorcao 0,0745, 6.578 ilhas; bake COR com IoUs identicos aos da T5 e determinismo ponta a ponta provado (3 SHAs identicos); max_cost 8 medido (+15% de densidade) e NAO adotado (muda o charting provado na T5). Veredito: margem cumprida por dois metodos (9 px linha/coluna, 10,0 px euclidiana); halo eliminado nos mips 512/256 (T5: 5.680 blocos mistos em 256); S3: nota de flip completada no docstring.


- **D2 + D7 FECHADOS (Etapa COR, 01/11, com verificacao independente -**
  **relatorios em docs/CRITICO-d2d7-relatorio.md e**
  **docs/CRITICO-d2d7-verificacao.md):** `oficina3d/cor/costura.py` -
  medicao de salto de cor costura x interna, com solda por posicao
  (obrigatoria para GLB) e distancia de cor por direcao. Besta com UV
  D-T5-1: D7 soldada - costura n=13.758, media 93,49, mediana 77,22,
  78,08% > 30; interna n=60.867, media 36,20, mediana 13,96; borda 0
  (malha fechada, 74.625 classificadas). D2: 512 px estavel (IoUs
  identicos, texels 0,2498 da base, sem_cor 0); sem costas degrada de
  fato as faces das costas (frame glTF, costas = -Z: alvo 28,23 /
  24,01% > 30 vs controle 7,05 / 5,86% a 0,5) e nao move as 3 vistas
  restantes (IoUs e faces pintadas identicos a base). A medicao
  original tinha dois erros achados pelo Critico (falta de solda;
  frame Blender aplicado a normais glTF) - corrigidos e republicados
  SEM novo bake (commit aa2758c), com previa flat/unlit (Emission) de
  regiao de costura. Suite: 252 testes OK, skipped=1. Pendencias
  restantes: S2-3 (troca esq/dir, bloqueia a textura base, nao D2/D7),
  S3-2, S4-2, D1 (fidelidade, segue ABERTA).

## Definicao de pronta da Fase 1 (docs/REVISAO_E_ROTEIRO.md)

Todos os 8 itens conferidos com evidencia pelo Critico (auditoria no 3 + adendo): **FASE 1 PRONTA**. O portao MET-03 (tres Criticos senior, baterias diferentes) acontece so no fim de TODAS as frentes, nao agora.

## Decisoes recentes do Mestre (DECISOES.md)

QUAL-01 (niveis de qualidade), QUAL-02 (forma nao e o app pronto: textura/pintura e a proxima frente; estudar as cartas antes), ANIM-01 (animacao como funcao futura/opcional do app), MET-01 (Critico rigoroso personalizado em toda melhoria), MET-02 (trabalho continuo em segundo plano, agentes para qualidade), MET-03 (portao final: TRES Criticos senior independentes, baterias diferentes), ARMAZ-01 (o que nao esta em uso vai para o Drive; PC do cunhado enxuto), QUAL-03 (bateria de variancia + Critico visual cacando defeitos contra a referencia + retrabalho local como frente do backlog). Diretrizes de 01/11 ~01:54-01:57: REF-01 (arsenal de referencias vivas para testes reais), APR-01 (autoaperfeicoamento: fluxograma + diario de licoes + antecipacao, com o Critico cada vez mais rigoroso), CORPO-01 (testes servem ao corpo: construir as partes que faltam, cor primeiro) e REG-01 (nunca confiar na memoria: o plano valido e o escrito nos documentos).

## Proximos passos (atualizado em 01/11/2026, por REG-01)

1. **Etapa COR (prioridade 1, CORPO-01):** T1-mecanismo FECHADO com aprovacao do Critico (ver REGISTRO 01/11 ~04:50); T5 FECHADA com aprovacao do Critico como passo de UV (ver REGISTRO 01/11 ~06:30). Proximos passos, em ordem: (a) D-T5-1 margem da UV - EXECUTADA (padding 8 em 2048; margem 9 px em 2048 no .npz e no GLB; ver REGISTRO 01/11); FECHADA com aprovacao do Critico (ver REGISTRO 01/11); (b) D2 + D7 - FECHADOS com verificacao independente (ver REGISTRO 01/11 ~09:00); (c) integracao do `cor` como etapa opcional da fila de jobs - EXECUTADA (codigo + testes + job de prova Orc Prata concluido; ver REGISTRO 01/11 ~10:30); o FECHAMENTO depende do veredito do Critico senior (nao autoaprovado); (d) T2 cor de vertice como rede de seguranca. T3 (Paint) continua como spike opcional, depois do T1-completo. Fidelidade de detalhe do Orc (D1) segue ABERTA (D2/D7 nao a julgam); S2-3 (suspeita de troca esquerda/direita nas imagens da Besta) segue ABERTA e bloqueia a textura base, nao D2/D7; previas Workbench nao servem como prova colorimetrica (D10: amostrar a textura).
2. **REF-01 lote 1 FECHADO (Orc):** Critico Visual rodada 2 APROVOU as 3 vistas v2 (orc_tpose_v2, orc_costas_v2, orc_tresquartos_v2) em testes/referencias/ - D1/D2/D3/D10 fechados, nenhum S1/S2 restante; ressalvas registradas: D5 (S3, pele da T-pose mais clara - a frente canonica e a autoridade de tom de pele) e D15 (S4, palmas para a frente - convencao a explicitar nos proximos pedidos). Folha de angulos abandonada em favor de vistas avulsas. **REF-01 lote 2 FECHADO (Besta Cristalina):** a rodada 1 do Critico reprovou a diag_esq (B1 SYM S2) e o topo (B2 DEF/MIS S2) e aprovou a diag_dir; o retrabalho v2 foi APROVADO na rodada 2 (docs/CRITICO-ref01-lote2-v2.md) - B1-B6 fechados por medida, autotestes do executor 8/8 confirmados; pendencias nomeadas: B7 (S3, diversidade angular do par de diagonais), B10 (S3, maos do topo em roseta), B11 (S3, tom do topo) e B9 (S4, margens). Conjunto final da Besta: 4 cardeais canonicos + diag_dir + diag_esq_v2 + topo_v2. Proximo sujeito da fila: Caprileo (lote 3); depois, as diagonais do Orc e a classificacao das bestas novas de 31/10.
3. **Retrabalho local (QUAL-03):** caso inaugural = machado do Orc Lenario (laminas multiplas/fundidas; a referencia tem lamina unica) - rotas R1/R4 do estudo (secao 8).
4. **APR-01 (criado):** docs/APRENDIZADO_E_FLUXO.md - fluxograma geral, protocolo de antecipacao, diario de licoes e regra de escalada do Critico; atualizar a cada tranche (REG-01).
5. Guardian do notebook: adiado pelo Mestre (sem o notebook agora).
6. Portao final MET-03: so depois de TODAS as frentes concluidas.
