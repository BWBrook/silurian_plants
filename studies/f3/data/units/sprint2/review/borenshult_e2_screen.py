"""Claude review of sprint 2: Borenshult-1 as a within-section E2 (M1) design. Screen only (m2.screen at f = 1),
one cluster, reported stages, rho = 1, the M2 common settings, unresolved E2 excluded or coded 0. A reviewer
diagnostic, not frozen before screening and not a qualified result. Output: borenshult_e2_screen.txt."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[6] / "studies/f3/models"))
import designs as dz, m2, envelope as ev
decl = dz.declarations()
ages = {f"BOR-{r['depth_m']}": r for r in dz._read("borenshult_ages.csv")}
for reading in ("main", "inclusive", "outlier"):
    for unres in ("excluded", "zero"):
        rows = []
        for r in dz._read("outcomes.csv"):
            if not r["unit_id"].startswith("BOR-") or r["event_id"] != "E2" or r["reading_id"] != reading:
                continue
            o = r["outcome"]
            if o == "unresolved" and unres == "excluded":
                continue
            s = ages[r["unit_id"]]["reported_stage"]
            rows.append(dz.Row(r["unit_id"], "bor", "Borenshult-1", "Core", dz.stage(s), dz.stage(s),
                               int(o == "detected"), "x", o))
        b = dz.Built("BOR-E2", {}, rows)
        for min_ref in (5, 10):
            u, _ = b.units(1.0)
            try:
                pr = ev.Problem(u, dz.spec(decl, 2.0, min_ref), ev.AgeModel.load())
            except ev.NoFirstAppearance as e:
                print(reading, unres, min_ref, "S0 fails:", e); continue
            ok, lr, crit = m2.screen(pr)
            print(reading, unres, min_ref, f"tau={pr.tau} n_ref={pr.n_ref} k_ref={int(pr.rd.sum())} n_old={pr.n_old} "
                  f"older_det={int(pr.od.sum())} LR(f=1)={lr:.3f} crit={crit:.3f} passes={ok}")
