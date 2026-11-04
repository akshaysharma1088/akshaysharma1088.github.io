"""Set each sitemap <lastmod> to the date of the last commit that changed that page's content.

Run by the daily workflow and on every push to main, so Google sees fresh dates without
anyone editing sitemap.xml by hand.
"""
import re
import subprocess
import sys

SITEMAP = "sitemap.xml"
SOURCES = {  # page URL -> files whose changes count as a change to that page
    "https://akshaysharma1088.github.io/": ["index.html", "data.json", "posts.json"],
    "https://akshaysharma1088.github.io/projects.html": ["projects.html"],
}


def last_change(files):
    out = subprocess.run(["git", "log", "-1", "--format=%cs", "--", *files],
                         capture_output=True, text=True, check=True).stdout.strip()
    return out or None


def main():
    xml = open(SITEMAP, encoding="utf-8").read()
    new = xml
    for url, files in SOURCES.items():
        date = last_change(files)
        if not date:
            continue
        pattern = re.compile(r"(<loc>" + re.escape(url) + r"</loc>\s*<lastmod>)[^<]*(</lastmod>)")
        new = pattern.sub(lambda m: m.group(1) + date + m.group(2), new)
    if new != xml:
        open(SITEMAP, "w", encoding="utf-8").write(new)
        print("sitemap.xml updated")
    else:
        print("sitemap.xml already current")
    return 0


if __name__ == "__main__":
    sys.exit(main())
