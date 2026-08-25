#!/usr/bin/env python3
"""
Instincts — camada de "memoria que aprende" para o ambiente do usuÃ¡rio.

Arquitetura inspirada no continuous-learning-v2 do everything-claude-code
(affaan-m), porem re-implementada de forma leve e sob medida, enxertada no
stack que ja existe (claude-mem), sem hooks de captura redundantes e SEM
encostar no vault_guard.

Conceito: cada "instinto" e uma licao atomica (gatilho -> acao) com uma nota
de confianca (0.3 tentativo .. 0.9 quase certo). A confianca REFORCA quando o
padrao se confirma e DECAI quando o usuÃ¡rio corrige. Instintos ativos (>= 0.5)
sao injetados no inicio de cada sessao para que sejam de fato seguidos.

Comandos:
  list                 Lista instintos com nota de confianca.
  inject [--hook]      Imprime instintos ativos (>=0.5). --hook = JSON p/ SessionStart.
  add                  Cria um instinto novo.
  reinforce <id>       Sobe a confianca (+0.1, teto 0.9).
  decay <id>           Desce a confianca (-0.2, piso 0.2; abaixo arquiva).
  show <id>            Mostra um instinto em detalhe.
  mine [--days N]      Garimpa correcoes no claude-mem.db e sugere instintos.
  seed                 Cria os instintos iniciais a partir dos padroes do usuÃ¡rio.
"""
import argparse
import datetime
import glob
import os
import re
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("[instincts] PyYAML necessario (pip install pyyaml)\n")
    sys.exit(0)  # nunca derrubar uma sessao

HOME = os.path.expanduser("~")
STORE = os.path.join(HOME, ".claude", "instincts", "personal")
ARCHIVE = os.path.join(HOME, ".claude", "instincts", "archive")
CLAUDE_MEM_DB = os.path.join(HOME, ".claude-mem", "claude-mem.db")

ACTIVE_THRESHOLD = 0.5
REINFORCE_STEP = 0.1
DECAY_STEP = 0.2
CONF_CEILING = 0.9
CONF_FLOOR = 0.2

# Sinais de correcao em PT/EN para garimpar no historico de prompts
CORRECTION_SIGNALS = [
    "nao gostei", "nao e assim", "nao era isso", "ta errado", "esta errado",
    "refaz", "refazer", "muda isso", "ja te falei", "ja pedi", "de novo nao",
    "nao precisa", "nao faz", "para de", "errado", "nao quero", "evita",
    "lembra que", "como eu pedi", "nao era pra", "ficou generico", "muito generico",
]


def _now():
    return datetime.datetime.now().isoformat(timespec="seconds")


def _ensure_dirs():
    os.makedirs(STORE, exist_ok=True)
    os.makedirs(ARCHIVE, exist_ok=True)


def _path(iid):
    return os.path.join(STORE, f"{iid}.yaml")


def _load_all():
    out = []
    for fp in sorted(glob.glob(os.path.join(STORE, "*.yaml"))):
        try:
            with open(fp, "r", encoding="utf-8") as f:
                d = yaml.safe_load(f) or {}
            d["_path"] = fp
            out.append(d)
        except Exception as e:
            sys.stderr.write(f"[instincts] erro lendo {fp}: {e}\n")
    return out


def _save(d):
    _ensure_dirs()
    fp = d.pop("_path", None) or _path(d["id"])
    with open(fp, "w", encoding="utf-8") as f:
        yaml.safe_dump(d, f, allow_unicode=True, sort_keys=False)
    return fp


def _get(iid):
    fp = _path(iid)
    if not os.path.exists(fp):
        return None
    with open(fp, "r", encoding="utf-8") as f:
        d = yaml.safe_load(f) or {}
    d["_path"] = fp
    return d


def _bar(conf):
    filled = int(round(conf * 10))
    return "█" * filled + "·" * (10 - filled)


def _band(conf):
    if conf >= 0.85:
        return "quase certo"
    if conf >= 0.65:
        return "forte"
    if conf >= 0.45:
        return "moderado"
    return "tentativo"


# ─────────────────────────────────────────────────────────────── comandos ───
def cmd_list(args):
    items = sorted(_load_all(), key=lambda x: -x.get("confidence", 0))
    if not items:
        print("(nenhum instinto ainda — rode: instincts.py seed)")
        return 0
    for d in items:
        c = d.get("confidence", 0)
        print(f"[{c:.2f}] {_bar(c)} {d.get('id')}  ({d.get('domain','?')}, {_band(c)})")
        print(f"        quando: {d.get('trigger','')}")
        print(f"        acao:   {d.get('action','')}")
    return 0


def cmd_show(args):
    d = _get(args.id)
    if not d:
        print(f"instinto '{args.id}' nao encontrado")
        return 1
    d.pop("_path", None)
    print(yaml.safe_dump(d, allow_unicode=True, sort_keys=False))
    return 0


INJECT_CAP = 24  # teto de instintos injetados por sessao (subido de 10 p/ acomodar o acervo de heuristicas destiladas; poda-se via decay/confianca)


def cmd_inject(args):
    items = [d for d in _load_all() if d.get("confidence", 0) >= ACTIVE_THRESHOLD]
    items.sort(key=lambda x: -x.get("confidence", 0))
    items = items[:INJECT_CAP]
    if not items:
        return 0
    lines = ["## 🧠 Instintos ativos (licoes aprendidas com o usuÃ¡rio — siga-as)"]
    for d in items:
        lines.append(f"- [conf {d.get('confidence',0):.1f}] QUANDO {d.get('trigger','')}: "
                     f"{d.get('action','')} ({d.get('id')})")
    text = "\n".join(lines)
    if args.hook:
        import json
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": text,
        }}))
    else:
        print(text)
    return 0


def cmd_add(args):
    _ensure_dirs()
    iid = args.id or re.sub(r"[^a-z0-9]+", "-", (args.trigger or "instinto").lower())[:40].strip("-")
    if _get(iid):
        print(f"ja existe instinto '{iid}'. Use reinforce/decay ou outro id.")
        return 1
    d = {
        "id": iid,
        "trigger": args.trigger,
        "action": args.action,
        "confidence": float(args.confidence),
        "domain": args.domain or "geral",
        "source": args.source or "manual",
        "scope": "global",
        "created_at": _now(),
        "updated_at": _now(),
        "reinforce_count": 0,
        "decay_count": 0,
        "evidence": [args.evidence] if args.evidence else [],
    }
    fp = _save(d)
    print(f"criado: {fp}  (conf {d['confidence']:.2f})")
    return 0


def cmd_reinforce(args):
    d = _get(args.id)
    if not d:
        print(f"instinto '{args.id}' nao encontrado")
        return 1
    old = d.get("confidence", 0.5)
    d["confidence"] = round(min(CONF_CEILING, old + REINFORCE_STEP), 2)
    d["reinforce_count"] = d.get("reinforce_count", 0) + 1
    d["updated_at"] = _now()
    if args.note:
        d.setdefault("evidence", []).append(f"[+] {args.note}")
    _save(d)
    print(f"{args.id}: {old:.2f} -> {d['confidence']:.2f} (reforcado)")
    return 0


def cmd_decay(args):
    d = _get(args.id)
    if not d:
        print(f"instinto '{args.id}' nao encontrado")
        return 1
    old = d.get("confidence", 0.5)
    newc = round(old - DECAY_STEP, 2)
    d["decay_count"] = d.get("decay_count", 0) + 1
    d["updated_at"] = _now()
    if args.note:
        d.setdefault("evidence", []).append(f"[-] {args.note}")
    if newc < CONF_FLOOR:
        # arquiva em vez de apagar (reversivel)
        _ensure_dirs()
        fp = d.pop("_path")
        d["confidence"] = newc
        with open(os.path.join(ARCHIVE, os.path.basename(fp)), "w", encoding="utf-8") as f:
            yaml.safe_dump(d, f, allow_unicode=True, sort_keys=False)
        os.remove(fp)
        print(f"{args.id}: {old:.2f} -> {newc:.2f} (abaixo do piso; arquivado)")
    else:
        d["confidence"] = newc
        _save(d)
        print(f"{args.id}: {old:.2f} -> {newc:.2f} (decaido)")
    return 0


def cmd_mine(args):
    if not os.path.exists(CLAUDE_MEM_DB):
        print(f"claude-mem.db nao encontrado em {CLAUDE_MEM_DB}")
        return 1
    import sqlite3
    db = sqlite3.connect(CLAUDE_MEM_DB)
    cutoff = int((datetime.datetime.now() - datetime.timedelta(days=args.days)).timestamp())
    rows = db.execute(
        "select prompt_text, created_at from user_prompts "
        "where created_at_epoch >= ? order by created_at_epoch desc",
        (cutoff,),
    ).fetchall()
    # Marcadores de prompt NAO-humano (injecoes do sistema) — devem ser ignorados
    NOISE = ("<task-notification>", "<system-reminder>", "<command-", "caveat:",
             "[system", "your questions have been answered", "<local-command",
             "stdout", "output-file", "tool-use-id", "<bash-")
    hits = []
    human = 0
    for text, ts in rows:
        low = (text or "").lower()
        if any(m in low for m in NOISE):
            continue
        if len(low) > 4000:  # despejos longos raramente sao correcao pontual
            continue
        human += 1
        for sig in CORRECTION_SIGNALS:
            if re.search(r"\b" + re.escape(sig) + r"\b", low):
                hits.append((sig, (text or "").strip().replace("\n", " ")[:160], ts))
                break
    print(f"Garimpei {len(rows)} prompts ({human} humanos) dos ultimos {args.days} dias.")
    print(f"Encontrei {len(hits)} possiveis correcoes (candidatos a instinto):\n")
    for sig, snippet, ts in hits[: args.limit]:
        print(f"  [{sig}] {snippet}")
    if hits:
        print("\nRevise os padroes recorrentes e crie instintos com:")
        print('  instincts.py add --trigger "..." --action "..." --domain ... --confidence 0.5')
    return 0


SEEDS = [
    dict(id="dados-reais-sem-placeholder", domain="entrega", confidence=0.7,
         trigger="ao entregar relatorio, pagina, copy ou qualquer deliverable",
         action="Validar que TODOS os links e imagens funcionam de verdade. Nunca usar placeholder, dado ou URL ficticio. Se algo for estimativa, marcar explicitamente como tal.",
         evidence="Recorrente: sua empresa (STLs ficticios), AMZSS (imagens placeholder), Fechamento Caixa (links quebrados)."),
    dict(id="escopo-minimo", domain="workflow", confidence=0.7,
         trigger="ao implementar uma tarefa",
         action="Fazer exatamente o que foi pedido, sem adicionar features nao solicitadas. Se algo parece faltar, perguntar antes de adicionar. Deixar campo vazio mas preparado em vez de implementar a mais.",
         evidence="Recorrente: Fechamento Caixa (adiou categorizacao/socios), sua comunidade (recusou complexidade em logos)."),
    dict(id="copy-evergreen", domain="copy", confidence=0.6,
         trigger="ao criar copy ou conteudo com numeros/dados especificos",
         action="Preferir formulacoes reutilizaveis que nao exijam atualizacao a cada uso. Abstrair numeros especificos em variavel ou placeholder claro em vez de hardcode efemero.",
         evidence="SORTEIOS: pediu trocar 'X mil participantes' por algo reutilizavel."),
    dict(id="hook-forte", domain="copy", confidence=0.7,
         trigger="ao escrever ou revisar copy",
         action="Investir tempo desproporcional no hook (primeiras linhas). Evitar aberturas genericas ou congratulatorias. Quando pedir revisao de copy, comecar a refacao pelo hook.",
         evidence="Recorrente: SORTEIOS e AMZSS. 'O hook ai nao esta legal', 'muito genericosao'."),
    dict(id="blend-de-versoes", domain="iteracao", confidence=0.6,
         trigger="quando o usuÃ¡rio comparar versoes de um deliverable",
         action="Entender quais partes ele prefere de cada versao e combinar (blend), em vez de descartar uma versao inteira. Parte X da v2 + parte Y da v3 = v4.",
         evidence="AMZSS: v2+v3 -> v4. 'una a segunda versao com as informacoes da terceira'."),
    dict(id="clones-completos", domain="clones", confidence=0.7,
         trigger="quando o usuÃ¡rio pedir para acionar um clone (ex: clone do Hormozi)",
         action="Carregar e usar TODOS os arquivos do clone (via INFINITY_VAULT_PATH ou fallback local), nao so o SYSTEM_PROMPT. Aplicar frameworks, heuristicas e exemplos reais.",
         evidence="AMZSS: 'nao usa so o prompt do Alex; usa os frameworks, heuristicas e explora todos os arquivos'."),
]


def cmd_seed(args):
    _ensure_dirs()
    created, skipped = 0, 0
    for s in SEEDS:
        if _get(s["id"]):
            skipped += 1
            continue
        d = {
            "id": s["id"], "trigger": s["trigger"], "action": s["action"],
            "confidence": s["confidence"], "domain": s["domain"],
            "source": "seed:feedback_patterns", "scope": "global",
            "created_at": _now(), "updated_at": _now(),
            "reinforce_count": 0, "decay_count": 0,
            "evidence": [s["evidence"]],
        }
        _save(d)
        created += 1
    print(f"seed concluido: {created} criados, {skipped} ja existiam.")
    return 0


def main():
    p = argparse.ArgumentParser(prog="instincts.py")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("list")
    sub.add_parser("seed")
    sp = sub.add_parser("show"); sp.add_argument("id")

    ip = sub.add_parser("inject"); ip.add_argument("--hook", action="store_true")

    ap = sub.add_parser("add")
    ap.add_argument("--id"); ap.add_argument("--trigger", required=True)
    ap.add_argument("--action", required=True); ap.add_argument("--domain")
    ap.add_argument("--confidence", default=0.5); ap.add_argument("--source")
    ap.add_argument("--evidence")

    rp = sub.add_parser("reinforce"); rp.add_argument("id"); rp.add_argument("--note")
    dp = sub.add_parser("decay"); dp.add_argument("id"); dp.add_argument("--note")

    mp = sub.add_parser("mine")
    mp.add_argument("--days", type=int, default=30); mp.add_argument("--limit", type=int, default=40)

    args = p.parse_args()
    dispatch = {
        "list": cmd_list, "show": cmd_show, "inject": cmd_inject, "add": cmd_add,
        "reinforce": cmd_reinforce, "decay": cmd_decay, "mine": cmd_mine, "seed": cmd_seed,
    }
    fn = dispatch.get(args.cmd)
    if not fn:
        p.print_help()
        return 0
    try:
        return fn(args)
    except Exception as e:
        sys.stderr.write(f"[instincts] erro: {e}\n")
        return 0  # nunca derrubar uma sessao


if __name__ == "__main__":
    sys.exit(main())
