#!/usr/bin/env python3
"""Extract Earth-system context series overlapping 485-383 Ma from EPRP's climate-forcing mirror.

Run on deep-server (stdlib only, read-only on /data/paleodata):
    ssh -o BatchMode=yes deep-server python3 - < context_climate.py
Writes to /data/codex/silurian_plants-eprp/context/context/ (redistributable sources) and .../local/context/
(sources with no stated licence or no-derivatives terms); copy back with rsync.
Source: /data/paleodata/climate-forcing (EPRP checkout ac42dfb, catalogue entry climate-forcing).
"""
import csv, hashlib, io, json, math, os, re, sys, unicodedata, zipfile
import xml.etree.ElementTree as ET

MIRROR = "/data/paleodata/climate-forcing"
OUT = "/data/codex/silurian_plants-eprp/context/context"
LOCAL = "/data/codex/silurian_plants-eprp/context/local/context"  # sources with no stated licence or no-derivatives terms
LO, HI = 383.0, 485.0  # window, Ma (inclusive)
os.makedirs(OUT, exist_ok=True)
os.makedirs(LOCAL, exist_ok=True)

# data/timescale.csv of the consuming project (ICS v2024/12): (stage, base_ma, base_unc_ma)
ICS2024 = [
    ("Givetian", 387.95), ("Eifelian", 393.47), ("Emsian", 410.62), ("Pragian", 413.02),
    ("Lochkovian", 419.62), ("Pridoli", 422.7), ("Ludfordian", 425.0), ("Gorstian", 426.7),
    ("Homerian", 430.6), ("Sheinwoodian", 432.9), ("Telychian", 438.6), ("Aeronian", 440.5),
    ("Rhuddanian", 443.1), ("Hirnantian", 445.2), ("Katian", 452.8), ("Sandbian", 458.2),
    ("Darriwilian", 469.4), ("Dapingian", 471.3), ("Floian", 477.1), ("Tremadocian", 486.85),
]
BASE = dict(ICS2024)


def stage_ics2024(age):
    """Stage of `age` on the project's scale; below the Givetian base the Frasnian base is not in timescale.csv."""
    if age > ICS2024[-1][1]:
        return "older_than_Tremadocian_base"
    best = None
    for name, base in ICS2024:
        if base >= age and (best is None or base < best[1]):
            best = (name, base)
    if best[0] == "Givetian" and age < BASE["Givetian"]:
        return "Givetian_or_younger"
    return best[0]


SERIES = {"ludlow": {"gorstian", "ludfordian"}, "wenlock": {"sheinwoodian", "homerian"},
          "llandovery": {"rhuddanian", "aeronian", "telychian"}}


def label_stages(label):
    """Set of stage names a source's stage label allows; None if the label names no stage."""
    t = unicodedata.normalize("NFKD", label or "").encode("ascii", "ignore").decode().lower().strip()
    t = re.sub(r"\b(l|e|m|late|early|middle|mid)\.?\s+", "", t)
    out = set()
    for part in re.split(r"[/&,]| and ", t):
        part = part.strip()
        out |= SERIES.get(part, {part} if part else set())
    known = {n.lower() for n, _ in ICS2024} | {"frasnian"} | set().union(*SERIES.values())
    out &= known
    return out or None


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
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
    return h.hexdigest()


def manifest_sha(route, ver, key):
    with open(os.path.join(MIRROR, route, "raw", ver, "MANIFEST.json"), encoding="utf-8") as f:
        m = json.load(f)
    for e in m["files"]:
        if e["key"] == key or e["key"].endswith("/" + key):
            return e.get("sha256", "")
    return ""


USED = []  # source files used


def use(route, ver, relpath, key=None, derived=False):
    p = os.path.join(MIRROR, route, "raw", ver, relpath) if not derived else os.path.join(MIRROR, route, ver, relpath)
    s = sha256(p)
    ms = "" if derived else manifest_sha(route, ver, key or relpath)
    USED.append([route, ver, os.path.basename(relpath), p, os.path.getsize(p), s, ms,
                 "derived-by-EPRP" if derived else ("match" if s == ms else "MISMATCH")])
    return p


def write_csv(name, header, rows, local=False):
    path = os.path.join(LOCAL if local else OUT, name)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print(f"wrote {'local/context' if local else 'context'}/{name}: {len(rows)} rows, {len(header)} columns")
    return len(rows)


def fnum(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


# ---------------------------------------------------------------- PhanDA
route, ver = "phanda", "2026-03-09_9f06c0d976"
p = use(route, ver, "5_Outputs/PhanDA_GMSTandCO2_percentiles.csv")
with open(p, encoding="utf-8", newline="") as f:
    r = csv.reader(f)
    header = next(r)
    allrows = list(r)
header_phanda = header
iu, il = header.index("UpperAge"), header.index("LowerAge")
phanda_rows = [x for x in allrows if float(x[iu]) < HI and float(x[il]) > LO]
write_csv("phanda_gmst_co2_window.csv", header, phanda_rows, local=True)
print("phanda: slices in file", len(allrows), "in window", len(phanda_rows))
slice_age = {x[header.index("Stage")]: (x[iu], x[il]) for x in phanda_rows}

# PhanDA latitudinal temperature gradient (surface air temperature by latitude), per slice
ltgdir = "5_Outputs/PhanDA_LTG_percentiles/PhanDA_SATgradient_percentiles_bystage"
ltg_rows, ltg_header = [], None
for stage, (up, lo) in slice_age.items():
    fn = f"PhanDA_LTG_{stage.replace('/', '&').replace(' ', '')}.csv"
    p = use(route, ver, f"{ltgdir}/{fn}")
    with open(p, encoding="utf-8", newline="") as f:
        r = csv.reader(f)
        h = next(r)
        ltg_header = h
        for x in r:
            ltg_rows.append([stage, up, lo] + x)
write_csv("phanda_ltg_window.csv",
          ["derived_slice_stage", "derived_slice_upper_age_ma", "derived_slice_lower_age_ma"] + ltg_header, ltg_rows, local=True)

# ---------------------------------------------------------------- PhanSST (GitHub head)
route, ver = "phansst", "2023-03-09_32cc98ed53"
p = use(route, ver, "PhanSST_v001.csv")
use(route, ver, "ReadMe.md")
with open(p, encoding="utf-8", newline="") as f:
    r = csv.reader(f)
    header = next(r)
    ia, istg = header.index("Age"), header.index("Stage")
    out, n_total = [], 0
    for x in r:
        n_total += 1
        a = fnum(x[ia])
        if a is not None and LO <= a <= HI:
            ds = stage_ics2024(a)
            out.append(x + [ds, label_differs(x[istg], ds)])
write_csv("phansst_window.csv", header + ["derived_ics2024_stage_of_age", "derived_stage_label_differs"], out, local=True)
PS_N = len(out)
PS_DIFF = sum(1 for x in out if x[-1] == "1")
PS_DEV_DIFF = sum(1 for x in out if x[-1] == "1" and float(x[ia]) < 419.62)
print("phansst head: rows", n_total, "in window", len(out))
# Zenodo release v0.0.1-beta for comparison (count only)
route2, ver2 = "phansst-zenodo", "v0.0.1-beta_7275402"
zp = use(route2, ver2, "EJJudd/PhanSST-v0.0.1-beta.zip", key="PhanSST-v0.0.1-beta.zip")
with zipfile.ZipFile(zp) as z:
    nm = [n for n in z.namelist() if n.endswith("PhanSST_v001.csv")][0]
    rb = csv.reader(io.TextIOWrapper(z.open(nm), encoding="utf-8", newline=""))
    hb = next(rb)
    iab = hb.index("Age")
    nb = wb = 0
    for x in rb:
        nb += 1
        a = fnum(x[iab])
        if a is not None and LO <= a <= HI:
            wb += 1
print("phansst zenodo beta: rows", nb, "in window", wb)

# ---------------------------------------------------------------- Song et al. 2021 (Database S1)
route, ver = "song2021-temperature-thresholds", "5027293"
p = use(route, ver, "Database S1.xlsx")
use(route, ver, "R code for Thresholds of temperature change for mass extinctions.R")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships"}


def col2n(c):
    n = 0
    for ch in c:
        n = n * 26 + ord(ch) - 64
    return n - 1


def read_xlsx(path, wanted):
    z = zipfile.ZipFile(path)
    ss = []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    for si in root.findall("m:si", NS):
        ss.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
    res = {}
    for s in wb.find("m:sheets", NS):
        if s.get("name") not in wanted:
            continue
        tgt = rels[s.get("{%s}id" % NS["r"])].lstrip("/")
        if not tgt.startswith("xl/"):
            tgt = "xl/" + tgt
        rows = []
        for row in ET.fromstring(z.read(tgt)).iter("{%s}row" % NS["m"]):
            cells = {}
            for c in row.findall("m:c", NS):
                ci = col2n(re.match(r"[A-Z]+", c.get("r")).group())
                v = c.find("m:v", NS)
                if c.get("t") == "inlineStr":
                    val = "".join(t.text or "" for t in c.iter("{%s}t" % NS["m"]))
                elif v is None:
                    continue
                elif c.get("t") == "s":
                    val = ss[int(v.text)]
                else:
                    val = v.text
                cells[ci] = val
            rows.append((int(row.get("r")), cells))
        res[s.get("name")] = rows
    return res


# sheet -> (header row number, age column header, stage column header or None)
SONG = {"O5": (1, "Age, Ma", "Stage"), "S1-S3": (2, "Age (Ma)", None), "D1-D3": (2, "Age (Ma)", "Stage")}
sheets = read_xlsx(p, set(SONG))
SONG_DIFF = {}
for sh, (hr, agecol, stagecol) in SONG.items():
    rows = sheets[sh]
    hdr = dict(rows)[hr]
    width = max(hdr) + 1
    header = [hdr.get(i, "") for i in range(width)]
    ia = header.index(agecol)
    istg = header.index(stagecol) if stagecol else None
    out = []
    n_data = 0
    for rn, cells in rows:
        if rn <= hr:
            continue
        n_data += 1
        a = fnum(cells.get(ia))
        if a is None or not (LO <= a <= HI):
            continue
        row = [cells.get(i, "") for i in range(width)]
        ds = stage_ics2024(a)
        diff = label_differs(row[istg], ds) if istg is not None else ""
        out.append(row + [str(rn), ds, diff])
    SONG_DIFF[sh] = (sum(1 for x in out if x[-1] == "1"), len(out))
    write_csv(f"song2021_{sh}_window.csv", header + ["derived_xlsx_row", "derived_ics2024_stage_of_age",
                                                    "derived_stage_label_differs"], out)
    print(f"song {sh}: data rows {n_data}, in window {len(out)}, age column {agecol!r}")

# ---------------------------------------------------------------- Scotese et al. 2021 (maps -> derived GMST)
route, ver = "scotese2021-gmst", "scotese02a_v21321-C1_8238875"
zp = use(route, ver, "gmst_scotese02a_v21321_csv-list.zip")
use(route, ver, "readme.md")
use(route, ver, "PhanerozoicPTempMapsv22021.pdf")
rows_s = []
with zipfile.ZipFile(zp) as z:
    for nm in sorted(z.namelist()):
        lab = int(nm.split("_")[0])
        if not (LO <= lab <= HI):
            continue
        sw = s = n = nn = 0.0
        tw = tn = pw = pn = 0.0
        mn, mx = 1e9, -1e9
        first2 = []
        with z.open(nm) as fh:
            rd = csv.reader(io.TextIOWrapper(fh, encoding="utf-8", newline=""))
            next(rd)
            for x in rd:
                lon, lat, t = float(x[0]), float(x[1]), fnum(x[2])
                if lat == 90.0 and len(first2) < 2:
                    first2.append(x[2])
                if t is None or math.isnan(t) or lon == 180.0:
                    nn += 1
                    continue
                w = 0.0 if abs(lat) == 90.0 else math.cos(math.radians(lat))
                n += 1
                sw += w * t
                s += w
                if abs(lat) < 90.0:
                    mn, mx = min(mn, t), max(mx, t)
                if abs(lat) <= 30:
                    tw += w * t
                    tn += w
                if abs(lat) >= 60:
                    pw += w * t
                    pn += w
        rows_s.append([str(lab), f"{sw / s:.4f}", f"{tw / tn:.4f}", f"{pw / pn:.4f}",
                       f"{mn:g}", f"{mx:g}", str(int(n)), str(int(nn)), ";".join(first2), nm])
write_csv("scotese2021_gmst_derived_window.csv",
          ["slice_ma_label", "derived_gmst_areaweighted_c",
           "derived_mean_30S_30N_areaweighted_c", "derived_mean_poleward_of_60_areaweighted_c",
           "min_cell_c_excl_lat90_row", "max_cell_c_excl_lat90_row", "n_cells_used", "n_cells_skipped",
           "lat90_first_two_values_as_in_file", "source_member"], rows_s)

# ---------------------------------------------------------------- Rothman et al. 2017 carbon events
derived = "derived/2026-10-23"
p = use("", derived, "rothman2017_events.tsv", derived=True)
use("rothman2017-carbon-events", "2026-10-23T0915Z_url", "PMC5606709_fullText.xml")
with open(p, encoding="utf-8", newline="") as f:
    r = csv.reader(f, delimiter="\t")
    header = next(r)
    ev = list(r)
# cross-check against Table 1 of the article XML (T1)
xml = open(os.path.join(MIRROR, "rothman2017-carbon-events/raw/2026-10-23T0915Z_url/PMC5606709_fullText.xml"),
           encoding="utf-8").read()
tw = re.search(r"<table-wrap id=\"T1\".*?</table-wrap>", xml, re.S).group()
trs = re.findall(r"<tr>(.*?)</tr>", tw, re.S)
xml_rows = []
for tr in trs:
    cells = [re.sub(r"<[^>]+>", "", c).strip().replace("−", "-") for c in re.findall(r"<t[dh][^>]*>(.*?)</t[dh]>", tr, re.S)]
    if len(cells) == 9 and re.match(r"^-?[0-9.]+$", cells[2]):
        xml_rows.append(cells)
agree = sum(1 for a, b in zip(ev, xml_rows)
            if a[:2] == b[:2] and all(abs(float(u) - float(v)) < 1e-9 for u, v in zip(a[2:], b[2:])))
print(f"rothman: EPRP derived events {len(ev)}, XML Table 1 rows {len(xml_rows)}, agree {agree}")
ia = header.index("Date [Ma]")
roth = [x for x in ev if LO <= float(x[ia]) <= HI]
write_csv("rothman2017_events_window.csv", header, roth)

# ---------------------------------------------------------------- Green et al. 2022 (repository tables)
route, ver = "green2022-code", "2023-03-21_e3038b5c02"
dd = "data"


def read_tsv_utf8(path):
    # The source holds U+FFFD where a degree sign was lost; kept as is. Rows with missing trailing
    # fields are padded with empty strings to the header width (structure only, no values changed).
    with open(path, encoding="utf-8", newline="") as f:
        t = list(csv.reader(f, delimiter="\t"))
    return [t[0]] + [x + [""] * (len(t[0]) - len(x)) for x in t[1:]]


def overlaps(lo_age, hi_age, lo_sig, hi_sig):
    """Window overlap using nominal ages, and again widened by 1 sigma; returns basis or None."""
    if hi_age >= LO and lo_age <= HI:
        return "nominal"
    if hi_age + hi_sig >= LO and lo_age - lo_sig <= HI:
        return "sigma-overlap"
    return None


# boundaries (GTS2012 unless a comment says otherwise)
p = use(route, ver, f"{dd}/boundaries.tsv")
t = read_tsv_utf8(p)
h = t[0]
ia, isg, igts = h.index("Age [Ma]"), h.index("Age sigma [Ma]"), h.index("GTS 2012 Age")
iab = h.index("Age/Stage above boundary")
out = []
for x in t[1:]:
    a, sg = fnum(x[ia]), fnum(x[isg]) or 0.0
    if a is None:
        continue
    b = overlaps(a, a, sg, sg)
    if b:
        up = x[iab]
        ics = BASE.get(up)
        out.append(x + [b, f"{ics:g}" if ics else "", f"{ics - a:+.2f}" if ics else ""])
write_csv("green2022_boundaries_window.csv",
          h + ["derived_window_basis", "derived_ics2024_base_of_stage_above_ma", "derived_ics2024_minus_source_myr"], out, local=True)

# LIPs (superset table, includes oceanic provinces)
p = use(route, ver, f"{dd}/LIPs Including Oceanic.tsv")
use(route, ver, f"{dd}/LIPs.tsv")
t = read_tsv_utf8(p)
h = t[0]
i_s, i_ss, i_e, i_es = (h.index(c) for c in ("Start Age [Ma]", "Start Age sigma [Ma]", "End Age [Ma]", "End Age sigma [Ma]"))
out = []
for x in t[1:]:
    s0, e0 = fnum(x[i_s]), fnum(x[i_e])
    if s0 is None or e0 is None:
        continue
    b = overlaps(e0, s0, fnum(x[i_es]) or 0.0, fnum(x[i_ss]) or 0.0)
    if b:
        out.append(x + [b])
write_csv("green2022_lips_window.csv", h + ["derived_window_basis"], out, local=True)

# impacts
p = use(route, ver, f"{dd}/impacts.tsv")
t = read_tsv_utf8(p)
h = t[0]
ia, isg = h.index("Age [Ma]"), h.index("Age_sigma [Ma]")
out = []
for x in t[1:]:
    a, sg = fnum(x[ia]), fnum(x[isg]) or 0.0
    if a is None:
        continue
    b = overlaps(a, a, sg, sg)
    if b:
        out.append(x + [b])
write_csv("green2022_impacts_window.csv", h + ["derived_window_basis"], out, local=True)

# ---------------------------------------------------------------- timescale crosswalks
# (1) stage bases on each scale, Ordovician (Tremadocian) to Givetian
tb = read_tsv_utf8(os.path.join(MIRROR, route, "raw", ver, f"{dd}/boundaries.tsv"))
hb = tb[0]
gts2012 = {}
for x in tb[1:]:
    gts2012[x[hb.index("Age/Stage above boundary")]] = (x[hb.index("GTS 2012 Age")], x[hb.index("Age [Ma]")])
# GTS2020 wall-chart Devonian bases as tabulated in the consuming project's docs/primer.md section 1.2 (not re-read here)
GTS2020_PRIMER = {"Lochkovian": "419.0", "Pragian": "412.4", "Emsian": "410.5", "Eifelian": "394.3"}
pd_lower = {}
for x in allrows:  # PhanDA percentiles file (read above)
    nm = x[header_phanda.index("Stage")]
    for part in nm.split("/"):
        pd_lower[part] = (nm, x[header_phanda.index("UpperAge")], x[header_phanda.index("LowerAge")])
ps_range = {}
with open(os.path.join(MIRROR, "phansst/raw/2023-03-09_32cc98ed53/PhanSST_v001.csv"), encoding="utf-8", newline="") as f:
    r = csv.reader(f)
    h = next(r)
    iag, ist = h.index("Age"), h.index("Stage")
    for x in r:
        a = fnum(x[iag])
        if a is not None:
            lo, hi, n = ps_range.get(x[ist], (1e9, -1e9, 0))
            ps_range[x[ist]] = (min(lo, a), max(hi, a), n + 1)
rows_tb, rows_tb_local = [], []
for st, base in ICS2024:
    g12 = gts2012.get(st, ("", ""))
    pdn = pd_lower.get(st, ("", "", ""))
    pr = ps_range.get(st)
    rows_tb.append([st, f"{base:g}", g12[0], GTS2020_PRIMER.get(st, "")])
    rows_tb_local.append([st, pdn[0], pdn[1], pdn[2], f"{pr[0]:.3f}" if pr else "", f"{pr[1]:.3f}" if pr else "",
                          str(pr[2]) if pr else ""])
write_csv("timescale_stage_bounds.csv",
          ["stage", "ics2024_12_base_ma_project_timescale_csv", "gts2012_base_ma_green2022_table_S1",
           "gts2020_chart_base_ma_from_project_primer_s1_2"], rows_tb)
write_csv("timescale_stage_bounds_phanda_phansst.csv",
          ["stage", "phanda_slice_name", "phanda_slice_upper_age_ma", "phanda_slice_lower_age_ma",
           "phansst_min_age_ma_by_stage_label_whole_file", "phansst_max_age_ma_by_stage_label_whole_file",
           "phansst_rows_with_stage_label"], rows_tb_local, local=True)

# (2) what each series says about its own timescale
TB = [
    ("phanda_gmst_co2_window.csv; phanda_ltg_window.csv", "GTS2020",
     "EPRP catalogue (PhanDA slice boundaries on GTS2020, from the PhanSST ReadMe and the main project's PhanDA notes). Observed: slice bounds in the file for Pragian/Lochkovian (410.5-419.0), Emsian base 410.5, Eifelian base 394.3 equal the GTS2020 chart values in docs/primer.md s1.2; the Eifelian/Givetian bound is 385.3.",
     "Devonian slice bounds differ from ICS v2024/12 (README table; local/context/timescale_stage_bounds_phanda_phansst.csv); Ordovician and Silurian bounds equal ICS v2024/12 to rounding (primer s1.1). Slices are stage-wide; no conversion applied."),
    ("phansst_window.csv", "GTS2020",
     "Observed: PhanSST ReadMe field 'Age: Age, in reference to GTS2020 (Ma)'. Observed: the age range of the points under each Devonian stage label does not follow one scale cleanly (local/context/timescale_stage_bounds_phanda_phansst.csv; for example Pragian points reach 408.6 Ma and Eifelian points 385.7 Ma).",
     "derived_stage_label_differs flags points whose Age falls in a different stage on the project's ICS v2024/12 scale from the stage label in the source (" + f"{PS_DIFF} of {PS_N} window rows, {PS_DEV_DIFF} of them Devonian by age" + "). No age has been changed."),
    ("scotese2021_gmst_derived_window.csv", "GTS2012 stage-midpoint ages (inferred); slice label = PALEOMAP plate-model age",
     "Observed: the 100 maps are labelled by integer Ma (385, 390, ... 450, 460, 470, 480, 490 ...). Inferred: the labels coincide with the 'plate tectonic model age' column of Table 1 in Scotese & Wright (2018), whose stratigraphic ages are 'from Ogg, Ogg & Gradstein (2012)' (GTS2012). The mirror does not name the stage of each temperature map.",
     "Treat slice labels as PALEOMAP model ages, not stage-resolved ICS v2024/12 dates. Several Devonian PALEOMAP stage labels (e.g. 410 Ma, 'Pragian, 409.2 Ma') fall in a different stage on ICS v2024/12 (paleodem_slices.csv)."),
    ("song2021_*_window.csv", "not stated for the Ordovician-Devonian sheets; Carboniferous-Permian sheets say 'Age (Ma)-2012'",
     "Observed: sheet headers 'Age (Ma)-2012' on C1-2, C2-P3 and P4-5; plain 'Age (Ma)' on S1-S3 and D1-D3; O5 has 'Age, Ma' (source) and 'Age-updated' (with references). Inferred, not verified against the paper: GTS2012.",
     "Devonian ages are interpolated between conodont-zone or stage ages (decimals such as 392.1731); the Emsian-Pragian and Lochkovian-Pragian boundaries move by 2-3 Myr between GTS2012 and ICS v2024/12, so stage labels in D1-D3 do not match the ICS v2024/12 stage of the age for " + f"{SONG_DIFF['D1-D3'][0]} of {SONG_DIFF['D1-D3'][1]}" + " rows (derived_stage_label_differs). O5 'Age-updated'/'Stage-updated' re-assign late-Katian samples to the Hirnantian at about 442.9 Ma; the filter uses the original 'Age, Ma'."),
    ("rothman2017_events_window.csv", "GTS2012 for biostratigraphically timed events (article reference 44), but not uniformly",
     "Observed: article Methods say pre-Quaternary events are 'timed by biostratigraphy with reference to the Geologic Time Scale (44)', reference 44 being Gradstein et al. (2012). Observed: Table 1 gives the K-Pg event at 65.50 Ma, a pre-GTS2012 value (outside the window).",
     "Window events (End-Ordovician 445.80, Mulde 428.20, Lau 423.50) are Ordovician-Silurian; no Devonian event in window. Ages are to 0.01 Myr as printed but not that precise."),
    ("green2022_boundaries_window.csv; green2022_lips_window.csv; green2022_impacts_window.csv", "GTS2012 for stage boundaries (unless a comment says otherwise); radioisotopic ages as published for LIPs and impacts",
     "Observed: Table S1 header 'Age reference and comments, if different from GTS2012'; in boundaries.tsv the 'GTS 2012 Age' and 'Age [Ma]' columns are identical for all window rows (empty comment column).",
     "derived_ics2024_minus_source_myr gives the shift to the project's scale for each boundary (Pragian/Emsian +3.02, Lochkovian/Pragian +2.22 Myr). LIP and impact ages are absolute radioisotopic ages, not scale-bound, but their stage associations are GTS2012."),
]
with open(os.path.join(OUT, "timescale_basis.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, lineterminator="\n")
    w.writerow(["delivered_file", "timescale_basis", "evidence", "devonian_and_other_notes"])
    w.writerows(TB)
print("wrote timescale_basis.csv:", len(TB), "rows")

# ---------------------------------------------------------------- sources used
with open(os.path.join(OUT, "sources_used_climate.tsv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["route", "version", "file", "deep_server_path", "bytes", "sha256_computed", "sha256_in_mirror_manifest", "check"])
    w.writerows(USED)
bad = [u for u in USED if u[-1] == "MISMATCH"]
print("sources used:", len(USED), "mismatches:", len(bad))
sys.exit(1 if bad else 0)
