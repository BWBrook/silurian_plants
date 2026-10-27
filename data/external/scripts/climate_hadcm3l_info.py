# /// script
# requires-python = ">=3.10"
# dependencies = ["openpyxl", "numpy", "scipy"]
# ///
"""Tabulate the PhanDA HadCM3L experiment metadata.

Reads ExperimentInfo.xlsx (Zenodo 8237751) and, from the PhanDA repository mirror, ExpNo.mat (a
MATLAB table that scipy cannot open directly; its subsystem stream is decoded here).

Writes, relative to data/external/climate/:
  hadcm3l_experiment_info.csv          suite x slice: age columns, PUMA run id, CO2
  hadcm3l_phanda_stage_slice_map.csv   PhanDA stage -> the two model slices its prior ensemble uses

Usage: uv run climate_hadcm3l_info.py EXPERIMENTINFO.xlsx EXPNO.mat OUTDIR
"""
import csv
import io
import sys

import numpy as np
import openpyxl
import scipy.io as sio
from scipy.io.matlab._mio5 import MatFile5Reader


def experiment_info(xlsx, out):
    ws = openpyxl.load_workbook(xlsx, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    suites = [(rows[0][i], i) for i in range(3, len(rows[0]), 2)]
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["suite", "experiment_no", "experiment_age_ma", "plate_age_ma", "puma_id", "co2_ppm"])
        for r in rows[2:]:
            for name, i in suites:
                w.writerow([name, r[0], r[1], r[2], r[i], r[i + 1]])


def decode_table(mat):
    m = sio.loadmat(mat)
    raw = m["__function_workspace__"].tobytes()
    hdr = open(mat, "rb").read(128)
    rd = MatFile5Reader(io.BytesIO(hdr + raw[8:]), struct_as_record=False, squeeze_me=False)
    rd.mat_stream.seek(128)
    rd.initialize_read()
    h, _ = rd.read_var_header()
    root = rd.read_var_array(h, process=False)[0, 0].MCOS[0]
    cells = root[2]
    data = cells.flat[2]
    varnames = [str(c[0]) for c in cells.flat[7].flat]
    stage = [str(c[0]) for c in data.flat[0].flat]
    cols = {varnames[0]: stage}
    for k, name in enumerate(varnames[1:], start=1):
        cols[name] = list(np.asarray(data.flat[k]).ravel())
    return cols


def phanda_map(mat, out):
    cols = decode_table(mat)
    n = len(cols["Stage"])
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["phanda_stage", "experiment_no_1", "experiment_no_2", "phanda_plate_age_ma"])
        for i in range(n):
            w.writerow([cols["Stage"][i], int(cols["ExpNo1"][i]), int(cols["ExpNo2"][i]), cols["PlateAge"][i]])


if __name__ == "__main__":
    xlsx, mat, outdir = sys.argv[1:4]
    experiment_info(xlsx, f"{outdir}/hadcm3l_experiment_info.csv")
    phanda_map(mat, f"{outdir}/../local/climate/hadcm3l_phanda_stage_slice_map.csv")  # no stated licence: untracked
