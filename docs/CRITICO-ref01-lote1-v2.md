# CRITICO VISUAL SENIOR - REF-01, lote 1 v2 (retrabalho): relatorio da RODADA 2

**Data:** 01/11/2026. **Papel:** Critico Visual senior, independente e imparcial (nao executou nada deste lote; julga o trabalho do executor). **Protocolo:** ESTUDO_MELHORIAS.md secao 7 (taxonomia EXT/MIS/FUS/DEF/SIL/SYM/FACE/PRP/TXT; severidades S1-S4) + bateria da secao 6 de APRENDIZADO_E_FLUXO.md adaptada as vistas avulsas + verificacoes novas desta rodada (escalada APR-01, secao 3 abaixo).

**Alvos julgados** (copias locais; SHA-256 conferidos e IDENTICOS aos informados na tarefa):
- `orc_tpose_v2.png` - 1328x1904, RGB, sha256 `26da22e25f5f87f8e4ea29df21533d89e84c7681bc30b7fa3beb74199f61e34f`
- `orc_costas_v2.png` - 1328x1904, RGB, sha256 `09890d74d6a43567c481de4bfb5395605fb3e03b732014292f810caf17a41362`
- `orc_tresquartos_v2.png` - 1328x1904, RGB, sha256 `7c9d9465d142e678dd2cb0d455f19c51cef050eb2bdb10a05efa79de8022ad84`

**Fontes canonicas:** `fonte_orc_frente.png` (1280x1820 RGBA, sha256 `30c0f83d3ede10fd6f91db91a986e14b1217fd0c9773a793a082a8e1cc903b6c`) e `fonte_orc_costas.png` (1280x1820 RGBA, sha256 `256c8a2fe22588f3895ec8b5fb08419e30fe25e6ff8b57d5fe814462a97fd20f`).

**Contexto da rodada:** a folha de angulos foi ABANDONADA por decisao registrada na rodada 1; o conjunto v2 e de vistas avulsas (T-pose + costas + 3/4). O retrabalho exigido na rodada 1 era: (a) bracos a 90 graus, (b) dedos separados e contaveis, (c) massa de pele no ombro direito do personagem, (d) costas avulsa com ancoras de lado explicitas. Os zooms e o script de medicao desta rodada estao em `hidden_files/critico-v2/` (`analise_v2.py`, zooms `tpose_v2_*`, `costas_v2_*`, `tresquartos_v2_*`).

---

## Veredito do lote

**LOTE APROVADO no criterio de aceite** (nenhum defeito S1/S2 de fidelidade). As tres vistas v2 corrigem todos os defeitos decisivos da rodada 1 (D1, D7, D10) e passam na bateria completa. Restam pendencias nomeadas S3/S4 (D5, D4, D14, D15) que NAO bloqueiam o uso como insumo de modelagem, mas devem ficar registradas — sobretudo D5: **para TOM DE PELE, a autoridade continua sendo a frente canonica, nao a T-pose v2** (pele mais clara). A palavra artistica final e do Mestre; este veredito e o tecnico.

| Imagem | Veredito | Pode entrar no arsenal de referencias como insumo de modelagem? |
|---|---|---|
| `orc_tpose_v2.png` | **APROVADA** | **SIM** — com as ressalvas D5 (tom de pele mais claro; usar a frente canonica como autoridade de cor) e D15 (palmas para a frente, nao para baixo) |
| `orc_costas_v2.png` | **APROVADA** | **SIM** — sem ressalva de lado: todas as ancoras conferem (secao 3c) |
| `orc_tresquartos_v2.png` | **APROVADA** | **SIM** — sem ressalva; todas as ancoras conferem (secao 3c) |

Nao ha especificacao de retrabalho v3 porque nao ha defeito S1/S2 a corrigir. O que resta e pendencia nomeada (secao 5), nao retrabalho bloqueante.

## 1. Bateria da secao 6 adaptada as 3 vistas avulsas, item a item

**1. Mesmo personagem? - PASSA.** Rosto da T-pose v2 (zoom `tpose_v2_rosto.png`): testa pesada, 3 listras vermelhas verticais na testa, marcas nas bochechas, olhos vermelhos, 2 presas inferiores grandes + dentes menores, cavanhaque preto pontudo, orelhas pontudas com argolas nos DOIS lados, coque alto com faixa vermelha/dourada, contas de cobre e pendente de osso nos dreads — tudo presente, simetrico e no lado certo (FACE: OK). Pele verde-oliva, ombros muito largos, tronco massivo, maos grandes — proporcoes da fonte, nas 3 vistas. O defeito de proporcao da v1 (D6, maos pequenas) sumiu: as maos v2 sao grandes, como na fonte.

**2. Caracteristicas preservadas? - PASSA.** Inventario conferido vista por vista contra as fontes: cabeca de lobo no ombro ESQUERDO do personagem (frente e 3/4: a direita de quem olha; costas: a esquerda de quem olha — correto nos tres casos); ombreira de espinhos no braco DIREITO do personagem nas 3 vistas; bracelete de espinhos no antebraco direito; bracelete de placas no antebraco esquerdo; colar de presas com caveira; alca diagonal de couro com fivelas (frente, costas e 3/4); cinto completo item a item (zoom `tpose_v2_cintura_pernas.png`: placa losango, fivela, 2 caveirinhas, caveira grande + presa longa no quadril esquerdo do personagem, aneis + gancho de osso, tubo de pergaminho no quadril direito, adaga); saiote de pele/couro com paineis de tecido vermelho; capa de pele clara nos dois ombros caindo pelas costas; grevas e botas de metal com espinhos e acabamento de pele. **Nenhuma bolsinha inventada em nenhuma das 3 vistas** (zooms de cinto da T-pose, das costas e do 3/4 conferidos). Nenhuma arma nova, nenhuma cor trocada (medido — secao 2).

**3. T-pose correta? - PASSA (com a ressalva D15).** Bracos MEDIDOS (regressao sobre o eixo medio da silhueta, metodo herdado da rodada 1): **3,18 graus abaixo da horizontal no braco esquerdo de quem olha e 1,88 grau no direito** — contra ~30 graus da v1. A exigencia (a) do retrabalho ("bracos a 90 graus, verificados por medicao") esta cumprida: 2-3 graus e T-pose para qualquer efeito pratico de modelagem. Extensao dos bracos perfeitamente simetrica: mao esquerda alcanca x=11, mao direita x=1317, centro da imagem x=664 — 653 px de cada lado. Dedos: **contados, nao estimados** — 5 digitos (polegar + 4 dedos) em cada mao, todos separados, com linhas de articulacao (zooms `tpose_v2_mao_esq_viewer.png` e `tpose_v2_mao_dir_viewer.png`; detalhe na secao 3a). Ressalva: as palmas estao voltadas PARA A FRENTE (para quem olha), nao para baixo — D15, DEF S4, sem impacto de modelagem (a geometria da mao esta toda legivel).

**4. Pernas como pedido? - PASSA COM RESSALVA S4 (D4 reduzido).** Pernas retas, um pouco afastadas, pes para a frente, sem fusao perna-perna. O painel central de tecido vermelho ainda desce PELA FRENTE entre as pernas (ate meia-canela), mas as faces internas das coxas estao legiveis e separadas — e peca do saiote, nao fusao. D4 cai de S3 para S4.

**5. Enquadramento e fundo - PASSA.** Corpo inteiro com margem nas 3 vistas; fundo cinza-claro uniforme; sem cenario, sem texto, sem sombra projetada forte. Observacoes S4 (as mesmas da rodada 1, sem mudanca): margem lateral de apenas 11 px na T-pose (bracos quase tocam a borda — nada cortado, dedos completos); geradas em RGB sem canal alfa, fontes em RGBA com transparencia — para insumo multivista o fundo uniforme basta.

**6. Consistencia cruzada ENTRE as 3 vistas v2 - PASSA.** Esta e a verificacao que a rodada 1 inaugurou, e a v2 a cumpre: lobo sempre no ombro esquerdo do personagem; ombreira de espinhos sempre no braco direito; braceletes sempre nos antebracos certos; inventario do cinto identico nas 3 vistas (mesma posicao relativa de caveira grande/presa, aneis/gancho, pergaminho, adaga); listras vermelhas e dreads coerentes; paleta coerente (medido — secao 2). A discordancia interna da v1 (T-pose sem a massa do ombro, folha com a massa) NAO se repete: a massa de pele do ombro direito do personagem esta presente na T-pose v2 (zoom `tpose_v2_ombro_dir_personagem.png`), na 3/4 e nas costas.

**7. Integridade tecnica - PASSA.** PNGs validos; dimensoes 1328x1904 nas 3 vistas; SHA-256 conferidos e identicos aos informados na tarefa; fundo uniforme; arquivos fora do repo por natureza (copias locais de trabalho do Critico, nao do projeto — nenhum commit feito por este Critico, conforme a tarefa).

**8. Classificacao de defeitos** - tabela completa na secao 4, na taxonomia do protocolo.

## 2. Verificacao herdada da rodada 1

**Amostragem quantitativa de paleta** (mesmo metodo da rodada 1: mediana RGB por classe de cor; acrescido de amostragem por REGIAO — peito/abdome e painel vermelho do saiote — para isolar o tom de pele da contaminacao por pele de lobo):

| Classe / regiao | Fonte | T-pose v2 | 3/4 v2 | Costas v2 (fonte costas) |
|---|---|---|---|---|
| Pele, imagem inteira | (133,113,60) | (156,134,76) — soma dos deltas = 60 | (129,111,60) — delta = 6 | (97,87,44) contra (125,104,50) — delta = 45* |
| Pele, regiao do peito | (133,112,59) | (151,129,73) — delta = 49 | (138,118,64) — delta = 16 | braco: (128,118,64) contra (143,122,63) — delta = 20 |
| Vermelho, painel do saiote | (100,22,18) | (107,28,24) — delta = 19 | (109,26,22) — delta = 17 | (86,18,14) contra (87,15,12) — delta = 6 |

\* A classe "pele" na imagem inteira das costas inclui pouco peito/braco e muito sombreado; o numero por regiao (braco, delta 20) e o mais confiavel para as costas.
**Leitura:** o tecido vermelho e FIEL nas 3 vistas (deltas 6-19). A pele esta fiel na 3/4 (delta 16) e nas costas (delta 20 por regiao), mas **a T-pose v2 tem a pele visivelmente mais clara/amarelada (delta 49-60)** — pior que o delta 41 da v1, nao melhor. E o D5, que persiste como S3 (secao 4). A conclusao da rodada 1 se mantem: o desvio do lote e de TOM/TEXTURA, nao de desenho nem de inventario.

**Medicao geometrica da T-pose v2** (regressao sobre o eixo medio da silhueta, ~400 colunas por lado): braco esquerdo de quem olha 3,18 graus, braco direito 1,88 grau abaixo da horizontal (v1: 31,6/29,9 graus). D2 FECHADO.

## 3. VERIFICACOES NOVAS DESTA BATERIA (escalada APR-01 — novidades da rodada 2)

### 3a. Contagem de dedos por mao, com zoom, na T-pose v2
- **Mao esquerda de quem olha (braco direito do personagem)** — zoom `tpose_v2_mao_esq_viewer.png`: **5 digitos contados** — polegar em cima, separado; indicador, medio, anelar e minimo individualmente separados, cada um com linha de articulacao visivel e ponta arredondada propria. Nenhuma fusao.
- **Mao direita de quem olha (braco esquerdo do personagem)** — zoom `tpose_v2_mao_dir_viewer.png`: **5 digitos contados** — polegar em cima, separado; 4 dedos individualmente separados, com articulacoes marcadas. Nenhuma fusao.
- **Resultado: D3 FECHADO.** A exigencia (b) do retrabalho ("dedos individualmente separados e contaveis nas duas maos") esta cumprida com folga — a v2 nao so separa como articula os dedos. Aceite da v2 pedia D3 no maximo S4; o resultado e melhor que o teto: zero defeito de dedo.

### 3b. Simetria espelhada medida da silhueta da T-pose v2
- **IoU(mascara, mascara espelhada) = 0,809** (interseccao 541.904 px, uniao 669.650 px). O valor NAO e 1,0 nem deveria ser: o personagem e deliberadamente assimétrico (lobo num ombro, ombreira de espinhos no outro braco, inventario do cinto assimétrico) — um IoU proximo de 1,0 aqui seria ate suspeito (indicaria perda dos acessorios assimétricos).
- **O que importa e simetrico:** extensao dos bracos 653 px de cada lado do centro (x=11 contra x=1317, centro x=664); angulos dos bracos 3,18 contra 1,88 grau (diferenca de 1,3 grau); faixa dos bracos: extensao media esquerda 510 px contra direita 519 px do centro. Pernas: afastamento simetrico, pes para a frente nos dois lados.
- **Assimetrias residuais sao as legitimas do personagem** (lobo, ombreira, cinto), nao defeito de pose. **Resultado: PASSA.** Nenhum defeito de simetria de pose na v2 (a v1 tambem passava neste item; a medicao agora o prova em numero).

### 3c. Auditoria de ancoras de LADO, ancora por ancora, contra a fonte de costas

Regra de orientacao (a que a v1 violou): o lobo fica no ombro ESQUERDO do personagem; visto POR TRAS, o lado esquerdo do personagem aparece a ESQUERDA de quem olha; visto DE FRENTE ou em 3/4 frontal, aparece a DIREITA de quem olha.

**Costas v2 contra a fonte de costas:**

| Ancora | Fonte de costas (esperado) | Costas v2 (observado) | Veredito |
|---|---|---|---|
| Peca de lobo | Esquerda de quem olha (ombro esquerdo do personagem) | Cabeca de lobo a esquerda de quem olha, focinho apontando para a esquerda, orelhas no alto | **APROVADA** |
| Ombreira de espinhos | Direita de quem olha (braco direito do personagem) | Ombreira de espinhos no braco direito de quem olha, com espinhos | **APROVADA** |
| Bracelete de espinhos | Braco esquerdo de quem olha (antebraco direito do personagem) | Bracelete de espinhos no antebraco esquerdo de quem olha | **APROVADA** |
| Bracelete de placas | Braco direito de quem olha (antebraco esquerdo do personagem) | Bracelete de placas sobrepostas no antebraco direito de quem olha | **APROVADA** |
| Comprimento da capa | Desce abaixo dos joelhos, mais longa do lado esquerdo de quem olha | Massa de pele desce abaixo dos joelhos do lado esquerdo de quem olha, longa e espessa | **APROVADA** |
| Direcao dos pes | Os dois apontando para longe do observador | Zoom `costas_v2_pes.png`: as duas botas apontam para longe do observador, levemente para fora — calcanhares para quem olha, sem pe virado de lado | **APROVADA** |
| Alca diagonal | Cruzando a capa, com fivela | Alca de couro com fivela cruzando a capa, fivela ao centro | **APROVADA** |
| Ausencia de bolsinhas no cinto | Nenhuma (trofeus = caveiras, presas, correntes) | Zoom `costas_v2_cinto.png`: placa losango, fivela, presas, correntes, aneis, gancho, caveira grande + presa — **zero bolsinhas** | **APROVADA** |

**3/4 v2 contra a fonte de costas (lado) e a fonte de frente (inventario):**

| Ancora | Esperado (3/4 frontal) | 3/4 v2 (observado) | Veredito |
|---|---|---|---|
| Peca de lobo | Direita de quem olha (ombro esquerdo do personagem, visto de frente) | Cabeca de lobo a direita de quem olha, rosto em 3/4 | **APROVADA** |
| Ombreira de espinhos | Esquerda de quem olha (braco direito do personagem) | Ombreira de espinhos no braco esquerdo de quem olha | **APROVADA** |
| Bracelete de espinhos | Antebraco esquerdo de quem olha | Bracelete de espinhos no antebraco esquerdo de quem olha | **APROVADA** |
| Bracelete de placas | Antebraco direito de quem olha | Bracelete de placas no antebraco direito de quem olha | **APROVADA** |
| Comprimento da capa | Massa de pele atras, descendo alem da cintura | Capa volumosa atras dos ombros, caindo alem da cintura e ao lado das pernas | **APROVADA** |
| Direcao dos pes | Coerente com o giro do corpo (pe da frente apontado para a frente, pe de tras angulado) | Zoom `tresquartos_v2_pes.png`: bota esquerda de quem olha apontada para a frente, bota direita angulada para a direita — coerente com o 3/4 | **APROVADA** |
| Alca diagonal | Cruzando o peito, com fivelas | Alca com duas fivelas cruzando o peito | **APROVADA** |
| Ausencia de bolsinhas no cinto | Nenhuma | Zoom `tresquartos_v2_cinto.png`: inventario completo, **zero bolsinhas** | **APROVADA** |

**Resultado da 3c: 16/16 ancoras APROVADAS.** O erro D10 (espelhamento) esta morto nas duas vistas novas — a licao da rodada 1 foi aprendida pelo executor.

## 4. Tabela de defeitos D1-D14 atualizada + defeitos novos

| ID | Imagem | Codigo | Regiao | Sev. v1 | Estado v2 | Evidencia v2 |
|---|---|---|---|---|---|---|
| D1 | orc_tpose.png | MIS/DEF | ombro direito do personagem (massa de pele) | S2 | **FECHADO** | Zoom `tpose_v2_ombro_dir_personagem.png`: massa espessa de pele clara sobre o ombro, com a ombreira de espinhos abaixo — como na fonte |
| D2 | orc_tpose.png | DEF | bracos ~30 graus abaixo da horizontal | S3 | **FECHADO** | Regressao: 3,18 / 1,88 grau (secao 2) |
| D3 | orc_tpose.png | FUS | dedos parcialmente fundidos, nao contaveis | S3 | **FECHADO** | 5 + 5 digitos contados com zoom (secao 3a) |
| D4 | orc_tpose.png | DEF/FUS | tecido/pele da cintura entre as pernas | S3 | **REDUZIDO — S4** | Painel central ainda desce entre as pernas, mas as faces internas das coxas estao separadas e legiveis; e saiote, nao fusao |
| D5 | orc_tpose.png | TXT | pintura lisa, pele mais clara | S3 | **REDUZIDO, mantem S3** | Grao melhor que na v1, mas o tom de pele da T-pose segue claro (delta 49 no peito, 60 na imagem inteira); vermelho fiel (delta ≤19). Pendencia nomeada: usar a frente canonica como autoridade de cor |
| D6 | orc_tpose.png | PRP | conjunto menos massivo (maos menores) | S4 | **FECHADO** | Maos grandes como na fonte; massa do tronco e ombros conferem |
| D7 | orc_angulos.png | MIS | vista de costas AUSENTE da folha | S2 | **FECHADO** (por superacao) | Folha abandonada; costas v2 avulsa entregue e com 8/8 ancoras aprovadas |
| D8 | orc_angulos.png | DEF | perfil quase duplicado, orientacao ambigua | S3 | **FECHADO** (por superacao) | Folha abandonada; 3/4 v2 avulso substitui os perfis |
| D9 | orc_angulos.png | EXT | bolsinha na 4a figura da folha | S3 | **FECHADO** (por superacao) | Folha arquivada; zero bolsinhas nas 3 vistas v2 |
| D10 | orc_costas_ref.png | SYM | personagem INTEIRO espelhado | S2 | **FECHADO** | 8/8 ancoras de lado aprovadas nas costas v2; 8/8 no 3/4 v2 (secao 3c) |
| D11 | orc_costas_ref.png | EXT | 2 bolsinhas no cinto das costas | S3 | **FECHADO** | Zoom do cinto das costas v2: zero bolsinhas |
| D12 | orc_costas_ref.png | MIS | alca diagonal das costas ausente | S3 | **FECHADO** | Alca com fivela presente sobre a capa nas costas v2 |
| D13 | orc_costas_ref.png | DEF | capa curta/uniforme; pe direito virado de lado | S3 | **FECHADO** | Capa abaixo dos joelhos; zoom dos pes: os dois apontam para longe do observador |
| D14 | orc_costas_ref.png | TXT | padrao de pele repetitivo/em escamas | S4 | **REDUZIDO — S4** | Sem padrao repetitivo na v2; textura ainda mais lisa que a fonte, sem prejuizo de leitura |

**Defeitos NOVOS encontrados nesta rodada (mesma taxonomia):**

| ID | Imagem | Codigo | Regiao | Sev. | Evidencia | Estado |
|---|---|---|---|---|---|---|
| D15 | orc_tpose_v2.png | DEF | maos: palmas voltadas para a frente (para quem olha), nao para baixo | S4 | Zooms das duas maos: linhas da palma visiveis, polegar em cima — palma para o observador, nao para o chao | **ABERTO** (ressalva, nao bloqueia: a geometria das maos esta toda legivel e os dedos sao contaveis; registrar a convencao para os proximos lotes pedirem palmas para baixo explicitamente) |

Nenhum defeito novo S1/S2/S3 foi encontrado. O Critico procurou ativamente por: espelhamento residual, bolsinhas, fusoes de dedos/pernas, inventario trocado, capa curta, pes virados, rosto errado — e nao achou nenhum alem do D15 (S4).

## 5. Pendencias nomeadas (nao bloqueiam o uso)

1. **D5 (S3):** tom de pele da T-pose v2 mais claro/amarelado que a fonte (delta 49 no peito). Ao usar a T-pose como insumo de cor, corrigir o tom pela frente canonica. Nos proximos lotes, pedir explicitamente o tom verde-oliva da fonte.
2. **D15 (S4):** palmas da T-pose para a frente, nao para baixo. Registrar a convencao no pedido dos proximos lotes.
3. **D4/D14 (S4):** painel central do saiote entre as pernas; textura ainda mais lisa que a fonte. Cosmeticos, sem impacto de modelagem.

## 6. Registro da escalada APR-01 desta rodada

Verificacoes ADICIONADAS pela rodada 2 (a rodada 1 nao tinha): **(a)** contagem de dedos por mao, com zoom, numero contado em cada mao; **(b)** simetria espelhada MEDIDA da silhueta (IoU mascara x espelho + extensoes e angulos por lado); **(c)** auditoria de ancoras de LADO, ancora por ancora, contra a fonte de costas, aplicada as costas v2 E ao 3/4 v2. Sugestao de linha para a tabela de escalada de APRENDIZADO_E_FLUXO.md (a ser lancada pelo executor, nao por este Critico): `01/11/2026 | Rodada 2 REF-01 lote 1 v2 | Contagem de dedos com zoom + simetria espelhada medida + auditoria de ancoras de lado (16/16) | D3, D10 e D1 fechados; D15 (palmas para a frente) achado`.

## 7. Conclusao

O retrabalho v2 cumpre integralmente a especificacao da rodada 1: bracos a 90 graus (medidos 3,18/1,88 grau), dedos separados e contaveis (5 + 5), massa de pele no ombro direito do personagem, costas avulsa com todos os lados certos, folha defeituosa abandonada. O lote passa no criterio de aceite (nenhum S1/S2). **As tres vistas v2 podem entrar no arsenal de referencias do Orc como insumo de modelagem**, com as ressalvas registradas (D5 para cor, D15 para convencao de palmas). Nao ha retrabalho v3 a especificar — o proximo passo do arsenal e o proximo sujeito da fila (Besta Cristalina), nao este lote.

**Assinatura:** Critico Visual senior (agente independente), 01/11/2026. Veredito tecnico; a palavra final de fidelidade artistica e do Mestre.

---

## Vereditos (linhas inequívocas)

- orc_tpose_v2.png: **APROVADA**
- orc_costas_v2.png: **APROVADA**
- orc_tresquartos_v2.png: **APROVADA**
- LOTE 1 v2: **APROVADO**
