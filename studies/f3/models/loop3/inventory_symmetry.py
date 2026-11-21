# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy", "pandas", "openpyxl", "scipy"]
# ///
"""Inventory-symmetry audit, Task 1A (studies/f3/docs/audits/2026-11-21-inventory-symmetry-spec.md).

Builds the candidate inventories S0, S1, S2a and S2b, with their sensitivity variants, from
horizons_reviewed.csv without changing it, and writes the cited disposition table of the wide-age
PBDB rows the duration filter of build_reviewed.py set aside (max - min > 20 Myr).

- S0: the reviewed primary inventory.
- S1: S0 plus restored wide-age PBDB rows lying wholly in the Early Devonian (393.47-419.62 Ma).
- S2a: PBDB-backed units only: eligible PBDB rows plus curated rows linked to a PBDB collection in
  material_links.csv, with their curated ages. S2b: S2a plus the restored rows.
Variants: `_with_28303` restores Kinzua Dam (pbdb:28303); `_merged` adds no restored row whose locality
key already belongs to an eligible row of S0; `_coord` (S2 only) gives linked curated rows the 0.1-degree
locality key of their PBDB collection, so the two linked Bathurst Island sections share one key.

    uv run studies/f3/models/loop3/inventory_symmetry.py
"""

from pathlib import Path

import pandas as pd

from analysis import select_records
from histories import YOUNG

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OUT = HERE / "out"
MACRO = ROOT / "studies/f3/data/macro"
PBDB = ROOT / "data/eprp/record"
LOCHKOVIAN_BASE = 419.62
COUNTING = ("locality_age", "region_stage")

EXCLUDE = {
    "pbdb:28216": ("miscoded_post_early_devonian",
                   "Price Fm, Cloyds Mountain VA (SUNY-B 390; PBDB ref 6895, unpublished 2002 accession list). Capel et al. "
                   "2025 Table S1 dates every Price Fm row Late Tournaisian (13 rows) and every Pocono row Late Tournaisian "
                   "or Late Famennian (11 rows). Macrostrat columns 37 and 38 near the site list surface Early Devonian "
                   "units, so the exclusion rests on the formation name."),
    "pbdb:28302": ("miscoded_post_early_devonian",
                   "Pocono Fm, Baker Run PA (SUNY-B 302; ref 6895), with Lepidodendropsis. Capel Table S1 dates Pocono rows "
                   "Late Tournaisian (10) and Late Famennian (1), including Lepidodendropsis scobiniformis. Macrostrat "
                   "column 305 lists surface Early Devonian units, so the exclusion rests on the formation name."),
    "pbdb:28303": ("miscoded_post_early_devonian_weak",
                   "Kinzua Dam, Allegheny Reservoir PA (SUNY-B 304; ref 6895); PBDB records 'Formation is uncertain'. The "
                   "nearest Macrostrat column (304, 0.25 degrees) holds Early Devonian units only in the subsurface. No "
                   "formation name; the weakest of the three, carried both ways (variant _with_28303)."),
    "pbdb:27917": ("duplicate_of_curated",
                   "Wutubulake Fm Bed 5 (Mu 1986), ?Zosterophyllum: the PBDB twin of tail:M-xinjiang-zosterophyllum (Cai et "
                   "al. 1993 Bed 5), which source_adjudications.csv L3S-037 excludes from primary. Its range also reaches "
                   "422.7 Ma, outside the Early Devonian."),
}


def linked_tail():
    links = pd.read_csv(MACRO / "material_links.csv")
    return {"tail:" + m for m in links.material_root}, links


def dispositions(h):
    """Every wide-age PBDB row with 393.47 <= min and max <= 422.7 Ma, any category (Task 1A scope)."""
    pc = pd.read_csv(PBDB / "pbdb_plant_collections.csv", low_memory=False).drop_duplicates("collection_no")
    ref = pd.read_csv(PBDB / "pbdb_plant_references.csv", low_memory=False).drop_duplicates("reference_no")
    pc = pc.merge(ref[["reference_no", "author1last", "pubyr", "reftitle"]], on="reference_no", how="left")
    pc = pc.set_index("collection_no")
    w = h[h.disposition.eq("wide_age_sensitivity") & h.source.eq("pbdb") & (h.min_ma >= YOUNG) & (h.max_ma <= 422.7)]
    primary_localities = set(h.loc[h.eligible_primary, "locality"])
    rows = []
    for r in w.itertuples():
        c = pc.loc[int(r.horizon_id.split(":")[1])]
        if r.horizon_id in EXCLUDE:
            decision, evidence = EXCLUDE[r.horizon_id]
        elif r.max_ma > LOCHKOVIAN_BASE:
            decision, evidence = "outside_early_devonian", "range reaches into the Silurian; not restored"
        else:
            decision, evidence = "restore", "Early Devonian coding with no contrary evidence found in the held sources"
        rows.append({"horizon_id": r.horizon_id, "b0": r.b0, "b1": r.b1, "b2": r.b2, "max_ma": r.max_ma, "min_ma": r.min_ma,
                     "region": r.region, "locality": r.locality,
                     "same_locality_as_primary": r.locality in primary_localities,
                     "collection_name": c.collection_name, "formation": c.formation if isinstance(c.formation, str) else "",
                     "pbdb_interval": f"{c.early_interval}" + (f" - {c.late_interval}" if isinstance(c.late_interval, str) else ""),
                     "reference": f"{c.author1last} {c.pubyr}: {str(c.reftitle)[:120]}", "reference_no": c.reference_no,
                     "names": r.names, "decision": decision, "evidence": evidence})
    return pd.DataFrame(rows).sort_values(["decision", "horizon_id"])


def build(h, disp, name):
    """Return a copy of h whose eligible_primary (and, for _coord, locality) defines inventory `name`."""
    base, _, variant = name.partition("_")
    restored = set(disp.loc[disp.decision.eq("restore"), "horizon_id"])
    if variant == "with_28303":
        restored |= {"pbdb:28303"}
    if variant == "merged":
        restored -= set(disp.loc[disp.same_locality_as_primary, "horizon_id"])
    linked, links = linked_tail()
    g = h.copy()
    if base == "S0":
        keep = g.eligible_primary
    elif base == "S1":
        keep = g.eligible_primary | g.horizon_id.isin(restored)
    elif base in ("S2a", "S2b"):
        keep = g.eligible_primary & (g.source.eq("pbdb") | g.horizon_id.isin(linked))
        if base == "S2b":
            keep = keep | g.horizon_id.isin(restored)
        if variant == "coord":
            for root, coll in links.groupby("material_root").collection_no:
                keys = set(h.loc[h.horizon_id.isin("pbdb:" + coll.astype(str)), "locality"])
                if len(keys) == 1:
                    g.loc[g.horizon_id.eq("tail:" + root), "locality"] = keys.pop()
    else:
        raise ValueError(name)
    g["eligible_primary"] = keep
    return g


SETS = ("S0", "S1", "S1_with_28303", "S1_merged", "S2a", "S2a_coord", "S2b", "S2b_with_28303", "S2b_merged", "S2b_coord")


def units(h, disp, name, category="B2", counting="locality_age", exclude_members=None):
    return select_records(build(h, disp, name), category, units=counting, exclude_members=exclude_members)


def main():
    h = pd.read_csv(MACRO / "horizons_reviewed.csv")
    disp = dispositions(h)
    disp.to_csv(OUT / "inventory_symmetry_dispositions.csv", index=False, lineterminator="\n")
    rows = []
    for name in SETS:
        for counting in COUNTING:
            u = units(h, disp, name, counting=counting)
            u.insert(0, "counting", counting)
            u.insert(0, "set", name)
            rows.append(u)
    allu = pd.concat(rows, ignore_index=True)
    allu.to_csv(OUT / "inventory_symmetry_units.csv", index=False, lineterminator="\n")
    s0 = allu[allu.set.eq("S0") & allu.counting.eq("locality_age")]
    ref = pd.read_csv(OUT / "primary_unit_membership.csv")
    ref = ref[ref.category.eq("B2") & ref.reading.eq("main")]
    assert sorted(s0.unit_id) == sorted(ref.unit_id), "S0 does not reproduce primary_unit_membership.csv"
    print(disp.decision.value_counts().to_string())
    print(allu.groupby(["set", "counting"]).size().to_string())


if __name__ == "__main__":
    main()
