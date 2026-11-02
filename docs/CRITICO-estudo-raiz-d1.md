# CRÍTICA SÊNIOR ADVERSARIAL — ESTUDO-RAIZ-D1-SOLUCOES.md

**Data:** 01/11/2026 · **Papel:** Crítico sênior adversarial (missão: tentar reprovar) · **Alvo:** `ESTUDO-RAIZ-D1-SOLUCOES.md` (398 linhas, ~68 KB)
**Método:** leitura integral do estudo; confronto com a evidência local do projeto (`ESTUDO_D1_FIDELIDADE.md`, `comparativo-blender/RESUMO.md`, `ESTUDO_T3_PAINT.md`, `VERIFICACAO-PESQUISA-TEXTURA.md`, relatórios do Crítico D2/D7 e do Crítico COR-08 e código em `hidden_files/cor08-*`); verificação web das afirmações externas decisivas (paper de Waechter et al., Text2Tex, Paint3D, SyncMVD, issue #139 do Hunyuan3D-2.1, instalação do PyTorch3D).
**Convenções:** S1 = bloqueador · S2 = maior · S3 = menor · S4 = observação. Nenhum defeito S1 foi encontrado: a espinha do plano (medir → conter vazamento/junção → forma → decisão gerativa) sobrevive. Os defeitos S2 abaixo, porém, são factuais e exigem correção antes de o estudo virar plano executado.

---

## 1. Defeitos

### C-01 (S2) — "H2 nunca foi medida neste projeto [fato]" é FALSO

- **Afirmação do estudo (§3.1):** "O que os números dizem: nada ainda — H2 nunca foi medida neste projeto [fato]. Os 49.750 tris do Orc Prata são contagem de faces, não auditoria."
- **Evidência contrária:** o relatório do Crítico da COR-08 (`hidden_files/cor08-critico/CRITICO-cor08-relatorio.md`, §3, item ii) executou parse próprio do GLB-âncora e mediu: **"Componentes 3D soldadas: 1 (49.750 faces, 23.768 vértices únicos soldados de 71.336)"**, concluindo que, com uma única componente e fontes diretas existentes, `faces_sem_fonte_alcancavel = 0` é forçado. Ou seja: a forma simples de H2 (componentes desconexos/cascas separadas) **já está refutada com prova na malha-âncora**, pelo protocolo correto (solda por posição antes de contar).
- **Agravante:** o D-H2.1 proposto pelo estudo (componentes via trimesh/Blender) nem sequer especifica a solda por posição — é uma versão mais fraca de uma auditoria já feita melhor. O que de fato continua aberto em H2 é apenas: autointerseção e faces internas (D-H2.2).
- **Correção exigida:** reescrever o status de H2 ("componentes: refutada na âncora, com prova; restam autointerseção e faces internas"); rebaixar D-H2.1 a confirmação de uma linha; recalibrar a "probabilidade prévia" de H2 e o texto da Fase 0.

### C-02 (S2) — "A auditoria de proveniência não foi refeita na era A3 [fato]" é FALSO — e descalibra R3.3

- **Afirmação do estudo (§4.1):** "A A3 trocou o mecanismo (UV → 3D), mas a auditoria de proveniência não foi refeita na era A3 [fato — é exatamente o D-H3.2]."
- **Evidência contrária:** o mesmo relatório do Crítico da COR-08 (§2 e §3) executou a **"Auditoria de proveniência v2"** sobre o bake da era A3, reproduzindo: direto 420.713/845.063 texels; **faces com fonte 24.590, preenchidas 25.160, sem fonte alcançável 0, anel médio 3,18, anel máximo 21**. A distância geodésica do preenchimento (em anéis) — metade do D-H3.2 proposto — **já está medida**. O limite honesto registrado pelo Crítico foi outro: sem intermediários salvos pelo bake (mapa texel-face), a verificação per-texel da fonte não foi refeita por fora; e o cruzamento **território da semente × território do texel** de fato não existe.
- **Consequência prática (a parte que morde):** R3.3 propõe "BFS com limite de anéis (ex.: 24–48 anéis)". Com máximo observado de **21 anéis** na âncora, um teto de 24 anéis **não muda nada**; o teto teria de ser ~8–12 para ter efeito, com custo de regiões chapadas muito maior que o sugerido. O estudo calibrou o remédio sem ler a medição que já existia. Sobram de pé, em R3.3, apenas as **barreiras territoriais** — que são o item que depende do cruzamento ainda não medido.
- **Correção exigida:** corrigir o "[fato]"; reduzir D-H3.2 ao que falta (cruzamento de territórios + salvar mapa de proveniência no bake, como o Crítico da COR-08 já recomendou); recalibrar ou remover o orçamento de anéis usando médio 3,18 / máx 21 como base.

### C-03 (S2) — A tabela de IoU antes/depois mistura réguas e atribui o ganho ao otimizador contra a decomposição do Crítico da COR-08

- **Afirmação do estudo (§1.1 e §2.1):** tabela "Antes da COR-08 → Depois" com frente 0,7929–0,7947 → 0,8177 e costas 0,7237–0,7241 → 0,7774; e o argumento causal "quando a função-objetivo é otimizada diretamente e o ganho é de ~0,03–0,05, o resíduo não é erro de otimização".
- **Evidência:** os valores "antes" vêm do `ESTUDO_D1_FIDELIDADE.md` (pipeline pré-COR-08). O Crítico da COR-08, reproduzindo o bake, mediu a baseline da própria tranche (bbox): **0,7941 / 0,7232 / 0,7925 / 0,7892**, com ganhos **+0,0236 / +0,0542 / +0,0140 / +0,0065** — e decompôs (§10 do relatório): "o ganho do otimizador sobre o inicial robusto é modesto (**frente 0,8070 → 0,8177; costas 0,7394 → 0,7774**): a maior parte do ganho sobre o v1 vem das caixas robustas + busca, não de um milagre afim". Ou seja: dentro da COR-08, o alinhamento que otimiza IoU contribuiu **+0,0107 na frente** (não ~+0,03), e o grosso veio de A0/busca. O estudo (i) usa a régua cruzada que ele próprio proíbe no §1.1 ("Não comparar entre réguas") e (ii) atribui à otimização de IoU um ganho que a fonte primária atribui a outra peça. O mesmo relatório do Crítico ainda registra a incoerência de citação **S3-COR08-3**: a faixa "0,7237–0,7929" citada para a âncora "não tem lastro naquele arquivo" — o estudo a repete sem a ressalva.
- **O que sobrevive:** o teto (~0,82) e a conclusão qualitativa. O que cai é a precisão quantitativa do argumento "otimizamos o objetivo e ele não se moveu" — ele se moveu pouco **em parte porque quem moveu foi outra alavanca**.
- **Correção exigida:** refazer a tabela com a decomposição do Crítico da COR-08 (baseline bbox × pós-otimizador, mesma régua) e reescrever o parágrafo causal com os números certos. Segundo caso do mesmo defeito: R1.2 compara "0,843 frontal de render (Blender) × 0,838 da Oficina" — números de render da era COR-05 — na mesma vizinhança argumentativa do 0,8177 da COR-08 (instrumento `projecao.iou` a 256 px), sem declarar que são instrumentos diferentes; um leitor pode concluir que a COR-08 **piorou** a frente (0,8177 < 0,838).

### C-04 (S2) — Vereditos do resumo têm status epistêmico acima do que os instrumentos permitem

- **Afirmações:** tabela do §0: H1 "**CONFIRMADA como causa primária estrutural**", confiança "**Alta**"; H4 "**Confirmada como mecanismo**". Ao mesmo tempo, §5.1 admite que a junção de vistas "**nunca foi medida diretamente**" e o plano inteiro se justifica por "instrumento antes de obra" (Fase 0) porque os testes decisivos (D-H1.x, D-H4.x) **ainda não existem**.
- **Problema 1 (H4):** um mecanismo não pode estar "confirmado" e "nunca medido" ao mesmo tempo. O status honesto é "mecanismo plausível com assinatura prevista, aguardando D-H4.1/D-H4.2" — que é o que o corpo do texto (§5.4) quase diz, mas a tabela do resumo, que é o que se lê e se cita, coroa a hipótese do Mestre antes da medição (risco de viés de confirmação institucionalizado: a hipótese "do dono" entra confirmada).
- **Problema 2 (H1):** o argumento "duas medições independentes travam no mesmo teto" é mais fraco do que parece: as duas rotas (Oficina e Blender) medem IoU de silhueta **contra as mesmas máscaras de referência** e com a mesma família de instrumento (silhueta a baixa resolução). Um artefato comum — ex.: a binarização das máscaras de uma arte com bordas suaves/pelo (ver C-07) — limitaria **as duas** identicamente, sem que isso prove divergência de geometria. Independência de implementação não é independência de instrumento. A conclusão "divergência real arte×malha" continua sendo a melhor explicação disponível (o comparativo do Blender e o D-H1.2 pendente a sustentam), mas "CONFIRMADA / confiança alta" é um degrau acima do lastro; o degrau correto é "forte indício convergente, decomposição pendente".
- **Correção exigida:** rebaixar os vereditos da tabela do §0 para o status que as próprias seções sustentam (H1: provável–forte; H4: plausível–não medida) e condicionar qualquer "confirmada" à Fase 0.

### C-05 (S2) — Omissão decisiva: ninguém audita se as 4 referências concordam ENTRE SI

- As vistas canônicas são imagens geradas e aprovadas pelo **olhar** (REF-01 julga cada vista contra o personagem), não por **consistência geométrica mútua**. Se o cinturão de crânios está numa altura na frente e noutra na lateral — inconsistência 2D entre as próprias referências —, então **nenhuma** malha e **nenhum** registro podem satisfazer as duas vistas: a discordância que D-H4.2 vai medir nascerá atribuída a H1/H4 quando a causa é a fonte.
- O estudo não propõe nenhum teste disso. O teste é barato e decisivo para a atribuição: auditoria 2D cruzada das referências (posições relativas de marcos — cinturão, ombreiras, crânio do cinto, bainha da saia — entre pares de vistas adjacentes, nas zonas de sobreposição). Sem ele, D-H4.2 mede discordância sem conseguir separar "registro errado" de "referências mutuamente impossíveis" — e a Fase 2 inteira pode estar perseguindo um fantasma parcial.
- **Correção exigida:** adicionar à Fase 0 um D-H0 (consistência cruzada das referências) anterior a D-H4.2, e explicitar no §6 que a cadeia causal admite um quinto elo a montante (a arte como conjunto, não só arte×malha).

### C-06 (S3) — Omissão: o deslocamento INTERNO da anatomia continua sem instrumento, e a Fase 4 só é julgada por silhueta

- O estudo admite (§2.1) que "IoU de silhueta não mede deslocamento interno" e lista isso como dúvida (c) — mas nenhum diagnóstico proposto o mede: D-H1.2 é diferença simétrica de silhuetas; D-H1.3 é perfil de largura de silhueta. Um teste barato existe e o projeto já tem as peças: erro de cor por caixas de região (método que os Críticos já usam — rosto/peito/pernas) e/ou distância entre marcos projetados e marcos da arte por vista.
- **Dano concreto:** a régua de promoção da Fase 4 (R1.4) é "IoU ≥0,88 **ou** ≥+0,05" medido no Blender — uma deformação pode "passar" em silhueta com a anatomia interna ainda errada (é o modo de falha clássico de otimizar contorno). Sem um medidor interno no aceite, a trava principal da rota mais arriscada do plano mede a coisa errada.
- **Correção exigida:** adicionar D-H1.4 (deslocamento interno por marcos/caixas) à Fase 0 e incluí-lo nas réguas das Fases 3–4.

### C-07 (S3) — Omissão: sensibilidade do instrumento de IoU (máscara, limiar, 256 px) nunca auditada; a régua 0,88 pode ser parcialmente artefato

- A arte tem pelo, capa e bordas suaves; a máscara binária a 256 px nasce de um limiar. Variar o limiar desloca a "silhueta da arte" e, com ela, o IoU de qualquer malha — inclusive o teto. Nenhum documento citado (nem o estudo) reporta a sensibilidade do IoU ao limiar da máscara. Se o teto variar ±0,03 com o limiar, parte da "divergência estrutural" de H1 é instrumento, e a régua global de 0,88 cobra um número que o instrumento não define com essa precisão.
- **Correção exigida:** D-H1.0 de custo ~zero: IoU da âncora sob 3 limiares de máscara (e, se possível, a 512 px), publicado junto de qualquer uso futuro do 0,88.

### C-08 (S3) — R1.4 ignora a fricção de plataforma: o PC é Windows e o PyTorch3D não tem instalação oficial simples nele

- O estudo trata a dependência como item genérico ("dependência PyTorch3D/nvdiffrast, perdas, guardas"). Fatos verificados no INSTALL.md oficial (facebookresearch/pytorch3d): a instalação CUDA via conda é "**on Linux only**"; wheels pré-compiladas oficiais são para Linux; no Windows o caminho é **compilar do fonte** com toolchain MSVC casada com a versão do PyTorch (a matriz oficial do INSTALL vai até PyTorch 2.4.1). Existem wheels **não oficiais** de terceiros para combinações específicas (torch 2.11/2.12 + CUDA 12.6/12.8) — ou seja, a rota não é inviável, mas o spike pode morrer na instalação ou ficar refém de uma combinação torch/CUDA diferente da do PC (CUDA 12.4 instalado pelo projeto).
- **Correção exigida:** a Fase 4 ganha um pré-check explícito e barato (instalação em venv isolado + tutorial de silhueta rodando) como porta de entrada do spike, com o resultado registrado antes de qualquer promessa sobre a rota; mencionar nvdiffrast (que tem suporte Windows melhor) como alternativa de renderizador.

### C-09 (S3) — R4.1: esforço "médio-alto" subestima a maior obra de engenharia do plano; o solver de graph-cut não é endereçado

- A receita completa (rotulagem MRF por face + nivelamento global + Poisson por arestas sobre a malha) é, na literatura, um **sistema** (o mvs-texturing é um projeto C++ dedicado). O estudo diz "resolvível por graph-cut ou, numa versão simples e determinística, por crescimento de regiões" — mas crescimento de regiões **não é** uma versão simples do mesmo algoritmo: sem o termo de suavidade global, a fronteira não é "empurrada para zonas de concordância" por otimização, e o comportamento é outro. E nenhum solver de graph-cut (gco/PyGCO etc.) é citado como disponível no ambiente Windows/Python do projeto — disponibilidade e licença (o gco clássico é restrito a pesquisa) ficam sem menção.
- **Correção exigida:** reclassificar o esforço de R4.1 como **alto**, fatiar a sub-entrega 1 em "rotulagem v0 (crescimento determinístico, julgado por D-H4.1)" e "rotulagem v1 (MRF, se v0 não bastar)", e registrar a decisão de solver com fonte.

### C-10 (S3) — A analogia do híbrido com o Paint3D está errada no ponto que importa

- **Afirmação (§7.3 e §5.3/R4.6 por tabela):** "a arquitetura coarse-to-fine do Paint3D (projeção primeiro, inpainting generativo consciente da forma depois) é exatamente esse híbrido".
- **Verificação (abstract oficial, CVPR 2024):** a etapa coarse do Paint3D **gera** imagens condicionadas por profundidade com um modelo de difusão e faz **fusão multivista** dessas imagens geradas — não projeta pixels de referência. O híbrido do projeto (projetar os pixels canônicos onde alcançam + inpainting generativo só no cego) é estruturalmente **análogo**, mas não é "exatamente" o Paint3D: a diferença é justamente a propriedade que o projeto mais valoriza (fidelidade de pixel na camada coarse).
- **Omissão acoplada:** o híbrido cria uma **nova junção** — a fronteira entre região projetada (com sombra embutida da arte, sem delight) e região gerada (iluminação tratada) — com estatísticas de cor diferentes dos dois lados. É um problema da mesma família de H4, transplantado, e o estudo não o nomeia nem propõe régua para ele.
- **Correção exigida:** corrigir a analogia ("análogo estrutural, com coarse de natureza distinta") e adicionar ao desenho do híbrido a régua de fronteira projetado×gerado (D-H4.1 cobre as classes de aresta — basta uma quarta classe).

### C-11 (S3) — Ordem das fases: a seleção de forma (barata, dados na Fase 0) deveria preceder a calibração das junções

- A Fase 2 calibra e mede tudo (D-H4.1 baseline, réguas de salto, R4.3 com trava em px) sobre a **forma-âncora atual**; a Fase 3 pode então trocar a âncora (R1.1), e o próprio estudo admite que "a pintura das Fases 1–2 deve ser re-provada sobre a forma vencedora". Re-provar é re-medir baselines e revalidar réguas — custo real, pago duas vezes. Como D-H1.1 já está na Fase 0, adotar a forma vencedora **antes** da Fase 2 (Fase 1.5) paga a troca uma vez só, e as junções já nascem calibradas sobre a forma definitiva. A justificativa implícita do estudo (não trocar a âncora no meio das correções de vazamento) vale para a Fase 1, não para a 2.
- **Correção exigida:** mover a adoção de R1.1 para entre as Fases 1 e 2 (mantendo a Fase 3 para a decisão de régua R1.6), ou justificar explicitamente o custo da dupla baseline.

### C-12 (S3) — D-H3.1: a definição de território torna as células frente↔flanco ambíguas

- Território é definido como "faces cuja normal aponta predominantemente para cada vista cardeal". Perto das diagonais (normais a ~45°), a classificação é uma faca: uma face de flanco classificada "frente" por margem mínima faz tinta legítima da frente contar como **diagonal** (esperado), e uma face de frente classificada "flanco" faz raspão contar como **fora da diagonal** (sangramento). A matriz pode, assim, simultaneamente esconder raspão e inflar sangramento conforme o limiar de dominância — e o estudo fixa a régua de decisão (≤2%) sem análise de sensibilidade ao critério de território.
- **Correção exigida:** definir território também por **ângulo de raspão** (faixas por cos θ em relação a cada eixo) ou reportar a matriz sob dois critérios; sem isso, D-H3.1 decide R3.1 com um instrumento enviesado justamente na região que ele quer medir.

### C-13 (S4) — Régua morta na Fase 2: "cobertura direta ≥35%" ao lado de "a COR-08 já mede 49,79%"

- O próprio estudo percebe a incoerência e pede re-baseline "no primeiro run desta fase" — mas deixa a régua de 35% escrita na tabela da fase. Régua já cumprida antes de a fase começar não é régua: ou sai da tabela, ou é substituída já pelo número re-baselado proposto (ex.: ≥49,79% sem regressão, na régua COR-08).

### C-14 (S4) — Custo de D-H1.1 ("< 10 min de GPU") ancorado só no motor rápido

- A âncora citada (mv-turbo ≤41,4 s, ≤6.435 MB) está correta e conferida no registro da Prova C (37,1–41,4 s; pico 6.435 MB). Mas a grade proposta é "2–3 motores × 3 seeds": motores da classe Hunyuan podem levar minutos por forma, e 6–9 formas podem estourar os 10 min. Declarar a estimativa por motor ou rotulá-la como otimista.

### C-15 (S4) — Higiene de fontes: a lista do §10 omite o documento que desmente C-01/C-02

- O §10 declara as fontes do projeto "lidas integralmente", mas **não lista** `CRITICO-cor08-relatorio.md` — o relatório que contém os números pós-COR-08 que o estudo cita (via REGISTRO/ESTADO, presumivelmente) e as duas auditorias que o estudo afirma não existirem (C-01/C-02). A omissão explica os dois defeitos S2 factuais: o estudo trabalhou sobre o resumo executivo da tranche, não sobre a auditoria dela. Correção: incluir o relatório na lista e revalidar contra ele qualquer afirmação marcada [fato] sobre a COR-08.

### C-16 (S4) — R1.6 (régua por região) é legítima no desenho, mas falta a trava anti-deriva

- A proposta é honesta **como desenhada**: nasce de D-H1.2, exige registro em DECISOES e a palavra do Mestre — não é rebaixamento disfarçado. Mas, para nunca virar um, falta a cláusula de **publicação dupla permanente**: o IoU global (com apêndices) continua reportado ao lado do IoU de corpo em todo run futuro, para que a régua nova não apague a antiga da memória do projeto.

### C-17 (S4) — Citações herdadas sem reverificação primária (registrar, não reprovar)

- TEXTure é citado via panorama secundário (deepwiki) — o próprio §10 o expõe; a descrição do trimapa está correta (partição em três estados keep/refine/generate), mas a cadeia de citação é fraca para um item que sustenta R4.5. Idem "Allène et al. aplicaram multibanda a atlas" e os detalhes de *Shadow Art Revisited* (arXiv:2107.14539): plausíveis, não verificados por mim na fonte primária nesta crítica. E o número do T2 (erro de rosto 28,38 → 17,10) não foi localizado por mim em relatório local de medição — apenas corrobados nas cartas de supervisão do projeto que o tratam como conferido; o estudo o usa como piso de comparação, uso de baixo risco.

---

## 2. O que foi verificado e está CORRETO (uma linha cada)

- **Correção do 93,49:** certa — relatório D2/D7, linha 45: "Tranche D2/D7, **Besta Cristalina, UV D-T5-1**"; `ESTUDO_D1_FIDELIDADE.md` §1.5 e tabela de réguas confirmam "(Besta)". É costura de UV, não junção de vistas. O estudo acertou onde a comunicação anterior ao Mestre errou.
- **Receita de Waechter et al. (ECCV 2014):** correta — conferida no paper: seleção de vista por face via MRF/graph-cut (estrutura de Lempitsky & Ivanov, termo de dados de Gal et al. + checagem de fotoconsistência), ajuste global de cor (valores por vértice, sistema global) e ajuste local por edição de Poisson em faixas. A atribuição em R3.1 (visibilidade como passo inicial) também confere.
- **Text2Tex (ICCV 2023):** correto — segmentação dinâmica em máscaras de geração que guiam inpainting ciente de profundidade, gerar/atualizar progressivo (abstract oficial).
- **Paint3D (CVPR 2024):** correto quanto a coarse-to-fine, fusão multivista e modelos UV Inpainting/UVHD, texturas 2K sem iluminação (abstract oficial) — a falha está só na analogia do híbrido (C-10).
- **SyncMVD:** correto — SIGGRAPH Asia 2024, difusão multivista sincronizada contra inconsistência entre vistas.
- **Hunyuan Paint 2.1 = 21 GB:** correto e é **VRAM** — o README oficial, citado literalmente na verificação primária do projeto: *"It takes 10 GB VRAM for shape generation, 21GB for texture generation and 29GB for shape and texture generation in total."*
- **Issue #139 (Hunyuan3D-2.1):** conferida na íntegra — inpainting 8.521,93 s = 99,5% de 8.564,20 s, um núcleo de CPU; o estudo a relata com a cautela devida ("relato único, de outra versão").
- **T3/2GP:** perfis mmgp 4/5 → ~6 GB, perfil 3 → 9 GB, issue #30 de OOM no fork e Windows ~+16 GB de RAM — tudo conforme `ESTUDO_T3_PAINT.md` e suas fontes.
- **UltraTex:** 10 vistas (6 canônicas + 4 guiadas a 45°), atlas até 8192², 15–18 min em RTX 5050 Laptop 8 GB com workflow 8K, código GPL-3.0 e base FLUX.2 Klein 9B não comercial — conforme as citações primárias do README em `VERIFICACAO-PESQUISA-TEXTURA.md`; o estudo rotula corretamente como alegação de fornecedor não medida.
- **Mecânica atual do pipeline:** visibilidade por centroide de face com BVH.ray_cast e corte `FACING_MIN = 0.05` — conferidos no código (`projecao.py`, `_blender_cor.py` em `hidden_files/cor08-a1/`). A reformulação de H3 (raspão + preenchimento) é, portanto, **dedução bem apoiada no código**, não especulação solta — embora §4.1 devesse citar o código em vez de apresentá-la como análise livre.
- **Números COR-08 (pós):** IoU 0,8177/0,7774/0,8065/0,7957 e cobertura 49,79% × 48,08% — reproduzidos identicamente pelo Crítico da COR-08. O defeito (C-03) está no "antes" e na atribuição, não no "depois".

## 3. O que NÃO consegui verificar (declarado, não chutado)

- Licença detalhada do FLUX.2 Klein 9B além do que o README do UltraTex declara (suficiente para o uso que o estudo faz, sob LIC-01).
- Composição exata de perdas de *Shadow Art Revisited* e a aplicação de multibanda por Allène et al. a atlas — plausíveis, sem leitura primária nesta crítica.
- O relatório de medição original do T2/C-COR01 (28,38 → 17,10) — corroborado apenas por documentos de supervisão.
- Disponibilidade de `scipy` e de solvers esparsos no ambiente do PC (afirmado em R4.1 sem evidência local acessível a mim).
- Se a máscara de referência usada no IoU tem sensibilidade relevante ao limiar — é justamente o teste que falta (C-07); não afirmo nem que sim, nem que não.

## 4. Vereditos separados

| Objeto | Veredito | Motivo em uma frase |
|---|---|---|
| (i) Análise causal (H1–H4 e a cadeia) | **APROVADO COM RESSALVAS** | A cadeia é a melhor explicação disponível e o corpo do texto é cuidadoso, mas a tabela-veredito coroa H1/H4 antes dos instrumentos, e dois "[fatos]" sobre H2/proveniência estão errados (C-01, C-02, C-04). |
| (ii) Diagnósticos D-* | **APROVADO COM RESSALVAS** | D-H3.1, D-H4.1 e D-H4.2 são os instrumentos certos; D-H2.1/D-H3.2 duplicam parcialmente o já medido, D-H3.1 tem viés de definição, e faltam três testes baratos e decisivos (C-05, C-06, C-07). |
| (iii) Rotas de solução | **APROVADO COM RESSALVAS** | A receita fotogramétrica está corretamente descrita e R3.2/R3.3 são rotas sensatas; mas R3.3 está descalibrada (C-02), R4.1 tem esforço subestimado e solver em aberto (C-09), R1.4 omite o risco Windows/PyTorch3D (C-08) e o híbrido é vendido com uma analogia errada (C-10). |
| (iv) Plano priorizado (Fases 0–5) | **APROVADO COM RESSALVAS** | A ordem geral (instrumento → contenção → forma → gerativas) é racional e as réguas são majoritariamente mensuráveis; exige a reordenação de R1.1 (C-11), a remoção da régua morta (C-13) e os testes novos da Fase 0 antes de executar. |
| **GERAL** | **APROVADO COM RESSALVAS** | Estudo utilizável como base do plano **depois** das correções S2 (C-01 a C-05). Sem elas, a Fase 0 gastaria esforço re-medindo o que já está provado, calibraria um remédio com o número errado e herdaria vereditos com confiança inflada. |

**Condição de promoção a APROVADO:** corrigir C-01–C-05 no texto (status de H2, proveniência, tabela de IoU decomposta, vereditos do §0, D-H0 de consistência das referências) e incorporar C-06/C-07 como diagnósticos da Fase 0. Nada disso pede nova pesquisa extensa — pede, sobretudo, ler o relatório do Crítico da COR-08 que o estudo não leu.
