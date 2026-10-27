"""Seed tiers `window` and `window-marine` from OpenAlex title_and_abstract.search queries.

Usage (on deep-server, from _tools/):
  python3 library_window.py probes    # count-only checks of query variants (group_by year), logged to queries.tsv
  python3 library_window.py seed      # page the seed queries, save full records to STORE/openalex/, write seeds
  python3 library_window.py finalize  # fill by_period and distinct counts for the seed rows of queries.tsv

Every OpenAlex call goes through library.py's get_json and openalex_url (via library_run, which counts
credits). `seed` pages each query with per-page 200 and a cursor and keeps the full work records (abstract
inverted index included) in the store exactly as library.py's `resolve` would, so a later `resolve` finds
them held. Tier `window` is the union of queries a, b and d; tier `window-marine` is query c.
Every query, with its date, hit count and credits, is appended to STORE/queries.tsv.
"""

import csv
import datetime
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import library_run as R  # noqa: E402

L = R.L
STORE = Path("/data/codex/silurian_plants/library")

ORD = ("Tremadoc OR Tremadocian OR Floian OR Arenig OR Dapingian OR Darriwilian OR Llanvirn OR Llandeilo OR "
       "Sandbian OR Katian OR Caradoc OR Ashgill OR Hirnantian")
SIL = ("Llandovery OR Rhuddanian OR Aeronian OR Telychian OR Wenlock OR Sheinwoodian OR Homerian OR Ludlow OR "
       "Gorstian OR Ludfordian OR Pridoli OR Přídolí")
DEV = "Lochkovian OR Gedinnian OR Pragian OR Siegenian OR Emsian"
OLD = ("Llandoverian OR Wenlockian OR Ludlovian OR Downtonian OR Gothlandian OR Dittonian OR Ashgillian OR "
       "Caradocian OR Llandeilian OR Arenigian")
STAGES = f"{ORD} OR {SIL} OR {DEV}"
SPORE_STAGE_TERMS = f'(Ordovician OR Silurian OR "Early Devonian" OR "Lower Devonian" OR {STAGES})'
PLANT_TERMS = ('spore OR spores OR cryptospore OR palynology OR palynomorph OR "land plant" OR "land plants" OR '
               'embryophyte OR tracheophyte OR flora OR rhyniophyte OR zosterophyll OR lycopsid OR Prototaxites OR '
               'nematophyte OR "Rhynie chert" OR terrestrialization')
SPORE6 = '(cryptospore OR miospore OR "trilete spore" OR "dispersed spore" OR "spore assemblage" OR "spore zone")'

PLANTS = f"(Silurian OR Devonian OR Ordovician) AND ({PLANT_TERMS})"
SPORE_B = (f'(cryptospore OR miospore OR trilete OR "dispersed spore" OR "spore assemblage" OR "spore zone" OR '
           f'palynozone OR "spore assemblages") AND {SPORE_STAGE_TERMS}')
STAGE_PLANTS = (f'(spore OR spores OR cryptospore OR cryptospores OR miospore OR miospores OR trilete OR palynology OR '
                f'palynomorph OR palynomorphs OR palynozone OR "land plant" OR "land plants" OR embryophyte OR '
                f'tracheophyte OR rhyniophyte OR zosterophyll OR lycopsid OR Prototaxites OR nematophyte OR '
                f'"Rhynie chert" OR terrestrialization OR terrestrialisation) AND ({STAGES} OR {OLD} OR '
                f'"Early Devonian" OR "Lower Devonian")')
MARINE = f"(acritarch OR chitinozoan OR phytoplankton) AND {SPORE_STAGE_TERMS}"

# id, tier, role, query, note
SEEDS_Q = [
    ("a", "window", "seed", PLANTS, "plants union as specified; 4,835 works on 2026-10-27"),
    ("b", "window", "seed", SPORE_B, "reconstruction of the plan 2 section 2 spore query; variant closest to its 493 works"),
    ("d", "window", "seed", STAGE_PLANTS, "extension: plant and spore terms with stage names but no period name"),
    ("c", "window-marine", "seed", MARINE, "acritarch, chitinozoan, phytoplankton with the section 2 stage terms"),
]
PROBES_Q = [
    ("p1", "window", "probe", f"{SPORE6} AND (Ordovician OR Silurian OR Devonian)", "spore terms with period names"),
    ("p2", "window", "probe", f"{SPORE6} AND ({STAGES})", "spore terms with stage names only"),
    ("p3", "window", "probe", f"{SPORE6} AND (Ordovician OR Silurian OR Devonian OR {STAGES})", "periods and stages"),
    ("p4", "window", "probe", f'{SPORE6} AND {SPORE_STAGE_TERMS}', "closest of the six-term variants"),
    ("p5", "window", "probe", f'{SPORE6} AND (Ordovician OR Silurian OR "Early Devonian" OR "Lower Devonian")', "no stage names"),
    ("p6", "window", "probe", f'{SPORE6} AND ("Early Devonian" OR "Lower Devonian" OR {STAGES})', "no Ordovician or Silurian period names"),
    ("p7", "window", "probe", f'{SPORE6} AND (Ordovician OR Silurian OR "Early Devonian" OR "Lower Devonian" OR {STAGES} OR {OLD})', "adds old stage names"),
    ("p8", "window-marine", "probe", f"(acritarch OR chitinozoan OR phytoplankton) AND (Ordovician OR Silurian OR Devonian)", "periods only"),
    ("p9", "window-marine", "probe", f"(acritarch OR chitinozoan OR phytoplankton) AND ({STAGES})", "stages only"),
    ("p10", "window-marine", "probe", f"(acritarch OR chitinozoan) AND {SPORE_STAGE_TERMS}", "without phytoplankton"),
    ("p11", "window-marine", "probe", f"acritarch AND {SPORE_STAGE_TERMS}", "acritarch only"),
    ("p12", "window", "probe", f'(cryptospore OR miospore OR "trilete spore" OR "dispersed spore" OR "spore assemblage" OR "spore zone" OR "spore assemblages") AND (Ordovician OR Silurian OR "Early Devonian" OR "Lower Devonian" OR {STAGES} OR {OLD})', "spore terms with plural, old names"),
    ("p13", "window-marine", "probe", f"(acritarch OR chitinozoan OR phytoplankton) AND (Ordovician OR Silurian OR Devonian OR {STAGES})", "periods and stages"),
    ("p14", "window-marine", "probe", f'(acritarch OR acritarchs OR chitinozoan OR chitinozoans OR phytoplankton OR chitinozoa) AND {SPORE_STAGE_TERMS}', "plural and chitinozoa"),
    ("p15", "window", "probe", "cryptospore", "single term, from the first header probe"),
]
QFIELDS = ["query_id", "tier", "role", "date", "hits", "by_period", "credits", "note", "filter"]


def flt(q):
    return f"title_and_abstract.search:{q}"


def periods(by):
    spans = {"to_1979": (0, 1979), "1980s": (1980, 1989), "1990s": (1990, 1999), "2000_06": (2000, 2006),
             "2007_26": (2007, 2026)}
    return {k: sum(v for y, v in by.items() if str(y) != "" and a <= int(y) <= b) for k, (a, b) in spans.items()}


def log_query(row):
    path = STORE / "queries.tsv"
    new = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, QFIELDS, delimiter="\t", lineterminator="\n")
        if new:
            w.writeheader()
        w.writerow(row)


def today():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")


def probe(qid, tier, role, q, note):
    before = R.TALLY["used"]
    data, _ = L.get_json(L.openalex_url("works", {"filter": flt(q), "group_by": "publication_year"}))
    by = {g["key"]: g["count"] for g in data["group_by"]}
    hits = sum(by.values())
    log_query({"query_id": qid, "tier": tier, "role": role, "date": today(), "hits": hits,
               "by_period": json.dumps(periods(by)), "credits": R.TALLY["used"] - before, "note": note,
               "filter": flt(q)})
    print(f"{qid} {hits} {periods(by)}", flush=True)


def save_record(rec):
    wid = L.short_wid(rec["id"])
    path = STORE / "openalex" / f"{wid}.json"
    if path.exists():
        return wid, False
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(rec, ensure_ascii=False))
    os.replace(tmp, path)
    return wid, True


def page_query(q):
    """Yield (record, hit count) for every work matching the query."""
    cursor, count = "*", None
    while cursor:
        data, _ = L.get_json(L.openalex_url("works", {"filter": flt(q), "per-page": "200", "cursor": cursor}))
        count = data["meta"]["count"]
        for rec in data["results"]:
            yield rec, count
        cursor = data["meta"].get("next_cursor") if data["results"] else None


def finalize():
    """Fill by_period for the seed queries from the seed files and replace the raw paging note with distinct counts."""
    seeds = {t: L.read_tsv(STORE / "_tools" / "seeds" / f"{t}.tsv") for t in ("window", "window-marine")}
    rows = L.read_tsv(STORE / "queries.tsv")
    for r in rows:
        if r["role"] != "seed":
            continue
        members = [w for w in seeds[r["tier"]] if r["query_id"] in w["queries"].split(";")]
        by = {}
        for w in members:
            by[w["year"]] = by.get(w["year"], 0) + 1
        r["by_period"] = json.dumps(periods(by))
        r["note"] = re.sub(r"; RETURNED (\d+) of \d+", rf"; {len(members)} distinct works kept (\1 rows returned, cursor pages repeat some)", r["note"])
    L.write_tsv(STORE / "queries.tsv", rows, QFIELDS)


def seed():
    (STORE / "openalex").mkdir(parents=True, exist_ok=True)
    tier_rows = {"window": {}, "window-marine": {}}
    for qid, tier, role, q, note in SEEDS_Q:
        before, got, new, count = R.TALLY["used"], 0, 0, 0
        for rec, count in page_query(q):
            wid, fresh = save_record(rec)
            got += 1
            new += fresh
            row = tier_rows[tier].setdefault(wid, {"openalex_id": wid, "doi": L.norm_doi(rec.get("doi")),
                                                   "year": rec.get("publication_year") or "",
                                                   "type": rec.get("type") or "", "queries": set()})
            row["queries"].add(qid)
        status = "" if got == count else f"; RETURNED {got} of {count}"
        log_query({"query_id": qid, "tier": tier, "role": role, "date": today(), "hits": count,
                   "by_period": "", "credits": R.TALLY["used"] - before,
                   "note": f"{note}; {new} new records stored{status}", "filter": flt(q)})
        print(f"{qid}: {count} hits, {got} returned, {new} new records, tier {tier} now {len(tier_rows[tier])}",
              flush=True)
    for tier, rows in tier_rows.items():
        out = [dict(r, queries=";".join(sorted(r["queries"]))) for r in sorted(rows.values(), key=lambda r: (str(r["year"]), r["openalex_id"]))]
        L.write_tsv(STORE / "_tools" / "seeds" / f"{tier}.tsv", out, ["openalex_id", "doi", "year", "type", "queries"])
        print(f"{tier}: {len(out)} works -> seeds/{tier}.tsv")


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    try:
        if mode == "probes":
            wanted = set(sys.argv[2:])
            for item in PROBES_Q:
                if not wanted or item[0] in wanted:
                    probe(*item)
        elif mode == "seed":
            seed()
        elif mode == "finalize":
            finalize()
        else:
            sys.exit(__doc__)
    finally:
        print(f"credits used: {R.TALLY['used']} in {R.TALLY['calls']} calls (remaining {R.TALLY['remaining']})")
        R.log_credits(STORE, f"library_window.py {mode}")
