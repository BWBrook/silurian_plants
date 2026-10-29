# Barry to action: literature access

This queue records literature-access blockers without leaving browser tabs open.
No request, purchase or message is sent unless Barry chooses to do so. Reopen the
listed page in Chrome when ready; keep the record until the resulting file and its
provenance have been verified. A failed route does not establish that no copy exists.

## Pending — rechecked 29 October 2026

Eight of the original fifteen unresolved items remain. Kanosh now goes to a library
request after the BioOne re-test below; Rubinstein retains an unverified BioOne route.
Six other items have only library-request routes in the authenticated catalogue searches. No requests, messages or purchases have been submitted. Earlier
pilot observations remain in `docs/audits/2026-10-28-literature-sourcing-pilot.md`;
the follow-up and verification record is `docs/audits/2026-10-29-literature-recovery.md`.

### Vecoli et al. 2015 — Kanosh Shale palynology

- ID `al2015f`; DOI `10.1017/jpa.2015.29`.
- Reopen: [UTAS LibKey article](https://libkey.io/libraries/729/articles/77516390/content-location?utm_source=api_3637&allow_speedbump=true).
- Follow-up, 2026-10-29: Barry opened the article through the UTAS proxy in the
  in-app browser. It displayed the abstract and **Access the full article** with
  sign-in/purchase options; **Download paper** was inactive. Institutional sign-in
  then reached **Pardon Our Interruption**, an automated-browser block. Barry
  reported a lockout in both the in-app browser and Chrome, and that UTAS appears
  not to have access to this journal. This is a probable entitlement gap, not a
  confirmed catalogue subscription finding.
- Cambridge alternative: its institution lookup now finds UTAS (the result was
  visible in a screenshot but omitted from accessibility text), and the existing
  UTAS session completes authentication. Cambridge then returns
  `SHIBBOLETH_NOT_FOUND`: the selected organisation has not supplied the account
  information required for Cambridge access. This is distinct from BioOne access.
- Action: library request for the Kanosh paper. Stop BioOne retries for this
  paper; clearing a security challenge alone would not establish entitlement.
  No request or purchase submitted. The original challenged Chrome tab was closed;
  the later user-opened in-app tab could not be closed through the available tool.

### Rubinstein et al. 2023 — Colombian cryptospores

- ID `al2023b`; DOI `10.5710/amgh.27.07.2023.3560`.
- Reopen: [UTAS LibKey article](https://libkey.io/libraries/729/articles/580033879/content-location?utm_source=api_3637&allow_speedbump=true).
- Current blocker: the catalogue supplies a UTAS BioOne route, also held at an
  hCaptcha **Additional security check is required** screen. Entitlement remains
  unverified. After the Kanosh re-test triggered a lockout, do not retry BioOne
  automatically. This is a different journal; Kanosh's probable entitlement gap
  does not establish whether UTAS covers Ameghiniana.
- [CONICET record](https://ri.conicet.gov.ar/handle/11336/251421) advertises the
  full PDF, but ordinary downloads timed out from both mini and Nectar. Chrome's
  attempted repository navigation also timed out. No repository PDF was acquired.
- [Journal record](https://www.ameghiniana.org.ar/index.php/ameghiniana/article/view/3560)
  labels its additional PDF **Requires Subscription**; supplement acquisition is
  still pending separately from the main text.
- Action: revisit entitlement separately once the BioOne block has cleared, or
  use the advertised public CONICET copy when its host is reachable. Main text
  and supplement both remain pending. Earlier work tabs were closed.

### Le Hérissé et al. 2007 — Hanadir environments (Q1, Q2)

- ID `al2007d`; DOI `10.1016/j.revmic.2007.01.010`.
- Authenticated UTAS **Everything** search returns the article and a HAL record;
  both say **Get it for me from other libraries**. No available-online route.
- [HAL record](https://hal.science/hal-00149675v1) loaded after its automatic
  protection screen. It has no attached downloadable manuscript; its full-text
  link points to ISTEX. The browser security policy rejected that linked URL as
  invalid, so no attempt was made to work around the restriction.
- Action: library request, or Barry inspects the ISTEX link himself. No request
  submitted; tab closed.

### Steemans et al. 1996 — Turkish Ordovician–Silurian spores (Q1, Q2)

- ID `al1996`; DOI `10.1016/0034-6667(95)00119-0`.
- Authenticated UTAS **Everything** search says **Get it for me from other libraries**.
- [ULiège ORBi](https://orbi.uliege.be/handle/2268/119948) lists the publisher
  postprint, but access is **Request a copy**, not a public PDF download.
- Action: library request or request through ORBi. Neither submitted.

### Vecoli et al. 2011 — Anticosti Island and Estonia cryptospores

- ID `al2011n`; DOI `10.1016/j.revpalbo.2011.05.006`.
- Authenticated UTAS **Everything** search says **Get it for me from other libraries**.
  Public publisher/Estonian reference records expose metadata and abstract, with
  no downloadable full text located in this pass.
- Action: library request. None submitted.

### Vecoli et al. 2009 — Ghadamis Basin palynology

- ID `al2008f`; DOI `10.1016/j.palaeo.2008.05.015`.
- Authenticated UTAS **Everything** search says **Get it for me from other libraries**.
  No public full-text copy located. The issue is 2009 (volume 273, pp. 378–394);
  the harvest register still labels it 2008. No full PDF obtained to reconcile all
  date/version details.
- Action: library request. None submitted.

### Vecoli & Cesari 2019 — Saq Formation conference paper

- ID `cesari2019`; DOI `10.2118/195108-ms`.
- Authenticated UTAS **Everything** search says **Get it for me from other libraries**.
- [OnePetro record](https://onepetro.org/SPEMEOS/proceedings-abstract/19MEOS/19MEOS/D021S004R001/218629)
  remained at **Performing security verification** on recheck; no interactive
  challenge was solved and no full text was reached. Title artefact **Manuscript
  Title** remains unverified against the paper itself.
- Action: library request; optionally Barry tests the publisher verification.
  No request submitted; tab closed.

### Mehlqvist 2013 — Swedish spore thesis

- ID `mehlqvist2013`; ISBN `978-91-86746-95-7`.
- Authenticated UTAS ISBN search returns two records, both **Get it for me from
  other libraries**. The [Lund repository](https://portal.research.lu.se/en/publications/early-land-plant-spores-from-the-paleozoic-of-sweden-taxonomy-str/)
  identifies the thesis but exposes no whole-thesis download in Chrome. The Lund
  publication record gives 106 pages; bounded primary-host searches did not find
  a whole-thesis PDF on ResearchGate, Libris or DiVA.
- Action: library request for the whole thesis. Constituent articles are not
  counted as the thesis. No request submitted; tab closed.

Library-request searches can be reopened in [UTAS Library Search](https://utas.primo.exlibrisgroup.com/discovery/search?lang=en&vid=61UOT_INST%3A61UOT_INST):
select **Everything**, sign in using **UTAS Student and Staff**, then search the
DOI or ISBN above. In this session the existing UTAS login was reused without new
credential entry.

## Resolved through diagnosis and follow-up

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
