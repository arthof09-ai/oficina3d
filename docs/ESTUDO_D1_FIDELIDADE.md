# ESTUDO D1 — Ataque à fidelidade da cor (rota projeção de vistas + bake)

**Data:** 01/11/2026 · **Autor:** Muse (CM-000009), frente de estudo — **somente leitura** (nada foi executado no PC, nenhum job rodado, nenhum arquivo do projeto alterado).
**Escopo:** elevar a fidelidade da cor da rota ATUAL (projeção das vistas canônicas + bake, `oficina3d/cor/`), **sem trocar de motor nem de rota** (T3/Hunyuan Paint e T7/UltraTex são frentes rivais separadas, fora deste estudo).
**Motivo:** o Mestre viu as prévias da prova COR-05 e julgou a pintura "mal feita, horrível" — mosaico/"confete" generalizado e rosto ilegível. A pendência D1 (fidelidade de detalhe) segue ABERTA e foi re-confirmada pelo Crítico sênior em todas as tranches da Etapa COR.

## Fontes lidas (não resumidas de memória)

- `app/docs/CRITICO-cor-integracao-relatorio.md` (PC; cópia local byte-idêntica, 23.203 B) — item 9 (julgamento visual) e verificações aritméticas.
- `app/docs/CRITICO-t1-mecanismo-relatorio.md` (cópia local byte-idêntica, 22.721 B) — itens 1, 4, 8 (fidelidade por região, cobertura, proveniência por texel, auditoria da UV).
- `app/docs/ESTADO_ATUAL.md` (PC, lido ao vivo em 01/11 ~12:2x) — sínteses T1, T5, D-T5-1, D2/D7, COR-05, D-COR05.
- `app/docs/DECISOES.md` (PC) — decisões COR-02…COR-06; rascunho registrado da COR-03 (D-T5-1) em `hidden_files/cor_margem/rascunho_docs_dt51.md`.
- `app/docs/ESTUDO_MELHORIAS.md` (PC) — seção T1: critério de fidelidade por região (SSIM por região, baseline no 1º run aprovado, nunca regredir) e risco nº 1 declarado da rota (alinhamento).
- Código da rota: `oficina3d/cor/projecao.py` (cópia em `hidden_files/pc_docs_2026-11-01/cor_projecao.py`) — lido integralmente.
- Medições brutas: `hidden_files/cor_integracao/resultado_cor_prova.json` (COR-05), `hidden_files/cor_t5_orc_xatlas/resultado_cor.json` + `metricas_xatlas.json` (T5).
- Inspeção visual própria (01/11): prévia de frente da COR-05, prévia de frente da T5 e vista canônica dourada de frente do Orc (`hidden_files/2026-11-01-cor/canonicas/orc_frente.png`, SHA-256 `30c0f83d…`).

---

## 1. Base factual — os números que mandam no diagnóstico

### 1.1 As três configurações já medidas no mesmo Orc Prata (49.750 tris, textura 1024²)

| Configuração | Ocupação UV | Ilhas | Texels/face | Faces <1 texel | Diretos | Cegos (→dilatação) |
|---|---|---|---|---|---|---|
| T1 — Smart UV do refino | 0,0398 raster (0,0432 analítica) | 8.098 | 0,91 | 61,7% | 8.513 / 42.494 = **20,03%** | 79,97% |
| T5 — xatlas, sem gutter | 0,61398 | 6.578 | 12,937 | 0,33% | 121.567 / 643.613 = **18,9%** | 81,11% |
| COR-05 — xatlas c/ gutter D-T5-1 (prova integrada) | 0,20152 | 8.844* | 4,247 | — | 41.070 / 211.268 = **19,4%** | 80,56% |

\* A contagem de ilhas difere por método: 8.844 pelo `metricas_uv` do `projecao.py` (componentes por aresta UV, medido a 512 px) vs 6.578 pelo charting do xatlas. Não comparar ilhas entre métodos.

### 1.2 O fato central: a fração direta é INVARIANTE (~19–20%)

Multiplicar os texels ocupados por ~15× (T1→T5) **não moveu** a fração de texels pintados diretamente: 20,03% → 18,9% → 19,4%. Conclusão forçada pelos dados: **o gargalo da cobertura não é a UV nem a resolução — é o lado da amostragem** (visibilidade + facing + máscara da arte). Qualquer plano que ataque só UV/resolução repete o erro de leitura que a T5 desfez: a T5 melhorou as prévias (fim das áreas pretas e da mancha branca, segundo o A/B registrado no ESTADO_ATUAL) **sem** aumentar a fração direta — melhorou porque a dilatação passou a copiar de ilhas maiores e mais próximas (ver C3).

### 1.3 IoU de silhueta por vista (bake, medido a 256 px) — estável em todas as tranches

| Vista | T1 | T5 | COR-05 |
|---|---|---|---|
| frente | 0,7947 | 0,7947 | 0,7929 |
| costas | 0,7241 | 0,7241 | 0,7237 |
| esquerda | 0,793 | 0,793 | 0,7885 |
| direita | 0,7872 | 0,7872 | 0,7827 |

Ou seja: **21–28% da silhueta projetada não coincide com a silhueta da arte**, e isso não mudou com nenhuma melhoria de UV — é propriedade do par (arte 2D × malha gerada) e do alinhamento afim atual.

### 1.4 Visibilidade por vista (COR-05, `resultado_cor_prova.json`)

Faces visíveis por centroide (BVH), de 49.750: frente 8.338 (16,8%), costas 11.686 (23,5%), esquerda 8.761 (17,6%), direita 7.055 (14,2%). Cada vista enxerga menos de 1/4 das faces; a união das 4 vistas, descontadas oclusões mútuas, facing e rejeição por máscara, produz os ~19% de texels diretos.

### 1.5 Costuras (D2/D7, Besta com UV D-T5-1, `cor/costura.py`, solda por posição)

Pares de costura soldados: n=13.758, **salto médio de cor 93,49** (mediana 77,22; 78,08% dos pares > 30). Pares internos (controle): n=60.867, média 36,20 (mediana 13,96). A vizinhança de costura salta ~2,6× mais que a vizinhança interna — fragmentação adicional medida, no mesmo pipeline.

### 1.6 O rosto, em números

- Crítico T1, caixas relativas idênticas: cabeça na prévia de frente com média (53,43,39) vs (84,60,43) na canônica — mais escura e mais marrom; ponto de pele amostrado na textura: (166,135,84) — **tan/laranja, não o verde da arte**. O verde da pele "praticamente não se transfere" (Crítico COR-05, item 9).
- Orçamento de amostragem: na prova integrada há **4,247 texels/face** em média. Traços como presas e olhos ocupam poucas faces da malha decimada (49.750 tris uniformes no corpo inteiro); um traço de 2 faces ≈ 8 texels — abaixo do mínimo para legibilidade, **antes** de qualquer erro de alinhamento ou dilatação.

### 1.7 O que as prévias mostram (inspeção própria, 01/11)

Nas prévias de frente da T5 e da COR-05 (mesmo caráter): tronco, ombros e cabeça são retalhos de fragmentos da foto (placas marrons/pretas/tan em escala errada); motivos reconhecíveis da arte aparecem em lugares anatomicamente errados (um rosto de orc legível na altura da cintura/saia; a cabeça de lobo — que na arte fica no ombro — sobre a coxa); as pernas, em contraste, carregam textura de pelo/couro coerente. As costas são a vista mais legível nas duas. O defeito é **sistemático e idêntico** nas duas configurações de UV — assinatura de desalinhamento + divergência de anatomia, não de UV.

### 1.8 Âncoras da prova "antes" (congeladas, para o antes/depois)

Job `20261101-101528-corint-orc-s7` (`--qualidade prata --seed 7 --cor`, 4 vistas canônicas): textura SHA-256 `ebd744a9…`, GLB colorido `0f838538…`, GLB refinado sem cor `5467f25e…`; tempo total 264,3 s (etapa cor 175,6 s, dos quais ~97,5 s de UV xatlas e ~61 s de bake standalone); determinismo da etapa já re-provado byte a byte na D-COR05. **Qualquer melhora de D1 se mede contra este job, com as mesmas opções.**

---

## 2. Diagnóstico — causas, mecanismo e evidência

### C1 — Desalinhamento estrutural: afim por extremos × anatomia divergente (causa primária do "motivo no lugar errado")

**Mecanismo (do código):** para cada vista, `alinhamento_silhueta` calcula uma afinidade **sem rotação, com escalas x e y independentes**, que mapeia a caixa envolvente de **todos os vértices projetados** da malha sobre a caixa envolvente do alfa da arte (`projecao.py`, `rasterizar_textura` + `alinhamento_silhueta`). Os extremos da caixa são definidos por outliers (o machado em pose diferente da malha, pontas de pelo, pés), não pelo corpo; e a arte é uma ilustração cujas proporções (cabeça grande, capa de lobo volumosa, machado) divergem da malha gerada pelo Hunyuan a partir dela.
**Evidência:** IoU residual travado em 0,72–0,79 em três tranches (§1.3); o Crítico T1 registrou a causa no código ("bbox usa todos os vértices projetados, incluindo partes fora da silhueta da arte — pode esticar o mapeamento, e é por isso que o IoU residual fica em 0,72–0,79"); o ESTADO_ATUAL, após o A/B da T5, nomeia o gargalo visível atual: "**alinhamento por silhueta + divergência geometria-vs-arte**"; motivos legíveis em regiões erradas nas prévias (§1.7).
**Efeito duplo:** (a) texels projetados caem na região errada da arte (pele ← pelo/couro → o marrom/tan do §1.6); (b) texels que caem **fora** do alfa da arte são rejeitados pela máscara → viram cegos → alimentam C3.

### C2 — Cobertura direta travada em ~19%: geometria da amostragem, não da UV

**Mecanismo:** um texel só é direto se a sua face passa em (i) visibilidade por centroide (BVH), (ii) facing da face > 0,05 e facing interpolado do texel > 0,05, e (iii) o ponto projetado cai dentro do alfa da arte já alinhada. Com 4 câmeras horizontais ortogonais: concavidades (axila, entrepernas, sob o queixo, dobras da capa) são oclusas das 4 direções; faixas de raspão em volta de cada silhueta falham no facing; e a faixa de não-sobreposição das silhuetas (21–28%, de C1) é impintável por construção.
**Evidência:** invariância da fração direta (§1.2) e visibilidade por vista de 14–24% das faces (§1.4). A ablação registrada no D2/D7 (remover a vista de costas degrada só as faces das costas) confirma que cada vista contribui localmente — não há vista "sobrando" nem vazamento compensando.
**Leitura:** ~81% da textura nasce sem fonte projetada. A qualidade final é, portanto, dominada por **como se preenche o cego** (C3) e por **quantos texels diretos existem por face** (C4) — nesta ordem depois de C1.

### C3 — Dilatação em espaço UV: o "confete" propriamente dito

**Mecanismo (do código):** `dilatar` preenche texels sem fonte por inundação 4-vizinhos **no espaço da textura**, 1 px por passe, a partir do texel pintado mais próximo **em UV** — ignorando ilhas e ignorando a topologia 3D. Vizinho UV ≠ vizinho no corpo: com ilhas pequenas, a cor salta de uma parte do corpo para outra sem relação (o Crítico T1 rastreou assim a mancha branca do antebraço — dilatação a partir de ilhas claras de pelo — e as áreas pretas laterais).
**Evidência:** proveniência por texel auditada pelo Crítico T1 (item 8a): "o confete é o sintoma visual exato de 80% de dilatação sobre 8.098 ilhas"; o A/B da T5 (ilhas com ~15× mais texels) suavizou o confete sem mudar a fração direta — a dilatação passou a ficar "em casa" dentro da mesma ilha; a COR-05, ao cair para 4,247 texels/face (C4), trouxe o confete de volta com força — exatamente o que o Mestre viu.
**Leitura:** a dilatação UV é um preenchedor de emergência tratado como solução. Enquanto ~80% da superfície depender dela, haverá confete na proporção inversa do tamanho das ilhas em texels.

### C4 — Orçamento de texels insuficiente para detalhe (e a regressão silenciosa do gutter)

**Mecanismo:** a prova integrada roda textura de **1024²** com a parametrização D-T5-1 desenhada para 2048 (padding 8 px em 2048). Em 1024, o mesmo gutter relativo consome o dobro da área: ocupação 0,614 → 0,233 (medido na D-T5-1) → 0,20152 (COR-05). Resultado: 4,247 texels/face — 3× menos que os 12,937 da T5 pura.
**Evidência:** §1.1 e DECISOES COR-03 ("com 6.578 ilhas pequenas, o gutter de 8 px em 2048 custa mais área UV que as ilhas"); padding 12/16 px derrubaria a ocupação para 0,161/0,117 (medido, rejeitado).
**Efeito no rosto:** §1.6 — mesmo com alinhamento perfeito, 4,247 texels/face não sustentam olhos/presas/pintura de guerra. **O rosto ilegível é, em parte, teorema de amostragem.**

### C5 — Costuras com salto de cor 2,6× o interno

**Mecanismo:** o bake pinta cada ilha a partir da projeção; nas bordas de ilha, os dois lados da mesma aresta 3D amostram regiões diferentes da arte (e um dos lados frequentemente é cego/dilatado). Não há nenhuma etapa de equalização pós-bake.
**Evidência:** §1.5 (média 93,49 vs 36,20 interna, Besta, mesmo pipeline e mesma UV da prova). No Orc a 4,247 texels/face, o efeito se soma ao confete (o Crítico T1 notou que, a ~1 texel/face, nem dá para separar costura do ruído global; a medição D7 é a prova quantitativa de que o salto existe e é grande).

### C6 — Fatores secundários (reais, mas não são o incêndio)

- **Amostragem nearest-neighbor** da arte (`astype(int)` em `rasterizar_textura`): aliasing texel a texel; barato de corrigir (bilinear), ganho pequeno perto de C1–C4.
- **Winner-take-all por facing, sem blending:** nas sobreposições entre vistas, a fronteira de troca é dura; com o desalinhamento de C1, cada vista traz a região ligeiramente deslocada → bordas de retalho. Blending ingênuo, porém, geraria fantasma (dupla imagem) enquanto C1 não for atacado — por isso é alavanca tardia (A7).
- **Sombra embutida na arte:** as vistas canônicas têm sombreamento pintado; a projeção o transfere como se fosse cor (risco declarado no ESTUDO_MELHORIAS; delight é a frente T6, fora desta rodada).
- **Higiene de julgamento:** as prévias Workbench são sombreadas e **não são colorimétricas** (Crítico T1: vermelho puro (255,0,0) renderiza (177,55,55)). Julgar cor por prévia sombreada exagera o escurecimento; a D2/D7 já produziu prévia flat/Emission para região de costura — esse deve ser o padrão de julgamento (ver §5).

---

## 3. Alavancas candidatas

Formato: o que muda · ganho esperado · custo · risco · **como medir**.

### A1 — Alinhamento por silhueta de verdade (otimizar o IoU, não a caixa)

- **O que muda:** substituir a afinidade por extremos de vértices por um alinhamento calculado sobre as **máscaras rasterizadas** das duas silhuetas (a da malha já é rasterizável por `rasterizar_mascara_2d`): (i) caixa robusta a partir da máscara da malha (não dos vértices — elimina outliers como o machado fora de pose); (ii) busca determinística sobre (escala, translação) — primeiro com escala uniforme, depois afim com trava de aspecto (ex.: |ax/ay − 1| ≤ 0,15) — **maximizando o IoU a 256 px**, que hoje é só reportado, nunca otimizado. Tudo no módulo puro `projecao.py`, sem tocar o Blender.
- **Ganho esperado:** IoU por vista 0,72–0,79 → alvo ≥ 0,88; cada ponto de IoU devolve texels hoje rejeitados pela máscara (C1b) e reduz a amostragem em região errada (C1a). É a única alavanca que ataca simultaneamente cobertura e colocação.
- **Custo:** baixo — código puro + testes; zero GPU; tempo de bake +segundos (busca em grade grossa→fina a 256 px).
- **Risco:** otimizar IoU de silhueta não garante alinhamento interno (a anatomia interna pode continuar deslocada mesmo com contornos casados) — mitigar reportando, além do IoU, o erro em caixas de região (método do Crítico T1) antes/depois. Escala uniforme pode piorar vistas cuja divergência é genuinamente anisotrópica — a trava de aspecto é o meio-termo; registrar por vista qual modo venceu.
- **Como medir:** IoU/vista (mesma função `iou`, mesma resolução 256) antes/depois no job-âncora; % de texels diretos (campo `cobertura` do `resultado_cor.json`); médias RGB das caixas cabeça/peito/pernas da prévia flat vs canônica (ΔE ou distância RGB), método do Crítico T1 item 1.

### A2 — Casar resolução do bake com a parametrização da UV (2048² real)

- **O que muda:** a etapa `cor` passa a assar em **2048×2048** (o `tamanho` já é parâmetro de `rasterizar_textura`), casando com o padding 8 px@2048 para o qual a D-T5-1 foi desenhada. Alternativa menor: manter 1024 e reduzir o padding proporcionalmente (4 px) — ganha ocupação, perde a régua de margem ≥8 px em 2048 que a D-T5-1 instituiu contra halo em mip. Recomendado: 2048.
- **Ganho esperado:** ocupação volta à faixa 0,35–0,61 conforme o charting; texels/face de 4,247 → **~17–50** (×4 da resolução × recuperação de ocupação). É a alavanca que torna o rosto *representável* (C4).
- **Custo:** bake em Python puro escala com texels: o bake standalone de 61 s (COR-05) pode ir a ~3–6 min; GLB cresce (PNG da textura de 349 KB → ~1,2–1,5 MB estimado); tempo total do job estimado 264 s → ~8–11 min. Dentro do orçamento de qualidade do projeto (QUAL/MET: tempo não é a régua; a régua de forma é ≤180 s e não se aplica à etapa cor).
- **Risco:** memória/tempo do rasterizador em laço Python a 2048² com 4 vistas — medir pico de RAM do processo Blender; se estourar, otimizar o laço (vetorizar por face) entra como sub-tarefa, não como abandono.
- **Como medir:** `metricas_uv` (ocupação, texels/face derivados), `tamanho_textura_px`, tempo da etapa `cor` no `relatorio.json`, tamanho do GLB; e o efeito visual nas caixas de região (§5).

### A3 — Preenchimento 3D: difusão por adjacência da malha no lugar da dilatação UV

- **O que muda:** texels cegos passam a herdar cor da **face vizinha no corpo**, não do texel vizinho na UV: (i) construir o grafo dual da malha com **solda por posição** (a infraestrutura já existe em `cor/costura.py`, que solda vértices de GLB com tolerância 1e-6); (ii) difusão multi-fonte determinística sobre faces: cada face cega recebe a cor média das faces diretas alcançáveis, propagada por BFS em anéis com ordem fixa (determinismo preservado); (iii) na rasterização, texel cego amostra a cor da sua face preenchida (ou do anel), em vez de participar da inundação UV. A dilatação UV sobrevive só como último recurso para texels fora de qualquer face (costura/margem), que é o papel legítimo dela (anti-halo).
- **Ganho esperado:** elimina a classe inteira de defeito "cor de outra parte do corpo" (mancha branca, retalhos estranhos): o preenchimento respeita a topologia — pele vizinha de pele, pelo vizinho de pelo. Com ~80% da superfície preenchida, é a alavanca de maior impacto visual depois de A1+A2.
- **Custo:** médio — módulo novo ao lado de `costura.py`, testes de unidade (sintético com regiões cegas conhecidas), +tempo de CPU pequeno (BFS sobre 49.750 faces é trivial perto do bake).
- **Risco:** propagação longa em regiões cegas grandes (ex.: uma lateral inteira sem vista) espalha uma cor média chapada — aceitável (é o comportamento correto de preenchimento) e estritamente melhor que importar cor de outra região; registrar a distância média de propagação (anéis) como métrica de honestidade. Converge com a frente T2 (cor de vértice): a difusão por faces é meio caminho andado — registrar a convergência na decisão para não construir duas vezes.
- **Como medir:** **auditoria de proveniência v2** (escalada natural da auditoria do Crítico T1): % de texels preenchidos cuja fonte está no mesmo componente/região 3D vs % importado de ilha estranha (hoje, por construção, ~100% do preenchido é "o que estiver perto na UV"); salto de cor nas fronteiras direto/preenchido; inspeção visual das prévias flat.

### A4 — Equalização de costura pós-bake

- **O que muda:** após o bake, para cada par soldado de `costura.py`, misturar as cores dos texels dos dois lados da costura em direção à média do par (raio de 1–2 texels, força parametrizável), usando os pares que o módulo já enumera.
- **Ganho esperado:** salto médio de costura 93,49 → alvo ≤ média interna (36,20). Remove a "linha de retalho" que hoje costura o mosaico.
- **Custo:** baixo — pós-processamento sobre a textura + pares existentes; testes sobre o sintético de costura da D7.
- **Risco:** suavizar costura sobre detalhe legítimo que cruza a aresta (listras de guerra) — mitigar com força limitada e medição antes/depois por par (a própria métrica D7 é o juiz).
- **Como medir:** reexecutar a medição D7 (`costura.py`) no mesmo modelo antes/depois: média, mediana e % > 30.

### A5 — Charting `max_cost` 8 (ilhas maiores e mais densas)

- **O que muda:** adotar o `max_cost` 8 no charting do xatlas, que a D-T5-1 **mediu e não adotou**: +15% de densidade (5,65 texels/face a 1024 na parametrização com gutter), ilhas 6.578 → 4.575, distorção média 0,0742 (≈ igual). Ilhas maiores = dilatação/difusão mais locais (C3) e menos costura por área (C5).
- **Ganho esperado:** moderado e composto com A2/A3.
- **Custo:** baixo (um parâmetro + reprova).
- **Risco:** foi recusado por "risco não medido de distorção local" — a condição de adoção é produzir a prova que faltou: mapa de distorção por face (percentis, não só média) antes/depois; se o p95 local piorar além de régua a definir, não adota.
- **Como medir:** distorção média **e p95 por face**, ocupação, nº de ilhas, texels/face — todos já saem de `metricas_uv`/`uv_xatlas` (acrescentar o p95 é a verificação nova da bateria).

### A6 — Vistas adicionais: diagonais de 45° e topo

- **O que muda:** projetar também `frente-esquerda`, `frente-direita`, `costas-esquerda`, `costas-direita` e `cima` — **o módulo já suporta** (`ANGULOS` com 8 direções + `direcao_camera("cima")` em `projecao.py`); o gargalo é a **arte**: as canônicas do Orc são 4 (frente/costas/esquerda/direita). As diagonais dependem da frente REF-01 (diagonais do Orc são o próximo item da fila REF-01; Besta e Capríleo já têm diagonais aprovadas nos lotes 2/3).
- **Ganho esperado:** as cunhas de raspão entre vistas cardinais e as zonas de sombra de oclusão ganham fonte: estimativa de cobertura direta 19% → 30–40% (estimativa a confirmar pela métrica de cobertura; cada vista atual pinta 14–24% das faces, com sobreposição parcial).
- **Custo:** médio — depende de arte aprovada pelo Crítico Visual (REF-01); no bake, cada vista extra é um passe completo sobre as faces (tempo cresce ~linear: +25% por vista sobre o bake).
- **Risco:** vistas geradas por IA (REF-01) divergem entre si em detalhes (a Besta lote 2 teve diagonal espelhada reprovada na rodada 1) — uma diagonal errada **piora** a fidelidade onde vence o facing. Gate: só entram vistas aprovadas pelo Crítico Visual, e a ablação por vista (infraestrutura do D2/D7) deve provar que cada vista nova não degrada as regiões das outras.
- **Como medir:** cobertura direta total e por vista; ablação liga/desliga por vista com Δ nas caixas de região; IoU das vistas novas.

### A7 — Blending por facing nas sobreposições + amostragem bilinear

- **O que muda:** (i) amostragem da arte com interpolação bilinear no lugar do nearest (`astype(int)`); (ii) nas zonas onde duas vistas pintam o mesmo texel com facings próximos (razão > 0,8, por exemplo), misturar as cores com pesos ∝ facing em vez de winner-take-all.
- **Ganho esperado:** pequeno-moderado: some o serrilhado texel a texel e as fronteiras duras de troca de vista.
- **Custo:** baixo.
- **Risco:** **fantasma** — misturar duas projeções desalinhadas (C1) produz imagem dupla borrada, pior que a fronteira dura. Só faz sentido **depois** de A1 elevar o IoU; adotar com interruptor medido (comparar nitidez — variância laplaciana — nas zonas de sobreposição, com/sem).
- **Como medir:** métrica de borda dupla nas sobreposições + inspeção visual; SSIM por região (§5) não pode regredir.

### A8 — Warp por marcos anatômicos (só se A1 não bastar)

- **O que muda:** alinhamento não-linear por vista: casar os **perfis de largura da silhueta** ao longo da altura (malha × arte) por programação dinâmica (DTW 1D) e deformar verticalmente o mapeamento; âncoras horizontais análogas por vista lateral. Ataca a divergência de proporções (cabeça grande da arte × cabeça menor da malha) que nenhuma afinidade resolve.
- **Ganho esperado:** potencialmente o maior em fidelidade de região (rosto volta para a cabeça), mas incerto.
- **Custo:** alto — algoritmo novo, superfície de teste grande, risco de deformações patológicas em sujeitos não-humanoides (Besta!).
- **Risco:** alto para generalidade (o app é para qualquer criatura do RPG, não só humanoides). **Não recomendado nesta rodada**; fica como carta registrada se A1+A6 deixarem o IoU/regiões abaixo da régua.
- **Como medir:** os mesmos instrumentos de A1 (IoU + caixas de região), comparados vista a vista e sujeito a sujeito (Orc **e** Besta, para provar generalidade).

### Fora de escopo desta rodada (registrado para não virar confusão)

- **Delight / remoção de sombra embutida (T6)** e **cor de vértice como produto (T2)**: frentes próprias do backlog. A3 conversa com T2, mas não o substitui.
- **Troca de rota (T3 Paint / T7 UltraTex)**: o ESTUDO_MELHORIAS registra o porquê da projeção ser a rota canônica — "a projeção usa os pixels da arte oficial do RPG; o Paint inventa uma textura parecida" (fidelidade ao cânone é o critério do Mestre). Este estudo assume essa decisão e a torna executável.

---

## 4. Ordem recomendada de execução

1. **A1 (alinhamento otimizado)** — primeiro porque é barato, puro, sem GPU, e multiplica todas as outras: sem ele, A2 pinta a região errada em alta resolução e A6 adiciona vistas desalinhadas. Também é a causa nomeada pelo próprio projeto como gargalo visível atual.
2. **A2 (bake 2048 casado com o gutter)** — segundo porque é mudança de configuração/parâmetro com ganho aritmético garantido (texels/face), e destrava a legibilidade mínima do rosto (C4). Fazer depois de A1 para a prova de A2 já nascer sobre o alinhamento novo (menos variáveis por prova — disciplina de tranche).
3. **A3 (preenchimento 3D)** — terceiro porque ataca os ~80% restantes (mesmo após A1+A6, metade ou mais da superfície será preenchida, não projetada) e elimina a classe do defeito que o Mestre viu (confete = cor importada de outra parte do corpo).
4. **A4 (equalização de costura) + A5 (max_cost 8)** — quarto, juntos: são baratos, medidos por instrumentos que já existem (`costura.py`, `metricas_uv`) e refinam o resultado de A1–A3.
5. **A6 (vistas diagonais/topo)** — quinto porque depende da REF-01 (arte do Orc) e seu ganho é real, mas condicionado a gate de qualidade da arte.
6. **A7 (blending/bilinear)** — por último entre os adotáveis: só com IoU alto (pós-A1) o blending ajuda em vez de borrar. **A8** fica estacionada como contingência.

Cada passo fecha como tranche própria, com Crítico sênior e bateria escalada (APR-01), e **nenhum passo declara a D1 fechada sozinho**: a D1 fecha quando a prova do §5 passar inteira.

---

## 5. Desenho da prova — como demonstrar a melhora ao Mestre

**Sujeito e condições (idênticos ao "antes"):** Orc Prata, job via fila com `--qualidade prata --seed 7 --cor`, mesmas 4 vistas canônicas douradas (SHAs das canônicas conferidos), mesmo GLB refinado de entrada (SHA `5467f25e…`). O "antes" é o job-âncora `20261101-101528-corint-orc-s7` (§1.8), já determinístico e arquivado — não precisa rodar de novo.

**Métricas objetivas (antes → depois, mesmos instrumentos):**

| Métrica | Instrumento | Antes (medido) | Régua proposta p/ fechar D1 |
|---|---|---|---|
| IoU de silhueta por vista | `projecao.iou` a 256 px, no `resultado_cor.json` | 0,7237–0,7929 | ≥ 0,88 em todas as vistas |
| Cobertura direta | campo `cobertura` do bake | 19,4% | ≥ 35% (com A6; ≥ 28% sem A6) |
| Texels/face (ocupação × resolução) | `metricas_uv` + `tamanho_textura_px` | 4,247 @1024 | ≥ 17 @2048 |
| Salto de cor em costura | `cor/costura.py` (D7) | média 93,49 (Besta) | ≤ média interna do mesmo modelo |
| SSIM por região (rosto/peitoral/pernas) | método do ESTUDO_MELHORIAS §T1: recortes de render flat × vista canônica | sem baseline (criar nesta prova, a partir do "antes") | > baseline em todas as regiões, sem regressão |
| Cor da pele (caixa do peitoral) | amostragem numérica na textura/render flat, método do Crítico T1 | pele sai tan (166,135,84) | família verde da canônica (ΔE a definir na 1ª medição) |
| Proveniência do preenchimento | auditoria de proveniência v2 (A3) | ~100% vizinho-UV | ≥ 95% mesma região 3D |
| Determinismo | reexecução do job, SHAs | provado (D-COR05) | manter byte-idêntico |

As réguas são **propostas deste estudo** — pela convenção do projeto, a régua final nasce no 1º run aprovado e nunca regride (ESTUDO_MELHORIAS, seção T1). SSIM/ΔE exigem **render flat (Emission/unlit)** nas mesmas câmeras das prévias, nunca Workbench sombreado (C6).

**Apresentação visual ao Mestre (o que ele recebe):**
1. Montagem 3 colunas × 4 vistas: **referência dourada | antes (COR-05) | depois**, renders flat + uma versão sombreada só para leitura de volume.
2. **Zoom do rosto** (recorte da cabeça nas 3 colunas) — é o ponto da queixa dele; a melhora tem que ser visível ali sem lupa retórica.
3. Zoom da cintura/saia (onde hoje aparece o rosto deslocado) mostrando o motivo no lugar certo — ou sua ausência.
4. A tabela de métricas acima, preenchida, com os SHAs dos artefatos novos.

**Veredito da prova:** o Crítico sênior julga a tabela + as montagens; o Mestre julga o visual. A D1 só fecha com os dois — e a frase de aceite é a do critério já registrado no projeto: fidelidade ao cânone medida por região, não "textura bonita" genérica.

---

## 6. Armadilhas de leitura (para a frente executora não tropeçar)

- **IoU do refino ≠ IoU do bake:** o REGISTRO já confundiu uma vez (0,76–0,81 citados eram do refino). Usar sempre `por_vista.*.iou_silhueta_256` do `resultado_cor.json`.
- **Prévia sombreada não é prova de cor** (Workbench escurece; vermelho puro vira (177,55,55)). Julgar pela textura ou por render flat.
- **Ilhas e ocupação mudam com o método de medição** (xatlas vs `metricas_uv`; 512 vs 2048 px). Comparar sempre mesmo instrumento, mesma resolução de medição.
- **A fração direta ~19% não é bug de uma tranche** — é o equilíbrio atual do desenho (4 vistas + máscara + facing). Esperar que UV/resolução sozinhas a movam é o erro que este estudo existe para não repetir.
- **`texels_por_dilatacao` conta a textura inteira** (inclui fora da UV: 1.007.506 na COR-05); o número honesto de preenchimento na UV é `texels_cegos_antes_dilatacao` (170.198).
- **Determinismo é inegociável:** qualquer alavanca nova (busca de alinhamento, BFS de difusão, blending) deve ter ordem de vizinhos/grade fixa e ser re-provada por reexecução com SHA, como a D-COR05 fez para a integração.

---

*Fim do estudo. Nenhuma linha de código do projeto foi alterada; nenhuma prova foi executada. A frente executora pode pegar daqui: A1 é autocontida no módulo `oficina3d/cor/projecao.py` + testes em `testes/test_cor.py`, e a prova do §5 roda contra o job-âncora `20261101-101528-corint-orc-s7`.*
