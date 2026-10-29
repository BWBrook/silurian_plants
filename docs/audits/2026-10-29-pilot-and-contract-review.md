# Pilot specification, deposited states and third F3 repair review

Codex, 29 October 2026, at `7c443f9`, reviewing Claude's commits `0ad77c7` and
`63205a1` and Correspondence 2560–2562. Barry re-prompted continuation while a
separate Codex reference scout acquires literature. `models/f3/` and
`docs/pilot-traits.md` remain Claude's; neither was edited. Two same-model
delegates (GPT-6, exact variant not exposed) performed independent contract/
logic checks and a bounded primary-specimen audit. The parent integrated the
findings, checked decisive implementation/source evidence, and wrote and
independently verified the deposited-state extraction. These amendments are
review findings for Claude, not an adopted new biological model.

## Assessment

The pilot's framing is a useful part of F3: assess the bridge from fossil event
to node claim. Retain it. The present specification needs narrower inference
rules and explicit distinctions between evidence from one attached specimen,
a taxon reconstruction, and separately reconstructed character marginals.
Neither a new tree nor a joint origin model is needed to make these corrections.
No empirical F3 fit, binding ensemble, clock rerun or ancestral-state inference
was run in this tranche.

## 1. The node-to-encounter implication needs its own statement

**L1 — Temporal precedence alone is insufficient for the current encounter
claim.** A trait can arise in an extinct stem side branch before the crown,
disappear there, and arise later in the crown. Its first origin precedes the
node, but an old, abundant crown then need not produce the event during the
sampled interval. Restricting the crown's rarity does not restrict trait loss,
replacement or producer identity. The missing bridge is: an older node would
entail a relevant event-specific production/encounter history in the tested
class, under stated assumptions about inheritance, loss and recurrence.
Keep temporal precedence separately. If an analysis genuinely bounded the
global earliest origin of that same trait across such histories, precedence
would suffice mathematically; F3's conditional encounter result does not
automatically supply that global bound.

**L2 — Crown-state reconstruction is not origin reconstruction.** Crown absence
does not refute an earlier gain followed by loss; crown presence supports an
ancestral state under its model, with its uncertainty, rather than a dated
transition. Separate crown-state support, transition-history evidence and
earliest-origin timing. Add `unresolved` for missing temporal evidence; do not
use `contradicted` merely because modal crown states lack the trait. A declared
history model that excludes earlier gain–loss histories would be an additional
assumption, not a conclusion from these marginals.

**L3 — Relative order is not placement relative to the crown.** “Cryptospores
first, triletes derived” permits both traits to arise on the ancestral stem
before the crown. It does not itself break P1. Replace that assertion with
“a reading placing the first relevant trilete production after crown
Embryophyta breaks P1”, requiring a source for that stronger placement. The
draft already correctly notes that a fossil's stem position does not date its
cryptospory; retain this distinction during scoring. A surviving stem side
branch can acquire a trait after the crown has originated.

**L4 — Split universal P3b into record identity and proxy specificity.** A C3
plant outside total-group Tracheophyta falsifies the universal proposition that
all C3 plants are tracheophytes. It does not by itself refute placement of the
Homerian specimen or a defined aggregate C3 encounter result. Assess each
calibration specimen's placement separately from whether multiple producer
lineages make the admitted event/reference frame comparable. The node implication
requires node existence to entail the relevant production history; its logical
converse is not generally required.

**L5 — Total group includes crown.** A generic *Cooksonia* tip inside the crown
does not contradict calling another record total-group. The substantive question
is the transfer from that generic tip and younger anatomical specimens to the
Homerian `cf.` material. Hooper Supplementary Table 4 explicitly makes the
younger-anatomy transfer (PDF pp. 16–17, 23–24). Retain this as an identity/
placement audit; it is not proof of an internally contradictory clock calibration.
Q9's input/output provenance remains unresolved independently.

## 2. Published ancestral-state extraction

`tools/hooper_asr.py` extracts X21 and X26 for crown Embryophyta and crown
Tracheophyta, retaining all labelled states under all four methods and three
trees. `data/pilot/hooper2026-asr/` contains the 240-row table, node identities,
matrix crosswalk, source hashes and receipt. Both archives match their retrieval
hashes. All 76 character/taxon comparisons match the master matrix.

An independent R/ape 5.8-1 check (`tools/check_hooper_asr.R`) verifies the six
MRCAs and descendant sets, all 208 reported values and all 32 omitted columns.
The absent columns remain empty with `column_absent`, not imputed zeros.
The extra `PARS_X21_ext2` file is an exact duplicate, not a fifth method.

**A1 — Aperture and dispersal results must stay separate.** Embryophyte-crown
X21 favours proximal trilete in every output. ER/ARD/SCM support is
0.770018–0.977218; parsimony assigns that state. The zyg-tree ARD **X26** result,
however, is dyad 0.700980651632401, hilate 0.297664090273339, n/a
0.00104323164599069, tetrad 0.000312026448269216, and pooled trilete/inaperturate
monad **0**. Its X21 trilete value is 0.977217664157549.

The broad “all methods reconstruct trilete monads” reading therefore does not
follow from the deposited tables. X26 state 4 also pools trilete and inaperturate
monads, so it cannot alone establish a trilete aperture. Do not multiply the two
marginals, infer a mixed-producing ancestor, or discard the ARD scenario. This
is evidence of separately modelled characters yielding a combination requiring
interpretation, not a new reconstruction or a demonstrated biological mixture.
The pilot should report the marginals and label their joint biological reading
unresolved. Re-estimation remains outside the current scope.

## 3. Primary-specimen audit

The delegate checked full texts and rendered key pages. The following identifies
what the held evidence establishes; it does not silently change any card's
coding or promote a taxon combination to a single-specimen observation.

| Material | Source evidence | Consequence for the pilot |
|---|---|---|
| *C. pertoni*, DE41 | Edwards et al. 1992, pp. 683–684, Figs 1–2: short single-sporangium fragment, in-situ *Streelispora newportensis* and axial secondary wall thickenings. UF597 and UF1877 lack diagnostic spores. Authors prefer tracheids but cannot conclusively exclude tubes from the incomplete elements | DE41 links C1 (via spore assignment) with the anatomical evidence for C4. It does not meet the pilot's attached two-sporangium C3 rule. A C1+C3+C4 row needs an explicitly labelled taxon bridge or another connected specimen |
| Pridoli *C. pertoni* strands | Edwards et al. 1992, p. 685, discusses central strands and inference of tracheidal identity by comparison with younger forms | The Ambitisporites card's “simple conducting strand”, with tissue coded unknown, is not a demonstrated claim of observed Pridoli tracheids. No Q5 error is established by this wording difference; keep direct anatomy separate from inference |
| *C. barrandei*, D552a,b | Libertín et al. 2018, pp. 269–270, Fig. 1: branched holotype with two sporangia; spores removed from its sporangium, illustrated aperture tied to D552a | Direct C1+C3. C4 unknown. Middle Sheinwoodian *M. belophorus* assignment uses associated material, lithology/fauna and the relocated locality (SI PDF pp. 2–4); the holotype's direct association is *M. flemingii*, not *M. belophorus* |
| *Partitatheca horrida* | Edwards et al. 2012, pp. 245, 247: new sporangia lack axes; Habgood's earlier branched axis with one terminal sporangium is reassigned on a stated spore interpretation; conducting tissue unknown | C2 plus branching, C3 unconfirmed, with the reassignment explicit. Trace original specimen identity/imaging in Habgood 2000 before treating it as a newly demonstrated attached *Partitatheca* plant |
| *Ficoiditheca aenigma*, V.68228(1), V.68258(1) | Morris et al. 2012, pp. 570–577, Figs 1I/J, 3A/M: two sporangia on each branched axis and in-situ palynomorphs; diagnostic internal walls are shown especially in V.68222(1), Fig. 4, and V.68263(1), Fig. 3I | A useful additional C2+C3 candidate already held. Direct architecture/spore link, but the permanent-dyad diagnosis transfers across assigned specimens; retain that bridge. Early Lochkovian |
| *Aglaophyton major* | Edwards 1986, pp. 182–183, Figs 12/18: Pb4601/B/R/10 and /24 trace a pair to one dichotomy; Fig. 13, Pb4601/C/L/2, is another connected pair. Anatomy lacks differential thickening (pp. 189–192). The explicit trilete statement on p. 176 reviews earlier work | C3 and the non-tracheidal anatomical reading are supported. An illustrated aperture linked to a connected pair was not located here; C1+C3 without C4 remains a taxon reconstruction pending that link. Modern Rhynie age requires its separate dating source |
| Homerian *Cooksonia* cf. *pertoni*, TCD22944–22956 | Hooper SI Table 4, PDF pp. 16–17 and 23–24: the calibration text explicitly transfers younger *C. pertoni* anatomy | Audit the specimen/age/placement transfer. Generic tip placement cannot silently settle this `cf.` assignment |

The Libertín supplement's “560 mm” axis length conflicts with its illustrated
scale; it was not used. These observations concern the held sources, not an
exhaustive refutation of evidence that could occur in another source.

**Proposed evidence rule:** keep direct attached/serially reconstructed specimen
combinations distinct from conspecific composites and from broader taxonomic
transfers. The latter can remain informative when their identity assumptions are
explicit. This makes the pilot feasible without weakening its observation standard.

Verified local source hashes (all under `library/closed/`, except the named SI
deposit):

```text
edwards1992_cooksonia.pdf 0bcf0cc087dc25cccf9bdebf08bb74d41dcf5467dbc7455548906f22d06c01ef
edwards1986_aglaophyton.pdf 96e57a34f6da0f325f6204c96cf361c25937b16b336c3a29ce21cf7391f16cdc
libertin2018.pdf 5564a5c21d2bed19e8b6a24a48922fa695bc5406041e2531176741645dc29e4f
libertin2018_SI.pdf b9b1f332bd6cdb4d8ed566def7bb6cfa5343f62e99c4b835f6d1c18e5b185147
al2012b_oup.pdf 6cac8172ce5d50f3518216f504bef17be8080e37ce09e11583b72cf3bc04b012
al2012e_oup.pdf 9cc08f877914339bb79a7d74322b61cb5676a4a72a7fb0a1a9a5c6350d80e61c
data/external/deposits/hooper2026-spore-evolution-esm/41477_2026_2432_MOESM1_ESM.pdf edf6fe2a68c42a4cb093fba9fa925b4ba34f49d7411e373bb62f493f17060e8b
```

## 4. Third contract repairs: what passes and what remains

All **159 F3 tests pass**. Stage 2 is executable, selects borderline cells and
pools only borderline quantities at 1,886. Ordinary receipt scope/protocol/global
delta checks work. Failed bound/set statuses now affect coverage; fixed-M2 and
endpoint summaries retain/filter numerical status. The core improvements stand.
The following lightweight injected cases identify remaining acceptance gaps;
they are not observations of such errors in the saved ensembles.

**V1 — Stage-one evidence is trusted through derived labels**
(`validate.py:518–530`, also `:511–515`). The reader validates metadata but not
the exact unique quantity set, count ranges or agreement of labels with counts.
Starting with 117 passing quantities, changing one `k1` from 1,000 to **0** while
retaining its `pass` labels is accepted; no cell is rerun and the pooled grid is
called accepted. Missing or duplicate quantity rows also pass `check_stage1`;
duplicates can survive the final set-based grid check. Validate the unique
quantity set, integer counts within 0–1,000 and null stage-two fields, then
derive labels/result from counts. Bind the verdict to its supporting replicate
evidence for the binding workflow.

**V2 — Delivered-bound coverage can still omit the truth** (`:368–379`). A
successful bound with f*=0.2, true target 0.3 and successful truth LR=0 counts
as `fcover=1`; only `mismatch_f=1` records the disagreement. Acceptance does not
refuse that mismatch. Require actual delivered containment with the declared
tolerance, or refuse acceptance on material bound/test disagreement. The origin
set now checks containment; the bound needs the same delivery guarantee.

**V3 — Every component shift needs validation** (`:469–477`). An otherwise valid
receipt with a last component `delta=NaN` can pass because Python's `max` can
ignore that later NaN. Require every component to be finite and non-negative
before checking the global maximum.

**V4 — Calibrated shift is a proposal from stored margins** (`:403–406`). A
grid-delivered origin set can exclude the truth while its exact test covers:
`ocover=0`, mismatch 1, yet stored-margin delta 0. Widening the critical value
also changes numerical searches/status. Qualify descriptions that call the
margin-derived shift the smallest shift delivering the target coverage; its
actual delivered coverage is established by the independent acceptance run.

Retain the agreed global shift and 0.955 tuning target pending evidence from the
real design. There is no current reason to introduce per-class shifts or expand
the calibration batch merely from three retrospective batches. Those batches
do not establish a bounded sampling distribution for the future shift.

## Handoff and structural review

Claude should amend the pilot with L1–L5 and A1, retain specimen-level evidence
tiers, and make the bounded V1–V4 repairs. Codex's extraction is ready for his
review; its results are deposited-output evidence, not independent biological
validation. The separate scout owns acquisition; Codex's next frame work is
the Pelmis companion/sample-to-age reconciliation, using the source inventory
without inferring the missing 113 negative samples.

Q1 gains a more explicit node implication and a remaining validation checklist;
Q2/Q4 gain specimen-link qualifications and the Ficoiditheca lead. Q5 does not
gain a proven Pridoli-strand error. Q9 retains the record-specific transfer
question without reviving a full clock run. The structure supports the next
investigation with a small auditable extraction and a focused review; no new
joint model, universal tree or broad schema is needed.
