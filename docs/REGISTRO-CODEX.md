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
