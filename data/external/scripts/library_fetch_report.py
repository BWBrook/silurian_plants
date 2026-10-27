"""Summarise a phase 2 fetch: one row per attempted work, plus counts by subset, from the store's own records.

Usage (on deep-server, from _tools/): python3 library_fetch_report.py [--out STORE/_build]
Reads manifest.tsv, attempts.tsv, _build/works.tsv and the quarantine folder. Writes fetch_results.tsv and fetch_counts.tsv.
No network. Rows cover every work of the fetched subsets (priority_spores, cards) that `fetch` selected.
Held copies get a full-text test: text_words counts words in STORE/text/<W>.txt, and fulltext_check is `short_under_1500`
below MIN_WORDS (an abstract or landing page passes the title and identity checks; review found six such), `no_text` when
the PDF has no text layer, otherwise `ok`.
"""

import argparse
import hashlib
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import library as L  # noqa: E402

ROUTE_OF_HOST = {"PubMed Central OA": "pmc_open_access_bucket", "Internet Archive": "internet_archive_scan",
                 "CORE": "core_repository_link", "Semantic Scholar": "semantic_scholar_oa_link"}
MIN_WORDS = 1500


def fulltext(store, wid):
    p = store / "text" / f"{wid}.txt"
    if not p.exists():
        return "", "no_text"
    n = len(p.read_text(encoding="utf-8", errors="replace").split())
    return str(n), "ok" if n >= MIN_WORDS else ("no_text" if n == 0 else "short_under_1500")


def route(host, kind_hint=""):
    return ROUTE_OF_HOST.get(host, "openalex_location")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", type=Path, default=Path("/data/codex/silurian_plants/library"))
    ap.add_argument("--out", type=Path)
    a = ap.parse_args()
    store, out = a.store, a.out or a.store / "_build"
    works = {r["openalex_id"]: r for r in L.read_tsv(out / "works.tsv")}
    seeds = set()
    for tier in ("priority_spores", "cards"):
        seeds |= {r["openalex_id"] for r in L.read_tsv(HERE / "seeds" / f"{tier}.tsv")}
    manifest_rows = L.read_tsv(store / "manifest.tsv") if (store / "manifest.tsv").exists() else []
    latest = {}
    for r in manifest_rows:
        latest[r["openalex_id"]] = r
    attempts = defaultdict(list)
    for r in L.read_tsv(store / "attempts.tsv"):
        attempts[r["openalex_id"]].append(r)
    qdir = store / "quarantine"
    qfiles = defaultdict(list)
    for p in qdir.glob("W*__*.pdf") if qdir.exists() else []:
        qfiles[p.name.split("__")[0]].append(p)

    rows = []
    for wid in sorted(seeds):
        w = works.get(wid)
        if not w:
            continue
        subs = [s for s in w["subsets"].split(";") if s in ("priority_spores", "cards")]
        m = latest.get(wid)
        att = attempts.get(wid, [])
        outcome, rt, host, url, size, sha, note, quar, path = "", "", "", "", "", "", "", "no", ""
        if m and m["status"] in ("ok", "no_text"):
            outcome, host, url, size, sha, path = m["status"], m["host"], m["url"], m["bytes"], m["sha256"], m["path"]
            rt = route(host)
            note = f"version {m['version'] or 'unknown'}; licence {m['license'] or 'not stated'}; title_match {m['title_match']}"
        elif m and m["status"] == "withdrawn":
            outcome, host, url, size, sha, rt = "withdrawn", m["host"], m["url"], m["bytes"], m["sha256"], route(m["host"])
            note = m["note"]
        else:
            fails = Counter(r["outcome"] for r in att if not r["outcome"].startswith(("s2_", "core_", "ia_")))
            lookups = [r for r in att if r["outcome"].startswith(("s2_", "core_", "ia_"))]
            if any(r["outcome"] == "mismatch" for r in att):
                outcome = "quarantined"
                bad = [r for r in att if r["outcome"] == "mismatch"][-1]
                host, url, rt = bad["host"], bad["url"], route(bad["host"])
                note = bad["detail"]
            elif fails:
                outcome = "failed"
                note = "; ".join(f"{k} x{v}" for k, v in fails.most_common())
                host = att[-1]["host"]
            else:
                outcome = "no_copy"
                note = "no open location, repository or lookup copy found" if lookups or not att else "no candidate"
        if wid in qfiles:
            quar = "yes"
            if outcome in ("quarantined", "failed"):
                p = qfiles[wid][-1]
                data = p.read_bytes()
                size, sha, path = str(len(data)), hashlib.sha256(data).hexdigest(), f"quarantine/{p.name}"
        words, check = fulltext(store, wid) if outcome in ("ok", "no_text") else ("", "")
        rows.append({"openalex_id": wid, "doi": w["doi"], "subsets": ";".join(subs), "outcome": outcome, "route": rt, "host": host,
                     "url": url, "bytes": size, "sha256": sha, "quarantine": quar, "attempts": len(att), "path": path,
                     "text_words": words, "fulltext_check": check, "note": note, "title": w["title"][:140]})
    fields = ["openalex_id", "doi", "subsets", "outcome", "route", "host", "url", "bytes", "sha256", "quarantine", "attempts",
              "path", "text_words", "fulltext_check", "note", "title"]
    L.write_tsv(out / "fetch_results.tsv", rows, fields)
    counts = []
    for sub in ("priority_spores", "cards", "all"):
        sel = [r for r in rows if sub == "all" or sub in r["subsets"].split(";")]
        c = Counter(r["outcome"] for r in sel)
        routes = Counter(r["route"] for r in sel if r["outcome"] in ("ok", "no_text"))
        counts.append({"subset": sub, "works_attempted": len(sel), "held_ok": c["ok"], "held_no_text": c["no_text"],
                       "held_short_under_1500": sum(1 for r in sel if r["fulltext_check"] == "short_under_1500"),
                       "quarantined": c["quarantined"], "failed": c["failed"], "no_copy": c["no_copy"], "withdrawn": c["withdrawn"],
                       "routes_held": "; ".join(f"{k} {v}" for k, v in routes.most_common()),
                       "mb_held": round(sum(int(r["bytes"] or 0) for r in sel if r["outcome"] in ("ok", "no_text")) / 1e6, 1)})
    L.write_tsv(out / "fetch_counts.tsv", counts, list(counts[0]))
    for c in counts:
        print(c)


if __name__ == "__main__":
    main()
