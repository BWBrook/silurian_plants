"""Check MVD-B extraction outputs: verbatim taxa, coverage, and agreement between two runs.

    python3 verify.py <papers.csv> <out_dir> [suffix_a suffix_b]
"""

import csv
import json
import re
import sys
from pathlib import Path


def norm(s):
    s = re.sub(r"-\s*\n\s*", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def load(path):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, json.JSONDecodeError):
        return None


def verbatim_share(result, text):
    taxa = [o["taxon_as_reported"] for a in result["items"] for o in a["occurrences"]]
    if not taxa:
        return 0, 0
    t = norm(text).replace(" ", "")
    found = 0
    for a in result["items"]:
        for o in a["occurrences"]:
            x, g = norm(o["taxon_as_reported"]), norm(o["genus"])
            words = [w for w in re.findall(r"[a-z][a-z-]{2,}", x) if w != g]
            epithet = words[-1] if words else ""
            variants = {x.replace(" ", "")[:40]}
            if g and epithet:
                variants |= {(g + epithet), (g[0] + "." + epithet), (g + "?" + epithet), (g[0] + ".?" + epithet)}
            found += any(v in t for v in variants)
    return found, len(taxa)


def genera(result):
    return {o["genus"].strip().lower() for a in result["items"] for o in a["occurrences"] if o["genus"].strip()}


def main(papers_csv, out_dir, *suffixes):
    papers = {r["openalex_id"]: r for r in csv.DictReader(open(papers_csv))}
    suffixes = suffixes or ("terra", "sol")
    for pid, p in papers.items():
        runs = {s: load(Path(out_dir) / f"{pid}_{s}.json") for s in suffixes}
        if not any(runs.values()):
            continue
        text = Path(p["text"]).read_text(encoding="utf-8", errors="replace")
        cells = []
        for s, r in runs.items():
            if r is None:
                cells.append(f"{s}: missing")
                continue
            found, n = verbatim_share(r, text)
            cells.append(f"{s}: {len(r['items'])} asm, {n} occ, verbatim {found}/{n}")
        if len(suffixes) == 2 and all(runs.values()):
            a, b = (genera(runs[s]) for s in suffixes)
            j = len(a & b) / max(1, len(a | b))
            cells.append(f"genus Jaccard {j:.2f} (only {suffixes[0]}: {sorted(a - b)[:4]}; only {suffixes[1]}: {sorted(b - a)[:4]})")
        print(pid, "|", " | ".join(cells))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    main(*sys.argv[1:])
