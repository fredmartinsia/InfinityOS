#!/usr/bin/env python3
"""
ingest_gate.py: apoio deterministico a ingestao de conhecimento com validade
temporal. NAO escreve no vault (isso e feito pelo agente via Write/Edit, que
passam pelo no_emdash guard e sao rastreaveis; o vault_guard bloqueia escrita
destrutiva por Bash de proposito). Este script so faz o que e seguro por Bash:
buscar relacionadas (read-only) e reindexar os indices.

Filosofia (decidida com o usuÃ¡rio em 2026-07-08):
  - O vault Obsidian e a UNICA fonte de verdade. LightRAG e FTS5 sao indices
    reconstruidos a partir dele, nunca escritos direto.
  - Toda decisao/mudanca vira nota em DECISOES/ com frontmatter temporal
    (status ativo|substituido|encerrado, data, projeto, supersede).
  - Quem julga contradicao e o Claude na sessao (custo zero). Este script da os
    dados (related) e o esqueleto (template); o agente grava e confirma.

Subcomandos:
  related "<termo>"                 read-only: notas do vault relacionadas (FTS5),
                                    pra o agente avaliar contradicao antes de gravar.
  template --project P --title T    imprime (stdout) frontmatter + path sugerido
    [--status ativo|encerrado]      pra o agente gravar via Write. Nao escreve nada.
    [--kind decisao|fato|mudanca]
    [--supersede <rel_path>]
  reindex                           FTS5 rebuild imediato + status do LightRAG.
"""
import argparse
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

VAULT = Path(os.environ.get("INFINITY_VAULT_PATH") or os.path.expanduser("~/Documents/Obsidian Vault"))
SCRIPTS = Path(os.path.expanduser("~/.claude/scripts"))
REINDEX_QUEUE = Path(os.path.expanduser("~/.claude/cache/lightrag_reindex_pending.txt"))

VALID_STATUS = ("ativo", "encerrado", "substituido")
VALID_KIND = ("decisao", "fato", "mudanca")


def _slug(text, maxlen=60):
    s = re.sub(r"[^\w\s-]", "", text.lower(), flags=re.UNICODE)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s[:maxlen] or "nota"


def _today():
    return datetime.now().strftime("%Y-%m-%d")


def cmd_related(term):
    """Reusa o FTS5 do vault_rag pra achar notas que podem conflitar."""
    sys.path.insert(0, str(SCRIPTS))
    try:
        import vault_rag as vr
    except Exception as e:
        print("ERRO ao importar vault_rag:", e, file=sys.stderr)
        sys.exit(1)
    import sqlite3
    conn = sqlite3.connect(vr.get_db_path())
    try:
        cur = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='vault_fts'")
        if not cur.fetchone() or conn.execute(
                "SELECT COUNT(*) FROM vault_fts").fetchone()[0] == 0:
            vr.build_index(conn)
        results = vr.search_vault(term, conn)
    finally:
        conn.close()
    if not results:
        print("(nenhuma nota relacionada; provavelmente e fato novo, sem contradicao)")
        return
    print(f"NOTAS RELACIONADAS a '{term}' (avalie contradicao antes de gravar):\n")
    for score, path, chunk in results:
        flag = "  <-- DECISAO existente" if path.startswith("DECISOES/") else ""
        snippet = re.sub(r"\s+", " ", chunk).strip()[:220]
        print(f"* {path}{flag}\n  {snippet}\n")


def cmd_template(args):
    """Imprime o path e o conteudo sugerido. O AGENTE grava via Write (nao aqui)."""
    date = _today()
    fname = f"{date}-{_slug(args.project, 24)}-{_slug(args.title)}.md"
    rel = f"DECISOES/{fname}"
    supersede_line = ""
    if args.supersede:
        supersede_line = f'supersede: "[[{Path(args.supersede).stem}]]"\n'
    fm = (
        "---\n"
        f"tipo: {args.kind}\n"
        f"projeto: {args.project}\n"
        f"status: {args.status}\n"
        f"data: {date}\n"
        f"{supersede_line}"
        "fonte: ingest_gate\n"
        "---\n\n"
        f"# {args.title}\n\n"
        "<CORPO: descreva o que vale agora. Se substitui algo, diga o que mudou.>\n"
    )
    print("PATH_ABSOLUTO:")
    print(str(VAULT / rel))
    print("\nCONTEUDO_SUGERIDO (grave via Write, troque o corpo):")
    print(fm)
    if args.supersede:
        print(f"ACAO_EXTRA: editar {args.supersede} -> status: substituido + "
              f'superseded_by: "[[{Path(fname).stem}]]" (via Edit).')


def _reindex_fts():
    try:
        subprocess.run(
            [sys.executable, str(SCRIPTS / "vault_rag.py"), "--rebuild"],
            capture_output=True, timeout=180)
        print("OK: FTS5 reindexado (nota ja buscavel localmente)")
    except Exception as e:
        print(f"AVISO: FTS5 rebuild falhou ({e})", file=sys.stderr)


def cmd_reindex(args):
    _reindex_fts()
    import urllib.request
    try:
        urllib.request.urlopen("http://127.0.0.1:9621/health", timeout=3)
        up = True
    except Exception:
        up = False
    if up:
        print("Servidor LightRAG no ar. Pra enriquecer o grafo:")
        print("  cd ~/lightrag-workspace && .venv/bin/python ingest_vault.py")
    else:
        print("Servidor LightRAG offline. O FTS5 ja cobre a busca; o grafo "
              "atualiza no proximo ingest_vault.py (server no ar).")


def main():
    p = argparse.ArgumentParser(prog="ingest_gate.py", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("related")
    s.add_argument("term")

    s = sub.add_parser("template")
    s.add_argument("--project", required=True)
    s.add_argument("--title", required=True)
    s.add_argument("--status", default="ativo", choices=VALID_STATUS)
    s.add_argument("--kind", default="decisao", choices=VALID_KIND)
    s.add_argument("--supersede", default=None)

    sub.add_parser("reindex")

    a = p.parse_args()
    if a.cmd == "related":
        cmd_related(a.term)
    elif a.cmd == "template":
        cmd_template(a)
    elif a.cmd == "reindex":
        cmd_reindex(a)


if __name__ == "__main__":
    main()
