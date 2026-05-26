#!/usr/bin/env python3
"""
vault_guard.py — Hook PreToolUse que protege o Obsidian Vault contra
deleção/movimentação destrutiva acidental.

Regra: qualquer comando Bash que APAGUE ou MOVA-PRA-FORA arquivos/pastas
dentro de ~/Documents/Obsidian Vault/ é BLOQUEADO, a menos que o comando
inclua VAULT_GUARD_CODE=<codigo> e esse código bata com o hash salvo em
~/.claude/vault_guard.sha256.

O código real nunca é armazenado — só o hash SHA-256. Quem sabe o código
é o usuário. Isso força uma confirmação humana antes de qualquer destruição.

Setup do código: python3 ~/.claude/scripts/vault_guard_setup.py

Exit codes:
  0 — libera a operação
  2 — bloqueia a operação (mensagem vai pro stderr e volta pro Claude)
"""
import sys
import os
import re
import json
import time
import hashlib

VAULT = os.path.expanduser(
    os.environ.get("CLAUDE_VAULT_PATH", "~/Documents/Obsidian Vault")
)
HASH_FILE = os.path.expanduser("~/.claude/vault_guard.sha256")
UNLOCK_FILE = os.path.expanduser("~/.claude/vault_unlock.json")

# Padrões de comandos destrutivos
DESTRUCTIVE = [
    r"\brm\b",
    r"\brmdir\b",
    r"\bunlink\b",
    r"\btrash\b",
    r"-delete\b",          # find ... -delete
    r"-exec\s+rm\b",       # find ... -exec rm
    r"\bshred\b",
    r">\s*['\"]?[^|]*Obsidian Vault",  # truncar arquivo do vault via redirect
]

# Move-pra-fora: mv com origem no vault e destino fora — detectado à parte


def read_input():
    try:
        return json.load(sys.stdin)
    except Exception:
        return {}


def expand(token: str) -> str:
    """Expande ~ e variáveis simples para comparar paths."""
    token = token.strip().strip("'\"")
    token = token.replace("$HOME", os.path.expanduser("~"))
    token = os.path.expanduser(token)
    return token


def touches_vault(command: str) -> bool:
    """True se o comando referencia algum path dentro do vault."""
    if "Obsidian Vault" in command:
        return True
    # caminhos absolutos expandidos
    expanded = command.replace("$HOME", os.path.expanduser("~"))
    if VAULT in expanded:
        return True
    return False


def is_destructive(command: str) -> bool:
    for pat in DESTRUCTIVE:
        if re.search(pat, command):
            return True
    # mv com origem no vault e destino fora do vault (ou pra .Trash)
    if re.search(r"\bmv\b", command):
        if "Obsidian Vault" in command or VAULT in command.replace("$HOME", os.path.expanduser("~")):
            # se menciona Trash/lixeira como destino, é destrutivo
            if re.search(r"\.Trash|/Trash|lixeira", command, re.IGNORECASE):
                return True
            # heurística: mv que tira algo do vault pra fora
            # (origem vault, e existe um token de destino que NÃO é vault)
            tokens = command.split()
            try:
                idx = next(i for i, t in enumerate(tokens) if t == "mv")
            except StopIteration:
                return False
            args = [t for t in tokens[idx + 1:] if not t.startswith("-")]
            if len(args) >= 2:
                dest = expand(args[-1])
                srcs = [expand(a) for a in args[:-1]]
                src_in_vault = any(VAULT in s for s in srcs)
                dest_in_vault = VAULT in dest
                if src_in_vault and not dest_in_vault:
                    return True
    return False


def code_is_valid(command: str) -> bool:
    m = re.search(r"VAULT_GUARD_CODE=(\S+)", command)
    if not m:
        return False
    code = m.group(1).strip().strip("'\"")
    if not os.path.exists(HASH_FILE):
        return False
    try:
        with open(HASH_FILE) as f:
            saved = f.read().strip()
    except Exception:
        return False
    digest = hashlib.sha256(code.encode("utf-8")).hexdigest()
    return digest == saved


def unlock_ticket_valid() -> bool:
    """Verifica e CONSOME um ticket de desbloqueio criado por vault_unlock.py.
    Retorna True se havia um ticket válido (e consome um uso)."""
    if not os.path.exists(UNLOCK_FILE):
        return False
    try:
        with open(UNLOCK_FILE) as f:
            ticket = json.load(f)
    except Exception:
        return False

    expires = ticket.get("expires", 0)
    uses = ticket.get("uses", 0)

    if time.time() > expires or uses < 1:
        # expirado — limpa
        try:
            os.remove(UNLOCK_FILE)
        except OSError:
            pass
        return False

    # consome um uso
    uses -= 1
    if uses < 1:
        try:
            os.remove(UNLOCK_FILE)
        except OSError:
            pass
    else:
        ticket["uses"] = uses
        with open(UNLOCK_FILE, "w") as f:
            json.dump(ticket, f)
    return True


def block(message: str):
    sys.stderr.write(message)
    sys.exit(2)


def main():
    data = read_input()
    tool = data.get("tool_name", "")
    if tool != "Bash":
        sys.exit(0)

    command = data.get("tool_input", {}).get("command", "")
    if not command:
        sys.exit(0)

    if not touches_vault(command):
        sys.exit(0)

    if not is_destructive(command):
        sys.exit(0)

    # Operação destrutiva no vault detectada.
    # 1) ticket de desbloqueio (vault_unlock.py — código não passa pelo chat)
    if unlock_ticket_valid():
        sys.exit(0)

    # 2) código embutido no comando (compatibilidade — expõe o código)
    if code_is_valid(command):
        sys.exit(0)

    if not os.path.exists(HASH_FILE):
        block(
            "\n🛑 VAULT GUARD: operação destrutiva no Obsidian Vault BLOQUEADA.\n"
            "O código de proteção ainda NÃO foi configurado.\n"
            "Peça ao usuário para rodar:  python3 ~/.claude/scripts/vault_guard_setup.py\n"
            "Enquanto isso, NÃO apague nem mova arquivos do vault.\n"
        )

    block(
        "\n🛑 VAULT GUARD: operação destrutiva no Obsidian Vault BLOQUEADA.\n\n"
        "Comando: " + command[:200] + "\n\n"
        "Esta operação apaga ou move arquivos pra fora do vault. Regra: SÓ CONFIRMAÇÃO.\n\n"
        "AÇÃO CORRETA:\n"
        "  1. PARE. Não tente de novo nem contorne.\n"
        "  2. Pergunte ao usuário via AskUserQuestion, listando exatamente o que será\n"
        "     apagado/movido, com opções 'Sim, apagar / Não'.\n"
        "  3. SÓ se ele responder 'Sim': rode  python3 ~/.claude/scripts/vault_grant.py\n"
        "     e na sequência re-execute este comando.\n\n"
        "NUNCA rode vault_grant.py sem uma resposta 'Sim' do usuário nesta conversa, nem\n"
        "preventivamente, em lote, ou dentro de squad/loop. É a confirmação humana que protege.\n"
    )


if __name__ == "__main__":
    main()
