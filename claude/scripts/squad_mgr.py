#!/usr/bin/env python3
"""
squad_mgr.py: arquiva/restaura squads (diretorios de comandos) sem deletar nada.

Squads dormentes saem do autoload (economiza tokens do indice de skills) indo pra
~/.claude/commands_archive/. Restaurar e mover de volta. Nada e apagado; reverter
e sempre um mv. Fora do vault, entao o vault_guard nao se aplica.

Uso:
  squad_mgr.py list                 lista squads ativos (commands/) e arquivados
  squad_mgr.py archive <nome> ...   move commands/<nome> -> commands_archive/<nome>
  squad_mgr.py restore <nome> ...   move commands_archive/<nome> -> commands/<nome>

Depois de arquivar/restaurar, reinicie a sessao pra o indice de skills refletir.
"""
import os
import shutil
import sys
from pathlib import Path

COMMANDS = Path(os.path.expanduser("~/.claude/commands"))
ARCHIVE = Path(os.path.expanduser("~/.claude/commands_archive"))

# squads/comandos que nunca devem ser arquivados por engano
PROTECTED = {
    "mudou.md", "aprender.md", "metaads-on.md", "travel-on.md",
    "mcp-status.md", "squad-archive.md", "squad-restore.md",
}


def _dirs(base):
    if not base.exists():
        return []
    return sorted(p.name for p in base.iterdir() if p.is_dir())


def cmd_list():
    print("ATIVOS (commands/):")
    for d in _dirs(COMMANDS):
        print("  " + d)
    print("\nARQUIVADOS (commands_archive/):")
    arch = _dirs(ARCHIVE)
    if not arch:
        print("  (nenhum)")
    for d in arch:
        print("  " + d)


def _move(names, src, dst, verb):
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for name in names:
        name = name.strip().strip("/")
        if name + ".md" in PROTECTED or name in PROTECTED:
            print(f"PROTEGIDO, ignorado: {name}", file=sys.stderr)
            continue
        s = src / name
        d = dst / name
        if not s.is_dir():
            print(f"nao encontrado em {src.name}/: {name}", file=sys.stderr)
            continue
        if d.exists():
            print(f"ja existe em {dst.name}/: {name}", file=sys.stderr)
            continue
        shutil.move(str(s), str(d))
        print(f"{verb}: {name}")


def main():
    if len(sys.argv) < 2:
        cmd_list()
        return
    cmd = sys.argv[1]
    args = sys.argv[2:]
    if cmd == "list":
        cmd_list()
    elif cmd == "archive" and args:
        _move(args, COMMANDS, ARCHIVE, "arquivado")
        print("\nReinicie a sessao pra o indice de skills refletir.")
    elif cmd == "restore" and args:
        _move(args, ARCHIVE, COMMANDS, "restaurado")
        print("\nReinicie a sessao pra o indice de skills refletir.")
    else:
        print("uso: squad_mgr.py [list | archive <nome>... | restore <nome>...]",
              file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
