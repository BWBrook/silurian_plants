import argparse
import ast
import csv
import hashlib
import json
import re
import statistics
import subprocess
import unicodedata
import zipfile
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ZIP_SHA = "5460e39df359db91ae16e8bff7d156f9f190901af9505d838b26dee8cc70db1a"
MDB_SHA = "eb1fa8c3b2f8a1e06a31e2194846ae541ac5240338b4194f63b00823ccde85c1"
WINDOW_TERMS = re.compile(
    r"cambr|tommot|atdaban|botom|toyon|merionet|menevi|solvan|caerfai|comley|acadian|potsdam|"
    r"dresbach|francon|trempeal|furong|miaoling|terreneuv|ordovic|tremado|arenig|llanvirn|llandeilo|caradoc|ashgill|hirnant|katian|sandbian|darriwil|"
    r"dapingian|floian|whiterock|silurian|gothland|llandover|wenlock|ludlo|pridol|downton|devonian|"
    r"gedinn|lochkov|siegen|prag|emsian|eifel|givet|dittonian|breconian", re.I)
CAMBRIAN_FAMILIES = (
    "Cambrian", "Acadian", "Atdabanian", "Botomian", "Toyonan", "Merioneth",
    "Potsdamian", "Solvan", "Tommotian", "Dresbachian", "Franconian", "Trempealeauan",
)
AGE_PREFIX = r"(?:(?:[EML]\.)|(?:Early |Middle |Late ))?"
CAMBRIAN_RE = re.compile(AGE_PREFIX + r"(?:" + "|".join(CAMBRIAN_FAMILIES) + r")$")
EXPLICIT_CAMBRIAN_RE = re.compile(AGE_PREFIX + r"Cambrian$")
TREMADOC_RE = re.compile(AGE_PREFIX + r"Tremadocian$")
MATCHES = [
    ("balme1961", "Samphire", "03280", "1961", "Palynological examination of samples from Samphire Marsh No.1."),
    ("strother1996", "Saudi Hanadir", "18701", "1996", "New evidence for land plants from the Lower Middle Ordovician of Saudi Arabia"),
    ("steemanspereira2002", "Paraguay", "21733", "2002", "Llandovery miospore biostratigraphy and stratigraphic evolution of the Paraná Basin, Paraguay – Palaeogeographic implications."),
    ("grahn2000", "Paraguay companion", "20806", "2000", "Silurian and Lower Devonian chitinoan biostratigraphy of the Parana Basin in Brazil and Paraguay."),
    ("edwardsfeehan1980", "M3 Irish Cooksonia primary", "09667", "1980", "Records of Cooksonia-Type Sporangia from Late Wenlock strata in Ireland."),
    ("edwardsfeehansmith1983", "M3 Irish Cooksonia companion", "16937", "1983", "A Late Wenlock flora from County Tipperary, Ireland."),
]
POST2006 = [
    ("strother2016", "Cambrian Tennessee", 2016, "Systematics and evolutionary significance of some new cryptospores from the Cambrian of eastern Tennessee, USA"),
    ("wang2022", "Cambrian Shandong", 2022, "A palynological assemblage from the Cambrian (Series 2, Stage 4) of Shandong Province, China, and its implications to the transition from algae to land plants"),
    ("rubinstein2010", "Argentine Dapingian", 2010, "Early Middle Ordovician evidence for land plants in Argentina (eastern Gondwana)"),
    ("rubinstein2011", "Argentine Dapingian companion", 2011, "Biostratigraphy and paleoenvironmental characterization of the Middle Ordovician from the Sierras Subandinas (NW Argentina) based on organic-walled microfossils and sequence stratigraphy"),
    ("strother2015", "Saudi Hanadir and Argentine reassessment", 2015, "Cryptospores from the Hanadir Shale Member of the Qasim Formation, Ordovician (Darriwilian) of Saudi Arabia: taxonomy and systematics"),
    ("wellman2015", "Saudi Qusaiba", 2015, "Spore assemblages from Upper Ordovician and lowermost Silurian sediments recovered from the Qusaiba-1 shallow core hole, Qasim region, central Saudi Arabia"),
    ("steemans2009a", "Saudi Qusaiba preliminary account", 2009, "Origin and Radiation of the Earliest Vascular Land Plants"),
    ("leherisse2015", "Saudi Qusaiba companion", 2015, "Late Ordovician to early Silurian acritarchs from the Qusaiba-1 shallow core hole, central Saudi Arabia"),
    ("strother2021", "Samphire reassessment", 2021, "A fossil record of land plant origins from charophyte algae"),
    ("libertin2018", "M3 Cooksonia barrandei primary", 2018, "Sporophytes of polysporangiate land plants from the early Silurian period may have been photosynthetically autonomous"),
]


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write(path, rows, fields=None):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields or list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def docnum(value):
    value = (value or "").strip()
    return str(int(value)) if value.isdigit() else value


def normalise(value):
    return re.sub(r"[^a-z0-9]", "", unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode().lower())


def window(row):
    try:
        a, b = float(row["agestart"]), float(row["ageend"])
        old, young = max(a, b), min(a, b)
        return old > 383 and young < 600, "numeric_overlap", old, young
    except ValueError:
        return bool(WINDOW_TERMS.search(" ".join(row[c] for c in ("oldage", "youngage", "tage")))), "age_name_only", None, None


def groups(labels):
    cambrian = any(CAMBRIAN_RE.fullmatch(x) for x in labels)
    tremadoc = any(TREMADOC_RE.fullmatch(x) for x in labels)
    explicit = any(EXPLICIT_CAMBRIAN_RE.fullmatch(x) for x in labels)
    result = []
    if explicit:
        result.append("cambrian_explicit_endpoint")
    if cambrian and not explicit:
        result.append("cambrian_regional_endpoint_without_explicit_Cambrian")
    if cambrian:
        result.append("cambrian_any_named_endpoint")
    if tremadoc:
        result.append("tremadocian_any_named_endpoint")
    if cambrian or tremadoc:
        result.append("cambrian_or_tremadocian_any_named_endpoint")
    if cambrian and tremadoc:
        result.append("cambrian_tremadocian_cross_range")
    if labels and all(CAMBRIAN_RE.fullmatch(x) for x in labels):
        result.append("cambrian_only_populated_endpoints")
    if labels and all(TREMADOC_RE.fullmatch(x) for x in labels):
        result.append("tremadocian_only_populated_endpoints")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", type=Path, default=Path("/Users/bwbrook/papers/silurian_plants"))
    ap.add_argument("--out", type=Path, default=Path(__file__).resolve().parent)
    args = ap.parse_args()
    repo, out = args.repo.resolve(), args.out.resolve()
    raw, regenerated = out / "raw", out / "regenerated"
    raw.mkdir(parents=True, exist_ok=True)
    regenerated.mkdir(exist_ok=True)
    external = repo / "data/external"
    source_zip = external / "local/spores/of_5793.zip"
    source_script = external / "scripts/spores_palynodata.py"
    hashes = []
    derivative_names = ["palynodata_taxon_window.csv", "palynodata_documents_window.csv", "palynodata_lithostr_window.csv",
                        "palynodata_theagetable.csv", "palynodata_agetable.csv", "palynodata_age_change.csv", "palynodata_taxloc.csv", "palynodata_codes.csv"]
    inputs = [source_zip, source_script, repo / "docs/sprint2-source-roster.md", external / "spores/README.md",
              external / "spores/MANIFEST.tsv"] + [external / "spores" / name for name in derivative_names]
    before = {str(p): sha(p) for p in inputs}
    assert before[str(source_zip)] == ZIP_SHA
    with zipfile.ZipFile(source_zip) as z:
        (raw / "Paly.CAB").write_bytes(z.read("apps/Paly.CAB"))
    subprocess.run(["bsdtar", "-xf", str(raw / "Paly.CAB"), "-C", str(raw), "paly.mdb"], check=True)
    assert sha(raw / "paly.mdb") == MDB_SHA
    tables = ("TAXON", "NewEng", "LITHOSTR", "THEAGETABLE", "agetable", "AGE_CHANGE", "TAXLOC")
    for table in tables:
        with open(raw / f"{table}.csv", "w", encoding="utf-8") as f:
            subprocess.run(["mdb-export", str(raw / "paly.mdb"), table], stdout=f, check=True)
    docs = read(raw / "NewEng.csv")
    citations = {docnum(r["AUTHDOCNUM"]): r for r in docs}
    assert len(citations) == len(docs)
    target_ids = {docnum(m[2]) for m in MATCHES}
    matched_rows = defaultdict(list)
    full_by_doc, window_by_doc = defaultdict(Counter), defaultdict(Counter)
    full_types = Counter()
    age_labels = Counter()
    coverage = defaultdict(Counter)
    coverage_docs = defaultdict(set)
    coverage_by_doc = defaultdict(Counter)
    full_n = window_n = 0
    derived = ["derived_window_basis", "derived_old_ma", "derived_young_ma", "derived_span_myr",
               "derived_fully_inside_window", "derived_docnum"]
    with open(raw / "TAXON.csv", newline="", encoding="utf-8") as f, open(regenerated / "palynodata_taxon_window.csv", "w", newline="", encoding="utf-8") as dest:
        reader = csv.DictReader(f)
        w = csv.DictWriter(dest, reader.fieldnames + derived, lineterminator="\n")
        w.writeheader()
        for r in reader:
            full_n += 1
            did, tmic = docnum(r["TDOC"]), r["TMIC"]
            full_types[tmic] += 1
            full_by_doc[did][tmic] += 1
            if did in target_ids:
                matched_rows[did].append(dict(r))
            labels = {r[c].strip() for c in ("oldage", "youngage", "tage") if r[c].strip()}
            age_labels.update(labels)
            selected = groups(labels)
            hit, basis, old, young = window(r)
            for group in selected:
                coverage[("full_release", group)][tmic] += 1
                coverage_docs[("full_release", group, tmic)].add(did)
                coverage_docs[("full_release", group, "ALL")].add(did)
                coverage_by_doc[(group, did)][tmic] += 1
                if hit:
                    coverage[("held_window", group)][tmic] += 1
                    coverage_docs[("held_window", group, tmic)].add(did)
                    coverage_docs[("held_window", group, "ALL")].add(did)
            if hit:
                window_n += 1
                window_by_doc[did][tmic] += 1
                r.update(derived_window_basis=basis, derived_old_ma="" if old is None else f"{old:g}",
                         derived_young_ma="" if young is None else f"{young:g}",
                         derived_span_myr="" if old is None else f"{old - young:g}",
                         derived_fully_inside_window="" if old is None else str(old <= 600 and young >= 383),
                         derived_docnum=did)
                w.writerow(r)
    types = sorted({t for c in window_by_doc.values() for t in c})
    window_docs = []
    for original in docs:
        did = docnum(original["AUTHDOCNUM"])
        if did not in window_by_doc:
            continue
        r = dict(original)
        for t in types:
            r[f"derived_window_rows_{t or 'blank'}"] = window_by_doc[did].get(t, 0)
        r["derived_window_has_spores"] = window_by_doc[did].get("S", 0) > 0
        window_docs.append(r)
    write(regenerated / "palynodata_documents_window.csv", window_docs)
    lith = [r for r in read(raw / "LITHOSTR.csv") if docnum(r["AUTHDOCNUM"]) in window_by_doc]
    write(regenerated / "palynodata_lithostr_window.csv", lith, ["AUTHDOCNUM", "AUTHSEQNUM", "LITHOSTGR"])
    for table, name in (("THEAGETABLE", "palynodata_theagetable.csv"), ("agetable", "palynodata_agetable.csv"),
                        ("AGE_CHANGE", "palynodata_age_change.csv"), ("TAXLOC", "palynodata_taxloc.csv")):
        write(regenerated / name, read(raw / f"{table}.csv"))
    tree = ast.parse(source_script.read_text())
    codes = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "CODES" for t in n.targets))
    write(regenerated / "palynodata_codes.csv", [dict(zip(("field", "code", "meaning"), r)) for r in codes])
    tmic_meaning = {code: meaning for field, code, meaning in codes if field == "TMIC"}
    for p in inputs:
        current = sha(p)
        assert current == before[str(p)], f"Input changed during census: {p}"
        fresh = regenerated / p.name
        hashes.append(dict(path=str(p), bytes=p.stat().st_size, sha256=current,
                           comparison="independently regenerated from verified archive" if fresh.exists() else "captured input",
                           regenerated_sha256=sha(fresh) if fresh.exists() else "",
                           identical_to_regenerated=sha(fresh) == current if fresh.exists() else ""))
    for p, expected in ((source_zip, ZIP_SHA), (raw / "paly.mdb", MDB_SHA)):
        hashes.append(dict(path=str(p), bytes=p.stat().st_size, sha256=sha(p), comparison="extractor pinned expected checksum",
                           regenerated_sha256=expected, identical_to_regenerated=sha(p) == expected))
    write(out / "hashes.csv", hashes)

    roster, roster_tmic, intervals = [], [], []
    for key, workstream, raw_id, year, title in MATCHES:
        did = docnum(raw_id)
        doc = citations[did]
        assert doc["PALYDATE"] == year and normalise(doc["ENGTITLE"]) == normalise(title), (key, doc)
        rr = matched_rows[did]
        ages = Counter((r["oldage"], r["youngage"], r["agestart"], r["ageend"]) for r in rr)
        numeric = []
        for old_label, young_label, a, b in ages:
            try:
                numeric.append((max(float(a), float(b)), min(float(a), float(b))))
            except ValueError:
                pass
        span = [o - y for o, y in numeric]
        roster.append(dict(source_key=key, workstream=workstream, document_id=doc["AUTHDOCNUM"], year=year,
                           authors=doc["Author"], title=doc["ENGTITLE"], journal=doc["Journal"], pages=doc["Pages"],
                           taxon_rows_full=sum(full_by_doc[did].values()), taxon_rows_window=sum(window_by_doc[did].values()),
                           spore_or_pollen_rows_full=full_by_doc[did].get("S", 0), unique_regions=len({r["TLOC"] for r in rr}),
                           unique_age_intervals=len(ages), oldest_legacy_ma=max((o for o, y in numeric), default=""),
                           youngest_legacy_ma=min((y for o, y in numeric), default=""),
                           min_unique_interval_span_ma=min(span, default=""), median_unique_interval_span_ma=statistics.median(span) if span else "",
                           max_unique_interval_span_ma=max(span, default=""),
                           original_age_labels="; ".join(sorted({r[c] for r in rr for c in ("oldage", "youngage", "tage") if r[c]})),
                           grain="taxon mention by document and textual region with age interval; no material/sample identifier"))
        for t in sorted(full_by_doc[did]):
            roster_tmic.append(dict(source_key=key, document_id=raw_id, TMIC=t, meaning=tmic_meaning.get(t, ""),
                                    rows_full=full_by_doc[did][t], rows_window=window_by_doc[did].get(t, 0)))
        for (old_label, young_label, a, b), n in sorted(ages.items()):
            intervals.append(dict(source_key=key, document_id=raw_id, oldage=old_label, youngage=young_label,
                                  agestart_legacy=a, ageend_legacy=b, taxon_rows=n))
    write(out / "roster_documents.csv", roster)
    write(out / "roster_tmic_counts.csv", roster_tmic)
    write(out / "roster_age_intervals.csv", intervals)
    write(out / "roster_taxon_rows.csv", [dict(source_key=m[0], **r) for m in MATCHES for r in matched_rows[docnum(m[2])]])
    unmatched = []
    for key, workstream, year, title in POST2006:
        found = [r for r in docs if normalise(r["ENGTITLE"]) == normalise(title)]
        assert not found, (key, found)
        unmatched.append(dict(source_key=key, workstream=workstream, year=year, title=title,
                              matched_document_ids="", status="no exact title match in full NewEng; publication postdates 2006 release coverage",
                              supplement_rule="supplements/reassessments are not inferred to be indexed through an older material source"))
    write(out / "roster_post2006_unmatched.csv", unmatched)

    summaries = []
    for (scope, group), counts in sorted(coverage.items()):
        for t in ["ALL"] + sorted(counts):
            summaries.append(dict(scope=scope, selection=group, TMIC=t, meaning="all indexed types" if t == "ALL" else tmic_meaning.get(t, ""),
                                  taxon_rows=sum(counts.values()) if t == "ALL" else counts[t],
                                  documents=len(coverage_docs[(scope, group, t)])))
    write(out / "legacy_coverage_summary.csv", summaries)
    perdoc = []
    for (group, did), counts in sorted(coverage_by_doc.items()):
        d = citations[did]
        perdoc.append(dict(selection=group, document_id=d["AUTHDOCNUM"], year=d["PALYDATE"], authors=d["Author"],
                           title=d["ENGTITLE"], taxon_rows=sum(counts.values()), spore_or_pollen_rows=counts.get("S", 0),
                           counts_by_TMIC=json.dumps(dict(sorted(counts.items())))))
    write(out / "legacy_document_coverage.csv", perdoc)
    agetable = {r["age_name"]: r for r in read(raw / "agetable.csv")}
    label_rows = []
    all_labels = set(age_labels) | set(agetable)
    for label in sorted(all_labels):
        if CAMBRIAN_RE.fullmatch(label) or TREMADOC_RE.fullmatch(label) or re.search("cambr|tremado", label, re.I):
            a = agetable.get(label, {})
            label_rows.append(dict(label=label, selected_group="Cambrian" if CAMBRIAN_RE.fullmatch(label) else "Tremadocian" if TREMADOC_RE.fullmatch(label) else "EXCLUDED",
                                   explicit_Cambrian_word=bool(EXPLICIT_CAMBRIAN_RE.fullmatch(label)),
                                   rows_with_this_label=age_labels[label], legacy_start=a.get("start", ""), legacy_end=a.get("end", "")))
    write(out / "legacy_label_selection.csv", label_rows)
    years = [int(r["PALYDATE"]) for r in docs if re.fullmatch(r"\d{4}", r["PALYDATE"])]
    receipt = dict(created_utc=datetime.now(timezone.utc).isoformat(), repo=str(repo),
                   git_head=subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=repo, text=True).strip(),
                   script_sha256=sha(__file__), archive_sha256=ZIP_SHA, mdb_sha256=MDB_SHA,
                   mdb_export_version=subprocess.check_output(["mdb-export", "--version"], text=True, stderr=subprocess.STDOUT).strip(),
                   full_taxon_rows=full_n, full_citation_documents=len(docs), full_taxon_document_ids=len(full_by_doc),
                   numeric_publication_year_min=min(years), numeric_publication_year_max=max(years),
                   full_TMIC=dict(full_types), window_taxon_rows=window_n, window_documents=len(window_by_doc),
                   derivative_hash_matches={name: sha(external / "spores" / name) == sha(regenerated / name) for name in derivative_names},
                   selected_roster_document_ids=[m[2] for m in MATCHES], post2006_roster_papers=len(POST2006),
                   census_note="Mention/document coverage only. Legacy labels select geological groups; numerical ages are descriptive source values. No sample negatives, taxonomic harmonisation, modern age conversion or admission decisions.")
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))
    print("ROSTER", json.dumps(roster, ensure_ascii=False))
    print("LEGACY ALL", json.dumps([r for r in summaries if r["scope"] == "full_release" and r["TMIC"] in ("ALL", "S")]))


if __name__ == "__main__":
    main()
