# D-H0 — Auditoria de consistência cruzada das 4 referências do Orc

**Tranche P0 (diagnóstico de raiz da D1), 01/11/2026. Executor: Muse CM-000009.
Exigência:** C-05 do Crítico do estudo de raiz (docs/CRITICO-estudo-raiz-d1.md):
ninguém tinha auditado se as 4 referências concordam ENTRE SI; sem isso, a
discordância que D-H4.2 vier a medir não se pode atribuir a registro (H1)
nem a junção (H4) — ela pode nascer na fonte.
**Status deste documento:** relatório do executor, pendente do veredito do
Crítico sênior (a submeter com bateria escalada, APR-02).

## 1. Sujeito: o insumo real do bake, não o arsenal v2

As 4 vistas canônicas efetivamente usadas pelo bake COR são o conjunto
dourado `testes/dourado/imagens/` (imagens 1280×1820, RGBA, fundo
transparente). SHAs conferidos PC = local, byte a byte:

| vista | arquivo | SHA-256 |
|---|---|---|
| frente | orc_frente.png | 30C0F83D…C903B6C |
| costas | orc_costas.png | 256C8A2F…97FD20F |
| esquerda | orc_esquerda.png | 769E600D…AF6681 |
| direita | orc_direita.png | 4F4775E2…010C59 |

**Divergência documental registrada (D-H0-P1, pendência nova):** a costas
dourada NÃO é a costas aprovada pela REF-01: `orc_costas_v2.png` tem SHA
09890D74… — outro arquivo. O arsenal REF-01 v2 do Orc tem só 3 vistas
(tpose_v2, costas_v2, tresquartos_v2) e nenhuma lateral canônica; logo, o
bake não usa o arsenal aprovado. O D-H0 julga o insumo real do bake (o
dourado). A migração do bake para o arsenal aprovado — ou a aprovação
formal do conjunto dourado — fica pendente e NÃO é decidida aqui.

## 2. Instrumento (pré-registrado antes de medir)

- **Máscara:** canal alfa (fundo transparente), limiar 128. Sensibilidade
  nos limiares 1, 128 e 200 (ver §5: o limiar 254 é inválido nestas imagens).
- **Geometria:** bbox da máscara, ocupação do bbox, perfil de largura em
  100 faixas de altura, IoU de silhueta bbox-alinhada a 256 px (esticado,
  como a régua COR-08, e preservando a razão de aspecto).
- **Marcos verticais:** 5 marcos lidos por grounding com a MESMA pergunta
  nas 4 vistas (topo do topete, fivela-losango do cinto, crânio grande do
  cinto, ponta do pano vermelho do cinto, joelheiras com espinhos), em
  coordenadas 0-1000, convertidos para y em fração da altura do bbox
  (0 = topo, 1 = base). A tabela integral está em
  `oficina3d/diagnostico_dh0_dados.json`; o cálculo, em
  `oficina3d/diagnostico_dh0.py` (função `faixas_dos_marcos`, testada).
- **Régua pré-registrada:** faixa (max−min) > 0,05 num marco de tronco =
  bandeira de inconsistência; > 0,10 = severa. O D-H0 atribui causa; ele
  sozinho não aprova nem reprova a D1.
- **Duas regras de leitura que mudam o juízo (registradas antes de medir):**
  (a) IoU frente×costas NÃO prova inconsistência — vistas opostas de um
  ser com capa grande nas costas e machado na mão lateral têm assimetria
  legítima (a capa aparece por trás; o machado na mão direita aparece à
  esquerda na frente e à direita nas costas); (b) o lado horizontal do
  kit NÃO se julga por espelhamento físico — a REGRA FINAL do Orc
  (reconciliação REF-01 lote 4, §5) manda o crânio sempre à DIREITA do
  losango em coordenadas de imagem, em qualquer vista.

## 3. Geometria das silhuetas

| vista | bbox (px) | largura × altura | razão L/A | ocupação |
|---|---|---|---|---|
| frente | 147,167–1147,1656 | 1001 × 1490 | 0,6718 | 0,6015 |
| costas | 148,178–1139,1610 | 992 × 1433 | 0,6923 | 0,5601 |
| esquerda | 148,153–1144,1651 | 997 × 1499 | 0,6651 | 0,5377 |
| direita | 211,151–1109,1667 | 899 × 1517 | 0,5926 | 0,5740 |

**IoU bbox-alinhado:** frente×costas 0,5638 (esticado) / 0,5623
(aspecto); esquerda×direita 0,5628 / 0,5532; esquerda×direita ESPELHADO
0,7887 / 0,7876. Leitura: os pares laterais espelhados casam bem (0,79);
o par frente×costas casa pouco (0,56) — mas, pela regra §2(a), isso mede
sobretudo a assimetria legítima de vista oposta, não contradição de fonte.

**Perfil de largura por região (diferença média absoluta):**

| região | frente × costas | esquerda × direita |
|---|---|---|
| cabeça (0–15) | 0,0829 | 0,0553 |
| tronco (15–40) | 0,1511 | 0,0643 |
| cinto/saia (40–65) | 0,0612 | 0,0401 |
| pernas/pés (65–100) | 0,0959 | 0,0601 |

O pico frente×costas no tronco (0,1511) é a capa: por trás ela cobre o
tronco inteiro; pela frente, só ombros e bordas. É o comportamento
esperado de uma capa, não uma contradição.

## 4. Marcos verticais — o juiz do D-H0

y em fração da altura do bbox (centro da caixa do marco):

| marco | frente | costas | esquerda | direita | faixa |
|---|---|---|---|---|---|
| topete (centro) | 0,0278 | 0,0346 | 0,0339 | 0,0295 | **0,0068** |
| fivela-losango | 0,5027 | 0,4883 | 0,4859 | 0,4646 | **0,0381** |
| crânio do cinto | 0,5412 | 0,5436 | 0,5315 | 0,5043 | **0,0393** |
| ponta do pano vermelho | 0,8412 | 0,8353 | 0,8000 | 0,8050 | **0,0412** |
| joelheiras | 0,8015 / 0,7453 | 0,7768 / 0,7717 | 0,8030 | 0,7306 | **0,0724** |

**Resultado: nenhum marco de tronco ultrapassa a régua 0,05.** O maior
desvio de tronco (pano vermelho, 0,0412) e os demais (0,038–0,039) ficam
abaixo da bandeira. **Só os joelhos ultrapassam (0,0724)** — e joelho é
pose, não anatomia de tronco: a frente tem pernas em passo assimétrico
(0,7453 × 0,8015 dentro da própria vista), as costas têm pernas simétricas
(0,7717 × 0,7768) e as laterais têm passada larga (direita 0,7306, a
perna da frente mais baixa). As 4 vistas NÃO partilham uma única pose de
pernas — isso é diferença de pose entre renders, não contradição de
cinto/crânio.

**Checagem da regra final do Orc:** o crânio está à direita da fivela em
coordenadas de imagem nas 4 vistas (centros x: frente 589,5 > 458,0;
costas 549,0 > 447,5; esquerda 502,5 > 420,0; direita 668,5 > 622,0). A
regra do cânone se confirma no conjunto dourado.

## 5. Sensibilidade do instrumento (C-07) e o artefato do limiar 254

IoU frente×costas nos limiares 1 / 128 / 200: 0,5793 / 0,5638 / 0,5558
(Δ total 0,0235). IoU esquerda×direita espelhado: 0,7949 / 0,7887 / 0,7863
(Δ 0,0086). O instrumento é estável ao limiar.

**Artefato achado e excluído pelo executor:** o limiar 254 dá IoU ≈ 0,0002
— não porque as silhuetas mudem, mas porque o platô de alfa do primeiro
plano fica em 252–253 em frente/esquerda/direita (costas: 254–255). A 254,
a frente some quase inteira (fração ≥254 = 0,0000). O limiar 254 é, pois,
inválido nestas imagens, e a sensibilidade publicada usa 1/128/200. O
platô de alfa diferente entre costas e as demais é mais uma impressão
digital de processamento distinto por arquivo — registrada, sem peso no
veredito.

## 6. O que NÃO foi medido (declarado, não omitido)

- **Tom de pele por vista:** não medido. A caixa central de tronco
  (x 0,35–0,65; y 0,30–0,45 do bbox) mistura pelo da capa, peito e
  armadura; suas medianas (frente 98,62,39; costas 109,74,52; esquerda
  122,79,50; direita 108,71,41) NÃO são tom de pele e não se usam como
  tal. Medir pele exige segmentação por cor, fora desta tranche.
- **Precisão do grounding:** as caixas são aproximadas; a incerteza
  estimada é ~0,01–0,02 em y normalizado. As faixas de tronco (0,038–0,041)
  estão a ~2× o ruído do instrumento: a conclusão honesta é "sem
  bandeira acima de 0,05", não "concordância exata".
- **Joelho lateral:** 1 caixa por vista lateral (a perna distante está
  ocluída/fundida à próxima); a faixa de joelho usa as caixas disponíveis.

## 7. Painel de métricas do Mestre (ordem de 01/11 19:06)

Esta tranche NÃO executou job de modelagem, geração ou texturização:
nenhum modelo foi gerado, nenhuma GPU foi usada, nenhum GLB resultou.
Por isso: tempo de job = não se aplica; pico de VRAM/RAM/CPU = não
medido (medições em CPU sobre PNGs, sem instrumentação de pico);
triângulos = não se aplica; peso em disco = não se aplica (nenhum GLB);
tokens = não se aplica (nenhuma plataforma de geração expôs tokens).
As medições desta tranche são CPU local sobre 4 PNGs de ~2 MB cada.

## 8. Veredito do executor (pendente do Crítico)

- **D-H0 CONCLUÍDO: a "quinta causa" NÃO se confirma no tronco.** Cinto,
  crânio e pano vermelho concordam verticalmente entre as 4 vistas dentro
  da régua (faixas ≤ 0,0412 < 0,05). A discordância que D-H4.2 vier a
  medir NÃO pode ser atribuída a "o cinto está noutra altura na frente e
  na lateral" — essa contradição não existe nestes dados.
- **O que o D-H0 entrega ao resto do P0:** (a) H1 segue a hipótese
  principal, mas D-H1.2 (decomposição por região) DEVE separar pernas de
  tronco — a diferença de pose das pernas (joelhos 0,0724, passo
  assimétrico na frente × simétrico nas costas) é parte do teto de IoU
  e não deve contaminar a régua do corpo; (b) D-H4.2 pode prosseguir sem
  a ressalva de fonte contraditória no tronco; (c) o IoU frente×costas
  (0,56) NÃO entra como prova de nada — é assimetria de vista oposta.
- **Portão REF-01:** o D-H0 NÃO reprova o conjunto dourado. Mas o portão
  só vale para o conjunto que o bake usa: a pendência D-H0-P1 (dourado ≠
  arsenal v2 aprovado) segue aberta e deve ser resolvida antes de qualquer
  afirmação de que "as referências aprovadas alimentam o bake".
- **Qualidade visual:** NENHUMA alegação nova nesta tranche (nenhum
  resultado visual novo; as imagens julgadas são os insumos, não uma
  saída). O mecanismo do D-H0 (script + tabela + testes) é o que vai ao
  Crítico; a qualidade visual da cor segue com o veredito da COR-08
  (7,0/10 com ressalva, D1 aberta).

## 9. Autoauditoria adversarial (APR-02, antes de submeter)

Defeitos achados pelo próprio executor e corrigidos ou declarados:
1. Limiar 254 inválido (platô de alfa) — corrigido para 1/128/200 (§5).
2. Interpretação ingênua do IoU frente×costas como "inconsistência" —
  corrigida pela regra §2(a) antes de escrever qualquer conclusão.
3. Grade da frente não renderizou no contexto do executor — substituída
  por grounding uniforme nas 4 vistas (mesma pergunta, coordenadas
  auditáveis), superior à leitura a olho.
4. Caixa central de tronco NÃO é tom de pele — medição retirada do
  veredito e declarada em §6, em vez de publicada como "pele".
5. Joelho lateral com caixa única — declarado em §6; a faixa de joelho
  é lida como pose, não como contradição de fonte.
6. Dourado ≠ v2: achado na checagem de SHA antes de medir — virou a
  pendência D-H0-P1 em vez de ser varrido para debaixo do relatório.
Restos conhecidos: precisão do grounding (~0,01–0,02) limita a
afirmação a "sem bandeira"; pele por vista segue sem instrumento;
D-H0-P1 segue aberta.
