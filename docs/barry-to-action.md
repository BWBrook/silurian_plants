# Barry to action: literature access

This queue records literature-access blockers without leaving browser tabs open.
No request, purchase or message is sent unless Barry chooses to do so. Reopen the
listed page in Chrome when ready; keep the record until the resulting file and its
provenance have been verified. A failed route does not establish that no copy exists.

## Active access actions

Two fresh route-level actions remain after the autonomous expansion; no tabs are held open for them. Reopen only when Barry is available. Liu 2016 remains resolved.

| Work | Observed blocker | Reopen route |
|---|---|---|
| Breuer et al. 2007 (`al2007c`), Saudi Devonian miospores | Public full-text record exposed a download, but the download stalled and a subsequent in-app visit presented a security check. No challenge was solved; access has not been disproved. | [ResearchGate author copy](https://www.researchgate.net/publication/233499781_Early_to_Middle_Devonian_miospores_from_northern_Saudi_Arabia) |
| Higgs et al. 2014 (`al2014c`), Bulls Head Formation | In-app JSTOR displayed browser verification; Chrome fallback inspection timed out. No PDF acquired and entitlement remains unestablished. | [JSTOR record](https://www.jstor.org/stable/10.3318/ijes.2014.32.55) |

The detailed autonomous audit records resolved reader/save failures and version qualifications. The metadata-only Mahmoudi DOI check remains unresolved; it does not require Barry to obtain the already-held paper.

The ten earlier request candidates and five newly observed archive-access gaps remain parked in
[`docs/literature-requests.md`](literature-requests.md), separately from this fresh
access action. No request has been submitted.

## Resolved through diagnosis and follow-up

### Regional-spore batch — recovered autonomously 2026-10-29

Six main texts and the Ghelli update companion are held in seven publisher PDFs;
no sign-in or manual intervention was needed. In-app access/linked-file checks
preceded Chrome's working native PDF-save fallback. The shared Ghelli map was
also secured. No active action added; tabs and Downloads residue were cleared.
See `docs/audits/2026-10-29-regional-spores-batch.md`.


### Stage B ResearchGate author copies — recovered autonomously 2026-10-29

Mehlqvist 2012 (`w2080475227-fulltext`, 12 pages) and Wellman chapter 29
(`wellman2013-open`, 16 pages) are verified and held in `library/closed/`.
The in-app Mehlqvist device check restricted access, but Chrome worked without
sign-in; Wellman's in-app check cleared automatically. No human action needed.
See `docs/audits/2026-10-29-researchgate-author-copies.md` for versions and checks.


### Liu et al. 2016 — recovered 2026-10-29 (`al2016e`; Q1/Q2, MVD-B)

- DOI `10.1016/j.revpalbo.2016.02.003`; RPP 233, 146–160.
- Earlier automated Chrome attempt showed **Full text access** but its PDF/LibKey
  routes stalled and the download yielded PDF-challenge HTML.
- Barry then opened the same paper immediately in Codex's in-app browser and
  saved its original publisher PDF to Downloads. This establishes a working
  route and successful entitlement; the cause of the earlier stall is unproven.
- Archived as `library/closed/liu2016.pdf`; title/DOI, all 15 nonempty text pages,
  printed endpoints 146–160, PDF structure and first/last renders checked. Bytes,
  SHA-256 and browser provenance are in `library/closed.tsv`. Downloads duplicate
  moved to the recoverable Bin after archive/hash verification; PDF tab closed.
- Workflow lesson: try the in-app browser as a bounded alternative when an
  entitled ScienceDirect PDF stalls in Chrome. An automation delivery failure
  does not establish that the paper is unavailable. No scientific reading changed.


### Kraft & Kvaček 2017 — recovered 2026-10-29 (Q1, Q2)

- Earlier observation (2026-10-28): UTAS access was displayed but PDF viewing and
  downloading did not complete. The cause of that earlier stall is unproven.
- Re-test: Barry clicked **View PDF** on the authenticated ScienceDirect article;
  the complete 11-page publisher PDF opened immediately in a new Chrome tab.
- Diagnosed automation limitation: the tab-level accessibility tree exposed only
  the asset URL, while a screenshot showed the rendered viewer. Chrome's native
  app accessibility tree exposed **Download**, the Save dialog and completion.
  A coordinate click first focused the download control; the native named-button
  click opened Save. Codex saved directly to `library/closed/kraft2017.pdf`.
- Verification: title, DOI, 11 non-empty text pages and printed endpoints 180–190;
  SHA-256 and access route recorded in `library/closed.tsv`. No separate supplement
  link found on the article page. Scientific re-reading remains pending.
- Repeatable procedure: inspect newly opened PDF tabs visually before classifying
  a blank accessibility view as a loading failure; use Chrome native accessibility
  for its PDF toolbar and Save dialog; verify the resulting local file. This
  removes a demonstrated automation obstacle, but does not establish the cause of
  yesterday's failure or prove that the initial PDF-opening step is automated.

### Garratt & Rickards 1984 — recovered 2026-10-29 (Q1, Q2)

- Route: [UTAS LibKey](https://libkey.io/libraries/729/articles/37016473/full-text-file?utm_source=api_3637&allow_speedbump=true)
  redirected to the UTAS EZproxy Lyell reader for `10.1144/pygs.44.4.377`.
- Observed: an initial **Reader environment loading** screen subsequently completed,
  with no further sign-in observed. Barry reported it ready; Codex then found the
  correct eight-page reader and used its **Download PDF** link successfully.
  No access failure was reproduced. The cause of the 2026-10-28 stall is unproven.
- Download saved automatically in Downloads, then was copied under the verified
  name `library/closed/garrattrickards1984.pdf`. The publisher's filename includes
  `2022`, but the article header, pagination and metadata identify February 1984.
- Verified: eight non-empty text pages, correct title/authors, printed pages
  377–384; file size and SHA-256 in `library/closed.tsv`. Scientific re-reading
  remains pending.
- Procedure: give library/proxy readers a bounded loading period, checking the
  eventual URL and rendered state before classifying access. A single loading
  screenshot is an intermediate state, not a demonstrated blocker. Check download
  completion and destination; prefer direct library saves when a Save dialog is
  offered, and use Downloads as staging when download is automatic.

### Garratt et al. 1984 — recovered 2026-10-29 (Q1, Q2)

- Route: [UTAS LibKey](https://libkey.io/libraries/729/articles/24442686/full-text-file?utm_source=api_3637&allow_speedbump=true)
  redirected to the signed Oxford/Silverchair PDF for
  `10.1111/j.1095-8339.1984.tb02566.x`. No new login or security challenge appeared.
- Observed: tab accessibility timed out during redirect. Native Chrome
  accessibility showed the publisher asset loading, then the correct four-page
  viewer. A further ten-second interval allowed the viewer to finish rendering.
- Codex used the native **Download** button and **Save** dialog to save directly
  as `library/closed/garratt1984.pdf`. Title, five authors, 1984 journal header,
  four non-empty text pages and printed endpoints 355–358 verified. UTAS/date
  watermark confirms institutional delivery. Provenance and SHA-256 are in
  `library/closed.tsv`; scientific re-reading remains pending.
- Procedure: when tab inspection times out during navigation, inspect native
  Chrome state and the eventual PDF before treating the timeout as a site access
  failure. Today's route succeeded without human intervention after opening;
  yesterday's security/sign-in stall was not reproduced.

### Raevskaya et al. 2016 — Siberian cryptospores — recovered 2026-10-29

- Register ID: `al2015e`; DOI: `10.1016/j.revpalbo.2015.10.010`.
- Held: `library/closed/raevskaya2016.pdf`, 10 PDF pages; SHA-256 and route in
  `library/closed.tsv`.
- Publisher PDF; title, DOI, ten non-empty text pages and printed endpoints 4–13 verified, with first/last page rendering checked. Printed issue year is 2016; source-register harvest had labelled it 2015. View PDF redirect and rendering completed before native Chrome save; a tab-level empty accessibility view was not used to infer failure.

### Tang et al. 2017 — Tarim Basin cryptospores — recovered 2026-10-29

- Register ID: `al2016i`; DOI: `10.1016/j.palwor.2016.01.004`.
- Held: `library/closed/tang2017.pdf`, 14 PDF pages; SHA-256 and route in
  `library/closed.tsv`.
- Publisher PDF; title, DOI, fourteen non-empty text pages and printed endpoints 50–63 verified, with first/last page rendering checked. Printed issue year is 2017; source-register harvest had labelled it 2016. Saved directly to library/closed after allowing PDF redirect/rendering to finish.

### Strother et al. 1996 — Saudi Arabian spores (Q1, Q2) — recovered 2026-10-29

- Register ID: `al1996b`; DOI: `10.1130/0091-7613(1996)024<0055:neflpf>2.3.co;2`.
- Held: `library/closed/strother1996.pdf`, 4 PDF pages; SHA-256 and route in
  `library/closed.tsv`.
- Publisher PDF; correct title/authors, four non-empty text pages and printed endpoints 55–58 verified, with first/last page rendering checked. UTAS watermark dated 29 October 2026. Native Chrome Save command saved directly to library/closed. No new login or security challenge appeared on this route.

### Strother 2000 — cryptospore chapter (author preprint) — recovered 2026-10-29

- Register ID: `strother2000`; DOI: `10.1017/s1089332600000681`.
- Held: `library/closed/strother2000_preprint.pdf`, 23 PDF pages; SHA-256 and route in
  `library/closed.tsv`.
- Author-formatted preprint dated 13 June 2018, 23 PDF pages including cover, references, figures and tables. Cover states same as final published version except pagination; this equivalence is the author statement, not an independent comparison. Cover citation says 3–19 whereas project publisher citation is 3–20. Version and pagination distinction retained. Public Download full-text PDF worked in Chrome; copied from Downloads/Strother2000.pdf into library/closed. All 23 pages have extractable text, first/last pages rendered. Published chapter remains unheld.
