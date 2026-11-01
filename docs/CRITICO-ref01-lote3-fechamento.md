# CRÍTICO VISUAL SÊNIOR — REF-01, lote 3 (Capríleo): rodada de FECHAMENTO (re-verificação C1)

**Data:** 01/11/2026. **Papel:** Crítico Visual sênior independente — não gerei nenhuma imagem deste lote. **Escopo:** fechado, conforme a tarefa: só conferência de hashes, re-verificação C1 item a item e a verificação nova de consistência de rótulos. O mérito das vistas não foi rejulgado; o `topo` só teve sua identidade confirmada por hash. **Nenhum arquivo foi alterado por mim.**

## 1. SHA-256 medidos contra os esperados

| Arquivo (local) | SHA-256 medido | Esperado pós-troca | Resultado |
|---|---|---|---|
| `caprileo_diag_tras_esq.png` | `46cbe2b9b645163909a6eb6ac745eb8b9d0694717122fdedfc8348d10d1ef07a` | `46cbe2b9…1ef07a` | **CONFERE** |
| `caprileo_diag_tras_dir.png` | `efd00a7d77e0830f609025a12307f6f00485032bb86d91f7496fe02ee59fa180` | `efd00a7d…fa180` | **CONFERE** |
| `caprileo_topo.png` | `f09270071bdea23cd587da96ee4b52bf4bb29b3204d47ca369aa4ba3c238b634` | `f0927007…38b634` | **CONFERE — mesmo arquivo da rodada 1** |

Confirmação adicional, só leitura, no PC (`app\testes\referencias\`, via `Get-FileHash`): `esq` = `46CBE2B9…`, `dir` = `EFD00A7D…`, `topo` = `F0927007…` — **idênticos aos locais e aos esperados**. A troca foi aplicada nos dois lados com o conteúdo intacto: os hashes do conteúdo não mudaram, só trocaram de nome, exatamente como a especificação da seção 7 da rodada 1 mandava.

## 2. Re-verificação C1, item a item, com os meus olhos

**Arquivo `caprileo_diag_tras_esq.png` (deve ser a vista traseira-ESQUERDA):**
- Cabeça à **esquerda** — focinho apontando para a esquerda, confirmado.
- Chifre próximo com **segundo anel pequeno e fechado** dentro do anel maior — confirmado: o chifre em primeiro plano enrola-se num pequeno laço fechado junto à cabeça.
- Cauda à **direita** — a cauda longa varre para a parte inferior direita da imagem, com a ponta apontando para baixo-esquerda. Confirmado.
- **3/3 batem.**

**Arquivo `caprileo_diag_tras_dir.png` (deve ser a vista traseira-DIREITA):**
- Cabeça à **direita** — focinho apontando para a direita, confirmado.
- Chifre próximo em **gancho aberto em "C"** — confirmado: o chifre em primeiro plano termina num gancho aberto, sem o anel interno fechado.
- Cauda à **esquerda** — a cauda longa varre para a parte inferior esquerda da imagem. Confirmado.
- **3/3 batem.**

Os três itens batem nos dois arquivos. **C1 FECHA.** Cada arquivo agora veste o nome do lado que realmente mostra; a inversão da rodada 1 está desfeita nos pixels e nos nomes, nos dois lados (local e PC).

## 3. Verificação NOVA desta rodada (escalada APR-01): consistência de rótulos no conjunto

Procurei referências textuais aos nomes antigos (nomes de arquivo e hashes por nome) em: todos os `.md` de `~/workspace/oficina-audit/` (incluindo `docs/`, `instalacao/`, `registro_lote2/`), e, só leitura, em todos os `.md` de `app\docs\` no PC. Achados:

**a) Registro histórico que ainda descreve o mapeamento pré-troca — `~/workspace/oficina-audit/CRITICO-ref01-lote3.md` (o próprio relatório da rodada 1).**
É o único documento local que associa os nomes antigos aos hashes: cabeçalho (esq = `efd00a7d…`, dir = `46cbe2b9…`), tabela de veredito ("conteúdo = vista traseira-direita/esquerda") e a nota do executor. **Avaliação honesta:** isso é registro histórico datado da reprovação, não um índice vivo do arsenal — e a seção 7 dele próprio ordena a troca. Ele não "ressuscita" a divergência para quem lê o documento inteiro, mas um leitor que copiar só a tabela do cabeçalho sem a data levaria o mapeamento errado. **Correção necessária (pendência de registro, não de imagem):** a instalação do relatório no PC ainda não aconteceu, e nenhum documento do projeto registra ainda os hashes novos por nome nem a convenção (`diag_tras_esq/dir` = lado do animal visível = lado da câmera). Esse registro pós-troca — item 4 da especificação da rodada 1 — segue pendente e deve acompanhar o relatório quando ele for instalado, para que o mapeamento novo exista por escrito em algum lugar além dos nomes dos arquivos.

**b) Zooms de evidência com nomes agora defasados — `~/workspace/oficina-audit/zooms_lote3/`.**
Os recortes foram feitos a partir dos arquivos pré-troca, então seus nomes `esq_*`/`dir_*` hoje descrevem o conteúdo oposto. Verifiquei com os meus olhos um deles: `esq_cabeca_chifres.png` mostra cabeça à direita e chifre próximo em gancho aberto em "C" — ou seja, conteúdo de vista traseira-**direita** sob nome "esq". Os demais (`esq_crista_cauda`, `dir_cabeca_chifres`, `dir_crista_cauda`) são, por construção, do mesmo caso — recortes dos mesmos arquivos pré-troca — mas só o de cabeça/chifres `esq` foi conferido visualmente por mim nesta rodada. **Avaliação:** são evidências de trabalho, não arquivos do arsenal, e não entram no modelo; o risco é só de confusão de leitura futura. Recomendo uma nota junto à pasta (ou renomeação dos zooms) na mesma rodada de registro do item (a), sem tocar no relatório histórico.

**c) Saídas brutas do gerador com os nomes originais — `~/workspace/oficina-audit/referencias/media-generation-caprileo-diag-tras-*.webp` + `.json`.**
Os arquivos brutos da geração (`…-dir-0-…webp`, `…-esq-0-…webp` e seus `.json`) preservam os rótulos pré-troca. São artefatos intermediários, não as referências instaladas; não descrevem conteúdo em texto, apenas carregam o nome antigo. Risco baixo, mas listado por completude: quem reconstituir o lote a partir dos brutos precisa saber da troca.

**d) Documentos do projeto no PC — nada achado.**
A varredura de `app\docs\*.md` por "caprileo" não retornou nenhuma ocorrência de `caprileo_diag_tras_*` (só menções genéricas ao Capríleo em ESTADO_ATUAL, REGISTRO e APRENDIZADO_E_FLUXO, e ao lote 2). Ou seja: **não existe referência textual defasada nos docs do PC** — mas, como dito em (a), também ainda não existe ali o registro pós-troca. A cópia local `registro_lote2/APRENDIZADO_E_FLUXO.md` igualmente só menciona o Capríleo de forma genérica, sem os nomes das diagonais.

**Resumo da verificação nova:** nenhuma referência viva do arsenal descreve o conteúdo com o rótulo pré-troca; o que existe é (i) o relatório histórico da rodada 1, que deve ser lido como documento datado e complementado pelo registro pós-troca ainda pendente, e (ii) zooms e brutos de trabalho com nomes defasados, fora do arsenal. **Nada disso reabre C1 nem bloqueia o lote** — mas o registro pós-troca (hashes novos por nome + convenção) precisa ser escrito, pois hoje ele existe só nos nomes dos arquivos.

## 4. Veredito (linhas inequívocas)

- **C1 (SYM S2, rótulos trocados): FECHADO** — hashes conferidos nos dois lados e 3/3 itens confirmados visualmente nos dois arquivos renomeados.
- **LOTE 3 (Capríleo): FECHADO** — as três vistas entram no arsenal: duas diagonais traseiras corretamente rotuladas + topo (já aprovado na rodada 1, arquivo idêntico confirmado por hash).
- **Pendências S3/S4 que permanecem (não bloqueiam, entram no plano por escrito):**
  - **C2 (PRP S3):** pernas do topo espraiadas — modelar a articulação pelos perfis/costas, nunca pelo topo.
  - **C3 (DEF S3):** espirais dos chifres do topo mais fechadas ("caracol") — modelar o número de voltas pelos perfis.
  - **C4 (DEF/SIL S3):** diagonais rasas, próximas dos perfis — futura diagonal profunda (~45°) opcional.
  - **C5 (SIL S4):** margens das bases abaixo de 5% — aceitar como está, nada cortado.
- **Pendente de registro (não de imagem):** escrever nos documentos do projeto os hashes novos por nome + a convenção de nomes, e instalar o relatório da rodada 1 com essa complementação; e anotar/renomear os zooms de `zooms_lote3/` para não herdarem rótulos defasados.

A palavra final de fidelidade artística é do Mestre; este veredito é técnico.

---

## Nota do executor (rodada de 01/11/2026, ~11:00–11:15)

Veredito de fechamento recebido e relatório preservado neste arquivo. **Registro nos documentos do projeto ADIADO de novo pela regra anti-colisão:** no momento de devolver os documentos ao PC, a árvore estava suja com a tranche da frente principal (M `oficina3d/uv_xatlas.py`, `oficina3d/worker.py`, `testes/test_cor_passo.py`). O relatório da rodada 1 chegou a ser copiado para `docs/CRITICO-ref01-lote3.md` e foi REMOVIDO em seguida para não ser varrido por um commit da outra frente — a árvore voltou a conter só as 3 modificações da frente principal. Os PNGs renomeados (gitignored) seguem intactos no PC. **Edições prontas e guardadas localmente** em `~/workspace/oficina-audit/pc_docs_lote3/` (REGISTRO/ESTADO/APRENDIZADO editados a partir dos docs baixados às ~11:00; script `aplicar_edits.py`): **a próxima rodada deve baixar os docs de novo e reaplicar/revisar as edições** (a frente principal pode ter tocado nos docs desde então) — não subir os arquivos guardados sem conferir o diff. Zooms em `zooms_lote3/` já renomeados localmente (`esq_*` ↔ `dir_*`) conforme a recomendação do Crítico. Próxima rodada, com a árvore limpa: instalar `CRITICO-ref01-lote3.md` + este relatório de fechamento, aplicar o registro, commit + push só de documentos, e só então o lote fechado é reportável ao Mestre, com as fotos.
