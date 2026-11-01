"""Arestas reais da defesa COLOR_0 e da guarda de transferencia de cor."""
import copy
import json
import os
from pathlib import Path
import struct
import sys
import tempfile
import unittest
import numpy as np

APP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(APP))
from oficina3d.cor.validacao_vertice import verificar_glb_vertice
from oficina3d.cor.vertice import avaliar_alinhamento_forma

class TestDefesaColor0(unittest.TestCase):
    def setUp(self):
        from oficina3d import config
        root=config.BASE/'jobs_teste';root.mkdir(parents=True,exist_ok=True)
        self.tmp=tempfile.TemporaryDirectory(prefix='glb_guardas_',dir=root)
        self.addCleanup(self.tmp.cleanup)
        self.path=Path(self.tmp.name)/'teste.glb'
        # Fixture da estrutura JSON, nao de payload: este validador NAO
        # promete verificar geometria/binario (os testes colorimetricos o decodificam).
        self.doc={'asset':{'version':'2.0'},'meshes':[{'primitives':[
            {'attributes':{'POSITION':0,'COLOR_0':1},'material':0},
            {'attributes':{'POSITION':2,'COLOR_0':3},'material':0}]}],
            'accessors':[{'count':3,'type':'VEC3','componentType':5126},
                         {'count':3,'type':'VEC4','componentType':5126},
                         {'count':3,'type':'VEC3','componentType':5126},
                         {'count':3,'type':'VEC4','componentType':5126}], 'materials':[{}]}

    def verify(self,doc=None):
        data=json.dumps(self.doc if doc is None else doc).encode()
        data+=b' '*((-len(data))%4)
        self.path.write_bytes(struct.pack('<III',0x46546c67,2,20+len(data))+struct.pack('<II',len(data),0x4e4f534a)+data)
        return verificar_glb_vertice(self.path)

    def test_controle_multiplos_primitivos(self):
        self.assertTrue(self.verify()['ok'])

    def test_contagens_nao_podem_se_compensar(self):
        self.doc['accessors'][1]['count']=2
        self.doc['accessors'][3]['count']=4
        res=self.verify()
        self.assertFalse(res['ok']);self.assertEqual(res['primitivos_sem_cor'],2)
        self.assertEqual(res['color_0_vertices'],res['posicao_vertices'])

    def test_indices_negativos_bool_e_fora_da_lista(self):
        for index in [-1,True,999,1.0,None]:
            with self.subTest(index=index):
                self.doc['meshes'][0]['primitives'][1]['attributes']['COLOR_0']=index
                self.assertFalse(self.verify()['ok'])

    def test_todos_os_meshes_e_mesh_vazio(self):
        self.doc['meshes'].append({'primitives':[{'attributes':{'POSITION':0},'material':0}]})
        self.assertFalse(self.verify()['ok'])
        self.doc['meshes'][1]['primitives']=[]
        self.assertFalse(self.verify()['ok'])

    def test_acessor_ou_material_malformado(self):
        base=copy.deepcopy(self.doc)
        for change in ['count_zero','count_negativo','count_bool','tipo_cor','sem_normalizar','material']:
            with self.subTest(change=change):
                self.doc=copy.deepcopy(base)
                if change=='count_zero':self.doc['accessors'][1]['count']=0
                elif change=='count_negativo':self.doc['accessors'][1]['count']=-3
                elif change=='count_bool':self.doc['accessors'][1]['count']=True
                elif change=='tipo_cor':self.doc['accessors'][1]['type']='SCALAR'
                elif change=='sem_normalizar':self.doc['accessors'][1]['componentType']=5121
                elif change=='material':self.doc['meshes'][0]['primitives'][0]['material']=999
                self.assertFalse(self.verify()['ok'])

    def test_cor_inteira_normalizada_valida(self):
        self.doc['accessors'][1].update(componentType=5121,normalized=True)
        self.assertTrue(self.verify()['ok'])

    def test_arquivo_quebrado_recusa_sem_excecao(self):
        for data in [b'',b'glTF',struct.pack('<III',0x46546c67,2,20)+struct.pack('<II',0xffffffff,0x4e4f534a)]:
            with self.subTest(data=data):
                self.path.write_bytes(data)
                self.assertFalse(verificar_glb_vertice(self.path)['ok'])
        for doc in [[],{'meshes':None},{'meshes':[None]},{'meshes':[{'primitives':None}]}]:
            with self.subTest(doc=doc):self.assertFalse(self.verify(doc)['ok'])

class TestDistanciasValidas(unittest.TestCase):
    def test_nan_infinito_negativo_e_nao_numerico_recusam(self):
        for distances in [[float('nan')],[float('inf')],[-.1],['erro'],[[.01,.02]]]:
            with self.subTest(distances=distances):
                accepted,_,metrics=avaliar_alinhamento_forma(distances,dict(x=1,y=1,z=1))
                self.assertFalse(accepted)
                json.dumps(metrics,allow_nan=False)

    def test_numpy_e_gerador_sao_aceitos_sem_truth_value_ambiguo(self):
        for distances in [np.array([.001,.002]),(v for v in [.001,.002])]:
            self.assertTrue(avaliar_alinhamento_forma(distances,dict(x=1,y=1,z=1))[0])

    def test_razoes_nao_finitas_ou_nao_numericas_recusam(self):
        for ratio in [float('nan'),float('inf'),'erro',None]:
            with self.subTest(ratio=ratio):
                accepted,_,metrics=avaliar_alinhamento_forma([.001],dict(x=ratio,y=1,z=1))
                self.assertFalse(accepted);json.dumps(metrics,allow_nan=False)

if __name__=='__main__':unittest.main()
