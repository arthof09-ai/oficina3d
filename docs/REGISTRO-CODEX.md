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

## Entrega 2 — auditoria independente T2/D-T2 e correcao C-COR01

### Reproducao e achados

- Mesmas entradas do J1 `20261101-124814-t2-orc`: refinado PRESERVADO `modelo_sem_cor.glb` e quatro `preproc/*.png`, copiados com hash conferido para `../evidencias/t2/entrada_orc`. O pedido historico aponta `saida/modelo.glb`, que depois foi sobrescrito pelo colorido; reproduzir por esse caminho seria entrada errada. Usado o refinado preservado, como manda L-11.
- Duas reproducoes do passo (CPU, sem nova geracao da forma e sem worker da principal): SHA **949e3cf7009b8e23e63474fc395d45226acb2ec63342e2a419b3996b7c9c2f3a**, identico a prova original. Parede do runner **3,5117 / 3,4919 s**; Blender do primeiro run **2,63 s** (original 2,57 s). Cobertura exata: 31.033 vista / 22.661 propagacao / 11.580 sem cor, total 65.274.
- D-T2 real, par `20261101-131410-crit-t2-soforma`: legitimo aceita (mediana 0,00056, p90 0,0013, caixas 1,00098/1,00184/1; 27.421 vertices da forma). Sabotagens proprias via trimesh: X2 recusa (0,02022/0,08138, caixa 2,00197); X0,5 recusa pelo p90 0,12702; Y2 recusa (caixa 2,00368); Z2 recusa (mediana 0,07758/p90 0,14608). Numeros reproduzem os do Critico, incluindo o X0,5 que ele tinha apenas relido.
- Misto X2 + vistas conclui, forma 0%, recusa registrada: 20.054 vista / 5.433 propagacao / 1.934 sem cor. Diferenca contra 20.034/5.450/1.937 do Critico NAO atribuida a regressao: usei as vistas PREPROCESSADAS do J1; a prova dele usou as canonicas cruas. O caso prova a recusa da forma e continuidade pelas vistas; nao alego identidade numerica com entradas diferentes. Evidencia persistida caso a caso em `../evidencias/dt2/resultado.json`.
- D-T2-2/3: campos modo/rotulo e aviso por modo confirmados no codigo atualizado e na suite; nao reexecutei um bake T1 completo nesta frente. D-T2-4: iteracao de todos os primitivos existe, mas a checagem de contagens ainda compara SOMAS; auditoria adicional de contagens cruzadas fica na Frente 3. A guarda de alinhamento tambem aceitou distancias NaN/negativas em probe independente: defesa numerica a corrigir na Frente 3, sem afirmar ocorrencia no job real.

### Defeito colorimetrico demonstrado e correcao

- Sonda no Blender **5.2.3 LTS**: PNG sRGB `(137,103,58)` chega em `img.pixels` como `(0,53725493;0,40392160;0,22745100)`. Escrever esses numeros em `FLOAT_COLOR.color` declara luz LINEAR; `color_srgb` devolve `(0,75935453;0,66815293;0,51421463)`, ou **(194,170,131)** em bytes. O bug e independente de silhueta/UV e nao e mera mudanca de iluminacao.
- Correcao C-COR01: decodificar sRGB das imagens byte antes de amostragem/propagacao; formas glTF e imagens float continuam lineares. Mascara e selecao de vistas permanecem calculadas sobre os mesmos pixels/normal/oclusao. Relatorio agora declara o espaco de cor. Nenhum ajuste de cor especifico ao Orc, nenhuma cor oliva forcada.
- Fontes primarias do contrato: [Blender FLOAT_COLOR / scene linear](https://docs.blender.org/api/3.2/bpy.types.FloatColorAttributeValue.html), [glTF 2.0, COLOR_0 linear](https://registry.khronos.org/glTF/specs/2.0/glTF-2.0.pdf). O comportamento exato da versao instalada foi MEDIDO; nao inferido dessas paginas.
- Testes novos: curva com tons intermediarios e segmento escuro; oliva conhecido; PNG real -> GLB real com COLOR_0 linear esperado; fonte GLB ja linear sem segunda conversao. A contraprova executa o teste PNG contra o exportador do HEAD antigo: **1 falha numerica esperada, 0 erros de infraestrutura**, erro maximo 0,28709664. Com a correcao: todos passam. O teste de forma tolera um passo de 8 bits: o importador Blender quantiza a cor em BYTE_COLOR (erro observado 0,00082202), nao se confunde isso com segunda conversao (~0,20).

### Antes/depois medido — Orc Prata

Render de prova: **Cycles CPU, Emission/unlit, Standard, exposicao 0, gamma 1**, 640x800, oito angulos antes e depois; 40,22 s totais do runner. Referencia ajustada pela mesma caixa envolvente, sem otimizacao de IoU; regioes aproximadas FIXAS (coordenadas em `metricas_cor.json`), pixels comuns com erosao de 3 px. Regioes incluem cabelo/equipamento: mediana da caixa NAO e mediana de pele; o teste isolado de oliva e a prova de preservacao do tom. As metricas abaixo comparam a MESMA correspondencia antes/depois; nao sao aprovacao semantica ou artistica.

| Regiao | SSIM antes | SSIM depois | DeltaE2000 medio antes | Depois |
|---|---:|---:|---:|---:|
| Rosto | 0,10359 | 0,13746 | 28,3777 | 17,1007 |
| Peito | 0,17095 | 0,22778 | 27,8305 | 14,8642 |
| Pernas | 0,14731 | 0,20239 | 26,7890 | 13,1707 |

- **Determinismo corrigido:** dois runs com SHA **eed4cdf74205a692f4659622ebdcf3b38bc53477345a3526e71b2149c1534111**. Parede **3,7892 / 3,6921 s**; primeiro tempo Blender **2,94 s**. Custo adicional observado ~0,2-0,3 s por Orc, nao ganho de desempenho.
- **Geometria/normais/UV/indices antes = depois**, hash independente dos acessores **c4bfc17342c982bd24c6a7b4a29da1f705373c8f9156aeab614135793cb553c7**. Alpha do render frontal identico. GLB **3.180.412 bytes** antes e depois. Cobertura identica, inclusive vertices pretos/sem fonte: a correcao nao esconde os buracos.
- Regressao adicional: Besta, geometria hash **e5e994b174f721708382ca604dbd21ab027e9b727050b2ce94508728937dc7e7** igual antes/depois; cobertura 28.195/14.820/5.157 intacta; tempo Blender 2,32 -> 2,93 s. Caprileo, geometria hash **37cfd1756c53a2a819cae6b94cbd2b80a099fd4dde2ed90cfb1a44fefaa0c114** igual; cobertura 30.967/9.056/4.164 intacta; 2,27 -> 2,83 s. Apenas nao-regressao de geometria/cobertura nesses dois: nao submetidos aqui a novo aceite artistico.
- **Suite completa: 300 executados, 0 falhas, 0 erros, 1 skip, 36,132 s** (`../evidencias/t2/suite.log`). O skip continua sendo pacote MCP ausente no interpretador, como na baseline. 4 testes novos, nenhum teste antigo removido.

### Autoauditoria adversarial e veredito separado

- Tentei refutar a correcao: o bug reproduz em cor uniforme sem silhueta complicada; primarias 0/1 do teste antigo nao o detectam; o teste novo reprova o codigo antigo; fonte GLB nao sofre dupla conversao; posicoes/normais/UV/indices e cobertura permanecem identicos; duas saidas novas sao byte-identicas; melhoria nas tres ROIs, com metodo e limites declarados.
- **Mecanismo C-COR01: corrigido e testado.** **Qualidade final: REPROVADA na autoauditoria visual**, ainda rascunho. Vi os renders antes/depois e a referencia: o clareamento indevido cai e cores recuperam contraste, mas rosto permanece ilegivel, pelo/armadura seguem fragmentados e a geometria nao coincide com a arte. Nao removi o rotulo rascunho. D1 permanece aberta. A melhora e mensuravel, mas nao tira o modelo do nivel rascunho.
- Previews locais (arte privada, fora do git): `../evidencias/t2/comparacao_frente.png`, `comparacao_regioes.png`, `comparacao_8_angulos.png`, e os 16 frames em `flat_antes/flat_depois/`. Scripts reproduziveis em `testes/codex/`; insumos/hash em `entradas.json`; metricas em `metricas_cor.json`; contraprova em `contraprova/`; todos os GLBs antes/depois preservados.
- COR-08: `git ls-remote origin refs/heads/main` ainda retornou **0e8746e355a6e55ed6ba9263e7574ab2bad00296** nesta checagem. Nao ha fechamento novo publicado para auditar. Nao toquei no codigo local em voo da principal.

- Manifesto de evidencia Entrega 2: `../evidencias/manifesto_entrega2.json`, 162 arquivos, SHA-256 **5efb8257f40a8ba9fda210821415cc10eea64d95e1ec02b95b4019c84f6fa2be**. PNG/GLB confirmados como ignorados; nenhuma arte ou log adicionado ao repo publico.

## Frente 3 — C-GUARD01, defesa da cor com provas adversariais

- Plano relido: T2/D-T2 existentes; COR-08 permanece trabalho da principal. Esta tranche so protege a validade da transferencia/COLOR_0, sem mudar alinhamento, pintar novas regioes ou duplicar o bake COR-08.
- **Antes (medido):** a guarda aceitou `[NaN]` e `[-0,1]` como distancias validas; um array numpy com varios elementos podia levantar erro de truth-value. O verificador aceitou dois primitivos com POSITION 3/3 e COLOR_0 2/4 (as somas empatavam em 6), indice -1 e indice booleano True; arquivo truncado levantava excecao de struct. Evidencias congeladas `../evidencias/guardas/antes.json` e fixtures sinteticas; casos numericos em `../evidencias/dt2/resultado.json`.
- **Correcao:** distancias devem ser vetor 1D, numericas, finitas e nao negativas; razoes devem ser numericas e finitas, alem das guardas anteriores. Recusa devolve motivo e metricas sem NaN. O verificador foi extraido para `oficina3d/cor/validacao_vertice.py`, importado pelo script Blender: cabecalho/JSON validos, indices inteiros nao booleanos/nao negativos, contagem positiva e igual POR PRIMITIVO, tipo de cor permitido/normalizado, material realmente referenciado. GLB quebrado retorna `ok=False`.
- **Depois (medido):** os 3 falsos positivos de GLB acima recusados; 1 truncado deixa de levantar e e recusado; controle valido continua aceito. NaN e negativo recusados; controle numerico legitimo aceito. Todos os JSONs de resultado serializam com `allow_nan=False`. Dez testes novos cobrem tambem multiplos meshes, mesh vazio, material invalido, contagens zero/negativas/booleanas, cor inteira normalizada, infinito, tipo nao numerico e numpy/gerador.
- **Nao-regressao real:** Orc/Besta/Caprileo corrigidos aprovados pelo verificador (COLOR_0/POSITION 65.469/65.469; 48.299/48.299; 44.293/44.293). Tempos observados de verificacao **0,291 / 0,216 / 0,191 ms**, sem pretensao de benchmark robusto. Reexecucao inteira do passo Orc apos endurecimento manteve SHA **eed4cdf74205a692f4659622ebdcf3b38bc53477345a3526e71b2149c1534111**, tempo Blender 3,15 s. Nenhuma mudanca visual desta tranche.
- **Suite final: 310 executados, 0 falhas, 0 erros, 1 skip, 30,967 s** (309 passaram; mesmo skip MCP). Evidencias `../evidencias/guardas/depois.json`, `suite.log`, `orc_reexecucao/`. 296 da base + 4 colorimetricos + 10 adversariais; nenhum teste original removido.
- **Autoauditoria adversarial:** controle positivo e arquivos reais ao lado dos ataques; igualdade de somas deixa de enganar; indices Python negativos/bool deixam de valer como indices glTF; falsos dados numericos nao passam pelas comparacoes com NaN. Artefato Orc identico prova que o endurecimento nao altera a pintura legitima. Limite explicito: verificador cobre estrutura JSON de cor, NAO offsets/payload binario, todas as extensoes ou validacao Khronos completa; guarda de alinhamento continua sem provar identidade do personagem. Sem alegacao de defeito desses tipos ocorrido em jobs reais da principal: sao falhas demonstradas da defesa em profundidade.
- Higiene dos executores: reexecucao do auditor nao substitui insumo congelado se o hash da fonte mudar; Gate 0 agora sai com exit 1 quando o resultado reprova. Arte mantida fora do repo, nenhuma tarefa agendada criada, nenhum job pesado de GPU lancado. Leitura da principal limitada aos arquivos/ambientes/fontes necessarios.

## Fechamento desta rodada e proximos passos

Entregas 0/1 registradas e publicadas; Entrega 2 trouxe auditoria independente, correcao colorimetrica e prova antes/depois. Frente 3 acrescentou guardas provadas. **O objetivo visual de sair do rascunho NAO foi atingido:** D1/rosto/alinhamento ainda abertos; melhoria de cor nao e cor final aprovada. T3 sem inferencia porque Gate 0 falhou, conforme roteiro.

COR-08 ainda nao publicada: ultima consulta `git ls-remote origin refs/heads/main` retornou `0e8746e355a6e55ed6ba9263e7574ab2bad00296`. Auditoria de seu fechamento fica pendente ate existir commit/artefatos publicados. Nao há monitor automatico nem servico Codex instalado. Proxima tranche: trazer esse fechamento para a branch, reproduzir as mesmas reguas e avaliar a composicao com C-COR01, mantendo os vereditos visual/mecanismo separados. Espaco ocupado pelo ambiente Paint preservado para reproducao; eventual arquivamento fora da copia nao foi feito por causa da regra de isolamento desta linha.

- Manifesto final Frente 3: `../evidencias/manifesto_frente3.json`, SHA-256 **48451cf4ab59af2fa1b6837ed97720820c014878adc1f44d36e05a83e599b00a**.
