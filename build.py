#!/usr/bin/env python3
"""Builds the static website of kleinod.studio.

Pages are written as HTML fragments in src/ (first lines: "title:" and "description:", then a
blank line, then the content). This script wraps them in the shared layout and writes the
finished pages where GitHub Pages serves them (the repository root). Markdown documentation
from the app repositories is converted with Pandoc.

Run:  python3 build.py
"""

import html
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
TYPECASE = Path.home() / "Development" / "Typecase"  # app repository next to this one

# source fragment -> published page
PAGES = {
    "index.html": "index.html",
    "typecase.html": "typecase/index.html",
    "typecase-templates.html": "typecase/templates/index.html",
    "imprint.html": "imprint/index.html",
    "privacy.html": "privacy/index.html",
    "404.html": "404.html",
}

LAYOUT = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta name="color-scheme" content="light dark">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="/" aria-label="kleinod.studio home">
      <img class="logo-light" src="/assets/kleinod-studio-logo-horizontal.svg" alt="kleinod.studio" width="230" height="34">
      <img class="logo-dark" src="/assets/kleinod-studio-logo-horizontal-dark.svg" alt="kleinod.studio" width="230" height="34">
    </a>
    <nav aria-label="Main">
      <a href="/typecase/">Typecase</a>
      <a href="https://github.com/kleinod-studio">GitHub</a>
    </nav>
  </div>
</header>
<main class="wrap">
{content}
</main>
<footer class="site-footer">
  <div class="wrap">
    <span>© 2026 Sascha Wübbena · kleinod.studio</span>
    <span><a href="/imprint/">Impressum</a> · <a href="/privacy/">Datenschutz</a></span>
  </div>
</footer>
</body>
</html>
"""


def read_fragment(path: Path) -> tuple[dict, str]:
    head, _, body = path.read_text(encoding="utf-8").partition("\n\n")
    meta = dict(line.split(":", 1) for line in head.splitlines() if ":" in line)
    return {k.strip(): v.strip() for k, v in meta.items()}, body


def templates_guide() -> None:
    """Typecase's template guide (docs/templates.md) as a page."""
    markdown = TYPECASE / "docs" / "templates.md"
    if not markdown.is_file():
        print(f"skipped: {markdown} not found")
        return
    body = subprocess.run(
        ["pandoc", "--from", "gfm", "--to", "html5", str(markdown)], check=True, capture_output=True, text=True
    ).stdout
    # The first heading becomes the page title; links into the repository point to GitHub.
    body = re.sub(r'href="(?!https?:|#|/)([^"]+)"', r'href="https://github.com/kleinod-studio/Typecase/blob/main/docs/\1"', body)
    (SRC / "typecase-templates.html").write_text(
        "title: Export templates · Typecase\n"
        "description: How Typecase export templates work and how to build your own.\n\n"
        f'<div class="prose">\n<p class="muted"><a href="/typecase/">Typecase</a> › Export templates</p>\n{body}</div>\n',
        encoding="utf-8",
    )


def main() -> None:
    templates_guide()
    for source, target in PAGES.items():
        meta, content = read_fragment(SRC / source)
        page = LAYOUT.format(
            lang=meta.get("lang", "en"),
            title=html.escape(meta.get("title", "kleinod.studio")),
            description=html.escape(meta.get("description", "")),
            content=content.rstrip(),
        )
        out = ROOT / target
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print("wrote", target)
    skill = TYPECASE / "dist" / "typecase-template.skill"
    if skill.is_file():
        shutil.copyfile(skill, ROOT / "downloads" / "typecase-template.skill")
        print("copied downloads/typecase-template.skill")


if __name__ == "__main__":
    main()
