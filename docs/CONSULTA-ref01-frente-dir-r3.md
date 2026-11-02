# CONSULTA DE PROCESSO — REF-01, diagonal frontal DIREITA do Orc, rodada 3

**Papel:** Crítico Visual sênior independente, convocado para CONSULTA DE
PROCESSO — não para julgar uma candidatura. Missão adversarial (APR-02):
tentar reprovar o que o executor afirma, com remedição própria das fontes.
Eu não gerei nenhuma imagem aqui; não audito execução própria.
**Data:** 01/11/2026 (reemissão integral; uma tentativa anterior desta
consulta foi perdida por reinício do daemon).
**Limite rígido desta consulta:** isto NÃO é veredito de candidatura.
Não aprovo nem reprovo a `r3-t2` como entrada do arsenal; não instalo
nada; não escrevo em nenhum caminho do PC
(`C:\Users\txcga\RPG_Local\Oficina3D\app`); não faço commit nem push.
A palavra final de fidelidade artística é do Mestre. O que segue são
respostas fundamentadas às 5 perguntas da convocação, para decidir o
próximo passo de processo — e só isso.

## 0. Leitura obrigatória (N6) e método próprio

Li, antes de qualquer conclusão:

- `CRITICO-ref01-lote4-reconciliacao.md` (§5 REGRA do kit, §7
  especificação exata, §8 N6/N7/N8);
- `autoauditoria-orc-diag-frente-dir-r2.md` (rodada anterior: 0/4,
  viés 7/7);
- `autoauditoria-orc-diag-frente-dir-r3.md` (esta rodada: 4 tentativas,
  t2 = melhor em 11).

Vi com os meus próprios olhos, em imagem inteira e em recortes
ampliados (lobo, cinto, pés): a candidata `orc_diag_frente_dir_r3_t2.png`,
as outras da rodada (`_t1`, `_t3`, `_t4`) e as autoridades
(`orc_frente.png`, `orc_tresquartos_v2.png`, `orc_costas_v2.png`,
`orc_diag_tras_dir.png`, `orc_diag_tras_esq_refeita.png`).

**Método de IoU (o mesmo dos relatórios, reproduzido do zero):**
script do executor `iou_ref01.py` — máscara de silhueta por distância
RGB à mediana dos quatro cantos, bbox recortado e redimensionado a
grade 500 × 500 (NEAREST). **Limiares:** 25/35/45 (N9 proposta).
**Referencial:** IoU contra cada uma das 6 vistas aprovadas
(`tresquartos_v2`, `frente`, `costas_v2`, `tras_dir`,
`tras_esq_refeita`, `tpose_v2`). **Limiar de novidade N5:** < 0,85.
Coordenadas x/y abaixo são frações da largura/altura da imagem,
lidas visualmente em imagem inteira e recortes (precisão estimada
±0,03) — suficientes para estabelecer ordem e lado, que é o que o
§5 e o §7 exigem; não são leitura com grade impressa no sentido
do N8, e não precisam ser, porque nenhuma conclusão abaixo depende
de um dígito na segunda casa decimal.

**Hashes conferidos (SHA-256 integral, recalculados por mim):**

| Arquivo | SHA-256 |
|---|---|
| `orc_diag_frente_dir_r3_t2.png` | `42510537…f9fa2355285eca` |
| `orc_diag_frente_dir_r3_t4.png` | `ec9a52ae…ac1a034caf23c8` |
| `orc_tresquartos_v2.png` | `7c9d9465…afb9a` (confere com a reconciliação) |
| `orc_frente.png` | `30c0f83d…903b6c` (confere) |
| `orc_costas_v2.png` | `09890d74…7a41362` (confere) |
| `orc_diag_tras_dir.png` | `acb515d2…7372250b` (confere) |
| `orc_diag_tras_esq_refeita.png` | `ad57447a…c95c618e` (confere) |

Achado incidental de higiene (sem efeito nas conclusões): nesta
pasta local, `orc_diag_tras_esq.png` tem o MESMO hash da refeita
(`ad57447a…`). Ou seja, a "original reprovada" já não está
distinguível da refeita neste diretório local — um IoU futuro
contra a original não pode ser reproduzido a partir daqui. Não
afeta esta consulta, porque a autoridade vigente é a refeita,
e foi contra ela que medi.

## 1. A leitura do executor sobre a t2 está certa? — SIM, item a item

**Veredito desta seção: CONFIRMADA em todos os subitens (a)–(d).
Tentei refutar cada um; nenhum se sustentou.**

### (a) Rosto em 3/4 para a esquerda de quem olha — CONFIRMADO

Na imagem inteira: nariz, presas e queixo projetam-se para a
esquerda; vemos o perfil esquerdo em 3/4, com a orelha esquerda
do orc visível e o olhar dirigido para a esquerda. É o inverso
exato do padrão das 7 tentativas anteriores (rosto para a
direita) e o inverso da `tresquartos_v2` (rosto para a direita).
Não é perfil puro nem frontal: há volume dos dois lados do
rosto, mas a direção dominante é inequivocamente esquerda.
**O viés de rosto foi quebrado — a âncora nas traseiras
funcionou neste item.**

### (b) Pé viewer-esquerdo em perfil para a esquerda; pé viewer-direito frontal — CONFIRMADO

Recorte dos pés conferido:

- **Viewer-esquerdo:** bota em perfil completo apontando para a
  esquerda — biqueira com espigão à esquerda, sola lateral
  visível, calcanhar à direita. É o pé em perfil que o §7
  exige, no lado certo e na direção certa.
- **Viewer-direito:** bota vista de cima/frente — biqueira com
  placa e espigões simétricos voltados para quem olha, sem
  perfil lateral. É a vista frontal-superior do §7, não um
  perfil para a direita como nas tentativas anteriores.

Os dois pés estão íntegros, conectados às pernas e apoiados
no mesmo plano. **O viés de pés foi quebrado junto com o de
rosto — os dois sinais de câmera que faltavam em 7/7 agora
estão certos em 1/4.**

### (c) Kit pela REGRA §5 — CONFIRMADO

REGRA (§5): em qualquer vista nova, caveira grande sempre à
DIREITA do losango em coordenadas de imagem e alça sempre na
diagonal superior-esquerda → inferior-direita; mudam de lado
apenas os sinais da câmera.

Na t2, em imagem inteira e no recorte do cinto:

- **Alça:** faixa larga cruzando o peito da parte superior
  esquerda para a inferior direita, com duas fivelas sobre a
  diagonal — a mesma orientação da frente canônica e das
  traseiras aprovadas. NÃO espelhada.
- **Losango:** central, no centro da cintura (x ≈ 0,47–0,49).
- **Caveira grande:** nitidamente à DIREITA do losango
  (centro x ≈ 0,60), com presas, argolas e pingente mantidos.
  Ordem losango → caveira da esquerda para a direita, como
  nas 6 vistas aprovadas.
- **Fivela da cintura** abaixo do losango, à esquerda da
  caveira, na posição canônica.

Nenhum elemento do kit foi espelhado, trocado de lado ou
omitido. O item 4 do §7 passa, e passa pela REGRA certa
(família), não por acidente de renderização.

### (d) N5 < 0,85 contra as 6 vistas aprovadas nos 3 limiares — CONFIRMADO, com margem

Medição própria, script `iou_ref01.py`, t2 contra cada vista:

| Vista aprovada | thr 25 | thr 35 | thr 45 |
|---|---|---|---|
| `tresquartos_v2` | 0,756 | 0,749 | 0,743 |
| `frente` | 0,699 | 0,673 | 0,647 |
| `costas_v2` | 0,755 | 0,749 | 0,745 |
| `tras_dir` | 0,722 | 0,714 | 0,710 |
| `tras_esq_refeita` | 0,731 | 0,724 | 0,720 |
| `tpose_v2` | 0,422 | 0,420 | 0,416 |

**Máximo em 18 medições: 0,756** (contra `tresquartos_v2` a
25) — 0,094 abaixo do limiar 0,85, em todos os limiares e
contra todas as vistas. Os números reproduzem EXATAMENTE os
do executor (diferença 0,000 em todas as células que ele
publicou). Não há instabilidade de limiar na t2: a curva
25→45 desce monotonicamente, como esperado, sem cruzar o
limiar em nenhum ponto.

**Conclusão da pergunta 1:** a leitura do executor está certa
nos quatro subitens. A t2 é, de fato, a primeira tentativa em
11 a passar rosto, pés, kit e novidade angular ao mesmo
tempo. Isso torna o defeito restante mais, e não menos,
importante: ele é o único obstáculo entre esta imagem e uma
vista nova genuína — e é por isso que ele precisa ser
classificado com precisão, e não minimizado.

Verificação cruzada das rivais (para não deixar a t2
supervalorizada por contraste): `r3-t1` (0,780/0,773/0,767
contra `tresquartos_v2`) e `r3-t3` (0,765/0,757/0,750) passam
N5, mas confirmei a olho que ambas falham rosto (direita) e
pés (esquerdo frontal / direito em perfil para a direita) —
o executor acertou também aí. A t2 não é "a menos ruim por
falta de opção"; é a única que quebrou o viés.

## 2. O lobo da t2 é falha do item 1 do §7 ou está dentro de tolerância? — FALHA, S2

**Classificação: defeito de fidelidade S2 (exige retrabalho /
impede a entrada como está; S1 = impede o uso; S2 é a classe
correta — ver fundamento ao fim). É falha do item 1 do §7,
segunda metade, sem atenuação por tolerância.**

### O que eu vejo (recorte ampliado do quadrante superior direito)

- **Tamanho:** cabeça do lobo grande, em escala de primeiro
  plano — largura aproximada x ≈ 0,70–0,95 da imagem
  (cerca de 0,25 da largura total), altura y ≈ 0,16–0,30.
  É maior que a cabeça do próprio orc na mesma imagem.
  Tamanho absoluto, isolado, NÃO é o problema: na
  `tresquartos_v2` (vista em que o lobo É o lado da câmera)
  a cabeça tem escala comparável. O problema é relacional:
  escala de primeiro plano num ombro que deveria ser o
  recuado.
- **Posição:** à direita de quem olha, como manda o §7 —
  a posição está certa. O erro não é de lado.
- **O que o cobre:** NADA. A cabeça está inteira à frente
  da capa de pele, sobre a ombreira de metal, com as duas
  orelhas, o olho amarelo, o focinho, o nariz e a boca
  totalmente visíveis e nítidos, em perfil para a direita.
  Nenhuma parte — nem a orelha traseira, nem a nuca, nem a
  base do pescoço — é cortada pela linha do ombro, pela
  capa ou pelo braço. O braço viewer-direito passa ABAIXO
  da cabeça, sem interceptá-la. A cabeça destaca-se
  livre contra o fundo cinza à direita, fora da silhueta
  do tronco. **Oclusão: 0%.** O §7 exige "parcialmente
  atrás da linha do ombro": o requisito de parcialidade
  não é cumprido em nenhum grau.
- **Contraste com as referências de "recuado":** em
  `costas_v2` e em `tras_dir` (vistas em que o lobo NÃO é
  o lado da câmera), o lobo aparece quase todo escondido
  atrás da capa — só focinho e uma orelha espiam. Na t2,
  o tratamento é o oposto: o tratamento de lado da câmera
  aplicado ao lado que não é o da câmera. É exatamente o
  resíduo do viés 11/11 que o executor descreveu: o
  gerador manteve o lobo "da família da diagonal esquerda"
  enquanto virou rosto e pés.
- **Observação secundária (S4, não é item §7):** o lobo
  olha para a direita enquanto o orc olha para a esquerda.
  Nas vistas frontais aprovadas (frente, `tresquartos_v2`)
  os dois olhares alinham-se; aqui divergem. Registro
  como flag de coerência a re-checar no candidato editado,
  não como falha autônoma — o §7 não regula o olhar do
  lobo, e nas costas o alinhamento também não vale. Não
  uso isto para agravar a severidade.

### Por que S2, e não S4, S3 ou S1

- **Não é S4 (observação) nem S3 (menor):** viola um item
  explícito e numerado da especificação (§7 item 1), e
  viola o sinal de câmera que JUSTIFICA a existência
  desta vista. Uma diagonal frontal direita cujo lobo se
  comporta como diagonal esquerda entrega ao modelador
  multivista um sinal contraditório de lado — a mesma
  classe de erro que já custou reprovação neste projeto
  (troca de lado, S2, nos lotes 1 e 3).
- **Não é S1 (impede o uso):** o defeito é LOCALIZADO
  (quadrante superior direito: cabeça do lobo + pele
  adjacente), não corrompe a identidade do personagem,
  não inventa nem omite elemento, não toca rosto, pés,
  kit ou silhueta geral — e é remediável sem regenerar a
  figura (ver pergunta 3). S1, neste projeto, é para o
  que torna a imagem inutilizável como base (criatura
  errada, personagem inteiro espelhado). A t2 continua
  sendo uma base válida PARA EDIÇÃO; o que ela não pode
  é entrar como está.
- **Portanto S2:** impede a entrada como está, exige
  retrabalho, não destrói a base. Esta é a classificação
  adversarialmente honesta: nem benevolente (não é
  tolerância) nem inflada (não é S1 para forçar um
  veredito dramático).

**Também confirmo o item 5 do §7 na t2, com a ressalva do
executor:** zero bolsinhas, zero machado, corpo inteiro,
fundo cinza-claro liso, tom oliva da frente canônica. O
pequeno item cilíndrico no quadril viewer-esquerdo é um
tubo de osso do kit — o mesmo motivo aparece nos dois
lados do cinto na frente canônica — não é bolsinha. Não
classifico como falha. A primeira metade do item 1
(ombreira de espinhos proeminente à esquerda, x ≈ 0,16–0,26)
também passa: o defeito é só a segunda metade.

## 3. A rota proposta é aceitável? — SIM, com condições exatas

**Resposta: SIM.** A edição controlada da t2 — empurrar o
lobo para trás da linha do ombro, preservando todo o resto,
com re-verificação total — é aceitável como PRÓXIMO PASSO
DE PROCESSO. Não é pré-aprovação de nenhum resultado: o
arquivo editado será um NOVO candidato, com hash próprio,
julgado do zero por um Crítico independente. Se qualquer
condição abaixo falhar, a edição é descartada — não se
"ajeita" o editado até passar.

**Por que SIM, e não "gere de novo":** o espaço de geração
direta foi varrido em 3 famílias de fonte (frente,
T-pose, traseiras) e 11 tentativas; o resíduo é UM
elemento localizado, e a base (rosto, pés, kit, N5 com
margem 0,094) é a melhor já obtida. Exigir outra geração
pura seria repetir o experimento que já falhou 11 vezes
no mesmo ponto. A edição é o experimento novo, não um
atalho — desde que cumpra as condições, que são o que a
separa de um "jeitinho".

### Condições exatas para eu aceitar o editado depois como candidato

1. **Região e proveniência.** A edição toca SOMENTE o
   quadrante superior direito (cabeça do lobo + pele da
   capa imediatamente adjacente, aproximadamente
   x > 0,65, y < 0,35). O arquivo original t2 é preservado
   intacto; o editado recebe nome e hash novos, nunca
   sobrescreve a t2. O executor declara a ferramenta e o
   comando/prompt da edição e entrega a máscara ou
   descrição da região tocada (proposta de verificação
   nova N10, abaixo).
2. **O lobo depois da edição (critério verificável a olho).**
   TODOS os três subcritérios, sem exceção:
   (i) a parte POSTERIOR da cabeça (orelha traseira e/ou
   nuca e base do pescoço) fica cortada pela capa de pele
   e/ou pela linha do ombro — oclusão parcial REAL,
   não apenas cabeça menor no mesmo lugar;
   (ii) a cabeça deixa de se destacar livre contra o
   fundo à direita: sua silhueta funde-se com o tronco/
   capa, como nas referências de "recuado"
   (`costas_v2`, `tras_dir`), e não se lê mais como
   sujeito em primeiro plano;
   (iii) o lobo continua SENDO o lobo do kit (mesma pele
   cinza-castanha, mesmo perfil para a direita, mesmo
   olho) — não pode ser apagado, substituído por outro
   animal, nem virar só pele sem cabeça. Apagar seria
   MIS (elemento faltando) e falharia o item 1 no outro
   sentido.
3. **Nenhuma regressão fora da região.** Re-verificação
   TOTAL do §7 no arquivo editado, item por item, por
   Crítico independente (não pelo executor, não por
   esta consulta): rosto 3/4 esquerda; pés
   esquerdo-perfil-esquerda / direito-frontal; kit pela
   REGRA §5 (alça sup-esq → inf-dir, losango central,
   caveira grande à direita do losango — ordem e
   orientação conferidas, não presumidas); item 5
   (inventário, corpo inteiro, fundo, tom). Se a
   ferramenta de edição re-renderizar a imagem inteira,
   a re-verificação trata o resultado como geração nova
   — o que é aceitável, mas então nada do que a t2
   passou é herdado: tudo é medido de novo.
4. **N5/N9 no editado.** IoU bbox-alinhado < 0,85 nos
   TRÊS limiares (25/35/45) contra TODAS as 6 vistas
   aprovadas, medido com o mesmo script, com a tabela
   completa publicada. Nota: encolher/ocultar o lobo
   deve, em princípio, AFASTAR a silhueta da
   `tresquartos_v2` (onde o lobo é proeminente), mas
   "em princípio" não é medição — mede-se.
5. **Nenhum defeito novo na região editada.** Sem segunda
   orelha, focinho duplicado, fusão pele-metal, halo ou
   costura visível no fundo, e sem deformação da
   ombreira/braço viewer-direito. Textura da pele
   editada contínua com a capa existente. Qualquer
   artefato S1/S2 na região invalida o editado, mesmo
   que o lobo esteja "recuado".
6. **Sem loop de remendo.** Uma única tentativa de
   edição julgada; se falhar em qualquer condição,
   abandona-se a edição (ver pergunta 4). Não se
   encadeiam edições sucessivas até o arquivo "passar
   por desgaste" — cada remendo adicional apaga a
   evidência de que a base era a t2.

**O que NÃO salvaria a t2, e fica vetado:** espelhamento
puro (flip) da imagem — inverteria a alça e a caveira e
violaria a REGRA §5; redução de escala da cabeça sem
oclusão (continuaria "proeminente, só que menor"); e
qualquer edição que toque rosto, pés ou cinto para
"compensar" o lobo.

## 4. Se a edição for inaceitável — rota de fallback (condicional)

Como respondo SIM à pergunta 3, esta pergunta é
condicional: **vale se a edição falhar nas condições do
§3, ou se a ferramenta disponível não permitir edição
regional controlada.** Nesse caso, a minha recomendação é:

**Declarar a vaga intratável por geração/edição direta e
pedir decisão do Mestre — sem mais uma rodada de geração
por fraseado.**

Fundamento: 11 tentativas em 3 famílias de fonte + 1
tentativa de edição falhada esgotam o que o processo
técnico pode decidir sozinho. Continuar gerando seria
loteria, não processo. A decisão que falta é ARTÍSTICA
e de prioridade, e por isso é dele — não do executor
nem do Crítico. O pedido a ele deve apresentar as
opções com o custo de cada uma, sem recomendação
disfarçada de ordem (pesquisa/proposta, nunca comando):

- (a) **Aceitar a lacuna:** fechar o arsenal do Orc com
  as 6 vistas aprovadas + a frontal esquerda
  (`tresquartos_v2`), sem diagonal frontal direita.
  Custo: assimetria do arsenal; benefício: nenhuma
  vista mentirosa entra no multivista.
- (b) **Edição manual externa:** um artista (humano)
  retoca SOMENTE a região do lobo da t2, sob as mesmas
  condições do §3. Custo: depende de disponibilidade;
  benefício: é o único caminho que preserva a base
  medida sem re-renderização generativa.
- (c) **Exceção documentada (desaconselhada por mim):**
  aceitar a t2 como está, com anotação permanente de
  que o sinal do lobo contradiz a câmera. Só o Mestre
  pode conceder exceção a um item §7 — e eu registro
  o meu parecer contrário: um arsenal de referência
  para modelagem multivista não deve conter um sinal
  de lado contraditório anotado como "tolerado",
  porque o modelador (humano ou motor) lê a imagem,
  não a anotação.

**O que NÃO recomendo como "outra rota concreta":**
mais uma variação de prompt sobre frente/T-pose/
traseiras; usar a `r3-t1` ou a `r3-t4` como base
(ambas falham rosto e pés — trocar um defeito S2 por
três); nem gerar a vista pedindo o lobo ausente para
"adicioná-lo depois" (criaria um segundo problema de
integração). Nenhuma destas é concreta no sentido de
ter uma hipótese nova testável — são repetições do
experimento já feito.

## 5. A verificação nova N9 deve ser adotada, corrigida ou refutada? — ADOTADA

**Resposta: ADOTAR, sem correção de substância, com um
refinamento de redação (abaixo).**

**Medição própria do contraexemplo (r3-t4 contra
`tresquartos_v2`, mesmo script): 0,856 / 0,848 / 0,840
nos limiares 25/35/45.** Reproduzo EXATAMENTE os números
do executor. Não há o que refutar: sob a regra antiga
(só o limiar 35), a t4 PASSARIA N5 (0,848 < 0,85) — e a
t4 é, a olho, composição da família da diagonal esquerda
(rosto para a direita, pé viewer-direito em perfil para
a direita, lobo proeminente à direita, a mesma que a
`tresquartos_v2`), com IoU limítrofe por construção.
Um critério de novidade que aprova uma quase-duplicata
por 0,002 de margem num único limiar é um critério com
um furo mensurável — e a t4 é a prova de que o furo não
é teórico.

**Por que a N9 não é excesso de rigor:**

- **Teste N7 (regra nova contra as aprovadas):** a N9
  não reprova retroativamente nenhuma vista aprovada.
  O par aprovado mais próximo do limiar,
  `tras_dir` × `costas_v2`, mede 0,832–0,841 na faixa
  25–45 (reconciliação §1.1) — abaixo de 0,85 nos três
  limiares. `refeita` × `costas_v2` fica em 0,793–0,799.
  A regra nova aperta onde há furo (quase-duplicatas)
  sem quebrar o arsenal existente. É exatamente o que
  o N7 exige de uma regra nova.
- **O limiar 25 é o mais estrito, e é o correto como
  pior caso:** limiar menor classifica mais pixels como
  silhueta (menor tolerância ao fundo), logo o IoU sobe.
  Exigir < 0,85 no pior caso (25) é exigir que a
  novidade não dependa da tolerância ao fundo — o
  análogo, para N5, do que o N8 exige para coordenadas
  (método declarado, sem dígito frágil).
- **A t2 passa N9 com folga (máximo 0,756):** a regra
  nova não foi desenhada para salvar ou condenar a t2;
  ela separa t2 (margem 0,094) de t4 (falha a 25) com
  clareza. Uma regra que só afeta o caso limítrofe é
  uma regra bem calibrada.

**Refinamento de redação (não muda a substância):**
escrever a N9 como "N5 exige IoU < 0,85 no MÁXIMO dos
três limiares (25/35/45), contra TODAS as vistas
aprovadas" — em vez de "nos três limiares", que pode
ser lido como três testes independentes. E registrar
que N9 não substitui a leitura visual de âncoras: IoU
é silhueta, não ângulo. A t4 falha nos dois (número a
25 + âncoras da família esquerda); a t2 passa nos dois.
Nenhum número, sozinho, aprova uma vista.

**Verificação nova proposta para a rodada da edição
(APR-01, a decidir pelo Crítico daquela rodada): N10 —
Auditoria de região da edição.** Todo candidato oriundo
de edição entrega (i) a região tocada, (ii) a
comparação antes/depois fora da região, e (iii) a
re-medição total do §7. Sem (i) e (ii), o editado é
julgado como geração nova integral — o que é válido,
mas perde o benefício da base medida. Proponho, não
decreto: quem adota a N10 é o Crítico da rodada da
edição, com medição própria, como manda o APR-01.

## Encerramento

- A leitura do executor sobre a t2 está certa nos 4
  subitens; a t2 é a melhor tentativa em 11, e o seu
  único defeito restante é o lobo — S2, localizado,
  0% de oclusão onde o §7 exige parcialidade.
- A edição controlada é aceitável, SOMENTE sob as 6
  condições do §3; o editado será novo candidato, com
  veredito próprio de Crítico independente.
- Se a edição falhar, a recomendação é declarar a vaga
  intratável por geração/edição e pedir decisão do
  Mestre (lacuna × edição manual × exceção
  documentada, esta última desaconselhada por mim).
- N9: ADOTADA, com a redação de "máximo dos três
  limiares" e o teste N7 cumprido.
- Nada aqui é veredito de candidatura, instalação,
  escrita no PC ou reporte ao Mestre. O próximo passo
  de processo é a tentativa de edição sob o §3 — ou,
  se ela falhar, o pedido de decisão do §4.
