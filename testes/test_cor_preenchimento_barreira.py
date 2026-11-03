"""Testes da P1.2 - preenchimento com barreiras territoriais.

Plano de testes da P1, secao 1.2 (U12-U19, malhas sinteticas) e 1.3
(U20, paridade guardiao com o artefato do laudo). U20 so roda quando a
variavel OFICINA3D_P1_PROVA aponta para um diretorio com
``territorios_orc.npz`` + ``modelo_uv.glb`` (a prova no job-ancora); sem
esses artefatos, o teste e pulado com o motivo - a suite nao pode
depender de um GLB de job para ficar verde num checkout limpo.
"""
import json
import os
import struct
import unittest
from pathlib import Path

import numpy as np

from oficina3d.cor import preenchimento as PF

VERMELHO = np.array([1.0, 0.0, 0.0])
AZUL = np.array([0.0, 0.0, 1.0])


def _adj_lista(vizinhos):
    """Adjacencia no formato do projeto (listas ordenadas de vizinhos)."""
    return [np.array(sorted(v), dtype=int) for v in vizinhos]


def _cores(n, fontes):
    cores = np.zeros((n, 3), dtype=np.float64)
    for f, cor in fontes.items():
        cores[f] = cor
    return cores


class TestDifundirBarreira(unittest.TestCase):
    def test_u12_ponte_cega_nao_entrega_em_territorio_alheio(self):
        # Cadeia 0(A, fonte) - 1(cega) - 2(cega) - 3(B): a onda de A
        # entrega nas cegas e PARA na parede B; a face 3 nunca recebe a
        # onda de A - e preenchida pela onda livre como ORFA rotulada
        # (politica das orfas do desenho, secao 3.3; correccao C-P1-2).
        adj = _adj_lista([[1], [0, 2], [1, 3], [2]])
        terr = np.array([0, -1, -1, 1], dtype=np.int8)
        tem = np.array([True, False, False, False])
        _c, anel, alc, _f, onda, classe = PF.difundir_barreira(
            adj, _cores(4, {0: VERMELHO}), tem, terr)
        self.assertTrue(alc[1] and alc[2])
        self.assertEqual(int(onda[1]), 0)
        self.assertEqual(int(onda[2]), 0)
        # Estado final julgado da face 3 (territorio B): alcancada,
        # classe ORFA, anel 3 (o anel da onda livre que a preencheu).
        self.assertTrue(alc[3])
        self.assertEqual(int(classe[3]), PF.ORFA)
        self.assertEqual(int(anel[3]), 3)
        # Propriedade de seguranca, explicita: B NAO recebe a onda de
        # A (onda 0); quem entrega em 3 e a onda livre (ONDA_LIVRE).
        self.assertEqual(int(onda[3]), PF.ONDA_LIVRE)
        self.assertNotEqual(int(onda[3]), 0)

    def test_u13_ilha_cercada_e_orfa_com_cor_livre(self):
        # Ilha A (face 1) cercada por B, fonte so em B (face 0, ligada
        # a ilha pela aresta 0-1 e ao resto por 0-2): a barreira nao
        # alcanca a ilha; a onda livre a preenche e a rotula ORFA.
        adj = _adj_lista([[1, 2], [0], [0]])
        terr = np.array([1, 0, 1], dtype=np.int8)
        tem = np.array([True, False, False])
        cores, anel, alc, _f, onda, classe = PF.difundir_barreira(
            adj, _cores(3, {0: AZUL}), tem, terr)
        self.assertTrue(alc[1])
        self.assertEqual(int(classe[1]), PF.ORFA)
        self.assertEqual(int(onda[1]), PF.ONDA_LIVRE)
        self.assertTrue((cores[1] == AZUL).all())
        # A face 2 (territorio da fonte) e BARREIRA, nao orfa.
        self.assertEqual(int(classe[2]), PF.BARREIRA)

    def test_u14_fonte_cega_so_entrega_em_faces_cegas(self):
        adj = _adj_lista([[1, 2], [0], [0]])
        terr = np.array([-1, 0, -1], dtype=np.int8)
        tem = np.array([True, False, False])
        _c, _a, alc, _f, onda, classe = PF.difundir_barreira(
            adj, _cores(3, {0: VERMELHO}), tem, terr)
        # A onda da fonte cega (onda -1) so entrega em faces cegas:
        # a face 2 (cega) recebe-a e e BARREIRA.
        self.assertTrue(alc[2])
        self.assertEqual(int(classe[2]), PF.BARREIRA)
        # A face 1 (territorio >= 0) e parede para a onda cega: acaba
        # preenchida pela onda livre como ORFA rotulada (politica das
        # orfas do desenho, secao 3.3; correccao C-P1-3).
        self.assertTrue(alc[1])
        self.assertEqual(int(classe[1]), PF.ORFA)
        self.assertEqual(int(onda[1]), PF.ONDA_LIVRE)
        # Propriedade de seguranca, explicita: a face territorial NAO
        # recebe a onda cega (-1).
        self.assertNotEqual(int(onda[1]), -1)

    def test_u15_componente_sem_fonte_fica_sem_fonte(self):
        adj = _adj_lista([[1], [0], []])
        terr = np.array([0, 0, 1], dtype=np.int8)
        tem = np.array([True, False, False])
        _c, anel, alc, _f, _o, classe = PF.difundir_barreira(
            adj, _cores(3, {0: VERMELHO}), tem, terr)
        self.assertFalse(alc[2])
        self.assertEqual(int(anel[2]), -1)
        self.assertEqual(int(classe[2]), PF.SEM_FONTE)

    def test_u16_barreira_vazia_e_difusao_livre(self):
        adj = _adj_lista([[1, 2], [0, 2], [0, 1]])
        terr = np.array([-1, -1, -1], dtype=np.int8)
        tem = np.array([True, False, False])
        c1, a1, alc1 = PF.difundir(adj, _cores(3, {0: VERMELHO}), tem)
        c2, a2, alc2, _f, _o, _cl = PF.difundir_barreira(
            adj, _cores(3, {0: VERMELHO}), tem, terr)
        self.assertTrue((c1 == c2).all())
        self.assertTrue((a1 == a2).all())
        self.assertTrue((alc1 == alc2).all())

    def test_u17_orcamento_sintetico_manual(self):
        # Cadeia 0(fonte A) - 1(cega) - 2(B, sem fonte): anel 1 na cega,
        # 2 inalcançavel por barreira e orfa pela livre (anel livre 2).
        adj = _adj_lista([[1], [0, 2], [1]])
        terr = np.array([0, -1, 1], dtype=np.int8)
        tem = np.array([True, False, False])
        _c, anel, alc, _f, _o, classe = PF.difundir_barreira(
            adj, _cores(3, {0: VERMELHO}), tem, terr)
        self.assertEqual(int(anel[1]), 1)
        self.assertEqual(int(anel[2]), 2)
        self.assertEqual(int(classe[2]), PF.ORFA)

    def test_u18_determinismo(self):
        adj = _adj_lista([[1, 2], [0, 2], [0, 1], []])
        terr = np.array([0, -1, 1, 0], dtype=np.int8)
        tem = np.array([True, False, False, False])
        r1 = PF.difundir_barreira(adj, _cores(4, {0: VERMELHO}), tem, terr)
        r2 = PF.difundir_barreira(adj, _cores(4, {0: VERMELHO}), tem, terr)
        for a, b in zip(r1, r2):
            self.assertTrue((np.asarray(a) == np.asarray(b)).all())

    def test_u19_classes_somam_e_nao_se_sobrepoem(self):
        adj = _adj_lista([[1], [0, 2], [1]])
        terr = np.array([0, -1, 1], dtype=np.int8)
        tem = np.array([True, False, False])
        _c, _a, _alc, _f, _o, classe = PF.difundir_barreira(
            adj, _cores(3, {0: VERMELHO}), tem, terr)
        total = sum(int((classe == v).sum())
                    for v in (PF.FONTE, PF.BARREIRA, PF.ORFA, PF.SEM_FONTE))
        self.assertEqual(total, 3)
        self.assertEqual(int((classe == PF.FONTE).sum()), 1)


# --- U20: paridade guardiao com o artefato do laudo -----------------------

def _ler_glb(caminho):
    """(verts (N,3) float64, faces (F,3) int) na ordem dos primitivos.

    Parser minimo de GLB (JSON + BIN), suficiente para o modelo_uv do
    ancora: POSITION float32, indices uint16/uint32, sem interleave.
    Nao usa trimesh: o parser nao pode reordenar nem fundir vertices,
    senao a chave de juncao (indice da face) muda em silencio.
    """
    bruto = Path(caminho).read_bytes()
    magia, _versao, _total = struct.unpack("<III", bruto[:12])
    if magia != 0x46546C67:
        raise ValueError("nao e GLB")
    tam, tipo = struct.unpack("<II", bruto[12:20])
    if tipo != 0x4E4F534A:
        raise ValueError("GLB sem bloco JSON")
    g = json.loads(bruto[20:20 + tam].decode("utf-8"))
    off = 20 + tam
    blen, _btype = struct.unpack("<II", bruto[off:off + 8])
    binario = bruto[off + 8:off + 8 + blen]

    def _acessor(indice):
        acc = g["accessors"][indice]
        vista = g["bufferViews"][acc["bufferView"]]
        base = vista.get("byteOffset", 0) + acc.get("byteOffset", 0)
        comp = {5120: "b", 5121: "B", 5122: "h", 5123: "H", 5125: "I",
                5126: "f"}[acc["componentType"]]
        tipos = {"SCALAR": 1, "VEC2": 2, "VEC3": 3, "VEC4": 4}
        n = acc["count"] * tipos[acc["type"]]
        fmt = "<" + comp * n
        vals = struct.unpack_from(fmt, binario, base)
        return np.array(vals, dtype=np.float64).reshape(acc["count"], tipos[acc["type"]])

    verts_list, faces_list = [], []
    for malha in g.get("meshes", []):
        for prim in malha.get("primitives", []):
            pos = _acessor(prim["attributes"]["POSITION"])
            idx = _acessor(prim["indices"]).astype(int).ravel()
            base = sum(len(v) for v in verts_list)
            verts_list.append(pos)
            faces_list.append((idx.reshape(-1, 3) + base))
    return (np.concatenate(verts_list, axis=0),
            np.concatenate(faces_list, axis=0).astype(int))


class TestParidadeLaudoU20(unittest.TestCase):
    def test_u20_paridade_com_npz_do_ancora(self):
        prova = os.environ.get("OFICINA3D_P1_PROVA")
        if not prova:
            self.skipTest("sem OFICINA3D_P1_PROVA (prova do job-ancora)")
        pasta = Path(prova)
        npz_path, glb_path = pasta / "territorios_orc.npz", pasta / "modelo_uv.glb"
        if not npz_path.is_file() or not glb_path.is_file():
            self.skipTest("artefatos do ancora ausentes em OFICINA3D_P1_PROVA")
        with np.load(npz_path, allow_pickle=False) as dados:
            terr = np.asarray(dados["territorio_face"])
            fonte_direta = np.asarray(dados["fonte_direta_face"], dtype=bool)
            anel_ref = np.asarray(dados["anel_bake_barreira"])
            onda_ref = np.asarray(dados["onda_bake_barreira"])
        verts, faces = _ler_glb(glb_path)
        self.assertEqual(len(faces), len(terr))
        adj = PF.adjacencia_faces(faces, verts)
        cores = np.zeros((len(faces), 3), dtype=np.float64)
        _c, anel, alc, _f, onda, classe = PF.difundir_barreira(
            adj, cores, fonte_direta, terr)
        # Onda 1 (barreira) tem de reproduzir o laudo EXATAMENTE; as
        # orfas sao as faces que a onda 1 nao alcanca (anel -1, nao-fonte).
        alc_barreira = anel_ref >= 0
        self.assertTrue((anel[alc_barreira] == anel_ref[alc_barreira]).all(),
                        "anel da onda de barreiras diverge do laudo")
        self.assertTrue((onda[alc_barreira] == onda_ref[alc_barreira]).all(),
                        "onda da onda de barreiras diverge do laudo")
        orfas = int((classe == PF.ORFA).sum())
        self.assertEqual(orfas, 254)
        preench = (classe == PF.BARREIRA)
        self.assertAlmostEqual(float(anel[preench].mean()), 3.24, places=2)
        self.assertEqual(int(anel[preench].max()), 21)


if __name__ == "__main__":
    unittest.main()
