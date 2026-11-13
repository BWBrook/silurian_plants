# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.4", "pandas==3.1.1", "scipy==1.18.1", "matplotlib==3.11.2"]
# ///
"""Separate public downstream reproduction, raw rebuild and private source checks."""

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LOOP = Path("studies/f3/models/loop3")
BASE = ["reviewed_bounds.csv", "age_sensitivity.csv", "classical_comparison.csv",
        "primary_unit_membership.csv", "shape_diagnostics.csv", "delay_sensitivity.csv"]
FLOAT_TOLERANCE = 1e-9
TOLERANCE_FILES = {LOOP / "out/stage2_murzuq/dependence_sensitivity.csv"}
IDENTITY_COLUMNS = {
    "grouping", "frailty_shape", "separate_well_rates", "n_reference", "n_older",
    "scope", "excluded_well",
}


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def execute(command, cwd):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(command)} failed:\n{result.stdout}\n{result.stderr}")


def compare_csv(reference, candidate, *, tolerance=FLOAT_TOLERANCE, identity_columns=()):
    """Compare a CSV strictly except for declared floating-point round-off.

    Headers, row count/order, and identity columns must match exactly. Other fields
    must either match exactly as text or parse as finite numbers within ``tolerance``.
    The result retains both file hashes so a receipt cannot be mistaken for byte
    identity.
    """
    with reference.open(newline="") as ref_file, candidate.open(newline="") as cand_file:
        ref_reader, cand_reader = csv.reader(ref_file), csv.reader(cand_file)
        ref_header, cand_header = next(ref_reader, None), next(cand_reader, None)
        if ref_header != cand_header:
            return {"status": "FAIL", "reason": "schema differs", "column": None}
        ref_rows, cand_rows = list(ref_reader), list(cand_reader)
    if len(ref_rows) != len(cand_rows):
        return {"status": "FAIL", "reason": "row count differs", "column": None}
    identity_columns = set(identity_columns)
    for row_number, (ref_row, cand_row) in enumerate(zip(ref_rows, cand_rows), start=2):
        if len(ref_row) != len(ref_header) or len(cand_row) != len(cand_header):
            return {"status": "FAIL", "reason": "row width differs", "row": row_number}
        for column, (ref_value, cand_value) in enumerate(zip(ref_row, cand_row), start=0):
            name = ref_header[column]
            if name in identity_columns or ref_value == cand_value:
                if ref_value != cand_value:
                    return {"status": "FAIL", "reason": "identity value differs", "row": row_number, "column": name}
                continue
            try:
                ref_number, cand_number = float(ref_value), float(cand_value)
            except ValueError:
                return {"status": "FAIL", "reason": "non-numeric value differs", "row": row_number, "column": name}
            if not (abs(ref_number - cand_number) <= tolerance):
                return {"status": "FAIL", "reason": "numeric value exceeds tolerance", "row": row_number, "column": name,
                        "reference": ref_number, "candidate": cand_number, "tolerance": tolerance}
    return {"status": "PASS", "rows": len(ref_rows), "columns": len(ref_header), "tolerance": tolerance}


def compare_output(reference, candidate):
    """Compare one output, using tolerance only for the known optimiser CSV."""
    reference_hash, candidate_hash = digest(reference), digest(candidate)
    relative = reference.relative_to(ROOT)
    if relative in TOLERANCE_FILES:
        comparison = compare_csv(reference, candidate, identity_columns=IDENTITY_COLUMNS)
    else:
        comparison = {"status": "PASS" if reference_hash == candidate_hash else "FAIL",
                      "reason": "byte identity" if reference_hash == candidate_hash else "byte hash differs"}
    comparison.update({"path": str(relative), "reference_sha256": reference_hash,
                       "candidate_sha256": candidate_hash})
    return comparison


def source_checks():
    relative = Path("library/closed/abuhmida2013-thesis-related_macbook20261030.pdf")
    needed = [ROOT / relative]
    manifest_rows = [row for row in csv.reader((ROOT / "library/closed.tsv").open(), delimiter="\t")
                     if row and row[0] == "abuhmida2013-thesis-related_macbook20261030"]
    if len(manifest_rows) != 1:
        raise RuntimeError("expected one Abuhmida source-manifest row")
    row = manifest_rows[0]
    expected_bytes, expected_hash, public_route = int(row[7]), row[8], row[4]
    missing = [str(p.relative_to(ROOT)) for p in needed if not p.is_file()]
    if missing:
        print(json.dumps({"scope": "private source checks", "status": "SKIPPED",
                          "missing": missing, "expected_bytes": expected_bytes,
                          "expected_sha256": expected_hash, "public_route": public_route,
                          "exact_2011_target": False,
                          "reason": "copyrighted sources are not distributed"}))
        return
    actual_bytes, actual_hash = needed[0].stat().st_size, digest(needed[0])
    if actual_bytes != expected_bytes:
        raise RuntimeError("Abuhmida thesis byte count differs from library/closed.tsv")
    if actual_hash != expected_hash:
        raise RuntimeError("Abuhmida thesis source hash differs from library/closed.tsv")
    execute([sys.executable, "studies/f3/tools/loop2_observations.py", "check"], ROOT)
    print(json.dumps({"scope": "held thesis observation check", "status": "PASS",
                      "source": str(relative), "bytes": actual_bytes,
                      "sha256": actual_hash, "public_route": row[4],
                      "exact_2011_target": False,
                      "note": "related 2013 thesis only; source text remains private"}))


def reproduce(mode):
    run_utc = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    tracked = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode().split("\0")
    compared = []
    with tempfile.TemporaryDirectory(prefix="silurian-reproduction-") as name:
        clone = Path(name)
        for relative in filter(None, tracked):
            p = ROOT / relative
            if p.is_symlink() or not p.is_file():
                continue
            q = clone / relative
            q.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(p, q)
        if mode == "source":
            path = ROOT / "data/external/scripts/fetch_pbdb_snapshot.py"
            spec = importlib.util.spec_from_file_location("pbdb_fetch", path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            manifest = json.loads((ROOT / "data/external/pbdb-snapshot.json").read_text())
            module.restore(clone / manifest["path"])
            execute([sys.executable, str(LOOP / "build_reviewed.py")], clone)
            for filename in ("horizons_reviewed.csv", "effort_reviewed.csv", "name_classifications.csv",
                             "material_links.csv", "accepted_occurrence_links.csv", "older_records_screen.csv"):
                compared.append(Path("studies/f3/data/macro") / filename)
        for script in ("analysis.py", "simulation.py", "suppression_sensitivity.py"):
            execute([sys.executable, str(LOOP / script)], clone)
        compared += [LOOP / "out" / filename for filename in BASE + ["simulation_results.csv", "suppression_sensitivity.csv"]]
        for script in ("frontier.py", "murzuq_stage2.py", "interval_feasibility.py"):
            execute([sys.executable, str(LOOP / script)], clone)
        compared += [LOOP / "out/frontier.csv", LOOP / "out/influential_taxa.csv"]
        for directory in ("stage2_murzuq", "stage2_interval"):
            compared += [p.relative_to(ROOT) for p in sorted((ROOT / LOOP / "out" / directory).glob("*.csv"))]
        if mode == "source":
            execute([sys.executable, str(LOOP / "timescale_sensitivity.py")], clone)
            compared += [p.relative_to(ROOT) for p in sorted((ROOT / LOOP / "out/stage2_timescale").glob("*.csv"))]
        comparisons = []
        for path in compared:
            comparisons.append(compare_output(ROOT / path, clone / path))
        mismatches = [item for item in comparisons if item["status"] != "PASS"]
        if mismatches:
            raise RuntimeError("reproduction differs: " + json.dumps(mismatches, sort_keys=True))
    receipt = {"mode": mode, "status": "PASS", "compared": comparisons,
               "source_pdf_checks": "not run; separate check-sources target", "frozen_qualification": "not regenerated",
               "timescale_rebuild": "PASS" if mode == "source" else "SKIPPED: requires archived raw PBDB input; use source target",
               "scope": "byte identity for selected outputs except the declared optimiser CSV, where schema, row order, identity fields and non-numeric values are exact and numeric fields use absolute tolerance 1e-9; not scientific validation"}
    out = ROOT / "studies/f3/docs/audits" / f"{run_utc[:10]}-reproduction-{mode}.json"
    receipt["run_utc"] = run_utc
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"mode": mode, "status": "PASS", "compared_files": len(compared)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("derived", "source", "sources"))
    args = parser.parse_args()
    source_checks() if args.mode == "sources" else reproduce(args.mode)
