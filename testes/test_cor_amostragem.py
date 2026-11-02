"""Regressoes de amostragem: centros, luz linear, borda e mascara."""
import sys
from pathlib import Path
import unittest
from unittest.mock import patch
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from oficina3d.cor import vertice as V

class TestBilinear(unittest.TestCase):
    def test_centros_e_media_linear(self):
        im=np.array([[[0.,0.,0.],[1.,1.,1.]],[[1.,1.,1.],[0.,0.,0.]]])
        got=V.amostrar_bilinear(im,np.ones((2,2),bool),np.array([.5,1.5,1.]),np.array([.5,.5,1.]))
        np.testing.assert_allclose(got,[[0,0,0],[1,1,1],[.5,.5,.5]])

    def test_fundo_nao_contamina_e_borda_nao_atravessa(self):
        im=np.ones((2,2,3));im[0,0]=[.1,.2,.3]
        mask=np.zeros((2,2),bool);mask[0,0]=True
        got=V.amostrar_bilinear(im,mask,np.array([.9,0.]),np.array([.9,0.]))
        np.testing.assert_allclose(got,[[.1,.2,.3]]*2)

    def test_imagem_de_um_pixel(self):
        got=V.amostrar_bilinear(np.array([[[.2,.3,.4]]]),np.ones((1,1),bool),np.array([0.,.99]),np.array([0.,.99]))
        np.testing.assert_allclose(got,[[.2,.3,.4]]*2)

    def test_pipeline_default_bilinear_e_controle_seco(self):
        im=np.array([[[0.,0.,0.],[1.,1.,1.]],[[1.,1.,1.],[0.,0.,0.]]])
        views=[dict(vista='frente',imagem=im,mascara=np.ones((2,2),bool),visivel=np.ones(1,bool))]
        with patch.object(V.P,'projetar',return_value=(np.array([1.]),np.array([1.]))),patch.object(V.P,'alinhamento_silhueta',return_value=(1.,0.,1.,0.)):
            args=(np.zeros((1,3)),np.array([[0.,-1.,0.]]),views,np.zeros(3),1.)
            a=V.amostrar_vertices(*args);b=V.amostrar_vertices(*args,amostragem='seco')
            np.testing.assert_allclose(a[0],[[.5,.5,.5]])
            np.testing.assert_allclose(b[0],[[0.,0.,0.]])
            np.testing.assert_array_equal(a[1],b[1])
            with self.assertRaises(ValueError):V.amostrar_vertices(*args,amostragem='erro')

if __name__=='__main__':unittest.main()
