# ESTUDO — Pesquisa de texturização do ChatGPT (2026-11-01) e o novo spike T7

Origem: pesquisa do ChatGPT entregue pelo Mestre em 2026-11-01, sobre fazer a Oficina entregar o modelo já pintado (cores, materiais, texturas), com o Blender só para correções finas. Íntegra preservada pelo Muse fora do repositório público (higiene GIT-02); este documento registra o resumo fiel, a análise e as decisões de fila. Verificação factual das afirmações em curso por agente dedicado; o que estiver por verificar está marcado PENDENTE-VERIFICAÇÃO.

## Convergência com o desenho já registrado

A montagem proposta pelo ChatGPT (referências aprovadas → geometria → pintura/materialização → validação automática em 8 vistas com costuras, cores e materiais → GLB quase pronto) é a mesma arquitetura da Etapa COR já registrada neste projeto (projeção padrão T1 + UV de qualidade T5/D-T5-1 + comparação com pintura por IA). A pesquisa não muda a arquitetura; ela adiciona candidatos concretos à etapa de pintura e um teste comparativo que já era o desenho: projeção direta das 4 vistas × texturização por IA, nos três cobaias (Orc, Capríleo, Besta), avaliados em 8 ângulos com inspeção de costuras e de detalhe.

## Candidatos e destino de cada um

- **UltraTex Modular (ComfyUI nodes) → NOVO SPIKE T7, à frente do T3.** É o candidato que melhor casa com o critério de fidelidade ao cânone deste projeto: aceita as NOSSAS referências (frente, costas, laterais, topo, base) em vez de inventar as vistas a partir de uma única imagem (o desenho do Hunyuan Paint). O desenvolvedor relata 15–18 min/modelo numa RTX 5050 Laptop de 8 GB (PENDENTE-VERIFICAÇÃO; não é benchmark da nossa RTX 4060). Produz rugosidade/metalicidade; normal/AO pedem etapa complementar. Exige ComfyUI + modelos FLUX.2/Qwen quantizados + extensões.
- **Eyek (addon Blender) → leitura comparativa do T1.** Implementa projeção multivista sobre um UV com transparência e oclusão — o mesmo problema do nosso T1; comparar antes de qualquer adoção.
- **Yedp UV Painter → frente de retrabalho local.** Pintura por região em camadas (pele, armadura, cinto, cabelo), desenhado para 8 GB, estado MVP — é a família de ferramenta dos defeitos que o retrabalho local precisa atacar (machado do Orc, rosto). Sem spike por ora; observar e, se a verificação confirmar, entrar como candidato da frente de retrabalho.
- **Comfy BlenderTools → automação potencial do bake.** UV + projeção + bake via Blender dentro do ComfyUI; interessa se/quando a Oficina ganhar uma camada ComfyUI pelo T7.
- **InstaMAT Studio, Material Maker, Poly Haven, Open Painter → acabamento e biblioteca, sem frente própria por ora.** InstaMAT = acabamento PBR fora do Blender (plano Pioneer gratuito com limite de receita — PENDENTE-VERIFICAÇÃO); Material Maker e Poly Haven = materiais/biblioteca; Open Painter = revisão final no Blender 5.2+.
- **StableGen → observação.** Pintura multivista via ComfyUI; execução em 8 GB não testada nem pelo autor da pesquisa.
- **SUPRA-Tex → observação.** Preserva a referência e gera PBR, mas a instalação oficial pede Linux/CUDA e recomenda ≥48 GB para melhor desempenho (PENDENTE-VERIFICAÇÃO).

## Divergência registrada — VRAM do Hunyuan Paint

A pesquisa afirma que o Hunyuan3D-Paint **2.1 oficial** recomenda **21 GB** de VRAM só para a pintura. O ESTUDO_T3_PAINT deste projeto mediu o **fork 2GP**, que mira ~6 GB nos perfis 4/5 do mmgp, com relato de OOM em issue — alvo, não garantia. As duas afirmações tratam de artefatos diferentes e ficam registradas lado a lado: o número oficial é 21 GB; o do fork é uma meta agressiva de offload. Consequência de fila: **o T3 (Paint) fica atrás do T7 (UltraTex)** e mantém o seu Gate 0 de compilação isolada.

## Régua pré-registrada do spike T7 (antes de qualquer download)

- **Gate 0 — disco:** inventariar o download total (ComfyUI + FLUX.2/Qwen quantizados + extensões + nós) e registrar os GB ANTES de baixar; se o total ameaçar o espaço livre do PC, parar e registrar em ERROS/REGISTRO. Nada de instalação parcial silenciosa.
- **Cobaia:** Orc Prata refinado + as 4 vistas canônicas (topo/base das referências REF-01 quando o fluxo pedir).
- **Ambiente isolado:** instalação própria, sob gpu.lock, sem tocar nos venvs dos motores atuais.
- **Métricas:** VRAM de pico; tempo total; SSIM/ΔE **por região** contra os números do T1 no mesmo modelo; folha de contato em 8 ângulos para o Mestre; Crítico Visual sobre o resultado.
- **Aceite (todas):** VRAM ≤ 8.188 MB **e** tempo ≤ 45 min **e** SSIM frontal não pior que o do T1 **e** zero OOM. Qualquer régua quebrada → o T7 volta a plano C arquivado, com evidência, e a projeção segue como caminho padrão.
- **Determinismo:** não é esperado byte-idêntico; registrar seeds e as duas execuções mesmo assim.

## Estado

Pesquisa protocolada em 2026-11-01. Verificação factual em curso. Spike T7 aguarda (1) o relatório de verificação e (2) a janela do laço de melhoria (a GPU é uma só; a fila da Etapa COR anda um item por vez: integração da cor à fila de jobs e, na sequência de spikes, T7 antes de T3).


## Resultado da verificacao factual (2026-11-01) — resolve os PENDENTE-VERIFICACAO

Relatorio completo com fontes primarias e trechos literais: `docs/VERIFICACAO_PESQUISA_TEXTURA.md`. Resumo decisorio:

- **UltraTex: CONFIRMADA integralmente.** GPL-3.0; referencias opcionais back/left/right/top/bottom; 10 vistas (6 canonicas + 4 a 45 graus); atlas ate 8192x8192; passada metallic/roughness; o numero 15-18 min em RTX 5050 Laptop de 8 GB e LITERAL no README. Pilha: ComfyUI + ComfyUI-GGUF + FLUX.2 Klein 9B Q4_0 GGUF + Qwen3-8B Q6_K GGUF. **Duas ressalvas que entram na regua do spike:** (1) o README NAO declara o tamanho dos downloads — o Gate 0 de disco segue obrigatorio e e ele quem mede; (2) as nossas fotos "guiam a cor" — o FLUX GERA a vista a partir delas, nao e projecao direta pixel a pixel (a projecao T1 continua sendo o unico caminho de fidelidade literal; o T7 e geracao condicionada por referencia, e e assim que o Critico deve julga-lo). **Licenca do modelo-base:** FLUX.2 e nao comercial (termos BFL; saidas comerciais restritas) — o spike de teste e legitimo; qualquer ADOCAO do UltraTex como etapa padrao exige decisao registrada sobre esse termo.
- **Hunyuan Paint 2.1: numero oficial confirmado, literal:** "21GB for texture generation" (README oficial, Models Zoo; forma = 10 GB; forma+textura = 29 GB). A divergencia registrada esta resolvida: oficial 21 GB x fork 2GP alvo ~6 GB com OOM relatado.
- **SUPRA-Tex: CONFIRMADA** (release de inferencia em 2026-10-19; Linux + CUDA 12.4; "pelo menos 48 GB; ate 24 GiB ligam offload para CPU"). Codigo MIT, mas o material adapter e Qwen Research License (nao comercial). Segue em observacao.
- **StableGen: CONFIRMADA** (GPL-3.0; addon de Blender sobre servidor ComfyUI; PBR via Marigold). Nuance de VRAM declarada: ~8 GB so no modo SDXL; Qwen Image pede 16 GB+. Segue em observacao.
- **Eyek: funcoes CONFIRMADAS; LICENCA NAO LOCALIZADA** (sem LICENSE no repo). Nao vira dependencia sem registro de licenca; leitura comparativa do T1 continua permitida como estudo.
- **Comfy BlenderTools: funcoes CONFIRMADAS; LICENCA NAO LOCALIZADA;** repo pequeno (7 stars, sem releases). Idem: estudo sim, dependencia nao.
- **InstaMAT Studio: CONFIRMADA** — Pioneer gratuita com uso comercial MEDIANTE ATRIBUICAO e elegibilidade de receita/financiamento anual < US$ 100 mil (os US$ 250 mil da mesma pagina sao o teto das faixas Indie pagas).
- **Open Painter: CONFIRMADA** — Blender 5.2+, GPL-3.0-or-later, acabamento PBR em camadas.
- **Yedp UV Painter: NAO LOCALIZADA — RETIRADA do plano.** Apos tres buscas distintas, nao existe repositorio nem pagina oficial localizavel; o unico rastro e o titulo de um post de Reddit reproduzido por sites-espelho. Sem fonte primaria, a prioridade "Alta" da pesquisa nao tem lastro: o Yedp deixa de ser candidato da frente de retrabalho local e fica registrado apenas como mencao nao verificada. A frente de retrabalho segue com as rotas ja registradas (troca local no Blender; acessorio como objeto separado).
