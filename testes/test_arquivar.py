"""Testes de oficina3d.arquivar (etapa 11: arquivar no Drive e liberar o disco).

Rodar (cwd = app):  py -3.12 -m unittest discover -s testes -p "test_arquivar.py" -v
O "Drive" é uma pasta temporária em <BASE>\\jobs_teste\\ (apagada no fim).
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import mock

APP = Path(__file__).resolve().parents[1]
JOBS_TESTE = APP.parent / "jobs_teste"
sys.path.insert(0, str(APP))

from oficina3d import arquivar  # noqa: E402


def _sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


class BaseArquivo(unittest.TestCase):
    def setUp(self):
        JOBS_TESTE.mkdir(parents=True, exist_ok=True)
        self.tmp = Path(tempfile.mkdtemp(prefix="g_arquivar_", dir=JOBS_TESTE))
        self.jobs = self.tmp / "jobs"
        self.drive = self.tmp / "drive" / "Oficina3D_v2"
        self.drive.mkdir(parents=True)
        self.jobs.mkdir()
        self._env = mock.patch.dict(os.environ, {}, clear=False)
        self._env.start()
        os.environ.pop(arquivar.ENV_DESTINO, None)

    def tearDown(self):
        self._env.stop()
        shutil.rmtree(self.tmp, ignore_errors=True)

    def criar_job(self, job_id="20261031-120000-orc", estado="concluido", **campos) -> Path:
        d = self.jobs / job_id
        (d / "saida" / "sprites").mkdir(parents=True)
        (d / "saida" / "modelo.glb").write_bytes(os.urandom(300_000))
        (d / "saida" / "previa_frente.png").write_bytes(os.urandom(5_000))
        (d / "saida" / "sprites" / "token.png").write_bytes(b"token")
        (d / "saida" / "relatorio.json").write_text(json.dumps({"id": job_id}), encoding="utf-8")
        job = {"id": job_id, "estado": estado, "historico": []}
        job.update(campos)
        (d / "job.json").write_text(json.dumps(job), encoding="utf-8")
        return d


class TestArquivarJob(BaseArquivo):
    def test_arquiva_confere_e_apaga(self):
        d = self.criar_job()
        hashes = {p.relative_to(d).as_posix(): _sha(p) for p in (d / "saida").rglob("*") if p.is_file()}
        r = arquivar.arquivar_job(d, self.drive)
        self.assertEqual(r["estado"], "arquivado", r)
        self.assertTrue(r["apagado"])
        destino = self.drive / "arquivo_jobs" / d.name
        self.assertEqual(Path(r["destino"]), destino)
        for rel, h in hashes.items():
            self.assertEqual(_sha(destino / rel), h, rel)
        manifesto = json.loads((destino / arquivar.MANIFESTO).read_text(encoding="utf-8"))
        self.assertEqual({e["caminho"]: e["sha256"] for e in manifesto["arquivos"]}, hashes)
        self.assertEqual(r["arquivos"], 4)
        self.assertFalse((d / "saida").exists())           # disco liberado
        self.assertTrue((d / "job.json").exists())         # o resto do job fica
        recibo = json.loads((d / arquivar.RECIBO).read_text(encoding="utf-8"))
        self.assertEqual(recibo["sha256_manifesto"], _sha(destino / arquivar.MANIFESTO))
        self.assertFalse(list(destino.rglob("*.parcial")))
        self.assertIn("[arquivar]", (d / "log.txt").read_text(encoding="utf-8"))
        # rodar de novo: nada a fazer
        self.assertEqual(arquivar.arquivar_job(d, self.drive)["estado"], "nada")

    def test_falha_de_hash_nao_apaga(self):
        d = self.criar_job()
        original = arquivar._copiar_arquivo

        def copiar_corrompendo(origem, destino):
            original(origem, destino)
            if destino.name == "modelo.glb":
                with open(destino, "r+b") as f:  # simula byte trocado no Drive
                    f.seek(1000)
                    b = f.read(1)
                    f.seek(1000)
                    f.write(bytes([b[0] ^ 0xFF]))

        with mock.patch.object(arquivar, "_copiar_arquivo", side_effect=copiar_corrompendo):
            r = arquivar.arquivar_job(d, self.drive)
        self.assertEqual(r["estado"], "erro", r)
        self.assertIn("SHA256", r["msg"])
        self.assertTrue((d / "saida" / "modelo.glb").exists())
        self.assertEqual(len([p for p in (d / "saida").rglob("*") if p.is_file()]), 4)
        self.assertFalse((d / arquivar.RECIBO).exists())
        # na próxima rodada (cópia boa) recopia o arquivo ruim e conclui
        r2 = arquivar.arquivar_job(d, self.drive)
        self.assertEqual(r2["estado"], "arquivado", r2)
        self.assertFalse((d / "saida").exists())

    def test_destino_inacessivel_fica_na_fila(self):
        d = self.criar_job()
        r = arquivar.arquivar_job(d, self.tmp / "G_sem_internet" / "Oficina3D_v2")
        self.assertEqual(r["estado"], "pendente")
        self.assertTrue((d / "saida" / "modelo.glb").exists())

    def test_erro_de_es_fica_na_fila(self):
        d = self.criar_job()
        with mock.patch.object(arquivar, "_copiar_arquivo", side_effect=OSError("rede caiu")):
            r = arquivar.arquivar_job(d, self.drive)
        self.assertEqual(r["estado"], "pendente")
        self.assertTrue((d / "saida" / "modelo.glb").exists())

    def test_sem_destino_nao_arquiva(self):
        d = self.criar_job()
        with self.assertLogs("oficina3d.arquivar", level="WARNING"):
            r = arquivar.arquivar_job(d)
        self.assertEqual(r["estado"], "sem_destino")
        self.assertTrue((d / "saida").exists())

    def test_destino_pela_variavel(self):
        d = self.criar_job()
        with mock.patch.dict(os.environ, {arquivar.ENV_DESTINO: str(self.drive)}):
            r = arquivar.arquivar_job(d)
        self.assertEqual(r["estado"], "arquivado")

    def test_saida_mudou_durante_copia_nao_apaga(self):
        d = self.criar_job()

        def conferir(destino, manifesto):
            (d / "saida" / "novo.png").write_bytes(b"chegou depois")
            return True

        r = arquivar.arquivar_job(d, self.drive, conferir_extra=conferir)
        self.assertEqual(r["estado"], "arquivado")
        self.assertFalse(r["apagado"])
        self.assertTrue((d / "saida" / "modelo.glb").exists())

    def test_conferencia_extra_recusa(self):
        d = self.criar_job()
        r = arquivar.arquivar_job(d, self.drive, conferir_extra=lambda *_: False)
        self.assertEqual(r["estado"], "pendente")
        self.assertTrue((d / "saida").exists())

    def test_id_invalido(self):
        d = self.criar_job()
        (d / "job.json").write_text(json.dumps({"id": "..\\..\\fora", "estado": "concluido"}))
        self.assertEqual(arquivar.arquivar_job(d, self.drive)["estado"], "erro")
        self.assertTrue((d / "saida").exists())


class TestArquivarPendentes(BaseArquivo):
    def test_politica(self):
        agora = datetime.now().astimezone()
        recente = (agora - timedelta(hours=5)).isoformat()
        velho = (agora - timedelta(days=4)).isoformat()
        aprovado = self.criar_job("20261031-100000-aprovado", concluido_em=recente, nota=9)
        sem_nota_novo = self.criar_job("20261031-110000-novo", concluido_em=recente)
        sem_nota_velho = self.criar_job("20261027-110000-velho", concluido_em=velho)
        rodando = self.criar_job("20261031-120000-rodando", estado="processando", nota=8)

        rs = arquivar.arquivar_pendentes(self.jobs, self.drive, agora=agora)
        ids = {r["id"]: r["estado"] for r in rs}
        self.assertEqual(ids, {aprovado.name: "arquivado", sem_nota_velho.name: "arquivado"})
        self.assertFalse((aprovado / "saida").exists())
        self.assertFalse((sem_nota_velho / "saida").exists())
        self.assertTrue((sem_nota_novo / "saida").exists())
        self.assertTrue((rodando / "saida").exists())

        # 3 dias depois o sem nota também vai
        rs = arquivar.arquivar_pendentes(self.jobs, self.drive, agora=agora + timedelta(days=3))
        self.assertEqual([r["id"] for r in rs], [sem_nota_novo.name])
        self.assertTrue((rodando / "saida").exists())

    def test_urgente_ignora_espera(self):
        agora = datetime.now().astimezone()
        d = self.criar_job(concluido_em=agora.isoformat())
        self.assertEqual(arquivar.arquivar_pendentes(self.jobs, self.drive, agora=agora), [])
        rs = arquivar.arquivar_pendentes(self.jobs, self.drive, agora=agora, urgente=True)
        self.assertEqual(rs[0]["estado"], "arquivado")
        self.assertFalse((d / "saida").exists())

    def test_sem_destino_so_avisa(self):
        d = self.criar_job(aprovado=True)
        with self.assertLogs("oficina3d.arquivar", level="WARNING"):
            rs = arquivar.arquivar_pendentes(self.jobs)
        self.assertEqual([r["estado"] for r in rs], ["sem_destino"])
        self.assertTrue((d / "saida").exists())

    def test_sem_internet_fica_tudo(self):
        d = self.criar_job(nota="boa")
        rs = arquivar.arquivar_pendentes(self.jobs, self.tmp / "nao_existe")
        self.assertEqual([r["estado"] for r in rs], ["pendente"])
        self.assertTrue((d / "saida").exists())

    def test_data_pelo_arquivo_quando_falta_no_job(self):
        d = self.criar_job()
        velho = (datetime.now() - timedelta(days=5)).timestamp()
        os.utime(d / "saida" / "relatorio.json", (velho, velho))
        rs = arquivar.arquivar_pendentes(self.jobs, self.drive)
        self.assertEqual([r["estado"] for r in rs], ["arquivado"])


if __name__ == "__main__":
    unittest.main()
