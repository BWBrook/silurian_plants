#!/usr/bin/env bash
# Fetch PhanDA HadCM3L priors (Zenodo 8237751, CC BY 4.0) files to nectar raw scratch,
# verify md5 against the Zenodo record, and log provenance.
# Run ON nectar:  ssh nectar 'bash -s' < climate_fetch_hadcm3l.sh [file ...]
# Default files: ExperimentInfo.xlsx scotese_02_tas.zip scotese_02_pr.zip
set -euo pipefail

RAW=/data/codex/silurian_plants/raw/hadcm3l
REC=8237751
UA="Mozilla/5.0 (compatible; research-data-fetch)"
SEGMENTS=4
FILES=("$@")
[ ${#FILES[@]} -gt 0 ] || FILES=(ExperimentInfo.xlsx scotese_02_tas.zip scotese_02_pr.zip)

mkdir -p "$RAW"
cd "$RAW"
PROV=PROVENANCE.tsv
[ -f "$PROV" ] || printf 'file\turl\tfetched_utc\tbytes\tmd5\tsha256\tmd5_zenodo\tmd5_match\n' > "$PROV"

curl -sS -A "$UA" "https://zenodo.org/api/records/$REC" -o record.json
meta() { python3 - "$1" <<'PY'
import json, sys
d = json.load(open('record.json'))
f = {x['key']: x for x in d['files']}[sys.argv[1]]
print(f['size'], f['checksum'].split(':', 1)[1])
PY
}

for name in "${FILES[@]}"; do
  read -r size md5_expected < <(meta "$name")
  url="https://zenodo.org/api/records/$REC/files/$name/content"
  if [ -f "$name" ] && [ "$(md5sum "$name" | cut -d' ' -f1)" = "$md5_expected" ]; then
    echo "$name: present, md5 ok"
  else
    rm -f "$name" "$name".part*
    echo "$name: downloading $size bytes in $SEGMENTS segments"
    seg=$(( (size + SEGMENTS - 1) / SEGMENTS ))
    pids=()
    for i in $(seq 0 $((SEGMENTS - 1))); do
      a=$(( i * seg )); b=$(( a + seg - 1 )); [ $b -ge $size ] && b=$(( size - 1 ))
      curl -sS -L -A "$UA" -r "$a-$b" --retry 5 --retry-delay 10 -o "$name.part$i" "$url" &
      pids+=($!)
    done
    for p in "${pids[@]}"; do wait "$p"; done
    cat "$name".part* > "$name"
    rm -f "$name".part*
  fi
  got=$(stat -c %s "$name")
  md5=$(md5sum "$name" | cut -d' ' -f1)
  sha=$(sha256sum "$name" | cut -d' ' -f1)
  [ "$md5" = "$md5_expected" ] && ok=yes || ok=NO
  if ! grep -q -P "^$name\t.*\t$sha\t" "$PROV"; then
    printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n' "$name" "$url" "$(date -u +%FT%TZ)" "$got" "$md5" "$sha" "$md5_expected" "$ok" >> "$PROV"
  fi
  echo "$name: bytes=$got md5=$md5 expected=$md5_expected match=$ok"
  [ "$ok" = yes ] || { echo "MD5 MISMATCH for $name" >&2; exit 1; }
done
