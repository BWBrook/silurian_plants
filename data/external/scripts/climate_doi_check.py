# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Check every DOI cited in climate/README.md and climate/other_sources.csv against its registry.

Crossref for journal and article DOIs; DataCite for Zenodo, figshare and GFZ dataset DOIs.
Writes climate/doi_check.tsv: doi, registry, status, title, first_author_or_creator, year.
A plain user agent, no email address.

Usage: uv run climate_doi_check.py
"""
import csv
import json
import re
import time
import urllib.error
import urllib.request
from pathlib import Path

CLIMATE = Path(__file__).resolve().parent.parent / "climate"
UA = "Mozilla/5.0 (compatible; research-data-fetch)"
DATACITE_PREFIXES = ("10.5281/", "10.6084/", "10.5880/", "10.5061/")


def dois():
    text = (CLIMATE / "README.md").read_text() + (CLIMATE / "other_sources.csv").read_text()
    found = re.findall(r"10\.\d{4,9}/[^\s\"'<>)\],;`]+", text)
    seen = {}
    for d in found:
        seen.setdefault(d.rstrip(".:").lower(), d.rstrip(".:"))
    return sorted(seen.values(), key=str.lower)


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None


def check(doi):
    if doi.startswith(DATACITE_PREFIXES):
        status, j = get(f"https://api.datacite.org/dois/{doi}")
        if status != 200:
            return "DataCite", status, "", "", ""
        a = j["data"]["attributes"]
        title = a["titles"][0]["title"] if a.get("titles") else ""
        creator = a["creators"][0]["name"] if a.get("creators") else ""
        return "DataCite", status, title, creator, a.get("publicationYear", "")
    status, j = get(f"https://api.crossref.org/works/{doi}")
    if status != 200:
        return "Crossref", status, "", "", ""
    m = j["message"]
    title = (m.get("title") or [""])[0]
    creator = (m.get("author") or [{}])[0].get("family", "")
    year = ((m.get("issued") or {}).get("date-parts") or [[""]])[0][0]
    return "Crossref", status, title, creator, year


def main():
    rows = []
    for d in dois():
        reg, status, title, creator, year = check(d)
        rows.append([d, reg, status, re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", title))[:120], creator, year])
        time.sleep(0.5)
    with open(CLIMATE / "doi_check.tsv", "w", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(["doi", "registry", "status", "title", "first_creator", "year"])
        w.writerows(rows)
    bad = [r[0] for r in rows if r[2] != 200]
    print(len(rows), "DOIs;", "unresolved:", bad or "none")


if __name__ == "__main__":
    main()
