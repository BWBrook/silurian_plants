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

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "studies/f3/tools"))
from occurrences import LAND, MARGINAL, unit_of

OUT = ROOT / "studies/f3/data/macro"
PBDB = ROOT / "data/eprp/record"
OCC = ROOT / "studies/f3/data/occurrences"
YOUNG, OLD, DOMAIN = 393.47, 445.2, 469.4
EMBRYOPHYTE = {"rhyniophytoid_cooksonioid", "lycophyte_line", "euphyllophyte", "tracheophyte_indet",
               "polysporangiophyte_indet", "embryophyte_axis_indet", "bryophyte_grade"}
BODY_CHANNELS = {"megafossil", "mesofossil"}
UNRESOLVED_UNITS = {"M-yea-unspecified", "M-kazakh-lycophytes", "M-kazakh-zosterophyllum",
                    "M-cooksonella-kazakhstan", "M-aberlemnia-krizii", "M-xinjiang-santanhu",
                    "M-xinjiang-zosterophyllum"}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def save(name, rows):
    rows.to_csv(OUT / name, index=False, lineterminator="\n")


def stage_ages(scale):
    if scale.stage.duplicated().any():
        raise ValueError("timescale stages must be unique")
    top = scale.base_ma.shift(1)
    if top.isna().iloc[-1]:
        raise ValueError("timescale does not provide numerical stage tops")
    return dict(zip(scale.stage, scale.base_ma)), dict(zip(scale.stage, top))


def _flag(value, field):
    if value not in {"yes", "no"}:
        raise ValueError(f"{field} must be yes or no")
    return value == "yes"


def body_membership_rows(obs, assignments, scale, membership):
    """Validate and materialise adjudicated body membership outside body channels."""
    required = {"membership_id", "obs_id", "source_channel", "readings", "stage_oldest",
                "stage_youngest", "b0", "b1", "b2", "disposition", "unit_scope",
                "evidence_source", "evidence_locator", "reason"}
    missing = required - set(membership)
    if missing:
        raise ValueError(f"body membership is missing columns: {sorted(missing)}")
    if membership.membership_id.duplicated().any() or membership.obs_id.duplicated().any():
        raise ValueError("body membership identifiers and observation identifiers must be unique")
    observations = obs.set_index("obs_id")
    if not observations.index.is_unique:
        raise ValueError("observation identifiers must be unique")
    base, top = stage_ages(scale)
    rows = []
    for decision in membership.itertuples(index=False):
        if decision.obs_id not in observations.index:
            raise ValueError(f"unknown body-membership observation: {decision.obs_id}")
        observation = observations.loc[decision.obs_id]
        if observation.channel != decision.source_channel:
            raise ValueError(f"source-channel mismatch for {decision.obs_id}")
        b0, b1, b2 = (_flag(getattr(decision, key), key) for key in ("b0", "b1", "b2"))
        if (b2 and not b1) or (b1 and not b0):
            raise ValueError(f"body-category nesting failed for {decision.obs_id}")
        accepted = b0 or b1 or b2
        if accepted != (decision.disposition == "accepted"):
            raise ValueError(f"body-membership disposition disagrees with categories for {decision.obs_id}")
        readings = decision.readings.split(";")
        if len(readings) != len(set(readings)) or not set(readings) <= {"main", "inclusive"}:
            raise ValueError(f"invalid body-membership readings for {decision.obs_id}")
        if accepted and set(readings) != {"main", "inclusive"}:
            raise ValueError(f"accepted body membership requires main and inclusive: {decision.obs_id}")
        matched = assignments[(assignments.obs_id == decision.obs_id) & assignments.reading_id.isin(readings)]
        expected = {(reading, decision.stage_oldest, decision.stage_youngest) for reading in readings}
        observed = set(zip(matched.reading_id, matched.stage_oldest, matched.stage_youngest))
        if observed != expected or not matched.event.eq("E2").all():
            raise ValueError(f"body-membership age/readings drifted for {decision.obs_id}")
        if not accepted:
            continue
        if decision.unit_scope != "one_locality_age_unit":
            raise ValueError(f"unsupported accepted unit scope for {decision.obs_id}")
        try:
            older, younger = base[decision.stage_oldest], top[decision.stage_youngest]
        except KeyError as exc:
            raise ValueError(f"unknown timescale stage in body membership: {exc.args[0]}") from exc
        if not older > younger:
            raise ValueError(f"invalid numerical stage interval for {decision.obs_id}")
        status = "primary" if older > YOUNG and younger < DOMAIN else "outside_analysis_window"
        for reading in readings:
            rows.append({"horizon_id": "tail:" + decision.obs_id, "source": "tail",
                         "source_channel": observation.channel, "reading": reading,
                         "max_ma": older, "min_ma": younger, "b0": b0, "b1": b1, "b2": b2,
                         "names": observation.reported_as, "low_confidence": False,
                         "region": observation.palaeo_unit,
                         "region_basis": "curated occurrence source; explicit cross-channel body adjudication",
                         "cc": observation.country,
                         "locality": str(observation.country) + "|" + str(observation.locality).strip().lower(),
                         "material_status": "curated category adjudication; " + decision.unit_scope,
                         "eligible_primary": status == "primary", "disposition": status,
                         "source_locator": decision.evidence_source + ": " + decision.evidence_locator,
                         "age_group": str(younger) + "|" + str(older)})
    return pd.DataFrame(rows)


def explicit_links(obs, occurrence):
    links = []
    for _, r in obs[obs.channel.isin(BODY_CHANNELS)].iterrows():
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
    classes = pd.read_csv(OUT / "name_classifications.csv")
    if classes.name.duplicated().any():
        raise ValueError("duplicate name classifications")
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
    g["source_channel"] = "pbdb"
    g["reading"] = "all"
    g["region"] = [unit_of(r.cc, r.state) for r in g.itertuples()]
    g["region_basis"] = "approximate country/state assignment; not independently reconstructed"
    xiemisitai = g.collection_no.eq(278439)
    if xiemisitai.sum() != 1 or g.loc[xiemisitai, "formation"].iloc[0].lower() != "xiemisitai":
        raise ValueError("Xiemisitai collection 278439 is missing or changed")
    g.loc[xiemisitai, "region"] = "Kazakhstania"
    g.loc[xiemisitai, "region_basis"] = (
        "West Junggar Arc; grouped with Kazakhstania for analysis; Liu et al. 2024, "
        "DOI 10.1016/j.palaeo.2023.111903"
    )
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
    base, top = stage_ages(scale)
    ra = pd.read_csv(OCC / "reading_assignments.csv")
    ra = ra[ra.event.isin(["E3", "E4", "E5"]) & ~ra.obs_id.str.startswith("M-pbdb-") & ra.same_material_as.isna()]
    channels = ra.obs_id.map(obs.set_index("obs_id").channel)
    if channels.isna().any() or not channels.isin(BODY_CHANNELS).all():
        bad = sorted(ra.loc[channels.isna() | ~channels.isin(BODY_CHANNELS), "obs_id"].unique())
        raise ValueError(f"body events from unadjudicated source channels: {bad}")
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
        tail.append({"horizon_id": "tail:" + oid, "source": "tail", "source_channel": r.channel,
                     "reading": reading, "max_ma": older, "min_ma": younger,
                     "b0": True, "b1": rows.event.isin(["E3", "E5"]).any(),
                     "b2": rows.event.eq("E5").any(), "names": r.reported_as,
                     "low_confidence": False, "region": r.palaeo_unit, "region_basis": "curated occurrence source",
                     "cc": r.country, "locality": str(r.country) + "|" + str(r.locality).strip().lower(),
                     "material_status": "curated observation; " + str(r.horizon), "eligible_primary": status == "primary",
                     "disposition": status, "source_locator": str(r.source_ids) + ": " + str(r.locator),
                     "age_group": str(younger) + "|" + str(older)})
    body_membership = pd.read_csv(OUT / "body_membership.csv", keep_default_na=False)
    admitted = body_membership_rows(obs, pd.read_csv(OCC / "reading_assignments.csv"), scale, body_membership)
    fields = list(tail[0])
    h = pd.concat([g[fields], pd.DataFrame(tail), admitted[fields]], ignore_index=True)
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
    xiemisitai = r.collection_no.eq(278439)
    if xiemisitai.sum() != 1 or r.loc[xiemisitai, "formation"].iloc[0].lower() != "xiemisitai":
        raise ValueError("Xiemisitai effort collection 278439 is missing or changed")
    r.loc[xiemisitai, "region"] = "Kazakhstania"
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
    inputs += [ROOT / "data/timescale.csv", ROOT / "studies/f3/tools/occurrences.py", Path(__file__).resolve()]
    inputs += [OUT / "source_adjudications.csv", OUT / "source_identity_map.csv",
               OUT / "older_candidate_adjudications.csv", OUT / "name_classifications.csv",
               OUT / "body_membership.csv"]
    pre = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    h, e = build(), effort()
    post = {str(p.relative_to(ROOT)): sha(p) for p in inputs}
    if pre != post:
        raise RuntimeError("source changed while building")
    outputs = [OUT / x for x in ("material_links.csv", "accepted_occurrence_links.csv",
                                "horizons_reviewed.csv", "effort_reviewed.csv", "older_records_screen.csv")]
    receipt = {"inputs": pre, "outputs": {str(p.relative_to(ROOT)): sha(p) for p in outputs},
               "rows": len(h), "dispositions": h.groupby(["source", "reading", "disposition"]).size().to_dict()}
    receipt["dispositions"] = {"|".join(k): int(v) for k, v in receipt["dispositions"].items()}
    (OUT / "build_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt["dispositions"], indent=2))


if __name__ == "__main__":
    main()
