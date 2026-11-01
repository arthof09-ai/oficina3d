# Verificação factual — Pesquisa do ChatGPT sobre texturização 3D para a Oficina3D

**Data da verificação:** 2026-11-01 · **Método:** leitura das páginas/repositórios oficiais de cada projeto (fontes primárias). Nenhum software foi instalado, nenhum modelo foi baixado e nenhum repositório foi alterado.
**Pesquisa verificada:** `PESQUISA-CHATGPT-TEXTURA-2026-11-01.md` (recebida do Mestre em 2026-11-01).

## Tabela-resumo

| # | Ferramenta | Afirmação-chave da pesquisa | Veredito |
|---|---|---|---|
| 1 | UltraTex Modular | Roda em GPU de 8 GB (RTX 5050 Laptop), 15–18 min/modelo, 10 vistas, atlas 8K, aceita referências próprias, exporta GLB com metallic/roughness | **CONFIRMADA** (só o tamanho total dos downloads não é declarado no README) |
| 2 | StableGen | Add-on de Blender via ComfyUI, pintura multivista com projeção, edição localizada e mapas PBR | **CONFIRMADA** (VRAM declarada: ~8 GB p/ SDXL; 16 GB+ p/ Qwen Image) |
| 3 | SUPRA-Tex | Inferência publicada em 19/10/2026; exige Linux/CUDA; recomenda GPU ≥48 GB; tem offload p/ CPU | **CONFIRMADA** |
| 4 | Eyek | Add-on de Blender que projeta várias imagens num único UV, com transparência e oclusão | **CONFIRMADA** nas funções; **licença NÃO LOCALIZADA**; Blender mínimo declarado 3.6 |
| 5 | Hunyuan3D-Paint 2.1 | Etapa de pintura recomenda 21 GB de VRAM | **CONFIRMADA** (número exato no README oficial) |
| 6 | Yedp UV Painter | Pintura por região em camadas, projetado p/ 8 GB, MVP experimental | **NÃO LOCALIZADA** — nenhum repositório/página oficial encontrado |
| 7 | Comfy BlenderTools | UV, projeção e bake via Blender dentro do ComfyUI | **PARCIAL** — funções confirmadas; **licença NÃO LOCALIZADA** |
| 8 | InstaMAT Studio | Plano Pioneer gratuito p/ quem está abaixo do limite de receita/financiamento | **CONFIRMADA** — limite real: receita anual **ou** financiamento total < US$ 100 mil, com atribuição obrigatória |
| 9 | Open Painter | Camadas, máscaras e PBR dentro do Blender 5.2+ | **CONFIRMADA** — site oficial declara Blender 5.2+ e licença GPL-3.0-or-later |

---

## 1. UltraTex Modular — CONFIRMADA

**Fonte:** https://github.com/Mstafa-awad/UltraTex-ComfyUI-nodes (README, lido integralmente em 2026-11-01; repo público, criado em 2026-10-11, 32 commits).

- **Existe; licença:** sim. O GitHub detecta e o README confirma: *"UltraTex Modular project-authored source is distributed under the GNU GPL version 3.0"* (GPL-3.0). Ressalva do próprio README: a licença não cobre os modelos/LoRAs de terceiros; o modelo-base FLUX.2 Klein 9B é de uso não comercial (os *outputs* podem ser comerciais "subject to its restrictions" da licença BFL).
- **Gratuito/local:** *"Free source code. No hosted service, subscription, or bundled model weights"* e *"Everything runs on your computer"*.
- **Malha + referências próprias:** *"UltraTex Modular turns a 3D mesh and one reference image into a textured, UV-mapped GLB inside ComfyUI"*. As vistas próprias são entradas **opcionais** do nó UTX 1: `reference_back`, `reference_character_left_side`, `reference_character_right_side`, `reference_top`, `reference_bottom` — ou seja, costas, esquerda, direita, topo e base, como afirma a pesquisa. Nuance fiel ao README: as fotos "guiam a cor" de cada câmera e o FLUX gera a vista a partir delas (não é projeção direta pixel a pixel); elas **não** afetam a passada metallic/roughness.
- **Cria vistas novas e exporta GLB pintado:** *"uses the official UltraTex FLUX.2 Klein base 9B adapters to paint the model from 10 cameras… and bakes them into a texture atlas"*; o fluxo termina em "Textured GLB".
- **Rugosidade/metalicidade:** *"together with a metallic/roughness map"* — passada MR separada (LoRA própria), gravada na textura metallic-roughness do GLB (G = roughness, B = metallic). A pesquisa também acerta ao dizer que normal/AO não são produzidos (o README não anuncia esses mapas).
- **Números — todos literais no README:**
  - *"Measured on an RTX 5050 Laptop GPU (8 GB) with the included 8K workflow (10 albedo views at 2048, 6 MR views at 1536, 4 steps, RealESR, 8K Quality bake): **about 15–18 minutes per model**"*.
  - **10 vistas de cor:** *"10 real views — Six canonical views + four guided 45° views"* (albedo: 10 views).
  - **Atlas 8K:** *"bakes them into a texture atlas of up to 8192 × 8192"* (opções 4096 ou 8192).
  - Requisitos testados: *"Windows, PyTorch 2.8.0+cu128, CUDA 12.8, Python 3.12, RTX 5050 Laptop 8 GB"*; e o aviso honesto: *"real 6 GB GPUs have not been tested"*.
- **Exige ComfyUI + modelos quantizados:** requisitos listam ComfyUI (interface V3), **ComfyUI-GGUF** instalado à parte e os downloads: **FLUX.2 Klein base 9B Q4_0 GGUF** (diffusion model), **Qwen3-8B Q6_K GGUF** (encoder de texto), VAE do FLUX.2, LoRA de albedo, LoRA MR, decoder e Real-ESRGAN x4v3. A pesquisa dizia "FLUX.2/Qwen quantizados" — correto (o "Qwen" é o Qwen3-8B, encoder de texto).
- **Tamanho total dos downloads:** **NÃO LOCALIZADA no README** — a tabela de modelos lista os arquivos e onde salvá-los, mas **não declara tamanhos individuais nem um total**. A cautela da pesquisa ("a ocupação total do disco deve ser medida antes da instalação") continua válida e sem número oficial.

**Veredito do item: CONFIRMADA** (única lacuna: tamanho total dos downloads não declarado).

---

## 2. StableGen — CONFIRMADA

**Fonte:** https://github.com/sakalond/StableGen (README; repo público, ~1.230 stars, 15 releases, criado em 2025-05-15).

- **Existe; licença:** sim — **GPL-3.0** (*"StableGen is released under the GNU General Public License v3.0"*). Ressalva do README: alguns modelos que ele roda têm licenças próprias, e três são só para uso não comercial (Qwen Image 2.1 — Qwen Research License; Bria FIBO 2.0 — CC BY-NC 4.0; modo Native do TRELLIS.2 — nvdiffrast/nvdiffrec da NVIDIA).
- **É add-on de Blender e depende de ComfyUI:** *"StableGen is a Blender add-on that textures meshes and whole scenes with diffusion models… It renders guidance images from cameras in your scene, sends the work to a ComfyUI server on the same computer or elsewhere on your network, and projects the results back onto the meshes."*
- **Pintura multivista com contexto + projeção:** *"StableGen generates a view from each camera and projects it onto every surface that camera sees; each view is generated with the earlier ones as context, so the texture stays consistent all the way round."*
- **Edição localizada:** seção "Edit part of a texture" — *Masked Edit* regenera só a região pintada.
- **Mapas PBR:** *"Marigold estimates albedo, roughness, metallic and normal maps from the generated views. StableGen projects them like the color and bakes them into standard maps."*
- **VRAM declarada (Requirements):** *"A ComfyUI server, preferably with an NVIDIA GPU: **about 8 GB of VRAM for SDXL, and 16 GB or more for Qwen Image**."* A pesquisa dizia apenas que "a execução real em 8 GB ainda precisa ser testada" — compatível: o modo SDXL declara ~8 GB; o modo Qwen Image **não** cabe em 8 GB segundo o próprio README. Disco: *"10 GB to over 50 GB of disk space for models, depending on what you install."*
- (Extra, não afirmado na pesquisa: exige Blender 4.2–4.5 ou 5.1+; o Blender 5.0 **não** é suportado.)

**Veredito do item: CONFIRMADA.**

---

## 3. SUPRA-Tex — CONFIRMADA

**Fonte:** https://github.com/Supra-3D/SUPRA-Tex (README integral; repo público, ~494 stars, criado em 2026-10-14).

- **Código de inferência em 19/10/2026:** notas de lançamento do README: *"🔥 **[2026-10-19]** Inference code released for image-to-3D and mesh texturing, along with a training overview."* — data exata da pesquisa.
- **Instalação exige Linux/CUDA:** *"SUPRA-Tex requires **Linux** with an **NVIDIA GPU**, a **CUDA 12.4** toolkit with `nvcc`, Git, and a C++ compiler."*
- **Recomendação ≥48 GB + offload para CPU:** seção *Inference Speed*: *"**Use a GPU with at least 48 GB.** GPUs with up to 24 GiB enable CPU offload automatically, which moves the Qwen model block by block during inference. Larger GPUs keep models resident, and the Qwen stage becomes much faster."* E na instalação: *"The full image-to-3D pipeline has been tested on an NVIDIA RTX 3090 (24 GB), where CPU offload is enabled automatically."* — exatamente o que a pesquisa afirma.
- **Fidelidade à referência e PBR nas superfícies não visíveis:** *"generates textured 3D assets from a single image, preserving details such as lettering, patterns, and material boundaries… completes unseen regions with an Interleaved Flow Transformer. The output is a relightable GLB with base color, metallic, and roughness textures."*
- **Licença:** **MIT** para o código-fonte original e os pesos de completion (*"Original SUPRA-Tex source code and the 3D completion weights are released under the MIT License"*). Ressalva registrada no próprio README: o *material adapter* usa a **Qwen Research License** (pesquisa/avaliação não comercial) e há componentes de terceiros (MIT, Apache-2.0, licença do DINOv3).

**Veredito do item: CONFIRMADA** (com a ressalva de licença do material adapter).

---

## 4. Eyek — CONFIRMADA nas funções; licença NÃO LOCALIZADA

**Fontes:** https://github.com/p4ymak/eyek (README e detalhes do repo) e o `__init__.py` / `Cargo.toml` do próprio repositório.

- **Existe; é add-on de Blender:** *"Blender add-on for texturing by projection mapping multiple images to one UV layer with non-destructive workflow."*
- **Múltiplas imagens → um único UV:** título do repo: *"Texturing tool for projecting images from multiple cameras to one UV Map"*; suporta UDIM por padrão e projeta sobre o UV existente.
- **Transparência:** *"Alpha channel supported."*
- **Controle de oclusão:** *"Optional shadowing — projections won't pass through objects"*; no código, a propriedade `occlude` ("Allow polygons shade each other. Otherwise, the projection goes through.") e `backface_culling`.
- **Versão do Blender suportada:** o `bl_info` do add-on declara `"blender": (3, 6, 0)` — ou seja, **mínimo declarado: Blender 3.6** (sem teto declarado). A pesquisa não afirmava versão; fica o registro para a Oficina (que usa Blender 5.2 — compatível pelo mínimo declarado, mas sem garantia expressa para 5.x no README).
- **Licença: NÃO LOCALIZADA.** O repositório **não tem arquivo LICENSE** (o GitHub não detecta licença), o `Cargo.toml` do núcleo Rust não declara campo `license` e o `bl_info` não menciona licença. Não há base primária para afirmar GPL nem qualquer outra licença.

**Veredito do item: CONFIRMADA** quanto às funções; **licença NÃO LOCALIZADA**.

---

## 5. Hunyuan3D-Paint 2.1 — CONFIRMADA (21 GB exatos)

**Fonte:** https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1 (README oficial, seção *Models Zoo*).

Trecho literal: *"**It takes 10 GB VRAM for shape generation, 21GB for texture generation and 29GB for shape and texture generation in total.**"*

Ou seja: forma = 10 GB; **textura/pintura (Hunyuan3D-Paint-v2-1) = 21 GB**; pipeline completa = 29 GB. O número da pesquisa está **exato** e está escrito no README oficial, logo acima da tabela de modelos. (O repo também oferece um `--low_vram_mode` no app Gradio, que a pesquisa não mencionava; isso não muda o requisito declarado de 21 GB para a geração de textura no modo normal.)

**Veredito do item: CONFIRMADA.**

---

## 6. Yedp UV Painter — NÃO LOCALIZADA

**Busca realizada:** três pesquisas web distintas ("Yedp UV Painter GitHub…", `"Yedp" UV painter github`, `"YEDP UV Painter" reddit comfyui`, além de variação com "ComfyUI custom nodes region layers").

- **Nenhum repositório no GitHub, página oficial ou documentação do projeto foi localizado.**
- O único rastro encontrado é o **título de um post no Reddit (r/comfyui)** — *"I've gotten YEDP UV Painter 'working' with Flux Klein for the most part!"* — reproduzido por sites-espelho de baixa qualidade (fastemoji/fastemote). É fonte de terceiro, sem acesso ao conteúdo do post nem a qualquer página do projeto.
- Portanto, **nenhuma** das afirmações da pesquisa pode ser verificada em fonte primária: pintura por região em camadas separadas (pele/armadura/cinto/cabelo), desenho para 8 GB, estado "MVP experimental" e licença ficam **sem confirmação**.

**Veredito do item: NÃO LOCALIZADA.** Recomendação prática: tratar o Yedp como **não homologado** — não contar com ele no plano da Oficina até que um repositório/página oficial seja apresentado (a pesquisa o marcava como "Alta" prioridade; essa prioridade não tem lastro verificável hoje).

---

## 7. Comfy BlenderTools — PARCIAL (funções confirmadas; licença não localizada)

**Fonte:** https://github.com/Rizzlord/Comfy_BlenderTools (README integral; repo público pequeno — 7 stars, 96 commits, criado em 2025-07-31, sem releases).

- **Existe; integra Blender ao ComfyUI:** *"a collection of custom nodes designed to integrate Blender's powerful 3D processing capabilities directly into your ComfyUI workflows. These nodes allow you to perform mesh decimation, UV unwrapping, texture projection, depth map rendering, and mesh cleanup without leaving ComfyUI."* Exige Blender instalado (4.0+ recomendado) apontado pela variável `BLENDER_EXE` — ou seja, o Blender roda como processo automatizado por trás dos nós, como diz a pesquisa.
- **UV:** nó *Blender Unwrap* (XAtlas, Smart UV Project, Angle Based, Conformal, Cube Projection).
- **Projeção:** nó *Texture Projection Bake (Blender)*: *"Projects images onto a 3D mesh from multiple camera angles and bakes them into a single texture."* Há ainda *Multiview Texture Bake* (projeta renders multivista em vertex colors e bakeia no UV) e *Apply Texture and Export GLB*.
- **Bake:** confirmado (arquivos `baking_nodes.py`/`vertexbake_nodes.py` e os nós acima).
- **Licença: NÃO LOCALIZADA.** O repositório **não tem arquivo LICENSE** e o README não menciona licença em nenhum ponto (o GitHub não detecta licença para este repo).

**Veredito do item: PARCIAL** — as funções afirmadas (UV/projeção/bake via Blender dentro do ComfyUI) são **CONFIRMADAS**; a licença é **NÃO LOCALIZADA**, e o projeto é pequeno/sem releases, o que pede cautela adicional antes de adotá-lo como peça permanente.

---

## 8. InstaMAT Studio — Pioneer CONFIRMADA (limite: US$ 100 mil)

**Fonte:** https://instamaterial.com/ (página oficial, seção *Pricing* e FAQ — fonte primária).

Trechos literais da seção de preços:

- *"Pioneer License — Free. Free and unrestricted access to InstaMAT Studio, without any features cut or limited."*
- Inclui: *"Includes InstaMAT Studio · Integrations for tools & game engines · Windows, macOS, and Linux · **Commercial use rights** · **Requires attribution**"*.
- Elegibilidade: *"**Available for individuals or businesses with annual revenue or total funding less than $100,000.**"*
- FAQ oficial: *"Can the Pioneer License be used for commercial projects? Yes, but proper attribution for InstaMAT is required whenever content is shared, published, or distributed."* A licença Pioneer se renova automaticamente ("auto-renews") e pode ser cancelada a qualquer momento.

**Esclarecimento de número:** a mesma página exibe US$ 250.000 — mas esse é o teto das faixas **Indie** (pagas), **não** da Pioneer. O limite da Pioneer gratuita é **receita anual OU financiamento total abaixo de US$ 100.000**, exatamente o tipo de condição que a pesquisa descreveu ("plano Pioneer gratuito para quem atende ao limite de receita/financiamento").

**Veredito do item: CONFIRMADA** — com as condições reais registradas: gratuito, Studio completo, uso comercial permitido, **atribuição obrigatória** e teto de US$ 100 mil (receita anual ou funding total).

---

## 9. Open Painter — CONFIRMADA

**Fonte:** https://openpainter.dev/ (site oficial do projeto).

- **Blender 5.2+:** o topo da página declara *"Blender 5.2+ · Core texturing works offline"* — bate com a pesquisa e com o Blender 5.2 instalado no CUNHADO-PC.
- **Estúdio de textura dentro do Blender, com camadas e máscaras:** *"A complete 3D texturing studio. Right inside Blender"*; *"Build it in layers… Open any layer or painted mask and make the material your own"*; números oficiais: **50 smart materials, 8 canais PBR, 18 smart masks, 65 fontes procedurais**. Descrição oficial: *"a free and open-source 3D texturing studio inside Blender. Paint, layer, age, bake and export materials."*
- **Licença:** *"Free and open source. **GPL-3.0-or-later.** Your work stays yours."* Preço: US$ 0 (serviços opcionais pagos — Materials+/Connect/Teams — não fazem parte do núcleo).

**Veredito do item: CONFIRMADA.**

---

## Fecho — o que muda para a Oficina3D

1. **A espinha dorsal da pesquisa está de pé:** UltraTex (candidato principal), projeção multivista e os números de VRAM foram confirmados nas fontes oficiais, inclusive os dois números mais citados — **15–18 min/modelo em GPU de 8 GB** (UltraTex) e **21 GB** (Hunyuan Paint 2.1).
2. **Três pontos de atenção antes de qualquer instalação:**
   - **Yedp não foi localizado** em fonte primária — não deve figurar como peça do plano até aparecer um repositório oficial.
   - **Eyek e Comfy BlenderTools não têm licença declarada** nos repositórios — para uso interno/teste isso é um risco menor, mas deve ser registrado antes de virarem dependência permanente do projeto.
   - **UltraTex não declara o tamanho total dos downloads** — medir o disco antes de instalar (FLUX.2 Klein 9B Q4 + Qwen3-8B Q6_K + VAE + LoRAs + Real-ESRGAN), como a própria pesquisa já recomendava.
3. **Nada aqui foi testado no CUNHADO-PC** — esta verificação cobre apenas a veracidade das afirmações públicas; desempenho e qualidade reais na RTX 4060 continuam pendentes de teste físico, como a própria pesquisa ressalvava.
