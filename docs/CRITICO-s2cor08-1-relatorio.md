# Relatorio do Critico Senior — Tranche S2-COR08-1 (Etapa COR)

Dinamica adversarial APR-02. Missao: TENTAR REPROVAR. Nada aceito pela
palavra do executor; tudo abaixo foi re-medido a partir das fontes.

## VEREDITO

- **MECANISMO: APROVADO — 9,0/10.**
- **S2-COR08-1: DESDOBRADO** — salvamento FECHADO; pipeline linear ABERTA
  como pendencia nova (ver secao Escopo).
- **QUALIDADE VISUAL: sem alegacao nova nesta tranche; nao julgada.**
  As previas do bake novo sao pixel-identicas as da reproducao COR-08
  (100%, IDAT igual) — isso prova AUSENCIA DE MUDANCA visual, e NAO e
  aprovacao de qualidade visual. O visual 7,0/10 com ressalva da COR-08
  segue inalterado, sem melhora nem piora.

## Objeto verificado

Repo `app`, HEAD real `26b6a13` (a brief dizia `29ebaa9`; dois commits
entraram depois: `27704b1` COR-08 e `26b6a13` observacao do Mestre —
correcao de registro, sem impacto). Arvore suja com EXATAMENTE 2 arquivos,
conferida por `git status --short` antes e depois do meu trabalho:
`oficina3d/cor/_blender_cor.py` (+7 linhas) e `testes/test_cor.py`
(+40 linhas). Nenhuma edicao minha na arvore principal; nenhum commit,
push ou toque na copia `Oficina3D-codex`. Todo o meu trabalho vive em
`jobs_teste/s2cor08-critico/` (fora do repo). Tarefa agendada
`S2CriticoJob` criada, executada e REMOVIDA (verificado).

## O que o fix faz (conferido no codigo)

`_blender_cor.py:546` fixa
`bpy.context.scene.view_settings.view_transform = "Standard"` na linha
imediatamente anterior ao `img.save_render(...)` da linha 547, dentro de
`main()` (que e a ultima funcao do arquivo, logo o fatiamento do teste
cobre exatamente o corpo de `main()`). Nada entre as duas linhas, nenhum
retorno condicional entre elas, nenhuma outra atribuicao de
`view_transform` entre elas. `renderizar_previas` (linha 287) ja fixava
Standard por conta propria e roda DEPOIS do save — logo as previas nao
deveriam mudar (confirmado: 100% identicas, secao 4).

## 1. Re-medicao das alegacoes do executor — TODAS CONFIRMADAS

### 1a. Bake sintetico (cubo, cores puras), com o fix
- `textura.png` vs PNG embutido no GLB: **100% identicos, diff 0**
  (forma 256x256x4 nos dois).
- Cores puras exatas no arquivo: vermelho 8084, verde 11645,
  azul 10965, amarelo 15130 — iguais aos numeros do executor.
- SHAs: textura `ab261e44...`, GLB `accfd13f...` — iguais aos alegados.

### 1b. Reproducao COR-08 (Orc, 2048, otimizado, 3d), com o fix
- GLB novo: `a8e793b267db27c2a06669dbb925c91b8863a99ec4f43f558c880a1d10a09b9a`
  = ancora alegada, **byte-identico** (exportacao verbatim, nao tocada
  pelo fix).
- Textura nova: `e4056741...` != textura COR-08 `c7302ee1...` — diferente
  como previsto.
- Textura nova vs GLB novo: **100% identicos, diff 0** (2048x2048x4).
- Proveniencia das ancoras (verificacao nova N7): os SHAs `a8e793...` e
  `c7302ee1...` sao EXATAMENTE os arquivos de
  `jobs_teste/cor08-critico/cor08rep/` (a reproducao propria do Critico
  COR-08, citada no relatorio COR-08, secoes 2). As ancoras sao genuinas.

### 1c. Suite
- Re-execucao MINHA, independente: **343 testes, 28,26 s, OK
  (skipped=1)** — igual ao alegado (28,4 s).
- `test_cor.py` sozinho, por mim: **33 testes, 1,437 s, OK**.

## 2. Verificacoes NOVAS (alem da bateria da COR-08)

- **N1 — Controle negativo (pre-fix).** Copia do pacote com
  `_blender_cor.py` do HEAD (sem fix), bake sintetico pelo mesmo caminho
  de producao: BAKE_OK True, GLB SHA **identico** ao do bake com fix
  (`accfd13f...`, verbatim confirmado), textura SHA diferente
  (`d6fd36...`), textura vs GLB so **30,08% identicos, diff_max 110,
  diff_media 34,35**, e **ZERO pixels de cor pura** (vs milhares com o
  fix). Sem o fix a prova FALHA; com o fix PASSA. A prova discrimina.
- **N2 — Mutacao do teste de regressao.** 5 variantes, so
  `TestSaveRenderStandard` (2 testes): base OK; fix revertido FALHA;
  Standard movido para DEPOIS do save FALHA; Standard removido de `main`
  (mantido so em `renderizar_previas`) FALHA; AgX reinserido entre
  Standard e save FALHA. O teste nao e tautologico quanto a local, ordem
  e sobrescrita. (Primeira tentativa minha de variante "depois" estava
  mal construida — inseria ANTES do save — e a de "overwrite" nao casou
  o padrao; ambas refeitas por manipulacao de linhas e re-rodadas.)
- **N3 — Diff completo de `resultado_cor.json` (novo vs cor08rep).**
  Resultado: **diff VAZIO** apos normalizar caminhos e remover
  `tempo_s` e `sha256_textura` (que deve diferir). IoUs bake
  (0,8177 / 0,7774 / 0,8065 / 0,7957), cobertura direta 420713/845063
  (49,79%), cegos 424350, preenchimento_3d 424350, dilatacao restrita
  2709638, faces com fonte 24590 / preenchidas 25160 / sem fonte 0,
  anel medio 3,18 / max 21 — TUDO identico. So a textura.png mudou.
- **N4 — Previas (pixel + IDAT, nunca bytes brutos).** Novo vs cor08rep:
  4/4 vistas **100% identicas, diff 0, IDAT igual**. O fix nao tocou as
  previas, como previsto (elas ja usavam Standard).
- **N5 — Varredura do app inteiro por outros caminhos de salvamento.**
  Unico `save_render` do app: `_blender_cor.py:547`. Outros
  `view_transform = "Standard"`: `_blender_cor.py:287` (previas),
  `_blender_vertice.py:390`, `_blender_previa.py:175` — todos renders
  proprios, nao o caminho da textura. Unico `.save(` de imagem:
  `entrada/imagem.py:46` (PIL, sem view transform). Nenhum codigo le
  `textura.png` esperando valores AgX (nenhum `197`/`AgX` no codigo ou
  nos testes, fora o comentario/docstring do proprio fix); `passo.py`
  so verifica existencia do arquivo; `costura.py` opera sobre arrays em
  memoria, antes do save — o fix melhora a validade dessas metricas,
  nao as quebra.
- **N6 — Suite re-executada por mim** (secao 1c).
- **N7 — Proveniencia das ancoras** (secao 1b).
- **N8 — Curva AgX re-medida no par antigo (cor08rep).** Par antigo:
  15,554% identicos, diff_max 64, diff_media 4,18 (4 canais; media RGB
  = 5,58, igual aos 5,57 do relatorio COR-08). Media do R da textura
  por valor R do GLB (amostra 1/16): 0->0,00; 32->24,08; 64->56,86;
  128->126,71; 191->174,99; 255->197,04 — a curva da sonda COR-08
  (24/57/127/175/197). O arquivo antigo esta PROVADO como AgX.

## 3. Armadilha desarmada (comparacao inicial errada, explicada)

Minha primeira comparacao usou `jobs/20261101-101528-corint-orc-s7/cor/`
como "COR-08" e divergiu muito (textura 1024 vs 2048, texels_uv 211268
vs 845063, previas 66-69% identicas). Explicacao encontrada: aquele
diretorio guarda um bake ANTIGO a 1024 — o proprio codigo o chama de
baseline SUPERADA (`projecao.py:34` cita `textura ebd744a9...`, que e o
SHA que medi la). A baseline correta da COR-08 e `cor08rep/` (2048).
Contra ela, tudo fecha (secoes N3/N4). Registro: quem re-checar deve
usar `cor08rep/`, nao o diretorio do job.

## 4. Confronto da autoauditoria do executor — TODOS OS 4 ITENS PROCEDENTES

- (i) `main()` nao tem variavel `cena`: CONFIRMADO. O fix usa
  `bpy.context.scene` (linha 546); um fix ingenuo com `cena` daria
  NameError. A linha 287 usa `cena` porque `renderizar_previas` a tem
  como parametro — padrao diferente, sem confusao.
- (ii) Teste com `/` vs `\`: CONFIRMADO corrigido. Comparacao por
  objetos Path; `test_cor.py` 33/33 por mim; suite 343 OK por mim.
- (iii) Prova via Start-Process morta com a sessao SSH, relancada via
  tarefa pythonw: CONFIRMADO o padrao; usei o mesmo (tarefa criada,
  executada, removida).
- (iv) Driver errou os nomes das chaves: CONFIRMADO. O driver le
  `res2.get("iou_bake_256")` (topo) e `"texels_diretos"`; os nomes reais
  em `resultado_cor.json` sao `por_vista.<vista>.iou_bake_256` e
  `cobertura.texels_pintados_direto`. Por isso o `status.json` do
  executor traz `iou_bake_256: null` e cobertura null. NENHUMA alegacao
  de SHA/pixel dependia dessas chaves; a evidencia de metricas foi
  refeita por mim via diff direto dos JSONs (N3, diff vazio).

## 5. Defeitos encontrados

- **S3-1 — `status.json` do executor e internamente contraditorio.**
  O bloco `suite` nele diz `returncode=1, FAILED (failures=1)`, enquanto
  `suite_s2.log` (e a minha re-execucao) dizem 343 OK. Causa: o
  `status.json` guardou a corrida da suite ANTERIOR a correcao do Path
  e nao foi reescrito apos o re-run. Impacto zero no codigo; impacto
  real no registro: quem ler so o `status.json` conclui que a suite
  falhou. CORRIGIR ANTES DO COMMIT: regenerar o `status.json` (ou
  anotar a corrida superada) — nao commitar um artefato de prova que
  se contradiz.
- **S3-2 — Driver `prova_s2.py` com chaves erradas (item iv acima).**
  Se o driver for mantido como ferramenta de prova, corrigir os nomes
  (`por_vista.<vista>.iou_bake_256`,
  `cobertura.texels_pintados_direto`); senao, a secao de metricas do
  Orc dele continuara nula. Nao bloqueia o mecanismo.
- **S4-1 — Teste de regressao trava a GRAFIA, nao so a semantica.**
  Ele casa a string literal exata
  `bpy.context.scene.view_settings.view_transform = "Standard"`. Um fix
  semanticamente identico via variavel local `cena` (o padrao que o
  proprio `renderizar_previas` usa) FALHARIA no teste apesar de correto.
  Nao bloqueia; documentar a grafia travada ou afrouxar o casamento.
- **S4-2 — O teste 1 fatia de `def main():` ate o EOF.** Valido apenas
  enquanto `main()` for a ultima funcao do arquivo; uma funcao futura
  apos `main()` com `save_render` quebraria o teste (o teste 2 tambem
  a pegaria). Documentar ou fatiar ate a proxima `def` de nivel 0.
- **S4-3 (registro) — HEAD da brief divergente** (29ebaa9 vs 26b6a13
  real). Sem impacto; vale o arquivo/registro, nao a brief.

NENHUM defeito S1/S2 no fix, no teste ou no mecanismo. Nenhum defeito
encontrado no GLB, na textura nova, nas previas ou na suite.

## 6. Escopo — DECISAO EXIGIDA: DESDOBRADO

O S2 como ESCRITO no relatorio COR-08 e "caminho de salvamento + medias
em espaco sRGB" (titulo da secao 4 e itens 1-2 da cadeia: carga SEM
decodificacao sRGB + `cores_diretas_por_face` tirando MEDIA de bytes
sRGB). O fix desta tranche corrige SO o salvamento. O proprio relatorio
COR-08 prescreve como "correcao provada" exatamente o fix do salvamento
+ teste de regressao, e classifica o erro das medias como "parte do S2"
  mas "nao quantificado como bloqueador isolado".

Decisao: **DESDOBRADO, nao FECHADO integral.**
- **S2-salvamento: FECHADO.** A falsificacao do `textura.png` (branco
  255 -> 197) esta eliminada e provada (100% identico ao GLB, controle
  negativo discriminante, diff de resultado vazio).
- **S2-pipeline-linear: ABERTA como pendencia nova nomeada** (carga sem
  decode sRGB + medias em espaco sRGB). Ela afeta os VALORES pintados
  (erro pequeno para cores proximas, maior para alto contraste, ainda
  nao quantificado) — e, portanto, nenhuma publicacao pode dizer
  "fidelidade de cor resolvida" nem a D1 pode ser dada como fechada em
  fidelidade de cor ate essa pendencia ser quantificada ou decidida
  pelo Mestre. Fechar o S2 integral com o fix do salvamento seria
  enterrar a metade das medias em silencio.

## 7. O que precisa mudar (condicoes, nao reprovacao do mecanismo)

1. Regenerar/anotar o `status.json` do executor (S3-1) antes do commit.
2. Corrigir as chaves do driver `prova_s2.py` se ele for mantido (S3-2).
3. Registrar o desdobramento (S2-salvamento fechado; S2-pipeline-linear
   aberta como pendencia nova) no REGISTRO/ESTADO — a proxima execucao
   continua do arquivo.
4. Opcional (S4): documentar/afrouxar a grafia travada do teste.

## 8. Sem verificacao plena (registrado, nao inventado)

- A figura "15,5% identicos" do relatorio COR-08 foi re-medida como
  15,554% sobre a imagem inteira do par antigo (cor08rep) — o relatorio
  a descreve sobre texels UV; a coincidencia numerica e forte, mas a
  mascara UV exata nao foi reconstruida aqui, logo a identidade de
  dominio (imagem inteira vs texels UV) fica como ressalva, nao como
  divergencia.
- A qualidade visual das previas novas NAO foi julgada alem da
  identidade pixel com a COR-08 (que e o que esta tranche alega: nenhuma
  mudanca). Qualquer juizo de fidelidade visual contra as canonicas
  continua sendo o da COR-08 (7,0/10 com ressalva).
- Contagens da suite por arquivo nao foram re-extraidas (total 343
  conferido; a soma por modulo da COR-08 era 323, e o delta +20 inclui
  os 2 testes novos de `test_cor` e demais testes da tranche COR-08
  posterior ao relatorio — nao reconciliado modulo a modulo aqui).

## Artefatos deste Critico (todos em jobs_teste/s2cor08-critico/)

- `relatorio.md` (este arquivo)
- `critico_resultado.json` (medidas rodada 1: SHAs, comparacoes,
  sweep, posicao do fix)
- `critico_resultado2.json` (medidas rodada 2 vs cor08rep: ancoras,
  curva AgX, diff vazio de resultado, previas 100%)
- `critico_mutacao.json` (5 variantes: base OK, 4 falsas FALHAM)
- `critico_negativo.json` (controle pre-fix: 30,08%, diff_max 110,
  zero cores puras; GLB identico ao com fix)
- `critico_suite.json` (suite por mim: 343 OK, skipped=1, 28,26 s)
- `critico_job.done`, `sint-prefix/` (bake do controle negativo),
  `mut/` (copias das variantes)
- Scripts: `critico_medidas.py`, `critico_medidas2.py`,
  `critico_mutacao.py`, `critico_job.py`
