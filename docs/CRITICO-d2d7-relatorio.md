# Relatório do Crítico sênior — D2 (adversarial) + D7 (costura), Etapa COR

## ADENDO — verificação contra o repo público (pós-correção do briefing)

O Crítico clonou (só leitura, sem SSH no PC, sem commit) o repo público
`arthof09-ai/oficina3d`: HEAD = `17462aa` exato ("D2/D7: medicao de
costura + 5 testes"). Confrontação:

- `oficina3d/cor/costura.py` do repo é BYTE-IDÊNTICO à cópia do staging;
  idem `testes/test_cor_costura.py`. A limitação registrada no relatório
  original ("não julguei o código de verdade") ESTÁ RETIRADA: o julgamento
  foi sobre o código real. Vereditos inalterados.
- `costura.py` real confirma: `classificar_arestas` chaveia arestas por
  IDs de vértice, sem nenhuma solda por posição (nenhum `weld`/`sold`/
  `unique` no módulo) — S2-1 confirmado no código, não só no comportamento.
  O teste real confirma: nenhum caso de vértice duplicado — é por isso que
  o bug passou na suite.
- `oficina3d/cor/projecao.py`, `direcao_camera`: docstring explícita —
  "Vetor unitario do centro do modelo ate a camera (coords Blender,
  Z-up)". `costas` = (0,1,0) Blender. Pela convenção do próprio módulo
  ("GLB: Y para cima, frente em +Z. No Blender: frente em -Y"), a
  conversão Blender→glTF é (x,y,z)→(x,z,−y): costas em frame glTF é
  DEFINITIVAMENTE **−Z** (não +X). Números corrigidos definitivos do D2
  sem-costas: limiar 0,5, alvo 28,23 / 24,01% > 30 vs controle 7,05 /
  5,86%; limiar 0,9, alvo 18,96 / 18,03% vs controle 8,41 / 7,07%.
- Bake NÃO afetado pelo bug de frame: `_blender_cor.py` usa
  `P.direcao_camera` com normais/vértices em frame Blender, dentro do
  Blender (facing + `BVH.ray_cast` com `dcam`) — correto no contexto do
  bake. O bug vive só no `run_prova.py`, que aplicou o vetor Blender
  cru às normais glTF. S3-4 RESOLVIDO favoravelmente: D2 fecha SEM novo
  bake.
- Margem 2 vs 11 RESOLVIDA como definicional: `gerar_uv` mede
  `P.metricas_uv` em **512 px** (margem 2); `margem_2048` do `run_prova`
  mede a mesma função em **2048 px** (margem 11). Resoluções diferentes,
  mesma métrica — não é contradição. Resta de S3-3 só a ausência dos
  hashes do GLB de entrada e do `uv.npz` (mitigada pela reprodução exata).

Vereditos finais inalterados: D7 REPROVA, D2 REPROVA (como publicados),
ambos fecháveis sem novo bake, nos termos da seção "Vereditos" abaixo.

---

# Relatório do Crítico sênior — D2 (adversarial) + D7 (costura), Etapa COR

Tranche D2/D7, Besta Cristalina, UV D-T5-1, commit 17462aa (informado pelo executor).
Método do Crítico: reimplementação própria em Python/numpy a partir dos artefatos
entregues, sem importar `costura.py` para as medições críticas. NÃO toquei no PC,
não fiz commit, não alterei git.

Nota de escopo corrigida: ao contrário da premissa da tarefa, as cópias de
`costura.py` e `testes/test_cor_costura.py` ESTAVAM no staging
(`hidden_files/d2d7/`), e eu as li e rodei sinteticamente. Isso não muda a
independência das medições (feitas com código próprio); só amplia o item 1.

## Artefatos conferidos (SHA-256)

- `textura_base.png` = `842b461d…c003dd01` ✓ igual ao `resultado_prova.json`
- `textura_adv512.png` = `0f0d520a…a446fc4` ✓ igual ao JSON
- `textura_adv3v.png` = `fd856d16…6ecf2` ✓ igual ao JSON
- `uv.npz`: `e8b76f32…f419` — SEM entrada no JSON para conferir (ver S3-3).
  Triangulação: minha reimplementação reproduziu EXATAMENTE os números do
  executor em D7 sem solda e em D2-res512 (ver abaixo); uma UV diferente não
  reproduziria ~10 estatísticas a 2 casas. A cópia é, para fins práticos, a
  mesma — mas o hash deveria estar no resultado.
- `besta_refinado.glb`: `ba8d6cd5…8621` — também SEM entrada no JSON (o JSON
  traz só `modelo_uv`, `bb180df6…`, que é outro arquivo, não entregue).
  Mesma triangulação vale: 49.750 faces, 47.476 vértices, idênticos às
  métricas do `gerar_uv`. O GLB de entrada deveria ter hash no resultado.
- Prévias base: 4 PNG 640×800 existem (`previa_cor_{frente,costas,esquerda,
  direita}.png`). São renders Workbench sombreados (D10): NÃO provam cor e
  não foram usados como prova de cor neste relatório.

## Bateria, item a item, com números próprios

### 1. Suite

- Os 5 testes novos entregues rodam e passam no meu interpretador
  (Python 3.12.3, cópias do staging, pacote montado em /tmp): 5/5 OK.
- A suite completa (252 OK, skipped=1, afirmada pelo executor) NÃO é
  re-verificável: nenhum `suite.log`, nenhum outro arquivo de teste foi
  entregue. Registro como LIMITE DECLARADO, não como fato conferido (S3-1).

### 2. Classificação costura/interna — reimplementação independente

Sem solda (código próprio, mesma regra de IDs): costura 4.017, interna
51.880, borda 37.456, não-manifold 0, classificadas 55.897 — REPRODUÇÃO
EXATA dos números do executor, a unidade. O código de classificação, dado
IDs compartilhados, está aritmeticamente certo.

Com solda por posição (tolerância 1e-6, arredondamento a 6 casas):
47.476 vértices → 24.805 únicos (colapso de 22.671 duplicados, exatamente o
esperado por Euler para 49.750 triângulos: V ≈ F/2 + 2 ≈ 24.877).
Resultado: costura 13.758, interna 60.867, borda 0, não-manifold 0,
classificadas 74.625 (= 3×49.750/2, malha fechada exata).

Conclusão do item 2: a medição do executor SUBCONTA as costuras em 3,4×
(4.017 de 13.758 reais; faltam 9.741) e inventa 37.456 "bordas" numa malha
fechada. As 4.017 arestas do executor são um SUBCONJUNTO das 13.758 reais
(interseção = 4.017), idem para as internas. Divergência de 242% no n de
costura — muito acima do limite de 0,1% da bateria. A MEDIÇÃO ESTÁ
REPROVADA (S2-1). Causa raiz: o GLB exportado duplica vértices (split por
normal/UV) e `classificar_arestas` assume que "aresta 3D compartilhada" =
mesmos IDs. Os testes não cobrem o caso de vértice duplicado — é por isso
que o bug passou na suite.

### 3. Proxy de cor (mediana de 4 amostras) × média rasterizada

Amostra aleatória de 1.200 faces (seed 42), textura base 1024:
1.197 rasterizáveis; texels/face mediana 7, média 7,6.
|proxy − raster| por face: média 14,68, mediana 6,65, p90 41,11,
16,62% > 30, 4,85% > 60. Correlação por canal 0,961–0,966.

Veredito: o proxy é ACEITÁVEL para conclusões distribucionais (medianas,
p90, frações), mas ruidoso por face (1 em cada 6 faces difere > 30 entre
os métodos) — e o erro NÃO some em faces grandes (texels 8–20: mediana
8,70, pior que faces de 1–4 texels: 1,22), porque a textura da Besta é de
alta frequência. Prova decisiva: re-medindo saltos com cores rasterizadas
(amostra de 400 arestas de costura + 400 internas, solda aplicada):
costura raster média 90,13, mediana 78,61, p90 183,90, 79,3% > 30;
interna raster média 25,59, mediana 14,25, p90 65,65, 29,3% > 30.
O gap costura × interna SOBREVIVE ao método independente. O proxy infla
as médias (costura +11,5%, interna +38% na amostra), mas não fabrica o
gap. Uso proibido: afirmar salto de UMA aresta isolada pelo proxy.

### 4. Costura (D7) — com a medição corrigida (solda)

Base, soldada: costura n=13.758, média 93,49, mediana 77,22, p90 199,86,
78,08% > 30, 59,90% > 60, máx 337,17; interna n=60.867, média 36,20,
mediana 13,96, p90 107,19, 36,61% > 30, 21,87% > 60.
Adv3v, soldada: costura média 96,42, mediana 79,45, 79,26% > 30;
interna média 33,65, mediana 11,02, 34,12% > 30. O gap persiste no adv3v.

Piores 20 costuras (soldadas): saltos 325,7–337,2; áreas UV medianas
5,07e-06 vs mediana geral 6,69e-06 — NÃO são ruído de faces miúdas.
Localização: 56,5% das costuras soldadas unem faces de eixo dominante
diferente, contra 18,3% das internas — as piores costuras CONCENTRAM-SE
nas transições de eixo (junções de vistas), mas NÃO só lá: 9 das 20
piores unem faces do MESMO eixo dominante (ex.: Z−/Z−, Y−/Y−, Y+/Y+).
Ou seja: salto visível SISTEMÁTICO nas costuras, com componente de
junção de vistas e componente intra-vista (chart interno). D7 como
fenômeno está CONFIRMADO na textura; como medição entregue, está
REPROVADO (números errados). Visibilidade no modelo renderizado ainda
não demonstrada (prévias Workbench são sombreadas, D10) — ressalva, não
novo experimento: uma prévia flat/unlit de região de costura fecha isso.

### 5. Adversarial 512 (D2-A) — CONFERIDO

- IoUs por vista idênticos à base nas 4 vistas (0,7231 / 0,7758 /
  0,3631 / 0,4085) e `faces_visiveis` idênticos: ESPERADO, não suspeito —
  IoU de silhueta depende da geometria, não da resolução da textura.
  Por isso mesmo, IoU é evidência FRACA de estabilidade de textura (S4-1);
  não é fraude, mas não prova nada sobre a textura.
- `faces_pintadas` caem de forma plausível e pequena (−4,1% frente,
  −5,5% costas, −4,2% esquerda, −6,2% direita) — sem crash, sem colapso.
- Cobertura rasterizada por mim: 91.356 texels a 512 (alegado 91.610,
  Δ 0,28%) e 366.140 a 1024 (alegado 366.673, Δ 0,15%); razão 0,2495
  (alegada 0,2498) ✓. Cegos 61,54% vs 61,56% base ✓.
- Distância base × 512 por face, reimplementada: média 37,91, mediana
  18,81, 38,27% > 30 — REPRODUÇÃO EXATA do alegado.
- `sem_cor 0`: NÃO re-verificável a partir dos artefatos (falta a
  máscara de cobertura do bake); alfa 255 em 100% dos pixels das 3
  texturas e todas as 49.750 faces amostráveis tornam o 0 plausível, mas
  não conferido (S3-2). D2-A, nos números entregues, APROVADO.

### 6. Adversarial sem costas (D2-B) — O DEFEITO CENTRAL (S2-2)

O bake não crashou; `por_vista` do adv3v tem 3 chaves (frente, esquerda,
direita) — a ausência da vista NÃO é silenciosa no resumo entregue.
(Ressalva S4-2: o `resultado_cor.json` nativo do bake não foi entregue;
verificar se ele próprio lista as vistas.)

O problema é a medição alvo/controle. Reprodução exata do executor:
com direção +Y (para cima) em frame glTF, limiar 0,5, obtenho alvo
n=13.204, média 18,95, mediana 0,0, 16,28% > 30 e controle n=12.248,
média 17,99, mediana 0,0, 14,26% > 30 — TODOS os números do executor, à
casa decimal. Ou seja: o `direcao_camera("costas")` usado no
`run_prova.py` vale (0,1,0) no frame em que foi aplicado às normais do
GLB — e (0,1,0) em frame glTF é PARA CIMA, não para trás. O executor
mediu topo × base, não costas × frente. A "separação fraca" é um
artefato desse erro de frame, não uma propriedade do bake.

Explicação mais provável (a confirmar pelo executor): a tabela de
direções vive em frame Blender (Z-up), onde costas = (0,1,0) está certo,
e o `run_prova` a aplicou crua às normais glTF (Y-up), sem a conversão
Blender→glTF (x,y,z) → (x,z,−y), que levaria costas a (0,0,−1) = −Z.
Se as câmeras do bake vivem dentro do Blender, o BAKE está correto e só
a MEDIÇÃO D2 está errada. Se a tabela for compartilhada sem conversão
também no bake, a vista "costas" do bake seria top-down — o executor
TEM de confirmar qual é o caso (S3-4). A assinatura de remoção aponta
para eixo horizontal (ver abaixo), o que favorece "só a medição errou",
mas não prova.

Recomputação no eixo correto (limiar 0,5; 0,9 = subconjunto quase puro):
- Se costas = −Z (conversão Blender→glTF): alvo 28,23 / 24,01% > 30 vs
  controle 7,05 / 5,86%; a 0,9: alvo 18,96 / 18,03% vs controle 8,41 /
  7,07%. Separação FORTE (4× na média a 0,5).
- Se costas = +X (outra convenção horizontal, melhor assinatura
  bruta): alvo 26,74 / 22,43% vs controle 8,97 / 7,49%; a 0,9: alvo
  21,43 / 17,52% vs controle 8,34 / 6,84%. Separação FORTE (3×).
- Em qualquer eixo horizontal, o adversarial sem costas DEGRADA de
  fato as faces da vista removida — a conclusão "adversarial fraco,
  precisa de caso mais forte (sem 2 vistas)" do executor está ERRADA
  como diagnóstico: o caso atual já é forte; era a régua que media o
  eixo errado. Não recomendo "sem 2 vistas" antes de republicar o D2
  com o eixo certo.

### 7. Escalada APR-01 — verificações NOVAS desta bateria

(a) Reimplementação independente da classificação de costura — revelou
a subcontagem de 3,4× e a malha fechada (borda 0 após solda).
(b) Proxy (mediana 4 amostras) × média rasterizada — gap confirmado por
método independente (item 3).
(c) Localização das piores costuras — 56,5% cruzam eixos dominantes vs
18,3% internas; piores 20 com área UV normal, não ruído de face miúda.
(d) Controle × alvo no sem-costas — revelou o erro de frame (+Y) e a
separação forte no eixo correto.
(e) Extras além do briefing: cobertura UV rasterizada independente
(Δ ≤ 0,28%); identificação exata do eixo medido pelo executor por busca
em grade (nenhuma direção horizontal reproduz os números dele; +Y
reproduz todos); teste flip-V quantitativo (item 8).

### 8. Limites declarados — flip V (L-23) e D10

Flip-V: recomputei D7 soldada e D2 com o mapeamento V invertido.
D7: costura média 113,98, mediana 100,81, 90,46% > 30; interna média
31,16, mediana 4,36, 30,25% > 30 — o GAP PERSISTE e até cresce. D2
(lim 0,9, eixo −X): alvo 15,95 vs controle 27,93 — a ORDENAÇÃO persiste.
Raciocínio L-23 CONFIRMADO para ordenações e gaps, com QUALIFICAÇÃO:
os valores absolutos mudam muito com o flip (costura 93,49→113,98;
mediana interna 13,96→4,36). Não se comparem absolutos entre convenções.
D10 confirmado: prévias Workbench são sombreadas; nenhuma conclusão de
cor foi tirada delas aqui.

### Pontos frágeis do executor — julgamento

(1) 37.456 bordas: CONFIRMADO como vício de falta de solda; após solda,
borda 0 e costura 13.758. A contagem do executor não sobrevive à solda
— mas a conclusão (costura salta mais) sobrevive e se fortalece.
(2) Separação fraca alvo/controle: REFUTADA como diagnóstico — era o
eixo errado (+Y). Com dot > 0,9 no eixo correto, a separação é forte.
(3) Proxy × raster: proxy aceitável para distribuições (item 3).
(4) Troca esquerda/direita nas imagens da Besta: NÃO RESOLVIDA e
ORTOGONAL a D2/D7. Evidência: IoUs laterais 0,3631/0,4085 contra
0,7231/0,7758 frente/costas — padrão compatível com troca, mas também
com arte lateral em 3/4 ou assimetria do modelo; as imagens de
referência não foram entregues, então não há como decidir. Se a troca
for real, D7 não é afetada (não usa rótulos de vista), D2-A não é
afetada (todas as vistas presentes) e D2-B só teria sua magnitude
alterada em segunda ordem (qual lateral pinta as diagonais das costas).
É um defeito S2 da TEXTURA BASE, não de D2/D7 — mas precisa ser fechado
antes de declarar a textura base boa.
(5) Prévias Workbench sombreadas (D10): confirmado, não usadas.

## Defeitos classificados

- S2-1 (D7): `classificar_arestas` não solda vértices por posição.
  Costura 4.017 vs 13.758 reais; 37.456 "bordas" falsas. Testes sem caso
  de vértice duplicado. Medição reprovada; fenômeno confirmado.
- S2-2 (D2): `direcao_camera("costas")` aplicada sem conversão de
  frame — D2 mediu topo/base (+Y/−Y), não costas/frente. Números do D2
  sem-costas publicados descrevem o eixo errado; conclusão de
  "separação fraca" é falsa.
- S2-3 (textura base, fora de D2/D7): suspeita de troca
  esquerda/direita não resolvida (IoU lateral baixo). Exige as imagens
  de referência; não bloqueia D2/D7, bloqueia a textura base.
- S3-1: suite 252 OK sem artefato (sem `suite.log`, sem demais testes).
- S3-2: `sem_cor 0` nos 3 bakes sem máscara entregue — plausível, não
  conferido.
- S3-3: margem da mesma UV: 2 px (`metricas_gerar_uv`) vs 11 px
  (`margem_2048`) — inconsistência não reconciliada; hashes do GLB de
  entrada e do `uv.npz` ausentes do resultado.
- S3-4: tabela de câmeras do bake sem frame documentado; executor deve
  confirmar se o bug de frame atinge só a medição D2 ou também o bake.
- S4-1: IoU idêntico entre bakes é esperado (silhueta) — evidência
  fraca, não fraude.
- S4-2: ausência da vista explícita no resumo (3 chaves); registro
  nativo do bake não entregue — verificar.
- S4-3: proxy infla médias (+11,5% costura, +38% interna na amostra) —
  vale para distribuições, nunca para aresta única.
- S4-4: flip-V muda absolutos, não ordenações (ver item 8).

## Vereditos (separados)

### D7 — REPROVA o fechamento nesta tranche
Motivo: os números entregues (costura n=4.017, interna n=51.880,
borda 37.456) estão errados — a medição não soldou vértices. Não se
fecha D7 sobre números falsos, mesmo com a conclusão qualitativa
confirmada. Para fechar, sem novo bake: (1) soldar por posição dentro
de `classificar_arestas` (tolerância 1e-6) e republicar os números —
os corrigidos, já verificados por mim, são costura n=13.758, média
93,49, mediana 77,22, p90 199,86, 78,08% > 30, 59,90% > 60; interna
n=60.867, média 36,20, mediana 13,96, p90 107,19, 36,61% > 30; borda 0,
não-manifold 0; (2) acrescentar teste de vértice duplicado à suite
(o caso que deixou o bug passar); (3) como ressalva, uma prévia
flat/unlit (não Workbench) de uma região de costura, para demonstrar
visibilidade no modelo, não só na textura.

### D2 — REPROVA o fechamento nesta tranche
Motivo: o D2 sem-costas publicado mediu o eixo errado (topo/base) e
concluiu "separação fraca" — falso sob o eixo correto, onde a
separação é forte (2,3×–4×). D2-A (512) está conferido e aprovado nos
números (item 5), mas D2 como um todo não fecha com o D2-B errado.
Para fechar, sem novo bake: (1) corrigir o frame da direção em
`run_prova` (documentar a tabela de câmeras em frame glTF; se costas
= −Z: alvo 28,23/24,01% vs controle 7,05/5,86% a 0,5 e 18,96/18,03% vs
8,41/7,07% a 0,9; se costas = +X: 26,74/22,43% vs 8,97/7,49% e
21,43/17,52% vs 8,34/6,84%) e republicar; (2) confirmar por escrito se
as câmeras do bake compartilham o bug de frame ou vivem só no Blender
(se compartilharem, o problema sobe para S1 do bake e D2 não fecha sem
novo bake); (3) registrar o eixo final usado, para a próxima execução
não precisar redescobri-lo por busca em grade.

Nenhum dos dois itens exige novo bake se as confirmações acima forem
favoráveis (medição D2 só no Blender; solda só no código de medição).
Se a confirmação do item (2) de D2 for desfavorável, D2 e a textura
base voltam para re-bake — e isso deve ser dito ao Mestre como
bloqueio real, não rotina.
