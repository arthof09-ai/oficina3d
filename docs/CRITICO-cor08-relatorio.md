# Critico senior — Tranche COR-08 (Etapa COR, ataque a D1)

**Dinamica:** APR-02 adversarial. O objetivo desta bateria foi TENTAR REPROVAR.
Nada abaixo foi aceito pela palavra do executor: tudo foi re-medido a partir
das fontes (codigo, resultados, GLBs, texturas, renders).

**Objeto:** repo `app/` em `C:\Users\txcga\RPG_Local\Oficina3D`, branch `main`,
HEAD `0e8746e` + arvore suja da COR-08 (M `oficina3d/cor/__init__.py`,
`_blender_cor.py`, `passo.py`, `projecao.py`, `testes/test_cor.py`;
novos `oficina3d/cor/preenchimento.py`, `testes/test_cor_alinhamento.py`,
`testes/test_cor_preenchimento.py`). Nenhum commit, nenhum push e nenhuma
edicao da arvore principal foram feitos por este Critico; todo o trabalho
proprio viveu em `jobs_teste/cor08-critico/` (fora do repo). A copia
`Oficina3D-codex` nao foi tocada.

**Base de comparacao:** job-ancora `jobs/20261101-101528-corint-orc-s7/cor/modelo_uv.glb`
+ 4 vistas canonicas `app/testes/dourado/imagens/orc_*.png`, os mesmos do
executor. Blender 5.2.3 LTS em todas as provas.

---

## VEREDITO

### (a) MECANISMO: APROVADO — 8,5/10

A0, A1, A2 e A3 funcionam como alegado, com os numeros reproduzidos
byte a byte por este Critico (secao Provas). O desconto de 1,5 vem do
defeito S2 do caminho de salvamento (pre-existente, nao introduzido pela
COR-08, mas atingindo em cheio a afirmacao de "fidelidade" desta tranche)
e dos S3 de nomenclatura/documentacao. O mecanismo A0–A3 em si nao tem
defeito S1/S2.

### (b) QUALIDADE VISUAL: APROVADA — 7,0/10 (com ressalva explicita)

NENHUM gatilho de reprovacao do padrao do olho do Mestre disparou: nao ha
confete generalizado, o rosto e legivel nas 4 vistas em que aparece, e as
regioes de cor se sustentam (pele verde, pano vermelho, pelo, armadura,
osso). A COR-08 e visualmente um pouco mais limpa que a baseline (rosto e
peito com menos mosqueado). **Ressalva:** esta aprovacao visual NAO e
aprovacao de fidelidade a arte: o modelo continua longe da arte canonica
em detalhe fino (o gap e de pose/geometria, nao so de alinhamento), e a
nota 7,0 reflete isso. Nao se deve citar esta secao como "a cor foi
aprovada" sem a ressalva.

### (c) D1: ABERTA (confirmado, nao refutado)

Nenhuma vista atinge a regua >= 0,88 do estudo D1. Maximo medido: frente
0,8177. A D1 NAO fecha nesta tranche. O executor admitiu isso e os numeros
confirmam.

### (d) Defeitos — o que exige correcao antes da publicacao

**Exige correcao antes de qualquer publicacao/afirmacao de fidelidade que
use `textura.png`, e antes do fechamento da D1:**

- **S2-COR08-1 (sRGB x LINEAR — caminho de salvamento + medias em espaco
  sRGB).** Ver secao "Auditoria sRGB". E pre-existente (v1), nao regressao
  da COR-08; nem por isso deixa de ser S2: ele falsifica o arquivo
  `textura.png` que a tranche entrega como prova. Correcao provada:
  fixar `cena.view_settings.view_transform = "Standard"` antes do
  `save_render` em `_blender_cor.py` (a sonda 2 mediu Standard = identidade
  byte a byte para o mesmo caminho de criacao de imagem) + teste de
  regressao (salvar valores conhecidos, comparar bytes). NAO usar "Raw"
  como correcao: a sonda mediu Raw = curva de potencia 2.2 (0,5 -> 55),
  ou seja, escurece. O codigo da COR-08 (A0–A3) pode ser commitado com o
  S2 registrado como pendencia aberta nomeada; a tranche NAO pode ser
  publicada como "fidelidade de cor resolvida" sem ele.

**Devem ser corrigidos (S3, nao bloqueiam o mecanismo):**

- **S3-COR08-2 (campo `texels_por_dilatacao_restrita` mente no modo `uv`).**
  Em `baseline` e `ablacao1024` o campo carrega o total da dilatacao
  IRRESTRITA (3.787.927 e 946.907) sob o nome "restrita". No modo `3d` o
  valor e de fato restrito. Renomear o campo do modo `uv` ou separa-lo
  (ex.: `texels_por_dilatacao_total` + `texels_por_dilatacao_restrita`
  so no modo `3d`).
- **S3-COR08-3 (argumento da ablacao via IoU e vazio; IoUs da ancora sem
  lastro no arquivo da ancora).** O IoU@256 e invariante ao tamanho da
  textura por construcao, logo "IoUs identicos aos da baseline @2048" nao
  prova nada sobre a A0. A evidencia valida e a cobertura direta
  (19,44% -> 48,12%), que esta correta. Alem disso, o `resultado_cor.json`
  da ancora COR-05 traz `iou_bake_256 = None` nas 4 vistas: a faixa
  "0,7237–0,7929" citada para a ancora nao tem lastro naquele arquivo
  (ela coincide com o diagnostico de silhueta do estudo D1, nao com um
  IoU de bake medido). Corrigir a citacao no registro da tranche.
- **S3-COR08-4 (`passo.py` nao fixa os controles).** O `pedido_cor` do
  passo nao passa `alinhamento` nem `preenchimento`: a fila de producao
  depende dos defaults de `_blender_cor.py` (`"otimizado"`/`"3d"`). Uma
  mudanca de default muda o bake de producao em silencio. Fixar as chaves
  no `pedido_cor`.

**Nits (S4, documentacao/observacao):**

- **S4-COR08-5 (`margem_min_px` escalada, rotulo enganoso).** A metrica e
  medida numa grade 512 e depois multiplicada por `tamanho/512`
  (`_blender_cor.py:369-371`). Por isso 4 @1024 e 8 @2048: E A MESMA
  MARGEM. Isso EXPLICA a divergencia do item 7 (nao e defeito de medicao),
  mas o campo `medido_em_px: 512` ao lado de um valor escalado induz a
  comparacoes erradas entre tamanhos. Reportar o valor normalizado ou
  renomear o campo.
- **S4-COR08-6 (dominio restrito: halo de faces inalcançaveis).**
  `dominio_dilatacao_restrita` subtrai os texels DAS faces inalcançaveis,
  mas NAO a faixa de 8 px ao redor delas: o halo em torno de uma
  componente isolada continua sendo pintado por dilatacao UV. Como esses
  texels estao fora de qualquer triangulo, nao ha impacto visual direto
  (salvo bleed em mips profundos, junto com os ~638 mil texels fora do
  dominio que ficam pretos por nunca serem pintados). A documentacao deve
  dizer isso com essas palavras, em vez de sugerir exclusao total.
- **Observacao (nao e defeito):** os tempos citados pelo executor
  (baseline 38,1 s / COR-08 54,35 s) sao o `tempo_s` interno do bake; o
  `status.json` registra tempos de parede maiores (39,1 s / 55,3 s); a
  minha reproducao levou 47,8 s. Tempos variam; os SHAs nao — e sao eles
  que importam.

---

## PROVAS (re-medicao propria)

### 1. Suite — CONFIRMADA (323, 0 falhas, 0 erros, skipped=1)

Re-executada por este Critico via discovery em `testes/` no `.venv_app`:
`SUITE_RESULT tests=323 failures=0 errors=0 skipped=1 ok=True` (28,8 s na
prova do executor; a minha rodou no mesmo script critico). Contagem
reconciliada por modulo (soma = 323): test_cor 31, test_cor_alinhamento
10, test_cor_preenchimento 8, test_cor_costura 7, test_cor_passo 14,
test_cor_vertice 28, test_job 36, test_motores 29, test_refino 30, resto
conforme `status_critico.json` (arquivo de trabalho do Critico, fora do
repo). Nenhuma divergencia. A contagem por arquivo confere com a contagem
AST local dos 3 arquivos novos/alterados do `cor`.

### 2. Reproducao do bake — CONFIRMADA, byte-identica

Reproducao propria do caso COR-08 (mesmo pedido: GLB-ancora, 2048,
dilatacao 256, `alinhamento=otimizado`, `preenchimento=3d`) em
`jobs_teste/cor08-critico/cor08rep/`:

- textura SHA-256 `c7302ee16f41a8f12577546223d509a906986fada1d3f39b61af1a35f4af989a`
  = alegado, exato.
- GLB SHA-256 `a8e793b267db27c2a06669dbb925c91b8863a99ec4f43f558c880a1d10a09b9a`
  = alegado, exato.
- Baseline baixada e conferida: textura `b4ae6ed7…`, GLB `318e8f70…` =
  alegados, exatos.
- Cobertura reproduzida identica: direto 420.713/845.063 (49,79%) vs
  baseline 406.377 (48,08%); cegos 424.350; preenchimento_3d 424.350;
  dilatacao restrita 2.709.638; sem_cor UV = 0; faces com fonte 24.590,
  preenchidas 25.160, sem fonte alcancavel 0, anel medio 3,18, max 21.
- IoUs bake reproduzidos identicos: frente 0,8177 / costas 0,7774 /
  esquerda 0,8065 / direita 0,7957 (baseline bbox: 0,7941 / 0,7232 /
  0,7925 / 0,7892). Ganho sobre a baseline: +0,0236 / +0,0542 / +0,0140 /
  +0,0065. O menor ganho (direita) e o maior (costas) sao reais, nao
  artefato de arredondamento: os valores saem do `resultado_cor.json`
  da minha reproducao com 4 casas iguais aos do executor.
- Determinismo: alem da reexecucao do executor (`cor08_det`, SHAs
  identicos), a MINHA reproducao independente deu os mesmos SHAs. Tres
  bakes, um unico par de SHAs. Determinismo PROVADO, nao so alegado.

### 3. Auditoria de proveniencia v2 (parse proprio do GLB, sem Blender)

Implementacao propria (nunca importei `projecao`/`preenchimento` para
isto): parse do GLB por struct, rasterizador baricentrico proprio,
expansao de mascara propria, solda por posicao propria. Resultados sobre
o GLB COR-08 entregue + `textura.png`:

- (i) **Texels UV recomputados: 845.063, diff 0** contra o alegado.
- (ii) **Componentes 3D soldadas: 1** (49.750 faces, 23.768 vertices
  unicos soldados de 71.336). Com uma unica componente e fontes diretas
  existentes, `faces_sem_fonte_alcancavel = 0` e FORCADO, nao so alegado.
  Faces com pelo menos 1 texel no meu mapa: 49.615 de 49.750 (135 faces
  minusculas nao cobrem nenhum centro de texel a 2048 — esperado e
  inofensivo; o bake conta faces por outro criterio).
- (iii) **Halo recomputado: 2.709.638, diff 0** contra o ganho de
  dilatacao alegado. Como antes da dilatacao TODOS os texels UV ja
  estavam pintados (direto 420.713 + 3d 424.350 = 845.063, exato), os
  2.709.638 ganhos sao necessariamente halo fora da UV — a alegacao do
  item 6 esta PROVADA, e o dominio e mesmo UV + 8 px (expansao Manhattan
  por 4-vizinhos, 8 passes, recomputada: dominio expandido 3.554.701
  texels, halo = 3.554.701 − 845.063 = 2.709.638).
- (iv) **Nenhum texel DENTRO da UV recebeu cor de dilatacao UV** — por
  construcao verificada no codigo (`dilatar` com `dominio` so pinta
  texels ainda nao pintados, e todos os UV ja estavam pintados) e pela
  aritmetica acima. A dilatacao UV no modo `3d` e 100% halo.
- (v) **Amostragem de consistencia do preenchimento 3D:** 12.970 faces
  sao monocromaticas na textura (136.626 texels) — esse numero NAO e o
  total preenchido (a maioria dos 424.350 texels preenchidos vive em
  faces MISTAS, parcialmente diretas, o que e consistente com
  24.590 faces-fonte + 25.160 preenchidas = 49.750). 69,2% das faces com
  >= 10 texels tem uma cor modal cobrindo >= 50% dos seus texels
  (modas tipicas: tons de pele/pelo e o vermelho (151,21,1) do pano) —
  assinatura compativel com preenchimento plano por face, nao prova
  isolada. **Limite honesto desta auditoria:** sem intermediarios
  salvos pelo bake (mapa texel-face, mascara direta), a verificacao
  per-texel "esta cor veio da face-fonte X via BFS" nao e refeita por
  fora; o que a fecha e a combinacao (reproducao byte-identica com o
  mesmo codigo + recomputacoes exatas (i)–(iv) + leitura do codigo de
  `aplicar_preenchimento`, que so toca texels cegos de faces
  alcancaveis). Registro o limite em vez de fingir cobertura total.

### 4. Auditoria sRGB x LINEAR — BUG REAL (S2), com a cadeia completa

Cadeia medida byte a byte (sondas Blender 5.2.3 em cena fresca, mesmo
estilo de invocacao do bake; o bake NAO altera `view_settings` antes do
`save_render` — o unico `view_transform = "Standard"` do script esta em
`renderizar_previas`, que roda DEPOIS do save):

1. **Carga da arte: SEM decodificacao sRGB.** `ler_imagem` via
   `foreach_get` devolve EXATAMENTE os bytes crus do PNG / 255 (5
   amostras de `orc_frente.png`: diff maxima 0,0000 contra o decode
   proprio; contra a conversao sRGB->linear, diff ate 0,2716). Os bytes
   sRGB da arte sao tratados como valores lineares durante todo o bake.
2. **Pintura e medias: em espaco sRGB.** `rasterizar_textura` copia a
   cor amostrada sem conversao; `cores_diretas_por_face` tira a MEDIA
   desses bytes sRGB (media em espaco nao-linear — erro pequeno para
   cores proximas, maior para misturas de alto contraste; nao quantificado
   como bloqueador isolado, mas parte do S2).
3. **Salvamento do `textura.png`: AgX.** `save_render` sob o default AgX
   mapeou [0,0,125,0,25,0,5,0,75,1,0] -> bytes [0,25,59,128,171,197]
   (medido 2 vezes, identico). Ou seja: branco 255 vira 197 (−23%) no
   arquivo. A sonda 2 mediu ainda: Standard -> identidade byte a byte
   ([0,32,64,128,191,255]); Raw -> potencia 2.2 ([0,4,13,55,133,255]).
4. **Exportacao glTF: verbatim.** A sonda 2 exportou um cubo com imagem
   de valores conhecidos como baseColor: o PNG embutido no GLB saiu
   EXATAMENTE [0,32,64,128,191,255] = os valores de entrada. O exportador
   nao transforma.
5. **Consequencia nos arquivos entregues (medida, nao inferida):**
   `textura.png` = AgX(textura do GLB). Para cada valor do GLB (canal R),
   a media no arquivo segue a curva AgX da sonda (GLB 32 -> arquivo 24;
   64 -> 57; 128 -> 127; 191 -> 175; 255 -> 197; diff media global
   5,57/255 na COR-08, maxima 64; so 15,5% dos texels UV sao identicos
   entre os dois arquivos; na baseline, 0,8%). **O GLB entregue e fiel
   aos bytes da arte nos texels diretos; o `textura.png` entregue NAO
   e.** Quem seguir a D10 ("amostrar a textura") no arquivo mede cores
   AgX, nao as cores entregues. Cores de vertice: nao ha neste caminho
   (material usa TexImage -> Principled Base Color; o achado C-COR01 do
   Codex e de outra frente e nao se aplica aqui — verificado: nenhum
   COLOR_0 no caminho de projecao).

### 5. QUALIDADE VISUAL, por regiao (previas do bake + analise numerica)

Metodo: previas Workbench do proprio bake (8 vistas, 2 casos, mesmas
camaras — comparacao apples-to-apples) vistas integralmente + crops de
rosto e peito/saia ampliados 3x, confrontadas com as canonicas. As
previas Workbench NAO foram usadas como prova colorimetrica (D10): a
cor foi amostrada numericamente na textura (secao 4).

- **Rosto (frente, perfil esquerda/direita): LEGIVEL nos dois casos.**
  Pele verde, listras vermelhas de pintura de guerra continuas, presas,
  headband, orelhas. A COR-08 tem o rosto um pouco mais limpo que a
  baseline (menos mosqueado nas bochechas). Nenhum rosto ilegivel.
- **Peito:** abdome verde, tira diagonal, cinto — sustentados nos dois
  casos; COR-08 com o pano vermelho central um pouco mais continuo.
- **Saia:** pano vermelho + cranio + ossos legiveis nos dois casos;
  sem manchas brancas invasoras (a mancha branca do antebraco do
  diagnostico D1 nao reaparece como classe).
- **Pernas/pes:** veu acinzentado nas pernas inferiores/pes EXISTE nos
  dois casos (mais forte na baseline direita) — pre-existente
  (highlight de estudio sobre armadura metalica + pelo claro), NAO
  regressao da COR-08.
- **Costas:** manto de pelo, trancas, saia vermelha posterior — coesos
  nos dois casos; e a vista de pior IoU (0,7774) e mesmo assim se
  sustenta visualmente.
- **Numerico (com a ressalva de que a metrica e confundida):** taxa de
  saltos adjacentes intra-face (distancia RGB > 180) na textura: COR-08
  5,8% vs baseline 4,1% vs arte ~2–3,3%. A COR-08 e MENOS suave que a
  baseline — esperado, porque a baseline suaviza por dilatacao (cor do
  vizinho mais proximo) enquanto a COR-08 pinta mais detalhe direto real
  (420.713 vs 406.377 texels) e junta plano/direto nas bordas de face.
  Esta metrica NAO mede confete e NAO foi usada para aprovar ou reprovar;
  o julgamento visual acima e que vale.
- **Tentativas proprias de render (registradas, sem maquiagem):** 3
  tentativas de renders independentes falharam em exibir a textura —
  (1) Workbench + material Emission: cinza plano (o Workbench nao
  sombreia material so-Emission); (2) EEVEE headless: modelo no quadro,
  cinza; (3) Workbench + material original importado: modelo no quadro
  (centro/dimensoes conferem com o bake: (0,0,0,5)/(0,6794,0,6966,1,0)),
  cinza. Verifiquei que os links (Image Texture.Color -> Principled
  Base Color) e a UV ativa (UVMap) do GLB importado estao corretos — o
  cinza e um quirk do meu harness de importacao no Blender 5.2, NAO
  evidencia contra a textura (cujos pixels foram decodificados e
  analisados diretamente, e que as previas do proprio bake exibem).
  Fica como pendencia de ferramenta, nao como defeito da tranche.

### 6. Ablacao A0 x resolucao — atribuicao CONFIRMADA, argumento parcial

- Ancora COR-05 (arquivo `resultado_cor.json` do job-ancora): 1024,
  direto 41.070/211.268 = 19,44% (exato), textura `ebd744a9…` (exata).
- Ablacao do executor (fix+bbox+uv @1024): direto 101.669/211.268 =
  48,12%; IoUs 0,7941/0,7232/0,7925/0,7892, identicos aos da baseline
  @2048 (verificados nos dois `resultado_cor.json`).
- **Isolamento limpo:** `git diff e3a4ca4..0e8746e` para
  `projecao.py`/`_blender_cor.py` e VAZIO — o caminho de projecao nao
  mudou entre a COR-05 e a base da COR-08 (so `passo.py` mudou, com
  roteamento do modo vertice, irrelevante para a ablacao, que chama
  `rodar_cor` direto). Com o mesmo codigo, a unica diferenca entre
  ancora e ablacao e a A0 (o codigo A1/A3 existe mas dorme nos controles
  bbox/uv, verificado por leitura). Logo: **a A0 (nao a resolucao)
  explica o salto 19,44% -> 48,12%**. Ressalva S3-COR08-3: a parte do
  argumento via IoU e vacua (IoU@256 independe do tamanho da textura) e
  os IoUs da ancora nao constam do arquivo da ancora.

### 7. Casos-limite do codigo novo — testados com entradas adversariais proprias

Fora dos testes do executor, com o codigo puro importado localmente
(14 checagens, 13 PASS + 1 expectativa minha corrigida):

- `dilatar` com dominio vazio: pinta 0, nao trava. Sem fonte e sem
  dominio: 0. Dominio com texel isolado longe da fonte: 0.
- `dominio_dilatacao_restrita` com componente isolada: passes=0 exclui
  exatamente os texels da face isolada; passes=8 mantem o halo ao redor
  dela (comportamento documentado; ver S4-COR08-6) e exclui os texels da
  face. Minha expectativa inicial (halo da isolada fora do dominio)
  estava errada contra a especificacao — corrigida, nao e defeito.
- `difundir` sem nenhuma fonte: tudo inalcançavel, anel −1.
- `otimizar_alinhamento`: pixel unico (IoU 1,0), aspecto extremo
  (trava 0,15 respeitada, nunca piora: 0,75 -> 0,7883), arte disjunta,
  mascara aleatoria deterministica (duas execucoes identicas), formatos
  distintos e mascaras vazias recusados/None conforme a API (ValueError
  no `otimizar_`, None no `alinhamento_otimizado`).
- `bbox_robusta_mascara` de 1 px nao degenera (10,10,11,11).
- `aplicar_alinhamento` com escala negativa (espelho) nao trava.
- `mapa_texel_face` com triangulo UV degenerado: ignorado, sem travar.
- Contagens de candidatos: 3.331/3.181/3.331/3.231 por vista sao
  consistentes com a grade documentada (1690 + 441 + ate 1225, menos os
  vetados pela trava de aspecto).

### 8. Autoauditoria do executor — confrontada, HONESTA nos 3 pontos

Nao ha documento de autoauditoria no repo (a tranche ainda nao atualizou
REGISTRO/ESTADO — esperado pre-commit; o registro final do executor deve
inclui-la). Confrontei os 3 defeitos alegados contra o codigo:

1. **`dilatar` sem o parametro `dominio`:** CONFIRMADO e corrigido —
   `projecao.py:539` tem `dominio=None` e `_blender_cor.py:467-471` o
   passa; os testes novos o exercem (`test_dominio_limita_o_preenchimento`).
2. **A3 existia mas NAO estava ligada ao bake:** CONFIRMADO o historico
   pela estrutura atual — hoje esta ligada (`_blender_cor.py:455-471`,
   controle `preenchimento` com default `"3d"`, pedido da prova com
   `"3d"`). Nenhum vestigio de ligacao parcial restante.
3. **Limiar +0,08 insatisfazivel em `test_recupera_protrusao`:**
   CONFIRMADO por prova analitica propria (nao pela palavra dele).
   Busca exaustiva sobre afins continuas (escalas 0,5–1,6 passo 0,01,
   deslocamentos ±40 passo 0,5, intersecao exata por retangulos) deu
   maximo EXATO 0,93632959 = 2500/2670 em (1,0,1,0), diff 1,5e-15.
   O teste atual afirma `iou_final >= iou_v1`, `>= iou0` e
   `~= 2500/2670` (3 casas) + `>= 0,85` — afirma o que o caso realmente
   prova. Correcao honesta, nao mascara de fraqueza. A recuperacao a
   partir de v1 genuinamente baixa segue coberta por
   `test_ponta_fina_recupera_iou`.

### 9. Coerencia documental — numeros com lastro

Todos os numeros do executor conferem com arquivos: suite (suite.log +
minha re-execucao), SHAs (textura/GLB baixados e hasheados por mim),
cobertura e IoUs (resultado_cor.json do executor + da minha reproducao),
ancora (resultado do job-ancora, salvo o ponto S3-COR08-3 sobre os
IoUs). Unica incoerencia de citacao encontrada: S3-COR08-3. O ESTADO e o
REGISTRO do repo ainda estao pre-COR-08 (correto: a tranche nao foi
commitada); o proximo passo declarado ("COR-08") bate com o objeto
desta critica.

### 10. Transferencia do alinhamento otimizado — verificada

O transform e otimizado na grade 256 e reescalado para a imagem cheia
(`ax/ay` inalterados, `bx/by` vezes `wi/256` e `hi/out_h`) em
`alinhamento_otimizado_vista`. A reescala e correta para grade uniforme
(erro < 1 px na grade 256, documentado); o IoU reportado e o da grade
256, comparavel numero a numero com o v1. Nenhum bug de transferencia
encontrado. O ganho do otimizador sobre o inicial robusto e modesto
(frente 0,8070 -> 0,8177; costas 0,7394 -> 0,7774): a maior parte do ganho
sobre o v1 vem das caixas robustas + busca, nao de um milagre afim —
leitura honesta, nao defeito.

---

## ITENS QUE FICARAM SEM VERIFICACAO PLENA (registrados, nao inventados)

1. Renders flat/unlit (Emission) independentes: 3 tentativas falharam
   como descrito na secao 5 (quirk do harness de importacao). A evidencia
   visual usada foram as previas do proprio bake (8 vistas + crops) e a
   analise numerica direta da textura/GLB. Se o executor quiser, um
   render flat pode ser refeito na sessao do bake (onde o material foi
   construido), sem importacao.
2. Verificacao per-texel da fonte BFS (qual face-fonte originou cada
   texel preenchido): sem intermediarios salvos, coberta indiretamente
   (secao 3, item (v) + reproducao byte-identica). Recomendo que o bake
   passe a salvar o mapa texel-face e a mascara de proveniencia como
   artefatos do job (custo pequeno, auditoria futura exata).
3. Tempos de bake: variam por maquina/carga (47,8 s na minha reproducao
   vs 54,35 s do executor); irrelevante diante dos SHAs identicos.

---

## RECOMENDACAO FINAL

- **Mecanismo A0–A3: APROVADO.** Pode ser commitado (com o S2 registrado
  como pendencia aberta nomeada S2-COR08-1, mais S3-COR08-2/3/4 e
  S4-COR08-5/6 no backlog da tranche seguinte).
- **Qualidade visual: APROVADA com a ressalva da secao (b).** Nao citar
  sem ela.
- **D1: ABERTA.** Proximo ataque precisa mirar o que o IoU nao alcanca:
  a diferenca de pose/proporcao entre arte e malha (a arte canonica tem
  pose e proporcoes distintas do modelo gerado; nenhuma afinidade fecha
  isso) — e, antes de qualquer nova afirmacao de fidelidade, o S2.
- **Nao aprovo:** fechamento da D1; qualquer texto que apresente a
  aprovacao de mecanismo como aprovacao de qualidade; qualquer uso de
  `textura.png` como prova colorimetrica ate o S2 ser corrigido (usar o
  GLB, ou o `textura.png` apos o fix, com o teste de regressao).
