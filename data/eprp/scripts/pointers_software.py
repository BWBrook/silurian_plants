"""Select EPRP software-landscape rows relevant to silurian_plants framings.

Usage: python3 scripts/pointers_software.py [EPRP_CHECKOUT]  (run from data/eprp/)
Reads resources/software/landscape.tsv; writes pointers/software_relevant.tsv.
The framing column is a rule-based mapping from EPRP's domain and method labels,
not a judgment about each tool.
"""

import csv
import subprocess
import sys
from pathlib import Path

eprp = Path(sys.argv[1] if len(sys.argv) > 1 else "/Users/bwbrook/git/eprp")
src = eprp / "resources/software/landscape.tsv"
out = Path("pointers/software_relevant.tsv")

DOMAIN_FRAMINGS = {
    "earth-system": "F5",
    "palaeoclimate": "F5",
    "sim-ecoevo": "F1 F2 F4 F7",
    "biogeography": "F4",
    "palaeogeography": "F4",
    "fossil-record-forward": "F3",
    "extinction-timing": "F3 F6",
    "biostratigraphy": "F3",
    "diversity-rates": "F3 F6",
}
PHYLO_KEYS = ("FBD", "Divergence dating", "Clock models", "tip-dating", "Tip dating")

commit = subprocess.run(
    ["git", "-C", str(eprp), "rev-parse", "--short", "HEAD"],
    capture_output=True, text=True, check=True,
).stdout.strip()

with src.open(newline="") as f:
    rows = list(csv.DictReader(f, delimiter="\t"))

entries = {p.name for p in (eprp / "resources/software").iterdir()
           if (p / "README.md").is_file()}

keep = []
for r in rows:
    framing = DOMAIN_FRAMINGS.get(r["domain"])
    if framing is None and r["domain"] == "phylogenetic" and any(
        k in r["method_family"] for k in PHYLO_KEYS
    ):
        framing = "F3"
    if framing is None:
        continue
    keep.append({
        "id": r["id"],
        "name": r["name"],
        "domain": r["domain"],
        "method_family": r["method_family"],
        "kind": r["kind"],
        "languages": r["languages"],
        "summary": r["summary"],
        "framings": framing,
        "eprp_entry": f"resources/software/{r['id']}/README.md" if r["id"] in entries else "",
        "home": r["home"] or r["github"] or r["other_repo"],
        "licence_scan": r["licence_scan"],
        "blockers": r["blockers"],
        "papers": r["papers"],
        "eprp_questions": r["eprp_questions"],
        "eprp_commit": commit,
    })

keep.sort(key=lambda k: (k["framings"], k["domain"], k["eprp_entry"] == "", k["name"].lower()))
out.parent.mkdir(exist_ok=True)
with out.open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(keep[0]), delimiter="\t", lineterminator="\n")
    w.writeheader()
    w.writerows(keep)
print(f"{len(keep)} of {len(rows)} tools -> {out}")
