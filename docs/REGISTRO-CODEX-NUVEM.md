# REGISTRO-CODEX-NUVEM — 02/11/2026

Missão: `MISSAO.md` recebido na raiz. Trabalho exclusivo em
`codex/auditoria-sem-pc`, base pública `5cd092d37bddf36a2d888404936d4c9f394528c4`.
`git fetch origin` concluiu; `origin/main` continua nessa base. Não se alterou
`main`, não houve force-push, acesso ao PCDANASA, uso de arte privada, job GPU
ou execução do Blender. Tudo desta rodada fica neste registro e nas evidências
textuais versionadas. Nenhuma rota paga ou pesquisa externa foi executada.

## Método, limites e desvios

- Inspeção inicial: branch já correta, HEAD na base pedida, única entrada não
  rastreada `MISSAO.md` (arquivo do usuário, preservado e fora dos commits).
  `rg --files -g AGENTS.md` não encontrou instruções adicionais na árvore;
  também não foram encontrados AGENTS.md nos diretórios ancestrais consultados.
- Fonte dos patches: objetos Git da branch **pública**
  `origin/codex/melhoria-paralela`, sem mudar para ela. Nenhum arquivo do PC foi
  consultado. Base/SHAs e diffs, em vez de memória, definem a comparação.
- **Desvio de execução:** ao inventariar essa branch pública, li também seu
  `docs/REGISTRO-CODEX.md` via `git show`. A missão manda não usar o registro
  antigo. Não foi acesso ao PC, mas foi leitura indevida diante dessa instrução.
  O arquivo não foi copiado, reconciliado nem usado como prova desta rodada.
  Resultados abaixo exigem código público, testes novos ou documentos da base.
- Autoauditoria é do executor; não constitui veredito de Crítico independente
  nem aprovação visual do Mestre. Nenhum resultado visual novo foi produzido.
- Interpretador inicial: Python 3.12.14 do runtime local; NumPy 2.3.5,
  Pillow 12.3.0; sem bpy, scipy, trimesh, FastAPI, httpx ou MCP inicialmente.
  Difere do ambiente do PC: números de tempo não são comparáveis entre máquinas.

## Frente 1 — centro na COR-08/S2: FECHADA em CPU

**Veredito: CORRIGIDO explicitamente pela COR-08/A0 (`27704b1`), não absorvido
pelo alinhamento e não persistente na base publicada.**

Prova de código: `oficina3d/cor/projecao.py:118` subtrai `centro` em
`projetar`; `:510` faz `rel = p3d - np.asarray(centro, dtype=np.float64)`
no bake, antes da mesma projeção. O diff do commit `27704b1` mostra a troca de
`qx = p3d @ direita; qy = p3d @ cima` por essa subtração.
O commit `22b9d5c` trata o salvamento Standard, sem desfazer a A0.
O teste publicado `test_amostragem_usa_centro_faixas` já cobre o erro.

Prova nova: `testes/test_cor_centro_nuvem.py` compara os **1.024 texels** de um
quadrilátero com uma fórmula independente de UV → 3D → pixel, usa imagem
retangular com gradiente que codifica coordenadas, e verifica invariância à
translação conjunta da malha e do centro nos caminhos bbox e override.
Controle negativo recompila somente a função em memória, removendo a subtração:
a cobertura continua 1.024, mas a faixa inferior amostra a metade superior;
erro máximo de canal >0,4. Nenhum código de produção foi alterado nesta frente.

O deslocamento antigo obedece a `Δy_arte = -ay * (centro·cima)/ortho * altura`.
No sintético explicitamente escolhido (altura 945, centro z=0,5, ortho=1,1,
ay=1), dá **−429,54545 px**, arredondado −429,5. Isso ilustra a fórmula;
**não** reproduz nem autentica os parâmetros ou o mapa de proveniência do
antigo job do Orc. O limite histórico y=511 e a ausência de amostras frontais
nas pernas não podem ser afirmados para a COR-08 sem seus artefatos.

Execução: `python -B testes/auditoria_nuvem.py frente1
testes.test_cor_centro_nuvem testes.test_cor` — **36 executados, 36 passaram,
0 falhas, 0 erros, 0 skips** (3 novos + 33 existentes).
Lista completa: `docs/evidencias-nuvem/frente1.txt`; painel medido:
`docs/evidencias-nuvem/frente1.json`.

| Medida desta execução CPU | Valor |
|---|---:|
| Tempo de parede | 86,757012 s |
| CPU do processo | 27,96875 s |
| Pico working set do processo desde início | 78.675.968 bytes |
| GPU | não usada |
| VRAM / consumo de energia | não medido |
| IoU/cobertura/cores do Orc real, SSIM, DeltaE, PNG×GLB | não medido |

O runner usa diretório temporário para BASE/jobs/caches e registra versões,
IDs de falhas/skips e recursos reais. A suíte completa inicial foi iniciada
separadamente; seu resultado será registrado na frente de integração.

**Para a volta do PC:** executar dois bakes da âncora COR-08 correta
(`cor08rep`, não o job antigo 1024), conferir hashes de entradas, exportar mapa
texel→face→vista→pixel e medir regiões inferiores, determinismo, textura×GLB e
render flat. Qualidade visual e fidelidade continuam pendentes; não reaplicar
um patch de centro que já entrou.
