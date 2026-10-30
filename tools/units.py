#!/usr/bin/env python3
"""Validate the source-audited sampling-unit evidence; never coerce unknowns to zero."""

import argparse
import csv
import hashlib
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def rows(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def check(directory=ROOT / "data/units"):
    units = rows(directory / "units.csv")
    outcomes = rows(directory / "outcomes.csv")
    sources = {r["source_id"] for r in rows(directory / "sources.csv")}
    ages = {r["age_model_id"] for r in rows(directory / "age_models.csv")}
    readings = {r["reading_id"] for r in rows(ROOT / "data/occurrences/readings.csv")}
    stages = {r["stage"]: float(r["base_ma"]) for r in rows(ROOT / "data/timescale.csv")}
    observations = {r["obs_id"] for r in rows(ROOT / "data/occurrences/observations.csv")}
    interpretations = {r["interp_id"] for r in rows(ROOT / "data/occurrences/interpretations.csv")}
    errors = []

    def require(condition, message):
        if not condition:
            errors.append(message)

    def references(row, field, allowed):
        for value in filter(None, row[field].split(";")):
            require(value in allowed, f"{row.get('unit_id', '')}: unknown {field} {value}")

    ids = [r["unit_id"] for r in units]
    require(len(ids) == len(set(ids)), "duplicate unit_id")
    material_keys = [(r["section_id"], r["material_id"]) for r in units]
    require(len(material_keys) == len(set(material_keys)), "duplicate material within a section")
    for unit in units:
        uid = unit["unit_id"]
        for field in ["material_id", "source_ids", "source_locator", "deduplication_basis", "age_evidence",
                      "preservation_evidence", "frame_status", "document_cluster", "section_cluster", "locality_cluster"]:
            require(bool(unit[field]), f"{uid}: empty {field}")
        references(unit, "source_ids", sources)
        references(unit, "obs_ids", observations)
        require(unit["age_model_id"] in ages, f"{uid}: unknown age model")
        old, young = unit["stage_oldest"], unit["stage_youngest"]
        require(old in stages and young in stages, f"{uid}: unknown stage")
        if old in stages and young in stages:
            require(stages[old] >= stages[young], f"{uid}: reversed age range")
        require(unit["trial_status"] == "pilot_only", f"{uid}: this evidence release is pilot_only")
        if unit["frame_id"] == "palynodata-2006":
            require(bool(unit["palynodata_doc_ids"]), f"{uid}: missing frame evidence")
        else:
            require(unit["frame_status"] == "outside-frame-new-material", f"{uid}: unresolved frame declaration")

    expected = {(uid, event, reading) for uid in ids for event in ["E1", "E2"] for reading in readings}
    keys = [(r["unit_id"], r["event_id"], r["reading_id"]) for r in outcomes]
    require(len(keys) == len(set(keys)), "duplicate unit/event/reading outcome")
    require(set(keys) == expected, "outcomes must cover exactly every unit x E1/E2 x named reading")
    for outcome in outcomes:
        uid = outcome["unit_id"]
        require(outcome["outcome"] in {"detected", "explicit_non_detection", "not_reported", "unresolved"}, f"{uid}: invalid outcome")
        require(outcome["eligibility"] in {"eligible", "ineligible", "unknown"}, f"{uid}: invalid eligibility")
        require(outcome["reporting_rule"] == "none-evidence-only", f"{uid}: binary reporting rule not adopted")
        for field in ["eligibility_class", "eligibility_evidence", "source_locator", "assessment_basis"]:
            require(bool(outcome[field]), f"{uid}: empty {field}")
        references(outcome, "source_ids", sources)
        references(outcome, "interpretation_ids", interpretations)
    lookup = dict(zip(keys, outcomes))
    for uid in ids:
        for event in ["E1", "E2"]:
            detected = False
            for reading in ["main", "inclusive", "outlier"]:
                row = lookup.get((uid, event, reading))
                if row:
                    require(not detected or row["outcome"] == "detected", f"{uid}/{event}: detection lost in wider reading")
                    detected |= row["outcome"] == "detected"
    for candidate in rows(directory / "candidates.csv"):
        references(candidate, "source_ids", sources)
        for uid in filter(None, candidate["linked_units"].split(";")):
            require(uid in ids, f"candidate {candidate['candidate_id']}: unknown linked unit {uid}")
    frames = rows(directory / "frames.csv")
    frame_ids = [r["study_frame_id"] for r in frames]
    require(len(frame_ids) == len(set(frame_ids)), "duplicate study frame")
    samples = rows(directory / "frame_samples.csv")
    sample_keys = [(r["study_frame_id"], r["sample_label"]) for r in samples]
    require(len(sample_keys) == len(set(sample_keys)), "duplicate frame sample")
    for frame in frames:
        references(frame, "source_ids", sources)
        references(frame, "linked_units", set(ids))
        require(frame["analysis_ready"] == "no", "audited candidate frames are not analysis-ready")
        require(bool(frame["inventory_status"] and frame["remaining_gap"]), "missing frame qualification")
        count = frame["listed_sample_count"]
        if count:
            require(count.isdecimal(), "invalid listed sample count")
            if count.isdecimal():
                require(int(count) == sum(r["study_frame_id"] == frame["study_frame_id"] for r in samples),
                        f"{frame['study_frame_id']}: listed sample count mismatch")
    for sample in samples:
        require(sample["study_frame_id"] in frame_ids, "unknown sample frame")
        require(sample["source_id"] in sources, "unknown frame sample source")
        require(bool(sample["source_locator"]), "missing frame sample source locator")
        require(sample["link_status"] in {"not-linked", "exact-specimen-link", "exact-depth-link", "provisional-depth-match"},
                "invalid material link status")
        linked = sample["linked_unit_id"]
        require((not linked and sample["link_status"] == "not-linked") or
                (linked in ids and sample["link_status"] != "not-linked"), "invalid frame sample link")
    borenshult = {r["linked_unit_id"]: r for r in samples
                 if r["study_frame_id"] == "borenshult2019-2023"}
    reporting = rows(directory / "borenshult_reporting.csv")
    reported_ids = [r["unit_id"] for r in reporting]
    require(len(reported_ids) == len(set(reported_ids)) and set(reported_ids) == set(borenshult),
            "Borenshult reporting must cover each inventoried material once")
    unit_lookup = {r["unit_id"]: r for r in units}
    for row in reporting:
        uid = row["unit_id"]
        sample = borenshult.get(uid, {})
        require(row["depth_m"] == sample.get("depth_m"), f"{uid}: reporting depth mismatch")
        require(row["sample_label"] == sample.get("sample_label"), f"{uid}: reporting sample mismatch")
        require(row["study_frame_id"] == sample.get("study_frame_id"), f"{uid}: reporting frame mismatch")
        references(row, "source_ids", sources)
        require(bool(row["source_locator"] and row["qualification"]), f"{uid}: missing reporting evidence")
        require(row["in_2019_spore_chart"] in {"yes", "no"}, f"{uid}: invalid chart membership")
        for event in ["E1", "E2"]:
            require(row[f"{event}_source_report"] in {
                "reported-presence", "category-not-listed", "study-complement-non-detection"},
                f"{uid}: invalid {event} source report")
        require(bool(row["E1_reported_taxa"]) == (row["E1_source_report"] == "reported-presence"),
                f"{uid}: E1 taxon/report mismatch")
        require((row["in_2019_spore_chart"] == "no") ==
                (row["E2_source_report"] == "study-complement-non-detection"),
                f"{uid}: E2 chart/report mismatch")
    age_rows = rows(directory / "borenshult_ages.csv")
    age_keys = [(r["study_frame_id"], r["sample_label"]) for r in age_rows]
    require(len(age_keys) == len(set(age_keys)) and set(age_keys) == {
        (r["study_frame_id"], r["sample_label"]) for r in borenshult.values()},
        "Borenshult ages must cover each inventoried sample once")
    by_sample = {r["sample_label"]: uid for uid, r in borenshult.items()}
    for row in age_rows:
        uid = by_sample.get(row["sample_label"])
        unit = unit_lookup.get(uid, {})
        require(row["reported_stage"] == unit.get("stage_oldest") == unit.get("stage_youngest"),
                f"{uid}: age stage mismatch")
        require(row["depth_m"] == borenshult.get(uid, {}).get("depth_m"), f"{uid}: age depth mismatch")
        require(bool(row["source_locators"] and row["age_evidence_status"]), f"{uid}: missing age evidence")
    for source_file in rows(directory / "source_files.csv"):
        require(source_file["source_id"] in sources, "unknown file source")
        require(len(source_file["sha256"]) == 64, f"invalid digest for {source_file['path']}")
        local = ROOT / source_file["path"]
        if local.is_file():
            require(hashlib.sha256(local.read_bytes()).hexdigest() == source_file["sha256"],
                    f"source file changed: {source_file['path']}")
    if errors:
        raise ValueError("\n".join(errors))
    return {"units": len(units), "outcomes": len(outcomes), "candidate_frames": len(frames),
            "frame_samples": len(samples),
            "main_E1": dict(Counter(r["outcome"] for r in outcomes if r["event_id"] == "E1" and r["reading_id"] == "main")),
            "main_E2": dict(Counter(r["outcome"] for r in outcomes if r["event_id"] == "E2" and r["reading_id"] == "main"))}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check"])
    parser.parse_args()
    print(check())
