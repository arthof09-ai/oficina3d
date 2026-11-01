# REGISTRO-CODEX — linha paralela da Oficina3D

## Escopo e plano vigente — 2026-11-01

Prompt atualizado do Mestre recebido neste chat. Mesma copia e branch `codex/melhoria-paralela`; principal somente leitura. Nenhum worker, tarefa agendada ou configuracao da principal sera alterado. Toda escrita de experimento fica em `Oficina3D-codex`. Antes de GPU: verificar a trava compartilhada e os jobs; nao iniciar concorrente. Compilacao e testes de CPU nao constituem inferencia GPU.

Ordem: (0) atualizar e medir a suite; (1) Gate 0 Paint 2.0/2GP em venv proprio, registrar comandos/versoes/imports; compilacao falhou = arquivar essa tentativa e seguir; (2) reproduzir T2/D-T2 e atacar qualidade de vertice com antes/depois; (3) melhorias medidas e auditoria da COR-08 quando publicada, sem duplicar sua implementacao. Licencas informativas (LIC-01). Mecanismo e qualidade visual sao vereditos separados; autoauditoria adversarial obrigatoria antes de fechar.

## Entrega 0 — base atualizada e suite medida

- HEAD inicial: `b30a5ad818aabb526a1800b7193f8fdee84dac12`; arvore limpa, copia e branch ja existiam. Nenhum clone novo necessario.
- Comandos: `git fetch origin`, `git merge --no-edit origin/main`.
- Merge fast-forward sem conflitos. HEAD apos merge: `0e8746e355a6e55ed6ba9263e7574ab2bad00296`. Nenhum arquivo da principal editado.
- Leitura dos sete documentos solicitados no setup e dos deltas apos atualizacao. T2/D-T2 ja fechados na principal; COR-08 ainda nao implementada neste HEAD. D-T2-2/3/4 ja corrigidas: auditar as correcoes, nao reaplicar patches antigos.
- Suite: `python -B -m unittest discover -s testes -v` na copia, **296 executados, 0 falhas, 0 erros, 1 skip** (295 passaram). Tempo unittest **26,193 s**, parede **28,3920497 s**.
- Interpretador/dependencias da `.venv_app` principal usados somente para leitura, bytecode desativado. `OFICINA3D_BASE`, `OFICINA3D_JOBS`, TEMP/TMP, HF_HOME e TORCH_HOME apontados para a base Codex antes de importar testes. Nao se instalou nada na principal. Gate 0 usara venv separado.
- Evidencias locais persistentes: `../evidencias/entrega0/suite.log` e `resultado.json` (logs fora do repo publico).
- Autoauditoria: conferir HEAD e merge; contar resultado real, incluindo skip; revisar destinos das escritas da suite; distinguir uso somente-leitura do interpretador de um venv independente. A suite passou, mas isso nao aprova qualidade visual. Sem inferencia pesada, sem novas imagens adicionadas ao git.

## Observacoes iniciais do Gate 0 (ainda nao e resultado)

- GPU detectada: RTX 4060, 8188 MiB. Espaço livre observado antes do ambiente: 42.071.654.400 bytes (~39,18 GiB).
- O batch do fork esta em `hy3dgen/texgen/differentiable_renderer/compile_mesh_painter.bat`, nao na raiz. Ele usa g++ e liga explicitamente Python 3.12; nao e receita MSVC/CPython 3.10. Existe `setup.py` com ramo Windows MSVC: sera o comando adequado ao Python 3.10 usado pelo projeto. Nenhuma alteracao do motor principal.
- `nvcc` nao encontrado no PATH; diretorio padrao CUDA e vswhere padrao nao encontrados na inspecao inicial. Resultado de compilacao ainda pendente; ausencia de driver NAO inferida (nvidia-smi funciona).
- SHA-256 suite.log: 1A2BA5BD825954061F01B09EEDEFB5993408F746DD1D2771AEB40E5B36A48207

- SHA-256 resultado.json: 841B3EDA23E801AA93582983B8EEBED1C455B9B1DEA3E5156C4F3BB322E8D209

- Preparacao do venv: tentativa inicial de Copy-Item por enumeracao expandiu os filhos dos pacotes em vez de preservar as pastas. Interrompida antes de qualquer build. Corrigida somente a site-packages Codex (caminho absoluto validado antes da limpeza), usando copia por diretorio. Python 3.10 tambem copiado para runtime proprio; nao ha system-site-packages nem link ao ambiente principal. O erro de preparacao nao sera apresentado como falha do Paint.

## Entrega 1 — Gate 0 T3 REPROVADO neste ambiente

- Ambiente proprio: `.venv_paint`, runtime CPython 3.10.22 (MSC v.1944, AMD64), torch 2.5.1+cu124, CUDA do wheel 12.4, setuptools 84.2.1, wheel 0.48.0, pybind11 3.1.0, ninja 1.13.2. Pacotes torch/dependencias copiados fisicamente; ferramentas de build instaladas somente no venv Codex. Codigo 2GP copiado da base (manifesto do projeto aponta f2456e0; sem .git no motor local, nao alego verificar o commit por git).
- Comando nas duas pastas de extensao: `.venv_paint/Scripts/python.exe -B setup.py build_ext --inplace`. Executar novamente, se necessario: `.venv_paint/Scripts/python.exe -B app/testes/codex/gate0_paint.py`.
- `custom_rasterizer`: exit 1 em **2,6017 s**; erro literal `OSError: CUDA_HOME environment variable is not set. Please set it to your CUDA install root.` O toolkit nao foi localizado no PATH/diretorio padrao. CUDA do wheel/driver nao implica compilador nvcc instalado.
- `differentiable_renderer`: exit 1 em **0,3714 s**; erro literal `Microsoft Visual C++ 14.0 or greater is required`. MSVC nao localizado pelo build. Nao instalei compiladores no sistema: alteracao fora da copia, e a regua manda seguir apos falha.
- Import `custom_rasterizer` tambem falhou por PIL ausente no venv minimo de build; isso e dependencia Python adicional, NAO a causa do erro CUDA. Import direto do kernel nativo confirmou `ModuleNotFoundError: custom_rasterizer_kernel`.
- **Autoauditoria adversarial:** `import mesh_processor` retornou sucesso, mas carregou `mesh_processor.py`, fallback Python do fork. Conferencia por EXTENSION_SUFFIXES reprova o falso positivo: nao existe .pyd no texgen. O executor reproduzivel agora exige extensao NATIVA e compilacao com exit 0; importar um .py nao passa o Gate 0. Nenhum peso Paint/Delight baixado, nenhuma inferencia GPU executada.
- Decisao: **T3 arquivado nesta tentativa/ambiente por falha de compilacao**. Nao e prova de que o algoritmo seja impossivel em uma RTX 4060 com toolchain preparado; e o resultado do Gate 0 solicitado neste PC. VRAM/RAM/tempo de inferencia, SSIM/DeltaE, cobertura e qualidade visual: NAO MEDIDOS. O Gate 0 nao autoriza afirmar qualidade boa ou ruim.
- Evidencias: `../evidencias/gate0/resultado.json` e logs por build/import/native; tamanhos e SHA-256 individuais registrados no JSON. Espaco livre apos preparo: **36.714.708.992 bytes**. Venv ocupa disco mas permanece como evidencia reproduzivel; nenhuma remocao/arquivo no Drive foi feita fora da copia.
- Proximo: Entrega 2, reproduzir T2/D-T2 na mesma malha e vistas; investigar conversao de espaco de cor com tons intermediarios (o teste sintetico atual usa so primarias 0/1, insuficientes para detectar erro de gamma). Isto e HIPOTESE a medir, nao causa confirmada.
- Suite apos Gate 0: **296 executados, 0 falhas, 0 erros, 1 skip**, **25,168 s** (log `../evidencias/gate0/suite.log`). Nenhum codigo do app alterado nesta entrega.
- Gate 0 SHA-256 resultado.json: 8674F7A0B982CD61A103FA541FF8E9AB56ADAF6F869DFEB837794CD6C17F6482
- Gate 0 SHA-256 suite.log: 6F48D581474C14B0FE9DE9E84FE34561BFC2D574AFB95710622A9E4192AFC112
