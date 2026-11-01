# Veredito — verificação independente D2/D7 (tranche de correções, commit `aa2758c`)

Método: reimplementação própria a partir do GLB (parse binário manual, sem `trimesh`, sem `costura.py`), solda por dicionário de posições arredondadas a 6 casas, cores por mediana de 4 amostras. Cópias do staging são byte-idênticas ao repo `aa2758c`; o diff `17462aa → aa2758c` confirma exatamente o prescrito (solda por posição com tolerância 1e-6 em `classificar_arestas`, `piores_costuras`, teste de vértice duplicado).

## D2 — FECHADO

- Reprodução independente exata, à casa decimal, em frame glTF com costas = (0,0,−1): limiar 0,5 — alvo n=12.632, média 28,23, 24,01% > 30 vs controle n=11.949, média 7,05, 5,86%; limiar 0,9 — alvo n=2.063, média 18,96, 18,03% vs controle n=2.250, média 8,41, 7,07%. Separação forte confirmada; o diagnóstico "separação fraca" era de fato o eixo errado.
- Frame confirmado na fonte: `projecao.py` — GLB Y-up, frente +Z; Blender frente −Y; `direcao_camera` docstring "coords Blender, Z-up", costas = (0,1,0) Blender; conversão (x,y,z)→(x,z,−y) dá (0,0,−1) = −Z glTF. Eixo final registrado na republicação (`"frame": "glTF… costas = (0,0,-1)…"`) e na docstring L-25 de `costura.py`.
- Bake não afetado: `_blender_cor.py` (linhas ~348–360) usa `P.direcao_camera` com normais e `BVH.ray_cast` dentro do Blender, mesmo frame — só a medição do `run_prova` estava errada. Nenhum novo bake necessário.

## D7 — FECHADO

- Reprodução independente exata, à casa decimal: solda 47.476 → 24.805 únicos; costura n=13.758, média 93,49, mediana 77,22, p90 199,86, 78,08% > 30, 59,90% > 60, máx 337,17; interna n=60.867, média 36,20, mediana 13,96, p90 107,19, 36,61% > 30; borda 0, não-manifold 0, classificadas 74.625 (= 3×49.750/2, malha fechada). Adv3v idem (costura 96,42 / interna 33,65). Conferência extra: `vmapping[indices]` do `uv.npz` reproduz exatamente as faces do GLB.
- Teste de vértice duplicado: os 7 testes de `test_cor_costura.py` passam no meu interpretador (7/7). Contra o `costura.py` de `17462aa` o teste novo falha (TypeError: sem o parâmetro `verts`); contra um stub que aceita `verts` mas ignora a solda, falha por asserção (0 != 1) — ou seja, o teste pega o comportamento do bug, não só a assinatura.
- Prévia flat: as duas imagens existem (800×800) e o script `_blender_flat.py` usa exclusivamente `ShaderNodeEmission` com a textura, sem luzes — cores planas, sem sombreamento. A pior costura nº 1 confere exatamente (faces 10776/10979, 337,17, ponto médio [−0.325465, 0.160957, −0.638934]), e a câmera aponta para esse ponto, logo a costura está no centro da imagem, onde há saltos abruptos de cor entre facetas (descontinuidade de textura, não sombreamento). Ressalva julgada **satisfeita no sentido prescrito** (prévia de região de costura): a limitação honesta permanece — sem marcação, a costura individual não é isolável a olho no meio das demais descontinuidades do cristal. Isso é limitação de leitura da imagem, não bloqueio do fechamento, que repousa nos números reproduzidos.
- Divergência explicada (não bloqueia): o 3º pior da republicação (faces 24253/24557) vs o meu (24271/24577) é um empate exato em 336,02 — há 2 costuras com essa distância; a ordem do top 3 é ambígua por desempate, o top 1 (usado na prévia) é idêntico.
- `suite.log` confere o exigido: `tests=252 failures=0 errors=0 skipped=1`. (Limite declarado: re-rodei localmente só os 7 testes de costura; os 252 atesto pelo log, não por re-execução integral.)

## Pendências que NÃO fecham aqui (registradas, não reprovação desta verificação)

- **S2-3** (suspeita de troca esquerda/direita nas imagens da Besta): ortogonal a D2/D7, sem nenhum elemento novo na republicação; segue aberta e bloqueia a textura base, não D2/D7.
- **S3-2** (`sem_cor 0` sem máscara de cobertura entregue): segue não conferido.
- **S4-2** (`resultado_cor.json` nativo do bake): segue não entregue.
- **S3-3**: parte de hashes FECHADA — a republicação traz `glb_refinado_entrada = ba8d6cd5…8621` e `uv_npz = e8b76f32…f419`, ambos conferidos por mim byte a byte; a parte da margem já estava resolvida como definicional no adendo do Crítico anterior (512 vs 2048 px).

**Resumo: D2 — FECHADO. D7 — FECHADO.**