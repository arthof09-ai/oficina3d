"""Testes do T2 (COR-07): matematica pura da cor de vertice, passo
``vertice`` da etapa cor (runner do Blender mockado), opcao ``cor_modo``
e despacho do worker. Nada aqui toca GPU; o Blender real e provado pelo
job de prova e pelo modo sintetico do script.
"""
import atexit
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

_BASE_TESTE = Path(os.environ.get("OFICINA3D_BASE") or r"C:\Users\txcga\RPG_Local\Oficina3D")
RAIZ_TESTE = _BASE_TESTE / "jobs_teste"


def _dentro(filho: Path, pai: Path) -> bool:
    f = os.path.normcase(os.path.abspath(filho))
    p = os.path.normcase(os.path.abspath(pai))
    return f.startswith(p + os.sep)


def _pasta_temporaria_dos_testes() -> Path:
    atual = os.environ.get("OFICINA3D_JOBS")
    if atual and _dentro(Path(atual), RAIZ_TESTE) and Path(atual).name.startswith("unittest_"):
        return Path(atual)
    RAIZ_TESTE.mkdir(exist_ok=True)
    p = Path(tempfile.mkdtemp(prefix="unittest_", dir=RAIZ_TESTE))
    os.environ["OFICINA3D_JOBS"] = str(p)
    atexit.register(shutil.rmtree, p, True)
    return p


TEMP_TESTES = _pasta_temporaria_dos_testes()

from oficina3d import cli, config, job, worker  # noqa: E402
from oficina3d.cor import passo, projecao as P, vertice as V  # noqa: E402

if os.path.normcase(str(config.JOBS)) != os.path.normcase(str(TEMP_TESTES)):
    raise RuntimeError(f"config.JOBS ({config.JOBS}) nao e a pasta temporaria dos testes; recuso rodar")


CORES = {"frente": (1.0, 0.0, 0.0), "costas": (0.0, 0.0, 1.0),
         "esquerda": (0.0, 1.0, 0.0), "direita": (1.0, 1.0, 0.0)}


def _vistas_solidas(n, nomes=("frente", "costas", "esquerda", "direita"), visivel=None):
    vistas = []
    for nome in nomes:
        img = np.zeros((100, 100, 3), dtype=np.float64)
        img[:] = CORES[nome]
        vistas.append({"vista": nome, "imagem": img,
                       "mascara": np.ones((100, 100), dtype=bool),
                       "visivel": np.ones(n, dtype=bool) if visivel is None else visivel})
    return vistas


class TestAmostrarVertices(unittest.TestCase):
    def _cena(self):
        # 4 vertices voltados para as vistas canonicas + polos de cima e
        # de baixo (sem facing para as vistas horizontais) - os polos dao
        # extensao vertical a caixa projetada (caixa degenerada levanta,
        # como no bake T1).
        centro = np.array([0.0, 0.0, 1.0])
        verts, normais = [], []
        for nome in ("frente", "costas", "esquerda", "direita"):
            d = np.array(P.direcao_camera(nome))
            verts.append(centro + d)
            normais.append(d)
        for d in (np.array([0.0, 0.0, 1.0]), np.array([0.0, 0.0, -1.0])):
            verts.append(centro + d)
            normais.append(d)
        return np.array(verts), np.array(normais), centro

    def test_cada_vertice_pinta_com_a_sua_vista(self):
        verts, normais, centro = self._cena()
        ortho = P.enquadramento((2.0, 2.0, 2.0), 100, 100)
        cores, fonte, _m, info = V.amostrar_vertices(
            verts, normais, _vistas_solidas(6), centro, ortho)
        for i, nome in enumerate(("frente", "costas", "esquerda", "direita")):
            self.assertEqual(fonte[i], V.FONTE_VISTA)
            np.testing.assert_allclose(cores[i], CORES[nome], atol=1e-9)
            self.assertEqual(info["vertices_por_vista"][nome], 1)

    def test_facing_baixo_nao_pinta(self):
        verts, normais, centro = self._cena()
        ortho = P.enquadramento((2.0, 2.0, 2.0), 100, 100)
        _c, fonte, _m, _i = V.amostrar_vertices(
            verts, normais, _vistas_solidas(6), centro, ortho)
        self.assertEqual(fonte[4], V.FONTE_NENHUMA)  # polo de cima
        self.assertEqual(fonte[5], V.FONTE_NENHUMA)  # polo de baixo

    def test_oculto_nao_pinta(self):
        verts, normais, centro = self._cena()
        ortho = P.enquadramento((2.0, 2.0, 2.0), 100, 100)
        vis = np.zeros(6, dtype=bool)
        _c, fonte, _m, _i = V.amostrar_vertices(
            verts, normais, _vistas_solidas(6, visivel=vis), centro, ortho)
        self.assertTrue((fonte == V.FONTE_NENHUMA).all())

    def test_mascara_vazia_nao_pinta(self):
        verts, normais, centro = self._cena()
        ortho = P.enquadramento((2.0, 2.0, 2.0), 100, 100)
        vistas = _vistas_solidas(6)
        for v in vistas:
            v["mascara"][:] = False
        _c, fonte, _m, info = V.amostrar_vertices(verts, normais, vistas, centro, ortho)
        self.assertTrue((fonte == V.FONTE_NENHUMA).all())
        self.assertTrue(all(v == 0 for v in info["vertices_por_vista"].values()))

    def test_desempate_primeira_vista_da_lista(self):
        centro = np.array([0.0, 0.0, 1.0])
        d = np.array(P.direcao_camera("frente")) + np.array(P.direcao_camera("esquerda"))
        d = d / np.linalg.norm(d)
        verts = np.array([centro + d, centro + np.array([0.0, 0.0, 1.0]),
                          centro + np.array([0.0, 0.0, -1.0])])
        normais = np.array([d, [0.0, 0.0, 1.0], [0.0, 0.0, -1.0]])
        ortho = P.enquadramento((2.0, 2.0, 2.0), 100, 100)
        cores, fonte, _m, _i = V.amostrar_vertices(
            verts, normais, _vistas_solidas(3, nomes=("frente", "esquerda")), centro, ortho)
        self.assertEqual(fonte[0], V.FONTE_VISTA)
        np.testing.assert_allclose(cores[0], CORES["frente"], atol=1e-9)


class TestMesclaEPropagacao(unittest.TestCase):
    def test_mesclar_forma_respeita_vista(self):
        cores = np.zeros((3, 3))
        fonte = np.array([V.FONTE_VISTA, V.FONTE_NENHUMA, V.FONTE_NENHUMA], dtype=np.int8)
        cores[0] = (1.0, 0.0, 0.0)
        forma = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [0.5, 0.5, 0.5]])
        n = V.mesclar_forma(cores, fonte, forma)
        self.assertEqual(n, 2)
        np.testing.assert_allclose(cores[0], (1.0, 0.0, 0.0))
        np.testing.assert_allclose(cores[1], (0.0, 0.0, 1.0))
        self.assertEqual(fonte[1], V.FONTE_FORMA)
        self.assertEqual(V.mesclar_forma(cores, fonte, None), 0)

    def test_propagacao_preenche_componente_e_isola_o_outro(self):
        # Dois triangulos ligados (0-1-2, 1-3-2) + um isolado (4-5-6).
        faces = np.array([[0, 1, 2], [1, 3, 2], [4, 5, 6]])
        cores = np.zeros((7, 3))
        fonte = np.zeros(7, dtype=np.int8)
        cores[0] = (0.2, 0.4, 0.6)
        fonte[0] = V.FONTE_VISTA
        n, passes = V.preencher_por_vizinhos(cores, fonte, faces)
        self.assertEqual(n, 3)  # vertices 1, 2 e 3
        self.assertTrue((fonte[:4] != V.FONTE_NENHUMA).all())
        self.assertTrue((fonte[4:] == V.FONTE_NENHUMA).all())
        resumo = V.resumo_cobertura(fonte)
        self.assertEqual(sum(resumo["por_fonte"].values()), 7)
        self.assertEqual(resumo["por_fonte"]["sem_cor"], 3)

    def test_propagacao_deterministica(self):
        faces = np.array([[0, 1, 2], [1, 3, 2], [2, 3, 4]])
        base_cores = np.zeros((5, 3))
        base_cores[0] = (0.9, 0.1, 0.3)
        base_fonte = np.zeros(5, dtype=np.int8)
        base_fonte[0] = V.FONTE_FORMA
        c1, f1 = base_cores.copy(), base_fonte.copy()
        V.preencher_por_vizinhos(c1, f1, faces)
        c2, f2 = base_cores.copy(), base_fonte.copy()
        V.preencher_por_vizinhos(c2, f2, faces)
        np.testing.assert_array_equal(c1, c2)
        np.testing.assert_array_equal(f1, f2)


class TestBaricentricas3d(unittest.TestCase):
    def test_centroide_e_cantos(self):
        a, b, c = (0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (0.0, 2.0, 0.0)
        w = V.baricentricas_3d((2.0 / 3, 2.0 / 3, 0.0), a, b, c)
        np.testing.assert_allclose(w, (1 / 3, 1 / 3, 1 / 3), atol=1e-9)
        np.testing.assert_allclose(V.baricentricas_3d(a, a, b, c), (1, 0, 0), atol=1e-9)

    def test_degenerado_devolve_none(self):
        self.assertIsNone(V.baricentricas_3d((0, 0, 0), (0, 0, 0), (1, 0, 0), (2, 0, 0)))


class TestPassoVertice(unittest.TestCase):
    def _forma_com_cor(self, tmp: Path) -> Path:
        import trimesh
        malha = trimesh.creation.box(extents=(1.0, 1.0, 1.0))
        cores = np.tile(np.array([[200, 30, 30, 255]], dtype=np.uint8),
                        (len(malha.vertices), 1))
        malha.visual = trimesh.visual.ColorVisuals(malha, vertex_colors=cores)
        p = tmp / "forma.glb"
        malha.export(str(p))
        return p

    def _fake_runner(self, escrever=True):
        def fake(pedido, pasta, progresso=None, timeout_s=900):
            if escrever:
                Path(pedido["saida_glb"]).write_bytes(b"glb-falso")
            return {"ok": True, "cobertura": {"total_vertices": 10, "por_fonte": {
                        "vista": 10, "forma": 0, "propagacao": 0, "sem_cor": 0},
                        "pct": {"vista": 100.0, "forma": 0.0, "propagacao": 0.0, "sem_cor": 0.0}},
                    "previas": [str(Path(pedido["pasta_previas"]) / "previa_cor_frente.png")],
                    "sha256_glb": "ab" * 32}
        return fake

    def test_sem_vistas_sem_forma_levanta(self):
        tmp = TEMP_TESTES / "vert_sem_nada"
        tmp.mkdir(exist_ok=True)
        refinado = tmp / "refinado.glb"
        refinado.write_bytes(b"x")
        with self.assertRaises(ValueError):
            passo.rodar_passo_vertice(tmp, refinado, [], pasta_cor=tmp / "cor")

    def test_sem_vistas_com_forma_prossegue_e_rotula(self):
        from oficina3d import cor as pacote_cor
        tmp = TEMP_TESTES / "vert_so_forma"
        tmp.mkdir(exist_ok=True)
        refinado = tmp / "refinado.glb"
        refinado.write_bytes(b"x")
        forma = self._forma_com_cor(tmp)
        original = pacote_cor.rodar_vertice
        pacote_cor.rodar_vertice = self._fake_runner()
        try:
            res = passo.rodar_passo_vertice(tmp, refinado, [], pasta_cor=tmp / "cor",
                                            glb_forma=forma)
        finally:
            pacote_cor.rodar_vertice = original
        self.assertEqual(res["modo_cor"], "vertice")
        self.assertEqual(res["rotulo"], "rascunho")
        self.assertEqual(res["vistas_usadas"], [])
        self.assertEqual(res["vistas_ausentes"], list(passo.VISTAS_COR))
        self.assertNotIn("textura", res["arquivos"])
        self.assertTrue(res["forma"]["color_0"])

    def test_com_vistas_repassa_ao_runner(self):
        from oficina3d import cor as pacote_cor
        tmp = TEMP_TESTES / "vert_com_vistas"
        tmp.mkdir(exist_ok=True)
        refinado = tmp / "refinado.glb"
        refinado.write_bytes(b"x")
        img = tmp / "frente.png"
        img.write_bytes(b"")
        capturado = {}

        def fake(pedido, pasta, progresso=None, timeout_s=900):
            capturado.update(pedido)
            return self._fake_runner()(pedido, pasta)

        original = pacote_cor.rodar_vertice
        pacote_cor.rodar_vertice = fake
        try:
            res = passo.rodar_passo_vertice(
                tmp, refinado, [{"arquivo": str(img), "vista": "frente"}],
                pasta_cor=tmp / "cor")
        finally:
            pacote_cor.rodar_vertice = original
        self.assertEqual([v["vista"] for v in capturado["vistas"]], ["frente"])
        self.assertIsNone(capturado["glb_forma"])
        self.assertEqual(res["vistas_usadas"], ["frente"])
        self.assertEqual(len(res["arquivos"]["previas"]), 1)

    def test_runner_sem_modelo_levanta_runtime(self):
        from oficina3d import cor as pacote_cor
        tmp = TEMP_TESTES / "vert_sem_modelo"
        tmp.mkdir(exist_ok=True)
        refinado = tmp / "refinado.glb"
        refinado.write_bytes(b"x")
        img = tmp / "frente.png"
        img.write_bytes(b"")
        original = pacote_cor.rodar_vertice
        pacote_cor.rodar_vertice = self._fake_runner(escrever=False)
        try:
            with self.assertRaises(RuntimeError):
                passo.rodar_passo_vertice(
                    tmp, refinado, [{"arquivo": str(img), "vista": "frente"}],
                    pasta_cor=tmp / "cor")
        finally:
            pacote_cor.rodar_vertice = original


class TestOpcaoCorModo(unittest.TestCase):
    def test_padrao_projecao(self):
        op, _ = job.validar_opcoes({}, "livre", ["frente"])
        self.assertEqual(op["cor_modo"], "projecao")

    def test_vertice_valido_e_desconhecido_rejeitado(self):
        op, _ = job.validar_opcoes({"cor_modo": "vertice"}, "livre", ["frente"])
        self.assertEqual(op["cor_modo"], "vertice")
        with self.assertRaises(ValueError):
            job.validar_opcoes({"cor_modo": "pintura-ia"}, "livre", ["frente"])


class TestCliCorModo(unittest.TestCase):
    def test_flag_cor_modo_no_enviar(self):
        a = cli.montar_parser().parse_args(
            ["enviar", "--cor-modo", "vertice", "--imagem", "a.png:frente"])
        self.assertEqual(a.cor_modo, "vertice")
        b = cli.montar_parser().parse_args(["enviar", "--imagem", "a.png:frente"])
        self.assertIsNone(b.cor_modo)


class TestWorkerDespachoCor(unittest.TestCase):
    def test_despacha_por_modo_e_rejeita_desconhecido(self):
        from oficina3d.cor import passo as passo_mod
        tmp = TEMP_TESTES / "vert_despacho"
        tmp.mkdir(exist_ok=True)
        glb = tmp / "m.glb"
        glb.write_bytes(b"x")
        chamadas = {}
        orig_v = passo_mod.rodar_passo_vertice
        orig_p = passo_mod.rodar_passo_cor
        passo_mod.rodar_passo_vertice = lambda *a, **k: chamadas.setdefault("v", k) or {"ok": True}
        passo_mod.rodar_passo_cor = lambda *a, **k: chamadas.setdefault("p", k) or {"ok": True}
        try:
            worker._etapa_cor(tmp, glb, [], modo="vertice", glb_forma=Path("forma.glb"))
            self.assertIn("v", chamadas)
            self.assertEqual(chamadas["v"].get("glb_forma"), Path("forma.glb"))
            worker._etapa_cor(tmp, glb, [], modo="projecao")
            self.assertIn("p", chamadas)
            with self.assertRaises(worker.ErroEtapa):
                worker._etapa_cor(tmp, glb, [], modo="pintura-ia")
        finally:
            passo_mod.rodar_passo_vertice = orig_v
            passo_mod.rodar_passo_cor = orig_p


if __name__ == "__main__":
    unittest.main()
