# Estudo — REUSO × RECRIAÇÃO das soluções de textura na Oficina3D

**Data:** 2026-11-01 · **Ordem:** Mestre (2026-11-01) · **Diretriz-mãe:** DONO-01/DONO-02 (app do Mestre, independente: tem de funcionar **sem precisar** das referências; referências preservadas só para auditoria dos Comestres).
**Método:** licenças lidas nos arquivos dos clones locais (`~/workspace/oficina-audit/referencias-codigo/`) e nos metadados locais (README, THIRD_PARTY_NOTICES, component_manifest.json) — nunca de memória. Desenho atual da Etapa COR lido dos documentos vivos do PC (DECISOES COR-01…COR-07 e ESTUDO_MELHORIAS: T1 projeção, T2 vértice, T5 xatlas, T6 delight+PBR próprio, T7 spike UltraTex à frente do T3).
**Regra de leitura dos vereditos:** REUSAR = a peça pode entrar como está (com as obrigações da licença); RECRIAR = a técnica entra, com código nosso, sem copiar o código alheio; SÓ ESTUDAR = leitura permitida, cópia proibida (licença ausente ou restritiva); DESCARTAR = não entra por inviabilidade, duplicidade ou fechamento da fonte.

---

## 0. O quadro jurídico em 30 segundos

- **GPL-3.0** (UltraTex Modular, StableGen): reusar código é legal, mas o copyleft obriga a distribuir o trabalho combinado sob GPL, com código-fonte e avisos. O repositório da Oficina é público, logo o cumprimento é viável — mas é um compromisso arquitetural: cada peça GPL embutida "contamina" o componente combinado. Recriar a técnica mantém o código do app sob os termos do próprio projeto.
- **BFL FLUX (não comercial)** é o maior bloqueio de todo o estudo: vale para o modelo-base FLUX.2 Klein 9B **e** para o VAE dele. Os *outputs* podem ser comerciais "sujeitos às restrições" da BFL, mas o **uso do modelo** em contexto comercial exige licença separada da BFL (README do UltraTex, §"Commercial use of generated outputs", lido no clone). Consequência: a pilha UltraTex completa pode ser **motor de spike/uso interno**, nunca o núcleo permanente de um app que se pretenda usar/distribuir comercialmente sem essa licença.
- **Sem licença = sem cópia.** Eyek e Comfy BlenderTools não têm arquivo LICENSE nem declaração de licença (confirmado nos clones): o padrão legal é "todos os direitos reservados" — estudar o comportamento é lícito, copiar código não.
- **Pesos não herdam a licença do código.** Cada peso tem termos próprios (manifesto do UltraTex declara isso peça a peça, e eu sigo o manifesto onde ele é a fonte mais precisa).

---

## 1. UltraTex Modular (clone: `referencias-codigo/ultratex/`)

Licença do código autoral do pacote: **GPL-3.0-only** — arquivo `LICENSE` lido no clone ("GNU GENERAL PUBLIC LICENSE Version 3, 29 June 2007") e `THIRD_PARTY_NOTICES.md` ("Project-authored UltraTex Modular v2 code is offered under GNU GPL-3.0-only"). Dentro dele há peças vendorizadas MIT/Apache-2.0 com avisos próprios preservados.

### 1.1 Desenho do pipeline UTX 0–4 (load → UV → preparar referências → gerar vistas → enhancer → bake → GLB)
- **O que faz / encaixe:** é a arquitetura de estágios que a Oficina já tem em embrião na fila de jobs (entrada → forma → refino → cor → exportar). O desenho UTX separa "gerar vistas" (por tarefa: albedo, depois MR) de "assar" (baker dedicado) — separação que a Etapa COR pode espelhar ao ganhar um modo `pintura-ia`.
- **Licença:** GPL-3.0 (os JSONs de workflow são parte do pacote).
- **Veredito: RECRIAR o desenho** (não copiar os workflows). A Oficina não roda sobre ComfyUI por decisão DONO-01 — o ComfyUI seria exatamente "a plataforma dos outros" como fundação. O spike T7 usa o pacote como está, como motor externo opcional (ver §5).
- **Esforço:** baixo (é desenho, não código). **Risco:** baixo.

### 1.2 Geração de vistas guiadas (UTX 2 — 6 canônicas + 4 guiadas a 45°, referências por câmera, `refine` de consistência)
- **O que faz / encaixe:** gera 10 vistas do modelo com FLUX.2+LoRA: 6 canônicas e 4 diagonais "guiadas" pelo que as primeiras viram; aceita foto de referência **por câmera** (costas/esquerda/direita/topo/base), com `view_reference_strength` controlando por quanto dos passos o FLUX fica preso à foto; a passada `refine_denoise` repinta todas as vistas a partir de uma textura compartilhada para concordarem entre si. Encaixe: é a matéria-prima que falta ao modo `projecao` quando falta vista (hoje a COR-05 usa só as 4 canônicas e ignora diagonais/topo — pendência registrada) e ao caminho T4 (gerar vista que falta → projetar).
- **Licença:** o mecanismo é código GPL-3.0; a execução depende dos pesos dos §1.5–1.8.
- **Veredito: RECRIAR a técnica** — o conjunto de câmeras (6+4), a referência por câmera com força ajustável e a passada de consistência são decisões de desenho transferíveis para qualquer gerador de vistas que a Oficina venha a ter (inclusive o T4/Flow). Não recriar o sampler nem o condicionamento interno do FLUX (isso é o modelo, não a técnica).
- **Esforço:** médio (desenho de câmeras + fiação), alto se incluir geração própria de vistas. **Risco:** médio — vista gerada inconsistente inventa detalhe (a régua do projeto continua sendo: projeção da arte oficial manda; vista gerada é preenchimento declarado).

### 1.3 Baker de superfície (UTX 3 — `core/fastbake.py`, `core/bake.py`, `core/visibility_v3.py`)
- **O que faz / encaixe:** rasterizador UV por software + teste de visibilidade consistente por plano + fusão em duas bandas: no modo Quality, **os pixels da câmera frontal ficam onde ela vê bem a superfície; as outras câmeras assumem nos ângulos íngremes**; completa a superfície sem a dilatação agressiva que é a causa medida do "confete" da D1. O `visibility_v3.py` renderiza IDs de face por câmera (cache) para saber exatamente o que cada câmera enxerga. Encaixe direto: é a evolução do bake do T1 (`oficina3d/cor/projecao.py` + `_blender_cor.py`), que hoje mistura por facing + oclusão BVH e depois dilata 256 passes.
- **Licença:** GPL-3.0-only, com declaração expressa no THIRD_PARTY_NOTICES de que fastbake/visibility são **implementações originais de técnicas padrão** ("original implementations of standard techniques… not copies of another project's code").
- **Veredito: RECRIAR a técnica no nosso bake** — fusão ponderada por facing/visibilidade com prioridade de câmera e preenchimento contido. É a peça de maior valor para a D1 (ver §5). Copiar o código GPL é legal, mas ele é acoplado a ModernGL/ComfyUI; o nosso bake vive no Blender — reimplementar a técnica no nosso trilho sai mais limpo que portar o código.
- **Esforço:** médio. **Risco:** médio — manter o determinismo byte a byte que o projeto cobra e não regredir os IoUs medidos (0,72–0,79); medir SSIM frontal contra o T1 antes/depois, como manda a régua do spike.

### 1.4 Costura de atlas (`core/uv_seams.py`) e grão de material (`core/material_grain.py`)
- **O que fazem / encaixe:** `uv_seams.py` é implementação NumPy/SciPy própria de restrições de borda bilineares esparsas (texels ocupados fixos) para a cor concordar dos dois lados da costura do atlas — a Oficina hoje **mede** costura (`cor/costura.py`, COR-04: salto médio 93,49 na costura × 36,20 interno) mas não a **corrige**. `material_grain.py` é síntese por retalhos (quilting de retalhos de exemplo, junções de erro mínimo, amostragem triplanar de detalhe) — preenche zonas cegas com a **própria textura do modelo** em vez de borrar cor vizinha.
- **Licença:** GPL-3.0-only (ambos declarados implementações independentes no THIRD_PARTY_NOTICES; a referência de pesquisa Seamless/SIGGRAPH Asia 2017 é MIT mas **não** está embutida).
- **Veredito: RECRIAR as duas técnicas** — costura: evoluir `costura.py` de medição para correção (esforço médio, risco médio: mexer na UV aprovada da T5 exige re-medir ocupação/distorção). Grão/retalhos: candidato para a fase de preenchimento de zonas cegas pós-A3 do estudo da D1 (esforço médio-alto, risco médio — síntese pode inventar padrão onde a arte não define; usar só onde não há vista, e declarado).

### 1.5 Peso — FLUX.2 Klein base 9B Q4_0 GGUF (o modelo-base gerador das vistas)
- **O que faz / encaixe:** é o "cérebro" que pinta as vistas no UTX 2. Sem ele, UltraTex não gera nada.
- **Licença:** **BFL FLUX — licença de modelo não comercial** (README §"Model terms" do THIRD_PARTY_NOTICES: "The selected FLUX.2 Klein base 9B model uses BFL's FLUX non-commercial model license"; `component_manifest.json`: "BFL FLUX non-commercial model license; quantizer provenance not established from local filename" — o arquivo GGUF vem da Unsloth, conforme a tabela de downloads do README). Outputs comerciais são permitidos "subject to its restrictions"; o **uso comercial do modelo** pede licença separada da BFL.
- **Veredito: REUSAR só como motor do spike T7 / uso interno não comercial. PROIBIDO como dependência permanente** de qualquer uso comercial do app sem licença BFL separada. **Recriar: inviável** (treinar um modelo desta classe está fora do alcance do projeto). É o gargalo jurídico nº 1 da rota T7 — já registrado no estudo T7 do projeto e aqui confirmado em três fontes locais (README, THIRD_PARTY_NOTICES, manifesto).

### 1.6 Peso — VAE do FLUX.2 (`flux2-vae.safetensors`)
- **O que faz / encaixe:** codifica/decodifica os latentes das vistas geradas; peça do mesmo pacote de modelo do FLUX.2 Klein (o README manda baixar dos arquivos do repo BFL do Klein base 9B).
- **Licença:** o manifesto do pacote manda "check the license attached to the exact VAE distribution" — a distribuição de origem é o repo BFL do FLUX.2 Klein, ou seja, **viaja sob os termos BFL não comerciais** do modelo. (A cópia estagiada pela Oficina veio do espelho Comfy-Org, arquivo FP32 de mesmo conteúdo tensorial — proveniência registrada no inventário de downloads.)
- **Veredito: mesmo destino do §1.5** — spike/uso interno sim; dependência comercial permanente não, sem licença BFL.

### 1.7 Pesos — LoRA albedo e LoRA MR (`ultratex_flux2*.safetensors`) e decoder foreground-aware (`ultratex_flux2_decoder.pt`)
- **O que fazem / encaixe:** os adaptadores são o que transforma o FLUX.2 genérico em "pintor de modelos 3D": a LoRA albedo gera as vistas de cor; a LoRA MR gera as vistas de metalicidade/rugosidade (6 vistas a 1536); o decoder decodifica latentes com consciência de primeiro plano (fundo não vaza para a textura). São publicados por Yibo-Zhang/UltraTex no ModelScope (tabela do README).
- **Licença:** ponto fino e importante — o **código** original do UltraTex (yiboz2001) é MIT, mas o manifesto do pacote declara, para as três peças: *"independent artifact-specific grant not established"* / *"base-model obligations remain"*. Ou seja: **não há, nas fontes locais, uma concessão específica e clara para os pesos** além das obrigações do modelo-base (BFL).
- **Veredito: REUSAR somente dentro do spike T7** (uso local, sem redistribuir os pesos), com status **PENDENTE DE CONFIRMAÇÃO** para qualquer adoção permanente — antes de virarem peça definitiva, é preciso confirmar a concessão dos artefatos na página do publicador. **Recriar:** treinar adaptadores equivalentes é esforço **alto** e pressupõe o modelo-base (bloqueado no §1.5) — fora do horizonte atual.

### 1.8 Peso — Qwen3-8B Q6_K GGUF (encoder de texto)
- **O que faz / encaixe:** interpreta os prompts que guiam a geração das vistas; peça genérica e substituível da pilha.
- **Licença:** **Apache-2.0** na origem — `component_manifest.json` (fonte local): *"Qwen3-8B upstream Apache-2.0; quantized artifact provider not established from local filename"*; a tabela do README aponta o arquivo GGUF da Unsloth como fonte da quantização.
- **Veredito: REUSAR como está** (manter o aviso Apache-2.0 na distribuição). É a única peça de peso da pilha T7 com licença permissiva limpa. Risco residual baixo: a proveniência do artefato quantizado é a Unsloth (declarada no README), não um terceiro obscuro.

### 1.9 Upscaler — Real-ESRGAN `realesr-general-x4v3.pth` (UTX 2.5 Intelligent View Enhancer)
- **O que faz / encaixe:** amplia as vistas geradas antes do bake (no fluxo 8K, entre o UTX 2 e o UTX 3). Encaixe na Oficina: passo opcional equivalente entre "vistas" e "bake" do modo projeção/pintura — barato e desacoplado.
- **Licença:** **BSD-3-Clause** — tabela de downloads do README ("Real-ESRGAN release v0.2.5.0 … (BSD-3-Clause)") e aviso retido em `vendor/licenses/REALESRGAN-BSD-3-Clause.txt` no clone. (O THIRD_PARTY_NOTICES cita também o `RealESRGAN_x4plus.pth` v0.1.0 como "quality upscaler" de referência, com SHA próprio — são arquivos diferentes; o do fluxo 8K é o general-x4v3.)
- **Veredito: REUSAR como está** (manter o aviso BSD-3). **Esforço de integração:** baixo. **Valor para a D1:** médio — melhora detalhe das vistas antes do bake, mas não corrige alinhamento nem costura; entra como reforço, não como cura.

### 1.10 Peças vendorizadas e utilidades do pacote
- `vendor/optim.py` (MIT, do wrapper visualbruno/ComfyUI-UltraTex) e `vendor/sparse_attention/` (Apache-2.0): otimizações de execução GGUF **dentro do runtime ComfyUI-GGUF** — sem correspondente na arquitetura da Oficina. **Veredito: DESCARTAR para o app** (só existem dentro do spike).
- UTX 0 (load mesh / unwrap xatlas), UTX 4 (cache cleaner): a Oficina já tem equivalentes próprios (T5 xatlas; disciplina de jobs/cache do worker). **Veredito: DESCARTAR** (duplicidade).
- View Enhancer VOSR2 opcional (`core/super_resolution.py`, backend externo Apache-2.0): pesado e opcional até no pacote de origem; o Real-ESRGAN (§1.9) cobre o papel. **Veredito: DESCARTAR por ora.**

---

## 2. StableGen (clone: `referencias-codigo/stablegen/`)

Licença do código: **GPL-3.0** — arquivo `LICENSE` lido no clone (GNU GPL v3). Add-on de Blender que manda o trabalho para um servidor ComfyUI. O README (via relatório de verificação) avisa que **alguns modelos que ele roda têm licenças próprias, três deles não comerciais** (Qwen Image 2.1 — Qwen Research License; Bria FIBO 2.0 — CC BY-NC 4.0; modo Native do TRELLIS.2 — termos NVIDIA nvdiffrast/nvdiffrec).

### 2.1 Geração sequencial com contexto entre câmeras
- **O que faz / encaixe:** gera a vista de cada câmera **com as anteriores como contexto**, mantendo a textura coerente ao redor do modelo; projeta cada vista nas superfícies que a câmera vê. Encaixe: é a mesma família de técnica do §1.2 — consistência entre vistas é um dos remédios para a D1 (hoje cada vista canônica é projetada sem "saber" das outras).
- **Veredito: RECRIAR a técnica** se/quando a Oficina gerar vistas próprias (frentes T4/T7): condicionar cada vista nova às já aceitas. **Esforço:** médio-alto. **Risco:** médio.
- **O add-on em si: SÓ ESTUDAR.** Além do GPL, ele exige Blender 4.2–4.5 ou 5.1+ (o 5.0 é expressamente não suportado) e um servidor ComfyUI — como ferramenta de bancada até serviria, mas não como peça do worker headless da Oficina (que usa o Blender 5.2 como motor, não como GUI de pintura).

### 2.2 Edição localizada por máscara (Masked Edit)
- **O que faz / encaixe:** regenera só a região mascarada da textura. É exatamente a frente de **retrabalho local** (seção 8 do ESTUDO_MELHORIAS: R1–R4) já desenhada no projeto.
- **Veredito: RECRIAR a técnica** quando a frente de retrabalho for executada (máscara → regenerar/reprojetar só a região → costura tratada). **Esforço:** médio. **Risco:** médio (a borda da máscara é onde nasce costura nova — a bateria de aceite da seção 8.5 já prevê isso).

### 2.3 Mapas PBR via Marigold (albedo/roughness/metallic/normal estimados das vistas)
- **O que faz / encaixe:** estima mapas PBR a partir das vistas geradas e os projeta/assa como a cor. Encaixe tentador para a T6 (delight + PBR simples), cuja rota própria hoje é barata e geométrica (roughness de luminância/contraste; normal da malha alta via F1).
- **Licença:** os pesos do Marigold **não estão no clone** e o README do StableGen ressalva que os modelos têm termos próprios — nas fontes locais deste estudo, a licença dos pesos do Marigold fica **PENDENTE DE CONFIRMAÇÃO**.
- **Veredito: SÓ ESTUDAR por ora.** A T6 própria continua sendo a rota: custo zero de GPU/disco e sem dependência nova. Reavaliar só se a T6 medida ficar aquém e a licença do Marigold for confirmada como permissiva.

---

## 3. SUPRA-Tex (clone: `referencias-codigo/supra-tex/`)

Licença do código-fonte original: **MIT** — arquivo `LICENSE` lido no clone ("MIT License, Copyright (c) 2026 SUPRA-Tex Authors"). O repositório embute componentes de terceiros com termos próprios (THIRD_PARTY_NOTICES lido no clone): TRELLIS/TRELLIS.2 e Tencent (MIT), GLIDE (MIT), runtime FireRed (Apache-2.0), componente sob licença DINOv3 — e o **material adapter sob Qwen Research License** (texto integral reproduzido no THIRD_PARTY_NOTICES do clone: uso **não comercial, só pesquisa/avaliação**).

### 3.1 Pipeline de texturização com completação de regiões não vistas
- **O que faz / encaixe:** de uma imagem gera GLB relightable (base color + metallic + roughness), preservando detalhes da referência e **completando as superfícies que a imagem não mostra** com um Interleaved Flow Transformer. É, em tese, a resposta mais completa ao problema das zonas cegas da D1.
- **Veredito: SÓ ESTUDAR (na prática).** O código MIT poderia ser reusado legalmente, mas a execução exige Linux + CUDA 12.4 e recomenda GPU ≥48 GB (offload de CPU até 24 GiB) — a RTX 4060 de 8 GB do CUNHADO-PC está abaixo do piso descrito nas fontes. Reuso inviável na máquina ≠ reuso útil. **Recriar a técnica** de completação é esforço **alto** (transformer de completação treinado) — fica como referência de desenho para as frentes de preenchimento, não como plano.
- **O material adapter (§3.2) contamina a saída PBR:** mesmo rodando o código MIT, os mapas de material sairiam de um componente não comercial.

### 3.2 Material adapter (Qwen Research License)
- **Veredito: SÓ ESTUDAR — nunca copiar, nunca embutir, nunca usar em contexto comercial.** Licença de pesquisa/avaliação não comercial, confirmada no texto integral dentro do próprio clone. É a peça "proibida" mais clara deste estudo depois do FLUX.2.

### 3.3 Geração de vista traseira (`supratex/backview/`)
- **O que faz / encaixe:** gera a vista das costas a partir da frente, mantendo a identidade de material — parente direto do caminho T4 (vista que falta → projetar).
- **Veredito: RECRIAR a técnica** no desenho do T4 (a ideia "gerar a vista ausente condicionada à identidade" é a mesma do §1.2/§2.1); o código MIT é reusável em tese, mas vem acoplado à pilha deles (modelos + renderers próprios), então o aproveitamento prático é de desenho, não de arquivo. **Esforço:** médio-alto. **Risco:** médio (vista inventada precisa ser declarada como preenchimento, nunca como arte).

---

## 4. Eyek (clone: `referencias-codigo/eyek/`)

**Licença: NÃO LOCALIZADA** — sem arquivo LICENSE no clone, sem campo `license` no `Cargo.toml`, sem menção no `bl_info`/README (conferido por busca nos três). Código pequeno: `__init__.py` de 292 linhas + núcleo Rust `src/main.rs` de 840 linhas.

- **O que faz / encaixe:** add-on de Blender que projeta várias imagens (câmeras/empties) num **único UV existente**, com alfa, UDIM por padrão e shadowing opcional (projeção não atravessa o objeto). É, funcionalmente, um primo do nosso T1.
- **Veredito: SÓ ESTUDAR — nunca copiar código** (sem licença, vale "todos os direitos reservados"). E nem precisa: **a técnica já foi recriada pelo projeto** — o T1 (COR-01) faz projeção multivista sobre UV com peso por facing e oclusão BVH, com código nosso. O único recurso dele que o T1 não tem é **UDIM**, de valor baixo para GLB de jogo (atlas único é o padrão do projeto). Esforço de recriar UDIM, se um dia fizer falta: médio; prioridade: nenhuma agora.

---

## 5. Comfy BlenderTools (clone: `referencias-codigo/comfy-blendertools/`)

**Licença: NÃO LOCALIZADA** — sem arquivo LICENSE no clone e sem menção de licença no README (conferido por busca). Repositório pequeno, sem releases; `requirements.txt` inclui `nvdiffrast` (termos próprios da NVIDIA — cautela extra registrada no relatório de verificação a propósito de outro projeto).

- **O que faz / encaixe:** nós de ComfyUI que chamam o Blender como processo: unwrap (xatlas etc.), *Texture Projection Bake* (projeta imagens de várias câmeras e assa numa textura), *Multiview Texture Bake* (projeta renders multivista em **vertex colors** e assa no UV) e exportação de GLB.
- **Veredito: SÓ ESTUDAR — nunca copiar código.** E, como no Eyek, há equivalência própria completa: xatlas = T5; projection bake = T1; multiview→vertex color = T2 (que inclusive nasceu por desenho próprio, COR-07). Nada a recriar de novo; o valor do clone é auditoria comparativa (DONO-02), só.

---

## 6. Demais soluções da pesquisa (sem clone local; fontes = relatório de verificação)

### 6.1 InstaMAT Studio (Pioneer)
- Software **fechado**, gratuito no plano Pioneer com **uso comercial permitido + atribuição obrigatória**, para quem tem receita anual **ou** financiamento total < US$ 100 mil (página oficial, via verificação).
- **Veredito: DESCARTAR como peça do app.** Não há componente embutível: é um aplicativo externo completo — usá-lo como etapa seria exatamente o "app que sabe usar a plataforma dos outros" que a DONO-01 proíbe como fundação. Pode existir como ferramenta manual externa de acabamento, fora do pipeline e por decisão do Mestre; nunca como dependência. As ideias (materiais inteligentes em camadas) são inspiração de desenho, não código acessível.

### 6.2 Open Painter
- Estúdio de textura **dentro do Blender 5.2+**, **GPL-3.0-or-later** (site oficial, via verificação): camadas, máscaras inteligentes, canais PBR, trabalho offline.
- **Veredito: DESCARTAR como componente do app** (é ferramenta de autoria manual com GUI, não motor para o worker headless). Uso legítimo possível: ferramenta de bancada do operador para retoque manual num Blender interativo — fora do pipeline automático, sem custo de licença além do GPL da própria ferramenta.

### 6.3 Hunyuan3D-Paint 2.1 / fork 2GP (frente T3 já existente)
- Não é clone desta leva, mas consta para o mapa ficar completo: o Paint oficial pede **21 GB de VRAM** só para textura (README oficial, via verificação) — inviável direto na 4060; o fork 2GP (alvo ~6 GB com offload e OOM relatado) é a rota do spike T3, **depois** do T7 por decisão registrada. Os pesos Hunyuan viajam sob os termos da Tencent (o projeto já registra, na DONO-01, que licenças tipo MIT/Tencent dos motores exigem manter os avisos). **Veredito: segue o plano T3 existente** — motor opcional sob demanda (Ouro Negro/Lendário), nunca fundação; nada muda por este estudo.

### 6.4 Yedp UV Painter
- **NÃO LOCALIZADO em nenhuma fonte primária** (sem repo, sem página oficial — só um título de post de Reddit espelhado). Já retirado do plano do projeto pela correção de 2026-11-01. **Veredito: DESCARTAR** — não existe peça para reusar, recriar ou estudar com lastro.

### 6.5 Material Maker, MeshCoat, Poly Haven (citados na pesquisa, fora do escopo de clones/verificação)
- Não foram clonados nem verificados em fonte primária nesta leva. **Veredito: PENDENTE DE CONFIRMAÇÃO** — nenhuma conclusão de licença ou de encaixe é afirmada aqui; se um dia entrarem no plano, exigem a mesma verificação peça a peça antes.

---

## 7. Mapa final — o que entra no app, por qual porta, em ordem de valor para a D1

A D1 (fidelidade da cor: mosaico/confete, rosto ilegível, IoU 0,72–0,79, cobertura direta ~19–20%) é o problema atual; o mapa ordena por valor contra ela.

| # | Peça / técnica | Porta de entrada | Onde pousa na Oficina | Esforço | Risco |
|---|---|---|---|---|---|
| 1 | **Fusão de bake ponderada** (câmera boa manda no seu território; sem dilatação agressiva) — técnica do baker do UltraTex (§1.3) | **RECRIAÇÃO** | Evolução do T1: `cor/projecao.py` + `cor/_blender_cor.py` | Médio | Médio (determinismo + não regredir IoU/SSIM) |
| 2 | **Correção de costura** (restrições de borda no atlas) — técnica do `uv_seams.py` (§1.4) | **RECRIAÇÃO** | Evolução do `cor/costura.py`: de medição (COR-04) para correção | Médio | Médio (re-medir a UV da T5) |
| 3 | **Real-ESRGAN general-x4v3** (§1.9) | **REUSO** (BSD-3) | Passo opcional de enhance das vistas, entre vistas e bake | Baixo | Baixo |
| 4 | **Conjunto de câmeras 6+4 e referência por câmera** (§1.2) | **RECRIAÇÃO** (desenho) | Modo `projecao` ganha diagonais; fecha a pendência "diagonais ignoradas" da COR-05 | Médio | Médio (vista gerada = preenchimento declarado) |
| 5 | **Preenchimento por retalhos da própria textura** (§1.4, material grain) | **RECRIAÇÃO** | Fase de zonas cegas pós-A3 (difusão por adjacência 3D) do estudo da D1 | Médio-alto | Médio |
| 6 | **Consistência sequencial entre vistas** (§2.1) + **vista ausente condicionada** (§3.3) | **RECRIAÇÃO** (desenho) | Desenho do T4 (gerar vista que falta → projetar) | Médio-alto | Médio |
| 7 | **Edição localizada por máscara** (§2.2) | **RECRIAÇÃO** | Frente de retrabalho local (seção 8 do ESTUDO_MELHORIAS) | Médio | Médio |
| 8 | **Pilha UltraTex completa** (pacote GPL + FLUX.2/VAE/LoRAs/decoder) (§1.1, §1.5–1.7) | **REUSO como motor externo de spike** (T7), com réguas pré-registradas (VRAM ≤ 8.188 MB, ≤ 45 min, SSIM frontal ≥ T1, zero OOM) | Modo `pintura-ia` **opcional e substituível**, nunca fundação | Baixo (já estagiado) | **Alto jurídico** (BFL não comercial + concessão dos adaptadores pendente) |
| 9 | **Qwen3-8B GGUF** (§1.8) | **REUSO** (Apache-2.0) | Dentro da pilha do item 8; peça genérica | Baixo | Baixo |
| 10 | **Convenção de canais MR do glTF** (G = roughness, B = metallic) | **REUSO** (padrão aberto glTF, sem licença de código) | T6 (PBR próprio) grava nos canais certos desde já | Baixo | Baixo |

**Não entra, em nenhuma porta:**
- **Material adapter do SUPRA-Tex** (Qwen Research License — só pesquisa não comercial): proibido embutir/copiar/usar comercialmente (§3.2).
- **Código do Eyek e do Comfy BlenderTools** (sem licença): proibido copiar; técnicas já existem em versão própria (T1/T2/T5) (§4, §5).
- **FLUX.2 + VAE como dependência permanente** sem licença BFL separada (§1.5, §1.6).
- **InstaMAT como etapa do pipeline** (fechado, externo; no máximo ferramenta manual fora do app) (§6.1).
- **Yedp** (inexistente em fonte primária) (§6.4).

**Pendências de confirmação (não chutar — confirmar antes de adotar):**
1. Concessão específica dos pesos LoRA albedo/MR e do decoder do UltraTex (manifesto local: "grant not established") — confirmar na página do publicador (Yibo-Zhang/UltraTex, ModelScope) antes de qualquer adoção permanente.
2. Licença dos pesos do Marigold (se a rota §2.3 for reavaliada).
3. Material Maker, MeshCoat e Poly Haven — sem verificação nesta leva (§6.5).

---

## 8. Síntese para o Mestre (linguagem simples)

A maior parte do que presta nessas ferramentas **não é o programa delas — é o truque**. Os truques bons (como misturar as vistas sem borrar, como costurar o atlas sem salto de cor, como preencher o que a câmera não vê usando a própria textura) a gente **recria com código nosso**, e é isso que ataca direto a pintura feia de hoje. O que dá para **reutilizar** de verdade é pouco e específico: o ampliador Real-ESRGAN (licença livre de verdade) e o encoder Qwen3 (Apache-2.0). O coração do UltraTex — o modelo FLUX.2 — tem licença **não comercial**: serve para o nosso teste interno (spike T7), mas **não pode ser a fundação** do seu app sem uma licença separada da empresa dona dele. E duas das ferramentas mais citadas (Eyek e Comfy BlenderTools) **não têm licença publicada**: podemos olhar e aprender, mas não copiar uma linha — sorte que o nosso app já faz, com código próprio, tudo o que elas fazem.
