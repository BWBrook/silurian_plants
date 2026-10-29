#!/usr/bin/env python3
"""Palaeogeography context for 485-383 Ma from EPRP's palaeogeography mirror.

Run on nectar (stdlib plus the pdftotext binary; read-only on the EPRP mirror backup):
    ssh -o BatchMode=yes nectar python3 - < context_palaeogeography.py
Inputs copied beforehand from the EPRP checkout at ac42dfb (read-only there) into
/data/codex/silurian_plants/eprp/context/inputs/ :
    resources/sources/palaeogeography/gplates-models-licences.tsv
    resources/sources/palaeogeography/profile/palaeogeography_profile.tsv
Writes context/plate_models.csv, context/paleodem_slices.csv, context/sources_used_palaeogeography.tsv and
copies the PaleoDEM window slices to local/context/paleodem/ (under /data/codex/silurian_plants/eprp/context/).
"""
import csv, hashlib, json, os, re, subprocess, sys, unicodedata, zipfile

PG = "/data/codex/artifacts/eprp-paleodata-backup/latest/palaeogeography"
RD = "/data/codex/artifacts/eprp-paleodata-backup/latest/register-deposits"
SCR = "/data/codex/silurian_plants/eprp/context"
INP = f"{SCR}/inputs"
OUT = f"{SCR}/context"
LOC = f"{SCR}/local/context/paleodem"
LO, HI = 383.0, 485.0
MODELS = f"{PG}/gplates-models/raw/2026-10-24T0301Z_url"
DEM = f"{PG}/paleomap-paleodem/raw/5460860"
WRIGHT = f"{PG}/wright2013-supplement/raw/2026-10-24T0320Z_url"
os.makedirs(OUT, exist_ok=True)
os.makedirs(LOC, exist_ok=True)

ICS2024 = [
    ("Givetian", 387.95), ("Eifelian", 393.47), ("Emsian", 410.62), ("Pragian", 413.02),
    ("Lochkovian", 419.62), ("Pridoli", 422.7), ("Ludfordian", 425.0), ("Gorstian", 426.7),
    ("Homerian", 430.6), ("Sheinwoodian", 432.9), ("Telychian", 438.6), ("Aeronian", 440.5),
    ("Rhuddanian", 443.1), ("Hirnantian", 445.2), ("Katian", 452.8), ("Sandbian", 458.2),
    ("Darriwilian", 469.4), ("Dapingian", 471.3), ("Floian", 477.1), ("Tremadocian", 486.85),
]
SERIES = {"ludlow": {"gorstian", "ludfordian"}, "wenlock": {"sheinwoodian", "homerian"},
          "llandovery": {"rhuddanian", "aeronian", "telychian"}}
ALIAS = {"tremadoc": "tremadocian", "darwillian": "darriwilian"}


def stage_ics2024(age):
    if age > ICS2024[-1][1]:
        return "older_than_Tremadocian_base"
    best = None
    for name, base in ICS2024:
        if base >= age and (best is None or base < best[1]):
            best = (name, base)
    return "Givetian_or_younger" if best[0] == "Givetian" and age < 387.95 else best[0]


def label_stages(label):
    t = unicodedata.normalize("NFKD", label or "").encode("ascii", "ignore").decode().lower().strip()
    t = re.sub(r"\b(l|e|m|late|early|middle|mid)\.?\s+", "", t)
    out = set()
    for part in re.split(r"[/&,]| and ", t):
        part = re.sub(r"\s*boundary", "", part.strip())
        part = ALIAS.get(part, part)
        out |= SERIES.get(part, {part} if part else set())
    known = {n.lower() for n, _ in ICS2024} | {"frasnian"} | set().union(*SERIES.values())
    return (out & known) or None


def label_differs(label, derived):
    allowed = label_stages(label)
    if allowed is None:
        return ""
    if derived == "Givetian_or_younger":
        return "0" if allowed & {"givetian", "frasnian"} else "1"
    return "0" if derived.lower() in allowed else "1"


def sha256(path_or_bytes):
    h = hashlib.sha256()
    if isinstance(path_or_bytes, bytes):
        h.update(path_or_bytes)
    else:
        with open(path_or_bytes, "rb") as f:
            for c in iter(lambda: f.read(1 << 20), b""):
                h.update(c)
    return h.hexdigest()


_MC = {}


def manifest_entries(d):
    if d not in _MC:
        with open(os.path.join(d, "MANIFEST.json"), encoding="utf-8") as f:
            _MC[d] = {e["key"]: e.get("sha256", "") for e in json.load(f)["files"]}
    return _MC[d]


USED = []


def use(d, key, manifest=None):
    p = os.path.join(d, key)
    s = sha256(p)
    ms = (manifest or manifest_entries(d)).get(key, "")
    USED.append([os.path.basename(d.rstrip("/")), key, p, os.path.getsize(p), s, ms,
                 "match" if s == ms else ("no-manifest-sha" if not ms else "MISMATCH")])
    return p


def read_tsv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.reader(f, delimiter="\t", quoting=csv.QUOTE_NONE))


# ------------------------------------------------------------ plate models
index_path = use(MODELS, "models.json")
index = json.load(open(index_path, encoding="utf-8"))
lic = {r[0]: r for r in read_tsv(f"{INP}/gplates-models-licences.tsv")[1:]}
prof = {}
for r in read_tsv(f"{INP}/palaeogeography_profile.tsv")[1:]:
    if len(r) >= 4 and r[0] == "models" and r[1] in index:
        prof[r[1]] = r[3].split("; ")  # rotation files; poles; moving plates; oldest pole (Ma); static polygons
aliases = {}
for k, v in index.items():
    if isinstance(v, str) and v.startswith("@"):
        aliases.setdefault(v[1:], []).append(k)
PBDB = {
    "wright2013": "PBDB 'gplates' palaeocoordinates (EPRP: plate IDs agree on 99.5-100% of collections)",
    "paleomap": "PBDB 'scotese' palaeocoordinates (EPRP matches it and scotese_and_wright2018; the rotation file here is the 2016 one, PBDB cites Scotese 2021)",
    "scotese_and_wright2018": "PBDB 'scotese' palaeocoordinates (see paleomap; its rotation file is byte-identical to paleomap's, observed)",
    "seton2012": "PBDB 'seton' palaeocoordinates; NSB palaeocoordinates (reproduced: 99.9% within 0.5 deg)",
    "matthews2016_mantle_ref": "Triton palaeocoordinates (mantle frame; 90.8% within 0.5 deg); NOT PBDB's default (plate IDs agree on 60.3% of PBDB collections)",
    "zahirovic2022": "default model of the GPlates Plate Model Manager index, not PBDB's",
}
EPRP_NOTES = {
    "alfonso2024": "Pole times to 3,000 Ma in the rotation file are placeholders (identity or frozen copies of the last in-range pole), far beyond the index range of 170 Ma. Index: PMAG frame via anchor plate 701701.",
    "clennett2020_m2019": "Pole times to 3,000 Ma are placeholders beyond the index range (170 Ma).",
    "muller2019": "Pole times to 3,000 Ma are placeholders beyond the index range (250 Ma).",
    "zahirovic2016": "Pole times to 3,000 Ma are placeholders beyond the index range (230 Ma).",
    "zahirovic2022": "Pole times to 3,000 Ma are placeholders beyond the index range (410 Ma). Default model of the index. Index: PMAG frame via anchor plate 701701.",
    "cao2024": "Poles to 2,100 Ma against an index range of 1,800 Ma.",
    "muller2025": "Poles to 2,100 Ma against an index range of 1,800 Ma; alias shirmard2025.",
    "muller2022": "Merdith et al. 2021 relative motions in a mantle reference frame; Paleozoic palaeolatitude and palaeolongitude diverge progressively from merdith2021 (index description).",
    "merdith2021": "Palaeomagnetic reference frame: longitudes unconstrained (index description). Combines Muller 2016 (0-230 Ma), Matthews 2016 pmag (250-410 Ma) and new earlier reconstruction.",
    "matthews2016_mantle_ref": "Mantle-frame variant of matthews2016_pmag_ref; alias matthews2016. Reference frame matters as much as the model: Triton palaeolatitudes match the mantle frame (90.8% within 0.5 deg) and the pmag frame only 31.9%.",
    "matthews2016_pmag_ref": "Palaeomagnetic-frame variant; builds on Domeier & Torsvik (2014) for 410-250 Ma. No licence stated in the index.",
    "domeier2014": "Index range 250-410 Ma only; poles to 2,000 Ma in the file. Index gives no source and no licence.",
    "young2018": "410-0 Ma global model with subduction zones.",
    "torsvikcocks2017": "Index range 0-540 Ma, coastlines and static polygons only (no topologies). No licence stated in the index.",
    "golonka": "Coastlines and static polygons only; its rotation file is named Phanerozoic_EarthByte.rot like Wright et al. 2013's and has the same pole statistics (max age, poles and plates in the window), but the files differ in bytes (observed). No licence stated in the index.",
    "paleomap": "PALEOMAP PaleoAtlas for GPlates (2016 rotation file; byte-identical to scotese_and_wright2018's, observed); alias scotese2016. Index range 0-750 Ma.",
    "scotese_and_wright2018": "Index range 0-540 Ma; has topologies and continental polygons. Observed: the rotation file header reads 'PALEOMAP Plate Model m15g60_v2d3'; the PaleoDEM report says to use the table's 'plate tectonic model age' with PALEOMAP Global Plate Model v2d3 in GPlates.",
    "rodinia": "Index range 530-1,100 Ma; does not reach the window; alias li2008. No licence stated in the index.",
    "muller2008": "Static polygons and rotations only; alias li2008 is NOT this model (li2008 -> rodinia). No licence stated in the index.",
    "seton2012": "0-200 Ma; PBDB 'seton' and NSB model.",
}


POLE = re.compile(r"^\s*(\d+)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(\d+)")


def scan_rot(name, raw, st):
    st["files"].append(f"{os.path.basename(name)} ({len(raw)} B, sha256 {sha256(raw)[:12]})")
    for line in raw.decode("latin-1").splitlines():
        m = POLE.match(line)
        if not m:
            continue
        plate, age, ang = m.group(1), float(m.group(2)), float(m.group(5))
        st["n"] += 1
        st["max"] = max(st["max"], age)
        if LO <= age <= HI:
            st["win_poles"] += 1
            if ang != 0.0:
                st["win_plates"].add(plate)
        if age >= HI and ang != 0.0:
            st["old_plates"].add(plate)


def parse_rot(zpath, member=None):
    """Aggregate pole statistics over every .rot file in a rotation zip (or one named member)."""
    st = {"max": 0.0, "n": 0, "win_poles": 0, "win_plates": set(), "old_plates": set(), "files": []}
    with zipfile.ZipFile(zpath) as z:
        for info in z.infolist():
            if (member and info.filename == member) or (not member and info.filename.lower().endswith((".rot", ".grot"))):
                scan_rot(info.filename, z.read(info.filename), st)
    return st


def coverage(small, big):
    if small <= LO and big >= HI:
        return "full"
    if big > LO and small < HI:
        return f"partial ({max(small, LO):g}-{min(big, HI):g} Ma only)"
    return "no"


rows = []
for name, v in index.items():
    if isinstance(v, str):
        continue
    small, big = float(v["SmallTime"]), float(v["BigTime"])
    zips = sorted(f for f in os.listdir(MODELS) if f.startswith(name + "__"))
    rot = parse_rot(f"{MODELS}/{name}__Rotations.zip") if f"{name}__Rotations.zip" in zips else None
    for z in zips:
        use(MODELS, z)
    L = lic.get(name, [name, "", "not stated", "", ""])
    pf = prof.get(name, ["", "", "", "", ""])
    rows.append([
        name, ";".join(sorted(aliases.get(name, []))), L[4], L[1], v.get("Version", ""), v.get("URL", ""),
        f"{small:g}", f"{big:g}", coverage(small, big), pf[3],
        str(rot["win_poles"]) if rot else "", str(len(rot["win_plates"])) if rot else "",
        str(len(rot["old_plates"])) if rot else "", f"{rot['max']:g}" if rot else "",
        ("yes" if rot["max"] > big else "no") if rot else "",
        ";".join(v.get("Layers", {})), "yes" if "TimeDepRasters" in v else "no",
        L[2], L[3], f"{MODELS}/{name}__*.zip", "; ".join(rot["files"]) if rot else "",
        PBDB.get(name, ""), EPRP_NOTES.get(name, ""),
        re.sub(r"\s*See the 'URL' below for more details\.", "", v.get("Description", "")),
    ])

# Wright et al. 2013 (PBDB's default 'gplates' model), not in the GPlates index
wz = use(WRIGHT, "bg-10-1529-2013-supplement.zip")
member = "SupplementaryMaterial/1_Phanerozoic_Plate_Motions_GPlates/Phanerozoic_EarthByte.rot"
wr = parse_rot(wz, member)
rows.append([
    "wright2013", "", "Wright et al. 2013 supplement: Phanerozoic EarthByte rotation file, coastlines and continental regions (GPlates)",
    "", "doi:10.5194/bg-10-1529-2013", "https://doi.org/10.5194/bg-10-1529-2013",
    "", "", "full (poles in the rotation file; no index range)", "",
    str(wr["win_poles"]), str(len(wr["win_plates"])), str(len(wr["old_plates"])), f"{wr['max']:g}", "n/a",
    "Coastlines;ContinentalRegions (no static polygons)", "no", "CC BY 3.0 (EPRP snapshots.tsv)", "",
    f"{WRIGHT}/bg-10-1529-2013-supplement.zip (member {member})",
    "; ".join(wr["files"]),
    PBDB["wright2013"],
    "NOT one of the 26 index models. PBDB's default palaeocoordinate model. EPRP profiler assigns plates from its continental regions (no static polygons) and reproduces PBDB plate IDs on 99.9% of collections; positions match PBDB within 1 deg for 98-99.7% of collections under 100 Ma but only 75-92% from 100 Ma (probably later rotation-file versions in PBDB; unresolved).",
    "Supplement of the model PBDB calls 'gplates'.",
])
HEADER = ["model", "aliases_in_index", "reference_title_eprp_licence_file", "zenodo_record_eprp", "doi_index_version",
          "index_url", "index_small_time_ma", "index_big_time_ma", "covers_485_383_ma_by_index", "oldest_pole_ma_eprp_profile",
          "derived_rot_poles_with_age_383_485", "derived_rot_plates_nonidentity_pole_383_485",
          "derived_rot_plates_nonidentity_pole_485_plus", "derived_rot_max_pole_age_ma",
          "derived_rot_max_pole_exceeds_index_range", "layers_in_index",
          "time_dependent_rasters_in_index", "licence_eprp", "licence_published_eprp", "deep_server_path",
          "rotation_files_in_zip", "pbdb_or_other_eprp_use", "eprp_notes", "index_description"]
rows.sort(key=lambda r: (r[8].startswith("no"), r[8].startswith("partial"), r[0]))
with open(f"{OUT}/plate_models.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(HEADER)
    w.writerows(rows)
print("plate_models.csv:", len(rows), "rows;", sum(1 for r in rows if r[8].startswith("full")), "full,",
      sum(1 for r in rows if r[8].startswith("partial")), "partial,", sum(1 for r in rows if r[8] == "no"), "no")

# ------------------------------------------------------------ PaleoDEM slices
pdf = subprocess.run(["pdftotext", "-layout", f"{DEM}/Scotese_Wright2018_PALEOMAP_PaleoDEMs.pdf", "-"],
                     capture_output=True, text=True, check=True).stdout
use(DEM, "Scotese_Wright2018_PALEOMAP_PaleoDEMs.pdf")
tab = {}
for line in pdf.splitlines():
    m = re.match(r"^\s+(\d+(?:\.\d+)?)\s{2,}(.+?)\s{2,}(\d+)\s*$", line)
    if m and 67 <= float(m.group(1)) <= 83 and float(m.group(1)) in (67.5, 68, 69, 70, 70.5, 71, 72, 73, 74, 75, 75.5, 76,
                                                                      77, 78, 79, 80, 80.5, 81, 81.5, 82, 82.5):
        tab[m.group(1)] = (m.group(2).strip(), int(m.group(3)))
assert len(tab) == 21, sorted(tab)
use(DEM, "PaleoDEMS_long_lat_elev_csv_v2.zip")
use(DEM, "Scotese_Wright_2018_Maps_1-88_1degX1deg_PaleoDEMS_nc.zip")
use(DEM, "Scotese_Wright_2018_Maps_1-88_6minX6min_PaleoDEMS_nc.zip")
SRC = {
    "csv_1deg": ("PaleoDEMS_long_lat_elev_csv_v2.zip", r"\.csv$"),
    "nc_1deg": ("Scotese_Wright_2018_Maps_1-88_1degX1deg_PaleoDEMS_nc.zip", r"\.nc$"),
    "nc_6min": ("Scotese_Wright_2018_Maps_1-88_6minX6min_PaleoDEMS_nc.zip", r"\.nc$"),
}
found = {k: {} for k in SRC}
for fmt, (zn, ext) in SRC.items():
    os.makedirs(f"{LOC}/{fmt}", exist_ok=True)
    with zipfile.ZipFile(f"{DEM}/{zn}") as z:
        for info in z.infolist():
            base = os.path.basename(info.filename)
            if base.startswith("._") or not re.search(ext, base) or info.is_dir():
                continue
            m = re.match(r"^Map(\d+(?:\.\d+)?)_", base)
            if m and m.group(1) in tab:
                dest = f"{LOC}/{fmt}/{base}"
                if not (os.path.exists(dest) and os.path.getsize(dest) == info.file_size):
                    with open(dest, "wb") as f:
                        f.write(z.read(info.filename))
                found[fmt][m.group(1)] = (base, info.file_size, sha256(dest))
BAL = f"{RD}/balembois2025-marine-biodiversity-drivers/raw"
BAL = os.path.join(BAL, os.listdir(BAL)[0])
srows = []
for mid in sorted(tab, key=float):
    desc, pma = tab[mid]
    dm = re.search(r"(?:,|\()\s*([0-9.]+)\s*(?:Ma)?\)", desc)
    dage = float(dm.group(1)) if dm else None
    lab = re.search(r"\(([^,)]+)[,)]", desc)
    row = [mid, str(pma), desc, f"{dage:g}" if dage else "",
           stage_ics2024(pma), stage_ics2024(dage) if dage else "",
           label_differs(lab.group(1), stage_ics2024(dage)) if (lab and dage) else ""]
    for fmt in SRC:
        b = found[fmt].get(mid)
        row += [b[0], str(b[1]), b[2]] if b else ["", "", ""]
    bf = f"{int(dage + 0.5)}Ma_monthly_SST.nc" if dage else ""
    row.append(bf if bf and os.path.exists(os.path.join(BAL, bf)) else "")
    srows.append(row)
hdr = ["map_id", "plate_model_age_ma_pdf_table1", "stratigraphic_age_description_pdf_table1",
       "derived_description_age_ma_parsed", "derived_ics2024_stage_at_plate_model_age",
       "derived_ics2024_stage_at_description_age", "derived_label_differs_at_description_age"]
for fmt in SRC:
    hdr += [f"{fmt}_file", f"{fmt}_bytes", f"{fmt}_sha256"]
hdr.append("derived_balembois2025_hadcm3_sst_file_matched_on_description_age")
with open(f"{OUT}/paleodem_slices.csv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(hdr)
    w.writerows(srows)
print("paleodem_slices.csv:", len(srows), "rows; files copied:", {k: len(v) for k, v in found.items()})
print("bytes copied:", sum(x[1] for d in found.values() for x in d.values()))

with open(f"{OUT}/sources_used_palaeogeography.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["mirror_dir", "file", "deep_server_path", "bytes", "sha256_computed", "sha256_in_mirror_manifest", "check"])
    w.writerows(USED)
bad = [u for u in USED if u[-1] == "MISMATCH"]
print("sources used:", len(USED), "mismatches:", len(bad))
sys.exit(1 if bad else 0)
