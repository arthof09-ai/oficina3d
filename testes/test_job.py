"""Testes de oficina3d.job (id, trava, escrita atômica, opções, imagens, desfazer criação).

As imagens são geradas aqui mesmo (PNG mínimo em bytes); nada de arte do RPG.
Tudo roda numa pasta temporária dentro de BASE\\jobs_teste, nunca em jobs\\.
"""
import atexit
import json
import os
import shutil
import struct
import sys
import tempfile
import threading
import time
import unittest
import zlib
from pathlib import Path
from unittest import mock

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

# --- pasta temporária dos testes: SEMPRE dentro de BASE\jobs_teste (antes de importar o config) ---
_BASE_TESTE = Path(os.environ.get("OFICINA3D_BASE") or r"C:\Users\txcga\RPG_Local\Oficina3D")
RAIZ_TESTE = _BASE_TESTE / "jobs_teste"


def _dentro(filho: Path, pai: Path) -> bool:
    f = os.path.normcase(os.path.abspath(filho))
    p = os.path.normcase(os.path.abspath(pai))
    return f.startswith(p + os.sep)


def _pasta_temporaria_dos_testes() -> Path:
    atual = os.environ.get("OFICINA3D_JOBS")
    if atual and _dentro(Path(atual), RAIZ_TESTE) and Path(atual).name.startswith("unittest_"):
        return Path(atual)
    RAIZ_TESTE.mkdir(exist_ok=True)
    p = Path(tempfile.mkdtemp(prefix="unittest_", dir=RAIZ_TESTE))
    os.environ["OFICINA3D_JOBS"] = str(p)
    atexit.register(shutil.rmtree, p, True)
    return p


TEMP_TESTES = _pasta_temporaria_dos_testes()

from oficina3d import config  # noqa: E402
from oficina3d import job  # noqa: E402

if os.path.normcase(str(config.JOBS)) != os.path.normcase(str(TEMP_TESTES)):
    raise RuntimeError(f"config.JOBS ({config.JOBS}) não é a pasta temporária dos testes; recuso rodar")

CARIMBO = "20261031-120000"


# --- imagens geradas em código ---
def png_bytes(w: int = 32, h: int = 32) -> bytes:
    linha = b"\x00" + b"\x80\x40\x20\xff" * w
    def pedaco(tipo, dados):
        return struct.pack(">I", len(dados)) + tipo + dados + struct.pack(">I", zlib.crc32(tipo + dados) & 0xFFFFFFFF)
    return (b"\x89PNG\r\n\x1a\n" + pedaco(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0))
            + pedaco(b"IDAT", zlib.compress(linha * h)) + pedaco(b"IEND", b""))


def jpeg_cabecalho(w: int, h: int) -> bytes:
    """Só o cabeçalho de um JPEG (SOI, APP0, SOF0, EOI): serve para o caminho sem Pillow."""
    app0 = b"\xff\xe0" + struct.pack(">H", 16) + b"JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"
    sof = b"\xff\xc0" + struct.pack(">HBHHB", 17, 8, h, w, 3) + b"\x01\x11\x00\x02\x11\x01\x03\x11\x01"
    return b"\xff\xd8" + app0 + sof + b"\xff\xd9"


def webp_vp8x(w: int, h: int) -> bytes:
    corpo = b"WEBP" + b"VP8X" + struct.pack("<I", 10) + b"\x00\x00\x00\x00" \
        + (w - 1).to_bytes(3, "little") + (h - 1).to_bytes(3, "little")
    return b"RIFF" + struct.pack("<I", len(corpo)) + corpo


def glb_minimo() -> bytes:
    return b"glTF" + struct.pack("<II", 2, 12)


class BaseJob(unittest.TestCase):
    def setUp(self):
        self.jobs = Path(tempfile.mkdtemp(prefix="caso_", dir=TEMP_TESTES))
        self.dados = Path(tempfile.mkdtemp(prefix="dados_", dir=TEMP_TESTES))
        self.assertTrue(_dentro(self.jobs, RAIZ_TESTE))
        self.assertFalse(_dentro(self.jobs, _BASE_TESTE / "jobs"))
        p = mock.patch.object(config, "JOBS", self.jobs)
        p.start()
        self.addCleanup(p.stop)
        self.addCleanup(shutil.rmtree, self.jobs, True)
        self.addCleanup(shutil.rmtree, self.dados, True)

    def img(self, nome="frente.png", conteudo=None, pasta=None) -> Path:
        pasta = Path(pasta or self.dados)
        pasta.mkdir(parents=True, exist_ok=True)
        p = pasta / nome
        p.write_bytes(png_bytes() if conteudo is None else conteudo)
        return p

    def pastas_de_job(self):
        return [p for p in self.jobs.iterdir() if p.is_dir()]


class TestId(BaseJob):
    RUINS = ["..\\x", "../20261031-120000-orc", "20261031-120000-..\\x", "20261031-120000-a/b",
             "20261031-120000-ORC", "20261031-120000-", "20261031-120000-orc\n", "2026103-120000-orc",
             "20261031-120000-" + "a" * 41, "20261031-120000-orc_2", "C:\\jobs\\20261031-120000-orc",
             "", None, 123]

    def test_validar_id(self):
        self.assertEqual(job.validar_id("20261031-120000-orc-2"), "20261031-120000-orc-2")
        self.assertEqual(job.validar_id("20261031-120000-" + "a" * 40), "20261031-120000-" + "a" * 40)
        for ruim in self.RUINS:
            with self.subTest(id=ruim), self.assertRaises(ValueError):
                job.validar_id(ruim)

    def test_toda_funcao_com_id_valida(self):
        for ruim in self.RUINS:
            with self.subTest(id=ruim):
                self.assertRaises(ValueError, job.pasta_job, ruim)
                self.assertRaises(ValueError, job.ler_job, ruim)
                self.assertRaises(ValueError, job.salvar_job, {"id": ruim})
                self.assertRaises(ValueError, job.atualizar_job, ruim, lambda j: None)
                with self.assertRaises(ValueError):
                    with job.trava_job(ruim):
                        pass
        self.assertEqual(self.pastas_de_job(), [])

    def test_ids_repetidos_ganham_sufixo(self):
        with mock.patch.object(job, "_carimbo", return_value=CARIMBO):
            ids = [job.criar_job([(self.img(), "frente")], nome="Orc")["id"] for _ in range(3)]
        self.assertEqual(ids, [f"{CARIMBO}-orc", f"{CARIMBO}-orc-2", f"{CARIMBO}-orc-3"])

    def test_nome_longo_e_acentuado(self):
        with mock.patch.object(job, "_carimbo", return_value=CARIMBO):
            a = job.criar_job([(self.img(), None)], nome="Capríleo " * 10)
            b = job.criar_job([(self.img(), None)], nome="Capríleo " * 10)
        for j in (a, b):
            job.validar_id(j["id"])
        self.assertTrue(b["id"].endswith("-2"))
        self.assertTrue(a["id"].startswith(f"{CARIMBO}-caprileo-caprileo"))

    def test_criacao_concorrente_sem_corrida(self):
        origem = self.img()
        ids, erros = [], []

        def criar():
            try:
                ids.append(job.criar_job([(origem, "frente")], nome="orc")["id"])
            except Exception as e:  # pragma: no cover - só aparece se der errado
                erros.append(e)

        with mock.patch.object(job, "_carimbo", return_value=CARIMBO):
            threads = [threading.Thread(target=criar) for _ in range(8)]
            for t in threads:
                t.start()
            for t in threads:
                t.join(60)
        self.assertEqual(erros, [])
        self.assertEqual(len(set(ids)), 8)
        self.assertEqual(len(self.pastas_de_job()), 8)


class TestCriarJob(BaseJob):
    def test_criacao_basica(self):
        j = job.criar_job([(self.img("01_FRENTE_S.png"), "frente")], nome="orc")
        raiz = job.pasta_job(j["id"])
        for s in job.SUBPASTAS:
            self.assertTrue((raiz / s).is_dir(), s)
        self.assertEqual(j["imagens"], [{"arquivo": "entrada/01_FRENTE_S.png", "vista": "frente"}])
        self.assertTrue((raiz / "entrada" / "01_FRENTE_S.png").is_file())
        self.assertEqual(j["estado"], "pendente")
        self.assertEqual(j["modo"], "livre")
        self.assertEqual(j["opcoes"]["motor"], "hunyuan-mini-turbo")
        self.assertEqual(len(j["historico"]), 1)
        self.assertIn("automático", j["historico"][0]["msg"])
        self.assertEqual(job.ler_job(j["id"]), j)
        self.assertFalse((raiz / job.NOME_TRAVA).exists())
        self.assertEqual(list(raiz.glob("*.tmp")), [])

    def test_motor_automatico(self):
        casos = [
            ([("frente.png", "frente")], "livre", "hunyuan-mini-turbo"),
            ([("frente.png", "frente"), ("costas.png", "costas")], "livre", "hunyuan-mv-turbo"),
            ([("a.png", None), ("b.png", None)], "livre", "hunyuan-mv-turbo"),
            ([("frente.png", "frente"), ("det.png", "detalhe")], "livre", "hunyuan-mini-turbo"),
            ([("prancha.png", None)], "multivista", "hunyuan-mv-turbo"),
        ]
        for itens, modo, esperado in casos:
            with self.subTest(itens=itens, modo=modo):
                arqs = [(self.img(n), v) for n, v in itens]
                self.assertEqual(job.criar_job(arqs, modo=modo)["opcoes"]["motor"], esperado)

    def test_motor_explicito_e_aviso(self):
        arqs = [(self.img("f.png"), "frente"), (self.img("c.png"), "costas")]
        j = job.criar_job(arqs, opcoes={"motor": "triposr"})
        self.assertEqual(j["opcoes"]["motor"], "triposr")
        self.assertTrue(any("uma imagem só" in a for a in j["avisos"]))
        self.assertNotIn("automático", j["historico"][0]["msg"])

    def test_nomes_repetidos_e_estranhos(self):
        a = self.img("Capríleo frente.png", pasta=self.dados / "a")
        b = self.img("Capríleo frente.png", pasta=self.dados / "b")
        j = job.criar_job([(a, "frente"), (b, "costas")])
        self.assertEqual([i["arquivo"] for i in j["imagens"]],
                         ["entrada/Capríleo_frente.png", "entrada/Capríleo_frente_2.png"])

    def test_extensao_corrigida_pelo_conteudo(self):
        with mock.patch.object(job, "_pillow", return_value=None):
            j = job.criar_job([(self.img("foto.png", jpeg_cabecalho(64, 48)), "frente")])
        self.assertEqual(j["imagens"][0]["arquivo"], "entrada/foto.jpg")

    def test_so_refinar(self):
        malha = self.dados / "orc.glb"
        malha.write_bytes(glb_minimo())
        j = job.criar_job([], modo="so-refinar", malha=malha)
        self.assertEqual(j["malha_entrada"], "entrada/orc.glb")
        self.assertEqual(j["nome"], "orc")
        self.assertTrue((job.pasta_job(j["id"]) / "entrada" / "orc.glb").is_file())

    def test_entradas_invalidas_nao_criam_pasta(self):
        boa = self.img()
        stl = self.dados / "x.stl"
        stl.write_bytes(b"solid x")
        glb_ruim = self.dados / "ruim.glb"
        glb_ruim.write_bytes(b"nao e glb")
        casos = [
            dict(arquivos=[(boa, "frente")], modo="inventado"),
            dict(arquivos=[], modo="livre"),
            dict(arquivos=[], modo="so-refinar"),
            dict(arquivos=[], modo="so-refinar", malha=stl),
            dict(arquivos=[], modo="so-refinar", malha=glb_ruim),
            dict(arquivos=[], modo="so-refinar", malha=self.dados / "nao_existe.glb"),
            dict(arquivos=[(boa, "lado")]),
            dict(arquivos=[(boa,)]),
            dict(arquivos=[(self.dados / "nao_existe.png", "frente")]),
            dict(arquivos=[(boa, "frente")], nome="   "),
            dict(arquivos=[(boa, None)] * (job.MAX_IMAGENS + 1)),
            dict(arquivos=[(boa, "frente")], opcoes={"motor": "hunyuan-full"}),
        ]
        for kw in casos:
            with self.subTest(kw=kw), self.assertRaises(ValueError):
                job.criar_job(**kw)
        self.assertEqual(self.pastas_de_job(), [])

    def test_falha_no_meio_apaga_a_pasta(self):
        arqs = [(self.img("a.png"), "frente"), (self.img("b.png"), "costas")]
        copia_real = shutil.copy2
        chamadas = []

        def copia_que_falha(origem, destino, *a, **k):
            chamadas.append(origem)
            if len(chamadas) == 2:
                raise OSError("disco cheio (simulado)")
            return copia_real(origem, destino, *a, **k)

        with mock.patch.object(job.shutil, "copy2", side_effect=copia_que_falha):
            with self.assertRaises(OSError):
                job.criar_job(arqs)
        self.assertEqual(len(chamadas), 2)
        self.assertEqual(self.pastas_de_job(), [])

        with mock.patch.object(job, "registrar", side_effect=RuntimeError("falha simulada")):
            with self.assertRaises(RuntimeError):
                job.criar_job(arqs)
        self.assertEqual(self.pastas_de_job(), [])


class TestImagens(BaseJob):
    def _ambos(self):
        """Roda o teste com o Pillow (se houver) e sem ele."""
        modos = [("sem Pillow", None)]
        if job._pillow() is not None:
            modos.append(("com Pillow", job._pillow()))
        return modos

    def test_png_valido(self):
        for rotulo, mod in self._ambos():
            with self.subTest(rotulo), mock.patch.object(job, "_pillow", return_value=mod):
                info = job.conferir_imagem(self.img("ok.png", png_bytes(40, 20)))
                self.assertEqual(info["formato"], "PNG")
                self.assertEqual((info["largura"], info["altura"]), (40, 20))

    def test_nao_e_imagem(self):
        for rotulo, mod in self._ambos():
            with self.subTest(rotulo), mock.patch.object(job, "_pillow", return_value=mod):
                for conteudo in (b"ola, eu sou texto", b"GIF89a" + b"\x00" * 30, b"%PDF-1.7 ..."):
                    with self.assertRaises(ValueError):
                        job.conferir_imagem(self.img("falsa.png", conteudo))
                with self.assertRaises(ValueError):
                    job.conferir_imagem(self.img("vazia.png", b""))
                with self.assertRaises(ValueError):
                    job.conferir_imagem(self.dados)  # pasta, não arquivo

    def test_png_truncado_sem_pillow(self):
        with mock.patch.object(job, "_pillow", return_value=None):
            with self.assertRaises(ValueError):
                job.conferir_imagem(self.img("cortada.png", png_bytes()[:-12]))

    def test_lados(self):
        for rotulo, mod in self._ambos():
            with self.subTest(rotulo), mock.patch.object(job, "_pillow", return_value=mod):
                with self.assertRaises(ValueError) as cm:
                    job.conferir_imagem(self.img("larga.png", png_bytes(job.LADO_MAX + 1, 16)))
                self.assertIn("px de lado", str(cm.exception))
                with self.assertRaises(ValueError):
                    job.conferir_imagem(self.img("mini.png", png_bytes(8, 8)))
                job.conferir_imagem(self.img("limite.png", png_bytes(job.LADO_MAX, 16)))

    def test_limite_de_bytes(self):
        p = self.img("normal.png")
        with mock.patch.object(job, "LIMITE_BYTES_IMAGEM", 100):
            with self.assertRaises(ValueError) as cm:
                job.conferir_imagem(p)
        self.assertIn("MB", str(cm.exception))
        self.assertEqual(job.LIMITE_BYTES_IMAGEM, 40 * 1024 * 1024)

    def test_jpeg_e_webp_sem_pillow(self):
        with mock.patch.object(job, "_pillow", return_value=None):
            info = job.conferir_imagem(self.img("a.jpg", jpeg_cabecalho(640, 480)))
            self.assertEqual((info["formato"], info["largura"], info["altura"]), ("JPEG", 640, 480))
            info = job.conferir_imagem(self.img("a.webp", webp_vp8x(300, 200)))
            self.assertEqual((info["formato"], info["largura"], info["altura"]), ("WEBP", 300, 200))
            with self.assertRaises(ValueError):
                job.conferir_imagem(self.img("g.jpg", jpeg_cabecalho(9000, 100)))
            with self.assertRaises(ValueError):
                job.conferir_imagem(self.img("sem_sof.jpg", b"\xff\xd8\xff\xd9"))


class TestOpcoes(unittest.TestCase):
    def test_padroes(self):
        op, avisos = job.validar_opcoes(None, "livre", ["frente"])
        self.assertEqual(op["motor"], "hunyuan-mini-turbo")
        self.assertEqual(op["octree"], 256)
        self.assertEqual(avisos, [])
        self.assertIsNone(config.OPCOES_PADRAO["motor"])  # o padrão não foi alterado

    def test_none_usa_padrao(self):
        op, _ = job.validar_opcoes({"passos": None, "octree": None, "motor": None}, "livre", ["frente"])
        self.assertIsNone(op["passos"])
        self.assertEqual(op["octree"], 256)

    def test_validas(self):
        op, _ = job.validar_opcoes({"motor": "hunyuan-mv", "passos": 30, "octree": 380, "seed": 0,
                                    "alvo_triangulos": 20000.0, "altura_m": 1.8, "simetrizar": True,
                                    "remover_fundo": False, "sementes": 2}, "livre", ["frente", "costas"])
        self.assertEqual((op["motor"], op["passos"], op["octree"], op["alvo_triangulos"]),
                         ("hunyuan-mv", 30, 380, 20000))
        self.assertIsInstance(op["alvo_triangulos"], int)
        self.assertEqual(op["remover_fundo"], "nao")
        self.assertEqual(op["altura_m"], 1.8)

    def test_invalidas(self):
        ruins = [
            {"motor": "hunyuan-full"}, {"motor": "../triposr"}, {"motor": 1},
            {"octree": 10}, {"octree": 4096}, {"octree": True}, {"octree": "256"}, {"octree": 256.5},
            {"passos": 0}, {"passos": 1000}, {"seed": -1}, {"seed": 2**32},
            {"alvo_triangulos": 10}, {"alvo_triangulos": 10**9},
            {"altura_m": 0}, {"altura_m": float("nan")}, {"altura_m": float("inf")}, {"altura_m": True},
            {"flashvdm": 1}, {"simetrizar": "sim"}, {"remover_fundo": "talvez"},
            {"sementes": 0}, {"sementes": 99},
            {"opcao_que_nao_existe": 1},
        ]
        for ruim in ruins:
            with self.subTest(op=ruim), self.assertRaises(ValueError):
                job.validar_opcoes(ruim, "livre", ["frente"])
        with self.assertRaises(ValueError):
            job.validar_opcoes(["motor"], "livre", ["frente"])

    def test_vista_repetida_vira_aviso(self):
        _, avisos = job.validar_opcoes({}, "livre", ["frente", "frente"])
        self.assertTrue(any("repetida" in a for a in avisos))


class TestGravacaoETrava(BaseJob):
    def novo(self):
        return job.criar_job([(self.img(), "frente")], nome="orc")

    def test_escrita_atomica_sem_lixo(self):
        j = self.novo()
        for i in range(5):
            job.registrar(j, "forma", f"passo {i}", progresso=i * 10)
        raiz = job.pasta_job(j["id"])
        self.assertEqual(sorted(p.name for p in raiz.iterdir() if p.is_file()), ["job.json"])
        self.assertEqual(job.ler_job(j["id"])["progresso"], 40)

    def test_falha_ao_serializar_nao_estraga(self):
        j = self.novo()
        antes = (job.pasta_job(j["id"]) / "job.json").read_bytes()
        j["resultado"] = {"glb": Path("x.glb")}  # Path não vira JSON
        with self.assertRaises(TypeError):
            job.salvar_job(j)
        self.assertEqual((job.pasta_job(j["id"]) / "job.json").read_bytes(), antes)

    def test_salvar_job_inexistente(self):
        with self.assertRaises(FileNotFoundError):
            job.salvar_job({"id": f"{CARIMBO}-fantasma"})
        self.assertEqual(self.pastas_de_job(), [])

    def test_registrar(self):
        j = self.novo()
        job.registrar(j, "entrada", "ok", progresso=150)
        self.assertEqual((j["etapa"], j["progresso"]), ("entrada", 100))
        job.registrar(j, None, "sem salvar", progresso=-5, salvar=False)
        self.assertEqual(j["progresso"], 0)
        self.assertEqual(job.ler_job(j["id"])["progresso"], 100)

    def test_atualizar_job(self):
        j = self.novo()

        def cancelar(x):
            x["estado"] = "cancelado"

        r = job.atualizar_job(j["id"], cancelar)
        self.assertEqual(r["estado"], "cancelado")
        self.assertEqual(job.ler_job(j["id"])["estado"], "cancelado")
        with self.assertRaises(ValueError):
            job.atualizar_job(j["id"], lambda x: dict(x, id=f"{CARIMBO}-outro"))

    def test_trava_ocupada_por_outra_thread(self):
        j = self.novo()
        segurando, soltar = threading.Event(), threading.Event()

        def dono():
            with job.trava_job(j["id"]):
                segurando.set()
                soltar.wait(10)

        t = threading.Thread(target=dono)
        t.start()
        try:
            self.assertTrue(segurando.wait(10))
            inicio = time.monotonic()
            with self.assertRaises(job.TravaOcupada):
                with job.trava_job(j["id"], timeout=0.3):
                    pass
            self.assertGreaterEqual(time.monotonic() - inicio, 0.25)
        finally:
            soltar.set()
            t.join(10)
        with job.trava_job(j["id"], timeout=1):  # liberada
            pass

    def test_trava_reentrante(self):
        j = self.novo()
        with job.trava_job(j["id"]):
            with job.trava_job(j["id"], timeout=0):
                job.salvar_job(j)
            self.assertTrue((job.pasta_job(j["id"]) / job.NOME_TRAVA).exists())
        self.assertFalse((job.pasta_job(j["id"]) / job.NOME_TRAVA).exists())

    def test_trava_abandonada(self):
        j = self.novo()
        trava = job.pasta_job(j["id"]) / job.NOME_TRAVA
        # 1) processo que não existe mais
        trava.write_text("999999999 abc 2026-10-31T12:00:00-03:00", encoding="utf-8")
        with job.trava_job(j["id"], timeout=1):
            pass
        self.assertFalse(trava.exists())
        # 2) processo vivo (este), mas trava velha demais
        trava.write_text(f"{os.getpid()} abc 2026-10-31T12:00:00-03:00", encoding="utf-8")
        velho = time.time() - job.TRAVA_VELHA_S - 60
        os.utime(trava, (velho, velho))
        with job.trava_job(j["id"], timeout=1):
            pass
        # 3) processo vivo e trava recente: espera e desiste
        trava.write_text(f"{os.getpid()} abc 2026-10-31T12:00:00-03:00", encoding="utf-8")
        with self.assertRaises(job.TravaOcupada):
            with job.trava_job(j["id"], timeout=0.2):
                pass
        trava.unlink()
        self.assertEqual([p.name for p in job.pasta_job(j["id"]).iterdir() if "velha" in p.name], [])

    def test_pid_vivo(self):
        self.assertTrue(job._pid_vivo(os.getpid()))
        self.assertFalse(job._pid_vivo(999999999))
        self.assertFalse(job._pid_vivo(0))


class TestLerEListar(BaseJob):
    def test_ler_inexistente_e_corrompido(self):
        with self.assertRaises(FileNotFoundError):
            job.ler_job(f"{CARIMBO}-nada")
        p = self.jobs / f"{CARIMBO}-quebrado"
        p.mkdir()
        (p / "job.json").write_text("{ isto nao e json", encoding="utf-8")
        with self.assertRaises(ValueError):
            job.ler_job(p.name)
        q = self.jobs / f"{CARIMBO}-trocado"
        q.mkdir()
        (q / "job.json").write_text(json.dumps({"id": f"{CARIMBO}-outro"}), encoding="utf-8")
        with self.assertRaises(ValueError):
            job.ler_job(q.name)

    def test_listar(self):
        self.assertEqual(job.listar_jobs(), [])
        with mock.patch.object(job, "_carimbo", return_value=CARIMBO):
            a = job.criar_job([(self.img(), "frente")], nome="a")
            b = job.criar_job([(self.img(), "frente")], nome="b")
        (self.jobs / "lixo").mkdir()
        (self.jobs / "lixo" / "job.json").write_text(json.dumps({"id": "lixo"}), encoding="utf-8")
        ruim = self.jobs / f"{CARIMBO}-quebrado"
        ruim.mkdir()
        (ruim / "job.json").write_text("{", encoding="utf-8")
        (self.jobs / "solto.txt").write_text("x", encoding="utf-8")
        ids = [j["id"] for j in job.listar_jobs()]
        self.assertEqual(sorted(ids), sorted([a["id"], b["id"]]))

    def test_listar_sem_pasta(self):
        with mock.patch.object(config, "JOBS", self.jobs / "nao_existe"):
            self.assertEqual(job.listar_jobs(), [])


if __name__ == "__main__":
    unittest.main()
