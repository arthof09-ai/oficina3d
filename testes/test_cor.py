"""Testes da Etapa COR (oficina3d.cor.projecao). Sem arte do RPG: dados gerados aqui.

Rodar (cwd = app):  py -3.12 -m unittest discover -s testes -p "test_cor.py" -v
Só matemática pura (numpy): não precisa do Blender.
"""
from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

APP = Path(__file__).resolve().parents[1]
if str(APP) not in sys.path:
    sys.path.insert(0, str(APP))

from oficina3d.cor import projecao  # noqa: E402
from oficina3d.refino import previa  # noqa: E402


class TestCameras(unittest.TestCase):
    def test_direcao_igual_a_previa(self):
        # A convenção de vistas da COR tem de ser idêntica à do refino.
        for vista in ("frente", "esquerda", "costas", "direita", "frente-direita", "cima"):
            self.assertEqual(projecao.direcao_camera(vista),
                             previa.direcao_camera(vista))

    def test_centro_vai_para_o_centro_da_imagem(self):
        centro = np.array([0.0, 0.0, 0.5])
        px, py = projecao.projetar(np.array([[0.0, 0.0, 0.5]]), centro, "frente", 2.0, 200, 200)
        self.assertAlmostEqual(px[0], 100.0)
        self.assertAlmostEqual(py[0], 100.0)

    def test_frente_ve_o_lado_esquerdo_a_direita(self):
        # Personagem de frente: o lado esquerdo dele (+X) aparece à direita.
        centro = np.array([0.0, 0.0, 0.5])
        px, _ = projecao.projetar(np.array([[1.0, 0.0, 0.5]]), centro, "frente", 2.0, 200, 200)
        self.assertGreater(px[0], 100.0)

    def test_facing(self):
        self.assertAlmostEqual(projecao.peso_facing(np.array([0.0, -1.0, 0.0]), "frente"), 1.0)
        self.assertAlmostEqual(projecao.peso_facing(np.array([0.0, 1.0, 0.0]), "frente"), 0.0)
        self.assertAlmostEqual(projecao.peso_facing(np.array([1.0, 0.0, 0.0]), "esquerda"), 1.0)
        self.assertAlmostEqual(projecao.peso_facing(np.array([0.0, 0.0, 0.0]), "frente"), 0.0)

    def test_vista_invalida_erro(self):
        with self.assertRaises(ValueError):
            projecao.direcao_camera("diagonal-inexistente")


class TestAlinhamento(unittest.TestCase):
    def test_caixas_iguais_da_identidade(self):
        ax, bx, ay, by = projecao.alinhamento_silhueta((10, 20, 110, 220), (10, 20, 110, 220))
        self.assertAlmostEqual(ax, 1.0)
        self.assertAlmostEqual(bx, 0.0)
        self.assertAlmostEqual(ay, 1.0)
        self.assertAlmostEqual(by, 0.0)

    def test_caixa_degenerada_erro_em_vez_de_lixo(self):
        with self.assertRaises(ValueError):
            projecao.alinhamento_silhueta((5, 5, 5, 10), (0, 0, 10, 10))

    def test_iou(self):
        a = np.array([[True, False], [False, True]])
        self.assertAlmostEqual(projecao.iou(a, a), 1.0)
        self.assertAlmostEqual(projecao.iou(a, ~a), 0.0)
        with self.assertRaises(ValueError):
            projecao.iou(a, np.zeros((3, 3), dtype=bool))

    def test_iou_vazias_zero_e_nao_um(self):
        # D8: duas mascaras vazias nao tem acordo mensuravel; 1,0 mentia.
        vazio = np.zeros((3, 3), dtype=bool)
        self.assertEqual(projecao.iou(vazio, vazio), 0.0)

    def test_alinhamento_aspectos_distintos(self):
        # D6: escalas x/y independentes (mascara larga, malha quadrada).
        ax, bx, ay, by = projecao.alinhamento_silhueta((0, 0, 20, 10), (0, 0, 10, 10))
        self.assertAlmostEqual(ax, 2.0)
        self.assertAlmostEqual(ay, 1.0)
        self.assertAlmostEqual(ax * 5 + bx, 10.0)
        self.assertAlmostEqual(ay * 5 + by, 5.0)


class TestAlinhamentoOtimizado(unittest.TestCase):
    def _retangulo(self, x0, y0, x1, y1, w=100, h=100):
        m = np.zeros((h, w), dtype=bool)
        m[y0:y1, x0:x1] = True
        return m

    def test_identico_nao_busca(self):
        # Fast path: IoU inicial 1,0 nao tem o que otimizar.
        m = self._retangulo(20, 30, 60, 80)
        ax, bx, ay, by, info = projecao.otimizar_alinhamento(m, m, (1.0, 0.0, 1.0, 0.0))
        self.assertEqual(info["candidatos_avaliados"], 0)
        self.assertEqual(info["modo"], "inicial")
        self.assertAlmostEqual(info["iou_final"], 1.0)

    def test_bbox_robusta_percentil_zero_igual_bbox(self):
        m = self._retangulo(10, 20, 50, 70)
        m[5, 90] = True  # ponta isolada: bbox por extremos a inclui
        self.assertEqual(projecao.bbox_robusta_mascara(m, 0.0), projecao.bbox_mascara(m))
        robusta = projecao.bbox_robusta_mascara(m)
        self.assertEqual(robusta, (10, 20, 50, 70))
        self.assertEqual(projecao.bbox_robusta_mascara(np.zeros((5, 5), dtype=bool)), None)
        with self.assertRaises(ValueError):
            projecao.bbox_robusta_mascara(m, 50.0)

    def test_ponta_fina_recupera_iou(self):
        # A malha tem um retangulo + uma ponta fina de 1 px que estica a
        # caixa por extremos; a arte e so o retangulo. O alinhamento v1
        # (caixas cheias) herda a ponta e perde IoU; a busca tem de
        # recuperar quase tudo (o caso que motivou a A1). A ponta tem
        # 12 px para o otimo caber na janela documentada da busca
        # (escala 0,80..1,25, deslocamento +-24 px).
        malha = self._retangulo(20, 30, 60, 80)
        malha[50, 60:72] = True  # ponta fina para a direita
        arte = self._retangulo(20, 30, 60, 80)
        ini = projecao.alinhamento_silhueta(projecao.bbox_mascara(arte),
                                            projecao.bbox_mascara(malha))
        iou_ini = projecao.iou_alinhado(malha, arte, *ini)
        # Ponto de partida robusto (o que o _blender_cor usa na A1).
        ini_r = projecao.alinhamento_silhueta(projecao.bbox_robusta_mascara(arte),
                                              projecao.bbox_robusta_mascara(malha))
        _, _, _, _, info = projecao.otimizar_alinhamento(malha, arte, ini_r)
        self.assertLess(iou_ini, 0.90)
        self.assertGreaterEqual(info["iou_final"], 0.95)
        self.assertGreater(info["iou_final"], iou_ini)

    def test_trava_de_aspecto_respeitada(self):
        # Arte = retangulo largo + quadrado isolado no canto: o alinhamento
        # v1 estica a malha quadrada para a caixa cheia (IoU ~0,69), e o
        # otimo sem trava exigiria sx/sy = 1,29 (esticar x e encolher y).
        # A busca tem de melhorar (ou manter) sem violar a trava.
        malha = self._retangulo(20, 20, 60, 60)
        arte = self._retangulo(10, 20, 90, 60)
        arte[5:10, 5:10] = True
        ini = projecao.alinhamento_silhueta(projecao.bbox_mascara(arte),
                                            projecao.bbox_mascara(malha))
        self.assertLess(projecao.iou_alinhado(malha, arte, *ini), 0.999)
        ax, bx, ay, by, info = projecao.otimizar_alinhamento(malha, arte, ini)
        self.assertGreater(info["candidatos_avaliados"], 0)
        self.assertLessEqual(abs(info["escala_x"] / info["escala_y"] - 1.0), 0.15 + 1e-9)
        self.assertGreaterEqual(info["iou_final"], info["iou_inicial"])

    def test_entradas_malformadas_recusadas(self):
        m = self._retangulo(20, 30, 60, 80)
        with self.assertRaises(ValueError):
            projecao.otimizar_alinhamento(m, np.zeros((50, 50), dtype=bool), (1.0, 0.0, 1.0, 0.0))
        with self.assertRaises(ValueError):
            projecao.otimizar_alinhamento(np.zeros((10, 10), dtype=bool), m, (1.0, 0.0, 1.0, 0.0))
        with self.assertRaises(ValueError):
            projecao.otimizar_alinhamento(m, np.zeros((10, 10), dtype=bool), (1.0, 0.0, 1.0, 0.0))

    def test_determinismo(self):
        malha = self._retangulo(20, 30, 60, 80)
        malha[50, 60:72] = True
        arte = self._retangulo(20, 30, 60, 80)
        ini = projecao.alinhamento_silhueta(projecao.bbox_robusta_mascara(arte),
                                            projecao.bbox_robusta_mascara(malha))
        r1 = projecao.otimizar_alinhamento(malha, arte, ini)
        r2 = projecao.otimizar_alinhamento(malha, arte, ini)
        self.assertEqual(r1, r2)

    def test_aplicar_alinhamento_desloca(self):
        # Mapeamento inverso (como o IoU v1): o pixel da arte (x, y)
        # amostra a malha em ((x - bx) / ax, ...); bx = +5 desloca o
        # retangulo (10..20) para (15..25) no espaco da arte.
        m = self._retangulo(10, 10, 20, 20, w=40, h=40)
        deslocada = projecao.aplicar_alinhamento(m, 1.0, 5.0, 1.0, 5.0)
        self.assertEqual(projecao.bbox_mascara(deslocada), (15, 15, 25, 25))
        with self.assertRaises(ValueError):
            projecao.aplicar_alinhamento(m, 0.0, 0.0, 1.0, 0.0)


class TestBake(unittest.TestCase):
    def _triangulo(self):
        verts = np.array([[0.0, -1.0, 0.0], [1.0, -1.0, 0.0], [0.0, -1.0, 1.0]])
        faces = np.array([[0, 1, 2]])
        norm = np.array([[0.0, -1.0, 0.0]] * 3)
        fuv = np.array([[[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]])
        return verts, faces, norm, fuv

    def test_triangulo_vermelho(self):
        verts, faces, norm, fuv = self._triangulo()
        img = np.zeros((10, 10, 3))
        img[:] = [1.0, 0.0, 0.0]
        vista = {"vista": "frente", "imagem": img, "mascara": np.ones((10, 10), dtype=bool),
                 "visivel": np.array([True]), "peso_face": np.array([1.0])}
        tex, pintado, _, info = projecao.rasterizar_textura(
            verts, faces, norm, fuv, [vista], 16, np.array([0.0, 0.0, 0.5]), (1.0, 1.0, 1.0), 2.0)
        self.assertGreater(int(pintado.sum()), 0)
        self.assertTrue(np.all(tex[pintado] == np.array([1.0, 0.0, 0.0])))
        self.assertEqual(info["faces_pintadas_por_vista"]["frente"], 1)

    def test_face_oculta_nao_pinta(self):
        verts, faces, norm, fuv = self._triangulo()
        img = np.zeros((10, 10, 3))
        img[:] = [1.0, 0.0, 0.0]
        vista = {"vista": "frente", "imagem": img, "mascara": np.ones((10, 10), dtype=bool),
                 "visivel": np.array([False]), "peso_face": np.array([1.0])}
        _, pintado, _, _ = projecao.rasterizar_textura(
            verts, faces, norm, fuv, [vista], 16, np.array([0.0, 0.0, 0.5]), (1.0, 1.0, 1.0), 2.0)
        self.assertEqual(int(pintado.sum()), 0)

    def test_facing_de_raspao_nao_pinta(self):
        verts, faces, norm, fuv = self._triangulo()
        img = np.zeros((10, 10, 3))
        img[:] = [1.0, 0.0, 0.0]
        vista = {"vista": "frente", "imagem": img, "mascara": np.ones((10, 10), dtype=bool),
                 "visivel": np.array([True]), "peso_face": np.array([0.01])}
        _, pintado, _, _ = projecao.rasterizar_textura(
            verts, faces, norm, fuv, [vista], 16, np.array([0.0, 0.0, 0.5]), (1.0, 1.0, 1.0), 2.0)
        self.assertEqual(int(pintado.sum()), 0)

    def test_empate_mantem_primeira_fonte(self):
        # Nome corrigido (D4 do Critico T1): este teste usa DUAS VEZES a mesma
        # vista, logo o peso por texel e igual; a primeira fonte vence no
        # empate (ganha = pes > melhor, estrito). O teste de maior-facing
        # de verdade e o seguinte, com duas vistas distintas.
        verts, faces, norm, fuv = self._triangulo()
        vermelha = np.zeros((10, 10, 3))
        vermelha[:] = [1.0, 0.0, 0.0]
        azul = np.zeros((10, 10, 3))
        azul[:] = [0.0, 0.0, 1.0]
        v1 = {"vista": "frente", "imagem": vermelha, "mascara": np.ones((10, 10), dtype=bool),
              "visivel": np.array([True]), "peso_face": np.array([1.0])}
        v2 = {"vista": "frente", "imagem": azul, "mascara": np.ones((10, 10), dtype=bool),
              "visivel": np.array([True]), "peso_face": np.array([1.0])}
        tex, pintado, _, _ = projecao.rasterizar_textura(
            verts, faces, norm, fuv, [v1, v2], 16, np.array([0.0, 0.0, 0.5]), (1.0, 1.0, 1.0), 2.0)
        self.assertTrue(np.all(tex[pintado] == np.array([1.0, 0.0, 0.0])))

    def test_maior_facing_vence_entre_vistas(self):
        # D4: triangulo com normal inclinada entre frente (-Y) e esquerda (+X):
        # facing frente = 0,894, esquerda = 0,447. A vista de maior facing tem
        # de vencer nos dois pedidos (ordem nao pode decidir).
        n = np.array([0.5, -1.0, 0.0])
        n = n / np.linalg.norm(n)
        centro = np.array([0.0, 0.0, 0.5])
        e1 = np.cross(n, np.array([0.0, 0.0, 1.0]))
        e1 = e1 / np.linalg.norm(e1)
        e2 = np.cross(n, e1)
        verts = np.array([centro, centro + e1 * 0.5, centro + e2 * 0.5])
        faces = np.array([[0, 1, 2]])
        norm = np.array([n, n, n])
        fuv = np.array([[[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]])
        vermelha = np.zeros((10, 10, 3))
        vermelha[:] = [1.0, 0.0, 0.0]
        azul = np.zeros((10, 10, 3))
        azul[:] = [0.0, 0.0, 1.0]
        vf = {"vista": "frente", "imagem": vermelha, "mascara": np.ones((10, 10), dtype=bool),
              "visivel": np.array([True]), "peso_face": np.array([0.894])}
        ve = {"vista": "esquerda", "imagem": azul, "mascara": np.ones((10, 10), dtype=bool),
              "visivel": np.array([True]), "peso_face": np.array([0.447])}
        for ordem in ([vf, ve], [ve, vf]):
            tex, pintado, _, _ = projecao.rasterizar_textura(
                verts, faces, norm, fuv, ordem, 16, centro, (1.0, 1.0, 1.0), 2.0)
            self.assertGreater(int(pintado.sum()), 0)
            self.assertTrue(np.all(tex[pintado] == np.array([1.0, 0.0, 0.0])))

    def test_mascara_rejeita_amostra(self):
        # D6: caminho amostra_ok = mascara & facing nunca era exercitado
        # (todos os testes usavam mascara toda-verdadeira).
        verts, faces, norm, fuv = self._triangulo()
        img = np.zeros((10, 10, 3))
        img[:] = [1.0, 0.0, 0.0]
        vista = {"vista": "frente", "imagem": img, "mascara": np.zeros((10, 10), dtype=bool),
                 "visivel": np.array([True]), "peso_face": np.array([1.0])}
        _, pintado, _, _ = projecao.rasterizar_textura(
            verts, faces, norm, fuv, [vista], 16, np.array([0.0, 0.0, 0.5]), (1.0, 1.0, 1.0), 2.0)
        self.assertEqual(int(pintado.sum()), 0)

    def test_uv_degenerada_pula_sem_quebrar(self):
        # D6: triangulo UV colinear (area zero) nao pinta nada e nao quebra.
        verts, faces, norm, _ = self._triangulo()
        fuv = np.array([[[0.0, 0.0], [0.5, 0.5], [1.0, 1.0]]])
        img = np.zeros((10, 10, 3))
        img[:] = [1.0, 0.0, 0.0]
        vista = {"vista": "frente", "imagem": img, "mascara": np.ones((10, 10), dtype=bool),
                 "visivel": np.array([True]), "peso_face": np.array([1.0])}
        _, pintado, _, info = projecao.rasterizar_textura(
            verts, faces, norm, fuv, [vista], 16, np.array([0.0, 0.0, 0.5]), (1.0, 1.0, 1.0), 2.0)
        self.assertEqual(int(pintado.sum()), 0)
        self.assertEqual(info["faces_pintadas_por_vista"]["frente"], 0)

    def test_override_de_alinhamento_e_usado(self):
        # Imagem azul com 1 px vermelho no canto (9, 9). No caminho v1, as
        # amostras alcancam o canto (clip) e algum texel sai vermelho; com
        # um override que desloca o mapeamento para dentro, nenhum texel
        # alcanca o canto - mas o bake continua pintando (azul). Se o
        # override fosse ignorado, os dois resultados seriam iguais.
        # Centro = origem: o teste isola o override (sem o deslocamento
        # de centro que o teste de faixas abaixo exercita).
        verts, faces, norm, fuv = self._triangulo()
        img = np.zeros((10, 10, 3))
        img[:] = [0.0, 0.0, 1.0]
        img[9, 9] = [1.0, 0.0, 0.0]
        base = {"vista": "frente", "imagem": img, "mascara": np.ones((10, 10), dtype=bool),
                "visivel": np.array([True]), "peso_face": np.array([1.0])}
        tex_v1, pin_v1, _, info_v1 = projecao.rasterizar_textura(
            verts, faces, norm, fuv, [dict(base)], 16, np.array([0.0, 0.0, 0.0]),
            (1.0, 1.0, 1.0), 2.0)
        self.assertEqual(info_v1["alinhamento_usado"]["frente"], "bbox")
        self.assertTrue(np.any(np.all(tex_v1[pin_v1] == np.array([1.0, 0.0, 0.0]), axis=1)))
        v2 = dict(base, alinhamento=(1.0, -5.0, 1.0, -2.0))
        tex_ov, pin_ov, _, info_ov = projecao.rasterizar_textura(
            verts, faces, norm, fuv, [v2], 16, np.array([0.0, 0.0, 0.0]),
            (1.0, 1.0, 1.0), 2.0)
        self.assertEqual(info_ov["alinhamento_usado"]["frente"], "otimizado")
        self.assertGreater(int(pin_ov.sum()), 0)
        self.assertFalse(np.any(np.all(tex_ov[pin_ov] == np.array([1.0, 0.0, 0.0]), axis=1)))

    def test_amostragem_usa_centro_faixas(self):
        # COR-08/A0: arte em faixas horizontais (topo vermelho, meio verde,
        # base azul) sobre o triangulo vertical com centro z = 0,5. A
        # amostragem tem de subtrair o centro, como ``projetar`` faz: o
        # texel do vertice da base (UV (0, 0) -> texel (0, 15)) tem de sair
        # azul, e o do vertice do topo (UV (0, 1) -> texel (0, 0)), vermelho.
        # Sem a subtracao, a base amostraria verde (deslocamento de
        # (0,5 / ortho) * altura) e o teste falharia - e foi exatamente
        # assim que o defeito foi achado: teste de cor solida nao o ve.
        verts, faces, norm, fuv = self._triangulo()
        img = np.zeros((10, 10, 3))
        img[0:3] = [1.0, 0.0, 0.0]
        img[3:7] = [0.0, 1.0, 0.0]
        img[7:10] = [0.0, 0.0, 1.0]
        vista = {"vista": "frente", "imagem": img, "mascara": np.ones((10, 10), dtype=bool),
                 "visivel": np.array([True]), "peso_face": np.array([1.0])}
        tex, pintado, _, _ = projecao.rasterizar_textura(
            verts, faces, norm, fuv, [vista], 16, np.array([0.0, 0.0, 0.5]),
            (1.0, 1.0, 1.0), 2.0)
        self.assertTrue(pintado[15, 0])
        self.assertTrue(np.all(tex[15, 0] == np.array([0.0, 0.0, 1.0])))
        self.assertTrue(pintado[0, 0])
        self.assertTrue(np.all(tex[0, 0] == np.array([1.0, 0.0, 0.0])))
        cores = {tuple(c) for c in tex[pintado]}
        self.assertIn((0.0, 1.0, 0.0), cores)

    def test_dilatacao_nao_atravessa_borda(self):
        # D6: o np.roll com anulacao da faixa nao pode vazar para o lado oposto.
        tex = np.zeros((5, 5, 3))
        tex[0, 0] = [1.0, 0.0, 0.0]
        pin = np.zeros((5, 5), dtype=bool)
        pin[0, 0] = True
        _, pin2, _ = projecao.dilatar(tex, pin, 1)
        self.assertTrue(pin2[1, 0] and pin2[0, 1])
        self.assertFalse(pin2[4, 0] or pin2[0, 4] or pin2[4, 4])

    def test_dilatacao_preenche_e_para(self):
        tex = np.zeros((5, 5, 3))
        tex[2, 2] = [1.0, 0.0, 0.0]
        pin = np.zeros((5, 5), dtype=bool)
        pin[2, 2] = True
        tex2, pin2, n = projecao.dilatar(tex, pin, 1)
        self.assertEqual(n, 4)
        self.assertTrue(pin2[1, 2] and pin2[3, 2] and pin2[2, 1] and pin2[2, 3])
        self.assertTrue(np.all(tex2[pin2] == np.array([1.0, 0.0, 0.0])))
        _, pin3, n3 = projecao.dilatar(tex2, pin2, 0)
        self.assertEqual(n3, 0)
        self.assertTrue(np.array_equal(pin3, pin2))


class TestMetricasUV(unittest.TestCase):
    def test_quadrado_sem_distorcao_uma_ilha(self):
        fuv = np.array([[[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]],
                        [[0.0, 0.0], [1.0, 1.0], [0.0, 1.0]]])
        met = projecao.metricas_uv(fuv, np.array([0.5, 0.5]), 16)
        self.assertAlmostEqual(met["distorcao_media"], 0.0, places=4)
        self.assertAlmostEqual(met["ocupacao"], 1.0, places=2)
        self.assertEqual(met["ilhas"], 1)
        self.assertIsNone(met["margem_min_px"])

    def test_distorcao_diferente_de_zero(self):
        # D6: areas UV desiguais com areas 3D iguais tem de dar distorcao > 0.
        # (A distorcao mede distribuicao relativa, nao escala absoluta.)
        fuv = np.array([[[0.0, 0.0], [0.2, 0.0], [0.0, 1.0]],
                        [[0.0, 0.0], [1.8, 0.0], [0.0, 1.0]]])
        met = projecao.metricas_uv(fuv, np.array([0.5, 0.5]), 16)
        self.assertGreater(met["distorcao_media"], 0.5)

    def test_quadrados_separados_duas_ilhas(self):
        # Vizinhos horizontais (mesma faixa de linhas) para a varredura medir.
        fuv = np.array([[[0.0, 0.0], [0.4, 0.0], [0.4, 0.4]],
                        [[0.0, 0.0], [0.4, 0.4], [0.0, 0.4]],
                        [[0.6, 0.0], [1.0, 0.0], [1.0, 0.4]],
                        [[0.6, 0.0], [1.0, 0.4], [0.6, 0.4]]])
        met = projecao.metricas_uv(fuv, np.array([0.08, 0.08, 0.08, 0.08]), 20)
        self.assertEqual(met["ilhas"], 2)
        self.assertIsNotNone(met["margem_min_px"])
        self.assertGreater(met["margem_min_px"], 0)


if __name__ == "__main__":
    unittest.main()
