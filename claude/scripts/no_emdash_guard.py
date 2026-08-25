#!/usr/bin/env python3
"""
no_emdash_guard.py - Hook PreToolUse (Write|Edit|MultiEdit).

Regra dura e global do usuÃ¡rio: NUNCA usar o travessao / em dash (o caractere longo de
pontuacao) em NENHUM texto produzido para ele (copy, posts, e-mails, documentos,
codigo, mensagens). Esse caractere denuncia texto gerado por IA. Hifen comum em
palavras compostas e permitido; o travessao longo NAO.

Como isto e DETERMINISTICO, roda em codigo em vez de depender do LLM lembrar a regra:
inspeciona o conteudo que o modelo esta prestes a gravar num arquivo e, se encontrar
um traco longo (em dash U+2014, en dash U+2013, horizontal bar U+2015, two/three-em
dash), BLOQUEIA (exit 2) e instrui a reescrever com ponto, virgula, dois-pontos,
parenteses ou reformulando a frase.

Escape para casos legitimos raros (ex: citar um texto de terceiro verbatim):
exportar ALLOW_EMDASH=1 antes da operacao.

Convencao dos hooks do usuÃ¡rio: nunca derruba a sessao. Qualquer erro interno -> exit 0
(fail-open), pois um guard de estilo jamais deve travar o trabalho por bug proprio.
Somente a deteccao real de travessao usa exit 2 (fail-closed intencional).
"""
import sys, os, json, re

# tracos longos proibidos (o hifen normal U+002D NAO entra)
BANNED = {
    "—": "— (em dash)",
    "–": "– (en dash)",
    "―": "― (horizontal bar)",
    "⸺": "⸺ (two-em dash)",
    "⸻": "⸻ (three-em dash)",
}
BANNED_RE = re.compile("[" + "".join(BANNED) + "]")


def texts_from_input(tool_input):
    """Extrai todo o texto que sera efetivamente gravado, por tipo de tool."""
    out = []
    if not isinstance(tool_input, dict):
        return out
    if isinstance(tool_input.get("content"), str):          # Write
        out.append(tool_input["content"])
    if isinstance(tool_input.get("new_string"), str):       # Edit
        out.append(tool_input["new_string"])
    for e in tool_input.get("edits", []) or []:             # MultiEdit
        if isinstance(e, dict) and isinstance(e.get("new_string"), str):
            out.append(e["new_string"])
    return out


def offending_lines(text):
    hits = []
    for i, line in enumerate(text.splitlines(), 1):
        if BANNED_RE.search(line):
            chars = sorted({BANNED[c] for c in line if c in BANNED})
            snippet = line.strip()
            if len(snippet) > 120:
                snippet = snippet[:117] + "..."
            hits.append((i, ", ".join(chars), snippet))
    return hits


def main():
    if os.environ.get("ALLOW_EMDASH") == "1":
        sys.exit(0)
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)
    data = json.loads(raw)
    tool = data.get("tool_name", "")
    if tool not in ("Write", "Edit", "MultiEdit"):
        sys.exit(0)
    tool_input = data.get("tool_input", {}) or {}
    path = tool_input.get("file_path", "?")

    all_hits = []
    for txt in texts_from_input(tool_input):
        all_hits.extend(offending_lines(txt))
    if not all_hits:
        sys.exit(0)

    msg = [
        "BLOQUEADO: travessao/em dash detectado no conteudo que voce ia gravar.",
        f"Arquivo: {path}",
        "Regra global do usuÃ¡rio (sem excecao): nunca use o traco longo de pontuacao.",
        "Troque por ponto, virgula, dois-pontos, parenteses, ou reescreva a frase.",
        "Hifen comum (-) em palavras compostas continua permitido.",
        "",
        "Ocorrencias:",
    ]
    for ln, chars, snip in all_hits[:8]:
        msg.append(f"  linha {ln} [{chars}]: {snip}")
    if len(all_hits) > 8:
        msg.append(f"  ... e mais {len(all_hits) - 8} linha(s).")
    sys.stderr.write("\n".join(msg) + "\n")
    sys.exit(2)  # bloqueia a operacao e devolve a mensagem ao Claude


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        sys.exit(0)  # fail-open: guard de estilo nunca derruba a sessao
