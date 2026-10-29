#!/usr/bin/env python3
"""Stage 1 of the silurian_plants library extraction.

Reads the EPRP works table and the OpenAlex records in the store and writes one
JSON line per work with the fields the screen needs: title, reconstructed
abstract, OpenAlex keywords, concepts and topics, and all author names.
Read-only on the store. stdlib only.

    python3 library_features.py --works works.tsv --store /data/codex/artifacts/eprp-paleodata-backup/latest/library --out features.jsonl
"""
import argparse
import csv
import json
import os


def abstract(inv):
    if not inv:
        return ""
    pos = []
    for word, idxs in inv.items():
        for i in idxs:
            pos.append((i, word))
    pos.sort()
    return " ".join(w for _, w in pos)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--works", required=True)
    ap.add_argument("--store", default="/data/codex/artifacts/eprp-paleodata-backup/latest/library")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    texts = set(os.listdir(os.path.join(a.store, "text")))
    n = 0
    with open(a.works, newline="", encoding="utf-8") as fh, open(a.out, "w", encoding="utf-8") as out:
        for row in csv.DictReader(fh, delimiter="\t"):
            wid = row["openalex_id"]
            rec = {}
            p = os.path.join(a.store, "openalex", wid + ".json")
            if os.path.exists(p):
                with open(p, encoding="utf-8") as jf:
                    rec = json.load(jf)
            f = dict(row)
            f["abstract"] = abstract(rec.get("abstract_inverted_index"))
            f["keywords"] = [k["display_name"] for k in rec.get("keywords") or []]
            f["concepts"] = [
                c["display_name"] for c in rec.get("concepts") or [] if c.get("score", 0) >= 0.3
            ]
            f["topics"] = [t["display_name"] for t in rec.get("topics") or []]
            f["authors"] = [
                (au.get("author") or {}).get("display_name") or au.get("raw_author_name") or ""
                for au in rec.get("authorships") or []
            ]
            f["has_json"] = bool(rec)
            f["has_text_file"] = (wid + ".txt") in texts
            out.write(json.dumps(f, ensure_ascii=False) + "\n")
            n += 1
    print(f"wrote {n} works to {a.out}")


if __name__ == "__main__":
    main()
