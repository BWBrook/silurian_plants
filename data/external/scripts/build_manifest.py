"""Merge the area manifests into MANIFEST.tsv and check them against the files on disk.

Usage: python3 scripts/build_manifest.py  (run from data/external/)
Areas are the top-level folders holding a MANIFEST.tsv (local/ and scripts/ excluded). For each
listed file it recomputes sha256 and data rows (parsed records minus header for .csv/.tsv); a
listed directory gets a file count and no hash. Declared values that disagree are reported, and
the recomputed values are written. Files on disk that no manifest lists are reported too.
"""

import csv
import hashlib
import sys
from pathlib import Path

FIELDS = ["path", "description", "source", "source_version", "licence", "script", "rows", "sha256", "extracted"]
IGNORE = {"README.md", "MANIFEST.tsv", ".gitignore", ".gitattributes", ".DS_Store"}

areas = sorted(p.name for p in Path(".").iterdir()
               if p.is_dir() and p.name not in {"local", "scripts"} and (p / "MANIFEST.tsv").exists())
rows, problems = [], []
for area in areas:
    with (Path(area) / "MANIFEST.tsv").open(newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            p = Path(r["path"])
            if p.is_dir():
                n = sum(1 for q in p.rglob("*") if q.is_file())
                r["rows"], r["sha256"] = f"{n} files", ""
            elif p.is_file():
                h = hashlib.sha256(p.read_bytes()).hexdigest()
                n = ""
                if p.suffix in {".csv", ".tsv"}:
                    with p.open(newline="", encoding="utf-8", errors="replace") as fh:
                        delim = "\t" if p.suffix == ".tsv" else ","
                        n = str(sum(1 for _ in csv.reader(fh, delimiter=delim)) - 1)
                for key, new in (("sha256", h), ("rows", n)):
                    old = (r.get(key) or "").removeprefix("sha256:")
                    if old and new and old != new:
                        problems.append(f"{p}: declared {key} {old} != {new}")
                r["sha256"], r["rows"] = h, n
            else:
                problems.append(f"listed but absent: {p}")
            rows.append({k: r.get(k, "") for k in FIELDS})

listed = {Path(r["path"]) for r in rows}
for q in sorted(Path(".").rglob("*")):
    if not q.is_file() or q.name in IGNORE or q.parts[0] == "scripts":
        continue
    if not any(q == p or p in q.parents for p in listed):
        problems.append(f"unlisted file: {q}")

with open("MANIFEST.tsv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
print(f"{len(rows)} entries from {len(areas)} areas ({', '.join(areas)}) -> MANIFEST.tsv")
for p in problems:
    print("CHECK:", p)
sys.exit(1 if problems else 0)
