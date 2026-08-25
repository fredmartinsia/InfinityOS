#!/usr/bin/env python3
"""
router_status.py: painel de saude do router_orchestrator.

Mostra:
  - Status de cada provider (has_key, ready / pending_key / missing_key)
  - Resumo das ultimas N chamadas da telemetria
  - Taxa de sucesso por provider
  - Latencia p50/p95 por provider
  - Top 3 modelos com mais falhas (candidatos a instinto de evitacao)

Uso:
  python3 router_status.py            # painel completo
  python3 router_status.py --json     # saida JSON
  python3 router_status.py --limit 50 # ultimas 50 chamadas
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))

import router_orchestrator as ro  # noqa: E402

TELEMETRY_PATH = Path.home() / ".claude/router/telemetry.jsonl"


def _percentile(values, p):
    if not values:
        return 0
    values = sorted(values)
    k = int(round((p / 100.0) * (len(values) - 1)))
    return values[k]


def _provider_summary(entries):
    """Agrega telemetria por provider."""
    by_provider = defaultdict(list)
    for e in entries:
        by_provider[e.get("provider", "?")].append(e)
    out = {}
    for prov, items in by_provider.items():
        total = len(items)
        ok = sum(1 for i in items if i.get("success") and i.get("qa_passed"))
        err = sum(1 for i in items if not i.get("success"))
        qa_fail = sum(1 for i in items if i.get("success") and not i.get("qa_passed"))
        latencies = [i.get("latency_ms", 0) for i in items if i.get("success")]
        out[prov] = {
            "total_calls": total,
            "success_rate_pct": round((ok / total) * 100, 1) if total else 0,
            "errors": err,
            "qa_failures": qa_fail,
            "latency_p50_ms": _percentile(latencies, 50),
            "latency_p95_ms": _percentile(latencies, 95),
        }
    return out


def _top_failures(entries, n=3):
    """Top N provider:model com mais falhas."""
    counts = defaultdict(lambda: {"errors": 0, "qa_failures": 0, "total": 0})
    for e in entries:
        key = f"{e.get('provider', '?')}:{e.get('model', '?')}"
        counts[key]["total"] += 1
        if not e.get("success"):
            counts[key]["errors"] += 1
        elif not e.get("qa_passed"):
            counts[key]["qa_failures"] += 1
    ranked = sorted(
        counts.items(),
        key=lambda kv: -(kv[1]["errors"] + kv[1]["qa_failures"]),
    )
    return [
        {"provider_model": k, **v} for k, v in ranked[:n]
        if v["errors"] + v["qa_failures"] > 0
    ]


def suggest_instincts(window_hours=24, min_attempts=3, failure_rate_pct=60):
    """Le telemetria da ultima janela de horas e sugere instintos pras
    combinacoes provider:model:task_type com taxa de falha alta.

    Heuristica do usuÃ¡rio: "modelo X caiu 3x em 1h gera instinto de evitacao".
    Nao cria automaticamente (regra 'manual primeiro'): so imprime a sugestao
    pra o usuÃ¡rio aprovar via `instincts.py add` ou colar no YAML.
    """
    import time as _t
    from datetime import datetime, timedelta

    if not TELEMETRY_PATH.exists():
        return []

    cutoff = (datetime.now() - timedelta(hours=window_hours)).strftime("%Y-%m-%dT%H:%M:%S")
    buckets = defaultdict(lambda: {"ok": 0, "fail": 0, "last_err": ""})
    with open(TELEMETRY_PATH) as f:
        for line in f:
            try:
                e = json.loads(line)
            except Exception:
                continue
            if e.get("timestamp", "") < cutoff:
                continue
            key = (e.get("provider", "?"), e.get("model", "?"), e.get("task_type", "?"))
            if e.get("success") and e.get("qa_passed"):
                buckets[key]["ok"] += 1
            else:
                buckets[key]["fail"] += 1
                buckets[key]["last_err"] = e.get("error") or "QA reprovado"

    sugestoes = []
    for (prov, model, task), counts in buckets.items():
        total = counts["ok"] + counts["fail"]
        if total < min_attempts:
            continue
        rate = (counts["fail"] / total) * 100
        if rate < failure_rate_pct:
            continue
        iid = f"router-evitar-{prov}-{task}".replace("/", "_").replace(":", "-")
        sugestoes.append({
            "id": iid,
            "provider": prov,
            "model": model,
            "task_type": task,
            "total_chamadas": total,
            "taxa_falha_pct": round(rate, 1),
            "ultimo_erro": counts["last_err"][:100],
            "confidence": 0.6 if rate >= 80 else 0.5,
        })
    return sorted(sugestoes, key=lambda s: -s["taxa_falha_pct"])


def render_suggestions(sugestoes):
    if not sugestoes:
        return ("Nenhuma sugestao de instinto no momento.\n"
                "Padroes de falha aparecem aqui quando algum provider:model:task_type\n"
                "falha em >=60% das chamadas com pelo menos 3 tentativas em 24h.")
    lines = ["SUGESTOES DE INSTINTO (mineradas da telemetria do router):", "=" * 64, ""]
    for s in sugestoes:
        sid = s["id"]
        prov = s["provider"]
        model = s["model"]
        task = s["task_type"]
        taxa = s["taxa_falha_pct"]
        total = s["total_chamadas"]
        conf = s["confidence"]
        acao = f"evitar {prov}:{model} para task {task} (falhou {taxa}% em {total} chamadas em 24h)"
        lines.append(f"ID: {sid}")
        lines.append(f"  provider={prov} model={model} task={task}")
        lines.append(f"  falha={taxa}% em {total} chamadas")
        lines.append(f"  ultimo erro: {s['ultimo_erro']}")
        lines.append(f"  confidence sugerida: {conf}")
        lines.append("  comando p/ criar:")
        lines.append("    python3 ~/.claude/scripts/instincts.py add \\")
        lines.append(f"      --id {sid} \\")
        lines.append(f"      --confidence {conf} \\")
        lines.append('      --trigger "QUANDO roteamento LLM" \\')
        lines.append(f'      --action "{acao}"')
        lines.append("")
    return "\n".join(lines)


def render_human(limit=100):
    cfg = ro._load_config()
    status = ro.provider_status()
    entries = ro.read_telemetry(limit=limit)
    summary = _provider_summary(entries)
    failures = _top_failures(entries)

    lines = []
    lines.append("=" * 64)
    lines.append("ROUTER ORCHESTRATOR - PAINEL DE SAUDE")
    lines.append("=" * 64)
    lines.append("")

    lines.append("PROVIDERS:")
    lines.append("-" * 64)
    for name, info in status.items():
        prov_cfg = cfg["providers"].get(name, {})
        cost = prov_cfg.get("cost", "?")
        kind = prov_cfg.get("kind", "?")
        models = len(prov_cfg.get("models", []))
        flag = {
            "subscription": "[SUB]",
            "ready": "[OK] ",
            "pending_key": "[PEND]",
            "missing_key": "[MISS]",
        }.get(info["status"], "[?]")
        lines.append(
            f"  {flag} {name:18s} cost={cost:6s} kind={kind:20s} models={models}"
        )
    lines.append("")

    lines.append("TASK TYPES:")
    lines.append("-" * 64)
    for tt_name, tt in cfg.get("task_types", {}).items():
        chain_len = len(tt.get("chain", []))
        policy = tt.get("policy", "?")
        lines.append(f"  {tt_name:14s} policy={policy:12s} chain_depth={chain_len}")
    lines.append("")

    if not entries:
        lines.append("TELEMETRIA: vazia (sem chamadas registradas ainda).")
        lines.append("")
        lines.append("Rode um smoke test:")
        lines.append("  python3 ~/.claude/scripts/router_orchestrator.py 'resuma: ola mundo' --type volume_short")
        return "\n".join(lines)

    lines.append(f"TELEMETRIA (ultimas {len(entries)} chamadas):")
    lines.append("-" * 64)
    for prov, s in sorted(summary.items(), key=lambda kv: -kv[1]["total_calls"]):
        lines.append(
            f"  {prov:18s} calls={s['total_calls']:4d} "
            f"success={s['success_rate_pct']:5.1f}% "
            f"err={s['errors']:3d} qa_fail={s['qa_failures']:3d} "
            f"p50={s['latency_p50_ms']:5d}ms p95={s['latency_p95_ms']:5d}ms"
        )
    lines.append("")

    if failures:
        lines.append("TOP CANDIDATOS A INSTINTO DE EVITACAO:")
        lines.append("-" * 64)
        for f in failures:
            pm = f["provider_model"]
            tot = f["total"]
            err_pct = ((f["errors"] + f["qa_failures"]) / tot * 100) if tot else 0
            lines.append(
                f"  {pm:50s} err={f['errors']:3d} qa_fail={f['qa_failures']:3d} "
                f"of {tot} ({err_pct:.0f}%)"
            )
    lines.append("")
    lines.append("=" * 64)
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true", help="saida em JSON")
    ap.add_argument("--limit", type=int, default=100, help="ultimas N chamadas")
    ap.add_argument("--suggest-instincts", action="store_true",
                    help="mina telemetria e sugere instintos de evitacao (nao cria)")
    ap.add_argument("--window-hours", type=int, default=24,
                    help="janela de horas pra minerar instintos (default 24)")
    args = ap.parse_args()

    if args.suggest_instincts:
        sugestoes = suggest_instincts(window_hours=args.window_hours)
        print(render_suggestions(sugestoes))
        return

    if args.json:
        cfg = ro._load_config()
        out = {
            "providers": ro.provider_status(),
            "task_types": list(cfg.get("task_types", {}).keys()),
            "telemetry_summary": _provider_summary(ro.read_telemetry(limit=args.limit)),
            "top_failures": _top_failures(ro.read_telemetry(limit=args.limit)),
            "config_path": str(ro.CONFIG_PATH),
        }
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print(render_human(limit=args.limit))


if __name__ == "__main__":
    main()
