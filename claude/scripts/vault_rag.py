#!/usr/bin/env python3
"""
RAG Hook para Claude Code
Injeta contexto do Obsidian automaticamente em cada prompt.
Baseado no guia do @thiagozaoo
"""

import sys
import json
import os
import sqlite3
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

VAULT_PATH = os.environ.get("INFINITY_VAULT_PATH") or os.path.expanduser("~/Documents/Obsidian Vault")
MAX_TOKENS = 450
TOP_CHUNKS = 6
DIARY_MAX_DAYS = 30

# Modo de entrega do RAG (Tarefa H do handoff):
#   push (default): injeta ate ~800 tokens de contexto em CADA prompt (atual).
#   pull: NAO injeta conteudo; quando o prompt e do negocio, injeta 1 linha (~25t)
#         lembrando o Claude de consultar mcp__lightrag__consultar_negocio /
#         rodar vault_search.py. Economia grande; ativar via  export RAG_MODE=pull
# Fica opt-in por env pra validar (10 perguntas) antes de virar padrao, sem risco.
RAG_MODE = os.environ.get("RAG_MODE", "push").strip().lower()

# Termos que indicam pergunta do negocio (gatilho do nudge no modo pull).
BUSINESS_TERMS = re.compile(
    r"sorteio|campanha|cliente|tr[aá]fego|oferta|criativo|nobres|vv\s*group|"
    r"clube\s*infinity|projeto|an[uú]ncio|lan[cç]amento|copy|funil|venda|lead|"
    r"decis[aã]o|planejamento|mudou|estrat[eé]gia",
    re.IGNORECASE,
)

PULL_NUDGE = (
    "## Memoria do negocio (modo pull)\n"
    "Este prompt parece ser sobre o negocio do usuário. Antes de responder, consulte "
    "a memoria: use a ferramenta mcp__lightrag__consultar_negocio (grafo+vetor do "
    "vault) e/ou rode `python3 ~/.claude/scripts/vault_search.py \"<consulta>\"`. "
    "Para o que vale HOJE (planejamento atual), priorize notas em DECISOES/ com "
    "status: ativo e ignore as status: substituido. Cite a nota-fonte."
)

FOLDER_WEIGHTS = {
    "clientes": 1.4,
    "projetos": 1.3,
    "🧠 segundo cerebro": 1.3,  # hub de contexto destilado (perfil do usuário, temas)
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


# ---------------------------------------------------------------------------
# LightRAG (grafo+vetor) — fonte primaria. Servidor local em :9621, modo
# only_need_context (so recupera, nao gera com LLM = gratis e rapido). Passamos
# keywords derivadas do prompt pra PULAR a extracao de keywords via LLM (que
# custaria ~3s); assim a query fica em ~0.6s. Fallback pro FTS5 se o server cair.
# ---------------------------------------------------------------------------
LIGHTRAG_URL = "http://127.0.0.1:9621/query"
LIGHTRAG_TIMEOUT = 10  # segundos; se estourar, cai no fallback FTS5 (margem p/ 1a query do dia)
LIGHTRAG_MAX_CHARS = 3200  # ~800 tokens de contexto injetado

_STOPWORDS = set("""
a o e de da do das dos em no na nos nas um uma uns umas para por com sem que se
ao aos as os à às pra pro como mais mas ou the of to and in on for with is are
me te lhe meu minha seu sua qual quais quando onde quem porque entao ja ainda
isso isto esse essa este esta aquele aquela voce vc fred quero preciso fazer
""".split())


def derive_keywords(prompt: str):
    """Keywords sem LLM: palavras significativas + termos Capitalizados (entidades)."""
    words = re.findall(r"[A-Za-zÀ-ÿ0-9][A-Za-zÀ-ÿ0-9_\.\-]{2,}", prompt)
    seen, kw, caps = set(), [], []
    for w in words:
        lw = w.lower()
        if lw in _STOPWORDS or lw in seen:
            continue
        seen.add(lw)
        kw.append(w)
        if w[0].isupper():
            caps.append(w)
    kw = kw[:10]
    # hl = temas (gerais); ll = entidades (Capitalizadas, mais especificas)
    return kw, (caps[:8] or kw)


def lightrag_context(prompt: str):
    """Consulta o servidor LightRAG (vault_main) por contexto. Retorna str ou None."""
    import urllib.request

    hl, ll = derive_keywords(prompt)
    if not hl:
        return None
    payload = json.dumps({
        "query": prompt[:1000],
        "mode": "mix",
        "only_need_context": True,
        "top_k": 6,
        "chunk_top_k": 3,
        "max_total_tokens": 800,
        "max_entity_tokens": 400,
        "max_relation_tokens": 300,
        "hl_keywords": hl,
        "ll_keywords": ll,
        "enable_rerank": False,
    }).encode("utf-8")
    try:
        req = urllib.request.Request(
            LIGHTRAG_URL, data=payload,
            headers={"content-type": "application/json"}, method="POST",
        )
        with urllib.request.urlopen(req, timeout=LIGHTRAG_TIMEOUT) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        ctx = (body.get("response") or "").strip()
    except Exception:
        return None
    # ignora respostas vazias (so os cabecalhos de JSON sem dados)
    if (not ctx or len(ctx) < 120
            or '"entity"' not in ctx
            or "chunk" not in ctx.lower()):
        return None
    if len(ctx) > LIGHTRAG_MAX_CHARS:
        ctx = ctx[:LIGHTRAG_MAX_CHARS] + "\n... (contexto truncado)"
    return (
        "## Contexto do vault (LightRAG: grafo+vetor)\n"
        "Entidades, relacoes e trechos relevantes do segundo cerebro do usuário:\n\n"
        + ctx
    )


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

            # CLONES/ fica de fora do indice: o clone consome o vault, mas nao deve
            # ser injetado como contexto (evita o clone se auto-citar / eco).
            if rel_path.startswith("CLONES/") or rel_path.startswith("CLONES\\"):
                continue

            if is_diary_too_old(rel_path):
                continue

            content = md_file.read_text(encoding="utf-8", errors="ignore")
            # Gravacoes tem transcricao gigante: nao indexar o bloco de transcricao
            # (poluiria os prompts). Indexa so resumo/decisoes/insights/mind map.
            if "/Gravacoes/" in rel_path or rel_path.startswith("Gravacoes/"):
                content = re.split(r"(?mi)^##+\s+Transcri[cç][aã]o\s+Completa", content)[0]
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
    _stamp_build(conn)
    conn.commit()


def _stamp_build(conn: sqlite3.Connection):
    """Grava quando o indice foi construido. E a marca que permite detectar
    depois que o vault andou para a frente e o indice ficou para tras."""
    conn.execute(
        "CREATE TABLE IF NOT EXISTS vault_meta (key TEXT PRIMARY KEY, value REAL)"
    )
    conn.execute(
        "INSERT OR REPLACE INTO vault_meta VALUES ('last_build', ?)", (time.time(),)
    )


def _last_build(conn: sqlite3.Connection) -> float:
    try:
        row = conn.execute(
            "SELECT value FROM vault_meta WHERE key = 'last_build'"
        ).fetchone()
        return float(row[0]) if row else 0.0
    except Exception:
        return 0.0


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
    "amigao", "irmao", "beleza", "fechou", "pegou", "visao", "sacou",
    "the", "of", "and", "to", "for", "in", "on", "at", "is", "are",
}


def search_vault(query: str, conn: sqlite3.Connection) -> list:
    # Remove pontuacao e normaliza
    clean = re.sub(r'[^\w\s]', ' ', query.lower())
    # Filtra stopwords e palavras muito curtas
    words = [w for w in clean.split() if w not in STOPWORDS_PT and len(w) >= 3]
    # Limita a 10 palavras chave
    words = words[:10]

    if not words:
        return []

    # Monta query FTS5 com OR pra ser mais permissivo
    # Escapa palavras com aspas duplas pra evitar interpretacao de sintaxe FTS
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
    cache_dir = os.path.expanduser("~/.claude/cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, "vault_rag.db")


def get_vault_mtime() -> float:
    vault = Path(VAULT_PATH)
    if not vault.exists():
        return 0.0
    latest = 0.0
    for md_file in vault.rglob("*.md"):
        try:
            rel = str(md_file.relative_to(vault))
            if rel.startswith("CLONES/") or rel.startswith("CLONES\\"):
                continue
            mtime = md_file.stat().st_mtime
            if mtime > latest:
                latest = mtime
        except Exception:
            pass
    return latest


COMPARE_LOG = os.path.expanduser("~/.claude/cache/rag_compare.log")

# Piso entre duas reconstrucoes. Sem ele, editar o vault durante a conversa
# dispararia rebuild a cada prompt. Com ele, o custo fica limitado.
REBUILD_MIN_INTERVAL = 300  # segundos


def needs_reindex(conn: sqlite3.Connection) -> bool:
    """Decide se o indice precisa ser reconstruido.

    Reconstroi quando a tabela esta ausente ou vazia (indice nao existe), e
    tambem quando o vault andou para a frente desde o ultimo build. Sem a
    segunda condicao o indice congela no primeiro build e passa a responder
    com dado velho sem nenhum sinal de erro.
    """
    try:
        cursor = conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='vault_fts'"
        )
        if not cursor.fetchone():
            return True
        if conn.execute("SELECT COUNT(*) FROM vault_fts").fetchone()[0] == 0:
            return True
    except Exception:
        return True

    built = _last_build(conn)
    if built <= 0:
        # indice antigo, de antes desta marca existir: reconstroi uma vez
        return True
    if time.time() - built < REBUILD_MIN_INTERVAL:
        return False
    try:
        return get_vault_mtime() > built
    except Exception:
        return False


def fts5_context(prompt: str):
    """Contexto via indice FTS5 local (fallback e modo compare). Reconstroi o
    indice quando ele nao existe ou quando o vault mudou. Retorna (str, n)."""
    try:
        conn = sqlite3.connect(get_db_path())
        try:
            if needs_reindex(conn):
                build_index(conn)
            results = search_vault(prompt, conn)
            return build_context(results), len(results)
        finally:
            conn.close()
    except Exception:
        return "", 0


def log_compare(prompt: str, lr_ctx, fts_ctx, fts_n: int):
    """Modo sombra (RAG_COMPARE=1): registra LightRAG vs FTS5 por prompt, pra
    decidir a migracao da leitura com dados em vez de no feeling. So observa."""
    try:
        lr_chars = len(lr_ctx) if lr_ctx else 0
        lr_ents = lr_ctx.count('"entity"') if lr_ctx else 0
        fts_chars = len(fts_ctx) if fts_ctx else 0
        if lr_chars and (fts_chars == 0 or lr_ents >= 3 or lr_chars >= fts_chars):
            winner = "LR"
        elif fts_chars:
            winner = "FTS5"
        else:
            winner = "none"
        q = re.sub(r"\s+", " ", prompt.strip())[:80]
        line = (f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] "
                f"q=\"{q}\" | LR:{lr_chars}c/{lr_ents}ent | "
                f"FTS5:{fts_n}res/{fts_chars}c | winner={winner}\n")
        with open(COMPARE_LOG, "a") as f:
            f.write(line)
    except Exception:
        pass


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except Exception:
        sys.stdout.write(raw if 'raw' in dir() else "")
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

    # Modo pull (opt-in via RAG_MODE=pull): nao injeta conteudo. Se o prompt for
    # do negocio, injeta so um nudge de 1 linha; o Claude puxa via MCP lightrag
    # (consultar_negocio) ou vault_search.py, formulando a query com a conversa
    # inteira. Retorna cedo pra nao rodar o push. Push segue intacto no default.
    if RAG_MODE == "pull":
        if BUSINESS_TERMS.search(prompt):
            existing_system = data.get("system_prompt", "")
            data["system_prompt"] = (
                PULL_NUDGE + "\n\n" + existing_system if existing_system else PULL_NUDGE)
        sys.stdout.write(json.dumps(data))
        return

    # 1) Fonte primaria: LightRAG (grafo+vetor) via servidor local em :9621.
    context = lightrag_context(prompt)

    # Modo sombra (RAG_COMPARE=1): roda tambem o FTS5 e loga a comparacao, mas
    # mantem o LightRAG como contexto real injetado. Custo: 1 query FTS5 local.
    fts_ctx = None
    if os.environ.get("RAG_COMPARE") == "1":
        fts_ctx, fts_n = fts5_context(prompt)
        log_compare(prompt, context, fts_ctx, fts_n)

    # 2) Fallback: indice FTS5 local (se o servidor LightRAG estiver fora/vazio).
    if not context:
        if fts_ctx is None:
            fts_ctx, _ = fts5_context(prompt)
        context = fts_ctx or None

    if context:
        existing_system = data.get("system_prompt", "")
        if existing_system:
            data["system_prompt"] = context + "\n\n" + existing_system
        else:
            data["system_prompt"] = context

    sys.stdout.write(json.dumps(data))


if __name__ == "__main__":
    # Reconstrucao manual do indice FTS5 (fora do fluxo de hook):
    #   python3 vault_rag.py --rebuild
    if "--rebuild" in sys.argv:
        _conn = sqlite3.connect(get_db_path())
        try:
            build_index(_conn)
            n = _conn.execute("SELECT COUNT(*) FROM vault_fts").fetchone()[0]
            files = _conn.execute(
                "SELECT COUNT(DISTINCT file_path) FROM vault_fts"
            ).fetchone()[0]
            print(f"FTS5 reconstruido: {n} chunks de {files} arquivos.")
        finally:
            _conn.close()
        sys.exit(0)
    main()
