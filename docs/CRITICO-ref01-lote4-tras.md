# CRÍTICO VISUAL — REF-01 lote 4 parcial (diagonais traseiras do Orc)

**Papel:** Crítico Visual sênior independente e ADVERSÁRIO (APR-02). Missão: tentar
reprovar. Nada aqui é benevolência: o que está aprovado passou por medição, não por
simpatia ao esforço.
**Data:** 01/11/2026. **Escopo:** SOMENTE o par traseiro. O par frontal, reprovado pelo
próprio executor na autoauditoria, NÃO foi julgado aqui.

## Arquivos julgados

| Arquivo | Tamanho | SHA-256 (local, conferido na leitura) |
|---|---|---|
| `orc_diag_tras_dir.png` | 1328 × 1904 px, 2.277.440 B | `acb515d2…7372250b` |
| `orc_diag_tras_esq.png` | 1328 × 1904 px, 2.128.241 B | `6d0b0b35…37a6ca26413` |

## Fontes canônicas (ordem de autoridade)

1. `orc_frente.png` (frente canônica — cor e inventário)
2. `orc_costas.png` (costas canônicas)
3. `orc_costas_v2.png` (costas aprovadas no lote 1)
4. `orc_tpose_v2.png`, `orc_tresquartos_v2.png` (aprovadas no lote 1)
5. Autoauditoria do executor: `oficina-audit/autoauditoria-orc-diag-tras.md`
   (lida antes do julgamento; NADA dela foi tomado como verdade — tudo foi re-medido)

**Método:** leitura visual das imagens inteiras + zooms 2× de cabeça, ombros/alça,
cinto, mãos e pés + medições por pixel (máscara de silhueta por distância ao fundo,
IoU, centroides, assimetria da faixa inferior, amostragem de cor com filtro oliva).
Convenção de lados em vista de COSTAS (rotação de 180°, não espelho): o lado direito
do personagem aparece à DIREITA de quem olha; o lado esquerdo, à ESQUERDA. Verificado
contra `orc_costas.png`/`orc_costas_v2.png`: cabeça-de-lobo (ombro esquerdo) à esquerda,
ombreira de espinhos (ombro direito) à direita.

**Severidades:** S1 = impede o uso como referência; S2 = erro de fidelidade que exige
retrabalho da imagem; S3 = desvio visível tolerável com registro; S4 = observação /
limitação de leitura, sem retrabalho.

## 1. Tabela de âncoras (medida, não estimada)

"Viewer" = quem olha a imagem. "Lado correto" = lado exigido pelo rótulo do arquivo.

| Âncora | `tras_dir` (rótulo: direita) | `tras_esq` (rótulo: esquerda) |
|---|---|---|
| Cabeça-de-lobo (ombro ESQ do personagem) | À ESQUERDA, focinho para a esquerda — correto para costas | À ESQUERDA, focinho para a esquerda — **lado errado para o rótulo**: numa diagonal esquerda genuína o lado do lobo seria o lado PRÓXIMO (proeminente em primeiro plano), não recuado atrás da capa como aqui |
| Ombreira de espinhos (ombro DIR) | À DIREITA, proeminente, em primeiro plano — correto: lado próximo da câmera direita-traseira | À DIREITA, proeminente, em primeiro plano — **idem à `tras_dir`**: o lado próximo é o mesmo, não o oposto |
| Rosto (perfil parcial) | Perfil parcial à DIREITA (nariz para a direita, orelha + brinco + presa visíveis) — correto: olha por cima do ombro direito, para a câmera direita-traseira | Perfil parcial à DIREITA (nariz para a direita) — **idêntico à `tras_dir`**; uma diagonal esquerda exigiria perfil à ESQUERDA |
| Alça diagonal + fivela | Fivela central, descida para o quadril viewer-direito — **idêntica a `costas_v2`** | Fivela central, descida para o quadril viewer-direito — **idêntica a `tras_dir` e a `costas_v2`**; uma diagonal esquerda exigiria a descida espelhada (para o quadril viewer-esquerdo) |
| Placa do cinto (losango) | Central, conforme `costas_v2` | Central, conforme `costas_v2` |
| Caveira grande + presas + argolas do cinto | Caveira grande à DIREITA de quem olha, argolas + pingente em seta abaixo, presas ladeando a caveirinha central — conforme `costas_v2` | **Exatamente a mesma disposição** (caveira grande à direita) — uma vista do lado oposto exigiria a caveira grande à esquerda, sob a convenção "cinto visível por trás" já estabelecida em `costas_v2` |
| Direção dos pés | Pé viewer-DIREITO em perfil lateral total (ponta para a direita); pé viewer-ESQUERDO em vista traseira (calcanhar) — coerente com corpo girado para a sua direita | **Idêntico**: pé viewer-DIREITO em perfil (ponta para a direita); pé viewer-ESQUERDO traseiro — o pé em perfil NÃO trocou de lado |
| Capa de pele | Domina o dorso, desce abaixo da cintura até meia-canela no lado viewer-esquerdo — sem D13 (capa curta) | Idem, mesma queda e mesma extensão |
| Mãos | Punhos fechados, sem dígito extra visível; mão viewer-direita com polegar enrolado legível; mão viewer-esquerda parcialmente oculta atrás da capa (oclusão esperada em 3/4) | Punhos fechados, sem dígito extra; mesma oclusão parcial da mão viewer-esquerda |
| Tom de pele / vermelho | Família oliva; saiote (151,31,27) vs frente (153,34,28): Δ ≤ 3 — conforme | Família oliva; saiote (152,31,26) vs frente: Δ ≤ 3 — conforme |
| Inventário proibido | Zero bolsinhas, zero machado, zero personagem extra, zero texto/marca | Zero bolsinhas, zero machado, zero personagem extra, zero texto/marca |
| Corpo inteiro / margens | Inteiro; bbox x 196–1117, y 88–1819 (margens: esq 14,8%, dir 15,9%, sup 4,6%, inf 4,5%) | Inteiro; bbox x 186–1114, y 87–1822 (margens equivalentes) |

**Leitura da tabela:** cada âncora lateralizada, isoladamente, está do lado CORRETO
para uma vista de costas — e é exatamente por isso que o defeito do par é grave:
as duas imagens passam nas âncoras de costas, mas **falham como PAR**, porque
representam o MESMO lado. Nenhuma âncora cruzou a linha média; o problema não é
espelhamento interno, é duplicação de lado.

## 2. Tabela de defeitos

| Código | Sev. | Imagem | Defeito e evidência medida |
|---|---|---|---|
| SYM-4.1 | **S2** | `orc_diag_tras_esq.png` | **Lado errado: diagonal direita duplicada como esquerda.** A imagem rotulada "esq" mostra a diagonal direita-traseira, não a esquerda. Provas convergentes, todas medidas: (1) rosto em perfil à direita (nariz para a direita) nas DUAS imagens — zooms de cabeça; (2) pé em perfil no lado viewer-direito nas DUAS, pé traseiro no viewer-esquerdo nas DUAS — zooms de pés; (3) assimetria da faixa inferior (y 0,80–0,99) com o MESMO sentido: `tras_dir` dir/esq = 70.854/39.910 = **1,78**; `tras_esq` = 67.716/38.594 = **1,75**; contra `costas_v2` simétrica = 52.876/52.003 = **1,02**. Uma diagonal esquerda genuína exigiria assimetria INVERTIDA (≈ 0,56); (4) silhuetas quase-idênticas: IoU bruto 0,895 e IoU alinhado por bbox **0,915** entre as duas, contra 0,765 (`tras_dir` × `costas_v2`) e 0,779 (`tras_esq` × `costas_v2`) — as duas traseiras se parecem entre si MUITO mais do que qualquer uma se parece com as costas retas; (5) centroides quase coincidentes (cx 0,482 vs 0,472; cy 0,500 vs 0,497) e bboxes quase iguais (922×1732 vs 929×1736 px); (6) proeminência do lado do lobo vs ombreira idêntica nas duas (lobo recuado, ombreira em primeiro plano). Conclusão: não é "baixa diversidade angular" — é **diversidade lateral zero**. |
| DEF-4.2 | S4 | ambas | **Tom de pele levemente mais escuro/saturado que `costas_v2`.** Amostragem com filtro oliva (G > B+15, G ≥ R−15): braço viewer-direito — `costas_v2` (126,118,64) sat 0,492; `tras_dir` (110,96,50) sat 0,541; `tras_esq` (101,87,46) sat 0,545. Mão viewer-direita — `costas_v2` (118,109,58) sat 0,508; `tras_dir` (97,83,42) sat 0,567; `tras_esq` (110,98,54) sat 0,509. Direção OPOSTA ao D5 (tom claro) dos lotes anteriores; mesmo matiz oliva, sem desvio para outro tom. Ressalva de método: as caixas anatômicas fixas capturam poucos pixels oliva puros nas traseiras (122–221 px, braço girado), porque armadura/pele se misturam na caixa — o delta é real mas pequeno (≈ +0,05 de saturação, −15 a −25 de luminância) e NÃO justifica reprovação. O vermelho do saiote, medido na mesma caixa, é praticamente idêntico ao canônico (Δ ≤ 3 por canal). |

**Caça aos modos de falha dos lotes anteriores — resultado:**

| Modo | Resultado |
|---|---|
| D10 espelhamento | NÃO PRESENTE em `tras_dir` (lado correto). Em `tras_esq` o erro é de outra natureza (lado duplicado, SYM-4.1), não espelho interno |
| D9/D11 bolsinhas | ZERO nas duas (conferido nos zooms de cinto) |
| D13 capa curta | NÃO PRESENTE: capa domina o dorso e desce até meia-canela |
| D3/D4 fusões | NÃO PRESENTE: punhos sem dígito extra; botas com biqueira de espigão nos DOIS pés — conferido na frente canônica, onde o pé viewer-esquerdo (direito do personagem) TAMBÉM tem biqueira com espigão; logo, o espigão do pé em perfil NÃO é erro de lateralização |
| D5 tom claro | NÃO PRESENTE (direção oposta, ver DEF-4.2, S4) |
| D15 palmas para a frente | NÃO PRESENTE: punhos fechados, palmas não voltadas para a câmera |

**Suspeitas da autoauditoria — veredito do Crítico:**

1. Diversidade angular: CONFIRMADA e agravada — não é "próxima", é o mesmo lado (SYM-4.1, S2).
2. Tom de pele: CONFIRMADA como delta pequeno (DEF-4.2, S4), sem força para reprovar.
3. Pés/mãos: FECHADA a favor das imagens — pés coerentes com o giro do corpo
   (perfil à direita + traseiro à esquerda, nos dois casos o giro é para a direita);
   punhos sem dígito extra. Limitação registrada: punho fechado não permite contagem
   de 5 dígitos — isso é limite de leitura, não defeito.
4. Alça dorsal: FECHADA a favor das imagens — trajeto idêntico ao de `costas_v2`
   (fivela central, descida para o quadril viewer-direito). Observação de registro,
   NÃO defeito deste lote: a alça desce para o mesmo lado na frente e nas costas,
   o que é geometricamente estranho para uma única faixa — mas essa é a convenção
   já estabelecida pela frente canônica e pelas costas aprovadas no lote 1; as
   traseiras apenas a reproduzem. Não se cobra deste lote o que a autoridade já
   consagrou.

**Outras observações S4 (sem retrabalho):** o cilindro estriado à direita do cinto
(cabo de ferramenta/punhal) existe identicamente na frente canônica e em `costas_v2` —
é kit canônico, não arma extra. A mão viewer-esquerda parcialmente oculta pela capa
nas duas traseiras é oclusão esperada em 3/4; o modelador deve usar `costas_v2` para
essa mão. Ausência de machado: conforme a especificação deste lote (como a
`tresquartos_v2` aprovada), embora `orc_costas.png` canônica mostre o machado na mão
direita — divergência de especificação registrada, não defeito.

## 3. Verificações novas desta rodada (escalada APR-01, seção 6)

Registradas como verificações permanentes do checklist pré-Crítico a partir deste lote:

- **N1 — Pureza do 3/4 traseiro.** Critérios aplicados: rosto SÓ em perfil parcial
  (nenhuma das duas mostra o rosto de frente — APROVADO nas duas); capa dominando o
  dorso e abaixo da cintura (APROVADO nas duas); pés apontando para longe do
  observador (APROVADO: pé em perfil aponta para a direita-longe, pé traseiro mostra
  o calcanhar). N1 não reprova nenhuma das duas — o que reprova `tras_esq` é N2.
- **N2 — Diversidade angular MEDIDA do par (não impressionista).** A partir deste
  lote, um par dir/esq só é aceito se cumprir OS TRÊS: (a) IoU entre as duas
  silhuetas < 0,85; (b) assimetria da faixa inferior INVERTIDA entre elas
  (razão dir/esq de um lado > 1,4 e do outro < 0,7); (c) pé em perfil em lados
  opostos. Este par falha nos três: IoU 0,915; razões 1,78 e 1,75 (mesmo sentido);
  pé em perfil à direita nas duas. N2 é o instrumento que transforma a suspeita
  "parecem próximas" do executor no defeito SYM-4.1.
- **N3 — Tom de pele MEDIDO por amostragem anatômica.** A partir deste lote, "tom"
  não se julga a olho: amostra-se a mesma caixa anatômica na fonte e no lote com
  filtro oliva e reportam-se mediana RGB e saturação. Aplicado aqui (ver DEF-4.2);
  o saiote vermelho entra como controle interno (Δ ≤ 3 = conforme).

## 4. Retrabalho exato (só `tras_esq`; `tras_dir` fica como está)

**NÃO espelhar `tras_dir` no editor de imagens** — espelhar produziria um falso
esquerdo com a textura do dorso invertida. Gerar de novo, do lado oposto, com esta
lista de âncoras (cada item é critério de aceite, conferível a olho e por medição):

1. Câmera na retaguarda ESQUERDA do personagem (lado da cabeça-de-lobo).
2. Rosto em perfil parcial apontando para a ESQUERDA de quem olha (nariz para a
   esquerda); orelha esquerda visível.
3. Cabeça-de-lobo PROEMINENTE em primeiro plano à esquerda; ombreira de espinhos
   recuada à direita.
4. Pé viewer-ESQUERDO em perfil lateral apontando para a esquerda; pé
   viewer-direito em vista traseira (calcanhar).
5. Alça com fivela central descendo para o quadril viewer-ESQUERDO (espelhada em
   relação a `costas_v2`).
6. Caveira grande do cinto à ESQUERDA de quem olha; placa em losango central mantida;
   presas, argolas e pingente em seta mantidos.
7. Painel da capa proeminente à esquerda, descendo abaixo da cintura até meia-canela.
8. Manter: zero bolsinhas, zero machado, corpo inteiro sem corte, fundo cinza-claro
   liso, tom oliva de `costas_v2`.
9. Critério de aceite numérico do novo par: IoU com `tras_dir` < 0,85 E razão
   dir/esq da faixa inferior < 0,7 E pé em perfil no lado esquerdo — os três, não
   um só. A nova imagem volta ao Crítico antes de ser instalada como definitiva; o
   arquivo atual `orc_diag_tras_esq.png` deve ser SUBSTITUÍDO, não mantido ao lado
   da refeita (duas "esquerdas" perpetuariam a ambiguidade).

## Veredito

orc_diag_tras_dir.png: APROVADA
orc_diag_tras_esq.png: REPROVADA
LOTE 4 parcial (traseiras): REPROVADO

Motivo em uma frase: o lote entrega UMA diagonal traseira excelente (a direita) e a
apresenta duas vezes — falta a diagonal esquerda, que é metade do que o par promete.
