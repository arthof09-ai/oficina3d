# CRITICO VISUAL SENIOR - REF-01, lote 1 (Orc): relatorio de auditoria

**Data:** 01/11/2026. **Papel:** Critico Visual senior, independente e imparcial (nao executou nada deste lote). **Protocolo:** ESTUDO_MELHORIAS.md secao 7 (taxonomia EXT/MIS/FUS/DEF/SIL/SYM/FACE/PRP/TXT; severidades S1-S4) + bateria oficial do lote em APRENDIZADO_E_FLUXO.md secao 6 (8 verificacoes).

**Alvos julgados** (copias locais identicas as do PC - SHA-256 conferidos nos dois lados):
- `orc_tpose.png` - 1328x1904, RGB, sha256 `1a82f46a2b9d911f...`
- `orc_angulos.png` - 2544x960, RGB, sha256 `2f1103055d63fb71...`
- `orc_costas_ref.png` - 1328x1904, RGB, sha256 `7b523cad0e669072...`

**Fontes canonicas:** `testes/dourado/imagens/orc_frente.png` (1280x1820 RGBA, sha256 `30c0f83d3ede10fd...`; copia local com MD5 identico ao arquivo usado pelo executor) e `orc_costas.png` (sha256 `256c8a2fe22588f3...`) para a vista de costas.

**Inventario da fonte (antes de julgar, protocolo 7.3):** testa pesada; orelhas pontudas COM brincos de argola; olhos vermelhos; 2 presas inferiores maiores + dentes menores; cavanhaque preto pontudo; listras vermelhas na testa e marcas nas bochechas; pele verde-oliva com riscos vermelhos nos ombros/peito; dreads pretos em coque alto (faixa vermelha/dourada) com contas e cilindros de cobre e pendentes de osso; **cabeca de lobo sobre o ombro ESQUERDO do personagem** (a direita de quem olha a frente); **ombreira de espinhos no braco DIREITO do personagem** (a esquerda de quem olha), bracelete de espinhos no antebraco direito, machado de lamina UNICA na mao direita (fora da pose por decisao registrada); antebraco esquerdo com bracelete de placas sobrepostas; colar de presas com caveira; alca diagonal de couro com fivelas; cinto com placa losango, caveira grande + presa longa no quadril esquerdo, 2 caveirinhas centrais, correntes com aneis e gancho de osso, tubo de pergaminho no quadril direito, adaga no quadril esquerdo; saiote de pele/couro com paineis de tecido vermelho; capa de pele clara cobrindo OS DOIS ombros (massa espessa sobre o ombro direito inclusive) e caindo pelas costas ate abaixo dos joelhos; grevas e botas de metal com espinhos e acabamento de pele. Nas costas canonicas: lobo a ESQUERDA de quem olha; ombreira de espinhos a DIREITA de quem olha; alca diagonal cruzando a capa com fivela; trofeus do cinto = caveiras, presas e correntes - **nenhuma bolsinha**.

---

## Veredito do lote

**LOTE REPROVADO no criterio de aceite** (APRENDIZADO_E_FLUXO secao 6: nenhum defeito de fidelidade S1/S2). Ha defeito S2 de fidelidade nas TRES imagens (D1, D7, D10 abaixo). Nada aqui e "mais ou menos aprovado": as tres imagens ficam como PREVIA de insumo, nao como referencia canonica de modelagem, ate o retrabalho. A palavra artistica final e do Mestre; este veredito e o tecnico. Todos os defeitos estao ABERTOS.

| Imagem | Veredito | Defeito decisivo |
|---|---|---|
| `orc_tpose.png` | **REPROVADA** | D1 - MIS S2 (massa de pele do ombro direito perdida) |
| `orc_angulos.png` | **REPROVADA** | D7 - MIS S2 (vista de costas ausente da folha) |
| `orc_costas_ref.png` | **REPROVADA** | D10 - SYM S2 (personagem inteiro espelhado) |

## Bateria da secao 6, item a item

**1. Mesmo personagem? - PASSA (com louvor no rosto).** Zoom do rosto da T-pose: testa pesada, listras vermelhas na testa do lado certo, marcas nas bochechas, olhos vermelhos, 2 presas inferiores grandes + dentes menores, cavanhaque pontudo, orelhas pontudas com argolas nos dois lados, coque com faixa vermelha/dourada, contas de cobre e pendente de osso nos dreads - tudo presente e simetrico (FACE: OK). Pele verde-oliva e proporcoes gerais (ombros muito largos, tronco massivo) reconheciveis nas 3 imagens. Ressalva menor: na T-pose o conjunto e ligeiramente menos massivo que a fonte (maos proporcionalmente menores) - D6, PRP S4.

**2. Caracteristicas preservadas? - FALHA PARCIAL (a falha central do lote).** Presentes e corretos na T-pose e na folha: lobo no ombro esquerdo, ombreira de espinhos no braco direito, colar, alca diagonal, inventario do cinto quase item a item (zoom da cintura: placa losango, fivela, 2 caveirinhas, caveira grande + presa, aneis + gancho, pergaminho, adaga). Faltas e invencoes:
- T-pose: a **massa de pele clara sobre o ombro direito do personagem sumiu** - o ombro aparece de pele nua com riscos vermelhos e a ombreira de metal pendurada por alca, onde a fonte tem a pele espessa cobrindo ombro e peito (zoom `zooms/tpose_ombro_dir_tela.png` x fonte). A capa existe (pende atras e ao lado), mas a massa do ombro - parte da silhueta-assinatura - nao. **D1, MIS/DEF S2.**
- Costas avulsa: personagem **inteiro espelhado** (D10) + **2 bolsinhas inventadas** no cinto (D11, EXT S3) + **alca diagonal das costas ausente** (D12, MIS S3).
- Folha: **1 bolsinha inventada** na 4a figura (D9, EXT S3) - o executor so confessou bolsinhas nas costas avulsas; a folha tambem tem.
- Nada de arma nova, nenhuma cor trocada (medido - ver verificacao nova).

**3. T-pose correta? - FALHA.** Palmas para baixo: sim. Simetria entre os bracos: sim (diferenca de ~1,7 grau). Mas:
- **Bracos ~30 graus abaixo da horizontal, MEDIDOS** (ajuste de regressao sobre o eixo medio da silhueta do braco, 279 colunas por lado: 31,6 graus no braco direito do personagem, 29,9 no esquerdo). A estimativa do executor (20-25 graus) era OTIMISTA - refutada na magnitude, confirmada na direcao. **D2, DEF S3** (nao funde nada e motores multivista toleram A-pose, mas a entrega pedida era T-pose).
- **Dedos nao contaveis:** zooms das duas maos mostram polegar separado, indicador legivel e os demais dedos em massas parcialmente fundidas (anelar+medio sem linha de separacao). **D3, FUS S3.**

**4. Pernas como pedido? - PASSA COM RESSALVA.** Pernas retas, um pouco afastadas, pes para a frente, sem fusao perna-perna. Ressalva: o painel de tecido vermelho e as abas de pele descem PELA FRENTE entre as pernas e se sobrepoem a face interna das coxas no topo (zoom da cintura) - sem fundir as pernas, mas e material entre as pernas onde a leitura da silhueta interna importa. **D4, DEF/FUS S3 leve.**

**5. Enquadramento e fundo - PASSA.** Corpo inteiro com margem nas 3 imagens; fundo cinza-claro uniforme; sem cenario, sem texto, sem sombra projetada forte. Observacao S4: as geradas sao RGB sem canal alfa; as fontes canonicas sao RGBA com transparencia. Para insumo multivista o fundo uniforme basta; registrado para o padrao dos proximos lotes.

**6. Folha de angulos - FALHA.** A folha tem 5 figuras: frente, 3/4 e TRES perfis - **nenhuma vista de costas** (D7, MIS S2: a vista que "completa o que nao aparece" e a razao da frente REF-01). Dos perfis, dois olham para a direita e um para a esquerda: ha um **perfil quase duplicado e ambiguidade de orientacao** (D8, DEF S3). A favor da folha: as vistas presentes sao mutuamente consistentes - lobo sempre no ombro esquerdo, inventario do cinto e listras vermelhas coerentes entre frente/3/4/perfis, paleta coerente (medido). Inconsistencia ENTRE entregas: a frente da folha TEM a massa de pele do ombro direito que a T-pose perdeu (D1) - as duas imagens do mesmo lote discordam entre si.

**7. Integridade tecnica - PASSA.** PNGs validos; dimensoes, tamanhos e SHA-256 registrados (REGISTRO do executor); hashes das copias do PC identicos aos das copias locais; `git check-ignore` no PC confirma os 3 arquivos FORA do git (`.gitignore:22:*.png`); copia local de seguranca existe. Arte do RPG fora do repo publico: confirmado.

**8. Classificacao de defeitos** - tabela completa abaixo, na taxonomia do protocolo.

## As 5 confissoes do executor, uma a uma

1. **"Bracos ~20-25 graus abaixo da horizontal"** - CONFIRMADA na direcao, **REFUTADA na magnitude**: medido ~30 graus (31,6/29,9) pelo eixo medio da silhueta. A autoconfissao subestimou o desvio em ~5-10 graus.
2. **"Dedos macios/parcialmente fundidos"** - CONFIRMADA nas duas maos (zooms dedicados; dedos nao contaveis de forma confiavel).
3. **"Folha sem costas e com perfil quase duplicado"** - CONFIRMADA integralmente; e o defeito mais bem diagnosticado pelo executor.
4. **"Lobo espelhado nas costas; ombreira no lado certo"** - PRIMEIRA METADE CONFIRMADA, **SEGUNDA METADE REFUTADA**: nas costas canonicas a ombreira de espinhos aparece a DIREITA de quem olha; na gerada, aparece a ESQUERDA, junto com o bracelete de espinhos - e o bracelete de placas, que nas costas canonicas fica a esquerda, saiu a direita. **O personagem inteiro esta lateralmente invertido**, nao so o lobo. Um MV alimentado com esta costas + a frente correta recebe instrucao contraditoria de lado - a mesma classe do defeito inaugural do machado (EXT+FUS S2 do Lendario). D10 SYM S2, com escalacao registrada: **se esta vista entrar num job multivista junto da frente correta, o defeito vale S1 para esse job.**
5. **"Bolsinhas EXT no cinto das costas"** - CONFIRMADAS (2 bolsinhas; as costas canonicas nao tem nenhuma) - **e ha uma terceira ocorrencia nao confessada**: a bolsinha na 4a figura da folha de angulos (D9).
6. **"Pintura mais lisa que a fonte"** - CONFIRMADA como textura (D5/D14, TXT S3/S4); quanto a COR, ver a verificacao nova: a paleta esta fiel, o que se perdeu foi o grao.

## O que o executor NAO viu (alem das confissoes)

- **D1** - a perda da massa de pele do ombro direito na T-pose (o defeito decisivo dessa imagem).
- **D9** - a bolsinha tambem existe na folha.
- **D10 (extensao)** - o espelhamento das costas e do personagem inteiro, nao so do lobo; a afirmacao "ombreira no lado certo" esta errada.
- **D12** - a alca diagonal das costas (com fivela, visivel nas costas canonicas sobre a capa) nao existe na costas gerada.
- **D13** - costas gerada: capa mais curta e uniforme (a canonica desce abaixo dos joelhos de um lado) e **pe direito virado de lado** numa vista que pedia os dois pes apontando para tras - postura inconsistente para referencia de modelagem.
- **Inconsistencia cruzada T-pose x folha** no ombro direito (item 6 acima).

## Verificacao NOVA desta auditoria (regra de escalada APR-01)

**Acréscimo de rigor: amostragem QUANTITATIVA de paleta por classe de cor.** Nenhuma bateria anterior mediu cor - "cores fieis" era impressao. Metodo: mediana RGB dos pixels da classe "pele verde" (matiz 0,11-0,30, saturacao 0,15-0,80) e da classe "tecido vermelho" (matiz <0,045 ou >0,96, saturacao >0,45), figura inteira, fonte x gerada:

| Classe | Fonte | T-pose | Folha | Costas gerada (fonte costas) |
|---|---|---|---|---|
| Pele | (134,113,60) | (148,127,73) - soma dos deltas = 41 | (137,118,67) - delta = 17 | (125,106,56) - delta = 10 |
| Vermelho | (94,32,24) | (91,32,26) - delta = 3 | (88,33,28) - delta = 11 | (80,34,27) - delta = 24 |

**Leitura:** a paleta e FIEL - o tecido vermelho e praticamente identico na T-pose; a pele esta levemente mais clara/amarelada na T-pose (delta 41) e quase exata na folha e nas costas. O desvio de estilo do lote e de TEXTURA (grao perdido), nao de cor. Esta verificacao entra para a bateria permanente dos proximos lotes: desvio de paleta vira numero, nao opiniao. (O angulo dos bracos tambem foi promovido de estimativa a medicao por regressao sobre a silhueta - item 3.)

## Tabela de defeitos (protocolo 7.5)

| ID | Imagem | Codigo | Regiao | Sev. | Evidencia | Estado |
|---|---|---|---|---|---|---|
| D1 | orc_tpose.png | MIS/DEF | ombro direito do personagem (massa de pele) | **S2** | zoom `zooms/tpose_ombro_dir_tela.png` x `orc_frente_canon.png` | ABERTO |
| D2 | orc_tpose.png | DEF | bracos ~30 graus abaixo da horizontal (medido) | S3 | regressao sobre silhueta, 279 colunas/lado | ABERTO |
| D3 | orc_tpose.png | FUS | dedos das duas maos parcialmente fundidos, nao contaveis | S3 | zooms `tpose_mao_esq_tela.png`, `tpose_mao_dir_tela.png` | ABERTO |
| D4 | orc_tpose.png | DEF/FUS | tecido/pele da cintura descendo entre as pernas, sobre a face interna das coxas | S3 | zoom `tpose_cintura_pernas.png` | ABERTO |
| D5 | orc_tpose.png | TXT | pintura lisa, sem o grao da fonte; pele +clara (delta 41) | S3 | leitura visual + amostragem de paleta | ABERTO |
| D6 | orc_tpose.png | PRP | conjunto ligeiramente menos massivo que a fonte (maos menores) | S4 | comparacao visual frente a frente | ABERTO |
| D7 | orc_angulos.png | MIS | vista de costas AUSENTE da folha | **S2** | folha inteira (5 figuras: frente, 3/4, 3 perfis) | ABERTO |
| D8 | orc_angulos.png | DEF | perfil quase duplicado; 2 perfis olham p/ direita, 1 p/ esquerda (orientacao ambigua) | S3 | folha inteira | ABERTO |
| D9 | orc_angulos.png | EXT | bolsinha de couro na 4a figura (nao existe na fonte) | S3 | folha, figura 4, quadril | ABERTO |
| D10 | orc_costas_ref.png | SYM | personagem INTEIRO espelhado: lobo, ombreira e braceletes trocados de lado | **S2** (S1 se entrar em job MV com a frente) | comparacao com `orc_costas_canon.png` | ABERTO |
| D11 | orc_costas_ref.png | EXT | 2 bolsinhas no cinto das costas (canonicas: nenhuma) | S3 | comparacao com `orc_costas_canon.png` | ABERTO |
| D12 | orc_costas_ref.png | MIS | alca diagonal das costas ausente sobre a capa | S3 | comparacao com `orc_costas_canon.png` | ABERTO |
| D13 | orc_costas_ref.png | DEF | capa curta/uniforme; pe direito virado de lado | S3 | imagem inteira | ABERTO |
| D14 | orc_costas_ref.png | TXT | padrao de pele repetitivo/em escamas, mais liso que a fonte | S4 | leitura visual | ABERTO |

## Retrabalho exigido (especificacao exata, sem "mais ou menos")

1. **T-pose v2** (geracao avulsa, ancorada na frente canonica): exigir no pedido (a) bracos a 90 graus da horizontal, verificados por medicao depois; (b) dedos individualmente separados e contaveis nas duas maos; (c) **massa espessa de pele clara cobrindo o ombro DIREITO do personagem** como na fonte; (d) manter todo o resto do inventario. Aceite da v2: D1 e D2 zerados; D3 no maximo S4.
2. **Folha de angulos: abandonar o formato folha.** Gerar as vistas AVULSAS (uma por geracao - a licao que o proprio executor levantou): perfil esquerdo verdadeiro e a vista de costas nova (item 3). A folha atual fica arquivada como "incompleta - nao usar como insumo".
3. **Costas v2** (avulsa, ancorada nas costas canonicas) com ancoras de lado EXPLICITAS no pedido: "cabeca de lobo no ombro ESQUERDO do personagem - nas costas, aparece a ESQUERDA da imagem; ombreira de espinhos no braco DIREITO do personagem - nas costas, aparece a DIREITA da imagem; alca diagonal de couro cruzando a capa com fivela; cinto SEM bolsinhas - trofeus sao caveiras, presas e correntes; os dois pes apontando para longe do observador; capa descendo alem da cintura". Aceite da v2: conferencia de lado item a item contra as costas canonicas antes de instalar.
4. **Bateria do proximo lote** herda: (a) a amostragem quantitativa de paleta (nova desta auditoria); (b) a medicao geometrica de pose por regressao; (c) conferencia de LADO explicita para qualquer vista de costas/perfil (o erro D10 nao pode se repetir sem ser pego na antecipacao).

**Assinatura:** Critico Visual senior (agente independente), 01/11/2026. Veredito tecnico; a palavra final de fidelidade artistica e do Mestre.
