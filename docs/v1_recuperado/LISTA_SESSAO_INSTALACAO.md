# Lista única da Sessão de instalação — Oficina 3D

27/10/2026 ~20:30 (UTC−3). Autor: Claude CM-000008 (sessão Local do Claude Code no PC do irmão).
Status: **PROPOSTO** — aguardando o "pode" do Mestre (uma vez só, para tudo desta lista).

---

## 1. O que o PC tem de verdade (Fase 0, medido 27/10 20:12) — VERIFICADO

| Item | Medido | Plano §2.1 |
|---|---|---|
| Placa de vídeo | NVIDIA GeForce **GTX 1660 SUPER**, **6144 MiB**, compute 7.5 (Turing) | bate |
| Driver | **610.88**, suporta até **CUDA 13.3** | — |
| VRAM livre em repouso | ~5,1 GB (1027 MiB já usados por Windows, Brave, Steam, NVIDIA Overlay, Claude) | — |
| CPU | AMD Ryzen 5 4600G, 6 núcleos / 12 threads | bate |
| RAM | 15,9 GB (2×8 GB DDR4-3200); ~9,6 GB livres no momento | bate |
| Arquivo de paginação | 7,25 GB, no disco E: | — |
| Windows | 11 Home Single Language, build 26200 | bate |
| Disco C: | SSD WD Green 120 GB — **10,8 GB livres** | — |
| Disco E: | WD10EARX 1 TB — **534,8 GB livres**. Modelo de **HD mecânico** (WD Green) → carregar modelos de IA vai ser lento (INFERIDO pelo modelo do disco) | — |
| Disco F: | SSD GO! Memory 240 GB — 7,1 GB livres | — |
| Python | **3.11.0** em `C:\Program Files\Python311` (pip 22.3) | — |
| Git | **2.50.1** ✅ | — |
| winget | 1.29.380 ✅ | — |
| Visual Studio / Build Tools C++ | **não tem** | — |
| CUDA Toolkit (nvcc) | **não tem** (não é obrigatório: o PyTorch traz o CUDA dele) | — |
| Blender / Godot | não tinha → **baixando agora (portáteis, sem UAC)** | — |

**Conclusões:**
- A placa é a esperada. 6 GB de VRAM: só **forma** (malha branca) é realista. Textura por IA (Hunyuan3D-Paint) **não** entra agora.
- **O disco C: é o gargalo.** Tudo vai para o E:, e o que for obrigado a ir para o C: (Build Tools) é configurado para usar o mínimo.
- **Hunyuan3D-2GP exige Python 3.10** (o PC tem 3.11). Precisa do Python 3.10 ao lado (sem tirar o 3.11).
- O repositório oficial do fork 2GP está no **GitHub** (`github.com/deepbeepmeep/Hunyuan3D-2GP`); não preciso do espelho `openi.pcl.ac.cn`.

## 2. Itens SEM janela do Windows (sem UAC)

| # | Item | Origem oficial | Download | No disco (E:) | Para quê |
|---|---|---|---|---|---|
| 1 | Blender 5.2.3 portátil | download.blender.org | 387 MB | ~1,2 GB (INFERIDO) | refino, UV, bake, render, export |
| 2 | Godot 4.7.2-stable portátil | github.com/godotengine | 82 MB | ~0,2 GB | teste de importação (Fase 4) |
| 3 | Python 3.10.11 (instalação "só para mim", em `Ferramentas\Python310`, sem PATH) | python.org | 28 MB | ~0,2 GB | exigido pelo Hunyuan3D-2GP |
| 4 | PyTorch 2.5.1 + torchvision, CUDA 12.4 | download.pytorch.org | **~2,6 GB** | ~5 GB por ambiente | rodar os motores na GPU |
| 5 | Dependências Python (Hunyuan3D-2GP, TripoSR, app: diffusers, transformers, trimesh, pymeshlab, rembg, fastapi…) | pypi.org / github.com | ~1,5 GB | ~3 GB | motores + app |
| 6 | Modelo **Hunyuan3D-2mini** (forma 0,6 B, fp16 + VAE) | huggingface.co/tencent | **4,0 GB** | 4,0 GB | motor principal (6 GB VRAM) |
| 7 | Modelo **Hunyuan3D-2mv** (multi-vista, fp16) | huggingface.co/tencent | **4,7 GB** | 4,7 GB | requisito multi-imagem |
| 8 | Modelo **Hunyuan3D-2** (forma 1,1 B, fp16 + VAE) | huggingface.co/tencent | **5,1 GB** | 5,1 GB | comparação de qualidade |
| 9 | Modelo **TripoSR** | huggingface.co/stabilityai | **1,6 GB** | 1,6 GB | motor alternativo (licença MIT) |
| 10 | Modelo de remoção de fundo (u2net, do rembg) | github.com/danielgatis/rembg | 0,2 GB | 0,2 GB | limpar fundo da imagem |

Notas:
- Itens 4–10 passam de 500 MB cada (4, 6, 7, 8, 9): **esta tabela é o aviso de nome, origem e tamanho** pedido no CLAUDE.md §5.
- Dos repositórios da Tencent baixo **só os arquivos fp16 .safetensors** necessários (o repositório inteiro passa de 60 GB, com cópias duplicadas em .ckpt).
- Dois ambientes Python separados (Hunyuan pede `transformers 4.49`, TripoSR pede `4.35`): `.venv` (Python 3.10, app + Hunyuan) e `.venv_triposr`.
- O item 3 roda um instalador (`Start-Process`) → está na lista do "pode", mas **não abre janela de UAC** (instalação por usuário, em E:).
- O pip vai usar pasta temporária no E: (para não encher o C:).

## 3. Itens COM janela do Windows (UAC — o irmão clica "Sim")

| # | Item | Origem | Download | Disco | Para quê |
|---|---|---|---|---|---|
| 11 | **Visual Studio 2022 Build Tools** — só "C++ para desktop" (MSVC v143 + Windows SDK), via `winget install Microsoft.VisualStudio.2022.BuildTools` | Microsoft (winget) | ~2 GB | ~6–7 GB no total; com pastas apontadas para o E:, **~3 GB ficam no C:** (INFERIDO) | compilar `torchmcubes` (TripoSR) e as extensões C++ do Hunyuan3D |

- `winget` pede aceitar os **termos de uso** (`--accept-source-agreements --accept-package-agreements`). O "pode" do Mestre vale para isso também.
- **Provavelmente não pede reiniciar.** Se pedir, aviso antes.

## 4. Fora desta lista (de propósito)

| Item | Por que fica de fora |
|---|---|
| CUDA Toolkit 12.4 (instalador NVIDIA, ~3 GB, vai para o C:) | Só serve para compilar extensões de **textura** por IA (Fase 3, opção C), que provavelmente nem cabem em 6 GB de VRAM. O C: não aguenta. Se um dia precisar: tentar primeiro o `nvcc` pelo pip (pacote oficial da NVIDIA no PyPI, sem UAC) — PROPOSTO, não testado. |
| Modelos de textura Hunyuan3D-Paint + Delight (~9 GB) | Mesma razão: Fase 3 opção C. |
| TRELLIS | Pede ≥16 GB de VRAM. Não cabe. |
| Mexer no arquivo de paginação (memória virtual) | É configuração do sistema. Só se faltar memória de verdade, e com ordem do Mestre. |

## 5. Totais

| | Valor |
|---|---|
| Download total | **~22 GB** |
| Uso no E: (ferramentas + 2 ambientes + modelos + cache do pip + parte do Build Tools) | **~40 GB** → sobram **~495 GB** |
| Uso no C: | **~3 GB** (Build Tools) → sobram **~7–8 GB** (INFERIDO) |
| Janelas de UAC | **1** (Build Tools) |
| Reinício | provavelmente nenhum |

## 6. Ordem da Sessão de instalação
1. (já em andamento, sem UAC) Blender e Godot: baixar, conferir SHA oficial, extrair, testar `--version`.
2. **Build Tools** (a única janela de UAC) — o irmão precisa estar presente.
3. Python 3.10 por usuário → criar `.venv` → PyTorch CUDA → testar `torch.cuda.is_available()`.
4. Clonar Hunyuan3D-2GP e TripoSR (GitHub) → dependências → compilar o que for preciso.
5. Baixar os modelos (itens 6–10) — demora; pode seguir depois que o irmão for embora.
6. Teste real: gerar a malha do Orc com o Hunyuan3D-2mini (perfil 4), medir tempo e VRAM de pico.

## 7. Licenças (PENDENTE de leitura completa)
- TripoSR: MIT (VERIFICADO no README).
- Hunyuan3D-2 / 2mini / 2mv: "Tencent Hunyuan Community License" — tem restrições de território e de uso comercial; ler o texto antes de usar modelos no jogo comercial (PENDENTE).
