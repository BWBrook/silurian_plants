# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""Occurrence data for the first deliverable (data/occurrences/README.md).

    uv run tools/occurrences.py spores          # tail of E1/E2 from data/spores (vetted dataset rows)
    uv run tools/occurrences.py import FILE...  # merge Codex JSON outputs (observations, interpretations, sources)
    uv run tools/occurrences.py effort PBDB.csv # effort by stage x unit: PBDB collections (all taxa) and Palynodata documents
    uv run tools/occurrences.py check           # schema, one main reading per observation, stages, quotes
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "occurrences"
SPORES = ROOT / "data" / "spores"
OBS_COLS = ["obs_id", "channel", "reported_as", "locality", "country", "unit", "horizon", "palaeo_unit",
            "source_ids", "locator", "events", "same_material_as", "notes"]
INT_COLS = ["interp_id", "obs_id", "label", "counts_for", "stage_oldest", "stage_youngest", "age_note", "held_by",
            "held_by_source_ids", "adjudicator", "main", "main_basis", "support", "support_from", "checked"]
SRC_COLS = ["source_id", "citation", "doi", "access"]
EVENTS = {"E1", "E2", "E3", "E4", "E5"}
CHECKED = {"full-text", "abstract", "card", "repo-doc", "secondary"}
EVENT_OF = {"trilete": "E1", "cryptospore": "E2"}
TAIL_BASE = {"trilete": 445.2, "cryptospore": 452.8}  # Hirnantian or older; Sandbian or older


def stages():
    return {r["stage"]: r for r in csv.DictReader(open(ROOT / "data" / "timescale.csv"))}


def read(name, cols):
    path = OUT / name
    return list(csv.DictReader(open(path))) if path.exists() else []


def write(name, cols, rows):
    with open(OUT / name, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def merge(name, cols, key, new):
    old = {r[key]: r for r in read(name, cols)}
    old.update({r[key]: r for r in new})
    write(name, cols, sorted(old.values(), key=lambda r: r[key]))


def cmd_spores():
    occ = list(csv.DictReader(open(SPORES / "occurrences.csv")))
    vet = {r["doc"]: r for r in csv.DictReader(open(SPORES / "crosswalks" / "doc_vetting.csv"))}
    docs = {r["AUTHDOCNUM"]: r for r in csv.DictReader(open(ROOT / "data/external/spores/palynodata_documents_window.csv"))}
    mvdb = {r["assemblage_id"]: r for r in csv.DictReader(open(SPORES / "sources" / "mvdb_assemblages.csv"))}
    w13 = {r["entry_id"]: r for r in csv.DictReader(open(SPORES / "sources" / "wellman2013_assemblages.csv"))}
    units = {}
    for r in occ:
        group = next((g for g in EVENT_OF if r["spore_class"].startswith(g)), None)
        if not group or not r["oldest_base_ma"] or float(r["oldest_base_ma"]) < TAIL_BASE[group]:
            continue
        units.setdefault((r["source"], r["record_id"], group), []).append(r)
    obs, ints, srcs, skipped = [], [], {}, 0
    for (source, rid, group), rows in sorted(units.items()):
        usable = [r for r in rows if r["usable"] == "true" or r["vetting"] in ("doubtful", "reject")]
        if not usable:
            skipped += 1
            continue
        rep = max(usable, key=lambda r: (float(r["oldest_base_ma"]), -float(r["span_myr"] or 99)))
        oid = f"S-{source}-{rid}-{group}"
        if source == "palynodata":
            d = docs.get(rid, {})
            sid = f"palynodata-{rid}"
            cite = f"{d.get('Author', '').strip()} ({d.get('PALYDATE', '').strip()}). {d.get('ENGTITLE', '').strip()}. {d.get('Journal', '').strip()} {d.get('Volume', '').strip()}: {d.get('Pages', '').strip()}"
            srcs[sid] = {"source_id": sid, "citation": cite.strip(), "doi": "", "access": "unknown"}
            v = vet.get(rid)
        elif source == "mvdb":
            a = mvdb.get(rid, {})
            sid = f"mvdb-{a.get('paper', rid)}"
            srcs[sid] = {"source_id": sid, "citation": a.get("citation", ""), "doi": a.get("doi", ""), "access": "open"}
            v = None
        else:
            a = w13.get(rid, {})
            sid = "wellman2013"
            srcs[sid] = {"source_id": sid, "citation": "Wellman CH, Steemans P, Vecoli M (2013). Palaeophytogeography of Ordovician–Silurian land plants. Geological Society, London, Memoirs 38: 461–476 (supplement, Appendix 2)", "doi": "10.1144/m38.29", "access": "open"}
            v = None
        taxa = sorted({r["taxon"] for r in usable})
        obs.append({"obs_id": oid, "channel": "spore", "reported_as": f"{group}s: " + "; ".join(taxa[:8]) + (" ..." if len(taxa) > 8 else ""),
                    "locality": rep["location"], "country": "", "unit": "", "horizon": "", "palaeo_unit": rep["palaeo_unit"],
                    "source_ids": sid, "locator": f"data/spores/occurrences.csv {source}:{rid}", "events": EVENT_OF[group],
                    "same_material_as": "", "notes": f"{len(usable)} usable rows; representative row is the oldest, narrowest"})
        base = {"obs_id": oid, "stage_oldest": rep["ics_oldest"], "stage_youngest": rep["ics_youngest"],
                "age_note": f"dataset age confidence {rep['age_confidence']}", "held_by_source_ids": sid}
        as_reported = {**base, "interp_id": oid + "-a", "label": f"{group}s as reported", "counts_for": EVENT_OF[group],
                       "held_by": "the reporting authors", "adjudicator": "", "support": "", "support_from": "", "checked": "repo-doc"}
        verdict = rep["vetting"]
        if verdict in ("doubtful", "reject") and v:
            ints.append({**as_reported, "main": "false", "main_basis": ""})
            ints.append({**base, "interp_id": oid + "-b", "label": f"{group}s not established ({verdict})", "counts_for": "",
                         "held_by": "", "adjudicator": v["made_by"], "main": "true",
                         "main_basis": "MVD-A vetting verdict; rejected and doubtful records are excluded from the strict set",
                         "support": v["reason"], "support_from": "data/spores/crosswalks/doc_vetting.csv", "checked": "repo-doc"})
        else:
            label = {"accept": "accepted at vetting", "curated": "curated (Wellman et al. 2013)"}.get(verdict, "not vetted")
            ints.append({**as_reported, "label": f"{group}s as reported ({label})", "main": "true",
                         "main_basis": "no published or project challenge recorded",
                         "adjudicator": v["made_by"] if v and verdict == "accept" else "",
                         "support": v["reason"] if v and verdict == "accept" else "",
                         "support_from": "data/spores/crosswalks/doc_vetting.csv" if v and verdict == "accept" else ""})
    merge("observations.csv", OBS_COLS, "obs_id", obs)
    merge("interpretations.csv", INT_COLS, "interp_id", ints)
    merge("sources.csv", SRC_COLS, "source_id", list(srcs.values()))
    print(f"spores: {len(obs)} observations, {len(ints)} interpretations; {skipped} units had no usable or vetted rows")


def crossref_doi(citation):
    """DOI for a citation from Crossref, accepted only if title words and year agree."""
    import urllib.parse
    import urllib.request
    year = re.search(r"\((\d{4})", citation)
    title = re.split(r"\)\.?\s*", citation, maxsplit=1)[-1].split(". ")[0]
    url = "https://api.crossref.org/works?rows=3&query.bibliographic=" + urllib.parse.quote(citation[:300])
    import time
    import urllib.error
    req = urllib.request.Request(url, headers={"User-Agent": "silurian_plants occurrences.py"})
    for attempt in range(6):
        try:
            items = json.load(urllib.request.urlopen(req, timeout=30))["message"]["items"]
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 5:
                raise
            time.sleep(5 * (attempt + 1))
    time.sleep(1)
    want = set(re.findall(r"[a-z]{4,}", title.lower()))
    for it in items:
        got = set(re.findall(r"[a-z]{4,}", " ".join(it.get("title", [""])).lower()))
        years = {p[0] for k in ("published-print", "published-online", "issued") for p in it.get(k, {}).get("date-parts", [[None]]) if p and p[0]}
        if want and len(want & got) / len(want) >= 0.8 and (not year or any(abs(int(year.group(1)) - y) <= 1 for y in years)):
            return it["DOI"].lower()
    return ""


def cmd_import(files):
    for f in files:
        d = json.load(open(f))
        for s in d.get("sources", []):
            if not s["doi"] and s["citation"]:
                s["doi"] = crossref_doi(s["citation"])
        merge("observations.csv", OBS_COLS, "obs_id", d.get("observations", []))
        merge("interpretations.csv", INT_COLS, "interp_id", d.get("interpretations", []))
        merge("sources.csv", SRC_COLS, "source_id", d.get("sources", []))
        print(f"{f}: {len(d.get('observations', []))} observations, {len(d.get('interpretations', []))} interpretations")


LAND = {"terrestrial indet.", "fluvial indet.", "fluvial-lacustrine indet.", "lacustrine indet.", "lacustrine - large", "pond",
        '"floodplain"', "wet floodplain", "fine channel fill", '"channel"', "alluvial fan", "crevasse splay", "mire/swamp",
        "fluvial-deltaic indet.", "delta plain"}
MARGINAL = {"coastal indet.", "marginal marine indet.", "lagoonal", "estuary/bay", "interdistributary bay", "paralic indet.",
            "deltaic indet.", "delta front", "prodelta", "peritidal", "foreshore"}
UNIT_BY_CC = {
    "US": "Laurentia", "CA": "Laurentia", "GL": "Laurentia", "SJ": "Laurentia", "MX": "multiple",
    "IE": "Avalonia", "BE": "Avalonia", "NL": "Avalonia", "LU": "Avalonia", "DE": "multiple",
    "EE": "Baltica", "LT": "Baltica", "LV": "Baltica", "SE": "Baltica", "NO": "Baltica", "DK": "Baltica", "BY": "Baltica",
    "UA": "Baltica", "PL": "multiple", "RU": "multiple",
    "CZ": "peri-Gondwana-Europe", "ES": "peri-Gondwana-Europe", "PT": "peri-Gondwana-Europe", "FR": "peri-Gondwana-Europe",
    "IT": "peri-Gondwana-Europe", "AT": "peri-Gondwana-Europe", "BG": "peri-Gondwana-Europe", "RS": "peri-Gondwana-Europe",
    "GR": "peri-Gondwana-Europe", "TR": "Gondwana-North-Africa-Arabia",
    "MA": "Gondwana-North-Africa-Arabia", "DZ": "Gondwana-North-Africa-Arabia", "LY": "Gondwana-North-Africa-Arabia",
    "EH": "Gondwana-North-Africa-Arabia", "MR": "Gondwana-North-Africa-Arabia", "GN": "Gondwana-North-Africa-Arabia",
    "GH": "Gondwana-North-Africa-Arabia", "SA": "Gondwana-North-Africa-Arabia", "JO": "Gondwana-North-Africa-Arabia",
    "OM": "Gondwana-North-Africa-Arabia", "IR": "Gondwana-North-Africa-Arabia", "AF": "multiple",
    "AR": "Gondwana-South-America", "BO": "Gondwana-South-America", "BR": "Gondwana-South-America",
    "PE": "Gondwana-South-America", "PY": "Gondwana-South-America", "CO": "Gondwana-South-America",
    "VE": "Gondwana-South-America", "CL": "Gondwana-South-America",
    "AU": "Gondwana-Australia-Antarctica", "NZ": "Gondwana-Australia-Antarctica", "AQ": "Gondwana-Australia-Antarctica",
    "ZA": "Gondwana-other", "IN": "Gondwana-other", "MY": "Gondwana-other", "TH": "Gondwana-other", "MM": "Gondwana-other",
    "VN": "multiple", "KZ": "Kazakhstania", "KG": "multiple", "TJ": "multiple", "UZ": "multiple", "MN": "multiple",
    "KR": "North-China", "KP": "North-China", "JP": "multiple",
}
UK = {"Scotland": "Laurentia", "England": "Avalonia", "Wales": "Avalonia"}
CHINA = {"Xinjiang": "Tarim", "Inner Mongolia": "North-China", "Hebei": "North-China", "Shanxi": "North-China",
         "Shandong": "North-China", "Liaoning": "North-China", "Ningxia": "North-China", "Henan": "North-China",
         "Beijing": "North-China", "Tianjin": "North-China", "Jilin": "North-China"}


def unit_of(cc, state):
    if cc == "UK":
        return UK.get(state.strip(), "multiple")
    if cc == "CN":
        return CHINA.get(state.strip(), "South-China" if state.strip() in {
            "Yunnan", "Guizhou", "Sichuan", "Chongqing", "Hunan", "Hubei", "Guangxi", "Jiangxi", "Zhejiang", "Anhui",
            "Jiangsu", "Guangdong", "Fujian"} else "multiple")
    return UNIT_BY_CC.get(cc, "unknown")


def cmd_effort(pbdb_csv):
    st = sorted(csv.DictReader(open(ROOT / "data" / "timescale.csv")), key=lambda r: -float(r["base_ma"]))
    spans = [(r["stage"], float(r["base_ma"]), float(st[k + 1]["base_ma"]) if k + 1 < len(st) else 0.0) for k, r in enumerate(st)]
    keep = [s for s in spans if 393.47 < s[1] <= 469.4]
    rows = list(csv.reader(open(pbdb_csv)))
    h = rows[0]
    ix = {k: h.index(k) for k in ("max_ma", "min_ma", "environment", "cc", "state")}
    acc = {}
    for r in rows[1:]:
        try:
            hi, lo = float(r[ix["max_ma"]]), float(r[ix["min_ma"]])
        except ValueError:
            continue
        env = r[ix["environment"]]
        cls = "land" if env in LAND else "marginal" if env in MARGINAL else "marine" if env else "unknown"
        unit = unit_of(r[ix["cc"]], r[ix["state"]])
        width = max(hi - lo, 1e-6)
        for name, base, top in keep:
            ov = min(hi, base) - max(lo, top)
            if ov > 0:
                a = acc.setdefault((unit, name, base), {"land": 0.0, "marginal": 0.0, "marine": 0.0, "unknown": 0.0})
                a[cls] += ov / width
    out = []
    for (unit, name, base), a in acc.items():
        out.append({"channel": "body", "palaeo_unit": unit, "stage": name, "base_ma": f"{base:.2f}",
                    "measure": "PBDB collections, all taxa, apportioned by age overlap",
                    "land": f"{a['land']:.2f}", "marginal": f"{a['marginal']:.2f}", "marine": f"{a['marine']:.2f}",
                    "unknown": f"{a['unknown']:.2f}", "n_docs": "", "n_docs_with_spores": ""})
    for r in csv.DictReader(open(SPORES / "effort_by_stage.csv")):
        if 393.47 < float(r["base_ma"]) <= 469.4:
            out.append({"channel": "spore", "palaeo_unit": r["palaeo_unit"], "stage": r["stage"], "base_ma": r["base_ma"],
                        "measure": "Palynodata documents with datable palynomorph records (to 2006)",
                        "land": "", "marginal": "", "marine": "", "unknown": "",
                        "n_docs": r["n_docs"], "n_docs_with_spores": r["n_docs_with_spores"]})
    out.sort(key=lambda r: (r["channel"], r["palaeo_unit"], -float(r["base_ma"])))
    write("effort.csv", ["channel", "palaeo_unit", "stage", "base_ma", "measure", "land", "marginal", "marine", "unknown",
                         "n_docs", "n_docs_with_spores"], out)
    print(f"effort: {len(out)} rows")


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def cmd_check():
    st = stages()
    obs = read("observations.csv", OBS_COLS)
    ints = read("interpretations.csv", INT_COLS)
    srcs = {r["source_id"] for r in read("sources.csv", SRC_COLS)}
    ids = {o["obs_id"] for o in obs}
    problems = []
    for o in obs:
        if o["channel"] not in ("spore", "megafossil", "mesofossil"):
            problems.append(f"{o['obs_id']}: channel {o['channel']!r}")
        if not set(filter(None, o["events"].split(";"))) <= EVENTS:
            problems.append(f"{o['obs_id']}: events {o['events']!r}")
        for s in filter(None, (x.strip() for x in o["source_ids"].split(";"))):
            if s not in srcs:
                problems.append(f"{o['obs_id']}: source {s!r} not in sources.csv")
        if o["same_material_as"] and o["same_material_as"] not in ids:
            problems.append(f"{o['obs_id']}: same_material_as {o['same_material_as']!r} unknown")
    mains = {}
    cache = {}
    for i in ints:
        tag = i["interp_id"]
        if i["obs_id"] not in ids:
            problems.append(f"{tag}: unknown obs_id {i['obs_id']!r}")
        if i["main"] == "true":
            mains[i["obs_id"]] = mains.get(i["obs_id"], 0) + 1
        for k in ("stage_oldest", "stage_youngest"):
            if i[k] not in st:
                problems.append(f"{tag}: {k} {i[k]!r} not in timescale")
        if i["stage_oldest"] in st and i["stage_youngest"] in st and \
                float(st[i["stage_oldest"]]["base_ma"]) < float(st[i["stage_youngest"]]["base_ma"]):
            problems.append(f"{tag}: stage range reversed")
        if not set(filter(None, i["counts_for"].split(";"))) <= EVENTS:
            problems.append(f"{tag}: counts_for {i['counts_for']!r}")
        if i["checked"] not in CHECKED:
            problems.append(f"{tag}: checked {i['checked']!r}")
        path = ROOT / i["support_from"]
        if i["support"] and i["checked"] in ("card", "repo-doc") and path.is_file():
            text = cache.setdefault(path, norm(path.read_text(errors="replace")))
            if norm(i["support"]) not in text:
                problems.append(f"{tag}: support not found verbatim in {i['support_from']}")
    for oid in ids:
        if mains.get(oid, 0) != 1:
            problems.append(f"{oid}: {mains.get(oid, 0)} main interpretations")
    for p in problems:
        print(p)
    print(f"{len(obs)} observations, {len(ints)} interpretations, {len(srcs)} sources; {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "spores":
        cmd_spores()
    elif cmd == "import":
        cmd_import(sys.argv[2:])
    elif cmd == "effort":
        cmd_effort(sys.argv[2])
    elif cmd == "check":
        sys.exit(cmd_check())
    else:
        sys.exit(__doc__)
