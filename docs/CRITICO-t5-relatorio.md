# Crítico sênior — Etapa T5 (UV de qualidade com xatlas)

- **Data da auditoria:** 01/11/2026 (manhã; terceira rodada da sonda Blender concluída com `ok=True`).
- **Alvo:** `app/oficina3d/uv_xatlas.py`, `app/oficina3d/cor/_blender_uv_xatlas.py`,
  `app/testes/test_uv_xatlas.py`, commit `ac8c15a`, e a prova no Orc Prata
  (`jobs/20261031-225432-provac-orc-s7/saida/modelo.glb`, 49.750 tris).
- **Escopo do veredito (estrito):** APROVA ou REPROVA **a T5 como passo de UV**.
  NÃO aprova D1 (fidelidade de detalhe), NÃO aprova o T1-completo, NÃO aprova
  determinismo geral do app — só o que esta bateria provou.
- **Postura:** nada aceito por fé. Todas as métricas abaixo foram recalculadas
  por decode próprio do GLB (sem Blender, sem trimesh), e os passos longos
  foram reexecutados no PC via tarefa agendada `CriticoT5` (criada sem trigger,
  disparada por `Start-ScheduledTask`, removida ao final — `TASK_ABSENT`
  confirmado). Nenhum código do projeto foi alterado e nada foi commitado.
- **Taxonomia (a do relatório do T1):** S1 = invalida a etapa (reprova);
  S2 = grave para a qualidade final / T1-completo, não para o passo;
  S3 = defeito/limitação relevante, sem reprovar; S4 = nota menor.

## Evidências lidas e medidas

- `jobs_teste/cor_t5/orc_xatlas/` integral: `uv.npz`, `modelo_uv.glb`,
  `modelo_cor.glb`, `textura.png`, `resultado_uv_xatlas.json`,
  `resultado_cor.json`, `metricas_xatlas.json`, `blender_uv_xatlas.log`,
  prévias `previa_cor_{frente,direita,esquerda,costas}.png`.
- `jobs_teste/cor_t5/resultado_exp.json` e `resultado_exp2.json` (experimentos
  Blender Smart UV / unwrap, usados no item 7).
- `jobs_teste/cor_t1/orc/` (prévias e textura Smart UV, para o A/B).
- `app/testes/dourado/imagens/orc_{frente,costas,esquerda,direita}.png` (vistas canônicas).
- Saídas da auditoria (não commitadas, fora do repo `app/`):
  `jobs_teste/cor_t5/critico_t5/` — `critico_run.log`, `comparacao_npz.json`,
  `suite.log`, `suite_counts.json`, `probe_seam.json`, `probe_seam.log`,
  `uv2.npz`, `metricas2.json`, `pedido_probe.json`.
- Hashes conferidos por download: `textura.png` =
  `794ced3d13ad109c117dc631d61072c578fb08a776924088b6521e132f27bcbb` ✓
  (igual ao alegado); `modelo_cor.glb` =
  `7730405eb234af1cb0996d2cb0ff869fc3ab4462c67eb993409080d5bf8595de` ✓
  (igual ao alegado); `modelo_uv.glb` =
  `3c3a73dbbdf63bf3b086ae146d3d479899aaa3690cb62bdbfa80b2584f1abbd6`
  (novo, para registro); `modelo.glb` (refinado) =
  `88c30236272510603c74eb99fc7c5ecd90133c8f01494b3f011d80e310e12514`.

## 1. Métricas de UV do `modelo_uv.glb` — CONFIRMADAS exatamente

Decode próprio do GLB (JSON+BIN, sem Blender), réplica da fórmula de
`projecao.metricas_uv` (distorção por razão de áreas, ocupação por amostragem
de centro de texel, ilhas por aresta UV compartilhada):

| métrica | alegado (spike/Blender) | medido por mim (GLB) | medido por mim (npz puro) |
|---|---|---|---|
| distorção média | 0,08787 | **0,08787** | 0,08787 |
| ocupação @512 | 0,61398 | **0,61398** | 0,61398 |
| ilhas | 6.578 | **6.578** | 6.578 |
| margem mínima @512 | 1 px | **1 px** | 1 px |
| área UV total | 0,61378 | **0,61378** | 0,61378 |
| texels/face @1024 | 12,937 | **12,937** | — |
| faces com <1 texel | 0,33% | **0,33%** | — |
| triângulos | 49.750 | **49.750** | 49.750 |

Controle Smart UV medido pelo mesmo código: distorção 0,10051, ocupação
0,03983, 8.098 ilhas, área UV 0,04324, 0,911 texel/face, 61,68% com <1 texel —
todos idênticos aos alegados. O ganho da T5 é real e grande: ocupação
15,4×, texels/face 14,2×, faces sub-texel 61,68% → 0,33%, distorção menor.

**Nota de método (erro meu, registrado):** minha primeira rasterização (fill
de borda do PIL) inflou a ocupação para 0,797 @512 — artefato meu para
triângulos de ~3 texels, não divergência do executor. A réplica por
amostragem de centro reproduziu 0,61398 e 0,03983 **exatamente**, nos dois
casos. Não há divergência de ocupação; há lição de método para a próxima
bateria (não usar fill de borda para UVs de triângulos pequenos).

Os valores de pack/unwrap do Blender alegados como inferiores também batem
com os arquivos: `smart66_pack` ocupação 0,07831; unwrap conformal/angle
ocupação 0,17489/0,17675 com distorção 0,57613/0,48249 — todos piores que o
xatlas em ocupação e (unwrap) em distorção. Nada a corrigir aqui.

## 2. [NOVO] Identidade geométrica — PROVADA, sem ressalva

Comparação face a face, na ordem e como multiconjunto, entre `modelo.glb`
(refinado) e `modelo_uv.glb`:

- Faces: 49.750 = 49.750 = 49.750 (`modelo.glb` / `modelo_uv.glb` /
  `modelo_cor.glb`).
- Posições dos vértices de cada face (ordenadas dentro da face): **diferença
  máxima 0,0**; 0 faces com diferença >1e-4; mediana 0,0.
- Como multiconjunto (independente da ordem das faces): 49.750 chaves nas
  duas malhas, interseção 49.750 — nenhuma face alterada, nenhuma perdida,
  nenhuma criada.
- UV por face/loop: `modelo_uv.glb` **não** é igual ao `.npz` direto
  (diferença máxima 1,0 em todas as faces), mas é igual ao `.npz` com **flip
  de V** — `UV_glb = (u_npz, 1 − v_npz)` — com diferença máxima **2,98e-08**
  em todas as 49.750 faces. Ou seja: a ordem das faces e a correspondência
  por loop estão exatas; o exportador glTF do Blender inverteu o V, como é
  o padrão do formato. O bake confirma o round-trip: `modelo_cor.glb`
  também casa com o `.npz` sob flip V com diferença máxima 2,98e-08 e 0
  faces divergentes — a UV atravessou **dois** round-trips Blender sem
  embaralhar.
- **Consequência de contrato (S3, abaixo):** quem ler `modelo_uv.glb` fora
  do Blender verá a textura verticalmente invertida em relação ao `.npz`.
  Dentro do pipeline Blender isso se cancela (o importador inverte de
  volta); fora dele, é armadilha. A correspondência garantida é **por
  face/loop**, nunca por índice de vértice (ver S3 de contagem de vértices).

**Nenhum defeito S1 aqui. O item 2 passa integralmente.**

## 3. [NOVO] Margem em 2048 e risco de vazamento (bleed) — REPROVADO contra a régua

Medição própria (mesma família de método do `projecao`: varredura de
linhas/colunas da imagem de ids de ilha), a partir do GLB decodificado:

- Margem mínima: **1 px @512 e 1 px @2048** (não escala: o par de ilhas mais
  próximo praticamente se toca — folga UV da ordem de 0,0005 ou menos).
- Régua do estudo: **≥8 px em 2048**. Resultado: **1 px ≪ 8 px — falha por
  8×**. O Smart UV, para contraste, media 3–4 px @512 (≈6–8 px @1024) — mas
  isso é folga comprada com ilhas-minúsculas e 96% de espaço vazio; não é
  um padrão a invejar, e sim a prova de que margem isolada não mede
  qualidade.
- **O que isso implica para o bake em 1024:** a folga é de ~0–1 texel. Na
  rasterização do bake, ilhas vizinhas encostam; a dilatação de 256 passes
  preenche os texels cegos espalhando a cor dos vizinhos — e, através de
  uma folga de ~0 px, o "vizinho" é outra ilha. Ou seja: **a dilatação
  compensa visualmente no nível base, mas mascara o problema em vez de
  resolvê-lo** — ela produz, por construção, cor misturada nas costuras.
  Em nível base as prévias continuam utilizáveis (o vazamento fica
  confinado às linhas de costura); **sob mipmapping/minificação, os texels
  de costura passam a mediar entre ilhas diferentes** e o vazamento vira
  halo visível à distância. A textura atual não é segura para uso com
  mipmapping sem correção.
- **Classificação: S2** (grave para o T1-completo, não invalida o passo UV —
  ver o raciocínio no veredito). **Pendência obrigatória antes do
  T1-completo:** dar folga real ao xatlas (gutter/padding na parametrização
  ou margem explícita no bake) e re-medir ≥8 px @2048; não alegar
  conformidade de margem até lá.
- Nota de divergência menor (S3): o `resultado_cor.json` do bake registra
  margem 2 @512, contra 1 @512 do spike e desta auditoria. É diferença de
  método (o bake refina ilhas por arestas da malha), não de dado — e ambas
  as medidas estão ordens abaixo da régua quando postas na mesma escala.

## 4. [NOVO] Fidelidade pela TEXTURA (lição D10) — sem troca grosseira de região; D1 segue aberto

Amostragem da `textura.png` (1024) nos centroides UV das faces, por região
3D (altura normalizada + facing), contra as vistas canônicas:

| região 3D (faces) | n | mediana RGB amostrada | leitura |
|---|---|---|---|
| peito frente (alt 0,55–0,78, nz>0,5) | 3.332 | [104, 70, 50] | família quente, sem verde-dominante |
| peito estrito (alt 0,60–0,72, nz>0,7) | 1.103 | [119, 79, 53] | idem |
| pernas frente (alt 0,08–0,35, nz>0,3) | 5.156 | [107, 71, 48] | idem |
| costas (alt 0,55–0,85, nz<−0,5) | 4.670 | [98, 62, 42] | idem |
| ombros/capa (alt 0,78–0,92) | 4.535 | [119, 77, 53] | idem |

- **Correção de um teste meu (registrada, não escondida):** meu primeiro
  teste "verde" (G>R) deu zero tanto na textura quanto na arte canônica —
  o teste estava mal calibrado, não a textura. A pele do Orc na arte é
  oliva quente (R>G>B, matiz ~35–45°), não verde-saturada; blocos da vista
  canônica medem [107–152, 67–114, 41–91] — **a mesma família quente da
  textura**. Não há, portanto, evidência de troca grosseira de região
  (o peito não recebeu céu, fundo preto ou pele de lobo por engano).
- **O que a textura mostra de fato:** paleta global praticamente idêntica
  à do bake Smart UV (medianas [98, 62, 43] vs [96, 62, 42]; texels pretos
  25,44% vs 23,12%; brilho >180 em 11,17% vs 11,04%; vermelho saturado
  3,57% vs 3,31%) — o que mudou foi a **resolução**, não a paleta, como
  esperado do mesmo bake sobre outra UV. E a resolução aparece nos
  números: contraste médio entre faces vizinhas em 3D saltou de 2,3
  (Smart, borrado pela dilatação) para **28,9** (xatlas), com 27,2% dos
  pares vizinhos diferindo >40 (Smart: 2,3%). Cada face agora carrega cor
  própria — mas **própria não quer dizer legível**: o mosaico das prévias
  é exatamente esse contraste por face sem estrutura reconhecível
  (sem pele contínua, sem cicatriz legível, sem aço contínuo).
- **Conclusão do item 4:** a T5 entregou resolução por face; a fidelidade
  de detalhe **D1 continua aberta** (S2 herdado do T1), agora com o gargalo
  isolado onde o executor apontou: alinhamento por silhueta +
  divergência geometria-vs-arte, não mais a UV. Amostrar a textura (e não
  só a prévia sombreada) confirma o diagnóstico em vez de refutá-lo.

## 5. [NOVO] A/B de prévias xatlas vs Smart UV — alegações CONFIRMADAS, por região

Mesma câmera, mesma geometria (silhuetas diferem ≤0,3% entre os pares —
limiar de máscara/antialiasing, S4). Fração de pixels quase-pretos
(máx<40) dentro da silhueta, e diferença pixel a pixel (Smart − xatlas):

| vista | quase-preto xatlas | quase-preto Smart | leitura visual + número |
|---|---|---|---|
| frente | 27,75% | 33,03% | **Melhora.** A mancha branca do braço esquerdo (célula y 0,375–0,50, x 0,625–0,75: 1.265 px onde o Smart é >60 mais claro) **sumiu** no xatlas — virou mosaico marrom. A massa preta central do torso encolheu (ainda há manchas escuras na cabeça e no centro, menores). Torso segue mosaico. |
| costas | 22,66% | 20,85% | **Empate técnico, leve piora no preto.** O xatlas varia mais (menos massa escura vertical central), mas o preto total é um pouco maior — sombreamento Workbench, não massa plana. Pernas com pele mais legível no xatlas. |
| esquerda | 26,08% | 25,92% | **Empate.** Braço esquerdo Smart era uma massa preta sólida; no xatlas virou mosaico marrom estruturado. Machado com lâmina mais padronizada no xatlas. |
| direita | 31,13% | 37,51% | **Melhora clara.** A grande massa preta do torso Smart (e o ombro bege plano) sumiram; xatlas mostra mosaico variado, pele das ancas legível, manchas esverdeadas nas pernas e machado padronizado. |

- "Sem grandes áreas pretas": **confirmado no sentido de massas planas**
  (as massas pretas sólidas do Smart — torso da direita, braço da
  esquerda, centro das costas — desapareceram); **não confirmado** se lido
  como "sem preto": 22–31% dos pixels seguem quase-pretos (sombra
  Workbench + pelagem escura + costuras), número que o preto total
  sozinho não distingue. A alegação do executor está correta na forma
  como ele a escreveu (áreas, não pixels).
- "Sem a mancha branca no antebraço": **confirmado** (frente, célula
  acima; fração de bege-claro na silhueta da frente: 0,02% xatlas vs
  0,18% Smart).
- "Pernas/pele mais legíveis": **confirmado parcialmente** — pernas e
  pelagem das ancas/coxas ganham estrutura no xatlas nas 4 vistas, mas a
  legibilidade continua longe da arte (D1).
- "Torso continua manchado/mosaico": **confirmado nas 4 vistas**.

## 6. [NOVO] Determinismo do passo xatlas — PROVADO, exatamente

`gerar_uv` reexecutado **três vezes** no PC sobre o mesmo GLB (rodadas 1–3
da tarefa `CriticoT5`; a rodada 1 e 2 valem como repetição mesmo antes da
sonda, pois o passo 1 rodou integral nas três):

- Métricas idênticas nas três rodadas: distorção 0,08787, ocupação
  0,61398, 6.578 ilhas, margem 1, área 0,61378, 12,937 texels/face,
  0,33%, 49.750 triângulos, 58.552 vértices originais, 63.948 com costura
  (tempos 26,43 / 26,75 / 26,46 / 26,84 s — variação só de relógio).
- Comparação de arrays `.npz` (original vs reexecutado): `vmapping`
  iguais, `indices` iguais, `uvs` **iguais exatamente** — diferença
  máxima **0,0** (não só métricas iguais: os arrays são bit a bit
  idênticos). O xatlas, neste pipeline e nesta máquina, é determinístico.
- Escopo: isto prova o determinismo **do passo xatlas** (o que foi
  pedido). Não prova determinismo geral do app, do refino, nem do bake.

## 7. [NOVO] Anomalia do controle sem-costuras — EXPLICADA (artefato do experimento, não do Blender)

Fatos medidos pela sonda Blender (`probe_seam.py`, Blender 5.2.3 LTS,
13,19 s, `ok=True`):

- O GLB importado traz **0 costuras em 100.809 arestas** — o importador
  glTF **não cria flags de costura** (as divisões de UV vivem por loop,
  não como costuras).
- "Limpar costuras" passou de 0 para 0: **o braço-controle era vácuo**.
- Unwrap conformal **com** e **sem** limpeza, na mesma sonda: UVs
  **bit a bit idênticas** (diferença máxima 0,0), métricas idênticas
  (distorção 0,57613, ocupação 0,17489, 8.098 ilhas, margem 2) — as
  "métricas idênticas até a 5ª casa" não são coincidência de
  arredondamento: são o mesmo array, porque os dois braços rodaram o
  mesmo unwrap sem costuras.
- **Veredito do item 7:** artefato do desenho do experimento, não
  comportamento misterioso do Blender. O experimento **não pode**
  concluir nada sobre o efeito de costuras — e, importante, **isso não
  afeta a decisão T5**: a T5 não usa costuras nem unwrap do Blender; os
  números do unwrap continuam válidos apenas como "unwrap sem costuras
  performa mal (distorção 0,48–0,58)", rótulo corrigido.
- **Não-explicado (declarado explicitamente, sem inventar):** por que o
  unwrap-sem-costuras e o Smart UV dão **exatamente 8.098 ilhas** — a
  sonda provou que os dois braços do unwrap são o mesmo cálculo, mas não
  provou por que a contagem de ilhas coincide com a do Smart UV. Essa
  coincidência residual fica registrada como **não-explicada**; ela diz
  respeito apenas à métrica de ilhas dos experimentos de unwrap e não
  toca a T5, cuja contagem (6.578) foi verificada por dois caminhos
  independentes (medição no Blender + decode próprio, item 1).

## 8. Regressão — suite completa: 244 testes, 0 falhas

Rodada no `.venv_app` do PC (padrão do runner: chdir `app`, unittest
discover `testes`), três execuções (a última após a correção da sonda):

```
Ran 244 tests in 23.260s — OK (skipped=1)
SUITE_RESULT tests=244 failures=0 errors=0 skipped=1 ok=True
```

Contagem arquivo a arquivo (soma 244): `test_arquivar` 14, `test_cli` 11,
`test_config` 15, `test_cor` 22, `test_entrada` 13, `test_job` 36,
`test_mcp` 7, `test_motores` 29, `test_qualidades` 14, `test_refino` 30,
`test_saude` 15, `test_travas` 18, **`test_uv_xatlas` 4**,
`test_web` 7, `test_worker` 9. Esperado 240 + 4 = 244: **confere
exatamente**. Nenhum número aceito de memória — todos lidos do
`suite.log` da rodada.

## 9. Revisão do código novo — nenhum defeito que invalide os resultados

Lidos integralmente: `uv_xatlas.py` (94 linhas), `_blender_uv_xatlas.py`
(146 linhas), `test_uv_xatlas.py` (83 linhas, 4 testes).

- **Ordem das faces:** preservada e **provada empiricamente** (item 2:
  UV por face casa sob flip V com erro 3e-08). O teste do cubo amarra o
  contrato no lado `.venv` (cada face nova usa os vértices do triângulo
  original, ordenados). Nada a corrigir.
- **Flip de V:** real, mas do exportador glTF, não do código — e o
  pipeline Blender→Blender o cancela (item 2). Vira S3 de documentação
  de contrato (abaixo), não defeito de cálculo.
- **GLB multi-geometria:** o lado `.venv` falha alto (`ValueError` se
  ≠1 geometria — bom). O lado Blender, porém, junta malhas em silêncio
  (`join()`), e a ordem dos polígonos após o join pode não corresponder
  à ordem das geometrias do trimesh — a checagem de contagem de
  polígonos passaria e a UV sairia embaralhada entre geometrias. O GLB
  refinado atual tem 1 geometria, então **sem impacto nesta prova**;
  fica como S3 (limite de escopo a documentar, não correção urgente).
- **Falha silenciosa / guarda de ocupação — ACHADO (S2):** a docstring
  do script Blender afirma que "se [a métrica] não bater, a
  correspondência de ordem falhou e o resultado sai com `ok=False`".
  **Isso não existe no código do script:** `ok` é setado `True`
  incondicionalmente após a exportação; não há comparação de métricas
  no script. A guarda **existe de fato no runner** `run_t5.py` (compara
  a ocupação do Blender com a do xatlas e aborta se |dif| > 0,02) — e,
  nesta prova, |0,61398 − 0,61398| = 0, então ela corretamente não
  disparou. Mas: (a) a docstring do script promete uma proteção que o
  script não tem — quem rodar o script fora do `run_t5.py` exportará
  um GLB errado com `ok=True`; (b) a guarda compara **só ocupação**,
  que é invariante a flip de V e a permutações dentro da face — ela
  não provaria a ordem sozinha (esta auditoria é que a provou, por
  comparação por face). **Teste de disparo:** não foi possível
  "disparar" a guarda sem adulterar código ou dados (proibido nesta
  auditoria); o que se prova é que ela **existe no runner, não no
  script**, que **não disparou corretamente** (diferença zero), e que
  **não dispararia** por flip V ou permutação — limitação, não falha
  de disparo.
- **Teste do cubo:** adequado ao que promete (contrato do `.npz` em
  malha pequena); o Orc real é provado pelos runners, como o próprio
  teste declara. Sem defeito.
- **IoUs e tempo do bake (limite da auditoria):** os IoUs do
  `resultado_cor.json` (frente 0,7947, costas 0,7241, esquerda 0,793,
  direita 0,7872) e o tempo 23,87 s foram **conferidos no arquivo**,
  não reexecutados (o bake não foi rodado de novo nesta bateria) — mas
  passam em checagens de consistência: faces pintadas ≈ faces visíveis
  − poucos (8.778/8.789, 11.100/11.135, 8.397/8.426, 7.498/7.503);
  texels pintados direto 121.567 = 14,3× os 8.513 do Smart, igual à
  razão de texels/face (14,2×); 121.567/643.613 = 18,9% dos texels UV,
  proporção próxima aos 20,0% do Smart. Nada inconsistente; a
  re-execução do bake fica para a bateria do T1-completo, se pedida.

## Lista de defeitos e pendências

**S1 (reprova a T5): nenhum.**

**S2 (grave para o T1-completo / qualidade final, não para o passo UV):**

- **D-T5-1 — Margem 1 px @2048 contra a régua de ≥8 px (item 3).** A
  dilatação mascara o vazamento no nível base; sob mipmapping ele vira
  halo. Obrigatório corrigir (gutter/padding real) e re-medir antes de
  qualquer "T1-completo". Não invalida a T5 porque a alternativa
  (Smart UV) é pior em todas as métricas que importam para resolução,
  e a margem do Smart é folga comprada com vazio — rejeitar a T5 por
  margem seria voltar ao confete.
- **D-T5-2 — Guarda de ocupação ausente no script Blender (item 9).**
  Docstring promete `ok=False` em divergência; o script não compara
  nada. Mitigação real hoje: o runner `run_t5.py`. Correção pedida:
  mover a comparação para dentro do script (ou corrigir a docstring
  para dizer onde a guarda vive) e ampliar a guarda para além da
  ocupação (ela não detecta flip V nem permutação).
- **D1 (herdado do T1, confirmado nos itens 4–5) — Fidelidade de detalhe
  ausente.** Torso mosaico nas 4 vistas, contraste por face sem
  estrutura legível. Continua bloqueando qualquer "T1 pronto"; a T5
  isolou o gargalo (alinhamento por silhueta + divergência
  geometria-vs-arte), não o resolveu.

**S3:**

- **D-T5-3 — Flip V não documentado no contrato `.npz`↔GLB.** O GLB
  exportado tem `v_glb = 1 − v_npz` exato. Documentar: consumidor fora
  do Blender deve inverter V; correspondência garantida é por
  face/loop.
- **D-T5-4 — Contagem de vértices não preservada pelo Blender.**
  `.npz` 63.948 → `modelo_uv.glb` 64.044 (+96) → `modelo_cor.glb`
  64.093 (+49). Geometria e UV por face exatas; só a correspondência
  por vértice quebra. Documentar junto ao D-T5-3.
- **D-T5-5 — Multi-geometria silenciosa no lado Blender** (join sem
  checagem de ordem entre geometrias; lado `.venv` falha alto). Sem
  impacto no GLB atual (1 geometria). Documentar como limite.
- **D-T5-6 — Margem do bake (2 @512) vs spike (1 @512).** Divergência
  de método, não de dado; ambas ≪ régua. Unificar o método de medição
  nas próximas baterias para não gerar falso alarme.
- **D-T5-7 — Coincidência 8.098 ilhas (item 7): não-explicada.**
  Registrada como tal; não afeta a T5.

**S4:**

- Silhuetas das prévias xatlas/Smart diferem ≤0,3% apesar da geometria
  idêntica (limiar de máscara/antialiasing da renderização).
- `lightmap_pack` do experimento 1 falhou (resultado vazio) — fora do
  escopo da T5, só registro.
- Falhas das duas primeiras sondas do crítico (caminho `APP` errado no
  meu script — o script de experimento vive em `app/oficina3d/cor/`,
  não em `jobs_teste/cor_t5/`): erro do crítico, não do projeto; a
  terceira rodada, corrigida, é a que vale. Registrado para que
  ninguém confunda "sonda falhou" com "projeto falhou".

## Veredito

**APROVA a T5 como passo de UV** — com as pendências S2 listadas acima
(D-T5-1 margem, D-T5-2 guarda no script, D1 herdado).

O que esta bateria provou, por medição própria: a UV xatlas é a UV
alegada (ocupação 0,61398, distorção 0,08787, 6.578 ilhas, 12,94
texels/face, 0,33% sub-texel), a geometria está intacta face por face,
a correspondência por loop está exata (sob o flip V padrão do glTF), o
passo é bit a bit determinístico em três execuções, a suite está em
244 testes com 0 falhas, e as prévias melhoram onde o executor disse
que melhorariam (fim das massas pretas planas e da mancha branca) sem
melhorar onde ele disse que não melhorariam (torso mosaico).

O que esta bateria **não** aprova, explicitamente: D1 (fidelidade de
detalhe), o T1-completo, o determinismo geral do app, a conformidade
de margem com a régua do estudo (reprovada: 1 px @2048 vs ≥8 px), nem
a guarda de ocupação como proteção suficiente (ela vive no runner, não
no script, e só olha ocupação). A próxima etapa honesta é: corrigir
D-T5-1 e D-T5-2, e atacar D1 com o gargalo agora isolado — não declarar
o COR pronto.

## Bateria nova registrada (escalada APR-01 — o que esta bateria acrescentou à do T1)

1. Reprodução de métricas de UV por decode próprio do GLB (sem Blender).
2. Identidade geométrica por face (ordem + multiconjunto) — **nova**.
3. Margem mínima recalculada em 2048 contra a régua do estudo — **nova**.
4. Fidelidade amostrada na textura, não só na prévia sombreada (D10) — **nova**.
5. A/B de prévias com estatística de pixels e diferença pixel a pixel — **nova**.
6. Determinismo do passo xatlas por reexecução e comparação de arrays — **nova**.
7. Sonda Blender da anomalia do controle sem-costuras (contagem de
   costuras + comparação de UV bit a bit) — **nova**.
8. Regressão com contagem arquivo a arquivo (herdada do T1, mantida).
9. Auditoria da guarda de ocupação script-vs-runner e do contrato
   `.npz`↔GLB (flip V, contagem de vértices, multi-geometria) — **nova**.
