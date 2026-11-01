"""Testes do T5 (lado .venv_app, sem Blender): xatlas sobre malhas pequenas.

O Orc real (49.750 tris) e provado pelos runners em jobs_teste/cor_t5, nao
pela suite: aqui o cubo basta para amarrar o contrato do .npz (ordem das
faces, uvs em [0, 1], um par de uv por vertice com costura) e as metricas.
"""
import json
import os
import sys
import tempfile
import unittest

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import trimesh  # noqa: E402
from oficina3d import uv_xatlas  # noqa: E402
from oficina3d.cor import projecao as P  # noqa: E402


def cubo():
    malha = trimesh.creation.box(extents=[2.0, 2.0, 2.0])
    return np.asarray(malha.vertices, dtype=np.float64), np.asarray(malha.faces, dtype=int)


class TestUvXatlas(unittest.TestCase):
    def test_parametrizar_preserva_faces_e_uv_em_01(self):
        verts, faces = cubo()
        vmapping, indices, uvs = uv_xatlas.parametrizar(verts, faces)
        self.assertEqual(indices.shape, faces.shape)
        self.assertEqual(len(uvs), len(vmapping))
        self.assertTrue(np.all(uvs >= -1e-6) and np.all(uvs <= 1.0 + 1e-6))
        # Cada face nova usa vertices do triangulo original (mesma geometria).
        for fi in range(len(faces)):
            novos = verts[vmapping[indices[fi]]]
            origem = verts[faces[fi]]
            self.assertTrue(np.allclose(np.sort(novos, axis=0), np.sort(origem, axis=0)))

    def test_metricas_cubo_sao_finitas_e_ocupacao_positiva(self):
        verts, faces = cubo()
        _, indices, uvs = uv_xatlas.parametrizar(verts, faces)
        faces_uv = uvs[indices]
        a, b, c = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
        areas = np.linalg.norm(np.cross(b - a, c - a), axis=1) * 0.5
        met = uv_xatlas.metricas(faces_uv, areas)
        self.assertEqual(met["triangulos"], len(faces))
        self.assertGreater(met["ocupacao"], 0.0)
        self.assertTrue(np.isfinite(met["distorcao_media"]))

    def test_gerar_uv_grava_npz_legivel(self):
        verts, faces = cubo()
        with tempfile.TemporaryDirectory() as tmp:
            glb = os.path.join(tmp, "cubo.glb")
            trimesh.Trimesh(vertices=verts, faces=faces).export(glb)
            npz = os.path.join(tmp, "cubo.npz")
            met = uv_xatlas.gerar_uv(glb, npz)
            with np.load(npz) as dados:  # fechar: no Windows, arquivo aberto trava o TemporaryDirectory
                idx_shape = dados["indices"].reshape(-1, 3).shape
                n_uvs = len(dados["uvs"])
                n_vmap = len(dados["vmapping"])
            self.assertEqual(idx_shape, faces.shape)
            self.assertEqual(n_uvs, n_vmap)
            self.assertEqual(met["triangulos"], len(faces))
            self.assertEqual(met["vertices_originais"], len(verts))

    def test_metricas_batem_com_projecao(self):
        # metricas() e so um empacotamento de P.metricas_uv + extras: a
        # distorcao e a ocupacao tem de ser identicas as da funcao base.
        verts, faces = cubo()
        _, indices, uvs = uv_xatlas.parametrizar(verts, faces)
        faces_uv = uvs[indices]
        a, b, c = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
        areas = np.linalg.norm(np.cross(b - a, c - a), axis=1) * 0.5
        base = P.metricas_uv(faces_uv, areas, 512)
        met = uv_xatlas.metricas(faces_uv, areas)
        self.assertEqual(met["distorcao_media"], base["distorcao_media"])
        self.assertEqual(met["ocupacao"], base["ocupacao"])
        self.assertEqual(met["ilhas"], base["ilhas"])


if __name__ == "__main__":
    unittest.main()


class TestUvMargemD_T5_1(unittest.TestCase):
    def test_margem_padrao_cubo_em_2048_cumpre_regua(self):
        # O cubo tem 6 ilhas grandes; o raster em 2048 e barato (12 faces).
        verts, faces = cubo()
        _, indices, uvs = uv_xatlas.parametrizar(verts, faces)
        faces_uv = uvs[indices]
        a, b, c = verts[faces[:, 0]], verts[faces[:, 1]], verts[faces[:, 2]]
        areas = np.linalg.norm(np.cross(b - a, c - a), axis=1) * 0.5
        met = P.metricas_uv(faces_uv, areas, 2048)
        self.assertIsNotNone(met["margem_min_px"])
        self.assertGreaterEqual(met["margem_min_px"], 8)

    def test_margem_sintetica_dois_quadrados_mede_o_gap(self):
        # Dois quadrados UV separados por um gap conhecido (0,01 em U):
        # o metodo tem de devolver uma faixa proporcional (~5-6 px em 512).
        # Valida o METODO de medicao (D-T5-6), nao o xatlas.
        q1 = np.array([[0.10, 0.10], [0.20, 0.10], [0.20, 0.20], [0.10, 0.20]])
        q2 = q1 + np.array([0.11, 0.0])
        faces_uv = np.array([
            [q1[0], q1[1], q1[2]], [q1[0], q1[2], q1[3]],
            [q2[0], q2[1], q2[2]], [q2[0], q2[2], q2[3]],
        ])
        areas = np.ones(4)
        met = P.metricas_uv(faces_uv, areas, 512)
        self.assertEqual(met["ilhas"], 2)
        self.assertIsNotNone(met["margem_min_px"])
        self.assertGreaterEqual(met["margem_min_px"], 4)
        self.assertLessEqual(met["margem_min_px"], 8)

    def test_gerar_uv_registra_parametros_do_empacotamento(self):
        verts, faces = cubo()
        with tempfile.TemporaryDirectory() as tmp:
            glb = os.path.join(tmp, "cubo.glb")
            trimesh.Trimesh(vertices=verts, faces=faces).export(glb)
            npz = os.path.join(tmp, "cubo.npz")
            met = uv_xatlas.gerar_uv(glb, npz)
            self.assertEqual(met["padding_px"], 8)
            self.assertEqual(met["resolucao"], 2048)
