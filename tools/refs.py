# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml"]
# ///
"""Build the programme bibliography from its DOI ledger.

    uv run tools/refs.py build   # references/dois.txt + manual.yaml -> references/refs.yaml

references/dois.txt (one DOI per line) is the ledger: add a DOI there, rebuild, cite the printed key.
Metadata comes from Crossref's CSL-JSON; works without a DOI go in references/manual.yaml.
Keys follow Better BibTeX's auth.lower + year + three-word short title, so a Zotero export matches.
"""

import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

REFS = Path(__file__).resolve().parents[1] / "references"
STOP = set("a an the of and or in on for to from with at by as into via its their is are be about over under "
           "between within without among during after before through new some".split())
TYPES = {"journal-article": "article-journal", "book-chapter": "chapter", "proceedings-article": "paper-conference",
         "posted-content": "article", "monograph": "book"}
KEEP = ["type", "title", "author", "issued", "container-title", "volume", "issue", "page", "article-number",
        "publisher", "DOI", "URL"]


def fetch(doi):
    url = ("https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/")
           + "/transform/application/vnd.citationstyles.csl+json")
    req = urllib.request.Request(url, headers={"User-Agent": "silurian_plants-refs/0.1"})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code != 429 or attempt == 4:
                raise
            time.sleep(2 ** attempt * 2)


def ascii_fold(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def markup(s):
    s = re.sub(r"</?(i|em)>", "*", s)
    s = re.sub(r"<sub>(.*?)</sub>", r"~\1~", s)
    s = re.sub(r"<sup>(.*?)</sup>", r"^\1^", s)
    return re.sub(r"<[^>]+>", "", s).strip()


def key(entry):
    family = ascii_fold(entry["author"][0].get("family", entry["author"][0].get("literal", ""))).lower()
    family = re.sub(r"[^a-z-]", "", family)
    year = entry["issued"]["date-parts"][0][0]
    words = [w for w in re.findall(r"[A-Za-z0-9-]+", ascii_fold(re.sub(r"<[^>]+>", "", entry["title"])))
             if w.lower() not in STOP]
    return f"{family}{year}" + "".join(w.replace("-", "").capitalize() for w in words[:3])


def clean(raw):
    entry = {k: raw[k] for k in KEEP if raw.get(k)}
    entry["type"] = TYPES.get(entry["type"], entry["type"])
    for k in ("title", "container-title"):
        if isinstance(entry.get(k), list):
            entry[k] = entry[k][0]
        if k in entry:
            entry[k] = markup(entry[k])
    entry["author"] = [{x: a[x] for x in ("family", "given", "literal") if a.get(x)} for a in raw["author"]]
    issued = raw.get("issued") or raw.get("published-print") or raw.get("published-online")
    entry["issued"] = {"date-parts": [issued["date-parts"][0][:1]]}
    if entry.get("DOI"):
        entry["DOI"] = entry["DOI"].lower()
        entry.pop("URL", None)
    entry["page"] = entry.get("page", "").replace("-", "–") or None
    return {k: v for k, v in entry.items() if v}


def build():
    dois = [d.strip().lower() for d in (REFS / "dois.txt").read_text().splitlines()
            if d.strip() and not d.startswith("#")]
    if len(set(dois)) != len(dois):
        sys.exit("duplicate DOI in dois.txt")
    entries = [clean(fetch(d)) for d in dois]
    entries += yaml.safe_load((REFS / "manual.yaml").read_text())["references"]
    out = []
    for e in entries:
        k = e.pop("id", None) or key(e)
        out.append({"id": k, "citation-key": k, **e})
    keys = [e["id"] for e in out]
    if len(set(keys)) != len(keys):
        sys.exit("key collision: " + ", ".join(k for k in keys if keys.count(k) > 1))
    out.sort(key=lambda e: e["id"])
    text = yaml.safe_dump({"references": out}, allow_unicode=True, sort_keys=False, width=200)
    (REFS / "refs.yaml").write_text("---\n" + text + "...\n")
    for e in out:
        print(e["id"], e.get("DOI", ""))


if __name__ == "__main__":
    if sys.argv[1:] != ["build"]:
        sys.exit(__doc__)
    build()
