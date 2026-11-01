"""Regressoes de colorimetria: tons medios reais, GLB e fonte ja linear."""
import os
from pathlib import Path
import sys
import tempfile
import unittest
import numpy as np
from PIL import Image
import trimesh

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP))
from oficina3d.cor import rodar_vertice, vertice as V
from oficina3d.refino.previa import achar_blender
from codex.glb_evidencia import ler_glb

class TestCurvaCor(unittest.TestCase):
    def test_tons_intermediarios_e_extremos(self):
        # Valores de referencia independentes, incluindo a zona linear escura.
        inp=np.array([0.,0.02,0.04045,0.5,1.])
        np.testing.assert_allclose(V.srgb_para_linear(inp),
            [0.,0.0015479876160990713,0.0031308049535603713,0.21404114048223255,1.],atol=1e-12)
        np.testing.assert_array_equal(inp,[0.,0.02,0.04045,0.5,1.])

    def test_oliva_nao_e_gravado_como_luz_linear_crua(self):
        actual=V.srgb_para_linear(np.array([137.,103.,58.])/255)
        np.testing.assert_allclose(actual,[0.2501582847,0.1356333297,0.0423114106],atol=1e-9)

@unittest.skipUnless(achar_blender(), 'Blender nao encontrado')
class TestCorGLBReal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from oficina3d import config
        root=config.BASE/'jobs_teste';root.mkdir(parents=True,exist_ok=True)
        cls.tmp=tempfile.TemporaryDirectory(prefix='cor_gamma_',dir=root)
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root=Path(cls.tmp.name)
        mesh=trimesh.creation.icosphere(subdivisions=1)
        # GLB Y-up: pivo nos pes, mesma geometria para forma/refinado.
        mesh.vertices[:,1]+=1
        mesh.export(cls.root/'refinado.glb')
        img=Image.new('RGBA',(32,32),(0,0,0,0))
        img.paste((137,103,58,255),(2,2,30,30));img.save(cls.root/'oliva.png')
        cls.from_png=cls.root/'png/modelo.glb';cls.from_png.parent.mkdir()
        cls.png_res=rodar_vertice({'modo':'glb','glb':str(cls.root/'refinado.glb'),
            'vistas':[{'vista':v,'arquivo':str(cls.root/'oliva.png')} for v in ['frente','costas','esquerda','direita']],
            'saida_glb':str(cls.from_png),'pasta_previas':str(cls.root/'png/previas'),'previas':[]},cls.root/'png')
        mesh.visual.vertex_colors=np.tile(np.array([64,32,16,255],dtype=np.uint8),(len(mesh.vertices),1))
        mesh.export(cls.root/'forma.glb')
        cls.from_forma=cls.root/'forma/modelo.glb';cls.from_forma.parent.mkdir()
        cls.forma_res=rodar_vertice({'modo':'glb','glb':str(cls.root/'refinado.glb'),
            'glb_forma':str(cls.root/'forma.glb'),'vistas':[],
            'saida_glb':str(cls.from_forma),'pasta_previas':str(cls.root/'forma/previas'),'previas':[]},cls.root/'forma')

    def test_png_real_exporta_oliva_linear(self):
        doc,prims=ler_glb(self.from_png)
        colors=np.vstack([p['COLOR_0'][:,:3] for p in prims])
        painted=colors[np.any(colors!=0,axis=1)]
        self.assertGreater(len(painted),20)
        np.testing.assert_allclose(painted,np.tile([0.2501582847,0.1356333297,0.0423114106],(len(painted),1)),atol=2e-5)
        self.assertEqual(len(doc.get('images',[])),0)
        self.assertEqual(self.png_res['espaco_cor']['atributo'],'linear')

    def test_forma_ja_linear_nao_sofre_segunda_conversao(self):
        _,prims=ler_glb(self.from_forma)
        colors=np.vstack([p['COLOR_0'][:,:3] for p in prims])
        # O importador glTF pode armazenar BYTE_COLOR (quantiza em sRGB).
        # Tolerancia de um passo de 8 bits; uma segunda curva daria erro ~0,20.
        np.testing.assert_allclose(colors,np.tile(np.array([64,32,16])/255,(len(colors),1)),atol=1/255)
        self.assertEqual(self.forma_res['cobertura']['pct']['forma'],100.)

if __name__=='__main__':unittest.main()
