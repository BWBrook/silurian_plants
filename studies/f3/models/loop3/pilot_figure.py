# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "pandas"]
# ///
"""Draft figure for the Loop 3 pilot: dated body-fossil horizons, older limits under each recovery
assumption, the crown-tracheophyte clock intervals and M3. Main reading. Pilot, not for the paper."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent / "out"
h = pd.read_csv(ROOT / "studies/f3/data/macro/horizons_v0.csv")
iv = pd.read_csv(OUT / "pilot_intervals.csv")
iv = iv[iv.reading == "main"]

CATS = [("B0", "Any embryophyte body"), ("B1", "Polysporangiophyte body"), ("B2", "Crown-tracheophyte member")]
EST = [("classical_to_Emsian", "uniform recovery", "#555555", "o"), ("constant", "effort-weighted, constant", "#1b6ca8", "s"),
       ("logistic", "effort-weighted, logistic ramp", "#c0392b", "D")]
CLOCKS = [("Hooper et al. 2026", 432, 428), ("Harris et al. 2022", 452, 447), ("Morris et al. 2018", 450.8, 419.3)]

fig, ax = plt.subplots(figsize=(9, 6.2))
y0 = 0
ticks = []
for cat, label in CATS:
    r = h[h[cat.lower()] & h.reading.isin(["all", "main"])].drop_duplicates("horizon_id")
    r = r[r.max_ma > 413].sort_values("max_ma")
    for i, (_, row) in enumerate(r.iterrows()):
        yy = y0 + i * 0.12
        ax.plot([row.min_ma, row.max_ma], [yy, yy], color="#8a8a8a", lw=0.9, alpha=0.7)
    top = y0 + len(r) * 0.12
    for k, (est, lab, c, m) in enumerate(EST):
        v = iv[(iv.category == cat) & (iv.estimator == est)].iloc[0]
        ax.errorbar(v.older_limit_ma, top + 0.25 + 0.22 * k, xerr=[[v.older_limit_ma - v.limit_q05], [v.limit_q95 - v.older_limit_ma]],
                    fmt=m, color=c, ms=5, capsize=2, label=lab if cat == "B0" else None)
    ticks.append(((y0 + top) / 2, f"{label}\n({len(r)} horizons older than 413 Ma)"))
    y0 = top + 1.3
ax.axvspan(469.4, 458.2, color="#f2d7a6", alpha=0.6, lw=0)
ax.text(463.8, y0 - 0.2, "embryophyte\ncryptospores\n(possible → certain)", ha="center", va="top", fontsize=7.5)
for i, (name, old, young) in enumerate(CLOCKS):
    yy = y0 + 0.35 * i
    ax.plot([young, old], [yy, yy], color="#2e7d32", lw=3, alpha=0.8, solid_capstyle="butt")
    ax.text(old + 0.5, yy, name, ha="right", va="center", fontsize=7.5, color="#2e7d32")
ax.axvline(431.2, color="#a32020", ls="--", lw=1)
ax.text(431.2, -0.6, "M3 431.2 Ma", color="#a32020", ha="center", fontsize=8)
ax.set_yticks([t[0] for t in ticks], [t[1] for t in ticks], fontsize=8)
ax.set_xlim(472, 413)
ax.set_ylim(-1, y0 + 1.2)
ax.set_xlabel("Age (Ma)")
ax.set_title("Pilot: older limits of first appearance (95%), main reading; crown-tracheophyte clock intervals in green", fontsize=9)
ax.legend(loc="lower left", fontsize=8, frameon=False)
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(OUT / "pilot_figure.png", dpi=180)
