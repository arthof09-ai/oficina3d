"""Testes de oficina3d.cor.costura (D7): medicao de costura e cor por face.

Sem Blender, sem arte do RPG: malhas sinteticas pequenas e texturas
pintadas a mao. O caso critico e a costura conhecida: dois triangulos
que compartilham a aresta 3D mas NAO o segmento UV tem de ser
classificados como costura; o mesmo par com UV compartilhada, como
interna. A distancia de cor tem de refletir a textura, nao a geometria.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d.cor import costura  # noqa: E402


def quadrado_costura():
    """Dois triangulos, um quadrado 3D, UV partida ao meio (costura).

    Vertices 3D: 0=(0,0,0), 1=(1,0,0), 2=(1,1,0), 3=(0,1,0).
    Faces: (0,1,2) e (0,2,3), aresta compartilhada 0-2.
    UV: face 0 usa o quadrado UV esquerdo; face 1, o direito: a aresta
    0-2 cai em segmentos UV diferentes -> costura.
    """
    faces = np.array([[0, 1, 2], [0, 2, 3]])
    faces_uv = np.array([
        [[0.0, 0.0], [0.4, 0.0], [0.4, 1.0]],
        [[0.6, 0.0], [1.0, 0.0], [0.6, 1.0]],
    ])
    return faces, faces_uv


def quadrado_interno():
    """Mesmo quadrado, UV continua: aresta 0-2 compartilhada na UV."""
    faces = np.array([[0, 1, 2], [0, 2, 3]])
    faces_uv = np.array([
        [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
        [[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]],
    ])
    return faces, faces_uv


class TestCostura(unittest.TestCase):
    def test_aresta_partida_e_costura_e_continua_e_interna(self):
        faces, fuv = quadrado_costura()
        pares, n_borda, n_nm = costura.classificar_arestas(faces, fuv)
        self.assertEqual(n_nm, 0)
        self.assertEqual(n_borda, 4)  # 4 lados do quadrado, 1 face cada
        self.assertEqual(len(pares), 1)
        self.assertTrue(pares[0][2])
        faces2, fuv2 = quadrado_interno()
        pares2, _, _ = costura.classificar_arestas(faces2, fuv2)
        self.assertEqual(len(pares2), 1)
        self.assertFalse(pares2[0][2])

    def test_cor_por_face_amostra_a_regiao_certa(self):
        # Textura 10x10: metade esquerda vermelha, direita azul.
        tex = np.zeros((10, 10, 3), dtype=np.uint8)
        tex[:, :5] = [255, 0, 0]
        tex[:, 5:] = [0, 0, 255]
        faces, fuv = quadrado_costura()
        cores = costura.cores_por_face(fuv, tex)
        # Face 0 vive no UV esquerdo -> vermelha; face 1, no direito -> azul.
        self.assertTrue(np.allclose(cores[0], [255, 0, 0], atol=1))
        self.assertTrue(np.allclose(cores[1], [0, 0, 255], atol=1))

    def test_descontinuidade_separa_costura_de_interna(self):
        tex = np.zeros((10, 10, 3), dtype=np.uint8)
        tex[:, :5] = [255, 0, 0]
        tex[:, 5:] = [0, 0, 255]
        faces, fuv = quadrado_costura()
        cores = costura.cores_por_face(fuv, tex)
        res = costura.descontinuidade(faces, fuv, cores)
        # Salto vermelho->azul na costura: sqrt(255^2 + 255^2) ~= 360.
        self.assertEqual(res["costura"]["n"], 1)
        self.assertGreater(res["costura"]["media"], 300)
        self.assertEqual(res["interna"]["n"], 0)
        faces2, fuv2 = quadrado_interno()
        cores2 = costura.cores_por_face(fuv2, tex)
        res2 = costura.descontinuidade(faces2, fuv2, cores2)
        self.assertEqual(res2["interna"]["n"], 1)
        # Na UV continua, as duas faces caem uma de cada lado da textura:
        # o salto interno existe (e o teste o registra), mas a
        # classificacao esta certa: n=1 interna, n=0 costura.
        self.assertEqual(res2["costura"]["n"], 0)

    def test_distancia_por_direcao_separa_alvo_de_controle(self):
        normais = np.array([[0.0, 0.0, 1.0], [0.0, 0.0, -1.0],
                            [1.0, 0.0, 0.0]])
        cores_a = np.array([[10.0, 10.0, 10.0], [10.0, 10.0, 10.0],
                            [10.0, 10.0, 10.0]])
        cores_b = np.array([[200.0, 10.0, 10.0], [10.0, 10.0, 10.0],
                            [10.0, 10.0, 10.0]])
        res = costura.distancia_cor_por_direcao(
            normais, cores_a, cores_b, np.array([0.0, 0.0, 1.0]))
        self.assertEqual(res["alvo"]["n"], 1)
        self.assertAlmostEqual(res["alvo"]["media"], 190.0)
        self.assertEqual(res["controle"]["n"], 1)
        self.assertAlmostEqual(res["controle"]["media"], 0.0)

    def test_vertice_duplicado_sem_solda_vira_borda_e_com_solda_classifica(self):
        # Quadrado com o vertice 0 duplicado como 4 (mesma posicao, ID
        # diferente) - o caso do GLB exportado que o Critico D2/D7 achou:
        # sem solda, a aresta compartilhada some (tudo vira borda);
        # com solda por posicao, ela e classificada (costura, UV partida).
        verts = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                          [1.0, 1.0, 0.0], [0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0]])
        faces = np.array([[0, 1, 2], [4, 2, 3]])
        faces_uv = np.array([
            [[0.0, 0.0], [0.4, 0.0], [0.4, 1.0]],
            [[0.6, 0.0], [1.0, 0.0], [0.6, 1.0]],
        ])
        pares, n_borda, n_nm = costura.classificar_arestas(faces, faces_uv)
        self.assertEqual(len(pares), 0)
        self.assertEqual(n_borda, 6)
        pares2, n_borda2, n_nm2 = costura.classificar_arestas(
            faces, faces_uv, verts=verts)
        self.assertEqual(len(pares2), 1)
        self.assertTrue(pares2[0][2])
        self.assertEqual(n_borda2, 4)
        self.assertEqual(n_nm2, 0)

    def test_piores_costuras_ordena_e_da_ponto_medio(self):
        tex = np.zeros((10, 10, 3), dtype=np.uint8)
        tex[:, :5] = [255, 0, 0]
        tex[:, 5:] = [0, 0, 255]
        faces, fuv = quadrado_costura()
        cores = costura.cores_por_face(fuv, tex)
        verts = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0],
                          [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]])
        piores = costura.piores_costuras(faces, fuv, cores, verts=verts, n=5)
        self.assertEqual(len(piores), 1)
        self.assertGreater(piores[0]["distancia"], 300)
        # Aresta compartilhada 0-2: ponto medio (0.5, 0.5, 0).
        self.assertTrue(np.allclose(piores[0]["ponto_medio"], [0.5, 0.5, 0.0]))

    def test_textura_rgba_usa_so_rgb(self):
        tex = np.zeros((4, 4, 4), dtype=np.uint8)
        tex[:, :, :3] = [7, 8, 9]
        tex[:, :, 3] = 0  # alfa zero nao pode apagar a cor
        faces, fuv = quadrado_interno()
        cores = costura.cores_por_face(fuv, tex)
        self.assertTrue(np.allclose(cores, [7, 8, 9]))


if __name__ == "__main__":
    unittest.main()
