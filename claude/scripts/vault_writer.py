#!/usr/bin/env python3
"""
Vault Writer — Stop hook do InfinityOS.
Lê o transcript e lança o worker em background sem bloquear o Claude.
"""
import sys
import json
import os
import subprocess
from pathlib import Path


def main():
    try:
        data = json.loads(sys.stdin.read())
        transcript_path = data.get('transcript_path', '')
        if not transcript_path or not os.path.exists(transcript_path):
            return

        bg_script = Path(__file__).parent / 'vault_writer_bg.py'
        log_file = Path.home() / '.claude/scripts/vault_writer.log'

        subprocess.Popen(
            ['python3', str(bg_script), transcript_path],
            stdout=subprocess.DEVNULL,
            stderr=open(log_file, 'a'),
            start_new_session=True
        )
    except Exception:
        pass  # Nunca bloquear o Claude


if __name__ == '__main__':
    main()
