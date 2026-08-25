#!/usr/bin/env python3
"""
check_links.py - Validador DETERMINISTICO de links para deliverables do usuário.

Regra do usuário (dados-reais-sem-placeholder / validar-deliverable): nunca entregar
relatorio, pagina ou copy com link que nao abre. Como isto e verificavel por codigo,
roda em script (custo de token zero) em vez de confiar que o LLM testou.

Uso:
  python3 ~/.claude/scripts/check_links.py arquivo.md [pagina.html ...]
Extrai todas as URLs http(s), faz HEAD (fallback GET) com timeout e reporta o status.
Exit code 1 se houver ao menos um link quebrado (>=400 ou erro de conexao); 0 se todos ok.
"""
import sys, re, urllib.request, urllib.error, concurrent.futures

URL_RE = re.compile(r'https?://[^\s"\'<>\)\]}]+')


def check(url):
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(
                url, method=method,
                headers={"User-Agent": "Mozilla/5.0 (link-check)"},
            )
            with urllib.request.urlopen(req, timeout=12) as r:
                return url, getattr(r, "status", 200), ""
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue  # alguns servidores recusam HEAD; tenta GET
            return url, e.code, ""
        except Exception as e:
            if method == "HEAD":
                continue
            return url, 0, str(e)[:70]
    return url, 0, "falhou"


def main():
    files = [a for a in sys.argv[1:] if not a.startswith("-")]
    if not files:
        print("uso: check_links.py <arquivo> [arquivo...]")
        return 0
    urls = []
    for fp in files:
        try:
            txt = open(fp, errors="ignore").read()
        except Exception as e:
            print(f"! nao consegui ler {fp}: {e}")
            continue
        for u in URL_RE.findall(txt):
            urls.append(u.rstrip('.,);:'))
    urls = sorted(set(urls))
    if not urls:
        print("nenhum link http encontrado.")
        return 0
    bad = 0
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for url, status, err in ex.map(check, urls):
            ok = 200 <= (status or 0) < 400
            if not ok:
                bad += 1
            results.append((ok, status, url, err))
    for ok, status, url, err in results:
        mark = "OK " if ok else "XX "
        print(f"{mark}{status or '-'} {url}{('  ' + err) if err else ''}")
    print(f"\n{len(urls)} links, {bad} com problema.")
    return 1 if bad else 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        sys.stderr.write(f"[check_links] {e}\n")
        sys.exit(0)
