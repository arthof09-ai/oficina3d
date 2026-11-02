"""Verificacao final somente-leitura do Git/codigo, com manifesto textual da rodada."""
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = "5cd092d37bddf36a2d888404936d4c9f394528c4"
OUT = ROOT / "docs/evidencias-nuvem"


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode("utf-8").strip()


def main():
    assert git("branch", "--show-current") == "codex/auditoria-sem-pc"
    assert git("rev-parse", "main") == BASE
    assert not git("ls-files", "MISSAO.md")
    suite = json.loads((OUT / "suite-final.json").read_text(encoding="utf-8"))
    assert suite["falhas"] == suite["erros"] == 0
    assert suite["testes_executados"] == suite["passaram"] + len(suite["skips"])
    manifesto = json.loads((OUT / "integracao-manifesto.json").read_text(encoding="utf-8"))
    hashes = {}
    for entry in manifesto["arquivos"]:
        path = ROOT / entry["arquivo"]
        sha = hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()
        assert sha == entry["sha256_integrado"], path
        hashes[entry["arquivo"]] = sha
    preservados = []
    for name in ("projecao.py", "_blender_cor.py", "preenchimento.py", "passo.py"):
        path = "oficina3d/cor/" + name
        original = subprocess.check_output(["git", "show", f"{BASE}:{path}"], cwd=ROOT)
        assert original == (ROOT / path).read_bytes().replace(b"\r\n", b"\n")
        preservados.append(path)
    fontes = [*sorted((ROOT / "oficina3d").rglob("*.py")), *sorted((ROOT / "testes").rglob("*.py"))]
    for path in fontes:
        compile(path.read_text(encoding="utf-8-sig"), str(path), "exec")
    alterados = set(git("diff", "--name-only", BASE).splitlines())
    alterados.update(git("ls-files", "--others", "--exclude-standard").splitlines())
    for name in alterados:
        assert Path(name).suffix in {".py", ".md", ".json", ".txt"}, name
    baseline = (OUT / "baseline-completa.txt").read_text(encoding="utf-8")
    aprovado_baseline = sum(line.endswith(" ... ok") for line in baseline.splitlines())
    assert aprovado_baseline == 293
    data = {"base_main_preservada": BASE, "branch": git("branch", "--show-current"),
            "head_antes_fechamento": git("rev-parse", "HEAD"),
            "arquivos_bake_preservados": preservados, "sha256_integracao_normalizado_lf": hashes,
            "fontes_python_compiladas_sem_executar": len(fontes),
            "alteracoes_somente_textuais": True, "MISSAO_md_preservado_fora_dos_commits": True,
            "baseline_aprovacoes_contadas_no_log": aprovado_baseline,
            "baseline_aprovacoes_json_antigo": 292,
            "motivo_correcao": "erro setUpClass nao conta como metodo executado; runner novo usa addSuccess",
            "suite_final": {k: suite[k] for k in ("testes_executados", "passaram", "falhas", "erros", "skips")},
            "gpu": "nao usada", "blender": "nao executado", "qualidade_visual": "nao medida"}
    (OUT / "fechamento.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
