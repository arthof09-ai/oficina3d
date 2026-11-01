# CRÍTICO VISUAL — REF-01 lote 4 RETRABALHO (diagonal traseira esquerda refeita + diagonal frontal esquerda)

**Papel:** Crítico Visual sênior independente e ADVERSÁRIO (APR-02). Missão: tentar
reprovar. Nada aqui é benevolência: o que está aprovado passou por medição contra as
fontes, não por simpatia ao esforço — e o que está reprovado como especificação
também está provado, não insinuado.
**Data:** 01/11/2026. **Escopo:** SOMENTE as duas imagens abaixo. Eu NÃO gerei nenhuma
delas. Nada foi escrito no PC do projeto, nenhum commit, nenhuma instalação: este
relatório é local e o executor decide a instalação depois do veredito.
**A palavra final de fidelidade artística é do Mestre.**

## Arquivos julgados (SHA conferido na leitura — batem com o lote)

| Arquivo | Tamanho | SHA-256 |
|---|---|---|
| `orc_diag_tras_esq_refeita.png` | 1328 × 1904 px, 2.274.898 B | `ad57447a…c95c618e` (integral: `ad57447a31c9743b9d40967a0824d0fee3d85848c84d3b2665d6ce59c95c618e`) |
| `orc_diag_frente_esq.png` | 1328 × 1904 px, 2.206.043 B | `895c0cd9…af09230a` (integral: `895c0cd9ae633b9a6858212f8bad0e877541cab6b8c47f2d13a13a2faf09230a`) |

## Fontes canônicas (ordem de autoridade)

1. `orc_frente.png` (frente canônica — cor e inventário)
2. `orc_costas_v2.png` (costas aprovadas no lote 1)
3. `orc_tresquartos_v2.png` (aprovada no lote 1)
4. `orc_diag_tras_dir.png` (diagonal traseira DIREITA aprovada no lote 4 parcial)
5. Autoauditoria do executor: `oficina-audit/autoauditoria-orc-diag-retrabalho.md`
   (lida antes do julgamento; NADA dela foi tomado como verdade — tudo foi re-medido)
6. Relatório do lote 4 parcial: `oficina-audit/CRITICO-ref01-lote4-tras.md`
   (especificação do retrabalho, seção 4, 9 itens + critério N2)

**Método:** leitura visual das imagens inteiras + zooms 2×/3× de cabeça, ombros/alça,
cinto, mãos e pés + medições por pixel com o mesmo método do lote anterior (máscara
de silhueta por distância ao fundo cinza, IoU alinhado por bbox em grade 500,
assimetria da faixa inferior y 0,80–0,99, amostragem de cor com filtro oliva
G > B+15, G ≥ R−15, saiote vermelho como controle interno). Validação do método:
meus números reproduzem os do Crítico anterior para os arquivos já julgados
(`tras_dir` faixa = 1,774 contra 1,78 dele; `costas_v2` = 1,017 contra 1,02 dele).
Convenção de lados, verificada contra as fontes (não assumida): em vista de FRENTE
o lado esquerdo do personagem aparece à DIREITA de quem olha (espelho: lobo à
direita na frente canônica); em vista de COSTAS o lado esquerdo aparece à ESQUERDA
(rotação de 180°: lobo à esquerda em `costas_v2`). Zooms de trabalho preservados
em `oficina-audit/tmp-critico4/` (evidência dos veredito abaixo, em especial o zoom
3× da alça).

**Severidades:** S1 = impede o uso; S2 = exige retrabalho / impede a entrada no
arsenal; S3 = desvio tolerável com registro; S4 = observação sem retrabalho.
ESP = erro da especificação anterior (não da imagem): o item como escrito está
provado errado contra as fontes; corrigir o item, não a imagem.

## 1. A refeita traseira contra os 9 itens da especificação

| Item | Exigência (seção 4 do lote 4 parcial) | Medido na refeita | Resultado |
|---|---|---|---|
| 1 | Câmera na retaguarda ESQUERDA (lado do lobo) | Lobo proeminente em primeiro plano à esquerda; ombreira de espinhos recuada à direita, parcialmente atrás da capa; rosto e pé do lado esquerdo | **PASSA** |
| 2 | Rosto em perfil parcial para a ESQUERDA; orelha esquerda visível | Zoom de cabeça: perfil esquerdo inequívoco (nariz para a esquerda, um olho, presas, listras vermelhas); orelha esquerda com brinco de argola visível | **PASSA** |
| 3 | Lobo PROEMINENTE em primeiro plano à esquerda; ombreira recuada à direita | Cabeça do lobo grande à esquerda, focinho para a esquerda, orelhas erguidas; ombreira à direita recuada, só os espigões acima da capa | **PASSA** |
| 4 | Pé viewer-ESQUERDO em perfil para a esquerda; pé viewer-direito traseiro | Zoom de pés: pé esquerdo em perfil total para a esquerda (biqueira com espigão à frente); pé direito em vista traseira (solado/calcanhar) — inversão exata de `tras_dir` | **PASSA** |
| 5 | Alça com fivela central descendo para o quadril viewer-ESQUERDO | Fivela central visível, mas a alça desce para o quadril viewer-DIREITO, com a MESMA orientação de `costas_v2` e `tras_dir` (zoom 3×: diagonal superior-esquerda → inferior-direita) | **NÃO CUMPRE como escrito — mas o item está errado (ESP-4.1, ver §3)** |
| 6 | Caveira grande do cinto à ESQUERDA; losango central; presas, argolas e pingente mantidos | Losango central mantido; presas, argolas e pingente em seta mantidos; mas a caveira grande está à DIREITA, com argolas + pingente abaixo — disposição idêntica a `costas_v2` e `tras_dir` | **NÃO CUMPRE como escrito — mas o item está errado (ESP-4.2, ver §3)** |
| 7 | Painel da capa proeminente à esquerda, abaixo da cintura até meia-canela | Painel de pele domina o dorso esquerdo, desce abaixo da cintura até meia-canela; sem D13 | **PASSA** |
| 8 | Zero bolsinhas, zero machado, corpo inteiro, fundo cinza-claro liso, tom oliva | Zero bolsinhas (cinto: presas, caveiras, correntes, cilindro — nenhuma bolsa); punhos vazios, zero machado; corpo inteiro (bbox x 195–1165, y 67–1833; margens esq 14,7%, dir 12,3%, sup 3,5%, inf 3,7%); fundo cinza-claro liso; tom oliva (N3, §4) | **PASSA** |
| 9 | Critério numérico N2 do novo par: os TRÊS, não um só | Ver §2: IoU 0,732 < 0,85 ✓; faixa 0,521 < 0,7, invertida contra `tras_dir` 1,774 ✓; pé em perfil à esquerda contra direita em `tras_dir` ✓ | **PASSA (os três)** |

## 2. N2 re-medido (par traseiro refeita × tras_dir) — os três critérios passam

| Critério N2 | Exigido | Medido por mim | Executor (para contraste) | Crítico anterior (referência) |
|---|---|---|---|---|
| (a) IoU bbox-alinhado entre as duas | < 0,85 | **0,732** | 0,745 | par anterior: 0,915 (reprovado) |
| (b) Razão dir/esq da faixa inferior (y 0,80–0,99) | um lado > 1,4 e o outro < 0,7 | refeita **0,521**; `tras_dir` **1,774** — sentidos invertidos | refeita 0,57; `tras_dir` 1,64 (método dele difere no limiar; o sentido é o mesmo) | `tras_dir` 1,78; `costas_v2` 1,02 (meu método reproduz ambos) |
| (c) Pé em perfil em lados opostos | opostos | refeita: esquerda; `tras_dir`: direita | idem | par anterior: direita nas duas (reprovado) |

Controles: IoU refeita × `costas_v2` = 0,796; IoU `tras_dir` × `costas_v2` =
0,835 — a refeita se parece com as costas retas tanto quanto a direita se parece,
ou seja, é uma diagonal genuína, não uma cópia da direita. Centroide da refeita
(0,503; 0,493) contra `tras_dir` (0,482; 0,500): massas deslocadas em sentidos
opostos, como exige um par. **N2: APROVADO nos três critérios, por medição
independente (não pela medição do executor).**

## 3. Por que os itens 5 e 6, como escritos, estão errados — e por que isso NÃO reprova a imagem

Tentei reprovar a refeita exatamente por onde o executor suspeitou (alça e caveira).
A evidência absolveu a imagem e condenou os dois itens. A confusão é uma só: a
especificação tratou itens **fixos ao corpo** como se fossem **sinais de lado da
câmera**. Sinais de câmera (lobo proeminente, direção do perfil, pé em perfil,
painel da capa) DEVEM inverter quando a câmera troca de lado — e invertem na
refeita. Itens fixos ao corpo NÃO invertem quando a câmera se move: eles apenas
ficam mais ou menos visíveis. Espelhá-los seria produzir um falso esquerdo — o
que a própria especificação proíbe ("NÃO espelhar `tras_dir`").

**ESP-4.1 — Item 5 (alça): a descida para a esquerda seria a diagonal da FRENTE,
não a das costas.** A faixa forma um laço: na frente canônica ela cruza o peito
do ombro direito do personagem para o quadril esquerdo (em coordenadas de imagem
da frente: superior-esquerda → inferior-direita); nas costas ela cruza do ombro
esquerdo para o quadril direito (em coordenadas de imagem das costas:
superior-esquerda → inferior-direita — a mesma orientação aparente, porque a
vista de costas inverte esquerda/direita). O zoom 3× da refeita mostra a alça
exatamente assim: segmento superior emergindo sob os dreads à esquerda, fivela
central, banda larga descendo para o cinto à direita — **idêntica em orientação
a `costas_v2` e a `tras_dir`**. Exigir a descida para o quadril viewer-esquerdo
é exigir, nas costas, a orientação da faixa do peito. Uma refeita que cumprisse
o item 5 como escrito estaria geometricamente errada. **Correção do item 5:
"alça com fivela central mantendo a diagonal das costas (superior-esquerda →
inferior-direita em coordenadas de imagem), descendo para o quadril
viewer-direito, como em `costas_v2`".**

**ESP-4.2 — Item 6 (caveira): nenhuma fonte sustenta a caveira grande à esquerda
numa vista traseira.** Auditoria vista por vista (verificação nova N4, §6): o
conjunto caveira grande + presa longa + argolas + pingente em seta aparece à
DIREITA de quem olha em **todas** as cinco vistas existentes — frente canônica,
`costas_v2`, `tras_dir`, refeita e frontal esquerda (zoom de cinto conferido).
Pior: o cânone contradiz a si mesmo sobre o lado corporal do conjunto (na frente
ele cai no lado esquerdo do personagem; nas costas, no direito), de modo que
não existe "lado corporal canônico" a impor — a única regra consistente com
todas as fontes é a convenção de imagem (à direita nas vistas traseiras), que a
refeita segue. Se a refeita pusesse a caveira à esquerda, o conjunto traseiro
ficaria internamente inconsistente (`costas_v2` direita, `tras_dir` direita,
`tras_esq` esquerda) — pior para o modelador do que a situação atual.
**Correção do item 6: "caveira grande do cinto à DIREITA de quem olha, como em
`costas_v2` e `tras_dir`; losango central; presas, argolas e pingente mantidos".
O item 6 como escrito deve ser retirado das exigências de retrabalho, não
cobrado da imagem.**

Registro honesto do que isto significa: a refeita cumpre 7 dos 9 itens como
escritos e os 2 restantes como corrigidos pela evidência. Não há benevolência
aqui — há prova contra as fontes de que os 2 itens estavam errados. Se o
executor ou o Mestre discordarem das correções ESP-4.1/ESP-4.2 e exigirem
cumprimento literal, o retrabalho terá de inverter alça e caveira — e este
Crítico registra desde já que essa versão seria geometricamente pior (faixa do
peito nas costas; cinto traseiro inconsistente consigo mesmo).

## 4. N1 e N3 nas duas imagens

**N1 — Pureza do 3/4 traseiro (refeita): PASSA.** Rosto SÓ em perfil parcial
(nenhuma face frontal); capa dominando o dorso e abaixo da cintura; pés
apontando para longe do observador (perfil para a esquerda-longe + traseiro com
calcanhar/solado). **N1 não reprova a refeita.**

**N3 — Tom medido por amostragem anatômica com filtro oliva (as duas): PASSA.**

| Imagem | Braço viewer-dir (mediana RGB, sat) | Braço viewer-esq | Saiote vermelho (controle) |
|---|---|---|---|
| `frente` (autoridade D5) | (66,53,25) sat 0,621 — caixa sombreada, n pequeno | (113,98,67) sat 0,407 | (158,33,27) |
| `costas_v2` | (114,106,56) sat 0,509 | (112,103,55) sat 0,509 | (158,27,23) |
| `tras_dir` | (75,61,30) sat 0,600 | (85,73,35) sat 0,588 | (163,32,27) |
| **refeita** | (108,95,46) sat 0,574 | (85,76,42) sat 0,506 | (159,29,24) — Δ=(1,4,3) contra a frente; Δ=(1,2,1) contra `costas_v2` |
| `tresquartos_v2` | (105,92,46) sat 0,562 | (72,60,34) sat 0,528 | (161,40,33) |
| **frentesq** | (116,103,59) sat 0,491 | (91,79,41) sat 0,549 | (164,40,33) — Δ=(6,7,6) contra a frente, mas Δ=(3,0,0) contra `tresquartos_v2` |

Leitura: as duas imagens estão na família oliva (G > B com folga em todas as
amostras), sem o desvio D5 (tom claro) e sem mudança de matiz. O vermelho do
saiote da refeita é praticamente idêntico ao canônico. O vermelho da frontal
esquerda desvia um pouco da frente canônica, mas **reproduz exatamente o da
`tresquartos_v2` aprovada** — desvio já consagrado na família 3/4, não um desvio
novo (S4, sem retrabalho). Ressalva de método herdada do lote anterior: caixas
anatômicas fixas capturam poucos pixels oliva puros onde armadura e pele se
misturam (ex.: `tras_dir` braço viewer-dir n=355); os deltas são pequenos e não
justificam reprovação. **N3: APROVADO nas duas.**

## 5. A frontal esquerda — passa no checklist (b), reprova como entrada nova

**Checklist (b), item a item:**

| Exigência | Medido em `orc_diag_frente_esq.png` |
|---|---|
| Anti-espelho: lobo à DIREITA de quem olha, ombreira à ESQUERDA, NÃO espelhar | **PASSA.** Lobo grande à direita; ombreira de espinhos à esquerda. O defeito SYM que reprovou o par frontal anterior NÃO se repete — crédito ao executor neste ponto. |
| Giro de fato diagonal | **PASSA em isolamento.** Tronco em 3/4 (não frontal reto: IoU com a frente canônica = 0,606, bem distinto); rosto em 3/4 voltado para a esquerda do personagem (direita de quem olha); ombros assimétricos. É uma diagonal frontal esquerda genuína. |
| Coerência dos pés com o giro | **PASSA em isolamento.** Pé viewer-direito (pé esquerdo do personagem, lado próximo) em perfil total apontando para a direita; pé viewer-esquerdo (pé direito, lado afastado) em vista frontal-superior. Postura de 3/4 esquerdo com pés desencontrados, idêntica à aprovada `tresquartos_v2` — o que nos leva ao defeito abaixo. |
| Inventário | **PASSA.** Zero bolsinhas, zero machado (punhos fechados vazios, palmas não voltadas para a câmera); colar com caveira e presas, losango do cinto, caveiras do cinto, cilindro e joelheiras — todo o kit canônico presente. Braçadeira esquerda conferida em zoom: placas de metal com rebites presentes (não falta a braçadeira; a suspeita não se confirmou). |
| Corpo inteiro, fundo | **PASSA.** Corpo inteiro (bbox x 158–1105, y 65–1843; margens esq 11,9%, dir 16,8%, sup 3,4%, inf 3,2%); fundo cinza-claro liso, sem texto ou marca. |

**O defeito que o checklist (b) não pega — e a verificação nova N5 pegou:**

| Código | Sev. | Defeito e evidência medida |
|---|---|---|
| DUP-4.3 | **S2** | **A "diagonal frontal esquerda nova" é a `tresquartos_v2` de novo.** Silhueta bbox-alinhada frontal-esquerda × `tresquartos_v2`: **IoU 0,960** — mais parecida com a vista aprovada do lote 1 do que `tras_dir` é de `costas_v2` (0,835). E não é só silhueta: TODAS as âncoras coincidem — lobo à direita, ombreira à esquerda, rosto 3/4 para a direita, colar, cinto (caveira grande à direita, duas caveirinhas centrais, cilindro à esquerda), pé esquerdo em perfil para a direita, pé direito frontal, pernas e joelheiras na mesma abertura. As diferenças são de re-renderização (rosto um pouco mais frontal, dreads rearranjados), não de ângulo. O rótulo "diagonal frontal esquerda" é verdadeiro; a alegação "nova" é falsa. Como entrada do arsenal ela não acrescenta nenhum ângulo de modelagem — e manter as duas lado a lado cria duas referências concorrentes para o mesmo ângulo, com detalhes divergentes (ex.: o rosto mais frontal aqui contra o mais virado lá), o que é custo real para o modelador. |

**Disposição recomendada (não é veredito, é consequência):** NÃO instalar a
frontal esquerda como diagonal nova. A vaga da diagonal frontal esquerda já está
ocupada — pela própria `tresquartos_v2`, aprovada no lote 1. Se o arsenal quer
um par frontal, a vaga aberta é a diagonal frontal DIREITA (parceira), não mais
uma esquerda. Se o executor preferir esta renderização à antiga, a troca teria
de ser por SUBSTITUIÇÃO explícita de `tresquartos_v2` (decisão dele/Mestre),
nunca por adição — e este Crítico não a recomenda, porque o ângulo do rosto
difere e a vista aprovada já cumpre a função.

## 6. Verificações novas desta rodada (escalada APR-01)

Registradas como verificações permanentes do checklist pré-Crítico a partir
deste lote (a bateria anterior tinha N1, N2, N3; esta rodada adiciona DUAS):

- **N4 — Auditoria de lateralização por vista cruzada.** Para cada item do kit
  fixo ao corpo (conjunto da caveira do cinto, diagonal da alça, painel da capa,
  placas das braçadeiras), registrar o lado em imagem em TODAS as vistas
  aprovadas/canônicas antes de exigir um lado na vista nova — e exigir da vista
  nova a coerência com a sua família (traseiras com traseiras, frontais com
  frontais), nunca um espelho postulado. Foi N4 que provou ESP-4.1 e ESP-4.2:
  alça e caveira são viewer-direita em todas as traseiras existentes, e a
  frente contradiz as costas sobre o lado corporal da caveira (logo, não há
  lado corporal canônico a impor). Sem N4, este lote teria reprovado uma imagem
  certa por dois itens errados — ou aprovado uma imagem errada no próximo.
- **N5 — Auditoria de novidade angular.** Toda candidata a entrada nova no
  arsenal deve ter seu IoU bbox-alinhado medido contra TODAS as vistas já
  aprovadas do mesmo personagem; IoU > 0,90 contra uma vista aprovada do mesmo
  lado = ângulo duplicado, não entrada nova (reprova como adição, qualquer que
  seja a qualidade do render). Foi N5 que pegou DUP-4.3: a frontal esquerda tem
  IoU 0,960 com `tresquartos_v2`. Contraponto: a refeita traseira passa em N5
  (IoU 0,732 com `tras_dir`; 0,796 com `costas_v2`) — ângulo novo de verdade.

## 7. Suspeitas da autoauditoria — veredito do Crítico (todas re-medidas)

1. **Caveira grande do cinto na refeita:** CONFIRMADA à direita — mas NÃO é
   defeito (ESP-4.2, §3). A suspeita do executor estava certa no fato e errada
   na implicação: o item 6 como escrito é que está errado.
2. **Descida da alça na refeita:** RESOLVIDA a favor da imagem — o trajeto é
   inequívoco no zoom 3× (superior-esquerda → inferior-direita, descida para o
   quadril viewer-direito, como `costas_v2`/`tras_dir`); a exigência de descida
   para a esquerda é o erro (ESP-4.1, §3). A dificuldade de leitura do executor
   é compreensível (o trecho superior some sob dreads e capa), mas o trecho
   visível basta.
3. **Frontal esquerda, ângulo e pés:** PARCIALMENTE CONFIRMADA e AGRAVADA por
   outro motivo — o tronco é de fato um 3/4 suave (mais frontal que
   `tresquartos_v2`) e os pés são coerentes com o giro esquerdo; mas o ângulo
   já existe no arsenal (DUP-4.3, S2). O executor desconfiou do giro; o
   problema real é a duplicidade.
4. **Tom (N3) nas duas:** MEDIDO e APROVADO nas duas (§4).
5. **Coerência interna do conjunto:** APROVADA para a refeita (nenhum acessório
   novo, nenhuma característica mudada: dreads com contas, topete com faixa
   vermelha/dourada, brinco, listras, braçadeiras, joelheiras, botas com
   espigão — tudo conforme as fontes). Para a frontal esquerda, o kit também é
   coerente — o problema dela é outro (duplicidade, não incoerência).
6. **N1 na refeita:** CONFIRMADO a favor da imagem (§4).

**Caça aos modos de falha dos lotes anteriores — resultado:**

| Modo | Refeita | Frontal esquerda |
|---|---|---|
| D10 espelhamento / SYM duplicação de lado | NÃO PRESENTE (lado oposto genuíno, N2 passa nos três) | Espelhamento NÃO PRESENTE; mas duplicação de ângulo PRESENTE (DUP-4.3) |
| D9/D11 bolsinhas | ZERO | ZERO |
| D13 capa curta | NÃO PRESENTE (painel até meia-canela) | N/A (vista frontal; capa atrás dos ombros, conforme) |
| D3/D4 fusões e dígitos | NÃO PRESENTE (punhos fechados, sem dígito extra; botas com espigão nos dois pés) | NÃO PRESENTE (punhos fechados, sem dígito extra) |
| D5 tom claro | NÃO PRESENTE (família oliva, N3) | NÃO PRESENTE |
| D15 palmas para a frente | NÃO PRESENTE | NÃO PRESENTE |

## 8. Outras observações S4 (sem retrabalho)

- **Pé afastado da refeita um pouco mais alto:** o pé viewer-direito (afastado)
  termina em y relativo 0,911 contra 0,963 do pé próximo (diferença 0,052),
  contra 0,036 em `tras_dir` e 0,002 em `costas_v2`. Explicado pela postura
  mais aberta da refeita (bbox 971 px de largura contra 921 de `tras_dir`) e
  pelo pé afastado virado para fora (solado visível): bota completa, perna
  conectada, sem flutuação. Não é defeito; o modelador deve usar `tras_dir`
  para a planta do pé afastado.
- **Ombreira direita recuada na refeita:** a ombreira de espinhos do lado
  afastado aparece só parcialmente acima da capa — oclusão esperada em 3/4
  traseiro esquerdo; usar `tras_dir`/`costas_v2` para o detalhe dela.
- **Tom levemente mais saturado num braço da refeita** (sat 0,574 contra 0,509
  de `costas_v2`): dentro da variação já registrada no lote anterior (DEF-4.2),
  sem mudança de matiz. S4.
- **Fundo da frente canônica é preto e a pose inclui o machado:** a razão de
  faixa da frente (31,985) não é comparável com as vistas de fundo cinza —
  limitação de método registrada, sem efeito nos veredito (a frente não entra
  em nenhum critério N2 deste lote).

## Veredito

**orc_diag_tras_esq_refeita.png: APROVADA**
— Substitui a reprovada `orc_diag_tras_esq.png` (SUBSTITUIR, não manter ao
lado: duas "esquerdas" perpetuariam a ambiguidade). O par traseiro FECHA:
`tras_esq` refeita + `tras_dir` formam um par genuíno dir/esq (N2 nos três
critérios, por medição independente). Os itens 5 e 6 da especificação anterior
ficam corrigidos por ESP-4.1/ESP-4.2 — a imagem não deve ser refeita por causa
deles.

**orc_diag_frente_esq.png: REPROVADA (como entrada nova no arsenal)**
— Não por espelho (não há), nem por inventário, corpo ou fundo (todos passam),
mas por duplicidade: é a `tresquartos_v2` re-renderizada (IoU 0,960, todas as
âncoras iguais). NÃO entra no arsenal como diagonal nova. A diagonal frontal
esquerda do arsenal continua sendo a `tresquartos_v2`; a vaga aberta no par
frontal é a diagonal direita.

**LOTE 4 RETRABALHO: PARCIALMENTE APROVADO** — a traseira esquerda fecha o par
traseiro; a frontal esquerda não entra.

Motivo em uma frase: a refeita traseira é a diagonal esquerda que faltava (e
provou errados dois itens da especificação no caminho), enquanto a frontal
esquerda é uma vista que o arsenal já tem — corrigir o espelho não basta quando
o ângulo já existe.
