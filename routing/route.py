#!/usr/bin/env python3
# ============================================================================
#  infinity-os — roteador de modelos
#  Decide qual modelo/CLI usar para uma tarefa, com base na complexidade e na
#  disponibilidade das ferramentas instaladas. Zero dependências obrigatórias
#  (usa pyyaml se existir para ler a config; senão, usa defaults embutidos).
#
#  Uso:
#    python3 route.py --task "refatorar esta função recursiva"
#    python3 route.py --task "resumir este PDF de 200 páginas" --dry-run
#    python3 route.py --score 8 --json
#    python3 route.py --type code_refactor
# ============================================================================
import argparse
import json
import os
import re
import shutil
import sys

CONFIG_PATH = os.path.expanduser(
    os.environ.get("INFINITY_OS_ROUTER_CONFIG", "~/.infinity-os/router.config.yaml")
)

# --- Defaults embutidos (espelham router.config.template.yaml) --------------
DEFAULTS = {
    "targets": {
        "claude": {"cli": "claude", "model": "default"},
        "gemini": {"cli": "gemini", "model": "gemini-2.5-pro",
                   "command": "gemini -p {prompt}"},
        "qwen":   {"cli": "ollama", "model": "qwen3-coder:30b",
                   "command": "ollama run {model} {prompt}"},
        "codex":  {"cli": "codex", "model": "default",
                   "command": "codex exec {prompt}"},
    },
    "complexity_routing": [
        {"range": [0, 2], "target": "claude"},
        {"range": [3, 6], "target": "gemini"},
        {"range": [7, 10], "target": "qwen"},
    ],
    "task_overrides": {
        "huge_context": "gemini",
        "image_generation": "gemini",
        "code_refactor": "qwen",
        "cross_validation": "codex",
    },
    "fallback": {
        "qwen": ["qwen", "gemini", "claude"],
        "gemini": ["gemini", "claude"],
        "codex": ["codex", "claude"],
        "claude": ["claude"],
    },
}

# Sinais de complexidade (heurística simples por palavras-chave).
# stems únicos (evitar sobreposição que inflaria o score, ex.: extrai/extrair)
HEAVY = ["refator", "refactor", "arquitet", "algorit", "otimiz", "debug",
         "concorr", "performance", "migra", "recursã", "complexo",
         "raciocí", "prova", "demonstr"]
MEDIUM = ["resum", "extrai", "ocr", "documento", "pdf", "planilha",
          "traduz", "classific", "analis", "tabela", "contexto grande"]


def load_config():
    cfg = json.loads(json.dumps(DEFAULTS))  # cópia profunda
    if os.path.exists(CONFIG_PATH):
        try:
            import yaml  # opcional
            with open(CONFIG_PATH, encoding="utf-8") as fh:
                user = yaml.safe_load(fh) or {}
            cfg.update(user)
        except Exception:
            pass  # sem pyyaml ou config inválida → usa defaults
    return cfg


def estimate_complexity(task: str) -> int:
    t = (task or "").lower()
    score = 1
    score += sum(2 for k in HEAVY if k in t)
    score += sum(1 for k in MEDIUM if k in t)
    if len(t) > 600:        # prompts muito longos tendem a ser complexos
        score += 2
    return max(0, min(10, score))


def target_for_score(cfg, score: int) -> str:
    for rule in cfg["complexity_routing"]:
        lo, hi = rule["range"]
        if lo <= score <= hi:
            return rule["target"]
    return "claude"


def is_available(cfg, target: str) -> bool:
    if target == "claude":
        return True  # o motor está sempre presente
    cli = cfg["targets"].get(target, {}).get("cli", target)
    return shutil.which(cli) is not None


def resolve(cfg, target: str):
    """Aplica a cadeia de fallback até achar um alvo disponível."""
    chain = cfg["fallback"].get(target, [target, "claude"])
    for cand in chain:
        if is_available(cfg, cand):
            return cand, (cand != target)
    return "claude", True


def main():
    ap = argparse.ArgumentParser(description="Roteador de modelos do infinity-os")
    ap.add_argument("--task", default="", help="descrição da tarefa")
    ap.add_argument("--score", type=int, help="complexidade 0-10 (sobrepõe heurística)")
    ap.add_argument("--type", help="tipo de tarefa (override): " +
                    ", ".join(DEFAULTS["task_overrides"]))
    ap.add_argument("--dry-run", action="store_true", help="só decide, não executa")
    ap.add_argument("--json", action="store_true", help="saída em JSON")
    args = ap.parse_args()

    cfg = load_config()
    score = args.score if args.score is not None else estimate_complexity(args.task)

    if args.type and args.type in cfg["task_overrides"]:
        primary = cfg["task_overrides"][args.type]
        reason = f"override de tipo '{args.type}'"
    else:
        primary = target_for_score(cfg, score)
        reason = f"complexidade {score}/10"

    chosen, did_fallback = resolve(cfg, primary)
    tgt = cfg["targets"].get(chosen, {})
    decision = {
        "task": args.task,
        "score": score,
        "primary": primary,
        "chosen": chosen,
        "fellback": did_fallback,
        "reason": reason,
        "cli": tgt.get("cli", chosen),
        "model": tgt.get("model", "default"),
        "command": tgt.get("command", "(inline no Claude Code)"),
    }

    if args.json:
        print(json.dumps(decision, ensure_ascii=False, indent=2))
    else:
        fb = "  (fallback: alvo preferido indisponível)" if did_fallback else ""
        print(f"→ {chosen}  [{decision['cli']}/{decision['model']}]  "
              f"— {reason}{fb}")
        if args.dry_run:
            print(f"  comando: {decision['command']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
