# ESTUDO RAIZ-D1 — Análise das hipóteses H1–H4 e rotas de solução para a fidelidade de cor

**Data:** 01/11/2026 · **Autor:** Muse (CM-000009), frente de pesquisa — **somente estudo** (nada foi executado no PC, nenhum job rodado, nenhum arquivo do projeto alterado).
**Escopo:** a pendência **D1** (fidelidade de cor/detalhe) da Oficina3D depois da tranche COR-08, organizada pelas quatro hipóteses do diagnóstico registrado no projeto: **H1** geometria × referência, **H2** duplicação na malha, **H3** sangramento de tinta entre vistas, **H4** junção das vistas (hipótese do Mestre).
**Relação com o estudo anterior:** este estudo **continua** o `ESTUDO_D1_FIDELIDADE.md` (01/11, pré-COR-08), que diagnosticou as causas C1–C6 e propôs as alavancas A1–A8. A COR-08 executou A0–A3 (caixa robusta, alinhamento otimizando IoU, bake 2048, preenchimento por adjacência 3D). Aqui eu **não recomeço do zero**: reorganizo o que restou pelas hipóteses H1–H4, acrescento o que a literatura e as medições novas trazem, e fecho com um plano priorizado único.
**Convenção de evidência:** afirmações sobre ferramentas/papers externos foram verificadas nas fontes citadas na seção 10 e marcadas **[Literatura]**; juízos e estimativas minhas estão marcados **[Análise]**. Números do projeto são os medidos e registrados (não inventei nenhum); quando um número vem de instrumento diferente, eu digo.

---

## 0. Resumo executivo

| Hipótese | Veredito provável [Análise] | Confiança | Teste que decide |
|---|---|---|---|
| **H1** — forma diverge da arte (IoU teto ~0,82) | **CONFIRMADA como causa primária estrutural.** Duas medições independentes (pipeline próprio e rota Blender) travam na mesma faixa de IoU; nenhuma melhoria de UV/alinhamento moveu o teto. | Alta | D-H1.1/D-H1.2 (decomposição do erro + variância entre seeds/motores) — para saber *onde* diverge e se seleção resolve |
| **H2** — duplicação/cascas dentro da malha | **Provavelmente menor ou parcial** (acessórios embutidos/intersectantes são comuns em malha gerada por IA), mas é a hipótese **mais barata de refutar** e, se confirmada, contamina H3/H4. | Baixa–média | D-H2.1/D-H2.2 (componentes + autointerseção) — custo de minutos |
| **H3** — tinta de uma vista pintando outra região | **Parcialmente confirmada, com reformulação:** com malha fechada + teste de visibilidade, a projeção direta "através do corpo" deve ser rara; o sangramento realista é (a) pintura de raspão (*grazing*) nas bordas de silhueta e (b) **propagação do preenchimento** que cruza territórios de vistas. | Média | D-H3.1 (matriz de ablação vista×região) + D-H3.2 (proveniência geodésica do preenchimento) |
| **H4** — junção das vistas duplica motivos | **Confirmada como mecanismo, com escopo a medir:** onde duas vistas disputam a mesma superfície com desalinhamento residual (H1), há dupla pintura; mas motivos repetidos **no meio das costas** (território de uma vista só) não se explicam só por H4 — ali pesam H1 (motivo projetado em anatomia errada, repetido a cada vista) e H3-preenchimento. | Média–alta | D-H4.1 (salto na fronteira de territórios 3D) + D-H4.2 (mapa de discordância de dupla pintura) |

**Tese central [Análise]:** as quatro hipóteses não são rivais — formam uma cadeia. **H1 é a raiz** (a pintura não casa com o corpo), **H4 é o amplificador visível** (nas junções, o erro de H1 aparece *duas vezes*, como dois orcs sobrepostos), **H3 é o vazamento** que espalha o erro para onde nenhuma vista alcança, e **H2 é o ruído de fundo** a excluir primeiro porque é barato. Por isso o plano (seção 8) ataca **na ordem: medir tudo (barato) → corrigir junções e vazamento dentro da rota atual (ganho certo, sem trocar de rota) → seleção/deformação de forma (ataca a raiz, com guarda-corpos) → decisão estratégica sobre as rotas gerativas T7/T3**, que dissolvem H1/H4 por construção ao custo de abandonar a fidelidade pixel a pixel à arte canônica — decisão que é do Mestre, não técnica.

---

## 1. Base factual pós-COR-08 (o que mudou e o que não mudou)

### 1.1 Números atuais (tranche COR-08, bake 2048, Orc Prata 49.750 tris)

| Métrica | Antes da COR-08 | Depois da COR-08 | Leitura |
|---|---|---|---|
| IoU frente | 0,7929–0,7947 | **0,8177** | subiu, longe da régua 0,88 |
| IoU costas | 0,7237–0,7241 | **0,7774** | maior ganho, pior vista continua sendo costas |
| IoU esquerda | 0,7885–0,793 | **0,8065** | idem |
| IoU direita | 0,7827–0,7872 | **0,7957** | idem |
| Cobertura direta | 48,08% (baseline mesma régua) | **49,79%** | +1,7 p.p. — alinhamento melhor devolveu poucos texels |
| Determinismo | provado | 3 bakes, SHAs idênticos | mantido |

⚠️ **Armadilha de leitura (já registrada no estudo anterior):** a cobertura de ~19–20% das tranches T1/T5/COR-05 foi medida a 1024 px com outro instrumento; os 49,79% são a 2048 px na régua da COR-08. **Não comparar entre réguas.** O fato robusto, válido nas duas réguas, é o mesmo: UV/resolução **não** são o gargalo; e mesmo com alinhamento otimizado (A1) o IoU não passa de ~0,82.

### 1.2 O que a rota Blender ensinou (comparativo de 01/11, mesmo Orc, mesmas vistas)

- Pintura por projeção em perspectiva com **blending ponderado (facing^1,5 × alfa × frustum × visibilidade por raycast) e SEM dilatação agressiva**: cobertura direta 63,43% (régua própria, a 1024), erro médio de cor frontal 42,8 × 47,8 da Oficina da época, etapa de cor em 4,4 s × 61,26 s.
- Resultado visual: base contínua e coerente ("aguada", sem detalhe fino), **sem confete** — mas **o mesmo teto de IoU (0,843 na frente)** e o mesmo rosto ilegível.
- **Lição dupla:** (1) o *como* misturar/preencher muda muito o aspecto (ganho real e barato — ataca H3/H4); (2) **nenhuma implementação de projeção rompe o teto imposto pelo desregistro arte×malha** (H1 é teto de todas as rotas de projeção).

### 1.3 Estado das rotas vizinhas (para o plano não duplicar frentes)

- **T2 (cor de vértice):** rede de segurança funcional; erro médio do rosto caiu de 28,38 → **17,10** após a correção sRGB×linear achada pelo Codex (C-COR01). Serve de piso de comparação por região e de *fallback*, não de solução de textura.
- **T3 (Hunyuan Paint):** estudo próprio (`ESTUDO_T3_PAINT.md`, verificado) — o spike realista nesta máquina é o **Paint 2.0 via fork 2GP** (perfis 4/5 do mmgp orçam ~6 GB de VRAM, sem garantia — há relato público de OOM mesmo no fork); o **Paint 2.1 oficial pede 21 GB de VRAM para textura** [Literatura: README oficial, ver seção 7] — fora do orçamento de 8 GB sem fork. E o Paint **sintetiza** a textura a partir de **uma** imagem: não usa as 4 vistas canônicas nem pinta os pixels da arte.
- **T7 (UltraTex):** verificação própria (`VERIFICACAO-PESQUISA-TEXTURA.md`) — workflow ComfyUI (FLUX.2 Klein 9B) que pinta a malha de **10 câmeras** e assa atlas até 8192²; aceita as vistas do projeto como **guias de cor** (o modelo *gera* cada vista a partir delas — não é projeção de pixels). O README **afirma** 15–18 min/modelo em GPU de 8 GB — **alegação do fornecedor, ainda não medida pelo projeto**; pesos já baixados e guardados no Drive, spike com réguas pré-registradas aguardando. Licença: código do projeto em GPL-3.0; o modelo-base FLUX.2 tem licença própria não comercial (fato registrado conforme LIC-01 — não bloqueia o spike).
- **REF-01 (arte):** as diagonais do Orc estão em produção pela frente de referências (lote 4) — a rota A6 (vistas diagonais) depende dessa arte aprovada, não de código.

### 1.4 O sintoma do Mestre, traduzido em mecanismos candidatos

"Parece que tem vários orcs um em cima do outro" — motivos (crânios do cinturão, pano vermelho, blocos de pelo) repetidos/sobrepostos, sobretudo nas costas. Tradução técnica [Análise] — três mecanismos produzem *exatamente* esse sintoma, e os testes diagnósticos das seções 2–5 os separam:

1. **Motivo certo, anatomia errada, 4 vezes (H1):** cada vista projeta os seus motivos sobre uma malha cuja anatomia está deslocada em relação àquela vista; o mesmo cinturão de crânios aparece pintado a partir de frente, laterais e costas, cada um numa altura/lugar ligeiramente diferente — no render final, o olho lê "vários cinturões/orcs".
2. **Dupla pintura na faixa de disputa (H4):** perto das bordas entre territórios (ombros, flancos), duas vistas pintam a mesma pele com registros diferentes e a mistura/winner-take-all alterna entre elas — motivo duplicado com deslocamento pequeno, o "fantasma" clássico.
3. **Preenchimento que importa motivo (H3):** regiões cegas recebem, por propagação, cor cuja fonte 3D está longe — um bloco de pelo ou de pano "viaja" para onde não pertence.

---

## 2. H1 — Geometria × referência (a raiz)

### 2.1 Análise da causa

A evidência acumulada é forte e convergente:

- O IoU ficou em **0,72–0,79** em três configurações de UV (T1, T5, COR-05) e subiu só para **0,78–0,82** quando o alinhamento passou a *otimizar* o próprio IoU (A1/COR-08). Quando a função-objetivo é otimizada diretamente e o ganho é de ~0,03–0,05, o resíduo **não é erro de otimização — é divergência real** entre a silhueta da malha e a silhueta da ilustração [Análise].
- A rota Blender, com câmeras em perspectiva ajustadas iterativamente (implementação independente), mediu a **mesma faixa** (caixas 0,65–0,80; render frontal 0,843). Dois métodos, um teto: é propriedade do par (arte × malha), não do código.
- A causa é conhecida e registrada desde o estudo anterior (C1): a arte é uma ilustração com proporções expressivas (cabeça grande, capa de lobo volumosa, machado em pose) e a malha é a *interpretação* de um motor gerativo a partir de uma imagem — os dois divergem em pose e proporção por construção. Nenhuma afinidade 2D corrige divergência 3D.
- Nuance importante: **parte do erro de IoU pode ser "inocente"** — apêndices que a malha nem possui em relevo (padrões pintados na arte) ou que estão em pose diferente (o machado). Se o erro se concentrar nos apêndices, o *corpo* pode estar melhor casado do que o número global sugere — e a régua de 0,88 global seria injusta. É o que D-H1.2 mede.

**O que ainda é dúvida:** (a) a decomposição do erro (onde, e de que tipo: escala global? proporção cabeça/corpo? apêndices?); (b) se a divergência varia muito entre seeds/motores (se variar, *seleção* é uma rota real; se for estável ~0,80 em tudo, é sistemática da ilustração); (c) quanto do erro interno (anatomia dentro da silhueta) acompanha o erro de contorno — IoU de silhueta não mede deslocamento interno.

### 2.2 Diagnóstico (barato, decisivo)

**D-H1.1 — Variância de IoU entre motores × seeds.** Gerar a forma do Orc em grade pequena (ex.: 2–3 motores × 3 seeds; a forma do mv-turbo levou ≤41,4 s e ≤6.435 MB na bateria dourada — custo total estimado < 10 min de GPU) e medir o IoU das 4 vistas de cada forma contra as máscaras canônicas (mesma função `iou` a 256 px). *Decide:* se o melhor caso ≥0,86, seleção (R1.1) entra no plano como ganha-pão; se todos clusterizam em 0,78–0,83, seleção é cosmética e a raiz é sistemática.

**D-H1.2 — Decomposição do descasamento.** Para a forma-âncora (seed 7), por vista: mapa da diferença simétrica das silhuetas (arte∖malha × malha∖arte) e sua distribuição por faixas do corpo (cabeça/tronco/pernas) e por apêndices (machado, capa/lobo, saia). Custo: numpy sobre máscaras que o pipeline já rasteriza. *Decide:* erro concentrado em apêndices → a régua global deve virar régua por região (corpo × apêndices) e o ataque é local; erro difuso/proporcional → deformação (R1.4) ou rota gerativa (seção 7).

**D-H1.3 — Perfis de largura × altura.** Extrair, por vista frontal, o perfil de largura da silhueta ao longo da altura (arte × malha normalizadas) — é o dado de entrada do warp por marcos (R1.5/A8 do estudo anterior) e quantifica a divergência de proporção (ex.: cabeça da arte X% mais larga que a da malha na mesma altura relativa). Custo: minutos. *Decide* a viabilidade de R1.5 e calibra expectativas de R1.4.

### 2.3 Rotas de solução

**R1.1 — Seleção de forma por IoU (escolher a forma que casa com a pintura).**
- *O que é:* gerar N formas (motores × seeds), pontuar cada uma por IoU médio/mínimo das 4 vistas e **só pintar a vencedora**; desempate por inspeção visual da forma (a forma também é produto — o Mestre aprovou o Orc Lendário pelo olho).
- *Encaixe:* trivial no pipeline (a etapa forma já é separada da etapa cor; o IoU já é calculado no bake — antecipar o cálculo para a forma crua).
- *Esforço:* baixo (1 tranche: script de varredura + relatório). *Ganho esperado:* **desconhecido até D-H1.1** — se a variância for a típica de motores gerativos, plausível +0,02–0,05 de IoU [Análise, sem base medida — declarar como hipótese]. Mesmo sem bater 0,88, cada ponto de IoU devolve texels diretos e reduz motivo-em-lugar-errado.
- *Riscos:* otimizar IoU pode escolher forma visualmente pior (mais "certinha", menos caráter) — mitigar com veto visual do Crítico sobre a forma plana (renders flat das 3 finalistas) antes de pintar; e registrar que a seleção é por sujeito (cada criatura terá sua varredura).
- *Verificação:* tabela de IoU da grade + IoU da vencedora vs âncora (0,8177/0,7774/0,8065/0,7957); régua de adoção: vencedora ≥ âncora +0,03 no IoU mínimo das vistas, sem reprovação visual da forma.

**R1.2 — Modelo de câmera mais rico na projeção (perspectiva + refinamento fotométrico).**
- *O que é:* trocar a projeção ortográfica+afim por câmeras em perspectiva calibradas (como a rota Blender fez: 32°, ajuste iterativo) e, sobre o alinhamento por silhueta, um refinamento que também minimize diferença fotométrica nas zonas de alta confiança (interior da silhueta, facing alto) — alinhar *conteúdo*, não só contorno.
- *Encaixe:* médio — a rota Blender já provou o desenho dentro de casa (script `pintar_blender.py` existe e roda em 4,4 s); portar a calibração para a etapa cor ou adotar o bake via Blender como motor da etapa (decisão de arquitetura registrada na época: lição favorável ao blending do Blender).
- *Ganho esperado:* pequeno em IoU (a rota Blender: 0,843 frontal de render vs 0,838 da Oficina — mesma ordem) [medido]; o ganho real desta rota não é IoU, é **qualidade de mistura** (ver H4). Não vender como solução de H1.
- *Riscos:* perspectiva introduz distorção de escala com a profundidade; em personagens "chatos" (pouca profundidade) o ganho some. *Verificação:* IoU + erro de cor por região na mesma régua do comparativo.

**R1.3 — Warp de pintura por marcos anatômicos (ex-A8).**
- *O que é:* alinhamento não-linear por vista: casar os perfis de largura (D-H1.3) por programação dinâmica e deformar o mapeamento vertical/horizontalmente, para que cabeça pinte na cabeça mesmo com proporções diferentes.
- *Encaixe:* fica dentro de `projecao.py`, depois do alinhamento afim. *Esforço:* alto. *Ganho:* potencialmente o maior *dentro* da projeção (ataca a divergência de proporção, que a afinidade não alcança) [Análise].
- *Riscos:* **altos** — deformações patológicas em sujeitos não-humanoides (a Besta não tem "cabeça/tronco/pernas" comparáveis); complexidade de teste grande; pode virar uma solução só-para-orcs. *Verificação:* IoU + caixas de região (método do Crítico) em **Orc e Besta**; se não generalizar, não adota.
- *Posição:* contingência — só se D-H1.2 mostrar divergência proporcional dominante **e** R1.1+R1.4 não resolverem.

**R1.4 — Deformação suave da forma guiada pelas 4 silhuetas (renderização diferenciável).**
- *O que é:* otimizar uma deformação 3D suave da malha (deslocamentos por vértice com regularização laplaciana e de consistência de normais, ou gaiola de controle de baixa resolução) minimizando a perda de silhueta suave nas 4 vistas canônicas. É a técnica dos tutoriais oficiais do **PyTorch3D** ("Fit a mesh via rendering": renderização diferenciável de silhueta e de textura para ajustar malha a imagens-alvo) [Literatura: pytorch3d.org/tutorials/fit_textured_mesh] e usada na literatura com perdas de silhueta + laplaciana + arestas (ex.: *Shadow Art Revisited*, arXiv:2107.14539). Como é 3D e multivista, a deformação é **consistente entre vistas por construção** — diferente de qualquer warp 2D.
- *Encaixe:* etapa nova **opcional** entre forma e cor ("forma ajustada para pintura"), executada numa malha-proxy decimada (~10–15 mil tris) com transferência da deformação para a malha cheia; renderização suave a 256² em 8 GB é folgada. Blender continua sendo o juiz final (renders e IoU medidos nele, não no otimizador).
- *Esforço:* alto (spike próprio: dependência PyTorch3D/nvdiffrast, perdas, guardas). *Ganho esperado:* é a única rota de projeção que pode **mover o teto** em vez de aproximar-se dele — plausível levar vistas de 0,80 → 0,86–0,90 **se** a divergência for de proporções suaves [Análise — hipótese a provar no spike, com D-H1.2 como pré-condição].
- *Riscos:* **sérios e de produto** — (1) deforma a forma que o Mestre aprovou pelo olho: a variante deformada precisa de aprovação visual própria (fotos flat + sombreadas), e o padrão deve ser **desligado** até provar valor; (2) silhueta é ambígua em profundidade — 4 vistas ortogonais + regularização mitigam, mas vistas diagonais de conferência (renders 45°) são obrigatórias no aceite; (3) pode "esticar" apêndices de forma estranha — limitar amplitude máxima de deslocamento (ex.: ≤3% da altura) como trava.
- *Verificação:* IoU pós-deformação medido no Blender (não no otimizador) ≥0,88 nas 4 vistas **ou** ganho ≥+0,05 com variação de volume ≤ régua a definir; Critic visual da forma (mecanismo × visual separados, L-33); determinismo por seed fixa.

**R1.5 — Inverter a dependência: vistas geradas a partir da forma (rota gerativa).**
- *O que é:* em vez de forçar a ilustração sobre a malha, gerar as vistas **da** malha (T7/T3): as vistas nascem registradas com a geometria, e H1 deixa de existir como erro de registro (vira, no máximo, divergência de *estilo* em relação à arte). Desenvolvida na seção 7 — é a bifurcação estratégica do projeto, não um item de H1.

**R1.6 — Aceitar e delimitar (régua por região).**
- *O que é:* se D-H1.2 mostrar que o descasamento mora nos apêndices/pose do machado, redefinir a régua da D1: IoU de **corpo** (sem apêndices) ≥0,88 + tratamento separado para apêndices (ex.: machado e capa pintados com alinhamento próprio, por parte). [Análise] É honestidade de régua, não maquiagem: a régua global atual mistura duas coisas diferentes e pode estar bloqueando um "bom o bastante" no corpo enquanto cobra o impossível no machado.
- *Verificação:* D-H1.2 entrega os dois números; a decisão de régua é registrada em DECISOES com a palavra final do Mestre.

### 2.4 Síntese H1

Confirmada e estrutural. Dentro da projeção, a ordem racional é **R1.1 (seleção — barata, ganho certo ainda que modesto) → R1.4 (deformação — cara, única que move o teto, com guarda-corpos) → R1.3 (warp — só se o diagnóstico mandar)**, sempre com **R1.6** como decisão de régua informada por D-H1.2. R1.2 não é rota de H1 (é rota de mistura, H4). E R1.5 muda o jogo inteiro (seção 7).

---

## 3. H2 — Duplicação na malha ("vários orcs" literal)

### 3.1 Análise da causa

Motores gerativos de forma (Hunyuan/TripoSG-like) produzem malhas por ocupação/marching-cubes ou por deformação; defeitos típicos [Análise, prática conhecida da área]: **componentes desconexos** pequenos (detritos), **partes intersectantes** (a cabeça de lobo da capa atravessando o ombro, crânios do cinturão como sólidos embutidos no tronco), **faces internas** (superfícies dentro do volume, invisíveis mas presentes) e, mais raro, **cascas duplicadas** quase coincidentes. Nenhum desses defeitos aparece em render comum — mas todos contaminam a pintura: faces internas roubam UV e votos de visibilidade; interseções criam bordas onde a projeção "pula" de uma superfície para outra (sintoma que imita H4); cascas duplicadas com *z-fighting* produzem textura tremida/duplicada **literalmente** — o sintoma que o Mestre descreveu, na forma mais literal possível.

**O que os números dizem:** nada ainda — **H2 nunca foi medida neste projeto** [fato]. Os 49.750 tris do Orc Prata são contagem de faces, não auditoria. A probabilidade prévia [Análise] é de H2 ser **contribuinte menor** (o grosso do sintoma tem explicação melhor em H1/H4/H3), mas o custo de medir é tão baixo (minutos, CPU) que ela deve ser a **primeira** a sair da frente: enquanto não for refutada, qualquer conclusão sobre H3/H4 fica sob suspeita.

### 3.2 Diagnóstico

**D-H2.1 — Componentes conexos.** Carregar o GLB da forma-âncora (trimesh ou Blender `Separate > By Loose Parts` em cópia) e listar: nº de componentes, faces/área/volume de cada um, e a fração dos 10 maiores fora do componente principal. *Refuta a forma simples de H2 se:* 1 componente dominante + detritos < 0,1% da área. *Confirma parcialmente se:* há componentes grandes secundários (ex.: capa/machado como sólidos separados intersectando o corpo — o que é normal em kit de personagem e muda o tratamento, ver R2.3).

**D-H2.2 — Autointerseção e faces internas.** (a) Contagem de arestas não-manifold e de fronteira (bmesh: `is_manifold`, `is_boundary` — diagnóstico padrão de limpeza de malha); (b) teste de autointerseção (trimesh collision / 3D Print Toolbox do Blender); (c) faces internas: para uma amostra de faces, raycast nos dois sentidos da normal — face cuja vizinhança está "dentro" dos dois lados é interna. *Decide:* interseções extensas casco×casco → R2.4 (voxel remesh) entra em cogitação; interseções só em acessórios → R2.3 (tratamento por parte); zero → H2 arquivada com prova.

### 3.3 Rotas de solução

**R2.1 — Limpeza cirúrgica (detritos e duplicados).** Remover componentes-detrito (área abaixo de limiar), *merge by distance*, recalcular normais, remover faces degeneradas/duplicadas exatas. Ferramentas: bmesh no Blender headless ou trimesh — operações padrão de limpeza [Literatura/prática: Blender Mesh Clean Up; diagnósticos `is_manifold`/`is_boundary` via bmesh]. *Esforço:* baixo (meia tranche, com antes/depois contados). *Ganho:* higiene — elimina ruído de UV/visibilidade; **não** promete ganho visual sozinha. *Verificação:* contadores D-H2 zerados ou reduzidos a lista nomeada; IoU e cobertura **não podem regredir**; determinismo mantido.

**R2.2 — Remoção de faces internas.** Apagar faces classificadas internas por D-H2.2(c). *Ganho:* devolve orçamento de UV e elimina votos fantasmas de visibilidade [Análise]. *Risco:* classificador agressivo apaga superfície real em concavidades (axila, entrepernas) — exigir margem: só apagar face interna com confirmação de oclusão total em N direções amostradas. *Verificação:* renders flat das 4 vistas antes/depois pixel-idênticos fora das regiões internas (diferença ~0 nas silhuetas); cobertura direta não regride.

**R2.3 — Pintura por partes (componentes com registro próprio).** Se D-H2.1 mostrar kit em sólidos separados (machado, capa, crânios), tratar cada componente grande como **sub-sujeito** na projeção: alinhamento e territórios por componente (o machado não precisa casar com a silhueta do corpo — precisa casar com o machado da arte). Sinergia direta com R1.6 (régua por região). *Esforço:* médio. *Ganho:* ataca o descasamento onde ele é pior (apêndices) sem deformar nada. *Riscos:* costuras entre partes viram o novo problema (mitigado pelas rotas de H4 aplicadas por parte). *Verificação:* IoU por componente + erro de cor por região (machado/capa entram nas caixas do Crítico).

**R2.4 — Voxel remesh (a "fusão" radical).** Remesh volumétrico (Blender Remesh VOXEL / OpenVDB) funde tudo numa casca única manifold: some qualquer duplicação/interseção interna por construção. *Esforço:* baixo de executar, **alto de consequências**: destrói UV (reparametriza — ok, a UV já é xatlas refeita), suaviza detalhe conforme o tamanho do voxel, e **muda a silhueta** (medir IoU antes/depois: voxel grande demais derruba justamente a métrica de H1). *Posição [Análise]:* último recurso, só se D-H2.2 provar duplicação casco×casco extensa; com voxel ≤ 1/300 da altura e régua "IoU não pode cair > 0,005".

### 3.4 Síntese H2

Medir primeiro (D-H2, custo ~zero), limpar o que for sujeira (R2.1/R2.2), tratar kit como partes se ele existir como partes (R2.3), e guardar o voxel remesh (R2.4) como artilharia improvável. H2 provavelmente **não** é a raiz do "vários orcs" — mas é a única hipótese que pode ser *encerrada com prova* numa tarde, e encerrá-la limpa o terreno para H3/H4.

---

## 4. H3 — Sangramento de tinta entre vistas

### 4.1 Análise da causa (com uma reformulação importante)

"Sangramento" cobre três fenômenos diferentes, e separá-los muda o remédio:

1. **Projeção através do corpo (o sentido literal de H3):** a vista da frente pintar as costas porque a projeção ignora o que está no caminho. No pipeline atual, a visibilidade é testada por **centroide da face (BVH)** — uma face das costas não é visível da frente, então a projeção direta através do corpo deve ser **rara ou nula** numa malha fechada [Análise]. Onde ela pode ocorrer: (a) malha com furos/cascas abertas (→ H2) deixando raios passarem; (b) faces grandes cujo centroide é visível de uma vista mas cujos texels periféricos estão atrás de outra parte do corpo (erro de granularidade do teste — a face do ombro "vê" a frente pelo centroide e pinta texels que na verdade pertencem à lateral oclusa); (c) câmeras em perspectiva × ortográfica desalinhadas.
2. **Pintura de raspão (*grazing*):** perto do contorno de cada vista, a superfície está quase paralela à direção de projeção; um pequeno erro de registro (H1) vira um deslocamento grande na superfície, e a tinta "escorre" para a lateral errada — o cinturão da frente aparecendo no flanco, a cor das costas vazando para o ombro. O corte atual de *facing* (> 0,05) é uma faca: aceita raspões quase tangentes.
3. **Propagação do preenchimento (o maior suspeito [Análise]):** com ~50% de cobertura direta pós-COR-08, metade da superfície é preenchida. O preenchimento A3 propaga por **adjacência 3D em anéis (BFS)** a partir das faces diretas — topologicamente correto, mas **cego a territórios**: um anel que parte de uma semente da frente pode, depois de muitos anéis, terminar pintando uma região cega das costas se as sementes das costas forem localmente esparsas (interior da capa, entre as pernas, sob a saia). Cor "de outra parte do corpo" sem nenhuma projeção envolvida — o sintoma é idêntico ao de H3 literal, o remédio é outro.

**Evidência existente:** a auditoria de proveniência do Crítico T1 já rastreou, na era da dilatação UV, cor importada de regiões estranhas (mancha branca do antebraço vinda de ilhas de pelo). A A3 trocou o mecanismo (UV → 3D), mas **a auditoria de proveniência não foi refeita na era A3** [fato — é exatamente o D-H3.2]. A ablação registrada no D2/D7 (desligar a vista de costas degrada só as costas) indica que a projeção direta é local — evidência **contra** H3 literal forte e **a favor** da reformulação acima.

### 4.2 Diagnóstico

**D-H3.1 — Matriz de sangramento vista × região.** Usar a infraestrutura de ablação que já existe (D2/D7): assar 4 vezes, cada vez com **uma única vista ativa**, e medir, por bake, quantos texels **diretos** caem em cada território (território = conjunto de faces cuja normal aponta predominantemente para cada vista cardeal). Matriz 4×4; a diagonal é o esperado; **fora da diagonal mede o sangramento direto** (através do corpo + raspão). Custo: 4 bakes (~minutos cada a 2048; pode rodar a 1024 para o diagnóstico, declarando a régua). *Decide:* fora-diagonal ≤ ~2% → H3 literal arquivada; células altas frente→flancos → raspão (R3.2); frente→costas relevante → furo/geometria (volta para H2) ou granularidade do teste (R3.1).

**D-H3.2 — Proveniência geodésica do preenchimento.** Na auditoria de proveniência v2 (já desenhada no estudo anterior para a A3): para cada texel preenchido, registrar a **distância geodésica** (em anéis de faces) até a semente e o **território da semente** vs o território do texel. *Decide:* se ≥95% do preenchimento é do mesmo território ou vizinho com distância curta, H3-preenchimento está sob controle; caudas longas cruzando territórios confirmam o vazamento e calibram R3.3 (limite de anéis/barreiras).

### 4.3 Rotas de solução

**R3.1 — Visibilidade por texel (profundidade), não por centroide.**
- *O que é:* para cada câmera de pintura, renderizar uma vez o **mapa de profundidade** da malha (z-buffer no Blender, na resolução do bake); um texel só aceita tinta de uma vista se a profundidade projetada dele casar com o z-buffer (com viés pequeno). É o teste padrão de projeção com oclusão em pipelines de texturização fotogramétrica [Literatura: Waechter et al. 2014 fazem seleção de vista por face com testes de visibilidade; a rota Blender do projeto já usa raycast BVH por face — R3.1 refina a granularidade de face para texel].
- *Encaixe:* a etapa cor já roda Blender headless para o bake na rota comparativa; o z-buffer por vista é um render a mais por vista (segundos). Na rota Python pura, a alternativa é raycast por amostra de texel via BVH — mais cara (16,7 M de raios a 2048² × 4 vistas é excessivo; amostrar por face×texels representativos reduz a custo aceitável).
- *Ganho esperado:* elimina a classe (b) de vazamento (texel periférico de face "visível") e qualquer através-do-corpo residual. *Não* resolve raspão nem preenchimento. [Análise] Ganho provavelmente **pequeno mas real** — D-H3.1 diz quanto.
- *Riscos:* viés de profundidade mal calibrado cria furos de tinta nas bordas (mitigar com viés proporcional à escala e teste A/B na matriz D-H3.1). *Verificação:* matriz D-H3.1 fora-diagonal → ≤2% **sem** perda de cobertura direta > 0,5 p.p.

**R3.2 — Pesos suaves de ângulo + autoridade territorial.**
- *O que é:* substituir o corte duro de facing por **peso contínuo** w = cos^p(θ) (p ≈ 2–4, calibrável) na mistura entre vistas, e impor **autoridade territorial**: fora do seu território (normal dentro de ±~55° do eixo da vista), uma vista **não pinta direto** — sua tinta só entra via mistura ponderada na faixa de fronteira (que é o assunto de H4) ou não entra. Raspão tangente recebe peso ~0 por construção.
- *Encaixe:* mudança local em `projecao.py`/bake (pesos já existem em embrião: o winner-take-all atual vira mistura ponderada — a rota Blender do projeto usa facing^1,5 exatamente assim, com bom resultado visual).
- *Ganho esperado:* some a "escorrida" de contorno; fronteiras entre vistas deixam de ser faca. [Medido indiretamente]: é um dos ingredientes que separaram a base "aguada porém coerente" do Blender do confete da época.
- *Riscos:* mistura de duas projeções desalinhadas (H1) gera **fantasma** (imagem dupla borrada) se aplicada cedo demais — por isso a faixa de mistura deve ser **estreita** e a autoridade territorial é o que a mantém estreita. *Verificação:* D-H3.1 (raspão cai), D-H4.1 (salto de fronteira não sobe), nitidez nas zonas de mistura (variância laplaciana) não regride vs winner-take-all.

**R3.3 — Preenchimento com barreiras e orçamento geodésico.**
- *O que é:* evoluir a A3: (i) BFS com **limite de anéis** (ex.: 24–48 anéis; além disso, a face recebe cor neutra da paleta da região em vez de importar de longe); (ii) **barreiras territoriais**: a propagação não cruza fronteiras de território — cada território preenche a partir das suas próprias sementes; regiões cegas sem semente no território herdam do território **vizinho mais próximo pela fronteira**, com a cor misturada na fronteira (e não a cor crua de lá); (iii) registrar distância média/máxima de propagação como métrica de honestidade (já desenhado no estudo anterior).
- *Encaixe:* evolução direta de `costura.py`/preenchimento atual; o mapa de territórios de R3.2 é compartilhado.
- *Ganho esperado:* elimina a classe (3) — cor importada de longe — que é o vazamento com pior aspecto (blocos inteiros fora do lugar). *Riscos:* regiões grandes sem nenhuma semente (interior da capa) ficam chapadas — aceitável e **estritamente melhor** que importar motivo errado; se a região for grande e visível, ela é candidata a vista adicional (A6/diagonais) ou a preenchimento gerativo (seção 7), não a importação.
- *Verificação:* D-H3.2 refeito: ≥95% do preenchimento intra-território ou vizinho-contíguo; distância p95 de propagação publicada; inspeção visual das prévias flat nas regiões antes problemáticas.

**R3.4 — Delight leve antes de projetar (nota, fora do caminho crítico).** As vistas canônicas têm sombreamento pintado; projetá-lo como cor faz a "sombra" de uma vista virar mancha em outra. A frente T6 (delight) já existe no backlog e os modelos de delight acompanham as rotas gerativas (Hunyuan Delight; UltraTex trabalha com vistas geradas já tratadas). Registrar a dependência: **se** D-H3.1/D-H4.2 mostrarem manchas compatíveis com sombra transferida (escuras, difusas, seguindo a luz da arte e não a anatomia), T6 sobe de prioridade. Não executar agora.

### 4.4 Síntese H3

H3 literal (através do corpo) provavelmente é pequena — prove com D-H3.1 e arquive ou corrija com R3.1. O sangramento que importa é **raspão + preenchimento sem fronteira**, e o par **R3.2 + R3.3** o fecha com mudanças locais e baratas, reusando o mapa de territórios que H4 também precisa. Ordem interna: D-H3.1/D-H3.2 → R3.2/R3.3 (juntos) → R3.1 se a matriz mandar.

---

## 5. H4 — Junção das vistas (a hipótese do Mestre)

### 5.1 Análise da causa

Primeiro, uma distinção que o projeto precisa manter nítida, porque as duas coisas têm o mesmo nome no uso diário:

- **Costura de UV** — a fronteira entre ilhas do atlas. Medida no D2/D7 (Besta, UV D-T5-1): salto médio **93,49** × 36,20 interno. É descontinuidade de *amostragem* (os dois lados da mesma aresta 3D leem lugares distantes da textura).
- **Junção de vistas** — a fronteira, **sobre o corpo**, entre o território pintado pela frente e o pintado pela lateral (etc.). É descontinuidade de *registro*: os dois lados foram pintados por projeções diferentes, cada uma com seu erro de alinhamento (H1). **Esta nunca foi medida diretamente** [fato] — o número 93,49 é da costura de UV, não dela. A hipótese do Mestre é sobre esta segunda.

Mecanismo [Análise]: na faixa de disputa entre duas vistas, três coisas se somam: (1) as duas projeções discordam por causa de H1 — o mesmo ponto do corpo recebe duas cores/motivos diferentes, deslocados; (2) o critério atual de escolha (winner-take-all por facing) cria uma fronteira **serrilhada** que alterna entre as duas pinturas texel a texel — o olho lê isso como duplicação/trepidação do motivo; (3) perto da fronteira, ambas as vistas estão em raspão (ver H3), onde o erro de registro é amplificado pela geometria (superfície quase paralela à projeção estica qualquer deslocamento). É por isso que a duplicação aparece **concentrada nos flancos/ombros** e é menos visível no centro de cada vista — assinatura que o D-H4.2 confirma ou refuta.

E a honestidade simétrica: motivos repetidos **no centro das costas** (território quase exclusivo da vista de costas) **não** são bem explicados por H4 — ali os suspeitos são H1 (a vista de costas projeta o cinturão dela sobre a anatomia errada, e a saia/capa da arte de costas "anda" sobre o corpo) e H3-preenchimento. H4 é um amplificador real, mas atribuir-lhe tudo seria repetir, ao contrário, o erro de achar uma causa única.

**O que a literatura faz com este problema** [Literatura]: a texturização fotogramétrica resolveu junções há uma década com uma receita em três tempos — (i) **seleção de vista por face** (cada face recebe UMA vista-fonte, escolhida por otimização global com termo de suavidade que prefere fronteiras onde as vistas concordam: formulação MRF de Lempitsky & Ivanov, refinada por Waechter et al.); (ii) **nivelamento de costura** (*seam leveling*): ajuste global de ganhos por vértice para as cores dos dois lados convergirem, seguido de ajuste local por **edição de Poisson** numa faixa ao longo da costura (Waechter, Moehrle & Goesele, *Let There Be Color!*, ECCV 2014 — framework completo, com implementação aberta no mvs-texturing/OpenMVS); (iii) quando há mistura, ela é **multibanda** (frequências baixas misturam numa faixa larga, altas numa estreita — Burt & Adelson; Allène et al. aplicaram a atlas de textura), o que esconde a costura sem criar fantasma de detalhe. Nas rotas gerativas, o problema é atacado por **pintura sequencial com trimapa** (TEXTure, Richardson et al. 2023: cada pixel é *manter/refinar/gerar*; Text2Tex, Chen et al., ICCV 2023: segmentação dinâmica manter/gerar/atualizar + inpainting ciente de profundidade, vista a vista) ou por **geração multivista sincronizada** (SyncMVD, SIGGRAPH Asia 2024), que produz as vistas já concordando entre si.

### 5.2 Diagnóstico

**D-H4.1 — Salto de cor na fronteira de territórios (a régua que falta).** Construir o grafo de arestas da malha; classificar cada aresta como *interna* (mesma vista-fonte dos dois lados), *fronteira de vista* (fontes diferentes) ou *costura de UV* (mesma fonte, ilhas diferentes); medir o salto médio de cor por classe no bake-âncora. Três números que separam os problemas de uma vez: se fronteira-de-vista >> interna, H4 está medida e quantificada; a comparação com costura-de-UV diz qual das duas "costuras" domina. Custo: um script sobre artefatos que já existem (mapa de fontes do bake + `costura.py`). *Este é o instrumento-juiz de todas as rotas de H4.*

**D-H4.2 — Mapa de discordância de dupla pintura.** Para cada texel com duas ou mais vistas candidatas diretas, medir a discordância entre as cores candidatas (distância RGB/ΔE) e gerar um **mapa de calor sobre as prévias flat**: onde a discordância é alta, ou há motivo duplicado ou um dos dois registros está errado. Cruzar com a localização dos defeitos que o Mestre apontou. *Decide* a fatia de H4 no sintoma total e serve de antes/depois para R4.1/R4.3.

### 5.3 Rotas de solução

**R4.1 — A receita fotogramétrica completa: rotulagem por face + nivelamento de costura.**
- *O que é (três peças, nesta ordem):*
  1. **Rotulagem (labeling) por face:** cada face ganha **uma** vista-fonte, por otimização: custo de dados = qualidade da vista para aquela face (facing, resolução projetada, confiança de registro estimada por D-H4.2); custo de fronteira = discordância de cor prevista entre vizinhos com fontes diferentes (termo de Potts: fronteira barata onde as vistas concordam, cara onde discordam) — resolvível por graph-cut ou, numa versão simples e determinística, por crescimento de regiões a partir das sementes de maior confiança com fronteira empurrada para zonas de concordância. Efeito: **dupla pintura deixa de existir por construção** — cada texel tem um pai só.
  2. **Nivelamento global (seam leveling):** com a rotulagem fixa, resolver ganhos suaves (por vértice/região, mínimos quadrados esparsos — o sistema de Waechter et al. é exatamente isso) para que, ao longo de cada fronteira, os dois lados **convirjam de cor** sem mover o interior.
  3. **Ajuste local de Poisson na faixa da fronteira:** resolver o gradiente na faixa de ±2–4 texels ao redor das fronteiras (de vista **e** de UV — o mesmo mecanismo serve às duas costuras, atacando também o 93,49 já medido) para costurar sem degrau.
- *Encaixe:* é a rota mais "industrial" e a que mais reusa o que existe: `costura.py` já enumera pares soldados; o mapa de fontes já sai do bake; o solver esparso é scipy (já no ambiente). Substitui o A4 do estudo anterior (equalização par-a-par) por sua versão global e correta — A4 era o caso particular ingênuo desta rota.
- *Esforço:* **médio-alto** (a maior tranche desta seção; três sub-entregas testáveis separadamente: rotulagem → leveling → Poisson).
- *Ganho esperado:* fronteira de vista e costura de UV ambas → alvo **≤ média interna do mesmo modelo** (a régua já proposta para costura: 36,20 de referência interna na Besta; medir a interna do Orc no D-H4.1). [Literatura] É a técnica com que a fotogrametria textura modelos de milhões de faces com centenas de fotos; o problema dela aqui é mais fácil (4–9 vistas, uma malha).
- *Riscos:* (i) rotulagem pode criar fronteiras longas em lugares visíveis se o custo de dados dominar — calibrar os pesos com D-H4.1/D-H4.2 como juízes; (ii) leveling pode "lavar" diferenças legítimas (pintura de guerra que cruza a fronteira) — limitar a amplitude do ganho (ex.: ±12 níveis RGB) e medir; (iii) Poisson em espaço UV atravessa ilhas — aplicar a faixa **sobre a malha** (por arestas/faces) e só depois rasterizar, não sobre a imagem da textura.
- *Verificação:* D-H4.1 refeito (as três classes de salto), D-H4.2 (discordância some por construção fora da faixa), inspeção visual das prévias flat nos flancos/ombros, e a régua global da D1 (SSIM por região não regride).

**R4.2 — Mistura multibanda/feathered nas fronteiras (a versão barata).**
- *O que é:* manter o winner-take-all no interior, mas numa **faixa geodésica** ao redor de cada fronteira de vista (ex.: 3–8 mm de superfície), misturar as duas pinturas com pesos pela distância à fronteira, separando frequências: cor média (baixa frequência) mistura na faixa toda; detalhe (alta frequência) escolhe um dos lados (sem mistura) para não criar fantasma.
- *Esforço:* baixo–médio. *Ganho:* esconde o degrau de cor; **não** corrige motivo duplicado deslocado (misturar dois motivos deslocados = fantasma; por isso o detalhe não mistura). É paliativo honesto para a componente "salto de cor" de H4, não para a componente "duplicação".
- *Posição:* adotar como **primeiro passo rápido** (ou como fallback se R4.1 atrasar); medir com D-H4.1 — se o salto cair sem queda de nitidez (laplaciano) nas faixas, fica; R4.1 continua sendo o destino.

**R4.3 — Refinamento de registro par-a-par nas sobreposições.**
- *O que é:* para cada par de vistas vizinhas (frente×esquerda, etc.), refinar o alinhamento **relativo** entre elas minimizando a discordância fotométrica **na zona de sobreposição** sobre a malha (uma correção afim 2D pequena por par, estimada por busca determinística como a A1, mas com objetivo fotométrico em vez de silhueta; é o análogo, em projeção, do *bundle adjustment* de panoramas).
- *Encaixe:* estende a A1 com um segundo estágio por par; reusa a infraestrutura de bake parcial.
- *Ganho esperado [Análise]:* ataca a componente de H4 que é **desalinhamento local**: se as vistas concordarem melhor **entre si** na sobreposição, a duplicação diminui mesmo sem o IoU global subir. Hipótese a provar com D-H4.2 (a discordância média na sobreposição é o antes/depois direto).
- *Riscos:* otimizar concordância fotométrica pode puxar uma vista para um compromisso que piora o registro dela com a **arte** (as vistas passam a concordar entre si num lugar errado) — travar a correção (ex.: ≤ 6 px a 2048) e exigir que o IoU por vista não regrida > 0,002.
- *Verificação:* D-H4.2 (discordância média e p90 nas sobreposições), IoU por vista estável, D-H4.1.

**R4.4 — Vistas-ponte sintéticas de 45° (reprojeção da própria pintura).**
- *O que é:* depois de um primeiro bake, renderizar a malha **já pintada** de 4 ângulos diagonais e tratar esses renders como vistas-fonte adicionais de **peso baixo**. O passo angular entre fontes cai de 90° para 45°: cada fronteira passa a ser entre vistas mais próximas (menos raspão, menos discordância), e as diagonais reais da REF-01 (A6), quando chegarem, substituem as pontes com arte de verdade.
- *Encaixe:* usa o renderizador que já produz as prévias; nenhum ativo novo. *Esforço:* baixo–médio.
- *Ganho esperado [Análise]:* reduz a severidade de cada junção (mais junções, porém mais fracas) e alimenta cobertura nas cunhas entre cardinais (sinergia com a régua de cobertura ≥35%).
- *Riscos:* **a ponte carrega os erros do primeiro bake** — se usada como fonte plena, ela eterniza defeitos; por isso peso baixo, uso restrito a mistura/preenchimento, e **nunca** como fonte de detalhe onde uma vista real alcança. *Verificação:* D-H4.1 (salto médio por fronteira cai), cobertura sobe, D-H4.2 não piora no interior dos territórios.

**R4.5 — Pintura sequencial com trimapa (TEXTure/Text2Tex adaptados às vistas reais).**
- *O que é:* em vez de projetar as 4 vistas "ao mesmo tempo" e arbitrar, pintar **em sequência ordenada** (frente → laterais → costas, pela ordem de autoridade do projeto): ao projetar cada vista nova, os texels já pintados com alta confiança são **mantidos** (máscara *keep*); os de baixa confiança/fronteira são **atualizados**; os vazios são **gerados** (aqui: projetados da vista real, não de difusão). É o trimapa do TEXTure e a segmentação dinâmica do Text2Tex [Literatura] com a etapa gerativa substituída pelas vistas canônicas do projeto. A fronteira deixa de ser uma disputa e vira uma **transição administrada**: a vista nova só entra onde a antiga é fraca.
- *Encaixe:* reestrutura o laço do bake (ordem + máscaras de estado por texel) — o pipeline já mantém proveniência por texel, que é 80% do caminho.
- *Esforço:* médio. *Ganho:* elimina dupla pintura fora das faixas de atualização e dá à frente (autoridade de cor) precedência real sobre o rosto/peito — coerente com a governança do projeto (frente é a autoridade).
- *Riscos:* a ordem vira viés (erros da primeira vista se consolidam) — mitigar com a faixa de atualização larga o bastante e com D-H4.2 comparando ordens (frente-primeiro × costas-primeiro devem convergir para resultados parecidos; divergência grande = a rota está escondendo discordância, não resolvendo).
- *Verificação:* D-H4.1/D-H4.2 + SSIM por região (a frente deve melhorar ou empatar; as costas não podem degradar além da régua).

**R4.6 — A saída gerativa para as junções.** Nas rotas T7/T3 as vistas são **geradas já registradas com a malha** (e, no caso do SyncMVD e dos modelos multivista atuais, geradas **sincronizadas entre si**), e o preenchimento é inpainting ciente da forma (Paint3D faz isso em espaço UV com modelos dedicados [Literatura: CVPR 2024]). Ou seja: H4 não é "resolvida" — ela **não chega a existir** na mesma forma. O preço e as condições estão na seção 7.

### 5.4 Síntese H4

A hipótese do Mestre está **certa quanto ao mecanismo** (junções duplicam e tremem motivos) e merece virar instrumento (D-H4.1) antes de virar obra. A solução de fundo é a receita completa **R4.1** (rotulagem + leveling + Poisson), com **R4.2** como passo rápido, **R4.3** atacando o desalinhamento local entre vistas, **R4.4** barateando as junções com pontes de 45°, e **R4.5** como alternativa de arquitetura do bake que combina com a autoridade da vista frontal. Todas se verificam com os mesmos dois instrumentos (D-H4.1/D-H4.2) — construir os instrumentos primeiro é o que torna o resto barato de julgar.

---

## 6. Síntese causal — e o que NÃO fazer

**A cadeia causal [Análise], em uma frase por elo:**

1. **H1** garante que cada vista, projetada, coloca uma fração dos motivos em anatomia errada (IoU ~0,80 = ~20% de silhueta fora do lugar, mais o deslocamento interno não medido).
2. **H4** faz esse erro aparecer **duas vezes e tremido** nas faixas entre territórios — é onde o olho do Mestre lê "vários orcs".
3. **H3** espalha o erro para as regiões que nenhuma vista pinta (raspão nas bordas + preenchimento que importa cor de longe).
4. **H2**, se existir além de detritos, adiciona bordas falsas e votos fantasmas que imitam H3/H4.
5. O **orçamento de texels** (resolvido em grande parte pela COR-08: bake 2048) decide se, depois de tudo isso, o detalhe que sobrou é legível — é condição, não causa.

**Anti-rotas (o que este estudo recomenda NÃO fazer, com o motivo):**

- **Não** aumentar resolução de novo como resposta ao sintoma: 2048 já está feito; 4096 quadruplica custo de bake para pintar a região errada com mais nitidez (o erro é de registro, não de amostragem — §1.1).
- **Não** misturar (blend) as vistas globalmente antes de rotular/alinhar: blending de projeções desalinhadas produz fantasma — a literatura e o bom senso concordam; mistura é o **último** passo (frequência baixa, faixa estreita), nunca o primeiro.
- **Não** voltar à dilatação UV como preenchimento principal: a A3 a substituiu por motivos medidos; o preenchimento correto é geodésico **e** territorial (R3.3).
- **Não** perseguir o IoU global de 0,88 antes de D-H1.2 decompor o erro: se o déficit mora no machado em pose, a régua global cobra da geometria do corpo um crime que ela não cometeu (ver R1.6).
- **Não** adotar rota gerativa como "solução da D1" sem renomear o critério: T7/T3 trocam a pergunta "os pixels da arte estão no lugar?" por "a textura gerada é coerente e fiel em espírito?" — pode ser a decisão certa, mas é uma decisão **do Mestre sobre o cânone**, não um conserto técnico (LIC-01 e a decisão registrada no ESTUDO_MELHORIAS: "a projeção usa os pixels da arte oficial; o Paint inventa uma textura parecida").

---

## 7. Rotas gerativas (T7 UltraTex / T3 Hunyuan Paint) — a bifurcação estratégica

### 7.1 Por que elas dissolvem H1/H4 (e o que sobra)

Nas duas rotas, as vistas de pintura são **geradas a partir da malha** (renderizações da própria geometria condicionam a geração), logo **não existe erro de registro arte×malha**: a "vista de costas" é, por construção, a vista *daquela* malha. H1 some como erro de projeção; H4 reduz-se às costuras entre vistas geradas — que os modelos multivista atuais tratam gerando as vistas **em conjunto** (consistência multivista é o coração do Hunyuan Paint e dos métodos sincronizados tipo SyncMVD [Literatura]) e com **inpainting em espaço UV** para os buracos (o desenho coarse-to-fine do Paint3D [Literatura: CVPR 2024] é o template publicado dessa arquitetura). H3 some junto (não há "outra vista" estrangeira para sangrar). H2 **não** some: malha com cascas internas continua gerando UV e sombras estranhas — D-H2 continua valendo antes de qualquer rota.

### 7.2 O que elas custam (fatos, não opinião)

- **Fidelidade de pixel à arte canônica: abandonada.** O UltraTex usa as vistas do projeto como **guias** e **gera** cada vista com FLUX.2 [fato verificado em `VERIFICACAO-PESQUISA-TEXTURA.md`]; o Hunyuan Paint sintetiza a partir de **uma** imagem de referência [fato do estudo T3]. Os crânios do cinturão serão *crânios parecidos*, não *os* crânios. Para um projeto cujo critério registrado é fidelidade ao cânone, isto é uma mudança de produto.
- **T3 nesta máquina é o Paint 2.0 via fork 2GP, não o 2.1.** O 2.1 oficial documenta **21 GB de VRAM para a etapa de textura** (29 GB o pipeline todo) [Literatura: README oficial do Hunyuan3D-2.1; corroborado por fontes secundárias] — inviável em 8.188 MB sem truques. O fork 2GP (mmgp) orça a textura do 2.0 em ~6 GB nos perfis 4/5, **sem garantia**: há relato público de OOM na geração de textura mesmo no fork (issue #30 do repositório 2GP, citada no estudo T3), e o mmgp avisa que o Windows pede ~16 GB de RAM a mais que os números de Linux (o PC tem 31,8 GB — perfil 5 é o ponto de partida seguro). Há ainda um risco de **tempo**: no 2.1 oficial, um usuário mediu a etapa de *inpainting* dominando 99,5% de um job de 8.564 s rodando em um núcleo de CPU (issue #139 do repositório oficial) — relato único, de outra versão, mas é o tipo de coisa que o spike existe para medir aqui.
- **T7 é uma alegação a medir, não um fato.** "15–18 min/modelo em GPU de 8 GB, atlas 8K, 10 vistas" é o que o README do UltraTex afirma [fato sobre o README]; o projeto ainda não rodou. Os pesos estão no Drive e as réguas do spike já estão pré-registradas (VRAM ≤ 8.188 MB, tempo ≤ 45 min, SSIM frontal ≥ T1, zero OOM) — o spike decide.
- **Licenças (registro, conforme LIC-01 — não bloqueiam o estudo/spike):** UltraTex: código GPL-3.0; modelo-base FLUX.2 Klein sob licença BFL não comercial (outputs com restrições da própria licença). Hunyuan: licença comunitária da Tencent com restrições territoriais documentadas [Literatura]. Adoção comercial espera o Mestre.
- **Delight vem junto:** as duas rotas tratam a sombra embutida na referência (Delight no ecossistema Hunyuan; geração já "limpa" no UltraTex) — respondem também à frente T6, que a projeção pura não resolve.

### 7.3 Papel correto das gerativas no plano [Análise]

Nem "plano B envergonhado" nem "solução mágica": são a **outra resposta legítima** à mesma pergunta, com critério de sucesso diferente. O desenho racional é **competição com réguas declaradas**: a rota de projeção melhorada (seções 2–5) e os spikes T7/T3 produzem, sobre o **mesmo Orc-âncora**, resultados julgados lado a lado pelo Crítico (mecanismo × visual) e pelo Mestre — com a diferença de critério (pixel da arte × coerência gerada) **explícita na folha de julgamento**, para a escolha ser informada e não retórica. Há ainda um **híbrido** tecnicamente atraente: usar a saída gerativa como **preenchimento inteligente** das regiões que a projeção não alcança (interior da capa, topo, solas) mantendo a projeção como fonte de tudo que ela alcança — a arquitetura coarse-to-fine do Paint3D (projeção primeiro, inpainting generativo consciente da forma depois) é exatamente esse híbrido [Literatura]. Se o híbrido entrar, a régua muda por região: regiões projetadas julgadas por fidelidade à arte; regiões geradas, por coerência com o entorno.

---

## 8. Plano priorizado

**Princípios:** (1) instrumento antes de obra — cada fase constrói a medição que julga a próxima; (2) nenhuma fase declara a D1 fechada sozinha; (3) toda execução reporta o **painel de métricas do Mestre** (tempo, VRAM/RAM/CPU, triângulos, peso do GLB/textura, tokens quando houver) — regra registrada em 01/11 19:06; (4) determinismo re-provado por reexecução com SHA em cada fase que tocar o bake; (5) fases 1–3 são **dentro da rota atual** e não dependem de nenhuma decisão nova do Mestre; a fase 4 (deformação) e a fase 5 (gerativas como candidatas a padrão) pedem o olho dele nos marcos indicados.

### Fase 0 — Diagnóstico completo (1–2 execuções; CPU/GPU leve)

| Item | Entrega | Régua de saída |
|---|---|---|
| D-H2.1 + D-H2.2 | Auditoria da malha-âncora: componentes, manifold, autointerseção, faces internas | H2 confirmada (com lista) ou **arquivada com prova** |
| D-H1.1 | Tabela IoU de 2–3 motores × 3 seeds (forma crua) | Variância conhecida; viabilidade de R1.1 decidida com número |
| D-H1.2 + D-H1.3 | Mapas de diferença simétrica por região + perfis de largura | Erro decomposto: apêndices × corpo × proporção; subsídio para R1.6 |
| D-H3.1 | Matriz de sangramento 4×4 (ablação, régua declarada) | H3 literal quantificada; destino de R3.1 decidido |
| D-H3.2 | Proveniência geodésica do preenchimento A3 | Cauda de importação medida; calibração de R3.3 |
| D-H4.1 + D-H4.2 | **Os dois instrumentos de junção**: saltos por classe de aresta + mapa de discordância | H4 quantificada; linha de base de todas as rotas R4 |

*Dependências:* nenhuma entre os itens (paralelizáveis). D-H2 primeiro na prática: se a malha estiver suja, os outros diagnósticos se repetem depois da limpeza.

### Fase 1 — Higiene e vazamento (rota atual; esforço baixo–médio)

1. **R2.1/R2.2** — limpeza cirúrgica conforme o laudo da Fase 0 (só o que o laudo mandar). *Régua:* contadores zerados/lista nomeada; IoU e cobertura sem regressão.
2. **R3.2 + R3.3 juntos** — pesos suaves de ângulo + autoridade territorial + preenchimento com barreiras/orçamento geodésico (compartilham o mapa de territórios). *Réguas:* D-H3.1 fora-diagonal ≤2%; D-H3.2 ≥95% intra-território/vizinho; D-H4.1 não piora; cobertura direta sem perda >0,5 p.p.
3. **R3.1** — somente se D-H3.1 apontar vazamento por granularidade. *Régua:* idem, sem furos novos nas bordas.

### Fase 2 — Junções de verdade (rota atual; esforço médio–alto)

1. **R4.2** (passo rápido) — mistura multibanda nas faixas de fronteira. *Régua:* salto de fronteira (D-H4.1) cai ≥30% sem perda de nitidez (laplaciano) nas faixas.
2. **R4.3** — refinamento de registro par-a-par nas sobreposições (trava ≤6 px; IoU por vista estável ±0,002). *Régua:* discordância média/p90 (D-H4.2) cai ≥25% nas sobreposições.
3. **R4.1** — rotulagem por face → nivelamento global → Poisson por arestas (três sub-entregas, cada uma medida). *Réguas finais da fase:* salto de fronteira de vista **e** salto de costura de UV ambos ≤ média interna do mesmo modelo; SSIM por região ≥ baseline do job-âncora em todas as regiões.
4. **R4.4** — vistas-ponte de 45° (peso baixo) **ou** A6 com diagonais reais da REF-01, conforme a frente de arte entregar. *Régua:* cobertura direta ≥35% (com diagonais; a régua histórica sem diagonais é ≥28% — e a COR-08 já mede 49,79% na régua nova, então a régua de cobertura deve ser **re-baselada** no primeiro run desta fase, no mesmo instrumento, antes de cobrar número).

*Dependências:* R4.1 depois de R3.2 (usa territórios como semente da rotulagem); R4.3 antes ou junto de R4.1 (rotular sobre registros refinados é melhor); R4.4 por último (pontes herdam o bake — quanto melhor o bake, melhor a ponte).

### Fase 3 — Forma: seleção (e régua honesta)

1. **R1.1** — varredura e adoção da forma vencedora por sujeito, com veto visual da forma. *Régua:* IoU mínimo das vistas ≥ âncora +0,03, sem reprovação visual.
2. **R1.6** — decisão de régua por região (corpo × apêndices) a partir de D-H1.2, registrada em DECISOES **com a palavra do Mestre** (muda o critério de aceite da D1).

*Dependências:* R1.1 consome D-H1.1 (Fase 0); a pintura das Fases 1–2 deve ser re-provada sobre a forma vencedora (o job-âncora muda — registrar o novo âncora com SHAs, como se fez com o `20261101-101528-corint-orc-s7`).

### Fase 4 — Forma: deformação guiada por silhueta (spike, com guarda-corpos)

**R1.4** como spike isolado, **desligado por padrão**: proxy decimada, PyTorch3D (silhueta suave multivista + regularização laplaciana/normais), amplitude travada, juiz = Blender. *Réguas de promoção:* IoU ≥0,88 nas 4 vistas medido no Blender **ou** ≥+0,05 sobre a Fase 3; variação de volume dentro de régua a fixar no spike; **aprovação visual da forma deformada pelo Crítico e fotos ao Mestre** antes de virar etapa. *Se falhar:* arquiva-se com o relatório — a D1 segue com o teto da Fase 3 e a decisão migra para a Fase 5.
*Dependências:* D-H1.2 (só vale se a divergência for suave/proporcional); REF-01 diagonais do Orc ajudam como vistas de conferência anti-ambiguidade.

### Fase 5 — Competição gerativa (decisão estratégica do Mestre)

1. **Spike T7** (pesos já no Drive; réguas pré-registradas: VRAM ≤8.188 MB, ≤45 min, SSIM frontal ≥ T1/projeção atual, zero OOM, painel de métricas completo).
2. **Spike T3** (Paint 2.0 via 2GP, perfil 5 → 4; mesmas réguas; medir pico de VRAM **e** RAM; papel esperado: preenchimento de zonas cegas, não pintura principal — conforme o estudo T3).
3. **Julgamento comparativo** no mesmo Orc-âncora: projeção melhorada (Fases 1–3) × T7 × T3-híbrido, folha única com o critério de cada rota declarado (pixel × coerência), Crítico sênior + olho do Mestre. *Saída:* decisão registrada — manter projeção como padrão, adotar gerativa como padrão, ou híbrido por região (projeção onde alcança, inpainting gerativo onde não alcança).

*Dependências:* nenhuma com as Fases 1–4 (os spikes podem correr em paralelo, respeitada a trava de GPU); o **híbrido** depende da Fase 2 (precisa de um bake de projeção bom para ser a camada "coarse").

### Régua de fechamento da D1 (consolidada, proposta)

A D1 fecha quando, no sujeito-âncora vigente, **todas** passarem no mesmo run: IoU ≥0,88 por vista **ou** régua por região da Fase 3 (a que estiver vigente, registrada); cobertura direta ≥ régua re-baselada da Fase 2; salto de fronteira de vista e de costura UV ≤ média interna; proveniência do preenchimento ≥95% intra-território/vizinho; SSIM por região (rosto/peito/pernas, render flat × canônica) acima do baseline do âncora em todas as regiões, sem regressão; pele na família verde da canônica (ΔE medido na caixa do peitoral); determinismo byte-idêntico em reexecução; **e** o Mestre aprovar o visual nas montagens (referência | antes | depois + zoom do rosto). Crítico julga a tabela; Mestre julga a imagem; a D1 só fecha com os dois.

---

## 9. Honestidade — onde a evidência é fraca

- **Nenhum ganho de rota foi medido ainda neste projeto, exceto os já citados** (COR-08: IoU +~0,03–0,05 e cobertura +1,7 p.p. na régua nova; comparativo Blender: erro de cor 42,8 × 47,8 e cobertura 63,43% × 20,03% em réguas distintas). Todos os "ganhos esperados" das rotas R são **hipóteses com mecanismo**, não promessas — cada um carrega sua medição de verificação justamente por isso.
- **O número 93,49 de costura é da Besta** (UV D-T5-1), não do Orc, e é de costura **de UV**, não de junção de vistas. Usá-lo como prova da H4 seria um erro de instrumento — D-H4.1 existe para produzir o número certo.
- **A variância de IoU entre seeds/motores é desconhecida** — R1.1 pode se revelar inútil (se tudo der ~0,80) ou a maior barganha do plano (se houver 0,87 no lote). D-H1.1 decide por < 10 min de GPU; qualquer afirmação anterior a ela é chute.
- **R1.4 (deformação) é a rota com maior distância entre promessa e prova**: a técnica é estabelecida na literatura para ajuste a silhuetas, mas não há medição dela em malhas deste pipeline, e o risco de produto (deformar a forma aprovada) é real. Está na Fase 4, atrás de spikes e travas, por isso.
- **Os números do UltraTex são do fornecedor** (README), e os do mmgp/2GP são orçamentos de perfil com contra-exemplo público de OOM. Os spikes T7/T3 existem porque folheto não é medição.
- **A percepção do Mestre ("vários orcs") é um sintoma, não um diagnóstico** — este estudo a trata como tal: três mecanismos a produzem, e os instrumentos da Fase 0 foram desenhados para **separar as fatias** em vez de coroar uma hipótese por afinidade com o sintoma. Se D-H4.2 mostrar a discordância espalhada pelo corpo todo (e não nas fronteiras), H4 cai para coadjuvante e o plano se reordena para H1 — o plano foi escrito para sobreviver a esse resultado.
- **ΔE/SSIM por região ainda não têm baseline no âncora pós-COR-08**: as réguas que os citam exigem criar a baseline no primeiro run da Fase 2 (convenção do projeto: a régua nasce no 1º run aprovado e nunca regride).

---

## 10. Fontes

**Do projeto (medições e estudos internos, lidos integralmente):**

1. `ESTUDO_D1_FIDELIDADE.md` (Oficina3D, 01/11/2026) — diagnóstico C1–C6, alavancas A1–A8, réguas e armadilhas de leitura.
2. `comparativo-blender/RESUMO.md` (01/11/2026) — rota Blender × COR-05: blending ponderado com oclusão, cobertura 63,43% × 20,03%, erro 42,8 × 47,8, mesmo teto de IoU.
3. `ESTUDO_T3_PAINT.md` — Hunyuan Paint 2.0 via 2GP: perfis mmgp (~6 GB), issue de OOM, RAM no Windows, desenho do spike e suas réguas.
4. `VERIFICACAO-PESQUISA-TEXTURA.md` — UltraTex Modular verificado no README oficial do repositório (10 câmeras, atlas 8K, referências como guias, GPL-3.0/licença BFL): https://github.com/Mstafa-awad/UltraTex-ComfyUI-nodes
5. `pendente-h4-juncao-vistas.md` — a hipótese do Mestre (19:10, 01/11/2026) e o desenho da medição de proveniência × defeitos.

**Literatura e ferramentas externas (verificadas nesta pesquisa):**

6. Waechter, Moehrle & Goesele — *Let There Be Color! Large-Scale Texturing of 3D Reconstructions*, ECCV 2014 — seleção de vista por face, nivelamento global de costura (ganhos por vértice) e ajuste local por edição de Poisson; implementação aberta mvs-texturing/OpenMVS. https://nsk.compsciclub.ru/attachments/classes/file_AkLJjlLB/waechter2014.pdf
7. Chen, Siddiqui, Lee, Tulyakov & Nießner — *Text2Tex: Text-driven Texture Synthesis via Diffusion Models*, ICCV 2023 — pintura progressiva com segmentação dinâmica (manter/gerar/atualizar) e inpainting ciente de profundidade. https://arxiv.org/abs/2303.11396
8. Richardson et al. — *TEXTure: Text-Guided Texturing of 3D Shapes*, 2023 — trimapa manter/refinar/gerar (descrito e comparado em [9] e no panorama em https://deepwiki.com/cwchenwang/awesome-3d-diffusion/3.6-texturing).
9. *Text-Guided Texturing by Synchronized Multi-View Diffusion* (SyncMVD), SIGGRAPH Asia 2024 — geração multivista sincronizada contra inconsistência entre vistas. https://ar5iv.labs.arxiv.org/html/2311.12891
10. Zeng et al. — *Paint3D: Paint Anything 3D with Lighting-Less Texture Diffusion Models*, CVPR 2024 — coarse-to-fine: fusão multivista + inpainting/HD em espaço UV conscientes da forma. https://arxiv.org/html/2312.13913v2 · https://cvpr.thecvf.com/virtual/2024/poster/29459
11. PyTorch3D — tutorial oficial *Fit a mesh via rendering* (renderização diferenciável de silhueta e textura para ajustar malha a imagens) e *Camera position optimization using differentiable rendering*. https://pytorch3d.org/tutorials/fit_textured_mesh · https://pytorch3d.org/tutorials/camera_position_optimization_with_differentiable_rendering
12. Sadekar, Tiwari & Raman — *Shadow Art Revisited: A Differentiable Rendering Based Approach* — exemplo de otimização de malha com perdas de silhueta + laplaciana + normais/arestas em PyTorch3D. https://arxiv.org/pdf/2107.14539
13. Tencent-Hunyuan/Hunyuan3D-2.1 — repositório oficial: pipeline de pintura (seleção de vistas, geração multivista, bake, inpainting) e requisitos documentados (21 GB de VRAM para textura); issue #139 com medição de usuário da etapa de inpainting dominando o tempo. https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/issues/139
14. Prática padrão de limpeza de malha no Blender (bmesh: `is_manifold`/`is_boundary`, Merge by Distance, Separate by Loose Parts, Remesh VOXEL) — referência de implementação: https://github.com/hotspoons/blender-agent/blob/HEAD/mcp/blmcp/data/skills/make-manifold/SKILL.md

*Fim do estudo. Nenhum arquivo do projeto foi alterado; o entregável é este documento. A frente executora pode pegar daqui: a Fase 0 é autocontida (scripts de medição sobre artefatos existentes + varredura de formas), e cada fase seguinte carrega seu instrumento-juiz construído na anterior.*
