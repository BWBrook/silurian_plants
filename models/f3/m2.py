# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""M2 on the frozen real designs (designs/m2.toml): the screen, and the empirical read-outs.

    uv run models/f3/m2.py screen            # out/m2_screen.csv: every design, variant, rho and reference minimum
    uv run models/f3/m2.py results            # out/m2_results.csv at the qualified critical-value shifts

The screen (S0, S1 in m2.toml) is the function `screen`, called unchanged by qualify.py on every simulated
replicate. It uses the unshifted critical value, so it does not depend on the calibration.
"""

import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

import designs as dz
import envelope as ev

OUT = Path(__file__).resolve().parent / "out"


def potential(u: ev.Units, transported: np.ndarray) -> ev.Units:
    """The units the screen sees (amendment 1): transported (older) outcomes set to 0."""
    return ev.Units(u.young, u.old, u.cls, u.cluster, np.where(transported, 0, u.d), u.mult, u.lo_ma, u.hi_ma)


def screen(pr: ev.Problem) -> tuple[bool, float, float]:
    """(passes, statistic at f = 1 with every older unit exposed, unshifted critical value). pr is built on
    potential(units)."""
    if pr.n_old == 0 or pr.exposure(pr.spec.domain_ma[1]) <= 0:
        return False, 0.0, ev.count_crit(0, pr.spec.alpha)
    T = pr.spec.domain_ma[1]
    crit = ev.count_crit(pr.n_older_detections(T), pr.spec.alpha)
    st = pr.lr("H0c", T, 1.0)
    return bool(st.converged and st.value > crit), float(st.value), crit


def problem(b: dz.Built, decl: dict, rho: float, cluster_k: float, min_ref: int, shift: float = 0.0,
            screened: bool = False) -> ev.Problem:
    u, _ = b.units(rho)
    if screened:
        u = potential(u, np.array([r.transported for r in b.rows]))
    spec = dz.spec(decl, cluster_k, min_ref)
    spec = ev.Spec(**{**spec.__dict__, "crit_shift": shift})
    return ev.Problem(u, spec, ev.AgeModel.load())


def vkey(v: dict) -> str:
    return ";".join(f"{k}={v[k]}" for k in sorted(v))


def is_primary(design: dict, v: dict, min_ref: int) -> bool:
    p = design.get("primary", {})
    return bool(p) and all(v.get(k, p[k]) == p[k] for k in p if k != "min_ref_units") and min_ref == p["min_ref_units"]


def run_screen() -> list[dict]:
    decl = dz.declarations()
    rows = []
    for design in decl["design"]:
        for v in dz.variants(design, decl):
            b = dz.build(design, v)
            for min_ref in decl["common"]["min_ref_units"]:
                for rho in decl["common"]["rho"]:
                    row = dict(design=design["id"], variant=vkey(v), min_ref=min_ref, rho=rho,
                               primary=is_primary(design, v, min_ref))
                    try:
                        pr = problem(b, decl, rho, v["cluster_k"], min_ref, screened=True)
                    except ev.NoFirstAppearance as e:
                        rows.append(row | dict(status=f"S0 fails: {e}", passes=False))
                        continue
                    ok, lr, crit = screen(pr)
                    ref = pr.rd
                    rows.append(row | dict(
                        status="passes" if ok else ("S0 fails: no exposed older unit" if pr.n_old == 0 else "S1 fails"),
                        passes=ok, tau=round(pr.tau, 3), n_ref=pr.n_ref, k_ref=int(ref.sum()),
                        r_ref=";".join(f"{r:.4g}" for r in pr.r_ref), n_old=pr.n_old, older_detections=int(pr.od.sum()),
                        dropped_uncalibrated=pr.n_dropped_uncalibrated, lr_f1=round(lr, 4), crit=round(crit, 4)))
    return rows


T_REPORT = (445.2, 452.8, 458.2, 459.1, 464.0, 469.4, 480.0, 560.0)


def shift_for(design_id: str, rho: float) -> tuple[float | None, str]:
    """The calibrated shift of the design's primary variant at rho, and the qualification result."""
    q = OUT / "qual"
    tag = f"{design_id}_rho{rho:g}"
    cal, acc, st2 = (q / f"{tag}_{p}.json" for p in ("calibrate", "accept", "stage2"))
    if not cal.exists():
        return None, "not qualified"
    delta = json.loads(cal.read_text())["delta"]
    if not acc.exists():
        return delta, "calibrated only"
    result = json.loads(acc.read_text())["result"]
    if result == "borderline" and st2.exists():
        result = json.loads(st2.read_text())["result"]
    return delta, result


def readouts(pr: ev.Problem) -> dict:
    out = {}
    for T in T_REPORT:
        if T <= pr.tau:
            continue
        for K in pr.spec.classes:
            b = pr.fstar(K, T)
            out[f"fstar_{K}_{T:g}"] = "" if b.state == "zero-exposure" else round(b.value, 4)
            out[f"state_{K}_{T:g}"] = b.state + ("" if b.converged else " (not converged)")
    grid = pr.grid(0.5)
    for f in pr.spec.readouts:
        for K in ("H0c", "H0m", "H0"):
            o = pr.origin_set(K, f, grid)
            out[f"origin_{K}_{f:g}"] = "unbounded" if o.unbounded else round(o.older_endpoint, 2)
            out[f"origin_ok_{K}_{f:g}"] = bool(o.ok.all()) and o.connected
        o = pr.origin_set("H0", f, grid, start=459.1)
        out[f"window_{f:g}"] = "unbounded" if o.unbounded else round(o.older_endpoint, 2)
        out[f"window_ok_{f:g}"] = bool(o.ok.all()) and o.connected
    return out


def run_results() -> list[dict]:
    decl = dz.declarations()
    screened = {(r["design"], r["variant"], int(r["min_ref"]), float(r["rho"])): r["passes"] == "True"
                for r in csv.DictReader(open(OUT / "m2_screen.csv"))}
    rows = []
    for design in decl["design"]:
        for v in dz.variants(design, decl):
            b = dz.build(design, v)
            for min_ref in decl["common"]["min_ref_units"]:
                for rho in decl["common"]["rho"]:
                    if not screened[(design["id"], vkey(v), min_ref, rho)]:
                        continue
                    delta, result = shift_for(design["id"], rho)
                    row = dict(design=design["id"], variant=vkey(v), min_ref=min_ref, rho=rho,
                               primary=is_primary(design, v, min_ref), qualification=result,
                               shift="" if delta is None else delta)
                    pr = problem(b, decl, rho, v["cluster_k"], min_ref, shift=delta or 0.0)
                    row.update(tau=pr.tau, n_ref=pr.n_ref, k_ref=int(pr.rd.sum()), n_old=pr.n_old,
                               older_detections=int(pr.od.sum()), r_ref=";".join(f"{r:.4g}" for r in pr.r_ref))
                    row.update(readouts(pr))
                    rows.append(row)
                    print(design["id"], vkey(v), min_ref, rho, result, flush=True)
    return rows


def write(path: Path, rows: list[dict]) -> None:
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, keys, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    if sys.argv[1:] == ["screen"]:
        rows = run_screen()
        write(OUT / "m2_screen.csv", rows)
        for r in rows:
            if r["primary"]:
                print({k: r.get(k) for k in ("design", "rho", "status", "n_ref", "k_ref", "n_old", "lr_f1", "crit")})
    elif sys.argv[1:] == ["results"]:
        write(OUT / "m2_results.csv", run_results())
    else:
        raise SystemExit("usage: m2.py screen | results")


if __name__ == "__main__":
    main()
