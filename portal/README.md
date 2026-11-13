# Private reading portal

The reading room and taxon atlas are generated from this repository. Markdown is authoritative;
do not edit generated HTML. The renderer preserves the scientific body text, card metadata,
trait notes and references. Card contrasts and borrowed trait origins are displayed explicitly;
Model transfer sections render directly from the Markdown. Images supplement the cards and do
not supply trait observations.

The live, owner-private Site is [Early Land Plants](https://silurian-plants-library.barry-brook.chatgpt.site).
Sites provides the access control. `noindex` is supplementary, not an access restriction.
Keep the audience private when refreshing. `.openai/hosting.json` records its stable project ID.

## Build and check

From the repository root:

```bash
uv run --locked portal/build.py
uv run --locked portal/check.py
node --check portal/app.js
```

`uv` installs the locked, script-local dependencies. No project-wide environment is needed.
The build reads committed, tracked `docs/**/*.md`, `taxa/*.md`, selected `data/**/README.md`,
`studies/f3/models/README.md`, the root README and `data/timescale.csv`. Referenced, tracked illustrations
are copied with source checksums; untracked and excluded image paths fail the build. The build
refuses uncommitted source changes. Data `local/`,
`closed/` and `work/` README files are excluded; full texts and bulk datasets are not bundled.
The generated site, search index and source checksums are in ignored `portal/dist/`.

For a local preview:

```bash
python3 -m http.server 8765 --bind 127.0.0.1 --directory portal/dist
```

Browse `http://127.0.0.1:8765/`. Local preview has no login gate; keep its binding on loopback.

## Refresh the hosted Site

Refresh on Barry's request; there is no scheduled job or GitHub push trigger.

1. Preserve any existing work. Fetch `origin` and fast-forward `main` when the checkout is clean.
   Commit authorised changes to the source/renderer before generating the published snapshot.
2. Read the Site identified in `portal/.openai/hosting.json` with Sites `get_site`. Confirm its
   owner-only audience and obtain a short-lived source repository write credential. Never print,
   save or commit that credential.
3. Use the installed Sites skill's `site-workflow.mjs` source helper to open the generated
   checkout in `.site-publish/` **before** overwriting it. If absent, restore it into an empty
   `.site-publish/`. Retain the helper's opening result. On the initial unpublished Site only,
   stage first so the new checkout has its hosting manifest.
4. Run `uv run --locked portal/build.py --stage`, then `uv run --locked portal/check.py` and
   `node --check portal/app.js`. `--stage` exports only generated `dist/`, the hosting manifest
   and a provenance README into ignored `.site-publish/`. This is a separate publication
   repository; do not change the research repository's remotes or push its full history to Sites.
5. Run the Sites source helper again from that checkout, passing the retained opening result,
   credential, `commands: []` and an absolute archive path outside the checkout. It commits,
   pushes and packages the generated source. Use its exact returned project ID, commit and archive
   with `save_version_and_deploy_private`. If the Site's access is no longer owner-private, stop
   the deployment and report the mismatch rather than widening access or publishing publicly.
6. Follow a pending deployment to a terminal status. Report the successful URL and the
   authoritative source revision from `portal/dist/provenance.json`.

The Sites workflow and current tool contracts are in the installed `sites:sites` skill. Use a
fresh credential for later refreshes; do not persist credentials in this repository. The hosting
ID is durable and must be reused, not recreated.

## Images and checks

The homepage and reading room lead with F3, the trait pilot and the questions register, followed
by the four foundation documents. Audits, data/implementation guides and operational notes are
grouped in expandable lists. All included documents remain searchable; this is navigation
curation, not a change to scientific priorities or source wording.

`images.json` records each image's source, creator, licence, caption, kind, retrieval date and
changes. Local copies are in `assets/`. Captioned images retain attribution and licence links;
the About page credits all assets. Atlas thumbnails may be visually cropped; full card images
show the complete web asset. Reconstructions and living comparisons are labelled.

`check.py` checks every local link and anchor, exact card coverage, search coverage, source
checksums, body-text preservation, contrast and borrowed-trait metadata, source links, reading-room
coverage, image metadata and excluded payload classes.
It is a presentation/integrity check, not scientific validation. Recheck interactive search and
atlas filters, keyboard access and desktop/mobile layouts after renderer or UI changes.
