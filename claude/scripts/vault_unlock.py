#!/usr/bin/env python3
"""
vault_unlock.py — Desbloqueia o Obsidian Vault para UMA operação destrutiva,
sem que o código precise passar pelo chat do Claude.

Como funciona:
  1. Você roda este script (num terminal, ou via `! python3 ...`).
  2. Ele pede o código (digitação OCULTA — o Claude não vê).
  3. Se o código bater com o hash, cria um "ticket de desbloqueio" temporário
     em ~/.claude/vault_unlock.json: válido por TEMPO limitado e para N operações.
  4. O hook vault_guard.py vê o ticket válido e libera a próxima deleção,
     consumindo um uso. Quando os usos acabam ou o tempo expira, trava de novo.

Uso:
  python3 ~/.claude/scripts/vault_unlock.py            # 1 operação, 5 minutos
  python3 ~/.claude/scripts/vault_unlock.py 3          # 3 operações
  python3 ~/.claude/scripts/vault_unlock.py 3 600      # 3 operações, 600s
"""
import os
import sys
import json
import time
import getpass
import hashlib

HASH_FILE = os.path.expanduser("~/.claude/vault_guard.sha256")
UNLOCK_FILE = os.path.expanduser("~/.claude/vault_unlock.json")

DEFAULT_USES = 1
DEFAULT_TTL = 300  # segundos


def main():
    uses = DEFAULT_USES
    ttl = DEFAULT_TTL
    if len(sys.argv) >= 2:
        try:
            uses = max(1, int(sys.argv[1]))
        except ValueError:
            pass
    if len(sys.argv) >= 3:
        try:
            ttl = max(30, int(sys.argv[2]))
        except ValueError:
            pass

    if not os.path.exists(HASH_FILE):
        print("❌ Nenhum código configurado. Rode primeiro: python3 ~/.claude/scripts/vault_guard_setup.py")
        sys.exit(1)

    with open(HASH_FILE) as f:
        saved = f.read().strip()

    code = getpass.getpass("Código de proteção do vault (oculto): ").strip()
    digest = hashlib.sha256(code.encode("utf-8")).hexdigest()

    if digest != saved:
        print("❌ Código incorreto. Vault continua bloqueado.")
        sys.exit(1)

    ticket = {"expires": time.time() + ttl, "uses": uses}
    with open(UNLOCK_FILE, "w") as f:
        json.dump(ticket, f)
    os.chmod(UNLOCK_FILE, 0o600)

    print(f"✅ Vault desbloqueado para {uses} operação(ões), válido por {ttl}s "
          f"(~{ttl // 60} min). Diga ao Claude que pode prosseguir.")


if __name__ == "__main__":
    main()
