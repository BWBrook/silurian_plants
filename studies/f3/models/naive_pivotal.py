# /// script
# requires-python = ">=3.12"
# dependencies = []
# ///
"""First, estimator-free pass at the pivotal records (studies/f3/docs/plan-f3.md, Loop 1 step 4).

For each event, the first appearance under the main reading of studies/f3/data/occurrences, as two ages:
`certain`, the youngest age at which some counting record is certainly present (the top of its
youngest stage), and `possible`, the oldest age any counting record could have (the base of its
oldest stage). Then every observation with alternative readings is switched, one at a time, and
the switches that move either age are listed. Observations linked by `same_material_as` move
together when the alias has a single reading (it mirrors its canonical observation).

    uv run studies/f3/models/naive_pivotal.py   # writes studies/f3/models/out/naive_pivotal.csv
"""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OCC = ROOT / "studies" / "f3" / "data" / "occurrences"
EVENTS = ["E1", "E2", "E3", "E4", "E5"]


def load():
    st = sorted(csv.DictReader(open(ROOT / "data" / "timescale.csv")), key=lambda r: -float(r["base_ma"]))
    base = {r["stage"]: float(r["base_ma"]) for r in st}
    top = {r["stage"]: (float(st[k + 1]["base_ma"]) if k + 1 < len(st) else 0.0) for k, r in enumerate(st)}
    obs = {o["obs_id"]: o for o in csv.DictReader(open(OCC / "observations.csv"))}
    ints = {}
    for i in csv.DictReader(open(OCC / "interpretations.csv")):
        ints.setdefault(i["obs_id"], []).append(i)
    return base, top, obs, ints


def canonical(oid, obs, ints):
    seen = set()
    while obs[oid]["same_material_as"] and len(ints[oid]) == 1 and oid not in seen:
        seen.add(oid)
        oid = obs[oid]["same_material_as"]
    return oid


def first_appearance(event, choice, base, top, obs, ints):
    certain = possible = None
    who_c = who_p = ""
    for oid in obs:
        i = choice[canonical(oid, obs, ints)] if canonical(oid, obs, ints) != oid else choice[oid]
        if event not in i["counts_for"].split(";"):
            continue
        c, p = top[i["stage_youngest"]], base[i["stage_oldest"]]
        if certain is None or c > certain:
            certain, who_c = c, oid
        if possible is None or p > possible:
            possible, who_p = p, oid
    return certain, possible, who_c, who_p


def main():
    base, top, obs, ints = load()
    main_choice = {oid: next(i for i in v if i["main"] == "true") for oid, v in ints.items()}
    rows = []
    for ev in EVENTS:
        c0, p0, wc, wp = first_appearance(ev, main_choice, base, top, obs, ints)
        rows.append({"event": ev, "switch": "(main reading)", "obs_id": "", "label": "", "certain_ma": c0, "possible_ma": p0,
                     "d_certain": 0, "d_possible": 0, "set_by_certain": wc, "set_by_possible": wp})
        for oid, alts in ints.items():
            for alt in alts:
                if alt["main"] == "true":
                    continue
                choice = dict(main_choice)
                choice[oid] = alt
                c, p, wc2, wp2 = first_appearance(ev, choice, base, top, obs, ints)
                if (c, p) != (c0, p0):
                    rows.append({"event": ev, "switch": alt["interp_id"], "obs_id": oid, "label": alt["label"],
                                 "certain_ma": c, "possible_ma": p, "d_certain": round((c or 0) - (c0 or 0), 2),
                                 "d_possible": round((p or 0) - (p0 or 0), 2), "set_by_certain": wc2, "set_by_possible": wp2})
    out = ROOT / "studies" / "f3" / "models" / "out" / "naive_pivotal.csv"
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        print(f"{r['event']} {r['switch'][:40]:40s} certain {r['certain_ma']} ({r['d_certain']:+}) possible {r['possible_ma']} ({r['d_possible']:+})  {r['label'][:60]}")


if __name__ == "__main__":
    main()
