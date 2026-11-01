# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas"]
# ///
"""Assemble inspectable positive record units and exposure proxies for Loop 3."""

import hashlib
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
from occurrences import LAND, MARGINAL, unit_of

OUT = ROOT / "data/macro"
PBDB = ROOT / "data/eprp/record"
OCC = ROOT / "data/occurrences"
YOUNG, OLD = 393.47, 445.2
EMBRYOPHYTE = {"rhyniophytoid_cooksonioid", "lycophyte_line", "euphyllophyte", "tracheophyte_indet",
               "polysporangiophyte_indet", "embryophyte_axis_indet", "bryophyte_grade"}
UNRESOLVED_UNITS = {"M-yea-unspecified", "M-kazakh-lycophytes", "M-kazakh-zosterophyllum",
                    "M-cooksonella-kazakhstan", "M-aberlemnia-krizii", "M-xinjiang-santanhu",
                    "M-xinjiang-zosterophyllum"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, rows):
    rows.to_csv(OUT / name, index=False, lineterminator="\n")


def explicit_links(obs, occurrence):
    links = []
    for _, r in obs[obs.channel.isin(["megafossil", "mesofossil"])].iterrows():
        text = " ".join(r.fillna("").astype(str))
        occ_ids = {int(x) for x in re.findall(r"occurrence(?:_no)?[= ]+(\d+)", text)}
        coll_ids = {int(x) for x in re.findall(r"collection(?:_no)?[= ]+(\d+)", text)}
        coll_ids |= set(occurrence[occurrence.occurrence_no.isin(occ_ids)].collection_no)
        for c in sorted(coll_ids):
            links.append({"collection_no": int(c), "obs_id": r.obs_id,
                          "material_root": r.same_material_as if pd.notna(r.same_material_as) else r.obs_id,
                          "basis": "explicit collection or occurrence identifier in curated observation",
                          "locator": r.locator})
    return pd.DataFrame(links).drop_duplicates()


def older_screen(occ):
    r = occ[(occ.d_record_type != "dispersed_spore") & (occ.min_ma >= OLD) & (occ.min_ma < 469.4)].copy()
    r["name"] = r.accepted_name.fillna(r.identified_name)
    adjudications = pd.read_csv(OUT / "older_candidate_adjudications.csv")
    decisions = {}
    for row in adjudications.itertuples():
        for number in re.findall(r"\d+", str(row.pbdb_occurrence_nos)):
            decisions[int(number)] = row.candidate_id
    r["source_review_id"] = r.occurrence_no.map(decisions).fillna("")
    r["screen_status"] = np.where(r.source_review_id != "", "excluded_non_embryophyte_source_review",
                                  "database_category_screened_not_source_audited")
    plausible = r.d_subset.isin(["embryophyta_pbdb_tree", "plantae_unplaced_pbdb_tree", "plant_unlinked_name", "plant_unlinked_organ"])
    if (plausible & r.source_review_id.eq("")).any():
        raise ValueError("older unplaced/plant candidate has no recorded source disposition")
    save("older_records_screen.csv", r[["occurrence_no", "collection_no", "name", "max_ma", "min_ma",
                                       "d_subset", "d_record_type", "reference_no", "source_review_id", "screen_status"]])


def build():
    classes = pd.DataFrame([r for p in sorted((ROOT / "work/codex/loop3").glob("out_*.json"))
                            for r in json.loads(p.read_text())["items"]])
    if classes.name.duplicated().any():
        raise ValueError("duplicate name classifications")
    save("name_classifications.csv", classes)
    cls = classes.set_index("name")
    occ = pd.read_csv(PBDB / "pbdb_plant_occurrences.csv", low_memory=False)
    older_screen(occ)
    obs = pd.read_csv(OCC / "observations.csv")
    links = explicit_links(obs, occ)
    save("material_links.csv", links)
    occ = occ[(occ.d_record_type != "dispersed_spore") & (occ.min_ma < OLD) & (occ.max_ma > YOUNG)].copy()
    occ["name"] = occ.accepted_name.fillna(occ.identified_name)
    occ = occ[occ.name.isin(cls.index)].copy()
    occ["b0"] = occ.name.map(cls.category).isin(EMBRYOPHYTE)
    occ["b1"] = occ.b0 & occ.name.map(cls.polysporangiophyte).eq("yes")
    occ["b2"] = occ.b1 & occ.name.map(cls.crown_tracheophyte).eq("yes")
    occ["low_confidence"] = occ.name.map(cls.confidence).eq("low")
    accepted = occ[occ.b0 | occ.b1 | occ.b2].copy()
    save("accepted_occurrence_links.csv", accepted[["occurrence_no", "collection_no", "name", "max_ma", "min_ma",
                                                   "b0", "b1", "b2", "low_confidence", "reference_no"]])
    collections = pd.read_csv(PBDB / "pbdb_plant_collections.csv", low_memory=False).drop_duplicates("collection_no")
    g = accepted.groupby("collection_no").agg(
        max_ma=("max_ma", "max"), min_ma=("min_ma", "min"), b0=("b0", "any"), b1=("b1", "any"), b2=("b2", "any"),
        names=("name", lambda s: "; ".join(sorted(set(s)))), low_confidence=("low_confidence", "any")).reset_index()
    g = g.merge(collections[["collection_no", "collection_name", "formation", "lat", "lng", "cc", "state", "localbed"]],
                on="collection_no", validate="one_to_one").fillna({"formation": "", "collection_name": "", "state": "", "localbed": ""})
    g["horizon_id"] = "pbdb:" + g.collection_no.astype(str)
    g["source"] = "pbdb"
    g["reading"] = "all"
    g["region"] = [unit_of(r.cc, r.state) for r in g.itertuples()]
    g["region_basis"] = "approximate country/state assignment; not independently reconstructed"
    g["locality"] = g.cc + "|" + g.formation.str.strip().str.lower() + "|" + g.lat.round(1).astype(str) + "," + g.lng.round(1).astype(str)
    missing_location = g.lat.isna() | g.lng.isna() | g.cc.isna()
    g.loc[missing_location, "locality"] = g.loc[missing_location, "horizon_id"]
    g["material_status"] = "collection identity; distinct bed not verified"
    g["eligible_primary"] = ~g.collection_no.isin(links.collection_no) & ((g.max_ma - g.min_ma) <= 20)
    g["disposition"] = np.where(g.collection_no.isin(links.collection_no), "replaced_by_curated_material",
                                 np.where((g.max_ma - g.min_ma) > 20, "wide_age_sensitivity", "primary"))
    regional = g.collection_no.eq(53659)
    g.loc[regional, "eligible_primary"] = False
    g.loc[regional, "disposition"] = "unresolved_material_sensitivity"
    g["source_locator"] = "PBDB collection " + g.collection_no.astype(str)
    g["age_group"] = g.min_ma.astype(str) + "|" + g.max_ma.astype(str)

    scale = pd.read_csv(ROOT / "data/timescale.csv")
    base, top = dict(zip(scale.stage, scale.base_ma)), dict(zip(scale.stage, scale.base_ma.shift(1)))
    ra = pd.read_csv(OCC / "reading_assignments.csv")
    ra = ra[ra.event.isin(["E3", "E4", "E5"]) & ~ra.obs_id.str.startswith("M-pbdb-") & ra.same_material_as.isna()]
    tail = []
    for (oid, reading), rows in ra.groupby(["obs_id", "reading_id"]):
        r = obs.set_index("obs_id").loc[oid]
        bounds = rows[["stage_oldest", "stage_youngest"]].drop_duplicates()
        if len(bounds) != 1:
            raise ValueError(f"event-dependent age ranges require adjudication: {oid}, {reading}")
        older, younger = base[bounds.iloc[0].stage_oldest], top[bounds.iloc[0].stage_youngest]
        status = "unresolved_material_sensitivity" if oid in UNRESOLVED_UNITS else "primary"
        if older <= YOUNG or younger >= OLD:
            status = "outside_analysis_window"
        tail.append({"horizon_id": "tail:" + oid, "source": "tail", "reading": reading, "max_ma": older, "min_ma": younger,
                     "b0": True, "b1": True, "b2": rows.event.eq("E5").any(), "names": r.reported_as,
                     "low_confidence": False, "region": r.palaeo_unit, "region_basis": "curated occurrence source",
                     "cc": r.country, "locality": str(r.country) + "|" + str(r.locality).strip().lower(),
                     "material_status": "curated observation; " + str(r.horizon), "eligible_primary": status == "primary",
                     "disposition": status, "source_locator": str(r.source_ids) + ": " + str(r.locator),
                     "age_group": str(younger) + "|" + str(older)})
    fields = list(tail[0])
    h = pd.concat([g[fields], pd.DataFrame(tail)], ignore_index=True)
    h.loc[h.horizon_id.eq("tail:M-ghin-ghin-b2"), "locality"] = "Australia|ghin ghin road, yea"
    h["partial_window"] = (h.min_ma < YOUNG) | (h.max_ma > OLD)
    if (h.b2 & ~h.b1).any() or (h.b1 & ~h.b0).any():
        raise ValueError("body-category nesting failed")
    save("horizons_reviewed.csv", h.sort_values(["source", "horizon_id", "reading"]))
    return h


def effort():
    raw_path = OCC / "raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv"
    r = pd.read_csv(raw_path, low_memory=False)
    r["environment"] = r.environment.fillna("")
    r["state"] = r.state.fillna("")
    r["region"] = [unit_of(x.cc, x.state) for x in r.itertuples()]
    plant_ids = set(pd.read_csv(PBDB / "pbdb_plant_collections.csv", usecols=["collection_no"]).collection_no)
    r["plant_overlap"] = r.collection_no.isin(plant_ids)
    t = pd.read_csv(ROOT / "data/timescale.csv")
    t["top_ma"] = t.base_ma.shift(1)
    t = t[(t.base_ma <= 469.4) & (t.top_ma >= YOUNG)]
    records = []
    for region, rr in [("global", r)] + list(r.groupby("region")):
        for s in t.itertuples():
            duration = s.base_ma - s.top_ma
            overlap = np.maximum(0, np.minimum(rr.max_ma, s.base_ma) - np.maximum(rr.min_ma, s.top_ma))
            width = rr.max_ma - rr.min_ma
            weights = np.divide(overlap, width, out=np.zeros(len(rr)), where=width > 0)
            environments = rr.environment.isin(LAND | MARGINAL)
            all_count = float(weights[environments].sum())
            excluded_count = float(weights[environments & ~rr.plant_overlap].sum())
            records.append({"region": region, "stage": s.stage, "young_ma": s.top_ma, "old_ma": s.base_ma,
                            "duration_myr": duration, "all_collection_equivalents": all_count,
                            "plant_excluded_equivalents": excluded_count,
                            "all_density_per_myr": all_count / duration,
                            "plant_excluded_density_per_myr": excluded_count / duration})
    result = pd.DataFrame(records)
    save("effort_reviewed.csv", result)
    return result


def main():
    OUT.mkdir(exist_ok=True)
    inputs = [PBDB / n for n in ("pbdb_plant_occurrences.csv", "pbdb_plant_collections.csv")]
    inputs += [OCC / n for n in ("observations.csv", "reading_assignments.csv", "raw/pbdb_collections_darriwilian_emsian_2026-10-28.csv")]
    inputs += [ROOT / "data/timescale.csv", ROOT / "tools/occurrences.py", Path(__file__).resolve()]
    inputs += [OUT / "source_adjudications.csv", OUT / "source_identity_map.csv", OUT / "older_candidate_adjudications.csv"]
    inputs += sorted((ROOT / "work/codex/loop3").glob("out_*.json"))
    pre = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    h, e = build(), effort()
    post = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    if pre != post:
        raise RuntimeError("source changed while building")
    outputs = [OUT / x for x in ("name_classifications.csv", "material_links.csv", "accepted_occurrence_links.csv",
                                "horizons_reviewed.csv", "effort_reviewed.csv", "older_records_screen.csv")]
    receipt = {"inputs": pre, "outputs": {str(p.relative_to(ROOT)): sha(p) for p in outputs},
               "rows": len(h), "dispositions": h.groupby(["source", "reading", "disposition"]).size().to_dict()}
    receipt["dispositions"] = {"|".join(k): int(v) for k, v in receipt["dispositions"].items()}
    (OUT / "build_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt["dispositions"], indent=2))


if __name__ == "__main__":
    main()
