"""Fase 0: teste real do Hunyuan3D-2 (forma) no PC do irmão, com perfil de memória do 2GP.

Uso:
  python teste_fase0_hunyuan.py --modelo mini --imagem orc.png --saida pasta
  python teste_fase0_hunyuan.py --modelo mv --vista front=f.png --vista back=c.png --vista left=e.png --vista right=d.png --saida pasta
Opções: --perfil 4 --passos 30 --octree 256 --orcamento 2200 --flashvdm --chunks 8000 --rotulo nome
Mede: tempo de carga, tempo de geração, VRAM de pico (torch), RAM de pico do processo,
triângulos/vértices, se a malha é fechada. Grava GLB + relatorio JSON na pasta de saída.
"""
import argparse
import json
import os
import sys
import threading
import time

os.environ.setdefault("HY3DGEN_MODELS", r"E:\RPG_Assimilacao\Oficina3D\_cache\hy3dgen")
sys.path.insert(0, r"E:\RPG_Assimilacao\Oficina3D\motores\Hunyuan3D-2GP")

import psutil
import torch
from PIL import Image

MODELOS = {
    "mini": ("tencent/Hunyuan3D-2mini", "hunyuan3d-dit-v2-mini"),
    "full": ("tencent/Hunyuan3D-2", "hunyuan3d-dit-v2-0"),
    "mv": ("tencent/Hunyuan3D-2mv", "hunyuan3d-dit-v2-mv"),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modelo", choices=MODELOS, default="mini")
    ap.add_argument("--imagem")
    ap.add_argument("--vista", action="append", default=[], help="front|back|left|right=arquivo (modelo mv)")
    ap.add_argument("--saida", required=True)
    ap.add_argument("--perfil", type=int, default=4)
    ap.add_argument("--passos", type=int, default=30)
    ap.add_argument("--octree", type=int, default=256)
    ap.add_argument("--orcamento", type=int, default=2200, help="MB de VRAM por modelo no mmgp (perfis 2/4/5)")
    ap.add_argument("--chunks", type=int, default=8000)
    ap.add_argument("--flashvdm", action="store_true")
    ap.add_argument("--rotulo", default="")
    a = ap.parse_args()
    os.makedirs(a.saida, exist_ok=True)

    proc = psutil.Process()
    pico_ram = [0]
    parar = threading.Event()

    def amostrar():
        while not parar.is_set():
            pico_ram[0] = max(pico_ram[0], proc.memory_info().rss)
            time.sleep(0.5)

    threading.Thread(target=amostrar, daemon=True).start()

    from mmgp import offload
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
    from hy3dgen.shapegen.pipelines import export_to_trimesh

    t0 = time.time()
    repo, sub = MODELOS[a.modelo]
    pipe = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(repo, subfolder=sub, use_safetensors=True, device="cuda")
    if a.flashvdm:
        # 'mc' em vez de 'dmc': o 'dmc' exige o pacote diso (compilação CUDA).
        pipe.enable_flashvdm(mc_algo="mc")
    # Mesmo esquema do gradio_app.py do 2GP para perfis de pouca VRAM.
    setattr(type(pipe), "_execution_device", property(lambda self: "cuda"))
    modelos = offload.extract_models("i23d_worker", pipe)
    kwargs = {}
    if a.perfil < 5:
        kwargs["pinnedMemory"] = "i23d_worker/model"
    if a.perfil not in (1, 3):
        kwargs["budgets"] = {"*": a.orcamento}
    offload.profile(modelos, profile_no=a.perfil, verboseLevel=1, **kwargs)
    t_carga = time.time() - t0

    if a.vista:
        img = {k: Image.open(v).convert("RGBA") for k, v in (x.split("=", 1) for x in a.vista)}
        nome = "mv_" + "-".join(img)
    else:
        img = Image.open(a.imagem).convert("RGBA")
        nome = os.path.splitext(os.path.basename(a.imagem))[0]
    torch.cuda.reset_peak_memory_stats()
    t1 = time.time()
    gen = torch.Generator().manual_seed(1234)
    out = pipe(image=img, num_inference_steps=a.passos, guidance_scale=5.0, generator=gen,
               octree_resolution=a.octree, num_chunks=a.chunks, output_type="mesh")
    t_gera = time.time() - t1
    mesh = export_to_trimesh(out)[0]
    t_total = time.time() - t0
    parar.set()

    tag = f"{nome}_hunyuan_{a.modelo}_p{a.perfil}_s{a.passos}_o{a.octree}_b{a.orcamento}" + ("_fvdm" if a.flashvdm else "") + (f"_{a.rotulo}" if a.rotulo else "")
    glb = os.path.join(a.saida, tag + ".glb")
    mesh.export(glb)
    rel = {
        "motor": f"{repo}/{sub}", "perfil_mmgp": a.perfil, "orcamento_mb": a.orcamento, "flashvdm": a.flashvdm,
        "passos": a.passos, "octree": a.octree, "chunks": a.chunks, "seed": 1234,
        "entrada": a.vista or a.imagem, "glb": glb, "bytes_glb": os.path.getsize(glb),
        "tempo_carga_s": round(t_carga, 1), "tempo_geracao_s": round(t_gera, 1), "tempo_total_s": round(t_total, 1),
        "vram_pico_torch_mb": torch.cuda.max_memory_allocated() // 2**20,
        "vram_reservada_pico_mb": torch.cuda.max_memory_reserved() // 2**20,
        "ram_pico_processo_mb": pico_ram[0] // 2**20,
        "vertices": int(mesh.vertices.shape[0]), "triangulos": int(mesh.faces.shape[0]),
        "fechada": bool(mesh.is_watertight),
    }
    with open(os.path.join(a.saida, f"relatorio_{tag}.json"), "w", encoding="utf-8") as f:
        json.dump(rel, f, ensure_ascii=False, indent=2)
    print("RELATORIO", json.dumps(rel, ensure_ascii=False))


if __name__ == "__main__":
    main()
