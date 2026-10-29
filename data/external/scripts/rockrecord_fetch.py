"""rockrecord_fetch.py: fetch the open BGS DiGMapGB-625 bedrock geology download and its catalogue records.

Run on nectar (stdlib only):  ssh nectar python3 - < rockrecord_fetch.py
Writes to /data/codex/silurian_plants/raw/bgs/<UTC stamp>/ : the Shapefile and GeoPackage zips, the BGS dataset
page and the NERC catalogue record (licence and version evidence), and PROVENANCE.tsv (URL, timestamp, licence,
bytes, sha256). Plain user agent, no credentials: BGS's 'free download' links are tokenised GET links on the
public download pages. DiGMapGB-50 is not fetched (not openly licensed).
"""
import datetime
import hashlib
import os
import re
import sys
import urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) research-data-fetch"
STAMP = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H%MZ")
OUT = f"/data/codex/silurian_plants/raw/bgs/{STAMP}/"
os.makedirs(OUT, exist_ok=True)
LICENCE = ("Open Government Licence (BGS licence page links v3; the DOI landing page links v2); acknowledgement wording differs: BGS page "
           "'Contains British Geological Survey materials (c) UKRI [year]', NERC record 'Contains NERC materials (c)NERC [year]'")
rows = []


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read(), r.headers.get("Content-Type", ""), r.geturl()


def save(name, url, note, licence=LICENCE):
    data, ctype, final = get(url)
    with open(OUT + name, "wb") as f:
        f.write(data)
    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rows.append([name, url, ts, licence, str(len(data)), hashlib.sha256(data).hexdigest(), note])
    print(name, len(data), ctype, file=sys.stderr)
    return data


def download_page(name_zip, page_url, note):
    page = save(name_zip.replace(".zip", "_page.html"), page_url, "BGS download page (version, size and dates)")
    m = re.search(r"(https://www\.bgs\.ac\.uk/download/[^\"'\s]+\?wpdmdl=\d+&(?:amp;|#038;)?refresh=\w+)", page.decode("utf-8", "replace"))
    assert m, page_url
    link = m.group(1).replace("&amp;", "&").replace("&#038;", "&")
    save(name_zip, link, note + " (tokenised download link of " + page_url + ")")


save("bgs-geology-625k_dataset_page.html", "https://www.bgs.ac.uk/datasets/bgs-geology-625k-digmapgb/",
     "BGS dataset page: licence, formats, links")
save("bgs-geology-50k_dataset_page.html", "https://www.bgs.ac.uk/datasets/bgs-geology-50k-digmapgb/",
     "BGS dataset page for DiGMapGB-50 (not downloaded: not openly licensed); evidence for the access limit", licence="not openly licensed; see page")
save("nerc_catalogue_record_9df8df52.xml",
     "https://data-search.nerc.ac.uk/geonetwork/srv/api/records/9df8df52-d788-37a8-e044-0003ba9b0d98/formatters/xml",
     "NERC catalogue ISO 19139 record for DiGMapGB-625 (2008), licence and constraint wording")
save("bgs_cited_data_d9c6923b.html",
     "https://www2.bgs.ac.uk/nationalgeosciencedatacentre/citedData/catalogue/d9c6923b-a339-48f7-b1cf-5c9bbb664ef5.html",
     "BGS cited-data page for DOI 10.5285/d9c6923b-a339-48f7-b1cf-5c9bbb664ef5 (DiGMapGB-625 2008)")
download_page("bgs_geology_625k_shapefile.zip",
              "https://www.bgs.ac.uk/download/bgs-geology-625k-gis-line-and-polygon-data-shapefile-format/",
              "BGS Geology 625k, GIS line and polygon data, Shapefile (page says 16.49 MB, updated 06/10/2025)")
download_page("bgs_geology_625k_geopackage.zip",
              "https://www.bgs.ac.uk/download/bgs-geology-625k-bedrock/",
              "BGS Geology 625k, GIS line and polygon data, GeoPackage link on the dataset page (page says 15.91 MB, updated 05/12/2024)")

with open(OUT + "PROVENANCE.tsv", "w") as f:
    f.write("file\turl\tretrieved_utc\tlicence\tbytes\tsha256\tnote\n")
    for r in rows:
        f.write("\t".join(r) + "\n")
print(OUT)
