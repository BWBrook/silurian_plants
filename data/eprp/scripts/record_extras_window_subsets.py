"""record_extras_window_subsets.py (tranche 2): keep the whole-tree PBDB taxa and opinions untracked, track window subsets.

Run from data/eprp/scripts/ after record_extras_pbdb.py has delivered its files (stdlib only):
    python3 record_extras_window_subsets.py
Moves record/pbdb_plant_taxa.csv and record/pbdb_plant_opinions.csv to local/record/ (if still in record/), then writes
record/pbdb_plant_taxa_window.csv (taxa with d_range_overlaps_window = yes) and record/pbdb_plant_opinions_window.csv
(opinions whose orig_no is one of those taxa). Rows and columns are copied unchanged.
"""
import csv
import os
import shutil

csv.field_size_limit(1 << 30)
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
REC, LOC = os.path.join(ROOT, "record"), os.path.join(ROOT, "local", "record")


def full(name):
    src, dst = os.path.join(REC, name), os.path.join(LOC, name)
    if os.path.exists(src):
        os.makedirs(LOC, exist_ok=True)
        shutil.move(src, dst)
    return dst


def subset(src, dst, keep):
    with open(src, newline="", encoding="utf-8") as f, open(dst, "w", newline="", encoding="utf-8") as g:
        rd, wr = csv.reader(f), csv.writer(g, lineterminator="\n")
        head = next(rd)
        wr.writerow(head)
        n = 0
        for row in rd:
            if keep(head, row):
                wr.writerow(row)
                n += 1
    print(f"{n:>6} rows -> {os.path.relpath(dst, ROOT)}")


taxa, opinions = full("pbdb_plant_taxa.csv"), full("pbdb_plant_opinions.csv")
with open(taxa, newline="", encoding="utf-8") as f:
    rd = csv.reader(f)
    head = next(rd)
    i, j = head.index("d_range_overlaps_window"), head.index("orig_no")
    window = {row[j] for row in rd if row[i] == "yes"}

subset(taxa, os.path.join(REC, "pbdb_plant_taxa_window.csv"),
       lambda h, r: r[h.index("d_range_overlaps_window")] == "yes")
subset(opinions, os.path.join(REC, "pbdb_plant_opinions_window.csv"),
       lambda h, r: r[h.index("orig_no")] in window)
