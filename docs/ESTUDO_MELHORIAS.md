# ESTUDO DE MELHORIAS DA OFICINA 3D — backlog, Etapa COR e função futura de animação

- **Autor:** Muse (CM-000009), como pesquisador do projeto Oficina3D.
- **Data:** 2026-11-01. **Natureza:** estudo — nada aqui foi implementado.
- **Ordem de origem:** QUAL-02 do Mestre (2026-11-01, 00:35) — "forma não é o app pronto": o app precisa **texturizar e pintar** (profundidade/cor), e há muitas frentes de melhoria. Ampliação de escopo (01/11, 00:44): **animação/movimento** entra como função **futura e opcional**, e cada item do backlog traz a **bateria de testes rigorosa sob medida** que provaria a melhoria (padrão do agente Crítico).
- **Método:** leitura integral das fontes fundadoras, dos docs vivos do projeto no PC, das auditorias do Crítico, das cartas e análises do Claude (CM-000008) no Notion (somente leitura) e pesquisa web de 01/11/2026. Cada juízo separa **VERIFICADO** (fonte primária lida/medida), **RELATADO** (fonte secundária do projeto) e **HIPÓTESE**.

## 0. Leitura de realidade antes de tudo

1. **Hardware real ≠ hardware dos documentos fundadores.** O PLANO fundador e as análises das cartas foram escritos para o "PC Gusta" com **GTX 1660 Super 6 GB**. A máquina real de construção é o PCDANASA: **RTX 4060 8 GB, 32 GB de RAM, i5-12600KF, SSD**. Toda conclusão do tipo "não cabe" herdada das cartas precisa ser re-medida em 8 GB — várias continuam verdadeiras (Paint nominal 24,5 GB), mas a margem mudou.
2. **Estado real do app hoje (v2, Fase 1):** entrada → forma (5 motores Hunyuan/TripoSR) → refino (≤50 mil triângulos, pivô nos pés, Y up, frente +Z) → saída GLB **sem cor** (white mesh; o TripoSR até produz cor, mas o refino a descarta no caminho atual — há um `triposr_bake_texture.patch` no clone). Suíte: 204 testes OK em `.venv_app`. Prova C: fatia do Orc aprovada nos dois motores turbo; Capríleo/Besta em bateria.
3. **A frase que resume o projeto** (REVISAO_E_ROTEIRO.md, escrita por mim e conferida pelo Crítico): *"Textura de verdade (paint) está fora da v2 atual: a saída é forma + cor de vértice. Se o Mestre quer textura pintada, é escopo de Fase 2."* — QUAL-02 promoveu esse escopo a obrigação.

---

## 1. Inventário fonte a fonte

Formato: **proposta → o que o Claude (CM-000008) achou/fez → meu juízo de aproveitamento hoje.**

### 1.1 PLANO_OFICINA_3D_PARA_CLAUDE_CODE.md — Claude CM-000008-I0001 (PC Gusta), v2, 2026-10-27
Documento fundador, escrito pelo próprio Claude a partir da sessão real dele com o Mestre. Pontos que importam:

- **§6 — as 4 alternativas da Etapa COR**, da mais segura à mais ambiciosa:
  - **A. Cor de vértice do próprio motor** — grátis, qualidade baixa.
  - **B. Projeção das vistas originais do RPG sobre a malha (bake no Blender headless)** — determinística, sem IA pesada, preserva a arte canônica; riscos: alinhamento de câmera com a malha gerada e costuras; **testar primeiro no Orc**.
  - **C. Gerador de textura por IA (Hunyuan3D-Paint)** — melhor visual; nominal ~24,5 GB de VRAM total; "provavelmente inviável a 6 GB sem offload pesado **[A VERIFICAR com o fork 2GP]**".
  - **D. Textura em nuvem gratuita (HF Space via gradio_client)** — motor *opcional*, limitado por cota, nunca dependência única.
- **§5.0 — diferenciais projetados:** escore de fidelidade de **silhueta (IoU)** por vista (render da malha × máscara alfa da imagem-fonte), permitindo *retry* de sementes; **divisor de folhas** (sheet splitter) já provado nas folhas do Capríleo (componentes conexas de alfa >10 → watershed quando as vistas se tocam; nunca cortar em quadrantes iguais); validações de entrada (fundo não removido, baixa resolução — Besta 768×512 —, objeto cortado na borda).
- **§3:** a hipótese do corpo-base do IBX-178 incorporada como **modo corpo-base** do app (tipo de job). Ressalva do próprio ChatGPT preservada: T-pose + muitos polígonos **não** garantem topologia animável.
- **§2.2 (medições da época):** `white_mesh.glb` da nuvem Hunyuan = 283.111 vértices / 566.538 triângulos, **sem material/textura/esqueleto**, Orc armado com machado fundido, fora de T-pose. Erro clássico registrado: folhas de 4 vistas enviadas inteiras ao Tripo viraram "4 bichinhos soltos" (erro de entrada, não do modelo).
- **§8:** Fase 3 Cor com aceite = alternativa A ou B (C só se couber); Orc + Capríleo com cor/textura visivelmente fiéis à arte, **julgados pelo Mestre**. Fase 4 = rig humanoide simples + renders de sprite em 8 direções.

**Juízo hoje:** é a espinha dorsal correta e continua válida. A alternativa B é a recomendação deste estudo (seção 3). O "[A VERIFICAR]" da alternativa C foi verificado na web nesta rodada — ver 1.12: o veredito muda de "provavelmente inviável" para **"testável com offload, lento, com risco de compilação no Windows"**.

### 1.2 BRIEF_ORC_CORPO_BASE_TPOSE.md — Claude, 2026-10-27
Brief (prompts EN/PT + checklist de aprovação) para gerar, numa IA de imagem externa (o Claude não tinha gerador de imagem), o **corpo-base do Orc em T-pose**: manter pele oliva/músculos/presas/cavanhaque; remover armadura, pele de lobo, machado, cicatrizes e cabelo. Sucesso = corpo fechado e simétrico, dedos separados e contáveis, nada fundido. Status PROPOSTO; **as imagens nunca foram geradas**.

**Juízo hoje:** barato e estratégico — é a matéria-prima que mais aumenta a chance de sucesso de **todas** as etapas futuras (forma multivista coerente, projeção de cor, rig). Reaparece no backlog como preparação (item P-0) e na seção de animação (4.6). Depende de geração de imagem pelo Mestre/Flow (custo zero — ver 1.6).

### 1.3 IBX-178 — ChatGPT (Mestre-side), 2026-10-27 → leitura do Claude
Carta consultiva (INFORMAÇÃO, P3, sem ACK): a inspeção do `white_mesh.glb` do Mestre (283.111 vértices, 566.538 triângulos, malha conectada, sem materiais/esqueleto/animação, machado integrado) e a **hipótese do corpo-base**: usar a geração 3D por IA como geradora de corpos-base em T-pose (sem armadura/armas/acessórios fundidos, dedos diferenciados), com o Blender como ferramenta principal de retopo, acessórios separados, UV/textura, rig e sprites. A própria carta se declara **HIPÓTESE NÃO VALIDADA** e manda comparar com bases reutilizáveis de Blender.
**O que o Claude fez:** leu (Estado LIDA por CM-000008-I0001), incorporou ao PLANO (§3, modo corpo-base) e escreveu o BRIEF operacional (1.2). No Diário registrou a carta como consultiva, sem ordem.
**Juízo hoje:** hipótese continua **não testada** — nenhum corpo-base foi gerado ainda. É o teste mais barato com maior efeito cascata (corpo limpo → projeção melhor → rig viável). Entra no backlog como P-0 junto com o BRIEF.

### 1.4 IBX-179 — ChatGPT → análise "Mensagem 1" do dossiê CM-000008 (I0002, 28–29/10, com auditor independente)
A carta sugeria TripoSG, TripoSF e talvez um mês pago da Tripo AI como estudo. A análise do Claude (perito + auditor que tentou refutar):

- **TripoSG (MIT, só forma, 1 imagem):** vale testar como 7º motor, com contornos: import de `diso` opcional, `use_flash_decoder=False`, venv separado, rembg/u2net no lugar do RMBG-1.4 (licença não comercial). Critério desenhado: pico ≤5,5 GB, ≤15 min, IoU ≥ Hunyuan mini no Orc.
- **Correção do auditor (importante):** a receita `enable_model_cpu_offload()` da carta **quebraria** — o pipeline não define `model_cpu_offload_seq`; é preciso defini-lo à mão ou usar offload sequencial (lento). Pesos fp16 ~4–4,8 GB residentes → "provavelmente cabe em 6 GB sem offload (hipótese)".
- **TripoSF:** só referência (só o VAE foi liberado; 12 GB; flash-attn/spconv inviáveis no Windows).
- **Tripo paga:** **adiar** — benchmark antes no plano gratuito; pagar 1 mês só com lista fechada de 20–40 assets, ToS lidos e Fase 4 estável; a compra é do Mestre.
- **Achados fora da carta (mais valiosos que ela):** **DetailGen3D** (refino de detalhe sobre saídas grosseiras), **HoloPart** (separar partes — mas o auditor corrigiu: ele **não segmenta sozinho**, pede máscara por face; **PartCrafter é mais eficiente** para a hipótese do IBX-178, pois gera as partes direto da imagem), UniRig/SkinTokens/AniGen (rig — só nuvem/GPU futura), MIDI-3D (cenários).
- **Textura nesta análise:** a textura da demo do TripoSG vem do **MV-Adapter** (SDXL, UV 4096, CV-CUDA voltado a Linux) — **não cabe**; frase-síntese do analista: *"a Fase 3 (projeção das vistas) da Oficina é o caminho viável"*. E o diagnóstico que QUAL-02 confirmou: *"o maior gargalo hoje não é a forma bruta, e sim a cor/textura e o rig"*; com o realismo estilizado (sem pixel art para esconder defeitos), **textura, topologia e rig viram o gargalo**.

**Juízo hoje:** análise de alta qualidade, quase tudo aproveitável. Atualizações: (i) os pesos do TripoSG (7,95 GB) e do PartCrafter/DetailGen3D **já estão no PC** (pasta de estudo `RPG_Local\oficina3d_ia`, 26,3 GB; zips com SHA-256/MD5 conferidos no Drive `modelos_guardados` pela ZIP-01) — o teste do TripoSG ficou mais barato do que o plano supunha; (ii) em 8 GB (não 6), o TripoSG fica ainda mais plausível; (iii) DetailGen3D/PartCrafter seguem como estudo — nenhum dos dois foi executado até hoje.

### 1.5 IBX-187 — ChatGPT (parecer arquitetural) → análise "Mensagem 9" do dossiê (I0002, 29/10)
Carta que junta as 8 anteriores; o Adendo R02 registra decisões do Mestre (Arcane > Castlevania > Blue Eye Samurai; desenho adulto pintado; pixel art só como opção) e a Oficina como **fábrica completa**, com **estudo de colorização: TripoSR, xatlas, Material Maker, ArmorPaint, Krita**. A análise do Claude verificou ~35 itens na web e concluiu, na parte de cor:

- **Diagnóstico certo (nas palavras dele):** *"Gerar malha não é o mesmo que ter cor fiel. TripoSR inventa cor, e projeção UV ingênua atravessa o corpo e duplica sombras."* — ou seja: projeção sim, mas **com teste de profundidade/oclusão e peso por ângulo**, não projeção ingênua.
- **Hunyuan3D-2GP:** README pede `--profile 4` entre 6–9 GB; 6 GB para forma e **24,5 GB para forma+textura** — "isso explica o resultado sem textura do diário". (Na época: Paint inviável local.)
- Ferramentas de pintura avaliadas: **Material Maker 1.8** (MIT, roda em Godot; autoria procedural — não é runtime Web), **ArmorPaint** (binários pagos; build exige VS+clang), **Krita** (GPL3; pintura manual 2D da textura).
- Ideias executáveis deixadas: **comparador A/B/C/D do Orc** (4 variantes × 8 ângulos, mesma luz flat em EEVEE, folha de contato PNG para o Mestre; medir tempo e tamanho de textura) e **validador headless de GLB** (importa, conta triângulos/materiais/ossos/animações, **verifica textura ligada ao albedo** — o caso do `texture.png` solto do TripoSR — e tira 8 capturas) virando ferramenta MCP `validate_asset`.
- Alerta de licença que a carta não detalhou: **Hunyuan3D tem licença territorial com limite** (a licença comunitária Tencent não se aplica em UE/Reino Unido/Coreia do Sul — confirmado também na pesquisa web de hoje). RF-03 do Mestre liberou o uso no projeto, mas o registro de motores deve manter a marca de licença por motor (a ideia "só licença comercial" do Msg1).

**Juízo hoje:** o comparador A/B/C/D e o validador são exatamente o formato de prova que o Crítico exige — incorporados às baterias da seção 2. O diagnóstico "projeção ingênua atravessa o corpo" define os requisitos técnicos do item T1.

### 1.6 Dossiê CM-000008 (página-mãe, 28/10) e missões executadas — I0002
Método declarado: para cada carta, um perito leu tudo e verificou na web; um **auditor independente tentou refutar**. Missões com resultado direto para a Oficina:

- **Carta 8 / Flow (IBX-186) — E1/E2 VERIFICADOS:** Google Flow acessível sem gasto (conta AI Pro do Mestre, 836 créditos); **geração de imagem não gasta crédito** (836 → 836 após gerar). Avaliação prática: de 2 saídas da mesma folha ortográfica, uma era coerente e a outra **inventava ornamento na vista de costas**. Conclusão do Claude: o Flow é uma **"fábrica de referências de custo zero"** — usar sempre 2+ saídas e escolher a mais consistente. É a base do caminho B de cor do relatório central (repintura → projeção) e do corpo-base (ART-01).
- **E3 — basemesh MPFB:** proposto para o PC Gusta (43,8 MB + 267 MB de assets CC0) porque o notebook não comportava. Vira a rota de rig humanoide do relatório central.
- **Correção de direção de arte pelo Mestre** (registrada no dossiê): realismo estilizado/cartoon realista, **não** pixel art — as ideias de pixel art das cartas passam a valer só como técnica de luz/render/sprite-bake.

**Juízo hoje:** o Flow gratuito muda o cálculo da Etapa COR: vistas faltantes, turnaround e repintura consistente podem ser **geradas** e depois projetadas — o caminho B não é concorrente da projeção, é um **alimentador** dela.

### 1.7 Relatório central "Oficina 3D v2" — Claude do notebook, 31/10 (síntese das Mensagens 1–14, da auditoria da sessão e dos relatórios do Codex)
O documento que efetivamente guiou a reconstrução. Fatos e plano:

- **V1 (27/10, 2h42):** entrada 1–4 vistas, forma Hunyuan, refino 50 mil tris, GLB com prévias e IoU, 5 portas. **"O que nunca existiu: cor, retopologia, rig e animação. As Fases 3 e 4 morreram no limite de uso (429)."** Na quebra do PC perderam-se ~3.600 linhas; recuperado o contrato/config/job/MCP/scripts/prompts — reconstruível 60–85% do núcleo; **"a cor e os extras têm de ser refeitos"**.
- **"O que faltou para ficar perfeito" (a lista-mãe do backlog):**
  1. **Cor: projeção das vistas (C9) e o pipeline inverso com repintura no Flow (C8)**;
  2. Retopologia: **QuadriFlow, 8–20 mil quads, com bake de normal**;
  3. Rig: humanoide **MPFB game_engine**; quadrúpede **Rigify**; bestas exóticas **Mesh2Motion**;
  4. Animação: **UAL1/2 (ZIPs CC0) + Retarget KBS**, IK nativo do Godot, marcha procedural;
  5. Validação: **Godot headless** com métricas e 8 capturas;
  6. Exportação: Compatibility, compressão, LOD; aceites EXP-01/EXP-02;
  7. Derivados: **sprites, tokens e retratos com manifesto**;
  8. Qualidade: várias sementes, escolhendo a melhor;
  9. UX: galeria, nota do Mestre, presets, reprocessar uma etapa, acesso pelo celular via Tailscale com token;
  10. Robustez: worker como serviço, retomada, limpeza de disco;
  11. Referências: módulo próprio para o Flow + MCP `catalogar_referencia`;
  12. Corpo-base: gerar o Orc em T-pose no Flow.
- **Plano v2:** Fase 2 = retopo QuadriFlow + **cor pelo caminho A (projeção) e pelo B (Flow repinta → projeta), comparando os dois** + testar TripoSG e DetailGen3D um por vez. Fase 3 = rig/animação/exportação. Fase 4 = produto (MCP 17 ferramentas, galeria, sprites, referências, Tailscale).

**Juízo hoje:** este estudo é, em grande parte, a execução analítica dessa lista com preços, riscos e baterias atualizados para a RTX 4060 e para o estado pós-Fase 1. Nada da lista foi descartado; a ordem é que muda (cor antes de retopo, porque QUAL-02 manda textura primeiro — mas ver a dependência T5/F1).

### 1.8 Biblioteca de downloads e estudos — PC Gusta (I0002, 29/10)
136 itens consolidados das 9 cartas + 3 pesquisas extras (63 para o Drive, 40 repositórios só-estudo, 8 pesos grandes, 16 que a Oficina já tem, 9 dependentes de decisão). **Prioridade 1:** MPFB 2.0.18, assets MakeHuman (CC0), SpriteSheetMaker 5.3.1, Mesh2Motion, mcp-for-blender, uv. Itens do itch.io (**UAL1/UAL2**, bibliotecas de animação CC0) exigem ação manual.
**Juízo hoje:** a biblioteca já resolveu a curadoria da animação futura (seção 4) — falta só baixar/executar na hora certa. Nenhum item de textura novo além dos já citados (xatlas aparece via carta IBX-187).

### 1.9 Docs vivos do projeto (PC, `app\docs\`) e `v1_recuperado\`
- **ARQUITETURA.md:** contrato v1 (caminhos antigos `E:\`), pipeline entrada→forma→refino→saída; o refino **já devolvia `silhueta_iou` por vista**; tabela de motores da época registra TripoSR "48 s, **com cor**, forma ruim" (na 1660) — a cor do TripoSR existia na v1 como subproduto, nunca como etapa.
- **USO_PARA_IAS.md:** 4 portas para a mesma fila; saída declarada: **só forma**; "Cor/textura: ver fases seguintes."
- **REVISAO_E_ROTEIRO.md:** os 8 critérios de "pronta" e as rodadas R1–R5; **R5 = "Fase 2 (decisão do Mestre): textura/paint, integração com Blender para limpeza da malha"** — QUAL-02 decidiu.
- **DECISOES.md:** ZIP-01 (PartCrafter/DetailGen3D/TripoSG = material de **estudo** do app próprio do Mestre; originais apagados só após hash conferido; TripoSG intocado), RF-03 final (Hunyuan liberado inclusive no resultado final), EXEC-02 (autorização total no projeto, com registro + Crítico), DONO-01/02 (app próprio e independente; referências **preservadas** para auditoria dos Comestres), QUAL-02.
- **REGISTRO.md (partes do Claude, 31/10 de manhã):** medição da pasta de estudo `oficina3d_ia` (TripoSG 12,6 GB; PartCrafter 10,2 GB; DetailGen3D 3,4 GB); execução da ZIP-01 com SHA-256/MD5 registrados (PartCrafter.zip SHA-256 `3332C55A…D191A`, DetailGen3D.zip `C2B0568E…4B48FA2`); sessão morreu no limite às 12:38 com o código da Fase 1 sem revisão/commit (recuperado depois por mim).
- **ERROS.md:** só 2 entradas (nível de caminho do plano; medição de SSD) — nada de textura.
- **`docs\v1_recuperado\` (inventário, 12 arquivos):** `.mcp.json`, `INICIAR_OFICINA3D.bat`, `LISTA_SESSAO_INSTALACAO.md`, `instalacao\` (baixar_modelos.py, instalar_triposr.bat, render_previa.py, testar_msvc.bat, teste_fase0_hunyuan.py, compat\torchmcubes), `oficina3d\config.py`, `job.py`, `servidor_mcp.py`. **Não** há código de cor/refino recuperado — coerente com "a cor tem de ser refeita".

### 1.10 Minhas auditorias (Crítico 1, 2 e adendo — `~/workspace/oficina-audit/`)
- **Auditoria 1:** desenhou as Provas A–D (a Prova C virou a bateria dourada) e o alerta P7 (imagens de teste pequenas demais distorcem qualquer conclusão — a Besta de 768×512 é o caso real).
- **Auditoria 2 + adendo:** N1 (eu apaguei 19 testes sem querer — lição permanente: **integridade da suíte é parte da prova**), N2/N3 corrigidos e conferidos; números finais da fatia do Orc: forma ≤41,4 s, VRAM ≤6.435 MB, GLB final 49.750 tris, determinismo byte-idêntico por semente nos dois motores turbo.
**Juízo:** o padrão de prova (conjunto dourado × sementes × réguas numéricas + nota do Mestre + auditoria independente) é o que cada bateria da seção 2 estende para cor e animação.

### 1.11 Relatório de continuidade v002 (Codex Local/Mestre, 01/11)
Relevante aqui: o acervo Orc/Besta/Capríleo está **indexado e recuperável** (117 ocorrências; 43 binários diretos no Drive — foi assim que as vistas da Besta e do Capríleo voltaram para a bateria); o pacote R13 (REF-PIPELINE) existe no Drive; regra permanente de preservação (arquivo útil em armazenamento persistente, verificado, localizável; duplicata por conteúdo antes de enviar).
**Juízo:** a Etapa COR depende de vistas canônicas íntegras — o índice é a garantia de que a matéria-prima da projeção existe e é autêntica (SHA-256 conferido na recuperação).

### 1.12 Pesquisa web (01/11/2026) — o que mudou desde as cartas
- **(a) Hunyuan3D Paint no fork 2GP:** o sistema de perfis do 2GP (mmgp) **orça a geração de textura em ~6 GB de VRAM nos perfis 4/5** (orçamento de 2.200 MB + offload agressivo para a RAM; tabela do DeepWiki: textura com perfil 4 = pico de 6 GB; perfil 3 = 9 GB). O pipeline de pintura é desacoplado: aceita **malha externa** ("bring your own mesh") + imagem. **Poréns:** (i) exige **compilar extensões C++/CUDA no Windows** (custom_rasterizer/mesh_painter — há `.bat` no fork; a v1 já previa `testar_msvc.bat`); (ii) os **pesos do Paint não foram baixados** na Fase 1 (só os DiTs de forma); (iii) velocidade com offload é desconhecida (esperar dezenas de minutos); (iv) a pintura é **sintetizada a partir de 1 imagem** — não usa as 4 vistas canônicas com fidelidade de pixel. Fontes: DeepWiki do 2GP (quick start, core concepts, memory optimization).
- **(b) Bake por projeção no Blender headless:** técnica padrão e madura — UV (Smart Project/xatlas) + Cycles bake DIFFUSE só-cor, selected-to-active com cage, margem "extend" contra vazamento nas costuras; projeção por câmera via UV Project/Project-from-View ou materiais com mapeamento por câmera assados para a UV final. A técnica anti-costura de referência (descrita publicamente por um addon comercial de pintura por IA): **peso por ângulo de facing + teste de profundidade projetivo + dilatação de UV + passe de inpainting mascarado** — exatamente o antídoto para o "atravessa o corpo" do Msg9. Fontes: DeepWiki AiMDoom (bake headless em lote), guia HeyGalatea (bake headless → glTF), página do Framanen AI Texture Studio (descrição da técnica).
- **(c) Alternativas abertas de texturização ≤8 GB:** **nenhuma provada** em Windows/8 GB nesta rodada. Paint3D (mapas UV 2K sem iluminação embutida, condicionado por imagem/texto — código de pesquisa, VRAM não confirmada); SyncMVD/TEXture (difusão SD, iterativos, lentos); MV-Adapter variante SD2.1 "<10 GB" mas com CV-CUDA de Linux (auditor do Msg1). TRELLIS.2 = 16–24 GB (fora). Conclusão: a escada realista é **vértice → projeção → Paint 2GP → nuvem opcional**.
- **(d) Animação:** ver seção 4 (UniRig ≥8 GB; Kimodo <3 GB com encoder na CPU; ARDY 6 GB).

---

## 2. Backlog priorizado de melhorias

Ordem = ordem de execução recomendada. Convenções: **Custo** separa tempo de desenvolvimento (sessões de trabalho), VRAM e disco. **Prova** = o que se mede. **Bateria do Crítico** = a bateria rigorosa sob medida que um agente Crítico independente deve rodar para aceitar o item (padrão do projeto: conjunto dourado Orc/Capríleo/Besta, réguas numéricas, adversarial, nota do Mestre onde houver juízo visual).

### P-0 — Preparação: corpo-base do Orc em T-pose (BRIEF + IBX-178) e vistas canônicas completas
- **O que é:** executar o BRIEF de 27/10 (gerar o corpo-base no Flow, custo zero de créditos, 2+ saídas e escolher a consistente) e garantir, via índice v002, o conjunto completo de vistas canônicas dos 3 personagens dourados em `testes\dourado\imagens\`.
- **Ganho esperado:** destrava qualidade em **todas** as frentes: forma multivista sem equipamento fundido, projeção de cor sem machado/armadura colados, e é o pré-requisito nº 1 do rig futuro.
- **Custo:** dev ~0 (é geração de imagem + curadoria); VRAM 0; disco desprezível. Depende de sessão com o Mestre/Flow.
- **Risco:** baixo. Risco real: escolher saída inconsistente do Flow (a falha "inventa ornamento nas costas" já foi observada) — mitigado pela regra das 2+ saídas e pelo checklist do BRIEF.
- **Prova:** checklist do BRIEF item a item (corpo fechado/simétrico, dedos separados e contáveis, zero equipamento) + arquivo persistido com SHA-256 e registro no REGISTRO.
- **Bateria do Crítico:** (1) conferir o checklist contra a imagem pixel a pixel (contagem de dedos nas 2 mãos); (2) gerar a forma do corpo-base no mv-turbo e medir IoU de silhueta nas 4 vistas — régua: IoU ≥ o do Orc armado atual; (3) adversarial: procurar assimetria/fusão em render 8 ângulos; (4) registrar divergências como defeito do artefato, não do pipeline.

### T1 — Etapa COR por projeção das vistas canônicas (bake no Blender headless) ★
- **O que é:** nova etapa `cor` (opcional, pós-refino): câmeras calibradas pela convenção de vistas do projeto posicionadas sobre a malha refinada; cada vista vira textura mapeada por câmera; bake para a UV final com **peso por ângulo de facing, teste de profundidade (só pinta o que a câmera vê), margem/dilatação** e preenchimento das zonas não vistas (v1: cor vizinha mais próxima/inpainting simples; evolução: T4/T3). Saída: GLB com textura de albedo embutida (1024 ou 2048 px conforme nível de qualidade).
- **Ganho esperado:** **o maior do projeto** — sai o "esqueleto branco", entra o personagem reconhecível com a **arte do próprio RPG** (fidelidade ao cânone é o critério do Mestre; nenhuma IA de pintura garante isso). Determinístico: mesma entrada → mesma textura (casa com o determinismo já provado na forma).
- **Custo:** dev alto (é a peça central da Fase 2: calibração de câmera é o trabalho fino); VRAM ~0 (bake em Cycles CPU ou EEVEE — GPU livre); disco ~0 (Blender 5.2 já instalado). Tempo por job: minutos (bake 2048² em CPU é o gargalo; medir).
- **Risco:** **médio-alto, concentrado num ponto**: o alinhamento entre as vistas 2D e a malha gerada (a malha não é uma projeção perfeita das vistas; proporções divergem). Mitigações: o IoU de silhueta já existente mede o desalinhamento antes do bake; aceitar "fidelidade de regiões" (rosto/cintura/pele) em vez de pixel-perfect; costuras tratadas por peso+profundidade+dilatação. Risco secundário: sombra embutida nas vistas vira "sombra pintada" (o Msg9 avisou) — v1 aceita; delight fica para T6.
- **Prova:** GLB texturizado do conjunto dourado; métricas por vista: **ΔE/SSIM** entre o render texturizado (luz flat) e a vista canônica correspondente; % de superfície coberta pelas vistas; folha de contato 8 ângulos; **nota do Mestre**.
- **Bateria do Crítico (sob medida para projeção):**
  1. **Fidelidade por região:** recortar regiões semanticamente estáveis (rosto, peitoral, pernas) dos renders e das vistas; SSIM por região ≥ régua definida no 1º run aprovado (baseline) e nunca regredir.
  2. **Costura:** renderizar 8 ângulos em luz flat e inspecionar as linhas de encontro de vistas; defeito = descontinuidade de cor visível a 100% de zoom nas junções frente/lateral e lateral/costas.
  3. **Atravessamento:** verificar que a cor da frente **não** aparece nas costas (teste do Msg9): amostras de cor em regiões-espelho devem diferir quando as vistas diferem (ex.: escudo nas costas do Capríleo).
  4. **Cobertura:** % de texels sem fonte (zonas cegas) reportada por personagem; régua: ≤ % combinado, e zonas cegas nunca no rosto.
  5. **Determinismo:** mesmo job 2× → SHA-256 da textura idêntico.
  6. **Adversarial:** rodar com a Besta (768×512, a menor resolução) e com uma vista faltante (só 3 vistas) — o app deve degradar com aviso registrado, nunca pintar lixo silencioso.
  7. **Regressão:** suíte unitária nova (calibração de câmera com malha sintética de geometria conhecida — cubo/esfera com vistas geradas por render: a projeção tem de reproduzir a cor exata nos polos das vistas).

### T2 — Cor de vértice imediata (alternativa A formalizada) + não descartar a cor do TripoSR
- **O que é:** (i) preservar a cor que o TripoSR já gera (o caminho atual a perde no refino — aplicar de verdade o `triposr_bake_texture.patch`/amostrar cor por vértice antes da decimação); (ii) oferecer o modo `cor: vertice` como nível rápido da etapa COR para qualquer motor (amostragem das vistas por projeção simples sobre os vértices da malha densa, antes de decimar).
- **Ganho esperado:** fim do "tudo branco" **já**, com custo quase zero; vira o nível Bronze da COR e a rede de segurança quando T1/T3 falharem.
- **Custo:** dev baixo; VRAM 0; disco 0.
- **Risco:** baixo. Qualidade intrinsecamente limitada pela densidade de vértices (25–50 mil tris = cor borrada) — deve ser **rotulada** como rascunho na UI/relatório para não virar "pronto" por engano (a lição do N2 da auditoria 2: texto velho engana).
- **Prova:** GLB com `COLOR_0` presente e render não-branco nos 3 personagens; tempo adicional por job ≈ 0.
- **Bateria do Crítico:** (1) presença de atributo de cor e material correto no GLB (validador T-P1); (2) render 4 ângulos × 3 personagens: cor média por região plausível vs vista (ΔE grosseiro); (3) garantir que o relatório do job **declara** o modo de cor usado (sem declaração = reprovado); (4) regressão: o caminho sem cor continua produzindo o mesmo GLB de forma de antes (SHA da geometria inalterado).

### T3 — Teste do Hunyuan Paint via fork 2GP (alternativa C reaberta) como motor opcional de pintura por IA
- **O que é:** spike controlado: baixar os pesos do Paint, compilar as extensões do texgen no Windows (MSVC), rodar `Hunyuan3DPaintPipeline` com perfil 4/5 do mmgp sobre a malha do Orc já refinada (bring-your-own-mesh), medir tempo/VRAM/qualidade. Se passar, vira o modo `cor: pintura-ia` (níveis Ouro Negro/Lendário da COR) — **opcional**, nunca o caminho padrão.
- **Ganho esperado:** textura **sintetizada completa** (inclui zonas que nenhuma vista alcança) com acabamento de pintura — o teto de qualidade visual das alternativas locais.
- **Custo:** dev médio (spike) / alto (integração); **VRAM: orçado 6 GB com offload** (perfil 4) — a medir; RAM 32 GB ajuda; disco: pesos do Paint (a medir no download; ordem de GB); tempo por job desconhecido (hipótese: dezenas de minutos com offload).
- **Risco:** **alto** em três frentes: compilação CUDA/MSVC no Windows pode falhar (a v1 já tinha `testar_msvc.bat` — nunca concluído); lentidão pode inviabilizar o uso na fila; e a pintura **inventa** a aparência a partir de 1 imagem (não é a arte canônica — pode divergir do cânone nas costas/laterais). Por isso: opcional e comparado, nunca padrão.
- **Prova:** o **comparador A/B/C/D do Msg9**: mesmo Orc, 4 variantes de cor (vértice / projeção / Paint / Flow+projeção), renders em 8 ângulos com a mesma luz flat, folha de contato para o Mestre + tempo e VRAM de cada uma.
- **Bateria do Crítico:** (1) pico de VRAM ≤ 8.188 MB e sem OOM em 3 runs seguidos na fila real (com gpu.lock ocupado por outro job antes — teste de contenção); (2) tempo total do job registrado — régua de aceite definida **antes** do spike (sugestão: ≤ 45 min no Orc para ser "usável sob demanda"); (3) fidelidade: SSIM/ΔE das vistas frontais vs canônica **não pode perder para a projeção (T1)** na frente; pode ganhar nas zonas cegas; (4) determinismo por semente (2 runs = textura igual ou divergência explicada); (5) se a compilação falhar: o spike termina com **relatório de falha** registrado (ERROS.md) e o item fecha como "inviável nesta máquina" — sem deixar o app quebrado (venv isolado).

### T4 — Repintura no Flow → projeção (caminho B do relatório central, C8)
- **O que é:** usar o Flow (grátis, verificado) para **gerar/repintar vistas consistentes** — turnaround completo, vista faltante, versão "limpa" sem sombra dura — e alimentar a projeção (T1) com essas vistas. Inclui o módulo de referências do relatório central (item 11: MCP `catalogar_referencia`).
- **Ganho esperado:** resolve os dois pontos fracos da projeção pura: **zonas cegas** (vistas que o Mestre não tem) e **inconsistência** entre vistas desenhadas em momentos diferentes. Mantém a projeção como mecanismo (determinístico) e usa a IA só onde ela é insubstituível: inventar a vista que falta.
- **Custo:** dev médio (fluxo é manual/sem API oficial — automação limitada; tratar como etapa assistida); VRAM 0 local; disco ~0; custo em créditos = 0 para imagem (verificado).
- **Risco:** médio — o Flow inventa detalhes (a falha observada: ornamento inexistente nas costas). Mitigação herdada do dossiê: 2+ saídas, escolha humana/registrada, e a vista gerada é **referência**, não cânone (marcar proveniência no manifesto do job).
- **Prova:** Orc com turnaround gerado → projeção cobre ≥ 99% da superfície; comparação de cobertura e de nota do Mestre contra T1 puro.
- **Bateria do Crítico:** (1) proveniência: toda vista não-canônica usada no bake está marcada no relatório do job (vista gerada sem marca = reprovado); (2) consistência: as vistas geradas passam no mesmo teste de "personagens diferentes/vistas repetidas" que a entrada já tem; (3) cobertura medida antes/depois no mesmo job; (4) adversarial: pedir ao Flow uma vista de costas do Orc e conferir se inventou equipamento — se inventou, a vista é rejeitada e o fato registrado (a bateria mede a taxa de rejeição, não finge que é zero).

### T5 — UV de qualidade para pintura (pré-requisito silencioso)
- **O que é:** trocar/garantir unwrap adequado à pintura (xatlas ou Smart UV com parâmetros de pintura: margem generosa, ilhas por região semântica quando possível, distorção medida) como passo explícito do refino quando `cor` está ligada, com métricas no relatório (distorção média/máxima, ocupação, nº de ilhas).
- **Ganho esperado:** sem UV boa, T1 e T3 pintam em cima de distorção — é o item que mais protege os outros dois. Também habilita o bake de normal da retopologia (F1).
- **Custo:** dev baixo-médio; VRAM 0; disco 0 (xatlas é biblioteca leve).
- **Risco:** baixo. Trocar a UV muda o GLB final (compatibilidade com o que o Godot espera é trivial — GLB carrega a UV que tiver).
- **Prova:** métricas de UV no relatório + os testes de T1 passam com a nova UV sem regressão de tempo.
- **Bateria do Crítico:** (1) distorção de área média ≤ régua (definir no 1º run; sugerir ≤ 15%); (2) nenhuma ilha com escala degenerada (área ~0); (3) margem mínima entre ilhas ≥ 8 px em 2048² (anti-vazamento); (4) regressão completa da suíte + Prova C de forma (a UV nova não pode mudar geometria: SHA da geometria idêntico).

### T6 — Delight e PBR simples (profundidade, no sentido do Mestre)
- **O que é:** depois da cor: remover sombra embutida das vistas antes do bake (delight simples: normalização por luminância/estimativa de iluminação) e gerar mapas derivados baratos — roughness a partir de luminância/contraste local e **normal a partir da malha de alta** (depende de F1) — para o GLB reagir à luz do Godot em vez de parecer "pintado chapado".
- **Ganho esperado:** o salto de "colorido" para "material de verdade" no motor do jogo; é a "profundidade" que QUAL-02 cita ao lado de "cor".
- **Custo:** dev médio; VRAM 0–baixa; disco 0.
- **Risco:** médio — delight agressivo lava a cor (perde fidelidade). Fazer **depois** de T1 aprovado, com o comparador visual como juiz.
- **Prova:** renders do mesmo GLB sob 2 iluminações diferentes no Godot/Blender: a forma lê-se pela luz, não pela sombra pintada; ΔE da albedo sob luz flat não piora vs T1.
- **Bateria do Crítico:** (1) teste de "sombra fantasma": render com luz vindo do lado oposto ao da arte original — sombra pintada na direção errada = defeito contado; (2) mapas presentes e ligados no material (validador); (3) A/B cego com o Mestre entre T1 e T1+T6 (folha de contato sem rótulo).

### F1 — Retopologia QuadriFlow (8–20 mil quads) + bake de normal
- **O que é:** etapa opcional `retopo` entre forma e cor: QuadriFlow do Blender sobre a malha densa → malha de quads limpa; bake de normal da malha original para a retopo. (Relatório central, item 2.)
- **Ganho esperado:** habilita **animação** (deformação limpa exige topologia decente — a ressalva do IBX-178), reduz o peso do asset final e melhora a UV/pintura. É a ponte entre "forma" e "asset de jogo".
- **Custo:** dev médio; VRAM 0 (CPU); disco 0.
- **Risco:** médio — QuadriFlow pode falhar em malhas muito sujas/fundidas (machado colado no corpo é o caso adverso conhecido); preservar sempre a malha original como fallback.
- **Prova:** malha retopo fechada, contagem na faixa, IoU de silhueta vs malha densa ≥ 0,98, normal bake sem artefatos óbvios em 8 ângulos.
- **Bateria do Crítico:** (1) topologia: % de quads, zero n-gons degenerados, malha fechada (a checagem que o refino já faz); (2) fidelidade geométrica: Hausdorff aproximado/IoU vs original nas 4 vistas; (3) adversarial: Orc armado (equipamento fundido) e Besta (forma orgânica estranha) — falha deve ser **detectada e registrada**, com fallback automático para a malha decimada; (4) tempo por job na régua (CPU — definir no 1º run).

### F2 — TripoSG como motor MIT + DetailGen3D na cadeia "rápido + detalhe"
- **O que é:** executar o teste desenhado pelo I0002 no Msg1: TripoSG em venv próprio (diso opcional, flash decoder off, `model_cpu_offload_seq` definido à mão, rembg no lugar do RMBG), comparado por IoU com mini/mv-turbo; depois, DetailGen3D sobre saídas do TripoSR/mini. Pesos **já estão no PC** (pasta de estudo) — custo de download ≈ 0.
- **Ganho esperado:** um motor de forma com **licença MIT limpa** (o Hunyuan tem licença territorial — importa para o app "do Mestre") e possivelmente forma mais nítida de 1 vista; DetailGen3D pode recuperar detalhe das gerações rápidas.
- **Custo:** dev médio; VRAM: hipótese do auditor ~4–4,8 GB residentes (cabe em 8 GB); disco ≈ 0 (já baixado; mover/referenciar da pasta de estudo com manifesto).
- **Risco:** médio — repo parado desde abr/2025, issues de Windows abertas; dependências velhas (numpy 1.22) exigem venv isolado de verdade.
- **Prova:** o critério do próprio Msg1: GLB válido sem NaN, VRAM ≤ régua, tempo ≤ 15 min, **IoU ≥ Hunyuan mini no Orc**.
- **Bateria do Crítico:** (1) executar o protocolo do Msg1 à risca e publicar a tabela comparativa (IoU/tempo/VRAM/tris) dos 3 motores no mesmo Orc e mesma semente; (2) malha fechada e sem NaN (checagem automática); (3) licença: o registro do motor no app declara MIT e a cadeia não inclui RMBG (grep nas dependências do venv); (4) DetailGen3D: ganho medido = IoU/detalhe antes-depois na mesma malha; sem ganho medido, não entra na cadeia.

### F3 — Portão de qualidade ativo: IoU com retry de sementes + métrica de cor
- **O que é:** ligar o diferencial do PLANO §5.0: após a forma, calcular o IoU por vista; abaixo da régua, **regerar com outra semente** (até N tentativas) e ficar com a melhor; após a cor, idem com a métrica de cor (T1). Tudo registrado no relatório do job.
- **Ganho esperado:** transforma "sorte da semente" em processo; é o que separa um brinquedo de uma oficina.
- **Custo:** dev baixo-médio (o IoU já existe no refino); VRAM = custo das regerações; disco 0.
- **Risco:** baixo — risco de fila mais lenta; mitigar com teto de tentativas por nível de qualidade (QUAL-01).
- **Prova:** num conjunto de jobs com sementes sabidamente ruins, o portão melhora o IoU final médio de forma mensurável vs sem portão.
- **Bateria do Crítico:** (1) A/B em 9 jobs (3 personagens × 3 sementes): IoU final com portão ≥ sem portão em todos, com ganho médio reportado; (2) o relatório registra **todas** as tentativas (tentativa escondida = reprovado — transparência é requisito do projeto); (3) teto de tentativas respeitado sob fila cheia (teste com 10 jobs).

### F4 — Fechar a medição dos níveis de qualidade (QUAL-01) e virar presets documentados
- **O que é:** completar a bateria dos 5 níveis (Bronze→Lendário) já iniciada (bateriaq), agora incluindo a etapa COR quando ela existir, e publicar a tabela oficial tempo/VRAM/disco/qualidade por nível no USO_PARA_IAS e na web.
- **Ganho esperado:** o Mestre escolhe qualidade sabendo o preço — decisão informada em vez de tentativa e erro.
- **Custo:** dev baixo (medição + documentação); VRAM/disco = os próprios jobs de medição.
- **Risco:** baixo.
- **Prova:** tabela completa dos 5 níveis × 3 personagens com tempo, VRAM de pico, tamanho do GLB e nota visual.
- **Bateria do Crítico:** (1) reproduzir 3 células da tabela ao acaso — desvio > 15% em tempo/VRAM = tabela reprovada; (2) cada nível produz GLB válido e distinto do vizinho (nada de nível "fake" que ignora o perfil — o defeito que a bateriaq foi desenhada para caçar); (3) monotonicidade: qualidade visual (IoU/SSIM) não pode cair quando o nível sobe.

### P1 — Validador de asset headless (ideia do Msg9) como ferramenta permanente
- **O que é:** `validar_asset` (CLI + MCP): importa o GLB (Blender e/ou Godot headless), conta triângulos/materiais/ossos/animações, **verifica textura ligada ao albedo** e atributo de cor, checa pivô/escala/orientação, e gera 8 capturas padronizadas + relatório JSON.
- **Ganho esperado:** toda etapa nova (cor, retopo, rig) ganha um juiz automático; mata a classe de defeito "texture.png solto" e "GLB bonito no Blender, quebrado no Godot".
- **Custo:** dev médio; VRAM 0; disco 0.
- **Risco:** baixo.
- **Prova:** o validador reprova de propósito um GLB sem textura, um com pivô errado e um com escala errada (fixtures defeituosos), e aprova os GLBs bons conhecidos.
- **Bateria do Crítico:** (1) fixtures adversariais: 6 GLBs defeituosos plantados (sem albedo, pivô no centro, escala 100×, normais invertidas, UV ausente, material duplicado) — o validador tem de pegar **todos**; (2) falsos positivos: 0 nos GLBs aprovados da Prova C; (3) as 8 capturas são geradas em ≤ tempo-régua e batem com as vistas esperadas (IoU contra máscaras).

### P2 — UX de oficina: galeria com nota do Mestre, presets e reprocessar etapa
- **O que é:** relatório central item 9: galeria de resultados na web com **nota do Mestre** por job (o aceite visual vira dado), presets nomeados (= níveis QUAL-01) e botão de **reprocessar só uma etapa** (ex.: refazer só a cor de um job antigo com T1 quando ela existir).
- **Ganho esperado:** fecha o ciclo humano da qualidade — e "reprocessar etapa" é o que torna T1/T3 úteis retroativamente para todo o acervo já gerado.
- **Custo:** dev médio; VRAM 0; disco 0.
- **Risco:** baixo (cuidado permanente: nada de lote que gere cartão de aprovação em massa — lição do projeto).
- **Prova:** job antigo reprocessado só na cor mantém SHA da geometria e ganha textura; nota do Mestre persistida e visível no relatório.
- **Bateria do Crítico:** (1) reprocessar não toca nas outras etapas (hashes por etapa antes/depois); (2) nota persiste após reinício do worker/web; (3) paridade web×MCP continua (a Prova B refeita após a mudança).

### P3 — Derivados com manifesto: sprites, tokens e retratos
- **O que é:** do GLB final (com cor), renderizar derivados 2D padronizados (retrato, token de mesa, sprite estático 8 direções) com manifesto JSON (origem, etapa, hashes). É também o ensaio geral da renderização de sprites da seção 4.
- **Ganho esperado:** o 3D volta a alimentar o jogo 2.5D e a mesa — valor visível imediato para o Mestre, sem depender da animação.
- **Custo:** dev baixo-médio (a v1 já tinha `render_previa.py`); VRAM 0; disco baixo.
- **Risco:** baixo.
- **Prova:** derivados dos 3 personagens em folha de contato aprovada; manifesto confere com os hashes reais.
- **Bateria do Crítico:** (1) regenerar um derivado e comparar hash com o manifesto; (2) consistência de enquadramento (bbox do personagem ocupa a faixa esperada do quadro em todas as direções); (3) fundo alfa limpo (0 pixels semi-transparentes espúrios fora da silhueta).

---

## 3. Recomendação de desenho da Etapa COR

**Desenho:** uma etapa `cor` única, opcional, pós-refino (e pós-retopo, quando F1 existir), com **três modos** que se encaixam nos níveis de qualidade do Mestre (QUAL-01):

| Modo | Níveis sugeridos | Mecanismo | Quando usar |
| --- | --- | --- | --- |
| `vertice` (T2) | Bronze | Cor amostrada nos vértices | Rascunho instantâneo; nunca "final" |
| `projecao` (T1, +T4 quando faltar vista) | Prata / Ouro (**padrão**) | Bake das vistas canônicas no Blender, com peso por facing + teste de profundidade + dilatação | O caminho oficial: é a arte do RPG no modelo |
| `pintura-ia` (T3) | Ouro Negro / Lendário (opcional) | Hunyuan Paint via 2GP com offload | Sob demanda, para zonas cegas ou acabamento — sempre comparado |

**Tentar primeiro: a projeção (T1). Por quê, em ordem de peso:**
1. **Fidelidade ao cânone é o critério do Mestre** — a projeção usa os pixels da arte oficial do RPG; o Paint *inventa* uma textura parecida. Para um acervo autoral, isso decide.
2. **Determinismo** — mesmo job, mesma textura (o projeto já provou e cobra determinismo na forma; a cor deve herdar a mesma régua).
3. **Custo zero de GPU e de disco** — roda no Blender já instalado, não disputa a fila de forma, não baixa GB de pesos.
4. **É o mecanismo que sustenta os outros caminhos:** o caminho B do relatório central (Flow repinta → projeta) e até o Paint (que por dentro também faz render multivista + bake) dependem da mesma infraestrutura de câmeras/UV/bake (T5). Construir T1 primeiro **não é retrabalho** para nenhum plano B.
5. **As fontes convergem:** PLANO §6 ("testar primeiro no Orc"), Msg1 ("a projeção é o caminho viável"), Msg9 (diagnóstico + requisitos anti-ingenuidade), relatório central (Fase 2 começa pela projeção, comparando com o Flow).

**Plano B (se a projeção não passar no aceite visual do Orc — costuras graves ou zonas cegas dominantes):**
- **B1:** T4 (Flow gera as vistas que faltam/turnaround consistente → projeção de novo). Mantém o mecanismo, troca a matéria-prima onde ela falta.
- **B2:** T3 (Paint 2GP) como preenchedor de zonas cegas **combinado** à projeção (projeção onde há vista; Paint só onde não há), se o spike do Paint provar que cabe.
- **B3 (último recurso):** motor de nuvem opcional (alternativa D do PLANO / HF Space), sempre marcado como externo e nunca dependência única — coerente com DONO-01/02 (o app funciona sem referências externas).

**Critério de aceite da Etapa COR (resumo):** a bateria do T1 aprovada pelo Crítico + folha de contato do conjunto dourado + **nota do Mestre** — os três, não dois de três.

---

## 4. Animação e movimento — função FUTURA e opcional (estudo de viabilidade)

**Status:** estudo apenas, por ordem do Mestre (01/11, 00:44). Nada a implementar agora. A v1 **nunca** teve rig/animação (morreram no limite de uso); o que a v1 fazia era renderizar **prévias** (e o PLANO fundador previa, na Fase 4, rig simples + renders de sprite em 8 direções).

### 4.1 Desenho proposto (para quando o app estiver completo)
Uma etapa `animacao`, **opcional por job** (o padrão é desligada), depois de cor/retopo, com duas saídas possíveis:
- **GLB animado** (esqueleto + ações embutidas) para o Godot;
- **Folhas de sprite 2D** renderizadas do modelo animado (8 direções × ações), com manifesto — o formato que o jogo 2.5D consome, e o mesmo pipeline de render dos derivados (P3).
Ações-alvo nomeadas pelo Mestre: **andar, correr, atacar em várias direções, ataques diferentes, magias** (+ idle como base). "Várias direções" se resolve de dois jeitos conforme a saída: no GLB, a direção é do motor do jogo (IK/rotação); nos sprites, renderiza-se a mesma ação nas 8 direções.

### 4.2 Rotas de rig (dar esqueleto à malha)
| Rota | Como | Custo/VRAM | Risco | Estado |
| --- | --- | --- | --- | --- |
| **Templates no Blender** — MPFB `game_engine` (humanoide), Rigify (quadrúpede) | Encaixe de esqueleto-modelo + pesos automáticos do Blender; determinístico, sem IA | CPU; ~0,3 GB de assets CC0 (MPFB+MakeHuman) | Baixo-médio: exige malha em pose conhecida e proporções razoáveis | **Rota principal** (relatório central item 3); MPFB já estava "proposto para o PC Gusta" desde o dossiê (E3) |
| **Mesh2Motion** (bestas exóticas) | Ferramenta aberta voltada a criaturas não-padrão | Baixo (a medir) | Médio: projeto menor/menos provado | Já está na **prioridade 1 da Biblioteca** de downloads |
| **UniRig (IA)** | Gera esqueleto + skinning de qualquer malha (VAST/Tsinghua, MIT) | **≥8 GB de VRAM** (no nosso teto), Python 3.11, dependências tipo spconv/flash-attn (Linux) | **Alto no Windows nativo**; o analista do Msg1 já o classificava "só nuvem/GPU futura". WSL2 é a hipótese local a testar | Referência/teste futuro; wrapper ComfyUI-UniRig empacota Blender e também o MIA (Make It Animatable, humanoide) |
| **AniGen (IA)** | Imagem → malha já rigada/animável | 18 GB+ | Fora local | Só nuvem alugada, se um dia |

### 4.3 Rotas de movimento (dar ações ao esqueleto)
| Rota | Como | Custo | Risco/observação |
| --- | --- | --- | --- |
| **Biblioteca de clipes CC0 + retarget** — UAL1/2 (itch.io, CC0) e afins, retarget no Blender (extensão Retarget oficial do Blender 5.x, Rokoko, ou o "Retarget KBS" citado no relatório central) | Clipes prontos (andar/correr/ataques) remapeados para o esqueleto do personagem | ~0; CPU | **Rota principal.** Pegadinhas clássicas verificadas na web: nome de osso ≠ posição (ex.: `LeftLeg` é coxa num esqueleto e canela noutro), BVH em centímetros × glTF em metros, T-pose × A-pose. Resolve-se com preset de mapeamento **por tipo de esqueleto**, feito uma vez |
| **Mixamo** (serviço Adobe) | Auto-rig + biblioteca enorme de animações | Grátis com conta | **ANIM-01 pendente de decisão do Mestre** (relatório central: "opcional"). É serviço externo: o app deve funcionar sem ele (DONO-01) — tratar como fonte opcional de clipes, nunca como etapa obrigatória |
| **Texto→movimento local (IA)** — **Kimodo** (NVIDIA) | Prompt de texto → movimento de esqueleto (SOMA, 77 juntas, ≤10 s/clipe), exporta BVH; addons de Blender fazem o retarget | **~17 GB, ou <3 GB com o encoder de texto na CPU** → **cabe nos nossos 8 GB** na configuração econômica; licença NVIDIA Open Model (uso comercial permitido) | **Promissor para o que biblioteca não tem: magias e ataques autorais.** Só humanoide. Sucessor **ARDY** (tempo real, 6 GB) no radar. HY-Motion 1.0 (Tencent) pede 24 GB — fora |
| **Procedural no Godot** | IK nativo (TwoBoneIK3D, SpringBone — verificados no 4.7 pelo Msg9), marcha procedural, física de acessórios | 0 (runtime do jogo) | Complemento, não substituto: dá vida (balanço, olhar, pisada) sem clipe novo |

### 4.4 Sprites 2D a partir do 3D animado
A v1 já renderizava prévias por script (`render_previa.py`, recuperado); a Biblioteca já separou o **SpriteSheetMaker 5.3.1**. O desenho: render headless no Blender (EEVEE, luz padronizada da Oficina) da ação × 8 direções × fps fixo → folha de sprites + JSON de manifesto (quadros, pivô, escala) no formato que o Tabletop/Godot consome. Custo: CPU/GPU leve, disco baixo. **Pré-condição de qualidade:** o sprite herda todos os defeitos do rig — por isso sprites animados são a **última** milha, depois do rig aprovado estático.

### 4.5 Custos e riscos consolidados da frente de animação
- **Maior risco do projeto inteiro:** qualidade de deformação. Malha gerada por IA tem topologia irregular; sem retopo (F1) e sem pose-base decente, qualquer rig — template ou IA — deforma mal (ombros que rasgam, joelhos que colapsam). É por isso que animação é **etapa final**: ela cobra, juntas, as dívidas de forma, retopo e cor.
- **Custo de desenvolvimento:** alto (é uma segunda oficina dentro da oficina). Custo de máquina: baixo nas rotas principais (templates + biblioteca CC0 = CPU), médio se UniRig/Kimodo entrarem.
- **Risco de escopo:** "atacar em várias direções, ataques diferentes, magias" é um **catálogo**, não uma ação só. Desenhar como biblioteca de ações nomeadas e versionadas (`andar`, `correr`, `ataque_1`…, `magia_1`…), cada uma aprovada individualmente — nunca "animar tudo" de uma vez.

### 4.6 O que preparar DESDE JÁ (barato, junto com a Fase 2)
1. **Manter e blindar as convenções atuais** — pivô nos pés, frente +Z, Y up, teto de triângulos: são exatamente o que rig e retarget esperam. Qualquer mudança futura nessas convenções quebra a animação antes de ela nascer.
2. **Preferir referências em T-pose/A-pose** ao gerar novas artes (o BRIEF do corpo-base já faz isso) e **executar o P-0**: corpo-base sem equipamento fundido é a diferença entre rig fácil e rig impossível.
3. **Guardar a malha de alta resolução** (pré-decimação) de cada job aprovado — é a fonte do bake de normal da retopo (F1) e a referência de deformação.
4. **Registrar no manifesto do job o "tipo de esqueleto"** (humanoide / quadrúpede / exótico / nenhum) — um campo de metadado hoje, o roteador da etapa de rig amanhã.
5. **Não fundir acessórios ao corpo quando evitável**: quando o Mestre gerar referências novas, preferir personagem e equipamento em imagens separadas (a hipótese IBX-178 inteira aponta para isso; PartCrafter fica como estudo para separar o que já nasceu fundido).
6. **Baixar na hora certa** (não agora): MPFB + assets CC0, Mesh2Motion, UAL1/2 — a curadoria já está feita na Biblioteca (1.8); baixar sem uso só ocupa o disco que a Fase 1 mediu com régua.

### 4.7 Bateria futura (desenho, para quando a etapa existir)
Conjunto dourado animado: Orc humanoide (idle/andar/correr/ataque nas 4 direções cardeais), Capríleo quadrúpede (idle/andar), Besta exótica (idle/ataque). Réguas: (1) GLB importa no **Godot headless** com esqueleto válido e ações nomeadas conforme o catálogo; (2) deformação sem explosão — caixa envolvente por quadro dentro de tolerância vs quadro de referência, nenhum vértice disparado (NaN/distância absurda); (3) pés: deslize grosseiro medido no andar (root motion coerente); (4) sprites: folha completa (8 direções × quadros), pivô estável entre quadros (o personagem não "flutua"); (5) **nota do Mestre** por ação — ação reprovada sai do catálogo, não "passa mais ou menos"; (6) adversarial: aplicar o andar do humanoide no quadrúpede deve ser **recusado** pelo roteador de tipo de esqueleto.

---

## 5. Resumo executivo para decisão

**Os 5 itens de maior prioridade:**
1. **T1 — Etapa COR por projeção das vistas canônicas** (bake no Blender): o maior ganho do projeto; é a arte do RPG no modelo, determinística e sem GPU.
2. **T2 — Cor de vértice imediata** (não descartar a cor do TripoSR): fim do "tudo branco" já, como nível Bronze e rede de segurança.
3. **T5 — UV de qualidade para pintura**: o pré-requisito silencioso que protege T1 e T3.
4. **P-0 — Corpo-base do Orc em T-pose + vistas canônicas completas**: preparação barata que melhora forma, cor e o rig futuro de uma vez.
5. **T3 — Spike do Hunyuan Paint (2GP, perfil de offload)**: a pesquisa web reabriu a alternativa C (orçada em ~6 GB com offload); testar com régua definida antes, como modo opcional — nunca como padrão.

**Recomendação de textura em uma frase:** construir a Etapa COR com a **projeção das vistas canônicas como caminho padrão** (Plano B: Flow gera as vistas que faltam e projeta de novo; Plano C: Paint por IA como preenchimento opcional), porque é a única alternativa que entrega a **arte do próprio RPG**, com determinismo e custo zero de GPU — e a infraestrutura dela (câmeras, UV, bake) é a mesma que qualquer plano B reutiliza.

**Animação (futuro):** viável como etapa opcional final — rig por templates (MPFB/Rigify/Mesh2Motion) + biblioteca de clipes CC0 com retarget como rota principal, Kimodo local (<3 GB com encoder na CPU) como rota autoral de magias/ataques humanoides, sprites renderizados do 3D animado como na v1 — **desde que** se prepare o terreno desde já: convenções de malha blindadas, corpo-base em T-pose (P-0), retopo (F1) e metadado de tipo de esqueleto por job.

---

## 6. Fontes

**Locais (máquina do Mestre / projeto):**
- `~/workspace/user/files/PLANO_OFICINA_3D_PARA_CLAUDE_CODE.md` (§§2.2, 3, 5.0, 6, 8)
- `~/workspace/user/files/BRIEF_ORC_CORPO_BASE_TPOSE.md`
- `~/workspace/user/files/2026-11-01_RPG_continuidade-para-Muse_v002.md` (+ índice CSV do acervo)
- PC `C:\Users\txcga\RPG_Local\Oficina3D\app\docs\`: ARQUITETURA.md, USO_PARA_IAS.md, REVISAO_E_ROTEIRO.md, DECISOES.md, ERROS.md, REGISTRO.md (partes do Claude, 31/10), `v1_recuperado\` (inventário de 12 arquivos)
- `~/workspace/oficina-audit/`: AUDITORIA-OFICINA3D.md, CRITICO-fase1-auditoria-1.md, CRITICO-fase1-auditoria-2.md, CRITICO-fase1-auditoria-2-adendo.md

**Notion (somente leitura, Laboratório do Claude / INBOX-COMESTRE-01):**
- DOSSIÊ CM-000008 — Análise das cartas da INBOX (28/10/2026): `408c2b32-4ede-817c-8ee0-d9deb07a0b95`
- Mensagem 1 — TripoSG, TripoSF e Tripo AI (IBX-179): `408c2b32-4ede-816a-8fe6-ce55e8ff32fa`
- Mensagem 9 — Parecer arquitetural: compatibilidade, Oficina 3D, Godot, HTML (IBX-187): `408c2b32-4ede-8118-90be-fbb7b6df332f`
- Oficina 3D v2 — Relatório central e plano de ação (CUNHADO-PC): `40ac2b32-4ede-8176-8ed5-f66aac1d40cf`
- Biblioteca de downloads e estudos — PC Gusta (Oficina 3D): `409c2b32-4ede-81d8-ab1f-cf48cb23a57a`
- IBX-178 — Sugestão consultiva: Orc-base IA em T-pose para Blender: `406c2b32-4ede-8195-90c8-dd3b9afdb50d`

**Web (pesquisa de 01/11/2026):**
- Hunyuan3D-2GP — guia rápido (VRAM por etapa; textura 24,5 GB nominal): https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/2.2-quick-start-guide
- Hunyuan3D-2GP — conceitos (arquitetura em 2 estágios; bring-your-own-mesh; perfis): https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/3-core-concepts
- Hunyuan3D-2GP — otimização de memória/perfis (textura orçada em 6 GB nos perfis 4/5): https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/3.2-memory-optimization-(gpu-poor)
- Hunyuan3D-2GP — getting started (extensões C++/CUDA do texgen): https://deepwiki.com/deepbeepmeep/Hunyuan3D-2GP/2-getting-started
- Bake headless em lote no Blender (AiMDoom, estágio 5): https://deepwiki.com/shiyao-li/AiMDoom/3.6-stage-5:-texture-baking-(warmp_texture_images.py)
- Bake headless → glTF (guia prático): https://heygalatea.com/guides/how-to-export-blender-to-three-js/
- Técnica de projeção multi-vistas sem costuras (peso por facing, teste de profundidade, inpainting): https://framanen.gumroad.com/l/FramanenAITextureStudio
- Paint3D (textura 2K sem iluminação, imagem/texto): https://paperium.net/article/en/3132/paint3d-paint-anything-3d-with-lighting-less-texture-diffusion-models
- UniRig — requisitos (≥8 GB VRAM, Python 3.11): https://deepwiki.com/mahmutdemr/UniRig/2-getting-started
- UniRig/ComfyUI (empacotamento com Blender + MIA): https://www.prompts.brightcoding.dev/blog/comfyui-unirig-the-revolutionary-tool-every-3d-animator-needs
- Texto→movimento hoje (Kimodo <3 GB c/ encoder na CPU; HY-Motion 24 GB; retarget e suas pegadinhas): https://gamesbyai.win/guides/ai-3d-animation-for-games/
- Kimodo dentro do Blender (addon, retarget SOMA): https://github.com/atticus-lv/kimodo_motion
- NVIDIA ARDY (tempo real, 6 GB, sucessor do Kimodo): https://gachoki.com/nvidia-ardy-just-made-real-time-ai-animation-possible-on-a-6gb-graphics-card/

*Fim do estudo. Próximo passo sugerido (fora deste escopo): o Mestre aprova a ordem do backlog; a execução começa por P-0/T2/T5/T1, cada item com seu Crítico e sua bateria, registrados no REGISTRO do projeto.*

---

# ADENDO (ordem do Mestre, 01/11/2026, 00:53)

## 7. Crítico Visual de modelos — protocolo de análise visual contra as referências

**Por que existe:** as métricas atuais (IoU de silhueta, tempo, VRAM, triângulos) **não veem** o defeito que mais importa ao Mestre: o modelo "quase perfeito" com um acessório errado. Quem detectou o caso inaugural foi o olho humano do Mestre; este protocolo transforma esse olho em **processo repetível**, executado por um agente Crítico Visual independente (visão), com registro permanente — o mesmo padrão das baterias numéricas, aplicado ao que é visual.

### 7.1 Caso inaugural (real, registrado)
- **Job:** Orc em qualidade **Lendário** (hunyuan-mv completo, alvo 500 mil tris; GLB final 497.500 tris).
- **Defeito:** o **machado ganhou lâminas múltiplas/fundidas** que **não existem** na arte de referência (a referência tem um machado de lâmina única). O restante do modelo estava quase perfeito — silhueta, pose, pele de lobo e mão segurando a arma reconhecíveis.
- **Quem achou:** o Mestre, olhando as prévias. Conferido nas prévias: **é verdade**.
- **Classificação (pela taxonomia abaixo):** código **EXT+FUS** (parte extra + fusão), gravidade **S2 (maior)** — justificativa: visível em vista normal, num acessório-assinatura do personagem; não é S1 porque não quebra a identidade geral nem a silhueta do corpo. **Escalação:** se o modelo fosse para rig com a arma na mão, ou se a lâmina extra alterasse a silhueta de leitura a distância de jogo, sobe para S1.
- **Lição estrutural:** IoU de silhueta **passou** — a lâmina extra vive *dentro* de uma silhueta parecida. Métrica numérica sozinha não aprova modelo; **nenhum nível de qualidade (nem o Lendário) está aprovado sem o Crítico Visual**.

### 7.2 Entradas do protocolo (o que o Crítico Visual recebe)
1. **Referências originais** do personagem (as vistas canônicas usadas no job + qualquer detalhe/turnaround registrado).
2. **Renders padronizados do modelo:** as mesmas câmeras da convenção de vistas (frente/costas/esquerda/direita) + 4 diagonais, em **luz flat** (a mesma do comparador do Msg9), fundo neutro.
3. **Renders de detalhe (zooms):** rosto/cabeça, cada mão, cada acessório do inventário, pés/base — câmeras aproximadas nomeadas, para que "rosto derretido" e "dedos fundidos" sejam vistos de perto, não de longe.
4. **Render em wireframe** (ou clay com wireframe sobreposto) dos mesmos ângulos dos zooms — para distinguir **defeito de geometria** de **ilusão de textura/sombra**.
5. **Folha de comparação:** referência × render lado a lado, por vista, gerada automaticamente (a infraestrutura de câmeras calibradas do T1 serve aqui também).

### 7.3 Checklist de defeitos (percorrer item a item, por personagem)
**Inventário primeiro:** antes de olhar o modelo, o Crítico lista, **a partir da referência**, o inventário esperado: membros (nº de braços/pernas/dedos), acessórios (arma, escudo, pele, cinto, chifres…), traços do rosto (presas, olhos, cavanhaque…). Cada item do inventário recebe um veredito: `OK`, ou um código de defeito:

| Código | Defeito | Como detectar | Exemplo |
| --- | --- | --- | --- |
| **EXT** | Parte **extra** (não existe na referência) | **Contagem** contra o inventário: nº de lâminas, chifres, dedos, membros no render × referência | Machado com 2–3 lâminas (caso inaugural) |
| **MIS** | Parte **faltante** | Contagem inversa: item do inventário sem correspondente no modelo | Presa faltando; dedo a menos |
| **FUS** | Partes **fundidas** (deveriam ser separadas) | Zoom + wireframe na junção: mão×arma, arma×corpo, perna×perna; ausência de linha de separação onde a referência tem | Machado fundido à mão; dedos colados |
| **DEF** | **Deformação** (existe, mas com forma errada) | Comparação de proporções na folha lado a lado; zoom da região | Lâmina torta; rosto derretido/assimétrico sem ser SYM |
| **SIL** | Desvio de **silhueta** | IoU por vista (numérico, já existe) + leitura visual do contorno | Ombro/cauda fora do contorno esperado |
| **SYM** | **Assimetria** indevida (personagem simétrico na referência) | Espelhar o render e sobrepor (diff visual); conferir pares: olhos, presas, ombros, braços | Um olho maior que o outro |
| **FACE** | **Rosto** ilegível/derretido | Zoom do rosto em 3 ângulos; o rosto é a região de maior peso — defeito aqui pesa um grau a mais | Olhos/boca borrados na malha |
| **PRP** | **Proporção** global errada | Alturas relativas (cabeça×corpo, arma×mão) medidas na folha de comparação | Cabeça pequena demais |
| **TXT** | Defeito **só de cor/textura** (quando a Etapa COR existir) | Mesmo render com e sem textura: se some sem textura, é TXT, não geometria | Mancha, costura de cor (liga com a bateria do T1) |

### 7.4 Gravidade (classificação obrigatória de cada defeito)
- **S1 — Bloqueante:** quebra a identidade ou o uso (membro extra/faltante, acessório-assinatura irreconhecível, fusão que impede o rig, rosto destruído). **Nenhum modelo com S1 é entregue como pronto**, em nenhum nível.
- **S2 — Maior:** visível em vista normal/distância de jogo, sem quebrar a identidade (o caso do machado). Modelo pode ser mostrado como *prévia*, nunca como *aprovado*; exige correção (seção 8) ou aceite expresso do Mestre.
- **S3 — Menor:** só aparece no zoom (dedo levemente torto, costura discreta). Registra; corrige se barato; não bloqueia.
- **S4 — Cosmético:** visível só em wireframe/zoom extremo, sem efeito na leitura. Registra para estatística do motor/semente.
Regra de ouro: **a gravidade é do defeito no uso pretendido** — o mesmo defeito sobe de grau se o destino for rig/animação ou sprite de perto.

### 7.5 Registro (como fica gravado)
Para cada job avaliado, um **relatório do Crítico Visual** (arquivo do job + entrada no REGISTRO do projeto) contendo:
1. Folha de comparação anotada (defeitos marcados **sobre o render**, com o código);
2. Tabela de defeitos: `id do job | código | região | gravidade | evidência (arquivo/ângulo) | estado`;
3. **Estado** de cada defeito: `ABERTO` → `CORRIGIDO` (com link do job de retrabalho) ou `ACEITO` (**só** por decisão expressa do Mestre, registrada — ninguém mais "aceita" defeito);
4. Estatística acumulada por motor/nível de qualidade (qual motor funde mais acessórios? qual semente?) — é o insumo que transforma defeito repetido em **item de backlog** (ex.: se EXT em armas se repetir, a rota preventiva da seção 8 vira prioridade).
5. **Nota do Mestre** continua existindo ao lado: o Crítico Visual propõe a classificação; a palavra final visual é do Mestre (foi ele quem pegou o caso inaugural).

### 7.6 Bateria do próprio protocolo (o Crítico também é auditado)
1. **Plantar defeitos:** pegar 3 GLBs bons e introduzir defeitos conhecidos (duplicar uma lâmina via Blender, apagar um dedo, fundir um acessório) — o protocolo tem de detectar **todos** os plantados, com código e gravidade corretos.
2. **Falso positivo:** rodar nos GLBs aprovados da Prova C — defeito S1/S2 inventado = protocolo reprovado (calibrar antes de usar).
3. **Reprodutibilidade:** o mesmo modelo avaliado 2× (sessões distintas) deve produzir a mesma tabela de defeitos S1/S2.
4. **Caso inaugural como regressão permanente:** o job do Orc Lendário entra no conjunto dourado **como exemplo de defeito EXT+FUS S2 conhecido** — qualquer versão futura do protocolo que não o detecte está reprovada.

## 8. Retrabalho local — corrigir só a área defeituosa (função futura)

**Objetivo:** um defeito localizado (o machado do Orc) não pode custar uma remodelagem inteira (que, no Lendário, levou ~134 s de forma + refino, e pode sair *pior* noutra região — regerar é loteria nova). Quatro rotas avaliadas:

### R1 — Troca local no Blender: acessório novo entra, defeituoso sai (rota principal)
- **Desenho:** (1) isolar e **apagar** a região defeituosa na malha (seleção por proximidade/segmentação manual assistida no Blender headless ou interativo); (2) gerar o **acessório substituto separadamente** (rota R2); (3) posicionar/escalar pela caixa envolvente e pela silhueta da referência; (4) **unir** (junção por boolean + faixa de remesh local, ou objeto separado anexado — ver R4); (5) **preservar pivô, origem, escala e o restante da malha intocados** (a geometria fora da região é byte-idêntica); (6) se houver Etapa COR, re-projetar/re-pintar **só** a região trocada.
- **Custo:** dev médio-alto (o isolamento automático da região é a parte difícil; a troca em si é Blender padrão); VRAM = só a geração do acessório (vista única, motores leves); tempo por retrabalho: minutos.
- **Risco:** **médio** — costura visível na junção, escala/estilo do acessório novo divergindo do corpo, e o isolamento cortar geometria boa junto. Mitigações: margem de segurança na região (cortar no "pescoço" natural do acessório — ex.: na guarda do machado, não no meio da lâmina), folha de comparação pós-troca, e o original **nunca** é sobrescrito (retrabalho = job novo derivado, com proveniência).
- **Prova de aceite:** ver bateria 8.5 — em especial: **diff por máscara** (renders antes/depois só diferem dentro da região), pivô/bbox globais idênticos, e o Crítico Visual (seção 7) reaprova o modelo inteiro.

### R2 — Geração separada de acessórios a partir de recorte da referência
- **Desenho:** recortar o acessório da arte de referência (caixa do machado na vista em que ele aparece melhor) → fundo limpo → motor de vista única (mini-turbo/TripoSR) ou multivista se houver mais ângulos → GLB do acessório sozinho, refinado no mesmo teto de triângulos proporcional. Variante com **Flow**: gerar primeiro uma **folha ortográfica limpa do acessório** (frente/lado/costas) — precedente real verificado no dossiê: o teste E2 do Flow foi exatamente uma **espada longa em folha ortográfica**, e uma das saídas era coerente o bastante para blockout.
- **Custo:** dev baixo-médio (reusa os motores existentes); VRAM normal de 1 job pequeno; disco baixo. Cria como subproduto uma **biblioteca de acessórios** reutilizável (armas do RPG viram acervo, não acidente de geração).
- **Risco:** **médio** — o recorte pode estar parcialmente ocluído na referência (machado atrás do corpo) ou em perspectiva que o motor lê mal; a folha via Flow pode inventar o lado que não se vê (a falha já observada nas costas da espada). Mitigação: 2+ saídas e escolha registrada; aceitar "fiel na vista principal" para acessório secundário.
- **Prova de aceite:** o acessório sozinho passa pelo Crítico Visual (inventário dele: 1 lâmina, 1 cabo…) e pela folha de comparação na mesma escala da referência.

### R3 — Reparo/inpainting 3D por IA (partes e completação) — rota de estudo
- **Estado da arte (verificado nesta rodada + análises anteriores):**
  - **PartCrafter** (já está na pasta de estudo do PC, ZIP-01): gera a cena/personagem **já em partes separadas** a partir de 1 imagem — não repara um modelo existente, mas muda a geração para nascer decomponível (alimenta R4).
  - **HoloPart** (open source, Tripo/VAST): faz **segmentação amodal de partes** — a partir de uma segmentação inicial (SAMPart3D), **completa a geometria oculta** de cada parte e devolve partes editáveis/substituíveis. O auditor do Msg1 já tinha avisado: ele **não segmenta sozinho** — a cadeia é segmentar → completar → substituir. É a rota de IA mais próxima de "retrabalho local" de verdade.
  - **Inpainting 3D difusivo** (NeRF/Gaussian Splatting) e preenchimento de buracos de malha: o primeiro não devolve malha de jogo limpa; o segundo só fecha buraco, não corrige forma errada (não remove lâmina extra com juízo). **DetailGen3D** adiciona detalhe — também não remove o que sobra.
  - **Reparo local manual-assistido no Blender** (esculpir/remesh só da região, apagar faces extras + fechar + suavizar a faixa): funciona hoje, sem IA, para defeitos **simples e bem separados** (uma lâmina extra destacável). É o degrau zero da R1.
- **Custo:** dev alto (cadeia nova de segmentação, venv próprio); VRAM desconhecida do HoloPart (a medir; pesos ~3,8 GB segundo o Msg1); disco: já há PartCrafter/HoloPart como estudo no PC (pasta `oficina3d_ia`).
- **Risco:** **alto** — segmentação errada numa malha fundida (justamente o nosso caso: lâminas *fundidas* entre si) pode não separar o que precisa; é pesquisa, não produção.
- **Prova de aceite:** no caso inaugural: a cadeia segmenta o machado do Orc Lendário e devolve a parte separada/editável sem tocar no corpo (diff por máscara fora da região = zero). Sem isso, continua estudo.
- **Veredito:** **não é a rota de curto prazo**; manter como estudo vigiado (é também o destino natural do material da ZIP-01) e reavaliar quando R1 estiver de pé.

### R4 — Rota preventiva: corpo-base sem arma + arma como objeto separado (a correção estrutural)
- **Desenho:** mudar a **entrada**, não a saída: o personagem é gerado **sem** acessórios (corpo-base do IBX-178/BRIEF, item P-0) e cada acessório é gerado à parte (R2) e **anexado como objeto independente** no GLB final (nó próprio, nomeado, com seu pivô de empunhadura). Trocar/corrigir um acessório vira **substituir um nó** — segundos, sem tocar no corpo; e é o formato que rig/animação e o jogo querem (arma que se equipa, troca e larga).
- **Custo:** dev médio (convenção de anexação + ponto de empunhadura por tipo de acessório); VRAM = jobs separados menores; disco baixo.
- **Risco:** **baixo-médio** — a junção mão×arma precisa de encaixe (posição/rotação por tipo, ajustável); em sprite/3D de jogo, objeto anexado é prática padrão. O risco real é de **processo**: exige que as referências futuras venham separadas (personagem × equipamento) — decisão de produção do Mestre, não técnica.
- **Prova de aceite:** o mesmo Orc com 2 machados diferentes anexados (troca registrada como operação, corpo byte-idêntico), render aprovado pelo Crítico Visual nas vistas de empunhadura.
- **Veredito:** **é a rota que elimina a classe inteira do defeito inaugural.** R1 continua necessária para o acervo já gerado "fundido"; para tudo que nascer depois do corpo-base, R4 torna o retrabalho trivial.

### 8.5 Bateria de aceite de qualquer retrabalho (Crítico, sob medida)
1. **Localidade provada:** renders antes/depois nas 8 vistas; fora da máscara da região, diff de pixels = 0 (luz flat) e SHA da geometria fora da região idêntico. Vazou da região = reprovado.
2. **Invariantes do asset:** pivô nos pés, origem, escala, orientação e teto de triângulos **idênticos** ao job original (validador P1).
3. **Defeito alvo extinto:** o Crítico Visual (seção 7) reexecuta o checklist completo — o defeito corrigido some **e nenhum defeito novo** S1/S2 nasce (em especial FUS novo na junção e SIL alterada).
4. **Junção:** zoom da faixa de união em 3 ângulos: sem buraco, sem costura de cor (pós-COR), sem normal quebrada.
5. **Proveniência:** o job derivado registra: job pai, região, rota usada (R1/R2/R3/R4), parâmetros e arquivos — retrabalho sem registro não existe (regra do projeto).
6. **Regressão do caso inaugural:** o machado do Orc Lendário é o **teste de aceitação nº 1** da função: entrada = o GLB defeituoso real; saída aceita = mesmo Orc, machado de lâmina única fiel à referência, resto intocado, aprovado pelo Mestre.

### 8.6 Recomendação da frente de retrabalho
**Curto prazo:** R1 na versão degrau zero (remoção local assistida no Blender + acessório via R2) para salvar o acervo fundido que vale a pena — a começar pelo caso inaugural. **Estrutural:** R4 (corpo-base + acessórios separados) como **convenção de nascimento** de todo modelo novo — é a mesma decisão do P-0/IBX-178, agora com um motivo a mais: ela transforma "retrabalho" em "troca de peça". **Estudo vigiado:** R3 (HoloPart/PartCrafter), reavaliar após R1.

**Fontes deste adendo (web, 01/11/2026):** HoloPart open source — segmentação amodal e completação de partes, partes substituíveis e prontas para animação: https://www.tripo3d.ai/blog/holopart-generate-parts-for-3d-model · PartCrafter — geração estruturada em partes a partir de 1 imagem, sem segmentação prévia: https://arxiv.org/pdf/2506.05573 · Caso inaugural e números do job Lendário: relatório da prova de qualidade (provaq) e prévias conferidas com o Mestre, 01/11/2026 (registros do projeto).


## Adendo 2026-11-01 — Pesquisa de texturizacao (ChatGPT) e o spike T7

- **T7 — Spike UltraTex Modular (NOVO; entra a frente do T3 na fila de spikes da Etapa COR).** Motor de pintura via ComfyUI que aceita as referencias canonicas do projeto (frente/costas/laterais/topo/base) e exporta GLB pintado com rugosidade/metalicidade. Regua pre-registrada completa em `docs/ESTUDO_T7_PESQUISA_TEXTURA.md`: Gate 0 = inventario de disco antes de baixar; aceite exige VRAM <= 8.188 MB, tempo <= 45 min, SSIM frontal nao pior que o T1 e zero OOM — qualquer regua quebrada arquiva o T7 como plano C com evidencia. Aguarda o relatorio de verificacao factual da pesquisa.
- **T3 — Hunyuan Paint:** rebaixado para depois do T7 (divergencia de VRAM registrada no estudo T7: oficial 2.1 = 21 GB recomendados; fork 2GP = alvo ~6 GB com OOM relatado). Gate 0 do T3 permanece como desenhado.
- **Retrabalho local:** Yedp UV Painter (pintura por regiao, desenhado para 8 GB, MVP) entra como candidato observado da frente. **T1:** Eyek (addon Blender de projecao multivista) entra como leitura comparativa.


**Correcao 2026-11-01 (verificacao factual; relatorio em `docs/VERIFICACAO_PESQUISA_TEXTURA.md`):** o item "Yedp UV Painter como candidato da frente de retrabalho local", lancado no adendo acima, fica **RETIRADO** — a ferramenta nao foi localizada em nenhuma fonte primaria (sem repositorio nem pagina oficial); mencao sem lastro nao vira plano. No mesmo relatorio: UltraTex confirmada com as ressalvas de licenca do modelo-base FLUX.2 (nao comercial) e de tamanho de download nao declarado (Gate 0 mede); Eyek e Comfy BlenderTools sem licenca declarada (estudo sim, dependencia nao); Paint 2.1 oficial = 21 GB literais.
