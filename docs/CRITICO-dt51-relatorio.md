# Relatório do Crítico Sênior — D-T5-1 (correção da margem da UV)

**Data:** 01/11/2026, ~07:40–08:00 (Horário de Brasília).
**Objeto julgado, somente este:** a correção D-T5-1, commit `038e60d`
(`D-T5-1: gutter real na UV xatlas (padding 8 em 2048) + testes + docs`),
no repo público `arthof09-ai/oficina3d`, pasta `app/` no PC (PCDANASA).
**Não julgado aqui:** o T1-completo, a fidelidade de detalhe D1
(segue aberta, herdada do T1), nem o portão final MET-03.
**Veredito: APROVA a D-T5-1 como correção** (ver seção 10).
O crítico não executou o trabalho julgado; todas as medições abaixo são
próprias, feitas a partir dos artefatos e do código, sem aceitar nenhuma
alegação do executor sem verificação.

## 0. Documentos lidos antes de medir (REG-01)

- `app/docs/ESTADO_ATUAL.md` (01/11 ~07:34), entrada D-T5-1 em
  `app/docs/REGISTRO.md`, `app/docs/CRITICO-t5-relatorio.md` (definição
  da D-T5-1: margem 1 px em 2048 contra a régua de ≥ 8 px, pendência S2
  obrigatória antes do T1-completo) e `app/docs/APRENDIZADO_E_FLUXO.md`
  (checklist pré-Crítico, seção 3, e regra de escalada, seção 5).
- Código novo lido integralmente: `oficina3d/uv_xatlas.py` (diff do
  commit conferido: só ele, os testes e os docs mudaram) e
  `testes/test_uv_xatlas.py` (classe nova `TestUvMargemD_T5_1`).
- Pré-condições verificadas: `git status` limpo, `HEAD == origin/main
  == 038e60d8a973c5f942cb2550558499238c628aba`. Nada do projeto foi
  alterado por esta auditoria: todo o trabalho vive em
  `jobs_teste/critico_dt51/` (fora do git), exceto este relatório.

## 1. Bateria reproduzida da T5 (o que for aplicável)

1. **Métricas da UV por decode próprio** (trimesh + `oficina3d.cor.projecao`,
   sem Blender): ocupação, distorção, ilhas, texels/face, margem.
2. **Identidade geométrica por face** (multiconjunto de faces + ordem).
3. **Determinismo do passo novo** (re-execução de `gerar_uv` + comparação
   bit a bit com o `.npz` da prova).
4. **Suite completa com contagem conferida arquivo a arquivo.**
5. **Conferência dos SHAs alegados** (recalculados a partir dos arquivos).
6. **Leitura dos números alegados contra os arquivos de resultado**
   (`resultado_prova.json`, `det_resultado.json`, `resultado_exp.json`,
   `resultado_exp2.json`, `resultado_cmp.json`, `resultado_cor.json`).
7. **Revisão do código novo** (diff + leitura integral).

## 2. Escalada APR-01 — verificações novas desta bateria

A bateria da T5 não tinha nenhuma destas; todas foram executadas e os
resultados estão nas seções 5–8:

1. **(c) Margem euclidiana própria, em 2048** — distância mínima entre
   pixels de borda de ilhas diferentes por KD-Tree, com prova de
   otimalidade (nenhum par mais próximo existe). O método do executor
   (`_margem_ilhas`) só varre linhas e colunas e admite não medir
   aproximações puramente diagonais; esta verificação fecha essa brecha
   para esta UV.
2. **(b) Distribuição de distorção LOCAL** (p50/p95/p99/máximo e frações
   de cauda, por face) — a média pode esconder estiramento local após o
   encolhimento das ilhas.
3. **(a) Halo sob mipmapping por blocos mistos** — contagem de blocos
   2×2 e 4×4 alinhados (mips 512 e 256) que contêm texels de duas ou
   mais ilhas diferentes: o teste direto da razão da D-T5-1. (Uma
   simulação ampla de mip, feita antes, mostrou-se dominada pelo borrão
   do mosaico por face e foi descartada como medida de halo — ver
   seção 7.)
4. **(d) Análise da queda de faces pintadas** — quais faces perderam
   TODA a cobertura de texel (não só quantas), com a regra exata do
   bake (faces com determinante UV < 1e-12 são puladas).
5. **UV do GLB por arquivo e por orientação** — `modelo_uv.glb` vs
   `modelo_cor.glb`, com e sem flip V, no UV novo e no da T5 (estende o
   item 2 da T5, que mediu o flip num único caminho).

## 3. Alegações do executor vs. medição própria

| Alegação | Medição própria | Resultado |
|---|---|---|
| `parametrizar()` usa API Atlas, padding 8 em 2048 como padrão; guarda `atlas_count==1`; `gerar_uv` registra padding/resolução/max_cost | Diff do commit + leitura integral + re-execução com os padrões: métricas devolvem `padding_px=8, resolucao=2048, max_cost=2.0`; nenhum outro chamador de `parametrizar`/`gerar_uv` existe no código (só o próprio módulo e os testes) | **CONFIRMADO** |
| Orc Prata: margem 9 px em 2048 no `.npz` e no GLB; ocupação 0,233; 4,92 texels/face em 1024; distorção 0,0745; 6.578 ilhas | Método do executor reproduzido: margem 2@512, 4@1024, **9@2048**; ocupação 0,23287@512, 0,23332@1024; distorção 0,07446; 6.578 ilhas; 4,92 texels/face; 2,49% das faces com < 1 texel | **CONFIRMADO** |
| Bake COR com IoUs idênticos aos da T5 (0,7947 / 0,7241 / 0,793 / 0,7872), mesmas faces visíveis; faces pintadas 8.723/10.916/8.299/7.424; texels diretos 46.343; 0 sem cor após dilatação | Conferido em `resultado_prova.json` e `resultado_cor.json`: IoUs e faces visíveis (8.789/11.135/8.426/7.503) idênticos aos da T5; texels UV 244.649, diretos 46.343, cegos 81,06%, 0 sem cor. **O bake não foi re-executado** (ver Limites) | **CONFERIDO EM ARQUIVO** (não re-executado) |
| Determinismo ponta a ponta: 3 SHAs idênticos; `.npz` bit a bit idêntico em 2 runs | SHAs recalculados: textura `5660c824…`, modelo_cor `9aa12f8e…`, modelo_uv `64782391…` **batem** em `prova/` e em `prova_det/`; `uv_a.npz` vs `uv_b.npz`: vmapping e índices iguais, UVs com maxdiff 0,0; **minha re-execução** de `gerar_uv` é bit a bit idêntica a `uv_a.npz` (vm/idx iguais, maxdiff 0,0) | **PROVADO** (re-execução própria do passo xatlas; determinismo do bake verificado por SHA, não por re-execução do Blender) |
| Suite 247 OK, skipped=1 (240 + 4 + 3) | Rodada própria no `.venv_app`: `Ran 247 tests in 33.359s — OK (skipped=1)`; soma das contagens `def test_` por arquivo = 247; `test_uv_xatlas.py` = 7 (4 + 3) | **CONFIRMADO** |
| Custo admitido: ocupação 0,614 → 0,233; max_cost 8 daria +15% (5,65 texels/face, 4.575 ilhas) e NÃO foi adotado | `resultado_exp2.json` conferido: max_cost 8 = 4.575 ilhas, ocupação 0,26828, 5,653 texels/face, distorção 0,07419 → 5,653/4,92 = **+14,9%**; a não-adoção é coerente (ver seção 9) | **CONFIRMADO** |

Detalhe de bookkeeping (S4, sem efeito nos números): o
`resultado_cor.json` dentro de `prova/` é o arquivo da rodada `det`
(caminhos `previas_det`, `sha256_glb = cb0dc675…`), não o da rodada
`prova`. O `cb0dc675…` é o `modelo_cor_det.glb` (+4 bytes pelo nome da
imagem embutida, lição L-21) — não é divergência: os três SHAs alegados
foram recalculados e batem nos arquivos com os nomes da rodada `prova`
e nos da rodada `det`. Os números do bake da rodada `prova` estão
preservados em `resultado_prova.json`.

## 4. Determinismo e SHAs — provado

- `gerar_uv` re-executado pelo crítico sobre o GLB refinado original
  (`jobs/20261031-225432-provac-orc-s7/saida/modelo.glb`, 49.750
  triângulos): métricas idênticas às alegadas (distorção 0,07446,
  ocupação 0,23287, 6.578 ilhas, 4,92 texels/face, 58.552 vértices
  originais, 63.948 com costura, tempo 27,53 s — relógio, não comparado)
  e arrays **bit a bit idênticos** aos de `uv_a.npz`.
- UVs em [0, 0,99987]; bbox [0, 0,9999] × [0, 0,9999].
- O determinismo do **bake** (Blender + bake) não foi re-executado; foi
  verificado por recomputação de SHA nos dois conjuntos de artefatos
  (`prova/` e `prova_det/`), que batem com os três SHAs alegados.

## 5. Margem — PROVADA por dois métodos (escalada c)

**Método do executor** (varredura linha/coluna, reproduzido):
margem 2@512, 4@1024, **9@2048** — régua (≥ 8 px em 2048) cumprida.

**Método próprio euclidiano** (rasterização baricêntrica centro-do-texel
em 2048, ilhas por aresta UV compartilhada, pixels de borda por
vizinhança-4, KD-Tree sobre ~pixels de borda):

- Menor distância centro-a-centro entre pixels de borda de ilhas
  diferentes: **10,0 px**, par (x=1540, y=14, ilha 4198) ↔ (x=1540,
  y=24, ilha 6354) — alinhado em coluna, ou seja, **9 texels vazios**
  entre as ilhas, exatamente o número do executor.
- Prova de otimalidade: busca por raio < 10,0 px em todos os pixels de
  borda encontrou **0 violações** — nenhum par mais próximo existe, em
  nenhuma direção, diagonal incluída. A limitação conhecida do método
  linha/coluna **não afeta este resultado**: a margem verdadeira é 9,
  não um artefato da varredura.
- Ocupação do meu raster em 2048: 0,23332 — idêntica à do executor.

**GLB:** o executor mediu 9 px no `modelo_cor.glb`. Esta auditoria
provou (seção 8) que a UV do `modelo_cor.glb` é **exatamente** a UV do
`.npz` (maxdiff 2,98e-08, só quantização float32); logo, a margem do
GLB é a margem do `.npz`: 9 px. Transferência exata, não analogia.

## 6. Distorção local — NENHUM estiramento escondido (escalada b)

Razão por face `(auv/Σauv)/(a3d/Σa3d)`, desvio `|razão − 1|`:

| Estatística | UV nova (D-T5-1) | UV T5 | Leitura |
|---|---|---|---|
| Média ponderada por área 3D | 0,07446 | 0,08787 | Melhora |
| p50 do desvio | 0,0430 | 0,0555 | Melhora |
| p95 do desvio | 0,2750 | 0,3587 | Melhora |
| p99 do desvio | 0,5413 | 0,6272 | Melhora |
| Desvio máximo | 5,013 | 12,643 | Melhora forte |
| Razão máxima / mínima | 6,013 / 0,0 | 13,643 / 0,0 | Melhora |
| Faces com razão > 2 | 0,070% | 0,147% | Metade |
| Faces com razão < 0,5 | 0,581% | 0,605% | Igual |
| Faces com razão > 3 | 0,012% | 0,016% | Igual |
| Faces com razão < 1/3 | 0,161% | 0,171% | Igual |

**Conclusão:** o encolhimento das ilhas **melhorou** a distribuição de
distorção em todos os percentis, não a piorou. A cautela do executor
em não adotar o max_cost 8 ("risco não medido de distorção local") era
honesta, mas a solução adotada não precisa dela: a cauda de distorção
já encolheu sem mudar o charting. Razão mínima 0,0 nos dois casos =
faces degeneradas em UV (5 faces com determinante UV < 1e-12, mesmo
número na T5 e na nova — pré-existente, sem efeito; ver S4).

## 7. Halo sob mipmapping — PROVADO pelo teste direto (escalada a)

**Teste dos blocos mistos** (raster de ids de ilha em 1024 + textura do
bake; bloco alinhado é exatamente o que o filtro box do mip calcula):

| | Blocos 2×2 (mip 512) | Blocos 4×4 (mip 256) |
|---|---|---|
| **UV nova** | **0 blocos mistos, 0 texels** | **0 blocos mistos, 0 texels** |
| UV T5 | 40 blocos mistos, 124 texels (desvio médio 10,23; 11,3% > 30) | 5.680 blocos mistos, 32.292 texels (desvio médio 18,47; 22,8% > 30) |

A UV nova **elimina** a mistura entre ilhas nos mips 512 e 256, onde a
T5 misturava 32 mil texels no mip 256. É a demonstração direta da razão
da D-T5-1 — e é mais forte que a régua geométrica sozinha, porque mede
contaminação de cor, não só distância.

**Simulação ampla descartada (lição de método, não defeito):** uma
primeira simulação (reduzir a textura para 512/256/128 e medir o
desvio por texel, dentro e fora da borda) deu números piores para a UV
nova no interior das ilhas (ex.: mip 512, interior 13,71 vs 12,33 na
T5). Isso não é halo: é o borrão do mosaico por face — cada face tem
cor própria, e qualquer redução borra o mosaico, tanto mais quanto
menor a densidade (4,92 vs 12,94 texels/face). O teste dos blocos
mistos isola a contaminação estrangeira e é o que vale para o halo.
O "detalhe fino mais macio" já admitido pelo executor é o mesmo preço,
visto por outro ângulo — não um defeito novo.

**Limite:** simulação com filtro box alinhado, não renderização em GPU
real. O que ela prova é a ausência geométrica de mistura nos dois
primeiros níveis de mip; um teste em GPU fica para o T1-completo, se
pedido.

## 8. Faces que perderam tinta + UV do GLB (escaladas d, e)

### 8.1 Faces sem nenhum texel (escalada d)

Cobertura por centro-de-texel em 1024, com a regra exata do bake
(determinante UV < 1e-12 pula a face; 5 faces puladas, igual na T5 e na
nova — o resultado é idêntico com ou sem a regra):

| | UV nova | UV T5 |
|---|---|---|
| Faces com ≥ 1 texel | 48.879 | 49.622 |
| **Perderam TODA a tinta** (tinham na T5, zero na nova) | **771** | — |
| Ganharam tinta | 28 | — |
| Sem texel em ambas | 100 | — |
| Área 3D das 771 perdidas | 0,0118 de 3,8648 (**0,31%**) | — |
| Faces com exatamente 1 texel | **3.468** | 319 |
| Mediana de texels/face | 5,0 | — |

**Leitura:** a queda de faces pintadas por vista alegada
(8.778→8.723, 11.100→10.916, 8.397→8.299, 7.498→7.424; 411 incidências
vista-face) é **consistente** com as 771 faces que perderam todo texel
no nível UV (uma face perdida conta numa vista só se for visível
nela; 411 ≤ 771, e o resto são faces não visíveis ou abaixo do limiar
de facing). Não há face grande perdida: as 771 somam 0,31% da área 3D
— são as faces miúdas do mosaico. E a dilatação as cobre (0 texels sem
cor após a dilatação, conferido): elas renderizam com cor emprestada
do vizinho, não com buraco. O preço real, a vigiar, é a fragilidade:
**3.468 faces penduradas num único centro de texel** (era 319) — qualquer
futura queda de densidade vira essas faces. Registrado como S3 (não
bloqueia a D-T5-1; vigiar no T1-completo).

### 8.2 UV do GLB vs `.npz` — exata, e o flip tem um detalhe (escalada e)

| Arquivo | Sem flip (maxdiff) | Com flip V (maxdiff) |
|---|---|---|
| novo `modelo_cor.glb` | **2,98e-08** | 1,0 |
| T5 `modelo_cor.glb` | **2,98e-08** | 1,0 |
| novo `modelo_uv.glb` | não legível pelo trimesh (ColorVisuals, sem textura) | idem |
| T5 `modelo_uv.glb` | idem | idem |

Ordem das faces preservada no GLB (verificação face a face, não só
multiconjunto). Geometria: multiconjunto de faces **idêntico** ao GLB
refinado original (49.750 faces; 58.552 → 64.093 vértices pelo Blender,
como na T5).

**Interpretação correta (corrige a primeira leitura desta auditoria):**
a primeira comparação do crítico aplicou o flip ao `modelo_cor.glb` e
deu maxdiff 1,0 — erro de método do crítico, não do projeto. O
`modelo_cor.glb` passou por **dois** round-trips glTF
(`.npz`→`modelo_uv`→`modelo_cor` via bake); cada round-trip inverte V,
dois cancelam. Logo, a UV do `modelo_cor.glb` **é** a UV do `.npz`, sem
flip — provado igual na T5 e na nova. O `modelo_uv.glb` não é legível
pelo trimesh (limitação conhecida, já registrada na T5: sem textura,
vira ColorVisuals); a orientação dele não foi re-provada aqui. A nota
de flip no docstring de `uv_xatlas.py` está correta por round-trip,
mas incompleta: falta dizer que o caminho do bake cancela o flip no
`modelo_cor.glb`. Vira S3 de documentação (seção 10); o bake não é
afetado, porque dentro do Blender a correspondência é por face/loop.

## 9. Julgamento do preço: a ocupação 0,233 é aceitável?

**Sim, com números, não com opinião:**

1. **A régua era a margem, e ela foi cumprida com folga medida por
   dois métodos** (9 px euclidianos, não só linha/coluna).
2. **O benefício é real e medido:** zero mistura entre ilhas nos mips
   512 e 256, contra 32.292 texels misturados na T5 no mip 256.
3. **A densidade restante ainda é 5,4× o Smart UV** (4,92 vs 0,91
   texels/face) e a distorção **melhorou** em todos os percentis.
4. **A alternativa medida (max_cost 8) só recuperaria +14,9%** de
   densidade (0,233 → 0,268) ao custo de trocar o charting provado na
   T5 — troca desproporcional para um ganho que não muda nenhuma
   decisão (a margem já está cumprida, a distorção local já melhorou).
   Fica registrada como otimização futura com números, não como
   pendência.
5. **O custo é vigiável, não escondido:** 771 faces sem texel direto
   (0,31% da área, cobertas pela dilatação) e 3.468 faces de 1 texel
   (S3 de vigilância, não bloqueio).

A correção deveria ser outra? Não. Padding maior (12/16) piora a
densidade (0,161/0,117) sem necessidade; max_cost 8 troca charting
provado por +15%; qualquer outra rota (ex.: repacking manual) seria
trabalho novo sem régua que a justifique. **O gutter de 8 px em 2048
é a correção certa, no tamanho certo.**

## 10. Lista de defeitos e pendências

**S1 (reprova a D-T5-1): nenhum.**

**S2 (grave para o T1-completo): nenhum introduzido pela D-T5-1.**
(D1, herdado do T1, segue aberto e fora do escopo deste veredito, como
determinado. D-T5-2 já estava fechada antes desta tranche.)

**S3 (ressalvas, nenhuma bloqueia o T1-completo):**

- **D-T5-1-DOC — Nota de flip incompleta no docstring de
  `uv_xatlas.py`.** A nota diz que o round-trip glTF inverte V
  (`v_glb = 1 − v_npz`). Isso vale por round-trip, mas o
  `modelo_cor.glb` entregue passa por dois round-trips e casa com o
  `.npz` **sem** flip (maxdiff 2,98e-08, provado na T5 e na nova).
  Quem ler o `modelo_cor.glb` fora do Blender e aplicar o flip vai
  inverter a textura inteira. Correção pedida (documentação, sem
  urgência): explicitar que o flip se cancela no caminho do bake e
  que a correspondência garantida continua sendo por face/loop. Não
  afeta o bake nem a D-T5-1.
- **D-T5-1-FRAG — 3.468 faces com exatamente 1 texel** (era 319) e 771
  faces sem texel direto (0,31% da área, cobertas pela dilatação).
  Vigilância para o T1-completo: se a densidade cair de novo, essas
  faces viram as primeiras a trocar de cor. Não é defeito da correção
  (é o preço medido dela), mas o T1-completo não deve aceitar nova
  queda de densidade sem re-medir este número.
- **D-T5-1-MET — Limitação do método de margem do código.**
  `_margem_ilhas` (linha/coluna) continua sem medir aproximações
  puramente diagonais — limitação já documentada no próprio código.
  Para esta UV, a verificação euclidiana desta bateria fechou a brecha
  (mínimo verdadeiro = 9 px). Baterias futuras de UV devem incluir a
  verificação euclidiana como padrão, em vez de confiar só na varredura.

**S4:**

- `resultado_cor.json` em `prova/` é o arquivo da rodada `det`
  (caminhos `previas_det`, SHA do `modelo_cor_det.glb`) — bookkeeping,
  sem efeito nos números (todos conferidos nos arquivos certos).
- 5 faces degeneradas (determinante UV < 1e-12) e razão mínima 0,0 —
  pré-existentes, idênticas na T5 e na nova, sem efeito.
- Simulação ampla de mip é dominada pelo borrão do mosaico e não
  serve como medida de halo; o teste dos blocos mistos é o que vale
  (lição de método desta bateria).

## 11. Veredito

**APROVA a D-T5-1 como correção.**

O que esta bateria provou, por medição própria: a margem cumpre a régua
por dois métodos independentes (9 px em 2048, euclidiano com prova de
otimalidade); o passo novo é bit a bit determinístico e reproduzido
pelo crítico; a geometria está intacta face por face; a UV do GLB
entregue é exatamente a UV do `.npz`; a distorção local melhorou em
todos os percentis; o halo entre ilhas foi eliminado nos mips 512 e
256 (zero blocos mistos, contra 5.680 na T5 no mip 256); a suite está
em 247 testes com 0 falhas; o preço (ocupação 0,233, 771 faces sem
texel direto, 3.468 faces de 1 texel) foi medido, é aceitável e fica
registrado como vigilância, não como bloqueio.

O que esta bateria **não** aprova, explicitamente: D1 (fidelidade de
detalhe), o T1-completo, o portão final MET-03, nem o bake por
re-execução (IoUs e SHAs do bake conferidos em arquivo e por
recomputação de SHA, com o mecanismo da queda de faces pintadas
reproduzido independentemente — a re-execução do bake em Blender fica
para a bateria do T1-completo, se pedida). A D-T5-1 está **FECHADA**;
o próximo passo obrigatório antes do T1-completo continua sendo o
adversarial D2 (e a costura D7 com a UV nova), na ordem já aceita.

## 12. Bateria nova registrada (escalada APR-01)

1. Margem euclidiana por KD-Tree com prova de otimalidade — **nova**.
2. Distribuição de distorção local (p95/p99/máximo, caudas) — **nova**.
3. Halo por blocos mip mistos (2×2 e 4×4) — **nova**.
4. Faces que perdem todo texel, com a regra exata do bake — **nova**.
5. UV do GLB por arquivo (`modelo_uv` vs `modelo_cor`) e por
   orientação (com/sem flip), novo vs T5 — **nova**.
6. Reprodução da T5 mantida: métricas por decode próprio, identidade
   geométrica por face, determinismo por re-execução, suite com
   contagem arquivo a arquivo, SHAs recalculados, números lidos dos
   arquivos de resultado.

## 13. Arquivos desta auditoria (PC, fora do git)

- `jobs_teste/critico_dt51/run.py`, `run2.py`, `run3.py` — scripts da
  bateria (reprodutíveis).
- `jobs_teste/critico_dt51/resultado.json`, `resultado2.json`,
  `status.txt`, `status2.txt`, `status3.txt`, `suite.log`, `uv_re.npz`
  — resultados brutos (a re-execução `uv_re.npz` é bit a bit idêntica
  a `prova/uv_a.npz`).
- Este relatório: `app/docs/CRITICO-dt51-relatorio.md`.

## 14. Lição do crítico (erro meu, registrado para não se repetir)

A primeira comparação UV-GLB desta auditoria aplicou o flip V ao
`modelo_cor.glb` e devolveu maxdiff 1,0 — parecia "GLB errado". Era o
arquivo errado para aquele flip: o `modelo_cor.glb` já é o segundo
round-trip. A correção foi medir os dois arquivos, com e sem flip, no
novo e na T5 — e o resultado (2,98e-08 sem flip, nos dois) é mais
forte que a medição original. Regra que fica: **comparação de UV de
GLB sempre declara o arquivo e a orientação antes de concluir**.
