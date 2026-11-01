"""Etapa COR (T1/T5): cor por projecao das vistas canonicas + metricas de UV.

- ``projecao``: matematica pura (cameras, facing, rasterizacao, dilatacao,
  metricas de UV) - testavel sem Blender.
- ``_blender_cor``: script headless do Blender (mesmo padrao de
  ``oficina3d.refino._blender_refino``): importa o GLB refinado, calcula
  oclusao por BVH, faz o bake e exporta o GLB texturizado.
- ``rodar_cor``: dispara o script via ``oficina3d.refino.previa.rodar_blender``.

Estado (01/11/2026): T1-mecanismo - provado no cubo sintetico e no Orc
dourado; a integracao como etapa da fila de jobs e o proximo passo (nao
faz parte desta tranche). Ver docs/REGISTRO.md.
"""
from __future__ import annotations

from pathlib import Path

AQUI = Path(__file__).resolve().parent
SCRIPT_COR = AQUI / "_blender_cor.py"


def rodar_cor(pedido: dict, pasta: Path, progresso=None, timeout_s: float = 1800):
    """Roda o bake de cor no Blender headless; retorna o resultado JSON."""
    from oficina3d.refino import previa  # noqa: PLC0415 - evita ciclo na importacao

    return previa.rodar_blender(SCRIPT_COR, pedido, Path(pasta), "cor",
                                progresso=progresso, timeout_s=timeout_s)
