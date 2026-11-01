# ESTADO ATUAL: Oficina 3D v2 (CUNHADO-PC)
**Atualizado em:** 31/10/2026, ~23:05 (horario do PC)
**Quem escreveu:** Muse (CM-000009), apos a auditoria n. 2 do Critico e as correcoes N1/N2/N3.

## Onde a Oficina esta
- **Fases 0 e 1 (itens 1 a 5) CONCLUIDAS e provadas ao vivo.** Suite oficial no
  interpretador de producao (`.venv_app`): **204 testes, OK** (1 skip desenhado:
  o registro do servidor MCP fora do `.venv_mcp`).
- **Item 6 (bateria dourada, Prova C): FATIA DO ORC APROVADA** em 31/10 ~22:57
  (imagens enviadas pelo Mestre: as 4 vistas cardinais do kit de 27/10, em
  `testes\dourado\imagens\`, gitignored). mv-turbo, sementes 7 e 42: forma em
  ~38 s (teto 180 s), VRAM de pico 6.411 MB (teto 8.188), GLB final com 49.750
  triangulos (teto 50 mil), e a repeticao da semente 7 gerou GLB **byte-identico**
  (determinismo provado). Falta a fatia do mini-turbo (em medicao) e os outros
  dois personagens: **Caprileo e Besta Cristalina** (as imagens estao no kit do
  notebook; o Mestre esta localizando/enviando).
- **Rodadas de melhoria R2, R3 e R4 CONCLUIDAS** (motores todos com prova viva,
  refino ponta a ponta, MCP por HTTP com token; resistencia do worker provada:
  retomada de orfao, espera de GPU, fila 10/10; instalacao do zero so com o
  GitHub, sem tocar em nenhuma referencia — e a DONO-02 provada).
- **DONO-01/DONO-02 valendo:** o app e novo e do Mestre, funciona SEM precisar
  das referencias; as referencias ficam PRESERVADAS para os Comestres
  auditarem o trabalho. Nada foi excluido.

## Auditoria n. 2 do Critico (31/10 ~22:51) — veredito: NAO PRONTA
Pela definicao de 8 itens: nucleo tecnico provado (1, 2, 4, 5, 6); item 3
bloqueado (Prova C, insumo); itens 7 e 8 nao provados por documentacao velha.
Defeitos achados pelo Critico e o destino de cada um:
- **N1 (GRAVE):** o commit 8030d4b (ciclo R2 do Muse) sobrescreveu
  `testes/test_motores.py` e apagou 19 dos 24 testes (TestPedido, TestGerarFalso
  com cancelamento/tree-kill/JobObject, TestBase). **CORRIGIDO:** arquivo
  restaurado do historico e fundido com os 5 testes novos (29 no arquivo);
  a fusao expos 1 teste antigo desatualizado frente a exigencia do config.yaml
  (31/10) — fixture corrigida. Suite final: **204 testes, OK**.
- **N2 (MEDIO):** o processo web era anterior ao ajuste RF-03 e servia a
  licenca antiga ("so rascunho"). **CORRIGIDO:** web reiniciada pela tarefa;
  `/api/motores` conferido servindo o texto final.
- **N3 (BAIXO):** este ESTADO estava parado nas ~20:20. **CORRIGIDO** por esta
  reescrita.
- Aguarda-se o **adendo do Critico** re-verificando N1/N2/N3 e a fatia do Orc.

## Pendente de verdade (so isto)
1. Imagens douradas do **Caprileo** e da **Besta Cristalina** (kit de 27/10 no
   notebook do Mestre; partes do download do Codex ou o kit inteiro servem).
2. Adendo do Critico sobre a auditoria n. 2.
3. **Fase 2** (textura/pintura e demais frentes do roteiro): decisao do Mestre.
4. Opcional do Mestre: gerar as imagens do Orc corpo-base em T-pose (o brief
   com prompts e checklist ja existe; a geracao e fora da Oficina).

## Operacao
- Tarefas `Oficina3D_Worker` e `Oficina3D_Web` sobem no logon; pagina em
  http://127.0.0.1:8765; MCP stdio (9 ferramentas) e HTTP com token disponivel.
- Repositorio publico: https://github.com/arthof09-ai/oficina3d (HEAD: ver
  `git log`). Espelho do REGISTRO no Drive conferido por MD5 a cada ciclo.
- Janela de trabalho pesado: PC livre ate domingo 01/11 a noite (USO-01).
