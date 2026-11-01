# CRÍTICO SÊNIOR — T1-mecanismo (Etapa COR, projeção + bake)

**Data:** 01/11/2026 · **Julgado:** o *mecanismo* do T1, não o T1 completo.
**Código julgado:** `app/oficina3d/cor/` — cópias fiéis do commit 69a44ca em
`hidden_files/2026-11-01-cor/cor_code/` (`projecao.py`, `_blender_cor.py`,
`__init__.py`, `test_cor.py`).
**Evidências lidas integralmente antes do veredito:** `sintetico/` (resultado.json,
textura.png, 4 prévias), `orc/` (resultado.json, textura.png, modelo_cor.glb,
4 prévias), `canonicas/` (4 vistas), `cor_code/` (4 arquivos), REGISTRO.md e
ESTADO_ATUAL.md da tranche, `pedido_orc.json` / `pedido_sintetico.json`.
**Método:** imagens vistas de verdade (não estimadas); GLB decodificado sem
Blender (parse do JSON + buffers binários); textura e prévias amostradas
numericamente (PIL/numpy); aritmética do resultado.json refeita; código lido
linha a linha. Não rodei o Blender (fora do escopo desta bateria, por ordem).

**Escala de severidade usada neste relatório:**
S1 = invalida o mecanismo (reprova) · S2 = grave para a qualidade final, não
reprova o mecanismo · S3 = moderado, corrigir antes do T1-completo ·
S4 = ressalva / documentação / cosmético.

---

## 0. Verificação aritmética das alegações numéricas (todas conferem)

| Alegação do executor | Conferência independente | Resultado |
|---|---|---|
| SHA textura Orc `93c14cc6…eb212` | `sha256sum` do arquivo baixado | **IGUAL** |
| SHA GLB Orc `fe73cf88…8c3bd` | `sha256sum` do arquivo baixado | **IGUAL** |
| SHA textura sintético `32cc0955…5c8e` | `sha256sum` do arquivo baixado | **IGUAL** |
| Textura Orc 1024 px, tempo 24,71 s | resultado.json | confere |
| IoU frente 0,7947 / costas 0,7241 / esquerda 0,793 / direita 0,7872 | resultado.json (não reproduzível sem Blender; valores plausíveis, sem contradição interna) | confere como registro |
| Cobertura direta 8.513/42.494 = 20,03%; cegos 33.981 = 79,97% | 8513/42494 = 20,034%; 33981/42494 = 79,966% | **EXATO** |
| 0 texels UV sem cor após 256 passes | `texels_uv_sem_cor_apos_dilatacao: 0` | confere |
| Dilatação 1.040.063 texels | = 1024² − 8.513 = 1.040.063 | **EXATO** (ver ressalva: inclui texels fora da área UV, item 4) |
| Sintético 4/4 cores exatas, IoU 1,0, 1,5 s | resultado.json + textura com 5 cores (4 sólidas + preto das zonas cegas) | confere, com ressalva sobre o IoU (item 6) |
| 15 testes novos; suite 233 = 218 + 15, skipped=1 | contagem no arquivo: 5 (câmeras) + 3 (alinhamento) + 5 (bake) + 2 (UV) = **15** | confere; o total 233 é número do executor (não re-executável daqui) |
| GLB Orc 49.750 tris | decode: 149.250 índices / 3 = **49.750** | **EXATO** |
| Vértices 58.552 (resultado.json) vs 58.732 no GLB | diferença de 180 = duplicação em costuras de UV na exportação glTF | **esperado, não é erro** (o "vértices" do JSON é da malha Blender, não do GLB) |
| Por vista: texels 3076+2593+2191+2093 = 9.953 > 8.513 diretos | reescritas por facing maior entre vistas (1.440 overwrites) | **consistente, não é erro** |

**Nenhuma alegação numérica verificável estava errada.** O que segue são
limitações de prova e de qualidade, classificadas uma a uma.

---

## 1. Fidelidade por região (prévia do Orc × vista canônica)

Método: inspeção visual das 4 prévias + amostragem numérica por caixas
relativas (mesmas caixas nas prévias e nas canônicas). Aviso metodológico
importante, provado nesta bateria: **as prévias Workbench NÃO são
colorimétricas** — o cubo sintético, cuja textura é vermelho puro (255,0,0),
renderiza (177,55,55) no centro da prévia. O sombreamento Workbench escurece
tudo; logo, escuridão na prévia ≠ escuridão na textura. A textura em si é
clara (ex.: ponto central (166,135,84)). Leituras de cor abaixo usam a
textura como referência final e as prévias como referência de distribuição.

- **Rosto — ERRADO (S2).** Na prévia de frente, a região da cabeça é um
  borrão escuro (média da caixa da cabeça (53,43,39), contra (84,60,43) na
  canônica): sem face legível, sem presas, sem olhos, sem cicatrizes
  vermelhas. O rosto canônico não sobrevive à projeção.
- **Peitoral/armadura — ERRADO (S2).** O centro do peito na prévia de frente
  é dominado por painéis escuros (70% dos pixels com max<60 na caixa do
  peito); o verde do peitoral, a tira diagonal e a cabeça de lobo canônicos
  não são legíveis. Tons de armadura (marrom/cinza) existem em traços largos,
  mas sem forma.
- **Braços — PARCIAL (S3).** Tons escuros de armadura presentes nos dois
  braços; mãos ilegíveis. Defeito local nomeado: **faixa clara vertical no
  lado direito da prévia de frente (braço esquerdo do personagem,
  x≈0,66–0,75)**, com núcleo de 295 px com os 3 canais >170 — a "mancha
  branca" do executor, confirmada e localizada. É tom de pele/pelo deslocado,
  não vazamento da vista de costas (ver item 3).
- **Pernas — PARCIAL (S3).** Mosqueado marrom/tan compatível com armadura em
  traço largo; sem grevas, sem bordas de pele e sem leitura de forma.
- **Tecido vermelho — PARCIAL, o que melhor sobrevive (S3).** O vermelho é a
  família de cor mais contrastante e aparece espalhado nas 4 prévias (faixas
  vermelhas na cintura da frente, laterais das costas, lâmina do machado nas
  laterais). Na textura, 7,2% dos texels são vermelhos fortes. Sobrevive como
  acento, não como peça de roupa: está fragmentado e deslocado.
- **Costas — PARCIAL, a vista mais legível (S3).** A prévia de costas é a
  única em que massas grandes batem com a canônica: massa tan de pele/capa,
  massa escura de cabelo, acentos vermelhos laterais. Ainda assim sem detalhe
  (sem tranças, sem caveiras, sem fivelas legíveis).
- **Laterais — PIOR REGIÃO (S2).** Esquerda e direita têm as maiores frações
  escuras (0,46 e 0,54 dos pixels de frente, respectivamente) e o "confete"
  mais denso. As grandes áreas pretas laterais do executor são reais — mas
  sua causa é dupla (item 8a): dilatação a partir de vizinhos escuros
  **mais** sombreamento Workbench sobre superfícies de perfil. Na textura,
  33,7% dos texels são escuros (max<60), o que inclui áreas fora da UV.

**Síntese do item 1:** o Orc é reconhecível pela silhueta e pela paleta em
traço largo, mas **nenhuma região tem fidelidade de detalhe**. Isso é
compatível com ~1 texel/face (item 8b) e NÃO é, por si só, reprovação do
mecanismo (critério de aceite): a fragmentação é explicada pela UV medida,
não por erro de projeção. A palavra final de fidelidade artística é do
Mestre, não deste relatório.

## 2. Costura (junções frente/lateral e lateral/costas)

**Não há descontinuidade de costura distinguível do ruído global (S3).**
Como cada face tem ~1 texel, a superfície inteira já é descontínua em
granularidade de face: não existe uma "linha de costura" visível para
julgar, nem nas prévias nem na textura (na textura, as 8.098 ilhas são
separadas por faixas dilatadas; a cor salta de ilha para ilha em toda parte).
Consequência honesta: **a continuidade de costura não é avaliável nesta
resolução de UV** — é uma pendência do T1-completo (com UV de qualidade, a
costura volta a ser testável), não um defeito de costura do mecanismo.
Nenhuma linha de costura anômala (faixa preta/branca contínua ao longo de
uma junção) foi encontrada nas 4 prévias.

## 3. Atravessamento — MEDIDO

**Controle sintético (prova forte):** as 4 faces laterais do cubo saem com a
cor EXATA da sua vista (tolerância 0,05, 2 amostras por face) e nenhuma
contaminação cruzada — frente vermelha, costas azul, esquerda verde, direita
amarela. Facing + oclusão por BVH separam as vistas no caso controlado.

**Teste-espelho no Orc (prova fraca por si só, registrada como tal):**
as paletas canônicas de frente e costas se sobrepõem muito (pele, pelo,
vermelho e armadura nos dois lados), então um teste-espelho no Orc não
isola bem o vazamento. O que foi medido:

- Caixa da cabeça: prévia de frente (53,43,39) vs prévia de costas (72,58,51)
  — a cabeça de costas é MAIS CLARA que a de frente, o oposto do que um
  vazamento da face (ou do cabelo preto) produziria de forma sistemática;
  não há massa de cor de frente sobre as costas.
- Lâmina do machado: a lâmina grande canônica aparece nas laterais do Orc
  (esquerda/direita) nas posições corretas de cada vista e NÃO aparece como
  massa prateada/vermelha na vista oposta.
- A mancha branca do antebraço de frente é tom de pele/pelo **da própria
  vista de frente** (a canônica de frente tem pelo claro no ombro esquerdo),
  ou seja, desalinhamento intra-vista + dilatação — não atravessamento.

**Conclusão do item 3:** nenhum atravessamento detectado; a prova que
sustenta isso é o controle sintético, não o teste-espelho do Orc (fraco
pela sobreposição de paletas — limitação declarada, não escondida).

## 4. Cobertura — 80% por dilatação: aceitável para o mecanismo?

**Sim, para o mecanismo; não, para qualquer alegação de qualidade.**
Os percentuais conferem (item 0). O que eles significam:

- O mecanismo prova o encanamento "sem buracos": após 256 passes, 0 texels
  UV sem cor. Isso é o que um mecanismo precisa provar.
- Mas o preço visual é explícito: **só 20,03% da superfície visível tem cor
  projetada de verdade; 79,97% tem cor de vizinho UV**. E vizinho UV ≠
  vizinho 3D: com 8.098 ilhas empacotadas em 4% do quadrado, a dilatação
  pega cor de ilhas de partes do corpo sem relação com a face. É por isso
  que o Orc sai "confete": a maioria das faces exibe a cor do vizinho UV,
  não a sua.
- Ressalva numérica: o `texels_por_dilatacao` (1.040.063) conta a textura
  inteira, incluindo área fora da UV. O preenchimento relevante para a UV é
  33.981 texels. O relatório do executor não esconde isso (o campo
  `texels_uv_sem_cor_apos_dilatacao` separa os dois), mas quem ler só o
  número grande pode superestimar o trabalho — fica registrado aqui.

**Implicação visual nas prévias:** o confete, as áreas pretas laterais e a
mancha branca são, em grande parte, artefatos de dilatação (item 8a), não
de projeção errada.

## 5. Determinismo — trilha de auditoria INSUFICIENTE (S3, não S1)

- Verificado: os SHAs do resultado.json **batem** com os arquivos baixados
  (textura e GLB). O resultado.json atual é, segundo a tarefa, o do 2º run.
- **Insuficiente como prova independente:** não há artefato preservado do
  1º run (nenhum JSON, log ou hash do 1º run no diretório de evidências nem
  no REGISTRO — o REGISTRO traz apenas a frase "2 runs deram SHA idênticos",
  sem os valores do 1º run). Um auditor que chegue agora não consegue
  reproduzir a comparação; só consegue confirmar o 2º run.
- **Por que não reprova o mecanismo:** (a) a alegação não foi refutada —
  é não-provada, não falsa; (b) inspeção do código mostra o caminho do bake
  determinístico por construção (ordem de vizinhos fixa na dilatação, ordem
  de faces fixa, sem aleatoriedade, sem carimbo de tempo nos bytes da
  textura; a única fonte externa de não-determinismo seria a exportação
  glTF, e o GLB entregue é byte-estável no que foi medido). O determinismo
  é plausível e o código não o contradiz — mas **antes do T1-completo
  exige-se re-prova com os dois resultado.json preservados** (ou re-execução
  com hashes registrados lado a lado). É pendência de prova, não defeito de
  código.

## 6. Regressão — leitura de test_cor.py e projecao.py

15 testes, contados um a um (item 0). Cobertura real:

- **Câmeras iguais às do refino — COBERTO E FORTE.** `test_direcao_igual_a_previa`
  compara diretamente contra `refino.previa.direcao_camera` nas 6 vistas:
  não é tautológico, é verificação cruzada entre módulos. Centro-no-centro e
  esquerda-à-direita na frente também cobertos.
- **Facing — COBERTO** (1,0 / 0,0 / normal nula). **Empate — COBERTO, mas o
  teste é MAL NOMEADO (S3):** `test_maior_facing_vence` usa DUAS VEZES a
  mesma vista e admite no comentário que testa o empate (primeira vence por
  `>` estrito). **A regra "maior facing vence" entre vistas DIFERENTES não
  tem teste de unidade.** É a lacuna de teste mais séria desta bateria: a
  prioridade por facing é o coração do bake multi-vista e só tem prova
  sistêmica (sintético + Orc, onde reescritas ocorreram — 9.953 writes
  contra 8.513 texels únicos — mas sem verificação numérica de que o maior
  venceu em cada texel).
- **Dilatação — COBERTO** (preenche 4 vizinhos em 1 passe, para com 0
  passes). Falta: comportamento de borda (o `np.roll` com anulação da faixa
  — código correto por inspeção, sem teste).
- **Métricas UV — COBERTO PARCIALMENTE.** Quadrado sem distorção/1 ilha e
  quadrados separados/2 ilhas com margem >0. Faltam: distorção com valor
  conhecido ≠ 0; margem diagonal (limitação documentada no código, sem
  teste); contagem de ilhas com arestas compartilhadas em malha real.
- **Não testados (lacunas nomeadas, S3/S4):** (a) rejeição por máscara —
  todos os testes de bake usam máscara toda-verdadeira, então o caminho
  `amostra_ok = mascara & facing` nunca é exercitado; (b) skip de UV
  degenerada; (c) alinhamento com aspectos diferentes (escalas x/y
  independentes podem achatar a anatomia — sem teste); (d) `iou` com duas
  máscaras vazias retorna 1,0 (degenerado: "acordo perfeito" sobre nada —
  no bake o caso é desviado por `continue`, mas a função em si mente);
  (e) **todo o caminho Blender** (BVH/oclusão, exportação GLB) não tem
  teste de unidade — compreensível (precisa do Blender), mas é exatamente
  o caminho que já quebrou uma vez nesta tranche (tupla do `ray_cast`).
  Sua única prova são as duas runs.
- **IoU sintético 1,0 — VACUO COMO EVIDÊNCIA DE SILHUETA (S3).** Com máscara
  sintética toda-verdadeira, o alinhamento estica a silhueta do cubo para o
  quadro inteiro e o IoU dá 1,0 qualquer que seja a geometria sólida. O
  número está aritmeticamente certo, mas não prova acordo de silhueta. A
  prova sintética que vale é a das cores exatas, não o IoU. O executor deve
  corrigir a leitura (nota de rodapé no REGISTRO), não o código.

**Nenhum teste é tautológico** no sentido estrito (nenhum testa o próprio
código contra si mesmo, exceto a comparação câmera×câmera, que é cruzada
entre módulos). Há um teste mal nomeado e lacunas acima — insuficientes
para reprovar o mecanismo, suficientes para exigir complemento antes do
T1-completo.

## 7. Adversarial PENDENTE (não reprova o mecanismo)

**Pendência nomeada, severidade S2 para o T1-completo / S4 para o
T1-mecanismo:** (a) Besta em menor resolução não testada; (b) vista faltante
não testada (o que acontece com 3 vistas? o código desvia máscara vazia com
`continue`, mas o comportamento ponta a ponta — buracos maiores, dilatação
ainda zerando? — não foi medido). Registradas aqui como pendências formais
do T1-completo. Conforme a ordem, **não são reprovação automática do
mecanismo**.

## 8. Escalada APR-01 (verificações novas)

### (a) Auditoria de proveniência por texel — Orc

- Pintura direta: **8.513 texels UV (20,03%)**. Dilatação UV: **33.981
  texels (79,97%)**. Por vista, texels únicos não somam (reescritas
  explicadas no item 0).
- Artefatos explicados pela dilatação, um a um:
  - **Confete generalizado:** face média <1 texel; a maioria das faces não
    contém nenhum centro de texel direto e herda a cor do vizinho UV mais
    próximo — que pertence a outra ilha, outra parte do corpo. O confete é
    o sintoma visual exato de 80% de dilatação sobre 8.098 ilhas.
  - **Áreas pretas laterais:** dilatação a partir de ilhas escuras
    (cabelo, armadura escura, sombras da arte) + sombreamento Workbench.
    NÃO é vazamento do fundo preto da arte: a máscara é por alfa
    (`origem_mascara: alfa` nas 4 vistas) e o fundo é excluído da amostra.
  - **Mancha branca no antebraço de frente:** dilatação a partir de ilhas
    claras (pelo) para faces do braço sem texel direto. Confirmada e
    localizada no item 1.
- Conclusão: a proveniência é **totalmente rastreável e honesta** — o
  executor reportou os 80% em vez de escondê-los. A dilatação v1 é o
  mecanismo correto para "sem buracos", mas é visualmente destrutiva nesta
  densidade de ilhas. T5 (UV de qualidade) é o gargalo, como o executor já
  concluiu.

### (b) Verificação independente da área UV — CONFIRMADA

Decode próprio do GLB (sem Blender): soma analítica das áreas UV =
**0,04324 (4,324% do quadrado UV)**; média de **0,91 texel/face** em 1024 px;
mediana **0,83**; **61,7% das faces (30.685/49.750) têm <1 texel**;
23,9% têm <0,5 texel. UV dentro de [0,1] em ambos os eixos (mín. 0,0042 /
0,0110; máx. 0,9958 / 0,9958).
**A alegação do executor (4,32%, ~1 texel/face) é CONFIRMADA**, com uma
nuance: a ocupação rasterizada do resultado.json é 0,03983 (medida a 512 px)
e a rasterização a 1024 px dá 42.494/1.048.576 = 4,05% — a diferença
4,32% (analítica) vs 4,05% (raster) é amostragem de centro de pixel, não
erro. A conclusão "a UV atual não sustenta detalhe" **está correta e é
independente do mecanismo de projeção**.

### (c) Integridade do GLB entregue — CONFIRMADA

Parse próprio do JSON do `modelo_cor.glb`: 1 malha; primitivas com
`POSITION`, `NORMAL` e **`TEXCOORD_0`**; **1 imagem** (PNG embutido,
bufferView própria); **1 material** (`cor`, `doubleSided: true`,
`baseColorTexture` presente, metallic 0, roughness 0,5). 49.750 triângulos.
O GLB é válido, texturizado e autocontido. A verificação do próprio script
(`verificar_glb_texturizado`) é fraca (só olha `materials[0]`), mas com 1
material o resultado é o mesmo — ressalva S4, não defeito.

## 9. Código — defeitos que invalidariam os resultados? NÃO HÁ (S1: nenhum)

Lidos integralmente `projecao.py` e `_blender_cor.py` (e `__init__.py`).
Nenhum defeito invalida os resultados. Itens examinados especificamente:

- **`ray_cast` com `(None,None,None,None)`** (`_blender_cor.py`, laço de
  visibilidade): tratamento **correto** para o Blender 5.2 — sem acerto,
  `hit[0] is None` → visível; com acerto, `hit[3] >= dist_cam - diag*1e-3`
  → acerto além da câmera não oclui. A comparação de distância usa o
  índice 3 (distância) corretamente. Caso conservador (`hit[3] is None`
  com acerto) marca invisível — seguro, não infla pintura.
- **`transform_apply` do cubo** (`criar_cubo`): **correto e documentado** —
  sem ele, vértices locais (z=0) vs BVH em mundo (z=1) deslocariam oclusão
  e enquadramento. Era o bug real da tranche e está corrigido.
- **Fallback Smart UV** (`uv_garantida`): correto (mesmos parâmetros do
  refino, reportado por `uv_gerada_no_bake`). **Ressalva S4:** nesta tranche
  o caminho NÃO foi exercitado pelo Orc (`uv_gerada_no_bake: false` — a
  entrada já tinha UV) e o cubo sintético usa Smart UV direto em
  `criar_cubo`, não via `uv_garantida`. O fallback em si segue sem prova de
  execução — pendência de prova, não defeito.
- **Limitações reais do código, declaradas como v1 (não defeitos
  silenciosos):** (a) oclusão por centroide da face — face grande
  parcialmente oclusa pinta inteira se o centroide estiver visível
  (irrelevante a 49.750 tris, faces pequenas); (b) `bbox_m` do alinhamento
  usa todos os vértices projetados, incluindo partes fora da silhueta da
  arte (ex.: machado em pose diferente) — pode esticar o mapeamento, e é
  por isso que o IoU residual fica em 0,72–0,79 em vez de ~1; (c) empate
  de facing vai para a primeira vista da lista (ordem do pedido) —
  determinístico, mas arbitrário; (d) `iou` com união vazia retorna 1,0
  (item 6d); (e) prévias Workbench são sombreadas — não servem como prova
  colorimétrica (item 1); a prova de cor é a textura, não a prévia.
- **Não encontrados:** inversão de eixo, troca de vista, erro de sinal no
  facing, vazamento de fundo, escrita fora da UV, não-determinismo no
  caminho da textura.

---

## Lista de defeitos e pendências (tudo o que o veredito carrega)

**S1 (reprova o mecanismo): nenhum.**
**S2 (grave p/ qualidade final, não p/ mecanismo):**
- D1. Fidelidade de detalhe ausente no Orc em todas as regiões (rosto e
  peitoral ilegíveis; laterais as piores) — explicada pela UV, não pelo
  mecanismo; bloqueia qualquer alegação de "T1 pronto" até o T5.
- D2. Adversarial pendente: Besta em menor resolução e vista faltante não
  testados.
**S3 (corrigir antes do T1-completo):**
- D3. Trilha de determinismo insuficiente: falta o artefato do 1º run;
  re-provar com os dois resultado.json preservados.
- D4. Teste `test_maior_facing_vence` mal nomeado: testa empate, não
  maior-facing-vence; criar o teste verdadeiro (duas vistas, facings
  distintos).
- D5. IoU sintético 1,0 é vacuo como evidência de silhueta; corrigir a
  leitura no REGISTRO (a prova sintética é a cor exata).
- D6. Lacunas de teste: rejeição por máscara, UV degenerada, borda da
  dilatação, distorção ≠ 0, alinhamento com aspectos distintos.
- D7. Costura não avaliável nesta densidade de UV (volta a ser testável
  com o T5).
**S4 (ressalvas):**
- D8. `iou` com união vazia = 1,0; `verificar_glb_texturizado` só olha
  `materials[0]`; fallback Smart UV sem prova de execução nesta tranche;
  oclusão por centroide; empate de facing para a primeira vista.
- D9. Limite desta auditoria: commit 69a44ca e suite 233 não foram
  re-verificados contra o repo/PC (cópias tomadas como fiéis por premissa
  da tarefa; 15 testes conferidos por leitura); IoUs do Orc aceitos como
  registro (não reproduzíveis sem Blender).
- D10. Prévias Workbench são sombreadas — leituras futuras de fidelidade
  devem amostrar a textura ou usar render plano, não a prévia.

## Veredito

**APROVA o T1-mecanismo** (projeção das vistas canônicas com bake): sintético
exato, GLB válido e texturizado, SHAs conferidos, UV medida independentemente
(4,32%, ~1 texel/face) explicando a fragmentação do Orc, limitações
registradas honestamente pelo executor, nenhuma falha silenciosa e nenhum
defeito de código que invalide os resultados. **Não aprova:** o T1 completo,
qualquer alegação de fidelidade de detalhe no Orc, o determinismo como
provado de forma independente (D3), nem o IoU sintético como evidência de
silhueta (D5). Próximo passo obrigatório antes do T1-completo: T5 (UV de
qualidade) + D2, D3 e D4. A palavra final de fidelidade artística é do
Mestre.
