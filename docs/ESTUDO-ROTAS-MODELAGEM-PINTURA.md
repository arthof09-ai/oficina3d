# ESTUDO ROTAS DE MODELAGEM E PINTURA — como os outros fazem, e A × B na nossa Oficina

**Data:** 01/11/2026 · **Autor:** Muse (CM-000009), frente de pesquisa — **somente estudo** (nada foi executado no PC, nenhum job rodado, nenhum arquivo do projeto alterado).
**Ordem do Mestre (01/11/2026 19:40):** (1) como os outros códigos/programas **pintam** um modelo 3D; (2) como usam **várias referências de ângulos diferentes** para fazer **uma** modelagem; (3) como funciona **1 referência + o app completa sozinho**; (4) se existe **outro jeito**; (5) **viabilizar as duas formas** (A = várias referências; B = 1 referência + completação) na nossa Oficina, para analisar qual é melhor; (6) pesquisa profissional e minuciosa, com fontes.
**Relação com os estudos anteriores:** este estudo é o mapa externo que faltava ao `ESTUDO-RAIZ-D1-SOLUCOES.md` (diagnóstico interno da D1) e incorpora as correções do `CRITICO-estudo-raiz-d1.md` — em especial: a malha-âncora tem **1 componente** (H2 simples refutada), a proveniência do preenchimento tem **máx. 21 anéis**, o ganho do otimizador de IoU foi **+0,0107 na frente**, e **falta ao projeto um teste de concordância 2D entre as 4 referências** (aqui ele vira peça central do desenho da rota A, §6.2 e §7).
**Convenção de evidência:** **[FATO]** = verificado em fonte primária citada (nome + URL); **[ALEGAÇÃO]** = o que um fornecedor/autor afirma sem medição independente — nunca tratado como fato; **[ANÁLISE]** = juízo meu para o caso da Oficina. Números do projeto são só os medidos e registrados.

---

## 0. Resumo executivo

**O mapa em quatro linhas [ANÁLISE sobre os fatos das §§1–4]:**

1. **Pintura:** ninguém no mundo publicado resolve ao mesmo tempo os nossos três problemas — junção entre vistas [J], fidelidade pixel-a-pixel à arte canônica [F] e cobertura do não-visto [C]. [F] só existe onde há **cópia** (projeção clássica fotogramétrica, projeção manual em Substance); [C] só existe onde há **invenção** (difusão); [J] é o campo de batalha entre as duas — e a evolução histórica é: trimapa (TEXTure) → geração sincronizada (SyncMVD, Hunyuan Paint) → correção em espaço UV (Paint3D, TEXGen).
2. **Forma multivista:** a consistência entre vistas, no estado da arte generativo, é **propriedade da geração conjunta** (as vistas nascem concordando porque são desruidadas juntas), **não** uma etapa de verificação. Reconstrutores feed-forward substituem verificação por um gargalo: sai **uma** representação 3D, concordem as vistas ou não — com degradação declarada e sem relatório de conflito. Só a fotogrametria **mede** consistência (erro de reprojeção) — e por isso mesmo falha com ilustrações que não são projeções de um objeto físico.
3. **Forma single-view:** o verso **nunca é recuperado — é amostrado** de um prior. Com a referência só de frente, ~50% da superfície do Orc seria invenção, e os elementos-assinatura das costas (capa de lobo, continuação do cinturão de crânios) têm probabilidade de acerto próxima da frequência deles no prior da categoria: perto de zero. A rota B é geradora de **rascunho fiel de frente**, não de asset canônico com verso desenhado.
4. **A descoberta prática desta pesquisa:** o único motor generativo aberto que aceita **nativamente as nossas 4 vistas nomeadas** (front/left/back/right) e cabe na RTX 4060 é o **Hunyuan3D-2mv / 2mv-Turbo** — e o "mv-turbo" que o projeto já roda é, com alta probabilidade, exatamente esse checkpoint [FATO de arquitetura + ANÁLISE de identificação, §2.3]. Ou seja: **a rota A provavelmente já está instalada**; o que falta é o teste de consistência das referências e a validação por marcos. E a composição "projeção do cânone onde ele existe + inpainting generativo só onde não existe" — a arquitetura que [F] exige — **não foi encontrada montada em nenhuma fonte primária**: os blocos existem separados e citáveis; montá-la é espaço aberto, e é a candidata natural a "rota oficial híbrida" da Oficina.

**Recomendação de desenho (detalhe nas §§6–7):** rodar primeiro o **spike da rota A** (forma 2mv-Turbo a partir das 4 vistas + pintura por projeção atual), porque ela usa o que já está pronto e responde à pergunta mais valiosa — *as nossas 4 vistas, alimentadas como condição, produzem forma melhor que a single-view?* — e, no mesmo Orc e com o mesmo painel de métricas, a **rota B** (frente só → forma single → pintura só-frente + completação). A comparação é desenhada para o Mestre decidir com número, incluindo o julgamento cego mecanismo × visual e um placar específico para os elementos-assinatura das costas.

---

## 1. Pergunta 1 — Como os outros PINTAM um modelo 3D

### 1.1 Projeção clássica/fotogramétrica — copiar pixel real, costurar com matemática

- **mvs-texturing (Waechter et al., ECCV 2014)** [FATO: paper — https://nsk.compsciclub.ru/attachments/classes/file_AkLJjlLB/waechter2014.pdf]: seleção de vista por face via **MRF/graph-cut** (termo de dados: nitidez/frontalidade/resolução; termo de suavidade: penaliza vizinhos com fontes diferentes), depois **nivelamento de costura global** (sistema linear entre patches) + **edição de Poisson** local na costura. Não gera pixel: escolhe e harmoniza pixel fotografado. [J] é o método desenhado especificamente para costura — o melhor da classe; [F] total onde há foto; [C] zero (face sem foto = buraco). CPU, sem difusão — VRAM irrelevante.
- **AliceVision/Meshroom** [FATO: manual — https://meshroom-manual.readthedocs.io/en/dev-custom_nodes/feature-documentation/nodes/Texturing.html]: unwrap automático, remapeamento de visibilidade e **multi-band blending** (Burt & Adelson: baixa frequência mistura em faixa larga, apagando diferença de exposição; alta frequência em faixa estreita, preservando detalhe). Licença MPL-2.0 [FATO]. [J] bom, [F] alta onde há foto, [C] só interpolação de buracos.
- **Metashape / RealityCapture** [FATO: docs Agisoft — https://www.agisoftmetashape.com/understanding-texture-map-types-in-agisoft-metashape-a-complete-guide/]: comerciais maduros; o Metashape expõe os modos que os outros escondem (Mosaic = seleção por visibilidade + blending em frequência; Average = sem costura mas borra; ghosting filter). Método interno além dos modos documentados: **não público**.
- **Leitura para nós [ANÁLISE]:** com fotos reais de todos os lados, ninguém precisa de difusão para [J]+[F]. Nosso problema é outro: nossa "foto" é **uma** arte canônica por ângulo, não 50 fotos calibradas — por isso a projeção pura nos dá [F] com cobertura de 49,79% e teto de registro (D1), e não o pacote fotogramétrico completo.

### 1.2 Pintura iterativa vista-a-vista com difusão — pintar, reprojetar, repetir

Princípio comum: renderiza uma vista → difusão condicionada por profundidade gera/inpinta → reprojeta para UV → próxima vista. Herda a inconsistência estocástica da difusão 2D: cada vista nova pode divergir das anteriores.

- **TEXTure (Richardson et al., SIGGRAPH 2023)** [FATO: arXiv:2302.01721 — https://ar5iv.labs.arxiv.org/html/2302.01721]: **trimapa dinâmico** por vista — `keep` (já texturizado de frente, não mexer), `refine` (ângulo raso, melhorar), `generate` (nunca visto, criar) — alimentando um depth-to-image (SD + ControlNet depth). [J] parcial (o trimapa reduz, não elimina); [F] não (entrada é texto; img2img redesenha); [C] sim, é o forte. VRAM não publicada; classe SD1.5+ControlNet ~6–8 GB por análise — limítrofe nos nossos 8.188 MB.
- **Text2Tex (ICCV 2023)** [FATO: http://openaccess.thecvf.com/content/ICCV2023/html/Chen_Text2Tex_Text-driven_Texture_Synthesis_via_Diffusion_Models_ICCV_2023_paper.html]: máscara de geração análoga, inpainting ciente de profundidade, **generate-then-refine** e **seleção automática da próxima melhor vista** (pontua por área nova coberta × área esticada a corrigir); inclui etapa para remover shading da textura. Melhor que TEXTure em [J] pela fase refine; [F] não; [C] sim.
- **InTeX (2024)** [FATO: arXiv:2403.11878]: unifica geração e **edição interativa** — um modelo de inpainting depth-aware em espaço de textura unificado permite selecionar uma região e repintar só ela, com o resto em `keep`. Diferencial único de [F] parcial: correção manual onde a difusão desobedeceu, sem garantia de pixel-exato.
- **TexFusion (ICCV 2023)** [FATO: https://openaccess.thecvf.com/content/ICCV2023/papers/Cao_TexFusion_Synthesizing_3D_Textures_with_Text-Guided_Image_Diffusion_Models_ICCV_2023_paper.pdf]: não pinta sequencialmente — intercala o denoising de **todas** as vistas agregando a cada passo num **mapa de textura latente partilhado** (SIMS). Consistência construída durante a difusão, não remendada depois; evita SDS explicitamente.
- **Paint-it (CVPR 2024) — correção de enquadramento** [FATO: arXiv:2312.11360 — https://arxiv.org/abs/2312.11360]: **não é vista-a-vista**; é **otimização SDS** sobre mapas PBR parametrizados por uma rede (filtro de ruído via Deep Image Prior), ~15 min/objeto no paper, saída diffuse+roughness+metalness+normal. [J] por construção (um mapa UV único otimizado globalmente); [F] não; [C] sim, com riscos SDS (Janus, saturação).

### 1.3 Geração multivista sincronizada + bake — fazer as vistas nascerem concordando

- **SyncMVD (SIGGRAPH Asia 2024)** [FATO: https://ar5iv.labs.arxiv.org/html/2311.12891]: difusão de **todas as vistas em paralelo**; a cada passo de denoising, os latentes são projetados para o domínio de textura, os que se sobrepõem são **misturados em consenso**, e o consenso volta para cada vista. A costura vira inconsistência residual, não fronteira dura. [J] o melhor da família difusão; [F] não pixel-exato (variante com IP-Adapter melhora aderência semântica); [C] sim, se o anel de câmeras cobrir a malha. VRAM não publicada; multivista simultânea em SDXL custa mais que a sequencial — assumir >8 GB até medição local.
- **Hunyuan3D-Paint 2.0/2.1 (Tencent)** [FATO: relatório técnico 2.0 — https://github.com/Tencent-Hunyuan/Hunyuan3D-2/raw/refs/heads/main/assets/report/Tencent_Hunyuan3D_2_0.pdf; README 2.1]: pipeline em 3 estágios — (1) **delighting** dedicado (Hunyuan3D-Delight remove luz/sombra da entrada) + **seleção de vistas gulosa ciente de geometria** (base ortogonal + a vista que mais cobre UV descoberto); (2) **síntese multivista** condicionada por normais/posição renderizadas, com **ReferenceNet** double-stream (preserva detalhe da referência nas outras vistas) e atenção multivista; configuração padrão de 6 vistas candidatas com pesos por vista; (3) **bake** para UV (merge tipo graph-cut), super-resolução e **inpainting dos buracos**. Canais: 2.0 = RGB/albedo delightado (sem metallic/roughness); **2.1 = albedo + metallic + roughness; nenhuma versão aberta gera normal map** [FATO]. VRAM oficial do 2.1: **10 GB forma, 21 GB textura, 29 GB total** [FATO do README] — a textura **não roda nativamente** nos nossos 8.188 MB. Licença: **Tencent Hunyuan Community License — não é OSI; exclui UE, Reino Unido e Coreia do Sul**, inclusive para outputs [FATO] (o Brasil não está excluído; registro conforme LIC-01). [J] bom; [F] o melhor entre os gerativos (ReferenceNet + delighting foram feitos para grudar na entrada) — **mas é regeneração, não cópia de pixel**; [C] sim.

### 1.4 Coarse-to-fine em espaço UV — corrigir a costura onde ela mora

- **Paint3D (CVPR 2024)** [FATO: https://arxiv.org/html/2312.13913v2]: estágio coarse (difusão depth-aware multivista → fusão → textura grosseira com buracos e luz embutida) + refino com **dois difusores treinados no espaço UV**, condicionados por mapa de posição: **UV Inpainting** (preenche buracos ciente da forma) e **UVHD** (detalhe + **remove iluminação**). Saída 2K lighting-less, condicionável por texto **ou imagem**. [J] bom por outro caminho (a costura é corrigida já em UV); [F] não pixel-exato; [C] é o ponto forte explícito — a literatura chama as regiões não vistas de *"incomplete areas"* e a operação de **inpainting**: o próprio campo admite que textura de verso é pintura generativa sobre buraco, não transferência de dado.
- **TEXGen (SIGGRAPH Asia 2024, Best Paper Honorable Mention)** [FATO: https://arxiv.org/abs/2411.14740; repo CVMI-Lab/TEXGen]: difusor de 700M parâmetros treinado **diretamente no espaço UV**, feed-forward, intercalando convoluções no mapa UV com atenção sobre nuvem de pontos (é a atenção 3D que impede pintar nonsense através de uma costura UV). Suporta inpainting em UV e **completação a partir de vistas esparsas**. VRAM de inferência/teste: **24 GB** [FATO do repo] — **inviável na 4060**. [J] o melhor tratamento conceitual da costura UV; [F] não; [C] sim.

### 1.5 Materiais PBR completos — pintar todos os canais, sem luz embutida

- **DreamMat (TOG 2024)** [FATO: https://arxiv.org/html/2405.17176v1]: difusor fine-tunado ciente de geometria e luz (condicionado por depth/normal + ambientes HDR renderizados com materiais-cobaia), destilado (CSD) sob **luz de ambiente aleatória a cada passo** — o que muda com a luz não pode ser albedo. Saída albedo+roughness+metallic sem luz embutida (delighting por construção). Otimização por objeto, lenta como SDS. Resolve um 4º problema — **relighting correto** — que os demais ignoram.
- **Material Anything (CVPR 2025 Highlight)** [FATO: https://openaccess.thecvf.com/content/CVPR2025/papers/Huang_Material_Anything_Generating_Materials_for_Any_3D_Object_via_Diffusion_CVPR_2025_paper.pdf]: feed-forward, triple-head com rendering loss, e o truque central para nós: **confidence mask progressiva** — em cada região, decide **estimar/preservar** o material do que já existe ou **gerar** do zero, alternando até cobrir. Saída albedo+roughness+metallic+bump. Licença relatada como MIT no repo (conferir o `LICENSE` antes de uso comercial). [F] parcial e o mais interessante da família: em objeto que **já tem albedo**, a confiança manda preservar em vez de reinventar.
- **Família correlata (registro):** MaterialMVP (ICCV 2025, PBR multivista com Reference Attention), TexGaussian (CVPR 2025, regressão feed-forward via Gaussianos, muito mais rápido), MatFuse (materiais tileable editáveis — não é pintura de personagem).

### 1.6 O híbrido que [F] exige — e a lacuna na literatura

**[FATO/ANÁLISE]** A composição "**projeta a arte canônica onde ela é visível (com blending tipo fotogramétrico), trava essa região em `keep` absoluto, e chama difusão só para o complementar, com inpainting em UV**" **não foi encontrada montada e medida em nenhuma fonte primária desta pesquisa**. Os blocos existem, separados e citáveis: trimapa `keep` do TEXTure + projeção MRF/Poisson do mvs-texturing + UV inpainting do Paint3D + confidence mask do Material Anything. No mundo comercial manual, o Substance 3D Painter faz a metade projetiva (Projection/Stencil em screen-space, artista repete por ângulo, clone stamp nas costuras) [FATO: https://experienceleague.adobe.com/en/docs/substance-3d-painter/using/painting/paint-tools/projection] — [F] máximo sob controle humano, [C] manual. **A composição automática é espaço aberto** — e é a arquitetura que o nosso requisito de cânone pede (ver §7.4, o híbrido como terceira saída da comparação).

### 1.7 UltraTex — ATENÇÃO: há dois artefatos com o mesmo nome (divergência resolvida na §5.1)

- **O framework de pesquisa UltraTex** [FATO: repo oficial — https://github.com/yiboz2001/ultratex/blob/HEAD/README.md]: *"UltraTex: Unleashing 2K Multi-View Diffusion for 3D Texturing"* (SIGGRAPH Asia 2026, Zhang et al.), difusão multivista em **2048×2048** sobre G-buffers, com otimizações de eficiência (Background Token Dropping, Block-Sparse Attention, Foreground-Aware VAE Decoding), backbones **FLUX.1-dev e FLUX.2-Klein (4B/9B)** via LoRAs próprios (albedo e metallic-roughness), dataset TexVerse (351.847 assets). Código **MIT** [FATO do README]; **os backbones FLUX têm licença própria não-comercial (BFL)** — o MIT do código não libera o peso base. **O README oficial NÃO publica VRAM, nº de vistas nem tempo absoluto**; os speedups citados (22,3×–74,6× de inferência) são **sobre o baseline denso dos próprios autores** [ALEGAÇÃO dos autores, sem medição independente localizada]. Código/pesos liberados em 2026-10-03 — projeto recentíssimo, sem replicação independente.
- **O pacote ComfyUI de comunidade** (o que o spike T7 do projeto de fato preparou): workflows de terceiros (PixelArtistry/VisualBruno/Pinokio) com quantização **GGUF** que não faz parte do repo oficial; os números que circulam (6–10 vistas, atlas até 8192², pico ~6,8 GB, "roda em 6 GB") são **[ALEGAÇÃO de comunidade/fornecedor]**, a medir na nossa 4060 pelas réguas já pré-registradas do spike. Ver §5.1 para a reconciliação completa com o que os documentos internos do projeto diziam.

### 1.8 Comerciais de texturização (caixa-preta — método não público)

Para todos: **método interno não público**; o que consta é só o que a documentação/API estabelece — qualquer avaliação de [J]/[F]/[C] exige medição própria, não leitura de marketing.

- **Meshy (Retexture, Meshy-6/7)** [FATO: https://docs.meshy.ai/en/api/retexture]: malha + texto **ou** imagem de referência; 7 aceita multiview; resolução 2K/4K/8K; `enable_pbr` entrega base color + metallic + roughness + normal; Texture Edit repinta região sem refazer tudo. Licença proprietária; outputs do plano free sob CC BY 4.0 segundo o próprio site.
- **Tripo (texturing API)** [FATO: https://www.3daistudio.com/Platform/API/Documentation/texturing/tripo]: malha + prompt/imagem/multiview; `texture_quality` até **extreme = 8K**; `pbr` gera os 4 canais; parâmetro `texture_alignment: original_image | geometry`; a versão 3.2 expõe `lighting_removal` (delighting da referência). Método não público.
- **Rodin/Hyper3D (Deemos)** [FATO: https://docs.hyper3d.ai/en/api-specification/rodin-gen2]: foco é geração image/text-to-3D (até 5 imagens); materiais PBR (4 canais), Shaded, Hybrid; texturas até 12K citadas na linha Gen-2.5 por fontes secundárias.
- **Kaedim — correção** [FATO: https://www.kaedim3d.com/case-study/dynamic/upland]: **não é** ferramenta de texturização de malha existente; é conversão 2D→3D **com humano no loop** (artistas fazem QA/retopo). O "método" inclui trabalho humano — que é o que garante a fidelidade nos clientes deles.

### 1.9 Síntese da pergunta 1

| Família | [J] Junção | [F] Fidelidade à arte | [C] Não-visto | Cabe em 8.188 MB? |
|---|---|---|---|---|
| Projeção fotogramétrica (mvs-texturing/Meshroom) | ★★★ MRF+Poisson / multi-band | ★★★ onde há fonte | ☆ | Sim (sem difusão) |
| Iterativa (TEXTure/Text2Tex/InTeX) | ★ trimapa mitiga | ☆ redesenha | ★★★ | Limítrofe (classe SD) |
| Sincronizada (SyncMVD / Hunyuan Paint) | ★★☆ consenso na geração | ★☆ (ReferenceNet) | ★★★ | **Não** (Hunyuan textura = 21 GB, fato oficial) |
| UV direto (Paint3D / TEXGen) | ★★☆ corrige em UV | ☆ | ★★★ | Paint3D: medir; TEXGen **não** (24 GB, fato do repo) |
| Otimização SDS (Paint-it / DreamMat) | ★★★ mapa único | ☆ | ★★★ | Provável, mas 15 min+/objeto |
| PBR feed-forward (Material Anything) | ★★ | ★☆ preserva albedo existente | ★★★ | Não verificado |
| Projeção manual (Substance) | manual | ★★★ | manual | Sim |
| UltraTex oficial / pacote ComfyUI | ★★ multivista 2K | ★☆ regeneração | ★★ | Oficial: sem VRAM publicada; 6–8 GB = alegação GGUF de terceiro, **a medir no spike T7** |

---

## 2. Pergunta 2 — Várias referências de ângulos diferentes → UMA modelagem

### 2.0 As três filosofias (confundi-las é o erro mais comum)

1. **Gerar as vistas já concordando** (difusão multivista): as vistas são **desruidadas juntas**, trocando informação a cada passo. A consistência é construída na origem, nunca verificada depois.
2. **Fundir vistas num gargalo 3D aprendido** (reconstrução feed-forward): um transformer/U-Net recebe N vistas com pose conhecida e é forçado a cuspir **uma** representação 3D única (triplane, Gaussianos, latente SDF). Vistas que discordam são mediadas pelo *prior* aprendido em renders perfeitamente consistentes — a rede **não detecta a contradição; ela a alisa silenciosamente**.
3. **Provar geometricamente que concordam** (fotogrametria): correspondência explícita + otimização global (bundle adjustment) minimizando erro de reprojeção, com rejeição de outliers. É o único método que **mede** a inconsistência — e o único que **falha abertamente** quando ela é grande.

> **[ANÁLISE] Consequência direta para a Oficina:** nenhum método das famílias 1 e 2 "resolve" vistas contraditórias fornecidas pelo usuário. Eles foram desenhados para vistas que eles mesmos geraram sincronizadas, ou para renders de treino perfeitos. Alimentar 4 vistas aprovadas "pelo olhar" num reconstrutor feed-forward não produz verificação — produz um **compromisso plausível inventado pela rede**, sem aviso de onde inventou.

### 2.1 Difusão multivista — a escada de mecanismos de consistência

- **Zero123 (o fracasso-linha-de-base)** [FATO: citação no paper do Zero123++ — https://pdfs.assets.alphaxiv.org/2310.15110v1.pdf]: gera **uma** vista por execução, independentemente — *"leads to a breakdown in consistency between the generated views"*. É o problema de Janus e a deriva de conteúdo em estado puro.
- **Zero123++** [FATO: https://github.com/sudo-ai-3d/zero123plus/blob/HEAD/README.md]: emenda as 6 vistas numa **grade única 3×2** (azimutes 30/90/150/210/270/330°) e modela a distribuição conjunta — o U-Net "vê" todas as vistas ao mesmo tempo porque são a mesma imagem. Exemplo do README requer ~5 GB [FATO]. **Armadilha de licença: código Apache-2.0, pesos CC-BY-NC 4.0 (não-comercial)** [FATO do README] — outputs livres, modelo não pode entrar em pipeline de produto comercial.
- **MVDream** (ByteDance, ICLR 2024) [FATO: https://arxiv.org/html/2308.16512v4]: texto → 4 vistas ortogonais; a peça canônica é a **atenção "3D"**: queries de uma vista atendem a keys/values de **todas** as vistas; câmera como embedding MLP. Ablação do paper: 1 vista = Janus grave; 4 vistas = *"barely suffers from any multiview consistency issues"*.
- **SyncDreamer** (ICLR 2024) [FATO: https://ar5iv.labs.arxiv.org/html/2309.03453]: N preditores de ruído **compartilham estado a cada passo** (distribuição conjunta, não N condicionais); atenção por **volume de frustum 3D-aware** que correlaciona features ao longo das linhas epipolares aproximadas. Gera 16 vistas; a malha vem de NeuS otimizado (~10 min no apêndice) — **não é feed-forward**.
- **ImageDream / MultiImageDream**: MVDream condicionado por imagem (controlador multinível estilo IP-Adapter); o MultiImageDream (arXiv:2404.17419) alimenta a saída multivista de volta como prompt multi-imagem — um dos poucos trabalhos com "várias imagens de entrada" na difusão, mas as imagens são geradas pela própria rede, não fornecidas por humano.
- **Wonder3D / Wonder3D++** (CVPR 2024) [FATO: arXiv:2310.15008; ++: https://arxiv.org/html/2511.01767v1]: difusão **cross-domain** — gera, para 6 vistas, **RGB + mapas de normal** acoplados por atenção cross-view **e** cross-domain (a normal ancora a geometria mesmo se a cor divergir); malha por **fusão de normais geometry-aware** (SDF implícito), ~2–3 min. Licença: fontes secundárias **divergem** (MIT × AGPL-3.0) — **não verificada; conferir o `LICENSE` do repo antes de qualquer adoção** [pendência declarada].
- **SV3D** (Stability, ECCV 2024) [FATO: https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/00150.pdf]: a órbita vira **vídeo** — difusão de vídeo latente gera 21 frames a 576×576; a consistência temporal do vídeo vira consistência multivista. O próprio paper usa *masked SDS* para as regiões que nem as 21 vistas cobrem — admissão explícita de que completação continua existindo a jusante. VRAM oficial não publicada; difusão de vídeo é o item mais pesado da família — assumir >8 GB até medição.
- **Era3D** (NeurIPS 2024) [FATO: https://arxiv.org/pdf/2405.11616]: difusão multivista em 512×512 com **atenção por linha (row-wise)** — no arranjo canônico, linhas epipolares coincidem com linhas da imagem, então cada linha só atende às mesmas linhas das outras vistas: prior epipolar embutido com custo ~12× menor que atenção densa (quantificação de complexidade do paper, não de VRAM). Estima focal/elevação da foto de entrada por difusão.

**Síntese [ANÁLISE]:** a escada de força do mecanismo é: nenhum (Zero123) → mesma grade (Zero123++) → atenção global entre vistas (MVDream/Wonder3D) → atenção restrita pela geometria epipolar (SyncDreamer/Era3D) → coerência temporal de vídeo (SV3D). Quanto mais geométrico o mecanismo, menos a rede precisa "decorar" consistência.

### 2.2 Reconstrução feed-forward — o gargalo substitui a verificação

Padrão: encoder (DINO/ViT) → decoder produz representação 3D → extração de malha. Treino sempre com renders de objetos reais (Objaverse, ~0,4–1M): a rede aprende como vistas consistentes se fundem **e** como um objeto plausível deve ser onde ninguém viu.

- **LRM / OpenLRM** (arXiv:2311.04400): transformer de 500M de parâmetros projeta features 2D num **triplane** via cross-attention; MLP decodifica NeRF. **Single-view por desenho** (vistas extras são só supervisão no treino). O LRM original nunca liberou código; OpenLRM (Apache-2.0) declara **mínimo de 8 GB para inferência** [FATO via DeepWiki do repo] — igual ao nosso teto.
- **InstantMesh** (Tencent ARC, arXiv:2404.07191): Zero123++ afinado (fundo branco — o fundo cinza variável gerava "floaters") + **sparse-view LRM** + FlexiCubes, ~10 s no total [ALEGAÇÃO dos autores]. Documentação de instalação recomenda **≥16 GB** [FATO] — **não cabe como documentado**; offload sequencial de estágios é engenharia de terceiros, a medir.
- **LGM** (ECCV 2024) [FATO: https://arxiv.org/html/2402.05054v1]: U-Net assimétrico funde **4 vistas com pose conhecida** (embeddings de raio Plücker) em até 65.536 Gaussianos pixel-alinhados; cross-view self-attention nas camadas profundas; Gaussianos contraditórios são punidos no treino via renderização de vistas novas. Checkpoint pequeno (~0,83 GB, levantamento de porting) — o gargalo de VRAM é a difusão da frente, não o reconstrutor.
- **GRM** (ECCV 2024) [FATO: https://arxiv.org/html/2403.14621v1]: transformer puro, 4 vistas → Gaussianos desprojetados, reconstrução em ~0,1 s. E traz **a confissão mais útil desta pesquisa**, citação direta da Discussion: *"The output quality of our sparse-view reconstructor suffers when the input views are inconsistent. The reconstructor is deterministic in nature"* — admissão formal de que o reconstrutor feed-forward **não tem mecanismo** para inconsistência: ele degrada.
- **CRM** (ECCV 2024) [FATO: https://ar5iv.labs.arxiv.org/html/2403.05034]: um triplane desenrolado **é** espacialmente correspondente a 6 imagens ortográficas — então a difusão gera as 6 vistas **+ Canonical Coordinate Maps** e um U-Net **convolucional** explora o alinhamento pixel-a-pixel (o CCM diz a cada pixel que ponto do espaço canônico ele é). Consistência **geométrica por construção**, o oposto do LRM (que precisa aprender o alinhamento via atenção). ~10 s (medido em A800, paper).
- **Unique3D + ISOMER** (arXiv:2405.20343): difusão multivista (4 vistas) + difusão de normais + o algoritmo ISOMER, que **[FATO] *"directly handles the case where the global normal of the same vertex is inconsistent across viewpoints"*** — o exemplo mais próximo, na literatura feed-forward, de fusão robusta a vistas que discordam. Ainda assim: robustez a **ruído de normal**, não a um cinturão desenhado em duas alturas.
- **VGGT** (Oxford VGG + Meta, CVPR 2025 Best Paper, arXiv:2503.11651) [FATO]: transformer que, de 1 a centenas de imagens **não posadas**, regrede em uma passada câmeras, profundidade, **pointmaps** densos e trilhas — sem bundle adjustment. Licença dividida: código com uso comercial permitido (atualização jul/2025); checkpoint default **VGGT-1B não-comercial**, checkpoint Commercial mediante aprovação. Teste independente relatou **não caber em 12 GB** no pipeline default (a atenção global cresce quadraticamente com nº de vistas) — com 4–8 vistas em bf16 é **plausível** em 8 GB, mas é estimativa, exige teste local. **Não é motor de forma** (saída é nuvem de pontos + câmeras, sem prior de objeto); **serve como instrumento de diagnóstico** (§2.5).

### 2.3 Quem aceita DIRETAMENTE as vistas do usuário? (o nosso caso)

A maioria dos pipelines famosos **não** aceita: aceita 1 imagem e gera as próprias vistas, em poses fixas. Aceitar vistas arbitrárias do usuário é exceção. Quadro decisivo:

| Motor | Aceita vistas do usuário? | Quantas/quais | Pose | Como funde | Forma em 8.188 MB? |
|---|---|---|---|---|---|
| **Hunyuan3D-2mv (+Turbo)** | **Sim, nativamente** | 1–4 **nomeadas**: front/left/back/right | Implícita no slot | Condicionamento do DiT de forma (prior generativo) | **Sim** — 6 GB declarados p/ forma na família 2.0 [FATO] |
| Hunyuan3D-2.1 shape | Não (1 imagem) | 1 | — | DiT single-image | **Não** — 10 GB oficiais [FATO] |
| TRELLIS-image | Sim, tuning-free | N imagens | Não usa com rigor | Features DINOv2 → SLAT único | Não no padrão (~16 GB) [FATO do README] |
| LGM / GRM | Tecnicamente sim | 4 ortogonais | Conhecida, fixa | U-Net/Transformer → Gaussianos | LGM provável; GRM não instalável de imediato |
| InstantMesh / CRM (reconstrutor) | Tecnicamente sim | 6 fixas | Conhecida, fixa (poses do Zero123++) | Triplane + FlexiCubes | Não (InstantMesh: 16 GB documentados) |
| VGGT | Sim (outro problema) | 1–centenas | **Estima** | Pointmaps em referencial único | Limítrofe p/ poucas vistas; saída ≠ malha |
| COLMAP/Meshroom | Sim (fotogrametria) | Dezenas+, com sobreposição | **Estima + otimiza** | Matching + BA + MVS/TSDF | CPU/GPU modesto — mas exige objeto físico consistente |
| TripoSG / PartCrafter | Não | 1 | — | Latente 3D direto | TripoSG: borda dos 8 GB (§3) |

**Hunyuan3D-2mv em detalhe** [FATO: repo Tencent-Hunyuan/Hunyuan3D-2 — https://github.com/Tencent-Hunyuan/Hunyuan3D-2; exemplo oficial `examples/shape_gen_multiview.py`]: checkpoint separado da família 2.0 (lançado 18/mar/2025, 1,1B de parâmetros, com variantes **-Turbo** step-distilled e -Fast). A entrada é um dicionário de slots semânticos — `front` obrigatória; `left`, `back`, `right` opcionais; **omitir um slot não renumera os outros**; **diagonais não têm slot**. Não se fornece matriz de câmera: a pose está implícita no nome. Fusão: cada imagem é codificada (DINOv2) e entra como condicionamento por cross-attention do DiT de forma (flow-matching sobre latentes ShapeVAE) — **não há triangulação nem média de SDF**: contradição entre vistas vira disputa dentro do prior generativo, e a forma final é a mais "provável" dados os condicionamentos, não a interseção geométrica deles [ANÁLISE a partir da arquitetura publicada]. VRAM: a família 2.0 declara **6 GB para forma** (16 GB forma+textura) [FATO do README] — a textura/Paint é etapa separada, com a forma descarregada, ou fora da 4060.

> **Identificação do nosso "mv-turbo" [ANÁLISE com alta probabilidade]:** o motor que o projeto já roda sob o nome "mv-turbo" corresponde, pela descrição e pelo nome, ao **`Hunyuan3D-DiT-v2-mv-Turbo`** — mesma entrada em dict de slots, amostragem destilada (5–8 passos em vez de 30), registrada na bateria dourada do projeto com forma do Orc em ≤41,4 s e pico de 6.435 MB (medido pelo projeto). **Confirmar a identidade no spike é um item de verificação de 5 minutos** (ler o nome do checkpoint na instalação) — se confirmado, a rota A de forma **já está instalada e medida**, e o debate A×B muda de "o que baixar" para "como alimentar e validar".

**Correlato na pintura [FATO]:** o Hunyuan3D-**Paint** também usa "multiview" — mas internamente (renderiza a malha pronta e gera a textura). Não confundir os dois usos da palavra nos READMEs: entrada multivista de **forma** é só o 2mv.

### 2.4 Fotogrametria — a referência de método, e por que não transfere

Pipeline COLMAP/Meshroom [FATO: docs do projeto COLMAP; síntese em https://www.preprints.org/manuscript/202504.0989]: (1) features (SIFT) casadas entre fotos com **verificação geométrica** (RANSAC epipolar) descartando o que nenhum par de câmeras explica; (2) **SfM + bundle adjustment**: poses e pontos 3D resolvidos juntos, minimizando o **erro de reprojeção total** com perdas robustas — a consistência é a função-objetivo; (3) **MVS/PatchMatch**: profundidade por vista só sobrevive se vistas vizinhas concordarem ao reprojetá-la; (4) fusão em nuvem/TSDF.

**Por que não transfere para ilustrações geradas [ANÁLISE sustentada nos pressupostos]:** SfM pressupõe **um objeto físico único** do qual todas as imagens são projeções. Nas vistas aprovadas pelo olhar, esse objeto **não existe**: cada vista é uma invenção 2D separada. Sem ponto físico, o SIFT casa desenhos parecidos (ou nada); o BA ou não converge, ou converge para câmeras/nuvem distorcidas que "explicam" casamentos falsos. Somam-se violações extras: projeção não-pinhole ("perspectiva artística"), escala de partes não rígida entre vistas, iluminação pintada que muda com o ângulo (quebra a consistência fotométrica do MVS). **A fotogrametria é honesta: denuncia a inconsistência falhando — mas não entrega a malha.** Uso correto aqui: **medidor**, não motor (§2.5).

### 2.5 Fusão de vistas — onde cada método quebra quando as vistas discordam

- **TSDF / fusão de profundidades** (média ponderada truncada; KinectFusion, `stereo_fusion` do COLMAP): média **não é voto**. Se a frente põe o cinturão em z=0 e a lateral o implica em z=+3 cm, o TSDF cria **superfície fantasma intermediária** — um cinturão "engordado" que não está em vista nenhuma. Outliers com peso alto viram geometria real.
- **Média de SDF / fusão de normais** (mínimos quadrados sobre todas as vistas; Wonder3D, NeuS, ISOMER): contradição estrutural vira **compromisso** — a superfície vai para o meio do caminho e perde o detalhe nítido das duas evidências. Pesos ajudam contra ruído aleatório, não contra duas vistas sistematicamente diferentes (ambas têm confiança alta).
- **Visual hull / interseção de silhuetas**: AND lógico — o mais frágil. **Uma** silhueta errada escava volume verdadeiro; e mesmo com silhuetas perfeitas, nunca recupera concavidades e pode conter volumes fantasmas compatíveis com todas elas. Com vistas contraditórias, a interseção pode ficar vazia ou mutilada.
- **Votação (k-de-N)**: mais robusta que os três contra **minoria** errada. Mas com **4 vistas**, maioria é 3-contra-1 no máximo; se frente+costas discordam das laterais (2×2), o voto empata — e o desempate volta a ser um prior (aprendido ou humano).

### 2.6 O problema da inconsistência 2D — a resposta honesta

**Fato do projeto:** as 4 vistas canônicas (+ diagonais) foram aprovadas por qualidade visual individual, não por consistência geométrica mútua (a crítica C-05 do estudo D1 já apontou a falta deste teste). Um cinturão pode estar numa altura na frente e noutra na lateral.

**O que a literatura faz com isso, por família:**
1. **Geração sincronizada resolve na origem — não se aplica ao nosso caso.** Usar Zero123++/SV3D/Era3D a partir de uma das nossas vistas significa **descartar as outras** e reinventar o personagem — perde-se exatamente o controle que as 4 vistas aprovadas davam.
2. **Reconstrução feed-forward ignora/media silenciosamente** (GRM, §2.2). No exemplo do cinturão: o DiT do 2mv amostrará a altura **mais provável sob o prior** dados os 4 condicionamentos — que pode não ser nenhuma das duas alturas desenhadas — sem relatório do ocorrido. Resultado plausível e limpo, não fiel.
3. **Reconstrução robusta clássica rejeita outliers — exige maioria consistente e correspondências detectáveis.** Com 4 desenhos estilizados, as duas premissas são fracas.
4. **Ninguém resolve de verdade [ANÁLISE]:** não foi encontrado, nas fontes primárias consultadas, método publicado que receba vistas 2D **mutuamente contraditórias em estrutura** (não em ruído) e produza a forma "correta" — porque "correta" está **indefinido**: frente e lateral não podem estar ambas certas sobre a altura do cinturão. Toda saída é uma **decisão** — tomada pelo prior da rede, por um peso de confiança, ou por um humano. A literatura trata inconsistência como ruído a robustecer, nunca como **contradição editorial a arbitrar**.

**Mitigações práticas [ANÁLISE] — incorporadas ao desenho da rota A (§§6–7):**
- **(i) Vista-hero e auditoria de marcos (o D-H0 que falta):** antes de reconstruir, medir a concordância 2D entre as vistas nos marcos mensuráveis (alturas relativas de cinturão/ombro/joelho/cabeça, em % da altura total, entre pares adjacentes). Vista que discorda da maioria vira candidata a correção 2D ou a rebaixamento de autoridade — decisão registrada, não silenciosa.
- **(ii) Diagnóstico geométrico barato:** rodar **VGGT ou COLMAP** sobre o conjunto de vistas e registrar matching/erro de reprojeção/confiança como **painel de consistência do lote de referências**. Em ilustração estilizada, as poses estimadas podem simplesmente falhar — e essa falha também é diagnóstico (a vista não pertence ao mesmo objeto geométrico das outras).
- **(iii) Diagonais como testemunhas:** um marco visível em frente+diagonal+lateral tem 3 evidências; divergência 1-contra-2 localiza a vista suspeita para o Mestre arbitrar. (As diagonais não entram no 2mv — sem slot — mas entram neste tribunal e na pintura.)
- **(iv) Registro honesto da rota:** se a forma vier do 2mv direto das 4 vistas sem correção, registrar no projeto que ela é **interpretação do modelo** das referências, validada por medição de marcos na malha (§7) — nunca apresentá-la como "reconstrução fiel das vistas".

---

## 3. Pergunta 3 — Uma referência só, e o app completa o resto

### 3.0 O fato matemático por trás

**[ANÁLISE]** Nenhuma rota de 1 imagem "reconstrói" o verso: ela **amostra** um verso plausível de uma distribuição aprendida. A imagem é uma projeção 2D que destrói profundidade e tudo o que está ocluso — existe uma família infinita de formas 3D compatíveis com ela. O que muda entre os métodos é só **onde** a invenção acontece: (A) dentro de uma rede feed-forward treinada em ~1M de objetos; (B) numa difusão multivista que primeiro *desenha* as vistas que faltam e depois reconstrói a partir dos desenhos; (C) numa otimização guiada por prior de difusão 2D (SDS). **Em todos os casos, o verso é geração, não recuperação** — e detalhe assimétrico que só existe no verso tem probabilidade de acerto igual à sua frequência no prior da categoria.

O paper fundador diz sem rodeio [FATO: LRM, arXiv:2311.04400 — https://arxiv.org/pdf/2311.04400]: treinado end-to-end em ~1 milhão de objetos (Objaverse + MVImgNet) para regressar um NeRF a partir de 1 imagem em 5 s — **o conhecimento do invisível vem do dataset, não da imagem**.

### 3.1 Família A — feed-forward direto (o prior é um prior de forma 3D nativo)

- **LRM (2023):** DINO → decoder transformer projeta features num **triplane** → NeRF. ~5 s. O triplane inteiro, incluindo o lado oposto, sai de uma passada. O verso tende a **borrar**: a regressão minimiza erro médio sobre o dataset — sai o "verso médio da categoria". Sem release oficial; usa-se via descendentes.
- **TripoSR (Tripo AI + Stability, 2024)** [FATO: README oficial — https://github.com/vast-ai-research/triposr/blob/HEAD/README.md]: descendente do LRM otimizado para velocidade (<0,5 s em A100, paper); saída com cores de vértice, **sem PBR e sem UV de verdade**. VRAM padrão **~6 GB** [FATO do README] — **cabe**. Licença **MIT para código e pesos** [FATO] — a mais limpa da lista. Não aceita multivista: as 4 vistas reais **não têm onde entrar**.
- **SF3D / Stable Fast 3D (Stability, 2024)** [FATO: https://github.com/stability-ai/stable-fast-3d/blob/HEAD/README.md]: TripoSR redesenhado para entregar malha de verdade — estimativa de material, *delighting*, **UV-unwrapping rápido** e textura em UV, 0,3–0,5 s. VRAM **~6 GB** [FATO do README] — **cabe**. Licença **Stability AI Community License**: comercial só até US$ 1M/ano de receita; pesos gated no HF [FATO]. **Agravante de cânone [ANÁLISE]:** o verso ganha textura UV *apresentável e inventada* — pior para nós que um verso obviamente borrado, porque **parece intencional**. E o delighting pode apagar detalhe pintado de verdade se ele parecer sombra.
- **TripoSG (VAST, 2025) — correção de premissa** [FATO: model card — https://github.com/mrforexample/comfyui-3d-pack/blob/HEAD/Checkpoints/Diffusers/VAST-AI/TripoSG/README.md; paper arXiv:2502.06608]: **não usa difusão multivista interna**. Consome **1 imagem** e gera **só geometria**: VAE-SDF + transformer de **rectified flow** de 1,5B de parâmetros sobre 2.048 tokens latentes, condicionado por CLIP+DINOv2. É difusão **no espaço latente 3D**, não em imagens. **Não produz textura.** VRAM: o model card exige **">8 GB"** → nos nossos 8.188 MB é **limítrofe/não garantido** (terceiros reportam ~8 GB na prática) — tratar como "exige medição de pico local", nunca como "cabe". Licença **MIT** [FATO]. A forma é uma **amostra** coerente e fechada do prior (não uma média borrada) — vantagem de qualidade, mesmo risco de conteúdo: proporções e apêndices do verso saem do prior.
- **Hunyuan3D-2.1 shape** [FATO: repo oficial — §2.3]: DiT de flow de 3,3B + ShapeVAE condicionado pela imagem; o Paint separado (2B) gera as vistas da malha a partir da referência e faz bake PBR até 4K. Ou seja, **mesmo no Hunyuan, a textura do verso é gerada a partir de vistas que o próprio Paint inventa** (config padrão `max_num_view=6, resolution=512`). Forma sozinha: **10 GB — não cabe**; e a versão single **não usa** nossas 4 vistas (quem usa é o irmão 2mv).

### 3.2 Família B — dois tempos: desenhar as vistas que faltam, depois reconstruir

**[ANÁLISE] A vantagem estrutural decisiva desta família para nós:** a invenção vira um **artefato inspecionável e editável**. Dá para ver, rejeitar, regenerar ou **substituir** a vista de costas inventada por uma vista real **antes** da reconstrução. É a única família em que a alucinação tem uma "porta" de intervenção — e é a ponte natural para a rota híbrida (§7.4).

- **Geradores de vistas:** Zero123++ (§2.1 — 6 vistas conjuntas em grade; atenção à licença dos pesos, CC-BY-NC) e **SV3D** (§2.1 — 21 frames orbitais por difusão de vídeo; o paper admite usar masked SDS justamente nas regiões que as vistas não cobrem). **Wonder3D** (§2.1) inventa a geometria do verso **duas vezes de forma consistente** — cor e normal acopladas — e a malha sai por fusão de normais; só 6 vistas → estruturas finas e oclusões severas sofrem (limitação declarada na literatura).
- **InstantMesh** (§2.2): Zero123++ → sparse-view LRM + FlexiCubes, ~10 s. O reconstrutor foi treinado com vistas **reais** — alimentá-lo com vistas reais no lugar das geradas é uso arquiteturalmente previsto (ver evidência 2 em §3.5).
- **CRM** (§2.2): 6 vistas ortográficas + CCMs → U-Net convolucional → FlexiCubes. Também aceita, por arquitetura, vistas ortográficas reais.
- **One-2-3-45++**: geração conjunta de 6 vistas + **difusão 3D nativa** — invenção em cascata dupla: a difusão 2D inventa as vistas, a difusão 3D inventa de novo ao interpretá-las; dois priors multiplicam a deriva.
- **LGM** (§2.2): o reconstrutor das 4 vistas cuja ablação é a evidência 1 abaixo.

### 3.3 Família C — otimização por prior (SDS e herdeiros): dominada

[FATO] **DreamFusion (2022)** introduz o SDS: renderiza a forma em formação de ângulos aleatórios e usa o gradiente de uma difusão 2D para empurrar cada render em direção a "imagem plausível". O modo de falha tem nome: **problema de Janus** — a difusão 2D é enviesada para vistas frontais "bonitas", então a otimização replica features da frente no verso (um urso com cara na frente **e** atrás), além de sobresaturação e oversmoothing [FATO, documentado p.ex. em HeadArtist — https://arxiv.org/html/2312.07539v2/]. Frequências medidas: Janus em **69%** (DreamFusion), **69%** (Magic3D), **87%** (DreamGaussian isolado), caindo para **8%** só quando combinado a prior multivista (MVDream) [FATO: https://arxiv.org/pdf/2402.18780 citado pela frente de rotas alternativas]. **Magic123** [FATO] combina prior 2D + prior 3D com um parâmetro explícito que os autores descrevem como o trade-off **imaginação × precisão** — a confissão formal do campo: nesta rota, imaginação e fidelidade são o mesmo botão em direções opostas; custo ~60 min/objeto. **DreamGaussian** reduz a ~2 min [ALEGAÇÃO dos autores: <8 GB numa V100 — a medir; e os trabalhos seguintes apontam *"significant blurriness to the unseen areas"*].

**[ANÁLISE]** Para a Oficina esta família está **dominada**: mais lenta, sem porta de inspeção do verso, e com o pior modo de falha exatamente no eixo frente→costas. Fica no mapa por completude, não como candidata.

### 3.4 Os priors que preenchem o invisível

1. **Prior de categoria (o dominante).** Treino em Objaverse/Objaverse-XL: "humanoides têm costas típicas" significa que, dado o contorno da frente, a amostra mais provável de costas é pele/armadura/capa **genérica, sem acessórios raros**. O prior é uma moda estatística — ele **apaga sistematicamente o que é autoral**, porque o autoral é, por definição, o improvável.
2. **Simetria bilateral — ajuda no eixo errado.** Há métodos que a impõem explicitamente (espelhar features pelo plano de simetria) e ela está embutida nos dados (a maioria dos personagens de treino é quase simétrica). Para um personagem visto **de frente**, os dois lados já aparecem — a simetria quase não é necessária e **nada diz sobre o eixo que importa (frente↔costas)**. Onde é aplicada ao volume, pode ainda espelhar detalhe assimétrico para onde não devia.
3. **Inpainting em espaço UV (Paint3D, §1.4):** a formalização honesta da completação de textura — buraco nomeado, preenchimento generativo treinado para **consistência semântica**, não para verdade.

### 3.5 Evidência comparativa publicada — o que se mede ao adicionar vistas

**Aviso metodológico [FATO]:** escalas de Chamfer Distance **não são comparáveis entre papers** (normalizações diferentes). Só valem comparações **dentro** da mesma tabela.

- **Evidência 1 — a ablação mais direta (LGM, ECCV 2024)** [FATO: https://arxiv.org/html/2402.05054v1, §4.4]: o mesmo reconstrutor treinado com **1 vista** vs **4 vistas**: o de 1 vista *"can reconstruct faithful front-view, but fails to distinguish the back view and results in blurriness"*. Experimento controlado dos próprios autores, isolando o número de vistas.
- **Evidência 2 — vistas reais vs geradas, mesmo reconstrutor (Freeplane, 2024)** [FATO: https://arxiv.org/html/2406.00750v1]: malhas de CRM/InstantMesh alimentados com vistas multivista **ground-truth** vs **geradas por difusão**: as GT produzem malhas "lisas e detalhadas"; as geradas, com suas inconsistências, degradam visivelmente a superfície. Conclusão dos autores: **o gargalo é a inconsistência das vistas inventadas, não o reconstrutor**. Corolário direto: **substituir vista inventada por vista real ataca o gargalo medido** — é a base empírica da rota A e do híbrido.
- **Evidência 3 — dois tempos vs direto, mesma régua (MeshFormer, arXiv:2408.10198, Tabela 1; GSO, n=1.030)** [FATO: https://arxiv.org/pdf/2408.10198]: TripoSR (direto) F-Score 0,896 / Chamfer 0,047 / PSNR 19,85; CRM (dois tempos) 0,886 / 0,051 / 19,99; InstantMesh 0,934 / 0,037 / 20,90; One-2-3-45++ 0,936 / 0,039 / 20,97. **Leitura honesta [ANÁLISE]:** o ganho dos dois tempos sobre o direto existe mas é **modesto e não uniforme** (InstantMesh: −21% de Chamfer vs TripoSR; o CRM fica **pior** que o TripoSR nesta tabela). Adicionar vistas **inventadas** não é vitória garantida.
- **Evidência 4 — outra régua, mesma direção (Unique3D, arXiv:2405.20343, Tabela 1; GSO)** [FATO]: OpenLRM (direto) CD 0,0229 / F-score 0,5907; Wonder3D 0,0184 / 0,6513; InstantMesh 0,0164 / 0,6421; CRM 0,0156 / 0,6697 — ~**30% menos Chamfer** dos dois tempos vs o LRM direto, na régua deste paper.
- **Evidência 5 — o teto do SDS (tabela em CraftsMan3D, GSO)** [FATO]: Magic123 CD 0,0516 / IoU 0,4528 a ~60 min/objeto; InstantMesh CD 0,0187 / IoU 0,6353 a ~10 s. A rota de otimização por prior é **simultaneamente a mais lenta e das menos fiéis** às réguas geométricas.
- **O que a literatura NÃO mede [ANÁLISE]:** nenhum benchmark pontua **fidelidade de detalhe canônico no verso** (capa de lobo certa/errada). GSO/Objaverse medem objetos genéricos contra GT geométrico, com o verso diluído na média global. Um modelo pode ganhar em Chamfer médio e apagar 100% dos elementos-assinatura das costas. **Ausência de métrica ≠ ausência do problema** — por isso o desenho da comparação (§7) inclui um placar próprio para elementos-assinatura.

### 3.6 O caso concreto do Orc — referência só de frente

**[ANÁLISE — quantificação qualitativa do risco, elemento a elemento, a partir de como os métodos funcionam]**

| Elemento | O que a frente mostra | O que a rota B entrega no verso | Risco |
|---|---|---|---|
| Superfície total | ~metade da área (hemisfério frontal) | A outra metade é 100% amostra do prior | **Estrutural** — não é "risco de erro": é ausência de dado em ~50% do asset |
| Capa de lobo (geometria) | No máximo bordas na silhueta lateral e sobre os ombros | Se a silhueta sugerir "algo atrás", um volume de capa/pano genérico; se não sugerir, costas nuas/armadura. A **cabeça do lobo** como adorno dorsal: frequência ~zero no prior de "orc" → **não será gerada** | **ALTO — perda quase certa do elemento-assinatura** |
| Capa de lobo (textura) | Nada do pelo/padrão do verso | Pelo genérico marrom/cinza, couro, ou continuação do material do peito — plausível, **não canônico** | **ALTO** |
| Cinturão de crânios | A parte frontal (visível) é reproduzível | A continuação posterior — número, tamanho e espaçamento dos crânios — é inventada: o prior tende a continuar o padrão com **período errado**, trocar crânios por fivela/couro, ou **interromper o cinturão** | **MÉDIO-ALTO** |
| Detalhes assimétricos da frente (cicatriz, ombreira desigual, arma num lado) | Visíveis | Em rotas SDS/multivista, risco de **vazamento para o verso** (Janus atenuado) ou de "correção" simétrica pelo prior | **MÉDIO** |
| Paleta/materiais gerais (pele, couro, metal) | Bem ancorados pela frente | Tendem a continuar corretamente — é o que o prior faz bem | **BAIXO** |

**Síntese do caso:** com 1 referência de frente, o Orc resultante é um orc **correto de frente, genérico de costas, e errado exatamente nos elementos que o tornam *este* Orc**. E o erro é **silencioso**: o verso sai limpo, fechado e renderizável — nada no output sinaliza que é invenção. Para um projeto com cânone (o Mestre é a autoridade final e o verso **é** cânone), isso classifica a rota B como **geradora de rascunho/protótipo**, não de asset final, sempre que o verso carregar design.

### 3.7 Mitigações reais (a ponte para o híbrido)

- **Condicionar pelo verso quando ele existe:** o **Hunyuan3D-2mv** (§2.3) é a prova, dentro da própria família Hunyuan, de que o fornecedor trata single-view como insuficiente para verso fiel: existindo a vista de costas, ela entra como condição e o verso deixa de ser amostra livre.
- **Reconstrutores alimentados com vistas reais** (InstantMesh/CRM/LGM): a troca de vistas geradas por reais é uso previsto — e a Evidência 2 mede o ganho.
- **Inspeção do estágio intermediário (só na Família B):** rejeitar/regenerar/**editar** a vista de costas antes de reconstruir — inclusive compor nela o elemento canônico. Única mitigação que não exige trocar de backend.
- **O que NÃO mitiga [ANÁLISE]:** trocar a seed (amostra nova = invenção nova, não mais certa); aumentar a resolução da textura (invenção em 4K continua invenção); pós-processar no Blender sem referência (move o erro, não o corrige).

### 3.8 Veredito de VRAM da rota single-view (teto 8.188 MB)

| Método | VRAM (fonte) | No teto? |
|---|---|---|
| TripoSR | ~6 GB (README oficial) | ✅ cabe |
| SF3D | ~6 GB (README oficial) | ✅ cabe (licença com teto de receita; pesos gated) |
| Zero123++ (só o estágio de vistas) | ~5 GB (README oficial) | ✅ cabe — pesos **CC-BY-NC** |
| TripoSG | ">8 GB" (model card) | ⚠️ **limítrofe** — sem folga; medição de pico local obrigatória |
| InstantMesh | ≥16 GB recomendados (docs) | ❌ como documentado; offload sequencial é workaround de terceiros |
| Hunyuan3D-2.1 shape | 10 GB (repo oficial) | ❌ só a forma já estoura |
| Wonder3D / CRM / SV3D / Magic123 | não publicado oficialmente | ❓ não afirmar — medir antes de adotar |

---

## 4. Pergunta 4 — Existe OUTRO jeito?

Resposta curta [ANÁLISE sobre os fatos]: existem **3 famílias realmente distintas** das duas rotas em debate, **2 multiplicadores** e **1 falsa via**. E uma delas — a pintura desacoplada da forma — não é bem "outra rota": é a formalização do híbrido que as §§1.6 e 3.7 já apontavam, e a peça mais aproveitável deste mapa inteiro.

### 4.1 Radiância → malha (NeRF / Gaussian Splatting como intermediário)

**Como funciona:** treina-se um campo de radiância (NeRF) ou um conjunto de Gaussianos 3D a partir de **dezenas de imagens posadas**; depois extrai-se a malha — marching cubes/tetrahedra sobre densidade ou SDF (variantes SDF como NeuS/VolSDF dão superfície muito mais limpa), ou, para splats, SuGaR (Poisson sobre Gaussianos achatados à superfície), 2DGS (TSDF sobre depth maps), Gaussian Opacity Fields (marching tetrahedra sobre campo de opacidade), GS2Mesh (estéreo sobre renders dos splats — **não** extrai geometria das Gaussianas diretamente), MILo (extração diferenciável dentro do loop, sucessor do SuGaR pelos mesmos autores) [FATO: páginas/papers oficiais de cada projeto].

**O problema da textura nesta família [FATO/ANÁLISE]:** NeRF **não tem textura UV** — a cor vive no campo, dependente do ângulo (o especular está "cozido" na radiância). Ao passar para malha há só 3 saídas: **cor por vértice** (resolução da "textura" = densidade da malha → pintura borrada em malha leve), **bake para UV** (renderizar de muitas vistas e projetar — é preciso colapsar um ângulo por texel; especular vira albedo falso) ou **decomposição difuso/especular** (Nerf2Mesh, ICCV 2023, MIT [FATO: https://github.com/ashawkey/nerf2mesh]). Em splats, a cor vive em harmônicos esféricos por Gaussiana (48 coeficientes SH de 59 números por splat [FATO: https://www.ultralytics.com/glossary/gaussian-splatting]) — ao assar para UV perde-se a dependência de vista e borra-se o detalhe fino. **Uma textura UV clássica desacopla resolução de pintura de densidade geométrica; vertex color e bake de splat, não.**

**Fatos de viabilidade:**
- **Instant-NGP** [FATO: https://github.com/NVlabs/instant-ngp]: treino rápido e conversão NeRF→Mesh incluída, mas a malha é subproduto (topologia de marching cubes, sem edge flow, exige retopo); relatos de mínimo 4 GB / recomendado ≥8 GB de VRAM; **licença NVIDIA Source Code License-NC — não-comercial** [FATO].
- **Nerfstudio** (Nerfacto) é **Apache-2.0** e exporta malha via TSDF/Poisson [FATO: https://ar5iv.labs.arxiv.org/html/2302.04264] — a base licenciável da família NeRF; o `gsplat` do Nerfstudio é reimplementação **Apache-2.0** do rasterizador de splats [FATO].
- **3DGS de referência (Inria)** [FATO: https://github.com/graphdeco-inria/gaussian-splatting/]: o repo oficial pede **24 GB de VRAM "to train to paper evaluation quality"** — acima do teto no regime publicado; e a **Gaussian-Splatting License é não-comercial (research/evaluation only)**, restrição que se propaga aos derivados que usam o rasterizador original (SuGaR, 2DGS incluídos) [FATO]. Nenhum repo de extrator declara mínimo próprio confiável de VRAM — qualquer número avulso é alegação de terceiros.

**Veredito [ANÁLISE]: NÃO APLICÁVEL como rota principal.** Pressupõe captura multivista **densa e posada de um objeto coerente** — exatamente o que ilustrações esparsas e mutuamente contraditórias não são (§2.4). Com 1–6 ilustrações, o campo fica subdeterminado: ou se gera antes um turntable denso (e já se está de volta à rota multivista), ou o campo inventa o resto. Acrescenta uma conversão com perda (splat→malha→retopo→bake) sem ganhar fidelidade ao cânone. Só faria sentido se a Oficina passasse a ter turntable denso validado — e aí sobre a base gsplat/Nerfstudio (Apache-2.0), nunca sobre a base NC.

### 4.2 Otimização por prior 2D (SDS/VSD) — forma e textura nascem juntas

Coberto como Família C na §3.3 (é também uma "rota de 1 referência/texto"): DreamFusion ~1,5 h/asset; Magic3D 40 min **em 8× A100**; ProlificDreamer (VSD) "generation takes hours" admitido pelos autores, ~8 h numa A800 em comparativos [FATO: https://arxiv.org/pdf/2211.10440; https://proceedings.neurips.cc/paper_files/paper/2023/file/1a87980b9853e84dfb295855b425c262-Paper-Conference.pdf]. Janus quantificado na §3.3. DreamFusion nunca liberou código/pesos (depende de Imagen proprietário). **DreamGaussian** (ICLR 2024, código **MIT** [FATO]) é a exceção prática: SDS sobre Gaussianos + extração + refinamento UV, ~2 min e <8 GB **[ALEGAÇÃO dos autores, numa V100 — a medir]**, com o pior Janus da tabela sem prior multivista e verso borrado documentado pelos trabalhos seguintes.

**Veredito [ANÁLISE]: NÃO APLICÁVEL para personagens canônicos.** O DreamGaussian serve, no máximo, como **rascunho rápido descartável** de silhueta. SDS ignora por construção a fidelidade à ilustração aprovada: o prompt manda, a referência sugere — o oposto do nosso requisito. ProlificDreamer/Magic3D estão fora por tempo e hardware.

### 4.3 Esculpir/retopo + projetar — a via do artista assistido (padrão-ouro)

**Como funciona:** sculpt high-poly fiel às ilustrações (humano decidindo, com as vistas ortográficas como guia no Blender/ZBrush) → retopologia → unwrap UV deliberado → projeção/bake das ilustrações ou de renders por câmera → costuras pintadas à mão. É a **única** via desta lista que entrega por defeito malha limpa + UV deliberado + textura PBR editável e re-iluminável — e a de **fidelidade máxima ao cânone**, porque há um humano arbitrando cada contradição (o "quinto elo" que nenhum algoritmo arbitra, §2.6).

**O que é automatizável de verdade [FATO]:**
- **Voxel Remesh do Blender** como selador de buracos/sobreposições de malhas geradas (pré-passo padrão).
- **QuadriFlow (integrado ao Blender, logo disponível headless na 5.2):** remesh quad que segue curvatura, determinístico por seed — **mas destrói camadas de dados (UVs e vertex colors perdem-se)** salvo preservação explícita; o correto é assar do original para o retopo.
- **Instant Meshes** (gratuito): edge flow em geral melhor em orgânicos; sem API Python oficial (subprocesso); exige entrada manifold limpa.
- **Limite honesto [FATO de ferramenta comercial de retopo]:** *"QuadriFlow and Instant Meshes produce even, all-quad meshes… They do not know where an eyelid or a knee is"* — loops de rosto/rig continuam decisão de artista.

**Veredito [ANÁLISE]: APLICÁVEL — como rota de fidelidade e estação de salvamento, não como automação total.** Automatizar retopo (Voxel→QuadriFlow/Instant Meshes), unwrap, bake e projeção; **não prometer** sculpt nem pintura de costuras automáticos. É o padrão-ouro contra o qual as rotas automáticas se medem — e a rede de segurança de qualquer malha gerada pelas outras vias.

### 4.4 Geração por partes — multiplicador, não via de pintura

- **PartCrafter (NeurIPS 2025)** [FATO: https://arxiv.org/html/2506.05573]: de **1 imagem**, desruída em simultâneo N conjuntos de latentes, um por parte (atenção local dentro da parte + global entre partes), sobre um DiT de malha pré-treinado (base TripoSG); até 8–16 partes, montagem direta no mesmo espaço canônico. **A saída é só geometria** — `O={pi}`, `pi={Vi,Fi}` por parte: **sem UV, sem material, sem textura** [FATO]. VRAM: o repo declara **"at least 8GB VRAM"**, com 1024 tokens/parte por defeito [FATO via documentação do repo] — **no limite exato do nosso teto**: objeto com poucas partes sim; cena com 16 partes, não prometer. Dataset de partes minerado de Objaverse — viés para objetos rígidos do quotidiano, não para personagens de fantasia vestidos.
- **DetailGen3D (arXiv:2411.16820) — correção de enquadramento** [FATO: https://arxiv.org/html/2411.16820v3]: **não é geração por partes** — é **refinamento geométrico coarse→fine** (flow dependente de dados com *token matching*) que transforma uma forma grosseira (de qualquer origem) em forma detalhada preservando a estrutura. Só geometria. Treino de ~8 dias em 8× A800 (irrelevante para uso); VRAM de inferência **não declarada na fonte primária — não inventar número**.
- **Família correlata [FATO]:** PartGen (Meta/Oxford, CVPR 2025) faz o inverso — segmenta renders multivista em partes, completa cada parte com difusor multivista e reconstrói cada uma; HoloPart completa amodalmente fragmentos de um segmentador externo.

**Efeito na pintura [ANÁLISE]:** positivo e indireto — cada parte separada pode ter **seu próprio UV, sua resolução e sua vista de referência/projeção** (cabeça ≠ armadura ≠ arma), e superfícies de contato deixam de ser pintadas por engano. Negativo: costuras entre partes, consistência de paleta entre partes pintadas em separado, e o N de partes é escolha do usuário — o modelo não "descobre" a anatomia canônica de uma besta.

**Veredito [ANÁLISE]: APLICÁVEL COMO PEÇA.** PartCrafter para **forma decomposta** (resolve o "monólito fundido ineditável" dos geradores single-image), assumindo pintura posterior por outro módulo; DetailGen3D como pós-passo de detalhe sobre qualquer forma grosseira, se a inferência couber quando medida.

### 4.5 Paramétricos/templates — SMPL e MakeHuman (só humanoides)

**Como funciona:** não se gera forma livre — ajustam-se parâmetros (shape/pose) de um template humano com topologia fixa, esqueleto e skinning prontos; a pintura vem do template + projeção/sculpt por cima.

- **SMPL** [FATO: https://smpl.is.tue.mpg.de/license.html]: **armadilha de licença clássica** — o **SMPL-Body** (malha+rig, sem os shape blendshapes completos) é **CC BY 4.0**; o **SMPL-Model completo e o software** são licença Max Planck **não-comercial** (investigação/educação/arte não-comercial), incluindo proibição de treinar métodos com fins comerciais.
- **Limite estrutural [FATO]:** SMPL representa humanos **minimamente vestidos**, topologia e resolução fixas. Roupa afastada do corpo, chifres, caudas, quadrúpedes, proporções não-humanas estão **fora do espaço do modelo** — não é parâmetro, é outra topologia.
- **MakeHuman/MPFB (Blender):** mesma ideia, com **código AGPL mas assets/output exportado CC0** na exceção oficial [FATO] — a alternativa licenciavelmente limpa para base humanoide no Blender. VRAM nulo (CPU).

**Veredito [ANÁLISE]: APLICÁVEL COMO PEÇA, só para humanoides de proporção humana** (base rigada a esculpir e vestir por partes, §§4.3–4.4). **Não aplicável** a bestas e orcs fortemente não-humanos: forçar o template aí produz "humano com fantasia", não a criatura do cânone.

### 4.6 Vídeo/turntable gerado (SV3D) — falsa via

[FATO: §2.1] SV3D gera um **vídeo orbital de 21 vistas** a partir de 1 imagem. **Veredito [ANÁLISE]: NÃO É VIA NOVA.** O vídeo é só um gerador de multivista mais consistente (a coerência temporal emprestada à coerência espacial); a jusante volta tudo ao mesmo — otimização tipo SDS/NeRF/GS ou reconstrução multivista. Licença: pesos para investigação não-comercial; comercial exige Stability AI Membership [FATO]. Avaliar, se tanto, **como fornecedor de vistas** dentro da rota multivista — com VRAM de difusor de vídeo, pesado para 8 GB — nunca como terceira família.

### 4.7 O cruzamento desacoplado — forma de uma rota, pintura de outra (a literatura chama isso de *texturing*)

**Pergunta:** "gerar as vistas **da** malha elimina o erro de registro por construção — alguém formaliza?" **Resposta [FATO]: sim — é a definição da literatura de texturing 2023–24, distinta da literatura de geração 3D.** A geometria já existe e é conhecida exatamente: renderiza-se **dela** o mapa de profundidade/normais por vista; esse mapa condiciona o difusor (depth-to-image/ControlNet-depth); a imagem gerada nasce alinhada pixel-a-pixel com aquela vista daquela malha, porque foi gerada **a partir** do render dela; a retroprojeção usa a mesma câmera. **Erro de registro geométrico = 0.** O que resta não é registro — é **inconsistência generativa entre vistas** e oclusão (TEXTure/Text2Tex/TexFusion/Paint3D, §§1.2–1.4, são exatamente esta família, com suas três estratégias de consistência: trimapa, latente partilhado, correção em UV).

O cruzamento inverso também é padrão [FATO]: Magic3D já é forma de uma rota (NeRF grosseiro) + refino de outra (malha DMTet); DreamGaussian é forma por Gaussianos + refinamento UV; SuGaR é forma por splats + rendering amarrado à malha. **Desacoplar forma e pintura não é gambiarra: é o desenho dominante dos sistemas que funcionam.**

**A variante com pixels reais [ANÁLISE]:** trocando o difusor condicionado por depth pelas **ilustrações aprovadas projetadas** a partir de câmeras definidas sobre a malha (nossa rota atual de pintura), o registro continua exato onde a câmera da projeção casa com a vista — e onde não casa, paga-se o erro de registro medido na D1. A composição completa — **projeção real onde há cânone, inpainting generativo só onde não há** — não aparece como produto único na literatura (§1.6), mas é a junção direta de peças citáveis. É ela que o §7.4 desenha como **híbrido candidato a rota oficial**.

### 4.8 Síntese da pergunta 4

| Via | Entrada mínima | Textura que entrega | Cabe em 8.188 MB? | Veredito p/ Oficina |
|---|---|---|---|---|
| NeRF→malha (Instant-NGP/Nerf2Mesh/Nerfstudio) | Dezenas de vistas posadas | Vertex color ou bake UV (view-dependence perdida) | Instant-NGP sim (mas NC); qualidade plena justa | **Não aplicável** (principal) |
| 3DGS→malha (SuGaR/2DGS/GOF/GS2Mesh/MILo) | Idem + COLMAP | SH→bake, borrada p/ detalhe fino | Só degradado; papel pede 24 GB; base NC | **Não aplicável** (principal); gsplat Apache é a única base limpa |
| SDS/VSD (DreamFusion/Magic3D/ProlificDreamer) | Texto (±1 imagem) | Gerada com a forma, saturada/Janus | Não — 40 min a 8 h em A100/A800 | **Não aplicável** |
| SDS rápido (DreamGaussian, MIT) | Texto ou 1 imagem | UV refinada, inventada atrás | Alegação dos autores: <8 GB, ~2 min — medir | Peça de rascunho, nunca cânone |
| Sculpt + retopo + projeção | Referências + artista | UV PBR deliberada, fidelidade máxima | Sim — o automatizável é CPU/headless | **Aplicável** — padrão-ouro e salvamento |
| Por partes (PartCrafter) + DetailGen3D | 1 imagem | **Nenhuma — só geometria** | PartCrafter: mínimo declarado = 8 GB, no limite | **Aplicável como peça** (forma decomposta / detalhe) |
| Desacoplado: forma qualquer + texturing da própria malha | Malha pronta + texto e/ou imagem | UV 2K clássica; registro geométrico = 0 na variante gerativa | Provável (difusão depth vista-a-vista) — medir | **Aplicável — recomendação central** (§4.7) |
| Paramétrico (SMPL-Body CC BY / MakeHuman CC0) | Parâmetros, sem imagem | Do template + trabalho por cima | Sim — CPU | Peça p/ humanoides; não p/ bestas |
| Vídeo turntable (SV3D) | 1 imagem → 21 vistas | A da rota a jusante | Pesado; licença comercial restrita | Não é via — fornecedor de vistas |

---

## 5. Divergências encontradas e correções (transparência da pesquisa)

As frentes de pesquisa divergiram entre si e dos documentos internos em pontos concretos. Resolvo cada um explicitamente, porque decisão tomada sobre premissa errada custa mais que a divergência:

### 5.1 UltraTex — DOIS artefatos, um nome (a divergência maior)

- **O que os documentos internos do projeto registravam** (`VERIFICACAO-PESQUISA-TEXTURA.md`, resumo da sessão): "UltraTex Modular (GPL-3.0; 10 vistas; atlas até 8192²; ComfyUI + FLUX.2 Klein 9B Q4_0 GGUF + Qwen3-8B Q6_K GGUF)", com pesos staged somando 13.738.832.407 B (FLUX GGUF, Qwen GGUF, VAE, 2 LoRAs, decoder, Real-ESRGAN).
- **O que a fonte primária mostra** (§1.7): o repo oficial `yiboz2001/ultratex` é um **framework de pesquisa** (SIGGRAPH Asia 2026), código **MIT**, backbones FLUX.1-dev/FLUX.2-Klein com LoRAs próprios, e **não publica** VRAM, nº de vistas nem tempo. Os números "10 vistas / atlas 8192 / ~6,8 GB" circulam nos **pacotes ComfyUI de comunidade**, não no repo oficial.
- **Reconciliação [ANÁLISE]:** o spike T7 do projeto foi montado sobre o **pacote ComfyUI de comunidade** (que usa FLUX.2 Klein quantizado em GGUF + Qwen3 como componentes do workflow), **não** sobre o framework oficial. As duas coisas compartilham o nome e a família de modelos, mas **não são o mesmo software**: licença (GPL-3.0 do pacote × MIT do framework — e em ambos os casos os **pesos FLUX têm licença BFL não-comercial própria**, que é o fato que importa), números de desempenho (todos do pacote são **[ALEGAÇÃO]**, nenhum é fato do paper) e superfície de risco (workflow de terceiro × código de pesquisa recém-liberado) são diferentes.
- **Consequência prática:** as **réguas do spike T7 continuam válidas e suficientes** — elas já foram desenhadas para medir localmente exatamente o que é alegação (VRAM ≤8.188 MB, tempo ≤45 min, SSIM frontal ≥ rota atual, zero OOM). O que muda é o **rótulo**: no registro do spike, escrever "pacote ComfyUI UltraTex (comunidade), números prévios = alegação" — e, se um dia se quiser o framework oficial, isso é **outro spike**, com outros pesos e outra licença de código. Nada do que está staged se perde: o que está no Drive é o pacote ComfyUI, e é ele que o spike mede.

### 5.2 TripoSG é single-view (e o que isso faz com a nossa lista de motores)

Duas frentes independentes (multivista e single-view) verificaram na fonte [FATO, §3.1]: **TripoSG consome 1 imagem e gera só geometria** — não é motor multivista e não tem difusão multivista interna. **Consequência:** na contabilidade da Oficina, o TripoSG pertence à **rota B** (e está no limite de VRAM: ">8 GB" declarado). O slot de "motor multivista" da rota A é ocupado por um só candidato aberto que cabe: **Hunyuan3D-2mv/-Turbo** (§2.3). E o "mv-turbo" da bateria dourada é, com alta probabilidade, esse checkpoint — a confirmar por leitura do nome na instalação (item de 5 min no spike A, §6.1).

### 5.3 DetailGen3D não gera partes; PartCrafter não pinta

[FATO, §4.4] DetailGen3D é **refinamento de detalhe** coarse→fine; PartCrafter é **geração por partes só de geometria**. Tratar os dois como "motores de forma completos" na mesma prateleira dos demais induz a erro de planejamento: nenhum dos dois entrega textura, e o DetailGen3D nem sequer é uma rota de entrada (é pós-passo). Corrigido no mapa (§4.8).

### 5.4 Paint-it não é pintura vista-a-vista; Kaedim não é texturizador

[FATO, §§1.2/1.8] Paint-it é otimização SDS sobre mapas PBR (família C da §3.3, com os riscos dela); Kaedim é conversão 2D→3D com humanos no loop. Ambos saem das prateleiras onde um mapa rápido os colocaria — e o Kaedim, curiosamente, valida a §4.3: onde o mercado precisa de fidelidade garantida, ele vende **artistas**, não um algoritmo.

### 5.5 InstantMesh: "≥16 GB documentados" × "roda com offload" — os dois, em camadas diferentes

[FATO] A documentação de instalação recomenda ≥16 GB. [ALEGAÇÃO de terceiros] Implementações comunitárias rodam os estágios **em sequência com offload** (a difusão descarrega, o reconstrutor carrega) e relatam caber em menos. **Resolução:** para planejamento, vale o número documentado (❌); o offload é **hipótese de spike**, não premissa — se um dia entrar, entra medido, como o T7. O mesmo critério foi aplicado ao TripoSG (">8 GB" = limítrofe, medir) e ao `low_vram_mode` do Hunyuan3D-2.1 (existe a flag; o repo **não publica número** para ela — qualquer valor menor é de terceiros).

### 5.6 Licenças que mudam de figura conforme o componente (registro consolidado, LIC-01)

- **Zero123++: código Apache-2.0, pesos CC-BY-NC** — o pipeline InstantMesh/CRM herda a restrição mais forte do seu estágio 1. Quem olhar só o repo do reconstrutor (Apache-2.0) conclui errado sobre o pipeline inteiro.
- **Hunyuan (2.0 e 2.1): Community License com exclusão territorial (UE/Reino Unido/Coreia do Sul)** — o Brasil não está excluído, mas a licença não é OSI e cobre outputs. Vale para 2mv, Paint e 2.1 igualmente.
- **3DGS de referência e derivados com o rasterizador original: não-comercial** — a restrição se propaga (SuGaR/2DGS); as saídas limpas são gsplat/Nerfstudio (Apache-2.0).
- **SMPL: Body = CC BY 4.0; Model completo = não-comercial** — a confusão entre os dois é o erro clássico desta prateleira.
- **UltraTex: framework MIT × FLUX não-comercial; pacote ComfyUI GPL-3.0 × FLUX não-comercial** — nos dois mundos, o gargalo de licença é o peso base, não o código em volta.
- **TripoSR e TripoSG: MIT (código e pesos)** — as licenças mais limpas do mapa inteiro [FATO].

---

## 6. Pergunta 5 — Viabilidade das duas formas NA NOSSA OFICINA

Premissas fixas: app Python + Blender 5.2 headless; **RTX 4060 com 8.188 MB de VRAM (teto duro)**; REF-01 já produz e aprova as vistas (Orc, Besta Cristalina e Capríleo com 4 cardeais + diagonais; no Orc, a frente é a autoridade de cor); pintura atual por projeção medida na COR-08 (IoU máx. 0,8177 na frente; cobertura direta 49,79%; comparativo Blender com blending ponderado venceu o pipeline próprio antigo: cobertura 63,43%, erro de cor 42,8 — réguas próprias de cada instrumento, não comparáveis entre si); painel de métricas obrigatório em todo job (regra do Mestre de 01/11 19:06: tempo, VRAM/RAM/CPU, triângulos, peso, tokens quando expostos).

### 6.1 ROTA A — várias referências com ângulos (as 4 vistas alimentam forma e pintura)

**Desenho da rota (com o que a pesquisa mostrou existir de verdade):**
`4 vistas REF-01 → [D-H0: auditoria de concordância 2D] → forma Hunyuan3D-2mv-Turbo (slots front/left/back/right) → pintura por projeção das 4 vistas (pipeline atual, com as melhorias das Fases 1–2 do estudo D1: territórios, pesos suaves, preenchimento com barreiras)`

**O que já está pronto [FATO do projeto]:**
- As **vistas**: REF-01 entrega as 4 cardeais aprovadas dos três sujeitos + diagonais do Orc em produção (lote 4). Custo marginal por sujeito novo: o da frente REF-01, já rotineira.
- O **motor de forma**: mv-turbo medido na bateria dourada (Orc ≤41,4 s, pico 6.435 MB) — com a identidade a confirmar como 2mv-Turbo (§5.2). Se confirmado, **a forma da rota A já roda hoje**; o que nunca foi feito é alimentá-la com as 4 vistas **como slots nomeados** e validar o resultado por marcos (até aqui ela foi usada como motor de forma, não como experimento multivista controlado).
- A **pintura**: pipeline de projeção completo e medido (COR-08), mais a rota Blender de blending ponderado (4,4 s na etapa de cor do comparativo) como alternativa interna já provada.
- As **diagonais** para a pintura (A6 do estudo D1) e para o tribunal de marcos (§2.6-iii).

**O que falta construir/baixar:**
1. **Confirmar a identidade do mv-turbo** (ler o checkpoint na instalação; 5 min). Se não for o 2mv, baixar o `Hunyuan3D-DiT-v2-mv-Turbo` (família 2.0; disco da ordem de poucos GB — medir no ato, regra ARMAZ-01: pesar antes de baixar e staged fora do PC até o spike).
2. **O teste D-H0 (concordância 2D entre as referências)** — não existe em nenhum lugar: é script nosso (meio dia de trabalho, CPU): extrair, por vista, as alturas relativas dos marcos (topo da cabeça, ombro, cinturão, joelho, bainha) em % da altura total e montar a matriz de discordância entre pares adjacentes; limiar de alerta a calibrar no primeiro sujeito (proposta: discordância >3% da altura num marco estrutural = vista sinalizada). Opcionalmente, VGGT/COLMAP como segunda opinião (§2.5 do estudo D1 vira §2.2/2.5 aqui) — com a ressalva de que em ilustração a falha de pose também é dado.
3. **Validação por marcos na malha** (script nosso, CPU/Blender): medir na forma gerada os mesmos marcos (altura do cinturão etc., via caixa envolvente por faixa de altura e inspeção das prévias flat) e comparar com as vistas — é o que transforma "interpretação do modelo" em número auditável.
4. **Nada de textura nova para a rota A em si**: a pintura é a atual. (O Paint entra só como candidato a *preenchimento* no híbrido, §7.4 — e aí é o spike T3 já desenhado: Paint 2.0 via fork 2GP, perfis ~6 GB [ALEGAÇÃO do fork, com contra-exemplo público de OOM], nunca o 2.1 oficial de 21 GB.)

**Custos estimados [ANÁLISE ancorada nas medições do projeto]:** forma por sujeito ~40 s de GPU (medido); pintura, minutos (bake 2048) ou segundos (rota Blender); D-H0 e validação, CPU. Disco: ~0 se o mv-turbo for o 2mv; poucos GB caso contrário. Tempo de spike: **1 execução** para o experimento-base (Orc, forma A × forma atual, mesmos marcos) + a construção do D-H0.

**Riscos (com o antídoto de cada um):**
- **R-A1 — O 2mv media a contradição em silêncio** (§2.3/2.6): a forma pode sair plausível e errada nos marcos sem nenhum aviso. *Antídoto:* D-H0 antes (saber onde as vistas discordam) + validação por marcos depois (medir onde a forma ficou). Sem os dois, a rota A é caixa-preta.
- **R-A2 — Diagonais não têm slot**: o 2mv só conhece as 4 cardeais. *Tratamento:* diagonais servem à pintura e ao tribunal de marcos; **não** prometer forma "de 8 vistas" neste motor — quem prometer isso está vendendo outro modelo.
- **R-A3 — A forma muda, a pintura re-prova**: trocar a forma-âncora obriga re-baseline da pintura (já registrado no estudo D1, C-11 da crítica: adotar a forma vencedora **antes** de calibrar junções, para não pagar a baseline duas vezes). *Tratamento:* a comparação da §7 já nasce com a forma A como candidata a nova âncora.
- **R-A4 — Licença Tencent** (§5.6): registrada; Brasil fora da exclusão; adoção comercial espera o Mestre (LIC-01).

### 6.2 ROTA B — 1 referência (frente) + o app completa sozinho

**Desenho da rota (melhor versão executável com o que existe):**
`vista de frente REF-01 → forma single-view (TripoSG, já no projeto) → pintura por projeção só da frente + completação do resto (preenchimento atual A3 como piso; completação generativa como teto a provar)`

**O que já está pronto [FATO do projeto]:**
- A **vista de frente** (autoridade de cor do Orc) — a rota B consome um subconjunto do que a REF-01 já entrega.
- A **forma single**: TripoSG instalado como motor do projeto (geometria SDF limpa, MIT). **Porém:** VRAM declarada ">8 GB" — no nosso teto é **limítrofe**; o spike B começa medindo o pico real dele na 4060 com o restante do pipeline residente. Alternativas que cabem com folga e **não** estão instaladas: TripoSR (~6 GB, MIT, mas sem UV/PBR — rebaixa a pintura a cor de vértice) e SF3D (~6 GB, com UV, mas licença com teto de receita e pesos gated) — baixar qualquer uma é decisão de spike, com pesagem prévia (ARMAZ-01).
- A **pintura de frente**: o mesmo pipeline de projeção, alimentado com 1 vista — a frente sai comparável à da rota A (é a mesma operação sobre a mesma autoridade de cor).

**O que falta construir/baixar:**
1. **A completação do verso — o coração da rota B, e a peça que NÃO existe pronta na Oficina.** Opções reais, em ordem de honestidade crescente sobre o que são:
   - **Preenchimento atual (A3, geodésico com barreiras):** já existe; entrega verso **chapado/plausível por vizinhança**, sem inventar detalhe — o verso do Orc sairia com as cores certas nos lugares certos e **nenhum** crânio/capa desenhados. É o piso: rápido, determinístico, e **visivelmente** incompleto (o que, para cânone, é uma virtude: não finge).
   - **Inpainting generativo em UV (tipo Paint3D):** não instalado; o Paint3D oficial é pesquisa (VRAM não publicada — medir), e o desenho "inpainting só no complementar com o projetado travado" é a composição aberta da §1.6. Custo: um spike próprio.
   - **Paint multivista gerativo (T3/T7):** os spikes já desenhados (T7 com pesos staged e réguas; T3 via 2GP sem garantia) — mas note: **usar o Paint/T7 para completar o verso da rota B é, na prática, trocar a pintura inteira pela gerativa** (o Paint gera as vistas todas, não só a de costas). Nesse ponto a rota B deixa de ser "projeção + completação" e vira "forma single + pintura gerativa" — legítimo, mas deve ser **nomeado** assim na comparação (§7), para o Mestre saber o que está escolhendo.
2. **O rótulo de proveniência no GLB/registro:** toda região completada deve ser marcada como **gerada** (mapa de proveniência que o bake já sabe produzir por texel) — sem isso, a rota B produz verso que "parece intencional" (§3.1, SF3D) e o cânone perde a fronteira entre o que é arte e o que é invenção. Custo: baixo (o pipeline já rastreia fonte por texel para as auditorias).

**Custos estimados:** forma ~dezenas de segundos (medir no spike, com o pico de VRAM do TripoSG como incógnita nº 1); pintura de frente, igual à da rota A; completação: ~0 (A3) ou um spike inteiro (generativa). Disco: ~0 no desenho-base.

**Riscos:**
- **R-B1 — O verso canônico não existe nesta rota** (§3.6): capa de lobo e continuação do cinturão **não serão gerados** por nenhuma completação disponível — serão aproximados (A3) ou inventados (generativa). Não é risco: é **certeza estrutural**. A rota B só é defensável onde o verso não carrega design, ou como rascunho.
- **R-B2 — VRAM do TripoSG no limite**: se o pico medido estourar com o pipeline residente, a forma B migra para TripoSR/SF3D (com as perdas declaradas acima) ou para o Hunyuan 2.0 single (6 GB declarados para forma na família 2.0 [FATO] — candidato a verificar na instalação, mesma família do 2mv).
- **R-B3 — Deriva de identidade frente↔verso na completação generativa** (§3.6, falha 3): o verso completado pode pertencer a um "primo" do Orc. *Antídoto parcial:* condicionar a completação pela paleta/marcos da frente e julgar o verso **contra a vista de costas real** que a REF-01 tem — na comparação (§7) o verso B é medido contra a verdade que a rota B fingiu não precisar. É exatamente esse número que o Mestre precisa ver.
- **R-B4 — Economia ilusória de referências:** a rota B "dispensa" as vistas de costas/laterais **que a REF-01 já produz por rotina**. A economia real é só nos sujeitos futuros em que se decida **não** gerar as outras vistas — decisão de custo da frente de arte, não da modelagem. Registrar para a comparação não comparar "custo total" errado.

### 6.3 O que as duas rotas compartilham (e onde o T7 se encaixa de verdade)

- **A pintura por projeção é comum às duas** no desenho-base — a variável em julgamento é **de onde vêm a forma e a cor do verso**, não o código de pintura. Isso é deliberado: é o que torna a comparação da §7 justa.
- **O spike T7 (UltraTex ComfyUI)** não pertence a nenhuma das duas rotas: ele é um **motor de pintura gerativa desacoplado** (§4.7) — recebe uma malha pronta (de A ou de B) e gera a textura a partir dela. Seu resultado alimenta a decisão do **híbrido** (§7.4), não a disputa A×B de forma. Rodá-lo em paralelo, sob suas réguas já registradas, continua correto.
- **PartCrafter/DetailGen3D** são ortogonais às duas rotas (forma decomposta / detalhe) — entram como melhoria futura de **qualquer** vencedora, não como terceira competidora.

---

## 7. Pergunta 6 — O desenho da comparação justa A × B (para o Mestre decidir com número)

### 7.1 Princípio do experimento

**Uma variável por vez, o mesmo sujeito, o mesmo juiz.** Sujeito: **Orc** (é o âncora do projeto, tem as 4 vistas + diagonais, a frente como autoridade de cor e os dois elementos-assinatura no verso). As duas rotas usam **a mesma pintura por projeção** (pipeline COR-08) e **a mesma régua de medição**; o que muda é (a) quantas vistas alimentam a **forma** e (b) quantas vistas alimentam a **pintura**. Um terceiro braço, barato, separa os dois efeitos:

| Braço | Forma | Pintura | O que ele isola |
|---|---|---|---|
| **A (rota A completa)** | 2mv-Turbo com **4 vistas** (slots nomeados) | Projeção das **4 vistas** | A proposta multivista inteira |
| **B (rota B completa)** | TripoSG com **1 vista** (frente) | Projeção **só da frente** + preenchimento A3 | A proposta single-view inteira |
| **C (ablação, opcional mas barata)** | 2mv-Turbo com **4 vistas** | Projeção **só da frente** + preenchimento A3 | Quanto da diferença A×B vem da **forma** e quanto vem da **pintura** (C×B isola a forma; A×C isola a pintura) |

Sem o braço C, uma vitória de A não diz **onde** ela ganhou — e a decisão de adoção (trocar o motor de forma? trocar a alimentação da pintura? os dois?) ficaria chutada. A pintura é a etapa barata do pipeline; o braço C custa minutos.

**Controle de variáveis:** mesma seed onde o motor expuser seed; mesma resolução de bake (2048, régua COR-08); mesmas máscaras e mesma função de IoU (a 256 px do projeto) para os três braços; **nenhuma** calibração de junções nova entre os braços (a comparação é das rotas como elas são hoje, não de versões retocadas); painel de métricas do Mestre completo em cada job.

### 7.2 Pré-etapa obrigatória (antes de qualquer braço): o D-H0

Rodar a **auditoria de concordância 2D das 4 referências do Orc** (§6.1, item 2) **antes** da comparação e publicar a matriz de discordância de marcos junto dos resultados. Sem ela, um mau resultado do braço A é ininterpretável (foi o motor ou foram as vistas? — é a correção C-05 da crítica ao estudo D1, agora incorporada ao desenho). Se o D-H0 sinalizar uma vista, a comparação roda **duas vezes para o braço A**: com o conjunto como está e com a vista sinalizada corrigida/rebaixada — a diferença entre os dois runs A **é** o preço medido da inconsistência das nossas referências, número que nenhum paper publica e que decide quanto vale investir na REF-01 geométrica.

### 7.3 O painel de métricas (idêntico nos três braços)

**Mecanismo (medido por script, sem olho humano):**
1. **IoU por vista** (frente/costas/esquerda/direita) da silhueta renderizada × máscara canônica — mesma função e resolução da COR-08 (comparável ao 0,8177/0,7774/0,8065/0,7957 atuais). Reportar também o **IoU global ao lado de qualquer recorte por região** (trava anti-deriva da crítica C-16).
2. **Marcos na malha**: altura relativa do cinturão, dos ombros e da bainha (em % da altura) medida na forma × o valor em cada vista de referência — o erro de marco por braço, em pontos percentuais.
3. **SSIM por região** (render flat × vista canônica), nas caixas do método do Crítico: rosto, peito, pernas — **e costas/capa**, a caixa que a comparação existe para medir.
4. **Cobertura direta %** da pintura (régua COR-08) e **proveniência do preenchimento** (distância média/máx. em anéis; base atual: médio 3,18, máx. 21).
5. **Placar de elementos-assinatura do verso** (semi-medir, julgar no cego): capa de lobo presente/ausente/distorcida; cabeça do lobo presente/ausente; cinturão de crânios contínuo nas costas (sim/não), contagem de crânios no verso × a da referência de costas.
6. **Painel do Mestre**: tempo total e por etapa; pico de **VRAM** e **RAM** (e CPU quando mensurável); **triângulos** do GLB final; **peso** do GLB + textura; **tokens** — motores locais não expõem tokens: registrar **"não se aplica — motor local, sem medição de tokens"** (declarar, nunca omitir nem estimar).
7. **Determinismo**: reexecutar o braço vencedor com os mesmos parâmetros e conferir SHA do GLB/textura.

**Qualidade visual (julgamento cego, separado do mecanismo — L-33):**
- Crítico sênior (bateria própria, adversarial, APR-02) recebe as montagens **referência | A | B | C** nas 4 vistas + zoom do rosto + zoom das costas, **sem saber qual braço é qual**, e julga **mecanismo** (a rota executou o que promete?) × **qualidade visual** (fidelidade ao cânone, pelo padrão do olho do Mestre) em vereditos separados, com defeitos numerados por região.
- O Mestre recebe as mesmas montagens **com os braços revelados e o painel ao lado** — a palavra final visual é dele, como em todas as tranches.

### 7.4 Critérios de decisão (propostos — a palavra final é do Mestre)

- **A vence (adotar multivista como rota oficial de forma)** se: IoU mínimo das vistas de A ≥ B + 0,03 **e** erro de marcos de A < B **e** placar de assinatura do verso de A completo (capa + cinturão presentes e corretos) com o de B incompleto — **mesmo que B seja mais rápida**: o tempo de forma (~40 s) é pequeno demais para compensar um verso errado num asset canônico.
- **B vence (adotar single-view como rota oficial)** se: A **não** superar B nos marcos e no IoU além do ruído (ΔIoU < 0,02 e marcos equivalentes) **e** o verso de B via A3 for julgado "suficiente" no cego **para sujeitos sem design de verso** — ou seja, B vence como **rota de rascunho/volume**, não como rota de cânone. Se B vencer só em tempo e perder em assinatura, o veredito correto é **divisão de trabalho**, não troca de rota (ver híbrido).
- **Híbrido vence (a saída mais provável, a julgar pela literatura)** se os braços se repartirem: A melhor em forma/verso, B equivalente na frente, e o custo de A for aceitável. O híbrido tem **duas formas distintas**, e a decisão deve dizer qual:
  - **Híbrido-1 (por sujeito):** rota A para sujeitos com verso canônico aprovado (Orc, bestas com design de costas); rota B para rascunhos, sujeitos novos ainda sem vistas aprovadas e testes de silhueta. Critério de enquadramento registrado por sujeito.
  - **Híbrido-2 (por região, dentro do mesmo asset):** forma da rota vencedora + pintura por projeção onde há vista canônica + **completação generativa só no complementar**, com mapa de proveniência marcando o que é arte e o que é gerado (§§1.6/4.7). Este depende do spike de completação (Paint3D-like ou T7 como pintor da malha pronta) e **só entra se esse spike passar nas suas réguas** — sem spike aprovado, Híbrido-2 é desenho, não rota.
- **Nenhuma das duas (manter o atual) se:** A não bater a forma-âncora atual nos marcos/IoU (o 2mv pode, legitimamente, perder para o motor atual no nosso sujeito — a bateria dourada mediu o mv-turbo como forma, não como fidelidade de marcos) **e** B confirmar o esperado no verso. Nesse caso a decisão registrada é: forma atual fica; o investimento vai para as Fases 1–2 do estudo D1 (junções/vazamento) e o D-H0 passa a valer como **portão de qualidade da REF-01** (as vistas passam a ser aprovadas também por concordância, não só pelo olhar).

### 7.5 Ordem de execução recomendada (o que rodar primeiro, e por quê)

1. **D-H0** (CPU, meio dia) — porque interpreta tudo o que vier depois.
2. **Braço A** (forma 2mv com 4 vistas + pintura atual) — porque usa o que já está pronto, responde à pergunta de maior valor (*as nossas vistas, como condição, melhoram a forma?*) e produz, de quebra, a candidata a nova forma-âncora (que a crítica C-11 manda adotar **antes** de calibrar junções).
3. **Braço B** (TripoSG com a frente; medir o pico de VRAM na primeira execução) — porque é o baseline honesto da economia prometida pela rota single.
4. **Braço C** (ablação) — minutos de pintura sobre a forma de A.
5. **Julgamento cego + painel consolidado → decisão do Mestre** registrada em DECISOES, com o nome exato do que foi adotado (rota oficial de forma / divisão por sujeito / híbrido por região / manter atual).
6. **Em paralelo (trava de GPU respeitada):** o spike T7 sob suas réguas — o resultado dele alimenta o Híbrido-2, não bloqueia os itens 1–5.

---

## 8. Honestidade — onde este estudo é fraco

- **Nenhum número de rota A ou B foi medido neste projeto ainda.** Tudo o que as §§6–7 afirmam sobre o 2mv e o TripoSG **neste** pipeline é arquitetura + números de terceiros; o desenho da §7 existe porque folheto não é medição — o mesmo princípio que o projeto já aplica ao T7/T3.
- **A identidade do mv-turbo como Hunyuan3D-DiT-v2-mv-Turbo é inferência forte, não fato** — nome, comportamento e os 6.435 MB medidos batem; a confirmação é um item explícito (e barato) do spike A. Se estiver errada, a rota A ganha um download e perde a vantagem "já instalado" — o desenho da comparação não muda.
- **Licença do Wonder3D ficou NÃO VERIFICADA** (fontes secundárias divergem entre MIT e AGPL-3.0) e VRAM oficial de Wonder3D/CRM/SV3D/Magic123 **não foi localizada** — declarados como pendências nas fichas, não chutados.
- **Os números do pacote ComfyUI UltraTex (6–8 GB, 10 vistas, 8K) são de comunidade/fornecedor** e os do framework oficial são speedups relativos dos autores — nenhum dos dois conjuntos foi medido independentemente até esta data. O spike T7 decide com as réguas que já tem.
- **As tabelas de benchmark citadas (MeshFormer, Unique3D) medem objetos genéricos (GSO)** com réguas próprias e incomparáveis entre si; usei-as apenas para direção e ordem de grandeza (vistas reais > vistas geradas > single, com ganhos de ~20–30% em Chamfer dentro de cada régua) — **nenhuma** mede fidelidade de verso canônico, métrica que este estudo precisou inventar (§7.3, item 5) porque a literatura não a tem.
- **A análise do caso Orc (§3.6) é quantificação qualitativa por mecanismo** (como cada método funciona ⇒ o que ele pode/não pode entregar), não medição: a medição correspondente é o placar de assinatura do braço B na §7.
- **Preços/tempos de serviços comerciais (Meshy/Tripo/Rodin) mudam sem aviso** e seus métodos são caixas-pretas declaradas: entraram no mapa para completude do "como os outros fazem", **não** como candidatas — a Oficina é local por decisão do projeto, e nenhuma conclusão das §§6–7 depende deles.

---

## Fontes consolidadas

**Do projeto (lidos integralmente):** `ESTUDO-RAIZ-D1-SOLUCOES.md`; `CRITICO-estudo-raiz-d1.md` (correções C-01–C-17); `ESTUDO_D1_FIDELIDADE.md`; `ESTUDO_T3_PAINT.md`; `VERIFICACAO-PESQUISA-TEXTURA.md`; `comparativo-blender/RESUMO.md` — todos em `~/workspace/oficina-audit/` e no repo do projeto.

**Pintura/texturização:** Waechter et al., ECCV 2014 — https://nsk.compsciclub.ru/attachments/classes/file_AkLJjlLB/waechter2014.pdf · Meshroom Texturing — https://meshroom-manual.readthedocs.io/en/dev-custom_nodes/feature-documentation/nodes/Texturing.html · Metashape texture types — https://www.agisoftmetashape.com/understanding-texture-map-types-in-agisoft-metashape-a-complete-guide/ · TEXTure, arXiv:2302.01721 — https://ar5iv.labs.arxiv.org/html/2302.01721 · Text2Tex, ICCV 2023 — http://openaccess.thecvf.com/content/ICCV2023/html/Chen_Text2Tex_Text-driven_Texture_Synthesis_via_Diffusion_Models_ICCV_2023_paper.html · InTeX, arXiv:2403.11878 · TexFusion, ICCV 2023 — https://openaccess.thecvf.com/content/ICCV2023/papers/Cao_TexFusion_Synthesizing_3D_Textures_with_Text-Guided_Image_Diffusion_Models_ICCV_2023_paper.pdf · Paint-it, arXiv:2312.11360 — https://arxiv.org/abs/2312.11360 · SyncMVD, SIGGRAPH Asia 2024 — https://ar5iv.labs.arxiv.org/html/2311.12891 · Hunyuan3D 2.0 tech report — https://github.com/Tencent-Hunyuan/Hunyuan3D-2/raw/refs/heads/main/assets/report/Tencent_Hunyuan3D_2_0.pdf · Paint3D, CVPR 2024 — https://arxiv.org/html/2312.13913v2 · TEXGen, arXiv:2411.14740 — https://arxiv.org/abs/2411.14740 · DreamMat, arXiv:2405.17176 — https://arxiv.org/html/2405.17176v1 · Material Anything, CVPR 2025 — https://openaccess.thecvf.com/content/CVPR2025/papers/Huang_Material_Anything_Generating_Materials_for_Any_3D_Object_via_Diffusion_CVPR_2025_paper.pdf · UltraTex (oficial) — https://github.com/yiboz2001/ultratex/blob/HEAD/README.md · Substance Painter Projection — https://experienceleague.adobe.com/en/docs/substance-3d-painter/using/painting/paint-tools/projection · Meshy Retexture API — https://docs.meshy.ai/en/api/retexture · Tripo texturing API — https://www.3daistudio.com/Platform/API/Documentation/texturing/tripo · Rodin Gen-2 API — https://docs.hyper3d.ai/en/api-specification/rodin-gen2

**Multivista → forma:** Zero123++, arXiv:2310.15110 — https://pdfs.assets.alphaxiv.org/2310.15110v1.pdf · repo e licenças — https://github.com/sudo-ai-3d/zero123plus/blob/HEAD/README.md · MVDream, arXiv:2308.16512 — https://arxiv.org/html/2308.16512v4 · SyncDreamer, arXiv:2309.03453 — https://ar5iv.labs.arxiv.org/html/2309.03453 · ImageDream, arXiv:2312.02201 — https://arxiv.org/html/2312.02201v1 · Wonder3D, arXiv:2310.15008; Wonder3D++ — https://arxiv.org/html/2511.01767v1 · SV3D, ECCV 2024 — https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/00150.pdf · Era3D, arXiv:2405.11616 — https://arxiv.org/pdf/2405.11616 · LRM, arXiv:2311.04400 — https://arxiv.org/html/2311.04400v2 · InstantMesh, arXiv:2404.07191 — https://arxiv.org/html/2404.07191v2 · LGM, arXiv:2402.05054 — https://arxiv.org/html/2402.05054v1 · GRM, arXiv:2403.14621 — https://arxiv.org/html/2403.14621v1 · CRM, arXiv:2403.05034 — https://ar5iv.labs.arxiv.org/html/2403.05034 · Unique3D, arXiv:2405.20343 — https://arxiv.org/html/2405.20343v1 · VGGT, arXiv:2503.11651 · Hunyuan3D-2 (2mv) — https://github.com/Tencent-Hunyuan/Hunyuan3D-2 · Hunyuan3D-2.1 — https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 · TRELLIS — https://github.com/microsoft/trellis/blob/HEAD/README.md

**Single-view + completação:** TripoSR — https://github.com/vast-ai-research/triposr/blob/HEAD/README.md · SF3D — https://github.com/stability-ai/stable-fast-3d/blob/HEAD/README.md · TripoSG model card — https://github.com/mrforexample/comfyui-3d-pack/blob/HEAD/Checkpoints/Diffusers/VAST-AI/TripoSG/README.md · Freeplane, arXiv:2406.00750 — https://arxiv.org/html/2406.00750v1 · MeshFormer (tabelas), arXiv:2408.10198 — https://arxiv.org/pdf/2408.10198 · Magic123/Janus — https://arxiv.org/pdf/2402.18780 · HeadArtist (Janus) — https://arxiv.org/html/2312.07539v2/

**Rotas alternativas:** Instant-NGP — https://github.com/NVlabs/instant-ngp · Nerfstudio, arXiv:2302.04264 — https://ar5iv.labs.arxiv.org/html/2302.04264 · Nerf2Mesh — https://github.com/ashawkey/nerf2mesh · 3DGS oficial — https://github.com/graphdeco-inria/gaussian-splatting/ · Gaussian Opacity Fields — https://niujinshuchong.github.io/gaussian-opacity-fields/ · MILo, arXiv:2506.24096 — https://arxiv.org/pdf/2506.24096 · DreamFusion/Magic3D (tempos) — https://arxiv.org/pdf/2211.10440 · ProlificDreamer, NeurIPS 2023 — https://proceedings.neurips.cc/paper_files/paper/2023/file/1a87980b9853e84dfb295855b425c262-Paper-Conference.pdf · DreamGaussian, arXiv:2309.16653 — https://arxiv.org/html/2309.16653v2 · PartCrafter, arXiv:2506.05573 — https://arxiv.org/html/2506.05573 · DetailGen3D, arXiv:2411.16820 — https://arxiv.org/html/2411.16820v3 · PartGen, arXiv:2412.18608 — https://arxiv.org/html/2412.18608v1 · SMPL (licença) — https://smpl.is.tue.mpg.de/license.html

*Fim do estudo. Nenhum arquivo do projeto foi alterado; o entregável é este documento. A frente executora pode pegar daqui: a pré-etapa D-H0 e os braços A/B/C da §7 são autocontidos e usam motores, vistas e réguas que o projeto já tem.*
