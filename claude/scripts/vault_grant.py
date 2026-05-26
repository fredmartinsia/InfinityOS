#!/usr/bin/env python3
"""
vault_grant.py — Libera UMA operação destrutiva no vault APÓS confirmação humana.

Modelo "só confirmação" (modelo de confirmação humana): não há código.
A proteção é a confirmação humana ativa via AskUserQuestion. Este script
cria o ticket de desbloqueio que o hook vault_guard.py consome.

REGRA CRÍTICA PARA O CLAUDE:
  Só rode este script IMEDIATAMENTE APÓS o usuário ter respondido "Sim, apagar"
  numa pergunta de confirmação (AskUserQuestion) sobre aquela deleção específica.
  NUNCA rode preventivamente, em lote sem confirmar, ou dentro de um squad/loop
  automático. Um processo automático não confirma — é isso que protege o vault.

Cria ticket de 1 uso, válido 120s.
"""
import os
import json
import time

UNLOCK_FILE = os.path.expanduser("~/.claude/vault_unlock.json")
TTL = 120  # segundos — janela curta: criar e usar na sequência

ticket = {"expires": time.time() + TTL, "uses": 1}
with open(UNLOCK_FILE, "w") as f:
    json.dump(ticket, f)
os.chmod(UNLOCK_FILE, 0o600)

print(f"✅ Liberada 1 operação destrutiva no vault (válida {TTL}s). "
      "Use já, na sequência.")
