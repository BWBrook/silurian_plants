#!/usr/bin/env python3
"""Write library/MANIFEST.tsv for the silurian_plants library extraction (stdlib only).

Run from data/eprp/scripts/ after library_assemble.py. Paths are relative to data/eprp/.
"""
import csv
import hashlib
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
EXTRACTED = "2026-10-26"
SRC = "EPRP resources/library/works.tsv; OpenAlex records and open texts in deep-server:/data/paleodata/library"
VER = "eprp@ac42dfb; store snapshot 2026-10-25 (search.sqlite built 2026-10-25 20:11)"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def nrows(path):
    with open(path, encoding="utf-8") as fh:
        return sum(1 for _ in fh) - 1


def main():
    rows = []
    ref = os.path.join(ROOT, "library", "references.tsv")
    out = os.path.join(ROOT, "library", "screened_out.tsv")
    rows.append(["library/references.tsv", "Kept works, one row per work: set, theme, found_by, EPRP tiers and questions, in_project, screen_note",
                 SRC, VER, "OpenAlex metadata CC0", "scripts/library_assemble.py", nrows(ref), sha(ref), EXTRACTED])
    rows.append(["library/screened_out.tsv", "Dropped candidates with a one-phrase reason, how decided and whether the title was read",
                 SRC, VER, "OpenAlex metadata CC0", "scripts/library_assemble.py", nrows(out), sha(out), EXTRACTED])
    rd = os.path.join(ROOT, "library", "README.md")
    rows.append(["library/README.md", "What this is, store state, routes and queries, screen, counts, limits and gaps, reproduction",
                 "this extraction", "", "project documentation", "scripts/library_assemble.py (generated)", "", sha(rd), EXTRACTED])
    tdir = os.path.join(ROOT, "local", "library", "text")
    files = sorted(f for f in os.listdir(tdir) if f.endswith(".txt"))
    h = hashlib.sha256()
    for f in files:
        h.update((f + " " + sha(os.path.join(tdir, f)) + "\n").encode())
    rows.append(["local/library/text/", "Open full texts (pdftotext output) of kept works; gitignored; one file per openalex_id; hash is of the sorted per-file hashes",
                 "deep-server:/data/paleodata/library/text/", VER,
                 "per-work open access; local copy only", "scripts/library_run.sh (rsync)", len(files), h.hexdigest(), EXTRACTED])
    for name, d, kind in (("candidates.tsv", "Candidates from all routes (7,959): evidence flags and routes per work; regenerate with library_run.sh", "tsv"),
                          ("fts_hits.tsv", "Every library.py search hit: work, query, matched part, rank", "tsv"),
                          ("texts_to_copy.txt", "Kept works with an open text file in the store", "txt"),
                          ("stats.json", "Counts behind the README", "json")):
        p = os.path.join(ROOT, "local", "library", "work", name)
        rows.append(["local/library/work/" + name, d, "this extraction (library_candidates.py / library_assemble.py)", VER, "OpenAlex metadata CC0; gitignored",
                     "scripts/library_run.sh", nrows(p) if kind == "tsv" else "", sha(p), EXTRACTED])
    scripts = [
        ("library_features.py", "Reads works.tsv and OpenAlex records into one JSON line per work (abstract, keywords, concepts, authors)"),
        ("library_queries.py", "Search vocabulary: 369 library.py FTS queries"),
        ("library_candidates.py", "Candidate routes (patterns, queries, topics, authors, venues, text density) over all works"),
        ("library_assemble.py", "Applies the screen, cross-checks the project, writes references, screened_out and README"),
        ("library_manifest.py", "Writes this manifest"),
        ("library_run.sh", "Driver for the whole extraction"),
    ]
    for name, d in scripts:
        p = os.path.join(HERE, name)
        rows.append(["scripts/" + name, d, "this extraction", "", "project code", "", "", sha(p), EXTRACTED])
    for name, d in (("library_decisions.tsv", "Manual screen: keep or drop per work, with set, theme, note and title"),
                    ("library_screen_read.txt", "Candidates whose titles were read in the screen")):
        p = os.path.join(HERE, name)
        rows.append(["scripts/" + name, d, "this extraction (screen decisions by Claude Sonnet 5.5)", "", "project documentation", "hand-written screen",
                     nrows(p) if name.endswith(".tsv") else sum(1 for _ in open(p)), sha(p), EXTRACTED])
    with open(os.path.join(ROOT, "library", "MANIFEST.tsv"), "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["path", "description", "source", "source_version", "licence", "script", "rows", "sha256", "extracted"])
        w.writerows(rows)
    print(len(rows), "rows")


if __name__ == "__main__":
    main()
