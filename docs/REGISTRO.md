# REGISTRO: diário da Oficina 3D v2 (CUNHADO-PC)
Regra: nunca apagar entradas; só acrescentar. Cada entrada: data/hora, o que fez, comando, resultado, evidência.

---

## 31/10/2026 ~11:45 — Início da sessão
- Prompt de entrada lido: `docs\PROMPT_ENTRADA_CLAUDE_CUNHADO_PC_OFICINA3D_v2.md`.
- Caminho real da pasta do plano (o prompt omite um nível): `C:\Users\txcga\Desktop\RPG Assimilação\RPG Assimilação\00 — Comece aqui\PC_Gusta_Oficina3D\OFICINA3D_v2_PLANO\`.
- Lidos: `RELATORIO_CENTRAL_E_PLANO_OFICINA3D_v2.md`, `analise_B_PC_CUNHADO.md`, `MANIFESTO_DOWNLOADS_OFICINA3D_v1.json`.

## 31/10/2026 ~11:50 — Medidas iniciais
- `hostname` → `PCdaNasa`.
- `nvidia-smi` → RTX 4060, driver 610.88, 8188 MiB total, 1098 MiB usados, 6859 MiB livres, 2% de uso. Processos com GPU: só aplicativos de desktop do dono do PC (lista omitida no repositório público).
- `Get-PSDrive C` → 46,2 GB livres. `G:` já existe ("Google Drive"), contém só `Meu Drive.lnk` → aponta para `C:\Users\txcga\Desktop\RPG Assimilação` (modo espelho).
- Pasta espelhada `Desktop\RPG Assimilação` = 6,9 GB.
- `RPG_Local\oficina3d_ia` = 26,3 GB (TripoSG 12,6; PartCrafter 10,2; DetailGen3D 3,4; python 0,1).
- `python --version` → 3.12.10; `py.exe` presente; `uv` ausente.
- Windows Update: chaves `PauseUpdatesExpiryTime` etc. vazias → **não pausado**.
- `gh auth status` → logado como arthof09-ai, escopo `repo`.

## 31/10/2026 ~11:55 — Repositório e pastas
- `gh repo create arthof09-ai/oficina3d --private --clone` (em `C:\Users\txcga\RPG_Local\Oficina3D`) → `https://github.com/arthof09-ai/oficina3d`; pasta renomeada para `app`.
- Criadas `motores`, `_cache`, `jobs`, `jobs_teste`, `locks` em `C:\Users\txcga\RPG_Local\Oficina3D`.
- Copiados para `app\docs\`: ARQUITETURA.md, USO_PARA_IAS.md, o prompt de entrada; para `app\docs\v1_recuperado\`: config.py, job.py, servidor_mcp.py, scripts de instalação, compat\torchmcubes; para `app\instalacao\`: o manifesto de downloads.
- Criados os arquivos de continuidade (ESTADO_ATUAL, REGISTRO, DECISOES, ERROS, COMANDOS_QUE_FUNCIONARAM.ps1, PROMPT_RETOMADA, SAUDE_FASE0.json).
- Commit `9661c68` em `main`, push OK. Evidência: `git ls-remote https://github.com/arthof09-ai/oficina3d.git main` → `9661c68fda6d...`; `gh api repos/arthof09-ai/oficina3d --jq .private` → `true`. VERIFICADO.

## 31/10/2026 ~12:00 — Drive: Oficina3D_v2 e item 0.1
- Criado `C:\Users\txcga\Desktop\RPG Assimilação\RPG Assimilação\Oficina3D_v2\` com `arquivo_jobs`, `referencias`, `aprovados`, `REGISTRO`, `modelos_guardados`, `instaladores`, `backups` (ainda no espelho; depois do streaming fica em `G:\Meu Drive\RPG Assimilação\Oficina3D_v2\`).
- `docs\*` (sem `v1_recuperado`) + manifesto copiados para `Oficina3D_v2\REGISTRO\`.
- Item 0.1 (Drive "atualizado"): **PENDENTE**. `%LOCALAPPDATA%\Google\DriveFS\Logs\drive_fs.txt` mostra o Drive em atividade (uploads dos arquivos novos, downloads vindos de outro PC) e erros de "Retrying operation" / `FAILED_PRECONDITION` às 14:56Z. Não dá para garantir "atualizado" pelo log: precisa de uma pessoa olhar o ícone do Drive.
- Item 0.2 (trocar para streaming): **PENDENTE**, precisa de cliques na tela (sem computer use nesta sessão).

## 31/10/2026 ~12:15 — Repositório público (pedido do Mestre)
- Mestre: "Quero o repositório público" e "Pode trabalhar com mais de um agente, mas registre tudo para uma possível sucessão".
- Tirados dos docs: o e-mail pessoal (prompt de entrada) e a lista de programas do cunhado (REGISTRO, SAUDE_FASE0). Conferido por busca: sem `gmail`/nomes de programas.
- Histórico refeito: branch órfã com a árvore limpa → force-push em `main` → `gh repo edit --visibility public`. Ver DECISOES GIT-02 a GIT-04.
- Drive conferido de novo: `G:\Meu Drive` não existe; G:\ ainda só tem `Meu Drive.lnk` → **continua em espelho**. Por isso nada de download/instalação ainda; sigo com código (Fase 1, item 1), que não depende do Drive.
