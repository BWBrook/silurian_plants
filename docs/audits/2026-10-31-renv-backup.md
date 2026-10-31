# renv cache-link backup repair and verified rerun — 31 October 2026

Barry authorised updating the backup script for renv symlinks while keeping existing
safeguards and snapshot retention, then rerunning and verifying the real backup.
Only `tools/backup_nectar.py`, its tests and backup documentation were owned by this
session. Concurrent scientific edits were preserved and were not committed by it.

## Change and scope

The script accepts only package-entry links under a project's renv library whose
literal absolute targets match the mini's known renv cache layout and the regular
project lockfile's package/version (and its hash where present). The current checkout
has 31 such links. Link identities and targets are recorded separately from file bytes;
all other symlinks and special files remain blocked. No manifest file or directory can
descend through an accepted package link. Existing protected-path, credential/database,
Git lock, source-drift, inherited-inode, capacity and promotion guards remain.

Inventory, payload hashing and restore input reads use descriptor-relative no-follow
operations so a concurrent directory-to-link replacement cannot redirect those reads
into the cache. Sealing uses file/directory descriptors, checks and skips only recorded
links, and avoids chmod on already read-only shared inodes. Each generation recreates
its own links; only unchanged regular files share read-only hardlinks with predecessors.
The sample restore includes every package link and its lockfile. macOS and Linux link
permission bits are not compared; destination-local link identities still detect replacement.

The backup stores **literal links and the lockfile, not external package-cache bytes**.
Those bytes were never part of the checkout. Restoring on a machine without that Mac
cache requires `renv::restore()` in the corresponding analysis directory. The backup
does not guarantee future availability of external package sources. Existing retained
manifests without link fields continue to verify/restore as link-free generations;
this is necessary for retention and recovery, not a rewrite of their recorded history.

## Checks

All 28 offline regression tests pass. New coverage includes live and dangling approved
links, disallowed targets and missing/mismatched locks, source directory/link replacement,
no-follow reads, cache-permission preservation, restored link targets and locks, corrupt
older links during a scrub, malformed manifest descendants and sealing read-only shared
inodes. Existing incremental, corruption, source-identity, lock, seven-day scrub and
retention tests also pass. An independent code review found and checked repairs to
restore/sealing/inventory races, no-op shared-inode chmod and exception handling; its
final SHA-pinned receipt has no outstanding material findings.

## Production result

The first run stopped safely on concurrent scientific-output/Git-object changes during
hashing. Its local and remote failed staging were retained. After a brief pause, the
second run captured a stable source and completed normally. Source-before and source-after
inventories are identical. The successful local capture was removed, with receipts retained.

- Generation: `20261031T003729.813012Z`, containing backup code commit `e86a56f`.
- Files: **7,155**, totalling **6,847,551,589 bytes**.
- Freshly checksummed/transferred: **1,645 files / 1,623,842,255 bytes**.
- Inherited with matching source metadata and prior destination identities: **5,510 files**.
- Package symlinks: **31 literal targets verified**, with cache payload explicitly not captured.
- Git HEAD matches the capture; `git fsck` succeeds.
- Sample restore: **28 regular files / 18,695,575 bytes**, plus **all 31 links** and their
  matching project lockfile; all reported checksums/targets match.
- `latest` points to `snapshots/20261031T003729.813012Z/project`; the completed generation
  is sealed read-only. Independent remote metadata, identity and restore checks pass.
- All **six previous completed generations** remain (seven total), and the failed
  `20261031T003625.519491Z.partial` remains. All pre-existing local stage directories remain.
- This was a daily incremental run. The weekly scrub was not due; its successful marker
  remains `20261028T235736.413753Z`, with no pending scrub. No retention or schedule changes.

The transfer took about 705 seconds; publication/verification took about 78 seconds.
The complete local run took about 822 seconds. Full retained-byte scrubbing was not
rerun unnecessarily; its successful/failure paths, including link integrity and an
unchanged success marker after failure, remain covered by the regression tests.

Evidence: `work/codex/backups/2026-10-31-renv-symlinks.json`, plus the retained local
stage's `result.json` and the generation's sealed manifests/verification/restore receipt
at `nectar:/data/codex/silurian_plants/backups/mac-mini/`. This audit and receipt were
created after the verified capture and are retained in Git for subsequent backups.

The existing daily-incremental/weekly-scrub structure serves the next backup. The
exposed assumption was that an ignored package library can contain legitimate links
outside the checkout: preserving link identity and a rebuild recipe is distinct from
archiving the external cache. No scientific input, interpretation or question status changed.
