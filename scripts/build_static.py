"""Copy data.json into index.html's static HTML, so search engines and visitors without JavaScript
see the same placards. Run after editing data.json:  python3 scripts/build_static.py
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
e = html.escape


def link(url, text):
    return f'<a href="{e(url)}">{e(text)}</a>' if url else f"<span>{e(text)}</span>"


def tag_class(status):
    if status == "Published":
        return "tag pub"
    if status == "Preprint":
        return "tag pre"
    if status == "Accepted":
        return "tag acc"
    if re.search("keynote|talk", status, re.I):
        return "tag inv"
    return "tag"


def card(c):
    out = [f'<article class="card{" wide" if c.get("wide") else ""}">', '<div class="card-top">',
           f'<span class="kind">{e(c["kind"])}</span>']
    if c.get("status"):
        out.append(f'<span class="{tag_class(c["status"])}">{e(c["status"])}</span>')
    out.append("</div>")
    mark = c.get("mark") or c["name"][:3].upper()
    logo_file = ROOT / c["logo"] if c.get("logo") else None
    if logo_file and logo_file.exists():
        logo = f'<img src="{e(c["logo"])}" alt="">'
    else:
        logo = f"<b>{e(mark)}</b>"
    out.append(f'<div class="head"><div class="logo">{logo}</div><div>')
    out.append(f'<h3>{link(c.get("url"), c["name"])}</h3>')
    if c.get("meta"):
        out.append(f'<p class="where">{e(c["meta"])}</p>')
    out.append("</div></div>")
    if c.get("items"):
        out.append("<ul>")
        for it in c["items"]:
            note = f'<span class="note">{e(it["note"])}</span>' if it.get("note") else ""
            out.append(f'<li>{link(it.get("url"), it["title"])}{note}</li>')
        out.append("</ul>")
    out.append("</article>")
    return "".join(out)


def bench(b):
    parts = [f'<a href="https://github.com/{e(b["repo"])}"><b>{e(b["name"])}</b><span>{e(b["summary"])}</span>',
             f'<code>github.com/{e(b["repo"])}</code>']
    if b.get("doi"):
        parts.append(f'<code>DOI {e(b["doi"])}</code>')
    if b.get("pypi"):
        parts.append(f'<span class="pypi">pip install {e(b["pypi"])}</span>')
    parts.append("</a>")
    return "".join(parts)


def main():
    d = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    blocks = {
        "runlog": "".join(f'<li><time>{e(r["date"])}</time><span>{e(r["text"])}</span></li>' for r in d["runlog"]),
        "research-cards": "".join(card(c) for c in d["research_cards"]),
        "bench": "".join(bench(b) for b in d["benchmarks"]),
        "outlet-cards": "".join(card(c) for c in d["outlet_cards"]),
        "speaking-cards": "".join(card(c) for c in d["speaking_cards"]),
        "service-cards": "".join(card(c) for c in d["service_cards"]),
    }
    page = (ROOT / "index.html").read_text(encoding="utf-8")
    for name, body in blocks.items():
        pattern = re.compile(rf"(<!-- gen:{name} -->).*?(<!-- /gen:{name} -->)", re.S)
        if not pattern.search(page):
            raise SystemExit(f"marker gen:{name} not found in index.html")
        page = pattern.sub(lambda m: m.group(1) + body + m.group(2), page)
    (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("index.html updated from data.json")


if __name__ == "__main__":
    main()
