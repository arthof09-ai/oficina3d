"""Testes da etapa validar (oficina3d/validar).

Os GLB de teste são montados aqui mesmo, byte a byte (biblioteca padrão): um triângulo,
com ou sem textura PNG. Os testes que chamam o Godot de verdade pulam se ele não existir.
Pastas temporárias só dentro de BASE\\jobs_teste (regra do projeto).
"""
import json
import shutil
import struct
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest import mock

from oficina3d import config
from oficina3d.validar import glb as vglb
from oficina3d.validar import godot as vgodot
from oficina3d.validar import validar


def _png(lado=4, cor=(200, 30, 30)) -> bytes:
    def chunk(tipo, dados):
        return struct.pack(">I", len(dados)) + tipo + dados + struct.pack(">I", zlib.crc32(tipo + dados))
    linhas = b"".join(b"\x00" + bytes(cor) * lado for _ in range(lado))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", lado, lado, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(linhas)) + chunk(b"IEND", b""))


def _alinhar(b: bytes, enchimento=b"\x00") -> bytes:
    return b + enchimento * ((4 - len(b) % 4) % 4)


def montar_glb(y0=0.0, textura: bytes | None = None, magic=b"glTF", mime="image/png") -> bytes:
    """Um triângulo (3 vértices, índices 0-1-2), opcionalmente com UV e textura no albedo."""
    pos = struct.pack("<9f", -0.5, y0, 0.0, 0.5, y0, 0.0, 0.0, y0 + 1.0, 0.0)
    idx = struct.pack("<3H", 0, 1, 2) + b"\x00\x00"
    uv = struct.pack("<6f", 0, 0, 1, 0, 0.5, 1)
    binario = pos + idx + uv
    vistas = [{"buffer": 0, "byteOffset": 0, "byteLength": 36},
              {"buffer": 0, "byteOffset": 36, "byteLength": 6},
              {"buffer": 0, "byteOffset": 44, "byteLength": 24}]
    gltf = {
        "asset": {"version": "2.0", "generator": "testes da Oficina"},
        "scene": 0, "scenes": [{"nodes": [0]}], "nodes": [{"mesh": 0, "name": "tri"}],
        "accessors": [
            {"bufferView": 0, "componentType": 5126, "count": 3, "type": "VEC3",
             "min": [-0.5, y0, 0.0], "max": [0.5, y0 + 1.0, 0.0]},
            {"bufferView": 1, "componentType": 5123, "count": 3, "type": "SCALAR"},
            {"bufferView": 2, "componentType": 5126, "count": 3, "type": "VEC2"},
        ],
        "meshes": [{"primitives": [{"attributes": {"POSITION": 0, "TEXCOORD_0": 2}, "indices": 1,
                                     "material": 0}]}],
        "materials": [{"pbrMetallicRoughness": {"baseColorFactor": [1, 1, 1, 1]}}],
    }
    if textura is not None:
        vistas.append({"buffer": 0, "byteOffset": len(binario), "byteLength": len(textura)})
        binario += textura
        gltf["images"] = [{"bufferView": 3, "mimeType": mime}]
        gltf["textures"] = [{"source": 0}]
        gltf["materials"][0]["pbrMetallicRoughness"]["baseColorTexture"] = {"index": 0}
    binario = _alinhar(binario)
    gltf["bufferViews"] = vistas
    gltf["buffers"] = [{"byteLength": len(binario)}]
    js = _alinhar(json.dumps(gltf).encode(), b" ")
    total = 12 + 8 + len(js) + 8 + len(binario)
    return (struct.pack("<4sII", magic, 2, total) + struct.pack("<II", len(js), 0x4E4F534A) + js
            + struct.pack("<II", len(binario), 0x004E4942) + binario)


class _ComPasta(unittest.TestCase):
    def setUp(self):
        config.JOBS_TESTE.mkdir(parents=True, exist_ok=True)
        self.pasta = Path(tempfile.mkdtemp(prefix="validar_", dir=config.JOBS_TESTE))

    def tearDown(self):
        shutil.rmtree(self.pasta, ignore_errors=True)

    def grava(self, nome, dados) -> Path:
        p = self.pasta / nome
        p.write_bytes(dados)
        return p


class TestLeitorGLB(_ComPasta):
    def test_triangulo(self):
        r = vglb.resumo(self.grava("t.glb", montar_glb()))
        self.assertEqual((r["triangulos"], r["vertices"], r["materiais"]), (1, 3, 1))
        self.assertEqual(r["primitivas_com_uv"], 1)
        self.assertEqual(r["caixa_min"][1], 0.0)

    def test_magic_errado(self):
        with self.assertRaisesRegex(vglb.ErroGLB, "magic"):
            vglb.ler(self.grava("m.glb", montar_glb(magic=b"gltf")))

    def test_comprimento_nao_bate(self):
        with self.assertRaisesRegex(vglb.ErroGLB, "comprimento"):
            vglb.ler(self.grava("c.glb", montar_glb() + b"\x00\x00\x00\x00"))

    def test_truncado(self):
        dados = bytearray(montar_glb())
        dados = dados[:-8]
        struct.pack_into("<I", dados, 8, len(dados))  # cabeçalho coerente, chunk BIN cortado
        with self.assertRaisesRegex(vglb.ErroGLB, "truncado"):
            vglb.ler(self.grava("tr.glb", bytes(dados)))

    def test_imagem_png_de_verdade(self):
        r = vglb.resumo(self.grava("tx.glb", montar_glb(textura=_png())))
        self.assertEqual(r["imagens"], [{"indice": 0, "ok": True, "info": "image/png"}])
        self.assertEqual(r["materiais_com_albedo"], 1)

    def test_imagem_que_mente_o_tipo(self):
        r = vglb.resumo(self.grava("mente.glb", montar_glb(textura=b"\xff\xd8\xff" + b"0" * 13)))
        self.assertFalse(r["imagens"][0]["ok"])


class TestRegrasSemGodot(_ComPasta):
    """Regras do validador com o Godot "ausente" (mock): só a régua do arquivo."""

    def _validar(self, dados, **op):
        with mock.patch.object(vgodot, "disponivel", return_value=False):
            return validar(self.grava("x.glb", dados), self.pasta, op)

    def _regra(self, r, id_):
        return next(x for x in r["regras"] if x["id"] == id_)

    def test_godot_ausente_nao_finge_aprovar_carga(self):
        r = self._validar(montar_glb())
        self.assertFalse(self._regra(r, "godot_carrega")["ok"])
        self.assertTrue(any("godot" in p for p in r["pendente"]))
        self.assertTrue((self.pasta / "validacao.json").is_file())

    def test_arquivo_ruim_reprova(self):
        r = self._validar(b"isto nao e um glb, so tem bytes")
        self.assertFalse(r["aprovado"])
        self.assertFalse(self._regra(r, "glb_valido")["ok"])

    def test_imagem_ruim_reprova(self):
        r = self._validar(montar_glb(textura=b"nao e png nenhum"))
        self.assertFalse(r["aprovado"])

    def test_perfil_jogo_exige_albedo(self):
        r = self._validar(montar_glb(), perfil="jogo")
        self.assertFalse(self._regra(r, "textura_albedo")["ok"])
        self.assertFalse(r["aprovado"])

    def test_limite_avulso_sobrescreve(self):
        r = self._validar(montar_glb(), max_triangulos=0)
        self.assertFalse(self._regra(r, "max_triangulos")["ok"])

    def test_perfil_desconhecido(self):
        from oficina3d.validar import ErroValidacao
        with self.assertRaises(ErroValidacao):
            self._validar(montar_glb(), perfil="inventado")


class TestEtapaNoWorker(_ComPasta):
    """worker._etapa_validar: nunca derruba o job."""

    def test_validador_quebrado_vira_reprovado(self):
        from oficina3d import worker
        (self.pasta / "saida").mkdir()
        with mock.patch("oficina3d.validar.validar", side_effect=RuntimeError("quebrou de propósito")):
            r = worker._etapa_validar(self.pasta, self.pasta / "x.glb", "oficina")
        self.assertFalse(r["aprovado"])
        self.assertIn("quebrou de propósito", r["erro_validador"])

    def test_grava_validacao_json_na_saida(self):
        from oficina3d import worker
        glb = self.grava("t.glb", montar_glb())
        with mock.patch.object(vgodot, "disponivel", return_value=False):
            r = worker._etapa_validar(self.pasta, glb, "oficina")
        self.assertEqual(r["relatorio"], "saida/validacao.json")
        self.assertTrue((self.pasta / "saida" / "validacao.json").is_file())

    def test_opcoes_do_job(self):
        from oficina3d import job
        op, _ = job.validar_opcoes({"validar_perfil": "jogo"})
        self.assertEqual((op["validar"], op["validar_perfil"]), (True, "jogo"))
        with self.assertRaises(ValueError):
            job.validar_opcoes({"validar_perfil": "inventado"})
        with self.assertRaises(ValueError):
            job.validar_opcoes({"validar": "sim"})


@unittest.skipUnless(vgodot.disponivel(), "Godot não encontrado neste PC")
class TestGodotDeVerdade(_ComPasta):
    def test_triangulo_aprovado(self):
        r = validar(self.grava("t.glb", montar_glb()), None, {})
        self.assertTrue(r["aprovado"], r["regras"])
        self.assertEqual(r["godot"]["triangulos"], 1)

    def test_textura_nao_derruba_o_godot(self):
        # Regressão de 01/11/2026: o modo padrão de imagem do GLTFState derrubava o Godot 4.7.2.
        r = validar(self.grava("tx.glb", montar_glb(textura=_png())), None, {"perfil": "jogo"})
        self.assertTrue(r["godot"]["ok"])
        self.assertEqual(r["godot"]["superficies_com_albedo"], 1)
        self.assertEqual(r["godot"]["albedo_px"], 4)
        self.assertTrue(r["aprovado"], r["regras"])

    def test_pivo_fora_dos_pes(self):
        r = validar(self.grava("alto.glb", montar_glb(y0=0.5)), None, {})
        self.assertFalse(next(x for x in r["regras"] if x["id"] == "pivo_nos_pes")["ok"])
        self.assertFalse(r["aprovado"])


if __name__ == "__main__":
    unittest.main()
