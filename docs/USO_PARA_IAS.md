# Oficina 3D — como Claude, ChatGPT/Codex e outras IAs usam o app

Quatro portas de entrada, todas para a mesma fila (`E:\RPG_Assimilacao\Oficina3D\jobs\`). O **worker** processa um job por vez na GPU; precisa estar rodando:

```
cd E:\RPG_Assimilacao\Oficina3D\app
E:\RPG_Assimilacao\Oficina3D\.venv\Scripts\python.exe -m oficina3d.worker
```

## 1. Pasta de jobs (qualquer IA com acesso a arquivos)
Use `oficina3d.job.criar_job(...)` (Python) ou crie a pasta à mão seguindo `ARQUITETURA.md` (`job.json` com `estado: "pendente"` + imagens em `entrada\`). O resultado aparece em `jobs\<id>\saida\` (`modelo.glb`, `previa_*.png`, `relatorio.json`).

## 2. Linha de comando
```
cd E:\RPG_Assimilacao\Oficina3D\app
..\.venv\Scripts\python.exe -m oficina3d.cli motores
..\.venv\Scripts\python.exe -m oficina3d.cli enviar --imagem C:\x\frente.png:frente --imagem C:\x\costas.png:costas --motor hunyuan-mv-turbo --esperar
..\.venv\Scripts\python.exe -m oficina3d.cli status
..\.venv\Scripts\python.exe -m oficina3d.cli baixar <id> D:\destino
```

## 3. Página e API HTTP (só neste PC)
```
..\.venv\Scripts\python.exe -m oficina3d.web      →  http://127.0.0.1:8765   (API em /api/..., ver /docs)
```

## 4. Servidor MCP (Claude Code, Claude Desktop, Codex, ChatGPT)
Ferramentas: `listar_motores`, `submeter_job`, `status_job`, `listar_jobs`, `obter_resultado`, `cancelar_job`, `iniciar_worker`, `saude`.
Roda no ambiente separado `.venv_mcp` (pacote `mcp` 2.x).

**Claude Code** (sessões abertas em `E:\RPG_Assimilacao\Oficina3D`): já configurado em `E:\RPG_Assimilacao\Oficina3D\.mcp.json` — o Claude Code pergunta uma vez se pode usar o servidor do projeto.

**Claude Desktop / outro cliente MCP por stdio:**
```json
{"mcpServers": {"oficina3d": {
  "command": "E:\\RPG_Assimilacao\\Oficina3D\\.venv_mcp\\Scripts\\python.exe",
  "args": ["-m", "oficina3d.servidor_mcp"],
  "env": {"PYTHONPATH": "E:\\RPG_Assimilacao\\Oficina3D\\app", "PYTHONUTF8": "1"}}}}
```

**Codex CLI** (`%USERPROFILE%\.codex\config.toml` no PC onde o Codex roda — tem que ser este PC, ou via HTTP abaixo):
```toml
[mcp_servers.oficina3d]
command = "E:\\RPG_Assimilacao\\Oficina3D\\.venv_mcp\\Scripts\\python.exe"
args = ["-m", "oficina3d.servidor_mcp"]
env = { PYTHONPATH = "E:\\RPG_Assimilacao\\Oficina3D\\app", PYTHONUTF8 = "1" }
```

**HTTP local (streamable-http)**, para clientes que não abrem processo:
```
..\.venv_mcp\Scripts\python.exe -m oficina3d.servidor_mcp --http --porta 8766   →  http://127.0.0.1:8766/mcp
```
Acesso de fora do PC (ChatGPT na nuvem, sessões em nuvem) exige túnel com chave (Tailscale/Cloudflare) — **não configurado**; decisão do Mestre.

## Dicas de entrada (para qualquer IA)
- PNG com **fundo transparente**; uma vista por imagem (prancha com várias vistas é separada sozinha, mas etiquete as partes).
- Vistas: `frente, costas, esquerda, direita` (+ diagonais, `detalhe`, `referencia-de-cor`). `esquerda` = personagem olhando para a esquerda da imagem.
- Motor: `hunyuan-mini-turbo` (1 imagem, rápido) ou `hunyuan-mv-turbo` (até 4 vistas, melhor forma). Corpo-base para rig: modo `corpo-base`, T-pose, sem armas/armadura, `simetrizar`.
- A saída é **só forma** (malha branca, ≤ 50 mil triângulos, pivô nos pés, Y para cima, frente +Z). Cor/textura: ver fases seguintes.
