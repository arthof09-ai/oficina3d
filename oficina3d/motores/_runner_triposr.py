"""Runner do TripoSR (MIT). Roda no Python do motor (.venv_triposr), num subprocesso.

Uso (só pelo oficina3d.motores.gerar):
    python -u _runner_triposr.py <pasta>\\pedido_motor.json
cwd = motores\\TripoSR; ambiente = config.env_subprocesso() (HF_HOME, TEMP...); HF_HUB_OFFLINE=1.

Como na v1: API do repositório (`tsr.system.TSR`, igual ao run.py), SEM rembg (as imagens de
preproc\\ já vêm com fundo transparente), malha com cor de vértice e GLB DE VERDADE exportado
pelo trimesh. Não usa o caminho --bake-texture do run.py (ele grava OBJ mesmo com extensão
.glb). Orientação Y para cima igual ao gradio_app.py do repo. O torchmcubes deste PC é o
substituto em CPU (instalacao/compat, ligado por .pth no venv).
Este arquivo NÃO importa nada do app.
"""
import inspect
import json
import os
import sys
import threading
import time
import traceback


def progresso(pct, msg):
    print(f"PROGRESSO {int(pct)} {msg}", flush=True)


def gravar_json(caminho, dados):
    tmp = caminho + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    os.replace(tmp, caminho)


def executar(pedido):
    t0 = time.time()
    repo_motor = pedido["repo_motor"]
    if repo_motor not in sys.path:
        sys.path.insert(0, repo_motor)

    pico_ram = [0]
    parar = threading.Event()
    progresso(1, "carregando bibliotecas")
    try:
        import psutil
        proc = psutil.Process()

        def amostrar():
            while not parar.is_set():
                pico_ram[0] = max(pico_ram[0], proc.memory_info().rss)
                time.sleep(0.5)
        threading.Thread(target=amostrar, daemon=True).start()
    except ImportError:
        psutil = None

    import numpy as np
    import torch
    import trimesh
    from PIL import Image
    from tsr.system import TSR

    avisos = []
    dispositivo = "cuda" if torch.cuda.is_available() else "cpu"
    if dispositivo == "cpu":
        avisos.append("TripoSR rodou na CPU (CUDA indisponível)")

    progresso(10, "carregando modelo TripoSR")
    modelo = TSR.from_pretrained(pedido.get("pesos") or "stabilityai/TripoSR",
                                 config_name="config.yaml", weight_name="model.ckpt")
    modelo.renderer.set_chunk_size(int(pedido.get("chunk") or 8192))
    modelo.to(dispositivo)
    t_carga = time.time() - t0
    progresso(40, "modelo carregado")

    caminho = pedido["imagens"][0]["caminho"]
    imagem = Image.open(caminho).convert("RGBA")
    proporcao = float(pedido.get("proporcao_frente") or 0.85)
    try:
        from tsr.utils import resize_foreground
        imagem = resize_foreground(imagem, proporcao)   # recorta pelo alfa e centraliza, como o run.py
    except Exception as e:  # noqa: BLE001
        avisos.append(f"resize_foreground não aplicado: {e}")
    # Fundo cinza 0,5 sob o alfa (igual ao run.py / gradio_app.py do repo).
    arr = np.array(imagem).astype(np.float32) / 255.0
    arr = arr[:, :, :3] * arr[:, :, 3:4] + (1 - arr[:, :, 3:4]) * 0.5
    imagem = Image.fromarray((arr * 255.0).astype(np.uint8))

    if dispositivo == "cuda":
        torch.cuda.reset_peak_memory_stats()
    t1 = time.time()
    progresso(50, "gerando campo 3D")
    with torch.no_grad():
        codigos = modelo([imagem], device=dispositivo)
    progresso(75, "extraindo malha (marching cubes)")
    resolucao = int(pedido.get("mc_resolucao") or 256)
    params = inspect.signature(modelo.extract_mesh).parameters
    if "has_vertex_color" in params:
        malhas = modelo.extract_mesh(codigos, True, resolution=resolucao)
    else:  # versões antigas do repo: sem o parâmetro (cor de vértice sempre ligada)
        malhas = modelo.extract_mesh(codigos, resolution=resolucao)
    mesh = malhas[0]
    t_gera = time.time() - t1
    if mesh is None or len(mesh.faces) == 0:
        raise RuntimeError("o TripoSR devolveu malha vazia")

    # Orientação do gradio_app.py do TripoSR: Y para cima, frente para +Z.
    mesh.apply_transform(trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0]))
    mesh.apply_transform(trimesh.transformations.rotation_matrix(np.pi / 2, [0, 1, 0]))

    progresso(90, "gravando forma.glb")
    saida = pedido["saida_glb"]
    mesh.export(saida, file_type="glb")
    with open(saida, "rb") as f:
        if f.read(4) != b"glTF":
            raise RuntimeError("o arquivo gravado não é GLB (cabeçalho glTF ausente)")
    parar.set()
    tem_cor = getattr(getattr(mesh, "visual", None), "kind", None) == "vertex"
    metricas = {
        "modelo": "stabilityai/TripoSR", "mc_resolucao": resolucao, "dispositivo": dispositivo,
        "vistas": [pedido["imagens"][0].get("vista") or "frente"],
        "tempo_carga_s": round(t_carga, 1), "tempo_geracao_s": round(t_gera, 1),
        "tempo_s": round(time.time() - t0, 1),
        "vram_pico_torch_mb": (torch.cuda.max_memory_allocated() // 2**20) if dispositivo == "cuda" else 0,
        "vram_reservada_pico_mb": (torch.cuda.max_memory_reserved() // 2**20) if dispositivo == "cuda" else 0,
        "ram_pico_mb": (pico_ram[0] // 2**20) if psutil else None,
        "vertices": int(mesh.vertices.shape[0]), "triangulos": int(mesh.faces.shape[0]),
        "fechada": bool(mesh.is_watertight), "cor_de_vertice": bool(tem_cor),
        "bytes_glb": os.path.getsize(saida), "eixo_cima": "Y",
    }
    return {"ok": True, "glb": saida, "metricas": metricas, "avisos": avisos}


def main():
    if len(sys.argv) != 2:
        print("uso: _runner_triposr.py <pedido_motor.json>", file=sys.stderr)
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        pedido = json.load(f)
    try:
        res = executar(pedido)
    except BaseException as e:  # noqa: BLE001
        tb = traceback.format_exc()
        print(tb, file=sys.stderr, flush=True)
        gravar_json(pedido["resultado"], {"ok": False, "erro": f"{type(e).__name__}: {e}", "traceback": tb})
        return 1
    gravar_json(pedido["resultado"], res)
    progresso(100, "pronto")
    print("RESULTADO", json.dumps(res["metricas"], ensure_ascii=False), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
