# ESTUDO T3 — Spike de viabilidade do Hunyuan3D Paint (textura por IA) como Plano C da Etapa COR

- **Data:** 2026-11-01 · **Tipo:** pesquisa documental (somente leitura) — nada foi instalado, nenhum job de GPU foi rodado.
- **Pergunta:** o módulo Paint do Hunyuan3D-2GP (o fork que o projeto já usa para a forma) pode servir como preenchimento/melhoria **opcional** da Etapa COR, pintando por IA a malha que o projeto já gera — dentro da RTX 4060 de 8 GB do PC do projeto?
- **Contexto:** a Etapa COR padrão é a projeção das vistas canônicas com bake no Blender (T1, aprovado), sobre a UV do xatlas (T5, aprovado) com margem (D-T5-1, aprovado). O gargalo atual é o **detalhe** da textura projetada: rosto e detalhes pequenos saem borrados/esticados. Este estudo aprofunda e re-verifica com fontes atuais o item T3 do `ESTUDO_MELHORIAS` (que orçava a textura em ~6 GB com offload e marcava o item como "reaberto").
- **Escopo do "Paint" aqui:** é o `Hunyuan3DPaintPipeline` do Hunyuan3D **2.0** (modelo `hunyuan3d-paint-v2-0`, 1.3B), que é o que o fork 2GP integra. O Hunyuan3D **2.1** (repo oficial separado, Paint PBR de 2B, 21 GB de VRAM recomendados) **não** é o objeto deste spike — ele não roda no orçamento de 8 GB sem o fork, e o fork é do 2.0.

---

## Veredito (resumo)

**Vale o spike prático — uma vez, com régua de aceite pré-registrada e venv isolado.** A viabilidade de VRAM é real (perfis 4/5 orçam a textura em 6 GB), a entrada aceita malha externa (é o desenho oficial do pipeline), e o custo de entrada é conhecido (pesos ~5,4 GB + compilação MSVC). Mas a evidência pública **não** sustenta a esperança de que ele resolva o gargalo atual (rosto/detalhe): benchmark independente mede a textura do Hunyuan como borrada justamente em regiões geometricamente complexas, e o Paint **sintetiza** a textura a partir de **uma** imagem — ele não usa as 4 vistas canônicas do projeto nem pinta os pixels da arte; ele inventa o que a frente não mostra. Ou seja: como **Plano C arquivado com experimento mínimo desenhado**, sim; como promessa de detalhe, não. Se o spike falhar em qualquer régua (tempo, VRAM, fidelidade frontal), o item fecha como inviável nesta máquina e a Etapa COR segue com T1+T4.

---

## 1. Roda em 8 GB? Perfis, quantização e custo de tempo

**Sim, no papel — só nos perfis 4 ou 5 do mmgp.**

- Sem otimização, a etapa de textura do Hunyuan3D-2.0 pede **18,5 GB** de VRAM (o pipeline completo, 24,5 GB) [1][2].
- O sistema de perfis do mmgp (o "GPU-Poor" do 2GP) orça a etapa de textura assim: **perfil 3 → 9 GB** (acima do teto útil da 4060 de 8 GB — não serve); **perfil 4 (LowRAM_LowVRAM) → 6 GB**; **perfil 5 (VerylowRAM_LowVRAM) → 6 GB**, com offload máximo [1][2]. É daí que vem o "~6 GB" do estudo anterior — **confirmado**.
- Mecanismos que tornam isso possível: nunca carregar os dois pipelines ao mesmo tempo, offload de modelos inativos para a RAM, **VAE slicing** na geração das vistas e **quantização int8 do transformer por padrão em todos os perfis** do mmgp [1][3].
- **Porém, há evidência de OOM real mesmo no fork:** a issue #30 do repositório 2GP é de um usuário cuja geração de **textura** estourou a memória apesar do fork ("generating textures would make my GPU run out of memory... I get the same fundamental issue") [4]. O orçamento de 6 GB é alvo do perfil, não garantia: picos (bake em 2048, inpainting) dependem da malha e da configuração. O spike precisa medir o pico, não confiar no folheto.
- **RAM de sistema — atenção ao Windows:** a documentação do mmgp avisa que, por diferenças de gerenciamento de memória, **o Windows exige ~16 GB a mais de RAM** que os números de Linux dos perfis [3]. O PC tem 31,8 GB: o perfil 4 (LowRAM) é plausível, o perfil 5 é a rota segura, e perfis de "HighRAM" devem ser evitados. Este é um risco concreto e pouco visível — fica registrado como item de medição do spike (RAM de pico junto da VRAM).
- **Custo de tempo — o número que falta:** não há benchmark publicado do Paint do 2GP em perfil 4/5 numa 4060. Os pontos de ancoragem públicos são: (a) no hardware grande, a etapa de textura é questão de ~1–3 min (a rasterização/bake otimizada mede 27–60 s para malhas de ~20 mil faces; a difusão multivista domina o restante) [5]; (b) um relato completo em RTX 3060 com o pipeline oficial em ajustes baixos levou **~600 s no total** (forma + textura) [6]. Com offload agressivo (perfil 4/5), cada troca CPU↔GPU tributa cada um dos 30 passos de difusão × 6 vistas a 1024×1024 [7]. **Hipótese de trabalho do spike: 10–30 min por modelo só de textura** — a confirmar medindo; a régua de aceite herdada do estudo anterior (≤ 45 min no Orc para ser "usável sob demanda") continua sendo o critério. Acima disso, o Paint não serve nem como opcional numa fila.

## 2. Aceita a malha do projeto (GLB externo) ou exige o pipeline dele?

**Aceita malha externa — é um recurso documentado e central do desenho ("bring your own mesh").**

- As duas etapas são desacopladas por arquitetura: "Generated bare meshes can be exported and retextured" e "Users can texture handcrafted or externally generated meshes by skipping Stage 1 entirely" [8]. A API é literal: `Hunyuan3DPaintPipeline.from_pretrained('tencent/Hunyuan3D-2')` chamado com `(bare_mesh, image='input.png')` [8], e a documentação de arquitetura do fork repete: o pipeline de textura "operates as a standalone, independently invokable system that can accept meshes from any source" [9].
- **Ressalva arquitetural importante:** o Paint **gera a própria UV** (o resultado da chamada "adds UV + texture" [8]; no 2.1 isso é explícito: unwrap por xatlas dentro do pipeline [10]). Consequência direta para o projeto: um GLB pintado pelo Paint **não usa a UV do T5/D-T5-1** — ele carrega a UV e a textura do próprio Paint. Para um modo opcional isso é aceitável, mas precisa estar declarado no relatório do job (o GLB de saída do modo `pintura-ia` não herda as garantias de margem/ocupação medidas no T5).
- **Ressalva de entrada:** o pipeline espera a malha "limpa" no sentido dele (a cadeia oficial passa por remoção de faces degeneradas/flutuantes antes da pintura). A malha refinada do projeto (fechada, centrada, pivô nos pés, ≤ 50 mil tris no Prata) está na mesma ordem de grandeza das malhas que o pipeline simplifica sozinho no 2.1 (>40 mil faces disparam simplificação automática lá [11]) — no 2.0 do fork, a malha entra como está; malha fundida (ex.: machado colado) tende a pintar "através" das fusões, o que é coerente com o defeito EXT+FUS já conhecido do projeto.

## 3. Ele respeita as vistas de referência ou inventa a textura?

**Ele é condicionado por UMA imagem — e inventa o resto. Não usa as vistas canônicas do projeto.**

O fluxo do texgen 2.0, por dentro [9][12][13]:

1. **Delight:** a imagem de referência passa pelo modelo `hunyuan3d-delight-v2-0` (remove a iluminação embutida — bom: ataca o problema da "sombra pintada" que o T6 do projeto trata; ruim: é uma reinterpretação da arte, não os pixels dela).
2. **Renderização geométrica:** a malha é renderizada em mapas de normais/posição de **6 pontos de vista fixos do pipeline** — azimutes `[0, 90, 180, 270, 0, 180]` (frente, lados, costas, cima/baixo), com pesos de mistura `[1, 0.1, 0.5, 0.1, 0.05, 0.05]` — a frente manda, as costas valem metade, os lados quase nada [9].
3. **Difusão multivista:** o modelo de pintura (UNet 2.5D condicionada) **gera** as 6 vistas texturizadas a partir da imagem de referência + dos mapas geométricos, com uma reference-net de fluxo duplo desenhada para preservar detalhe de alta frequência da imagem original **nas vistas geradas** [12].
4. **Bake + inpainting:** as vistas geradas são projetadas de volta à UV e as regiões que nenhuma vista alcança são **preenchidas por inpainting** (o `mesh_processor` do differentiable renderer) [13].

Tradução para o projeto: a "referência" do Paint é **a vista de frente** (a mesma imagem do job). As costas, os lados e as zonas cegas **não vêm da arte do Mestre — são sintetizados** para serem plausíveis com a frente. Isso é exatamente o avesso do critério do T1 ("a arte do próprio RPG, fidelidade ao cânone"). Como **preenchimento** de zonas cegas ele é atraente; como **fonte** da textura ele compete com o cânone. E há um descompasso prático: o projeto tem 4 vistas canônicas por personagem (REF-01 está produzindo mais), e o Paint **ignora** 3 delas.

## 4. Qualidade em rostos/detalhes vs. a projeção atual — o que a evidência diz

Aqui o estudo precisa ser frio, porque é o ponto que motiva o T3:

- **A autoavaliação da Tencent** coloca o Hunyuan3D-2.0 no topo da tabela deles em fidelidade ao condicionamento (CMMD 3.193, CLIP-score 0.809, melhores da comparação) e num estudo com 50 voluntários/300 resultados ele vence os comparados em "aderência às condições da imagem" [14][15]. É evidência real, mas é do fabricante, em ativos gerais — não em rostos de personagens com arte 2D estilizada como referência única.
- **O benchmark independente mais direto (CaliTex, CVPR 2026)** mediu Hunyuan3D-2.1 (a geração seguinte do Paint) e concluiu, textualmente: "MV-Adapter, Hunyuan3D2.1 and Hunyuan3D-3.0 **tend to produce blurry textures on geometrically complex regions** and sometimes fail to align semantically with the reference image in certain parts" [16]. Na tabela quantitativa deles, o Hunyuan3D-2.1 marca FID 167,4 e, no estudo de usuários, **Qual 2,48 / GeoAlign 2,60 / MV-Cons 2,51 (escala ~5)**, contra 4,53/4,47/4,52 do método proposto [16]. Rosto é a região geometricamente complexa por excelência — **a fraqueza medida é exatamente o gargalo do projeto**.
- **O que joga a favor do Paint:** a frente. A reference-net foi desenhada para carregar o detalhe de alta frequência da imagem para as vistas [12], e a vista frontal gerada tende a ser nítida e coerente — plausivelmente **melhor que o bake atual do projeto na frente** (onde hoje a projeção estica). Mas é uma frente **re-sintetizada** (delight + difusão), não a arte: traços finos do rosto (cicatrizes, pintura de guerra, presas do Orc) podem sair "parecidos", não idênticos. A régua do Crítico do T1 (SSIM/ΔE por região contra a vista canônica) é o juiz certo — e o Paint pode perdê-la justamente no rosto.
- **Síntese honesta:** a projeção atual erra por **geometria** (desalinhamento malha×vista estica o detalhe); o Paint erra por **síntese** (inventa detalhe plausível e borra o complexo). Para o critério do Mestre — fidelidade ao cânone — nenhum dos dois é inocente; a projeção ao menos pinta os pixels certos nos lugares aproximadamente certos. O ganho esperado do Paint concentra-se onde a projeção é estruturalmente cega: **costas, lados e zonas de oclusão** — que é o papel de Plano C/preenchimento, não o de substituto.

## 5. Riscos

| Risco | Evidência / nota |
|---|---|
| **Compilação MSVC no Windows** | As duas extensões do texgen (`custom_rasterizer` CUDA + `differentiable_renderer`) são **obrigatórias** para o Paint (sem elas, só a forma roda) e no Windows exigem VS 2022 com workload C++ e ambiente do VsDevCmd; o erro clássico "Microsoft Visual C++ 14.0 or greater is required" está documentado no próprio guia do fork [17]. A v1 do projeto já tinha um `testar_msvc.bat` nunca concluído (estudo anterior). O fork traz `compile_mesh_painter.bat` [13], o que ajuda, mas a compilação é o **primeiro portão** do spike: se falhar, o item fecha com relatório de falha, sem tocar no app (venv isolado). |
| **OOM no meio do job** | Issue real de textura estourando VRAM mesmo no fork [4]; orçamento de 6 GB é alvo, não teto garantido. Numa fila com `gpu.lock`, um OOM do Paint não pode derrubar o worker: o spike roda fora da fila, e a integração (se houver) exige subprocesso isolado com o lock. |
| **RAM no Windows** | mmgp: Windows pede ~+16 GB sobre os números Linux dos perfis [3]; PC com 31,8 GB → perfil 5 como ponto de partida seguro, perfil 4 como tentativa medida. |
| **Download novo** | `hunyuan3d-paint-v2-0`: **5,36 GB** [18]; mais o `hunyuan3d-delight-v2-0` (também 1.3B params; total estimado da ordem de **8–11 GB** a confirmar no download). Pelo ARMAZ-01, entram no manifesto de modelos do projeto e o que não for usado volta para o Drive. |
| **Licença** | Os pesos são **Tencent Hunyuan Community License** (a mesma família que já cobre os motores de forma em uso — nenhuma classe nova de risco): uso **não se aplica à UE, Reino Unido e Coreia do Sul** (o Brasil está dentro do território) [19][20]; **as saídas são do usuário** e não são "derivados do modelo" [19]; acima de 1 milhão de usuários ativos/mês exige licença separada [20]; proibido usar saídas para melhorar outros modelos de IA [20]; avisos de licença devem ser mantidos (coerente com o que o projeto já faz). Registrar a decisão em DECISOES como se fez com o RF-03 do Hunyuan de forma. |
| **Determinismo mais fraco** | O T1 é byte-determinístico; o Paint é um modelo de difusão com offload/quantização — mesmo com semente fixa, igualdade byte a byte entre runs **não é esperada**. O modo, se existir, nasce rotulado como não-determinístico no relatório do job (a lição do projeto: relatório que não declara o modo reprova). |
| **Divergência de cânone silenciosa** | O Paint inventa costas/lados a partir da frente (ver §3). Se um dia entrar, o relatório do job precisa marcar a proveniência por região (projetado × sintetizado), como o T4 já exige para vistas geradas. Sem isso, o app passaria invenção por arte — inaceitável pelo critério do Mestre. |

## 6. Veredito e experimento mínimo

**Veredito: VALE O SPIKE — uma rodada, com régua pré-registrada; NÃO vale adoção direta.** A pergunta "roda em 8 GB?" só se responde medindo nesta máquina (o folheto diz 6 GB; a issue #30 diz que nem sempre). A pergunta "pinta melhor o rosto?" tem evidência pública **contra** a expectativa — por isso o spike se justifica como **teste de fronteira do Plano C** (preenchimento de zonas cegas), com o comparador A/B/C do estudo anterior como juiz, e não como nova direção da Etapa COR.

### Experimento mínimo (para a fila do projeto, quando o Mestre/clock de GPU permitir)

- **Ambiente:** venv isolado novo (nunca o `.venv_app` de produção); clone 2GP que já está em `motores\` (o código do texgen já está no disco — ver §7); compilar as extensões com o `.bat` do fork; baixar **só** `hunyuan3d-paint-v2-0` + `hunyuan3d-delight-v2-0` com hash registrado no manifesto.
- **Portão 0 (compilação):** `import custom_rasterizer` e o painter importam no venv isolado. Falhou → relatório em ERROS.md, item T3 fechado como inviável nesta máquina, fim.
- **Sujeito único:** o **Orc Prata refinado** (49.750 tris — o mesmo GLB da prova do T1) + a **vista de frente canônica** como imagem de referência. Nada de fila, nada de segundo personagem.
- **Configuração:** perfil **5** primeiro; se o pico ficar ≤ 6,5 GB, repetir no perfil **4**. Passos de difusão padrão do modelo (30) [7]; semente fixa registrada; 2 runs idênticos por perfil.
- **Métricas obrigatórias (todas no relatório do spike):** pico de VRAM (amostragem `nvidia-smi` a 1 Hz durante o job) e de RAM; tempo de parede da etapa de textura; SHA-256 da textura nos 2 runs (determinismo); SSIM/ΔE **por região (rosto/peito/pernas)** do render frontal em luz flat contra a vista canônica — **comparado com os números que o T1 já tem** no mesmo Orc; % de superfície coberta; folha de contato 8 ângulos (Paint × T1 lado a lado) para o Mestre.
- **Critério de aceite (definido ANTES, como manda o estudo anterior):** pico de VRAM ≤ 8.188 MB **e** tempo ≤ 45 min **e** SSIM frontal total **não pior** que o T1 (pode perder no rosto se ganhar declarado nas zonas cegas — mas aí o veredito é "preenchimento", não "pintura") **e** zero OOM nos 2 runs. Qualquer régua furada → T3 volta a **Plano C arquivado**, com este estudo + o relatório do spike como lastro, e a Etapa COR segue T1 → T4 → T6.
- **Bateria do Crítico do spike:** a do item T3 do estudo anterior (contenção com `gpu.lock` ocupado, determinismo por semente ou divergência explicada, relatório de falha honesto se a compilação quebrar) + a régua de SSIM por região herdada do T1.

## 7. Estado verificado no PC (leitura, 2026-11-01)

Verificação somente-leitura via SSH (listagens de diretório; nada executado):

- **Código do texgen: PRESENTE.** O clone em `motores\Hunyuan3D-2GP\` contém `hy3dgen\texgen\hunyuanpaint\` — o spike não precisa de clone novo.
- **Extensões compiladas: AUSENTES.** Nenhum `.pyd` sob `hy3dgen\texgen\` (busca recursiva até profundidade 3) — `custom_rasterizer` e o painter **nunca foram compilados** nesta máquina. O Portão 0 do experimento (§6) é, portanto, trabalho real e incerto, não formalidade.
- **Pesos do Paint/Delight: AUSENTES.** O hub HF do projeto (`_cache\huggingface\hub\`) contém apenas `models--tencent--Hunyuan3D-2mini`, `models--tencent--Hunyuan3D-2mv`, `models--stabilityai--TripoSR` e `models--facebook--dino-vitb16`; o cache `hy3dgen` só tem `hunyuan3d-vae-v2-0-turbo`. Não existe `tencent--Hunyuan3D-2` (o repositório-pai de `hunyuan3d-paint-v2-0` e `hunyuan3d-delight-v2-0`) — o download de ~5,36 GB do Paint [18] + o Delight é pré-requisito integral do spike, a registrar no manifesto de modelos (ARMAZ-01).

## Fontes

[1] DeepWiki — Hunyuan3D-2GP, Memory Optimization (GPU-Poor): perfis 1–5, textura 18,5 GB → 9 GB (perfil 3) / 6 GB (perfil 4), VAE slicing. https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/3.2-memory-optimization-(gpu-poor)
[2] DeepWiki — Hunyuan3D-2GP, Core Concepts: pipeline desacoplado, perfis, mínimos de 6 GB. https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/3-core-concepts
[3] mmgp no PyPI (DeepBeepMeep): perfis desenhados para 6 GB de VRAM; Windows exige ~+16 GB de RAM sobre os números Linux; transformer quantizado a 8 bits por padrão. https://pypi.org/project/mmgp/3.1.4.post1/
[4] GitHub — deepbeepmeep/Hunyuan3D-2GP, issue #30: OOM durante a geração de textura mesmo no fork. https://api.github.com/repos/deepbeepmeep/Hunyuan3D-2GP/events (índice de eventos citando a issue)
[5] DeepWiki — cann-recipes-spatial-intelligence, Rasterization Optimizations: texgen de 59,83 s → 26,52 s (malha de 20 mil faces) com paralelização do bake. https://deepwiki.com/hicann/cann-recipes-spatial-intelligence/3.4.3-rasterization-optimizations
[6] tspi.at — "A Local Image/Text to 3D Solution: Hunyuan3D": RTX 3060, pipeline oficial em ajustes baixos, ~600 s no total. https://www.tspi.at/2026/05/01/opensource3dassets.html
[7] DeepWiki — Hunyuan3D-2GP, Model Variants Overview: hunyuan3d-paint-v2-0, 1.3B, 30 passos, 1024×1024 por vista, 6 vistas. https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/8.1-model-variants-overview
[8] DeepWiki — Hunyuan3D-2GP, Quick Start Guide / Core Concepts: "Bring Your Own Mesh", `Hunyuan3DPaintPipeline` standalone (mesh, image). https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/2.2-quick-start-guide
[9] DeepWiki — Hunyuan3D-2GP, Pipeline Architecture (texgen): azimutes `[0, 90, 180, 270, 0, 180]`, pesos `[1, 0.1, 0.5, 0.1, 0.05, 0.05]`, render/texture 2048, modelos delight+multiview. https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/5.1-pipeline-architecture
[10] DeepWiki — ComfyUI-Hunyuan3d-2-1, Texture Generation Pipeline: unwrap por xatlas (`mesh_uv_wrap()`) dentro do pipeline de pintura 2.1. https://deepwiki.com/visualbruno/ComfyUI-Hunyuan3d-2-1/3.3-texture-generation-pipeline
[11] DeepWiki — Hunyuan3D-2.1, Texture Generation Pipeline: componentes de VRAM (total recomendado 21 GB); simplificação automática acima de ~40 mil faces. https://deepwiki.com/Tencent-Hunyuan/Hunyuan3D-2.1/4.2-texture-generation-pipeline
[12] DebuggerCafe — Hunyuan3D 2.0 explanation: multiview por reference-net de fluxo duplo preservando detalhe de alta frequência; bake + inpainting das regiões faltantes. https://debuggercafe.com/hunyuan3d-2-0-explanation-and-runpod-docker-image/
[13] DeepWiki — Hunyuan3D-2GP, Getting Started: extensões `custom_rasterizer` (bake) e `differentiable_renderer/mesh_processor.cpp` (inpainting por vértice); `compile_mesh_painter.bat`. https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/2-getting-started
[14] Tencent — Hunyuan3D 2.0 Technical Report (arXiv 2501.12202): CMMD 3.193 / CLIP 0.809; Paint para malhas geradas ou artesanais. https://arxiv.org/html/2501.12202v2
[15] biff.ai — guia Hunyuan3D 2.0: estudo de usuários da Tencent (50 voluntários, 300 resultados) e métricas do README. https://biff.ai/hunyuan-3d-20-a-game-changing-sota-open-source-3d-foundation-model/
[16] CaliTex (CVPR 2026) — "Geometry-Calibrated Attention for View-Coherent 3D Texture Generation": Hunyuan3D-2.1/3.0 "tend to produce blurry textures on geometrically complex regions"; tabela com FID 167,4 e estudo de usuários Qual 2,48/GeoAlign 2,60/MV-Cons 2,51 para o Hunyuan3D-2.1. https://arxiv.org/html/2511.21309v1
[17] DeepWiki — Hunyuan3D-2GP, Installation: Windows exige VS 2022 + workload C++; erro clássico de MSVC; extensões indispensáveis para o Paint. https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/2.1-installation
[18] Hugging Face — tencent/Hunyuan3D-2, pasta `hunyuan3d-paint-v2-0`: 5,36 GB. https://hg.pleisto.app/tencent/Hunyuan3D-2/tree/491728575ae08428daa230f9fc457d89393e2353/hunyuan3d-paint-v2-0
[19] DeepWiki — Hunyuan3D-2.1, Licensing and Usage: saídas são do usuário e não são derivados do modelo; território exclui UE/Reino Unido/Coreia do Sul; limiar de 1M MAU. https://deepwiki.com/Tencent-Hunyuan/Hunyuan3D-2.1/8-licensing-and-usage
[20] triposr.org — "TripoSR vs Hunyuan3D (2026)": as três condições da Community License (1M MAU, território, não treinar outros modelos com as saídas). https://triposr.org/blog/triposr-vs-hunyuan3d

*Nota de método: onde a fonte é DeepWiki, o conteúdo resume o código/README do repositório citado (com referências de arquivo/linha nas páginas). Números sem fonte pública direta (tempo do Paint em perfil 4/5 numa 4060) estão marcados como hipótese a medir no spike — não são apresentados como fato.*
