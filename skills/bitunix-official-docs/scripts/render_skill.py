#!/usr/bin/env python3
"""
render_skill.py -- Build a verifying SKILL.md from an extract_params.json document.

Reads endpoints.json (produced by extract_params.py) and writes a markdown
SKILL.md whose every endpoint carries an endpoint index plus full markdown
parameter tables. Designed so any agent loading the skill can copy-paste a
parameter list and verify their code against the official documentation.

Usage:
  python3 render_skill.py --in endpoints.json --out skills/bitunix-endpoint-parameters/SKILL.md \
      --provider Bitunix --provider-base-url https://fapi.bitunix.com \
      --name bitunix-endpoint-parameters \
      --description "verify any Bitunix API call's parameters against the official docs"

Standard library only. Output is pure markdown — no external assets.
"""

from __future__ import annotations

import argparse
import datetime
import html
import json
import os
import re
import sys

BOOLEAN_MAP = {
    True: "yes",
    False: "no",
    None: "?",
}

TYPE_NORM = {
    "string": "string",
    "number": "number",
    "int": "number",
    "integer": "number",
    "int64": "number",
    "boolean": "boolean",
    "bool": "boolean",
    "float": "number",
    "array": "array",
    "list": "array",
    "object": "object",
    "json": "object",
}


def esc(text):
    return html.escape(text or "", quote=False).replace("|", "\\|")


def norm_type(raw):
    key = (raw or "").strip().lower()
    if not key:
        return "-"
    return TYPE_NORM.get(key, key)


def norm_required(raw):
    if raw is True:
        return "yes"
    if raw is False:
        return "no"
    text = (raw or "").strip().lower()
    return BOOLEAN_MAP.get(text, "?")


def anchor(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "endpoint"


def write_header(fh, name, description, provider, base_url, generated_at, source_count):
    fh.write(f"---\n")
    fh.write(f"name: {name}\n")
    fh.write(f"description: {description}\n")
    fh.write(f"provider: {provider}\n")
    fh.write(f"---\n\n")
    fh.write(f"# {provider} API Endpoint Parameter Reference\n\n")
    fh.write(f"Generated from official documentation on {generated_at}. ")
    fh.write(f"Base URL: `{base_url}`. Source pages: {source_count}.\n\n")
    fh.write(
        "Every section below lists an endpoint's HTTP method, path, rate limit, "
        "description, and every request / response / push parameter exactly as the "
        "official documentation defines it. Use it to verify any agent-generated code "
        "before you call the API: if a parameter name, type, or required-flag differs "
        "from this file, fix the code.\n\n"
    )
    fh.write("> Source: official docs. Parameter names, types, enum values, and required flags are taken verbatim; do not invent alternatives.\n\n")


def write_parameter_table(fh, rows, caption):
    fh.write(f"\n### {caption}\n\n")
    if not rows:
        fh.write("_No parameters documented._\n\n")
        return
    fh.write("| Parameter | Type | Required | Description |\n")
    fh.write("|---|---|---|---|\n")
    for row in rows:
        fh.write(
            "| {name} | {typ} | {req} | {desc} |\n".format(
                name=esc(row.get("name", "-")),
                typ=norm_type(row.get("type")),
                req=norm_required(row.get("required")),
                desc=esc(row.get("description", "-")),
            )
        )
    fh.write("\n")


def write_endpoint_section(fh, endpoint):
    """Render one endpoint's full parameter tables."""
    title = endpoint.get("title") or endpoint.get("url", "").split("/")[-1]
    label = endpoint.get("label") or title

    fh.write(f"## {esc(title)}\n\n")

    # Identity line
    method = endpoint.get("method") or "-"
    path = endpoint.get("path") or "-"
    doc_type = endpoint.get("doc_type") or "reference"
    rate = endpoint.get("rate_limit")
    rate_text = f" | Rate limit: `{rate}`" if rate else ""
    fh.write(f"**Type:** {doc_type} &nbsp;·&nbsp; **Method:** `{method}` &nbsp;·&nbsp; **Path:** `{path}`{rate_text}\n")
    if endpoint.get("description"):
        desc = esc(endpoint["description"]).replace("\n", "<br>")
        fh.write(f"\n{desc}\n\n")
    fh.write(f"Official doc: [{endpoint.get('url')}]({endpoint.get('url')})\n\n")

    write_parameter_table(fh, endpoint.get("request_params", []) or [], "Request Parameters")
    write_parameter_table(fh, endpoint.get("response_params", []) or [], "Response Parameters")
    write_parameter_table(fh, endpoint.get("push_params", []) or [], "Push Parameters")
    write_parameter_table(fh, endpoint.get("error_codes", []) or [], "Error Codes")
    fh.write("\n---\n\n")


def write_index(fh, endpoints):
    fh.write("## Endpoint Index\n\n")
    fh.write("| # | Endpoint | Type | Method | Path | Doc |\n")
    fh.write("|---|---|---|---|---|---|\n")
    for i, endpoint in enumerate(endpoints, 1):
        title = esc(endpoint.get("title") or endpoint.get("url", "").split("/")[-1])
        doc_type = endpoint.get("doc_type") or "reference"
        method = esc(endpoint.get("method") or "-")
        path = esc(endpoint.get("path") or "-")
        url = endpoint.get("url", "#")
        fh.write(f"| {i} | {title} | {doc_type} | {method} | {path} | [doc]({url}) |\n")
    fh.write("\n")


def write_failure_section(fh, failures):
    if not failures:
        return
    fh.write("## Source Pages That Could Not Be Extracted\n\n")
    fh.write("| URL | Error |\n")
    fh.write("|---|---|\n")
    for fail in failures:
        fh.write(f"| {esc(fail.get('url',''))} | {esc(fail.get('error',''))} |\n")
    fh.write("\n")


def build(input_path, output_path, provider, base_url, name, description):
    with open(input_path, "r", encoding="utf-8") as handle:
        document = json.load(handle)

    endpoints = document.get("endpoints", [])
    failures = document.get("errors", [])
    generated_at = document.get("generated_at") or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as fh:
        write_header(fh, name, description, provider, base_url, generated_at, len(endpoints))
        write_index(fh, endpoints)
        fh.write("## Endpoint Details\n\n")
        for endpoint in endpoints:
            if endpoint.get("error"):
                continue
            write_endpoint_section(fh, endpoint)
        write_failure_section(fh, failures)

    return output_path


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="input", required=True, help="endpoints.json from extract_params.py")
    parser.add_argument("--out", required=True, help="output SKILL.md path")
    parser.add_argument("--provider", default="Provider", help="provider display name")
    parser.add_argument("--provider-base-url", dest="base_url", default="", help="base URL shown in the skill")
    parser.add_argument("--name", default="api-endpoint-parameters", help="skill name written to YAML frontmatter")
    parser.add_argument("--description", default="Verify API call parameters against official documentation.", help="skill description")
    args = parser.parse_args(argv)
    path = build(args.input, args.out, args.provider, args.base_url, args.name, args.description)
    print(f"Wrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
