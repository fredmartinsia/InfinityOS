#!/usr/bin/env python3
"""
vault_search.py: busca FTS5 no vault Obsidian via CLI, sob demanda.

E o mesmo motor de fallback do vault_rag.py exposto como ferramenta chamavel:
custo zero no startup (nao carrega nada), o Claude roda quando precisa de um
trecho literal do vault sem depender do servidor LightRAG estar no ar.

Uso:
  vault_search.py "<consulta>" [n_resultados]
"""
import os
import sqlite3
import sys

sys.path.insert(0, os.path.expanduser("~/.claude/scripts"))
import vault_rag as vr  # noqa: E402


def main():
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print('uso: vault_search.py "<consulta>" [n]', file=sys.stderr)
        sys.exit(2)
    query = sys.argv[1]
    n = int(sys.argv[2]) if len(sys.argv) > 2 else vr.TOP_CHUNKS

    conn = sqlite3.connect(vr.get_db_path())
    try:
        # mesma regra do hook: reconstroi se o indice nao existe ou se o vault
        # mudou desde o ultimo build (vr.needs_reindex centraliza a decisao)
        if vr.needs_reindex(conn):
            vr.build_index(conn)
        results = vr.search_vault(query, conn)
    finally:
        conn.close()

    if not results:
        print("(nada encontrado no vault para essa consulta)")
        return
    for score, path, chunk in results[:n]:
        print(f"### {path}")
        print(chunk.strip()[:500])
        print()


if __name__ == "__main__":
    main()
