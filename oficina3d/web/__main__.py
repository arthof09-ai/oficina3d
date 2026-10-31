"""python -m oficina3d.web [--porta 8765] — sobe a página só em 127.0.0.1 (não há opção de host)."""
import argparse
import sys
import tempfile

from . import HOST, PORTA


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Página e API da Oficina 3D (só 127.0.0.1)")
    ap.add_argument("--porta", type=int, default=PORTA)
    a = ap.parse_args(argv)
    if not 1024 <= a.porta <= 65535:
        print("porta inválida (1024–65535)", file=sys.stderr)
        return 2

    from .. import config
    # Uploads grandes são guardados em arquivo temporário pelo servidor: no _cache\tmp da Oficina, não no TEMP do C:.
    config.TMP.mkdir(parents=True, exist_ok=True)
    tempfile.tempdir = str(config.TMP)

    import uvicorn
    from .app import criar_app

    print(f"Oficina 3D: http://{HOST}:{a.porta}  (Ctrl+C para parar)", file=sys.stderr)
    uvicorn.run(criar_app(), host=HOST, port=a.porta, log_level="info", proxy_headers=False,
                server_header=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
