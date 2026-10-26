#!/usr/bin/env bash
# Full silurian_plants library extraction. Run from data/eprp/scripts/ on a machine that can reach deep-server.
# Stage 1-2 run on deep-server (reads /data/paleodata/library, writes only to scratch); stage 3 runs locally.
set -euo pipefail
cd "$(dirname "$0")"
ROOT=$(cd .. && pwd)
PROJECT=$(cd ../../.. && pwd)
EPRP=${EPRP:-$HOME/git/eprp}
REMOTE=${REMOTE:-deep-server}
RDIR=${RDIR:-/data/codex/silurian_plants-eprp/library}
WORK=$ROOT/local/library/work

ssh -o BatchMode=yes "$REMOTE" "mkdir -p $RDIR"
scp -q "$EPRP/resources/library/works.tsv" library_features.py library_queries.py library_candidates.py "$REMOTE:$RDIR/"
ssh -o BatchMode=yes "$REMOTE" "cd $RDIR && python3 library_features.py --works works.tsv --out features.jsonl \
  && python3 library_candidates.py --features features.jsonl --out candidates.tsv --fts-out fts_hits.tsv --workers 16 2> cand.log"
mkdir -p "$WORK" "$ROOT/library" "$ROOT/local/library/text"
scp -q "$REMOTE:$RDIR/candidates.tsv" "$REMOTE:$RDIR/fts_hits.tsv" "$WORK/"

ASSEMBLE=(python3 library_assemble.py --works "$EPRP/resources/library/works.tsv" --candidates "$WORK/candidates.tsv" \
  --fts "$WORK/fts_hits.tsv" --decisions library_decisions.tsv --project "$PROJECT" --read library_screen_read.txt \
  --out "$ROOT/library" --work "$WORK")
"${ASSEMBLE[@]}"
rsync -a --files-from="$WORK/texts_to_copy.txt" "$REMOTE:/data/paleodata/library/text/" "$ROOT/local/library/text/"
"${ASSEMBLE[@]}" --texts-dir "$ROOT/local/library/text"
python3 library_manifest.py
