# ERROS: Oficina 3D v2
Cada erro: data, mensagem, causa, solução, se virou script/patch.

| Data | Onde | Mensagem | Causa | Solução | Virou script/patch? |
|---|---|---|---|---|---|
| 31/10/2026 | Prompt de entrada | Pasta do plano não encontrada | O caminho do prompt omite o nível `RPG Assimilação\RPG Assimilação\` | Usar `C:\Users\txcga\Desktop\RPG Assimilação\RPG Assimilação\00 — Comece aqui\...` | Não (corrigir no prompt) |
| 31/10/2026 | Medida do SSD | `Get-PhysicalDisk` e `Win32_DiskDrive` voltaram vazios | Provável falta de admin | Pendente: ver em Gerenciador de Tarefas > Desempenho > Disco | Não |
| 31/10/2026 | Medida do SSD (resolução) | — | A consulta via sessão SSH do Muse respondeu | SSD NVMe NX-512 2280, 477 GB — erro encerrado | Não |
| 01/11/2026 | validar / Godot 4.7.2 headless | Godot sai com 3221225477 (0xC0000005) em `append_from_file` | O modo padrão `handle_binary_image=1` (extrair texturas) falha fora do editor num GLB com textura | `estado.handle_binary_image = 3` (embutir sem compressão) em `_godot_validar.gd` | Sim: teste `test_textura_nao_derruba_o_godot` (prova de mutação feita) |
| 01/11/2026 | validar / Godot headless | Nenhuma malha contada (0 triângulos) | No `--headless` o `generate_scene` cria `ImporterMeshInstance3D`, não `MeshInstance3D` | O script conta as duas formas e calcula a caixa pelos vértices | Sim (`_godot_validar.gd`) |
| 01/11/2026 | validar / Godot | Linha `VALIDACAO_JSON` não aparecia | `--quiet` do Godot cala também o `print` | Rodar sem `--quiet` | Sim (`godot.py`) |
