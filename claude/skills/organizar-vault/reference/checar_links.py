#!/usr/bin/env python3
"""
checar_links.py: depois de mover notas dentro do vault, confere se algum link
interno ficou apontando pro lugar errado.

Como o Obsidian funciona: um link [[Nome]] sem barra (wikilink simples) e
resolvido pelo NOME do arquivo, nao pelo caminho. Entao mover uma nota de
pasta normalmente NAO quebra esse tipo de link, desde que o nome continue
unico no vault. Ja um link com caminho, tipo [[Pasta/Nome]] ou um link
markdown [texto](Pasta/Nome.md) ou um embed ![[Pasta/Nome.png]], aponta pro
CAMINHO, e esse sim quebra quando a nota muda de pasta.

Este script:
  1. Le uma lista de movimentos (de -> para).
  2. Varre as notas do vault procurando por referencias ao caminho antigo.
  3. Por padrao so REPORTA o que encontrou (nada e alterado).
  4. Com --fix, substitui as referencias de caminho encontradas pelo caminho
     novo, e avisa separadamente sobre wikilinks simples que citam um nome
     que mudou (esses o script nao arrisca reescrever sozinho: pede revisao
     manual, porque um wikilink simples pode ser ambiguo).

Uso:
  python3 checar_links.py "/caminho/do/vault" movimentos.json
  python3 checar_links.py "/caminho/do/vault" movimentos.json --fix

Formato do movimentos.json: lista de objetos
  [{"de": "Diario/Ideia.md", "para": "Projetos/Cliente A/Ideia.md"}, ...]
Caminhos relativos a raiz do vault, com ou sem a extensao .md (tanto faz).
"""
import argparse
import json
import os
import re
import sys

IGNORED_DIR_NAMES = {".obsidian", ".git", ".trash", ".Trash", "node_modules"}

WIKILINK_PATH_RE = re.compile(r"(\[\[)([^\]|#]+)((?:#[^\]|]*)?(?:\|[^\]]*)?)(\]\])")
MDLINK_RE = re.compile(r"(\]\()([^)]+\.(?:md|png|jpg|jpeg|gif|pdf|svg|webp))(\))")


def strip_ext(path):
    return path[:-3] if path.lower().endswith(".md") else path


def iter_notes(vault_path):
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIR_NAMES]
        for fname in files:
            if fname.lower().endswith(".md"):
                full = os.path.join(root, fname)
                yield full, os.path.relpath(full, vault_path)


def build_maps(moves):
    # caminho antigo (sem extensao, com barra normal) -> caminho novo
    path_map = {}
    # nome antigo (so basename, sem extensao) -> nome novo, so quando o NOME mudou
    rename_map = {}
    for mv in moves:
        de = strip_ext(mv["de"]).replace("\\", "/").strip("/")
        para = strip_ext(mv["para"]).replace("\\", "/").strip("/")
        path_map[de] = para
        base_de = os.path.basename(de)
        base_para = os.path.basename(para)
        if base_de.lower() != base_para.lower():
            rename_map[base_de.lower()] = base_para
    return path_map, rename_map


def resolve_candidate(raw_target, source_rel_dir, path_map):
    """Tenta casar o alvo de um link (path-based) com uma entrada do path_map,
    testando como caminho relativo a raiz do vault e como caminho relativo ao
    arquivo de origem (as duas formas sao validas em vaults Obsidian, dependendo
    da configuracao 'new link format')."""
    candidate = strip_ext(raw_target).replace("\\", "/").strip("/")
    if candidate in path_map:
        return candidate
    if source_rel_dir:
        joined = os.path.normpath(os.path.join(source_rel_dir, candidate)).replace("\\", "/")
        if joined in path_map:
            return joined
    return None


def scan(vault_path, path_map, rename_map):
    path_hits = []    # (arquivo, alvo_antigo, alvo_novo)
    rename_hits = []  # (arquivo, nome_citado_no_wikilink)

    for full, rel in iter_notes(vault_path):
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        source_dir = os.path.dirname(rel)

        for m in MDLINK_RE.finditer(text):
            raw_target = m.group(2)
            matched = resolve_candidate(raw_target, source_dir, path_map)
            if matched:
                path_hits.append((rel, raw_target, path_map[matched]))

        for m in WIKILINK_PATH_RE.finditer(text):
            raw_target = m.group(2).strip()
            if "/" in raw_target:
                matched = resolve_candidate(raw_target, source_dir, path_map)
                if matched:
                    path_hits.append((rel, raw_target, path_map[matched]))
            else:
                new_name = rename_map.get(raw_target.strip().lower())
                if new_name:
                    rename_hits.append((rel, raw_target, new_name))

    return path_hits, rename_hits


def apply_fix(vault_path, path_map):
    """Reescreve links com caminho (markdown e wikilink-com-barra) que apontam
    pro caminho antigo, trocando pelo caminho novo. Wikilinks simples (sem
    barra) NAO sao tocados aqui: ficam na lista pra revisao manual."""
    changed_files = 0
    for full, rel in iter_notes(vault_path):
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        source_dir = os.path.dirname(rel)
        original = text

        def repl_mdlink(m):
            raw_target = m.group(2)
            matched = resolve_candidate(raw_target, source_dir, path_map)
            if not matched:
                return m.group(0)
            ext = ""
            if "." in raw_target:
                ext = "." + raw_target.rsplit(".", 1)[-1]
            return m.group(1) + path_map[matched] + ext + m.group(3)

        def repl_wikilink(m):
            raw_target = m.group(2).strip()
            if "/" not in raw_target:
                return m.group(0)
            matched = resolve_candidate(raw_target, source_dir, path_map)
            if not matched:
                return m.group(0)
            return m.group(1) + path_map[matched] + m.group(3) + m.group(4)

        text = MDLINK_RE.sub(repl_mdlink, text)
        text = WIKILINK_PATH_RE.sub(repl_wikilink, text)

        if text != original:
            with open(full, "w", encoding="utf-8") as fh:
                fh.write(text)
            changed_files += 1
    return changed_files


def main():
    parser = argparse.ArgumentParser(description="Confere e opcionalmente corrige links quebrados por movimentos no vault.")
    parser.add_argument("vault_path")
    parser.add_argument("movimentos_json", help="Arquivo JSON com a lista de movimentos [{'de':..., 'para':...}]")
    parser.add_argument("--fix", action="store_true", help="Corrige automaticamente os links com caminho (nao mexe em wikilinks simples)")
    args = parser.parse_args()

    vault_path = os.path.abspath(os.path.expanduser(args.vault_path))
    if not os.path.isdir(vault_path):
        print(f"ERRO: vault nao encontrado em {vault_path}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.movimentos_json, "r", encoding="utf-8") as fh:
            moves = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERRO ao ler {args.movimentos_json}: {exc}", file=sys.stderr)
        sys.exit(1)

    path_map, rename_map = build_maps(moves)

    if args.fix:
        changed = apply_fix(vault_path, path_map)
        print(f"Links com caminho corrigidos em {changed} arquivo(s).")
        print("Rode de novo sem --fix pra conferir o que ainda sobrou (wikilinks simples com nome renomeado, se houver).")

    path_hits, rename_hits = scan(vault_path, path_map, rename_map)

    print("=" * 60)
    print("CHECAGEM DE LINKS APOS MOVIMENTACAO")
    print("=" * 60)
    print(f"Movimentos considerados: {len(moves)}")
    print("")
    print(f"Links com caminho que ainda apontam pro lugar antigo: {len(path_hits)}")
    for rel, old, new in path_hits[:50]:
        print(f"  - {rel}: referencia \"{old}\" deveria virar \"{new}\"")
    if len(path_hits) > 50:
        print(f"  ... e mais {len(path_hits) - 50}")
    print("")
    print(f"Wikilinks simples citando um nome que mudou (revisar na mao): {len(rename_hits)}")
    for rel, old, new in rename_hits[:50]:
        print(f"  - {rel}: cita \"[[{old}]]\", nome novo e \"{new}\"")
    if len(rename_hits) > 50:
        print(f"  ... e mais {len(rename_hits) - 50}")
    print("=" * 60)


if __name__ == "__main__":
    main()
