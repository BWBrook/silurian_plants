"""Export the first pages of held and quarantined PDFs as text excerpts for the Codex identity checks.

Usage (on deep-server, from _tools/): python3 library_text_export.py [--pages 2] [--quarantine-pages 3]
Writes STORE/_build/identity_excerpts.json (accepted copies; scans without a text layer are OCR'd for the first pages) and quarantine_excerpts.json
(quarantine/*.pdf of the fetched subsets). Items are {id, text}; text is `pdftotext -l N` output cut to 6,000 characters.
Copies under tdm/ are never read (the folder does not exist when TDM routes are off).
"""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import library as L  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--store", type=Path, default=Path("/data/codex/silurian_plants/library"))
ap.add_argument("--pages", type=int, default=2)
ap.add_argument("--quarantine-pages", type=int, default=3)
a = ap.parse_args()
store = a.store


def head(path, pages):
    r = subprocess.run(["pdftotext", "-q", "-l", str(pages), "-enc", "UTF-8", str(path), "-"], capture_output=True, timeout=120)
    text = r.stdout.decode("utf-8", "replace") if r.returncode == 0 else ""
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()[:6000]


def ocr_head(path, pages):
    """First pages of a scan without a text layer, by pdftoppm + tesseract (used only for the identity check)."""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-r", "150", "-png", "-f", "1", "-l", str(pages), str(path), f"{tmp}/p"], capture_output=True, timeout=300)
        text = ""
        for img in sorted(Path(tmp).glob("p*.png")):
            r = subprocess.run(["tesseract", str(img), "-", "-l", "eng"], capture_output=True, timeout=300)
            text += r.stdout.decode("utf-8", "replace") + "\n\n"
    return re.sub(r"[ \t]+", " ", re.sub(r"\n{3,}", "\n\n", text)).strip()[:6000]


latest = {}
for r in L.read_tsv(store / "manifest.tsv"):
    latest[r["openalex_id"]] = r
held = [{"id": w, "text": head(store / r["path"], a.pages) if r["status"] == "ok" else "[OCR of the first pages; the PDF has no text layer]\n" + ocr_head(store / r["path"], a.pages)}
        for w, r in sorted(latest.items())
        if r["status"] in ("ok", "no_text") and not r["path"].startswith("tdm/") and (store / r["path"]).exists()]
(store / "_build" / "identity_excerpts.json").write_text(json.dumps(held, ensure_ascii=False))
q = []
for p in sorted((store / "quarantine").glob("W*__*.pdf")):
    q.append({"id": p.name.split("__")[0] + "|" + p.stem.split("__")[1], "text": head(p, a.quarantine_pages)})
(store / "_build" / "quarantine_excerpts.json").write_text(json.dumps(q, ensure_ascii=False))
print(len(held), "accepted excerpts;", len(q), "quarantine excerpts;", sum(1 for x in held if len(x["text"]) < 200), "accepted with <200 chars")
