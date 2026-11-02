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
## Rodada A–E — retomada em 2026-11-01

Base preservada: 53e845c, mesma branch codex/melhoria-paralela. Entregas anteriores nao refeitas. Plano local relido (ESTADO_ATUAL, DECISOES, ESTUDO_MELHORIAS, APRENDIZADO_E_FLUXO e estudos T3/T7/verificacao). Remote main agora aponta 6d93280; isso sozinho nao foi tratado como liberacao dos quatro arquivos reservados. Sem merge nesta rodada. Hashes desses quatro congelados em frente_b/resultado.json e conferidos apos a implementacao.

GPU: arquivo de trava principal presente; nenhum trabalho pesado de GPU executado. Provas desta rodada em CPU, Cycles CPU com 4 threads, ambientes e temporarios na copia. Nenhuma escrita na principal. Os modelos da bateria de qualidade tinham sido arquivados: localizados pelo arquivamento.json e COPIADOS do arquivo para evidencias/frente_b/entradas, com SHA conferido; nao foi necessario gerar forma nem refazer refino.

## Frente B — C-COR02, amostragem bilinear e curva de qualidade

Regua congelada da Entrega 2: mesma referencia frontal, bbox [117,101,523,699], mesmas ROIs rosto/peito/pernas e mesmos 7.369/15.637/21.767 pixels. Emission, Cycles CPU, Standard, exposicao 0, gamma 1, 640x800. Nao retunei alinhamento, ROI ou mascara para melhorar o numero. Pixels fora da silhueta candidata continuam na metrica; Lendario perde 52 pixels no rosto e 12 nas pernas, explicitamente contados. Scripts: frente_b.py, variantes_vertice_blender.py, metricas_frentes.py, validar_frente_b.py.

| Nivel real | Vertices Blender | Triangulos | Rosto seco DeltaE / SSIM | Rosto bilinear DeltaE / SSIM | Cor CPU seco / bilinear (s) |
|---|---:|---:|---:|---:|---:|
| Prata | 65.274 | 49.750 | 17,100706 / 0,137458 | 17,093655 / 0,145694 | 2,18 / 2,20 |
| Ouro | 142.019 | 149.250 | 14,572806 / 0,267354 | 14,249079 / 0,269898 | 4,56 / 4,66 |
| Lendario | 371.199 | 497.500 | 18,537382 / 0,056966 | 18,259641 / 0,063245 | 12,89 / 13,60 |

- **Curva erro x nivel nao monotona:** Ouro vence nesta prova. Os perfis tambem mudam octree/motor/forma: nao atribuo toda a diferenca exclusivamente a densidade. Comparacao causal da amostragem e DENTRO de cada nivel, com geometria identica. Nao alterei o perfil padrao do app para Ouro.
- **Meta numerica atingida:** Prata bilinear 17,093655 < 17,10, mas ganho de apenas 0,007051 (0,041%) nao resolve nitidez. Ouro bilinear 14,249079, ganho de 0,323727 sobre Ouro seco e 2,851627 sobre a baseline Prata; este ultimo inclui mudanca de geometria/perfil.
- Bilinear melhora as tres ROIs em todos os niveis. Ouro peito: DeltaE 12,154360 -> 11,931728, SSIM 0,380232 -> 0,388779; pernas: 11,025661 -> 10,688905, SSIM 0,328102 -> 0,341240. Prata peito 14,864229 -> 14,731746; pernas 13,170665 -> 12,958736.
- **Facing 0,5 / 1 / 1,5 / 2:** todos produziram o MESMO SHA e os mesmos erros (17,100706 no rosto Prata seco). A selecao e argmax com limiar aplicado antes: potencia positiva preserva o vencedor e o desempate. Resultado negativo medido, sem parametro placebo no app. Mantida selecao existente; nao introduzi mescla de vistas.
- Implementacao: bilinear em LUZ LINEAR apos C-COR01; centros em i+0,5; vizinhos fora da mascara excluidos e pesos renormalizados para evitar halo do fundo. Default bilinear no T2, controle seco explicito disponivel na funcao/pedido Blender. Relatorio declara amostragem. Nenhuma alteracao de facing, visibilidade, alinhamento, propagacao, forma ou rotulo rascunho.
- **Producao real sem monkeypatch:** Prata e Ouro identicos aos experimentos por SHA; Prata repetido duas vezes, ambos 44d6d066e136bcb0048f83a0f8a001048a1120a177a3a66496343630de56ad1e, 3.180.412 bytes, 2,24 s cada. Ouro 0b6bfdbc43399580420921566f0d4e9148144a1b39aca0dab1e24caade0eac7a, 8.053.592 bytes, 4,59 s. Hash independente de posicoes/normais/UV/indices inalterado por nivel. Cobertura inalterada por nivel, inclusive vertices sem cor. Tempos sao observacoes locais, nao benchmark estatistico nem ganho de velocidade.
- Testes novos (test_cor_amostragem.py): centros/meio de gradiente linear, renormalizacao com fundo hostil, bordas/um pixel e caminho real de amostrar_vertices com controle seco. **Suite completa: 314 executados, 0 falhas, 0 erros, 1 skip; 26,767 s.** O skip MCP e o mesmo da baseline.
- **APR-02:** tentei reprovar por mascara mudada, selecao diferente, falso ganho de expoente, mudanca de geometria, artefato de teste distinto do app e custo omitido; guardas/provas acima passam. Limite: um personagem, tres perfis; ganho Prata muito pequeno. Inspecao da folha antes_depois.png: Ouro recupera separacao de boca/olhos, mas continua com rosto deformado e ruido generalizado na armadura. **Mecanismo bilinear aprovado pelos testes; qualidade visual final NAO aprovada, continua rascunho, depende do olho do Mestre.** Nao alego rosto nitido/fidelidade resolvida.
- Evidencias privadas: ../evidencias/frente_b/metricas.json, resultado.json, producao.json, suite.log, antes_depois.png, comparacao.png e oito vistas em producao_ouro/flat. Manifesto: 112 arquivos, SHA-256 1a7ff9e38fe4fd174c2058706aa6b8c25ccf5923f0bdd2d772144de1b822c44e. Entradas/GLBs/frames fora do git.
- Intercorrencia de ferramenta durante construcao: um script auxiliar de edicao terminou com NameError (ast ausente) ANTES de alterar os arquivos do app; corrigido import e aplicado patch uma unica vez, seguido da suite e prova de producao. Nenhuma medicao baseada nessa execucao falha.
## Frente A — auditoria somente leitura da COR-05

**Veredito medido: o GLB T1/COR-05 NAO repete C-COR01.** A textura embutida preserva os bytes sRGB do rasterizador, como exige o caminho de textura; decodificar a fonte e continuar gravando a mesma imagem byte introduziria escurecimento indevido. Ha outro defeito: o PNG externo passa por AgX e diverge do albedo embutido.

- Mesmos artefatos COR-05, copiados com SHA: textura ebd744a9fe1bd0fb1b73334efb1eacbb0b147e4f9b2ff714aed5a2c213d2139d; modelo 0f8385380b22f86894355e6e944fc74ce910ef3a3b60d56ef341bfb57e9bf48c. Duas reproducoes instrumentadas apenas em memoria: textura E GLB byte-identicos aos originais (22,84 / 23,56 s no Blender). Nenhum arquivo de producao T1 editado.
- Raster capturado antes de gravacao; proveniencia por texel (vista vencedora e pixel-fonte), PNG embutido extraido diretamente do bufferView do GLB, decodificacao independente com Pillow. Todos os 1.048.576 texels embutidos = arredondamento dos bytes do raster, erro maximo 0. PNG externo difere por ate 69 niveis/canal.
- ROIs frontais normalizadas iguais as da Entrega 2, aqui aplicadas aos pixels-FONTE da referencia; mede preservacao de tom, nao correspondencia semantica da superficie. Rosto: **1.559 texels**, DeltaE2000 medio fonte->embutida **0**, fonte->PNG externo **2,872481**, erro byte max 59. Peito/pele aproximada: **1.800 texels**, DeltaE **0 / 2,700298**, erro byte max 58. Erro float raster vs fonte <=0,000019 niveis. ROI pernas sem texels cuja fonte vencedora e a frente nessa faixa: NAO inventado numero nem substituida a ROI. As regioes incluem roupa/cabelo; nao sao segmentacao semantica de pele.
- Sonda isolada do MESMO caminho de escrita no Blender 5.2.3: imagem byte sRGB, entrada (137,103,58), view default AgX. save_render default -> **(136,99,52)**; save_render Standard -> **(137,103,58)**; save -> **(137,103,58)**. Isto separa transformacao de visualizacao de erro sRGB declarado como COLOR_0 linear. O ultimo era o defeito T2, nao o desta textura.
- Render flat do GLB original, Emission/Cycles CPU/Standard, mesma regua FIXA B (7.369/15.637/21.767 pixels): rosto DeltaE **24,853960**, SSIM **0,030589**; peito **28,486167 / 0,043030**; pernas **22,323554 / 0,058203**. Numeros de render incluem alinhamento/UV/dilatacao/interpolacao, por isso NAO se confundem com os zeros de preservacao de texels. Sem Workbench nesta prova.

**Achado adicional somente leitura (nao aplicar durante COR-08):** projetar() subtrai centro; rasterizar_textura() calcula qx/qy de p3d absoluto. Na malha real centro=[~-1,49e-8,0,0,5], as duas formulas deslocam y da imagem-fonte em **-429,496684 px** apos a afinidade. Medido independentemente no Blender e salvo em centro/resultado_centro.json. Proveniencia de todas as vistas termina em y=511; pernas da referencia ficam sem amostras frontais. A previa Emission mostra o rosto na regiao inferior do corpo. Isso explica uma inconsistencia espacial concreta, mas nao medi o ganho de uma correcao e nao afirmo que esgote a D1. Encaminhar para conferir sobre COR-08 publicada; nao sobrescrever o alinhamento novo.

**Esboco de patch para revisao apos COR-08:** (1) albedo byte deve ser gravado com image.save() e colorspace sRGB explicito, preservando os mesmos pixels no PNG e no GLB; nao aplicar C-COR01 cegamente ao bake; (2) unificar projecao dos pontos baricentricos com projetar(...,centro,...) ou subtrair centro antes dos produtos escalares, preservando a afinidade/otimizacao nova; (3) testes com tons intermediarios, igualdade PNG externo x embutido, independencia de view transform e invariancia de translacao da malha+centro. Se futuramente houver mistura, trabalhar linear internamente e codificar sRGB UMA vez na saida. Patch NAO aplicado aos quatro arquivos reservados.

**APR-02:** reprovar hipoteses por artefato real, nao por leitura isolada de img.pixels. Reproduzi SHAs originais, distingui PNG externo/embutido e medicao de tom/medicao espacial, conferi fonte por texel, sonda uniforme independente e render Emission. Corrigido erro de sintaxe no instrumento antes da execucao valida; primeira tentativa de agregacao recusou ROI sem amostras, corrigida para declarar n=0, sem mudar ROI. **Mecanismo de preservacao sRGB do GLB confirmado; PNG externo inconsistente. Qualidade visual REPROVADA na autoauditoria**, confete e rosto fora do lugar; nao aprovada pelo Mestre.

Evidencias: ../evidencias/frente_a/{entradas.json,texels.json,metricas_flat.json,embutida.png,flat/frente.png,sonda/medicao.json,centro/resultado_centro.json}; dois bakes em reproducao/ e proveniencia/. Suite completa do estado atual: **316 executados, 0 falhas, 0 erros, 1 skip; 26,678 s**, log em ../evidencias/frente_c/suite.log (inclui os dois testes da Frente C, publicados no commit seguinte). Nenhuma alteracao de projecao.py, _blender_cor.py, passo.py ou test_cor.py; hashes conferidos.
## Frente C — contagens cruzadas por primitivo, complemento adversarial

A nota D-T2-4 da Entrega 2 foi superada pelo commit **53e845c**, anterior a esta nova ordem: a producao JA compara POSITION/COLOR_0 por primitivo. Nao reescrevi a guarda nem aleguei corrigir duas vezes o mesmo defeito. Acrescentei os ataques explicitamente pedidos.

- Controle desigual valido: partes 3/3 e 5/5 aceitas; reordenar primitivos inteiros permanece valido.
- Sabotagem 1: trocar referencias COLOR_0 entre essas partes -> 3/5 e 5/3; soma 8=8, **recusada**, dois primitivos sem cor valida.
- Sabotagem 2: deslocar contagens para COLOR_0 4/4 com POSITION 3/5; soma 8=8, **recusada**, dois primitivos invalidos. Complementa o 3/3 vs 2/4 ja existente.
- Contraprova automatica no verificador de **7511a68**, antes de C-GUARD01: os mesmos dois testes produzem **2 falhas de assercao esperadas, 0 erros de infraestrutura**; os controles positivos passam antes das sabotagens. No codigo atual ambos passam.
- **Suite completa: 316 executados, 0 falhas, 0 erros, 1 skip, 26,678 s**. Testes em test_cor_guardas.py; contraprova reproduzivel em testes/codex/contraprova_primitivos.py; logs em ../evidencias/frente_c/.
- **APR-02:** igualdade global de somas nao basta; ordem legitima nao deve ser recusada. Trocar cores entre partes com contagens IGUAIS e estruturalmente valido e NAO e detectavel por contagem: esta guarda nao promete identidade semantica nem validar payload binario. Esse limite permanece explicito. **Mecanismo validado; nenhuma mudanca visual nesta frente.** Qualidade artistica nao julgada por estes testes.
## Frente D — PRONTO PARA INTEGRAR

Pacote de integracao C-COR01/C-GUARD01 publicado na branch codex/melhoria-paralela. Integracao na principal pertence ao Muse, apos liberar a COR-08; nada aplicado na arvore oficial por esta linha.

### Ordem e escopo exato

1. **7511a682a7160144bc24b8da0d8e16fe2763c634** — C-COR01, decodifica imagens byte sRGB para COLOR_0 linear.
   - Producao: oficina3d/cor/vertice.py e oficina3d/cor/_blender_vertice.py.
   - Testes: testes/test_cor_colorimetria.py.
   - Executores em testes/codex/: auditar_dt2.py, auditar_t2.py, contraprova_gamma.py, glb_evidencia.py, medir_cor.py, probe_gamma_blender.py, render_flat_blender.py, reproduzir_outros.py.
   - Documentacao: docs/APRENDIZADO_E_FLUXO.md, DECISOES.md, ESTADO_ATUAL.md, REGISTRO-CODEX.md.
2. **53e845c470a31322705d02f8c791960fe7fb3bd2** — C-GUARD01, defesa numerica e validacao por primitivo. Aplicar DEPOIS do anterior: extrai o verificador de _blender_vertice e depende da versao desse arquivo.
   - Producao: oficina3d/cor/vertice.py, _blender_vertice.py e novo validacao_vertice.py.
   - Testes: testes/test_cor_guardas.py.
   - Executores: testes/codex/auditar_t2.py e gate0_paint.py.
   - Documentacao: os mesmos quatro documentos acima.

Sequencia sugerida na copia de integracao do Muse: cherry-pick 7511a68 e depois 53e845c; executar suite completa com OFICINA3D_BASE/JOBS e TEMP/TMP apontados para essa copia. Ambos sao posteriores a base main 0e8746e; 7511a68 tem como pai a entrega documental Gate 0 cbca11f. O patch do app nao depende do Gate 0, mas os hunks documentais/pequeno ajuste do script de Gate 0 em 53e845c podem exigir contexto das entregas anteriores. Se integrar so o codigo, levar tambem os testes e o resumo de prova; nao aplicar cegamente hunks de ESTADO_ATUAL sobre o estado novo da principal.

### Contratos e provas que precisam sobreviver

- C-COR01: so imagens byte sao decodificadas; alpha/mascara calculados ANTES, imagens float e forma glTF ja linear preservadas; nao converter cor duas vezes. _blender_vertice ganhou guarda __main__ para ser importavel pelos testes.
- Testes de curva/oliva conhecido, PNG real -> GLB real e forma GLB sem segunda conversao. Contraprova: teste PNG falha numericamente no exportador antigo. Atol 1/255 no teste de transferencia GLB cobre quantizacao BYTE_COLOR do importador, nao autoriza tolerancia de gamma.
- Baseline -> C-COR01, MESMO Orc Prata: rosto DeltaE **28,377653 -> 17,100706**, SSIM **0,103590 -> 0,137458**; peito DeltaE **27,830549 -> 14,864229**; pernas **26,789014 -> 13,170665**. Geometria/cobertura/3.180.412 bytes intactos; SHA corrigido **eed4cdf74205a692f4659622ebdcf3b38bc53477345a3526e71b2149c1534111** repetido duas vezes.
- Suite apos C-COR01: 300, zero falhas/erros, um skip; apos C-GUARD01: 310, zero falhas/erros, um skip. C-GUARD01 reexecutou o Orc com MESMO SHA, recusa somas compensadas/indices invalidos/NaN sem alterar pintura legitima. Sua extracao exige levar validacao_vertice.py junto.
- Custo C-COR01 observado +0,2–0,3 s/Orc; C-GUARD01 verificador ~0,2–0,3 ms/GLB (observacoes locais, nao benchmark).
- **Dependencias posteriores opcionais:** C-COR02 **4836e6f** altera o default para bilinear; por isso seus SHAs/metricas novos NAO devem ser exigidos ao testar somente os dois commits deste pacote. **80c48d0** acrescenta os dois ataques cruzados da Frente C, sem mudar producao. Auditoria A **2cc5ff9** acrescenta scripts/documentacao; nenhum patch de projecao foi aplicado.
- **Aviso concreto da A:** nao estender a conversao de C-COR01 a _blender_cor por analogia. O GLB T1 ja preserva sRGB; o PNG externo usa AgX e ha discordancia espacial no centro. Tratar os dois achados separadamente apos COR-08.
- Os quatro arquivos reservados NAO constam do diff desses dois commits. Nenhuma dependencia Python nova do app: numpy/bpy ja existentes. Arte, pesos, ambientes e logs nao acompanham o commit; executores de prova pressupõem as entradas privadas documentadas, testes unitarios geram suas proprias fixtures.

**APR-02:** lista conferida contra git show --stat dos SHAs completos; ordem, dependencia documental do pai, arquivo novo obrigatorio e mudanca posterior de default explicitados. Nao fiz cherry-pick na principal e nao prometo ausencia de conflitos com commits da COR-08 ainda nao integrados nesta copia. Veredito: pacote de codigo/testes/provas pronto para revisao/integracao; qualidade visual continua NAO aprovada. Suite atual segue **316 / 0 falhas / 0 erros / 1 skip**, nenhuma mudanca executavel nesta entrega documental.
## Frente E — Gate 0 Paint, tentativa 2: APROVADO (retomada noturna)

Tentativa 1 preservada. Toolchain em terminal novo vcvars64: **MSVC 14.44.35207 / cl 19.44.35229 / nvcc 12.4.131**. Venv proprio Python 3.10.22, torch 2.5.1+cu124, setuptools 84.2.1, wheel 0.48.0, pybind11 3.1.0 e ninja 1.13.2. CUDA_HOME/PATH alterados so no processo. Comando em ambas as extensoes da copia: python -B setup.py build_ext --inplace, TORCH_CUDA_ARCH_LIST=8.9, MAX_JOBS=2.

| Extensao | Build | Tempo | Nativo | Bytes | SHA-256 |
|---|---|---:|---|---:|---|
| custom_rasterizer | exit 0 | 58,1232 s | custom_rasterizer_kernel.cp310-win_amd64.pyd | 294.400 | f5f480989015c42f9b05545fabb5bf2371b57554d3150f4926d18439394bfb7b |
| differentiable_renderer | exit 0 | 3,2791 s | mesh_processor.cp310-win_amd64.pyd | 165.376 | 5e265ffb33a66b161ba41e661cc7166449451b7f19824b7142e57369557004c3 |

- Falhas intermediarias preservadas: pacote sem Pillow, kernel importado antes de torch (DLL nao localizada), depois cv2 ausente. Resolvidas no ambiente proprio; NAO eram falhas de compilacao. Imports completos e ambos nativos comprovados por EXTENSION_SUFFIXES em resultado_final.json, sem aceitar fallback .py.
- Dependencias copiadas fisicamente do ambiente fonte somente-leitura, hashes por arquivo: Pillow 10.4.0, pygltflib 1.16.5, scipy 1.15.3, OpenCV headless 5.0.0.93 e transitivas. Duas sondas pip ausente registradas; ensurepip instalou pip 23.0.1 somente no venv proprio. Sem site-packages compartilhado/symlinks. Depois foram copiadas as dependencias da pipeline: diffusers 0.39.0, transformers 4.49.0, torchvision 0.20.1+cu124, mmgp 3.2.7, accelerate 1.15.0, xatlas 0.0.11 e trimesh 5.2.0; torch preservado.
- Preflight da pipeline completa + mmgp, offline/CPU: passou em **26,8255 s**. Suite inteira: **316 executados, 0 falhas, 0 erros, 1 skip, 27,238 s**.
- APR-02: distinguir build/import/native/inferencia; resultado inicial nao apagado, resultado_final.json reconcilia os builds e imports finais. Executor agora enumera tentativa, recusa sobrescrever prova, importa torch antes da extensao, persiste timeout/OSError. **Gate 0 aprovado; spike visual ainda em curso.**
- Evidencias: ../evidencias/gate0_tentativa2/{resultado.json,resultado_final.json,suite.log,*_build.log,*_native*.log,dependencias_copiadas.json,dependencias_opencv.json,dependencias_pipeline.json}. Erro de sintaxe de uma chamada de ferramenta documental nao executou shell; depois a revisao automatica negou execucao por limite de uso. Nenhuma tentativa de alterar limite/plano; apos nova ordem do usuario a revisao voltou a aprovar normalmente. Registro/publicacao retomados aqui.

### Pesos, trava e primeiras cargas (ainda nao sao pintura)

Inventario ANTES do download em ../evidencias/paint_spike/inventario_pesos.json: repo tencent/Hunyuan3D-2, revision **9cd649ba6913f7a852e3286bad86bfa9a2d83dcf**. Pastas Paint+Delight completas: **13.504.594.413 bytes**; selecao inicial sem binarios duplicados: **9.506.772.449 bytes**, disco livre antes **21.732.290.560 bytes**. Download concluido com hashes LFS conferidos, livre apos **11.749.711.872 bytes**. Destino exclusivo modelos/paint_spike. Reserva de 6 GiB conferida por bloco. Erro inicial de API tqdm_class preservado em download_erro_argumento.*; streaming HTTP/Range corrigido sem perder registro.

**Autoauditoria encontrou erro meu na selecao:** o UNet customizado do fork faz torch.load do nome .bin fixo; safetensors nao e substituto automatico neste carregador. Segunda carga falhou por esse arquivo ausente. Inventario complementar ANTES do novo download: **3.663.114.747 bytes**, livre observado **12.607.848.448 bytes**, destino igual; detalhes em download_bin.json. Nao estimei tamanho nem escondi essa falha.

Trava: existencia de gpu.lock vazio NAO prova ocupacao. Sonda pelo byte **1<<30** do protocolo Windows, handle **rb**, adquiriu/soltou sem escrever na principal. Livre naquele instante, GPU 2%, 1.013/8.188 MiB. Launcher mantem trava exclusiva durante todo o processo e rejeita uso externo >=30% ou VRAM inicial >=3.000 MiB. Registro local, sem escrever dono na principal. RAM fisica medida **34.178.985.984 bytes**, disponivel **17.729.679.360 bytes**, swap **14.950.580.224 bytes**.

Codigo real do fork: Delight seed **42**, **50 passos**; Paint seed **0**, **30 passos**. Perfil 5, VAE slicing e budgets 2200 conforme gradio_app. Sem alterar arquitetura/passos para caber artificialmente.

| Tentativa de carga | Parede supervisionada | Pico VRAM total | Pico RAM processo | Resultado |
|---|---:|---:|---:|---|
| perfil5_A | 12,1149 s | 1.209 MiB | 2.913.501.184 bytes | Diffusers exige opt-in para custom_pipeline local |
| perfil5_A_local | 16,1629 s | 1.205 MiB | 10.427.797.504 bytes | UNet .bin ausente |

Primeiro erro resolvido com opt-in RESTRITO aos caminhos locais inspecionados e hashados; carregamento offline, sem confiar genericamente em repos remotos. Segundo erro em resolucao por download complementar. Ambos falharam em carregar_modelos, **nao chegaram a pintura**; zero OOM observado nessas cargas nao comprova capacidade da inferencia. Triangulos/GLB/textura de saida, tempo de pintura e SSIM/DeltaE: **nao medidos** ate existir saida. Regua do spike permanece <=8.188 MB, <=45 min, zero OOM e qualidade frontal nao pior que T1. Proximo adendo registra o resultado final.

## Nova ordem noturna recebida — fila preservada

COR-08/S2 publicadas, congelamento dos quatro arquivos oficialmente cancelado pelo Mestre. Depois de fechar E: merge da main publicada (fetch identificou b6074f3, descendente dos commits informados), reproduzir IoUs/cobertura COR-08, auditar centro no bake publicado, compor C-COR01/C-COR02 sobre a base nova e atualizar PRONTO PARA INTEGRAR v2. Leitura preliminar encontrou a subtracao de centro na COR-08; isso NAO substitui a medicao ainda pendente. Arvore principal continua intocada.
