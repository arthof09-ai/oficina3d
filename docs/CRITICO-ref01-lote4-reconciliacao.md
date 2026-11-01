# CRÍTICO VISUAL DE RECONCILIAÇÃO — REF-01 lote 4 do Orc (3º avaliador)

**Papel:** Crítico Visual sênior de RECONCILIAÇÃO, convocado por ordem do Mestre como
terceiro avaliador, mais rigoroso que os dois anteriores. Missão (APR-02): auditar OS
DOIS CRÍTICOS, não só as imagens — nenhum dos dois tem presunção de acerto; o que não
for re-medido por mim não vale.
**Data:** 01/11/2026. **Escopo:** as duas imagens contestadas do lote 4
(`orc_diag_tras_esq_refeita.png`, `orc_diag_frente_esq.png`), os dois relatórios em
disputa, e o destino da `orc_diag_tras_dir.png` já aprovada.
**A palavra final de fidelidade artística é do Mestre.**

**Resumo do desfecho:** o Crítico 1 acertou os dois vereditos (refeita aprovada,
frontal reprovada por duplicidade) e errou parte da justificativa geométrica do
ESP-4.1. O Crítico 2 acertou os FATOS que mediu (alça não espelhada, caveira à
direita) e errou tudo o que decidiu com eles: inventou uma regra (NV-1) que o
próprio cânone viola, aplicou-a com dois pesos (S2 na imagem nova, "desvio
tolerado" na aprovada) e aprovou uma duplicata provada sem executar a auditoria
de novidade que a rodada anterior tinha criado. Detalhes e provas abaixo.

## 0. Arquivos e hashes conferidos

SHA-256 recalculados por mim nesta VM — todos batem com os registros dos dois
relatórios e do registro pendente:

| Arquivo | Dimensões | Bytes | SHA-256 (prefixo…sufixo) |
|---|---|---|---|
| `orc_frente.png` (autoridade) | 1280 × 1820 | 2.316.006 | `30c0f83d…903b6c` |
| `orc_costas_v2.png` (autoridade) | 1328 × 1904 | 2.090.890 | `09890d74…7a41362` |
| `orc_tresquartos_v2.png` (aprovada lote 1) | 1328 × 1904 | 2.164.479 | `7c9d9465…8022ad84` |
| `orc_diag_tras_dir.png` (aprovada lote 4) | 1328 × 1904 | 2.277.440 | `acb515d2…7372250b` |
| `orc_diag_tras_esq.png` (reprovada original) | 1328 × 1904 | 2.128.241 | `6d0b0b35…37a6ca26413` |
| `orc_diag_tras_esq_refeita.png` (CONTESTADA) | 1328 × 1904 | 2.274.898 | `ad57447a…c95c618e` |
| `orc_diag_frente_esq.png` (CONTESTADA) | 1328 × 1904 | 2.206.043 | `895c0cd9…af09230a` |

Nenhuma das duas contestadas é outro arquivo disfarçado: julguei os bytes certos.

## 1. Re-medições próprias (método e números)

**Método (o mesmo declarado nos relatórios, reproduzido do zero):** máscara de
silhueta por distância RGB à mediana dos quatro cantos (fundo); IoU com as duas
silhuetas recortadas pelo bbox e redimensionadas a grade 500 × 500 (NEAREST);
faixa inferior = linhas 0,80–0,99 da altura do bbox, razão dir/esq de pixels de
silhueta nas metades do bbox; solas = pixel mais baixo da máscara em cada metade
do bbox. Rodei com TRÊS limiares de fundo (25/35/45) para medir a estabilidade:
nenhuma conclusão muda. Posições do cinto lidas em recortes com **grade impressa
de 0,1** sobre a largura total da imagem (precisão ±0,015) — método que nenhum
dos dois usou e que se mostrou necessário (ver §2, item C2-2). Trajeto da alça,
lados de lobo/ombreira/rosto/pés lidos por mim em zooms 2× das imagens inteiras.

### 1.1 IoU bbox-alinhado (grade 500)

| Par | Meu valor (limiar 35) | Faixa (25–45) | Quem mediu antes |
|---|---|---|---|
| refeita × `tras_dir` | **0,734** | 0,730–0,738 | C1: 0,732 · executor: 0,745 · **C2: 0,68** |
| refeita × `costas_v2` | **0,797** | 0,793–0,799 | C1: 0,796 |
| `tras_dir` × `costas_v2` | **0,835** | 0,832–0,841 | C1: 0,835 · C0: 0,765* |
| `tras_esq` original × `tras_dir` | **0,910** | 0,904–0,915 | C0: 0,915 |
| **`frente_esq` × `tresquartos_v2`** | **0,962** | **0,954–0,969** | C1: 0,960 |
| `frente_esq` × `frente` | **0,628** | 0,600–0,655 | C1: 0,606 |

*O 0,765 do C0 era IoU bruto sem alinhamento por bbox; alinhado, reproduzo 0,835 —
a conclusão dele não muda.

### 1.2 Faixa inferior (razão dir/esq) e centroides

| Imagem | Faixa dir/esq (minha) | C1 | C0 |
|---|---|---|---|
| refeita | **0,580** (< 0,7 ✓) | 0,521 | — |
| `tras_dir` | **1,601** (> 1,4 ✓) | 1,774 | 1,78 |
| `costas_v2` | **1,010** | 1,017 | 1,02 |
| `tras_esq` original | **1,596** (mesmo sentido da dir ✗) | — | 1,75 |

O par refeita × `tras_dir` está INVERTIDO no meu método também (0,580 contra
1,601). As diferenças absolutas entre métodos (limiar e definição da faixa) não
tocam nenhum critério: N2 passa nos três itens com folga em todas as medições já
feitas por quatro medidores (executor, C0, C1 e eu).

Centroide da refeita: o meu, relativo ao bbox, é (0,487; 0,493); convertido ao
referencial da imagem dá x = 0,503 — exatamente o (0,503; 0,493) do Crítico 1.
Os números dos dois lados concordam quando se identifica o referencial (o C1
não declarou o dele; ver lição N8 no §8).

### 1.3 Solas (pixel mais baixo por metade do bbox; 1,000 = base do bbox)

| Imagem | Sola esq | Sola dir | Δ (pé afastado acima) |
|---|---|---|---|
| refeita | 0,999 | 0,945 | **0,054** |
| `tras_dir` (aprovada) | 0,960 | 0,999 | **0,039** |
| `costas_v2` (reta) | 0,998 | 0,999 | **0,001** |

Os três medidores concordam na refeita: C1 mediu 0,052, eu 0,054, C2 "≈0,06".
E a série mostra o padrão: vista reta Δ≈0; diagonais Δ 0,04–0,05 — o deslocamento
acompanha a PROFUNDIDADE da postura diagonal (o pé afastado está mais longe da
câmera e projeta mais alto), não flutuação. No zoom dos pés da refeita: bota
direita completa, perna conectada, sola voltada para a câmera (pé afastado
virado para fora) — não há pé flutuando no ar.

### 1.4 Posições do cinto com grade impressa (x relativo à largura da imagem)

| Vista | Fivela da cintura | Losango | Caveira grande |
|---|---|---|---|
| `frente` (canônica) | ≈ 0,455 | ≈ 0,45 | **≈ 0,57** |
| `costas_v2` (canônica) | ≈ 0,445 | ≈ 0,46 | **≈ 0,56** |
| **refeita** | ≈ 0,55 | ≈ 0,58 | **≈ 0,64** |
| `tras_dir` | ≈ 0,42 (zoom s/ grade) | topo cortado | ≈ 0,50 — a mais à direita do conjunto (+0,08 sobre a fivela) |

Leitura: em TODAS as vistas a caveira grande é o elemento mais à direita do
conjunto do cinto, +0,09 a +0,13 à direita da fivela. Na refeita ela NÃO está
"longe" das irmãs: está deslocada para a direita junto com o conjunto inteiro,
como manda uma vista 3/4 (o centro do tronco projeta deslocado). O Crítico 2
publicou fivela ≈ 0,63, losango ≈ 0,60 e caveira ≈ 0,76 para a refeita: a grade
mostra 0,55 / 0,58 / 0,64 — a caveira dele está errada por **+0,12 da largura da
imagem**, e o espaçamento caveira−losango dele (0,16) é quase o triplo do real
(0,06). A ORDEM que ele afirmou (caveira à direita do losango) está certa; os
números decisivos dele, não.

### 1.5 Alça e sinais de câmera (leitura visual minha, zooms 2×)

- **Frente canônica:** a alça cruza o peito na diagonal superior-esquerda →
  inferior-direita, com DUAS fivelas visíveis sobre a diagonal, descendo ao
  quadril viewer-direito. Lobo à direita; ombreira à esquerda.
- **`costas_v2`:** a faixa larga emerge sob os dreads à esquerda do centro,
  fivela grande no meio do dorso (x ≈ 0,48) e desce para o cinto no lado
  viewer-DIREITO: **superior-esquerda → inferior-direita**, a mesma orientação
  aparente da frente.
- **Refeita:** idem — emerge sob os dreads, fivela dorsal à direita do centro
  (x ≈ 0,61 no zoom do dorso), desce ao cinto viewer-direito. Lobo proeminente
  em primeiro plano à ESQUERDA (focinho para a esquerda), rosto do Orc em
  perfil para a esquerda, ombreira recuada à direita, pé viewer-esquerdo em
  perfil para a esquerda, pé viewer-direito traseiro. Todos os sinais de
  câmera invertidos em relação a `tras_dir`, como exige uma diagonal esquerda
  genuína — e o N2 numérico (§1.1/1.2) confirma.
- **`frente_esq` × `tresquartos_v2` a olho:** mesma pose e mesmo ângulo — lobo
  à direita em perfil para a direita, ombreira à esquerda, alça na mesma
  diagonal com as fivelas nos mesmos lugares, losango central, caveira grande
  viewer-direita, caveirinhas gêmeas centrais, pé viewer-direito em perfil
  para a direita, pé viewer-esquerdo frontal, mesma abertura das pernas. As
  diferenças são de re-renderização (rosto um pouco mais frontal, dreads e
  franja rearranjados), não de ângulo.

## 2. Meta-auditoria — afirmações decisivas dos dois Críticos × meu veredito

| # | Afirmação | Autor | Meu veredito | Minha prova |
|---|---|---|---|---|
| C1-1 | N2 da refeita passa: IoU 0,732 < 0,85 | C1 | **CONFIRMADA** | meu IoU 0,734 (0,730–0,738) |
| C1-2 | Faixa invertida: refeita 0,521 × `tras_dir` 1,774 | C1 | **CONFIRMADA** (sentido e critérios) | meu 0,580 × 1,601; quatro medidores, mesma conclusão |
| C1-3 | ESP-4.2 (fato): caveira grande viewer-direita em TODAS as vistas | C1 | **CONFIRMADA e ampliada** | grade: frente 0,57, costas 0,56, refeita 0,64; + frente_esq e tresquartos a olho: 6/6 vistas |
| C1-4 | ESP-4.1 (fato): alça das costas desce sup-esq → inf-dir em costas_v2/tras_dir/refeita | C1 | **CONFIRMADA** | zoom próprio nas três (§1.5) |
| C1-5 | ESP-4.1 (justificativa): "a descida à esquerda seria a diagonal da FRENTE" | C1 | **REFUTADA como mecanismo** | §4: faixa contínua exige diagonais OPOSTAS frente×costas; o cânone viola isso nas duas canônicas — a conclusão do C1 se sustenta por outro fundamento (precedente do C0 + N4), não por este |
| C1-6 | DUP-4.3: `frente_esq` é `tresquartos_v2` re-renderizada, IoU 0,960 | C1 | **CONFIRMADA** | meu IoU 0,962 (0,954–0,969) + âncoras idênticas conferidas a olho (§1.5) |
| C1-7 | Pé afastado da refeita: Δ0,052, bota completa, S4 | C1 | **CONFIRMADA** | meu Δ0,054; zoom dos pés: sola visível, perna conectada |
| C1-8 | Centroide da refeita (0,503; 0,493) | C1 | **CONFIRMADA** após identificar o referencial | meu bbox-relativo 0,487 ≡ 0,503 em coordenadas de imagem |
| C2-1 | SYM-5.1 (fato): alça da refeita não espelhada, desce ao quadril viewer-direito | C2 | **CONFIRMADA como fato; REFUTADA como defeito** | é o mesmo fato do ESP-4.1; a regra que o condena (NV-1) é inválida (§3a) |
| C2-2 | SYM-5.2 (fato + números): caveira à direita, x ≈ 0,76 × losango ≈ 0,60; fivela ≈ 0,63 | C2 | **Fato CONFIRMADO; números REFUTADOS; defeito REFUTADO** | grade: caveira 0,64 (erro dele +0,12), fivela 0,55, losango 0,58 (§1.4) |
| C2-3 | NV-1: "exigir inversão entre frente e costas" | C2 | **REFUTADA** | o par canônico frente × costas_v2 NÃO inverte a caveira (0,57 e 0,56, ambas à direita); para a alça, a inversão condenaria costas_v2 junto (§4) — a regra reprova a autoridade, logo não governa |
| C2-4 | N2 dele: IoU refeita × tras_dir = 0,68 | C2 | **NÃO REPRODUZ** | 0,730–0,738 em três limiares (C1: 0,732; executor: 0,745); erro −0,05, sem efeito no critério |
| C2-5 | Faixa "0,521/0,569" invertida | C2 | **PARCIALMENTE CONFIRMADA** | 0,521 bate com C1 (meu: 0,580); 0,569 só se lê como razão INVERTIDA de tras_dir (1/1,756) — convenções misturadas na mesma linha; a inversão em si confirma-se no meu método |
| C2-6 | POS-5.1: pé viewer-direito fora do solo, sola ≈ 0,06 acima (S3) | C2 | **Medida CONFIRMADA; severidade REFUTADA** | meu Δ0,054, mas a `tras_dir` aprovada tem Δ0,039 e as costas retas Δ0,001: é profundidade de postura, não flutuação; o limiar NV-2 dele (> 0,04) está descalibrado para diagonais. Reclassifico S4 |
| C2-7 | CAP-5.1: painel da capa até o alto da canela (S4) | C2 | **CONFIRMADA como observação S4** | na refeita inteira, a ponta do painel proeminente fica na altura do joelho/alto da canela; a redação do item 7 do C1 ("até meia-canela — PASSA") é generosa. Sem retrabalho |
| C2-8 | `frente_esq` APROVADA (anti-espelho, pés, inventário ok) | C2 | **REFUTADA** | não executou a auditoria de novidade N5 da rodada anterior: IoU 0,962 com `tresquartos_v2` = duplicata (DUP-4.3). O checklist dele passa; a entrada, não |
| C2-9 | ANG-5.1: giro de tronco fraco ~20° (S3) | C2 | **NÃO MEDIDA** (sem método angular declarado por nenhum dos dois) | irrelevante após o DUP-4.3 |
| C0-1 | Precedente do relatório original: alça descer para o mesmo lado frente×costas é "convenção já estabelecida… não se cobra deste lote o que a autoridade já consagrou" | C0 | **CONFIRMADA — é o precedente que decide o §3a** | e registro: os itens 5/6 da spec do próprio C0 contradizem a análise do próprio C0; a contradição nasceu na especificação, não nas imagens nem nos Críticos seguintes |

## 3. Julgamento item a item

### 3(a). ESP-4.1/ESP-4.2 (Crítico 1) × SYM-5.1/SYM-5.2 e NV-1 (Crítico 2) — a regra do kit fixo ao corpo

**Quem governa é a coerência com a família das traseiras (N4 do Crítico 1). A
NV-1 do Crítico 2 está refutada. Quem errou foi o Crítico 2 — no regra, na
aplicação e nos números; o Crítico 1 acertou a decisão com uma justificativa
geométrica imperfeita.**

Três fundamentos, todos medidos por mim:

1. **A NV-1 reprova o próprio cânone.** A regra manda "exigir inversão entre
   frente e costas" nas posições de fivela, losango e caveira. Mas o par de
   autoridade — frente canônica × `costas_v2` — NÃO inverte a caveira: grade
   0,57 na frente e 0,56 nas costas, à direita nas duas (§1.4). Uma regra que a
   vista canônica de costas reprova não pode reprovar a candidata que a imita.
   Aplicada com consistência, a NV-1 reprovaria 3 das 5 vistas traseiras/
   frontais existentes (`costas_v2`, `tras_dir`, refeita) — **o tamanho do
   erro do Crítico 2 é o arsenal traseiro inteiro**, não uma imagem.
2. **O precedente já existia e era do autor da especificação.** O Crítico
   original (lote 4 parcial) viu o mesmo traço na `tras_dir` e nas costas,
   registrou que ele é "geometricamente estranho" e decidiu expressamente:
   convenção consagrada pela autoridade, não cobrável do lote. Os itens 5/6 da
   spec dele contradizem essa análise (exigem o espelho que a análise
   desculpa). O Crítico 1 resolveu a contradição a favor da análise e das
   fontes; o Crítico 2 resolveu-a a favor da letra dos itens — e mesmo assim
   só contra a imagem nova (ver §3c). Entre as duas resoluções, só a do
   Crítico 1 é coerente.
3. **A física não salva nenhum dos lados — e é por isso que ela não governa**
   (prova completa no §4): para uma faixa contínua, frente e costas deveriam
   mostrar diagonais opostas; o cânone mostra a mesma nas duas. O Crítico 1
   escreveu que a descida à esquerda nas costas "seria a diagonal da frente" —
   isso está errado como mecanismo (a descida à esquerda nas costas seria
   justamente o espelho fisicamente esperado de uma faixa contínua). O acerto
   do Crítico 1 é a CONCLUSÃO (corrigir os itens 5/6, manter a orientação da
   família), sustentada pelos fundamentos 1 e 2 — não pela geometria que ele
   invocou. Registro o erro dele com o tamanho certo: é um erro de
   justificativa, sem efeito no veredito, mas que induziria um leitor futuro a
   crer que a física apoia a orientação da família. Não apoia; quem apoia é o
   cânone.

**Disposição:** ESP-4.1 e ESP-4.2 ficam de pé como correções da especificação
(itens 5/6 reescritos como o Crítico 1 propôs). SYM-5.1 e SYM-5.2 são fatos
verdadeiros promovidos a defeitos por uma regra inválida: **anulam-se como
defeitos**. NV-1 é **retirada** do checklist (substituída por N7, §8).

### 3(b). DUP-4.3 (Crítico 1) × aprovação da frontal (Crítico 2)

**O Crítico 1 está certo e o Crítico 2 está errado, por omissão mensurável.**

Meu IoU bbox-alinhado `frente_esq` × `tresquartos_v2` = **0,962** (0,954–0,969
em três limiares) — acima do limiar de duplicidade do N5 (0,90) e acima até do
IoU entre `tras_dir` e `costas_v2` (0.835), que todos concordam serem ângulos
DIFERENTES. Some-se a leitura âncora a âncora (§1.5): lobo, ombreira, alça,
cinto, pés e postura coincidem um a um. A frontal esquerda é a `tresquartos_v2`
re-renderizada, não um ângulo novo.

O Crítico 2 aprovou a imagem com um checklist que ela de fato passa
(anti-espelho, pés, inventário, fundo) — e **não executou a auditoria de
novidade N5**, criada na rodada imediatamente anterior exatamente para este
caso e registrada como pendência. Aprovar como "nova" uma vista cuja novidade
ninguém mediu é o erro processual central desta disputa. O S3 dele (ANG-5.1,
giro fraco) fica sem objeto: o problema da imagem não é o giro ser fraco, é o
ângulo já existir.

Registro lateral, resolvendo o "ponto a reconciliar" do registro pendente:
pela minha leitura das âncoras, a `tresquartos_v2` mostra o lado esquerdo do
personagem proeminente (lobo grande à direita de quem olha, rosto virado para
esse lado) — ou seja, ela É a diagonal frontal esquerda do arsenal, como
concluiu o Crítico 1. **A vaga aberta no par frontal é a diagonal frontal
DIREITA.**

### 3(c). A incoerência do Crítico 2 com a tras_dir

**Procede — e é pior do que o Adendo 2 descreveu.** O Crítico 2 manteve a
`tras_dir` aprovada "com o desvio anotado" pelo mesmo traço que valeu S2 à
refeita. Mas a NV-1 dele não atinge só a `tras_dir`: atinge a `costas_v2`, a
autoridade do lote 1 sobre a qual TODAS as traseiras se apoiam — e ele nem a
menciona. Um mesmo traço não pode ser, simultaneamente, defeito S2 na imagem
submetida e desvio tolerável em duas imagens aprovadas, uma delas canônica.
Isso não é rigor; é dois pesos com a mesma régua.

**Destino da `tras_dir` sob a MINHA regra final:** nenhum. Sob a regra que
governa (família das traseiras), o traço da `tras_dir` não é desvio — é a
convenção. A aprovação dela fica **mantida sem ressalva**, e a anotação de
"desvio" do relatório v2 deve ser riscada quando o registro for aplicado.
Declaro o contrafactual para não deixar dúvida: se a NV-1 tivesse vencido, a
consistência obrigaria a re-julgar e reprovar `tras_dir` E `costas_v2` juntas
— foi esse custo, invisível no relatório do Crítico 2, que a regra dele
escondeu.

### 3(d). Itens menores

- **POS-5.1 (C2, pé fora do solo, S3):** medida verdadeira (Δ 0,052–0,06 por
  três medidores; meu 0,054), interpretação errada. A série costas retas
  Δ0,001 → `tras_dir` Δ0,039 → refeita Δ0,054 mostra o efeito da profundidade
  da postura diagonal; no zoom, a bota está completa, conectada e com a sola
  voltada à câmera. **Reclassifico para S4**, fundido à observação que o
  Crítico 1 já tinha feito. O limiar NV-2 do Crítico 2 (> 0,04 = pé fora do
  solo) fica **descalibrado para vistas diagonais**: por 0,001 ele não
  reprovou a própria `tras_dir` que ele manteve aprovada.
- **CAP-5.1 (C2, capa até o alto da canela, S4):** **confirmada** como
  observação. A ponta do painel proeminente da refeita fica na altura do
  joelho/alto da canela, e a frase do item 7 do Crítico 1 ("até meia-canela —
  PASSA") é generosa. S4, sem retrabalho: a função do painel (dominar o dorso
  esquerdo abaixo da cintura) está cumprida e as irmãs variam na mesma faixa.
- **S4s do Crítico 1** (ombreira afastada ocluída pela capa; braço da refeita
  com saturação 0,574 × 0,509 de `costas_v2`): a oclusão eu confirmei a olho
  no zoom do dorso; a saturação eu **não re-medi** (amostragem N3 não era
  decisiva para nenhum veredito) — fica como S4 registrado, sem efeito.

## 4. Verificação nova desta rodada (escalada APR-01) — o kit como objeto 3D único

Nenhum dos dois Críticos tratou o cinto e a alça como objetos físicos únicos
projetados de 5 ângulos. Fiz as duas contas:

**O cinto como anel rígido.** Atribuo a cada peça um azimute φ ao redor da
cintura (0° = centro da frente; + no sentido do lado esquerdo do personagem).
Pela grade (§1.4): na FRENTE, a caveira grande está à direita de quem olha =
quadrante frontal-esquerdo do personagem → φ ≈ +50°. Nas COSTAS (`costas_v2`,
`tras_dir`, refeita), ela está à direita de quem olha = quadrante
traseiro-DIREITO do personagem → φ ≈ 220°. Uma caveira rígida única não pode
estar em φ ≈ +50° e φ ≈ 220° ao mesmo tempo (Δφ ≈ 170°): **as vistas geradas
não retratam um cinto rígido único — cada vista re-renderiza o motivo na mesma
disposição de imagem.** Logo, qualquer regra derivada de projeção de corpo
rígido (a NV-1 é uma) é inaplicável a este arsenal por construção. A única
regra consistente com as 6 vistas existentes é a convenção de imagem da
família: caveira sempre à direita do losango, alça sempre na mesma diagonal.

**A alça como faixa contínua.** Desenrolando o torso (cilindro → plano), uma
faixa contínua que cruza o peito numa diagonal aparece nas costas com a
diagonal aparente OPOSTA (o desenrolo inverte o sentido horizontal ao passar
da frente para as costas; vale para faixa em laço e para faixa de duas pontas
presas ao cinto). O cânone mostra a MESMA diagonal aparente na frente
(verificada: duas fivelas sobre a diagonal sup-esq → inf-dir) e nas costas
(verificada em `costas_v2` e na refeita). **O traje canônico, como desenhado,
não é uma faixa fisicamente contínua** — o Crítico original já o tinha notado
("geometricamente estranho") e consagrado como convenção. Consequência:
"correção física" não pode ser portão de nenhuma vista deste arsenal, porque
reprovaria a costas canônica que serve de autoridade às demais.

**Teste de predição (a régua que decide):** dada a frente e as costas, onde
cada peça deveria aparecer na traseira esquerda?
- Pela regra da família (C1): alça sup-esq → inf-dir e caveira à direita —
  é EXATAMENTE o que a refeita mostra. Acerto 6/6 vistas existentes.
- Pela NV-1 (C2): alça espelhada e caveira à esquerda — não corresponde a
  NENHUMA vista traseira existente e contradiz a `costas_v2` com a qual a
  refeita forma conjunto. Acerto 0/6.
A regra da família vence por 6 a 0 nas próprias fontes.

## 5. A REGRA final (uma frase executável)

> **Em qualquer vista nova do Orc, frontal ou traseira, desenhe o kit fixo ao
> corpo exatamente como ele aparece nas vistas já aprovadas da mesma família —
> caveira grande sempre à DIREITA do losango em coordenadas de imagem e alça
> sempre na diagonal superior-esquerda → inferior-direita — e mude de lado
> apenas os sinais da câmera: cabeça-de-lobo, ombreira, direção do perfil do
> rosto e pé em perfil.**

## 6. Veredito final das imagens contestadas e destino da tras_dir

- **`orc_diag_tras_esq_refeita.png` (SHA ad57447a…c95c618e): INSTALAR.**
  A aprovação do Crítico 1 fica de pé, agora com fundamento corrigido
  (precedente do C0 + regra da família, §3a/§4). Instalação = SUBSTITUIR a
  reprovada `orc_diag_tras_esq.png` no PC (nunca manter as duas "esquerdas"),
  conferindo o SHA após a cópia. **O par traseiro do Orc FECHA:**
  `tras_dir` + refeita, N2 nos três critérios por medição independente.
- **`orc_diag_frente_esq.png` (SHA 895c0cd9…af09230a): REJEITAR como entrada
  nova.** A reprovação do Crítico 1 (DUP-4.3) fica de pé; a aprovação do
  Crítico 2 é anulada. Não instalar no arsenal; pode ser guardada fora dele
  como re-render alternativo, se o executor quiser, sem status de referência.
  NÃO regenerar outra diagonal esquerda: a vaga aberta é a frontal DIREITA.
- **`orc_diag_tras_dir.png`: aprovação MANTIDA, sem ressalva.** A anotação de
  "desvio" do relatório v2 deve ser riscada no registro — sob a regra final,
  não há desvio.
- **LOTE 4: traseiras FECHADAS; frontal permanece aberto só na vaga direita.**

## 7. Especificação exata de regeneração (se aplicável)

**Nenhuma das duas contestadas se regenera.** A refeita está aprovada como
está; a frontal esquerda não se refaz porque o ângulo já existe
(`tresquartos_v2`). Regenerar a refeita com o cinto espelhado, como exigia o
relatório v2, produziria a única traseira do arsenal inconsistente com
`costas_v2` e `tras_dir` — fica expressamente desautorizado por esta
reconciliação.

Para a vaga aberta (diagonal frontal DIREITA, geração futura, não retrabalho),
a especificação exata — já com a REGRA do §5 embutida:
1. Câmera na frente-DIREITA do personagem: ombreira de espinhos proeminente em
   primeiro plano à esquerda de quem olha; cabeça-de-lobo recuada à direita,
   parcialmente atrás da linha do ombro.
2. Rosto em 3/4 virado para a ESQUERDA de quem olha (para o lado da câmera).
3. Pé viewer-ESQUERDO em perfil apontando para a esquerda; pé viewer-direito
   em vista frontal-superior.
4. Kit PELA REGRA: alça na diagonal superior-esquerda → inferior-direita;
   caveira grande do cinto à DIREITA do losango; losango central; presas,
   argolas e pingente mantidos. NÃO espelhar o kit.
5. Zero bolsinhas, zero machado, corpo inteiro, fundo cinza-claro liso, tom
   oliva da frente canônica.
6. Aceite numérico obrigatório antes de instalar: IoU bbox-alinhado <
   0,85 contra `tresquartos_v2` E contra `frente` (auditoria de novidade N5
   contra TODAS as vistas aprovadas, não só a irmã).

## 8. Lição para o checklist pré-Crítico

Esta contradição não nasceu das imagens; nasceu de processo. Três verificações
novas, permanentes a partir desta reconciliação:

- **N6 — Leitura obrigatória dos vereditos anteriores.** Antes de julgar um
  retrabalho, o Crítico lê TODOS os relatórios anteriores sobre as mesmas
  imagens/personagem e, para cada afirmação decisiva anterior, ou a reproduz
  com medição própria ou a refuta explicitamente com medição própria. Julgar
  sem ler — como o Crítico 2 fez com o DUP-4.3 e com o precedente do C0 — é
  falha de processo que invalida o veredito, mesmo quando o checklist local
  passa.
- **N7 — Regra nova não retroage seletivamente.** Toda regra nova (como a
  NV-1) é executada contra TODAS as vistas já aprovadas da família ANTES de
  ser aplicada à candidata. Se a regra reprova uma autoridade aprovada, quem
  volta para revisão é a regra, não a autoridade. E um mesmo traço jamais
  recebe severidades diferentes em imagens diferentes sem uma diferença
  medida entre elas: um peso, uma régua.
- **N8 — Coordenada decisiva exige grade e referencial.** Toda coordenada
  x/y usada como evidência decisiva é lida em recorte com grade impressa (ou
  computada por script) e declara o referencial (imagem × bbox) e a convenção
  de qualquer razão (dir/esq × esq/dir). Coordenada "a olho" sem grade não é
  medição: a caveira do Crítico 2 estava 0,12 fora do lugar, e a razão
  "0,521/0,569" dele misturou duas convenções na mesma linha.

**Encerramento:** com esta reconciliação, o lote 4 tem um único veredito por
imagem (§6). Os relatórios do Crítico 1 e do Crítico 2 devem ser registrados no
repo junto com este, sem apagar nenhum dos dois — o histórico da disputa faz
parte da prova. A palavra final de fidelidade artística continua sendo do
Mestre.
