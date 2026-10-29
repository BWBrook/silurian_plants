"""Stream the two GBDB xlsx workbooks to UTF-8 CSV with the standard library only.

Usage (on nectar):
  ssh nectar python3 -I - <RAW_DIR> < gbdb_xlsx2csv.py
  RAW_DIR = /data/codex/silurian_plants/raw/gbdb/<UTC stamp>   (holds extracted/*.xlsx)

Writes RAW_DIR/csv/<workbook>__<sheet>.csv, one per non-empty sheet, and RAW_DIR/csv/xlsx_inventory.tsv.
Cell values are the workbook's own: shared strings resolved, numbers written as the stored text
(no float round-trip), booleans as 1/0, errors as #ERR. Dates are not converted (GBDB stores none
as Excel dates; a date-styled numeric cell would appear as its serial number). Row and column
positions are kept: a missing cell is an empty field, and every row is padded to the sheet width.
The sheet XML is parsed as a stream from the zip; nothing is expanded to disk.
"""
import csv
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
RNS = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
PKG = "{http://schemas.openxmlformats.org/package/2006/relationships}"
REF = re.compile(r"([A-Z]+)(\d+)")


def col_index(letters):
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n - 1


def shared_strings(z):
    out = []
    with z.open("xl/sharedStrings.xml") as fh:
        for _, el in ET.iterparse(fh, events=("end",)):
            if el.tag == NS + "si":
                parts = []
                for t in el.iter(NS + "t"):
                    parts.append(t.text or "")
                out.append("".join(parts))
                el.clear()
    return out


def sheets(z):
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
    target = {r.get("Id"): r.get("Target") for r in rels.iter(PKG + "Relationship")}
    for s in wb.iter(NS + "sheet"):
        t = target[s.get(RNS + "id")]
        yield s.get("name"), "xl/" + t.lstrip("/").removeprefix("xl/")


def stream_rows(z, path, sst):
    with z.open(path) as fh:
        for _, el in ET.iterparse(fh, events=("end",)):
            if el.tag != NS + "row":
                continue
            r = int(el.get("r"))
            cells = {}
            for c in el.iter(NS + "c"):
                m = REF.match(c.get("r"))
                t = c.get("t")
                v = c.find(NS + "v")
                if t == "inlineStr":
                    is_ = c.find(NS + "is")
                    val = "".join((x.text or "") for x in is_.iter(NS + "t")) if is_ is not None else ""
                elif v is None or v.text is None:
                    continue
                elif t == "s":
                    val = sst[int(v.text)]
                elif t == "b":
                    val = "1" if v.text.strip() == "1" else "0"
                elif t == "e":
                    val = "#ERR"
                else:
                    val = v.text
                cells[col_index(m.group(1))] = val
            el.clear()
            yield r, cells


def main(raw):
    raw = Path(raw)
    out = raw / "csv"
    out.mkdir(exist_ok=True)
    inv = []
    for xl in sorted((raw / "extracted").glob("*.xlsx")):
        z = zipfile.ZipFile(xl)
        sst = shared_strings(z)
        for name, path in sheets(z):
            dst = out / f"{xl.stem.replace(' ', '_')}__{name}.csv"
            n_rows = width = 0
            with dst.open("w", newline="", encoding="utf-8") as fo:
                w = csv.writer(fo, lineterminator="\n")
                pending, last = [], 0
                for r, cells in stream_rows(z, path, sst):
                    if not cells:
                        continue
                    width = max(width, max(cells) + 1)
                    pending.append((r, cells))
                    if len(pending) >= 20000:
                        pending, last, n_rows = flush(w, pending, last, n_rows, width)
                pending, last, n_rows = flush(w, pending, last, n_rows, width)
            if n_rows == 0:
                dst.unlink()
            inv.append((xl.name, name, path, n_rows, width, dst.name if n_rows else ""))
            print(xl.name, name, n_rows, width, flush=True)
    with (out / "xlsx_inventory.tsv").open("w") as f:
        f.write("workbook\tsheet\tpart\tnon_empty_rows\twidth_columns\tcsv\n")
        for row in inv:
            f.write("\t".join(map(str, row)) + "\n")


def flush(w, pending, last, n_rows, width):
    # pad to the running width; the final width is applied at read time (trailing empties are harmless)
    for r, cells in pending:
        row = [cells.get(i, "") for i in range(width)]
        w.writerow(row)
        n_rows += 1
        last = r
    return [], last, n_rows


if __name__ == "__main__":
    main(sys.argv[1])
