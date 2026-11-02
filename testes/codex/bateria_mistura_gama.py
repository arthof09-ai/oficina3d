"""Bateria explicita T1 gama. Executar diretamente: bake conhecido pode reprovar.
Fora do discover test_*.py enquanto tranche esta PARADA, sem expectedFailure.
"""
import sys,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from oficina3d.cor import vertice as V, preenchimento as PF

OBSERVACOES_BAKE=[]

class TestMisturaVertice(unittest.TestCase):
    def verificar(self,peso,esperado):
        srgb=np.repeat(np.array([[[.25],[.75]]]),3,axis=2)
        linear=V.srgb_para_linear(srgb)
        vistas=[dict(vista='frente',imagem=linear,mascara=np.ones((1,2),bool),visivel=np.ones(1,bool))]
        with patch.object(V.P,'projetar',return_value=(np.array([.5+peso]),np.array([.5]))),patch.object(V.P,'alinhamento_silhueta',return_value=(1.,0.,1.,0.)):
            cores,_,_,_=V.amostrar_vertices(np.zeros((1,3)),np.array([[0.,-1.,0.]]),vistas,np.zeros(3),1.)
        np.testing.assert_allclose(cores,[[esperado]*3],rtol=0,atol=1e-12)
    def test_meio(self):self.verificar(.5,.2866988210699744)
    def test_pesos_25_75(self):self.verificar(.75,.40461018751918326)

class TestMisturaBake(unittest.TestCase):
    def verificar(self,tons,esperado):
        # Contrato real do bake: textura byte/sRGB como float 0..1,
        # media dos texels diretos e aplicada ao texel cego da mesma face.
        tex=np.repeat(np.array([[*tons,0.]])[...,None],3,axis=2)
        pin=np.array([[True]*len(tons)+[False]])
        mapa=np.zeros(pin.shape,dtype=int)
        cores,tem,cont=PF.cores_diretas_por_face(tex,pin,mapa,1)
        got,_,aplicada=PF.aplicar_preenchimento(tex,pin,mapa,cores,tem)
        OBSERVACOES_BAKE.append({'tons_srgb':list(tons),'saida_medida_srgb':got[0,-1].tolist(),'referencia_srgb':esperado})
        self.assertEqual(int(cont[0]),len(tons));self.assertTrue(aplicada[0,-1])
        np.testing.assert_array_equal(got[pin],tex[pin])
        np.testing.assert_allclose(got[0,-1],[esperado]*3,rtol=0,atol=1e-12)
    def test_meio(self):self.verificar([.25,.75],.5718735140718357)
    def test_pesos_25_75(self):self.verificar([.25,.75,.75,.75],.6686320581212071)

if __name__=='__main__':unittest.main(verbosity=2)
