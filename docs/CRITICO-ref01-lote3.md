# CRÍTICO VISUAL SÊNIOR — REF-01, lote 3 (Capríleo): relatório do veredito

**Data:** 01/11/2026. **Papel:** Crítico Visual sênior, independente e imparcial (não gerou nenhuma imagem deste lote; lealdade à fidelidade MEDIDA contra as fontes). **Protocolo:** ESTUDO_MELHORIAS seção 7 (taxonomia EXT/MIS/FUS/DEF/SIL/SYM/FACE/PRP/TXT; severidades S1–S4) + bateria da seção 6 de APRENDIZADO_E_FLUXO adaptada a monstro quadrúpede + escalada APR-01 desta rodada (seções 4a e 4b, obrigatórias) + reaplicação dos precedentes do lote 2 (B1, B2, B7, B9).

**Alvos julgados** (cópias locais; SHA-256 conferidos por este Crítico e IDÊNTICOS aos informados na tarefa):
- `caprileo_diag_tras_esq.png` — 1600×1600, RGB, SHA-256 `efd00a7d77e0830f609025a12307f6f00485032bb86d91f7496fe02ee59fa180`
- `caprileo_diag_tras_dir.png` — 1920×1280, RGB, SHA-256 `46cbe2b9b645163909a6eb6ac745eb8b9d0694717122fdedfc8348d10d1ef07a`
- `caprileo_topo.png` — 1600×1600, RGB, SHA-256 `f09270071bdea23cd587da96ee4b52bf4bb29b3204d47ca369aa4ba3c238b634`

**Fontes canônicas (autoridade; SHA-256 conferidos, idênticos aos da tarefa):** `caprileo_frente_fonte.png` (`585525bf…`), `caprileo_costas_fonte.png` (`7fc334ae…`), `caprileo_esquerda_fonte.png` (`4b7d88eb…`), `caprileo_direita_fonte.png` (`73532ba0…`).

**Evidências desta rodada:** inspeção visual direta das 3 vistas em resolução plena + os 7 zooms do executor em `~/workspace/oficina-audit/zooms_lote3/` + meus próprios recortes de patas (4 patas próximas por diagonal) + medições próprias por script (máscara por distância à cor de fundo; medianas de paleta por classe; correlação de luminância entre vistas em grade 128×128 com fundo normalizado para branco). **Nota de método honesta:** dois dos meus recortes de patas traseiras próximas ficaram descentralizados (peguei borda da pata, não o centro); a contagem de garras das seções 4b/5 usa a imagem plena em resolução original, não esses dois recortes falhos — os demais recortes confirmam dígitos distintos, sem fusão.

---

## Veredito do lote

**LOTE 3 REPROVADO — com retrabalho mínimo e sem regeneração.** O conteúdo das três vistas é bom: nenhuma criatura errada, nenhum membro inventado, nenhum defeito S1, e o topo é uma planta verdadeira. Mas há **um defeito S2 de fidelidade: C1 — os rótulos das duas diagonais traseiras estão trocados em relação ao lado que cada uma mostra** (seção 4a, três âncoras independentes + correlação). Como o critério de aceite exige nenhum S1/S2, o lote não fecha nesta rodada. O retrabalho é só **renomear os dois arquivos (troca simultânea, conteúdo intacto)** e re-conferir os hashes — nenhuma vista precisa ser gerada de novo. Após a renomeação e a re-verificação da seção 7, o lote fecha com as pendências S3/S4 nomeadas abaixo. A palavra artística final é do Mestre; este veredito é técnico.

| Imagem | Veredito | Pode entrar no arsenal? |
|---|---|---|
| `caprileo_diag_tras_esq.png` (conteúdo = vista traseira-**direita**) | **Imagem APROVADA como vista; rótulo REPROVADO** | **NÃO (ainda)** — só entra após renomeada para `diag_tras_dir` (C1) |
| `caprileo_diag_tras_dir.png` (conteúdo = vista traseira-**esquerda**) | **Imagem APROVADA como vista; rótulo REPROVADO** | **NÃO (ainda)** — só entra após renomeada para `diag_tras_esq` (C1) |
| `caprileo_topo.png` | **APROVADA como vista de topo** | **SIM** — pendências C2 (S3), C3 (S3) e C5 (S4) |
| **Lote 3** | **REPROVADO (C1 S2, só renomeação)** | Fecha após a seção 7, sem nova geração |

**O que NÃO é problema (registro explícito, para não virar retrabalho inútil):** o par de diagonais, como conjunto, cobre os dois lados traseiros — não falta lado nenhum; o topo passa no teste de pureza da planta (precedente B2); nenhuma garra ou espinho inventado/fundido (seção 4b); a paleta é fiel (seção 2); nada cortado nas margens (C5 é só aperto cosmético).

## 1. Bateria da seção 6 adaptada a quadrúpede, item a item

**1. Mesma criatura? — PASSA nas três.** Quadrúpede quimera: cabeça de carneiro com escamas cinzentas, orelhas pequenas, olhos âmbar, dois chifres enormes espiralados e anelados marrons, crina ondulada creme longa no pescoço/peito, corpo reptiliano de escamas cinza-esverdeadas, crista de espinhos triangulares do pescoço à ponta da cauda, cauda longa afilada, quatro patas com garras escuras. Nenhuma criatura diferente, nenhum membro inventado (EXT: zero).

**2. Características preservadas? — PASSA nas diagonais; PASSA COM RESSALVAS no topo.** Inventário: (a) chifres espiralados anelados — presentes e grandes nas três; (b) crina creme longa e ondulada — presente nas três, repartida ao centro no topo; (c) crista dorsal — fileira única e contínua nas três (seção 4b); (d) cauda longa afilada — presente nas três, curvando para o lado direito do animal (âncora da seção 4a); (e) olhos âmbar — visíveis nos perfis das diagonais e como pontos laterais no topo; (f) orelhas pequenas — visível a próxima na diagonal `esq` (zoom `esq_cabeca_chifres`: orelha pontuda nítida à direita do chifre); na diagonal `dir`, a orelha próxima fica quase toda oculta atrás do chifre e há um pequeno ponto cinzento acima da crina, à direita do chifre afastado, compatível com a ponta da orelha afastada — registro como inconclusivo, sem classificação (não é característica alterada, é oclusão). Ressalvas do topo: pernas espraiadas (C2) e espirais mais fechadas (C3).

**3. Pose/enquadramento coerente com frente/costas/perfis? — PASSA nas diagonais; PASSA COM RESSALVA no topo.** As diagonais mantêm o quadrúpede em pé, quatro patas apoiadas, eixo cabeça–cauda coerente com os perfis (seção 4a). O topo é câmera diretamente acima (planta), mas as pernas leem espraiadas, não em pé (C2, seção 3b). Nenhuma vista é folha (vistas avulsas, como exigido).

**4. Integração das patas e da cauda — PASSA nas diagonais; PASSA COM RESSALVA no topo.** Nas diagonais, as quatro patas articulam com o tronco sem flutuação nem amputação: as duas traseiras são a informação nova genuína do lote (plano do dorso + raiz da cauda + traseiras, como o executor antecipou). A cauda nasce na raiz correta, afila continuamente e termina em ponta fina nas três vistas. No topo, a articulação coxa–tronco é legível, mas a abertura lateral das pernas é o defeito C2.

**5. Enquadramento e fundo — PASSA com ressalva S4 (C5).** Corpo inteiro nas três, fundo claro uniforme, sem cenário, texto, marca d'água ou sombra forte. Margens medidas pela máscara (fundo claro, distância > 45): `diag_tras_esq` L 8,4% / R 12,4% / T 4,0% / B 2,9%; `diag_tras_dir` L 13,8% / R 11,7% / T 3,3% / B 2,3%; `topo` L 20,1% / R 21,1% / T 3,2% / B 3,7%. Reprodução exata dos números do executor. Nada cortado; as bases das diagonais (2,3–2,9%) e do topo (3,7%) ficam abaixo dos 5% pedidos — precedente B9, S4.

**6. Consistência cruzada ENTRE as vistas — FALHA EM UM PONTO (C1) e passa no resto.** As três vistas são rotações de um só indivíduo em: crista contínua, crina, chifres, curva da cauda para o lado direito do animal, cor (seção 2). A falha é de atribuição de lado entre as duas diagonais (seção 4a). O topo é consistente com as costas na curva da cauda: no topo (cabeça para cima) a cauda curva para a direita inferior da imagem; nas costas canônicas a cauda vai para a direita da imagem — ambas são o lado direito do animal (o executor acertou aqui).

**7. Integridade técnica — PASSA.** PNGs válidos (1600×1600, 1920×1280, 1600×1600, RGB); SHA-256 locais idênticos aos da tarefa (portanto, às cópias instaladas no PC, conforme o enunciado). Não verifiquei `git check-ignore` neste papel porque as cópias julgadas são as locais e a tarefa já as declara idênticas às do PC — o executor confirma o gitignore no registro de instalação.

**8. Classificação de defeitos** — tabela completa na seção 6.

## 2. Paleta — medição própria (a lacuna que o executor declarou)

**Método:** classificador por regras RGB aplicado só aos pixels da criatura (fontes: alfa > 200; alvos: distância à cor de fundo). Classes: crina creme (R > 150, R−G ≥ 10, G−B ≥ 15, R−B ≥ 35); escamas (canais próximos entre si, |R−G| < 28, |G−B| < 28, R 90–185, fora da crina); chifre marrom (R 95–200, R−G ≥ 15, G−B ≥ 15, R−B ≥ 40). Autoridade declarada: frente canônica; controle: costas canônicas (a vista dorsal, ponto de vista mais próximo das traseiras e do topo).

**Medianas RGB por classe:**

| Vista | Crina creme | Escamas | Chifre marrom |
|---|---|---|---|
| frente canônica (autoridade) | (192, 165, 135) | (114, 107, 99) | (158, 132, 106) |
| costas canônica (controle dorsal) | (190, 163, 134) | (120, 116, 108) | (160, 134, 109) |
| esquerda canônica | (189, 162, 130) | (119, 114, 105) | (155, 129, 103) |
| direita canônica | (188, 160, 129) | (116, 111, 103) | (154, 128, 102) |
| `diag_tras_esq` | (192, 167, 141) | (125, 121, 112) | (159, 134, 109) |
| `diag_tras_dir` | (194, 169, 143) | (124, 121, 113) | (160, 135, 111) |
| `topo` | (191, 165, 139) | (123, 118, 110) | (161, 135, 110) |

**Deltas (soma |Δ| por canal) contra a frente:** crina 8 (`esq`), 14 (`dir`), 5 (topo); chifre 6, 10, 10; escamas 38, 38, 31. **Leitura honesta, que o número bruto contra a frente esconde:** a própria variação canônica entre vistas já é grande nas escamas — frente vs. costas dá delta 24 (6+9+9), porque a frente tem sombreamento mais escuro e as costas são vistas dorsais claras. Contra as costas (a autoridade de ponto de vista para traseiras e topo), os deltas das escamas caem para **14, 14 e 7** — dentro da variação canônica entre vistas. A direção do desvio é a mesma nas três vistas (render globalmente um pouco mais claro, +3 a +5 por canal contra as costas), sem troca de matiz: crina continua creme, escama continua cinza-esverdeada, chifre continua marrom. **Conclusão: cor fiel; NENHUM defeito TXT aberto.** A cobertura por classe varia com o ponto de vista (crina 13–14% da criatura nos alvos contra 18–23% nas fontes, porque nas traseiras/topos a crina fica parcialmente oculta atrás do corpo e o dorso de escamas domina o quadro) — efeito de vista, não perda de característica. Observação sem classificação (não defeito): o render é uniformemente um pouco mais claro que as fontes; se um dia se quiser tom exato, o ajuste é global, não por vista.

## 3. Testes do lote 2, reaplicados

### 3a. Pureza da planta no topo (precedente B2) — PASSA

Critério binário: se a boca ler inteira, de frente, não é topo. **Observado no `topo` (zoom `topo_cabeca_chifres`):** a cabeça lê-se como focinho visto de cima — narinas no alto, dorso do focinho escamado, olhos âmbar como pontos laterais, sem linha de boca frontal, sem face frontal, sem focinho de perfil. As espirais dos chifres leem num só plano, a crina reparte-se ao centro, a crista corre pela linha média até a cauda. **É planta verdadeira. Nenhum DEF/MIS S2 do tipo B2.** A antecipação do executor ("cabeça vista de cima, focinho para cima, sem face frontal") confirma-se integralmente.

### 3b. Diversidade angular medida do par de diagonais (precedente B7) — C4, S3

Correlação de luminância (fundo normalizado para branco, grade 128×128):

| Par | Correlação |
|---|---|
| `diag_esq` × `diag_dir` (bruta) | 0,167 |
| `diag_esq` × espelho de `diag_dir` | **0,633** |
| `diag_esq` × perfil direita | **0,519** (× espelho: 0,186) |
| `diag_esq` × perfil esquerda | 0,191 (× espelho: 0,471) |
| `diag_dir` × perfil esquerda | **0,482** (× espelho: 0,194) |
| `diag_dir` × perfil direita | 0,235 (× espelho: 0,536) |
| `diag_esq` × costas | 0,156; `diag_dir` × costas | 0,408 |
| `topo` × costas / frente / diagonais | 0,437 / 0,417 / 0,314 / 0,282 |

**Leitura:** as diagonais NÃO são duplicatas uma da outra (bruta 0,167 — ao contrário do par do lote 2, que marcou 0,778 na mesma orientação), porque mostram lados opostos; espelhada uma sobre a outra, porém, a semelhança salta para 0,633 — são vistas de mesma profundidade, espelhadas. E cada uma é próxima do seu perfil correspondente (0,519 e 0,482): são **diagonais rasas**, mais perto do perfil do que de um três-quartos de ~45°. A informação genuinamente nova existe (plano do dorso, raiz da cauda, as duas patas traseiras — confirmado visualmente), por isso não é duplicata inútil; mas o ganho angular sobre os perfis já existentes é pequeno. **C4 (DEF/SIL S3, extensão de B7 ao par do Capríleo): pendência nomeada** — uma futura diagonal profunda (~45°) de um dos lados enriqueceria o conjunto; não bloqueia, pelo mesmo critério com que o lote 2 fechou com B7 aberto. O topo, por contraste, é vista própria (0,28–0,44 contra todas as demais, sem parente próximo).

## 4. Verificações NOVAS desta rodada (escalada APR-01, obrigatórias)

### 4a. ATRIBUIÇÃO DE LADO DAS DIAGONAIS TRASEIRAS — FALHA: C1 SYM S2

**Regra de atribuição (geometria, não rótulo):** fixado o animal voltado para o norte, uma foto traseira-esquerda (câmera a sudoeste, olhando para nordeste) projeta a cabeça à ESQUERDA da imagem e mostra o flanco esquerdo; uma foto traseira-direita (câmera a sudeste, olhando para noroeste) projeta a cabeça à DIREITA e mostra o flanco direito. A cauda, que anatomicamente curva para o lado direito do animal (âncora das costas: cauda para a direita da imagem vista por trás), aparece à direita da imagem na vista traseira-esquerda (lado afastado) e à esquerda na vista traseira-direita (lado da câmera, varrendo o primeiro plano). O chifre próximo confirma: o chifre esquerdo (perfil esquerda canônico) tem a ponta enrolada num segundo anel pequeno e fechado; o chifre direito (perfil direita canônico) tem a ponta num gancho aberto em "C".

| Âncora | `diag_tras_esq` (arquivo) | `diag_tras_dir` (arquivo) |
|---|---|---|
| Posição da cabeça | à DIREITA (focinho para a direita) | à ESQUERDA (focinho para a esquerda) |
| Cauda na imagem | varre para a esquerda inferior, ponta enrolando para cima | varre para a direita inferior, ponta apontando para baixo-esquerda |
| Flanco visível | direito (perna dianteira próxima à direita, garupa próxima ao centro) | esquerdo (perna dianteira próxima à esquerda, garupa próxima ao centro-direito) |
| Motivo do chifre próximo | gancho aberto em "C", ponta para baixo-esquerda (zoom `esq_cabeca_chifres`) = chifre DIREITO | segundo anel pequeno e fechado dentro do anel maior (zoom `dir_cabeca_chifres`) = chifre ESQUERDO |
| Correlação com perfis (seção 3b) | 0,519 com perfil direita (0,186 espelhado) | 0,482 com perfil esquerda (0,194 espelhado) |
| **Lado real mostrado** | **Traseira-DIREITA** | **Traseira-ESQUERDA** |

**As cinco âncoras concordam, e todas apontam para a inversão dos rótulos:** o arquivo chamado `diag_tras_esq` contém a vista traseira-direita, e o arquivo chamado `diag_tras_dir` contém a vista traseira-esquerda. Não se trata de imagem espelhada internamente — cada vista é coerente em si (chifre, flanco e cabeça concordam dentro dela) — e sim de **troca de lado no par rotulado**, o que para o arsenal tem o mesmo efeito prático do B1 do lote 2: um modelador que usar o arquivo `esq` para detalhar o lado esquerdo copiará o chifre direito e a curva da cauda do lado errado. **C1 (SYM S2).** Remédio na seção 7: renomear, não regenerar. (Se o projeto documentasse outra convenção de nomes — p. ex., pelo lado da cauda na imagem — ela precisaria estar escrita no REGISTRO; pela convenção do arsenal, lado do animal visível / lado da câmera, a troca acima é o fato medido.)

### 4b. CONTAGEM DE GARRAS POR PATA COM ZOOM + CONTINUIDADE DA CRISTA DORSAL — PASSA (sem defeito)

**Referência canônica:** 4 garras por pata — frente canônica (4 nas três patas dianteiras visíveis), perfis (4 por pata) e o próprio topo deste lote (abaixo). Em vista oblíqua, a 4ª garra pode ficar oclusa atrás da pata; conta visível de 3 com dígitos distintos e sem fusão é oclusão normal, não falta.

**Garras contadas (imagem plena + zooms; dígitos distintos, garras escuras, nenhuma fundida, nenhuma pata com 5+):**

| Vista / pata | Garras visíveis | Leitura |
|---|---|---|
| `diag_esq` — traseira próxima (centro) | 4 (2 grandes frontais + 1 inferior + 1 de borda) | canônico |
| `diag_esq` — dianteira próxima (direita) | 3 nítidas + 1 oclusa atrás (recorte próprio confirma 2 grandes + 1 arredondada de perfil) | oclusão normal |
| `diag_esq` — dianteira afastada (centro) | 3 | oclusão normal |
| `diag_esq` — traseira afastada (esquerda inferior) | 3–4 (recorte próprio: 1 grande à direita + dedos arredondados de trás, sem fusão) | oclusão normal (pata vista por trás) |
| `diag_dir` — dianteira próxima (esquerda) | 4 (recorte próprio: 2 grandes + 1 inferior + 1 de borda) | canônico |
| `diag_dir` — dianteira afastada (centro) | 3 (recorte próprio: 2 grandes + 1 pequena) | oclusão normal |
| `diag_dir` — traseira próxima (centro-direita) | 4 | canônico |
| `diag_dir` — traseira afastada (direita) | 3 | oclusão normal |
| `topo` — dianteira esquerda / direita | 4 / 4 (dedos longos, separados, cada um com garra) | canônico |
| `topo` — traseira esquerda / direita | 4 / 4 (zoom `topo_crista_patas`) | canônico |

**Crista dorsal:** fileira ÚNICA e contínua, sem falha, sem fileira dupla, sem espinho fundido, em todas as três vistas. Diagonais: espinhos triangulares do pescoço (7 visíveis saindo da crina no zoom `esq_cabeca_chifres`) ao longo do dorso, diminuindo progressivamente até virarem pequenos relevos na ponta da cauda (zooms `esq_crista_cauda` e `dir_crista_cauda`: ~40 projeções por diagonal, contando as diminutas da ponta; os perfis canônicos mostram ~35–40 — a diferença é o ângulo dorsal, que expõe espinhos que o perfil esconde). Topo: losangos pontudos na linha média exata, do fim da crina à ponta da cauda (zoom `topo_cauda`: a fileira encolhe suavemente até relevos mínimos na curva final, sem interrupção; ~45 elementos contando as diminutas). **Nenhum defeito de garra ou de crista.** O formato "losango" do topo contra o "triângulo" dos perfis é efeito de ponto de vista (o mesmo espinho triangular, visto de cima, lê-se como losango) — não é troca de característica.

## 5. Antecipação do executor — destino item a item

| # | Antecipação declarada | Destino | Evidência deste Crítico |
|---|---|---|---|
| 1 | Margens: `esq` L 8,4/R 12,4/T 4,0/B 2,9%; `dir` L 13,8/R 11,7/T 3,3/B 2,3%; topo L 20,1/R 21,1/T 3,2/B 3,7%; bases < 5%, nada cortado | **CONFIRMADO exatamente** | Máscara própria reproduz os 12 números (seção 1.5) → C5 (S4) |
| 2 | Diagonais próximas dos perfis; `dir` próxima do perfil esquerda, `esq` espelhada do perfil direita; informação nova = dorso + raiz da cauda + traseiras | **CONFIRMADO na substância, e é a pista de C1** | Corr 0,482 (`dir`×perfil esquerda) e 0,519 (`esq`×perfil direita); o "espelhada do perfil direita" do executor é, medido, "família direita" — o que torna o rótulo `esq` insustentável (seção 4a) |
| 3 | Topo é a vista mais forte: focinho para cima sem face frontal, espirais espelhadas, crina repartida, crista na linha média, cauda para a direita inferior consistente com as costas | **CONFIRMADO integralmente** | Seções 3a e 4a; crina repartida visível no zoom `topo_cabeca_chifres`; crista mediana no zoom `topo_crista_patas` |
| 4 | Ressalva do topo: patas muito abertas (leitura de pose espraiada) | **CONFIRMADO e elevado a pendência nomeada** | C2 (PRP S3, seção 3b abaixo) — o executor viu o fato; a classificação e a instrução ao modelador são deste Crítico |
| 5 | Ressalva do topo: espirais dos chifres um pouco mais "caracol" | **CONFIRMADO e elevado a pendência nomeada** | C3 (DEF S3) — ~2–2,5 voltas aparentes no topo contra ~1,25 volta nos perfis |
| 6 | Zooms de forma feitos, mas paleta NÃO medida | **LACUNA PREENCHIDA** | Seção 2: crina e chifre fiéis (deltas 5–14 e 6–10); escamas explicadas por ponto de vista (vs. costas 7–14) |
| 7 | (Implícito) rótulos `esq`/`dir` dados como certos | **REFUTADO por medida** | C1 (seção 4a) — o que a antecipação não cobria |

Saldo: **6/7 confirmados (dois elevados a pendência nomeada) e 1 refutado (C1)**. Diferente do lote 2, a antecipação desta vez não subestimou defeitos de forma — o único S2 escapou porque é um defeito de rótulo, não de pixels: nenhuma medição de cor ou margem o pegaria; só a atribuição de lado (a verificação nova desta rodada) o pega. Lição para o APRENDIZADO_E_FLUXO: checagem de lado tem de existir antes da instalação, não depois.

## 6. Tabela de defeitos

| ID | Imagem | Código | Sev. | Estado | Evidência |
|---|---|---|---|---|---|
| C1 | `diag_tras_esq` + `diag_tras_dir` (par) | SYM | **S2** | **ABERTO — bloqueia o lote** | Seção 4a: 5 âncoras (cabeça, cauda, flanco, motivo do chifre, correlação) provam a troca de rótulos; remédio = renomear (seção 7), sem regenerar |
| C2 | `topo` | PRP | S3 | ABERTO (pendência nomeada) | Pernas abertas lateralmente (~80–90° no par dianteiro, ~45–60° no traseiro, em relação ao eixo do corpo): lê-se pose espraiada, não quadrúpede em pé visto de cima — onde as pernas apareceriam encurtadas e as patas apenas despontando do contorno do corpo. A geometria dorsal está correta; a articulação NÃO deve ser copiada do topo |
| C3 | `topo` | DEF | S3 | ABERTO (pendência nomeada) | Espirais dos chifres mais fechadas que nas fontes ("caracol": ~2–2,5 voltas aparentes contra ~1,25 nos perfis; zoom `topo_cabeca_chifres`). Posição, tamanho, simetria e textura anelada estão certos; o número de voltas deve ser modelado pelos perfis, não pelo topo |
| C4 | par de diagonais | DEF/SIL | S3 | ABERTO (pendência nomeada) | Seção 3b: diagonais rasas — corr 0,519/0,482 com os perfis correspondentes; espelhadas entre si, 0,633. Informação nova real, mas ganho angular pequeno (extensão de B7) |
| C5 | três vistas | SIL | S4 | ABERTO (cosmético) | Bases 2,9% (`esq`), 2,3% (`dir`), 3,7% (topo) — abaixo dos 5% pedidos; nada cortado (precedente B9) |

**Achados positivos registrados:** paleta fiel com números (crina deltas 5–14, chifre 6–10, escamas 7–14 contra as costas); crista única e contínua até a ponta da cauda nas três vistas; 4 garras por pata onde a vista permite ver (topo 4/4/4/4); topo é planta verdadeira (B2 não se repete); nenhum elemento inventado, nenhuma fusão, nenhum rosto errado; margens reproduzidas exatamente. Nenhum defeito S1.

## 7. Especificação de retrabalho (numerada; sem regeneração)

1. **Renomear os dois arquivos da diagonal, por troca simultânea (usar nomes temporários para não sobrescrever):** o conteúdo atual de `caprileo_diag_tras_esq.png` (SHA-256 `efd00a7d…fa180`) passa a chamar-se `caprileo_diag_tras_dir.png`; o conteúdo atual de `caprileo_diag_tras_dir.png` (SHA-256 `46cbe2b9…1ef07a`) passa a chamar-se `caprileo_diag_tras_esq.png`. Os hashes do conteúdo NÃO mudam com a renomeação — conferir isso explicitamente após a troca, no PC e nas cópias locais, e registrar os dois hashes novos por nome no REGISTRO.
2. **Aplicar a mesma troca nos dois lados** (pasta `testes\referencias\` no PC e cópias em `~/workspace/oficina-audit/referencias/`), para não ressuscitar a divergência PC ≠ local.
3. **Re-verificação de fechamento de C1 (checklist, sem novo Crítico completo, salvo decisão do executor):** no arquivo renomeado `diag_tras_esq`, confirmar cabeça à esquerda + motivo de chifre com segundo anel fechado + cauda à direita; no renomeado `diag_tras_dir`, cabeça à direita + gancho em "C" + cauda à esquerda. Se os três itens baterem nos dois arquivos, C1 fecha e o lote fecha.
4. **Registrar a convenção de nomes por escrito** em ESTADO_ATUAL/REGISTRO: "`diag_tras_esq/dir` = lado do animal visível ( = lado da câmera) na vista traseira" — para a próxima rodada não herdar a ambiguidade.
5. **Pendências que NÃO bloqueiam o fechamento pós-C1, mas entram no plano por escrito:** C2 (modelar articulação das patas pelos perfis/costas, nunca pelo topo); C3 (modelar as voltas do chifre pelos perfis); C4 (futura diagonal profunda opcional); C5 (margens — aceitar como está, sem reenquadrar, pois nada está cortado).
6. **O `topo` entra no arsenal já nesta rodada**, com as instruções de C2/C3 anexadas ao seu registro (o modelador precisa lê-las antes de usar o topo para pernas ou chifres).

## 8. Registro da escalada APR-01 desta rodada

Verificações ADICIONADAS pela rodada do lote 3 (Capríleo): **(a) Atribuição de lado das diagonais traseiras** — cabeça, lado da cauda, flanco visível, motivo do chifre próximo e correlação com os perfis, medidos contra costas + perfis sem aceitar os rótulos do executor: pegou C1 SYM S2; **(b) Contagem de garras por pata com zoom + continuidade da crista dorsal** — garras contadas pata por pata e espinhos contados ao longo da linha média, confrontados com perfis e frente: passou sem defeito, mas estabeleceu o padrão (4/pata; fileira única contínua até a ponta). Reaplicadas: pureza da planta no topo (B2 — passa) e diversidade angular medida do par de diagonais (B7 — vira C4 S3). Sugestão de linha para a tabela de escalada de APRENDIZADO_E_FLUXO.md: `01/11/2026 | REF-01 lote 3 (Capríleo) | Atribuição de lado das diagonais traseiras (5 âncoras) + contagem de garras/crista com zoom | Achado C1 SYM S2 (rótulos das diagonais trocados — retrabalho = só renomear); topo aprovado como planta verdadeira; pendências C2 PRP S3 (pernas espraiadas do topo), C3 DEF S3 (chifres-caracol do topo), C4 S3 (diagonais rasas), C5 S4 (margens); LOTE REPROVADO até a renomeação`.

## 9. Conclusão

O lote 3 é, em pixels, um bom lote: o topo é a melhor vista do conjunto, as diagonais entregam o dorso, a raiz da cauda e as traseiras que faltavam, a cor está medida e fiel, e não há garra, espinho ou rosto errado. Ele reprova por um motivo só, mas que o critério de aceite não permite relativizar: **os dois arquivos diagonais vestem o nome do lado oposto**. É o tipo de erro que custa pouco agora (uma renomeação + uma conferência de hashes) e custaria um modelo espelhado depois — por isso o veredito é reprovação condicional, não aprovação com ressalva. Feita a seção 7, o Capríleo entra no arsenal com frente, costas, dois perfis, duas diagonais traseiras corretamente rotuladas e um topo verdadeiro.

**Assinatura:** Crítico Visual sênior (agente independente), 01/11/2026. Veredito técnico; a palavra final de fidelidade artística é do Mestre.

---

## Vereditos (linhas inequívocas)

- `caprileo_diag_tras_esq.png` (conteúdo atual, vista traseira-direita): **IMAGEM APROVADA, RÓTULO REPROVADO** — só entra no arsenal renomeada para `diag_tras_dir` (C1 SYM S2)
- `caprileo_diag_tras_dir.png` (conteúdo atual, vista traseira-esquerda): **IMAGEM APROVADA, RÓTULO REPROVADO** — só entra no arsenal renomeada para `diag_tras_esq` (C1 SYM S2)
- `caprileo_topo.png`: **APROVADA como vista de topo** (pendências C2 S3, C3 S3, C5 S4)
- **LOTE 3 (Capríleo): REPROVADO — retrabalho = apenas a renomeação da seção 7 + re-verificação de hashes; nenhuma regeneração necessária**

---

## Nota do executor (01/11/2026, rodada oficina3d-referencias)

Veredito recebido e relatório preservado localmente NESTE arquivo. **Instalação no PC e registro nos documentos do projeto (REGISTRO/ESTADO/APRENDIZADO + commit só de documentos) ADIADOS para a próxima rodada pela regra anti-colisão da frente:** no momento do veredito, a árvore do repo no PC estava suja com a tranche da frente principal (Etapa COR, integração do `cor` à fila: `oficina3d/cli.py`, `config.py`, `job.py`, `worker.py` modificados; `oficina3d/cor/passo.py` e `testes/test_cor_passo.py` novos) — e a regra manda NÃO escrever no repo com a árvore suja. Nenhuma escrita no PC foi feita nesta rodada após o veredito; conferido explicitamente que os 3 arquivos seguem com os nomes e hashes originais no PC (esq `efd00a7d…fa180`, dir `46cbe2b9…1ef07a`, topo `f0927007…38b634`, sem arquivo temporário). **Retrabalho pendente exato (próxima rodada, com a árvore limpa):** (1) trocar os nomes das diagonais nos DOIS lados (PC `testes\referencias\` + `~/workspace/oficina-audit/referencias/`) via nome temporário; (2) conferir que os hashes por conteúdo não mudaram; (3) re-verificação C1: no renomeado `diag_tras_esq` confirmar cabeça à esquerda + chifre com segundo anel fechado + cauda à direita; no renomeado `diag_tras_dir`, cabeça à direita + gancho em "C" + cauda à esquerda; (4) instalar este relatório como `docs/CRITICO-ref01-lote3.md` e registrar veredito + convenção de nomes (`diag_tras_esq/dir` = lado do animal visível = lado da câmera) + pendências C2/C3/C4/C5 em REGISTRO/ESTADO/APRENDIZADO (linha de escalada + lição nova: checagem de lado ANTES da instalação); (5) commit + push só de documentos. Confirmação visual pré-renomeação do executor: o arquivo atual `diag_tras_esq` mostra cabeça à direita e cauda para a esquerda inferior; o atual `diag_tras_dir` mostra cabeça à esquerda e cauda para a direita inferior — consistentes com as âncoras do Crítico.
