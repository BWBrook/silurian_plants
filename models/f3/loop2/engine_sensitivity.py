# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///
"""Frozen-engine influence and chronology diagnostics; no transferred qualification."""

import argparse
import csv
import hashlib
import json
import math
import platform
import sys
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import replace
from pathlib import Path

import numpy as np
import scipy

HERE = Path(__file__).resolve().parent
F3 = HERE.parent
ROOT = F3.parent.parent
sys.path.insert(0, str(F3))
import designs as dz
import envelope as ev
import m2


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def bound_inputs():
    names = ["envelope.py", "sim.py", "designs.py", "m2.py", "designs/m2.toml", "out/m2_results.csv"]
    paths = [F3 / x for x in names]
    paths += [ROOT / "data/timescale.csv"]
    paths += [ROOT / "data/units" / x for x in
              ("libya_appendix1.csv", "libya_chart_reports.csv", "libya_prose_support.csv")]
    paths += [HERE / "robustness_design.json", Path(__file__),
              ROOT / "docs/audits/2026-11-01-loop2-count-gate.md"]
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def cases(config):
    e = config["engine_sensitivities"]
    variants = [("baseline", "none", "chart", "stage")]
    variants += [("omit-" + w, w, "chart", "stage") for w in e["leave_out"] if w != "none"]
    variants += [("ages-" + a, "none", a, "stage") for a in e["age_scenarios"] if a != "chart"]
    variants += [("allocation-" + a, "none", "chart", a) for a in e["allocations"] if a != "stage"]
    return [(name, omit, age, alloc, rho) for name, omit, age, alloc in variants for rho in e["rho"]]


def make_problem(case):
    name, omit, age_name, allocation, rho = case
    decl = dz.declarations()
    design = next(d for d in decl["design"] if d["id"] == "LY-MZ-CU")
    variant = {k: v for k, v in design["primary"].items() if k != "min_ref_units"}
    variant["allocation"] = allocation
    built = dz.build(design, variant)
    built.rows = [r for r in built.rows if r.cluster_name != omit]
    units, _ = built.units(rho)
    spec = replace(dz.spec(decl, 2.0, 5), age_scenario=age_name)
    age = ev.AgeModel.load(scenario=age_name)
    return built, ev.Problem(units, spec, age), decl


def evaluate(case):
    started = time.perf_counter()
    name, omit, age, allocation, rho = case
    built, pr, decl = make_problem(case)
    passed, screen_lr, screen_crit = m2.screen(pr)
    row = dict(case=name, omitted_well=omit, age_scenario=age, allocation=allocation,
               rho=rho, status="unqualified-sensitivity", tau=pr.tau, n_ref=pr.n_ref,
               k_ref=int(pr.rd.sum()), n_old=pr.n_old, older_detections=int(pr.od.sum()),
               screen_pass=passed, screen_lr=screen_lr, screen_crit=screen_crit,
               exposure459_1=pr.exposure(459.1), reference_rate=float(pr.r_ref[0]))
    for cls in ("H0", "H0c"):
        b = pr.fstar(cls, 459.1)
        row[f"fstar_{cls}"] = b.value
        row[f"state_{cls}"] = b.state
        row[f"converged_{cls}"] = bool(b.converged)
    for f in (1.0, 0.1, 0.01):
        result = pr.origin_set("H0", f, pr.grid(decl["common"]["origin_step_ma"]), start=459.1)
        row[f"window_{f:g}"] = "unbounded" if result.unbounded else result.older_endpoint
        row[f"window_ok_{f:g}"] = bool(result.ok.all()) and result.connected
    row["failed_fits"] = pr.n_failed
    row["seconds"] = time.perf_counter() - started
    return row


def baseline_check(rows):
    with open(F3 / "out/m2_results.csv", newline="") as f:
        old = {float(r["rho"]): r for r in csv.DictReader(f)
               if r["design"] == "LY-MZ-CU" and r["primary"] == "True"}
    checks = []
    for r in rows:
        if r["case"] != "baseline":
            continue
        reference = old[r["rho"]]
        for cls in ("H0", "H0c"):
            error = abs(r[f"fstar_{cls}"] - float(reference[f"fstar_{cls}_459.1"]))
            checks.append(dict(rho=r["rho"], quantity=f"fstar_{cls}", difference=error,
                               tolerance=0.0011, passes=error <= 0.0011))
        for f in (1.0, 0.1, 0.01):
            key = f"window_{f:g}"
            same = str(r[key]) == reference[key] if isinstance(r[key], str) else abs(r[key] - float(reference[key])) < 0.011
            checks.append(dict(rho=r["rho"], quantity=key, passes=same))
    if not all(c["passes"] for c in checks):
        raise AssertionError(checks)
    return checks


def reference_inventory():
    decl = dz.declarations()
    rows = []
    for design_id in ("LY-MZ-CU", "LY-XW-CO"):
        design = next(d for d in decl["design"] if d["id"] == design_id)
        variant = {k: v for k, v in design["primary"].items() if k != "min_ref_units"}
        b = dz.build(design, variant)
        pr = m2.problem(b, decl, 1.0, 2.0, 5)
        for well in sorted({r.cluster_name for r in b.rows}):
            rr = [r for r in b.rows if r.cluster_name == well]
            ref = [r for r in rr if r.old <= pr.s_star and r.young >= pr.s_star-pr.spec.reference_stages+1]
            old = [r for r in rr if r.old > pr.s_star]
            rows.append(dict(design=design_id, well=well, n_ref=len(ref), positive_ref=sum(r.d for r in ref),
                             n_old=len(old), positive_old=sum(r.d for r in old),
                             reference_depths=";".join(f"{r.depth:g}:{r.d}" for r in ref),
                             interpretation="not a matched core-cutting experiment; no contamination estimate"))
    return rows


def write_csv(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    if dz.DESIGNS.resolve() != (F3 / "designs/m2.toml").resolve():
        ap.error("this sensitivity is bound to designs/m2.toml")
    if not 1 <= args.workers <= 4:
        ap.error("local workload permits 1–4 workers")
    before = bound_inputs()
    config = json.loads((HERE / "robustness_design.json").read_text())
    jobs = cases(config)
    if args.smoke:
        jobs = [next(c for c in jobs if c[0] == "baseline" and c[-1] == 1.0)]
    started = time.perf_counter()
    with ProcessPoolExecutor(max_workers=args.workers) as pool:
        rows = list(pool.map(evaluate, jobs))
    checks = baseline_check(rows)
    if bound_inputs() != before:
        raise RuntimeError("inputs changed during run")
    out = HERE / "out"
    out.mkdir(exist_ok=True)
    tag = "engine_smoke" if args.smoke else "engine_sensitivity"
    table = out / (tag + ".csv")
    write_csv(table, rows)
    inventory = out / (tag + "_reference_inventory.csv")
    write_csv(inventory, reference_inventory())
    if bound_inputs() != before:
        raise RuntimeError("inputs changed during inventory construction")
    payload = dict(status="unqualified-sensitivity; frozen baseline reproduced only", cases=len(rows),
                   input_sha256=before, outputs={p.name: digest(p) for p in (table, inventory)},
                   baseline_checks=checks, numerical_failures=sum(r["failed_fits"] for r in rows),
                   all_delivered_converged=all(r["converged_H0"] and r["converged_H0c"] and
                                               all(r[f"window_ok_{f:g}"] for f in (1.0, 0.1, 0.01)) for r in rows))
    payload["seconds"] = time.perf_counter()-started
    payload["runtime"] = dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__)
    (out / (tag + ".json")).write_text(json.dumps(payload, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k: payload[k] for k in ("status", "cases", "seconds", "numerical_failures", "all_delivered_converged")}))


if __name__ == "__main__":
    main()
