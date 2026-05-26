#!/usr/bin/env python3
"""
Vault Writer BG — Worker em background do Stop hook do InfiniteOS.
Lê transcript, chama Gemini, detecta projeto (existente ou novo), grava no Obsidian.
Retry 2x com backoff. Novos projetos vão para .draft.md.

Configuração:
  CLAUDE_VAULT_PATH — caminho do vault Obsidian (default: ~/Documents/Obsidian Vault)
  CLAUDE_GEMINI_CMD — caminho do binário Gemini CLI (default: ~/.npm-global/bin/gemini)
                      Se não existir, o worker sai silenciosamente.
"""
import sys
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from datetime import datetime

VAULT_PATH = Path(os.path.expanduser(
    os.environ.get("CLAUDE_VAULT_PATH", "~/Documents/Obsidian Vault")
))
GEMINI_CMD = os.path.expanduser(
    os.environ.get("CLAUDE_GEMINI_CMD", "~/.npm-global/bin/gemini")
)
LOG_FILE = Path.home() / '.claude/scripts/vault_writer.log'
MIN_MESSAGES = 3
MAX_ARG = 38_000


def log(msg):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")


# ── GEMINI ────────────────────────────────────────────────────────────────────

def _gemini_once(prompt, timeout=90):
    if len(prompt.encode('utf-8')) <= MAX_ARG:
        r = subprocess.run([GEMINI_CMD, '-y', '-p', prompt],
                           capture_output=True, text=True, timeout=timeout)
    else:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt',
                                         delete=False, encoding='utf-8') as f:
            f.write(prompt)
            tmp = f.name
        try:
            r = subprocess.run(['bash', '-c', f'cat "{tmp}" | "{GEMINI_CMD}" -y -p ""'],
                               capture_output=True, text=True, timeout=timeout)
        finally:
            try:
                os.unlink(tmp)
            except Exception:
                pass

    out = r.stdout.strip()
    if not out or len(out) < 30:
        raise ValueError(f"Resposta vazia ({len(out)} chars)")
    return out


def call_gemini(prompt, max_retries=2, backoffs=None):
    if backoffs is None:
        backoffs = [3, 8]
    for attempt in range(max_retries):
        try:
            return _gemini_once(prompt), None
        except FileNotFoundError:
            return None, "Gemini CLI não encontrado"
        except Exception as e:
            log(f"Gemini tentativa {attempt+1}: {e}")
            if attempt < max_retries - 1:
                time.sleep(backoffs[min(attempt, len(backoffs)-1)])
    return None, "Falhou após retries"


# ── TRANSCRIPT ────────────────────────────────────────────────────────────────

def read_transcript(path):
    messages = []
    try:
        with open(path, 'r', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                    role = entry.get('type', '')
                    if role == 'user':
                        content = entry.get('message', {}).get('content', '')
                        if isinstance(content, list):
                            content = ' '.join(c.get('text', '') for c in content
                                               if isinstance(c, dict) and c.get('type') == 'text')
                        content = str(content).strip()
                        if len(content) > 10:
                            messages.append(('user', content[:600]))
                    elif role == 'assistant':
                        content = entry.get('message', {}).get('content', '')
                        if isinstance(content, list):
                            content = ' '.join(c.get('text', '') for c in content
                                               if isinstance(c, dict) and c.get('type') == 'text')
                        content = str(content).strip()
                        if len(content) > 10:
                            messages.append(('assistant', content[:1000]))
                except Exception:
                    pass
    except Exception as e:
        log(f"Erro ao ler transcript: {e}")
    return messages


# ── OBSIDIAN ──────────────────────────────────────────────────────────────────

def get_vault_projects():
    p = VAULT_PATH / "Projetos"
    if not p.exists():
        return []
    names = set()
    for folder in p.iterdir():
        if folder.is_dir() and not folder.name.startswith('_'):
            names.add(folder.name)
    for f in p.glob("*.md"):
        if f.name != "README.md":
            names.add(f.stem)
    return sorted(names)


def find_note(project_name):
    p = VAULT_PATH / "Projetos"
    if not p.exists():
        return None
    nl = project_name.lower()
    for folder in p.iterdir():
        if folder.is_dir():
            for f in folder.glob("*.md"):
                if nl in f.stem.lower() or f.stem.lower() in nl:
                    return f
    for f in p.glob("*.md"):
        if nl in f.stem.lower() or f.stem.lower() in nl:
            return f
    return None


def update_obsidian(parsed, vault_projects):
    projetos = VAULT_PATH / "Projetos"
    projetos.mkdir(parents=True, exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')

    project_name = parsed.get('projeto', 'GERAL')
    is_new = parsed.get('novo_projeto', False)
    confianca = parsed.get('confianca', 'baixa')

    note_path = find_note(project_name)

    if note_path is None:
        if is_new and confianca == 'alta':
            safe_name = project_name.replace('/', '-').replace(':', '-')
            nova_pasta = projetos / safe_name
            nova_pasta.mkdir(exist_ok=True)
            draft_path = nova_pasta / f"{safe_name}.draft.md"
            header = f"""---
tags: [projeto, auto-gerado, rascunho]
criado_em: {date_str}
status: rascunho
---

# {project_name}

> 🆕 Projeto detectado automaticamente em {date_str}
> Sinais identificados: {', '.join(parsed.get('sinais_novo_projeto', []))}
> Revisa e remove este aviso quando estiver pronto.

"""
            block = build_block(parsed, date_str)
            with open(draft_path, 'w') as f:
                f.write(header + block)
            log(f"🆕 Novo projeto detectado → draft: {draft_path.name}")
            return
        else:
            note_path = projetos / "📋 Sessões Claude Code.md"

    block = build_block(parsed, date_str)
    with open(note_path, 'a') as f:
        f.write(block)
    log(f"✓ Gravado em: {note_path.name}")


def build_block(parsed, date_str):
    project_name = parsed.get('projeto', 'GERAL')
    block = f"\n\n---\n## 🤖 {date_str} — {project_name}\n"
    block += f"**Resumo:** {parsed.get('resumo', '—')}\n"

    decisoes = [d for d in parsed.get('decisoes', []) if d]
    if decisoes:
        block += "\n**Decisões:**\n" + ''.join(f"- {d}\n" for d in decisoes)

    passos = [p for p in parsed.get('proximos_passos', []) if p]
    if passos:
        block += "\n**Próximos passos:**\n" + ''.join(f"- [ ] {p}\n" for p in passos)

    ctx = parsed.get('contexto_tecnico', '').strip()
    if ctx:
        block += f"\n**Contexto técnico:** {ctx}\n"

    return block


# ── PROMPT ────────────────────────────────────────────────────────────────────

def build_prompt(conversation_text, vault_projects):
    projects_str = ', '.join(vault_projects) if vault_projects else 'nenhum'
    return f"""Analisa esta conversa do Claude Code e extrai informações para atualizar o Obsidian.

Projetos existentes no vault: {projects_str}

CONVERSA:
{conversation_text}

Classifica o projeto e responde SOMENTE em JSON válido:
{{
  "projeto": "nome exato de um projeto da lista OU nome do novo projeto detectado",
  "novo_projeto": true ou false (true se não existe na lista e há ≥3 sinais abaixo),
  "sinais_novo_projeto": ["sinal 1", "sinal 2"],
  "confianca": "alta" ou "media" ou "baixa",
  "resumo": "1-2 frases do que foi feito/discutido",
  "decisoes": ["decisão 1", "decisão 2"],
  "proximos_passos": ["próximo passo 1"],
  "contexto_tecnico": "info técnica importante para lembrar"
}}

Sinais de novo projeto: nome próprio/marca repetido, stack técnico definido, objetivo/deliverable claro, stakeholders nomeados, ausência de match na lista.
Só "novo_projeto: true" se tiver ≥3 sinais E confianca "alta".

Se conversa for trivial/sem conteúdo útil, responde: {{"ignorar": true}}"""


# ── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        log("Nenhum transcript_path fornecido")
        return

    transcript_path = sys.argv[1]
    if not os.path.exists(transcript_path):
        log(f"Transcript não encontrado: {transcript_path}")
        return

    if not os.path.exists(GEMINI_CMD):
        log(f"Gemini CLI não encontrado em {GEMINI_CMD} — worker encerrando silenciosamente")
        return

    log(f"Processando: {Path(transcript_path).name}")

    messages = read_transcript(transcript_path)
    if len(messages) < MIN_MESSAGES:
        log("Conversa curta, ignorando")
        return

    recent = messages[-40:]
    conversation_text = '\n'.join(
        f"{'USER' if r == 'user' else 'CLAUDE'}: {c}" for r, c in recent
    )

    vault_projects = get_vault_projects()
    prompt = build_prompt(conversation_text, vault_projects)

    output, err = call_gemini(prompt)
    if not output:
        log(f"Erro Gemini: {err}")
        return

    try:
        raw = output
        if '```json' in raw:
            raw = raw.split('```json')[1].split('```')[0]
        elif '```' in raw:
            raw = raw.split('```')[1].split('```')[0]
        parsed = json.loads(raw.strip())
    except Exception as e:
        log(f"Erro JSON: {e} | Raw: {output[:200]}")
        return

    if parsed.get('ignorar'):
        log("Conversa irrelevante, ignorando")
        return

    update_obsidian(parsed, vault_projects)


if __name__ == '__main__':
    main()
