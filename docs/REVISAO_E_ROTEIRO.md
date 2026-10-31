# Revisão e roteiro — o que falta para a Oficina estar PRONTA

Escrito pelo Muse em 31/10/2026 (pedido do Mestre, 19:52: revisar tudo o que
falta, definir o que é "pronta" de verdade e rodar rodadas de melhoria sem
economizar — o que importa é a qualidade). Estado medido na escrita:
Fase 1 com itens 1–5 concluídos, dívida P6 paga, 5/5 motores disponíveis,
suite com 199 testes verde no interpretador de produção, Prova B (web × MCP)
aprovada pelo desenho do Crítico. Auditoria independente nº 1 do Crítico:
"aprovado com ressalvas graves" — status das ressalvas no fim deste documento.

## 1. O que "PRONTA" significa (definição de pronto da Oficina)

A Oficina v2 só pode ser chamada de pronta quando TODOS estes itens forem
verdade ao mesmo tempo, cada um com prova registrada (não com impressão):

1. **Suite verde na régua certa:** `unittest discover` 100% verde rodando no
   `.venv_app` (o interpretador de produção), sem skip além dos desenhados.
2. **Os 5 motores com prova viva:** cada motor (mv-turbo, mini-turbo, mini,
   mv, triposr) gerou pelo menos 1 GLB válido de verdade nesta máquina, com
   tempo e VRAM registrados — "arquivo de pesos presente" não é prova.
3. **Prova C (bateria dourada) aprovada:** Orc, Capríleo e Besta × {mv-turbo,
   mini-turbo} × 2 seeds, com os limites do Crítico: 12/12 GLBs válidos,
   ≤ 50 mil triângulos, Orc 4 vistas mv-turbo ≤ 180 s nas duas seeds, VRAM
   ≤ 8.188 MB, determinismo por seed e hashes registrados.
4. **Paridade das 4 portas:** o mesmo job submetido por pasta/CLI, web e MCP
   produz o mesmo resultado; web e MCP no ar sozinhos a cada logon.
5. **Arquivo no Drive provado:** job concluído aparece em `arquivo_jobs` com
   manifesto SHA-256 conferindo (ida) — e um job restaurado de lá abre igual.
6. **Repositório completo:** o clone do GitHub contém TODO o código-fonte do
   app (a classe do erro GIT-01 conferida arquivo a arquivo), e uma
   instalação do zero a partir do repositório reproduz o ambiente.
7. **Documentação sem deriva:** ESTADO_ATUAL descreve o presente, o USO não
   aponta caminho/módulo que não existe, e toda decisão está em DECISOES.
8. **Crítico independente aprovou a rodada final**, com a bateria dele rodada
   de novo (não reaproveitar a aprovação de uma rodada anterior).

## 2. Lacunas conhecidas hoje (honestidade antes de otimismo)

- **Prova C não rodou** — faltam as imagens douradas (Orc/Capríleo/Besta em
  tamanho útil). Procuradas no PC e no Drive (Oficina3D_v2 e `03 — Modelos
  3D`): não estão aqui; eram material da v1, noutra máquina. As imagens dos
  jobs de teste são minúsculas (objeto de 49×241 px) e não servem (P7).
- **Motores mini e mv (não-turbo) nunca rodaram ao vivo:** os pesos chegaram
  e o verificador os aceita, mas nenhum GLB saiu deles ainda (item 2 acima).
- **Refino (pymeshlab) só tem prova de unidade**, nenhum job real de refino
  ponta a ponta nesta máquina.
- **Textura de verdade (paint) está fora da v2 atual:** a saída é forma +
  cor de vértice. Se o Mestre quer textura pintada, é escopo de Fase 2.
- **MCP por HTTP (porta 8766) nunca foi exercitado ao vivo** — o stdio está
  provado com cliente real; o HTTP exige token e ficou sem prova.
- **Estabilidade longa do worker não foi medida:** nenhum teste de horas de
  fila, nem simulação de queda no meio de um job (a retomada de órfãos tem
  teste de unidade, não prova viva).
- **A página web nunca passou por revisão visual humana** (funciona; a
  aparência não foi julgada).

## 3. Rodadas de melhoria (ordem e critério de saída)

- **R1 — Fechar a Fase 1:** conseguir as imagens douradas, montar
  `testes\dourado\` e rodar a Prova C; auditoria nº 2 do Crítico sobre o
  resultado. Sai quando: Prova C aprovada ou reprovada com defeitos
  registrados e corrigidos.
- **R2 — Prova viva do resto:** 1 job real em cada motor que falta (mini,
  mv) e 1 job de refino ponta a ponta; MCP HTTP com token exercitado.
  Sai quando: item 2 da definição de pronto é verdade.
- **R3 — Robustez:** simulações de falha (matar o worker no meio do job,
  GPU ocupada por outro programa, disco apertando) e uma fila longa
  (10 jobs mistos) sem intervenção. Sai quando: nenhuma perda silenciosa;
  tudo vira erro claro ou retomada correta.
- **R4 — Instalação do zero:** instalar a Oficina numa BASE limpa só com o
  repositório + instalador, e repetir um job dourado. Sai quando: o item 6
  da definição de pronto é verdade.
- **R5 — Fase 2 (decisão do Mestre):** textura/paint, integração com
  Blender para limpeza da malha, e o que mais ele priorizar.

## 4. Riscos permanentes (vigiar, não resolver uma vez)

- **PC único:** a Oficina vive no PC do cunhado. Mitigação atual: código no
  GitHub (público por decisão GIT-02), registros espelhados no Drive e jobs
  arquivados com SHA-256. Os PESOS (modelos) não estão no GitHub — re-baixar
  leva ~1 h com internet boa; o manifesto de hashes está no repositório.
- **GPU compartilhada (USO-01):** trabalho pesado avisa o Mestre antes;
  o worker já espera a GPU livre quando outro programa a usa.
- **Repositório público:** nunca commitar e-mail, token, IP da tailnet,
  caminho com nome de usuário ou arte do RPG (regra GIT-02).

## 5. Status das ressalvas da auditoria nº 1 do Crítico

| item | o que era | status em 31/10 ~21:00 |
|---|---|---|
| P1 (grave) | suite vermelha no venv de produção (PID do trampoline do uv) | **corrigido** (o processo filho grava o próprio PID; suite verde na régua certa) |
| P2 | "152 OK" medido no interpretador errado | **corrigido** (régua oficial = `.venv_app`; 199 testes) |
| P3 | internet do PC quebrada (push impossível) | **resolvido** (era o túnel da VPN Windscribe em blackhole; desligada com autorização do Mestre; push sincronizado) |
| P4 | restart do worker sem explicação no log | **explicado e registrado** (era a troca do INFRA-01; causa no REGISTRO) |
| P5 | arquivamento no Drive desligado (env sem OFICINA3D_ARQUIVO) | **corrigido e provado** (job real arquivado com manifesto) |
| P6 | 5 testes + LISTA faltando | **pago** (47 testes novos + LISTA_INSTALACAO_FASE1.md) |
| P7 | imagens de prova minúsculas | **aberto** — é o bloqueio da Prova C (seção 2) |

Achados posteriores à auditoria, já corrigidos e registrados: **INFRA-01**
(venv errado do Hunyuan em `config.py`), **numpy 2 no venv TripoSR**
(fixado 1.26.4), **web morta no pythonw** (stderr inexistente; lançador usa
python.exe com log), **GIT-01** (`oficina3d/motores` inteiro fora do git) e
derivas de texto (RF-03 "só rascunho", módulo MCP no USO).
