#!/usr/bin/env python3
"""
vault_guard_setup.py — Define (ou troca) o código de proteção do Obsidian Vault.

O código que você digitar NÃO é salvo em lugar nenhum em texto puro.
Só o hash SHA-256 vai pra ~/.claude/vault_guard.sha256 (modo 600).
Guarde o código na sua cabeça / gerenciador de senhas. Sem ele, operações
destrutivas no vault ficam bloqueadas pelo hook vault_guard.py.

Uso:  python3 ~/.claude/scripts/vault_guard_setup.py
"""
import os
import sys
import getpass
import hashlib

HASH_FILE = os.path.expanduser("~/.claude/vault_guard.sha256")


def main():
    print("=== Configuração do Código de Proteção do Vault ===")
    print("O código não será exibido enquanto você digita.")
    print("Ele NÃO é salvo em texto — só o hash. Anote num lugar seguro.\n")

    if os.path.exists(HASH_FILE):
        print("⚠️  Já existe um código configurado. Isto vai SUBSTITUÍ-LO.\n")

    code1 = getpass.getpass("Digite o código novo: ").strip()
    if len(code1) < 4:
        print("❌ Código muito curto (mínimo 4 caracteres). Abortado.")
        sys.exit(1)

    code2 = getpass.getpass("Confirme o código: ").strip()
    if code1 != code2:
        print("❌ Os códigos não batem. Abortado.")
        sys.exit(1)

    digest = hashlib.sha256(code1.encode("utf-8")).hexdigest()
    with open(HASH_FILE, "w") as f:
        f.write(digest + "\n")
    os.chmod(HASH_FILE, 0o600)

    print(f"\n✅ Código configurado. Hash salvo em {HASH_FILE}")
    print("A partir de agora, apagar/mover-pra-fora arquivos do vault exige esse código.")


if __name__ == "__main__":
    main()
