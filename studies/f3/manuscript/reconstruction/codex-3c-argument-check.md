# Step 3c: argument and new-source check

Codex, 11 November 2026. Reviewed the Introduction, Discussion, Data accessibility and drafting notes
of `c0f83fc`, with four targeted original-source checks. Only this review note is edited.

**Recommendation.** Keep the roughly 3,000-word article. Its length serves the argument; comparator
word counts supply no reason to expand it. Make the four scope repairs below before accepting this
step. The new literature supports the central additions without requiring a broader review essay.

## Material repairs

1. **Separate source access from deposit reproduction.** Data accessibility currently says copyrighted
   sources and third-party deposits are fetched by script and hash-checked. The deposit fetcher's
   documented scope is openly licensed deposits; it explicitly excludes paywalled or unlicensed
   local material. `studies/f3/manuscript/README.md` instead distinguishes excluded copyrighted full texts from
   fetched deposits. Restore that distinction, for example: “Copyrighted full texts are excluded from
   the repository; source routes and held-file hashes are recorded separately. Openly licensed
   third-party deposits are fetched by script and hash-checked.” Do not promise automatic restoration
   of the whole literature collection.

2. **Compare effective marginal priors with posteriors.** The closing recommendation says comparing
   “calibration priors” with posteriors shows what the molecular data add. Brown and Smith's point is
   specifically to sample the joint prior without molecular data and compare its marginal age
   distributions with the corresponding posteriors. Supplied calibration curves can differ from
   those marginals after their interaction with the tree prior and other calibrations. Name that
   effective prior, so a reader can perform the intended diagnostic. The [original publisher
   abstract](https://academic.oup.com/sysbio/article/67/2/340/4107448) directly supports this narrower
   recommendation; it does not make prior sensitivity a finding of the present analysis.

3. **Restore geographical scope in the mechanisms paragraph.** The Introduction correctly limits
   scarce pre-latest-Silurian terrestrial deposits to western Europe. The Discussion repeats the
   scarcity as a general statement. Retain the regional qualification there, or leave scarcity as a
   conditional mechanism without asserting a global geological pattern. This is the same scope
   correction accepted in steps 3a–3b.

4. **Restore “absence-based” in the maximum definition.** The Introduction now defines every maximum
   as an argument that older rocks would have yielded the lineage. Benton and Donoghue discuss that
   approach alongside other ways to formulate maximum constraints, including modelling and
   phylogenetic information. “An absence-based maximum adds an argument…” describes the cases being
   tested without making an unnecessary universal definition. Their [original
   paper](https://doi.org/10.1093/molbev/msl150), especially pp. 28–29, supports that formulation.

## Findings that stand

The calibration-uncertainty sentence is supported at its current strength: it says calibrations *can*
dominate absolute-age uncertainty, rather than asserting that they dominate every analysis. The
original dos Reis et al. discussion of the limits of divergence-time estimation explains the
time–rate confounding and reports empirical examples in which calibration uncertainty dominates
sequence-data uncertainty. No further generalisation is needed. [Original accepted
manuscript](https://discovery.ucl.ac.uk/id/eprint/1473649/1/PRR_dos_Reis_in_revision_1445434492_78-for-self-archiving.pdf).

Kenrick and Crane support stepwise acquisition of branched sporophytes and conducting anatomy: their
phylogenetic discussion and diagrams place fossil plants with combinations of these characters
between living groups. That is an appropriate reason to keep character acquisition distinct from
divergence and first recording. It supplies no estimate of the particular delay required by this
paper's scenarios. The draft correctly leaves individual mechanisms and their contributions open;
it measures their possible combined recording contrast.

The comparator paragraph distinguishes the fitted genus-origin analysis, conditional category bounds
and calibration densities without claiming to have audited the assumptions of Silvestro or
CladeDate. This comparative role is coherent. Their numerical results and implementations were not
freshly re-audited in this check.

The PBDB archive statement has independent live support. The public Zenodo API returns record
24028289 with the stated frozen Darriwilian–Emsian collections-extract title, CC0 licence, provenance
file and the named CSV.gz. These agree with `data/external/pbdb-snapshot.json`. I checked metadata and
file listing, not a fresh payload download or SHA-256 reproduction. [Archive
record](https://doi.org/10.5281/zenodo.24028289).

## Length and reading provenance

The main text already gives the scientific problem, three distinct tests, the recording-bound
equation, model conditions, decisive sensitivities and the two routes accommodating older dates.
Add words only where an essential inferential link remains unexplained. Building the planned figures
and checking their agreement with the text is more valuable than expanding towards comparator
lengths. The targeted repairs above require little additional space.

The draft reports an 11-source delegated read and four quotes independently checked by Claude. A
bounded search of the current repository's `work/`, reconstruction notes and relevant documentation
did not locate a separate receipt for that job. I did not inspect unrelated session logs. This audit
therefore verifies the targeted support below, not every reported delegated read. Preserve any
available source URL, section/page and scope receipt so the broader reading claim remains reviewable;
there is no need to re-read all eleven merely to complete a checklist.

| Original material read in this check | Scope and limits |
|---|---|
| Benton and Donoghue, *Paleontological Evidence to Date the Tree of Life*, DOI `10.1093/molbev/msl150`; [institutionally hosted publisher PDF](https://bpb-eu-w2.wpmucdn.com/blogs.bristol.ac.uk/dist/3/589/files/2019/08/Benton__Donoghue_2007.pdf) | Introduction and maximum-constraint discussion, printed pp. 26 and 28–29. The 30 calibration case studies were not audited. |
| dos Reis, Donoghue and Yang, *Bayesian molecular clock dating of species divergences in the genomics era*, DOI `10.1038/nrg.2015.8`; UCL accepted manuscript linked above | “Limits of Bayesian divergence time estimation”, manuscript pp. 6–7, with the preceding Bayesian-model definition and nearby fossil-calibration discussion. No numerical reanalysis. Web PDF rereads timed out; the ordinary institutional download succeeded. |
| Kenrick and Crane, *The origin and early evolution of plants on land*, DOI `10.1038/37918`; local institutional copy `library/closed/kenrick1997nature_tier2.pdf` | “Building a land plant”, Box 1, Box 2 and character diagrams/captions, printed pp. 34–37. Local acquisition provenance is in `library/closed.tsv`. No updating of its historical phylogeny or fossil assignments. |
| Brown and Smith, *The Past Sure is Tense*, DOI `10.1093/sysbio/syx074`; original publisher abstract linked above | Read the full original abstract, including its joint-prior sampling and marginal prior/posterior recommendation. The publisher PDF route returned its abstract/purchase page; full methods and results were not reviewed. This limited read directly covers the cited recommendation. |

Yang/Rannala and Parham retain the targeted source checks recorded in `codex-3b-reference-check.md`;
they were not re-read. Other newly added sources, including Ho, Peters, Lenton and the spore papers,
were not independently rechecked here. No new journal-rule claim, model result or biological
plausibility judgement is made by this note.
