"""rockrecord_lexicon.py: BGS Lexicon of Named Rock Units entries for the DiGMapGB-625 Silurian-Devonian LEX codes.

Run on nectar after rockrecord_bgs_polygons.py (stdlib only):  ssh nectar python3 - < rockrecord_lexicon.py
For every LEX code in <raw stamp>/derived/sd_lex_codes.txt, and every ancestor of those codes (and the Old Red Sandstone Supergroup's
children), fetches
  - the linked-data record  https://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/<code>.json   (JSON-LD: ages, rank, status, lithology
    classes and description, boundary definitions, parent, source-info ids), and
  - the Lexicon web page    https://webapps.bgs.ac.uk/lexicon/lexicon.cfm?pub=<code>      (age range, parent, reference list)
and the BGS Geochronology Division records for every age term they use. Raw responses go to <stamp>/lexicon/, with
PROVENANCE_lexicon.tsv (URL, timestamp, licence note, sha256). Parsed tables go to <stamp>/derived/:
  lexicon_entries.csv       one row per Lexicon code fetched
  lexicon_divisions.csv     one row per Geochronology Division used (BGS's own age values)
Plain user agent, one request at a time with a 0.4 s pause; no credentials.
"""
import csv
import datetime
import glob
import hashlib
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) research-data-fetch"
RAW = os.path.dirname(sorted(glob.glob("/data/codex/silurian_plants/raw/bgs/*/bgs_geology_625k_shapefile.zip"))[-1]) + "/"
LEXDIR = RAW + "lexicon/"
DER = RAW + "derived/"
os.makedirs(LEXDIR, exist_ok=True)
LIC = ("no licence statement found on the Lexicon web pages, the linked-data scheme or the BGS Lexicon page (BGS: free access, 'as seen', "
       "UKRI copyright); treat as attribution-required, reuse terms unconfirmed")
NS = "http://data.bgs.ac.uk/ref/Lexicon/"
GNS = "http://data.bgs.ac.uk/ref/Geochronology/"
SKOS = "http://www.w3.org/2004/02/skos/core#"
prov = []


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def fetch(name, url, licence=LIC, tolerate404=True):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code == 404 and tolerate404:
                prov.append([name, url, datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), licence, "0", "", "HTTP 404"])
                time.sleep(0.4)
                return None
            time.sleep(2)
            data = None
        except Exception:
            time.sleep(2)
            data = None
    if data is None:
        raise RuntimeError("failed " + url)
    with open(LEXDIR + name, "wb") as f:
        f.write(data)
    prov.append([name, url, datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), licence, str(len(data)),
                 hashlib.sha256(data).hexdigest(), ""])
    time.sleep(0.4)
    return data


def jv(o, key, ns=NS):
    """list of plain values (strings, numbers) or @id codes for a predicate"""
    out = []
    for x in o.get(ns + key, []):
        if "@value" in x:
            out.append(x["@value"])
        elif "@id" in x:
            out.append(x["@id"])
    return out


def code_of(uri):
    return uri.rsplit("/", 1)[-1]


def parse_json(code, data):
    d = json.loads(data)
    o = [x for x in d if x["@id"].endswith("/NamedRockUnit/" + code)][0]
    lith = sorted({code_of(u) for u in jv(o, "hasLithology")})
    status = [code_of(x["@id"]) for x in o.get("http://purl.org/linked-data/registry#status", [])]
    return dict(
        pref_label=(o.get(SKOS + "prefLabel", [{}])[0].get("@value", "")),
        definition=(o.get(SKOS + "definition", [{}])[0].get("@value", "")),
        alt_labels=" | ".join(x["@value"] for x in o.get(SKOS + "altLabel", [])),
        status=";".join(status),
        rank=";".join(code_of(u) for u in jv(o, "hasRockUnitRank")),
        oldest_div=";".join(code_of(u) for u in jv(o, "hasOldestAge")),
        oldest_ma=";".join(str(x) for x in jv(o, "hasOldestAgeValue")),
        youngest_div=";".join(code_of(u) for u in jv(o, "hasYoungestAge")),
        youngest_ma=";".join(str(x) for x in jv(o, "hasYoungestAgeValue")),
        predominant_div=";".join(code_of(u) for u in jv(o, "hasPredominantAge")),
        broader_predominant_div=";".join(code_of(u) for u in jv(o, "hasBroaderPredominantAge")),
        lithology_classes=";".join(lith),
        lithology_description=" ".join(str(x).strip() for x in jv(o, "hasLithologyDescription")),
        lower_boundary=" ".join(str(x).strip() for x in jv(o, "hasLowerBoundaryDefinition")),
        upper_boundary=" ".join(str(x).strip() for x in jv(o, "hasUpperBoundaryDefinition")),
        thickness=" ".join(str(x).strip() for x in jv(o, "hasThicknessDescription")),
        geographical_distribution=" ".join(str(x).strip() for x in jv(o, "hasGeographicalDistribution")),
        map_notation=";".join(str(x) for x in jv(o, "hasMapNotation")),
        broader=";".join(code_of(x["@id"]) for x in o.get(SKOS + "broader", [])),
        n_narrower=len(o.get(SKOS + "narrower", [])),
        narrower=";".join(code_of(x["@id"]) for x in o.get(SKOS + "narrower", [])),
        obsolete_equivalents=";".join(code_of(u) for u in jv(o, "hasObsoleteEquivalent")),
        is_obsolete_equivalent_of=";".join(code_of(u) for u in jv(o, "isObsoleteEquivalentOf")),
        lateral_equivalents=";".join(code_of(u) for u in jv(o, "hasLateralEquivalent")),
        n_source_info=len(jv(o, "hasSourceInfo")),
        source_info_ids=";".join(code_of(u) for u in jv(o, "hasSourceInfo")),
        n_type_localities=len(jv(o, "hasTypeLocality")),
        n_50k_sheets=len(jv(o, "isContainedBy50kMapSheet")),
    )


def clean(s):
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).replace("\xa0", " ").strip()


def parse_web(data):
    s = data.decode("utf-8", "replace")
    rows = re.findall(r"<tr[^>]*>(.*?)</tr>", s, flags=re.S)
    kv, refs, last = {}, [], None
    for r in rows:
        ths = re.findall(r"<th[^>]*>(.*?)</th>", r, flags=re.S)
        tds = re.findall(r"<td[^>]*>(.*?)</td>", r, flags=re.S)
        if ths:
            for i, t in enumerate(ths):
                lab = clean(t).rstrip(":")
                val = clean(tds[i]) if i < len(tds) else ""
                kv[lab] = val
                last = lab
        elif tds and last == "Reference(s)":
            t = clean(tds[0])
            if not t.lower().startswith("none recorded"):
                refs.append(t)
        elif tds and last and last.startswith("1:50K"):
            kv["maps"] = (kv.get("maps", "") + " " + clean(tds[0])).strip()
    return dict(
        web_status=kv.get("Status Code", ""), web_age_range=kv.get("Age range", ""),
        web_lithological_description=kv.get("Lithological Description", ""),
        web_parent_unit=kv.get("Parent Unit", ""), web_previous_names=kv.get("Previous Name(s)", ""),
        web_alternative_names=kv.get("Alternative Name(s)", ""), web_geographical_limits=kv.get("Geographical Limits", ""),
        web_n_references=len(refs), web_references=" || ".join(refs))


codes = [l.strip() for l in open(DER + "sd_lex_codes.txt") if l.strip()]
entries = {}
todo = list(codes)
ors_children = []
while todo:
    c = todo.pop(0)
    if c in entries:
        continue
    jd = fetch(f"NamedRockUnit_{c}.json", f"https://data.bgs.ac.uk/id/Lexicon/NamedRockUnit/{c}.json")
    wd = fetch(f"lexicon_{c}.html", f"https://webapps.bgs.ac.uk/lexicon/lexicon.cfm?pub={c}")
    e = {"code": c, "in_lod": "yes" if jd else "no", "in_web": "yes" if wd else "no"}
    if jd:
        e.update(parse_json(c, jd))
        for b in e["broader"].split(";"):
            if b and b not in entries:
                todo.append(b)
        if c == "ORS":
            ors_children = [x for x in e["narrower"].split(";") if x]
            for x in ors_children:
                todo.append(x)
    if wd:
        e.update(parse_web(wd))
    entries[c] = e
    log(c, e.get("pref_label", ""), e.get("oldest_ma", ""), e.get("youngest_ma", ""), e.get("status", ""))
log("entries", len(entries), "ORS children", len(ors_children))

# labels of the rank and lithology codes used
def label_of(url_kind, code):
    data = fetch(f"{url_kind.replace('/', '_')}_{code}.json", f"https://data.bgs.ac.uk/id/{url_kind}/{code}.json")
    if not data:
        return ""
    for x in json.loads(data):
        if x["@id"].endswith("/" + code):
            return x.get(SKOS + "prefLabel", x.get("http://www.w3.org/2000/01/rdf-schema#label", [{}]))[0].get("@value", "")
    return ""


rank_codes = sorted({e.get("rank", "") for e in entries.values()} - {""})
lith_codes = sorted({c for e in entries.values() for c in e.get("lithology_classes", "").split(";") if c})
RANKL = {c: label_of("Lexicon/RockUnitRank", c) for c in rank_codes}
LITHL = {c: label_of("EarthMaterialClass/RockClassAll", c) for c in lith_codes}
log("rank labels", RANKL)
log("lithology labels", len(LITHL), "unlabelled", [c for c, v in LITHL.items() if not v])
for e in entries.values():
    e["rank_label"] = RANKL.get(e.get("rank", ""), "")
    e["lithology_labels"] = ";".join(LITHL.get(c, c) for c in e.get("lithology_classes", "").split(";") if c)

# divisions used
divs = set()
for e in entries.values():
    for k in ("oldest_div", "youngest_div", "predominant_div", "broader_predominant_div"):
        for x in e.get(k, "").split(";"):
            if x:
                divs.add(x)
drows = {}
todo = sorted(divs)
while todo:
    d = todo.pop(0)
    if d in drows:
        continue
    data = fetch(f"Division_{d}.json", f"https://data.bgs.ac.uk/id/Geochronology/Division/{d}.json")
    if not data:
        drows[d] = dict(code=d)
        continue
    o = [x for x in json.loads(data) if x["@id"].endswith("/Division/" + d)][0]
    b = [code_of(x["@id"]) for x in o.get(SKOS + "broader", [])]
    drows[d] = dict(code=d, pref_label=o.get(SKOS + "prefLabel", [{}])[0].get("@value", ""),
                    rank=";".join(code_of(u) for u in jv(o, "hasGeochronologyRank", GNS)),
                    max_age_ma=";".join(str(x) for x in jv(o, "maxAgeValue", GNS)),
                    min_age_ma=";".join(str(x) for x in jv(o, "minAgeValue", GNS)),
                    broader=";".join(b),
                    definition=o.get(SKOS + "definition", [{}])[0].get("@value", ""))
    for x in b:
        if x not in drows:
            todo.append(x)
fetch("Geochronology_Division_scheme.ttl", "https://data.bgs.ac.uk/v/vocab/gchrnlgy:Division")
fetch("Lexicon_NamedRockUnit_scheme.ttl", "https://data.bgs.ac.uk/v/vocab/lxcn:NamedRockUnit")
fetch("bgs_lexicon_technology_page.html", "https://www.bgs.ac.uk/technologies/the-bgs-lexicon-of-named-rock-units/")
with open(DER + "lexicon_divisions.csv", "w", newline="", encoding="utf-8") as f:
    cols = ["code", "pref_label", "rank", "max_age_ma", "min_age_ma", "broader", "definition"]
    w = csv.DictWriter(f, cols, lineterminator="\n")
    w.writeheader()
    for d in sorted(drows):
        w.writerow({k: drows[d].get(k, "") for k in cols})

cols = ["code", "in_lod", "in_web", "pref_label", "rank", "rank_label", "status", "web_status", "broader", "web_parent_unit", "oldest_div",
        "oldest_ma", "youngest_div", "youngest_ma", "predominant_div", "broader_predominant_div", "web_age_range", "definition",
        "lithology_classes", "lithology_labels", "lithology_description", "web_lithological_description", "lower_boundary", "upper_boundary", "thickness",
        "geographical_distribution", "map_notation", "alt_labels", "web_previous_names", "web_alternative_names", "obsolete_equivalents",
        "is_obsolete_equivalent_of", "lateral_equivalents", "n_narrower", "narrower", "n_source_info", "source_info_ids",
        "web_n_references", "web_references", "n_type_localities", "n_50k_sheets", "web_geographical_limits"]
with open(DER + "lexicon_entries.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, cols, lineterminator="\n", extrasaction="ignore")
    w.writeheader()
    for c in sorted(entries):
        w.writerow(entries[c])
with open(RAW + "PROVENANCE_lexicon.tsv", "w") as f:
    f.write("file\turl\tretrieved_utc\tlicence\tbytes\tsha256\tnote\n")
    for r in prov:
        f.write("\t".join(r) + "\n")
log("wrote", DER, "divisions", len(drows))
