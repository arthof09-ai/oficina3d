"""Isola xatlas nativo em subprocesso e registra inclusive abort sem traceback."""
import json
import importlib.metadata
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def filho():
    print("inicio", flush=True)
    import numpy as np
    import xatlas
    print("imports OK", flush=True)
    # Tetraedro independente de trimesh/arquivos e de qualquer arte do projeto.
    vertices = np.array([[0., 0., 0.], [1., 0., 0.], [0., 1., 0.], [0., 0., 1.]], dtype=np.float32)
    faces = np.array([[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3]], dtype=np.uint32)
    atlas = xatlas.Atlas()
    print("Atlas OK", flush=True)
    atlas.add_mesh(vertices, faces)
    print("add_mesh OK", flush=True)
    chart, pack = xatlas.ChartOptions(), xatlas.PackOptions()
    pack.padding, pack.resolution = 8, 2048
    print("antes generate", flush=True)
    atlas.generate(chart, pack)
    print("generate OK", flush=True)
    mapping, indices, uv = atlas.get_mesh(0)
    assert len(indices) == 4 and len(uv) == len(mapping)
    print(json.dumps({"faces": len(indices), "vertices_uv": len(uv), "atlas_count": atlas.atlas_count}), flush=True)


def main():
    if "--filho" in sys.argv:
        filho()
        return 0
    start = time.perf_counter()
    cmd = [sys.executable, "-X", "utf8", "-X", "faulthandler", "-B", __file__, "--filho"]
    timeout = False
    try:
        run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60)
        code, stdout, stderr = run.returncode, run.stdout, run.stderr
    except subprocess.TimeoutExpired as exc:
        timeout = True
        code = None
        stdout = (exc.stdout or b"").decode("utf-8", errors="replace")
        stderr = (exc.stderr or b"").decode("utf-8", errors="replace")
    data = {"comando": cmd, "exit_code": code, "timeout_60s": timeout,
            "numpy": importlib.metadata.version("numpy"), "xatlas": importlib.metadata.version("xatlas"),
            "parede_s": round(time.perf_counter() - start, 6), "stdout": stdout, "stderr": stderr,
            "gpu": "nao usada", "blender": "nao executado", "cpu_filho_s": "nao medido",
            "pico_memoria_filho": "nao medido", "vram": "nao medido"}
    label = sys.argv[1] if len(sys.argv) > 1 else "xatlas-isolado"
    if not label.replace("-", "").isalnum():
        raise ValueError("rotulo invalido")
    path = ROOT / f"docs/evidencias-nuvem/{label}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))
    return 0 if code == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
