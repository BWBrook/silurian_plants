"""Open-but-unread works (the project's open_unread.tsv): fetch through the library's open routes, then from the stated URL.

Usage (on nectar, from /data/codex/silurian_plants/library/_tools/;
input is a copy of the project's library/open_unread.tsv in _tools/open_unread_input.tsv):
  python3 library_open_unread.py seeds     # write seeds/open_unread.tsv (mapped OpenAlex ids, plus the Zenodo DOI)
  python3 library_open_unread.py direct    # for works with no held copy: BHL probes and the stated URL, with library.py's own
                                           # download, title check and manifest code (library.try_candidate); TDM routes stay off
  python3 library_open_unread.py report    # write _build/open_unread_results.tsv (merge with the Codex identity verdicts if present)

The store is nectar:/data/codex/silurian_plants/library.

Policy (from the project): open copies only; no BHL API key and no registration (public itempdf links only, once per item);
a host that answers with a bot challenge, CAPTCHA, 403 or similar is recorded as `blocked` with host and status and is not
worked around; no email or personal identifier is sent. The mapping from input rows to OpenAlex ids is OPENALEX_ID below
(checked against title, year and venue in works.tsv; the Codex identity check then tests each stored file).
"""

import argparse
import csv
import hashlib
import json
import re
import sys
import threading
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import library_run as R  # noqa: E402  (library.py with TDM routes emptied)

L = R.L
STORE = Path("/data/codex/silurian_plants/library")
INPUT = HERE / "open_unread_input.tsv"
UA_NOTE = "library.py user agent (EPRP-library/0.2, no email)"

# input row number -> OpenAlex id. None: no OpenAlex record is needed or known (BHL volumes, PalAss pre-2000, Zenodo).
OPENALEX_ID = {
    1: "W2150004271", 2: "W1994498836", 3: "W2021681869", 11: "W4399565014", 12: "W2963287438", 13: "W1820528062",
    14: "W2118077543", 15: "W3214901098", 16: "W3217259987", 17: "W4281742796", 18: "W4313652636", 19: "W4327970396",
    20: "W4403278171", 21: "W2994812694", 22: "W4414281078", 23: "W7162764070", 24: "W2289323837", 25: "W1843710198",
    26: "W2100880278", 27: "W2062921085", 28: "W2551960245", 29: "W4400899891", 30: "W1964309047", 31: "W2007890326",
    32: "W1990866222", 33: "W2091539779", 34: "W4293382743", 35: "W2897184852", 36: "W1977743584", 37: "W2292842751",
    38: "W1982800406", 39: "W2793000306", 40: "W2314927738", 41: "W4311402486",
}
# works with no OpenAlex record: pseudo ids `XU<nn>` carry the stated URL's provenance; title from the project's own citation line.
PSEUDO = {
    10: {"id": "XU010", "title": "Early Devonian plant fossils from a southern England borehole", "year": 1978,
         "authors": "Chaloner, Hill & Rogerson", "venue": "Palaeontology"},
}
# BHL items in the input, split into the works they hold (row, label, BHL item, citation start page)
BHL_WORKS = [
    (4, "Kidston & Lang 1917 Part I (Trans RSE 51: 761)", "130747"),
    (5, "Kidston & Lang 1920 Part II (Trans RSE 52: 603)", "189113"),
    (5, "Kidston & Lang 1920 Part III (Trans RSE 52: 643)", "189113"),
    (5, "Kidston & Lang 1921 Part IV (Trans RSE 52: 831)", "189113"),
    (5, "Kidston & Lang 1921 Part V (Trans RSE 52: 855)", "189113"),
    (6, "Jaeger 1966 (Proc R Soc Vic 79: 393)", "257910"),
    (7, "Halle 1916 (K Svenska Vetensk Akad Handl 57(1))", "131280"),
    (8, "Banks, Leclercq & Hueber 1975 (Palaeontographica Americana 8: 77)", "40614"),
    (9, "Hueber 1961 (Ann Mo Bot Gard 48: 125)", "54726"),
]
ZENODO_PART_IV = {"record": "2503478", "label": "Kidston & Lang 1921 Part IV (Trans RSE 52: 831)"}
CHALLENGE = re.compile(r"just a moment|cf-chl|captcha|attention required|access denied|are you a robot|verify you are human|bot protection", re.I)


def read_input():
    rows = L.read_tsv(INPUT)
    for i, r in enumerate(rows, 1):
        r["n"] = i
    return rows


def pdf_like(url):
    return bool(re.search(r"\.pdf($|\?)|/bitstream/|/document$", url, re.I))


def api_json(url):
    return L.get_json(url, tries=2)[0]


def stated_urls(row):
    """Candidate (kind, url) pairs from the stated URL; figshare and Zenodo go through their public record APIs."""
    url = row["url"]
    host = urllib.parse.urlsplit(url).hostname or ""
    if "figshare.com" in host:
        aid = re.search(r"/(\d+)$", url)
        data = api_json(f"https://api.figshare.com/v2/articles/{aid.group(1)}") if aid else {}
        return [("pdf", f["download_url"]) for f in data.get("files", []) if f["name"].lower().endswith(".pdf")] or [("landing", url)]
    return [("pdf" if pdf_like(url) else "landing", url)]


def seeds():
    rows = [{"openalex_id": w, "doi": ""} for w in sorted(set(OPENALEX_ID.values()))]
    rows.append({"openalex_id": "", "doi": "10.5281/zenodo.2503478"})
    L.write_tsv(HERE / "seeds" / "open_unread.tsv", rows, ["openalex_id", "doi"])
    print(len(rows), "seed rows -> seeds/open_unread.tsv")


class Spy:
    """Remember the last page fetched per URL so a failed landing page can be checked for a bot challenge."""

    def __init__(self):
        self.last = {}
        self.orig = L.get_bytes

    def __call__(self, url, pacer, accept="application/pdf,*/*;q=0.5", headers=None):
        out = self.orig(url, pacer, accept, headers)
        self.last[url] = (out[0], out[2][:4000])
        return out


def classify_failure(outcome, spy, tried_url):
    """blocked / not_found / failed, with host and status, from a library.py fetch outcome."""
    host = urllib.parse.urlsplit(tried_url).hostname or ""
    m = re.fullmatch(r"http_(\d+)", outcome)
    if m:
        code = int(m.group(1))
        if code in (401, 403, 429, 451, 503):
            return "blocked", host, f"HTTP {code}"
        if code in (404, 410):
            return "not_found", host, f"HTTP {code}"
        return "failed", host, f"HTTP {code}"
    for url, (final, body) in spy.last.items():
        if CHALLENGE.search(body.decode("utf-8", "replace")):
            return "blocked", urllib.parse.urlsplit(final).hostname or host, "bot challenge page"
    return "failed", host, outcome


def log_attempt(wid, url, host, outcome, detail):
    L.append_tsv(STORE / "attempts.tsv", {"openalex_id": wid, "url": url, "host": host, "outcome": outcome, "detail": detail,
                                           "when": L.now()}, L.ATTEMPT_FIELDS, lock)


lock = threading.Lock()


def held_status(wid):
    m = {r["openalex_id"]: r for r in L.read_tsv(STORE / "manifest.tsv")}.get(wid)
    return m if m and m["status"] in ("ok", "no_text") and (STORE / m["path"]).exists() else None


def direct():
    rows = read_input()
    pacer = L.HostPacer(3.0)
    spy = Spy()
    L.get_bytes = spy
    tool_sha = hashlib.sha256((HERE / "library.py").read_bytes()).hexdigest()
    results = []
    recs = L.load_records(STORE)

    def attempt(label, wid, rec, urls):
        for kind, url in urls:
            spy.last.clear()
            host = urllib.parse.urlsplit(url).hostname or ""
            outcome, detail = L.try_candidate(rec, (kind, url, host, "", ""), STORE, pacer, lock, tool_sha)
            log_attempt(wid, url, host, outcome, detail)
            if outcome in L.OPEN_HELD:
                results.append({"label": label, "openalex_id": wid, "outcome": "fetched", "route": "stated_url", "url": url,
                                "host": host, "status": outcome, "note": detail})
                return
            kind_, h, st = classify_failure(outcome, spy, url)
            last = {"label": label, "openalex_id": wid, "outcome": kind_, "route": "stated_url", "url": url, "host": h, "status": st,
                    "note": detail}
        results.append(last)

    # 1. BHL: one public itempdf request per item, no key; a challenge page or 403 is recorded and not worked around.
    seen_items = {}
    for n, label, item in BHL_WORKS:
        url = f"https://www.biodiversitylibrary.org/itempdf/{item}"
        if item not in seen_items:
            pacer.wait(url)
            status = detail = ""
            try:
                req = urllib.request.Request(url, headers={"User-Agent": L.UA, "Accept": "application/pdf,*/*;q=0.5"})
                with urllib.request.urlopen(req, timeout=60) as r:
                    head = r.read(2000)
                    status = f"HTTP {r.status}"
                    detail = "a PDF was offered (whole-volume item); not downloaded" if head.startswith(b"%PDF") else "non-PDF response"
            except urllib.error.HTTPError as e:
                body = e.read(4000).decode("utf-8", "replace")
                status = f"HTTP {e.code}"
                detail = "bot challenge page (Cloudflare 'Just a moment')" if CHALLENGE.search(body) else "refused"
            except Exception as e:
                status, detail = "error", f"{type(e).__name__}: {str(e)[:80]}"
            seen_items[item] = (status, detail)
            log_attempt(f"BHL-item-{item}", url, "www.biodiversitylibrary.org", "bhl_probe", f"{status}; {detail}")
        status, detail = seen_items[item]
        outcome = "blocked" if status.startswith("HTTP 4") or "challenge" in detail else "failed"
        results.append({"label": label, "openalex_id": "", "outcome": outcome, "route": "bhl_itempdf", "url": url,
                        "host": "www.biodiversitylibrary.org", "status": status, "note": detail})

    # 2. Zenodo copy of Kidston & Lang 1921 Part IV (public record API, no key)
    rec_id = ZENODO_PART_IV["record"]
    zurl = f"https://zenodo.org/api/records/{rec_id}"
    try:
        zj = api_json(zurl)
        files = [f for f in zj.get("files", []) if f.get("key", "").lower().endswith(".pdf")]
        link = (files[0].get("links") or {}).get("self") if files else ""
        title = ((zj.get("metadata") or {}).get("title")) or ""
    except Exception as e:
        files, link, title = [], "", ""
        log_attempt("XU-zenodo", zurl, "zenodo.org", "error", f"{type(e).__name__}: {str(e)[:80]}")
    if link:
        wid = "XU101"
        rec = {"id": f"https://openalex.org/{wid}", "title": title, "doi": f"10.5281/zenodo.{rec_id}", "publication_year": 1921}
        attempt(ZENODO_PART_IV["label"], wid, rec, [("pdf", link)])
    else:
        results.append({"label": ZENODO_PART_IV["label"], "openalex_id": "", "outcome": "not_found", "route": "zenodo_api",
                        "url": zurl, "host": "zenodo.org", "status": "no PDF file in the record", "note": ""})

    # 3. Everything else: library routes have run first; try the stated URL for works with no held copy.
    for row in rows:
        n = row["n"]
        if n in {x[0] for x in BHL_WORKS}:
            continue
        if n in PSEUDO:
            ps = PSEUDO[n]
            wid = ps["id"]
            rec = {"id": f"https://openalex.org/{wid}", "title": ps["title"], "doi": "", "publication_year": ps["year"]}
        else:
            wid = OPENALEX_ID[n]
            rec = recs.get(wid)
            if not rec:
                results.append({"label": row["work"], "openalex_id": wid, "outcome": "failed", "route": "none", "url": row["url"],
                                "host": "", "status": "no OpenAlex record in store", "note": ""})
                continue
        m = held_status(wid)
        if m:
            results.append({"label": row["work"], "openalex_id": wid, "outcome": "fetched", "route": "library_open_routes",
                            "url": m["url"], "host": m["host"], "status": m["status"], "note": "held before the stated-URL pass"})
            continue
        try:
            urls = stated_urls(row)
        except Exception as e:
            results.append({"label": row["work"], "openalex_id": wid, "outcome": "failed", "route": "stated_url", "url": row["url"],
                            "host": "", "status": f"{type(e).__name__}", "note": str(e)[:80]})
            continue
        attempt(row["work"], wid, rec, urls)
    out = STORE / "_build" / "open_unread_direct.json"
    out.write_text(json.dumps(results, indent=1, ensure_ascii=False))
    for r in results:
        print(r["outcome"], "|", r["label"][:55], "|", r["host"], r["status"])


def doi_target_host(url):
    """Host a doi.org link resolves to, from the public handle API (a request to doi.org only, not to the publisher)."""
    m = re.search(r"doi\.org/(10\.\S+)", url)
    if not m:
        return ""
    try:
        data = api_json("https://doi.org/api/handles/" + urllib.parse.quote(m.group(1), safe="/"))
        for v in data.get("values", []):
            if v.get("type") == "URL":
                return urllib.parse.urlsplit(v["data"]["value"]).hostname or ""
    except Exception:
        pass
    return ""


def report():
    rows = read_input()
    direct_rows = json.loads((STORE / "_build" / "open_unread_direct.json").read_text())
    manifest = {r["openalex_id"]: r for r in L.read_tsv(STORE / "manifest.tsv")}
    identity = {}
    p = STORE / "_build" / "identity_verdicts.json"
    if p.exists():
        identity = {r["id"]: r for r in json.loads(p.read_text())}
    out = []
    for r in direct_rows:
        wid = r["openalex_id"]
        m = manifest.get(wid)
        held = bool(m and m["status"] in ("ok", "no_text"))
        outcome = r["outcome"]
        withdrawn = bool(m and m["status"] == "withdrawn")
        if withdrawn:
            outcome = "failed"
        elif held:
            outcome = "fetched"
        host = (m or {}).get("host") or r["host"]
        route = r["route"]
        if held and r["route"] == "library_open_routes":
            route = {"PubMed Central OA": "pmc_open_access_bucket", "Internet Archive": "internet_archive_scan", "CORE": "core_repository_link",
                     "Semantic Scholar": "semantic_scholar_oa_link"}.get(host, "openalex_location")
        if outcome in ("blocked", "failed") and host == "doi.org":
            host = doi_target_host(r["url"]) or host
        out.append({"work": r["label"], "outcome": outcome, "route": route if outcome == "fetched" or r["route"] == "bhl_itempdf" else r["route"],
                    "url_used": (m or {}).get("url") if held else r["url"], "host": host,
                    "blocked_status": "" if withdrawn else (r["status"] if outcome in ("blocked", "failed", "not_found") else ""),
                    "openalex_id": wid, "bytes": (m or {}).get("bytes", "") if held else "", "sha256": (m or {}).get("sha256", "") if held else "",
                    "identity_check": identity.get(wid, {}).get("verdict", "") if (held or withdrawn) else "",
                    "note": (m or {}).get("note", "") if (held or withdrawn) else r["note"]})
    for r in out:
        if r["openalex_id"] == "W2314927738" and r["outcome"] == "failed":
            r["note"] = ("the figshare file is the chapter's Supplementary Material (appendix of spore assemblages); it failed the title check "
                         "and is quarantined (Codex quarantine review: same_work, SUPPLEMENT); the chapter text was not obtained")
    L.write_tsv(STORE / "_build" / "open_unread_results.tsv", out, ["work", "outcome", "route", "url_used", "host", "blocked_status",
                                                                     "openalex_id", "bytes", "sha256", "identity_check", "note"])
    from collections import Counter
    print(Counter(r["outcome"] for r in out))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["seeds", "direct", "report"])
    a = ap.parse_args()
    {"seeds": seeds, "direct": direct, "report": report}[a.cmd]()
