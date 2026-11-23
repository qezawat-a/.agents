#!/usr/bin/env python3
"""
verify_params.py -- Verify project code against official API parameter tables.

Loads endpoints.json (produced by extract_params.py), scans a project tree for
API call sites (HTTP calls or SDK function calls that target a known endpoint),
collects the parameters each call passes, and cross-references them against the
official tables:

  * unknown param   -- code sends a parameter the official docs don't list
  * missing param   -- an officially-required parameter is never passed
  * likely typo     -- an unknown param is one edit away from an official param

Outputs a JSON report and a markdown summary so any agent (or reviewer) can
see exactly where code diverges from the official docs.

Usage:
  python3 verify_params.py \
    --in endpoints.json \
    --scan /path/to/project \
    --out reports/param_verification.json \
    --md reports/param_verification.md

Standard library only.
"""

from __future__ import annotations

import argparse
import datetime
import difflib
import json
import os
import re
import sys

BOOLEAN_MAP = {True: "yes", False: "no", None: "?"}

DEFAULT_EXTS = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".java", ".kt", ".rb", ".php", ".cs", ".rs", ".swift"}

DEFAULT_SKIP_DIRS = {
    ".git", ".svn", ".hg", "node_modules", ".venv", "venv", "__pycache__",
    ".gradle", "build", "dist", "target", ".next", "coverage", ".mypy_cache",
}

# How a call site names its target endpoint. Ordered: most specific first.
URL_RE = re.compile(
    r'''(?:["'])                                  # opening quote
        (?:https?://[^/"']+/)?                    # optional base host
        ([A-Za-z0-9_./{}:%\-]+)                   # path
    ["']''',
    re.VERBOSE,
)
QUERY_RE = re.compile(r"[?&]([A-Za-z_][A-Za-z0-9_]*)\s*=", re.IGNORECASE)
JS_OBJECT_KEY_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(?![\s,}\]])")
PY_KWARG_RE = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(?![\s,\)\]])")
DICT_KEY_RE = re.compile(r'''["']([A-Za-z_][A-Za-z0-9_]*)["']\s*:''')
HTTP_VERB_RE = re.compile(r"\b(GET|POST|PUT|DELETE|PATCH)\b", re.IGNORECASE)


def esc(text):
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def load_endpoints(input_path):
    with open(input_path, "r", encoding="utf-8") as handle:
        document = json.load(handle)
    return document.get("endpoints", [])


def index_endpoints(endpoints):
    """Build lookup structures: by path, by slug, by title keywords."""
    by_path = {}
    by_slug = {}
    entries = []
    for ep in endpoints:
        if ep.get("error"):
            continue
        entry = {
            "title": ep.get("title") or "",
            "method": (ep.get("method") or "").upper(),
            "path": ep.get("path") or "",
            "url": ep.get("url") or "",
            "label": ep.get("label") or "",
            "request_params": [p.get("name", "") for p in (ep.get("request_params") or []) if p.get("name")],
            "response_params": [p.get("name", "") for p in (ep.get("response_params") or []) if p.get("name")],
            "all_params": [],
        }
        entry["all_params"] = list(dict.fromkeys(
            entry["request_params"] + entry["response_params"] + entry.get("push_params", [])
        ))
        entries.append(entry)
        if entry["path"]:
            by_path[entry["path"]] = entry
        slug = re.sub(r"[^a-z0-9]+", "", entry["title"].lower())
        if slug:
            by_slug[slug] = entry
        for word in re.findall(r"[A-Za-z]{3,}", entry["title"].lower()):
            by_slug.setdefault(word, entry)
    return entries, by_path, by_slug


def find_call_sites(root, exts, skip_dirs):
    """Walk the project and return list of {file, line, text} for text lines that look like API calls."""
    sites = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs and not d.startswith(".")]
        for fname in filenames:
            if os.path.splitext(fname)[1].lower() not in exts:
                continue
            full = os.path.join(dirpath, fname)
            try:
                with open(full, "r", encoding="utf-8", errors="replace") as handle:
                    lines = handle.readlines()
            except OSError:
                continue
            for lineno, line in enumerate(lines, 1):
                if looks_like_api_call(line):
                    sites.append({"file": full, "line": lineno, "text": line.rstrip("\n")})
    return sites


API_HINTS = (
    "http", "fetch", "axios", "request", "curl", "api", "endpoint",
    "place_order", "placeOrder", "get_tickers", "getTickers", "get_depth",
    "getDepth", "get_kline", "getKline", "change_leverage", "modify_order",
    "cancel_order", "create_order", "order", "position", "ticker", "depth",
    "kline", "funding", "trade", "account", "websocket", "ws",
)


def looks_like_api_call(line):
    low = line.lower()
    if not any(hint in low for hint in API_HINTS):
        return False
    return bool(
        re.search(r"(fetch|axios|request|curl|http|ajax)\s*[\(\[]", line, re.IGNORECASE)
        or re.search(r"\.(get|post|put|delete|patch|request)\s*\(", line, re.IGNORECASE)
        or re.search(r"\b(place_order|get_tickers|get_depth|get_kline|modify_order|cancel_order|create_order|placeOrder|getTickers|getDepth|getKline)\s*[\\(]", line)
        or re.search(r"/api/", line)
        or re.search(r'["\']/(?:futures|spot|market|trade|account|position|websocket)/', line)
    )


def endpoint_for_site(text, by_path, by_slug, entries):
    """Guess which official endpoint a call site targets, by URL or by name keywords."""
    matched = []

    # 1) Direct path match in a string URL
    for match in URL_RE.finditer(text):
        path = match.group(1)
        norm = path if path.startswith("/") else "/" + path
        norm = re.sub(r"/+", "/", norm)
        for candidate_path, entry in by_path.items():
            if norm == candidate_path or norm.endswith(candidate_path) or candidate_path in norm:
                matched.append(entry)
        # query-string embedded params
        if "?" in path:
            qparams = QUERY_RE.findall(path)
            if qparams:
                matched.append({"_qparams": qparams, "_path": norm, "_match": "query"})

    # 2) Name keyword match (function name / variable)
    words = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", text))
    low_words = {w.lower() for w in words}
    for entry in entries:
        title_words = set(re.findall(r"[A-Za-z]{3,}", entry["title"].lower()))
        slug_words = set(re.sub(r"[^a-z0-9]+", "", entry["title"].lower()))
        if title_words and title_words & low_words:
            matched.append(entry)
        elif slug_words and slug_words & low_words:
            matched.append(entry)

    # De-duplicate
    seen = set()
    unique = []
    for m in matched:
        key = m.get("path") or m.get("title") or str(m)
        if key in seen:
            continue
        seen.add(key)
        unique.append(m)
    return unique


def collect_params(text):
    """Extract parameter names passed at one call site (object keys, kwargs, dict keys, query string)."""
    params = []
    for pattern in (JS_OBJECT_KEY_RE, PY_KWARG_RE, DICT_KEY_RE):
        params.extend(match.group(1) for match in pattern.finditer(text))
    params.extend(QUERY_RE.findall(text))
    # de-duplicate preserving order
    out = []
    seen = set()
    for p in params:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


def edit_distance(a, b):
    a, b = a.lower(), b.lower()
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        current = [i] + [0] * len(b)
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            current[j] = min(
                current[j - 1] + 1,      # deletion
                previous[j] + 1,         # insertion
                previous[j - 1] + cost,  # substitution
            )
        previous = current
    return previous[-1]


def likely_typo(unknown, official):
    matches = difflib.get_close_matches(unknown, official, n=3, cutoff=0.75)
    return matches


def verify_site(site, official_params, by_path, by_slug):
    text = site["text"]
    params = collect_params(text)
    # strip common non-parameter identifiers
    noise = {"data", "body", "params", "query", "headers", "config", "options", "payload", "req", "res"}
    params = [p for p in params if p.lower() not in noise and len(p) > 1]

    results = []
    for entry in official_params:
        official = set(entry["all_params"])
        required = set(entry["request_params"])  # approximation: treat request params as the formal set
        used = set(params)

        unknown = sorted(p for p in used if p not in official)
        missing = sorted(p for p in required if p not in used)
        typos = {}
        for p in unknown:
            guesses = likely_typo(p, sorted(official))
            if guesses:
                typos[p] = guesses

        if unknown or missing or typos:
            results.append({
                "endpoint": entry["title"],
                "method": entry["method"],
                "path": entry["path"],
                "url": entry["url"],
                "file": site["file"],
                "line": site["line"],
                "code": site["text"],
                "params_used": params,
                "unknown_params": unknown,
                "missing_required": missing,
                "likely_typos": typos,
            })
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="input", required=True, help="endpoints.json from extract_params.py")
    parser.add_argument("--scan", required=True, help="project directory to scan")
    parser.add_argument("--out", default="reports/param_verification.json", help="JSON report path")
    parser.add_argument("--md", default="", help="optional markdown summary path")
    parser.add_argument("--ext", action="append", default=[], help="extra file extension to scan (e.g. .py)")
    parser.add_argument("--skip-dir", action="append", default=[], help="extra directory to skip")
    args = parser.parse_args(argv)

    endpoints = load_endpoints(args.input)
    entries, by_path, by_slug = index_endpoints(endpoints)

    exts = set(DEFAULT_EXTS)
    exts.update(e if e.startswith(".") else "." + e for e in args.ext)
    skip_dirs = set(DEFAULT_SKIP_DIRS)
    skip_dirs.update(args.skip_dir)

    if not os.path.isdir(args.scan):
        print(f"error: scan directory not found: {args.scan}", file=sys.stderr)
        return 1

    sites = find_call_sites(args.scan, exts, skip_dirs)

    findings = []
    for site in sites:
        matched = endpoint_for_site(site["text"], by_path, by_slug, entries)
        for entry in matched:
            findings.extend(verify_site(site, [entry], by_path, by_slug))

    report = {
        "schema_version": "1.0",
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "source": args.input,
        "scan_dir": os.path.abspath(args.scan),
        "sites_scanned": len(sites),
        "findings": findings,
        "summary": {
            "unknown_params": sum(len(f["unknown_params"]) for f in findings),
            "missing_required": sum(len(f["missing_required"]) for f in findings),
            "likely_typos": sum(len(f["likely_typos"]) for f in findings),
            "endpoints_with_issues": len({f["path"] for f in findings}),
        },
    }

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)

    if args.md:
        md_dir = os.path.dirname(os.path.abspath(args.md))
        if md_dir:
            os.makedirs(md_dir, exist_ok=True)
        with open(args.md, "w", encoding="utf-8") as handle:
            handle.write(f"# Parameter Verification Report\n\n")
            handle.write(f"Generated: {report['generated_at']}  |  Scanned: `{args.scan}`  |  Sites: {report['sites_scanned']}\n\n")
            handle.write(f"## Summary\n\n")
            handle.write(f"- Findings: {len(findings)}\n")
            handle.write(f"- Unknown parameters: {report['summary']['unknown_params']}\n")
            handle.write(f"- Missing required parameters: {report['summary']['missing_required']}\n")
            handle.write(f"- Likely typos: {report['summary']['likely_typos']}\n")
            handle.write(f"- Endpoints with issues: {report['summary']['endpoints_with_issues']}\n\n")
            if findings:
                handle.write("## Findings\n\n")
                for f in findings:
                    handle.write(f"### {esc(f['endpoint'])} ({f['method']} {f['path']})\n\n")
                    handle.write(f"File: `{f['file']}` line {f['line']}\n\n")
                    handle.write(f"Code: `{esc(f['code'])}`\n\n")
                    if f["unknown_params"]:
                        handle.write(f"- Unknown params: {', '.join(f['unknown_params'])}\n")
                    if f["missing_required"]:
                        handle.write(f"- Missing required: {', '.join(f['missing_required'])}\n")
                    if f["likely_typos"]:
                        for p, guesses in f["likely_typos"].items():
                            handle.write(f"- Likely typo `{p}` → did you mean {', '.join(guesses)}?\n")
                    handle.write("\n")

    print(f"Wrote {args.out}: {len(findings)} findings across {len(sites)} call sites")
    if args.md:
        print(f"Wrote {args.md}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
