"""Etapa COR (T1/T5/T2): cor por projecao das vistas canonicas + metricas
de UV + cor de vertice (rascunho/rede de seguranca).

- ``projecao``: matematica pura (cameras, facing, rasterizacao, dilatacao,
  metricas de UV) - testavel sem Blender.
- ``preenchimento``: preenchimento 3D das zonas cegas (COR-08/A3) -
  difusao por adjacencia da malha com solda, no lugar da dilatacao UV.
- ``vertice``: matematica pura do T2 (amostragem das vistas nos vertices,
  mescla da cor da forma, propagacao pela malha) - testavel sem Blender.
- ``_blender_cor``: script headless do Blender (mesmo padrao de
  ``oficina3d.refino._blender_refino``): importa o GLB refinado, calcula
  oclusao por BVH, faz o bake e exporta o GLB texturizado.
- ``_blender_vertice``: idem para o T2 - escreve COLOR_0 (sem textura),
  com a cor da forma (TripoSR) como fonte secundaria.
- ``rodar_cor`` / ``rodar_vertice``: disparam os scripts via
  ``oficina3d.refino.previa.rodar_blender``.

Estado (01/11/2026): T1-mecanismo provado e integrado a fila (COR-05);
T2 (cor de vertice) integrado como modo ``cor_modo=vertice`` da mesma
etapa (COR-07). Ver docs/REGISTRO.md e docs/DECISOES.md.
"""
from __future__ import annotations

from pathlib import Path

AQUI = Path(__file__).resolve().parent
SCRIPT_COR = AQUI / "_blender_cor.py"
SCRIPT_VERTICE = AQUI / "_blender_vertice.py"


def rodar_cor(pedido: dict, pasta: Path, progresso=None, timeout_s: float = 1800):
    """Roda o bake de cor no Blender headless; retorna o resultado JSON."""
    from oficina3d.refino import previa  # noqa: PLC0415 - evita ciclo na importacao

    return previa.rodar_blender(SCRIPT_COR, pedido, Path(pasta), "cor",
                                progresso=progresso, timeout_s=timeout_s)


def rodar_vertice(pedido: dict, pasta: Path, progresso=None, timeout_s: float = 900):
    """Roda a cor de vertice no Blender headless; retorna o resultado JSON."""
    from oficina3d.refino import previa  # noqa: PLC0415 - evita ciclo na importacao

    return previa.rodar_blender(SCRIPT_VERTICE, pedido, Path(pasta), "vertice",
                                progresso=progresso, timeout_s=timeout_s)
