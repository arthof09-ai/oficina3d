# Oficina 3D — contrato da arquitetura (Fase 1 / MVP)

Fonte de verdade para quem escreve código no app. Plano completo: `..\PLANO_OFICINA_3D_PARA_CLAUDE_CODE.md`.
Regras: escrever só em `E:\RPG_Assimilacao\Oficina3D\`; **nada no disco C:** (caches e temporários no E:); arte do RPG é privada (nunca sai do PC); **nunca alterar `KIT_TESTE_3D\`** (copiar para `jobs\` ou `app\testes\_dados\`).

## Ambientes
| O quê | Caminho |
|---|---|
| Python do app (3.10) | `E:\RPG_Assimilacao\Oficina3D\.venv\Scripts\python.exe` — tem torch cu124, fastapi, uvicorn, pydantic 2.10, trimesh, pillow, numpy, scipy, scikit-image, opencv, pymeshlab, rembg, gradio |
| Python do TripoSR | `...\.venv_triposr\Scripts\python.exe` (transformers 4.35; separado de propósito) |
| Blender 5.2.3 | `...\Ferramentas\Blender\blender-5.2.3-windows-x64\blender.exe` (headless: `-b --factory-startup -P script.py -- args`) |
| Motores | `...\motores\Hunyuan3D-2GP`, `...\motores\TripoSR` |
| Modelos | `HY3DGEN_MODELS=...\_cache\hy3dgen`, `HF_HOME=...\_cache\huggingface`, `U2NET_HOME=...\_cache\u2net` |

`oficina3d.config` tem todos esses caminhos e `env_subprocesso()` (variáveis de ambiente já apontando para o E:). **Use sempre isso** ao chamar subprocessos.

## Pastas
```
app\oficina3d\            pacote Python (rodar com .venv, cwd = app\)
  config.py  job.py       (prontos — contrato)
  worker.py  cli.py       (agente "núcleo")
  motores\                (agente "núcleo")
  entrada\                (agente "entrada")
  refino\                 (agente "refino")
  web\                    (agente "web")
app\testes\               testes por módulo (unittest ou scripts simples)
jobs\<id>\
  job.json
  entrada\   imagens/malha como o usuário mandou (cópias)
  preproc\   imagens prontas para o motor: <vista>.png (RGBA, fundo limpo, quadradas)
  forma\     saída crua do motor (forma.glb) + log do motor
  refino\    trabalho intermediário do refino
  saida\     modelo.glb, previa_<vista>.png, relatorio.json  (ENTREGA)
  log.txt
```

## job.json (ver `job.py`)
```json
{
  "id": "20261027-223000-orc",
  "criado_em": "2026-10-27T22:30:00-03:00",
  "nome": "orc",
  "modo": "livre | corpo-base | multivista | so-refinar",
  "imagens": [{"arquivo": "entrada/01_FRENTE_S.png", "vista": "frente"}],
  "malha_entrada": null,
  "opcoes": {"motor": "hunyuan-mini-turbo", "passos": null, "octree": 256, "seed": 1234,
             "flashvdm": true, "alvo_triangulos": 50000, "altura_m": null, "simetrizar": false,
             "dividir_pranchas": true, "remover_fundo": "auto"},
  "estado": "pendente | processando | concluido | erro | cancelado",
  "etapa": null, "progresso": 0, "erro": null, "avisos": [],
  "resultado": null,
  "historico": [{"quando": "...", "etapa": "...", "msg": "..."}]
}
```
`resultado` quando concluído: `{"glb": "saida/modelo.glb", "glb_cru": "forma/forma.glb", "previas": ["saida/previa_frente.png", ...], "relatorio": "saida/relatorio.json"}` (caminhos relativos à pasta do job).

### Vistas (etiquetas)
`frente, costas, esquerda, direita, frente-esquerda, frente-direita, costas-esquerda, costas-direita, cima, detalhe, referencia-de-cor`.
**Convenção (conferida no Orc e nos exemplos do Hunyuan):** `esquerda` = imagem em que o personagem **olha para a esquerda da imagem** (mostra o lado esquerdo do corpo). Hunyuan-mv: frente→front, costas→back, esquerda→left, direita→right.
Nomes do kit: `01_FRENTE_S`→frente, `02_DIREITA_E`→direita, `03_COSTAS_N`→costas, `04_ESQUERDA_O`→esquerda, `05_FRENTE_DIREITA_SE`→frente-direita, `06_COSTAS_DIREITA_NE`→costas-direita, `07_COSTAS_ESQUERDA_NO`→costas-esquerda, `08_FRENTE_ESQUERDA_SO`→frente-esquerda; Capríleo/Besta: `01_FRENTE, 02_COSTAS, 03_ESQUERDA, 04_DIREITA, 05_FRENTE_ESQUERDA, 06_FRENTE_DIREITA, 07_COSTAS_ESQUERDA, 08_COSTAS_DIREITA` (conferir visualmente a convenção esquerda/direita de cada kit).

### Motores (`opcoes.motor`)
| nome | modelo | entrada | tempo medido no Orc |
|---|---|---|---|
| `hunyuan-mini` | Hunyuan3D-2mini (0,6B), 30 passos | 1 imagem (frente) | 3,6 min com FlashVDM |
| `hunyuan-mini-turbo` | 2mini turbo, ~5 passos | 1 imagem | a medir (padrão provável) |
| `hunyuan-full` | Hunyuan3D-2 (1,1B) | 1 imagem | a medir |
| `hunyuan-mv` | Hunyuan3D-2mv (1,1B) | 1–4 vistas: frente/costas/esquerda/direita | ~35 min com 4 vistas (lento) |
| `triposr` | TripoSR (MIT) | 1 imagem | 48 s, com cor, forma ruim |
Medidas do PC: GTX 1660 SUPER 6 GB, ~5 s por passo de difusão no mini (limite é cálculo, não memória). **A GPU é uma só: um job por vez.**

## Interfaces entre módulos (Python, .venv)
Todas recebem `progresso: Callable[[int, str], None] | None` opcional (0–100 dentro da etapa, mensagem curta em português).

```python
# entrada  (agente "entrada")
oficina3d.entrada.preparar(job_dir: Path, job: dict, progresso=None) -> dict
#  -> {"imagens": [{"arquivo": "preproc/frente.png", "vista": "frente"}, ...],
#      "avisos": ["..."], "pranchas_divididas": [{"origem": "...", "partes": [...]}]}
oficina3d.entrada.vista_pelo_nome(nome_arquivo: str) -> str | None

# motores  (agente "núcleo")
oficina3d.motores.listar() -> list[dict]          # nome, descrição, aceita_multivista, disponivel
oficina3d.motores.gerar(nome: str, imagens: list[dict], opcoes: dict, pasta: Path, progresso=None) -> dict
#  imagens com caminhos ABSOLUTOS; grava pasta/forma.glb
#  -> {"glb": Path, "metricas": {"tempo_s":..., "vram_pico_mb":..., "triangulos":..., "vertices":..., "fechada":...}}

# refino  (agente "refino")
oficina3d.refino.refinar(glb_entrada: Path, pasta_trabalho: Path, pasta_saida: Path, opcoes: dict,
                         imagens: list[dict] | None = None, progresso=None) -> dict
#  grava pasta_saida/modelo.glb e pasta_saida/previa_<vista>.png
#  -> {"glb": Path, "previas": [Path], "silhueta_iou": {"frente": 0.91, ...},
#      "metricas": {"triangulos_antes":..., "triangulos_depois":..., "fechada":..., "altura":..., "pivo": "pes", ...}}

# job / worker / cli  (job.py pronto; worker e cli do agente "núcleo")
oficina3d.job.criar_job(arquivos: list[tuple[Path, str|None]], modo, opcoes, nome=None, malha=None) -> dict
oficina3d.job.ler_job(id) / listar_jobs() / salvar_job(job) / registrar(job, etapa, msg)
oficina3d.worker.processar_job(job_id) ; oficina3d.worker.loop()   # python -m oficina3d.worker
python -m oficina3d.cli enviar --imagem arq[:vista] ... --modo livre --motor hunyuan-mini-turbo
python -m oficina3d.cli status [id] ; baixar id destino ; motores ; worker

# web  (agente "web")
python -m oficina3d.web   # FastAPI em http://127.0.0.1:8765 (só local; nada exposto à rede)
```

## Etapas do worker
1. `entrada` (0–10%): `entrada.preparar` (pula no modo `so-refinar`).
2. `forma` (10–80%): `motores.gerar` → `forma\forma.glb`.
3. `refino` (80–98%): `refino.refinar` → `saida\`.
4. `exportar` (98–100%): `saida\relatorio.json` = job + métricas de todas as etapas.
Falha numa etapa → `estado="erro"`, `erro` com a mensagem, nada apagado.
