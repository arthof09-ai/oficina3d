"""python -m oficina3d.validar <arquivo.glb> [--perfil oficina|jogo] [--saida PASTA] [--json]

Código de saída: 0 = aprovado, 1 = reprovado, 2 = erro do próprio validador.
"""
import argparse
import json
import sys

from oficina3d.validar import PERFIS, ErroValidacao, validar


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m oficina3d.validar",
                                 description="Valida um GLB para o Godot (estrutura + carga headless).")
    ap.add_argument("glb")
    ap.add_argument("--perfil", choices=sorted(PERFIS), default="oficina")
    ap.add_argument("--saida", help="pasta onde gravar validacao.json")
    ap.add_argument("--max-triangulos", type=int)
    ap.add_argument("--json", action="store_true", help="imprime o relatório inteiro em JSON")
    a = ap.parse_args(argv)
    try:
        r = validar(a.glb, a.saida, {"perfil": a.perfil, "max_triangulos": a.max_triangulos})
    except ErroValidacao as e:
        print(f"ERRO do validador: {e}", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(("APROVADO" if r["aprovado"] else "REPROVADO") + f"  perfil={r['perfil']}  ({r['tempo_s']} s)")
        for x in r["regras"]:
            marca = "ok " if x["ok"] else ("ERRO" if x["severidade"] == "erro" else "aviso")
            extra = f"  [{x['valor']} / {x['limite']}]" if x["limite"] is not None else ""
            print(f"  {marca:5} {x['id']}: {x['msg']}{extra}")
        for p in r["pendente"]:
            print(f"  PENDENTE {p}")
    return 0 if r["aprovado"] else 1


if __name__ == "__main__":
    sys.exit(main())
