#!/usr/bin/env python3
"""Page GBIF and iDigBio public search APIs for early-land-plant fossil specimens; keep every raw JSON page.

Modes (stdlib only, no credentials, plain user agent without contact details):
  gbif           GBIF occurrence search, basisOfRecord=FOSSIL_SPECIMEN: Plantae and other kingdoms by chronostratigraphic fields,
                 Plantae by free-text period and stage names, and every scope name (genus-level q, backbone taxonKey)
  idigbio        iDigBio record search, basisofrecord=fossilspecimen: plantae by free-text period and stage names, other and
                 missing kingdoms by period, and every scope name
  gbif-datasets  GBIF dataset and organisation records for the datasetKeys in a finished GBIF harvest
  gbif-verbatim  GBIF verbatim records for gbifIDs listed in a file (names as recorded)
  idigbio-media  iDigBio media records (accessURI) for media UUIDs listed in a file
  idigbio-recordsets  iDigBio recordset records (collection name, stated data rights) for the recordsets in a harvest

usage:
  python3 specimens_harvest.py gbif OUTROOT SCOPE_CSV [--workers N] [--smoke] [--only names]
  python3 specimens_harvest.py idigbio OUTROOT SCOPE_CSV [--smoke] [--only names]
  python3 specimens_harvest.py gbif-datasets HARVEST_DIR
  python3 specimens_harvest.py gbif-verbatim HARVEST_DIR KEYFILE [--workers N]
  python3 specimens_harvest.py idigbio-media HARVEST_DIR UUIDFILE [--workers N]
  python3 specimens_harvest.py idigbio-recordsets HARVEST_DIR
OUTROOT is /data/codex/silurian_plants/raw on deep-server; a harvest lands in OUTROOT/<source>/<UTC stamp>/ with
provenance.tsv (URL, query, timestamp, record count, sha256 per page) and queries.tsv (one row per query).
Remote run: scp the script and scope CSV, then ssh deep-server python3 specimens_harvest.py ...
"""
import csv
import datetime
import glob
import hashlib
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "silurian-plants-specimen-harvest/1.0"
GBIF = "https://api.gbif.org/v1"
IDIG = "https://search.idigbio.org/v2"
PAGE_SAFE = 9000        # GBIF pages beyond an offset of about 10,000 are slow; partition below this
NAME_CAP = 6000         # a name query with more hits than this is restricted to the window periods
OSD = ["Ordovician", "Silurian", "Devonian"]

GBIF_FIELDS = {
    "period": ("earliestPeriodOrLowestSystem", "latestPeriodOrHighestSystem"),
    "epoch": ("earliestEpochOrLowestSeries", "latestEpochOrHighestSeries"),
    "stage": ("earliestAgeOrLowestStage", "latestAgeOrHighestStage"),
}
GBIF_EPOCH_VALUES = ["Ordovician", "LowerOrdovician", "MiddleOrdovician", "UpperOrdovician", "Silurian", "Llandovery",
                     "Wenlock", "Ludlow", "Pridoli", "Devonian", "LowerDevonian", "MiddleDevonian"]
GBIF_STAGE_VALUES = GBIF_EPOCH_VALUES + [
    "Tremadocian", "Floian", "Dapingian", "Darriwilian", "Sandbian", "Katian", "Hirnantian", "Rhuddanian", "Aeronian",
    "Telychian", "Sheinwoodian", "Homerian", "Gorstian", "Ludfordian", "Lochkovian", "Pragian", "Emsian", "Eifelian",
    "Givetian"]
GBIF_TEXT_TERMS = ["Devonian", "Silurian", "Ordovician", "Lochkovian", "Pragian", "Emsian", "Eifelian", "Givetian",
                   "Pridoli", "Ludlow", "Wenlock", "Llandovery", "Gorstian", "Ludfordian", "Homerian", "Sheinwoodian",
                   "Telychian", "Aeronian", "Rhuddanian", "Hirnantian", "Katian", "Sandbian", "Darriwilian", "Dapingian",
                   "Floian", "Tremadocian", "Gedinnian", "Siegenian", "Downtonian", "Dittonian", "Ludlovian"]
GBIF_OTHER_KINGDOMS = [5, 4, 7, 3, 0, 2]   # Fungi, Chromista, Protozoa, Bacteria, incertae sedis, Archaea
IDIG_TERMS = GBIF_TEXT_TERMS + ["niagaran", "cincinnatian", "alexandrian", "cayugan", "helderbergian", "oriskanian",
                                "ulsterian", "erian"]
IDIG_OTHER_KINGDOMS = ["fungi", "protozoa", "chromista", "incertae sedis", "taxon-indet.", "unknown", "bacteria",
                       "microfossils/palynology", "eukaryota", "ichnofossil", "archaea", "protista", "algae",
                       "to be looked up"]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def get(url, retries=7, timeout=600):
    delay = 2
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and i < retries - 1:
                time.sleep(delay)
                delay = min(delay * 2, 90)
                continue
            raise
        except (urllib.error.URLError, TimeoutError, ConnectionError, OSError):
            if i < retries - 1:
                time.sleep(delay)
                delay = min(delay * 2, 90)
                continue
            raise


class Store:
    def __init__(self, root, source, stamp=None):
        self.source = source
        self.stamp = stamp or datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.dir = os.path.join(root, source, self.stamp) if stamp is None else root
        os.makedirs(self.dir, exist_ok=True)
        self.lock = threading.Lock()
        self.seen = set()
        self.nfiles = 0
        self.nbytes = 0
        self.prov = open(os.path.join(self.dir, "provenance.tsv"), "a", encoding="utf-8")
        self.queries = open(os.path.join(self.dir, "queries.tsv"), "a", encoding="utf-8")
        if self.prov.tell() == 0:
            self.prov.write("file\turl\tquery\ttimestamp_utc\toffset\tn_records\tcount_reported\tbytes\tsha256\n")
        if self.queries.tell() == 0:
            self.queries.write("qid\tgroup\tquery\tcount\tfetched\tnew_unique\tnote\tseconds\n")

    def save(self, qid, offset, url, query, body, n, count, subdir=""):
        name = "%s__%06d.json" % (qid, offset)
        d = os.path.join(self.dir, subdir) if subdir else self.dir
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, name), "wb") as f:
            f.write(body)
        sha = hashlib.sha256(body).hexdigest()
        with self.lock:
            self.prov.write("\t".join([os.path.join(subdir, name) if subdir else name, url, json.dumps(query, sort_keys=True),
                                       utc(), str(offset), str(n), str(count), str(len(body)), sha]) + "\n")
            self.prov.flush()
            self.nfiles += 1
            self.nbytes += len(body)

    def log(self, qid, group, query, count, fetched, new, note, seconds):
        with self.lock:
            self.queries.write("\t".join([qid, group, json.dumps(query, sort_keys=True), str(count), str(fetched), str(new),
                                          note, "%.1f" % seconds]) + "\n")
            self.queries.flush()
            print("%s %-8s count=%s fetched=%s new=%s %s" % (qid, group, count, fetched, new, note), flush=True)

    def mark_new(self, ids):
        with self.lock:
            before = len(self.seen)
            self.seen.update(ids)
            return len(self.seen) - before


def read_scope(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- GBIF

def gbif_url(params, limit, offset, extra=()):
    pairs = []
    for k, v in sorted(params.items()):
        if isinstance(v, (list, tuple)):
            pairs.extend((k, x) for x in v)
        else:
            pairs.append((k, v))
    pairs.extend(extra)
    pairs.extend([("limit", limit), ("offset", offset)])
    return GBIF + "/occurrence/search?" + urllib.parse.urlencode(pairs)


def gbif_count(params):
    d = json.loads(get(gbif_url(params, 0, 0)))
    return d["count"]


def gbif_facet(params, field):
    out, off = [], 0
    while True:
        d = json.loads(get(gbif_url(params, 0, 0, [("facet", field), ("facetLimit", 500), ("facetOffset", off)])))
        c = d["facets"][0]["counts"] if d.get("facets") else []
        out.extend((x["name"], x["count"]) for x in c)
        if len(c) < 500:
            return out
        off += 500


def gbif_page_all(st, qid, params, count, group, note=""):
    t0 = time.time()
    fetched = new = 0
    parts = [("", params, count)]
    if count > PAGE_SAFE:
        fac = gbif_facet(params, "datasetKey")
        parts = [("_ds%s" % k[:8], dict(params, datasetKey=k), c) for k, c in fac if c > 0]
        note += " partitioned_by_datasetKey=%d" % len(parts)
    for suffix, p, c in parts:
        offset = 0
        while offset < min(c, 100000):
            url = gbif_url(p, 300, offset)
            body = get(url)
            d = json.loads(body)
            res = d.get("results", [])
            st.save(qid + suffix, offset, url, p, body, len(res), c)
            fetched += len(res)
            new += st.mark_new([r["key"] for r in res])
            if not res or d.get("endOfRecords"):
                break
            offset += 300
            time.sleep(0.15)
    st.log(qid, group, params, count, fetched, new, note, time.time() - t0)


def gbif_novelty(params):
    n = gbif_count(params)
    if n == 0:
        return 0, 0
    a = {"earliestPeriodOrLowestSystem": OSD}
    b = {"latestPeriodOrHighestSystem": OSD}
    na = gbif_count({**params, **a})
    nb = gbif_count({**params, **b})
    nab = gbif_count({**params, **a, **b})
    return n, n - (na + nb - nab)


def run_gbif(root, scope_csv, workers, smoke, only="all"):
    st = Store(root, "gbif")
    print("GBIF harvest dir", st.dir, flush=True)
    base = {"basisOfRecord": "FOSSIL_SPECIMEN"}
    scope = read_scope(scope_csv)
    tasks = []

    def primary(qid, extra, group):
        def f():
            p = {**base, **extra}
            gbif_page_all(st, qid, p, gbif_count(p), group)
        return f

    def secondary(qid, extra, group):
        def f():
            p = {**base, **extra}
            n, nov = gbif_novelty(p)
            if nov > 0:
                gbif_page_all(st, qid, p, n, group, note="novel_vs_period_queries=%d" % nov)
            else:
                st.log(qid, group, p, n, 0, 0, "skipped: every record is already in the period queries", 0.0)
        return f

    scopes = [("plantae", {"taxonKey": 6})] + [("kingdom%d" % k, {"kingdomKey": k}) for k in GBIF_OTHER_KINGDOMS]
    if smoke:
        scopes = scopes[:1]
    if only == "names":
        scopes = []
    pv = ["Silurian"] if smoke else OSD
    for sname, sp in scopes:
        tasks.append(primary("%s_earliest_period" % sname, {**sp, "earliestPeriodOrLowestSystem": pv}, "period"))
        tasks.append(primary("%s_latest_period" % sname, {**sp, "latestPeriodOrHighestSystem": pv}, "period"))
    sec = []
    for sname, sp in scopes:
        for lvl, vals in (("epoch", GBIF_EPOCH_VALUES), ("stage", GBIF_STAGE_VALUES)):
            for fld in GBIF_FIELDS[lvl]:
                for v in vals:
                    sec.append(secondary("%s_%s_%s" % (sname, fld, v), {**sp, fld: v}, lvl))
    for t in (GBIF_TEXT_TERMS if only != "names" else []):
        sec.append(secondary("plantae_q_%s" % t, {"taxonKey": 6, "q": t}, "text"))
    if smoke:
        sec = sec[:6]
    tasks.extend(sec)

    genera = []
    for r in scope:
        if r["role"] == "card_assemblage" or r["name_rank"] == "higher":
            continue
        g = r["genus"]
        if g and g not in genera:
            genera.append(g)
    if smoke:
        genera = ["Cooksonia", "Prototaxites"]
    matches = []
    BACKBONE = "d7dddbf4-2cf0-4f39-9b2a-bb099caae36c"
    for g in genera:
        url = GBIF + "/species?" + urllib.parse.urlencode({"name": g, "datasetKey": BACKBONE, "limit": 100})
        body = get(url)
        usages = json.loads(body).get("results", [])
        matches.append((g, usages))
        st.save("namelookup_%s" % g, 0, url, {"name": g, "datasetKey": BACKBONE}, body, len(usages), len(usages), subdir="namelookup")

        def name_task(g=g, usages=usages):
            p = {**base, "q": g}
            n = gbif_count(p)
            if n > NAME_CAP:
                for fld in ("earliestPeriodOrLowestSystem", "latestPeriodOrHighestSystem"):
                    pp = {**p, fld: OSD}
                    gbif_page_all(st, "name_%s_%s" % (g, fld[:3]), pp, gbif_count(pp), "name",
                                  note="capped: %d hits, restricted to window periods" % n)
            else:
                gbif_page_all(st, "name_%s_q" % g, p, n, "name")
            for u in usages:
                if u.get("kingdom") != "Animalia" and u.get("rank") in ("GENUS", "SPECIES") and u.get("key"):
                    p2 = {**base, "taxonKey": u["key"]}
                    n2 = gbif_count(p2)
                    if n2 <= NAME_CAP:
                        gbif_page_all(st, "name_%s_taxonKey%s" % (g, u["key"]), p2, n2, "name")
        tasks.append(name_task)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(t) for t in tasks]
        for f in futs:
            f.result()
    with open(os.path.join(st.dir, "name_matches.tsv"), "w", encoding="utf-8") as f:
        f.write("query_name\tusageKey\tscientificName\trank\ttaxonomicStatus\tkingdom\tphylum\tclass\torder\tfamily\tacceptedKey\n")
        for g, usages in matches:
            if not usages:
                f.write("\t".join([g] + [""] * 10) + "\n")
            for u in usages:
                f.write("\t".join([g] + [str(u.get(k, "")) for k in ("key", "scientificName", "rank", "taxonomicStatus", "kingdom",
                                                                   "phylum", "class", "order", "family", "acceptedKey")]) + "\n")
    print("done: %d unique records, %d files, %.0f MB, dir %s" % (len(st.seen), st.nfiles, st.nbytes / 1e6, st.dir), flush=True)


def run_gbif_datasets(hdir):
    keys = set()
    for fp in glob.glob(os.path.join(hdir, "*.json")):
        for r in json.load(open(fp)).get("results", []):
            keys.add(r["datasetKey"])
    st = Store(hdir, "gbif", stamp="x")
    orgs = {}
    for k in sorted(keys):
        url = GBIF + "/dataset/" + k
        body = get(url)
        st.save("dataset_%s" % k, 0, url, {"datasetKey": k}, body, 1, 1, subdir="datasets")
        d = json.loads(body)
        o = d.get("publishingOrganizationKey")
        if o and o not in orgs:
            url = GBIF + "/organization/" + o
            ob = get(url)
            st.save("organization_%s" % o, 0, url, {"organizationKey": o}, ob, 1, 1, subdir="datasets")
            orgs[o] = 1
        time.sleep(0.1)
    print("datasets %d organisations %d" % (len(keys), len(orgs)))


def run_gbif_verbatim(hdir, keyfile, workers=4):
    keys = [x.strip() for x in open(keyfile) if x.strip()]
    st = Store(hdir, "gbif", stamp="x")
    done = set(os.path.basename(p).split("__")[0] for p in glob.glob(os.path.join(hdir, "verbatim", "*.json")))

    def one(k):
        if "verbatim_%s" % k in done:
            return
        url = GBIF + "/occurrence/%s/verbatim" % k
        try:
            body = get(url)
        except urllib.error.HTTPError as e:
            st.log("verbatim_%s" % k, "verbatim", {"key": k}, 0, 0, 0, "HTTP %s" % e.code, 0.0)
            return
        st.save("verbatim_%s" % k, 0, url, {"gbifID": k}, body, 1, 1, subdir="verbatim")
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, keys))
    print("verbatim records requested: %d" % len(keys))


# ---------------------------------------------------------------- iDigBio

def idig_url(rq, limit, offset):
    return IDIG + "/search/records/?" + urllib.parse.urlencode(
        {"rq": json.dumps(rq, separators=(",", ":")), "limit": limit, "offset": offset, "sort": '[{"uuid":"asc"}]'})


def idig_page_all(st, qid, rq, group, note=""):
    t0 = time.time()
    fetched = new = 0
    offset = 0
    count = None
    while True:
        url = idig_url(rq, 1000, offset)
        body = get(url)
        d = json.loads(body)
        if count is None:
            count = d["itemCount"]
            if count > 100000:
                note += " truncated at offset 100000"
        items = d.get("items", [])
        st.save(qid, offset, url, rq, body, len(items), count)
        fetched += len(items)
        new += st.mark_new([it["uuid"] for it in items])
        offset += 1000
        if not items or offset >= min(count, 100000):
            break
        time.sleep(0.3)
    st.log(qid, group, rq, count, fetched, new, note, time.time() - t0)
    return count


def idig_count(rq):
    d = json.loads(get(IDIG + "/summary/count/records/?" + urllib.parse.urlencode({"rq": json.dumps(rq, separators=(",", ":"))})))
    return d["itemCount"]


def run_idigbio(root, scope_csv, smoke, only="all"):
    st = Store(root, "idigbio")
    print("iDigBio harvest dir", st.dir, flush=True)
    base = {"basisofrecord": "fossilspecimen"}
    scope = read_scope(scope_csv)

    def ft(v):
        return {"type": "fulltext", "value": v}
    terms = ["silurian"] if smoke else IDIG_TERMS
    if only == "names":
        terms = []
    for t in terms:
        idig_page_all(st, "plantae_ft_%s" % t, {**base, "kingdom": "plantae", "data": ft(t)}, "text")
    for t in terms[:3]:
        idig_page_all(st, "otherkingdoms_ft_%s" % t, {**base, "kingdom": IDIG_OTHER_KINGDOMS, "data": ft(t)}, "text")
        idig_page_all(st, "nokingdom_named_ft_%s" % t,
                      {**base, "kingdom": {"type": "missing"}, "scientificname": {"type": "exists"}, "data": ft(t)}, "text")
    names = []
    for r in scope:
        if r["role"] == "card_assemblage" or r["name_rank"] == "higher":
            continue
        if r["genus"] and r["genus"] not in names:
            names.append(r["genus"])
    if smoke:
        names = ["Cooksonia", "Prototaxites"]
    for g in names:
        rq = {**base, "scientificname": ft(g)}
        n = idig_count(rq)
        if n > NAME_CAP:
            for t in ("devonian", "silurian", "ordovician"):
                idig_page_all(st, "name_%s_%s" % (g, t), {**base, "scientificname": ft(g), "data": ft(t)}, "name",
                              note="capped: %d hits, restricted to window period words" % n)
        else:
            idig_page_all(st, "name_%s" % g, rq, "name")
    print("done: %d unique records, %d files, %.0f MB, dir %s" % (len(st.seen), st.nfiles, st.nbytes / 1e6, st.dir), flush=True)


def run_idigbio_media(hdir, uuidfile, workers=3):
    ids = [x.strip() for x in open(uuidfile) if x.strip()]
    st = Store(hdir, "idigbio", stamp="x")

    def one(u):
        url = IDIG + "/view/mediarecords/" + u
        try:
            body = get(url)
        except urllib.error.HTTPError as e:
            st.log("media_%s" % u, "media", {"uuid": u}, 0, 0, 0, "HTTP %s" % e.code, 0.0)
            return
        st.save("media_%s" % u, 0, url, {"uuid": u}, body, 1, 1, subdir="media")
        time.sleep(0.05)
    done = set(os.path.basename(p).split("__")[0] for p in glob.glob(os.path.join(hdir, "media", "*.json")))
    ids = [u for u in ids if "media_%s" % u not in done]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, ids))
    print("media records requested: %d" % len(ids))


def run_idigbio_recordsets(hdir):
    ids = set()
    for fp in glob.glob(os.path.join(hdir, "*.json")):
        for it in json.load(open(fp)).get("items", []):
            rs = it.get("indexTerms", {}).get("recordset")
            if rs:
                ids.add(rs)
    st = Store(hdir, "idigbio", stamp="x")
    for u in sorted(ids):
        url = IDIG + "/view/recordsets/" + u
        st.save("recordset_%s" % u, 0, url, {"uuid": u}, get(url), 1, 1, subdir="recordsets")
        time.sleep(0.2)
    print("recordsets: %d" % len(ids))


if __name__ == "__main__":
    a = sys.argv[1:]
    smoke = "--smoke" in a
    workers = 3
    if "--workers" in a:
        workers = int(a[a.index("--workers") + 1])
    pos = [x for i, x in enumerate(a) if not x.startswith("--") and (i == 0 or a[i - 1] not in ("--workers", "--only"))]
    mode = pos[0]
    only = a[a.index("--only") + 1] if "--only" in a else "all"
    if mode == "gbif":
        run_gbif(pos[1], pos[2], workers, smoke, only)
    elif mode == "idigbio":
        run_idigbio(pos[1], pos[2], smoke, only)
    elif mode == "gbif-datasets":
        run_gbif_datasets(pos[1])
    elif mode == "gbif-verbatim":
        run_gbif_verbatim(pos[1], pos[2], workers if "--workers" in a else 4)
    elif mode == "idigbio-media":
        run_idigbio_media(pos[1], pos[2], workers if "--workers" in a else 3)
    elif mode == "idigbio-recordsets":
        run_idigbio_recordsets(pos[1])
    else:
        sys.exit(__doc__)
