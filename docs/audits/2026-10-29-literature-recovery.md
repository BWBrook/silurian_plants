# Literature-access recovery, 29 October 2026

The original pilot held five of twenty target papers. Rechecking its fifteen
unresolved entries recovered **seven more full texts: six publisher PDFs and one
explicitly labelled author preprint**. Twelve of the original twenty now have full
texts locally; eight remain pending. This is an improvement from 25% to 60% for
that fixed batch, below Barry's desired near-95% acquisition rate. Supplements are
not counted as separate papers. A preprint does not establish possession of the
published pagination.

Barry first asked for shared Chrome diagnosis, then authorised autonomous work
through the remainder after the first three successes. Codex acquired four more
texts autonomously. All acquired files are git-ignored; only provenance and
workflow findings are committed. Acquisition does not alter scientific readings.

## Recovered texts

This table lists the seven texts recovered today: the first three during the
shared-diagnosis phase and the last four in the subsequent autonomous pass. The
five texts acquired in the original pilot are not repeated here.

| Register ID | Source | Pages | File | Version |
|---|---|---:|---|---|
| `kraft2017` | Kraft & Kvaček 2017 | 11 | `library/closed/kraft2017.pdf` | publisher, pp. 180–190 |
| `garrattrickards1984` | Garratt & Rickards 1984 | 8 | `library/closed/garrattrickards1984.pdf` | publisher, pp. 377–384 |
| `garratt1984` | Garratt et al. 1984 | 4 | `library/closed/garratt1984.pdf` | publisher, pp. 355–358 |
| `al2015e` | Raevskaya et al. 2016 | 10 | `library/closed/raevskaya2016.pdf` | publisher, pp. 4–13 |
| `al2016i` | Tang et al. 2017 | 14 | `library/closed/tang2017.pdf` | publisher, pp. 50–63 |
| `al1996b` | Strother et al. 1996 | 4 | `library/closed/strother1996.pdf` | publisher, pp. 55–58 |
| `strother2000` | Strother 2000 | 23 | `library/closed/strother2000_preprint.pdf` | self-formatted author preprint dated 13 June 2018 |

Each file was parsed with `pdfinfo` and `pdftotext`; all pages contain text. Title,
authors and printed first/last pages were checked, and first/last renderings
inspected (Kraft's first page was observed in Chrome). SHA-256, bytes, URLs and
version notes are in `library/closed.tsv`. No separate supplementary file is
referenced in the text of the four texts acquired during the autonomous pass;
this is not a claim that no supplementary asset exists anywhere.

The Strother preprint cover states equivalence to the published chapter except
pagination; equivalence has not been independently compared. It cites published
pp. 3–19 whereas the publisher citation in the register gives 3–20. The actual
saved preprint has 23 pages, superseding a scout's provisional 28-page estimate
from a web-text view. Raevskaya and Tang issue years are 2016 and 2017; their
register citations were corrected from the harvest's online years, retaining
source IDs `al2015e` and `al2016i`.

## Remaining blockers

| ID | Observed end state | Next useful action |
|---|---|---|
| `al2015f` | Later shared in-app test reaches abstract plus sign-in/purchase gate, with inactive download; institutional sign-in triggers automated-browser block; Barry reports lockout in Chrome too and probable lack of UTAS journal access. Cambridge also returns `SHIBBOLETH_NOT_FOUND` | Library request; no further automatic BioOne retries |
| `al2023b` | Barry subsequently reports personal/institutional login options; the institutional link immediately triggers the same automated-browser block. Entitlement unknown. Public CONICET copy timed out from mini and Nectar; journal additional PDF requires subscription | Library-request batch, including relevant supplement; retain public CONICET lead; no further BioOne attempts |
| `al2007d` | Signed-in UTAS catalogue: request from other libraries; HAL has no attached manuscript and links ISTEX, whose URL was rejected by browser security policy as invalid | Library request, or Barry tests official ISTEX link |
| `al1996` | Signed-in UTAS catalogue: request from other libraries; ORBi publisher postprint is request-only | Library or ORBi request |
| `al2011n` | Signed-in UTAS catalogue: request from other libraries; no public PDF located | Library request |
| `al2008f` | Signed-in UTAS catalogue: request from other libraries; no public PDF located | Library request |
| `cesari2019` | Signed-in UTAS catalogue: request from other libraries; OnePetro security verification persists | Library request, optionally publisher verification with Barry |
| `mehlqvist2013` | Both signed-in UTAS ISBN results: request from other libraries; Lund has no downloadable whole thesis | Whole-thesis library request |

These are observed routes, not proofs that no lawful copy exists. No requests,
purchases, account registrations, credential changes or messages were submitted.
All autonomous-pass work tabs were closed; subsequent intervention routes are in
`docs/barry-to-action.md`. A later user-opened in-app BioOne tab could not be closed
through the available browser tool. The re-test below supersedes the earlier
suggestion to handle the two BioOne challenges together.

## What changed in the process

1. Search the authenticated UTAS catalogue using **Everything**. Its default
   **Our library** scope excludes the article results needed here. Reusing the
   existing staff SSO was sufficient; no fresh credentials were entered.
2. Use the catalogue's actual LibKey route before treating an anonymous publisher
   403 or an unproxied access message as a subscription test. Strother 1996's
   institutional GeoScienceWorld route worked despite the earlier public block.
3. A loading page or tab-inspection timeout is intermediate evidence. Allow a
   bounded period for redirects/rendering and inspect the eventual URL and native
   Chrome state. Stop on a concrete error or a persistent unchanged state, with
   the observed route and error retained.
4. Empty tab accessibility does not establish an empty page. Screenshots exposed
   loaded PDFs and Cambridge's UTAS suggestion; native Chrome accessibility
   exposed PDF toolbar and Save dialogs. The PDF Save command also worked.
5. Save directly to `library/closed/` when a Save dialog is offered. If the site
   downloads automatically, use Downloads as staging and copy after identifying
   the file. Verify the local file, not the viewer alone. Check dates in the
   source: Garratt & Rickards' server filename misleadingly used 2022.
6. Public author-uploaded files may download through normal Chrome controls even
   when a direct request fails. Strother's ResearchGate download succeeded and
   was retained as a preprint. Human verification, a subscription requirement and
   a browser-policy rejection remain distinct blockers; do not work around them.
7. Escalate only the remaining human actions together. The later Kanosh re-test
   moved it to the library-request group; Barry then reproduced the same sign-in
   block for Rubinstein. All eight are now request candidates, while Rubinstein
   retains its public CONICET lead. Repeated BioOne retries have stopped. Catalogue gaps and the observed access gate mean browser
   automation alone is insufficient for the desired 19/20 rate on this selection.

## Later shared BioOne re-test, 29 October 2026

Barry supplied the Kanosh article in the in-app browser through the UTAS proxy.
Its page showed the abstract and a sign-in/purchase gate, with no active paper
download. The institutional-sign-in target returned **Pardon Our Interruption**.
Barry then reported a lockout in Chrome as well and that UTAS appears not to have
access to this journal. Subscription absence is probable, not independently
confirmed. The action is now a library request, with no further automatic BioOne
retries. Barry subsequently reported the same institutional-sign-in block for
Rubinstein after its download offered personal or institutional access. It joins
the library-request batch, including its relevant supplement. Entitlement to its
different journal remains unknown; no personal account or request was submitted.

## Roles and verification

Codex desktop integrated acquisition and provenance. Bounded `gpt-5.6-luna`
executor/scout delegates checked public repository metadata, alternate routes and
CONICET connectivity from Nectar; they retrieved no target PDFs. Their findings
were treated as leads. A final read-only delegate check independently confirmed
the four new files' hashes, sizes, page counts and version labels, and the eight
pending entries; the report now makes the three-plus-four recovery split explicit. Parent Chrome inspection supplied the successful public
preprint download, authenticated holdings and specific BioOne/Cambridge errors.
The scientific cards and occurrence/interpretation tables were not edited.
