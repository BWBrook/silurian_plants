# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""Additive Borenshult reading screen; no geological-age test or qualification."""

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

import screen

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/units/borenshult_review"
OUT = Path(__file__).resolve().parent / "out/borenshult_review"
READINGS = ("figure3-definite", "figure4-definite", "concordant-definite")
DEFINITE = {"BOR-43.1", "BOR-41.9", "BOR-41.1", "BOR-40.35", "BOR-40.2", "BOR-33.05"}
POSSIBLE = {"BOR-48.2", "BOR-34"}
ZERO_STATES = {"explicit_non_detection", "not_reported"}
CONFLICT = "figure3-definite_figure4-category-not-listed"


def read_csv(path):
    with Path(path).open(newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def validate(rows, readings, spec):
    ids = [r["reading_id"] for r in readings]
    require(len(ids) == len(set(ids)) and set(ids) == set(READINGS), "reading definitions must match all three alternatives")
    require(spec["reading_ids"] == list(READINGS), "specification reading order differs")
    require(spec["target_f"] == screen.TARGET_F and spec["critical_value"] == screen.CRIT
            and spec["ceilings"] == screen.CEILINGS and spec["design"] == screen.DESIGN,
            "screen settings differ from declared homogeneous design")
    require(spec["fixed_age_test"] is False and spec["qualification"] == "not performed",
            "this screen has no fixed-age test or qualification")
    base = {r["unit_id"]: r for r in read_csv(ROOT / "data/units/outcomes.csv")
            if r["unit_id"].startswith("BOR-") and r["event_id"] == "E1" and r["reading_id"] == "inclusive"}
    depth = {f"BOR-{r['depth_m']}": r["depth_m"] for r in read_csv(ROOT / "data/units/borenshult_ages.csv")}
    reporting = {r["unit_id"]: r for r in read_csv(ROOT / "data/units/borenshult_reporting.csv")}
    require(len(base) == 34 and set(base) == set(depth) == set(reporting), "canonical Borenshult inventory differs")
    keys = [(r["reading_id"], r["unit_id"]) for r in rows]
    require(len(keys) == len(set(keys)), "duplicate reading/unit ID")
    require(set(keys) == {(reading, uid) for reading in READINGS for uid in base},
            "outcomes must cover exactly all 34 units for each reading")
    for r in rows:
        uid, reading = r["unit_id"], r["reading_id"]
        expected = ("unresolved" if uid in POSSIBLE or (reading == "concordant-definite" and uid == "BOR-41.1") else "detected"
                    if uid in DEFINITE and (reading == "figure3-definite" or uid != "BOR-41.1")
                    else base[uid]["outcome"])
        require(r["event_id"] == "E1" and r["depth_m"] == depth[uid], f"{uid}: event or depth mismatch")
        require(r["outcome"] == expected, f"{reading}/{uid}: outcome contradicts published reading mapping")
        require(r["figure3_report"] == ("definite" if uid in DEFINITE else "possible" if uid in POSSIBLE
                                       else "no-trilete-symbol"), f"{uid}: Figure 3 mapping mismatch")
        require(r["figure4_report"] == reporting[uid]["E1_source_report"]
                and r["figure4_taxa"] == reporting[uid]["E1_reported_taxa"], f"{uid}: Figure 4 mapping mismatch")
        require(r["conflict"] == (CONFLICT if uid == "BOR-41.1" else ""), f"{uid}: figure conflict not preserved")
        require(r["source_ids"] == base[uid]["source_ids"] and r["source_locator"] and r["assessment_basis"],
                f"{uid}: source provenance missing or changed")


def calculate(rows):
    results, membership = [], []
    for reading in READINGS:
        mine = {r["unit_id"]: r for r in rows if r["reading_id"] == reading}
        depth = {uid: float(r["depth_m"]) for uid, r in mine.items()}
        ordered = lambda units: sorted(units, key=lambda uid: depth[uid], reverse=True)
        hits = {uid for uid, r in mine.items() if r["outcome"] == "detected"}
        boundary = max(depth[uid] for uid in hits)
        older = {uid for uid in mine if depth[uid] > boundary}
        reference = set(mine) - older
        unresolved = {uid for uid, r in mine.items() if r["outcome"] == "unresolved"}
        zeros = {uid for uid, r in mine.items() if r["outcome"] in ZERO_STATES}
        old_trials = older & zeros
        for conversion in ("complete reported-category", "explicit-only (optimistic diagnostic)"):
            ref_trials = reference - unresolved if conversion == "complete reported-category" else {
                uid for uid in reference if mine[uid]["outcome"] in {"detected", "explicit_non_detection"}}
            k, n, m = len(hits & ref_trials), len(ref_trials), len(old_trials)
            membership.append(dict(reading=reading, reference_conversion=conversion, onset_depth_m=boundary,
                                   older_inventory_ids=ordered(older), reference_inventory_ids=ordered(reference),
                                   older_trial_ids=ordered(old_trials), reference_trial_ids=ordered(ref_trials),
                                   detected_reference_ids=ordered(hits & ref_trials),
                                   unresolved_older_ids=ordered(older & unresolved),
                                   unresolved_reference_ids=ordered(reference & unresolved),
                                   omitted_reference_not_reported_ids=ordered({uid for uid in reference - ref_trials
                                                                            if mine[uid]["outcome"] == "not_reported"})))
            for cls, ceiling in screen.CEILINGS.items():
                known, profiled = screen.smallest_excludable(k, n, m, ceiling)
                lr = screen.profile_lr(k, n, m, screen.TARGET_F)
                results.append(dict(reading=reading, reference_conversion=conversion, onset_depth_m=boundary,
                                    design=screen.DESIGN, exposure="all eligible older units fully exposed",
                                    k=k, n_ref=n, m_older=m, older_inventory_count=len(older),
                                    unresolved_older_count=len(older & unresolved), history_class=cls,
                                    ceiling=ceiling, target_f=screen.TARGET_F, critical_value=screen.CRIT,
                                    lr_known_at_target=2 * m * screen.TARGET_F * screen.rate(k, n),
                                    lr_profile_at_target=lr,
                                    lr_known_at_ceiling=2 * m * ceiling * screen.rate(k, n),
                                    lr_profile_at_ceiling=screen.profile_lr(k, n, m, ceiling),
                                    f_known=known, f_profile=profiled, excludes_target=lr > screen.CRIT,
                                    verdict="ceiling-limited" if math.isinf(profiled) else "constant-path threshold finite",
                                    fixed_age_test=False, qualification="not performed"))
    return results, membership


def run(data=DATA, out=OUT):
    data, out = Path(data), Path(out)
    require(not out.exists(), "output directory already exists; select a fresh --out-dir")
    spec = json.loads((data / "screen_spec.json").read_text())
    rows, readings = read_csv(data / "outcomes.csv"), read_csv(data / "readings.csv")
    validate(rows, readings, spec)
    preserved = spec["preserved_qualification_files"]
    require(all(sha256(ROOT / name) == digest for name, digest in preserved.items()),
            "frozen qualification inputs differ from the review baseline")
    source = ROOT / spec["source_file"]
    require(sha256(source) == spec["source_sha256"], "published source checksum differs")
    paths = {name: ROOT / name for name in (
        "data/units/outcomes.csv", "data/units/borenshult_ages.csv", "data/units/borenshult_reporting.csv",
        "data/units/source_files.csv", "models/f3/screen.py", "models/f3/borenshult_review.py")}
    paths.update({spec["source_file"]: source, spec["source_audit"]: ROOT / spec["source_audit"]})
    published = [r for r in read_csv(ROOT / "data/units/source_files.csv")
                 if r["source_id"] in {"rubinstein2019-open", "rubinstein2023"}]
    require({r["source_id"] for r in published} == {"rubinstein2019-open", "rubinstein2023"},
            "published source registry incomplete")
    for item in published:
        path = ROOT / item["path"]
        require(sha256(path) == item["sha256"], f"published source checksum differs: {item['source_id']}")
        paths[item["path"]] = path
    paths.update({f"review/{name}": data / name for name in ("outcomes.csv", "readings.csv", "screen_spec.json", "README.md")})
    before = {name: sha256(path) for name, path in paths.items()}
    results, membership = calculate(rows)
    require(before == {name: sha256(path) for name, path in paths.items()}, "review inputs changed during calculation")
    require(all(sha256(ROOT / name) == digest for name, digest in preserved.items()),
            "frozen qualification inputs changed during calculation")
    out.mkdir(parents=True)
    with (out / "screen.csv").open("x", newline="") as handle:
        writer = csv.DictWriter(handle, list(results[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)
    (out / "membership.json").write_text(json.dumps(membership, indent=2) + "\n")
    receipt = dict(schema=spec["schema"], qualification="not performed", fixed_age_test=False,
                   limitation="Fully exposed older trials; no numerical chronology or fixed-459.1 Ma result. "
                              "Homogeneous independent design only; constant-path thresholds are not full H1 bounds.",
                   input_sha256=before, preserved_qualification_files=preserved,
                   preserved_qualification_files_unchanged=True,
                   membership=membership, results_rows=len(results),
                   output_sha256={name: sha256(out / name) for name in ("screen.csv", "membership.json")})
    (out / "receipt.json").write_text(json.dumps(receipt, indent=2, allow_nan=False) + "\n")
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DATA)
    parser.add_argument("--out-dir", type=Path, default=OUT)
    args = parser.parse_args()
    results = run(args.data_dir, args.out_dir)
    print(f"Wrote {len(results)} homogeneous screen rows to {args.out_dir}")
    print("All-exposure diagnostic only; no fixed-459.1 Ma test or new qualification.")


if __name__ == "__main__":
    main()
