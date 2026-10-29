#!/usr/bin/env bash
# Fetch the BRIDGE annual-mean climatology file (<code>a.pdclann.nc, about 1.3 MB: land-surface fields
# including soil moisture, evaporation, runoff) for each HadCM3L run code, from the Bristol BRIDGE site.
# Used for the land-sea mask (soil-moisture footprint) and as an independent check on the Zenodo files.
# The site states no licence and no login is required; see climate/README.md.
# Run ON nectar:  ssh nectar 'bash -s -- teXPt teXPs ...' < climate_fetch_bristol_pdclann.sh
set -euo pipefail

RAW=/data/codex/silurian_plants/raw/hadcm3l
UA="Mozilla/5.0 (compatible; research-data-fetch)"
BASE=https://www.paleo.bristol.ac.uk/ummodel/data
OUT="$RAW/bristol_pdclann"
mkdir -p "$OUT"
cd "$RAW"
PROV=PROVENANCE.tsv
[ -f "$PROV" ] || printf 'file\turl\tfetched_utc\tbytes\tmd5\tsha256\tmd5_zenodo\tmd5_match\n' > "$PROV"

for code in "$@"; do
  name="${code}a.pdclann.nc"
  url="$BASE/$code/climate/$name"
  f="$OUT/$name"
  if [ ! -s "$f" ]; then
    curl -sS -L -A "$UA" --retry 3 -o "$f" "$url"
    sleep 1
  fi
  head -c 3 "$f" | grep -q -E 'CDF|HDF' || { echo "$name is not netCDF" >&2; exit 1; }
  sha=$(sha256sum "$f" | cut -d' ' -f1)
  if ! grep -q -P "\t$sha\t" "$PROV"; then
    printf 'bristol_pdclann/%s\t%s\t%s\t%s\t%s\t%s\tn/a\tn/a\n' "$name" "$url" "$(date -u +%FT%TZ)" "$(stat -c %s "$f")" "$(md5sum "$f" | cut -d' ' -f1)" "$sha" >> "$PROV"
  fi
  echo "$name $(stat -c %s "$f")"
done
