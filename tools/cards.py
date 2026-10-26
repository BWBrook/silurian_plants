# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Validate taxon cards, check cited DOIs against Crossref, and build the card index.

    uv run tools/cards.py check   # schema and vocabulary checks on taxa/*.md
    uv run tools/cards.py dois    # every DOI in taxa/ and docs/ against Crossref
    uv run tools/cards.py index   # rewrite taxa/README.md
"""

import csv
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
TAXA = ROOT / "taxa"
DOCS = ROOT / "docs"

RANKS = {"species", "genus", "morphogroup", "assemblage"}
KINDS = {"megafossil", "mesofossil", "dispersed_spores", "assemblage"}
GROUPS = {
    "streptophyte-alga",
    "cryptospore-plant",
    "bryophyte",
    "rhyniophytoid",
    "protracheophyte",
    "rhyniopsid",
    "zosterophyll",
    "lycopsid",
    "basal-euphyllophyte",
    "tracheophyte-other",
    "fungus",
    "lichen",
    "nematophyte",
    "incertae-sedis",
}
CONFIDENCE = {"low", "medium", "high"}
STATUS = {"draft", "reviewed"}
PRESERVATION = {"compression", "permineralised", "charcoalified", "adpression", "cast", "dispersed"}
TRAIT_STATES = {
    "branching": {"none", "isotomous", "anisotomous", "pseudomonopodial", "monopodial",
                  "K-branching", "H-branching", "mixed"},
    "leaves": {"absent", "enations", "microphylls", "megaphylls"},
    "stomata": {"present", "absent"},
    "conducting_tissue": {"absent", "hydroids", "non-lignified", "tracheids-G", "tracheids-S",
                          "tracheids-P", "tracheids"},
    "sporangium_position": {"terminal", "lateral", "both"},
    "spores": {"cryptospores", "trilete", "both"},
    "heterospory": {"absent", "present"},
    "rooting": {"rhizoids", "rhizomes", "roots", "rooting-axes"},
    "gametophyte": {"known"},
}
NUMERIC_TRAITS = {"height_cm", "axis_diameter_mm"}
REQUIRED = ["name", "authority", "rank", "kind", "group", "lineage", "placement_confidence",
            "range", "regions", "localities", "preservation", "habitat", "status", "updated",
            "references"]
SECTIONS = ["In brief", "Morphology and anatomy", "Age and distribution",
            "Affinity and controversies", "Ecology and physiology",
            "Why it matters for modelling", "Open questions"]
DOI_RE = re.compile(r"\b10\.\d{4,9}/[^\s\"'<>\])]+[^\s\"'<>\]).,;:]")


def timescale():
    with open(ROOT / "data" / "timescale.csv") as f:
        return {row["stage"]: float(row["base_ma"]) for row in csv.DictReader(f)}


def card_paths():
    return sorted(p for p in TAXA.glob("*.md") if not p.name.startswith(("_", "README")))


def read_card(path):
    text = path.read_text()
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        raise ValueError("no YAML front matter")
    return yaml.safe_load(m.group(1)), m.group(2)


def check_card(path, stages):
    problems = []
    try:
        meta, body = read_card(path)
    except (ValueError, yaml.YAMLError) as e:
        return [str(e)]
    for key in REQUIRED:
        if meta.get(key) in (None, "", []):
            problems.append(f"missing {key}")
    for key, allowed in [("rank", RANKS), ("kind", KINDS), ("group", GROUPS),
                         ("placement_confidence", CONFIDENCE), ("status", STATUS)]:
        if meta.get(key) is not None and meta[key] not in allowed:
            problems.append(f"{key}={meta[key]!r} not in vocabulary")
    for p in meta.get("preservation") or []:
        if p not in PRESERVATION:
            problems.append(f"preservation {p!r} not in vocabulary")
    rng = meta.get("range") or {}
    first, last = rng.get("first"), rng.get("last")
    for label, stage in [("first", first), ("last", last)]:
        if stage not in stages:
            problems.append(f"range.{label}={stage!r} is not an ICS stage in data/timescale.csv")
    if first in stages and last in stages and stages[first] < stages[last]:
        problems.append(f"range.first ({first}) is younger than range.last ({last})")
    for trait, value in (meta.get("traits") or {}).items():
        if trait in NUMERIC_TRAITS:
            if not isinstance(value, dict):
                problems.append(f"{trait} must be a {{min, max, note}} mapping")
                continue
            lo, hi = value.get("min"), value.get("max")
            if any(v is not None and not isinstance(v, (int, float)) for v in (lo, hi)):
                problems.append(f"{trait} min/max must be numbers or null")
            elif lo is not None and hi is not None and lo > hi:
                problems.append(f"{trait} min > max")
        elif trait in TRAIT_STATES:
            state = value.get("state") if isinstance(value, dict) else None
            if state not in TRAIT_STATES[trait] | {"unknown", "na"}:
                problems.append(f"{trait} state {state!r} not in vocabulary")
        else:
            problems.append(f"unrecognised trait {trait!r}")
    for i, ref in enumerate(meta.get("references") or []):
        if not isinstance(ref, dict) or not ref.get("cite"):
            problems.append(f"reference {i + 1} lacks a cite string")
        elif "doi" not in ref:
            problems.append(f"reference {i + 1} lacks a doi key (use null if none exists)")
        elif ref["doi"] is not None and not DOI_RE.fullmatch(str(ref["doi"])):
            problems.append(f"reference {i + 1} doi {ref['doi']!r} is malformed")
    headings = re.findall(r"^## (.+)$", body, re.M)
    for s in SECTIONS:
        if s not in headings:
            problems.append(f"missing section '## {s}'")
    return problems


def cmd_check():
    stages = timescale()
    n_bad = 0
    for path in card_paths():
        problems = check_card(path, stages)
        if problems:
            n_bad += 1
            print(f"{path.relative_to(ROOT)}:")
            for p in problems:
                print(f"  - {p}")
    print(f"{len(card_paths())} cards, {n_bad} with problems")
    return 1 if n_bad else 0


def crossref(doi):
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "silurian_plants-cards/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            msg = json.load(r)["message"]
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}"}
    except (urllib.error.URLError, TimeoutError) as e:
        return {"error": str(e)}
    year = (msg.get("issued", {}).get("date-parts") or [[None]])[0][0]
    authors = msg.get("author") or []
    return {"title": " ".join(msg.get("title") or [""]), "year": year,
            "first_author": authors[0].get("family", "") if authors else ""}


def words(s):
    return {w for w in re.findall(r"[a-z]{4,}", s.lower())}


def cmd_dois():
    occurrences = {}
    for path in card_paths() + sorted(DOCS.glob("**/*.md")):
        lines = path.read_text().splitlines()
        for i, line in enumerate(lines):
            for doi in DOI_RE.findall(line):
                context = " ".join(lines[max(0, i - 1): i + 1])
                occurrences.setdefault(doi.lower(), []).append((path.relative_to(ROOT), context))
    with ThreadPoolExecutor(8) as pool:
        records = dict(zip(occurrences, pool.map(crossref, occurrences)))
    n_bad = 0
    for doi, rec in sorted(records.items()):
        for path, context in occurrences[doi]:
            if "error" in rec:
                issue = f"Crossref lookup failed ({rec['error']})"
            else:
                title = words(rec["title"])
                overlap = len(title & words(context)) / max(1, len(title))
                issues = []
                if overlap < 0.6:
                    issues.append(f"title overlap {overlap:.0%}")
                if rec["year"] and str(rec["year"]) not in context:
                    issues.append(f"year {rec['year']} not in citation")
                if rec["first_author"] and rec["first_author"].lower() not in context.lower():
                    issues.append(f"first author {rec['first_author']} not in citation")
                if not issues:
                    continue
                issue = "; ".join(issues) + f" — Crossref: {rec['first_author']} {rec['year']}, {rec['title']}"
            n_bad += 1
            print(f"{path}: {doi}\n  {issue}")
    print(f"{len(records)} distinct DOIs, {n_bad} flagged")
    return 1 if n_bad else 0


def cmd_index():
    stages = timescale()
    rows = []
    for path in card_paths():
        meta, _ = read_card(path)
        rng = meta["range"]
        rows.append((stages.get(rng["first"], 0), meta, path.name, rng))
    rows.sort(key=lambda r: (-r[0], r[1]["name"]))
    out = ["# Taxon cards", "",
           "Generated by `uv run tools/cards.py index` from the cards' front matter; do not edit by hand.",
           "Ordered by first appearance. Ages are ICS v2024/12 stage bases (`data/timescale.csv`).", "",
           "| Taxon | Group | First | Last | Kind | Placement confidence | Status |",
           "|---|---|---|---|---|---|---|"]
    for base, meta, fname, rng in rows:
        first = f"{rng['first']} ({base:g} Ma)"
        out.append(f"| [{meta['name']}]({fname}) | {meta['group']} | {first} | {rng['last']} | "
                   f"{meta['kind']} | {meta['placement_confidence']} | {meta['status']} |")
    (TAXA / "README.md").write_text("\n".join(out) + "\n")
    print(f"wrote taxa/README.md ({len(rows)} cards)")
    return 0


if __name__ == "__main__":
    commands = {"check": cmd_check, "dois": cmd_dois, "index": cmd_index}
    if len(sys.argv) != 2 or sys.argv[1] not in commands:
        sys.exit(__doc__)
    sys.exit(commands[sys.argv[1]]())
