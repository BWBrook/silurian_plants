# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "scipy"]
# ///

"""The real-design adapter for M2 (designs/m2.toml): source tables to the engine's binary Units.

Each generated unit keeps its source key, the named reading, the variant and the rule version, so every
binary outcome traces to a literal source report (data/units/). Source tables are never edited here.

    uv run models/f3/designs.py      # writes out/m2_units.csv: every generated row of every variant
    F3_DESIGNS=models/f3/designs/<other>.toml uv run models/f3/designs.py   # another declaration file

Rules (RULES; designs/m2.toml states them in prose):
  libya-chart-v1  Abuhmida (2013): appendix entry with an exact chart row; >= 1 marine-group symbol;
                  barren scopes and the possibly caved I3 Ash Shabiyat rows excluded; target mark = 1,
                  blank target cell = 0; age from the formation and assemblage zone; cluster = well.
  qusaiba-table2-v1  Wellman et al. (2015) Table 2: trilete taxon mark = 1, none = 0.
  borenshult-outcomes-v1  outcomes.csv under the reading: explicit_non_detection and not_reported = 0,
                  detected = 1, unresolved excluded or 0.
"""

import csv
import itertools
import math
import os
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

import envelope as ev
import sim

ROOT = Path(__file__).resolve().parents[2]
UNITS = ROOT / "data" / "units"
DESIGNS = Path(os.environ.get("F3_DESIGNS", Path(__file__).resolve().parent / "designs" / "m2.toml"))
OUT = Path(__file__).resolve().parent / "out"
RULES = {"libya": "libya-chart-v1", "qusaiba": "qusaiba-table2-v1", "borenshult": "borenshult-outcomes-v1"}
TS = sim.Timescale.load()
PRE459 = (459.1, float(TS.base[TS.index("Darriwilian")]))


def stage(name: str) -> int:
    return TS.index(name)


def declarations(path: Path = DESIGNS) -> dict:
    with open(path, "rb") as f:
        return tomllib.load(f)


@dataclass
class Row:
    """One generated binary unit with its provenance."""

    unit_id: str
    source: str
    cluster_name: str
    cls_name: str
    young: int
    old: int
    d: int
    rule: str
    evidence: str
    lo_ma: float = math.nan
    hi_ma: float = math.nan
    rate_class: str = ""
    depth: float = math.nan
    formation: str = ""
    transported: bool = False


@dataclass
class Built:
    design: str
    variant: dict
    rows: list[Row]
    excluded: list[tuple[str, str]] = field(default_factory=list)

    def units(self, rho: float = 1.0) -> tuple[ev.Units, list[str]]:
        """Units with rate classes and clusters by sorted name. rho multiplies the rate of every unit the
        design declares transported (Libya: the Ordovician formations; QB: Borenshult)."""
        classes = sorted({r.rate_class or r.cls_name for r in self.rows})
        clusters = sorted({r.cluster_name for r in self.rows})
        a = lambda f: np.array([f(r) for r in self.rows])
        young, old = a(lambda r: r.young), a(lambda r: r.old)
        mult = np.where(a(lambda r: r.transported), rho, 1.0)
        u = ev.Units(young, old, a(lambda r: classes.index(r.rate_class or r.cls_name)),
                     a(lambda r: clusters.index(r.cluster_name)), a(lambda r: r.d), mult,
                     a(lambda r: r.lo_ma), a(lambda r: r.hi_ma))
        return u, classes


# --- Libya -------------------------------------------------------------------------------------------

def _read(name: str) -> list[dict]:
    with open(UNITS / name, newline="") as f:
        return list(csv.DictReader(f))


def _key(r: dict) -> tuple[str, float]:
    return r["well"], float(r["depth_ft"])


def libya_age(formation: str, zone: str) -> tuple[str, str]:
    """(youngest stage, oldest stage) from the formation and the assemblage-zone context."""
    f = formation.lower()
    if "hawaz" in f:
        return "Darriwilian", "Darriwilian"
    if "bir tlacsin" in f:
        return "Hirnantian", "Hirnantian"
    if "shugran" in f or "memouniat" in f:
        return "Hirnantian", "Katian"
    if "tanezzuft" in f or "taezzuft" in f or "hot shale" in f:
        if "Cr4" in zone:
            return "Telychian", "Rhuddanian"
        if "Cr3" in zone:
            return "Rhuddanian", "Rhuddanian"
        return "Telychian", "Rhuddanian"
    raise ValueError(f"no declared age for formation {formation!r}")


def libya(wells: list[str], classes: list[str], material_type: str, allocation: str,
          a28i: str = "column-absent-zero", e1_7287: str = "prose-detected", core_as: str = "") -> Built:
    app = {_key(r): r for r in _read("libya_appendix1.csv")}
    chart = {_key(r): r for r in _read("libya_chart_reports.csv")}
    prose = {_key(r): r for r in _read("libya_prose_support.csv")}
    rows, excluded = [], []
    for k in sorted(app):
        well, depth = k
        if well not in wells:
            continue
        a, p, c = app[k], prose[k], chart.get(k)
        uid = f"{well}:{depth:g}"
        if c is None:
            excluded.append((uid, "appendix entry without an exact chart row"))
            continue
        kind = a["type"] if a["type"] in ("Core", "Cutting") else {"CU": "Cutting", "CO": "Core"}[c["type_code"]] \
            if material_type == "chart-code" else ""
        if not kind:
            excluded.append((uid, "unspecified appendix material type"))
            continue
        if kind not in classes:
            continue
        if p["productivity_prose_status"].startswith("explicit-barren") or int(c["marine_symbols"]) == 0:
            excluded.append((uid, "no non-target recovery or explicit barren scope"))
            continue
        if "ash sh" in a["formation"].lower():
            excluded.append((uid, "Ash Shabiyat recovery possibly caved (printed p. 367)"))
            continue
        report = c["ambitisporites_dilutus_report"]
        if report == "column-absent":
            if a28i != "column-absent-zero":
                excluded.append((uid, "no A. dilutus column in this well's chart"))
                continue
            d, ev_ = 0, "chart has no A. dilutus column (taxon not recorded in the well)"
        elif depth == 7287 and well == "E1-NC174":
            if e1_7287 == "unresolved":
                excluded.append((uid, "7287 ft: prose specimen against a blank chart cell, unresolved"))
                continue
            d, ev_ = 1, "prose specimen, printed pp. 381-382 (chart cell blank)"
        else:
            d, ev_ = (1, "chart target mark") if report == "mark-present" else (0, "blank target cell")
        young, old = libya_age(a["formation"], p["e1_assemblage_context"])
        lo = hi = math.nan
        if young == "Darriwilian" and allocation == "pre459":
            lo, hi = PRE459
        rows.append(Row(uid, "abuhmida2013", well, kind, stage(young), stage(old), d, RULES["libya"],
                        f"{ev_}; {c['source_locator']}; appendix {a['source_locator']}", lo, hi,
                        core_as if (core_as and kind == "Core") else "", depth, a["formation"],
                        stage(young) > stage("Rhuddanian")))
    return Built("", {}, rows, excluded)


# --- Qusaiba and Borenshult --------------------------------------------------------------------------

def qusaiba() -> list[Row]:
    out = []
    for r in _read("qusaiba_inventory.csv"):
        if r["wellman_table2_member"] != "yes":
            continue
        quwarah = "Quwarah" in r["wellman_stratigraphic_label"]
        young, old = ("Katian", "Katian") if r["record_id"] == "QSBA-depth-551p0" else \
            (("Hirnantian", "Katian") if quwarah else ("Hirnantian", "Hirnantian"))
        d = int(r["e1_table2_status"] == "taxon-mark-present")
        out.append(Row(r["record_id"], "wellman2015", "Qusaiba-1", "Core", stage(young), stage(old), d,
                       RULES["qusaiba"], f"{r['e1_table2_status']} {r['e1_table2_taxa']}; {r['source_locators'][:60]}",
                       depth=float(r["depth_value_ft_interpretation"]), formation=r["wellman_stratigraphic_label"]))
    return out


def borenshult(reading: str, unresolved: str) -> tuple[list[Row], list[tuple[str, str]]]:
    ages = {f"BOR-{r['depth_m']}": r for r in _read("borenshult_ages.csv")}
    out, excluded = [], []
    for r in _read("outcomes.csv"):
        if not r["unit_id"].startswith("BOR-") or r["event_id"] != "E1" or r["reading_id"] != reading:
            continue
        o = r["outcome"]
        if o == "unresolved" and unresolved == "excluded":
            excluded.append((r["unit_id"], "unresolved E1 identification"))
            continue
        d = 1 if o == "detected" else 0
        s = ages[r["unit_id"]]["reported_stage"]
        out.append(Row(r["unit_id"], "rubinstein2019;rubinstein2023", "Borenshult-1", "Core", stage(s), stage(s), d,
                       RULES["borenshult"], f"{o} under {reading}", depth=float(ages[r['unit_id']]["depth_m"]),
                       transported=True))
    return out, excluded


# --- designs and variants ----------------------------------------------------------------------------

def variants(design: dict, decl: dict) -> list[dict]:
    """Every declared variant of one design (rho and the reference minimum excluded: they act at analysis)."""
    if design["id"].startswith("LY-"):
        axes = {"material_type": decl["libya"]["material_type"], "allocation": decl["libya"]["allocation"],
                "cluster_k": design["cluster_k"]}
        if "A28i-NC186" in design["wells"]:
            axes["a28i"] = decl["libya"]["a28i"]
        if "E1-NC174" in design["wells"] and "Core" in design["classes"]:
            axes["e1_7287"] = decl["libya"]["e1_7287"]
    elif design["id"] == "QB-CO":
        axes = {"reading": design["reading"], "bor_unresolved": design["bor_unresolved"], "cluster_k": design["cluster_k"]}
    else:
        return []
    return [dict(zip(axes, v)) for v in itertools.product(*axes.values())]


def build(design: dict, variant: dict) -> Built:
    if design["id"].startswith("LY-"):
        b = libya(design["wells"], design["classes"], variant["material_type"], variant["allocation"],
                  variant.get("a28i", "column-absent-zero"), variant.get("e1_7287", "prose-detected"),
                  design.get("core_as", ""))
    elif design["id"] == "QB-CO":
        bor, excluded = borenshult(variant["reading"], variant["bor_unresolved"])
        b = Built("", {}, qusaiba() + bor, excluded)
    else:
        raise ValueError(design["id"])
    b.design, b.variant = design["id"], variant
    return b


def spec(decl: dict, cluster_k: float, min_ref: int) -> ev.Spec:
    c = decl["common"]
    return ev.Spec(reference_stages=c["reference_stages"], min_units_per_class=min_ref, domain_ma=(0.0, c["domain_ma"]),
                   classes=tuple(c["classes"]), h1_ceiling=c["h1_ceiling"], h0m_lag_ma=c["h0m_lag_ma"],
                   alpha=c["alpha"], readouts=tuple(c["readouts"]), cluster_shape_k=cluster_k,
                   nodes=c["nodes"], fa_rule=ev.FA_RULES[c["fa_rule"]])


def main() -> None:
    decl = declarations()
    OUT.mkdir(exist_ok=True)
    out = []
    for design in decl["design"]:
        for v in variants(design, decl):
            b = build(design, v)
            vkey = ";".join(f"{k}={v[k]}" for k in sorted(v) if k != "cluster_k")
            for r in b.rows:
                out.append(dict(design=b.design, variant=vkey, unit_id=r.unit_id, source=r.source, cluster=r.cluster_name,
                                cls=r.cls_name, rate_class=r.rate_class or r.cls_name, formation=r.formation, depth=r.depth,
                                youngest_stage=TS.names[r.young], oldest_stage=TS.names[r.old],
                                lo_ma="" if math.isnan(r.lo_ma) else r.lo_ma, hi_ma="" if math.isnan(r.hi_ma) else r.hi_ma,
                                d=r.d, transported=r.transported, rule=r.rule, evidence=r.evidence, excluded=""))
            for uid, why in b.excluded:
                out.append(dict(design=b.design, variant=vkey, unit_id=uid, excluded=why))
    seen, rows = set(), []
    for r in out:
        k = (r["design"], r["variant"], r["unit_id"])
        if k not in seen:
            seen.add(k)
            rows.append(r)
    with open(OUT / f"{decl['common']['maximum'].lower()}_units.csv", "w", newline="") as f:
        w = csv.DictWriter(f, list(out[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in out[0]})
    print(f"{len(rows)} rows")


if __name__ == "__main__":
    main()
