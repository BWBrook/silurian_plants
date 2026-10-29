# Continue Silurian Plants literature access with Barry on the MacBook

This is a handoff from the Codex literature-sourcing session on `mini`, prepared
30 October 2026 (Australia/Hobart). Barry is working on the MacBook at the office
because screen sharing to the mini is unavailable. He requested this package and a
detailed prompt so a counterpart Codex agent can continue with him. **Act on this
prompt: orient briefly, then work through the remaining access cases with Barry.**
Do not begin scientific extraction, taxon-card changes, modelling or methods review.

## Start here

1. Read the MacBook's current `~/.codex/AGENTS.md`. Before remote work, read its
   `~/work/nectar/README.md`, `docs/workflows/cross-machine-access.md`,
   `docs/decisions.md` and `docs/exchange/current_status.md`. Current local guidance
   supersedes older route descriptions in copied historical notes.
2. This package should be at
   `/Users/bwbrook/input/silurian-plants-literature-2026-10-30/`.
   Read `docs/barry-to-action.md` (current Tier 2 section first, then Tier 1),
   `docs/literature-requests.md`, and the two acquisition audits under `docs/audits/`.
3. `blocked-first-study.csv` is the machine-readable **48-row current focal queue**:
   16 Tier 1 and 32 Tier 2 unresolved/incomplete rows. It combines the live focused
   statuses with citations, DOIs, question IDs, links and observed blockers. These are
   not all proven unobtainable: several need only a save or human sign-in/terms step.
4. `docs/first-study-literature.csv` is the original 135-row prioritisation input,
   unchanged. `docs/first-study-literature-status.csv` records all current outcomes.
   `docs/closed-literature.csv` is the wider 565-row master, included for context;
   **do not treat its hundreds of background gaps as this task's queue**.
5. Inspect any existing MacBook checkout at `/Users/bwbrook/papers/silurian_plants`
   before relying on it. Read its applicable AGENTS. The source mini checkout for this
   package is commit `2d16b95920b3d874544e23788855b98d5a771650` on `main`, pushed to GitHub. If a clean local
   checkout needs updating, use the normal fetch/fast-forward-only workflow. Do not
   reset dirty work. A Git checkout does not contain the ignored PDF library.

## Current result and scope

Tier 1: 58 rows, 40 main-held (including one duplicate), two complete abstracts,
one partial and 15 blocked. The pass secured 39 new main texts and ten new supporting
files. Tier 2: 77 attempted rows, 30 new main texts plus twelve exact prior works
reconciled (42 main-held), two abstracts, one already-held data archive, one partial,
one supplement-only and 30 blocked. Tier 2 filed 92 asset entries, including copies
of existing datasets; that is not 92 new papers. The 48-row queue is the 16+32
unresolved/incomplete subset. Earlier ancillary cases remain in the ledgers for
context; the two explicitly still-parked sources (`al2008f`, `al2012g`) stay parked.

Barry has already authorised routine public/institutional retrieval, filing and
provenance checking. He is now available to perform sign-ins, explicit terms actions
and browser challenges himself. No library/author request, message to another person,
purchase, new account or explicit terms acceptance has been submitted on his behalf.
If such a step is useful, present the exact page and let Barry decide/take it. Never
bypass an access control or security challenge. Never submit Barry's email or other
personal data to a service/API. No Sci-Hub or equivalent access route.

## Suggested working order

Start with six Tier 2 quick actions, one tab at a time:

| ID | Route and what has already worked |
|---|---|
| `rubinstein2016` | UTAS ScienceDirect full text and 12-page PDF opened. Automated download timed out; mini's native save was unavailable while locked. Open https://www-sciencedirect-com.ezproxy.utas.edu.au/science/article/pii/S0034666715001268 and save the original PDF using the MacBook's unlocked browser. |
| `strother2016` | UTAS full text and View Open Manuscript appeared. Save was blocked/stalled on locked mini. https://www-sciencedirect-com.ezproxy.utas.edu.au/science/article/pii/S0034666715001931 |
| `wang2022` | UTAS full text and inline PDF opened. Main save remains; original supporting spreadsheet is already held on mini, so do not count that supplement as new. https://www-sciencedirect-com.ezproxy.utas.edu.au/science/article/pii/S0034666722000434 |
| `al2018d` | Tomescu 2018 bryophyte-taphonomy chapter full text was accessible through UTAS; View PDF download stalled. https://www-sciencedirect-com.ezproxy.utas.edu.au/science/chapter/edited-volume/pii/B9780128130124000164 |
| `edwardsrichardson2004` | Wiley Free Access HTML; Chrome PDF reader loaded all 28 pages, but its Download PDF request timed out. https://onlinelibrary-wiley-com.ezproxy.utas.edu.au/doi/full/10.1002/gj.997 |
| `hoffmeister1959` | UTAS JSTOR access confirmed. Download opens explicit Accept and download terms; Barry must click it. Dialog was cancelled on mini. https://www-jstor-org.ezproxy.utas.edu.au/stable/1484424 |

Then prioritise Tier 1 human-action cases:

- `ottone1999`: confirmed UTAS JSTOR access; Barry's Accept and download step remains.
- `al2011f`, `al2012c`, `morris2012`: exact Academia author-copy leads, with sign-in/
  explicit terms or target-download verification needed. Use exact ledger links; the
  2012 Ficoiditheca paper already held is not the Further insights paper.
- `zalesie-dating`: Trela & Szczepanik 2009 public PGI PDF, native-save/verification
  issue on locked mini. Exact route:
  https://www.pgi.gov.pl/images/stories/przeglad/pg_2009_02_21.pdf . Masiak 2003 is a
  separately held 19-page component, printed pp.311–329; cited p.330 is still unverified.
  Do not close this combined row merely because one component is held.
- `earp2024-open`: open CSIRO/ConnectSci target met browser security verification.
- `delapuente2013`, `rubinstein2011`, `al2023b`: CONICET author copies were indexed but
  repository requests timed out from mini; a fresh MacBook/network route may work.
- The remaining Tier 1 subscription, thesis and older-report cases are itemised in
  the ledger. Garratt 1978 is still missing; later papers/maps are explicitly
  non-equivalent surrogates. Keep that distinction.

After those, work the Tier 2 browser/access checks. `lakova1992`, `cesari2019` and
`cardona2016` hit security/delivery blocks. `al2016h`, `careybolger1995` and
`eggert1974` still need target entitlement established. A site recognising UTAS does
not establish access to the article. The Full Access badge seen beside Carey–Bolger
and Garratt belonged to related articles. Eggert has JSTOR alternative 2441808.
Bulls Head (`al2014c`) now has explicit JSTOR no-institutional-access evidence,
superseding its earlier browser-only diagnosis. The twenty Tier 2 library/archive
candidates are separated in `docs/literature-requests.md`; do not let requests stall
ordinary save/login successes. Let Barry choose when to tackle their real-world forms.

## Browser and download workflow

Use the in-app browser first where available, Chrome as fallback, unless Barry chooses
Chrome for a joint diagnosis. Inspect the available CUA/browser tool documentation at
initialisation; do not assume an old API or a session/cookie from mini exists here.
A fresh general UTAS library sign-in helped on mini; Barry can do it on the MacBook.
Keep one target, or at most a very small number of active targets, open at a time.
**Close each successful or failed acquisition tab after recording the outcome.**
Preserve user-owned unrelated tabs. If action cannot happen now, log the blocker and
close it, then move on. No repeated unchanged failing retries or unattended tab pile-up.

Proven route details, not guarantees:

- ScienceDirect in-app full text can work even when downloadMedia or an immediate
  transfer of its signed asset URL fails (403). On mini, native browser save needed
  an unlocked desktop. Do not infer a subscription gap from save failure.
- Chrome's Wiley ePDF reader worked where the in-app reader spun indefinitely. Its
  actual Download PDF link (`?download=true`) saved Edwards Xylem and Wellman 2014.
- Springer/Nature Download PDF and Cardiff ORCA Download links saved originals
  directly, even while mini was locked. ORCA CLI403 was not proof of browser failure.
- Royal Society/GSW short-lived PDF delivery links worked when immediately downloaded
  through an authorised route; log a stable publisher/source URL, never auth cookies,
  signed security tokens or credentials in durable provenance.
- Zenodo's large download continued as `.crdownload` after the tool's timeout; check
  completion and published checksum before restarting or declaring failure.
- ResearchGate “Full text available” may deliver only a title/abstract page. Inspect
  actual page extent. Recommendation badges can belong to a different paper.
- RMIT migrated from Esploro to Figshare; McSweeney's thesis is already acquired.
  Do not spend time obtaining it again merely because an old link redirects.

## Filing and verification on MacBook

Create `acquired/` and `results/` in this package. Save new original PDFs under
`acquired/<source-id>_macbook.pdf`, supplements under similarly explicit names.
Saving directly there is preferred; temporary Downloads copies are fine if necessary.
Do not overwrite a held partial/AAM/publisher PDF. Retain original bytes and versions.
Do not count an HTML print export or reconstructed scan as an original PDF.

For every successful file, verify title/authors/DOI or official report identity,
pages and plates/appendices, PDF readability and expected extent. Use locally available
pdfinfo/qpdf/pdftotext plus first/last and representative figure/plate renders. The
MacBook has limited RAM: keep this sequential and bounded; do not launch bulk OCR or
large jobs. Preserve recoverable source PDF warnings in notes rather than silently
repairing originals. Check SHA-256 and byte count from the actual saved file. Archives
must be inspected safely without executing downloaded content. Record each supplement
separately and explicitly list unavailable supporting/data deposits.

Important non-closures: Canning Part One (`quintvalle2006`) currently has only one
page of88; Part Two (`quintavalle2006`) is separate. White2008 is a data/software
archive. `steemans2009` is Philippe Steemans's IPC2008 abstract, separate from the
already-held Science2009 Brevia. `strother2017` is a GSA abstract. `libertin2022-open`
is an online2022/print2023 alias of an already-held work. McSweeney's thesis is
January2022/deposit2024. Edwards2015 ORCA is an AAM despite its repository label;
its published PMC version is already held. Never close a main-paper gap with a
supplement, abstract, first page, unrelated paper or catalogue record.

## Additive result records and reintegration

The package is a dated snapshot, not a second canonical register. Keep the supplied
CSVs/ledgers/manifest unchanged as evidence. Work additively under `results/` so that
mini's canonical checkout is not overwritten by a stale MacBook copy. The main
scientific agent may also be changing the repository; no ownership of scientific
files is transferred here. No model/card/occurrence edits are needed for this task.

Produce:

1. `results/outcomes.csv`: one row per attempted source, with source ID, component,
   outcome, observed route/blocker, next action, local file, date and notes. Distinguish
   full main, supplement, abstract, partial and unresolved. State what Barry actually did.
2. `results/acquisition-manifest.tsv`: one row per new file; columns `id`, `doi`,
   `citation`, `file`, `url`, `access`, `version`, `pages`, `bytes`, `sha256`,
   `acquired`, `notes`. Paths are package-relative `acquired/...`, not claimed mini
   holdings. Record stable source URL, serving repository, original/accepted version,
   and supporting omissions; verify any newly introduced DOI against Crossref.
3. `results/barry-to-action-updates.md`: resolved IDs, revised blocker diagnoses and
   exact remaining manual actions/links. Do not erase earlier provenance history.
4. `results/handoff-report.md`: recovered full texts versus components, duplicates,
   partials, quality caveats, outstanding blockers and where the return package is.

PDFs remain private/ignored; **never commit copyrighted PDFs to Git**. Do not mark
mini's master/status register resolved before the file actually reaches mini and its
hash is verified. Return files plus additive records through the authorised hub:

```bash
ssh nectar 'mkdir -p /data/share/silurian_plants/returns/macbook-2026-10-30'
rsync -a acquired results nectar:/data/share/silurian_plants/returns/macbook-2026-10-30/
```

Verify remote sizes/SHA-256 against the local manifest. Preserve any existing return
package; use a fresh suffix for another session instead of overwriting results.
On campus use public SSH through the `nectar` alias; SMB/Tailscale may be blocked.
Do not create reverse tunnels, change network configuration or revive old campus
routes. `mini` may be reachable outbound from MacBook through the configured Nectar
route, but this handoff does not require it. Barry will return to the mini session this
evening for integration; report the exact return directory to him. If connectivity
fails, retain all local files/results for later transfer and report that limitation.

A concise progress report to Barry and this return package complete the owned tranche.
He will re-prompt the mini session; do not wait or poll for an unprompted counterpart.
