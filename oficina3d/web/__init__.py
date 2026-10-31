"""Página e API HTTP da Oficina 3D (v2).

    python -m oficina3d.web [--porta 8765]   ->  http://127.0.0.1:8765   (API em /api/..., documentação em /docs)

Só escuta em 127.0.0.1 (nada exposto à rede). Pedido que não venha mesmo deste PC (túnel, proxy,
Host estranho) precisa de token — mesmas regras do MCP por HTTP (oficina3d.mcp.seguranca).
Este __init__ não importa o FastAPI: o app fica em oficina3d.web.app (criar_app).
"""
HOST = "127.0.0.1"
PORTA = 8765
VERSAO = "2.0.0"
