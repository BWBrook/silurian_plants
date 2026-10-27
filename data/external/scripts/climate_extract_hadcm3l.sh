#!/usr/bin/env bash
# Extract the 485-383 Ma slices (ExperimentInfo experiment numbers 012-032, five 20-yr means each)
# of one PhanDA HadCM3L suite from the verified Zenodo zips, byte-identical, and write sha256 sums.
# Run ON deep-server:  ssh deep-server 'bash -s' < climate_extract_hadcm3l.sh [experiment]
# Default experiment: scotese_02. Output: $RAW/extracted/<experiment>/ and SHA256SUMS in it.
set -euo pipefail

EXP="${1:-scotese_02}"
RAW=/data/codex/silurian_plants/raw/hadcm3l
OUT="$RAW/extracted/$EXP"
FIRST=12   # experiment number 12: Experiment Age 485.4 Ma, plate age 485 Ma
LAST=32    # experiment number 32: Experiment Age 385.2 Ma, plate age 385 Ma

mkdir -p "$OUT"
cd "$RAW"
for var in tas pr; do
  zip="${EXP}_${var}.zip"
  grep -q -P "^$zip\t.*\tyes$" PROVENANCE.tsv || { echo "$zip not verified in PROVENANCE.tsv" >&2; exit 1; }
  members=$(unzip -Z1 "$zip" | awk -v f=$FIRST -v l=$LAST -F_ '{ n=$3+0; if (n>=f && n<=l) print }' | sort)
  [ "$(echo "$members" | wc -l)" -eq $(( (LAST - FIRST + 1) * 5 )) ] || { echo "unexpected member count for $zip" >&2; exit 1; }
  # shellcheck disable=SC2086
  echo "$members" | xargs unzip -o -q "$zip" -d "$OUT"
done
cd "$OUT"
ls | grep '\.nc$' | sort | xargs sha256sum > SHA256SUMS
echo "extracted $(ls | grep -c '\.nc$') files, $(du -sh . | cut -f1)"
