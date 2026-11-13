# B0 membership closure: pre-Silurian E2 material

Codex specialist delegate (sol_medium_scientist; configured GPT-5.6-sol/medium), 7 November 2026.
Bounded independent review at commit `1067c88`.
I checked the 111 observations carrying E2 in `data/occurrences/observations.csv`, their main
interpretations, the declared B0 and unit definitions, the held primary reports most likely to contain
non-dispersed material, and the 2022 synthesis used by the occurrence table. I did not search private
correspondence, contact authors or infer an exhaustive literature census beyond these data and held
sources.

## 1. Scientific conclusion and decision

**Only S-w22-K12 qualifies, on the evidence checked, as an accepted pre-Silurian land-plant
mesofossil under the declared B0.** Its admission is specifically as one Ghaba-1 locality-age unit
containing spore-filled fragments with preserved covering interpreted as sporangial wall. It is not a
macrofossil, a whole plant, an axis, or evidence for B1, E3 or E4. Dispersed spores and unbounded
spore masses without attached tissue do not qualify merely because they occur in E2.

The only additional substantive candidate is the Darriwilian Hawaz material behind S-w22-Dr4.
Abuhmida & Wellman (2017) figured two `cuticle-like` sheets and a cluster of monads whose status as
sporangial contents carries a question mark. Neither has a demonstrated sporangial wall or a secure
land-plant tissue identity. The later synthesis expressly treats Ordovician cuticle-like sheets as
biologically enigmatic. These remains therefore fail the word **accepted** in B0 and should not be
admitted. This is an exclusion for identity, not for age or size.

One-locality-age-unit admission for K12 is the least assumption-dependent count supported by the
published report. The 12 fragments came from three of 13 samples within a 3.3 m core interval, but
the paper does not map individual fragments to sample depths. Counting 12 specimens, three unnamed
samples, or a separate dispersed-spore occurrence would create unsupported replication. No existing
Oman/Ghaba B0 member was found in `horizons_reviewed.csv` or `primary_unit_membership.csv`, so the
additive unit is not a duplicate of the frozen body inventory.

## 2. Evidence and assumptions

### Declared target and observation process

`docs/plan-loop3.md` defines B0 as an "accepted land-plant macro- or mesofossil, sterile axes
included" and the analysis unit as a dated horizon (locality x bed). The estimand is the start of a
recoverable **body-fossil** process under declared recovery histories, not embryophyte origin. That
requires preserved non-spore material attributable to a land plant; E2 membership alone only denotes
evidence considered for the cryptospore event.

The relevant observation processes differ. The main body inventory is dominated by macrofossil
collections. K12 and Dr4 came from palynological acid maceration and sieving. Admission is therefore
a category decision as well as a taxonomic decision: it broadens B0 across recovery channels. This is
already acknowledged by the Oman sensitivity and is not a reason to exclude K12 selectively, because
the frozen B0 also contains macerated axial mesofossils.

### Oman identity and age

Wellman, Osterloff & Mohiuddin (2003), pp. 282-284 and Figs 1-2, report:

- Ghaba-1 core 21, 1542.0-1545.3 m, Hasirah Member, Safiq Formation;
- 13 processed samples, with large quantities of three samples top-sieved at 100 micrometres;
- 12 fragments, 0.24-0.49 mm, consisting of spore masses, some preserving part of a thin covering;
- specimens CW47a, CW47f and CW47i as a fragment, relatively complete contents, and fragmentary
  sporangium respectively; sectioning shows the covering overlying and penetrating among the outer
  spores; and
- the authors' conclusion that the spores formed in sporangia and that the fragments are direct
  evidence of land plants. They distinguish them from spore-rich coprolites by covering, shape,
  single-spore-type contents and absence of mixed plant debris.

The direct observations are spore masses plus covering and its contact with spores. "Sporangial wall"
and "bona fide land plant" are the authors' biological interpretation, albeit a well-supported and
subsequently retained one. Wellman, Cascales-Minana & Servais (2022), section *The fossil record of
land plants* and Fig. 2, call the same remains partial sporangia with fragments of sporangial wall and
retain them as land-plant remains. This meets the project's present accepted-reading threshold for
B0; it does not establish parent architecture or affinity.

The primary paper dates the fossil-bearing deposits only as Late Ordovician `Caradoc`, using
palynology, sequence stratigraphy and bracketing marine shale units. Caradoc is not uniquely Katian on
the current timescale. The project's Katian assignment is supported by the 2022 synthesis (Table 1
K12, the surrounding text, and Fig. 2 caption), not by a numeric date or sample-specific tie in the
2003 paper. Thus 452.8-445.2 Ma is a defensible updated stage assignment, but its dependence on a
secondary reassignment should remain explicit.

### Other plausible E2 material

| Observation | What the held evidence reports | B0 disposition |
|---|---|---|
| `S-w22-Dr4` | Abuhmida & Wellman (2017), accepted-manuscript PDF pp. 24-25 and Plate 6 nos 17-19: two dispersed `cuticle-like sheets` from separate wells/depths and one cluster of monads; the discussion says `?sporangial contents`. Mid-Darriwilian age is supported by acritarchs and chitinozoans. Visual inspection of Plate 6 shows a monad cluster but no attached covering. | **Exclude.** The source does not demonstrate a wall or connection; the cluster can be only a spore mass. Wellman et al. (2022), phytodebris section, say Ordovician cuticle-like sheets may be early land plants but may have other origins and are difficult to distinguish from marine material. Neither is an accepted land-plant body. |
| `S-palynodata-20245-cryptospore` | The cited work concerns Upper Silurian-Lower Devonian sporangia and spore masses. Its Palynodata Katian-Telychian range was already rejected in the main interpretation because the comparative occurrence does not substantiate a pre-Silurian record (`interpretations.csv`, rows 248-249). | **Exclude as pre-Silurian.** This is a database age/attribution problem, not an additional Ordovician body occurrence. |
| All other E2 observations | Dispersed spores, cryptospores, polyads or assemblage aggregates; no reported attached tissue in the structured observation or main interpretation. | **Exclude from B0.** Spores and masses without tissue remain in the spore channel. |

The 2022 review's general sentence that spore masses or partial sporangia have been recovered cites
both Wellman et al. (2003) and Abuhmida & Wellman (2017). Its case-specific wording attributes
homogeneous covering and partial sporangial wall to Oman. The Hawaz primary report is more cautious.
The general sentence should not be used to upgrade the Hawaz `?sporangial contents` into a second
sporangial-fragment occurrence.

## 3. Analyses and checks performed

### Explicit E2 inventory

All 111 E2 observations and all 111 corresponding main interpretations were read mechanically and
screened for sporangia, masses, clusters, cuticle, tissue, fragments and axes. The observations divide
as follows:

| Inventory tranche | n | IDs checked | Non-dispersed candidate found |
|---|---:|---|---|
| Targeted rows | 3 | `S-borenshult-pre-sandbian-cryptospores`; `S-cambrian-irregular-polyads`; `S-tremadocian-australia-polyads` | none |
| MVD-B sample rows | 13 | `S-mvdb-W2068754956-A026-cryptospore` through `-A037-cryptospore`; `S-mvdb-W2336620452-A001-cryptospore` | none |
| Palynodata rows | 32 | `S-palynodata-06209`, `08606`, `10843`, `10876`, `12678`, `13735`, `13842`, `14467`, `16121`, `16552`, `17957`, `17964`, `18162`, `18412`, `18701`, `18821`, `19047`, `19092`, `19344`, `19443`, `19557`, `20245`, `20323`, `20618`, `21120`, `21208`, `21354`, `21598`, `21736`, `21884`, `22019`, `22139` (all suffixed `-cryptospore`) | `20245` only, rejected as an unsupported pre-Silurian attribution |
| Wellman 2022 review/table rows | 48 | `S-w22-Dp1-Dp2`; `Dr1-Dr5`; `H1-H16` as present; `K1-K14`; `KH1-KH5`; `S1-S6` | K12 qualifies; Dr4 prompted the Hawaz primary-source check but fails identity |
| Wellman 2013 appendix rows | 15 | `S-wellman2013-W13-006`, `007`, `008`, `010-017`, `019-022` (all suffixed `-cryptospore`) | none |

This gives 110 dispersed-spore/cryptospore rows and one row (K12) whose structured description also
contains spore masses and sporangial fragments. Eighteen rows carry `same_material_as` links; K12
does not, and its note explicitly says that it already covers Wellman et al. (2003). I also searched
the frozen and reviewed B0 membership files for Oman, Ghaba, Hasirah and Safiq and found no competing
body member.

### Source and computation checks

- Inspected the held four-page Wellman et al. (2003) paper directly, including Figs 1-2, rather than
  relying on the card. SHA-256:
  `89843e7476e1f78e88ce9d6f906920ee7fe113a90515859463c101baef8c95b0`.
- Inspected the held Abuhmida & Wellman (2017) accepted manuscript, its discussion and Plate 6.
  SHA-256: `844a33c9ed11867ce376cf8882ceb20a241c20dd460c2a1fccc9d6240f3a09a9`.
- Checked the 2022 synthesis text used by the occurrence table (SHA-256
  `a30ae76b9bf23bd6cd36987c1996f4ffd2389fb0e8e6ad62e9a60423a66357b5`) against both primary
  reports.
- Checked `oman_sensitivity.py`: its live-input guard checks that the selected K12 rows are Katian and
  uses `set(k12.reading_id) < {"main", "inclusive"}`. That strict-subset expression is not a robust
  validation that both required readings are present; the parent methods audit handles this guard
  limitation. The script reproduces the 48 frozen B0 result rows and adds one member with
  `n_members = 1`. The additive row appears once per analysis inventory, not once per specimen. I did
  not rerun it because this membership audit changes no input or calculation.

## 4. Uncertainty, limitations and next decision required

This is a closure of membership within the present E2 table and held relevant sources, not proof that
no unentered pre-Silurian mesofossil exists. The structured table understates Hawaz by recording only
the cryptospore assemblage; its cuticle-like sheets and monad cluster are visible only in the primary
paper. They should remain explicit rejected/disputed candidates if the occurrence ledger is later
expanded, rather than silently disappearing.

The Oman count is conservatively one unit because sample-depth membership is unavailable. If the
three top-sieved samples can ever be mapped to distinct depths from an already-held published source,
the unit structure could be revisited before any unfrozen reanalysis. The current evidence does not
justify doing so. The Katian range also remains a review-level reassignment of the primary paper's
broader Caradoc designation.

**No further membership decision is required for Review C:** retain K12 as the sole added B0 unit,
retain the frozen E3-E5 inventory as a separately labelled comparison, and do not add Dr4 or
S-palynodata-20245. The manuscript should say `sporangial fragments` or `spore-filled mesofossil
fragments`, not imply an Ordovician axis, whole plant or ordinary macrofossil collection.
