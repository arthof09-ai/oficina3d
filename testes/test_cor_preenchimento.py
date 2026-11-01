"""COR-08/A3: preenchimento por adjacencia 3D (modulo preenchimento).

Malha sintetica com vertices DUPLICADOS por posicao (estilo GLB): a
adjacencia so existe com a solda de costura.py (L-24). Cadeia de faces
0-1-2 ligadas por arestas + face 3 isolada: a cor da face 0 tem de
chegar a 1 (anel 1) e a 2 (anel 2) e NUNCA a 3; os texels cegos das
faces alcancaveis herdam a cor difundida; os da isolada, nao.
"""
import unittest

import numpy as np

from oficina3d.cor import preenchimento as PF

VERMELHO = np.array([1.0, 0.0, 0.0])


def _malha():
    # Posicoes: quadrado A B C D + extensao E; isolada G H I.
    # Indices duplicados de proposito (split de GLB): a solda e por posicao.
    verts = np.array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0],   # face 0: A B C
        [1, 0, 0], [1, 1, 0], [0, 1, 0],   # face 1: B D C (aresta B-C)
        [1, 0, 0], [1, 1, 0], [2, 0, 0],   # face 2: B D E (aresta B-D)
        [5, 5, 5], [6, 5, 5], [5, 6, 5],   # face 3: isolada
    ], dtype=float)
    faces = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]])
    # Ilhas UV separadas numa textura 16x16.
    faces_uv = np.array([
        [[0.0, 0.0], [0.25, 0.0], [0.0, 0.25]],
        [[0.3, 0.0], [0.55, 0.0], [0.3, 0.25]],
        [[0.6, 0.0], [0.85, 0.0], [0.6, 0.25]],
        [[0.0, 0.6], [0.25, 0.6], [0.0, 0.85]],
    ])
    return verts, faces, faces_uv


class TestPreenchimento(unittest.TestCase):
    def setUp(self):
        self.verts, self.faces, self.faces_uv = _malha()
        self.tamanho = 16
        self.mapa = PF.mapa_texel_face(self.faces_uv, self.tamanho)

    def test_mapa_texel_face(self):
        self.assertTrue((self.mapa[self.mapa >= 0] >= 0).all())
        for f in range(4):
            self.assertGreater(int((self.mapa == f).sum()), 0)
        # Fora das ilhas: -1.
        self.assertEqual(int(self.mapa[15, 15]), -1)

    def test_adjacencia_com_solda(self):
        adj = PF.adjacencia_faces(self.faces, self.verts)
        self.assertEqual(adj[0].tolist(), [1])
        self.assertEqual(sorted(adj[1].tolist()), [0, 2])
        self.assertEqual(adj[2].tolist(), [1])
        self.assertEqual(adj[3].tolist(), [])

    def test_cores_diretas_media(self):
        tex = np.zeros((16, 16, 3))
        pin = np.zeros((16, 16), dtype=bool)
        sel0 = self.mapa == 0
        tex[sel0] = VERMELHO
        pin[sel0] = True
        cores, tem, contagem = PF.cores_diretas_por_face(tex, pin, self.mapa, 4)
        self.assertTrue(tem[0])
        self.assertTrue(np.allclose(cores[0], VERMELHO))
        self.assertFalse(tem[1:].any())
        self.assertEqual(int(contagem[0]), int(sel0.sum()))

    def test_difusao_em_cadeia(self):
        cores = np.zeros((4, 3))
        cores[0] = VERMELHO
        tem = np.array([True, False, False, False])
        adj = PF.adjacencia_faces(self.faces, self.verts)
        finais, anel, alc = PF.difundir(adj, cores, tem)
        self.assertEqual(anel.tolist(), [0, 1, 2, -1])
        self.assertTrue(np.allclose(finais[1], VERMELHO))
        self.assertTrue(np.allclose(finais[2], VERMELHO))
        self.assertFalse(alc[3])
        # Determinismo: segunda difusao identica.
        finais2, anel2, _ = PF.difundir(adj, cores, tem)
        self.assertTrue((finais == finais2).all() and (anel == anel2).all())

    def test_aplicar_so_nas_alcancaveis(self):
        tex = np.zeros((16, 16, 3))
        pin = np.zeros((16, 16), dtype=bool)
        sel0 = self.mapa == 0
        tex[sel0] = VERMELHO
        pin[sel0] = True
        cores, tem, _ = PF.cores_diretas_por_face(tex, pin, self.mapa, 4)
        adj = PF.adjacencia_faces(self.faces, self.verts)
        finais, _anel, alc = PF.difundir(adj, cores, tem)
        tex2, pin2, aplicada = PF.aplicar_preenchimento(
            tex, pin, self.mapa, finais, alc)
        # Faces 1 e 2 preenchidas; face 3 intocada.
        self.assertTrue(pin2[self.mapa == 1].all())
        self.assertTrue(pin2[self.mapa == 2].all())
        self.assertFalse(pin2[self.mapa == 3].any())
        self.assertTrue(np.allclose(tex2[self.mapa == 2], VERMELHO))
        self.assertEqual(int(aplicada.sum()),
                         int((self.mapa == 1).sum() + (self.mapa == 2).sum()))
        # O direto original nao foi sobrescrito nem contado como aplicado.
        self.assertFalse(aplicada[sel0].any())

    def test_dominio_exclui_face_inalcancavel(self):
        # A dilatacao restrita cobre a faixa em torno da UV mas NUNCA os
        # texels de uma face de componente sem fonte (face 3, isolada):
        # preenche-la por UV importaria cor de outra parte do corpo.
        alc = np.array([True, True, True, False])
        dominio = PF.dominio_dilatacao_restrita(
            self.mapa >= 0, self.mapa, alc, passes=1)
        self.assertFalse(dominio[self.mapa == 3].any())
        # Faixa: vizinho imediato de uma ilha alcancavel entra no dominio.
        vizinhos = np.zeros((16, 16), dtype=bool)
        vizinhos[self.mapa == 0] = True
        expandida = PF.expandir_mascara(vizinhos, 1)
        self.assertTrue(dominio[expandida & (self.mapa < 0)].any())
        # Longe de qualquer ilha: fora do dominio.
        self.assertFalse(dominio[15, 15])

    def test_dominio_passe_zero_e_area_uv_menos_inalcancavel(self):
        alc = np.array([True, True, True, False])
        dominio = PF.dominio_dilatacao_restrita(
            self.mapa >= 0, self.mapa, alc, passes=0)
        esperado = (self.mapa >= 0) & (self.mapa != 3)
        self.assertTrue((dominio == esperado).all())

    def test_expandir_mascara_sem_wrap(self):
        m = np.zeros((5, 5), dtype=bool)
        m[0, 0] = True
        e1 = PF.expandir_mascara(m, 1)
        self.assertTrue(e1[0, 0] and e1[1, 0] and e1[0, 1])
        self.assertFalse(e1[4, 0] or e1[0, 4])
        e2 = PF.expandir_mascara(m, 2)
        self.assertTrue(e2[2, 0] and e2[0, 2] and e2[1, 1])


if __name__ == "__main__":
    unittest.main()
