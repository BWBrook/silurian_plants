import json
import math
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "models/f3"))
import pytest
import screen
import test_envelope as te
import validate as val

print("Borenshult counts:", json.dumps(screen.borenshult(), indent=2))
for n in (17, 31):
    for f in (1, 3):
        print("homogeneous", dict(k=7, n=n, m=3, f=f,
              known=6 * f * screen.rate(7, n),
              profiled=screen.profile_lr(7, n, 3, f)))

T = float(te.AGE.base[te.I("Darriwilian")])
scenarios = [
    ("homogeneous-explicit", math.inf,
     [("Sandbian", "Sandbian", 0, j, int(j < 7)) for j in range(17)]),
    ("heterogeneous", math.inf,
     [("Sandbian", "Sandbian", 0, j, int(j < 7)) for j in range(8)]
     + [("Sandbian", "Sandbian", 1, 20 + j, 0) for j in range(9)]),
    ("zeros-clustered", 2.0,
     [("Sandbian", "Sandbian", 0, j if j < 7 else 20, int(j < 7)) for j in range(17)]),
]
for name, shape, rows in scenarios:
    rows += [("Darriwilian", "Darriwilian", 0, 100 + j, 0) for j in range(3)]
    problem = te.problem(rows, k=shape, nodes=128, h1_ceiling=3.0)
    print(name, "r_ref", problem.r_ref, "LR1", problem.lr("H0", T, 1.0),
          "LR3", problem.lr("H1", T, 3.0),
          "H0", problem.fstar("H0", T), "H1", problem.fstar("H1", T))

for args in [(0, 0, 3), (7, 17, 3), (0, 17, 3), (7, 17, 0)]:
    print("smallest_excludable", args, screen.smallest_excludable(*args))

scratch = tempfile.TemporaryDirectory(prefix="sp-screen-review-")
base = Path(scratch.name)
with pytest.MonkeyPatch.context() as monkeypatch:
    first = te._stage1(base, monkeypatch)
    rows = [dict(row) for row in te._a4_replicates()]
    cell = val.CELLS[0]
    summary = val.summarise(cell, rows)
    target = next(i for i, row in enumerate(rows)
                  if not row["no_tau"] and not row["trivial"] and row["abar_rel"] > 0)
    rows[target]["fstar_H0c"] = 0.0
    for state in ("finite", "bogus"):
        rows[target]["state_H0c"] = state
        evidence = te._write_stage1(base, rows, [summary])
        try:
            val.check_stage1(first | dict(evidence=evidence), "r", base)
            print("state", state, "ACCEPTED", "fcover_H0c", val.summarise(cell, rows)["fcover_H0c"])
        except SystemExit as exc:
            print("state", state, "REFUSED", str(exc))

scratch.cleanup()
