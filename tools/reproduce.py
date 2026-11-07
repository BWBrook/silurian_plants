# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy==2.5.4", "pandas==3.1.1", "scipy==1.18.1", "matplotlib==3.11.2"]
# ///
"""Separate public downstream reproduction, raw rebuild and private source checks."""

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOOP = Path("models/f3/loop3")
BASE = ["reviewed_bounds.csv", "age_sensitivity.csv", "classical_comparison.csv",
        "primary_unit_membership.csv", "shape_diagnostics.csv", "delay_sensitivity.csv"]


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def execute(command, cwd):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    if result.returncode:
        raise RuntimeError(f"{' '.join(command)} failed:\n{result.stdout}\n{result.stderr}")


def source_checks():
    needed = [ROOT / "library/closed/abuhmida2013-thesis-related_macbook20261030.pdf"]
    missing = [str(p.relative_to(ROOT)) for p in needed if not p.is_file()]
    if missing:
        print(json.dumps({"scope": "private source checks", "status": "SKIPPED",
                          "missing": missing, "reason": "copyrighted sources are not distributed"}))
        return
    execute([sys.executable, "tools/loop2_observations.py", "check"], ROOT)
    print(json.dumps({"scope": "held thesis observation check", "status": "PASS"}))


def reproduce(mode):
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
                compared.append(Path("data/macro") / filename)
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
        mismatches = [str(p) for p in compared if digest(ROOT / p) != digest(clone / p)]
        if mismatches:
            raise RuntimeError("reproduction differs: " + ", ".join(mismatches))
    receipt = {"mode": mode, "status": "PASS", "compared": {str(p): digest(ROOT / p) for p in compared},
               "source_pdf_checks": "not run; separate check-sources target", "frozen_qualification": "not regenerated",
               "timescale_rebuild": "PASS" if mode == "source" else "SKIPPED: requires archived raw PBDB input; use source target",
               "scope": "byte identity for selected public Loop 3 outputs; not scientific validation"}
    out = ROOT / "docs/audits" / f"2026-11-07-reproduction-{mode}.json"
    out.write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps({"mode": mode, "status": "PASS", "compared_files": len(compared)}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("derived", "source", "sources"))
    args = parser.parse_args()
    source_checks() if args.mode == "sources" else reproduce(args.mode)
