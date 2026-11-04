"""Keep page dates current for search engines.

- sitemap.xml: each <lastmod> = date of the last commit that changed that page's content.
- index.html: the ProfilePage "dateModified" = the same moment as a full ISO 8601 datetime with
  a time zone (Google rejects a bare date there).

Commits made by this script ("Update sitemap dates") are ignored, so it never chases its own
changes. Run by the daily workflow and on every push to main.
"""
import re
import subprocess
import sys

SITEMAP = "sitemap.xml"
SOURCES = {  # page URL -> files whose changes count as a change to that page
    "https://akshaysharma1088.github.io/": ["index.html", "data.json", "posts.json"],
    "https://akshaysharma1088.github.io/projects.html": ["projects.html"],
}


SELF = "^Update sitemap dates"


def last_change(files, fmt="%cs"):
    out = subprocess.run(["git", "log", "-1", f"--format={fmt}", "--invert-grep", f"--grep={SELF}",
                          "--", *files], capture_output=True, text=True, check=True).stdout.strip()
    return out or None


def update_profile_date():
    stamp = last_change(SOURCES["https://akshaysharma1088.github.io/"], fmt="%cI")
    if not stamp:
        return False
    html = open("index.html", encoding="utf-8").read()
    new = re.sub(r'("dateModified":\s*")[^"]*(")', lambda m: m.group(1) + stamp + m.group(2), html, count=1)
    if new != html:
        open("index.html", "w", encoding="utf-8").write(new)
        print("index.html dateModified updated")
        return True
    return False


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
    update_profile_date()
    return 0


if __name__ == "__main__":
    sys.exit(main())
