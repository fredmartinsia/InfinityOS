#!/usr/bin/env python3
"""
RAG Hook para Claude Code — InfinityOS
Injeta contexto do Obsidian automaticamente em cada prompt.

Configuração:
  CLAUDE_VAULT_PATH — caminho do vault Obsidian (default: ~/Documents/Obsidian Vault)
  CLAUDE_RAG_MAX_TOKENS — orçamento de tokens do contexto (default: 450)
  CLAUDE_RAG_TOP_CHUNKS — número de chunks por query (default: 6)
  CLAUDE_RAG_DIARY_MAX_DAYS — cutoff de notas em Diario/ (default: 30)

Baseado no guia do @thiagozaoo.
"""

import sys
import json
import os
import sqlite3
import re
from datetime import datetime, timedelta
from pathlib import Path

VAULT_PATH = os.path.expanduser(
    os.environ.get("CLAUDE_VAULT_PATH", "~/Documents/Obsidian Vault")
)
MAX_TOKENS = int(os.environ.get("CLAUDE_RAG_MAX_TOKENS", "450"))
TOP_CHUNKS = int(os.environ.get("CLAUDE_RAG_TOP_CHUNKS", "6"))
DIARY_MAX_DAYS = int(os.environ.get("CLAUDE_RAG_DIARY_MAX_DAYS", "30"))

FOLDER_WEIGHTS = {
    "clientes": 1.4,
    "projetos": 1.3,
    "infra": 1.2,
    "diario": 1.1,
}

SKIP_PATTERNS = [
    r"^git\s",
    r"^npm\s",
    r"^deploy\s",
    r"^yarn\s",
    r"^pnpm\s",
    r"^docker\s",
    r"^kubectl\s",
]


def should_skip(prompt: str) -> bool:
    if len(prompt.strip()) < 5:
        return True
    prompt_lower = prompt.strip().lower()
    for pattern in SKIP_PATTERNS:
        if re.match(pattern, prompt_lower):
            return True
    return False


def estimate_tokens(text: str) -> int:
    return len(text) // 4


def get_folder_weight(file_path: str) -> float:
    path_lower = file_path.lower()
    for folder, weight in FOLDER_WEIGHTS.items():
        if f"/{folder}/" in path_lower or path_lower.startswith(folder + "/"):
            return weight
    return 1.0


def is_diary_too_old(file_path: str) -> bool:
    path_lower = file_path.lower()
    if "/diario/" not in path_lower and not path_lower.startswith("diario/"):
        return False
    try:
        filename = Path(file_path).stem
        date_match = re.search(r"(\d{4}-\d{2}-\d{2})", filename)
        if date_match:
            file_date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
            cutoff = datetime.now() - timedelta(days=DIARY_MAX_DAYS)
            return file_date < cutoff
    except Exception:
        pass
    try:
        full_path = os.path.join(VAULT_PATH, file_path)
        mtime = os.path.getmtime(full_path)
        file_date = datetime.fromtimestamp(mtime)
        cutoff = datetime.now() - timedelta(days=DIARY_MAX_DAYS)
        return file_date < cutoff
    except Exception:
        return False


def chunk_text(text: str, chunk_size: int = 300) -> list:
    words = text.split()
    chunks = []
    current = []
    current_len = 0
    for word in words:
        current.append(word)
        current_len += len(word) + 1
        if current_len >= chunk_size:
            chunks.append(" ".join(current))
            current = []
            current_len = 0
    if current:
        chunks.append(" ".join(current))
    return chunks


def build_index(conn: sqlite3.Connection):
    conn.execute("DROP TABLE IF EXISTS vault_fts")
    conn.execute(
        """
        CREATE VIRTUAL TABLE vault_fts USING fts5(
            file_path,
            chunk_text,
            tokenize='unicode61'
        )
    """
    )

    vault = Path(VAULT_PATH)
    if not vault.exists():
        return

    rows = []
    for md_file in vault.rglob("*.md"):
        try:
            rel_path = str(md_file.relative_to(vault))

            if is_diary_too_old(rel_path):
                continue

            content = md_file.read_text(encoding="utf-8", errors="ignore")
            content = re.sub(r"^---[\s\S]*?---\n", "", content)
            content = re.sub(r"#+ ", "", content)
            content = re.sub(r"\[\[([^\]]+)\]\]", r"\1", content)
            content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", content)
            content = content.strip()

            if not content:
                continue

            for chunk in chunk_text(content):
                rows.append((rel_path, chunk))
        except Exception:
            continue

    conn.executemany("INSERT INTO vault_fts VALUES (?, ?)", rows)
    conn.commit()


STOPWORDS_PT = {
    "a", "o", "as", "os", "um", "uma", "uns", "umas",
    "de", "da", "do", "das", "dos", "em", "no", "na", "nos", "nas",
    "por", "para", "pra", "pelo", "pela", "pelos", "pelas",
    "com", "sem", "sob", "sobre", "entre", "ate", "ate",
    "e", "ou", "mas", "se", "que", "quem", "qual", "quais",
    "como", "onde", "quando", "porque", "pois",
    "eu", "tu", "ele", "ela", "nos", "vos", "eles", "elas",
    "me", "te", "lhe", "lhes",
    "meu", "minha", "teu", "tua", "seu", "sua",
    "este", "esta", "estes", "estas", "esse", "essa", "esses", "essas",
    "aquele", "aquela", "isto", "isso", "aquilo",
    "ta", "to", "tao", "tambem", "ja", "nao", "sim",
    "ser", "estar", "ter", "foi", "sera", "era", "esta", "estao",
    "do", "da", "fez", "faz", "faca", "fazer",
    "aqui", "ali", "la", "hoje", "ontem", "amanha",
    "agora", "depois", "antes", "entao", "logo",
    "muito", "mais", "menos", "bem", "mal",
    "the", "of", "and", "to", "for", "in", "on", "at", "is", "are",
}


def search_vault(query: str, conn: sqlite3.Connection) -> list:
    clean = re.sub(r'[^\w\s]', ' ', query.lower())
    words = [w for w in clean.split() if w not in STOPWORDS_PT and len(w) >= 3]
    words = words[:10]

    if not words:
        return []

    escaped = [f'"{w}"' for w in words]
    fts_query = " OR ".join(escaped)

    try:
        cursor = conn.execute(
            """
            SELECT file_path, chunk_text, rank
            FROM vault_fts
            WHERE vault_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """,
            (fts_query, TOP_CHUNKS * 3),
        )
        results = cursor.fetchall()
    except sqlite3.OperationalError:
        return []

    scored = []
    for file_path, chunk, rank in results:
        if is_diary_too_old(file_path):
            continue
        weight = get_folder_weight(file_path)
        score = abs(rank) * weight
        scored.append((score, file_path, chunk))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:TOP_CHUNKS]


def build_context(results: list) -> str:
    if not results:
        return ""

    parts = ["[CONTEXTO DO VAULT OBSIDIAN]"]
    total_tokens = 0

    for score, file_path, chunk in results:
        header = f"\n### {file_path}\n"
        content = chunk.strip()
        entry = header + content

        entry_tokens = estimate_tokens(entry)
        if total_tokens + entry_tokens > MAX_TOKENS:
            remaining = MAX_TOKENS - total_tokens
            if remaining > 50:
                words = content.split()
                truncated = []
                count = 0
                for word in words:
                    count += len(word) // 4 + 1
                    if count > remaining:
                        break
                    truncated.append(word)
                parts.append(header + " ".join(truncated) + "...")
            break

        parts.append(entry)
        total_tokens += entry_tokens

    parts.append("\n[FIM DO CONTEXTO]")
    return "\n".join(parts)


def get_db_path() -> str:
    cache_dir = os.environ.get("CLAUDE_RAG_CACHE_DIR")
    if not cache_dir:
        home = os.path.expanduser(os.environ.get("CLAUDE_HOME", "~/.claude"))
        cache_dir = os.path.join(home, "cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, "vault_rag.db")


def get_vault_mtime() -> float:
    vault = Path(VAULT_PATH)
    if not vault.exists():
        return 0.0
    latest = 0.0
    for md_file in vault.rglob("*.md"):
        try:
            mtime = md_file.stat().st_mtime
            if mtime > latest:
                latest = mtime
        except Exception:
            pass
    return latest


def dry_run():
    print(f"[infinity-os vault_rag] VAULT_PATH = {VAULT_PATH}")
    if not Path(VAULT_PATH).exists():
        print("  [WARN] Vault não existe. Configure CLAUDE_VAULT_PATH.")
        return 1
    md_count = sum(1 for _ in Path(VAULT_PATH).rglob("*.md"))
    print(f"  Vault OK, {md_count} notas .md encontradas.")
    print(f"  MAX_TOKENS={MAX_TOKENS}, TOP_CHUNKS={TOP_CHUNKS}, DIARY_MAX_DAYS={DIARY_MAX_DAYS}")
    return 0


def reindex():
    """Constrói o índice FTS agora (usado pelo instalador, p/ RAG pronto na 1ª sessão)."""
    print(f"[infinity-os vault_rag] Reindexando: {VAULT_PATH}")
    if not Path(VAULT_PATH).exists():
        print("  [WARN] Vault não existe. Configure CLAUDE_VAULT_PATH.")
        return 1
    conn = sqlite3.connect(get_db_path())
    try:
        build_index(conn)
        try:
            n = conn.execute("SELECT COUNT(*) FROM vault_fts").fetchone()[0]
            print(f"  Índice construído: {n} chunks.")
        except Exception:
            print("  Índice construído.")
    finally:
        conn.close()
    return 0


def main():
    if "--dry-run" in sys.argv:
        sys.exit(dry_run())
    if "--reindex" in sys.argv:
        sys.exit(reindex())

    raw = ""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except Exception:
        sys.stdout.write(raw)
        return

    prompt = ""
    if isinstance(data.get("prompt"), str):
        prompt = data["prompt"]
    elif isinstance(data.get("messages"), list):
        for msg in reversed(data["messages"]):
            if msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str):
                    prompt = content
                elif isinstance(content, list):
                    for block in content:
                        if block.get("type") == "text":
                            prompt = block.get("text", "")
                            break
                break

    if should_skip(prompt):
        sys.stdout.write(json.dumps(data))
        return

    vault_path = Path(VAULT_PATH)
    if not vault_path.exists():
        sys.stdout.write(json.dumps(data))
        return

    db_path = get_db_path()
    conn = sqlite3.connect(db_path)

    try:
        needs_rebuild = True
        try:
            cursor = conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='vault_fts'"
            )
            if cursor.fetchone():
                cursor = conn.execute("SELECT COUNT(*) FROM vault_fts")
                count = cursor.fetchone()[0]
                if count > 0:
                    needs_rebuild = False
        except Exception:
            pass

        if needs_rebuild:
            build_index(conn)

        results = search_vault(prompt, conn)
        context = build_context(results)

        if context:
            existing_system = data.get("system_prompt", "")
            if existing_system:
                data["system_prompt"] = context + "\n\n" + existing_system
            else:
                data["system_prompt"] = context

    finally:
        conn.close()

    sys.stdout.write(json.dumps(data))


if __name__ == "__main__":
    main()
