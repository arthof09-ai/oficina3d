# CRITICO VISUAL SENIOR - REF-01, lote 2 (Besta Cristalina): relatorio da RODADA 2 DO RETRABALHO (vistas v2)

**Data:** 01/11/2026. **Papel:** Critico Visual senior, independente e imparcial (nao gerou nada deste lote; sua lealdade e a fidelidade MEDIDA contra as fontes). **Protocolo:** ESTUDO_MELHORIAS.md secao 7 (taxonomia EXT/MIS/FUS/DEF/SIL/SYM/FACE/PRP/TXT; severidades S1-S4) + bateria da secao 6 de APRENDIZADO_E_FLUXO.md adaptada a monstro serpentina + bateria integral da rodada 1 deste lote (relatorio CRITICO-ref01-lote2.md: lote REPROVADO, B1 SYM S2, B2 DEF/MIS S2, B3-B6 S3, especificacao de retrabalho na secao 6) + UMA verificacao nova obrigatoria desta rodada (escalada APR-01, secao 4a) e uma segunda adicional (secao 4b).

**Alvos julgados** (copias locais; SHA-256 conferidos por este Critico e IDENTICOS aos informados na tarefa e aos instalados no PC - Get-FileHash no PC confere; `git check-ignore` confirma os dois fora do git):
- `besta_diag_esq_v2.png` - 1920x1280, RGB, sha256 `cea0262ef59b31c06eb99d938dd0df70434849c7a0ae934c247286617daccd73`
- `besta_topo_v2.png` - 1920x1280, RGB, sha256 `208906f0c678891876d81b6fc1df3da2a457efdda2c32cebb133e773d68b9ec0`
- Membro do conjunto ja aprovado (NAO rejulgado): `besta_diag_dir.png`, sha256 `8640c324b45b624c3ec1b7ba01e07269d96fa62ba6aaa0374636dd7525f03dd1`.

**Fontes canonicas (autoridade):** `besta_frente.png` (`8d5aef2b...`), `besta_costas.png` (`72cd6ff0...`), `besta_esquerda.png` (`542d0f58...`), `besta_direita.png` (`a6df7869...`) - mesmas da rodada 1.

**Evidencias desta rodada:** zooms em `~/workspace/oficina-audit/zooms_lote2_v2/` (G_bocas_v2, H_bracos_esq_v2, I_placa_esq_v2, J_topo_cabeca_v2, K_maos_v2, L_bracos_comparativo); medicoes proprias por script (mascara de criatura por textura local; classes HSV; centroide/distribuicao de cristal; bbox/margens; correlacao entre vistas); ancoras por grounding visual. **Nota de calibracao (honestidade de metodo):** o script de medicao da rodada 1 nao foi preservado; reimplementei o metodo e o calibre nas ancoras publicadas. As grandezas ESTRUTURAIS reproduzem a rodada 1 quase exatamente (centroide da frente 0,482 contra 0,481; topo v1: centroide 0,532 e metade-esq 46,0% - identicos). A COBERTURA de cristal depende do classificador: reporto tres escalas (secao 2) e so tiro conclusoes que valem nas tres.

---

## Veredito do lote

**LOTE 2 FECHADO - APROVADO.** Os dois defeitos S2 da rodada 1 foram corrigidos E MEDIDOS como corrigidos: a `diag_esq_v2` voltou a familia frontal (a cauda nao cruza mais a linha media: B1 FECHADO) e a `topo_v2` e uma planta verdadeira (a boca nao le frontal: B2 FECHADO). B3, B4, B5 e B6 tambem fechados com evidencia. TODOS os autotestes geometricos do executor se confirmaram na substancia (8/8, secao 5) - o protocolo L-26 funcionou. Restam apenas pendencias S3/S4 nomeadas: B7 estendido ao par de diagonais (diversidade angular baixa, medida nova), B10 (maos do topo em roseta - achado da verificacao nova de coerencia interna), B11 (tom do topo) e B9 (margens). Nenhum defeito S1/S2 de fidelidade restante. A palavra artistica final e do Mestre; este veredito e o tecnico.

| Imagem | Veredito | Pode entrar no arsenal? |
|---|---|---|
| `besta_diag_dir.png` (rodada 1) | **APROVADA** (mantido) | SIM - ressalva B7 |
| `besta_diag_esq_v2.png` | **APROVADA** | **SIM** - pendencias B7-par (S3) e B9 (S4) |
| `besta_topo_v2.png` | **APROVADA como vista de topo** | **SIM** - pendencias B10 (S3), B11 (S3) e B9 (S4) |

## 1. Bateria da secao 6 adaptada a Besta, item a item (vistas v2)

**1. Mesma criatura? - PASSA nas duas.** Serpente cristalina enrolada, cabeca-capuz com boca triangular e interior roxo granulado, veios roxos, pele cinza rochosa rachada, bracos com placa e maos de cristal. Nenhuma criatura diferente, nenhum membro inventado.

**2. Caracteristicas preservadas? - PASSA na diag_esq_v2; PASSA COM RESSALVA no topo_v2.** Inventario: (a) aglomerado de cristais atras da cabeca - presente e denso nas duas (a v1 da diag_esq o tinha reduzido); (b) **placa de cristal frontal - PRESENTE e fiel na diag_esq_v2 (zoom I)**: o segmento blindado coberto de cristais pendurado na frente inferior do corpo, como na frente canonica - era o item central de B5; no topo nao se aplica (vista dorsal); (c) roseta dorsal - presente no topo_v2, centrada atras da cabeca, com o cristal central longo apontando para o corpo, como nas costas canonicas; (d) fileira de cristais da cauda - presente e continua nas duas; (e) fenda/veio roxo ventral - presente na diag_esq_v2, correndo pelo centro do tronco. Ressalva do topo: as MAOS sairam em forma de roseta radial (B10, secao 4a). Nenhum elemento inventado (EXT).

**3. Pose/enrolamento coerente com frente/costas? - PASSA nas duas.** A diag_esq_v2 manteve o enrolamento compacto em S da pose canonica (a v1 tinha DESENROLADO a criatura) e os bracos pendentes junto ao tronco. No topo_v2 a espiral le-se inteira num so plano, com a cabeca no alto e a cauda varrendo o arco inferior ate a direita.

**4. Integracao dos bracos - PASSA nas duas (B3 e B6 fechados).** Diag_esq_v2: o comparativo de 4 paineis (zoom L: frente canonica | diag_dir aprovada | diag_esq v1 | diag_esq_v2) mostra que o segmento arredondado UNICO do braco da v2 e o mesmo elemento anatomico da fonte e da diag_dir aprovada; a v1 tinha bola DUPLA empilhada com o braco estendido - leitura de boneco articulado que a v2 nao tem. Suspeita inicial deste Critico ao zoom H isolado, REFUTADA pelo comparativo: registro a refutacao porque ela e o metodo funcionando. Topo_v2: antebracos RETOS com placa (cuff) flanqueando o corpo - sem a espiral-caracol da v1 (B6) e conforme a especificacao 6.2.4 da rodada 1.

**5. Enquadramento e fundo - PASSA com ressalva S4 (B9 persiste).** Corpo inteiro, fundo claro uniforme, sem cenario/texto/sombra forte. Margens pela bbox da mascara: diag_esq_v2 esq 2,4% / dir 4,7% / topo 1,6% / base 1,4% - a especificacao 6.1.6 pedia ponta da cauda a >= 5% da borda; veio 2,4% do lado da cauda. Topo_v2: esq 2,1% / dir 2,0% / topo 3,8% / base 2,5%. Nada cortado em nenhuma; margem apertada e pendencia cosmetica (precedente B9 da rodada 1: S4).

**6. Consistencia cruzada ENTRE vistas - PASSA nas ancoras estruturais; UMA contradicao de forma (verificacao nova, secao 4a).**

**7. Integridade tecnica - PASSA.** PNGs validos 1920x1280 RGB; SHA-256 PC == local nos dois arquivos; `git check-ignore` confirma ambos fora do git; copias locais de seguranca existentes.

**8. Classificacao de defeitos** - tabela completa na secao 6.

## 2. Paleta e cobertura - metodo, calibracao e numeros

**Medianas RGB por classe** (classificador HSV deste Critico; deltas contra as medianas canonicas da frente publicadas na rodada 1: cristal (170,24,147), roxo (70,11,60), pele (114,91,93)):

| Vista | Cristal | Roxo brilhante | Pele |
|---|---|---|---|
| diag_esq_v2 | (167,26,151) - **delta 9** | (71,15,64) - **delta 9** | (111,90,92) - **delta 5** |
| topo_v2 | (176,12,161) - **delta 32** | (72,15,63) - delta 9 | (122,101,103) - **delta 28** |

A diag_esq_v2 e fiel em cor (deltas 5-9, dentro da faixa aprovada do lote 1). O topo_v2 tem desvio tonal proprio: cristal mais saturado (G cai 12, B sobe 14) e pele mais clara (+8/+10/+10 por canal) - a imagem inteira e "mais quente/viva" que o canonico (B11, TXT S3; precedentes: D5 do lote 1 = S3 com delta 41 de pele; B8 = S4 com deltas <= 25). A frente canonica segue como autoridade de cor do conjunto.

**Cobertura de cristal (% dos pixels da criatura) em TRES classificadores** (o comparavel honesto e coluna contra coluna):

| Vista | R1 (publicado) | Equilibrada (HSV S>=90,V>=115) | Ancorada (HSV S>=85,V>=108) | RGB media |
|---|---|---|---|---|
| fonte frente | 32,1 | 29,8 | 32,5 | 27,0 |
| fonte costas | 35,9 | 33,0 | 35,8 | 31,0 |
| fonte esquerda | 36,4 | 33,7 | 36,3 | 31,1 |
| fonte direita | 36,2 | 33,1 | 36,1 | 30,7 |
| diag_esq v1 | 21,3 | 22,4 | 24,0 | 20,0 |
| diag_dir (aprov.) | 24,3 | 27,1 | 29,7 | 24,3 |
| topo v1 | 29,7 | 31,8 | 34,7 | 28,7 |
| **diag_esq_v2** | - | **29,1** | **31,8** | **25,8** |
| **topo_v2** | - | **32,8** | **35,5** | **30,1** |

A escala "ancorada" reproduz as fontes a <= 0,4 pp dos valores da rodada 1. **Leitura invariante:** a diag_esq_v2 fica a 0,7-1,2 pp do piso canonico (a frente) em TODAS as escalas e 5,8-7,8 pp ACIMA da v1 - a perda de ~1/3 do cristal (B5) foi corrigida; o residuo contra os perfis (36%) e o mesmo efeito de barriga exposta aceito na diag_dir aprovada. O topo_v2 esta DENTRO da faixa canonica nas tres escalas. O numero do executor para a diag_esq_v2 (29,0%, classificador dele) coincide com a minha escala equilibrada (29,1%); o do topo (28,9%) e da escala dele - a substancia (perto do canonico) se confirma, o absoluto nao e comparavel, como ele mesmo declarou.

## 3. Testes da rodada 1, reaplicados

### 3a. ATRIBUICAO DAS DIAGONAIS - diag_esq_v2 PASSA (B1 FECHADO)

Regra (rodada 1): em qualquer diagonal frontal, ponta da cauda na metade esquerda e maioria dos cristais na metade esquerda - massas lateralizadas nao cruzam a linha media.

| Vista | Ponta da cauda (x/1000) | Centroide x dos cristais | Metade esq. | Veredito |
|---|---|---|---|---|
| fonte frente | 107 (R1) | 0,481 (R1) / 0,482 (meu) | 56,1% (R1) / 55,3% | autoridade |
| diag_dir | 143 (R1) | 0,479 / 0,485 | 56,0% / 54,9% | PASSA (R1) |
| diag_esq v1 | 885 | 0,557 / 0,552 | 38,7% / 39,8% | FALHA (B1) |
| **diag_esq_v2** | **~24 (mascara) / 27 (executor)** | **0,483** | **51,2%** | **PASSA** |

A ponta extrema da cauda medida pela mascara de criatura esta em x = 24/1000 (o grounding ancorou a espiga superior do leque em (259,443) - ainda no terco esquerdo; a ancora extrema e a da mascara). Quartos da v2: [23,7 / 27,5 / 31,2 / 17,6] - o Q3 pesado e o cristal do enrolamento inferior direito e da mao direita, sem violar nenhuma das duas condicoes do teste. A maioria esquerda (51,2%) e mais estreita que a da frente (55,3%) porque a vista e diagonal de verdade no tronco - mas a cauda, a ancora dura, esta inequivocamente a esquerda. **B1 (SYM S2) FECHADO por medida.**

### 3b. PUREZA DA VISTA DE TOPO - topo_v2 PASSA (B2 FECHADO)

Criterio binario (rodada 1): se o perimetro inteiro da boca e o interior leem de frente, nao e planta. **Observado no topo_v2 (zoom J):** o capuz le-se como DOMO de escamas visto de cima; na borda frontal da cabeca ha apenas uma **fenda fina e escura escornada** - nenhum perimetro de boca, nenhum interior granulado exposto, nenhuma franja visivel em volta. Ancora da cabeca por grounding: (490,144), no alto do quadro, como pede a convencao do conjunto. A espiral, a roseta e a fileira dorsal leem num so plano. **E planta verdadeira (~90 graus). B2 (DEF/MIS S2) FECHADO.** O que a antecipacao do executor disse ("so fenda fina") esta confirmado - desta vez a magnitude tambem estava certa.

## 4. VERIFICACOES NOVAS DESTA RODADA (escalada APR-01)

### 4a. COERENCIA INTERNA DO CONJUNTO (nova - obrigatoria)

Pergunta: diag_dir (aprovada) + diag_esq_v2 + topo_v2 sao rotacoes de UMA criatura? Ancora por ancora, ENTRE as vistas (nao so contra as fontes):

| Ancora | diag_dir | diag_esq_v2 | topo_v2 | Coerente? |
|---|---|---|---|---|
| Flanco da cauda (anatomico direito) | cauda a esq. da imagem (frontal) | cauda a esq. da imagem (frontal) | cauda a dir. da imagem (planta, cabeca no alto) | **SIM** - um so individuo |
| Placa frontal | presente (zoom D da R1) | presente (zoom I) | n/a (vista dorsal) | SIM |
| Roseta: posicao e orientacao | aglomerado atras da cabeca, massa a esq. | idem | centrada atras da cabeca, cristal longo apontando para o corpo (= costas canonicas) | SIM |
| Fenda ventral | presente, central | presente, central | n/a (ventre para baixo) | SIM |
| Boca/cabeca | frontal triangular | frontal triangular | domo + fenda (planta) | SIM |
| **Maos de cristal** | **feixe alongado pendente** | **feixe alongado pendente** | **ROSETA RADIAL simetrica (flor)** | **NAO - contradicao** |

Seis ancoras estruturais coerentes; UMA contradicao, de FORMA: nas fontes e nas duas diagonais, as maos sao feixes irregulares de cristais alongados que pendem da placa do antebraco; no topo_v2, as duas maos sao rosetas radiais regulares, com cristal central e aneis concentricos - o motivo da roseta DORSAL transplantado para as maos (zoom K, contra a mao das costas canonicas e contra as diagonais). Posicao, lado e classe de tamanho estao certos; a forma do elemento-assinatura esta errada e CONTRADIZ as vistas irma do proprio conjunto. **B10 (DEF S3)** - pendencia nomeada; nao bloqueia (a geometria de modelagem - onde a mao esta e quanto ocupa - esta correta; a forma fina da mao se modela pelas diagonais/fontes).

### 4b. DIVERSIDADE ANGULAR DO PAR DE DIAGONAIS (nova - adicional)

Correlacao de luminancia (imagens reduzidas a 256x171, quadros alinhados): corr(diag_dir, diag_esq_v2) = **0,778**; controles: corr(diag_dir, diag_esq_v1) = 0,168; corr(diag_dir, topo_v2) = 0,293; corr(diag_esq_v1, diag_esq_v2) = 0,153. Impressoes digitais laterais quase identicas (centroides 0,485 x 0,483; ambas familia frontal). As duas "diagonais opostas" sao, na pratica, **duas frontais rasas do mesmo lado** - nao sao duplicata de pixels, mas entregam pouca informacao angular nova uma sobre a outra. **B7 (DEF/SIL S3) estende-se da diag_dir ao PAR**: pendencia nomeada para rodada futura (uma diagonal genuinamente profunda, ~45 graus, aumentaria o conjunto); nao bloqueia o lote, pelo mesmo criterio com que a rodada 1 aprovou a diag_dir com B7 aberto.

## 5. Autotestes do executor - destino item a item

| # | Autoteste declarado | Destino | Evidencia deste Critico |
|---|---|---|---|
| 1 | diag_esq_v2: ponta da cauda x~27/1000 | **CONFIRMADO** | Mascara: extremo da criatura em x=24/1000; grounding na espiga do leque (259,443), terco esquerdo |
| 2 | diag_esq_v2: centroide 0,475; 52,5% a esquerda | **CONFIRMADO** | Meu: 0,483 e 51,2% (deltas 0,008 e 1,3 pp - dentro do ruido entre classificadores) |
| 3 | diag_esq_v2: placa frontal presente | **CONFIRMADO** | Zoom I: placa blindada coberta de cristais na frente inferior, como a fonte |
| 4 | diag_esq_v2: cobertura 29,0% (classificador do executor) | **CONFIRMADO** | 29,1% na minha escala equilibrada; 31,8% na ancorada; B5 fechado em todas |
| 5 | diag_esq_v2: margem esquerda 2,7% | **CONFIRMADO (e vira pendencia)** | Mascara: 2,4%. Abaixo dos 5% da especificacao - B9 (S4) |
| 6 | topo_v2: boca nao le frontal, so fenda fina | **CONFIRMADO** | Zoom J: domo + fenda escornada; nenhum perimetro/interior |
| 7 | topo_v2: cauda a direita, x=964 | **CONFIRMADO na substancia** | Extremo direito da mascara x=980; o aglomerado terminal da cauda ocupa a borda direita (a espiga exata varia 806-980 conforme a definicao); lateralizacao inequivoca |
| 8 | topo_v2: cobertura 29,7%->28,9% declarada | **CONFIRMADO na substancia** | Nas minhas escalas: 32,8% / 35,5% - dentro da faixa canonica; o absoluto e da escala do executor, como declarado |
| 9 | topo_v2: bracos abertos lateralmente | **CONFIRMADO como fato; conforme a especificacao** | A 6.2.4 da rodada 1 pedia antebracos retos flanqueando o corpo; o desvio esta na FORMA DAS MAOS (B10), que o autoteste nao cobria |

Saldo: **8/8 autotestes confirmados** (dois "na substancia", com a ressalva de escala declarada pelo proprio executor). Diferente da rodada 1, a antecipacao nao subestimou nenhum defeito estrutural - os dois S2 fecharam exatamente onde os autotestes disseram que fechariam. O que escapou migrou de nivel: forma fina de elemento (B10) e tom (B11), que os autotestes geometricos nao medem - dai a licao L-27.

## 6. Tabela de defeitos

| ID | Imagem | Codigo | Sev. | Estado nesta rodada | Evidencia |
|---|---|---|---|---|---|
| B1 | diag_esq v1 | SYM | S2 | **FECHADO na v2** | Secao 3a: cauda x~24, centroide 0,483, metade esq. 51,2% |
| B2 | topo v1 | DEF/MIS | S2 | **FECHADO na v2** | Secao 3b: domo + fenda; boca nao le frontal (zoom J) |
| B3 | diag_esq v1 | DEF | S3 | **FECHADO na v2** | Zoom L (4 paineis): segmento arredondado unico = canonico; v1 tinha bola dupla |
| B4 | diag_esq v1 | FACE | S3 | **FECHADO na v2** | Zoom G: franja curta, fina e irregular como a fonte; sem fileira de presas |
| B5 | diag_esq v1 | MIS | S3 | **FECHADO na v2** | Placa presente (zoom I); cobertura no piso canonico nas 3 escalas (secao 2) |
| B6 | topo v1 | DEF | S3 | **FECHADO na v2** | Antebracos retos com placa; nenhuma espiral |
| B7 | diag_dir -> **par de diagonais** | DEF/SIL | S3 | **ABERTO (pendencia nomeada)** | Secao 4b: corr 0,778 e centroides gemeos - diversidade angular baixa do par |
| B8 | todas (v1) | TXT | S4 | **FECHADO para a diag_esq_v2** (deltas 5-9); **substituido por B11 no topo_v2** | Secao 2 |
| B9 | diag_esq_v2, topo_v2 | SIL | S4 | **ABERTO (cosmetico)** | Margens 2,0-2,5% nos lados criticos; nada cortado (secao 1.5) |
| B10 | topo_v2 | DEF | S3 | **ABERTO (novo - pendencia nomeada)** | Secao 4a/zoom K: maos em roseta radial contradizem o feixe das fontes e das diagonais |
| B11 | topo_v2 | TXT | S3 | **ABERTO (novo - pendencia nomeada)** | Secao 2: cristal delta 32 (saturado), pele delta 28 (clara) contra a frente canonica |

**Achados positivos registrados:** autotestes do executor 8/8 confirmados (o protocolo L-26 funcionou na integra); os dois S2 corrigidos com margem medida, nao no limite; placa, roseta e enrolamento fieis; integridade tecnica completa. Nenhum defeito S1. Nenhum elemento inventado (EXT).

## 7. Registro da escalada APR-01 desta rodada

Verificacoes ADICIONADAS pela rodada 2 do retrabalho do lote 2: **(a) Coerencia interna do conjunto** - as vistas candidatas conferidas umas contra as outras, ancora por ancora (flanco da cauda, placa, orientacao da roseta, lado do aglomerado maior, forma dos elementos-assinatura), e nao so cada uma contra as fontes: pegou B10; **(b) Diversidade angular medida do par de diagonais** - correlacao entre vistas + impressao digital lateral comparada: estendeu B7 ao par. Sugestao de linha para a tabela de escalada de APRENDIZADO_E_FLUXO.md: `01/11/2026 | Rodada 2 do retrabalho REF-01 lote 2 (Besta v2) | Coerencia interna do conjunto (ancora x ancora ENTRE as vistas) + diversidade angular medida do par de diagonais | B1/B2/B3/B4/B5/B6 fechados por medida; achados novos B10 DEF S3 (maos-roseta do topo) e B11 TXT S3 (tom do topo); B7 estendido ao par; LOTE FECHADO`.

## 8. Conclusao

O retrabalho fez o que a especificacao mandava e PROVOU com autotestes que desta vez resistiram a medicao independente - os dois defeitos estruturais que reprovaram o lote (espelhamento e pseudo-planta) estao fechados com numeros, nao com promessas. As pendencias que restam sao de refinamento (diversidade angular do par, forma das maos na planta, tom da planta, margens), todas nomeadas e nenhuma capaz de ensinar geometria errada ao modelo. **O lote 2 esta FECHADO: o conjunto da Besta Cristalina tem os 4 cardeais canonicos + diag_dir + diag_esq_v2 + topo_v2.** Proximo sujeito da fila do arsenal: **Caprileo (lote 3)**.

**Assinatura:** Critico Visual senior (agente independente), 01/11/2026. Veredito tecnico; a palavra final de fidelidade artistica e do Mestre.

---

## Vereditos (linhas inequivocas)

- besta_diag_esq_v2.png: **APROVADA** (B1/B3/B4/B5 fechados; pendencias B7-par S3, B9 S4)
- besta_topo_v2.png: **APROVADA como vista de topo** (B2/B6 fechados; pendencias B10 S3, B11 S3, B9 S4)
- besta_diag_dir.png: **APROVADA** (rodada 1, mantido)
- LOTE 2 (Besta Cristalina): **FECHADO - APROVADO**
