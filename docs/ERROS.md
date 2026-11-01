# ERROS: Oficina 3D v2
Cada erro: data, mensagem, causa, solução, se virou script/patch.

| Data | Onde | Mensagem | Causa | Solução | Virou script/patch? |
|---|---|---|---|---|---|
| 31/10/2026 | Prompt de entrada | Pasta do plano não encontrada | O caminho do prompt omite o nível `RPG Assimilação\RPG Assimilação\` | Usar `C:\Users\txcga\Desktop\RPG Assimilação\RPG Assimilação\00 — Comece aqui\...` | Não (corrigir no prompt) |
| 31/10/2026 | Medida do SSD | `Get-PhysicalDisk` e `Win32_DiskDrive` voltaram vazios | Provável falta de admin | Pendente: ver em Gerenciador de Tarefas > Desempenho > Disco | Não |
| 31/10/2026 | Medida do SSD (resolução) | — | A consulta via sessão SSH do Muse respondeu | SSD NVMe NX-512 2280, 477 GB — erro encerrado | Não |
| 01/11/2026 | Codex T3 Gate 0 isolado | `CUDA_HOME environment variable is not set` e `Microsoft Visual C++ 14.0 or greater is required` | Compilacao sem CUDA Toolkit/MSVC localizados; PyTorch CUDA 12.4 nao inclui nvcc | Tentativa arquivada por regua pre-registrada; sem alterar sistema/principal, sem baixar pesos; seguir T2. Ver REGISTRO-CODEX | `testes/codex/gate0_paint.py` guarda comandos/logs/versoes e exige import NATIVO |
