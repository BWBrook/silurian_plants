"""Reproduce review findings against commit 4e0d757; later repairs may reject the fixture."""

import math
import tempfile
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "models/f3"))
import pytest
import screen
import test_envelope as te
import validate as val

print("constant-profiled threshold", screen.smallest_excludable(7, 17, 3, 3))
rows = [("Sandbian", "Sandbian", 0, j, int(j < 7)) for j in range(17)]
rows += [("Darriwilian", "Darriwilian", 0, 100 + j, 0) for j in range(3)]
problem = te.problem(rows, h1_ceiling=3.0)
T = float(te.AGE.base[te.I("Darriwilian")])
print("full H1", problem.fstar("H1", T))
print("H1 at 2.5", problem.lr("H1", T, 2.5))
print("constant at 2.5", screen.profile_lr(7, 17, 3, 2.5))

scratch = tempfile.TemporaryDirectory(prefix="sp-f3-repair-review-")
base = Path(scratch.name)
with pytest.MonkeyPatch.context() as monkeypatch:
    first = te._stage1(base, monkeypatch)
    rows = [dict(row) for row in te._a4_replicates()]
    summary = val.summarise(val.CELLS[0], rows)
    j = next(i for i, row in enumerate(rows)
             if not row["no_tau"] and not row["trivial"] and row["abar_rel"] > 0)
    rows[j].update(state_H0c="zero-exposure", fstar_H0c=math.nan)
    print("changed row", {k: rows[j][k] for k in
          ("rep", "state_H0c", "fstar_H0c", "abar_rel", "lr_H0c", "trivial", "n_old")})
    evidence = te._write_stage1(base, rows, [summary])
    try:
        val.check_stage1(first | dict(evidence=evidence), "r", base)
        print("inconsistent zero exposure ACCEPTED", val.summarise(val.CELLS[0], rows)["fcover_H0c"])
    except SystemExit as exc:
        print("REFUSED", str(exc))

print("individual conditional coverage", 1 - 0.0225 / 0.5)
print("coverage after selecting the smallest of two independent passing values",
      (0.9775 ** 2 - 0.5 ** 2) / (1 - 0.5 ** 2))

scratch.cleanup()
