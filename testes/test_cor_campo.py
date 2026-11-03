"""T-COR-3: campo de difusao por texel (K2+) - PACOTE-T-COR-3 SS7.

Bateria aditiva, fora do Blender, sobre ``oficina3d.cor.campo_difusao``
e a fixture da cerca (6) de ``testes/campo_fixture.py``:

1. conversoes sRGB<->linear (valores conhecidos, extremos, limiares,
   ida-e-volta);
2. acoplamento: o micro-caso da costura (dois triangulos, uma aresta
   soldada, duas ilhas) - o par fantasma esperado, recomputado por
   reimplementacao independente da reflexao de SS1.3; simetria do
   grafo; sem auto-lacos nem duplicados; guardas de SS1.3;
3. doadora nomeada (SS2): a distancia manda; desempates por contagem
   e por indice; fonte -> ela propria; inalcancavel -> -1;
4. resolvedor contra solucao densa (<= 1e-8); o chute nao altera a
   solucao; o STOP nomeado ``CampoNaoConvergiu`` dispara por tecto;
5. a fixture da cerca (6) com as leituras (a)-(g) de SS3.2 - com a
   superficie de comparacao de (b) FIXADA pela descarga C-2 de
   Metodo: valores COMO ESCRITOS na textura (a solucao densa
   convertida em P2 contra a textura de saida) - e os dentes
   M-a..M-d, cada um contra o seu controlo limpo;
6. a medicao de SS3.3 (artefacto ``campo_divergencia.json``, nas duas
   variantes da descarga C-1): existencia, esquema, finitude,
   mediana/p95 recomputados do array - SEM assercao sobre valores;
7. a flag ``campo_difusao`` do pedido: a funcao de validacao de
   ``_blender_cor.py`` exercitada por extraccao AST (o script do
   Blender nao e importavel fora dele - padrao da casa).
"""
import ast
import json
import sys
import unittest
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))
AQUI = Path(__file__).resolve().parent
if str(AQUI) not in sys.path:
    sys.path.insert(0, str(AQUI))

import campo_fixture as FX  # noqa: E402
from oficina3d.cor import campo_difusao as CD  # noqa: E402
from oficina3d.cor import preenchimento as PF  # noqa: E402


def _correr(fx, pares=None, converter_entrada=None, converter_saida=None):
    """Composicao do campo sobre a fixture a partir das pecas do
    modulo (a mesma composicao de ``aplicar_campo``, com os pontos
    de mutacao expostos para os dentes): devolve
    (textura, aplicada, estruturas)."""
    _c, _t, _ct, _a, cores_final, _an, alc = FX.produtos_preenchimento(fx)
    if pares is None:
        estruturas = CD.construir_acoplamento(
            fx["texel_face"], fx["pintado"], fx["faces"], fx["faces_uv"],
            fx["verts"], alc)
    else:
        estruturas = CD.montar_estruturas(
            fx["texel_face"], fx["pintado"], alc, pares)
    x, _parcial = CD.resolver_campo(
        estruturas, fx["textura"], cores_final,
        converter_entrada=converter_entrada or CD.srgb_para_linear)
    tex, _pin, aplicada = CD.escrever_campo(
        fx["textura"], fx["pintado"], estruturas, x,
        converter_saida=converter_saida or CD.linear_para_srgb)
    return tex, aplicada, estruturas


def _solucao_densa(estruturas, fx):
    """Solucao independente do mesmo problema (SS3.2(b)):
    ``numpy.linalg.solve`` sobre a matriz montada das estruturas,
    com o rhs convertido em P1 - devolvida JA convertida em P2
    (a superficie de comparacao sao os valores como escritos)."""
    u = estruturas["n_incognitas"]
    a = np.zeros((u, u))
    vp, vi = estruturas["viz_ptr"], estruturas["viz_idx"]
    for t in range(u):
        a[t, t] = estruturas["grau"][t]
        a[t, vi[vp[t]:vp[t + 1]]] = -1.0
    fp, fi = estruturas["front_ptr"], estruturas["front_idx"]
    rhs = np.zeros((u, 3))
    if len(fi):
        valores = CD.srgb_para_linear(fx["textura"].reshape(-1, 3)[fi])
        linhas_f = np.repeat(np.arange(u), np.diff(fp))
        for c in range(3):
            rhs[:, c] = np.bincount(linhas_f, weights=valores[:, c],
                                    minlength=u)
    sol = np.linalg.solve(a, rhs)
    return CD.linear_para_srgb(sol)


def _leitura_b(tex, estruturas, fx):
    """(b) na superficie fixada por C-2 de Metodo: o campo da
    implementacao contra a solucao densa convertida em P2, sobre os
    valores como escritos na textura, <= 1e-8 por canal."""
    if estruturas["n_incognitas"] == 0:
        return False
    esperado = _solucao_densa(estruturas, fx)
    obtido = tex[estruturas["linhas"], estruturas["colunas"]]
    return bool(np.abs(obtido - esperado).max() <= 1e-8)


class TestConversoes(unittest.TestCase):
    def test_valor_conhecido(self):
        v = float(CD.srgb_para_linear(np.array(0.5)))
        self.assertAlmostEqual(v, 0.21404114048223255, delta=1e-15)

    def test_extremos(self):
        self.assertEqual(float(CD.srgb_para_linear(np.array(0.0))), 0.0)
        self.assertEqual(float(CD.srgb_para_linear(np.array(1.0))), 1.0)
        self.assertEqual(float(CD.linear_para_srgb(np.array(0.0))), 0.0)

    def test_limiares(self):
        # Ramo linear nos limiares (<=), ramo de potencia acima deles.
        self.assertAlmostEqual(float(CD.srgb_para_linear(np.array(0.04045))),
                               0.04045 / 12.92, delta=1e-15)
        acima = 0.04045 + 1e-9
        self.assertAlmostEqual(float(CD.srgb_para_linear(np.array(acima))),
                               ((acima + 0.055) / 1.055) ** 2.4, delta=1e-12)
        self.assertAlmostEqual(float(CD.linear_para_srgb(np.array(0.0031308))),
                               12.92 * 0.0031308, delta=1e-15)
        acima_l = 0.0031308 + 1e-9
        self.assertAlmostEqual(
            float(CD.linear_para_srgb(np.array(acima_l))),
            1.055 * acima_l ** (1.0 / 2.4) - 0.055, delta=1e-12)

    def test_ida_e_volta(self):
        g = np.linspace(0.0, 1.0, 2001)
        volta = CD.linear_para_srgb(CD.srgb_para_linear(g))
        self.assertLessEqual(float(np.abs(volta - g).max()), 1e-12)


def _micro_caso():
    """Dois triangulos, uma aresta soldada (A-B), duas ilhas UV."""
    verts = np.array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0],   # face 0: A B C
        [1, 0, 0], [0, 0, 0], [1, 1, 0],   # face 1: B' A' D (soldada)
    ], dtype=float)
    faces = np.array([[0, 1, 2], [3, 4, 5]])
    faces_uv = np.array([
        [[0.05, 0.05], [0.45, 0.05], [0.05, 0.45]],
        [[0.55, 0.55], [0.95, 0.55], [0.95, 0.95]],
    ])
    return verts, faces, faces_uv, 16


def _fantasmas_independentes(texel_face, faces, faces_uv, verts, tamanho):
    """Reimplementacao independente da reflexao de SS1.3 (sem usar
    as rotinas do modulo nem as de ``projecao`` para as
    baricentricas): resolve o sistema 2x2 de cada texel, reflecte
    pela combinacao (a_A, a_B, -a_C) avaliada nas coordenadas de
    pixeis de g, e escolhe o texel de g mais perto (desempate por
    (linha, coluna)). Devolve o conjunto de pares nao dirigidos."""
    from oficina3d.cor import costura
    faces_w = costura._faces_soldadas(faces, verts)
    arestas = costura._pares_adjacentes(faces_w)
    px = np.empty_like(faces_uv)
    px[..., 0] = faces_uv[..., 0] * tamanho
    px[..., 1] = (1.0 - faces_uv[..., 1]) * tamanho
    texeis = [np.nonzero(texel_face == f) for f in range(len(faces))]
    pares = set()
    for (va, vb), inc in arestas.items():
        if len(inc) != 2:
            continue
        for o, d in ((inc[0], inc[1]), (inc[1], inc[0])):
            if len(texeis[o][0]) == 0 or len(texeis[d][0]) == 0:
                continue
            tri_o, tri_d = faces_w[o], faces_w[d]
            cantos_o = [k for k in range(3) if tri_o[k] in (va, vb)]
            cantos_d = [k for k in range(3) if tri_d[k] in (va, vb)]
            ka_o = cantos_o[0] if tri_o[cantos_o[0]] == va else cantos_o[1]
            kb_o = cantos_o[1] if ka_o == cantos_o[0] else cantos_o[0]
            kc_o = 3 - cantos_o[0] - cantos_o[1]
            ka_d = cantos_d[0] if tri_d[cantos_d[0]] == va else cantos_d[1]
            kb_d = cantos_d[1] if ka_d == cantos_d[0] else cantos_d[0]
            kc_d = 3 - cantos_d[0] - cantos_d[1]
            ls_o, cs_o = texeis[o]
            ls_d, cs_d = texeis[d]
            po = px[o]
            m = np.array([[po[1][0] - po[0][0], po[2][0] - po[0][0]],
                          [po[1][1] - po[0][1], po[2][1] - po[0][1]]])
            for i in range(len(ls_o)):
                p = np.array([cs_o[i] + 0.5, ls_o[i] + 0.5])
                uv = np.linalg.solve(m, p - po[0])
                w = np.array([1.0 - uv[0] - uv[1], uv[0], uv[1]])
                pt = (w[ka_o] * px[d][ka_d] + w[kb_o] * px[d][kb_d]
                      - w[kc_o] * px[d][kc_d])
                melhor, melhor_chave = None, None
                for j in range(len(ls_d)):
                    dist = float(np.hypot(pt[0] - (cs_d[j] + 0.5),
                                          pt[1] - (ls_d[j] + 0.5)))
                    chave = (dist, int(ls_d[j]), int(cs_d[j]))
                    if melhor_chave is None or chave < melhor_chave:
                        melhor_chave = chave
                        melhor = int(ls_d[j]) * tamanho + int(cs_d[j])
                t = int(ls_o[i]) * tamanho + int(cs_o[i])
                if melhor is not None and melhor != t:
                    pares.add((min(t, melhor), max(t, melhor)))
    return pares


class TestAcoplamento(unittest.TestCase):
    def setUp(self):
        self.verts, self.faces, self.faces_uv, self.tam = _micro_caso()
        self.texel_face = PF.mapa_texel_face(self.faces_uv, self.tam)
        self.pintado = np.zeros((self.tam, self.tam), dtype=bool)
        self.alc = np.array([True, True])
        self.est = CD.construir_acoplamento(
            self.texel_face, self.pintado, self.faces, self.faces_uv,
            self.verts, self.alc)

    def test_pares_fantasma_esperados(self):
        esperado = _fantasmas_independentes(
            self.texel_face, self.faces, self.faces_uv, self.verts,
            self.tam)
        self.assertGreater(len(esperado), 0)
        self.assertEqual(self.est["pares_e2"], esperado)

    def test_grafo_simetrico_sem_lacos_nem_duplicados(self):
        vp, vi = self.est["viz_ptr"], self.est["viz_idx"]
        u = self.est["n_incognitas"]
        t_rep = np.repeat(np.arange(u), np.diff(vp))
        self.assertTrue(bool((t_rep != vi).all()))
        ida = set(zip(t_rep.tolist(), vi.tolist()))
        volta = set(zip(vi.tolist(), t_rep.tolist()))
        self.assertEqual(ida, volta)
        self.assertEqual(len(ida), len(vi))  # sem duplicados

    def test_e1_so_intra_face(self):
        tf = self.texel_face
        for a, b in self.est["pares_e1"]:
            self.assertEqual(tf.flat[a], tf.flat[b])
            la, ca = divmod(a, self.tam)
            lb, cb = divmod(b, self.tam)
            self.assertEqual(abs(la - lb) + abs(ca - cb), 1)

    def test_guarda_componente_sem_fronteira_exclui(self):
        # Duas ilhas numa grelha 8x8: a face 1 e declarada alcancavel
        # mas nenhum dos seus texeis tem vizinho de fronteira nem
        # acoplamento para a face 0 - a guarda de SS1.3 exclui-os e
        # conta-os; o texel isolado da face 2 (grau 0) idem.
        tf = -np.ones((8, 8), dtype=np.int32)
        tf[0:2, 0:2] = 0
        tf[5:7, 5:7] = 1
        tf[7, 0] = 2
        pin = np.zeros((8, 8), dtype=bool)
        pin[0:2, 0:2] = True
        alc = np.array([True, True, True])
        pares = CD.pares_e1(tf)
        est = CD.montar_estruturas(tf, pin, alc, pares)
        self.assertEqual(est["n_incognitas"], 0)
        self.assertEqual(est["excluidos_sem_acoplamento"], 5)


class TestDoadora(unittest.TestCase):
    @staticmethod
    def _adj(cadeia):
        adj = [[] for _ in range(len(cadeia))]
        for i, viz in enumerate(cadeia):
            adj[i] = np.array(sorted(viz), dtype=int)
        return adj

    def test_distancia_manda(self):
        adj = self._adj([[1], [0, 2], [1, 3], [2]])
        tem = np.array([True, False, False, True])
        cont = np.array([100, 0, 0, 1])
        d = CD.doadora_nomeada(adj, tem, cont)
        # Face 2 esta a anel 1 da face 3 (contagem 1) e a anel 2 da
        # face 0 (contagem 100): a distancia manda.
        self.assertEqual(int(d[2]), 3)
        self.assertEqual(int(d[1]), 0)

    def test_desempate_contagem_e_indice(self):
        adj = self._adj([[1], [0, 2], [1]])
        tem = np.array([True, False, True])
        d = CD.doadora_nomeada(adj, tem, np.array([3, 0, 7]))
        self.assertEqual(int(d[1]), 2)  # mesma distancia, maior contagem
        d = CD.doadora_nomeada(adj, tem, np.array([7, 0, 7]))
        self.assertEqual(int(d[1]), 0)  # mesmo tudo, menor indice

    def test_fonte_e_ela_propria_e_inalcancavel_menos_um(self):
        adj = self._adj([[1], [0], []])
        tem = np.array([True, False, False])
        d = CD.doadora_nomeada(adj, tem, np.array([1, 0, 0]))
        self.assertEqual(int(d[0]), 0)
        self.assertEqual(int(d[1]), 0)
        self.assertEqual(int(d[2]), -1)


class TestResolvedor(unittest.TestCase):
    def setUp(self):
        self.fx = FX.construir_fixture()
        _c, _t, _ct, _a, self.cores_final, _an, self.alc = \
            FX.produtos_preenchimento(self.fx)
        self.est = CD.construir_acoplamento(
            self.fx["texel_face"], self.fx["pintado"], self.fx["faces"],
            self.fx["faces_uv"], self.fx["verts"], self.alc)

    def test_contra_solucao_densa(self):
        tex, _pin, _apl = CD.escrever_campo(
            self.fx["textura"], self.fx["pintado"], self.est,
            CD.resolver_campo(self.est, self.fx["textura"],
                              self.cores_final)[0])
        self.assertTrue(_leitura_b(tex, self.est, self.fx))

    def test_chute_nao_altera_a_solucao(self):
        x1, _r1 = CD.resolver_campo(self.est, self.fx["textura"],
                                    self.cores_final)
        zeros = np.zeros_like(self.cores_final)
        x2, _r2 = CD.resolver_campo(self.est, self.fx["textura"], zeros)
        self.assertLessEqual(float(np.abs(x1 - x2).max()), 1e-8)

    def test_stop_nomeado_por_tecto(self):
        original = CD.MAX_ITERACOES
        CD.MAX_ITERACOES = 1
        try:
            with self.assertRaises(CD.CampoNaoConvergiu):
                CD.resolver_campo(self.est, self.fx["textura"],
                                  self.cores_final)
        finally:
            CD.MAX_ITERACOES = original


def _leituras(fx, tex, aplicada, estruturas):
    """As leituras (a)-(g) de SS3.2 sobre uma corrida do campo."""
    tf = fx["texel_face"]
    faixa = np.isin(tf, list(fx["faces_faixa"]))
    cegas_faixa = np.isin(tf, [2, 3, 4, 5, 6, 7]) & ~fx["pintado"]
    q2 = np.isin(tf, [4, 5])
    inalc = np.isin(tf, list(fx["faces_inalcancavel"]))
    leituras = {}
    leituras["a"] = bool(
        aplicada[cegas_faixa].all()
        and aplicada[tf == fx["face_cega_desligada"]].all())
    leituras["b"] = _leitura_b(tex, estruturas, fx)
    if (q2 & aplicada).any():
        media_q2 = CD.srgb_para_linear(tex[q2 & aplicada]).mean(axis=0)
        leituras["c"] = bool(media_q2[0] > 0.05 and media_q2[2] > 0.05)
    else:
        leituras["c"] = False  # Q2 sem campo: a costura nao foi cruzada
    g_faixa = tex[faixa & aplicada][:, 1]
    leituras["d"] = bool(len(g_faixa) == 0 or g_faixa.max() <= 1e-9)
    vals = tex[aplicada]
    leituras["e"] = bool(len(vals) == 0
                         or (vals.min() >= 0.0 and vals.max() <= 1.0))
    leituras["f"] = bool(
        (tex[fx["pintado"]] == fx["textura"][fx["pintado"]]).all())
    leituras["g"] = bool((~aplicada[inalc]).all()
                         and (tex[inalc] == fx["textura"][inalc]).all())
    return leituras


class TestFixture(unittest.TestCase):
    def setUp(self):
        self.fx = FX.construir_fixture()

    def test_leituras_a_g(self):
        tex, aplicada, est = _correr(self.fx)
        leituras = _leituras(self.fx, tex, aplicada, est)
        for nome in "abcdefg":
            self.assertTrue(leituras[nome], "leitura (%s) falhou" % nome)

    def test_mutante_a_sem_e2(self):
        # M-a: acoplamento sem fantasmas - a difusao fica confinada
        # as ilhas; Q2 (ilha sozinha) nao recebe campo: (a)/(c).
        tex, aplicada, est = _correr(self.fx, pares=CD.pares_e1(
            self.fx["texel_face"]))
        leituras = _leituras(self.fx, tex, aplicada, est)
        self.assertFalse(leituras["a"] and leituras["c"],
                         "M-a passou: o teste nao tem dentes")
        # Controlo limpo: as mesmas leituras passam.
        tex2, apl2, est2 = _correr(self.fx)
        limpo = _leituras(self.fx, tex2, apl2, est2)
        self.assertTrue(limpo["a"] and limpo["c"])

    def test_mutante_b_campo_em_srgb(self):
        # M-b: conversoes omitidas (o campo computado em sRGB) -
        # chumba em (b) na superficie fixada por C-2 (so morde porque
        # (b) compara os valores como escritos, com P2 na referencia).
        ident = lambda v: np.asarray(v, dtype=np.float64)  # noqa: E731
        tex, aplicada, est = _correr(
            self.fx, converter_entrada=ident, converter_saida=ident)
        self.assertFalse(_leitura_b(tex, est, self.fx),
                         "M-b passou: o teste nao tem dentes")
        tex2, _a2, est2 = _correr(self.fx)
        self.assertTrue(_leitura_b(tex2, est2, self.fx))

    def test_mutante_c_plano_pela_doadora(self):
        # M-c: atribuicao plana por face (o mecanismo A3) em vez do
        # campo - chumba em (b).
        _c, _t, _ct, _a, cores_final, _an, alc = \
            FX.produtos_preenchimento(self.fx)
        tex, _pin, _apl = PF.aplicar_preenchimento(
            self.fx["textura"], self.fx["pintado"], self.fx["texel_face"],
            cores_final, alc)
        est = CD.construir_acoplamento(
            self.fx["texel_face"], self.fx["pintado"], self.fx["faces"],
            self.fx["faces_uv"], self.fx["verts"], alc)
        self.assertFalse(_leitura_b(tex, est, self.fx),
                         "M-c passou: o teste nao tem dentes")

    def test_mutante_d_sem_restricao_de_componente(self):
        # M-d: acoplamento cuja vizinhanca de grelha ignora a face
        # (sem a restricao texel_face[u] == texel_face[t] que mantem
        # o campo dentro de cada componente): o verde Z da componente
        # desligada - cuja ilha esta colada a ilha A na grelha -
        # atravessa para a faixa: chumba em (d).
        tf = self.fx["texel_face"]
        t = tf.shape[0]
        pares = set()
        ok = tf[:, :-1] >= 0
        ls, cs = np.nonzero(ok & (tf[:, 1:] >= 0))
        for l, c in zip(ls.tolist(), cs.tolist()):
            a = l * t + c
            pares.add((a, a + 1))
        ok = tf[:-1, :] >= 0
        ls, cs = np.nonzero(ok & (tf[1:, :] >= 0))
        for l, c in zip(ls.tolist(), cs.tolist()):
            a = l * t + c
            pares.add((a, a + t))
        pares |= CD.propostas_e2(
            tf, self.fx["faces"], self.fx["faces_uv"], self.fx["verts"])[0]
        tex, aplicada, est = _correr(self.fx, pares=pares)
        leituras = _leituras(self.fx, tex, aplicada, est)
        self.assertFalse(leituras["d"],
                         "M-d passou: o teste nao tem dentes")
        tex2, apl2, est2 = _correr(self.fx)
        self.assertTrue(_leituras(self.fx, tex2, apl2, est2)["d"])


class TestMedicao(unittest.TestCase):
    def test_artefacto_esquema_e_recomputacao(self):
        caminho = AQUI / "campo_divergencia.json"
        self.assertTrue(caminho.is_file(),
                        "campo_divergencia.json nao existe - correr "
                        "testes/gerar_medicao_campo.py")
        doc = json.loads(caminho.read_text(encoding="utf-8"))
        self.assertIn("variantes", doc)
        for nome in ("binaria", "intermedia"):
            self.assertIn(nome, doc["variantes"])
            bloco = doc["variantes"][nome]
            self.assertEqual(len(bloco["fixture_sha256"]), 64)
            delta = np.array(bloco["delta"], dtype=np.float64)
            self.assertEqual(bloco["n"], len(delta))
            self.assertGreater(bloco["n"], 0)
            self.assertTrue(bool(np.isfinite(delta).all()))
            self.assertTrue(bool((np.diff(delta) >= 0).all()),
                            "o array publicado e o ordenado")
            self.assertAlmostEqual(
                bloco["mediana"], float(np.percentile(delta, 50)),
                places=12)
            self.assertAlmostEqual(
                bloco["p95"], float(np.percentile(delta, 95)), places=12)
            self.assertAlmostEqual(
                bloco["maximo"], float(delta.max()), places=12)
            # SEM assercao sobre os valores (SS3.3: medicao sem limiar).


def _validar_campo_difusao():
    """Extrai ``validar_campo_difusao`` de ``_blender_cor.py`` por
    AST e devolve a funcao compilada (o script importa ``bpy`` e
    corre ``main()`` na importacao - nao e importavel fora do
    Blender; padrao de extraccao da casa)."""
    fonte = (APP / "oficina3d" / "cor" / "_blender_cor.py").read_text(
        encoding="utf-8")
    arvore = ast.parse(fonte)
    for no in arvore.body:
        if isinstance(no, ast.FunctionDef) \
                and no.name == "validar_campo_difusao":
            modulo = ast.Module(body=[no], type_ignores=[])
            ns = {}
            exec(compile(modulo, "_blender_cor.py", "exec"), ns)
            return ns["validar_campo_difusao"]
    raise AssertionError("validar_campo_difusao nao encontrada em "
                         "_blender_cor.py")


class TestFlag(unittest.TestCase):
    def setUp(self):
        self.validar = _validar_campo_difusao()

    def test_omissao_e_desligado(self):
        self.assertEqual(self.validar({}, "3d"), "desligado")
        self.assertEqual(
            self.validar({"campo_difusao": "desligado"}, "uv"),
            "desligado")

    def test_k2plus_valido_no_3d(self):
        self.assertEqual(
            self.validar({"campo_difusao": "k2plus"}, "3d"), "k2plus")

    def test_desconhecido_e_erro(self):
        with self.assertRaises(ValueError):
            self.validar({"campo_difusao": "turbo"}, "3d")

    def test_k2plus_fora_do_3d_e_erro(self):
        with self.assertRaises(ValueError):
            self.validar({"campo_difusao": "k2plus"}, "uv")


if __name__ == "__main__":
    unittest.main()
