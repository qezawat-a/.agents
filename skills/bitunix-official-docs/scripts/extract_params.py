#!/usr/bin/env python3
"""
extract_params.py -- Extract API endpoint parameters from official HTML documentation.

Reads a list of documentation URLs (or discovers them from an index page), fetches
each page, and extracts the HTTP method, path, and every parameter table into a
single JSON document that `render_skill.py` turns into markdown tables and
`verify_params.py` checks project code against.

Standard library only. Raw HTML is cached so re-runs are offline and cheap.

Usage:
  # From a URL list file (one URL per line, '#' comments allowed)
  python3 extract_params.py --urls endpoints.txt --out endpoints.json

  # Discover every doc page linked from an index page
  python3 extract_params.py --discover https://example.com/api-docs/ \
      --discover-prefix /api-docs/ --out endpoints.json

  # Ad-hoc URLs
  python3 extract_params.py --url https://a.example/doc.html \
      --url https://b.example/doc.html --out endpoints.json
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser

SCHEMA_VERSION = "1.0"

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}
BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "br", "dd", "div", "dl",
    "dt", "fieldset", "figcaption", "figure", "footer", "h1", "h2", "h3",
    "h4", "h5", "h6", "header", "hr", "li", "main", "nav", "ol", "p", "pre",
    "section", "table", "tbody", "td", "tfoot", "th", "thead", "tr", "ul",
}

HEADER_HINTS = {
    "parameter", "parameter name", "name", "type", "required", "description",
    "default", "example", "remark", "note", "comment", "field", "property",
    "key", "value", "errcode", "errorcode", "error code", "httpstatuscode",
    "http status code", "mandatory", "optional", "meaning", "range", "unit",
}

TRUE_VALUES = {"true", "yes", "y", "required", "mandatory", "1", "√", "✓", "✔", "必填"}
FALSE_VALUES = {"false", "no", "n", "optional", "0", "-", "—", "nil", "null", "选填"}


# --------------------------------------------------------------------------
# Minimal DOM
# --------------------------------------------------------------------------

class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs=None, parent=None):
        self.tag = tag
        self.attrs = attrs or {}
        self.children = []
        self.parent = parent

    def classes(self):
        return (self.attrs.get("class") or "").split()

    def __repr__(self):  # pragma: no cover - debugging aid
        return f"<Node {self.tag} children={len(self.children)}>"


class DOMBuilder(HTMLParser):
    """Builds a small DOM tree from an HTML string."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.stack[-1])
        self.stack[-1].children.append(node)
        if tag not in VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        node = Node(tag, {k: (v if v is not None else "") for k, v in attrs}, self.stack[-1])
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def find_all(node, pred):
    out = []
    for child in node.children:
        if isinstance(child, Node):
            if pred(child):
                out.append(child)
            out.extend(find_all(child, pred))
    return out


def find_first(node, pred):
    for child in node.children:
        if isinstance(child, Node):
            if pred(child):
                return child
            found = find_first(child, pred)
            if found is not None:
                return found
    return None


def norm_ws(text):
    return re.sub(r"\s+", " ", text or "").strip()


def inline_text(node):
    """Text of a node with block boundaries collapsed to single spaces."""
    parts = []

    def rec(n):
        for child in n.children:
            if isinstance(child, str):
                parts.append(child)
            else:
                if child.tag in BLOCK_TAGS:
                    parts.append(" ")
                rec(child)
                if child.tag in BLOCK_TAGS:
                    parts.append(" ")

    rec(node)
    return norm_ws("".join(parts))


def cell_text(node):
    """Text of a table cell, preserving line structure from <br> and <p>."""
    parts = []

    def rec(n):
        for child in n.children:
            if isinstance(child, str):
                parts.append(child)
            else:
                if child.tag == "br":
                    parts.append("\n")
                elif child.tag in BLOCK_TAGS:
                    parts.append("\n")
                rec(child)
                if child.tag in BLOCK_TAGS and child.tag != "br":
                    parts.append("\n")

    rec(node)
    text = "".join(parts).replace("​", "")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def content_root(dom):
    """Return the node holding the main documentation body."""
    candidates = [
        lambda n: "vp-doc" in n.classes(),
        lambda n: n.tag == "main",
        lambda n: n.tag == "article",
        lambda n: "doc-content" in n.classes(),
        lambda n: n.tag == "body",
    ]
    for pred in candidates:
        found = find_first(dom, pred)
        if found is not None:
            return found
    return dom.root


def iter_events(node):
    """Yield document-order events: headings, tables, paragraphs, list items, code."""
    for child in node.children:
        if isinstance(child, str):
            continue
        if child.tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            yield ("heading", int(child.tag[1]), child.attrs.get("id", ""), inline_text(child))
        elif child.tag == "table":
            yield ("table", child)
        elif child.tag == "p":
            yield ("p", child)
        elif child.tag == "li":
            yield ("li", child)
        elif child.tag == "pre":
            yield ("pre", child)
        else:
            yield from iter_events(child)


# --------------------------------------------------------------------------
# Table parsing
# --------------------------------------------------------------------------

def is_header_row(cells):
    low = [c.lower().strip() for c in cells]
    if any("parameter" in c for c in low):
        return True
    hits = sum(1 for c in low if c in HEADER_HINTS)
    return hits >= 2


def map_columns(header):
    idx = {}
    for i, raw in enumerate(header):
        key = norm_ws(raw).lower()
        if "parameter" in key or key in ("field", "name", "property", "key", "attr"):
            idx.setdefault("name", i)
        elif "type" in key:
            idx.setdefault("type", i)
        elif "required" in key or key in ("mandatory", "optional"):
            idx.setdefault("required", i)
        elif "description" in key or key in ("remark", "note", "comment", "meaning", "detail"):
            idx.setdefault("description", i)
        elif "default" in key:
            idx.setdefault("default", i)
        elif "example" in key:
            idx.setdefault("example", i)
        elif "error" in key and "code" in key:
            idx.setdefault("code", i)
        elif "httpstatus" in key:
            idx.setdefault("http_status", i)
        else:
            idx.setdefault("extra", i)
    if "name" not in idx and header:
        # Tables such as error-code listings key on the first column.
        idx["name"] = 0
    return idx


def parse_required(value):
    text = norm_ws(value).lower()
    if text in TRUE_VALUES:
        return True
    if text in FALSE_VALUES:
        return False
    return None


def parse_table(table_node):
    """Return {'headers': [...], 'rows': [ {col: value}, ... ]}."""
    header = None
    body_rows = []
    for tr in find_all(table_node, lambda n: n.tag == "tr"):
        cells = []
        for cell in tr.children:
            if isinstance(cell, Node) and cell.tag in ("td", "th"):
                cells.append(cell_text(cell))
        if not cells:
            continue
        if header is None and is_header_row(cells):
            header = cells
        else:
            body_rows.append(cells)
    if header is None:
        return {"headers": [], "rows": []}
    idx = map_columns(header)
    rows = []
    for cells in body_rows:
        row = {}
        for col, i in idx.items():
            row[col] = cells[i] if i < len(cells) else ""
        raw_name = norm_ws(row.get("name", ""))
        if not raw_name:
            continue
        depth = len(raw_name) - len(raw_name.lstrip("> "))
        name = raw_name.lstrip("> ").strip()
        row["name"] = name
        row["raw_name"] = raw_name
        row["depth"] = depth
        row["nested"] = depth > 0
        row["required"] = parse_required(row.get("required", ""))
        rows.append(row)
    return {"headers": header, "rows": rows}


def table_kind(section_id, section_text, headers):
    """Classify a table by the heading above it, falling back to its headers."""
    blob = f"{section_id} {section_text}".lower()
    if "request" in blob or "body" in blob or "query" in blob or "input" in blob:
        return "request"
    if "response" in blob or "result" in blob or "reply" in blob or "output" in blob:
        return "response"
    if "push" in blob or "subscribe" in blob or "message" in blob or "event" in blob:
        return "push"
    low = [norm_ws(h).lower() for h in headers]
    if any("errorcode" in h or h == "error code" for h in low):
        return "error_code"
    if "required" in low:
        return "request"
    if any("parameter" in h for h in low):
        return "response"
    return "other"


# --------------------------------------------------------------------------
# Page extraction
# --------------------------------------------------------------------------

METHOD_RE = re.compile(r"\b(GET|POST|PUT|DELETE|PATCH)\b\s*[:\-]?\s*(/?[A-Za-z0-9_./{}:%\-]+)")
RATE_RE = re.compile(r"rate\s*limit\s*[:\-]?\s*([^\n]+)", re.IGNORECASE)


def split_url_path(raw):
    raw = norm_ws(raw).rstrip(".,;")
    match = re.match(r"^(https?://[^/\s]+)(/.*)?$", raw)
    if match:
        return match.group(1), match.group(2) or "/"
    return None, raw


def find_method_path(texts):
    """Find the first 'METHOD /path' occurrence, preferring list items."""
    for text in texts:
        match = METHOD_RE.search(text or "")
        if match:
            base, path = split_url_path(match.group(2))
            return match.group(1).upper(), path, base
    return None, None, None


def title_from_url(url):
    """Humanise the last path segment of a documentation URL."""
    path = urllib.parse.urlparse(url).path
    slug = re.sub(r"\.(html?|php|aspx?)$", "", path.rstrip("/").split("/")[-1])
    slug = urllib.parse.unquote(slug)
    slug = re.sub(r"[_%]+", " ", slug)
    slug = re.sub(r"[-]+", " ", slug)
    slug = norm_ws(slug)
    return slug.title() if slug else None


def extract_page(html, url):
    """Extract one documentation page into an endpoint record."""
    dom = DOMBuilder()
    try:
        dom.feed(html)
        dom.close()
    except Exception as exc:  # pragma: no cover - malformed markup
        return {"url": url, "error": f"parse failed: {exc}"}

    root = content_root(dom.root)

    title = None
    h1 = find_first(root, lambda n: n.tag == "h1")
    if h1 is not None:
        title = inline_text(h1).replace("​", "").strip() or None
    if not title:
        doc_title = find_first(dom.root, lambda n: n.tag == "title")
        candidate = inline_text(doc_title).replace("​", "").strip() if doc_title is not None else ""
        # Site-wide generic titles ("OpenApi | Bitunix") are worse than the URL slug.
        if candidate and len(candidate.split("|")[0].split("｜")[0].strip()) > 2 and "openapi" not in candidate.lower():
            title = candidate
        else:
            title = title_from_url(url)

    section_id = ""
    section_text = ""
    sections = []
    tables = []
    li_texts = []
    pre_texts = []
    paragraphs = []
    current_section = None

    for event in iter_events(root):
        kind = event[0]
        if kind == "heading":
            _, level, hid, text = event
            section_id = hid or norm_ws(text).lower().replace(" ", "-")
            section_text = text
            current_section = {"id": section_id, "heading": text, "level": level, "text": [], "examples": []}
            sections.append(current_section)
        elif kind == "table":
            parsed = parse_table(event[1])
            if parsed["headers"]:
                parsed["kind"] = table_kind(section_id, section_text, parsed["headers"])
                parsed["section"] = section_text
                tables.append(parsed)
        elif kind == "li":
            text = inline_text(event[1])
            li_texts.append(text)
            if current_section is not None:
                current_section["text"].append(text)
        elif kind == "p":
            text = inline_text(event[1])
            paragraphs.append(text)
            if current_section is not None:
                current_section["text"].append(text)
        elif kind == "pre":
            text = event[1].children and "".join(
                c if isinstance(c, str) else inline_text(c) for c in event[1].children
            ) or ""
            text = text.replace("​", "")
            pre_texts.append(text)
            if current_section is not None:
                current_section["examples"].append(text)

    method, path, base_url = find_method_path(li_texts + pre_texts)
    if method is None:
        method, path, base_url = find_method_path(paragraphs)

    rate_limit = None
    for text in paragraphs:
        match = RATE_RE.search(text)
        if match:
            rate_limit = norm_ws(match.group(1))
            break

    description = None
    for sec in sections:
        blob = f"{sec['id']} {sec['heading']}".lower()
        if any(word in blob for word in ("description", "overview", "introduction", "summary")):
            body = [t for t in sec["text"] if t and not RATE_RE.search(t)]
            if body:
                description = "\n\n".join(body)
            break
    if description is None and sections:
        body = [t for t in sections[0]["text"] if t and not RATE_RE.search(t)]
        description = "\n\n".join(body) if body else None

    request_params = []
    response_params = []
    push_params = []
    error_rows = []
    other_tables = []
    for tbl in tables:
        kind = tbl["kind"]
        if kind == "request":
            request_params.extend(tbl["rows"])
        elif kind == "response":
            response_params.extend(tbl["rows"])
        elif kind == "push":
            push_params.extend(tbl["rows"])
        elif kind == "error_code":
            error_rows.extend(tbl["rows"])
        else:
            other_tables.append(tbl)

    lowered = f"{url} {title or ''}".lower()
    if error_rows and not request_params and not response_params:
        doc_type = "error_code"
    elif push_params or "websocket" in lowered or "channel" in lowered:
        doc_type = "ws"
    elif method and path:
        doc_type = "rest"
    elif tables:
        doc_type = "reference"
    else:
        doc_type = "article"

    record = {
        "url": url,
        "title": title,
        "doc_type": doc_type,
        "method": method,
        "path": path,
        "base_url": base_url,
        "rate_limit": rate_limit,
        "description": description,
        "request_params": request_params,
        "response_params": response_params,
        "push_params": push_params,
        "error_codes": error_rows,
        "extra_tables": other_tables,
        "examples": [t for t in pre_texts if t.strip()],
        "sections": [
            {"id": s["id"], "heading": s["heading"], "level": s["level"],
             "text": "\n\n".join(t for t in s["text"] if t),
             "examples": s["examples"]}
            for s in sections if s["text"] or s["examples"]
        ],
    }
    if not tables and not description:
        record["error"] = "no parameter tables or description found"
    return record


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------

def cache_path(cache_dir, url):
    digest = hashlib.sha1(url.encode("utf-8")).hexdigest()
    return os.path.join(cache_dir, digest + ".html")


def decode_body(raw, content_type):
    match = re.search(r"charset=([\w\-]+)", content_type or "", re.IGNORECASE)
    encodings = []
    if match:
        encodings.append(match.group(1))
    encodings.extend(["utf-8", "gb18030", "latin-1"])
    for enc in encodings:
        try:
            return raw.decode(enc)
        except (LookupError, UnicodeDecodeError):
            continue
    return raw.decode("utf-8", errors="replace")


def fetch(url, timeout, retries, cache_dir, offline, user_agent):
    """Fetch a URL with caching and retries. Returns (html, from_cache)."""
    path = cache_path(cache_dir, url)
    if offline:
        if not os.path.exists(path):
            raise RuntimeError(f"offline and not cached: {url}")
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read(), True
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            return handle.read(), True

    last_error = None
    for attempt in range(retries + 1):
        try:
            request = urllib.request.Request(
                url,
                headers={
                    "User-Agent": user_agent,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                },
            )
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read()
                html = decode_body(raw, response.headers.get("Content-Type", ""))
            os.makedirs(cache_dir, exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(html)
            return html, False
        except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(min(2 ** attempt, 8))
    raise RuntimeError(f"fetch failed: {url}: {last_error}")


def discover_urls(index_url, prefix, same_host_only, timeout, retries, cache_dir, offline, user_agent):
    """Harvest documentation page links from an index page."""
    html, _ = fetch(index_url, timeout, retries, cache_dir, offline, user_agent)
    dom = DOMBuilder()
    dom.feed(html)
    dom.close()
    base_host = urllib.parse.urlparse(index_url).netloc
    seen = []
    for anchor in find_all(dom.root, lambda n: n.tag == "a"):
        href = anchor.attrs.get("href")
        if not href or href.startswith(("#", "javascript:", "mailto:")):
            continue
        absolute = urllib.parse.urljoin(index_url, href)
        parsed = urllib.parse.urlparse(absolute)
        if parsed.scheme not in ("http", "https"):
            continue
        if same_host_only and parsed.netloc != base_host:
            continue
        if prefix and not parsed.path.startswith(prefix):
            continue
        if not re.search(r"\.(html?|php|aspx?)$", parsed.path, re.IGNORECASE):
            continue
        clean = absolute.split("#")[0]
        if clean != index_url and clean not in seen:
            seen.append(clean)
    return seen


# --------------------------------------------------------------------------
# Input handling
# --------------------------------------------------------------------------

def parse_url_file(path):
    """Read a URL list file. Lines may be 'URL', 'NAME=URL', or '#' comments."""
    urls = []
    labels = {}
    with open(path, "r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            label = None
            if "=" in line and not line.lower().startswith(("http://", "https://")):
                label, line = line.split("=", 1)
                label = label.strip()
                line = line.strip().strip('"').strip("'")
            if not line.lower().startswith(("http://", "https://")):
                continue
            urls.append(line)
            if label:
                labels[line] = label
    return urls, labels


def build_arg_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--urls", help="File with one documentation URL per line")
    source.add_argument("--discover", help="Index page to harvest documentation links from")
    source.add_argument("--url", action="append", default=[], help="Documentation URL (repeatable)")
    parser.add_argument("--discover-prefix", default="", help="Only keep discovered URLs whose path starts with this")
    parser.add_argument("--discover-any-host", action="store_true", help="Allow discovered links on other hosts")
    parser.add_argument("--out", default="endpoints.json", help="Output JSON path")
    parser.add_argument("--provider", default="", help="Provider name recorded in the JSON")
    parser.add_argument("--base-url", default="", help="Override the base URL recorded in the JSON")
    parser.add_argument("--cache-dir", default=".cache/api-docs", help="Raw HTML cache directory")
    parser.add_argument("--no-cache", action="store_true", help="Ignore cached HTML and refetch")
    parser.add_argument("--offline", action="store_true", help="Use only cached HTML; fail if missing")
    parser.add_argument("--timeout", type=int, default=45)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--delay", type=float, default=0.4, help="Seconds between fetches")
    parser.add_argument("--user-agent", default="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0 Safari/537.36")
    parser.add_argument("--quiet", action="store_true")
    return parser


def main(argv=None):
    args = build_arg_parser().parse_args(argv)

    cache_dir = args.cache_dir
    if args.no_cache:
        cache_dir = cache_dir + ".tmp"

    labels = {}
    if args.urls:
        urls, labels = parse_url_file(args.urls)
    elif args.discover:
        urls = discover_urls(
            args.discover, args.discover_prefix, not args.discover_any_host,
            args.timeout, args.retries, cache_dir, args.offline, args.user_agent,
        )
        if not args.quiet:
            print(f"[discover] {len(urls)} documentation pages found", file=sys.stderr)
    else:
        urls = list(args.url)

    if not urls:
        print("error: no URLs to process", file=sys.stderr)
        return 1

    endpoints = []
    errors = []
    seen = set()
    for index, url in enumerate(urls, 1):
        if url in seen:
            continue
        seen.add(url)
        try:
            html, cached = fetch(url, args.timeout, args.retries, cache_dir, args.offline, args.user_agent)
        except RuntimeError as exc:
            errors.append({"url": url, "error": str(exc)})
            if not args.quiet:
                print(f"[{index}/{len(urls)}] FAILED {url}", file=sys.stderr)
            continue
        record = extract_page(html, url)
        if labels.get(url):
            record["label"] = labels[url]
        record["from_cache"] = cached
        endpoints.append(record)
        if not args.quiet:
            counts = (
                f"req={len(record.get('request_params', []))} "
                f"resp={len(record.get('response_params', []))} "
                f"push={len(record.get('push_params', []))}"
            )
            print(f"[{index}/{len(urls)}] {record.get('method') or '--'} {record.get('path') or record.get('doc_type')} ({counts})", file=sys.stderr)
        if args.delay and index < len(urls):
            time.sleep(args.delay)

    base_url = args.base_url
    if not base_url:
        for record in endpoints:
            if record.get("base_url"):
                base_url = record["base_url"]
                break

    document = {
        "schema_version": SCHEMA_VERSION,
        "provider": args.provider,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "base_url": base_url,
        "source_urls": urls,
        "endpoints": endpoints,
        "errors": errors,
    }

    out_dir = os.path.dirname(os.path.abspath(args.out))
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(document, handle, indent=2, ensure_ascii=False)

    if not args.quiet:
        print(f"\nWrote {args.out}: {len(endpoints)} pages, {len(errors)} failures", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
