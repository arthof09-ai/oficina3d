# CRÍTICO — Adendo da Auditoria nº 2 da Oficina3D (re-verificação N1/N2/N3 + Prova C, fatia do Orc)

- **Data/hora:** 2026-10-31, ~23:07–23:25 (America/Sao_Paulo, relógio do PCDANASA)
- **Auditor:** Agente Crítico oficial do projeto (EXEC-02), independente
- **Objeto:** as alegações do construtor de que (a) corrigiu N1, N2 e N3 da auditoria nº 2 e (b) executou e aprovou a fatia do Orc da Prova C. Nada foi aceito por alegação: suíte reexecutada por mim no interpretador de produção, hashes SHA-256 recalculados por mim sobre os GLBs em disco, triângulos contados por parse próprio do GLB, licenças consultadas ao vivo na web e na CLI, git dissecado (disco × commit × remoto).
- **Regra cumprida:** o Crítico não corrigiu nada; julga e aponta.

---

## VEREDITO FINAL ATUALIZADO

**NÃO PRONTA** — por um único motivo restante, e ele não é de engenharia: o **item 3 (Prova C) continua aberto** porque a bateria só rodou para **1 dos 3 personagens** (Orc, aprovado integralmente nos dois motores). Faltam as imagens do **Capríleo** e da **Besta Cristalina**, que não estão nesta máquina (estão no kit do notebook do Mestre). Pela definição do projeto (os 8 itens verdade ao mesmo tempo), o carimbo não sai com a bateria incompleta.

O que mudou desde a auditoria nº 2: **N1, N2 e N3 estão corrigidos de verdade** (evidência minha abaixo), e o item 7 passa a ser **PROVADO COM RESSALVA MENOR**. Os itens 1, 2, 4, 5 e 6 seguem provados. Se o Mestre declarar a bateria parcial aceitável, o estado de engenharia é "pronta aguardando insumo"; pelo texto da definição, o veredito formal é NÃO PRONTA até Capríleo e Besta rodarem.

| Ponto re-verificado | Veredito |
|---|---|
| N1 (testes apagados restaurados) | ✅ CONFERE |
| N2 (web servindo licença velha) | ✅ CONFERE |
| N3 (ESTADO_ATUAL desatualizado) | ✅ CONFERE COM RESSALVA MENOR |
| Prova C — fatia do Orc (2 motores) | ✅ CONFERE (integral, números meus) |
| Item 7 (documentação sem deriva) | ✅ PROVADO COM RESSALVA MENOR |
| Item 8 (aprovação da rodada final) | ❌ NÃO PROVADO (depende do item 3 fechar) |
| Item 3 (Prova C completa) | ⛔ AINDA BLOQUEADO — falta Capríleo e Besta Cristalina |

---

## N1 — CONFERE ✅

- **Suíte reexecutada por mim** (tarefa agendada própria, removida ao final) no interpretador de produção `.venv_app\Scripts\python.exe -m unittest discover -s testes -t .`, cwd=`app`, env do projeto: **Ran 204 tests in 22.971s — OK (skipped=1), EXIT=0** (log `_cache\logs\critico2_adendo_suite.txt`). O skip é o desenhado (registro MCP fora do `.venv_mcp`). São 204 — nem os 180 da auditoria nº 2, nem os 199 que os documentos afirmavam então: 180 + 19 restaurados + 5 novos preservados.
- **`testes\test_motores.py` em disco:** classes `TestPedido`, `TestGerarFalso`, `TestBase` (restauradas) **e** `TestPesosNecessarios`, `TestListarFormatoPublico` (novas) presentes, além de `AmbienteNucleo` e `TestListar`; **29 definições `def test_`** no arquivo.
- **Git:** HEAD local = `49e89e4ec1d05ce17d1c638e8917d2e3f47a9693`; `git ls-remote origin main` = **o mesmo hash** (paridade local×GitHub). `git status` limpo. `git show 49e89e4:testes/test_motores.py` contém as 7 classes e os 29 testes — a restauração está **no commit**, não só no disco. O commit também inclui a cópia do meu relatório (`docs/CRITICO-fase1-auditoria-2.md`), o ESTADO reescrito e o REGISTRO.
- A explicação do construtor para a 1 falha transitória da fusão (fixture antiga sem o `config.yaml` que a correção de 31/10 passou a exigir) é coerente com o código e com o resultado final verde que medi.

## N2 — CONFERE ✅

- `GET http://127.0.0.1:8765/api/motores` **ao vivo, consultado por mim**: os 4 motores Hunyuan com licença **"Tencent Hunyuan Community (uso liberado, inclusive no resultado final — RF-03 final, 31/10/2026)"** e o triposr com "MIT". **Nenhuma** ocorrência de "só rascunho".
- `cli motores` no mesmo ciclo: os mesmos 5 motores, todos "sim" (disponível). Ids, disponibilidade e conteúdo jurídico agora **batem** entre web e CLI — a paridade de conteúdo do item 4 está restaurada.

## N3 — CONFERE COM RESSALVA MENOR ✅⚠️

- `docs\ESTADO_ATUAL.md` foi **reescrito** (cabeçalho 31/10/2026 ~23:05, autoria declarada): afirma **204 testes** (verdade, medi), conhece R2/R3/R4, DONO-01/DONO-02, o veredito da auditoria nº 2 e o destino de N1/N2/N3; a seção "Pendente de verdade" lista só o que falta de fato (imagens de Capríleo/Besta; este adendo; Fase 2 como decisão do Mestre). **Zero** ocorrências de "199" no documento; nenhuma dívida paga figura como pendente. A deriva estrutural que motivou o N3 está corrigida.
- **Ressalva menor 1:** o ESTADO diz "Falta a fatia do mini-turbo (em medição)" — era verdade às 23:05; a fatia concluiu às ~23:06 e o REGISTRO já traz o adendo correspondente. O ESTADO ficou um passo atrás nesse detalhe (não é dívida paga listada como pendente; é um status superado por minutos). Recomendo atualizar essa frase na próxima passada.
- **Ressalva menor 2:** `docs\REVISAO_E_ROTEIRO.md` ainda cita **"199 testes"** em dois pontos (linha 7 e a tabela de status do P2, linha 92). O REVISAO é o roteiro datado da rodada, mas o número está factualmente errado no HEAD (204). Recomendo corrigir ou anotar como retrato datado.
- Julgamento: o item 7 passa a **PROVADO COM RESSALVA MENOR** — os documentos vivos de retomada (ESTADO + REGISTRO) refletem o real; os resíduos acima são de precisão, não de retrato.

## PROVA C — FATIA DO ORC — CONFERE ✅ (integral, com números meus)

Imagens-fonte: `app\testes\dourado\imagens\` contém as 4 cardinais (`orc_frente.png` 2.316.006 B, `orc_direita.png` 2.065.034 B, `orc_costas.png` 2.109.089 B, `orc_esquerda.png` 2.038.874 B — os mesmos tamanhos dos PNGs do pacote enviado pelo Mestre). **Fora do git:** `git check-ignore` confirma a regra `.gitignore:28 testes/dourado/imagens/` e `git status` está limpo com as imagens presentes.

Os 6 jobs em `BASE\jobs`, examinados por mim (job.json + `saida\relatorio.json` + SHA-256 recalculado sobre `saida\modelo.glb`):

| job | motor / seed | estado | GLB (bytes) | SHA-256 (meu cálculo) |
|---|---|---|---|---|
| 20261031-225432-provac-orc-s7 | mv-turbo / 7 | concluido | 2.173.168 | `88C30236…0E12514` |
| 20261031-225544-provac-orc-s42 | mv-turbo / 42 | concluido | 2.251.760 | `D78E4F2F…616A378` |
| 20261031-225703-provac-orc-s7b | mv-turbo / 7 | concluido | 2.173.168 | `88C30236…0E12514` |
| 20261031-230121-provac-orc-mini-s7 | mini-turbo / 7 | concluido | 1.506.640 | `5A2D94CC…81E30481E73` |
| 20261031-230214-provac-orc-mini-s42 | mini-turbo / 42 | concluido | 1.586.716 | `10CB12F5…08B793A6D6B` |
| 20261031-230306-provac-orc-mini-s7b | mini-turbo / 7 | concluido | 1.506.640 | `5A2D94CC…81E30481E73` |

Critérios da bateria, conferidos um a um:

- **(a) 6/6 concluídos** — `estado=concluido` nos 6 job.json. ✅
- **(b) Determinismo por semente, nos DOIS motores** — mv-turbo: s7 e s7b com **hash e tamanho idênticos**; mini-turbo: s7 e s7b **idênticos**; a semente 42 difere nos dois motores (a semente manda no resultado). ✅
- **(c) Triângulos do GLB final ≤ 50.000** — contagem minha por parse do chunk JSON do GLB (soma dos acessores de índices ÷ 3): **49.750 triângulos em cada um dos 6 GLBs**. ✅
- **(d) VRAM de pico ≤ 8.188 MB e tempo de forma ≤ 180 s** — dos `relatorio.json`: forma mv-turbo **39,5 / 41,4 / 40,5 s**; mini-turbo **33,1 / 31,2 / 31,2 s**; `vram_pico_mb` mv-turbo **6.411 / 6.411 / 6.435 MB**; mini-turbo **5.358 / 5.356 / 5.358 MB**. Totais de job entre 46,8 s e 74,9 s. ✅

**Observação de precisão (não muda o veredito):** o REGISTRO cita tempos de forma ~2 s menores que os dos `relatorio.json` (37,1/38,9/37,9 s no mv-turbo; 31,2/29,3/29,1 s no mini) — provavelmente mede só o trecho interno do motor. Os valores que atesto são os dos relatórios dos próprios jobs (tabela acima); o critério ≤ 180 s passa com folga nas duas métricas. Recomendo ao construtor declarar qual métrica o REGISTRO usa.

## ITENS 7 E 8, E O QUE RESTA PARA O ITEM 3

- **Item 7 (documentação sem deriva): PROVADO COM RESSALVA MENOR** (ressalvas no N3 acima).
- **Item 8 (Crítico aprovou a rodada final): NÃO PROVADO ainda** — não por defeito novo: a aprovação da rodada está atrelada à definição completa, e o item 3 segue aberto. Este adendo aprova, com evidência, N1/N2/N3 e a fatia do Orc; não aprova a Oficina como "pronta" enquanto a bateria estiver incompleta.
- **Para o item 3 fechar, falta exatamente isto:** (1) as imagens das vistas do **Capríleo** e da **Besta Cristalina** em tamanho útil (as do kit de 27/10 que está no notebook do Mestre), instaladas em `testes\dourado\imagens\`; (2) rodar a mesma bateria para cada um — 2 motores (mv-turbo e mini-turbo) × sementes 7 e 42 + repetição da 7 — e conferir os mesmos tetos: 6/6 concluídos por personagem, forma ≤ 180 s, VRAM de pico ≤ 8.188 MB, GLB final ≤ 50.000 triângulos e determinismo s7 == s7b byte a byte. Nada de engenharia falta: o caminho (imagens → jobs → relatórios → arquivo) é o mesmo que o Orc acabou de percorrer sob medição.

---

*Assinado: Crítico independente da Oficina3D — adendo gerado exclusivamente de evidência própria colhida ao vivo no PCDANASA (suíte executada pelo auditor, hashes recalculados, GLBs parseados, web/CLI consultados, git conferido contra o remoto).*
