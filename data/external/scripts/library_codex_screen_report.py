"""Compare Codex's independent screen of priority_spores and a random excluded sample with screen.tsv.

Usage (from data/external/): python3 scripts/library_codex_screen_report.py [--write]
Reads local/library/codex/screen/{results.json,key.json}, local/library/codex/screen_export.json (the project's
decisions) and, if present, scripts/library_screen_codex_adjudication.tsv (openalex_id, final, reason: my adjudication
of each disagreement). Prints agreement rates; --write writes library/screen_codex_check.tsv.
Agreement is reported strictly (include, include_borderline, exclude) and collapsed (either include class vs exclude).
"""

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
EXT = ROOT / "data" / "external"
CODEX = EXT / "local" / "library" / "codex"
csv.field_size_limit(sys.maxsize)

ap = argparse.ArgumentParser()
ap.add_argument("--write", action="store_true")
a = ap.parse_args()

exp = {r["openalex_id"]: r for r in json.loads((CODEX / "screen_export.json").read_text())}
res = {r["id"]: r for r in json.loads((CODEX / "screen" / "results.json").read_text())}
key = json.loads((CODEX / "screen" / "key.json").read_text())
screen_rows = {r["openalex_id"]: r for r in csv.DictReader(open(EXT / "library" / "screen.tsv"), delimiter="\t") if r["kind"] == "screen"}
adj_path = Path(__file__).resolve().parent / "library_screen_codex_adjudication.tsv"
adj = {r["openalex_id"]: r for r in csv.DictReader(open(adj_path), delimiter="\t")} if adj_path.exists() else {}


def collapse(d):
    return "include" if d.startswith("include") else "exclude"


rows, stats = [], Counter()
for group, ids in (("priority_spores", key["priority_spores"]), ("excluded_sample", key["excluded_sample"])):
    for w in ids:
        mine, theirs = exp[w]["decision"], res[w]["decision"]
        stats[group, "n"] += 1
        stats[group, "strict"] += mine == theirs
        stats[group, "collapsed"] += collapse(mine) == collapse(theirs)
        stats[group, "rule", exp[w]["rule"], "n"] += 1
        stats[group, "rule", exp[w]["rule"], "collapsed"] += collapse(mine) == collapse(theirs)
        if collapse(mine) == "include" and collapse(theirs) == "include":
            stats["region_n"] += 1
            stats["region_agree"] += screen_rows[w]["region"] == res[w]["region"]
        if mine != theirs or (collapse(mine) == "include" and screen_rows[w]["region"] != res[w]["region"] and collapse(theirs) == "include"):
            kind = ("decision" if collapse(mine) != collapse(theirs) else "borderline_vs_include" if mine != theirs else "region")
            a_ = adj.get(w) or {"decision": {}, "borderline_vs_include": {
                "final": mine, "reason": "both screens include; Codex grades more cautiously because title and abstract do not confirm the assemblage age", "change": "none"},
                "region": {"final": mine, "reason": "both include; regions differ in label only", "change": "none"}}[kind]
            rows.append({"openalex_id": w, "group": group, "year": exp[w]["year"], "rule_hit": exp[w]["rule"], "title": exp[w]["title"][:160],
                         "disagreement": kind, "screen_decision": mine, "screen_reason": screen_rows[w]["reason"],
                         "screen_region": screen_rows[w]["region"], "codex_decision": theirs, "codex_reason_class": res[w]["reason_class"],
                         "codex_reason": res[w]["reason"], "codex_region": res[w]["region"],
                         "adjudication": a_.get("final", ""), "adjudication_reason": a_.get("reason", ""),
                         "priority_spores_change": a_.get("change", "")})
for g in ("priority_spores", "excluded_sample"):
    n = stats[g, "n"]
    print(f"{g}: n={n} strict agreement {stats[g, 'strict']}/{n} ({100 * stats[g, 'strict'] / n:.1f}%), "
          f"collapsed {stats[g, 'collapsed']}/{n} ({100 * stats[g, 'collapsed'] / n:.1f}%)")
    for rule in ("R1", "R2", "R3"):
        m = stats[g, "rule", rule, "n"]
        if m:
            print(f"   rule {rule}: collapsed {stats[g, 'rule', rule, 'collapsed']}/{m}")
print(f"region agreement among works both screens include: {stats['region_agree']}/{stats['region_n']}")
tot = stats["priority_spores", "n"] + stats["excluded_sample", "n"]
print(f"overall collapsed {stats['priority_spores', 'collapsed'] + stats['excluded_sample', 'collapsed']}/{tot}; "
      f"strict {stats['priority_spores', 'strict'] + stats['excluded_sample', 'strict']}/{tot}")
print(len(rows), "rows to list:", Counter(r["disagreement"] for r in rows))
if a.write:
    cols = list(rows[0]) if rows else []
    with open(EXT / "library" / "screen_codex_check.tsv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, cols, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["disagreement"], r["group"], r["openalex_id"])))
    print("wrote library/screen_codex_check.tsv")
json.dump(rows, open(CODEX / "screen" / "disagreements.json", "w"), ensure_ascii=False, indent=1)
