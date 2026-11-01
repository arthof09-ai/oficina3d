# Comparativo de pintura 3D — Oficina3D (etapa COR-05) × Blender nativo

> Estudo registrado no projeto em 2026-11-01. Artefatos completos (scripts-fonte `pintar_blender.py` e `renderizar.py` nesta mesma pasta; GLBs, texturas, renders e logs) em `BASE\_cache\tmp\comparativo-blender\` no PC e espelhados em `~/workspace/oficina-audit/comparativo-blender/` na VM do Muse.


**Pedido do Mestre (2026-11-01):** pegar um modelo 3D sem cor, mandar o Blender pintar/texturizar sozinho e comparar com o que a Oficina3D produz na sua etapa de cor.
**Sujeito:** Orc Prata da prova COR-05 (job `20261101-101528-corint-orc-s7`, motor hunyuan-mv-turbo, 49.750 tris).
**Mesma matéria-prima para os dois lados:** o GLB refinado sem cor que entrou na etapa de cor da Oficina (`cor\modelo_uv.glb`), as mesmas 4 vistas canônicas pré-processadas (`preproc\frente|costas|esquerda|direita.png`) e textura de 1024×1024 nos dois lados.

## Método da rota Blender (100% nativo, headless, sem janela visível)

Script `scripts\pintar_blender.py` (Blender 5.2.3, `blender -b`), rodado por tarefa agendada destacada no PCDANASA:

1. **UV própria do Blender** — Smart UV Project (66°, margem 0,003) sobre a malha, descartando a UV xatlas da Oficina. Ocupação medida: 30,5% da textura.
2. **Calibração automática de orientação** — silhuetas ortográficas renderizadas nas 4 direções e casadas por IoU com as máscaras das vistas: frente=−Y (IoU 0,787), costas=+Y (0,738), esquerda=+X (0,792), direita=−X (0,762). Mesma faixa de IoU que a Oficina mediu (0,72–0,79).
3. **Câmeras de projeção com ajuste fino** — 4 câmeras em perspectiva (32°) ajustadas iterativamente até a caixa projetada dos vértices casar com a caixa da máscara de cada vista (IoU de caixa 0,65–0,80).
4. **Visibilidade por raycast (BVH do Blender)** — sem isso a projeção pinta *através* do modelo. Faces visíveis por vista: 41,5–48,9%. Gravada como atributo por face e multiplicada no peso da projeção.
5. **Pintura por projeção** — material de nós do Blender: para cada vista, projeção perspectiva da imagem de referência (via objeto-câmera no nó Texture Coordinate), peso = facing^1,5 × alfa × frustum × visibilidade; mistura normalizada das 4 vistas; **sem dilatação/invenção de cor** — o que nenhuma câmera enxerga fica em neutro escuro.
6. **Bake Cycles (EMIT, GPU)** para a textura 1024² + bake de cobertura + material Principled + exportação GLB.

Renders de prévia (`scripts\renderizar.py`): Eevee, **cena idêntica para os dois GLBs** (mesma luz, mesma câmera, mesmos ângulos: frente, 3/4, costas).

> Registro honesto de escopo: o Texture Paint interativo (pincel/stencil na tela) não é executável em modo headless; a rota acima é o equivalente nativo do Blender nomeado no pedido — projeção por câmeras + bake — com o acréscimo do teste de oclusão por raycast. Um artista no Blender interativo faria o mesmo e ainda retocaria as costuras à mão.

## Medições

| Medida | Oficina3D (COR-05) | Blender nativo |
|---|---|---|
| Tempo da etapa de cor | **61,26 s** (resultado_cor.json; inclui subprocessos e as 4 prévias da etapa) | **4,4 s** de script completo (import→GLB pronto; bake de cor 0,67 s) |
| Textura | 1024², UV xatlas (8.844 ilhas) | 1024², UV Smart Project (ilhas minúsculas, ~6 texels/face em média) |
| Cobertura direta (texels UV com cor projetada de verdade) | **20,03%** (medido pela Oficina a 512px); resto preenchido por **dilatação de 256px** até 0% cego | **63,43%** (medido a 1024px no bake de cobertura); resto = neutro escuro, sem invenção |
| Erro médio de cor vs referência (frente, mesma régua, 0–255; menor = melhor) | **47,8** | **42,8** |
| IoU de silhueta do render vs referência (frente) | 0,838 | 0,843 |
| GLB colorido | 3.230.584 B | 3.592.080 B |

## O que se vê nas prévias (frente / 3/4 / costas, mesma cena)

**Oficina3D:** o defeito já conhecido e reprovado (pendência D1): mosaico/"confete" generalizado — fragmentos duros de cor por toda a superfície, manchas pretas, pedaços fora do lugar (uma placa bege flutuando sobre o braço do machado; uma faixa vermelha/branca cortando o peito no 3/4), rosto ilegível. Na textura, o mecanismo aparece nu: um mosaico tipo Voronoi — a dilatação espalhou a cor de poucas faces por áreas enormes. As cores são "da família certa" (beges de pele/pelo, vermelhos), mas sem regiões coerentes.

**Blender nativo:** pintura contínua, sem confete: as regiões de cor caem nos lugares certos nos 3 ângulos (pano vermelho embaixo, tons de pele/pelo, costas dominadas pelo marrom do manto de pele, como na referência). Porém é uma **base aguada** ("watercolor"): borrada, escura, sem detalhe fino — rosto ilegível também, vazamento de vermelho para botas e machado, e zonas cegas (topo da cabeça, solas, concavidades) em neutro escuro.

## Causa-raiz comum (nenhuma das rotas resolve)

As imagens de referência foram geradas por IA e **não casam com a malha** que o motor gerou a partir delas: IoU de silhueta 0,72–0,79 nas duas medições independentes. Com esse desregistro, detalhe fino (rosto, cabeça de lobo no ombro, caveiras do cinto) não tem onde pousar — e parte desses elementos nem existe em relevo na malha. Projeção, de qualquer implementação, tem esse teto neste sujeito.

## Veredito

**Neste teste, a rota nativa do Blender pintou melhor que a etapa de cor atual da Oficina** — por coerência visual (regiões contínuas em vez de mosaico), por fidelidade média de cor medida (42,8 × 47,8) e por velocidade (~14× mais rápida na etapa equivalente). **Mas "melhor" aqui significa "menos ruim": nenhum dos dois resultados é aproveitável como pintura final.** O Blender entrega uma base aguada que serviria de *underpainting* para retoque; a Oficina entrega o confete já reprovado pelo Mestre e pelo Crítico sênior (o que foi aprovado na COR-05 foi o **mecanismo** — fila, GLB válido, sem regressão — não a qualidade visual, que segue aberta na pendência D1).

Lição prática para a Oficina: a mistura ponderada por facing + oclusão, **sem** a dilatação agressiva de 256px, produz base muito mais limpa que o pintar-texel + dilatar atual; a dilatação é a principal suspeita pelo confete (espalha cor de face única por áreas grandes com bordas duras). As rotas gerativas em estudo (T7 UltraTex / T3 Hunyuan Paint) atacam a causa-raiz — não dependem de registro perfeito imagem×malha — e seguem sendo a aposta principal para qualidade final.

## Arquivos

- No PC: `BASE\_cache\tmp\comparativo-blender\` (scripts, GLBs, texturas, renders, logs, `saida\resultado_blender.json`).
- Na VM do Muse: `~/workspace/oficina-audit/comparativo-blender/` (renders dos dois lados, `montagem_comparativa.png`, `montagem_texturas.png`, texturas, GLB do Blender, este resumo).
- GLB da Oficina comparado: `saida\modelo.glb` do job COR-05 (sha256 do GLB no `resultado_cor.json`: 0f838538…).
