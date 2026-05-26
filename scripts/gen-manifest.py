#!/usr/bin/env python3
"""Gera installer/manifest/install-manifest.yaml com SHA256 de cada arquivo.
Espelha o padrão do AIOX para detecção de mudanças em upgrades."""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "installer", "manifest", "install-manifest.yaml")
SKIP_DIRS = {".git", "__pycache__", ".DS_Store", "manifest"}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    entries = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if fn == ".DS_Store":
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            if rel.startswith("installer/manifest/"):
                continue
            entries.append((rel, sha256(full)))
    entries.sort()

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write("# install-manifest — SHA256 de cada arquivo do infinity-os\n")
        f.write("# Gerado por scripts/gen-manifest.py. Não editar à mão.\n")
        f.write(f"file_count: {len(entries)}\n")
        f.write("files:\n")
        for rel, digest in entries:
            f.write(f'  - path: "{rel}"\n    sha256: {digest}\n')
    print(f"Manifest: {len(entries)} arquivos → {OUT}")


if __name__ == "__main__":
    sys.exit(main())
