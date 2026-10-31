# Prompt de retomada: Oficina 3D v2 (CUNHADO-PC)

Cole o texto abaixo numa sessão nova do Claude Code no CUNHADO-PC, aberta em `C:\Users\txcga\RPG_Local\Oficina3D\app`.

---

Você é o Claude do CUNHADO-PC e vai continuar a construção da Oficina 3D v2. Não comece do zero.

1. Leia, nesta ordem:
   - `C:\Users\txcga\RPG_Local\Oficina3D\app\docs\PROMPT_ENTRADA_CLAUDE_CUNHADO_PC_OFICINA3D_v2.md` (regras e tarefa; valem todas as regras da seção 3);
   - o plano: `RELATORIO_CENTRAL_E_PLANO_OFICINA3D_v2.md`, na pasta `00 — Comece aqui\PC_Gusta_Oficina3D\OFICINA3D_v2_PLANO\` do Drive (antes do streaming: `C:\Users\txcga\Desktop\RPG Assimilação\RPG Assimilação\...`; depois: `G:\Meu Drive\RPG Assimilação\...`);
   - `C:\Users\txcga\RPG_Local\Oficina3D\app\docs\ESTADO_ATUAL.md`;
   - o fim de `docs\REGISTRO.md`, `docs\DECISOES.md` e `docs\ERROS.md`.
2. Rode `git -C C:\Users\txcga\RPG_Local\Oficina3D\app pull` e confira que o `ESTADO_ATUAL.md` bate com o git. Em conflito: Git > ESTADO_ATUAL.md > conversa.
3. Confira processos listados em "Processos rodando agora" (PID, log).
4. Continue a partir do **"Próximo comando exato"** do `ESTADO_ATUAL.md`.
5. Ao fim de cada tarefa: atualize ESTADO_ATUAL e REGISTRO, commit + push, e copie `docs\` para `Oficina3D_v2\REGISTRO\` no Drive.
