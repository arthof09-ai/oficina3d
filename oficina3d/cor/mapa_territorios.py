"""Mapa de territorios de vista da Etapa COR (P1).

Papel: carregar e VALIDAR o mapa de territorios (artefato
``territorios_<sujeito>.npz`` produzido pelo pacote P1 de auditoria) e
entregar ao bake os arrays de decisao da tranche P1. Este modulo NAO
calcula o mapa e NUNCA o recalcula dentro do app (laudo P1 §6: ~10 min
de Python puro por calculo; o caminho de producao e cache por malha,
consumido por hash).

ATENCAO - homonimo: este modulo NAO e o script
``adocao/p1/territorios.py`` (auditoria, roda fora do app e CALCULA o
mapa). O modulo do app apenas CONSOME o .npz, por hash.

Regras de seguranca (desenho P1, §1/§4.2, com as correcoes O2-C-P1-1/2):
1. O .npz carrega ``glb_sha256`` da malha para a qual foi calculado.
   Carga com SHA divergente do GLB do job = RECUSA tipada
   (``MapaIncompativel``): o bake PARA antes de pintar. Nunca usar
   mapa de outra malha silenciosamente.
2. A ordem das vistas vem do array ``vistas`` do .npz e e casada POR
   NOME com a ordem do pedido; divergencia de conjunto = recusa.
3. Mapa AUSENTE para a malha do job (arquivo inexistente) NAO e erro
   do bake: o chamador desliga a tranche com motivo registrado e o job
   segue pelo pipeline atual. Ausencia e estado conhecido do cache;
   divergencia e corrupcao.
4. ``piso`` em [0,5; 1,0) e ``d_ref`` > 0, com recusa (ValueError) fora
   da faixa: ``piso`` -> 0 degenera a P1.1 em rotulagem (P2) sem custo
   de fronteira; ``piso`` = 1 desliga a fatia (autoauditoria, D7).
"""
from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np

VISTAS_ORDEM = ["frente", "costas", "esquerda", "direita"]  # ordem do pedido


class MapaIncompativel(Exception):
    """Mapa nao pertence a esta malha / esta corrompido. Erro EXPLICITO:
    o bake PARA antes de pintar. (Diferente de mapa AUSENTE para a
    malha, que desliga a tranche com motivo e o job segue.)"""


class MapaTerritorios:
    def __init__(self, dados, sha_npz: str):
        self.sha_npz = sha_npz
        self.glb_sha256 = str(dados["glb_sha256"])
        self.vistas = [str(v) for v in dados["vistas"]]
        self.territorio_face = np.asarray(dados["territorio_face"])  # (F,) int8
        self.dist_geo_fronteira = np.asarray(dados["dist_geo_fronteira"])  # (F,) f32
        self.facing = np.asarray(dados["facing"])  # (F,4) f32
        self.fronteira_face = np.asarray(dados["fronteira_face"])  # (F,) bool
        # Arrays por texel (2048^2): usados SO na medicao offline e na
        # paridade com o laudo - a DECISAO dentro do bake e por face
        # (autoauditoria do desenho, defeito D1). Opcional: um .npz sem
        # eles ainda carrega para o bake; a medicao offline os exige.
        self.texel_territorio = (np.asarray(dados["texel_territorio"])
                                 if "texel_territorio" in dados else None)
        self.texel_vencedor = (np.asarray(dados["texel_vencedor"])
                               if "texel_vencedor" in dados else None)
        self.texel_anel_fronteira = (np.asarray(dados["texel_anel_fronteira"])
                                     if "texel_anel_fronteira" in dados else None)

    @property
    def n_faces(self) -> int:
        return len(self.territorio_face)


def carregar_mapa(caminho_npz, glb_bytes: bytes, n_faces_job: int) -> MapaTerritorios:
    """Valida e carrega. Levanta MapaIncompativel em qualquer divergencia.

    Validacoes (todas obrigatorias):
    - SHA-256 do GLB do job == campo ``glb_sha256`` do .npz;
    - nº de faces do mapa == nº de faces da malha extraida do job
      (a chave de juncao e o INDICE da face na ordem do primitivo do
      GLB - premissa validada na replica do laudo P1 §2: faces visiveis
      exatas nas 4 vistas contra o bake real);
    - conjunto de vistas do .npz == conjunto do pedido.
    """
    bruto = Path(caminho_npz).read_bytes()
    sha_npz = hashlib.sha256(bruto).hexdigest()
    with np.load(caminho_npz, allow_pickle=False) as dados:
        mapa = MapaTerritorios(dados, sha_npz)
    sha_job = hashlib.sha256(glb_bytes).hexdigest()
    if sha_job != mapa.glb_sha256:
        raise MapaIncompativel(
            f"mapa de outra malha: job {sha_job[:12]} x mapa {mapa.glb_sha256[:12]}")
    if mapa.n_faces != n_faces_job:
        raise MapaIncompativel(
            f"faces divergem: job {n_faces_job} x mapa {mapa.n_faces}")
    if set(mapa.vistas) != set(VISTAS_ORDEM):
        raise MapaIncompativel(f"vistas do mapa: {mapa.vistas}")
    return mapa


def validar_parametros_pesos(piso: float, d_ref: float) -> None:
    """Recusa (ValueError) parametros fora da faixa vetada do desenho."""
    if not 0.5 <= float(piso) < 1.0:
        raise ValueError(f"piso fora da faixa vetada [0,5; 1,0): {piso!r}")
    if not float(d_ref) > 0:
        raise ValueError(f"d_ref deve ser > 0: {d_ref!r}")


def fator_territorial(mapa: MapaTerritorios, piso: float, d_ref: float) -> np.ndarray:
    """Matriz (F, 4) de fatores de peso da P1.1, em VISTAS_ORDEM.

    fator[f, v] =
      1,0                          se territorio[f] == v (autoridade)
      1,0                          se territorio[f] == -1 (sem autoridade:
                                   nenhuma vista e penalizada)
      1 - (1-piso)*min(1, d/D_REF) se territorio[f] == w != v (disputa):
                                   na fronteira (d=0) a corrida e pura;
                                   no interior profundo do territorio
                                   alheio a intrusa paga o piso.

    Limites de desenho: piso em [0,5; 1,0), d_ref default 0,03 (~p90 da
    dist_geo medida: mediana 0,00416; p90 0,03045; max 0,13492 - laudo
    P1 §3.2). Deterministico: funcao pura dos arrays do mapa e de
    (piso, d_ref).
    """
    validar_parametros_pesos(piso, d_ref)
    terr = mapa.territorio_face.astype(np.int64)  # (F,)
    d = np.minimum(1.0, mapa.dist_geo_fronteira.astype(np.float64) / float(d_ref))
    fator_disputa = 1.0 - (1.0 - float(piso)) * d  # (F,)
    vistas_idx = np.arange(4)[None, :]  # (1,4)
    autoridade = (terr[:, None] == vistas_idx) | (terr[:, None] < 0)
    return np.where(autoridade, 1.0, fator_disputa[:, None]).astype(np.float32)


def fator_para_pedido(fator: np.ndarray, nomes_pedido: list) -> np.ndarray:
    """Reordena as colunas do fator (VISTAS_ORDEM) para a ordem do pedido.

    ``rasterizar_textura`` usa o indice da vista NA LISTA do pedido
    (vi); sem esta reordenacao, um pedido fora da ordem canonica
    aplicaria o pedágio da vista errada. Nomes desconhecidos = erro.
    """
    cols = []
    for nome in nomes_pedido:
        if nome not in VISTAS_ORDEM:
            raise ValueError(f"vista fora do conjunto canonico: {nome!r}")
        cols.append(VISTAS_ORDEM.index(nome))
    return np.asarray(fator)[:, cols]
