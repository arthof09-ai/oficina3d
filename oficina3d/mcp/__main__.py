"""python -m oficina3d.mcp [--http] [--porta 8766]"""
import sys

from .servidor import main

sys.exit(main())
