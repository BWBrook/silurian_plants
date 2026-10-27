#!/usr/bin/env python3
"""Write deposits/deposit_index.csv from the catalogue (WORKS), deposits/crossref_check.tsv and deposits/MANIFEST.tsv.

Run after deposits_build.py:  python3 -I deposits_index.py
Size and paths come from the files on disk, so the index cannot drift from the mirror.
"""
import csv
import json
import sys
from pathlib import Path

EXT = Path(__file__).resolve().parents[1]
DEP, LOC = EXT / "deposits", EXT / "local" / "deposits"
RAW = "/data/codex/silurian_plants/raw/deposits"
sys.path.insert(0, str(Path(__file__).parent))
from deposits_catalogue import CAT, WORKS  # noqa: E402

crossref = {r["key"]: r for r in csv.DictReader(open(DEP / "crossref_check.tsv"), delimiter="\t")}


def dir_stats(dep_id):
    size, files = 0, 0
    dirs = []
    for base in (DEP, LOC):
        d = base / dep_id
        if d.exists():
            dirs.append(d.relative_to(EXT).as_posix() + "/")
            for p in d.rglob("*"):
                if p.is_file() and p.name != "PROVENANCE.json":
                    size += p.stat().st_size
                    files += 1
    stamps = []
    for base in (DEP, LOC):
        pj = base / dep_id / "PROVENANCE.json"
        if pj.exists():
            for s in json.loads(pj.read_text()):
                stamps.append(f"{RAW}/{dep_id}/{s['stamp']}/")
            break
    return size, files, dirs, sorted(set(stamps))


cols = ["id", "role", "citation", "doi", "what_the_deposit_holds", "repository_and_record", "licence", "size_bytes", "files", "status",
        "timescale_basis", "mac_paths", "deep_server_paths", "note"]
rows = []
for w in WORKS:
    doi = ""
    if w.get("crossref"):
        c = crossref[w["crossref"]]
        doi = f"{c['doi_crossref']} (Crossref-checked 2026-10-27: {c['first_author']} {c['year']}, {c['container']})"
    elif w.get("doi"):
        doi = w["doi"]
    if w.get("data_doi"):
        doi += f"; data {w['data_doi']}"
    size = files = 0
    mac, deep = [], []
    for d in w["deposits"]:
        s, f, dirs, stamps = dir_stats(d)
        size += s
        files += f
        mac += dirs
        deep += stamps
    rows.append([w["key"], w["role"], w["citation"], doi, w["holds"], w["repo"], w["licence"], size or "", files or "", w["status"],
                 w["timescale"], ";".join(mac), ";".join(deep), w["note"]])

with open(DEP / "deposit_index.csv", "w", newline="") as f:
    wr = csv.writer(f, lineterminator="\n")
    wr.writerow(cols)
    wr.writerows(rows)
print(len(rows), "rows;", sum(1 for r in rows if r[1] == "target"), "targets")


# Keep the area manifest complete: list the files this step and the hand-written README add.
import hashlib  # noqa: E402

man = DEP / "MANIFEST.tsv"
with open(man, newline="") as f:
    old = list(csv.reader(f, delimiter="\t"))
head, body = old[0], old[1:]
own = {"deposits/crossref_check.tsv", "deposits/deposit_index.csv", "deposits/README.md"}
body = [r for r in body if r[0] not in own]
for rel, desc, src, script in [
    ("deposits/crossref_check.tsv", "Crossref record check of every DOI in the index: title, first author, year, container, publisher, licence URLs",
     "Crossref REST API, fetched 2026-10-27", "scripts/deposits_crossref_check.py"),
    ("deposits/deposit_index.csv", "One row per target, added or related work: citation, Crossref-checked DOI, what the deposit holds, repository and record, licence, size, status, timescale basis, Mac and deep-server paths, note",
     "this task", "scripts/deposits_index.py"),
    ("deposits/README.md", "What was found and not found, method, licences, timescale bases, caveats, what was not done", "this task", "hand-written"),
]:
    p = EXT / rel
    n = ""
    if p.suffix in (".csv", ".tsv"):
        with open(p, newline="", encoding="utf-8", errors="replace") as fh:
            n = str(sum(1 for _ in csv.reader(fh, delimiter="\t" if p.suffix == ".tsv" else ",")) - 1)
    body.append([rel, desc, src, "2026-10-27", "", script, n, hashlib.sha256(p.read_bytes()).hexdigest(), "2026-10-27"])
body.sort(key=lambda r: r[0])
with open(man, "w", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(head)
    w.writerows(body)
print("manifest rows:", len(body))
