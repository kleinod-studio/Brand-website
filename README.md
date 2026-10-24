# kleinod.studio

Website of [kleinod.studio](https://kleinod.studio), served by GitHub Pages from this repository's root.

- Page sources: `src/*.html` (first lines `title:`, `description:`, optional `lang:`, then a blank line and the content)
- Build: `python3 build.py` wraps them in the shared layout, converts Typecase's `docs/templates.md` with Pandoc and copies the Typecase skill download. Commit the generated files.
- Brand assets and guidelines: `brand/` (`python3 brand/build.py` regenerates them)
- Preview locally: `python3 -m http.server` and open http://localhost:8000

No external fonts, scripts or trackers.
