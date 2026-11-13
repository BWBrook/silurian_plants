"""Extract literal point reports from the six held Abuhmida thesis enclosures.

Run with: uv run --with pymupdf==2.0.0 studies/f3/tools/libya_charts.py
Requires the registered, git-ignored thesis PDF. This creates source reports,
not adjudicated event outcomes or binary analysis inputs.
"""

import csv
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

import pymupdf


ROOT = Path(__file__).resolve().parents[3]
DATA = ROOT / "studies/f3/data/units"
SOURCE = ROOT / "library/closed/abuhmida2013-thesis-related_macbook20261030.pdf"
SHA256 = "c0e3bf798fb3c27db0bf9cbb155396be5b4b8e003ee2228defb615a65abf3211"
PAGES = [(630, "A28i-NC186", 24), (632, "B2-NC186", 17),
         (634, "D1-200", 35), (636, "E1-NC174", 15),
         (638, "H2-NC186", 28), (640, "I3-NC186", 39)]
MARINE = {(0.0, 0.0, 1.0), (0.0, 1.0, 1.0), (1.0, 1.0, 0.0)}


def key(row):
    return row["well"], float(row["depth_ft"])


def read_csv(path):
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def extract_page(page, page_number, well, expected):
    words = page.get_text("words")
    depths = [w for w in words if re.fullmatch(r"\d{4}\.\d{2}'", w[4])]
    xmin = min(w[0] for w in depths)
    labels = []
    for word in depths:
        if word[0] > xmin + 0.3:
            continue
        codes = [w[4] for w in words if abs(w[1] - word[1]) < 0.05
                 and 0 <= w[0] - word[2] < 9 and w[4] in {"CO", "CU", "LOG"}]
        assert len(codes) == 1, (well, word, codes)
        labels.append({"depth": float(word[4][:-1]), "code": codes[0],
                       "y": (word[1] + word[3]) / 2, "height": word[3] - word[1],
                       "marine": 0, "other": 0, "target": 0})
    labels.sort(key=lambda row: row["y"])
    samples = [row for row in labels if row["code"] != "LOG"]
    assert len(samples) == 2 * expected, (well, len(samples))
    upper, lower = samples[:expected], samples[expected:]
    assert [(r["depth"], r["code"]) for r in upper] == [
        (r["depth"], r["code"]) for r in lower], well
    headers = [w for w in words if w[4] == "Ambitisporites"]
    assert len(headers) == (0 if well == "A28i-NC186" else 2), well
    targets = [(h[0] + h[2]) / 2 for h in headers]
    if targets:
        assert abs(targets[0] - targets[1]) < 0.01, well
    markers = [d for d in page.get_drawings() if d["fill"]
               and len(set(d["fill"])) > 1
               and 0 < d["rect"].width < 3 and 0 < d["rect"].height < 3]
    max_residual = 0.0
    for marker in markers:
        rect = marker["rect"]
        x, y = (rect.x0 + rect.x1) / 2, (rect.y0 + rect.y1) / 2
        nearest = sorted(labels, key=lambda row: abs(y - row["y"]))
        row = nearest[0]
        distance = abs(y - row["y"])
        assert distance < row["height"] * 0.35, (well, x, y, row)
        assert abs(y - nearest[1]["y"]) > row["height"] * 0.35, (well, x, y)
        assert row["code"] != "LOG", (well, x, y)
        max_residual = max(max_residual, distance)
        if targets and abs(x - targets[0]) < 0.5:
            row["target"] += 1
        elif marker["fill"] in MARINE:
            row["marine"] += 1
        else:
            assert marker["fill"][0] == 0 and marker["fill"][2] == 0, marker
            row["other"] += 1
    result = []
    for first, second in zip(upper, lower):
        assert all(first[c] == second[c] for c in ["target", "marine", "other"]), (
            well, first, second)
        assert first["target"] <= 1, (well, first)
        result.append({
            "well": well, "depth_ft": f'{first["depth"]:.2f}',
            "type_code": first["code"],
            "ambitisporites_dilutus_report": ("mark-present" if first["target"] else
                                              "no-mark" if targets else "column-absent"),
            "target_symbols": first["target"],
            "marine_symbols": first["marine"],
            "other_green_symbols": first["other"],
            "total_symbols": first["target"] + first["marine"] + first["other"],
            "panels_agree": "yes", "source_id": "abuhmida2013",
            "source_locator": f"Enclosure printed p.{page_number - 16}; PDF p.{page_number}; both panels",
        })
    return result, {"well": well, "pdf_page": page_number, "chart_rows": expected,
                    "vector_symbols_both_panels": len(markers),
                    "max_row_residual_pt": round(max_residual, 6),
                    "unmapped_symbols": 0, "panels_agree": True}


def main():
    assert digest(SOURCE) == SHA256, "Source hash differs from the inspected thesis"
    appendix = {key(r): r for r in read_csv(DATA / "libya_appendix1.csv")}
    enclosure = {key(r): r for r in read_csv(DATA / "libya_enclosures.csv")}
    rows, checks = [], []
    with pymupdf.open(SOURCE) as pdf:
        for page_number, well, expected in PAGES:
            extracted, check = extract_page(pdf[page_number - 1], page_number, well, expected)
            rows.extend(extracted)
            checks.append(check)
    assert len(rows) == len(enclosure) == 158
    assert {key(r) for r in rows} == set(enclosure)
    for row in rows:
        assert row["type_code"] == enclosure[key(row)]["type_code"]
        row["exact_appendix_match"] = "yes" if key(row) in appendix else "no"
    output = DATA / "libya_chart_reports.csv"
    with output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    receipt = {
        "source_path": str(SOURCE.relative_to(ROOT)), "source_sha256": SHA256,
        "pymupdf_version": pymupdf.VersionBind,
        "script_sha256": digest(Path(__file__)),
        "input_sha256": {name: digest(DATA / name) for name in
                         ["libya_appendix1.csv", "libya_enclosures.csv"]},
        "output_sha256": {output.name: digest(output)}, "pages": checks,
        "chart_rows": len(rows), "exact_appendix_matches": sum(
            row["exact_appendix_match"] == "yes" for row in rows),
        "target_report_counts": dict(Counter(row["ambitisporites_dilutus_report"] for row in rows)),
        "rows_with_marine_symbols": sum(row["marine_symbols"] > 0 for row in rows),
        "rows_without_symbols": sum(row["total_symbols"] == 0 for row in rows),
        "interpretation": "Literal source symbols only; blanks and omitted columns are not adopted absences."
    }
    (DATA / "libya_chart_receipt.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
