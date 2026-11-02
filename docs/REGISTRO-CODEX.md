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

## Frente E — fechamento do spike (02/11/2026)

Gate 0 aprovado; inferencia real perfil 5 concluida, mas configuracao ARQUIVADA por piorar DeltaE do rosto contra T1 COR-08/S2. Nao significa impossibilidade de qualquer Paint futuro. A baseline originalmente COR-05 e superada; a comparacao adicional com a principal publicada responde a nova ordem de aperfeicoar seu resultado atual, sem ocultar a mudanca de baseline.

| Regiao fixa | COR-05 DeltaE / SSIM | COR-08/S2 DeltaE / SSIM | Paint DeltaE / SSIM |
|---|---|---|---|
| Rosto | 24,853960 / 0,030589 | 21,811685 / 0,000844 | 22,241797 / 0,045126 |
| Peito | 28,486167 / 0,043030 | 21,752279 / 0,043063 | 18,471548 / 0,082708 |
| Pernas | 22,323554 / 0,058203 | 17,017702 / 0,067412 | 15,260030 / 0,117669 |

Painel medido perfil5_A_bin: parede supervisionada 141,285151 s; worker 138,689036 s, carga 20,738958 s e pintura 115,595942 s. Pico amostrado VRAM TOTAL 3.306 MiB (inicial 1.106), RSS arvore do processo 15.863.304.192 bytes, 140 amostras aproximadamente 1 Hz. Nao e pico instantaneo absoluto nem VRAM exclusiva do processo. Exit 0, zero OOM observado. Saida 49.750 triangulos, 71.195 vertices exportados; GLB 6.687.892 bytes, SHA 09af5fad2d143cdccb55e9d359c3287311b1d36c57f7f955a1d218373edaf4e4; PNG 4.665.659 bytes, SHA f4ba352d08b42187109b752c1c24b78aca06e0bcc8e71061edc8f41bd43d8c15.

Pesos finais 28 arquivos / 9.507.250.724 bytes. Bin complementar verificado; duplicata safetensors nao usada removida apenas apos verificar caminho e hash (3.662.636.472 bytes). Venv 5.092.110.048 bytes, runtime 61.232.289, motor 260.796.374. Downloader corrigido para selecionar o .bin exigido pelo UNet desde o inicio; download_verificado.json reconfere arquivos locais, launcher verifica tamanho e SHA antes de adquirir GPU. Historicos anteriores preservados. Aviso de classe UNet de modulo customizado diferente emitido pelo diffusers: inferencia concluiu, compatibilidade geral nao comprovada.

APR-02: alfa T1/Paint exatamente identico, ROIs/mascara congeladas, nenhum ajuste para ganhar nota. T1 comparador copiado da prova COR-08, SHA a8e793b267db27c2a06669dbb925c91b8863a99ec4f43f558c880a1d10a09b9a. Prova independente de trava durante inferencia recusou segundo handle; gpu.lock principal permaneceu vazio, sem escrita. Oito angulos inspecionados em painel_8_angulos.png: Paint suaviza manchas mas descaracteriza rosto, cabelo e capa. SSIM por caixas fixas nao equivale a identidade visual. Rosto DeltaE piora 0,430112 contra COR-08, portanto nao promover. Determinismo em duas execucoes, perfil 4 e cobertura semantica: NAO MEDIDOS; nao continuar gasto de GPU apos quebrar a regua de qualidade atual. Mecanismo de compilacao/inferencia comprovado; qualidade visual final NAO aprovada pelo Mestre.

Suite integral 316 testes, 0 falhas, 0 erros, 1 skip, 42,162 s (CPU compartilhada com renders nesta observacao; nao benchmark). Evidencias privadas em ../evidencias/paint_spike/: supervisao/telemetria/resultado/metricas do perfil5_A_bin, comparacao_t1_atual.json, auditoria_final.json, prova_trava.json, painel_8_angulos.png, suite.log e manifestos de pesos. Arte e pesos fora do git.

## Integracao da base publicada — em verificacao

Merge de origin/main b6074f3 na branch paralela. Quatro conflitos documentais (APRENDIZADO_E_FLUXO, DECISOES, ERROS, ESTADO_ATUAL), nenhum de codigo/testes. Preservados ambos os lados; novas linhas de tabelas da principal antes das secoes Codex. Estado Codex antigo explicitamente historico, com adendo atual. Nao alterados fontes da principal nem seus arquivos privados. A0 da principal ja subtrai centro; veredito aguarda bake medido, nao leitura apenas.

### Base publicada reproduzida — merge verificado

Suite integral: **363 testes, 0 falhas, 0 erros, 1 skip MCP**, 44,702 s. Sao 343 da main mais 20 desta linha, nenhum removido. Bake de PRODUCAO (sem instrumentacao), com malha UV ancora e quatro imagens canonicas copiadas por hash: IoUs frente/costas/esquerda/direita **0,8177 / 0,7774 / 0,8065 / 0,7957**, identicos. Cobertura **420.713 / 845.063 = 49.78480894%**; a chamada 49,79% da tarefa e aproximacao, registrar contagens exatas (arredondamento decimal a duas casas = 49,78%). Preenchimento 3D 424.350 texels, 25.160 faces, zero sem fonte alcancavel, anel medio 3,18/max 21.

GLB SHA **a8e793b267db27c2a06669dbb925c91b8863a99ec4f43f558c880a1d10a09b9a**, PNG **e4056741a2d124947873fe50e1d547ce6a9d9f7a77cf2c465a9bf2bb8184fd93**: ambos reproduzem COR-08/S2. Bake 120,48 s, parede Blender 121,25 s; CPU concorrente nesta observacao, nao benchmark contra tempos historicos. 49.750 triangulos / 71.289 vertices Blender. RAM/VRAM deste bake CPU: nao medidas. Artefatos e manifestos em ../evidencias/cor08_composicao/producao e entradas.json.

APR-02 do merge: hashes e contagens remedidos dos artefatos, nao copiados do relatorio; dados canonicos COR-08 nao substituidos pelas vistas preproc do T2. Codigo de projecao, bake, passo e testes COR-08 identicos a origin/main; apenas os tres arquivos T2 diferem em producao. Conflitos documentais mantiveram os dois historicos; estado antigo rotulado como superado. Mecanismo de composicao passou; nenhum novo aceite visual. Auditoria de proveniencia/contraprova do centro segue em frente propria.

## Achado do centro — ENCERRADO: COR-08/A0 corrigiu (02/11/2026)

Veredito medido no bake publicado: o deslocamento NAO persiste. A0 corrige explicitamente a projecao dos pontos baricentricos; nao e apenas compensacao casual da A1. Nenhum patch adicional de centro aplicado. Comparacao controlada: mesmos inputs canonicos, UV, otimizacao A1, tamanho 2048, preenchimento A3 e save S2; contraprova remove SOMENTE a subtracao do centro em memoria, sem tocar producao.

| Medida | Contraprova sem A0 | COR-08/S2 de producao |
|---|---:|---:|
| Erro maximo das coordenadas contra projetar(), frente | 711,298456 px | 0 px |
| Costas / esquerda / direita | 698,551172 / 715,231225 / 715,256917 px | 0 / 0 / 0 px |
| Texels diretos / dominio UV | 167.568 / 845.063 (19.82905417%) | 420.713 / 845.063 (49,78480894%) |
| Fonte frontal, y minimo..maximo | 165..869 | 165..1581 |
| Maximo y fonte, costas/esquerda/direita | 882 / 869 / 871 | 1580 / 1584 / 1586 |
| Texels vindos da ROI frontal das pernas | 0 | 20.278 |
| Desses texels, na faixa inferior da malha | 0 | 20.278 |
| Fonte rosto aplicada na faixa inferior | 3.068 | 0 |
| Fonte peito aplicada na faixa inferior | 7.023 | 0 |
| Preenchimento 3D, anel medio / max | 20,49 / 84 | 3,18 / 21 |

Imagens CANONICAS desta prova: frente 1280x1820; a antiga prova COR-05 usava preproc 1024 e afinidade diferente. Por isso os 711 px atuais da contraprova nao contradizem os 429,496684 px historicos; nao comparar valores em pixels como se a resolucao fosse a mesma. Regioes-fonte normalizadas mantidas (.40,.07,.62,.21 rosto; .30,.26,.70,.43 peito; .25,.64,.86,.94 pernas). ROI pernas aqui [398,1121,1011,1568].

Faixa inferior = 35% inferiores da altura geometrica, reconstruida independentemente dos acessores GLB e UV; nao e segmentacao semantica das pernas e pode conter capa/equipamento. Todos os texels diretos tem posicao no mapa reconstruido (zero fora); nodes sem transformacao verificados. Total de texels com fonte frontal nessa faixa e 35.062 na contraprova contra 32.821 corrigidos: QUANTIDADE sozinha enganaria, porque antes vinha rosto/peito. A prova de recuperacao e a fonte correta chegando a faixa, nao simplesmente mais tinta.

Producao sem instrumentacao e instrumentada: GLB a8e793... e PNG e4056741... BYTE-IDENTICOS, comprovando que capturar proveniencia nao mudou o resultado. Erro coordenado maximo calculado para os pontos baricentricos visitados nas quatro vistas = 0, antes de clipping/arredondamento. Contraprova GLB bf98a7b1e4e5ec8ba5529bad733f3757fb1af4d2dca93643f6d7bb4fc67dc585. PNG externo vs PNG extraido do GLB corrigido: erro maximo RGB **0**, confirmando S2 no artefato novo. IoUs iguais nas tres execucoes: a A1 sozinha NAO detecta a regressao A0, mas proveniencia e cobertura detectam.

### Regua flat e autoauditoria adversarial (APR-02)

| Regiao | Sem A0 DeltaE / SSIM | COR-08/S2 DeltaE / SSIM |
|---|---|---|
| Rosto | 22,052280 / 0,058384 | 21,811685 / 0,000844 |
| Peito | 25,015092 / 0,077407 | 21,752279 / 0,043063 |
| Pernas | 23,808634 / 0,048014 | 17,017702 / 0,067412 |

Todos os DeltaEs melhoram; SSIM PIORA no rosto e peito apesar da correcao espacial obvia. Mantive os numeros negativos, nao mudei a regua. Painel Emission inspecionado: sem A0, rosto fica na parte inferior e topo escuro; com A0 volta ao lugar, mas persistem desencaixe/anatomia e costuras. A metrica pixel-a-pixel em caixas congeladas pode premiar borramento e punir detalhe deslocado: nao pode, sozinha, ranquear fidelidade global entre T1/T2/Paint nem aprovar identidade. Isto tambem limita a interpretacao das entregas anteriores; C-COR01 tem prova fisica independente de gamma, C-COR02 tem ganho pequeno de amostragem, nenhum promete fidelidade resolvida.

Instrumentacao exige ancoras unicas no codigo antes de substituir; contraprova deve falhar criterios de coordenada/pernas, controles positivos devem reproduzir SHA de producao. Instrumentado 122,51 s; contraprova 119,73 s; producao 120,48 s. Tempos concorrentes locais, nao ganho de desempenho. RAM/VRAM CPU nao medidas. Artefatos canonicos de producao 49.750 triangulos, GLB 5.978.716 bytes e PNG 3.097.592 bytes. Mecanismo A0/S2 confirmado; nenhuma nova aprovacao visual final. Achado de centro encerrado sem duplicar correcao da principal.

Evidencias: ../evidencias/cor08_composicao/auditoria_centro.json, metricas_composicao.json, painel_composicao.png, producao/, instrumentado/ e contraprova_absoluto/. Reproducao: testes/codex/reproduzir_cor08.py e medir_cor08.py; composicao T2 real: compor_t2_cor08.py. Executores e registro em git, entradas/GLBs/PNGs fora do git.

Fechamento da auditoria/composicao: suite integral repetida **363 testes, zero falhas/erros, 1 skip MCP, 41,849 s**, suite_final.log. Contraprovas e render concluidos, nenhum processo proprio pendente. Uma consulta intermediaria tentou nome de log cor.log inexistente; corrigida para blender_cor.log, sem efeito sobre execucoes.
Manifesto privado paint_spike/manifesto_fechamento.json: 58 arquivos, SHA-256 3cb0c1592c8030de22ebd8480437ac39336c9cc0563f209d9dcfbf7d21255f98.
Manifesto privado cor08_composicao/manifesto_fechamento.json: 71 arquivos, SHA-256 18ce3c6237e692625221452d5678a5d7140289ca01046e718efbd85fa74d4f4f.

## Frente D v2 — PRONTO PARA INTEGRAR

Substitui o pacote parcial da Frente D. Base testada: main b6074f3 (inclui COR-08 27704b1 e S2 22b9d5c), merge nesta linha 6083b89. Integracao na arvore oficial e decisao/execucao do Muse; nao realizada por esta linha.

### Ordem dos commits e arquivos

| Ordem | Commit | Producao | Testes | Dependencia |
|---|---|---|---|---|
| 1 | 7511a68 (C-COR01) | oficina3d/cor/vertice.py, _blender_vertice.py | testes/test_cor_colorimetria.py (4) | sRGB byte -> linear; sem converter forma GLB novamente |
| 2 | 53e845c (C-GUARD01) | vertice.py, _blender_vertice.py, NOVO validacao_vertice.py | testes/test_cor_guardas.py (10 originais) | extracao do verificador: levar modulo novo junto |
| 3 | 4836e6f (C-COR02) | vertice.py, _blender_vertice.py | testes/test_cor_amostragem.py (4) | requer C-COR01: bilinear precisa de amostras lineares |
| 4 | 80c48d0 (Frente C) | nenhum | test_cor_guardas.py (+2) | ataques ao verificador de C-GUARD01 |

C-COR01: curva/tons medios, PNG real -> GLB real, forma ja linear sem dupla conversao. C-GUARD01: indices invalidos, materiais/acessores malformados, multiplos meshes, contagens compensadas, NaN/inf/dados nao numericos e arrays/geradores. Frente C: troca de acessores entre primitivos 3/5, contagens deslocadas 4/4 versus 3/5, reordenacao legitima aceita. C-COR02: centro/meio de pixel linear, fundo mascarado renormalizado, bordas, imagem de um pixel, default bilinear/controle seco/caminho real.

Arquivos auxiliares/documentais acompanham cada commit: 7511a68 e 53e845c tocam APRENDIZADO_E_FLUXO, DECISOES, ESTADO_ATUAL e REGISTRO-CODEX, alem dos executores listados no D original. 4836e6f leva frente_b.py, metricas_frentes.py, validar_frente_b.py, variantes_vertice_blender.py e REGISTRO-CODEX. 80c48d0 leva contraprova_primitivos.py e REGISTRO-CODEX. Nenhum desses quatro commits altera projecao.py, _blender_cor.py, passo.py ou test_cor.py. Paint e auditoria A nao sao dependencias do codigo T2.

### Conflitos concretos e criterio de integracao

Merge completo da main nesta branch teve SOMENTE conflitos documentais: APRENDIZADO_E_FLUXO, DECISOES, ERROS e ESTADO_ATUAL. Codigo/testes foram combinados automaticamente. ERROS veio do historico Gate 0, nao dos quatro commits T2 acima. Cherry-pick seletivo pode pedir contexto em REGISTRO-CODEX (historico intermediario omitido) e no ajuste do gate0_paint.py de 53e845c; nao e dependencia funcional da cor. Nao substitua o estado atual da main por paragrafo historico Codex. Resolucao de referencia: preservar linhas novas da principal nas tabelas, manter adendos Codex e rotular estados antigos como superados. Nao foi ensaiado cherry-pick numa terceira arvore; o ensaio executado foi o merge completo 6083b89 com provas reais e suite.

Nao reintroduzir patch antigo de centro/PNG: A0 e S2 pertencem a principal e devem permanecer. C-COR01 nao deve ser aplicado ao albedo de textura T1 por analogia. Sem dependencias novas do app; instrumentos de medicao pressupõem bibliotecas/Blender e arte privada documentadas. Todos os testes unitarios geram fixtures. Arte/pesos/venvs nao acompanham git; check-ignore da imagem canonica confirmado.

### Antes/depois REEXECUTADO sobre COR-08/S2

Baseline executada com AMBOS os modulos T2 extraidos da main b6074f3, evitando contaminar a baseline com default bilinear desta branch. Controles C-COR01 seco e C-COR02 executados pelo caminho de producao atual; render Emission/Cycles CPU/Standard, mesma mascara/ROIs congeladas.

| Caso | Rosto DeltaE / SSIM | Peito DeltaE | Pernas DeltaE | Cor CPU (s) | GLB bytes |
|---|---|---|---|---|---|
| Main Prata | 28,377653 / 0,103590 | 27,830549 | 26,789014 | 1,87 | 3.180.412 |
| C-COR01 Prata seco | 17,100706 / 0,137458 | 14,864229 | 13,170665 | 2,02 | 3.180.412 |
| C-COR02 Prata bilinear | 17,093655 / 0,145694 | 14,731746 | 12,958736 | 2,04 | 3.180.412 |
| C-COR02 Ouro bilinear | 14,249079 / 0,269898 | 11,931728 | 10,688905 | 6,37 | 8.053.592 |

SHAs reproduzidos: main 949e3cf7009b8e23e63474fc395d45226acb2ec63342e2a419b3996b7c9c2f3a; C01 eed4cdf74205a692f4659622ebdcf3b38bc53477345a3526e71b2149c1534111; C02 Prata 44d6d066e136bcb0048f83a0f8a001048a1120a177a3a66496343630de56ad1e; C02 Ouro 0b6bfdbc43399580420921566f0d4e9148144a1b39aca0dab1e24caade0eac7a. Todos identicos as provas anteriores. Prata 49.750 triangulos/65.274 vertices Blender; Ouro 149.250/142.019. RAM/VRAM desses passos CPU: nao medidas. Tempos sao observacoes concorrentes, nao ganho de desempenho alegado.

Geometria Prata SHA c4bfc17342c982bd24c6a7b4a29da1f705373c8f9156aeab614135793cb553c7 identica nos tres controles. Cobertura identica: 31.033 vertices de vista, 22.661 propagados, 11.580 sem cor. Nao ocultar vertices sem cor nem comparar cobertura T2 em vertices com cobertura T1 em texels. T1 composto reproduz exatamente IoUs/cobertura/GLB/PNG de COR-08/S2 (secao do merge). Ganho entre niveis inclui mudanca de forma: Ouro nao e prova causal isolada de densidade. Ganho bilinear Prata segue pequeno, sem declarar rosto resolvido.

APR-02 v2: verificacao por hashes dos arquivos novos e reexecucao das fontes, mascara congelada, geometria/cobertura invariantes. Repetida contraprova das duas sabotagens contra 7511a68: duas falhas de assercao esperadas, nenhum erro de infraestrutura; codigo composto passa ambos na suite de 363. Limites continuam: guarda estrutural nao prova semantica de cores/payload binario; testes de gamma nao aprovam anatomia; parametro facing continua nao introduzido por ser placebo no argmax. Mecanismo pronto para integracao; qualidade visual final NAO aprovada ate julgamento do Mestre.

Provas novas: ../evidencias/cor08_composicao/{t2_composicao.json,t2_metricas.json,contraprova_guardas.log,suite.log}, executores testes/codex/compor_t2_cor08.py e reproduzir_cor08.py. Pacote tem 20 testes adicionais, sem remover os 343 da base.

Fechamento v2: auditoria/composicao publicada em **548b61c**, merge em **6083b89**, Paint em **197ef15**. Suite final da mesma arvore executavel: **363 / 0 falhas / 0 erros / 1 skip**, 41,849 s. Este commit acrescenta somente documentacao; nenhuma alteracao executavel desde essa suite. A0 encerrada por prova positiva e negativa, S2 confirmada pixel a pixel, nao ha patch de centro adicional. Pendencia externa: integracao seletiva pelo Muse e julgamento visual do Mestre; nenhuma tarefa A–E desta rodada ficou em execucao oculta.
