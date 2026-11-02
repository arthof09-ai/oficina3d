"""Extracao seletiva e verificavel dos patches publicos, sem merge de docs antigos.

Somente prepara arquivos da branch da missao; nao faz commits nem chama Blender.
"""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
FONTE = "31c2d88"
BASE_ANTIGA = "0e8746e"
BASE_NOVA = "5cd092d"
ARQUIVOS = ["oficina3d/cor/vertice.py", "oficina3d/cor/_blender_vertice.py",
            "oficina3d/cor/validacao_vertice.py", "testes/test_cor_amostragem.py",
            "testes/test_cor_colorimetria.py", "testes/test_cor_guardas.py",
            "testes/codex/glb_evidencia.py"]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def main():
    if git("branch", "--show-current").strip() != b"codex/auditoria-sem-pc":
        raise RuntimeError("branch fora da missao")
    fonte_sha = git("rev-parse", FONTE).decode().strip()
    rows = []
    # Tudo validado antes da primeira escrita: nao sobrescrever trabalho posterior.
    for name in ARQUIVOS:
        path = ROOT / name
        data = git("show", f"{fonte_sha}:{name}")
        if path.exists():
            old = git("show", f"{BASE_ANTIGA}:{name}")
            new = git("show", f"{BASE_NOVA}:{name}")
            if old != new or path.read_bytes().replace(b"\r\n", b"\n") != new:
                raise RuntimeError(f"reconciliacao manual necessaria: {name}")
        rows.append((path, data))
    manifest = {"fonte_commit": fonte_sha, "base_antiga": BASE_ANTIGA,
                "base_nova": BASE_NOVA, "arquivos": []}
    for path, data in rows:
        name = path.relative_to(ROOT).as_posix()
        if name == "testes/test_cor_colorimetria.py":
            data = data.replace(b"from codex.glb_evidencia", b"from testes.codex.glb_evidencia")
            data = data.replace(b"@unittest.skipUnless(achar_blender(), 'Blender nao encontrado')",
                                b"@unittest.skipUnless(not os.environ.get('OFICINA3D_AUDITORIA_SEM_PC') and achar_blender(), 'Blender nao executado nesta rodada sem PC')")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        original = git("show", f"{fonte_sha}:{name}")
        manifest["arquivos"].append({"arquivo": name,
            "sha256_fonte": hashlib.sha256(original).hexdigest(),
            "sha256_integrado": hashlib.sha256(data).hexdigest(),
            "adaptado": data != original})
    (ROOT / "testes/codex/__init__.py").write_text('"""Leitores puros das provas de CPU."""\n', encoding="utf-8")
    out = ROOT / "docs/evidencias-nuvem/integracao-manifesto.json"
    out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
