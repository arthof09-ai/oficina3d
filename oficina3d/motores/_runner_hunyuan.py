"""Runner do Hunyuan3D-2 (forma). Roda no Python do motor (.venv_app, ver INFRA-01 em DECISOES), num subprocesso.

Uso (só pelo oficina3d.motores.gerar):
    python -u _runner_hunyuan.py <pasta>\\pedido_motor.json
cwd = motores\\Hunyuan3D-2GP; ambiente = config.env_subprocesso() (HY3DGEN_MODELS, HF_HOME, TEMP...).

Lógica copiada do teste da Fase 0 da v1 (instalacao/teste_fase0_hunyuan.py, que funcionou):
from_pretrained -> enable_flashvdm(mc_algo="mc") -> _execution_device -> mmgp offload.profile
-> pipe(image=..., output_type="mesh") -> export_to_trimesh(out)[0] -> GLB.
Acréscimos da v1/v2: progresso por passo de difusão (embrulho do tqdm do hy3dgen), multivista
(dict front/back/left/right), resultado em JSON e linhas "PROGRESSO <0-100> <msg>" no stdout.
Este arquivo NÃO importa nada do app (o venv do motor não tem o pacote oficina3d).
"""
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


def instalar_progresso_tqdm():
    """Troca o `tqdm` dos módulos hy3dgen por um embrulho que imprime PROGRESSO a cada iteração.

    Difusão ("Diffusion Sampling") vai de 26 a 85%; decodificação do volume (FlashVDM) de 85 a 91%.
    Só embrulha chamadas com iterável (o `for ... in tqdm(...)` do pipeline); o resto passa direto.
    """
    import tqdm as tqdm_mod
    original = tqdm_mod.tqdm

    def embrulho(iterable=None, *args, **kwargs):
        barra = original(iterable, *args, **kwargs)
        if iterable is None:
            return barra
        desc = str(kwargs.get("desc") or "")
        total = kwargs.get("total")
        if total is None:
            try:
                total = len(iterable)
            except TypeError:
                total = None
        if "Diffusion" in desc:
            ini, fim, rotulo = 26, 85, "difusao"
        elif "Decoding" in desc or "Volume" in desc:
            ini, fim, rotulo = 85, 91, "decodificando volume"
        else:
            return barra

        def gerar_itens():
            if total:
                progresso(ini, f"{rotulo} 0/{total}")
            for i, item in enumerate(barra, 1):
                yield item
                if total:
                    progresso(ini + (fim - ini) * i / total, f"{rotulo} {i}/{total}")
        return gerar_itens()

    for nome, mod in list(sys.modules.items()):
        if nome.startswith("hy3dgen") and getattr(mod, "tqdm", None) is original:
            setattr(mod, "tqdm", embrulho)


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

    import torch
    from PIL import Image
    from mmgp import offload
    from hy3dgen.shapegen import Hunyuan3DDiTFlowMatchingPipeline
    from hy3dgen.shapegen.pipelines import export_to_trimesh

    if not torch.cuda.is_available():
        raise RuntimeError("CUDA indisponível neste Python (torch sem GPU)")

    repo, sub = pedido["repo"], pedido["subpasta"]
    progresso(5, f"carregando modelo {sub}")
    pipe = Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(repo, subfolder=sub, use_safetensors=True, device="cuda")
    if pedido.get("flashvdm"):
        # 'mc' em vez de 'dmc': o 'dmc' exige o pacote diso (compilação CUDA). Troca a VAE pela turbo.
        pipe.enable_flashvdm(mc_algo=pedido.get("mc_algo") or "mc")
    # Mesmo esquema do gradio_app.py do 2GP para perfis de pouca VRAM.
    setattr(type(pipe), "_execution_device", property(lambda self: "cuda"))
    modelos = offload.extract_models("i23d_worker", pipe)
    perfil = int(pedido.get("perfil_mmgp") or 4)
    kwargs = {}
    if perfil < 5:
        kwargs["pinnedMemory"] = "i23d_worker/model"
    if perfil not in (1, 3):
        kwargs["budgets"] = {"*": int(pedido.get("orcamento_mb") or 2200)}
    offload.profile(modelos, profile_no=perfil, verboseLevel=1, **kwargs)
    t_carga = time.time() - t0
    progresso(25, "modelo carregado")
    instalar_progresso_tqdm()

    vistas = [im.get("vista") or "frente" for im in pedido["imagens"]]
    if pedido.get("multivista"):
        img = {im["vista_motor"]: Image.open(im["caminho"]).convert("RGBA") for im in pedido["imagens"]}
    else:
        img = Image.open(pedido["imagens"][0]["caminho"]).convert("RGBA")

    torch.cuda.reset_peak_memory_stats()
    t1 = time.time()
    seed = int(pedido.get("seed") if pedido.get("seed") is not None else 1234)
    gen = torch.Generator().manual_seed(seed)
    passos = int(pedido.get("passos") or 30)
    out = pipe(image=img, num_inference_steps=passos, guidance_scale=float(pedido.get("guidance") or 5.0),
               generator=gen, octree_resolution=int(pedido.get("octree") or 256),
               num_chunks=int(pedido.get("chunks") or 8000), output_type="mesh")
    t_gera = time.time() - t1
    progresso(92, "convertendo malha")
    malhas = export_to_trimesh(out)
    mesh = malhas[0] if malhas else None
    if mesh is None or len(mesh.faces) == 0:
        raise RuntimeError("o motor devolveu malha vazia (superfície não encontrada no volume)")

    progresso(96, "gravando forma.glb")
    saida = pedido["saida_glb"]
    mesh.export(saida, file_type="glb")
    parar.set()
    metricas = {
        "modelo": f"{repo}/{sub}", "passos": passos, "octree": int(pedido.get("octree") or 256),
        "flashvdm": bool(pedido.get("flashvdm")), "seed": seed, "perfil_mmgp": perfil,
        "orcamento_mb": int(pedido.get("orcamento_mb") or 2200), "chunks": int(pedido.get("chunks") or 8000),
        "vistas": vistas,
        "tempo_carga_s": round(t_carga, 1), "tempo_geracao_s": round(t_gera, 1),
        "tempo_s": round(time.time() - t0, 1),
        "vram_pico_torch_mb": torch.cuda.max_memory_allocated() // 2**20,
        "vram_reservada_pico_mb": torch.cuda.max_memory_reserved() // 2**20,
        "ram_pico_mb": (pico_ram[0] // 2**20) if psutil else None,
        "vertices": int(mesh.vertices.shape[0]), "triangulos": int(mesh.faces.shape[0]),
        "fechada": bool(mesh.is_watertight), "bytes_glb": os.path.getsize(saida),
        "eixo_cima": "Y",
    }
    return {"ok": True, "glb": saida, "metricas": metricas, "avisos": []}


def main():
    if len(sys.argv) != 2:
        print("uso: _runner_hunyuan.py <pedido_motor.json>", file=sys.stderr)
        return 2
    with open(sys.argv[1], encoding="utf-8") as f:
        pedido = json.load(f)
    try:
        res = executar(pedido)
    except BaseException as e:  # noqa: BLE001 — qualquer falha vira resultado legível para o worker
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
