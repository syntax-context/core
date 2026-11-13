"""Bring SYNTAX's notes from the editor (prayasabhinav.net/panel, the mount "SYNTAX · Notes") into site-notes/.

His words, 13 November 2026: "there is no syntax notes page - why? mount it in editor too". A note published in the
editor is kept on the home app's server; this copies each one into site-notes/<slug>.json, removes any the editor no
longer has, and prints "changed" when anything differs, so the caller rebuilds and deploys the site only then.
build.py makes /notes/ and /notes/<slug>/ from these files. Needs the notes key, kept outside this repository.
Run from this folder: python3 notes-pull.py
"""
import json
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "site-notes"
KEY = next(l.split("=", 1)[1].strip() for l in (HERE / "NOTES_SOURCE").read_text().splitlines() if l.startswith("NOTES_KEY="))
API = "<notes source>"


def get(path):
    req = urllib.request.Request(API + path, headers={"Authorization": "Bearer " + KEY})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


tree = get("/tree")
urls = [c["url"] for s in tree["sections"] for c in s.get("children", [])]
OUT.mkdir(exist_ok=True)
changed, keep = False, set()
for url in urls:
    page = get("/pages" + urllib.parse.quote(url))
    slug = url.rstrip("/").split("/")[-1]
    keep.add(slug + ".json")
    text = json.dumps({k: page.get(k) for k in ("title", "url", "text", "date", "updated")}, ensure_ascii=False, indent=1) + "\n"
    fp = OUT / (slug + ".json")
    if not fp.exists() or fp.read_text() != text:
        fp.write_text(text)
        changed = True
for fp in OUT.glob("*.json"):
    if fp.name not in keep:
        fp.unlink()
        changed = True
print("changed" if changed else "unchanged", len(keep), "notes")
