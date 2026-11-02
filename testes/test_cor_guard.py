"""Testes-guarda do C-GUARD01 (Frente D, passo 2): sabotagens cruzadas
re-miradas ao verificador actual ``verificar_glb_vertice`` de
``oficina3d/cor/_blender_vertice.py`` (linha 314).

O script do Blender nao e importavel fora dele (importa ``bpy`` e
executa ``main()`` na importacao, linha 588), por isso a funcao e
carregada por extraccao AST do fonte real: parse do ficheiro e
compilacao so do ``FunctionDef`` do verificador, com ``json``/``struct``
no namespace. O que corre aqui e o codigo exacto publicado, sem
executar o script e sem tocar em codigo de producao.

Cobertura desta bateria (desenho julgado do passo 2):
- controlo: GLB valido de 2 primitivos e aceite;
- (i) 2.o primitivo sem COLOR_0 -> reprova;
- (ii) primitivo malformado (acessor invalido, acessor sem contagem,
  POSITION ausente) -> reprova SEM excepcao;
- (iii) COLOR_0 com contagem diferente de POSITION -> reprova.

Fronteira declarada: a igualdade de contagens POR primitivo
(compensacao entre primitivos, troca de acessores, contagem deslocada)
NAO esta nesta bateria; corre como sonda registada do passo 2 (ver
REGISTRO da Frente D) porque o verificador actual so impoe igualdade
AGREGADA - a sonda e o veiculo da escalacao desse defeito, sem deixar
testes vermelhos permanentes a corromper a regua D-1.
"""
import ast
import json
import struct
import sys
import tempfile
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

FONTE_VERIFICADOR = APP / "oficina3d" / "cor" / "_blender_vertice.py"


def carregar_verificador(caminho_fonte):
    """Extrai e compila ``verificar_glb_vertice`` do fonte dado."""
    arvore = ast.parse(Path(caminho_fonte).read_text(encoding="utf-8"))
    for no in arvore.body:
        if isinstance(no, ast.FunctionDef) and no.name == "verificar_glb_vertice":
            modulo = ast.Module(body=[no], type_ignores=[])
            namespace = {"json": json, "struct": struct}
            exec(compile(modulo, str(caminho_fonte), "exec"), namespace)
            return namespace["verificar_glb_vertice"]
    raise AssertionError(
        f"verificar_glb_vertice nao encontrado em {caminho_fonte}")


verificar_glb_vertice = carregar_verificador(FONTE_VERIFICADOR)


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
                self.assertEqual(res["primitivos_sem_cor"], 0)


if __name__ == "__main__":
    unittest.main()
