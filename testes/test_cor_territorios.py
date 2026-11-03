"""Testes da P1.1/P1 - mapa de territorios (``cor/mapa_territorios.py``).

Plano de testes da P1, secao 1.1 (U1-U11): carga validada por SHA/faces/
vistas, matriz de fatores e vetos de parametros. Nada aqui toca GPU nem
Blender: o mapa e um .npz sintetico montado no teste (o .npz real do
ancora so entra na prova U20, em test_cor_preenchimento_barreira.py).
"""
import hashlib
import io
import os
import tempfile
import unittest
from pathlib import Path

import numpy as np

from oficina3d.cor import mapa_territorios as MT


def _npz_sintetico(path, glb_sha="a" * 64, n_faces=5,
                   vistas=("frente", "costas", "esquerda", "direita"),
                   territorio=None, dist_geo=None):
    """Monta um .npz com o formato do artefato do laudo P1 §5."""
    if territorio is None:
        territorio = np.array([0, 1, -1, 2, 3], dtype=np.int8)
    if dist_geo is None:
        dist_geo = np.array([0.0, 0.03, 0.015, 0.06, 0.0], dtype=np.float32)
    np.savez(
        path,
        glb_sha256=np.array(glb_sha),
        vistas=np.array(list(vistas)),
        territorio_face=np.asarray(territorio, dtype=np.int8),
        dist_geo_fronteira=np.asarray(dist_geo, dtype=np.float32),
        facing=np.zeros((n_faces, 4), dtype=np.float32),
        fronteira_face=np.zeros(n_faces, dtype=bool),
        texel_territorio=np.zeros((2, 2), dtype=np.int8),
        texel_vencedor=np.zeros((2, 2), dtype=np.int8),
        texel_anel_fronteira=np.zeros((2, 2), dtype=np.int16),
    )


class TestMapaTerritorios(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)
        self.glb = b"GLB-FALSO-PARA-TESTE"
        self.sha = hashlib.sha256(self.glb).hexdigest()

    def tearDown(self):
        self.tmp.cleanup()

    def _caminho(self, nome="mapa.npz", **kw):
        p = self.dir / nome
        _npz_sintetico(p, glb_sha=self.sha, **kw)
        return p

    def test_u1_npz_valido_carrega(self):
        mapa = MT.carregar_mapa(self._caminho(), self.glb, 5)
        self.assertEqual(mapa.territorio_face.shape, (5,))
        self.assertEqual(mapa.facing.shape, (5, 4))
        self.assertEqual(mapa.glb_sha256, self.sha)
        self.assertEqual(mapa.sha_npz, hashlib.sha256(
            (self.dir / "mapa.npz").read_bytes()).hexdigest())

    def test_u2_glb_com_1_byte_alterado_recusa(self):
        p = self._caminho()
        with self.assertRaises(MT.MapaIncompativel):
            MT.carregar_mapa(p, b"GLB-FALSO-PARA-TESTF", 5)

    def test_u3_faces_divergentes_recusam(self):
        with self.assertRaises(MT.MapaIncompativel):
            MT.carregar_mapa(self._caminho(), self.glb, 6)

    def test_u4_vistas_trocadas_recusam(self):
        p = self._caminho(vistas=("frente", "costas", "esquerda", "cima"))
        with self.assertRaises(MT.MapaIncompativel):
            MT.carregar_mapa(p, self.glb, 5)

    def test_u5_fator_autoridade_e_1(self):
        mapa = MT.carregar_mapa(self._caminho(), self.glb, 5)
        fator = MT.fator_territorial(mapa, 0.6, 0.03)
        # Face 0 tem territorio 0 (frente): fator[0, 0] == 1,0 exato.
        self.assertEqual(float(fator[0, 0]), 1.0)

    def test_u6_fator_face_cega_e_1_para_toda_vista(self):
        mapa = MT.carregar_mapa(self._caminho(), self.glb, 5)
        fator = MT.fator_territorial(mapa, 0.6, 0.03)
        self.assertTrue((fator[2] == 1.0).all())

    def test_u7_fator_disputa_na_fronteira_e_1(self):
        mapa = MT.carregar_mapa(self._caminho(), self.glb, 5)
        fator = MT.fator_territorial(mapa, 0.6, 0.03)
        # Face 0 (territorio 0, dist 0.0) disputada por qualquer vista:
        # na fronteira a corrida e pura.
        self.assertEqual(float(fator[0, 1]), 1.0)

    def test_u8_fator_disputa_no_interior_e_piso(self):
        mapa = MT.carregar_mapa(self._caminho(), self.glb, 5)
        fator = MT.fator_territorial(mapa, 0.6, 0.03)
        # A matriz e float32 por desenho julgado: a igualdade exacta
        # exige-se no dominio f32 da matriz (f32(0,6) alargado para
        # float64 e 0.6000000238418579 - errata C-P1-1 ao plano U8).
        # Face 1 (territorio 1, dist 0.03 == d_ref) disputada pela frente.
        self.assertEqual(fator[1, 0], np.float32(0.6))
        # Face 3 (territorio 2, dist 0.06 >= d_ref) disputada pela frente.
        self.assertEqual(fator[3, 0], np.float32(0.6))

    def test_u9_fator_monotonico_em_dist_geo(self):
        # Rampa de distancias na mesma disputa: fator nao-crescente.
        dist = np.array([0.0, 0.01, 0.02, 0.03, 0.06], dtype=np.float32)
        terr = np.array([1, 1, 1, 1, 1], dtype=np.int8)
        p = self._caminho(n_faces=5, territorio=terr, dist_geo=dist)
        mapa = MT.carregar_mapa(p, self.glb, 5)
        fator = MT.fator_territorial(mapa, 0.6, 0.03)
        coluna = fator[:, 0]  # disputa pela frente contra territorio 1
        self.assertTrue((np.diff(coluna) <= 0).all())

    def test_u10_piso_fora_da_faixa_vetada_recusa(self):
        mapa = MT.carregar_mapa(self._caminho(), self.glb, 5)
        with self.assertRaises(ValueError):
            MT.fator_territorial(mapa, 0.4, 0.03)
        with self.assertRaises(ValueError):
            MT.fator_territorial(mapa, 1.0, 0.03)
        with self.assertRaises(ValueError):
            MT.fator_territorial(mapa, 0.6, 0.0)

    def test_u11_determinismo_do_fator(self):
        mapa = MT.carregar_mapa(self._caminho(), self.glb, 5)
        a = MT.fator_territorial(mapa, 0.6, 0.03)
        b = MT.fator_territorial(mapa, 0.6, 0.03)
        self.assertTrue((a == b).all())
        self.assertEqual(a.tobytes(), b.tobytes())

    def test_c_p1_4_guarda_da_disputa_v3_exclui_face_cega(self):
        # C-P1-4: a contagem de disputa da proveniencia v3 (em
        # _blender_cor) usa a definicao do laudo
        # (adocao/p1/territorios.py:622): texel direto de face CEGA
        # (territorio -1) NAO e disputa - sem a guarda, ele contava.
        # O contador vive inline no entrypoint do Blender; o teste
        # fixa a formula sobre arrays construidos E prende a expressao
        # guardada no codigo de producao.
        direto = np.array([True, True, True])
        texel_face = np.array([0, 1, 2])
        terr_tex = np.array([-1, 0, 0])
        vencedor = np.array([0, 1, 0])
        sem_guarda = int((direto & (texel_face >= 0)
                          & (vencedor != terr_tex)).sum())
        com_guarda = int((direto & (texel_face >= 0) & (terr_tex >= 0)
                          & (vencedor != terr_tex)).sum())
        self.assertEqual(sem_guarda, 2)   # a face cega contava como disputa
        self.assertEqual(com_guarda, 1)   # com a guarda, so a disputa real
        fonte = (Path(__file__).resolve().parents[1] / "oficina3d" / "cor"
                 / "_blender_cor.py").read_text(encoding="utf-8")
        self.assertIn("& (terr_tex >= 0) & (vencedor != terr_tex)", fonte)

    def test_fator_para_pedido_reordena_por_nome(self):
        mapa = MT.carregar_mapa(self._caminho(), self.glb, 5)
        fator = MT.fator_territorial(mapa, 0.6, 0.03)
        reord = MT.fator_para_pedido(fator, ["direita", "frente", "costas", "esquerda"])
        # Coluna 0 do reordenado = coluna 3 (direita) do original.
        self.assertTrue((reord[:, 0] == fator[:, 3]).all())
        self.assertTrue((reord[:, 1] == fator[:, 0]).all())
        with self.assertRaises(ValueError):
            MT.fator_para_pedido(fator, ["frente", "cima"])


if __name__ == "__main__":
    unittest.main()
