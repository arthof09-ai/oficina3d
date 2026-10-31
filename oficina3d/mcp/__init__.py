"""Servidor MCP da Oficina 3D (v2).

Não importa a biblioteca `mcp` aqui (import preguiçoso em servidor.criar_servidor), para que
`oficina3d.mcp.seguranca` sirva também à página web e aos testes sem nada instalado.

    python -m oficina3d.mcp                 (stdio)
    python -m oficina3d.mcp --http          (HTTP local em 127.0.0.1:8766/mcp, exige token)
"""
