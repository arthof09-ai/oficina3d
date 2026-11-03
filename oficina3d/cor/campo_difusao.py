"""Campo de difusao por texel (K2+, T-COR-3) - mecanismo atras da flag
``campo_difusao="k2plus"`` do pedido do bake da Etapa COR.

O mecanismo A3 (``preenchimento.py``) atribui a cada face cega UMA cor
lisa - a da sua face-fonte, propagada por BFS - e pinta todos os texeis
cegos da face com ela. E essa atribuicao plana por face que produz o
mosaico medido na T-COR-2. K2+ substitui-a, atras de flag, por um
CAMPO por texel: cada texel cego de face alcancavel recebe o valor da
extensao harmonica discreta das cores directas sobre o grafo de texeis
do corpo - vizinhanca intra-face (E1) + fantasmas atraves da costura
(E2) - calculada em LUZ LINEAR. Especificacao: PACOTE-T-COR-3 (julgado
PRONTO COM RESSALVAS pelas lentes de Regras e de Metodo em 2026-11-03),
aberto pelo ACTO-ABERTURA-T-COR-3.

Contrato (pacote SS1.2): as entradas sao os produtos que o caminho
actual ja produz (``texel_face``, ``pintado``, ``faces``, ``faces_uv``,
``verts``, ``alcancavel``, ``cores_final`` de ``preenchimento``); as
saidas sao a textura com as incognitas escritas, a mascara aplicada
(classe de proveniencia ``preenchimento_3d`` - o mesmo assento do A3)
e o relatorio do campo. ``preenchimento.py`` fica INTOCADO e os seus
produtos calculam-se nos dois bracos.

Espaco de cor (pacote SS1.5): o campo vive em luz linear e as
conversoes acontecem em EXACTAMENTE dois pontos, ambos neste modulo:
P1 - os valores de fronteira que alimentam ``rhs`` e o chute inicial
convertem-se de sRGB para linear uma unica vez, ao montar o sistema;
P2 - os valores resolvidos convertem-se de linear para sRGB uma unica
vez, ao escrever cada texel incognito. Nenhuma outra media ou
interpolacao existe dentro do campo: a unica agregacao e a equacao de
SS1.3. Media em sRGB dentro do campo e STOP (cerca (7)).

Resolvedor (pacote SS1.6): gradiente conjugado pre-condicionado
(Jacobi: pre-condicionador = diagonal ``grau``), float64, tres canais
em simultaneo sobre as estruturas CSR, so numpy. Criterio unico:
residuo maximo da equacao, recomputado directamente do stencil,
<= 1e-9; tecto de 8192 iteracoes; nao verificado (incl. por tecto) =>
excepcao nomeada ``CampoNaoConvergiu`` - nunca aceitacao silenciosa.

Instrumentacao (descarga de Metodo C-3 no julgamento do pacote): o
relatorio do campo regista, SEM limiar, a distribuicao das distancias
das propostas E2 aceites (ponto reflectido -> centro do texel
escolhido, em pixeis: mediana/p95/maximo), a contagem de pontos
reflectidos fora do triangulo UV da face de destino e a contagem de
propostas falhadas por face sem texeis rasterizados (SS1.3).

A doadora nomeada (pacote SS2) vive neste modulo como instrumento de
medicao e de despejo - NUNCA como ingrediente do campo (SS1.9).
"""

from __future__ import annotations

import numpy as np

from oficina3d.cor import costura as _costura
from oficina3d.cor import preenchimento as _PF
from oficina3d.cor import projecao as _P

TOL_RESIDUO = 1e-9
MAX_ITERACOES = 8192


class CampoNaoConvergiu(Exception):
    """O campo nao atingiu o residuo verificado <= 1e-9 (SS1.6).

    STOP nomeado do pacote: o bake falha as claras; nao existe
    aceitacao silenciosa de um campo por convergir.
    """


# ----------------------------------------------------------------------------
# Conversoes de espaco de cor (SS1.5 - as formulas declaradas, sem clamp)
# ----------------------------------------------------------------------------

def srgb_para_linear(c):
    """sRGB -> luz linear: c/12.92 se c <= 0.04045, senao
    ((c+0.055)/1.055)^2.4. Ponto P1 quando alimenta rhs/chute."""
    c = np.asarray(c, dtype=np.float64)
    return np.where(c <= 0.04045, c / 12.92,
                    ((c + 0.055) / 1.055) ** 2.4)


def linear_para_srgb(l):
    """Luz linear -> sRGB: 12.92*l se l <= 0.0031308, senao
    1.055*l^(1/2.4) - 0.055. Ponto P2 quando escreve a incognita."""
    l = np.asarray(l, dtype=np.float64)
    return np.where(l <= 0.0031308, 12.92 * l,
                    1.055 * np.power(np.maximum(l, 0.0), 1.0 / 2.4) - 0.055)


# ----------------------------------------------------------------------------
# Acoplamento: arestas E1 (intra-face) e fantasmas E2 (atraves da costura)
# ----------------------------------------------------------------------------

def _texeis_por_face(texel_face: np.ndarray, n_faces: int):
    """Lista por face de (linhas, colunas) dos seus texeis, em ordem
    raster (a de ``np.nonzero``) - a ordem fixa de toda a construcao."""
    return [np.nonzero(texel_face == f) for f in range(n_faces)]


def pares_e1(texel_face: np.ndarray) -> set:
    """Arestas intra-face (SS1.3, E1): pares (a, b), a < b, de indices
    lineares de texeis 4-vizinhos na grelha com a MESMA face. A
    restricao ``texel_face[u] == texel_face[t]`` e o que mantem o
    campo dentro de cada face/componente no espaco da textura."""
    tf = np.asarray(texel_face)
    t = tf.shape[0]
    pares = set()
    # Vizinho a direita (mesma linha, coluna + 1).
    ok = (tf[:, :-1] >= 0) & (tf[:, :-1] == tf[:, 1:])
    ls, cs = np.nonzero(ok)
    for l, c in zip(ls.tolist(), cs.tolist()):
        a = l * t + c
        pares.add((a, a + 1))
    # Vizinho abaixo (linha + 1, mesma coluna).
    ok = (tf[:-1, :] >= 0) & (tf[:-1, :] == tf[1:, :])
    ls, cs = np.nonzero(ok)
    for l, c in zip(ls.tolist(), cs.tolist()):
        a = l * t + c
        pares.add((a, a + t))
    return pares


def propostas_e2(texel_face: np.ndarray, faces: np.ndarray,
                 faces_uv: np.ndarray, verts: np.ndarray):
    """Fantasmas atraves da costura (SS1.3, E2) + instrumentacao C-3.

    Para cada aresta do grafo dual soldado (f, g) - extremos soldados
    (A, B) - e cada texel t de f: baricentricas (a_A, a_B, a_C) de t no
    triangulo UV de f (rotinas registadas de ``projecao``:
    ``_uv_para_pixels``/``_baricentricas``, no centro do texel); o
    ponto reflectido em g tem baricentricas (a_A, a_B, -a_C); a
    proposta de t e o texel de g cujo centro esta mais perto desse
    ponto (euclidiana em pixeis; desempate: menor (linha, coluna) - a
    ordem raster da lista de texeis de g, que ``np.argmin`` respeita
    ao devolver a primeira ocorrencia). A proposta e dirigida; o
    conjunto devolvido e o de pares nao dirigidos (uniao dos dois
    sentidos fica a cargo de quem monta o grafo).

    Leitura de implementacao, declarada: o ponto reflectido avalia-se
    como a combinacao a_A*A_g + a_B*B_g - a_C*C_g das coordenadas de
    pixeis de g - a semantica de avaliacao das rotinas registadas
    (ponto = soma w_i * P_i, a de ``_baricentricas``). Os pesos somam
    1 - 2*a_C: o ponto cai fora do triangulo de g sempre que a_C > 0,
    e o texel escolhido pode estar longe da aresta partilhada. E
    exactamente este comportamento que a instrumentacao C-3 conta e
    publica (pontos fora, distancias) - sem guarda nem correccao
    silenciosa, como o julgamento de Metodo pediu.

    Devolve (pares, estatisticas): estatisticas regista, sem limiar
    (descarga C-3): n. de propostas aceites e a distribuicao das suas
    distancias (mediana/p95/maximo em pixeis); n. de pontos
    reflectidos fora do triangulo UV de g (teste ``dentro`` da rotina
    registada; triangulo degenerado conta como fora); n. de propostas
    falhadas - contado uma vez por (aresta, sentido) em que a face de
    destino nao tem texeis rasterizados e a de origem tem (SS1.3:
    "nao ha proposta por essa aresta - declara-se e conta-se");
    arestas duais ignoradas por soldadura degenerada (os extremos nao
    ocupam exactamente dois cantos da face).
    """
    texel_face = np.asarray(texel_face)
    tamanho = texel_face.shape[0]
    faces = np.asarray(faces, dtype=int)
    faces_uv = np.asarray(faces_uv, dtype=np.float64)
    n_faces = len(faces)
    faces_w = _costura._faces_soldadas(faces, verts)
    arestas = _costura._pares_adjacentes(faces_w)
    faces_px = _P._uv_para_pixels(faces_uv, tamanho)
    texeis = _texeis_por_face(texel_face, n_faces)
    # Baricentricas dos texeis de cada face, uma vez por face:
    # cache[f] = (w (3, N), linhas, colunas) ou None se a face nao tem
    # texeis ou o seu triangulo UV e degenerado para a rotina.
    cache = []
    for f in range(n_faces):
        ls, cs = texeis[f]
        if len(ls) == 0:
            cache.append(None)
            continue
        res = _P._baricentricas(faces_px[f],
                                cs.astype(np.float64) + 0.5,
                                ls.astype(np.float64) + 0.5)
        if res is None:
            cache.append(None)
            continue
        _dentro, w0, w1, w2 = res
        cache.append((np.stack([w0, w1, w2]), ls, cs))

    pares = set()
    distancias = []
    n_fora = 0
    n_falhadas = 0
    n_ignoradas = 0
    for (va, vb) in sorted(arestas.keys()):
        incidentes = arestas[(va, vb)]
        if len(incidentes) != 2:
            continue  # borda (1) ou nao-manifold (>2): sem aresta dual
        f, g = int(incidentes[0]), int(incidentes[1])
        for origem, destino in ((f, g), (g, f)):
            ls_o, _cs_o = texeis[origem]
            ls_d, cs_d = texeis[destino]
            if len(ls_o) == 0:
                continue  # sem texeis de origem, nao ha propostas
            if len(ls_d) == 0:
                n_falhadas += 1  # SS1.3: declara-se e conta-se
                continue
            if cache[origem] is None:
                continue  # origem sem baricentricas: nada a propor
            tri_o = faces_w[origem]
            tri_d = faces_w[destino]
            cantos_o = [k for k in range(3) if tri_o[k] in (va, vb)]
            cantos_d = [k for k in range(3) if tri_d[k] in (va, vb)]
            if len(cantos_o) != 2 or len(cantos_d) != 2:
                n_ignoradas += 1
                continue
            co_c = 3 - cantos_o[0] - cantos_o[1]  # o canto fora da aresta
            cd_c = 3 - cantos_d[0] - cantos_d[1]
            # A e B casados por id soldado, nao por posicao no tri.
            k_a_o = cantos_o[0] if tri_o[cantos_o[0]] == va else cantos_o[1]
            k_b_o = cantos_o[1] if k_a_o == cantos_o[0] else cantos_o[0]
            k_a_d = cantos_d[0] if tri_d[cantos_d[0]] == va else cantos_d[1]
            k_b_d = cantos_d[1] if k_a_d == cantos_d[0] else cantos_d[0]
            w, ls_t, cs_t = cache[origem]
            a_a = w[k_a_o]
            a_b = w[k_b_o]
            a_c = w[co_c]
            px_d = faces_px[destino]
            pt_x = a_a * px_d[k_a_d][0] + a_b * px_d[k_b_d][0] \
                - a_c * px_d[cd_c][0]
            pt_y = a_a * px_d[k_a_d][1] + a_b * px_d[k_b_d][1] \
                - a_c * px_d[cd_c][1]
            res_d = _P._baricentricas(px_d, pt_x, pt_y)
            if res_d is None:
                n_fora += len(ls_t)
            else:
                n_fora += int((~res_d[0]).sum())
            centros_x = cs_d.astype(np.float64) + 0.5
            centros_y = ls_d.astype(np.float64) + 0.5
            d2 = (pt_x[:, None] - centros_x[None, :]) ** 2 \
                + (pt_y[:, None] - centros_y[None, :]) ** 2
            esc = np.argmin(d2, axis=1)  # 1.a ocorrencia = menor (lin, col)
            distancias.append(np.sqrt(d2[np.arange(len(ls_t)), esc]))
            for i in range(len(ls_t)):
                t_lin = int(ls_t[i]) * tamanho + int(cs_t[i])
                u_lin = int(ls_d[esc[i]]) * tamanho + int(cs_d[esc[i]])
                if t_lin != u_lin:
                    pares.add((min(t_lin, u_lin), max(t_lin, u_lin)))
    if distancias:
        dist = np.concatenate(distancias)
        est = {"propostas": int(len(dist)),
               "distancia_mediana": float(np.percentile(dist, 50)),
               "distancia_p95": float(np.percentile(dist, 95)),
               "distancia_maxima": float(dist.max())}
    else:
        est = {"propostas": 0, "distancia_mediana": None,
               "distancia_p95": None, "distancia_maxima": None}
    est["pontos_fora_do_triangulo"] = int(n_fora)
    est["propostas_falhadas_sem_texeis"] = int(n_falhadas)
    est["arestas_ignoradas_degeneradas"] = int(n_ignoradas)
    return pares, est


def montar_estruturas(texel_face: np.ndarray, pintado: np.ndarray,
                      alcancavel: np.ndarray, pares: set) -> dict:
    """Monta o sistema de SS1.3 sobre as incognitas, com as guardas.

    Incognitas (por esta ordem): texeis do dominio (``texel_face >=
    0``), nao directos, cuja face e alcancavel. Vizinhos: os pares
    dados (E1 + E2 simetrizados) repartidos em vizinhos incognitos e
    vizinhos de fronteira (texeis directos). Guardas de SS1.3: uma
    componente conexa de incognitas SEM nenhum vizinho de fronteira -
    incluindo a incognita isolada de grau 0 - e excluida inteira e
    contada em ``excluidos_sem_acoplamento`` (um problema de Dirichlet
    sem fronteira nao tem solucao unica; nao se inventa ancora). As
    sobreviventes renumeram-se em ordem raster.

    Devolve as estruturas fechadas de SS1.3: ``viz_ptr`` (U+1) int64 e
    ``viz_idx`` (E) int32 CSR das arestas incognita-incognita (vizinhos
    em ordem crescente), ``grau`` (U) int (vizinhos incognitos + de
    fronteira), ``front_ptr``/``front_idx`` CSR dos vizinhos de
    fronteira (indices lineares de texel), ``idx`` (T, T) int64 com o
    numero de cada incognita (-1 fora), posicoes e faces das
    incognitas em ordem raster.
    """
    texel_face = np.asarray(texel_face)
    pintado = np.asarray(pintado, dtype=bool)
    alcancavel = np.asarray(alcancavel, dtype=bool)
    tamanho = texel_face.shape[0]
    dominio = texel_face >= 0
    seguro = np.where(dominio, texel_face, 0)
    bruto = dominio & ~pintado & alcancavel[seguro]
    idx_bruto = -np.ones((tamanho, tamanho), dtype=np.int64)
    n_bruto = int(bruto.sum())
    idx_bruto[bruto] = np.arange(n_bruto, dtype=np.int64)
    linhas_b, colunas_b = np.nonzero(bruto)  # ordem raster
    flat_b = (linhas_b * tamanho + colunas_b).astype(np.int64)
    # Vizinhos de cada incognita bruta, a partir dos pares.
    vizinhos = [set() for _ in range(n_bruto)]
    fronteira = [set() for _ in range(n_bruto)]
    for a, b in pares:
        ia = idx_bruto.flat[a] if dominio.flat[a] else -1
        ib = idx_bruto.flat[b] if dominio.flat[b] else -1
        da = dominio.flat[a] and pintado.flat[a]
        db = dominio.flat[b] and pintado.flat[b]
        if ia >= 0 and ib >= 0:
            vizinhos[ia].add(int(ib))
            vizinhos[ib].add(int(ia))
        elif ia >= 0 and db:
            fronteira[ia].add(int(b))
        elif ib >= 0 and da:
            fronteira[ib].add(int(a))
    # Componentes conexas das incognitas (BFS em ordem crescente) e a
    # guarda: componente sem vizinho de fronteira e excluida inteira.
    componente = -np.ones(n_bruto, dtype=np.int64)
    tem_fronteira = np.zeros(n_bruto, dtype=bool)
    for i in range(n_bruto):
        tem_fronteira[i] = len(fronteira[i]) > 0
    n_comp = 0
    for i in range(n_bruto):
        if componente[i] >= 0:
            continue
        pilha = [i]
        componente[i] = n_comp
        while pilha:
            u = pilha.pop()
            for v in sorted(vizinhos[u]):
                if componente[v] < 0:
                    componente[v] = n_comp
                    pilha.append(v)
        n_comp += 1
    comp_com_fronteira = np.zeros(n_comp, dtype=bool)
    for i in range(n_bruto):
        if tem_fronteira[i]:
            comp_com_fronteira[componente[i]] = True
    mantem = comp_com_fronteira[componente]
    excluidos = int((~mantem).sum())
    # Renumeracao em ordem raster das sobreviventes.
    novo = -np.ones(n_bruto, dtype=np.int64)
    novo[mantem] = np.arange(int(mantem.sum()), dtype=np.int64)
    idx = -np.ones((tamanho, tamanho), dtype=np.int64)
    sel = np.nonzero(mantem)[0]
    idx[linhas_b[sel], colunas_b[sel]] = novo[sel]
    linhas = linhas_b[sel]
    colunas = colunas_b[sel]
    u_total = int(mantem.sum())
    viz_listas = []
    front_listas = []
    grau = np.zeros(u_total, dtype=np.int64)
    for pos, i in enumerate(sel.tolist()):
        vs = sorted(int(novo[v]) for v in vizinhos[i] if mantem[v])
        fs = sorted(int(x) for x in fronteira[i])
        viz_listas.append(vs)
        front_listas.append(fs)
        grau[pos] = len(vs) + len(fs)
    viz_ptr = np.zeros(u_total + 1, dtype=np.int64)
    viz_ptr[1:] = np.cumsum([len(v) for v in viz_listas])
    viz_idx = np.array([v for vs in viz_listas for v in vs], dtype=np.int32)
    front_ptr = np.zeros(u_total + 1, dtype=np.int64)
    front_ptr[1:] = np.cumsum([len(f) for f in front_listas])
    front_idx = np.array([f for fs in front_listas for f in fs],
                         dtype=np.int64)
    return {"idx": idx, "linhas": linhas, "colunas": colunas,
            "faces": texel_face[linhas, colunas].astype(np.int64),
            "viz_ptr": viz_ptr, "viz_idx": viz_idx, "grau": grau,
            "front_ptr": front_ptr, "front_idx": front_idx,
            "excluidos_sem_acoplamento": excluidos, "n_incognitas": u_total}


def _matvec(estruturas: dict, x: np.ndarray,
            linhas_csr: np.ndarray) -> np.ndarray:
    """Operador de SS1.3 sobre as CSR: grau(t)*x(t) - soma x(viz)."""
    viz_idx = estruturas["viz_idx"]
    if len(viz_idx):
        contrib = x[viz_idx]  # (E, 3)
        soma = np.stack(
            [np.bincount(linhas_csr, weights=contrib[:, c],
                         minlength=len(x)) for c in range(3)], axis=1)
    else:
        soma = np.zeros_like(x)
    return estruturas["grau"][:, None] * x - soma


def resolver_campo(estruturas: dict, textura: np.ndarray,
                   cores_final: np.ndarray,
                   converter_entrada=srgb_para_linear):
    """Resolve o sistema de SS1.3 em luz linear (SS1.5/SS1.6).

    P1 acontece aqui, uma unica vez: os valores de fronteira que
    alimentam ``rhs`` e o chute inicial ``x0(t) =
    cores_final[texel_face[t]]`` convertem-se com
    ``converter_entrada`` (em producao, ``srgb_para_linear``; a
    corrida S da medicao de SS3.3 passa a identidade - e vive nos
    testes, nunca neste modulo como caminho de producao).

    CG pre-condicionado (Jacobi = diagonal ``grau``), float64, 3
    canais em simultaneo; o residuo usado no criterio e recomputado
    do stencil a cada iteracao (nunca o da recorrencia) e, ao sair,
    recomputa-se outra vez para o relatorio. Residuo verificado
    > 1e-9 - incluindo por tecto de iteracoes - levanta
    ``CampoNaoConvergiu``.

    Devolve (x (U, 3) em luz linear, relatorio parcial com
    ``iteracoes`` e ``residuo_maximo_verificado``).
    """
    u_total = estruturas["n_incognitas"]
    if u_total == 0:
        return np.zeros((0, 3)), {"iteracoes": 0,
                                  "residuo_maximo_verificado": 0.0}
    textura = np.asarray(textura, dtype=np.float64)
    cores_final = np.asarray(cores_final, dtype=np.float64)
    front_idx = estruturas["front_idx"]
    front_ptr = estruturas["front_ptr"]
    if len(front_idx):
        valores = converter_entrada(textura.reshape(-1, 3)[front_idx])
        linhas_f = np.repeat(np.arange(u_total),
                             np.diff(front_ptr))
        rhs = np.stack(
            [np.bincount(linhas_f, weights=valores[:, c],
                         minlength=u_total) for c in range(3)], axis=1)
    else:
        rhs = np.zeros((u_total, 3))
    x = converter_entrada(cores_final[estruturas["faces"]]).copy()
    grau = estruturas["grau"].astype(np.float64)
    linhas_csr = np.repeat(np.arange(u_total),
                           np.diff(estruturas["viz_ptr"]))

    def residuo(xv):
        return rhs - _matvec(estruturas, xv, linhas_csr)

    r = residuo(x)
    res_max = float(np.abs(r).max()) if r.size else 0.0
    if res_max <= TOL_RESIDUO:
        return x, {"iteracoes": 0, "residuo_maximo_verificado": res_max}
    z = r / grau[:, None]
    p = z.copy()
    rs = float((r * z).sum())
    for it in range(1, MAX_ITERACOES + 1):
        ap = _matvec(estruturas, p, linhas_csr)
        denominador = float((p * ap).sum())
        if denominador <= 0.0:
            break  # operador nao avancou: cai na verificacao (STOP)
        alfa = rs / denominador
        x = x + alfa * p
        r = residuo(x)  # residuo do stencil, nao o da recorrencia
        res_max = float(np.abs(r).max())
        if res_max <= TOL_RESIDUO:
            verificado = float(np.abs(residuo(x)).max())
            return x, {"iteracoes": it,
                       "residuo_maximo_verificado": verificado}
        z = r / grau[:, None]
        rs_novo = float((r * z).sum())
        if rs_novo <= 0.0:
            break
        p = z + (rs_novo / rs) * p
        rs = rs_novo
    verificado = float(np.abs(residuo(x)).max())
    raise CampoNaoConvergiu(
        "campo nao convergiu: residuo maximo verificado %.6g > %g "
        "apos %d iteracoes (U=%d)" % (verificado, TOL_RESIDUO,
                                      MAX_ITERACOES, u_total))


def escrever_campo(textura: np.ndarray, pintado: np.ndarray,
                   estruturas: dict, valores_lineares: np.ndarray,
                   converter_saida=linear_para_srgb):
    """Escreve SO as incognitas na textura (SS1.7). P2 acontece aqui,
    uma unica vez: ``converter_saida`` (em producao,
    ``linear_para_srgb``) aplica-se aos valores resolvidos ao
    escrever. Texeis directos nunca sao escritos (L-5).

    Devolve (textura, pintado com as incognitas marcadas, mascara
    aplicada) - o espelho do contrato de ``aplicar_preenchimento``;
    a mascara aplicada e a classe ``preenchimento_3d`` do despejo.
    """
    tex = np.array(textura, dtype=np.float64, copy=True)
    pin = np.array(pintado, dtype=bool, copy=True)
    aplicada = np.zeros(pin.shape, dtype=bool)
    if estruturas["n_incognitas"]:
        ls = estruturas["linhas"]
        cs = estruturas["colunas"]
        tex[ls, cs] = converter_saida(
            np.asarray(valores_lineares, dtype=np.float64))
        pin[ls, cs] = True
        aplicada[ls, cs] = True
    return tex, pin, aplicada


def construir_acoplamento(texel_face: np.ndarray, pintado: np.ndarray,
                          faces: np.ndarray, faces_uv: np.ndarray,
                          verts: np.ndarray,
                          alcancavel: np.ndarray) -> dict:
    """A construcao completa de SS1.3: pares E1 + fantasmas E2
    (uniao simetrizada, sem auto-lacos nem duplicados - sao conjuntos),
    estruturas com as guardas, e a simetria verificada por assercao.

    O ditado devolvido e o de ``montar_estruturas`` acrescido de
    ``pares_e1``, ``pares_e2`` e ``estatisticas_e2`` (instrumentacao
    C-3, sem limiar)."""
    p_e1 = pares_e1(texel_face)
    p_e2, est = propostas_e2(texel_face, faces, faces_uv, verts)
    estruturas = montar_estruturas(texel_face, pintado, alcancavel,
                                   p_e1 | p_e2)
    # Guarda (i) de SS1.3: simetria do grafo incognita-incognita,
    # sem auto-lacos nem duplicados - verificada por assercao sobre
    # as chaves (t, u) das CSR nos dois sentidos.
    viz_ptr = estruturas["viz_ptr"]
    viz_idx = estruturas["viz_idx"]
    u_total = estruturas["n_incognitas"]
    if len(viz_idx):
        t_rep = np.repeat(np.arange(u_total), np.diff(viz_ptr))
        assert bool((t_rep != viz_idx).all()), "auto-laco no grafo"
        chave_ida = t_rep.astype(np.int64) * u_total \
            + viz_idx.astype(np.int64)
        chave_volta = viz_idx.astype(np.int64) * u_total \
            + t_rep.astype(np.int64)
        assert len(np.unique(chave_ida)) == len(chave_ida), \
            "aresta duplicada no grafo do campo"
        assert np.array_equal(np.sort(chave_ida), np.sort(chave_volta)), \
            "grafo do campo nao simetrico"
    estruturas["pares_e1"] = p_e1
    estruturas["pares_e2"] = p_e2
    estruturas["estatisticas_e2"] = est
    return estruturas


def aplicar_campo(textura: np.ndarray, pintado: np.ndarray,
                  texel_face: np.ndarray, faces: np.ndarray,
                  faces_uv: np.ndarray, verts: np.ndarray,
                  alcancavel: np.ndarray, cores_final: np.ndarray):
    """O mecanismo K2+ completo (SS1.8, ponto unico de divergencia):
    montar baricentricas/acoplamento (SS1.3) -> converter a fronteira
    (P1) -> resolver (SS1.6) -> aplicar (P2, SS1.7).

    Devolve (textura, pintado, mascara aplicada, relatorio do campo):
    o relatorio e o produto obrigatorio de SS1.6 - incognitas,
    arestas (comprimento CSR de ``viz_idx``; ``arestas_entre_
    incognitas`` = pares nao dirigidos), excluidos de SS1.3,
    iteracoes, residuo maximo verificado, convergiu - acrescido do
    bloco ``e2`` da instrumentacao C-3 (sem limiar)."""
    estruturas = construir_acoplamento(texel_face, pintado, faces,
                                       faces_uv, verts, alcancavel)
    x, parcial = resolver_campo(estruturas, textura, cores_final)
    tex, pin, aplicada = escrever_campo(textura, pintado, estruturas, x)
    relatorio = {
        "incognitas": int(estruturas["n_incognitas"]),
        "arestas": int(len(estruturas["viz_idx"])),
        "arestas_entre_incognitas": int(len(estruturas["viz_idx"]) // 2),
        "excluidos_sem_acoplamento": int(
            estruturas["excluidos_sem_acoplamento"]),
        "iteracoes": int(parcial["iteracoes"]),
        "residuo_maximo_verificado": float(
            parcial["residuo_maximo_verificado"]),
        "convergiu": True,
        "e2": estruturas["estatisticas_e2"],
    }
    return tex, pin, aplicada, relatorio


# ----------------------------------------------------------------------------
# A doadora nomeada (pacote SS2) - medicao e despejo; NUNCA entra no campo
# ----------------------------------------------------------------------------

def doadora_nomeada(adjacencia, tem_cor, contagem) -> np.ndarray:
    """Doadora de cada face na construcao fechada de SS2: a face COM
    FONTE directa de menor distancia de anel no grafo dual soldado,
    com desempate deterministico por (distancia, maior contagem de
    texeis directos, menor indice de face).

    Computacao: ``anel`` = a BFS multi-fonte de ``difundir``
    (reutilizada - nao se constroi segunda BFS); candidatas propagam
    por camadas crescentes de anel (cand(f) = uniao de cand(g) sobre
    os vizinhos g com anel(g) = anel(f) - 1); doadora(f) = o elemento
    de cand(f) que maximiza (contagem, -indice). Face com fonte -> ela
    propria; face inalcançavel -> -1. Devolve (F,) int.
    """
    tem_cor = np.asarray(tem_cor, dtype=bool)
    contagem = np.asarray(contagem)
    n = len(adjacencia)
    _cores, anel, alcancavel = _PF.difundir(
        adjacencia, np.zeros((n, 3)), tem_cor)
    cand = [None] * n
    for f in range(n):
        if tem_cor[f]:
            cand[f] = {f}
    if alcancavel.any():
        d_max = int(anel[alcancavel].max())
        for d in range(1, d_max + 1):
            for f in range(n):
                if anel[f] != d:
                    continue
                s = set()
                for g in adjacencia[f]:
                    if anel[g] == d - 1 and cand[g]:
                        s |= cand[g]
                cand[f] = s
    doadora = -np.ones(n, dtype=int)
    for f in range(n):
        if cand[f]:
            doadora[f] = max(cand[f],
                             key=lambda c: (int(contagem[c]), -int(c)))
    return doadora
