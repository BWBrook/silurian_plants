"""Estimate the overlap between GBDB window plant records and the project's PBDB plant extract.

Usage (from the project root, after gbdb_extract.py has produced data/external/gbdb/*.csv):
  python3 data/external/scripts/gbdb_pbdb_overlap.py

Reads  data/external/gbdb/gbdb_plant_fossils.csv, gbdb_plant_sections.csv, gbdb_window_sections_all.csv
       data/eprp/record/pbdb_plant_occurrences.csv, pbdb_plant_collections.csv, pbdb_plant_references.csv
Writes data/external/gbdb/gbdb_pbdb_overlap_references.csv, gbdb_pbdb_overlap_sections.csv,
       gbdb_pbdb_overlap_pbdb_collections_china.csv, gbdb_pbdb_overlap_records.csv and gbdb_pbdb_overlap_summary.json
Nothing is deleted or merged; the tables only label candidate pairs. Standard library only.
"""
import collections
import csv
import json
import math
import re
import unicodedata
from pathlib import Path

G = Path("data/external/gbdb")
P = Path("data/eprp/record")
csv.field_size_limit(10**9)


def rd(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


gfos = rd(G / "gbdb_plant_fossils.csv")
gsec = rd(G / "gbdb_plant_sections.csv")
gnoage = rd(G / "gbdb_plant_no_age_candidates.csv")
gwin = rd(G / "gbdb_window_sections_all.csv")
pocc = rd(P / "pbdb_plant_occurrences.csv")
pcol = {r["collection_no"]: r for r in rd(P / "pbdb_plant_collections.csv")}
pref = rd(P / "pbdb_plant_references.csv")


def fold(s):
    return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())


def words(s):
    t = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return {w for w in re.findall(r"[a-z]{3,}", t) if w not in {"the", "and", "from", "with", "for", "des", "der", "die", "del"}}


def haversine(lat1, lon1, lat2, lon2):
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi, dl = p2 - p1, math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 6371.0 * 2 * math.asin(math.sqrt(a))


def fnum(s):
    try:
        return float(s)
    except (TypeError, ValueError):
        return None


GENERIC = {"formation", "fm", "group", "member", "mbr", "upper", "lower", "middle", "the", "and", "of", "also", "called", "unit", "section",
           "beds", "bed", "series", "unknown", "unnamed", "shale", "sandstone", "limestone"}


def ftokens(s):
    t = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return {w for w in re.findall(r"[a-z]{3,}", t) if w not in GENERIC}


# ---------------------------------------------------------------------------------------------------------------
# 1. References: GBDB (window and anchor plant records) against PBDB plant references
# ---------------------------------------------------------------------------------------------------------------
pby = collections.defaultdict(list)
for r in pref:
    names = [r["author1last"], r["author2last"]] + [x.split()[-1] for x in re.split(r"[,;]", r["otherauthors"]) if x.strip()]
    for n in {fold(x) for x in names if x}:
        pby[(n, r["pubyr"])].append(r)

grefs = collections.OrderedDict()
for r in gfos:
    g = grefs.setdefault(r["ReferenceID"], {"last": r["ref_FirstAuthorLastName"], "given": r["refFirstAuthor"], "year": r["ref_PublicationYear"],
                                          "title": r["ref_Title"], "journal": r["ref_JournalOrBookTitle"], "core": 0, "flag": 0})
    g["core" if r["derived_in_core"] == "yes" else "flag"] += 1
for r in gnoage:
    g = grefs.setdefault(r["ReferenceID"], {"last": r["ref_FirstAuthorLastName"], "given": r["refFirstAuthor"], "year": r["ref_PublicationYear"],
                                          "title": r["ref_Title"], "journal": r["ref_JournalOrBookTitle"], "core": 0, "flag": 0})
    g["noage"] = g.get("noage", 0) + 1

ref_match = {}          # ReferenceID -> list of (pbdb reference_no, level, similarity)
with open(G / "gbdb_pbdb_overlap_references.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["gbdb_ReferenceID", "gbdb_first_author_last", "gbdb_first_author_given", "gbdb_year", "gbdb_title", "gbdb_journal_or_book",
                "n_core_window_records", "n_flagged_window_records", "n_no_age_candidate_records", "pbdb_reference_no", "pbdb_formatted", "title_overlap_coefficient",
                "match_level"])
    for rid, g in grefs.items():
        key = (fold(g["last"]), g["year"])
        cands = pby.get(key, []) if fold(g["last"]) else []
        gw = words(g["title"])
        out = []
        for c in {c["reference_no"]: c for c in cands}.values():
            pw = words(c["reftitle"])
            if len(gw) >= 3 and len(pw) >= 3:
                sim = len(gw & pw) / min(len(gw), len(pw))
                level = "author_year_and_title" if sim >= 0.6 else "author_year_but_different_title"
            else:
                sim = ""
                level = "author_year_title_not_comparable"
            out.append((c["reference_no"], level, sim, c["formatted"]))
        ref_match[rid] = [(a, b, c) for a, b, c, _ in out]
        if not out:
            w.writerow([rid, g["last"], g["given"], g["year"], g["title"][:200], g["journal"][:120], g["core"], g["flag"], g.get("noage", 0), "", "", "",
                        "no_candidate" if fold(g["last"]) else "first_author_not_latin"])
        for a, level, sim, fm in out:
            w.writerow([rid, g["last"], g["given"], g["year"], g["title"][:200], g["journal"][:120], g["core"], g["flag"], g.get("noage", 0), a, fm[:250],
                        f"{sim:.2f}" if sim != "" else "", level])

STRONG = {"author_year_and_title"}
MODERATE = {"author_year_and_title", "author_year_title_not_comparable"}

# ---------------------------------------------------------------------------------------------------------------
# 2. PBDB side: occurrences per collection, collection coordinates
# ---------------------------------------------------------------------------------------------------------------
occ_by_col = collections.defaultdict(list)
for r in pocc:
    occ_by_col[r["collection_no"]].append(r)
pb_cols = []
for cno, c in pcol.items():
    lat, lng = fnum(c["lat"]), fnum(c["lng"])
    if lat is None or lng is None:
        continue
    pb_cols.append((cno, lat, lng, c))
pb_refs_of_col = {}
for cno, c in pcol.items():
    pb_refs_of_col[cno] = {c["reference_no"]} | {o["reference_no"] for o in occ_by_col[cno]}

# ---------------------------------------------------------------------------------------------------------------
# 3. GBDB plant sections against PBDB plant collections
# ---------------------------------------------------------------------------------------------------------------
sec_form = collections.defaultdict(set)
sec_geo = {}
for r in gsec:
    sid = r["sectionID"]
    if int(r["derived_n_core_plant_records_window_or_anchor"] or 0) + int(r["derived_n_flagged_records_window_or_anchor"] or 0) > 0:
        sec_form[sid].add(r["Formation_name"])
    lat, lon = fnum(r["derived_lat"]), fnum(r["derived_lon"])
    sec_geo[sid] = (lat, lon, r["SectionName"], r["Country"], r["Province"])
sec_rec = collections.defaultdict(list)
for r in gfos:
    sec_rec[r["sectionID"]].append(r)

sec_rows = []
rec_level = {}                      # (sectionID, sections_xlsx_row) -> level
pb_genera = collections.defaultdict(set)
for r in pocc:
    pb_genera[r["collection_no"]].add(r["d_genus"].lower())
for sid, (lat, lon, sname, ctry, prov) in sec_geo.items():
    if sid not in sec_rec:
        continue
    recs = sec_rec[sid]
    ggen = {r["derived_genus"].lower() for r in recs if r["derived_in_core"] == "yes" and r["derived_genus"]}
    gform = sec_form[sid]
    gft = set().union(*[ftokens(f) for f in gform]) if gform else set()
    grefids = {r["ReferenceID"] for r in recs}
    pbref_strong = {m[0] for rid in grefids for m in ref_match.get(rid, []) if m[1] in STRONG}
    pbref_mod = {m[0] for rid in grefids for m in ref_match.get(rid, []) if m[1] in MODERATE}
    near = []
    if lat is not None and lon is not None:
        for cno, clat, clng, c in pb_cols:
            d = haversine(lat, lon, clat, clng)
            if d <= 100:
                near.append((d, cno, c))
        near.sort(key=lambda x: x[0])
    n10 = sum(1 for d, _, _ in near if d <= 10)
    n50 = sum(1 for d, _, _ in near if d <= 50)
    form_hit = [(d, cno) for d, cno, c in near if d <= 50 and (ftokens(c["formation"]) & gft)]
    ref_hit = []
    if lat is not None and lon is not None:
        ref_hit = sorted((haversine(lat, lon, clat, clng), cno) for cno, clat, clng, c in pb_cols if pb_refs_of_col[cno] & pbref_strong)
    gen_hit_cols = [(d, cno) for d, cno, c in near if d <= 50 and (pb_genera[cno] & ggen)]
    shared_genera = sorted(set().union(*[pb_genera[c] & ggen for _, c in gen_hit_cols])) if gen_hit_cols else []
    if ref_hit:
        cls = "same_reference_any_distance"
    elif form_hit and shared_genera:
        cls = "same_formation_name_within_50km_and_shared_genus"
    elif form_hit:
        cls = "same_formation_name_within_50km_no_shared_genus"
    elif near and near[0][0] <= 10:
        cls = "within_10km_other_formation_or_reference"
    elif n50:
        cls = "within_50km_only"
    else:
        cls = "no_pbdb_plant_collection_within_50km"
    sec_rows.append([sid, sname, ctry, prov, lat if lat is not None else "", lon if lon is not None else "", "; ".join(sorted(gform))[:150],
                     len(recs), sum(1 for r in recs if r["derived_in_core"] == "yes"), ";".join(sorted(grefids)), ";".join(sorted(pbref_strong)),
                     ";".join(sorted(pbref_mod - pbref_strong)), f"{ref_hit[0][0]:.0f}" if ref_hit else "",
                     f"{near[0][0]:.1f}" if near else "", near[0][1] if near else "", n10, n50,
                     ";".join(f"{c}" for _, c in form_hit[:5]), ";".join(shared_genera[:12]), cls])

# record-level labels for every core GBDB window record (any distance for reference and formation-name matches; China only)
pb_col_geo = {cno: (clat, clng, c) for cno, clat, clng, c in pb_cols}
pb_genus_cols = collections.defaultdict(set)
for o in pocc:
    if o["d_genus"]:
        pb_genus_cols[o["d_genus"].lower()].add(o["collection_no"])
strong_pb_of_gbdb_ref = {rid: {m[0] for m in ms if m[1] in STRONG} for rid, ms in ref_match.items()}
for sid, recs in sec_rec.items():
    lat, lon = sec_geo[sid][0], sec_geo[sid][1]
    for r in recs:
        if r["derived_in_core"] != "yes" or not r["derived_genus"]:
            continue
        g = r["derived_genus"].lower()
        gft = ftokens(r["Formation_name"])
        cols = [c for c in pb_genus_cols.get(g, ()) if c in pb_col_geo]
        lv = "none"
        dmin = ""
        best = None
        for c in cols:
            clat, clng, cc = pb_col_geo[c]
            if cc["cc"] != "CN":
                continue
            d = haversine(lat, lon, clat, clng) if lat is not None and lon is not None else None
            rank = 9
            if pb_refs_of_col[c] & strong_pb_of_gbdb_ref.get(r["ReferenceID"], set()):
                rank = 1
            elif gft and (ftokens(cc["formation"]) & gft):
                rank = 2
            elif d is not None and d <= 25:
                rank = 3
            elif d is not None and d <= 100:
                rank = 4
            if rank < 9 and (best is None or rank < best[0] or (rank == best[0] and d is not None and (best[1] is None or d < best[1]))):
                best = (rank, d)
            if d is not None and (dmin == "" or d < dmin):
                dmin = d
        if best:
            lv = {1: "A_same_reference_and_genus", 2: "B_same_formation_name_and_genus",
                  3: "C_genus_in_pbdb_collection_within_25km", 4: "D_genus_in_pbdb_collection_25_to_100km"}[best[0]]
        rec_level[r["derived_sections_xlsx_row"]] = (lv, f"{dmin:.0f}" if dmin != "" else "")

with open(G / "gbdb_pbdb_overlap_sections.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["gbdb_sectionID", "gbdb_section_name", "gbdb_country", "gbdb_province", "gbdb_derived_lat", "gbdb_derived_lon",
                "gbdb_formations_with_plant_records", "n_window_plant_records", "n_core_window_plant_records", "gbdb_reference_ids",
                "pbdb_reference_nos_strong_match", "pbdb_reference_nos_moderate_match", "distance_km_to_pbdb_collection_with_same_reference",
                "nearest_pbdb_plant_collection_km",
                "nearest_pbdb_plant_collection_no", "n_pbdb_plant_collections_within_10km", "n_pbdb_plant_collections_within_50km",
                "pbdb_collections_with_formation_name_overlap_within_50km", "shared_core_genera_within_50km", "overlap_class"])
    w.writerows(sec_rows)

with open(G / "gbdb_pbdb_overlap_records.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["gbdb_sections_xlsx_row", "derived_genus", "sectionID", "SectionName", "Formation_name", "Province", "early_age", "late_age",
                "derived_flag", "pbdb_counterpart_level", "km_to_nearest_pbdb_china_collection_with_genus"])
    for r in gfos:
        if r["derived_in_core"] == "yes":
            w.writerow([r["derived_sections_xlsx_row"], r["derived_genus"], r["sectionID"], r["SectionName"], r["Formation_name"], r["Province"],
                        r["early_age"], r["late_age"], r["derived_flag"], *rec_level.get(r["derived_sections_xlsx_row"], ("none", ""))])

# ---------------------------------------------------------------------------------------------------------------
# 4. Reverse: PBDB plant collections in China against all GBDB window sections
# ---------------------------------------------------------------------------------------------------------------
gw_geo = []
gw_forms = {}
for r in gwin:
    lat, lon = fnum(r["derived_lat"]), fnum(r["derived_lon"])
    if lat is not None and lon is not None:
        gw_geo.append((r["sectionID"], lat, lon, r))
plant_sids = set(sec_rec)
grefs_by_sid = {sid: {r["ReferenceID"] for r in rs} for sid, rs in sec_rec.items()}
rows_cn = []
for cno, lat, lng, c in pb_cols:
    if c["cc"] != "CN":
        continue
    near = sorted(((haversine(lat, lng, glat, glon), sid, r) for sid, glat, glon, r in gw_geo if abs(glat - lat) < 1.5 and abs(glon - lng) < 1.5),
                  key=lambda x: x[0])
    n_core = sum(1 for o in occ_by_col[cno] if o["d_in_core"] == "yes")
    pft = ftokens(c["formation"]) | ftokens(c["geological_group"])
    hit = [(d, sid) for d, sid, r in near if d <= 50 and (ftokens(r["derived_formation_names_window"]) & pft)]
    plant_near = [(d, sid) for d, sid, r in near if d <= 50 and sid in plant_sids]
    rows_cn.append([cno, c["collection_name"][:80], c["formation"], c["geological_group"], c["state"], lat, lng, c["early_interval"], c["max_ma"], c["min_ma"],
                    c["ref_author"], c["ref_pubyr"], c["reference_no"], len(occ_by_col[cno]), n_core,
                    f"{near[0][0]:.1f}" if near else "", near[0][1] if near else "", sum(1 for d, _, _ in near if d <= 10),
                    sum(1 for d, _, _ in near if d <= 50), ";".join(s for _, s in hit[:5]), ";".join(s for _, s in plant_near[:5])])
with open(G / "gbdb_pbdb_overlap_pbdb_collections_china.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["pbdb_collection_no", "collection_name", "formation", "geological_group", "state", "lat", "lng", "early_interval", "max_ma",
                "min_ma", "ref_author", "ref_pubyr", "pbdb_reference_no", "n_plant_filter_occurrences", "n_core_occurrences",
                "nearest_gbdb_window_section_km", "nearest_gbdb_window_section_id", "n_gbdb_window_sections_within_10km",
                "n_gbdb_window_sections_within_50km", "gbdb_window_sections_with_formation_name_overlap_within_50km",
                "gbdb_window_sections_with_plant_records_within_50km"])
    w.writerows(rows_cn)

# PBDB China core occurrences against GBDB window plant records and GBDB no-age candidates
gb_by_genus = collections.defaultdict(list)
for pool, rs in (("W", gfos), ("N", gnoage)):
    for r in rs:
        if r["derived_in_core"] == "yes" and r["derived_genus"]:
            gb_by_genus[r["derived_genus"].lower()].append((pool, ftokens(r["Formation_name"]), r["ReferenceID"], fnum(r["derived_lat"]), fnum(r["derived_lon"])))
rev_rows = []
for o in pocc:
    c = pcol.get(o["collection_no"])
    if o["d_in_core"] != "yes" or not c or c["cc"] != "CN" or not o["d_genus"]:
        continue
    g = o["d_genus"].lower()
    refs = {o["reference_no"], c["reference_no"]}
    pft = ftokens(c["formation"]) | ftokens(c["geological_group"])
    clat, clng = fnum(c["lat"]), fnum(c["lng"])
    best = {}
    for pool, gft, rid, glat, glon in gb_by_genus.get(g, ()):
        d = haversine(clat, clng, glat, glon) if None not in (clat, clng, glat, glon) else None
        rank = 9
        if refs & strong_pb_of_gbdb_ref.get(rid, set()):
            rank = 1
        elif gft & pft:
            rank = 2
        elif d is not None and d <= 25:
            rank = 3
        elif d is not None and d <= 100:
            rank = 4
        if rank < 9 and rank < best.get(pool, 9):
            best[pool] = rank
    names = {1: "A_same_reference_and_genus", 2: "B_same_formation_name_and_genus", 3: "C_genus_within_25km", 4: "D_genus_25_to_100km"}
    if "W" in best:
        lvl = "window_" + names[best["W"]]
    elif "N" in best:
        lvl = "no_age_only_" + names[best["N"]]
    else:
        lvl = "none"
    rev_rows.append([o["occurrence_no"], o["collection_no"], o["d_genus"], c["formation"], c["ref_author"], c["ref_pubyr"], o["reference_no"], o["max_ma"],
                     o["min_ma"], lvl])
with open(G / "gbdb_pbdb_overlap_pbdb_occurrences_china_core.csv", "w", newline="", encoding="utf-8") as fo:
    w = csv.writer(fo, lineterminator="\n")
    w.writerow(["pbdb_occurrence_no", "pbdb_collection_no", "d_genus", "pbdb_formation", "pbdb_ref_author", "pbdb_ref_pubyr", "pbdb_reference_no",
                "max_ma", "min_ma", "gbdb_counterpart_level"])
    w.writerows(rev_rows)

# ---------------------------------------------------------------------------------------------------------------
# 5. Summary
# ---------------------------------------------------------------------------------------------------------------
core = [r for r in gfos if r["derived_in_core"] == "yes"]
unfl = [r for r in core if not r["derived_flag"]]
lv = collections.Counter(rec_level.get(r["derived_sections_xlsx_row"], ("none", ""))[0] for r in core)
lv_unfl = collections.Counter(rec_level.get(r["derived_sections_xlsx_row"], ("none", ""))[0] for r in unfl)
pb_cn_core = [o for o in pocc if o["d_in_core"] == "yes" and pcol.get(o["collection_no"], {}).get("cc") == "CN"]
gb_genera_all = {r["derived_genus"].lower() for r in gfos if r["derived_genus"]}
gb_core_genera = {r["derived_genus"].lower() for r in core if r["derived_genus"]}
pb_core_genera = {o["d_genus"].lower() for o in pocc if o["d_in_core"] == "yes" and o["d_genus"]}
pb_cn_genera = {o["d_genus"].lower() for o in pb_cn_core if o["d_genus"]}
sec_cls = collections.Counter(r[-1] for r in sec_rows)
ref_levels = collections.Counter()
for rid, ms in ref_match.items():
    levels = {m[1] for m in ms}
    ref_levels["strong" if levels & STRONG else "moderate" if levels & MODERATE else "weak_or_none"] += 1
cn_cover = collections.Counter()
for r in rows_cn:
    cn_cover["with_gbdb_window_section_within_50km" if int(r[18]) > 0 else "no_gbdb_window_section_within_50km"] += 1
    if r[19]:
        cn_cover["with_gbdb_section_with_same_formation_name_within_50km"] += 1
    if r[20]:
        cn_cover["with_gbdb_plant_section_within_50km"] += 1
summary = {
    "gbdb_window_plant_records": len(gfos), "gbdb_core_window_plant_records": len(core), "gbdb_core_records_without_doubt_flag": len(unfl),
    "gbdb_plant_sections": len(sec_rows), "gbdb_references_in_window_plant_records": len(grefs),
    "reference_match_levels_gbdb_references": dict(ref_levels),
    "section_overlap_classes": dict(sec_cls),
    "core_record_counterpart_levels_all": dict(lv), "core_record_counterpart_levels_unflagged": dict(lv_unfl),
    "genera": {"gbdb_core_window": len(gb_core_genera), "pbdb_core_window": len(pb_core_genera),
               "gbdb_core_genera_also_in_pbdb_core_window": len(gb_core_genera & pb_core_genera),
               "pbdb_china_core_genera": len(pb_cn_genera), "gbdb_core_genera_also_in_pbdb_china_core": len(gb_core_genera & pb_cn_genera),
               "pbdb_china_core_genera_also_in_gbdb_window_plants": len(pb_cn_genera & gb_genera_all)},
    "pbdb_china": {"collections": len(rows_cn), "core_occurrences": len(pb_cn_core), "coverage": dict(cn_cover),
                   "core_occurrence_gbdb_counterpart_levels": dict(collections.Counter(r[-1] for r in rev_rows))},
}
json.dump(summary, open(G / "gbdb_pbdb_overlap_summary.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
