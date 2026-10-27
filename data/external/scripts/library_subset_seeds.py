"""Write the phase 2 fetch seed tiers `priority_spores` and `cards` from the project's works.tsv.

Usage (on deep-server, from _tools/): python3 library_subset_seeds.py [--works STORE/_build/works.tsv]
Reads the `subsets` column and writes _tools/seeds/priority_spores.tsv and cards.tsv (openalex_id, doi), one row
per canonical work, so `library_run.py fetch --tier priority_spores cards` fetches exactly these subsets.
"""

import argparse
import csv
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import library as L  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--works", type=Path, default=Path("/data/codex/silurian_plants/library/_build/works.tsv"))
a = ap.parse_args()
rows = L.read_tsv(a.works)
for subset in ("priority_spores", "cards"):
    out = [{"openalex_id": r["openalex_id"], "doi": r["doi"]} for r in rows if subset in r["subsets"].split(";")]
    L.write_tsv(HERE / "seeds" / f"{subset}.tsv", out, ["openalex_id", "doi"])
    print(f"{subset}: {len(out)} works -> seeds/{subset}.tsv")
