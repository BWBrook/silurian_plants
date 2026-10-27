# /// script
# requires-python = ">=3.10"
# dependencies = ["numpy", "netCDF4"]
# ///
"""Build hadcm3l_slices.csv, hadcm3l_land_summary.csv and hadcm3l_qc.csv for one PhanDA HadCM3L suite.

Inputs (paths relative to data/external/ unless absolute):
  local/climate/hadcm3l/<experiment>/       extracted slice files (tas and pr, M1-M5) and SHA256SUMS
  local/climate/hadcm3l/bristol_pdclann/    BRIDGE annual-mean climatology files, one per run code
  climate/hadcm3l_experiment_info.csv       from climate_hadcm3l_info.py
  ../timescale.csv                          project stage bases (ICS v2024/12)

Land mask: grid cells where the BRIDGE soil-moisture field (sm_mm_soil) is defined. Its footprint is the
complement of the sea-evaporation field (evapsea_mm_srf); cells where the two do not complement are
counted in the QC table and treated as sea.
Area weights: sin(lat_north) - sin(lat_south) per cell, polar cells half-height, sphere of radius 6371 km.
Land ice (derived heuristic): land cells whose BRIDGE annual-mean lying-snow mass (snowdepth_mm_srf) exceeds
5000 kg m-2. Across the 21 slices that field is bimodal: seasonal snow is below 500 kg m-2 in 98% of land cells
and ice-sheet cells hold at least 10 000 (768 hold exactly 50 000), with 0.2% of cells between 500 and 10 000.
Annual mean: mean of the 12 monthly values (equal-length months in the 360-day model calendar), then the
mean of the five 20-yr blocks M1-M5 (the last 100 model years).
Precipitation: the supplied `pr` variable (mm per year equivalent, = precip_mm_srf in kg m-2 s-1 x 31 536 000).

Usage: uv run climate_hadcm3l_tables.py [EXPERIMENT]   (run from anywhere; paths are resolved from this file)
"""
import csv
import re
import sys
from pathlib import Path

import netCDF4 as nc
import numpy as np

EXT = Path(__file__).resolve().parent.parent          # data/external
EXPERIMENT = sys.argv[1] if len(sys.argv) > 1 else "scotese_02"
FIRST, LAST = 12, 32
R_KM = 6371.0
ICE_SNOW_KG_M2 = 5000.0
SLICE_DIR = EXT / "local/climate/hadcm3l" / EXPERIMENT
MASK_DIR = EXT / "local/climate/hadcm3l/bristol_pdclann"
OUT = EXT / "climate"
RE_FILE = re.compile(rf"{EXPERIMENT}_(\d{{3}})_(\d+)Ma_(\d+)pCO2_M(\d)_(tas|pr)\.nc$")

NOMINAL_BASIS = "PALEOMAP map age (ExperimentInfo Plate Age)"
EXPERIMENT_BASIS = "source stage-mid-point label, timescale not stated (GTS2012-era by arithmetic; inferred)"
AVERAGING = "final 100 model years as five 20-yr blocks M1-M5"
TEMPORAL = "12 monthly means (climatology of a 20-yr block; 360-day calendar)"
GRID = "HadCM3L 96 lon x 73 lat regular, 3.75 x 2.5 deg, lat 90 to -90"


def read_info():
    with open(EXT / "climate/hadcm3l_experiment_info.csv") as fh:
        return {int(r["experiment_no"]): r for r in csv.DictReader(fh) if r["suite"] == EXPERIMENT}


def read_timescale():
    with open(EXT.parent / "timescale.csv") as fh:
        rows = sorted(csv.DictReader(fh), key=lambda r: float(r["base_ma"]))
    return [(float(r["base_ma"]), r["stage"]) for r in rows]


def stage_of(age, scale):
    for base, stage in scale:
        if base >= age:
            return stage
    return ""


def lat_weights(lat):
    edges = np.empty(len(lat) + 1)
    edges[1:-1] = (lat[:-1] + lat[1:]) / 2
    edges[0], edges[-1] = 90.0, -90.0
    return np.sin(np.radians(edges[:-1])) - np.sin(np.radians(edges[1:]))


def load(path, var):
    with nc.Dataset(path) as d:
        a = np.ma.filled(d[var][:].astype(float), np.nan)
    return a[:, 0]


def sha_table():
    out = {}
    for line in open(SLICE_DIR / "SHA256SUMS"):
        h, name = line.split()
        out[name] = h
    return out


def wmean(field, w2, mask):
    return float(np.nansum(field * w2 * mask) / np.sum(w2 * mask))


def main():
    info = read_info()
    scale = read_timescale()
    shas = sha_table()
    files = {}
    for p in sorted(SLICE_DIR.glob("*.nc")):
        m = RE_FILE.match(p.name)
        files.setdefault(int(m.group(1)), []).append((int(m.group(4)), m.group(5), p, m.group(2), m.group(3)))
    assert sorted(files) == list(range(FIRST, LAST + 1)), "slice set differs from the window"
    for n, lst in files.items():
        assert len(lst) == 10, (n, len(lst))

    slices, summary, qc = [], [], []
    for n in range(FIRST, LAST + 1):
        row = info[n]
        age_plate, age_exp = float(row["plate_age_ma"]), float(row["experiment_age_ma"])
        st_plate, st_exp = stage_of(age_plate, scale), stage_of(age_exp, scale)
        label = f"{EXPERIMENT}_{n:03d}"
        for mean_id, var, path, _, _ in sorted(files[n]):
            if var == "tas":
                units, in_file = "K", "tas; temp_mm_1_5m (same data, other orientation)"
            else:
                units, in_file = "mm yr-1 (annual-rate equivalent of precip_mm_srf, kg m-2 s-1)", "pr; precip_mm_srf; pr_anomaly; prln_anomaly"
            slices.append({
                "experiment": EXPERIMENT, "slice_label": label, "experiment_no": n, "mean_id": f"M{mean_id}",
                "nominal_age_ma": age_plate, "nominal_age_basis": NOMINAL_BASIS,
                "experiment_age_ma": age_exp, "experiment_age_basis": EXPERIMENT_BASIS,
                "project_stage_by_plate_age": st_plate, "project_stage_by_experiment_age": st_exp,
                "co2_ppm": row["co2_ppm"], "puma_id": row["puma_id"],
                "file": str(path.relative_to(EXT)), "variable": var, "variables_in_file": in_file, "units": units, "grid": GRID,
                "temporal_resolution": TEMPORAL, "averaging_period": AVERAGING,
                "bytes": path.stat().st_size, "sha256": shas[path.name],
            })

        t = {mid: path for mid, var, path, _, _ in files[n] if var == "tas"}
        p = {mid: path for mid, var, path, _, _ in files[n] if var == "pr"}
        tas_o = np.stack([load(t[k], "temp_mm_1_5m") for k in range(1, 6)])        # (5,12,73,96) K
        pr_o = np.stack([load(p[k], "pr") for k in range(1, 6)])                    # (5,12,96,73) mm/yr
        tas_l = np.stack([load(t[k], "tas") for k in range(1, 6)])
        pr_raw = np.stack([load(p[k], "precip_mm_srf") for k in range(1, 6)])       # (5,12,73,96) kg m-2 s-1
        tas_chk = float(np.nanmax(np.abs(np.roll(np.transpose(tas_l, (0, 1, 3, 2)), -48, axis=3) - tas_o)))
        pr_o = np.roll(np.transpose(pr_o, (0, 1, 3, 2)), -48, axis=3)               # to (5,12,73,96), lon 0..356
        pr_chk = float(np.nanmax(np.abs(pr_o - pr_raw * 31536000.0)))

        code = row["puma_id"]
        with nc.Dataset(MASK_DIR / f"{code}a.pdclann.nc") as d:
            sm = np.ma.filled(d["sm_mm_soil"][:].astype(float), np.nan)[0, 0]
            ev = np.ma.filled(d["evapsea_mm_srf"][:].astype(float), np.nan)[0, 0]
            t_b = np.ma.filled(d["temp_mm_1_5m"][:].astype(float), np.nan)[0, 0]
            p_b = np.ma.filled(d["precip_mm_srf"][:].astype(float), np.nan)[0, 0] * 31536000.0
            snow = np.ma.filled(d["snowdepth_mm_srf"][:].astype(float), np.nan)[0, 0]
            lat = d["latitude"][:].astype(float)
            lon = d["longitude"][:].astype(float)
        land = (~np.isnan(sm)).astype(float)
        ice = ((snow > ICE_SNOW_KG_M2) & (land > 0)).astype(float)
        free = land * (1 - ice)
        non_complement = int(np.sum(np.isnan(sm) == np.isnan(ev)))
        assert lat.shape == (73,) and lon.shape == (96,) and lat[0] == 90 and lon[0] == 0

        w = lat_weights(lat)
        w2 = np.repeat(w[:, None], 96, axis=1)
        cell_km2 = R_KM ** 2 * np.radians(3.75) * w2
        land_area = float(np.sum(cell_km2 * land))

        ann_t = tas_o.mean(axis=1) - 273.15                       # (5,73,96) per M
        ann_p = pr_o.mean(axis=1)
        lt = [wmean(ann_t[k], w2, land) for k in range(5)]
        lp = [wmean(ann_p[k], w2, land) for k in range(5)]
        ft = float(np.mean([wmean(ann_t[k], w2, free) for k in range(5)]))
        fp = float(np.mean([wmean(ann_p[k], w2, free) for k in range(5)]))
        gm = float(np.mean([wmean(ann_t[k], w2, np.ones_like(land)) for k in range(5)]))
        summary.append({
            "experiment": EXPERIMENT, "slice_label": label, "experiment_no": n,
            "nominal_age_ma": age_plate, "experiment_age_ma": age_exp, "co2_ppm": row["co2_ppm"],
            "project_stage_by_plate_age": st_plate, "project_stage_by_experiment_age": st_exp,
            "grid_cells": land.size, "land_cells": int(land.sum()),
            "derived_land_cell_fraction": round(land.sum() / land.size, 4),
            "derived_land_area_1e6_km2": round(land_area / 1e6, 2),
            "derived_land_area_fraction": round(land_area / (4 * np.pi * R_KM ** 2), 4),
            "derived_land_tas_c": round(float(np.mean(lt)), 2),
            "derived_land_tas_c_min_over_M": round(min(lt), 2), "derived_land_tas_c_max_over_M": round(max(lt), 2),
            "derived_land_pr_mm_yr": round(float(np.mean(lp)), 1),
            "derived_land_pr_mm_yr_min_over_M": round(min(lp), 1), "derived_land_pr_mm_yr_max_over_M": round(max(lp), 1),
            "derived_gmst_c": round(gm, 2),
            "derived_land_ice_cells": int(ice.sum()),
            "derived_land_ice_area_1e6_km2": round(float(np.sum(cell_km2 * ice)) / 1e6, 2),
            "derived_icefree_land_tas_c": round(ft, 2),
            "derived_icefree_land_pr_mm_yr": round(fp, 1),
        })
        qc.append({
            "slice_label": label, "puma_id": code,
            "tas_equals_temp_mm_1_5m_rolled_max_abs_k": tas_chk,
            "pr_equals_precip_x_31536000_max_abs": pr_chk,
            "cells_with_neither_or_both_of_sm_and_evapsea": non_complement,
            "m1_m5_mean_vs_bridge_100yr_tas_max_abs_k": round(float(np.nanmax(np.abs(tas_o.mean(axis=(0, 1)) - t_b))), 5),
            "m1_m5_mean_vs_bridge_100yr_pr_max_abs_mm_yr": round(float(np.nanmax(np.abs(pr_o.mean(axis=(0, 1)) - p_b))), 4),
            "m1_vs_m5_land_tas_diff_k": round(lt[0] - lt[4], 3),
        })

    def dump(name, rows):
        with open(OUT / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rows)

    dump("hadcm3l_slices.csv", slices)
    dump("hadcm3l_land_summary.csv", summary)
    dump("hadcm3l_qc.csv", qc)
    print(len(slices), "slice rows;", len(summary), "slices")


if __name__ == "__main__":
    main()
