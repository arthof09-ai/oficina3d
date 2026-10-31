"""Testes do refino (oficina3d.refino). Sem arte do RPG: malhas e imagens geradas aqui.

Rodar (cwd = app):  py -3.12 -m unittest discover -s testes -p "test_refino.py" -v

- IoU, PBM, PNG e GLB: Python puro (rodam em qualquer Python 3.10+).
- refinar() de ponta a ponta: precisa do Blender (pula se não houver).
- Caminho pymeshlab: precisa de numpy + trimesh + pymeshlab (pula se não houver).
Temporários em <Oficina3D>\\jobs_teste\\teste_refino_<pid>\\ (apagados no fim;
OFICINA3D_MANTER_TESTE=1 mantém para inspeção).
"""
from __future__ import annotations

import os
import shutil
import sys
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d.refino import malha, previa, silhueta  # noqa: E402

JOBS_TESTE = Path(os.environ.get("OFICINA3D_JOBS_TESTE") or (APP.parent / "jobs_teste"))
BLENDER = previa.achar_blender()


def _pasta_temp(nome: str) -> Path:
    p = JOBS_TESTE / f"teste_refino_{os.getpid()}" / nome
    if p.exists():
        shutil.rmtree(p)
    p.mkdir(parents=True)
    return p


def _limpar_temp():
    if os.environ.get("OFICINA3D_MANTER_TESTE") == "1":
        return
    raiz = JOBS_TESTE / f"teste_refino_{os.getpid()}"
    if raiz.exists():
        shutil.rmtree(raiz, ignore_errors=True)


def tearDownModule():  # noqa: N802 — nome exigido pelo unittest
    _limpar_temp()


# ----------------------------------------------------------------------------
# Geometria sintética (glTF: Y para cima, frente +Z)
# ----------------------------------------------------------------------------
H_FORMA = 2.0


def _z_frente(y: float) -> float:
    """A frente (+Z) avança para cima: perfil lateral em trapézio (assimétrico)."""
    return 0.2 + 0.4 * (y / H_FORMA)


def forma_trapezio(aneis: int = 30, por_lado: int = 10, desloc=(5.0, 3.0, -1.0), buraco=True, pedaco=True):
    """Tubo de seção retangular (x em [-0,2; 0,2], z em [-0,2; z_frente(y)]), tampas em leque.

    ``buraco``: tira 2 triângulos da tampa de cima (malha aberta, como o FlashVDM).
    ``pedaco``: acrescenta um tetraedro solto e pequeno longe do corpo (floater).
    """
    dx, dy, dz = desloc
    verts, faces = [], []

    def perimetro(y):
        a, zb, zf = 0.2, -0.2, _z_frente(y)
        pts = []
        cantos = [(-a, zb), (a, zb), (a, zf), (-a, zf)]
        for i in range(4):
            (x0, z0), (x1, z1) = cantos[i], cantos[(i + 1) % 4]
            for k in range(por_lado):
                t = k / por_lado
                pts.append((x0 + (x1 - x0) * t, z0 + (z1 - z0) * t))
        return pts

    m = 4 * por_lado
    for r in range(aneis + 1):
        y = H_FORMA * r / aneis
        for x, z in perimetro(y):
            verts.append((x + dx, y + dy, z + dz))
    for r in range(aneis):
        for i in range(m):
            a = r * m + i
            b = r * m + (i + 1) % m
            c = a + m
            d = b + m
            faces += [(a, b, d), (a, d, c)]
    # tampas
    cb = len(verts)
    verts.append((dx, dy, (-0.2 + _z_frente(0)) / 2 + dz))
    ct = len(verts)
    verts.append((dx, H_FORMA + dy, (-0.2 + _z_frente(H_FORMA)) / 2 + dz))
    topo = aneis * m
    tampa_cima = []
    for i in range(m):
        faces.append((cb, (i + 1) % m, i))
        tampa_cima.append((ct, topo + i, topo + (i + 1) % m))
    faces += tampa_cima[2:] if buraco else tampa_cima
    if pedaco:
        b0 = len(verts)
        s = 0.02
        px, py, pz = dx + 3.0, dy + 0.5, dz
        verts += [(px, py, pz), (px + s, py, pz), (px, py + s, pz), (px, py, pz + s)]
        faces += [(b0, b0 + 2, b0 + 1), (b0, b0 + 1, b0 + 3), (b0, b0 + 3, b0 + 2), (b0 + 1, b0 + 2, b0 + 3)]
    return verts, faces


def imagem_vista(vista: str, caminho: Path, largura=220, altura=300):
    """Silhueta ideal da forma_trapezio na vista pedida (PNG RGBA, fundo transparente)."""
    k = 120.0          # px por unidade
    base = 270         # linha dos pés
    x0 = 20
    px = []
    for row in range(altura):
        y = (base - row) / k
        linha = []
        for col in range(largura):
            dentro = False
            if 0 <= y <= H_FORMA:
                u = (col - x0) / k  # unidades a partir da borda esquerda da área
                if vista == "esquerda":     # câmera +X: frente (+Z) à ESQUERDA da imagem
                    z = 0.6 - u
                    dentro = -0.2 <= z <= _z_frente(y)
                elif vista == "direita":    # câmera −X: frente à direita
                    z = u - 0.2
                    dentro = -0.2 <= z <= _z_frente(y)
                else:                       # frente/costas: retângulo de 0,4 de largura
                    dentro = 0.0 <= u <= 0.4
            linha.append((200, 180, 160, 255) if dentro else (0, 0, 0, 0))
        px.append(linha)
    silhueta.salvar_png(px, caminho, canais=4)
    return caminho


# ----------------------------------------------------------------------------
class TestIoUPuro(unittest.TestCase):
    def test_iguais(self):
        a = [[0, 1, 1], [0, 1, 0]]
        self.assertEqual(silhueta.iou(a, a), 1.0)

    def test_disjuntas(self):
        self.assertEqual(silhueta.iou([[1, 0], [0, 0]], [[0, 0], [0, 1]]), 0.0)

    def test_parcial(self):
        a = [[1, 1, 0, 0]]
        b = [[0, 1, 1, 0]]
        self.assertAlmostEqual(silhueta.iou(a, b), 1 / 3)

    def test_aceita_bool(self):
        self.assertAlmostEqual(silhueta.iou([[True, False]], [[True, True]]), 0.5)

    def test_vazias(self):
        self.assertEqual(silhueta.iou([[0, 0]], [[0, 0]]), 0.0)

    def test_tamanho_diferente(self):
        with self.assertRaises(ValueError):
            silhueta.iou([[1, 0]], [[1], [0]])

    def test_recortar_caixa(self):
        m = [[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]]
        self.assertEqual(silhueta.caixa(m), (1, 1, 3, 3))
        self.assertEqual(silhueta.recortar(m), [[1, 1], [0, 1]])
        self.assertEqual(silhueta.recortar([[0, 0]]), [])

    def test_redimensionar_espelhar(self):
        m = [[1, 0], [0, 1]]
        self.assertEqual(silhueta.redimensionar(m, 4, 2), [[1, 1, 0, 0], [0, 0, 1, 1]])
        self.assertEqual(silhueta.espelhar([[1, 0, 0]]), [[0, 0, 1]])
        self.assertEqual(silhueta.area(m), 2)

    def test_alinhado_ignora_escala_e_posicao(self):
        # Mesmo retângulo 1:3, em tamanhos e posições diferentes -> IoU ~1.
        img = [[1 if 2 <= x < 6 and 1 <= y < 13 else 0 for x in range(20)] for y in range(16)]
        mod = [[1 if 10 <= x < 18 and 5 <= y < 29 else 0 for x in range(30)] for y in range(32)]
        r = silhueta.iou_alinhado(img, mod)
        self.assertGreater(r["iou"], 0.97)

    def test_alinhado_detecta_espelho(self):
        # "L": pé apontando para a esquerda na imagem e para a direita no modelo.
        def bota(pe_esquerda):
            m = []
            for y in range(20):
                linha = []
                for x in range(12):
                    corpo = 4 <= x < 8
                    pe = y >= 16 and ((0 <= x < 8) if pe_esquerda else (4 <= x < 12))
                    linha.append(1 if corpo or pe else 0)
                m.append(linha)
            return m
        r = silhueta.iou_alinhado(bota(True), bota(False))
        self.assertGreater(r["iou_espelhada"], r["iou"] + 0.05)
        self.assertGreater(r["iou_espelhada"], 0.95)

    def test_alinhado_vazia(self):
        r = silhueta.iou_alinhado([[0, 0]], [[1, 1]])
        self.assertEqual(r["iou"], 0.0)
        self.assertEqual(r["vazia"], "imagem")


class TestNota(unittest.TestCase):
    def test_lateral_e_costas(self):
        n = silhueta.nota_iou({"frente": 0.95, "esquerda": 0.7, "direita": 0.8, "costas": 0.6})
        self.assertAlmostEqual(n["iou_lateral"], 0.75)
        self.assertAlmostEqual(n["iou_costas"], 0.6)
        self.assertAlmostEqual(n["nota_iou"], 0.675)

    def test_so_um_lado(self):
        n = silhueta.nota_iou({"esquerda": 0.8})
        self.assertAlmostEqual(n["nota_iou"], 0.8)
        self.assertIsNone(n["iou_costas"])

    def test_frente_sozinha_nao_vira_nota(self):
        self.assertIsNone(silhueta.nota_iou({"frente": 0.9})["nota_iou"])


class TestArquivosPuros(unittest.TestCase):
    def setUp(self):
        self.pasta = _pasta_temp("puros")

    def test_pbm_ida_e_volta(self):
        m = [[1, 0, 1, 1, 0, 0, 0, 1, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1]]
        p = silhueta.salvar_pbm(m, self.pasta / "m.pbm")
        self.assertEqual(silhueta.ler_pbm(p), m)
        (self.pasta / "t.pbm").write_bytes(b"P1\n# comentario\n3 2\n1 0 1\n0 1 0\n")
        self.assertEqual(silhueta.ler_pbm(self.pasta / "t.pbm"), [[1, 0, 1], [0, 1, 0]])

    def test_png_assinatura(self):
        p = silhueta.salvar_png([[(255, 0, 0), (0, 255, 0)]], self.pasta / "a.png")
        self.assertTrue(p.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))

    def test_glb_ida_e_volta(self):
        v, f = forma_trapezio(aneis=4, por_lado=2, buraco=False, pedaco=False)
        p = malha.escrever_glb(v, f, self.pasta / "f.glb")
        info = malha.info_glb(p)
        self.assertEqual(info["triangulos"], len(f))
        self.assertEqual(info["vertices"], len(v))
        self.assertAlmostEqual(info["caixa"]["max"][1] - info["caixa"]["min"][1], H_FORMA, places=5)
        self.assertFalse(info["tem_uv"])

    def test_glb_invalido(self):
        (self.pasta / "x.glb").write_bytes(b"nao e glb nenhum")
        with self.assertRaises(ValueError):
            malha.info_glb(self.pasta / "x.glb")


class TestConvencaoVistas(unittest.TestCase):
    def test_blender(self):
        self.assertEqual(previa.direcao_camera("frente"), (0.0, -1.0, 0.0))
        self.assertEqual(previa.direcao_camera("esquerda"), (1.0, 0.0, 0.0))   # lado esquerdo = +X
        self.assertEqual(previa.direcao_camera("direita"), (-1.0, 0.0, 0.0))
        self.assertEqual(previa.direcao_camera("costas"), (0.0, 1.0, 0.0))

    def test_gltf(self):
        self.assertEqual(previa.direcao_camera("frente", "gltf"), (0.0, 0.0, 1.0))  # frente +Z
        self.assertEqual(previa.direcao_camera("costas", "gltf"), (0.0, 0.0, -1.0))
        self.assertEqual(previa.direcao_camera("cima", "gltf"), (0.0, 1.0, 0.0))

    def test_vista_desconhecida(self):
        with self.assertRaises(ValueError):
            previa.direcao_camera("detalhe")


class TestRefinarErros(unittest.TestCase):
    def test_entrada_inexistente(self):
        from oficina3d.refino import ErroRefino, refinar
        pasta = _pasta_temp("erros")
        with self.assertRaises(ErroRefino):
            refinar(pasta / "nao_existe.glb", pasta / "refino", pasta / "saida", {})


@unittest.skipUnless(BLENDER, "Blender não encontrado")
class TestRefinarBlender(unittest.TestCase):
    """Ponta a ponta com o Blender, limpeza pelo próprio Blender (backend_malha='blender')."""

    @classmethod
    def setUpClass(cls):
        from oficina3d.refino import refinar
        cls.job = _pasta_temp("job")
        (cls.job / "entrada").mkdir()
        v, f = forma_trapezio()
        cls.n_tri = len(f)
        cls.glb = malha.escrever_glb(v, f, cls.job / "forma.glb")
        imagens = []
        for vista in ("frente", "costas", "esquerda", "direita"):
            arq = imagem_vista(vista, cls.job / "entrada" / f"{vista}.png")
            imagens.append({"arquivo": str(arq), "vista": vista})
        imagens.append({"arquivo": "entrada/nao_existe.png", "vista": "costas-esquerda"})
        cls.passos = []
        cls.res = refinar(cls.glb, cls.job / "refino", cls.job / "saida",
                          {"alvo_triangulos": 1000, "altura_m": None, "simetrizar": False,
                           "backend_malha": "blender"},
                          imagens=imagens, progresso=lambda p, m: cls.passos.append((p, m)))

    def test_glb_e_triangulos(self):
        m = self.res["metricas"]
        self.assertTrue(Path(self.res["glb"]).is_file())
        self.assertEqual(m["triangulos_antes"], self.n_tri)
        self.assertLessEqual(m["triangulos_depois"], 1000)
        self.assertGreater(m["triangulos_depois"], 200)

    def test_fechada_e_limpa(self):
        m = self.res["metricas"]
        self.assertFalse(m["fechada_antes"])
        self.assertTrue(m["fechada"], self.res["avisos"])
        self.assertGreaterEqual(m["componentes_removidos"], 1)

    def test_normalizacao(self):
        m = self.res["metricas"]
        self.assertAlmostEqual(m["altura"], 1.0, places=3)
        self.assertEqual(m["pivo"], "pes", m["pivo_centro_base"])
        info = malha.info_glb(self.res["glb"])
        mn, mx = info["caixa"]["min"], info["caixa"]["max"]
        self.assertAlmostEqual(mn[1], 0.0, places=3)                 # pés em Y = 0
        self.assertAlmostEqual((mn[0] + mx[0]) / 2, 0.0, places=3)   # centrado em X
        self.assertAlmostEqual((mn[2] + mx[2]) / 2, 0.0, places=3)   # centrado em Z
        # proporção preservada: profundidade 0,8 / altura 2 -> 0,4
        self.assertAlmostEqual(mx[2] - mn[2], 0.4, places=2)
        self.assertTrue(info["tem_uv"])

    def test_previas(self):
        nomes = sorted(p.name for p in self.res["previas"])
        self.assertEqual(nomes, sorted(f"previa_{v}.png" for v in previa.VISTAS_PREVIA))
        for p in self.res["previas"]:
            self.assertGreater(p.stat().st_size, 1000)

    def test_iou_e_convencao(self):
        iou = self.res["silhueta_iou"]
        for v in ("frente", "costas", "esquerda", "direita"):
            self.assertGreater(iou[v], 0.9, (v, iou))
        # A frente (+Z) tem de aparecer à ESQUERDA da imagem na vista "esquerda".
        d = self.res["silhueta_detalhe"]["esquerda"]
        self.assertGreater(d["iou"], d["iou_espelhada"] + 0.05, d)
        self.assertTrue(Path(d["comparacao"]).is_file())
        self.assertGreater(self.res["nota_iou"], 0.9)
        self.assertEqual(self.res["metricas"]["nota_iou"], self.res["nota_iou"])
        self.assertFalse(any("trocada" in a for a in self.res["avisos"]), self.res["avisos"])
        self.assertTrue(any("costas-esquerda" in a for a in self.res["avisos"]))

    def test_progresso(self):
        pcts = [p for p, _ in self.passos]
        self.assertEqual(pcts[-1], 100)
        self.assertEqual(pcts, sorted(pcts))


@unittest.skipUnless(BLENDER, "Blender não encontrado")
class TestRefinarSimetriaSemUV(unittest.TestCase):
    def test_simetrizar(self):
        from oficina3d.refino import refinar
        job = _pasta_temp("job_sim")
        v, f = forma_trapezio(aneis=12, por_lado=6, pedaco=False)
        glb = malha.escrever_glb(v, f, job / "forma.glb")
        res = refinar(glb, job / "refino", job / "saida",
                      {"alvo_triangulos": 400, "altura_m": 1.8, "simetrizar": True, "uv": False,
                       "backend_malha": "blender", "previas": ["frente"]})
        m = res["metricas"]
        self.assertLessEqual(m["triangulos_depois"], 400)
        self.assertAlmostEqual(m["altura"], 1.8, places=3)
        self.assertTrue(m["fechada"], res["avisos"])
        self.assertEqual(m["pivo"], "pes")
        self.assertIsNone(res["nota_iou"])
        self.assertEqual([p.name for p in res["previas"]], ["previa_frente.png"])


@unittest.skipUnless(BLENDER and malha.pymeshlab_disponivel(), "precisa de Blender + numpy/trimesh/pymeshlab")
class TestRefinarPymeshlab(unittest.TestCase):
    def test_backend_pymeshlab(self):
        from oficina3d.refino import refinar
        job = _pasta_temp("job_pml")
        v, f = forma_trapezio()
        glb = malha.escrever_glb(v, f, job / "forma.glb")
        res = refinar(glb, job / "refino", job / "saida",
                      {"alvo_triangulos": 1000, "backend_malha": "pymeshlab", "previas": ["frente"]})
        m = res["metricas"]
        self.assertEqual(m["backend_malha"], "pymeshlab")
        self.assertLessEqual(m["triangulos_depois"], 1000)
        self.assertTrue(m["fechada"], res["avisos"])
        self.assertEqual(m["pivo"], "pes")


if __name__ == "__main__":
    unittest.main(verbosity=2)
