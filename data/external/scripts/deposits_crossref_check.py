#!/usr/bin/env python3
"""Verify the target works' DOIs against Crossref and write deposits/crossref_check.tsv.

Usage: python3 deposits_crossref_check.py OUT.tsv
Plain user agent, no contact address; requests are paced to stay inside the public rate limit.
"""
import csv, json, sys, time, urllib.error, urllib.request

UA = "Mozilla/5.0 (X11; Linux x86_64) research-fetch"

TARGETS = [
    ("capel2021", "10.1016/j.palaeo.2020.110170", "Capel et al. 2021"),
    ("capel2022", "10.1016/j.earscirev.2022.104085", "Capel et al. 2022"),
    ("capel2023", "10.1111/pala.12644", "Capel et al. 2023"),
    ("cascales2016", "10.1016/j.revpalbo.2015.10.005", "Cascales-Miñana 2016"),
    ("xiong2013", "10.1371/journal.pone.0075706", "Xiong et al. 2013"),
    ("silvestro2015", "10.1111/nph.13247", "Silvestro et al. 2015"),
    ("kenrick1997", "10.1038/37918", "Kenrick & Crane 1997"),
    ("toledo2021", "10.1111/nph.17511", "Toledo et al. 2021"),
    ("clark2023", "10.1038/s41477-023-01513-x", "Clark et al. 2023"),
    ("claisse2025", "10.1093/aob/mcaf146", "Claisse et al. 2025"),
    ("hooper2026", "10.1038/s41477-026-02432-3", "Hooper et al. 2026"),
    ("morris2018", "10.1073/pnas.1719588115", "Morris et al. 2018"),
    ("harris2022", "10.1038/s41559-022-01885-x", "Harris et al. 2022"),
    ("foster2017", "10.1038/ncomms14845", "Foster et al. 2017"),
    ("dahl2022", "10.1038/s41467-022-35085-9", "Dahl et al. 2022"),
    ("witkowski2018", "10.1126/sciadv.aat4556", "Witkowski et al. 2018"),
    ("lenton2016", "10.1073/pnas.1604787113", "Lenton et al. 2016"),
    ("krause2018", "10.1038/s41467-018-06383-y", "Krause et al. 2018"),
    ("glasspool2010", "10.1038/ngeo923", "Glasspool & Scott 2010"),
    ("haq2008", "10.1126/science.1161648", "Haq & Schutter 2008"),
    ("yuan2023", "10.1126/sciadv.ade9510", "Yuan et al. 2023"),
    ("avila2025", "10.1144/jgs2023-148", "Avila et al. 2025"),
    ("cai2026", "10.1038/s41559-026-02995-6", "Cai et al. 2026"),
    ("wu2026", "10.1029/2025jf009085", "Wu et al. 2026"),
    ("shu2025", "10.5194/essd-17-3567-2025", "Shu et al. 2025 (coordinator addition)"),
    ("veizer1999", "10.1016/s0009-2541(99)00081-9", "Veizer et al. 1999 (related)"),
    ("prokoph2008", "10.1016/j.earscirev.2007.12.003", "Prokoph et al. 2008 (related)"),
    ("veizer2015", "10.1016/j.earscirev.2015.03.008", "Veizer & Prokoph 2015 (related)"),
    ("mcarthur2001", "10.1086/319243", "McArthur et al. 2001 (related)"),
    ("capel2025", "10.1080/08912963.2025.2568087", "Capel et al. 2025 (related)"),
    ("grossman2022", "10.1038/s41598-022-11493-1", "Grossman & Joachimski 2022 (related)"),
    ("vandermeer2025", "10.1016/j.epsl.2025.119526", "van der Meer et al. 2025 (related)"),
]

def fetch(doi):
    url = "https://api.crossref.org/works/" + doi
    for attempt in range(6):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40))["message"]
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(doi)

def main(out):
    rows = []
    for key, doi, label in TARGETS:
        m = fetch(doi)
        if m is None:
            rows.append([key, label, doi, "NOT FOUND", "", "", "", "", ""])
        else:
            issued = (m.get("issued", {}).get("date-parts") or [[""]])[0][0]
            au = (m.get("author") or [{}])[0].get("family", "")
            lic = ";".join(sorted({l.get("URL", "") for l in m.get("license", [])}))
            rows.append([key, label, m["DOI"], " ".join((m.get("title") or [""])[0].split()), au, issued,
                         " ".join((m.get("container-title") or [""])[0].split()), m.get("publisher", ""), lic])
        time.sleep(1.5)
    with open(out, "w", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["key", "label", "doi_crossref", "title", "first_author", "year", "container", "publisher", "licence_urls"])
        w.writerows(rows)

if __name__ == "__main__":
    main(sys.argv[1])
