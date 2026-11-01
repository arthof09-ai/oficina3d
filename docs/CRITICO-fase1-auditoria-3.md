# Auditoria nº 3 do Crítico — Fase 1 da Oficina3D (FINAL)

**Data:** 01/11/2026, ~01:00–01:10 no relógio do PC (America/Sao_Paulo). **Crítico:** agente independente (CM-000009 convocou; esta auditoria não reaproveita relatórios do autor — tudo abaixo foi medido, lido ou executado por mim, nesta sessão).
**Escopo:** os 8 itens da definição de pronta (`app\docs\REVISAO_E_ROTEIRO.md` §1), com foco no que mudou desde a auditoria nº 2 e seu adendo: a Prova C completa (Besta Cristalina + Capríleo) e o QUAL-01 (perfis de qualidade).

## Veredito

# NÃO PRONTA — por dois itens (6 e 7), com uma única causa-raiz.

A engenharia está provada de ponta a ponta com evidência própria: suíte, motores, Prova C inteira, paridade, arquivamento e o QUAL-01 funcionando e reproduzível. O que impede o carimbo é documental/registral: **o QUAL-01 nunca foi commitado** (o código vive só na árvore de trabalho) **e a decisão QUAL-01 não existe em DECISOES.md**, embora o ESTADO_ATUAL a cite como registrada lá e declare o item 6 (repositório completo) "provado" sem ressalva. É a classe do erro GIT-01 reincidindo em miniatura. A correção é pequena (1 commit, 1 linha em DECISOES, 1 ressalva no ESTADO) — mas, enquanto não for feita, os itens 6 e 7 não são verdade, e o item 8 depende deles.

## Item a item

### Item 1 — Suíte verde na régua certa: ✅ PROVADO
Rodei `unittest discover -s testes -t .` no `.venv_app`, via tarefa agendada própria: **"Ran 218 tests in 24.965s — OK (skipped=1)", exit 0**. O número fecha exatamente com o alegado (204 da auditoria nº 2 + 14 do QUAL-01) — e confirma, de quebra, que `testes/test_qualidades.py` está na árvore e verde (sem ele, seriam 204).

### Item 2 — Os 5 motores com prova viva: ✅ PROVADO
Um job concluído com GLB real em disco por motor, conferido por mim: `hunyuan-mini` (prova-mini-full-2, 1.134 KB), `hunyuan-mini-turbo` (prova-refino, 1.134 KB), `hunyuan-mv` (prova-mv-full, 1.096 KB), `hunyuan-mv-turbo` (fumaca-mv-turbo, 1.096 KB), `triposr` (fumaca-arquivo-2, 1.099 KB) — somados às provas vivas da rodada R2 e aos 18 jobs da Prova C.

### Item 3 — Prova C (bateria dourada): ✅ PROVADO INTEGRAL
Medi os 18 jobs (`provac-*`) com o `medida.py` (parse próprio do GLB):

- **18/18 concluídos.** Finais: **49.750 triângulos em todos** (teto 50.000). Forma: máx. **38,9 s** (Orc mv-turbo: 37,1 s e 38,9 s — teto de 180 s folgado). VRAM: máx. **6.435 MB** (teto 8.188 MB).
- **Determinismo byte-idêntico nas 6 combinações** (sha256 do GLB, semente 7 == repetição; semente 42 difere): Orc mv `88c30236…`, Orc mini `5a2d94cc…`, Besta mv `ba8d6cd5…`, Besta mini `0dbf7062…`, Capríleo mv `1b92e3b8…`, Capríleo mini `742df2bd…`.
- **Autenticidade das imagens:** os sha256 das 8 imagens da Besta e do Capríleo em `app\testes\dourado\imagens` batem **8/8** com o índice da auditoria do Codex (`indice-orc-e-monstros.csv`, relatório de continuidade v002) e com as cópias que baixei do Drive nesta sessão. As imagens são as do kit de 27/10 (Besta 768×512; Capríleo ~700×700).

O item que bloqueou as auditorias nº 1 e nº 2 está fechado, sem ressalva.

### Item 4 — Paridade das 4 portas: ✅ PROVADO
Worker e web como tarefas `Running`. `/api/motores` ao vivo serve a licença final da RF-03 ("uso liberado, inclusive no resultado final") — sem o texto velho de "só rascunho". **MCP real, cliente meu nesta sessão:** servidor `oficina3d` respondeu com as **9 ferramentas** e a chamada `listar_motores` devolveu dados vivos. O caminho comum `validar_opcoes` (CLI/web/MCP) é o mesmo onde o QUAL-01 se aplica — verificado na sonda do item QUAL-01 abaixo.

### Item 5 — Arquivo no Drive provado: ✅ PROVADO
Conferi no `job.json` cru dos jobs recentes (varq-orc-s42/s1234): seção de arquivo com `"estado": "arquivado"`, além das provas de ida/volta com manifesto das rodadas anteriores, que nada no código de arquivamento mudou desde então.

### Item 6 — Repositório completo: ❌ NÃO PROVADO NO ESTADO ATUAL (achado C3-1)
A rodada R4 provou a instalação do zero para o código **de então**. Mas hoje:

```
git status --porcelain (HEAD local == remoto == eadceb0):
 M oficina3d/cli.py
 M oficina3d/config.py
 M oficina3d/job.py
?? oficina3d/qualidades.py
?? testes/test_qualidades.py
```

**Todo o QUAL-01 está fora do git.** Um clone do GitHub neste momento **não contém** os perfis de qualidade que o ESTADO_ATUAL anuncia como "no ar". Enquanto o commit não existir, a frase "o clone contém todo o código-fonte do app" é falsa para a funcionalidade mais recente — a mesma classe do GIT-01 (que a auditoria nº 1 tratou como grave).

### Item 7 — Documentação sem deriva: ❌ NÃO PROVADO (achados C3-2 e C3-3)
O grosso confere — e confere ao byte: os números da Prova C e a tabela de custos do QUAL-01 no ESTADO_ATUAL (24.874/1.250 KB, 49.750/2.332, 149.250/6.188, 298.500/10.703, 497.500/17.431; Lendário forma 1.209.599 tris em 157,2 s; VRAM ~6,4 GB) reproduzem exatamente as minhas medições, e a entrada do REGISTRO de ~00:50–01:00 existe e é fiel. Mas há duas derivas concretas:

- **C3-2:** o ESTADO_ATUAL lista "QUAL-01 (níveis de qualidade)" entre as "Decisões recentes do Mestre (DECISOES.md)". **DECISOES.md não tem nenhuma linha QUAL-01** (busca por `QUAL-01`, `Bronze` e `Lendário`: vazia). A lista de diretivas da entrada do REGISTRO também omite o QUAL-01 (traz QUAL-02, ANIM-01, MET-01/02/03, ARMAZ-01, QUAL-03). A decisão que fundou a funcionalidade não tem registro decisório — só comentários de código.
- **C3-3:** o ESTADO declara "Itens 1, 2, 4, 5 e 6 provados" sem ressalva — o que deixou de ser verdade no momento em que o QUAL-01 entrou sem commit (ver C3-1).

### Item 8 — Crítico aprovou a rodada final: ❌ NÃO (depende dos itens 6–7)
Esta é a rodada final. Com 6 e 7 reprovados, o item 8 não pode ser carimbado. Cumpridas as correções de C3-1/C3-2/C3-3, basta uma **conferência curta e dirigida** (git limpo e sincronizado + linha QUAL-01 em DECISOES + ressalva do ESTADO) para o item 8 virar verdade — não é necessária uma quarta auditoria completa.

## QUAL-01 sob as minhas mãos (além dos itens)

- **Código lido:** `oficina3d/qualidades.py` é limpo e faz o que promete (perfil = pacote de parâmetros + classe de motor; explícito vence). Integração mínima e correta: `config.py` (chave `qualidade`), `job.py` (validação do slug + `qualidades.aplicar` antes da mescla), `cli.py` (`--qualidade` com choices).
- **Sonda da API de validação (sem job):** `lendario` com 4 vistas → motor `hunyuan-mv`, passos 50, octree 384, alvo 500.000; com `octree=200, motor=hunyuan-mv-turbo, alvo=99999` explícitos → **os explícitos vencem** (e o `passos` do perfil permanece, como desenhado); `bronze` 1 vista → `triposr`; 4 vistas → automático turbo; slug `diamante` → **ValueError**. Tudo correto.
- **Jobs submetidos por mim:** `20261101-010133-critico3-bronze` → opcoes gravadas (bronze, mv-turbo, octree 128, alvo 25.000) e GLB final **sha256 `aa322a8da3576c8f` — byte-idêntico ao `bateriaq-bronze`** de horas antes. `20261101-010133-critico3-ouronegro` → opcoes (ouro-negro, hunyuan-mv sugerido pelo perfil, octree 320, alvo 300.000, passos 30) e GLB final **`9986658043ad0619` — byte-idêntico ao `bateriaq-ouro-negro`** (298.500 tris, 10.703 KB). Perfis reproduzíveis entre submissões independentes: provado duas vezes.

## Achados

| # | Gravidade | Achado |
|---|---|---|
| **C3-1** | **GRAVE** (para o item 6) | QUAL-01 inteiro fora do git: `qualidades.py` e `test_qualidades.py` não rastreados; `cli.py`/`config.py`/`job.py` modificados sem commit. Clone do GitHub não reproduz a funcionalidade anunciada. Correção: commit + push dos 5 arquivos. |
| **C3-2** | MÉDIO (item 7) | A decisão **QUAL-01 não existe em DECISOES.md**, mas o ESTADO_ATUAL a cita como registrada lá; o REGISTRO também a omite da lista de diretivas. Correção: acrescentar a linha QUAL-01 a DECISOES (data 01/11/2026, diretriz dos níveis Bronze→Lendário). |
| **C3-3** | BAIXO (item 7) | ESTADO declara o item 6 "provado" sem a ressalva do QUAL-01 não commitado. Correção: após C3-1, a frase volta a ser verdade; até lá, ressalvar. |
| **C3-4** | OBSERVAÇÃO (método) | Registro de transparência desta auditoria: leituras iniciais de `job.json` me sugeriram um "travamento de 3 h" da bateria varq. Era ilusão de relógio: o PC marca America/Sao_Paulo (01:04–01:07 durante as sondas) e a minha VM ~3 h a mais; ancorando no relógio do PC, a bateria varq fluiu normal (s42 concluído 00:59:50, s1234 01:03:19, ambos arquivados; s7b processando normalmente ao fim da auditoria; nenhum processo runner zumbi). **Nenhum travamento existiu.** Fica o aprendizado: em auditorias futuras, ancorar todo tempo no relógio do PC. |

## O que falta para PRONTA (lista fechada)

1. Commit + push do QUAL-01 (5 arquivos) e árvore limpa, local == remoto. **[C3-1]**
2. Linha QUAL-01 em `docs/DECISOES.md`. **[C3-2]**
3. ESTADO_ATUAL coerente com 1–2 (a frase do item 6 volta a ser verdade). **[C3-3]**
4. Conferência curta do Crítico sobre 1–3 → carimbo do item 8.

Nada de engenharia falta. A Fase 1 está a um commit e duas linhas de distância do PRONTA.
