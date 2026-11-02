"""Testes-guarda do C-GUARD01 (Frente D, passo 2; re-mirados na
tranche 2b): sabotagens cruzadas contra o verificador
``verificar_glb_vertice``, agora importado do modulo puro
``oficina3d.cor.validacao_vertice`` (extraido na tranche 2b pelo
mecanismo de import do proprio script do Blender).

Historico: no passo 2 esta bateria carregava a funcao por extraccao
AST de ``_blender_vertice.py`` (o script do Blender nao e importavel
fora dele: importa ``bpy`` e executa ``main()`` na importacao). Com a
extraccao do verificador para o modulo puro, a bateria importa-o
directamente - contagem inalterada (4 testes).

Cobertura desta bateria (desenho julgado do passo 2):
- controlo: GLB valido de 2 primitivos e aceite;
- (i) 2.o primitivo sem COLOR_0 -> reprova;
- (ii) primitivo malformado (acessor invalido, acessor sem contagem,
  POSITION ausente) -> reprova SEM excepcao;
- (iii) COLOR_0 com contagem diferente de POSITION -> reprova.

Nota da re-miragem (tranche 2b, tabela CD-1 clausula 11): no
verificador extraido, ``primitivos_sem_cor`` conta QUALQUER violacao
por primitivo - incluindo a divergencia de contagem de (iii), que no
verificador agregado antigo contava 0 (so primitivos ilegiveis
contavam) e reprovava so pela soma. A assercao de (iii) acompanha a
semantica julgada: 1.

Fronteira: a igualdade de contagens POR primitivo (compensacao entre
primitivos, troca de acessores, contagem deslocada) corre na bateria
irma ``test_cor_guardas.py`` (tranche 2b), que nasceu da sonda
registada do passo 2 e da contraprova CD-2.
"""
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d.cor.validacao_vertice import verificar_glb_vertice


def doc_base():
    """GLB estrutural valido: 1 mesh, 2 primitivos 3/3, 1 material."""
    return {
        "asset": {"version": "2.0"},
        "meshes": [{"primitives": [
            {"attributes": {"POSITION": 0, "COLOR_0": 1}, "material": 0},
            {"attributes": {"POSITION": 2, "COLOR_0": 3}, "material": 0}]}],
        "accessors": [
            {"count": 3, "type": "VEC3", "componentType": 5126},
            {"count": 3, "type": "VEC4", "componentType": 5126},
            {"count": 3, "type": "VEC3", "componentType": 5126},
            {"count": 3, "type": "VEC4", "componentType": 5126}],
        "materials": [{}]}


def gravar_glb(caminho, doc):
    dados = json.dumps(doc).encode("utf-8")
    dados += b" " * ((-len(dados)) % 4)
    caminho.write_bytes(
        struct.pack("<III", 0x46546C67, 2, 20 + len(dados))
        + struct.pack("<II", len(dados), 0x4E4F534A) + dados)


class TestVerificarGlbVerticeGuard(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="glb_guard_")
        self.addCleanup(self.tmp.cleanup)
        self.caminho = Path(self.tmp.name) / "teste.glb"
        self.doc = doc_base()

    def verificar(self, doc=None):
        gravar_glb(self.caminho, self.doc if doc is None else doc)
        return verificar_glb_vertice(self.caminho)

    def test_controle_dois_primitivos_completos(self):
        res = self.verificar()
        self.assertTrue(res["ok"])
        self.assertTrue(res["color_0"])
        self.assertEqual(res["primitivos"], 2)
        self.assertEqual(res["primitivos_sem_cor"], 0)
        self.assertEqual(res["color_0_vertices"], 6)
        self.assertEqual(res["posicao_vertices"], 6)

    def test_segundo_primitivo_sem_color0_reprova(self):
        self.doc["meshes"][0]["primitives"][1]["attributes"] = {"POSITION": 2}
        res = self.verificar()
        self.assertFalse(res["ok"])
        self.assertFalse(res["color_0"])
        self.assertEqual(res["primitivos_sem_cor"], 1)

    def test_primitivo_malformado_reprova_sem_excecao(self):
        variantes = {}
        doc = doc_base()
        doc["meshes"][0]["primitives"][1]["attributes"]["COLOR_0"] = 999
        variantes["acessor_fora_da_lista"] = doc
        doc = doc_base()
        doc["accessors"][3] = {"type": "VEC4", "componentType": 5126}
        variantes["acessor_sem_contagem"] = doc
        doc = doc_base()
        doc["meshes"][0]["primitives"][1]["attributes"] = {"COLOR_0": 3}
        variantes["position_ausente"] = doc
        for nome, doc_sabotado in variantes.items():
            with self.subTest(variante=nome):
                res = self.verificar(doc_sabotado)
                self.assertFalse(res["ok"])
                self.assertEqual(res["primitivos_sem_cor"], 1)

    def test_contagem_color0_diferente_reprova(self):
        for nome, contagem in (("maior", 4), ("menor", 2)):
            with self.subTest(sentido=nome):
                doc = doc_base()
                doc["accessors"][3]["count"] = contagem
                res = self.verificar(doc)
                self.assertFalse(res["ok"])
                # Clausula 11 da tabela CD-1 (tranche 2b): a divergencia
                # de contagem por primitivo CONTA em primitivos_sem_cor
                # no verificador extraido (no agregado antigo contava 0).
                self.assertEqual(res["primitivos_sem_cor"], 1)


if __name__ == "__main__":
    unittest.main()
