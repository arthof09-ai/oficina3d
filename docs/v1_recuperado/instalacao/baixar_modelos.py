"""Baixa só os arquivos de modelo necessários (fp16 .safetensors + config) para o E:.

Estrutura igual à que o Hunyuan3D-2GP procura em HY3DGEN_MODELS:
  <HY3DGEN_MODELS>/tencent/<repo>/<subpasta>/{config.yaml, model.fp16.safetensors}
TripoSR vai para o cache do Hugging Face (HF_HOME).
"""
import os
import sys
import time

from huggingface_hub import snapshot_download, hf_hub_download

BASE = r"E:\RPG_Assimilacao\Oficina3D\_cache"
HY3DGEN_MODELS = os.path.join(BASE, "hy3dgen")

HUNYUAN = [
    ("tencent/Hunyuan3D-2mini", "hunyuan3d-dit-v2-mini"),
    ("tencent/Hunyuan3D-2mini", "hunyuan3d-vae-v2-mini"),
    ("tencent/Hunyuan3D-2mv", "hunyuan3d-dit-v2-mv"),
    ("tencent/Hunyuan3D-2", "hunyuan3d-dit-v2-0"),
    ("tencent/Hunyuan3D-2", "hunyuan3d-vae-v2-0"),
]


def baixar_hunyuan(repo, sub):
    destino = os.path.join(HY3DGEN_MODELS, *repo.split("/"))
    snapshot_download(
        repo_id=repo,
        allow_patterns=[f"{sub}/config.yaml", f"{sub}/model.fp16.safetensors"],
        local_dir=destino,
    )
    return os.path.join(destino, sub)


def main():
    pedidos = sys.argv[1:] or ["hunyuan", "triposr"]
    t0 = time.time()
    if "hunyuan" in pedidos:
        for repo, sub in HUNYUAN:
            t = time.time()
            pasta = baixar_hunyuan(repo, sub)
            arquivos = {f: os.path.getsize(os.path.join(pasta, f)) for f in os.listdir(pasta)}
            print(f"OK {repo}/{sub} em {time.time() - t:.0f}s: {arquivos}", flush=True)
    if "triposr" in pedidos:
        t = time.time()
        for f in ("config.yaml", "model.ckpt"):
            p = hf_hub_download("stabilityai/TripoSR", f)
            print(f"OK stabilityai/TripoSR/{f} {os.path.getsize(p)} B em {time.time() - t:.0f}s", flush=True)
    print(f"Total: {(time.time() - t0) / 60:.1f} min")


if __name__ == "__main__":
    main()
