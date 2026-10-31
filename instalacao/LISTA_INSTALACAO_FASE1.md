# Lista de instalação — Fase 1

O que a Fase 1 instalou nesta máquina, com as versões conferidas ao vivo em
31/10/2026 (pelo Muse, fechando a dívida do agente B). Caminhos relativos à
BASE da Oficina (`<BASE>`); o código fica em `<BASE>\app`.

## 1. Runtime

- **uv** (gerenciador de Python/venvs), no PATH do usuário.
- **Python 3.10.22** instalado pelo uv em `<BASE>\_cache\uv_python` — nenhum
  Python do sistema foi tocado.

## 2. Ambientes (venvs em `<BASE>\`, locks em `app\instalacao\requisitos\`)

| venv | papel | pacotes-chave (conferidos) |
|---|---|---|
| `.venv_app` | app, worker, web, CLI | torch 2.5.1+cu124 (CUDA ok), transformers 4.49.0, diffusers 0.39.0, fastapi 0.162.0, trimesh 5.2.0, numpy 2.2.6, setuptools 84.2.1 + wheel (correção pós-instalação: sem eles o import do app falhava) |
| `.venv_triposr` | runner do TripoSR | torch 2.5.1+cu124, **numpy 1.26.4** (fixado: o trimesh 4.0.5 quebra no numpy 2), trimesh 4.0.5, torchmcubes via shim em `instalacao\compat` |
| `.venv_mcp` | servidor MCP | mcp 2.3.0 |

Locks congelados: `requisitos\app.lock.txt`, `triposr.lock.txt`, `mcp.lock.txt`
(`uv pip freeze` de cada venv após a instalação e as correções).

## 3. Motores (clones em `<BASE>\motores\`)

| clone | commit | observação |
|---|---|---|
| Hunyuan3D-2GP (kijai) | `f2456e0` | roda os 4 motores Hunyuan |
| TripoSR (VAST-AI-Research) | `107cefd` | + patch `instalacao\patches\triposr_bake_texture.patch` aplicado |

## 4. Modelos (cache HF em `<BASE>\_cache\huggingface\`)

- **13 arquivos do manifesto** (`instalacao\modelos.sha256.json`), **11,42 GB**,
  SHA-256 conferido um a um na instalação: DiTs turbo do mv (4,93 GB) e do mini
  (3,82 GB), 2 VAEs turbo, `model.ckpt` do TripoSR (1,68 GB), `u2net.onnx` e
  configs.
- **Baixados depois (31/10, com a internet de volta):** os DiTs completos
  (30 passos) do `hunyuan-mini` e do `hunyuan-mv`. Resultado: **`cli motores`
  mostra os 5 motores disponíveis**.

## 5. Ambiente (`app\instalacao\env.cmd` / `env.ps1`)

Define, sempre a partir da BASE: `OFICINA3D_BASE`, `HF_HOME`, `HY3DGEN_MODELS`,
`U2NET_HOME`, `TORCH_HOME`, `UV_CACHE_DIR` (tudo sob `<BASE>\_cache\`, nunca no
G:/Drive) e `OFICINA3D_ARQUIVO` (pasta `arquivo_jobs` da Oficina no Drive,
resolvida por curinga para não depender de acento em arquivo ASCII).

## 6. Tarefas agendadas (usuário atual, sem admin, no logon)

| tarefa | o que sobe | log |
|---|---|---|
| `Oficina3D_Worker` | fila de jobs (`instalacao\tarefa_worker\`) | `<BASE>\_cache\logs\tarefa_worker.log` |
| `Oficina3D_Web` | página/API em 127.0.0.1:8765 (`instalacao\tarefa_web\`) | `<BASE>\_cache\logs\tarefa_web.log` + `web_server.log` |

## 7. Portas de entrada no ar

- CLI: `.venv_app\Scripts\python.exe -m oficina3d.cli motores|status|enviar|...`
- Web: http://127.0.0.1:8765 (sobe sozinha no logon).
- MCP: `.mcp.json` pronto na BASE (stdio, `oficina3d.mcp`, 9 ferramentas);
  HTTP opcional na 8766, sempre com token.
- Pasta de jobs: integração por arquivos (ver `docs\USO_PARA_IAS.md`).

## 8. Como conferir em 1 minuto

```
.venv_app\Scripts\python.exe -m oficina3d.cli motores      (5 motores: sim)
.venv_app\Scripts\python.exe -m unittest discover -s testes (suite verde)
curl http://127.0.0.1:8765/api/saude                          (ok: true)
```
