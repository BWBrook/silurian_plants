"""rockrecord_bgs_polygons.py: unpack the BGS DiGMapGB-625 (V5.17) bedrock polygons, add area and centroid, and select the
Silurian-Devonian polygons on BGS's own age fields.

Run on deep-server after rockrecord_fetch.py (stdlib + the GDAL command-line tools):
    ssh deep-server python3 - < rockrecord_bgs_polygons.py
Reads the newest /data/codex/silurian_plants/raw/bgs/<stamp>/ (shapefile and GeoPackage zips); writes to <stamp>/derived/ :
  bedrock_shapefile_epsg27700.gpkg    the shapefile bedrock layer re-written to GeoPackage with EPSG:27700 assigned (the .prj has no EPSG code); intermediate
  bedrock_polygons.csv                all 11,244 bedrock polygons: every source attribute (unchanged) + area_m2 (planar, EPSG:27700)
                                      + centroid_lon / centroid_lat (EPSG:4326)
  bgs_625k_bedrock_silurian_devonian.gpkg   the polygons that overlap Silurian-Devonian on BGS's own years (below), geometry and
                                      all attributes, EPSG:27700 (local only: vector)
  sd_lex_codes.txt                    LEX codes of those polygons plus the Old Red Sandstone codes named in the polygon attributes
  checks.txt                          shapefile vs GeoPackage agreement and counts

BGS's polygon age fields (MAX_TIME_Y / MIN_TIME_Y, in years) are on BGS's own scale (2008 edition): they are not converted.
Selection: MAX_TIME_Y > 354,000,000 and MIN_TIME_Y < 443,000,000, i.e. the polygon's age range overlaps BGS's own Devonian top
(354 Ma) to Silurian base (443 Ma), read from the terms' values in the data (see the README).
"""
import csv
import glob
import os
import subprocess
import sys
import zipfile
import collections

csv.field_size_limit(1 << 30)
RAWS = sorted(glob.glob("/data/codex/silurian_plants/raw/bgs/*/bgs_geology_625k_shapefile.zip"))
RAW = os.path.dirname(RAWS[-1]) + "/"
DER = RAW + "derived/"
os.makedirs(DER, exist_ok=True)
SD_TOP_Y, SD_BASE_Y = 354_000_000, 443_000_000
CHK = open(DER + "checks.txt", "w")


def log(*a):
    print(*a, file=sys.stderr, flush=True)
    print(*a, file=CHK, flush=True)


for z, d in (("bgs_geology_625k_shapefile.zip", "x_shp"), ("bgs_geology_625k_geopackage.zip", "x_gpkg")):
    if not os.path.isdir(RAW + d):
        zipfile.ZipFile(RAW + z).extractall(RAW + d)
SHP = RAW + "x_shp/BGS_Geology_625k_Shapefile/Bedrock/625k_V5_BEDROCK_Geology_Polygons.shp"
GPKG = RAW + "x_gpkg/625k_V5_Geology_UK_EPSG27700.gpkg"
log("raw dir", RAW)

SHP27700 = DER + "bedrock_shapefile_epsg27700.gpkg"
if os.path.exists(SHP27700):
    os.remove(SHP27700)
subprocess.run(["ogr2ogr", "-f", "GPKG", SHP27700, SHP, "-nln", "bedrock", "-nlt", "PROMOTE_TO_MULTI", "-a_srs", "EPSG:27700"], check=True)
SQL = ('SELECT *, ST_Area(geom) AS area_m2, ST_X(ST_Transform(ST_Centroid(geom), 4326)) AS centroid_lon, '
       'ST_Y(ST_Transform(ST_Centroid(geom), 4326)) AS centroid_lat FROM bedrock')
out = DER + "bedrock_polygons.csv"
if os.path.exists(out):
    os.remove(out)
subprocess.run(["ogr2ogr", "-f", "CSV", out, SHP27700, "-dialect", "SQLite", "-sql", SQL], check=True)
rows = list(csv.DictReader(open(out, newline="", encoding="utf-8")))
log("bedrock polygons", len(rows), "total area km2", round(sum(float(r["area_m2"]) for r in rows) / 1e6, 3))

# shapefile vs GeoPackage: same polygons?
tmp = DER + "gpkg_check.csv"
if os.path.exists(tmp):
    os.remove(tmp)
subprocess.run(["ogr2ogr", "-f", "CSV", tmp, GPKG, "-dialect", "SQLite", "-sql",
                'SELECT LEX, LEX_D, RCS, MAX_TIME_Y, MIN_TIME_Y, MAX_TIME_D, MIN_TIME_D, ST_Area(geom) AS area_m2 FROM "625k_V5_BEDROCK_Geology"'],
               check=True)
g = list(csv.DictReader(open(tmp, newline="", encoding="utf-8")))
os.remove(tmp)
key = lambda r: (r["LEX"], r["RCS"], r["MAX_TIME_D"], r["MIN_TIME_D"], r["MAX_TIME_Y"], r["MIN_TIME_Y"])
a1, a2 = collections.defaultdict(float), collections.defaultdict(float)
n1, n2 = collections.Counter(), collections.Counter()
for r in rows:
    a1[key(r)] += float(r["area_m2"])
    n1[key(r)] += 1
for r in g:
    a2[key(r)] += float(r["area_m2"])
    n2[key(r)] += 1
bad = [k for k in set(a1) | set(a2) if n1[k] != n2[k] or abs(a1[k] - a2[k]) > 1.0]
log("GeoPackage polygons", len(g), "groups differing from the shapefile (count or area > 1 m2):", len(bad))


def sd(r):
    a, b = r["MAX_TIME_Y"], r["MIN_TIME_Y"]
    return bool(a) and bool(b) and int(a) > SD_TOP_Y and int(b) < SD_BASE_Y


S = [r for r in rows if sd(r)]
log("Silurian-Devonian polygons on BGS years", len(S), "area km2", round(sum(float(r["area_m2"]) for r in S) / 1e6, 3))
gp = DER + "bgs_625k_bedrock_silurian_devonian.gpkg"
if os.path.exists(gp):
    os.remove(gp)
subprocess.run(["ogr2ogr", "-f", "GPKG", gp, SHP27700, "-nln", "bgs_625k_bedrock_silurian_devonian", "-nlt", "PROMOTE_TO_MULTI",
                "-where", f"MAX_TIME_Y > {SD_TOP_Y} AND MIN_TIME_Y < {SD_BASE_Y}"], check=True)
info = subprocess.run(["ogrinfo", "-so", gp, "bgs_625k_bedrock_silurian_devonian"], capture_output=True, text=True).stdout
log([l for l in info.splitlines() if "Feature Count" in l][0])

codes = {r["LEX"] for r in S}
ors = {r["LEX"] for r in rows if "OLD RED SANDSTONE" in r["LEX_D"] or r["SUPGP_EQ"] == "ORS" or "OLD RED SANDSTONE" in r["PREV_NAME"]
       or r["LEX"] == "ORS"}
log("S-D LEX codes", len(codes), "ORS-labelled codes in all bedrock polygons", sorted(ors))
with open(DER + "sd_lex_codes.txt", "w") as f:
    for c in sorted(codes | ors | {"ORS"}):
        f.write(c + "\n")
log("wrote", DER)
