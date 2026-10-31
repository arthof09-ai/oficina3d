"""Testes de oficina3d.motores: a lista de pesos exigidos por tipo de motor
(a regressao de 31/10/2026: o hunyuan-mini constava disponivel sem o
config.yaml e morria ao rodar) e o formato publico de listar().
"""
import sys
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d import motores  # noqa: E402


class TestPesosNecessarios(unittest.TestCase):
    def test_hunyuan_exige_safetensors_e_config(self):
        spec = {"tipo": "hunyuan", "repo": "tencent/Hunyuan3D-2mini",
                "subpasta": "hunyuan3d-dit-v2-mini"}
        req = motores._pesos_necessarios(spec, flashvdm=False)
        self.assertIn(("tencent/Hunyuan3D-2mini", "hunyuan3d-dit-v2-mini/model.fp16.safetensors"), req)
        self.assertIn(("tencent/Hunyuan3D-2mini", "hunyuan3d-dit-v2-mini/config.yaml"), req)

    def test_hunyuan_com_flashvdm_soma_o_vae_turbo(self):
        spec = {"tipo": "hunyuan", "repo": "tencent/Hunyuan3D-2mv",
                "subpasta": "hunyuan3d-dit-v2-mv-turbo",
                "vae_turbo": ("tencent/Hunyuan3D-2mv", "hunyuan3d-vae-v2-mv-turbo")}
        req = motores._pesos_necessarios(spec, flashvdm=True)
        self.assertIn(("tencent/Hunyuan3D-2mv", "hunyuan3d-vae-v2-mv-turbo/model.fp16.safetensors"), req)
        sem = motores._pesos_necessarios(spec, flashvdm=False)
        self.assertNotIn(("tencent/Hunyuan3D-2mv", "hunyuan3d-vae-v2-mv-turbo/model.fp16.safetensors"), sem)

    def test_triposr_exige_ckpt_e_config(self):
        req = motores._pesos_necessarios({"tipo": "triposr"}, flashvdm=False)
        self.assertIn(("stabilityai/TripoSR", "model.ckpt"), req)
        self.assertIn(("stabilityai/TripoSR", "config.yaml"), req)

    def test_tipo_desconhecido_sem_pesos(self):
        self.assertEqual(motores._pesos_necessarios({"tipo": "outro"}, flashvdm=False), [])


class TestListar(unittest.TestCase):
    def test_os_cinco_motores_no_formato_publico(self):
        lista = motores.listar()
        self.assertEqual({m["nome"] for m in lista},
                         {"hunyuan-mv-turbo", "hunyuan-mini-turbo", "hunyuan-mini",
                          "hunyuan-mv", "triposr"})
        for m in lista:
            for chave in ("nome", "descricao", "disponivel", "aceita_multivista", "licenca"):
                self.assertIn(chave, m)


if __name__ == "__main__":
    unittest.main()
