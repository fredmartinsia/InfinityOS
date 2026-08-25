#!/usr/bin/env python3
"""
diagnostico.py: varredura de leitura do vault Obsidian para a skill organizar-vault.

NAO MODIFICA NADA. So le arquivos e pastas e imprime um retrato em texto.
Existe pra a FASE 1 (diagnostico automatico) da skill nao precisar carregar o
vault inteiro no contexto do Claude: o script varre tudo localmente (barato,
determinístico) e devolve so o resumo que interessa.

Uso:
  python3 diagnostico.py "/caminho/do/vault"
  python3 diagnostico.py "/caminho/do/vault" --json     # saida em JSON, pra uso programatico

O que ele calcula:
  - contagem de notas (.md), pastas de primeiro nivel, profundidade maxima
  - arquivos soltos na raiz do vault
  - pastas fragmentadas (poucas notas dentro)
  - notas orfas (sem nenhum link de entrada nem de saida)
  - duplicatas provaveis (mesmo nome; ou nome com sufixo " 2" / "(1)", tipico
    de conflito de sincronizacao)
  - pastas de primeiro nivel com nome parecido, que provavelmente deveriam
    virar uma unica pasta
  - separa o que e estrutura do InfinityOS (CLONES, SQUADS, DECISOES, etc.)
    do que e conteudo proprio da pessoa
"""
import argparse
import json
import os
import re
import sys
import unicodedata
from collections import defaultdict

# Pastas que sao estrutura do InfinityOS, nao conteudo da pessoa.
# Comparacao e case-sensitive porque e assim que o instalador cria essas pastas.
STRUCTURAL_TOP_FOLDERS = {
    "CLONES",
    "SQUADS",
    "DECISOES",
    "_META",
    "_memory",
    "_opensquad",
    "Templates",
    "_revisar-duplicatas",  # pasta de quarentena que a propria skill usa
}

# Pastas de sistema/sync que nunca entram na varredura.
IGNORED_DIR_NAMES = {
    ".obsidian",
    ".git",
    ".trash",
    ".Trash",
    "node_modules",
    ".DS_Store",
}

# Nomes de arquivo genericos demais pra virarem "duplicata provavel" so por
# terem o mesmo nome em pastas diferentes (isso e normal em qualquer vault).
GENERIC_BASENAMES = {
    "index", "readme", "moc", "dashboard", "overview", "template",
    "readme.md".replace(".md", ""), "untitled", "novo arquivo", "new note",
}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)")          # [[nota]], [[nota|alias]], [[nota#bloco]]
MDLINK_RE = re.compile(r"\]\(([^)]+\.md)\)")          # [texto](caminho/nota.md)
SYNC_CONFLICT_RE = re.compile(r"^(?P<base>.+?)\s(?:\d+|\(\d+\))$")  # "Nota 2", "Nota (1)"


def strip_accents(text):
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))


def normalize_name(name):
    """Reduz um nome de pasta/arquivo ao essencial pra comparar por semelhanca:
    sem acento, sem emoji/pontuacao, minusculo, sem espacos duplicados."""
    name = strip_accents(name).lower()
    name = re.sub(r"[^a-z0-9]+", " ", name)
    return name.strip()


def levenshtein(a, b):
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + cost)
        prev = cur
    return prev[-1]


def iter_vault_dirs(vault_path):
    """os.walk que poda pastas de sistema/estrutura sem descer nelas."""
    for root, dirs, files in os.walk(vault_path):
        dirs[:] = sorted(d for d in dirs if d not in IGNORED_DIR_NAMES)
        yield root, dirs, files


def relpath(vault_path, full_path):
    return os.path.relpath(full_path, vault_path)


def is_structural_relpath(rel):
    top = rel.split(os.sep, 1)[0]
    return top in STRUCTURAL_TOP_FOLDERS


def scan(vault_path):
    vault_path = os.path.abspath(os.path.expanduser(vault_path))
    if not os.path.isdir(vault_path):
        print(f"ERRO: caminho nao existe ou nao e uma pasta: {vault_path}", file=sys.stderr)
        sys.exit(1)

    has_obsidian = os.path.isdir(os.path.join(vault_path, ".obsidian"))

    all_notes = []          # relpaths de arquivos .md
    all_other_files = []    # relpaths de arquivos que nao sao .md
    max_depth = 0
    folder_note_count = defaultdict(int)   # relpath da pasta -> notas diretas nela
    all_folders = set()

    for root, dirs, files in iter_vault_dirs(vault_path):
        rel_root = relpath(vault_path, root)
        if rel_root != ".":
            all_folders.add(rel_root)
            depth = rel_root.count(os.sep) + 1
            max_depth = max(max_depth, depth)
        for fname in files:
            if fname == ".DS_Store":
                continue
            full = os.path.join(root, fname)
            rel = relpath(vault_path, full)
            depth = rel.count(os.sep) + 1
            max_depth = max(max_depth, depth)
            if fname.lower().endswith(".md"):
                all_notes.append(rel)
                parent = rel_root if rel_root != "." else ""
                folder_note_count[parent] += 1
            else:
                all_other_files.append(rel)

    # arquivos soltos direto na raiz (fora de qualquer pasta)
    root_loose_files = [f for f in (all_notes + all_other_files) if os.sep not in f]

    # pastas de primeiro nivel (so as que estao logo abaixo da raiz)
    top_level_folders = sorted(
        {f.split(os.sep, 1)[0] for f in all_folders} |
        {d for d in os.listdir(vault_path)
         if os.path.isdir(os.path.join(vault_path, d)) and d not in IGNORED_DIR_NAMES}
    )
    structural_top = sorted(f for f in top_level_folders if f in STRUCTURAL_TOP_FOLDERS)
    personal_top = sorted(f for f in top_level_folders if f not in STRUCTURAL_TOP_FOLDERS)

    # pastas fragmentadas: poucas notas DIRETAS dentro (nao conta subpasta),
    # ignorando estrutura do InfinityOS.
    empty_folders = []
    thin_folders = []  # 1 ou 2 notas
    for folder, count in sorted(folder_note_count.items()):
        if not folder or is_structural_relpath(folder):
            continue
        if count == 0:
            empty_folders.append(folder)
        elif count in (1, 2):
            thin_folders.append((folder, count))
    # pastas sem NENHUM arquivo .md e tambem sem entrada no dict (pasta so com subpastas)
    for folder in sorted(all_folders):
        if folder in folder_note_count or is_structural_relpath(folder):
            continue
        empty_folders.append(folder)
    empty_folders = sorted(set(empty_folders))

    # ---- duplicatas provaveis ----
    basename_map = defaultdict(list)  # nome sem extensao (lowercase) -> [relpaths]
    for rel in all_notes:
        stem = os.path.splitext(os.path.basename(rel))[0]
        basename_map[stem.lower()].append(rel)

    exact_name_dupes = {}
    sync_conflict_dupes = defaultdict(list)
    for stem_lower, paths in basename_map.items():
        m = SYNC_CONFLICT_RE.match(stem_lower)
        if m:
            base_key = m.group("base").strip()
            sync_conflict_dupes[base_key].extend(paths)
        if len(paths) > 1 and stem_lower not in GENERIC_BASENAMES:
            exact_name_dupes[stem_lower] = sorted(paths)
    # junta a nota "base" (sem sufixo) na lista de conflito de sync, se existir
    for base_key, paths in list(sync_conflict_dupes.items()):
        if base_key in basename_map:
            sync_conflict_dupes[base_key] = sorted(set(sync_conflict_dupes[base_key] + basename_map[base_key]))
        else:
            sync_conflict_dupes[base_key] = sorted(set(sync_conflict_dupes[base_key]))
    sync_conflict_dupes = {k: v for k, v in sync_conflict_dupes.items() if len(v) > 1}

    # ---- pastas de primeiro nivel com nome parecido ----
    similar_groups = []
    seen_pairs = set()
    norm_top = [(f, normalize_name(f)) for f in personal_top]
    for i in range(len(norm_top)):
        for j in range(i + 1, len(norm_top)):
            name_a, norm_a = norm_top[i]
            name_b, norm_b = norm_top[j]
            if not norm_a or not norm_b:
                continue
            key = tuple(sorted((name_a, name_b)))
            if key in seen_pairs:
                continue
            is_similar = False
            if norm_a == norm_b:
                is_similar = True
            elif norm_a in norm_b or norm_b in norm_a:
                is_similar = True
            elif levenshtein(norm_a, norm_b) <= 2 and min(len(norm_a), len(norm_b)) >= 4:
                is_similar = True
            if is_similar:
                seen_pairs.add(key)
                similar_groups.append(key)

    # ---- notas orfas (sem link de entrada nem de saida) ----
    # so olha conteudo proprio da pessoa: ignora estrutura do InfinityOS e Templates
    personal_notes = [n for n in all_notes if not is_structural_relpath(n)]
    stem_to_paths = defaultdict(list)
    for n in personal_notes:
        stem = os.path.splitext(os.path.basename(n))[0].lower()
        stem_to_paths[stem].append(n)

    out_links = defaultdict(set)   # nota -> {notas apontadas}
    in_links = defaultdict(set)    # nota -> {notas que apontam pra ela}
    for n in personal_notes:
        full = os.path.join(vault_path, n)
        try:
            with open(full, "r", encoding="utf-8", errors="ignore") as fh:
                text = fh.read()
        except OSError:
            continue
        targets = set()
        for m in WIKILINK_RE.finditer(text):
            targets.add(m.group(1).strip())
        for m in MDLINK_RE.finditer(text):
            targets.add(os.path.splitext(os.path.basename(m.group(1)))[0])
        for t in targets:
            t_stem = t.strip().lower()
            candidates = stem_to_paths.get(t_stem, [])
            for c in candidates:
                if c != n:
                    out_links[n].add(c)
                    in_links[c].add(n)

    orphan_notes = sorted(
        n for n in personal_notes
        if not out_links.get(n) and not in_links.get(n)
    )

    return {
        "vault_path": vault_path,
        "has_obsidian_folder": has_obsidian,
        "total_notes": len(all_notes),
        "total_other_files": len(all_other_files),
        "top_level_folders_count": len(top_level_folders),
        "structural_top_folders": structural_top,
        "personal_top_folders": personal_top,
        "max_depth": max_depth,
        "root_loose_files": sorted(root_loose_files),
        "empty_folders": empty_folders,
        "thin_folders": sorted(thin_folders),
        "exact_name_dupes": exact_name_dupes,
        "sync_conflict_dupes": sync_conflict_dupes,
        "similar_top_folder_pairs": sorted(similar_groups),
        "orphan_notes": orphan_notes,
        "orphan_notes_count": len(orphan_notes),
    }


def print_human(report):
    p = print
    p("=" * 60)
    p("DIAGNOSTICO DO VAULT (leitura apenas, nada foi alterado)")
    p("=" * 60)
    p(f"Caminho: {report['vault_path']}")
    if not report["has_obsidian_folder"]:
        p("AVISO: nao encontrei a pasta .obsidian aqui dentro. Confirme se")
        p("este e mesmo o caminho do vault antes de continuar.")
    p("")
    p("-- Numeros gerais --")
    p(f"Notas (.md): {report['total_notes']}")
    p(f"Outros arquivos (imagens, pdf, etc.): {report['total_other_files']}")
    p(f"Pastas de primeiro nivel: {report['top_level_folders_count']}")
    p(f"Profundidade maxima de pastas: {report['max_depth']}")
    p(f"Arquivos soltos direto na raiz do vault: {len(report['root_loose_files'])}")
    if report["root_loose_files"]:
        for f in report["root_loose_files"][:20]:
            p(f"  - {f}")
        if len(report["root_loose_files"]) > 20:
            p(f"  ... e mais {len(report['root_loose_files']) - 20}")
    p("")
    p("-- Estrutura do InfinityOS (nao mexer sem necessidade) --")
    p(f"Pastas de sistema encontradas: {', '.join(report['structural_top_folders']) or '(nenhuma)'}")
    p("")
    p("-- Conteudo proprio da pessoa (pastas de primeiro nivel) --")
    p(", ".join(report["personal_top_folders"]) or "(nenhuma)")
    p("")
    p("-- Fragmentacao --")
    p(f"Pastas vazias (0 notas direto dentro): {len(report['empty_folders'])}")
    for f in report["empty_folders"][:20]:
        p(f"  - {f}")
    if len(report["empty_folders"]) > 20:
        p(f"  ... e mais {len(report['empty_folders']) - 20}")
    p(f"Pastas quase vazias (1 ou 2 notas, sinal de fragmentacao): {len(report['thin_folders'])}")
    for f, c in report["thin_folders"][:20]:
        p(f"  - {f} ({c} nota{'s' if c != 1 else ''})")
    if len(report["thin_folders"]) > 20:
        p(f"  ... e mais {len(report['thin_folders']) - 20}")
    p("")
    p("-- Notas orfas (sem nenhum link de entrada ou de saida) --")
    p(f"Total: {report['orphan_notes_count']}")
    for n in report["orphan_notes"][:20]:
        p(f"  - {n}")
    if report["orphan_notes_count"] > 20:
        p(f"  ... e mais {report['orphan_notes_count'] - 20}")
    p("")
    p("-- Duplicatas provaveis por conflito de sincronizacao (sufixo \" 2\", \"(1)\") --")
    if report["sync_conflict_dupes"]:
        for base, paths in sorted(report["sync_conflict_dupes"].items()):
            p(f"  grupo \"{base}\":")
            for pth in paths:
                p(f"    - {pth}")
    else:
        p("  (nenhuma encontrada)")
    p("")
    p("-- Duplicatas provaveis por mesmo nome em pastas diferentes --")
    if report["exact_name_dupes"]:
        for stem, paths in sorted(report["exact_name_dupes"].items()):
            p(f"  \"{stem}\":")
            for pth in paths:
                p(f"    - {pth}")
    else:
        p("  (nenhuma encontrada)")
    p("")
    p("-- Pastas de primeiro nivel com nome parecido (candidatas a virar uma so) --")
    if report["similar_top_folder_pairs"]:
        for a, b in report["similar_top_folder_pairs"]:
            p(f"  \"{a}\"  <->  \"{b}\"")
    else:
        p("  (nenhuma encontrada)")
    p("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Diagnostico de leitura do vault Obsidian (nao modifica nada).")
    parser.add_argument("vault_path", help="Caminho absoluto do vault Obsidian")
    parser.add_argument("--json", action="store_true", help="Imprime o relatorio em JSON em vez de texto")
    args = parser.parse_args()

    report = scan(args.vault_path)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_human(report)


if __name__ == "__main__":
    main()
