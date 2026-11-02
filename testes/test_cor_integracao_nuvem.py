"""Contraprovas CPU antes/depois dos tres patches sobre a base COR-08/S2."""
import json
from pathlib import Path
import struct
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import numpy as np

from oficina3d.cor import vertice as V
from oficina3d.cor.validacao_vertice import verificar_glb_vertice
from testes.publicado_nuvem import fonte, funcao, modulo, ROOT


class TestIntegracaoCPU(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.antigo = modulo("oficina3d/cor/vertice.py")

    def test_c_cor01_leitor_byte_decodifica_e_float_preserva(self):
        # Simula somente a API de pixels. Exportacao Blender real continua pendente.
        def ler(codigo, is_float):
            px = np.array([.5, .5, .5, .5], dtype=np.float32)
            imagem = SimpleNamespace(size=(1, 1), channels=4, is_float=is_float,
                                     pixels=SimpleNamespace(foreach_get=lambda out: out.__setitem__(slice(None), px)))
            bpy = SimpleNamespace(data=SimpleNamespace(images=SimpleNamespace(
                load=lambda *a, **kw: imagem, remove=lambda im: None)))
            return funcao(codigo, "ler_imagem", {"np": np, "bpy": bpy, "V": V})("sintetico")
        antigo = fonte("oficina3d/cor/_blender_vertice.py")
        novo = (ROOT / "oficina3d/cor/_blender_vertice.py").read_text(encoding="utf-8")
        a, ma, _ = ler(antigo, False)
        b, mb, _ = ler(novo, False)
        f, mf, _ = ler(novo, True)
        np.testing.assert_allclose(a, .5)
        np.testing.assert_allclose(b, .21404114048223255)
        np.testing.assert_allclose(f, .5)
        np.testing.assert_array_equal(ma, mb)
        np.testing.assert_array_equal(ma, mf)

    def test_c_cor02_bilinear_muda_cor_preserva_fonte(self):
        im = np.array([[[0., 0., 0.], [1., 1., 1.]], [[1., 1., 1.], [0., 0., 0.]]])
        vistas = [dict(vista="frente", imagem=im, mascara=np.ones((2, 2), bool), visivel=np.ones(1, bool))]
        args = (np.zeros((1, 3)), np.array([[0., -1., 0.]]), vistas, np.zeros(3), 1.)
        with patch.object(V.P, "projetar", return_value=(np.array([1.]), np.array([1.]))), \
                patch.object(V.P, "alinhamento_silhueta", return_value=(1., 0., 1., 0.)):
            a = self.antigo.amostrar_vertices(*args)
            b = V.amostrar_vertices(*args)
            seco = V.amostrar_vertices(*args, amostragem="seco")
        np.testing.assert_array_equal(a[0], [[0., 0., 0.]])
        np.testing.assert_allclose(b[0], [[.5, .5, .5]])
        for i in range(3):
            np.testing.assert_array_equal(a[i], seco[i])
        np.testing.assert_array_equal(a[1], b[1])

    def test_c_guard01_nan_antes_aceito_agora_recusado(self):
        razoes = dict(x=1., y=1., z=1.)
        self.assertTrue(self.antigo.avaliar_alinhamento_forma([float("nan")], razoes)[0])
        self.assertFalse(V.avaliar_alinhamento_forma([float("nan")], razoes)[0])

    def test_c_guard01_contagens_cruzadas_antes_aceitas_agora_recusadas(self):
        verificar_antigo = funcao(fonte("oficina3d/cor/_blender_vertice.py"), "verificar_glb_vertice",
                                 {"json": json, "struct": struct})
        doc = {"meshes": [{"primitives": [
            {"attributes": {"POSITION": 0, "COLOR_0": 1}, "material": 0},
            {"attributes": {"POSITION": 2, "COLOR_0": 3}, "material": 0}]}],
            "accessors": [{"count": n, "type": t, "componentType": 5126}
                          for n, t in [(3, "VEC3"), (2, "VEC4"), (3, "VEC3"), (4, "VEC4")]],
            "materials": [{}]}
        data = json.dumps(doc).encode()
        data += b" " * (-len(data) % 4)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "estrutura.glb"
            path.write_bytes(struct.pack("<IIIII", 0x46546c67, 2, 20 + len(data), len(data), 0x4e4f534a) + data)
            a, b = verificar_antigo(path), verificar_glb_vertice(path)
        self.assertTrue(a["ok"])
        self.assertFalse(b["ok"])
        self.assertEqual(b["primitivos_sem_cor"], 2)
        self.assertEqual(b["color_0_vertices"], b["posicao_vertices"])


if __name__ == "__main__":
    unittest.main()
