# CRÍTICO VISUAL — REF-01 lote 4 RETRABALHO (2ª rodada) — REGISTRO-RESUMO

**AVISO DE PROVENIÊNCIA (não apagar):** o texto integral deste relatório foi entregue
num handoff de rodada em 01/11/2026 ~16:07 e NÃO ficou preservado em arquivo local;
o que segue é o registro fiel do seu conteúdo a partir do resumo pendente
(`oficina-audit/pendente-critico-ref01-lote4-v2.md`, 01/11/2026): vereditos, números,
verificações novas e retrabalho exigido. NÃO foram recriadas tabelas de âncoras que
não constam do resumo. A disposição final destes vereditos está no relatório de
reconciliação (`docs/CRITICO-ref01-lote4-reconciliacao.md`), que os julga item a item
e prevalece sobre este documento — ler os dois juntos, nunca este sozinho.

**Papel:** Crítico Visual sênior independente e ADVERSÁRIO (APR-02). Missão: tentar
reprovar.
**Data:** 01/11/2026 ~16:07 (rodada agendada das 15:54). **Escopo:** as mesmas duas
imagens do relatório `CRITICO-ref01-lote4-retrabalho.md`.
**A palavra final de fidelidade artística é do Mestre.**

## Arquivos julgados (SHA conferido — batem com o lote)

| Arquivo | SHA-256 |
|---|---|
| `orc_diag_tras_esq_refeita.png` | `ad57447a…c95c618e` |
| `orc_diag_frente_esq.png` | `895c0cd9…af09230a` |

## Veredito final por imagem (deste Crítico 2 — VER DISPOSIÇÃO FINAL ABAIXO)

- **`orc_diag_tras_esq_refeita.png` — REPROVADA (S2).** O retrabalho corrigiu a
  duplicata global SYM-4.1 (N1 passa; N2 numérico passa com folga: IoU 0,68 < 0,85,
  faixa 0,521/0,569 < 0,7, pé em perfil à esquerda), mas falhou em 2 das 9 âncoras
  da especificação, ambas do motivo do cinto: SYM-5.1 (alça não espelhada: fivela
  em x ≈ 0,63, descida para o quadril viewer-direito, igual à `tras_dir`) e
  SYM-5.2 (caveira grande do cinto à direita do losango, x ≈ 0,76 vs losango
  ≈ 0,60). NÃO instalar no PC. S3: POS-5.1 (pé viewer-direito fora do solo,
  sola ≈ 0,06 acima). S4: CAP-5.1 (painel da capa até o alto da canela, não a
  meia-canela).
- **`orc_diag_frente_esq.png` — APROVADA**, com S3 (ANG-5.1, giro de tronco fraco
  ~20°) e S4 (OBS-5.1, biqueiras/gancho do cinto) registrados. Anti-espelho passa
  (lobo à direita, ombreira à esquerda), pés coerentes com a diagonal esquerda,
  zero bolsinhas, zero machado, corpo inteiro, fundo liso, tom oliva.

## Verificações novas da rodada (APR-01, registradas e aplicadas)

- **NV-1 — Lateralização do cinto por vista:** medir x de fivela, losango e
  caveira grande relativos ao centro do tronco e exigir inversão entre frente e
  costas. Descobriu SYM-5.1/5.2 — e, retroativamente, o mesmo motivo na
  `tras_dir` JÁ APROVADA (fivela descendo para a direita, caveira à direita do
  losango). Aprovação da `tras_dir` mantida, mas com o desvio anotado; a refeita,
  submetida contra especificação expressa, não herdaria essa tolerância.
- **NV-2 — Linha do solo / pés plantados:** diferença de y das solas > 0,04 da
  altura = pé fora do solo. Refeita 0,06 (S3); `frente_esq` passa.
- **NV-3 — Uniformidade do fundo + margens:** cantos com std ≤ 2 e margens > 0,02
  nos quatro lados. Ambas passam.

## Retrabalho exato exigido (só a refeita traseira, segundo este Crítico 2)

Regenerar mantendo o que passou (lobo proeminente à esquerda, rosto em perfil
para a esquerda, pé esquerdo em perfil para a esquerda, pé direito traseiro,
capa proeminente à esquerda, tom oliva, fundo liso, zero bolsinhas, zero
machado) e corrigindo: (1) cinto espelhado de fato — fivela central
(x ≈ 0,50), alça para o quadril viewer-esquerdo, caveira grande à esquerda do
losango, resto espelhado junto; (2) pés plantados (± 0,02); (3) painel da capa
até a meia-canela; (4) re-submeter ao Crítico antes de instalar; pedido deve
nomear explicitamente "cinto espelhado, caveira à esquerda, alça para o
quadril esquerdo".

## DISPOSIÇÃO FINAL (reconciliação, terceiro Crítico — prevalece sobre este relatório)

- SYM-5.1 e SYM-5.2: fatos verdadeiros promovidos a defeitos por uma regra
  inválida — **ANULADOS como defeitos**. NV-1 **RETIRADA** do checklist
  (substituída por N7): aplicada com consistência, ela reprovaria o próprio par
  canônico (`costas_v2`, `tras_dir`, refeita); seus números decisivos não
  reproduzem (caveira 0,76 × grade real 0,64; IoU 0,68 = −0,05 abaixo de todos os
  outros medidores).
- POS-5.1 **reclassificado S4** (Δ sola 0,054 = profundidade da postura diagonal;
  a `tras_dir` aprovada tem 0,039). CAP-5.1 confirmado S4.
- A aprovação da `frente_esq` por este Crítico 2 está **ANULADA**: ele não
  executou a auditoria de novidade N5 (IoU 0,962 com `tresquartos_v2` = DUP-4.3).
- `orc_diag_tras_esq_refeita.png`: **INSTALAR** (substitui a reprovada).
  `orc_diag_tras_dir.png`: aprovação mantida **SEM ressalva** — riscar a anotação
  de "desvio" deste relatório.
- **Nenhuma das duas contestadas se regenera.** Regenerar a refeita com o cinto
  espelhado, como exigia este relatório, produziria a única traseira do arsenal
  inconsistente com `costas_v2` e `tras_dir` — expressamente desautorizado pela
  reconciliação.
