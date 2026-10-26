"""Check every DOI in library/references.tsv against Crossref.

Usage: python3 scripts/library_crossref.py  (run from data/eprp/)
Writes library/crossref_check.tsv. A row is `match` when Crossref resolves the DOI, the
normalised titles agree (similarity >= 0.85, or one contains the other) and the years differ by
at most one (print versus online year); otherwise `check`. Crossref's answer is recorded as
returned; nothing in references.tsv is changed.
"""

import csv
import difflib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

SRC, OUT = "library/references.tsv", "library/crossref_check.tsv"


def norm(t):
    t = re.sub(r"<[^>]+>", " ", t or "")
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def lookup(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=30) as r:
                return "ok", json.load(r)["message"]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return "not_found", None
            time.sleep(2 ** attempt)
        except Exception:
            time.sleep(2 ** attempt)
    return "error", None


with open(SRC, newline="") as f:
    refs = list(csv.DictReader(f, delimiter="\t"))

dois = [r["doi"].removeprefix("https://doi.org/") for r in refs]
with ThreadPoolExecutor(max_workers=4) as pool:
    answers = list(pool.map(lambda d: lookup(d) if d else ("no_doi", None), dois))

rows = []
for r, doi, (status, m) in zip(refs, dois, answers):
    ct = (m.get("title") or [""])[0] if m else ""
    ca = ((m.get("author") or [{}])[0].get("family", "") if m else "")
    cy = ((m.get("issued", {}).get("date-parts") or [[None]])[0][0] if m else None)
    a, b = norm(r["title"]), norm(ct)
    sim = difflib.SequenceMatcher(None, a, b).ratio() if a and b else 0.0
    contained = bool(a and b and (a in b or b in a))
    ydiff = abs(int(r["year"]) - cy) if (cy and r["year"].isdigit()) else ""
    ok = status == "ok" and (sim >= 0.85 or contained) and ydiff != "" and ydiff <= 1
    rows.append({
        "openalex_id": r["openalex_id"], "doi": doi, "crossref_status": status,
        "verdict": "match" if ok else "check", "title_similarity": f"{sim:.2f}",
        "year_openalex": r["year"], "year_crossref": cy or "", "year_diff": ydiff,
        "first_author_crossref": ca, "title_openalex": r["title"], "title_crossref": " ".join(ct.split()),
    })

with open(OUT, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
n = {v: sum(1 for x in rows if x["verdict"] == v) for v in ("match", "check")}
s = {v: sum(1 for x in rows if x["crossref_status"] == v) for v in ("ok", "not_found", "error", "no_doi")}
print(f"{len(rows)} references: {n}; crossref {s}")
