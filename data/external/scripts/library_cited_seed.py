"""Collect every DOI cited in taxa/*.md and docs/*.md into the library seed tier `cited`.

Usage: python3 scripts/library_cited_seed.py [--out DIR]   (run from data/external/; no network)

DOI_RE and clean_doi are the project's own rule from tools/cards.py. They are copied here and checked
against that file's source on every run, so a change to the rule stops this script instead of drifting.
Writes DIR/cited.tsv (the seed: doi, files) for library.py's `resolve`, one row per distinct DOI.
Default DIR is library/seeds/; copy cited.tsv to deep-server:.../library/_tools/seeds/.
"""

import argparse
import csv
import inspect
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]

DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"]+")


def clean_doi(raw):
    """Strip trailing prose punctuation and unbalanced closing brackets (DOIs may contain both)."""
    doi = raw.rstrip(".,;:'")
    for opener, closer in ("()", "[]", "<>"):
        while doi.endswith(closer) and doi.count(closer) > doi.count(opener):
            doi = doi[:-1].rstrip(".,;:'")
    return doi


def check_against_cards():
    src = (ROOT / "tools" / "cards.py").read_text(encoding="utf-8")
    rule = re.search(r"^DOI_RE = .*$", src, re.M).group(0)
    func = re.search(r"^def clean_doi\(raw\):\n(?:    .*\n|\n)+?(?=\n\ndef )", src, re.M).group(0).rstrip()
    mine_rule = 'DOI_RE = re.compile(r"\\b10\\.\\d{4,9}/[^\\s\\"]+")'
    if rule != mine_rule or func != inspect.getsource(clean_doi).rstrip():
        sys.exit("DOI_RE or clean_doi differs from tools/cards.py; update this script")


def collect():
    files = sorted((ROOT / "taxa").glob("*.md")) + sorted((ROOT / "docs").glob("*.md"))
    found = {}
    for path in files:
        rel = str(path.relative_to(ROOT))
        for line in path.read_text(encoding="utf-8").splitlines():
            for raw in DOI_RE.findall(line):
                found.setdefault(clean_doi(raw).lower(), set()).add(rel)
    return files, found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=ROOT / "data/external/library/seeds")
    a = ap.parse_args()
    check_against_cards()
    files, found = collect()
    a.out.mkdir(parents=True, exist_ok=True)
    with open(a.out / "cited.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["openalex_id", "doi", "files"])
        for doi in sorted(found):
            w.writerow(["", doi, ";".join(sorted(found[doi]))])
    print(f"{len(files)} files scanned, {len(found)} distinct DOIs -> {a.out / 'cited.tsv'}")


if __name__ == "__main__":
    main()
