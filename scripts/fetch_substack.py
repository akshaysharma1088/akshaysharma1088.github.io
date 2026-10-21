"""Fetch the latest Substack issues into posts.json for the website.

Run by .github/workflows/update-newsletter.yml once a day. Uses only the
Python standard library. If the feed cannot be read, posts.json is left as is.
"""
import email.utils
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEED = "https://akshaysharma10.substack.com/feed"
OUT = "posts.json"
KEEP = 5


def clean(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def main():
    try:
        req = urllib.request.Request(FEED, headers={"User-Agent": "akshaysharma1088.github.io site updater"})
        with urllib.request.urlopen(req, timeout=30) as r:
            root = ET.fromstring(r.read())
    except Exception as e:  # noqa: BLE001
        print(f"Feed not read, keeping existing {OUT}: {e}")
        return 0

    posts = []
    for item in root.iter("item"):
        title = clean(item.findtext("title"))
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        date = ""
        raw = item.findtext("pubDate")
        if raw:
            try:
                date = email.utils.parsedate_to_datetime(raw).date().isoformat()
            except (TypeError, ValueError):
                date = ""
        summary = clean(item.findtext("description"))
        if len(summary) > 180:
            summary = summary[:177].rsplit(" ", 1)[0] + "..."
        posts.append({"title": title, "url": link, "date": date, "summary": summary})
        if len(posts) >= KEEP:
            break

    if not posts:
        print("Feed had no posts, keeping existing file")
        return 0

    try:
        old = json.load(open(OUT, encoding="utf-8")).get("posts")
    except (OSError, ValueError):
        old = None
    if old == posts:
        print("No new posts")
        return 0

    data = {"updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "posts": posts}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {len(posts)} posts")
    return 0


if __name__ == "__main__":
    sys.exit(main())
