# Supplement: methods, sensitivities and audit trail

For *Older than their fossils? What the Ordovician–Silurian record can test about the maxima that divide land-plant molecular clocks*.

<div id="authors"></div>

This supplement holds the machinery behind the main text. Repository paths are given so that every
number can be traced to the table or script that produced it. Internal labels appear here because
the repository uses them: **M1**, **M2** and **M3** are the 515.5, 459.1 and 431.2 Ma maxima; **E1**
trilete spores, **E2** cryptospores accepted as embryophytic under a named reading, **E3**
polysporangiate bodies, and **E5** crown vascular-plant members. **B0**, **B1** and **B2** are the
body-record categories: any land-plant body (any accepted macro- or mesofossil; canonically including
the Katian Oman sporangial fragments, S5.1), polysporangiophyte body and crown vascular-plant member.
`manuscript/estimands.md` states what each analysis bounds and which phrasings are not allowed.

## S1. Readings, observations and units

**Named readings.** Disputed identifications, affinities and ages are carried as alternatives, not
resolved by fiat. The *main* reading accepts what the cited sources accept. The *inclusive* reading
adds records that a named source accepts against others, and the *outlier* reading admits further
records that are explicitly contested. A wider reading requires a record-specific acceptance; it does
not promote every unresolved grain or axis to a detection. The E2 rule separates spore morphology and
producer evidence from the embryophyte affinity accepted by each reading (`data/units/e2-unit-rule.md`).
Rejected, reassigned and disputed records are listed in `docs/rejected-records.md`.

**Observations.** Within each frame, the same reporting rule applies to older and reference material.
An explicit non-detection is scoped to the material actually examined. A missing report becomes a zero
only after a full-category reporting audit. Unresolved identification, missing links and unreported
effort remain distinct from absence.

**Ages.** Stage bases follow ICS v2024/12 (`data/timescale.csv`). Source-specific age statements and
their numerical conversions are retained separately. Literature before 2024 mostly uses GTS2012 Early
Devonian boundaries, which differ from ours by up to 3 Myr. Uniform within-range ages and shared
within-range positions are modelling choices, not measured dating distributions.

## S2. The Murzuq encounter comparison

### S2.1 Source and frame

Abuhmida [@abuhmida2013PalynologicalAnalysisOrdovician] reports palynology from six Murzuq Basin wells. All [164]{.C38} appendix samples were
transcribed independently, with 158 chart depth and type labels (153 exact matches). The 164 prose-scope
rows and 158 chart reports were mapped, retaining barren material and possible caving
(`data/units/libya_*.csv`; `docs/audits/2026-10-31-libya-event-map.md`). The primary frame is the
chart-coded cuttings design `LY-MZ-CU`. Five wells contribute [59]{.C02} Llandovery reference cuttings ([51]{.C02} with trilete reports), and three of them contribute [28]{.C01} older cuttings without trilete reports.

### S2.2 Model, targets and qualification

Let $d_i\in\{0,1\}$ be the reported trilete outcome for eligible cutting $i$, $c(i)$ its eligibility
class, $k(i)$ its well, and $[l_i,h_i]$ its declared age range. Conditional on the fixed stage
boundaries, latent age is uniform on that range. Let $r_c>0$ be the nuisance reference encounter hazard
for class $c$. A mean-one well effect
$u_k\sim\mathrm{Gamma}(\nu,\nu)$ is shared by the reference and older cuttings in well $k$;
the primary across-well design fixes $\nu=2$. Well effects are integrated out, not estimated.
Cutting outcomes are independent conditional on their well effect and latent ages.

The first-appearance rule gives $\tau=443.1$ Ma. Encounter intensity is scaled to $a(t)=1$ in the
five-stage reference window. For a candidate origin $T>\tau$, $a(t)=0$ for $t>T$. The declared older-to-
reference delivery and recovery multiplier is $m_i=\rho$ for transported older cuttings and 1 otherwise,
with $\rho\in\{1,0.5,0.25,0.1\}$ fixed in separate analyses rather than estimated. Partition
$(\tau,T]$ at stage and numerical-range boundaries. If $w_{ip}$ is the fraction of unit $i$'s age range
in piece $p$, $Q_i$ the fraction in the reference interval at or younger than $\tau$, and $x_p$ the mean
of $a(t)$ in piece $p$, its age-integrated detection probability conditional on $u$ is

$$
\pi_i(u;r,x)=Q_i\{1-\exp(-r_{c(i)}m_i u)\}
 +\sum_p w_{ip}\{1-\exp(-r_{c(i)}m_i u x_p)\}.
$$

The unshown remainder of the age range lies older than $T$ and contributes zero detection probability.
For piecewise-constant histories this expression is exact. The joint likelihood is

$$
L(r,x)=\prod_k\int_0^\infty
  g_{\nu,\nu}(u)
  \prod_{i:k(i)=k}\pi_i(u;r,x)^{d_i}
       \{1-\pi_i(u;r,x)\}^{1-d_i}\,du .
$$

Thus samples from the same well are marginally dependent. The likelihood profiles $r$ jointly with the
history; the reference-only fit supplies starting values, not a plug-in rate held fixed. In the primary
data there are [59]{.C02} reference cuttings ([51]{.C02} positive) and [28]{.C01} older zeros, across five wells; the older zeros come from three of them. At $T=459.1$ Ma,
18 older cuttings have all their age support in $(\tau,T]$, while each of the ten Darriwilian cuttings
has exposure weight $q_i=0.9/11.2=0.08036$. Under the constant history $a(t)=f$, its zero probability
reduces to

$$
1-q_i+q_i\exp(-r\rho u f),
$$

inside the same well integral as the reference outcomes.

For nonconstant histories the reported target is the fitted-rate-weighted mean intensity

$$
\bar a_r(T)=\sum_p c_p(r)x_p,\qquad
c_p(r)=\frac{\sum_i r_{c(i)}m_i w_{ip}}
             {\sum_i r_{c(i)}m_i\sum_q w_{iq}}.
$$

The rates in these weights are profiled in the likelihood. With the primary cutting-only design there is
one rate class, so class-rate uncertainty does not change the relative piece weights.

| Class | Restriction on $a(t)$ for $\tau<t\le T$ | Ceiling | Reported use |
|---|---|---:|---|
| H0c | $a(t)=x$, constant | 1 | exact constant-history bound and origin read-out |
| H0 | any path $0\le a(t)\le1$ | 1 | bound on $\bar a_r$; pointwise origin and window read-outs |
| H0m | H0 plus intensity non-decreasing towards $\tau$ | 1 | monotone bound; origin read-out permits the declared 10 Myr delay |
| H1 | any path $0\le a(t)\le3$ | 3 | higher-ceiling sensitivity for $\bar a_r$; no origin read-out |

For H0c the age-integrated likelihood is exact. For H0, H0m and H1 the implementation bounds each
piece using the convex chord for non-detections and Jensen's inequality for detections, then maximises
over piece means. With no older detections, as in the primary Murzuq design, the H0 and H1 bounds are
attainable. The H0m within-piece relaxation remains conservative because its extremal path need not be
monotone inside every piece.

For class $K$ and threshold $f$, let $\bar\ell_{0,K}(f;T)$ be the supremum of the implemented
chord/Jensen **upper log-likelihood envelope** over nuisance rates and piece means satisfying
$\bar a_r(T)\ge f$, and let $\ell_{A,K}(T)$ be the exact log likelihood of the best constant history up
to that class's ceiling. For H0c the null is also exact, so $\bar\ell_{0,K}=\ell_{0,K}$. For H0 and H1
the envelope is attained in the present no-older-detection application; for H0m it can remain strictly
above the likelihood supremum over monotone paths and therefore gives a conservative statistic. The
implemented statistic is

$$\Lambda_K(f;T)=\max\left[0,\ 2\{\ell_{A,K}(T)-\bar\ell_{0,K}(f;T)\}\right].$$

The reported $f_K^*(T)$ is the largest $f$ not excluded. H0c, H0m and H0 share the constant alternative
on $[0,1]$; H1 uses its ceiling of 3. The declared critical value is the one-sided count-matched value
for the number of older detections plus a simulation-calibrated nonnegative shift. Here there are no
older detections and the accepted shift is zero, giving $-2\log(0.05)=5.991$.

Origin read-outs impose pointwise restrictions rather than only the mean target. H0c requires a
constant $a\ge f$ on $(\tau,T]$; H0 requires $f\le a(t)\le1$ throughout that interval; H0m requires the
floor from $T-10$ Ma to $\tau$ and permits lower intensity, down to zero, during the first 10 Myr after origin. The separate H0
window read-out beginning at 459.1 Ma requires $a(t)\ge f$ only on $(459.1,T]$ and allows any path in
$[0,1]$ between $\tau$ and 459.1 Ma. These are marginal read-outs, not a simultaneous confidence band.

“Qualified” means that the complete screen, first-appearance selection, likelihood fitting and test
inversion attained at least the declared 0.93 marginal-coverage floor on the frozen finite simulation
grid, with a calibration target of 0.955 and a separate acceptance run. It does not validate uniform age
within stages, Gamma$(2,2)$ well heterogeneity, conditional independence, equal reporting scope, the
chosen $\rho$, or the historical sampling process outside that grid. Inverse-block-size weighting and
leave-one-well-out results in S2.5 are retrospective unqualified sensitivities, not alternative qualified
dependence models.

The potential screen, eligibility and estimation path were simulated on a declared finite grid. Results
are nominal 95% compatibility bounds, qualified per quantity and design against a 0.93 coverage floor
(calibration target 0.955), conditional on passing the potential screen, with abstentions counted as
covering. The largest observed marginal miss proportion was 38/1,000. At the B4 boundary of the 462.6 Ma
window, [20 of 1,000]{.C06} screen-passing simulations excluded the truth, and [60]{.C06} delivered non-abstaining window
claims, so 20 of those 60 missed. Population 95% coverage, coverage conditional on a non-abstaining
result, simultaneous coverage and validity beyond the tested histories are not established. Thirteen
Murzuq design/delivery combinations qualify. A fourteenth qualified pair, QB-CO, supplies no older M2
interval and has a narrower class scope. The receipts are in `models/f3/out/qual/`.

**Table S12.** What the Murzuq comparison allows: model-conditional 95% compatibility limits, assessed on the declared simulation grid, on older trilete-producer intensity as a fraction *f* of the Llandovery reference, primary stage allocation. Rows 1–2 constrain intensity sustained from 459.1 Ma to the reference; rows 3–4 constrain an interval of fixed intensity beginning at 459.1 Ma and extending further back.

| Question asked of the 28 older cuttings | Delivery equal ($\rho$ = 1) | Delivery halved | Delivery quartered | Delivery a tenth |
|------------------------------------|-----------:|-----------:|-----------:|-----------:|
| Largest constant producer intensity, 459.1 Ma to the Llandovery | [0.091]{.C24} | [0.182]{.C24} | [0.364]{.C24} | [0.910]{.C24} |
| Largest intensity, exposure-weighted history class | [0.184]{.C24} | [0.258]{.C24} | [0.421]{.C24} | [0.921]{.C24} |
| Oldest end of a reference-intensity interval beginning at 459.1 Ma | [462.6]{.C03} Ma | [464.1]{.C03} Ma | [467.1]{.C03} Ma | [no limit]{.C03} |
| Oldest end of an interval at 0.1 or 0.01 of reference intensity | [no limit]{.C05} | [no limit]{.C05} | [no limit]{.C05} | [no limit]{.C05} |

### S2.3 Contamination and an identification limit

Murzuq's palynofacies fractions use a different preparation and a 200-particle denominator. They cannot
supply separate trilete and cryptospore counts for the chart search, so binary observations are retained
and contamination enters as a sensitivity model. Let $g$ be the indigenous fraction of reference
*encounter intensity* (not of positive samples), and $\kappa$ the transfer of the contaminant component
into older cuttings. For age-exposure weight $q_i$, an older zero has probability

$$\exp[-ru\kappa(1-g)]\{(1-q_i)+q_i\exp[-ru\rho gf]\}.$$

The likelihood depends on these parameters only through $a=\rho gf$ and $b=\kappa(1-g)$, so tuples
preserving both are observationally equivalent within the model. If every $q_i=1$, only their sum
enters the older-zero likelihood. Declining indigenous output can thus be offset by delivery and
reference contamination along stated parameter combinations. This is an identification result within
the declared model, not a universal property of binary observations.

A predeclared 5,760-row factorial grid varies delivery, indigenous fraction, transfer, allocation,
chronology, interval and intensity. Independent uniform ages are compared with fixed, depth-ordered
10%, 50% and 90% positions within source ranges. The threshold $-2\log(0.05)$ is an uncalibrated
comparison convention. A contamination scenario that conflicts with older zeros even at $f=0$ is
flagged separately. The 384 break-even entries fix $\kappa=b=0$. These surfaces and the 36-case
well/age influence exercise are unqualified sensitivities.

**Table S1.** Murzuq sensitivities (`models/f3/loop2/out/`; `docs/loop2-sprint1-results.md`).

| Challenge at $\rho=1$ | Observed sensitivity | Scope |
|--------------------|------------------------------|----------------|
| Five leave-one-well-out cases | H0 [0.1850–0.3646]{.C07}; window endpoints [462.6–468.1]{.C07} Ma | one factor at a time; unqualified |
| All nine influence/age/allocation cases | H0 [0.1775–0.3646]{.C07} | unqualified |
| $\kappa=0$, independent uniform stage ages | critical $g$: [0.0910]{.C08} for constant origin intensity; [0.9559, 0.2363, 0.1735]{.C08} for windows ending 462.6, 467.1, 469.4 Ma | $f=1$; comparison contours, not confidence limits |
| Shared midpoint ages | no exposure in the [459.1–462.6]{.C09} Ma window | fixed chronology scenario |
| Shared 90% ages | no exposure in the window ending at 467.1 Ma | fixed chronology scenario |

### S2.4 The calibration material: Borenshult-1

Hooper et al. [@hooper2026ReconstructingSporeEvolution] base the 459.1 Ma maximum on the oldest possible trilete spores from the
Borenshult-1 core, Östergötland, Sweden [@rubinstein2019BalticaCradleEarly]. Their Supplementary Table 4 keys the soft
maximum to *Chelinospora?* sp. at 48.2 m (*Baltoniodus variabilis* zone, lower Sandbian) and takes the value from
the GTS2012 Sandbian base plus its uncertainty, [458.4 + 0.7 = 459.1]{.C42} Ma. The same rule on our timescale gives
[458.9]{.C42} Ma. They did not use the Borenshult spores for a minimum because the trilete marks might be
compression artefacts.

Rubinstein and Vajda's Fig. 3 separates definite from possible triletes. It plots definite triletes at
six depths from 43.1 to 33.05 m, all Sandbian or younger and the lowest below the [454.41]{.C43} Ma Kinnekulle
K-bentonite, and possible triletes only at 48.2 and 34.0 m. Their Fig. 4 lists no trilete taxon at 41.1 m,
so five depths are concordant between the figures[]{.C43}. We carry three readings: Fig. 3 definite, Fig. 4
definite and the concordant five, each with the two possible-only depths unresolved, plus Hooper et al.'s
wholesale exclusion as a sensitivity (`data/units/borenshult_review/`,
`docs/audits/2026-11-05-trilete-evidence-rubric.md`). Symbols and positive depths are not specimen counts.

The readings bear on three separate questions. (1) The maximum: the stage-base rule gives 459.1 Ma from the
definite 43.1 m level as from the possible 48.2 m one. (2) A minimum: the definite triletes would set a
crown-embryophyte minimum only under an added mapping of their producers to the crown; that mapping is not
supplied by the mark, and its minimum would be the young edge of the bentonite age, not the level itself.
(3) An absence test: only three Darriwilian samples lie below the first definite trilete. With all three
fully exposed, the screen statistic at reference intensity is [1.3157]{.C44}, [1.0753]{.C44} and [1.1155]{.C44} for the
three readings, against [5.9915]{.C44}, so the core cannot exclude reference-level intensity before its first
definite trilete under any reading (`models/f3/out/borenshult_review/screen.csv`). This screen has no
numerical chronology and is not a test at 459.1 Ma.

The comparison of the earliest trilete claims on common axes (specimen basis, the describing authors'
confidence, independent age control, artefact evidence and documentary consistency) keeps Qusaiba-1 as
the secure comparator, retains the Turkish occurrence with its original Ashgillian–Hirnantian age wording,
and keeps the Hirnantian Zbrza marks outside strict trilete occurrences because their authors doubt them.
No composite score is computed.

### S2.5 Time support by well and dependence among cuttings

Fig. S2 plots every chart-coded cutting by well and depth with its full stage enclosure. The older frame
has three Darriwilian cuttings in D1-200 and seven in H2-NC186, whose enclosures reach before 459.1 Ma, and
18 Katian or Hirnantian cuttings in D1-200, H2-NC186 and I3-NC186 that are wholly younger[]{.C45}. In the
encounter likelihood a Darriwilian cutting enters as a mixture: with probability $1-q_i$ its age lies
before 459.1 Ma, where a history sustained from 459.1 Ma gives no producers, and with probability $q_i$ it
lies inside the window ($q_i = 0.9/11.2$ under a uniform age within the stage).

The qualified model shares a Gamma(2, 2) frailty within each well. Three retrospective, unqualified
sensitivities (`models/f3/loop3/murzuq_stage2.py`) ask how much the constant-history contour on $\rho f$
depends on cuttings being independent given the shared well effect. Each uses the declared $-2\log(0.05)$ threshold as a comparison
convention, not a calibrated critical value.

| Treatment | Contour on $\rho f$ |
|---|---:|
| Conditionally independent cuttings given shared well frailty (as qualified) | [0.0910]{.C51 .V087} |
| A separate reference rate for each well, no frailty | [0.0995]{.C51 .V086} |
| Each cutting weighted by 1/(size of its well × formation block) | [0.393]{.C51 .V084} |
| Each cutting weighted by 1/(size of its well × stage-support block) | [0.419]{.C51 .V085} |
| One well left out at a time | [0.093]{.C51 .V082} to [0.186]{.C51 .V083} |

**Table S1b.** Murzuq dependence sensitivities (`models/f3/loop3/out/stage2_murzuq/dependence_sensitivity.csv`).

Inverse block-size weights give each block unit total likelihood weight: about seven reference and six
older blocks in total weight. Reference blocks mix positive and negative cuttings, so a block is not
replaced by a single binary observation. This composite sensitivity does not estimate correlation or full
block dependence; its unqualified comparison contour is about four tenths of reference intensity, against
about a tenth for the qualified model. Dropping
I3-NC186, which holds ten of the 18 younger older-frame cuttings, has the largest single-well effect. Claude
reproduced the four undropped contours with an independent implementation.

### S2.6 Stage-level comparisons outside Libya

The compilation of Wellman et al. [@wellman2013Chapter29Palaeophytogeography] lists six trilete-bearing
review entries wholly within the adopted Katian–Hirnantian crosswalk. Checking their cited sources
narrows the comparison used here to Saudi Arabia and Turkey[]{.C54}. Steemans et al.
[@steemans2009OriginRadiationEarliest] report true triletes in the Katian Qasim and Hirnantian Sarah
formations of Saudi Arabia; Steemans et al. [@steemans1996OrdovicianSilurianCryptospores, p. 40] place
the oldest Turkish *Ambitisporites avitus* occurrence possibly between middle Ashgillian and
Hirnantian. These are overlapping stage-age enclosures, not demonstrated simultaneous deposition,
independent geographical replicates or evidence of a crown-embryophyte producer.

The review's British entries conflict with their cited source. Burgess
[@burgess1991SilurianCryptosporesMiospores, pp. 594, 596] distinguishes the older
*Ambitisporites?* material, probably fragments of cryptospore tetrads, from true triletes in later
Llandovery samples. The later tentative reinterpretation of one figured specimen by Steemans et al.
[@steemans1996OrdovicianSilurianCryptospores, p. 47] concerns a Rhuddanian sample and does not restore
a Hirnantian positive. The Belgian entry remains unverified against primary sources in this audit.
We preserve the published extraction but omit these entries from the
secure examples. The source-by-source audit and exact selectors are in
`docs/audits/2026-11-13-c54-independent-check.md`; C54 covers only the narrowed comparison.

## S3. QSIM-801: a model-conditional floor calculation

Vecoli et al. [@vecoli2017MiddleOrdovicianCryptospores] [Table 1, p. 321] report [99]{.C11} cryptospore morphotaxon occurrences across [17 of 20]{.C11}
tabled samples assigned to the late Dapingian–early Darriwilian. Their p. 330 explicitly reports no
triletes in the studied sequence. The table was independently reconstructed from the rendered source
(`data/units/loop2/replication/`). Its 22 categories include informal morphotypes. Marks are distinct
recorded occurrences, not counts of independent producers or dispersal events. The table-defined depths
are 675.1–767.8 ft. The methods' shallower endpoint, 586.9 ft, is inconsistent and is not used.

Let $\theta_i$ be the trilete/control unit-intensity ratio in sample $i$, and $h>0$ a relative effective
recovery factor. Suppose the reported objects form a co-ascertained, independent target/control sample.
Conditioning Poisson counts on the true land-spore total $N_i$ then gives target probability
$h\theta_i/(1+h\theta_i)$. For a persistent floor $\psi=\min_i\theta_i\geq\theta$, the all-zero
probability is at most $(1+h\theta)^{-\sum_iN_i}$. If each mark contributes a distinct target-detectable
unit, $M\leq\sum_iN_i$ permits a conservative rejection rule: no targets and $(1+h\theta)^{-M}\leq\alpha$.
Randomness of $M$ does not invalidate the rule: conditional on the actual totals, rejection is a subset
of the all-zero event with enough units to cross the threshold. Then $U=\{\alpha^{-1/M}-1\}/h$ bounds the
*minimum* ratio, not every sample's ratio, a mean, or the pooled share.

| Relative effective recovery $h$ | Independent units, $D=1$ | Heuristic $D=2$ | Heuristic $D=4$ |
|---:|---:|---:|---:|
| 1 | [0.031]{.C12} | 0.062 | 0.129 |
| 0.5 | 0.061 | 0.125 | 0.257 |
| 0.25 | 0.123 | 0.250 | 0.515 |
| 0.1 | [0.307]{.C12} | 0.624 | [1.287]{.C23} |

**Table S2.** Model-conditional floor limits; none is an admitted empirical confidence bound. $D$ divides the exponent as a heuristic for clustering, not a validated correction.

The source specifies preparation but not the search coverage needed to show that every mark represents
a unit on which triletes were detectable. Independence, effective ascertainment and sampling and stopping
conditions are unverified. The calculation therefore stays exploratory. Toy Poisson simulations check the
algebra[]{.C13} but cannot validate the historical protocol. No matched counted Katian–Llandovery reference was
recovered. Qusaiba-1 supplies reference context only. Röstånga and Caspalá/Lipeón are younger than M2,
and Hanadir/TAYM-4 is separate material without a qualified design[]{.C22} (`manuscript/external_candidates.csv`).

## S4. The 515.5 Ma maximum (M1): affinity and the preservation-control argument

Morris et al. [@morris2018TimescaleEarlyLand] place the maximum at the base of the *Olenellus* Biozone, about [515.5]{.C46} Ma, below the
oldest possible total-group records (Stage 4 Rome Formation cryptospores), and argue for a real absence
before it: land-plant spores share the preservation potential of the marine algal cysts with which they
usually occur, so older cyst-bearing sequences without land-plant spores record absence
[@morris2018ReplyHedgesEt]. Our earlier drafts described only the placement (`docs/audits/2026-11-07-m1-rationale.md`). The
control shows that sporopollenin-walled microfossils survived and were recovered; it does not by itself
show comparable terrestrial delivery, coverage of the land areas where early plants grew, sensitivity of
preparation and search to small cryptospores, or production of recognisable spores by the earliest
producers. The assessment below concerns whether the assembled material can quantify the argument.

No assessed frame admits an E2 older-zero/reference design. The Borenshult 71.1 m zero is secure under
the main reading but belongs to a frame that fails its potential screen. It is not a pre-515.5 Ma
observation. Strother [@strother2016SystematicsEvolutionarySignificance] places the Tennessee taxa in Charophyta. Taylor and Strother [@taylor2024UltrastructureCambrianCryptospores] interpret
the packets as pre-embryophytic, and Wang et al. [@wang2022PalynologicalAssemblageCambrian] favour ancestral aeroterrestrial algae while
calling direct embryophyte affinity unlikely and the interpretation premature. None explicitly accepts
the assessed Stage 4 producers as embryophytes. Wall ultrastructure and developmental features bear on
precursor relationships, so the inclusive reading stays an explicit alternative. Argentine sample
RIOCAP-7999 is unresolved under main and detected under inclusive and outlier readings. Stage 4 converts
to [514.5–506.5]{.C16} Ma, all younger than 515.5 Ma by the maximum's design (`data/units/loop2/m1-m3/`).

## S5. The positive body-record analysis

### S5.1 Inventory and units

**Names.** The [241]{.C38} distinct PBDB macrofossil names overlapping 445.2–393.47 Ma were classified by
`gpt-6.1-sol` with web search. Each name received a category, polysporangiophyte and crown-member flags,
a basis, a cited source and a confidence (`data/macro/name_classifications.csv`). Names judged
implausible for the window, for example the Cretaceous angiosperm leaf genus *Protophyllum*, cannot enter
any category. A stratified source audit is in `docs/audits/2026-11-01-loop3-source-review.md`; it does not
certify all 241 assignments.

**Material identity.** Only explicit collection or occurrence identifiers justify replacing a PBDB record
with its curated interpretation. Country, taxon and overlapping ages do not establish identity; the pilot
used them and falsely merged distinct localities (S7). Regional checklists and unresolved duplicates are
withheld from the primary count and kept in a sensitivity. Source decisions are in
`data/macro/source_adjudications.csv`. Example: the two Yea horizons are kept as separate units with the
full disputed Gorstian–Emsian range, because the Gorstian attribution rests on a disputed graptolite
identification. Neither a fixed Gorstian nor a fixed Devonian age is justified.

**Units.** The primary unit is a locality–age proxy: PBDB formation plus coordinates rounded to 0.1° and
identical age support, or a curated named site plus identical age support. For a collapsed unit, the
oldest-member age has support from the maximum of member lower ages to the maximum of member upper ages.
Missing geographic keys retain the collection identifier. The proxy is conservative but is not a verified
bed (`models/f3/loop3/out/primary_unit_membership.csv` lists every constituent record).

**Older screen.** A separate screen covers all [556]{.C38} older-only non-spore PBDB rows (69 names). Source
review of the seven plausible or unplaced names (17 occurrences) found cyanobacteria, algae or trace
fossils and the rejected *Boiophyton*, not an additional embryophyte body. These exclusions are not
fossil non-detections, and the screen is not a search denominator
(`data/macro/older_records_screen.csv`; `docs/audits/2026-11-01-loop3-older-records-review.md`).

**Category admission.** Membership is tested by the builder from each record's evidence channel
(`data/macro/body_membership.csv`). B1 requires E3 (branched axes bearing sporangia) or nested E5 (crown
membership) evidence. Tracheids alone (E4) are synthesis evidence and do not show a branched sporophyte
with several sporangia, so E4-only material does not enter B1: the Lochkovian Lang tracheid axis, a
sterile axis, stays out. The E3 channel was enumerated only for the Homerian and older, so a younger
record without an E3 row was never assessed for branching, and its absence is not a negative. Two such
records have published branched fertile material and are admitted to B1 on that evidence:
*Cooksonia bohemica* from Kosov, whose emended diagnosis and holotype describe isotomously branched axes
with terminal sporangia [@libertin2022EarlyLandPlant], and the Upper Roman Camp Beds at Capel Horeb, which
yielded branching specimens of *Steganotheca striata* and *Cooksonia* sp. from the same Ludlow beds as
the tracheid-bearing sterile axis [@edwards1979RecordsFertileRhyniophytina, Plate 1e, g]. Branching,
conducting anatomy and crown membership are adjudicated separately for each, and tracheids are not
transferred to the fertile specimens (`docs/audits/2026-11-07-gpt6pro-review2-triage.md`).
Separately, PBDB collection
278439 (Xiemisitai Bed 16, Hoboksar County) is in West Junggar, not Tarim
[@liu2024EvolutionSilurianPhytogeography]; it is now grouped with the other West Junggar material under Kazakhstania in
both the fossil and the effort tables, which changes the region–stage sensitivity (C30) but no
locality–age unit.

**The Oman sporangial fragments.** B0 was declared as any accepted land-plant macro- or mesofossil,
sterile axes included (`docs/plan-loop3.md`). The inventory as first built took curated records from the
E3–E5 channels only, so the spore-filled sporangial fragments of the Ghaba-1 borehole, Oman
[@wellman2003FragmentsEarliestLand], recorded in E2 (observation S-w22-K12), never entered it. The primary report describes
fragments from three samples of one core, some with a sporangial covering around in situ cryptospores; it
dates them Caradoc, and the later review we follow correlates them to the Katian. No associated axes or
conducting tissue are preserved, so they stay out of B1 and B2, but the declared B0 admits them. The omission was an
inventory-assembly error, so the Oman-inclusive B0 is canonical and the former inventory is reported as
an exclusion sensitivity. The fragments enter as one locality–age unit (Katian enclosure 452.8–445.2 Ma),
not as twelve fragments or three samples. Codex's membership audit of all 111 E2 observations found no
other record that passes the declared B0 before the Silurian
(`docs/audits/2026-11-07-b0-membership-review.md`); the older Hawaz sheets lack secure land-plant tissue
identity. Their recovery through palynological preparation differs from the macrofossil collections that
dominate the recording proxies, which is a further reason the B0 histories may misdescribe the sequence.
The B0 values now come from the canonical `build_reviewed.py` and `analysis.py` pipeline. The
explicit `body_membership.csv` admits K12 as B0 only and excludes the Hawaz candidate on tissue
identity; `variant=without_oman_fragments` reconstructs the former inventory. Bounds and allocation
diagnostics for both inventories come from the same current analysis. The earlier additive outputs
are retained as archived provenance, with their receipt bound to historical commit `df805b2`.

<!-- table:oman -->
| Reading | Oman | Units | Oldest | Const. | PBDB | PBDB −plant | Decl. 25 | Decl. 10 | −plant × decl. 10 |
|---------|-------:|-----:|-----:|-----:|-----:|----------:|-------:|-------:|----------------:|
| main | included | 76/78 | 452.8 | 455.19 | 456.62 | 456.09 | 465.21 | none | none |
| main | excluded | 75/77 | 432.9 | 434.51 | 436.38 | 435.73 | 437.16 | none | none |
| inclusive | included | 80/82 | 452.8 | 455.06 | 456.43 | 455.92 | 464.40 | none | none |
| inclusive | excluded | 79/81 | 445.2 | 447.20 | 448.27 | 447.85 | 452.98 | none | none |
<!-- /table:oman -->
**Table S3b.** Land-plant body (B0) bounds (Ma) with the Katian Oman fragments included (canonical) and excluded, Emsian cutoff. Units: guaranteed/possible; Oldest: oldest possible age. History abbreviations: Const., constant; PBDB, proportional to PBDB land and marginal-marine collection density; PBDB −plant, the same with plant-matched collections removed; Decl. 25 and Decl. 10, exponential decline into the past on 25 and 10 Myr timescales; −plant × decl. 10, their product. "None": no bound within the 469.4 Ma limit of the declared domain.

With the fragments, the oldest unit is Katian, followed by more than 12 Myr with no body unit, and every
declared history fits the sequence poorly (Table S7)[]{.C41}. The bounds move about 20 Myr older[]{.C40}. Under the
inclusive reading without Oman, the Hirnantian Zbrza axes are the oldest unit and give [447.20]{.C29} Ma under constant
intensity. Neither
inventory supplies a lag or delay: the 458.2 Ma cryptospore value is a fossil minimum, not an origin, and
the bounds are model-conditioned endpoints. The comparison shows how far an endpoint bound depends on its
oldest admitted unit.

**Table S13.** Pivotal records: what each shows directly, how we use it, and what a crown claim would
additionally need.

| Record | Observed or documented | Age support | Our use | A crown claim would also need |
|---|---|---|---|---|
| Ghaba-1 fragments, Oman [@wellman2003FragmentsEarliestLand] | Sporangial fragments with in situ cryptospores, some with a sporangial covering; no preserved associated axes or demonstrated conducting tissue | Katian on later correlation (Caradoc in the original) | Land-plant body, one unit | Characters placing the producer in a crown group; not a polysporangiophyte or crown member |
| Borenshult-1 triletes, Sweden [@rubinstein2019BalticaCradleEarly] | Possible trilete at 48.2 m; definite triletes from 43.1 m; the figures disagree at 41.1 m | Sandbian; the oldest definite level lies below the 454.41 Ma bentonite | The 459.1 Ma maximum's basis; a weak absence screen | An argument placing the producer in the crown; a trilete mark alone does not |
| *Cooksonia barrandei*, Czech Republic [@libertin2018SporophytesPolysporangiateLand] | Branched fertile sporophyte with terminal sporangia and in situ trilete spores; no tracheids reported | Sheinwoodian, horizon inferred from slab fauna and correlation | Oldest polysporangiophyte | Placement on the lycophyte or euphyllophyte side; tracheids alone would not suffice |
| Irish Homerian axes [@edwards1980RecordsCooksoniatypeSporangia] | Fragmentary sporangia on short axes, one branched; no tracheids seen | Late Homerian graptolite zone | Hooper et al.'s 431.2 Ma anchor | As for *C. barrandei* |
| Yea *Baragwanathia*, Victoria | Microphyllous leafy axes; no reproductive structures reported from the material claimed as Silurian [@libertin2024GenusAberlemniaSiluriandevonian] | Gorstian on graptolites versus Early Devonian on brachiopods and mapping [@earp2024NotanopliidBrachiopodsAssociated]; full range carried | Influential crown vascular-plant unit | Matching the competing dates to the exact horizons |
| Bathurst Island zosterophylls, Arctic Canada [@kotyk2002MorphologicallyComplexPlant] | Fertile zosterophylls in spikes and clusters | Late Ludlow on conodonts, graptolites and brachiopods; possibly Pridoli | Influential crown vascular-plant unit (lycophyte line) | None for crown Tracheophyta; not crown Lycophyta |

### S5.2 The endpoint calculation

For a fixed younger cutoff $c$, let $U(a)=\int_c^a w(s)\,ds$ be cumulative recovery. Conditional on $n$
independent units with ages drawn with density proportional to $w$ on $[c,T]$, the maximum $A$ satisfies
$P(A\leq a)=\{U(a)/U(T)\}^n$. Inverting at 0.05 gives the exact one-sided 95% older bound

$$U(T_{\mathrm{upper}})=U(A)\,0.05^{-1/n}.$$

The absolute recovery rate cancels. For constant $w$ this is the Strauss and Sadler [@strauss1989ClassicalConfidenceIntervals] and Marshall [@marshall1990ConfidenceIntervalsStratigraphic] expression with a fixed cutoff, which uses all $n$ observations. Marshall [-@marshall1994ConfidenceIntervalsStratigraphic; -@marshall1997ConfidenceIntervalsStratigraphic] and Wang et al. [@wang2016AdaptiveCredibleIntervals] relax the assumption of uniform recovery in other ways. A bound beyond the declared history's
domain (469.4 Ma, where the held PBDB effort series ends) is reported as *not bounded within the domain*,
not as an infinite-age inference.

**Age envelope.** The primary age treatment uses the greatest possible oldest age and the smallest number
of units guaranteed older than $c$. The bound increases with $A$ and decreases with $n$, so this is an
envelope of the exact-age bounds whenever every reported age interval contains the true age. That
geological condition is separate from statistical coverage. Independent-uniform and shared-quantile
allocations (256 draws, case-keyed seeds rooted at 20261102) are reported as sensitivities. Their quantiles are not confidence
bounds (Table S8).

**Histories.** Six histories are fixed without fitting them to the focal fossils:

1. constant recovery in calendar time;
2. PBDB all-taxa land and marginal-marine collections per Myr, apportioned by age overlap;
3. the same, with collections matching the held plant-filtered extract removed;
4. exponential decline into the past, 25 Myr timescale;
5. exponential decline into the past, 10 Myr timescale;
6. the plant-excluded density multiplied by the 10 Myr decline.

Plant exclusion is a response-related filter, not verified independent effort. No proxy establishes
actual search opportunities. Cutoffs are the ends of the Emsian, Pragian, Lochkovian and Pridoli.

**Shape diagnostics.** Conditional on the maximum, the remaining unit ages should be distributed as
$U(a)/U(A)$. Kolmogorov–Smirnov statistics at midpoint ages and across age draws expose histories that
fit the observed sequence poorly (Table S7). Table S7 reports every declared age treatment: midpoint ages,
independent uniform draws within each range and a shared quantile applied to all ranges. No probability
law for ages within ranges was declared, so none is preferred. For crown vascular-plant bodies, constant
recovery fits under independent draws but not at midpoint ages or shared quantiles; the 10 Myr decline
fits poorly under all three. The robust result is discrimination against steep declines, not support for
constant recovery. The *p* values are asymptotic Kolmogorov–Smirnov values computed on allocated ages
treated as exact, not exact finite-sample tests, and their spread across draws is a set of percentiles,
not a combined test for interval-dated fossils, a model-selection criterion or an empirical calibration.
**Interval feasibility.** A history that fails under the allocations drawn may fit another allocation
that the ranges admit; the GPT-6 Pro review constructed such allocations for the 25 Myr decline. For each
category and history, `models/f3/loop3/interval_feasibility.py` finds the admissible allocation that
minimises the Kolmogorov–Smirnov distance $D$. Each unit's age support becomes an interval of
transformed exposure; compatibility of a unit with an order-statistic rank changes only at finitely many
values of the maximum's exposure, so the search enumerates every such event point and the open cells
between them and solves a bipartite matching in each, bracketing the global minimum of $D$ to within
$5 \times 10^{-11}$. The two units in each category whose support straddles the Emsian cutoff may fall below it
and leave the conditional sample, so all four inclusion states are searched. The cutoff is held at
393.47 Ma; shared boundary shifts are treated separately (S5.3). Table S7b displays, for each state and
history, the finite-sample *p* at the best allocation, and flags where the asymptotic reference would
change the classification; both values are in the source CSV. Where no allocation reaches 0.05 these are
upper bounds, so the failure holds for every allocation within the recorded supports; where one does, the
allocation file is a witness.

**What a failure and a pass mean.** Fix the recording history, cutoff, timescale, inventory and unit
rule. Let $z$ be the latent exact ages and inclusion state, $S$ the allocations allowed by the recorded
supports, and $p(z)$ the finite-sample conditional-on-count-and-maximum KS *p* value under independent
continuous occurrence ages. The interval rule rejects only if every $z'\in S$ has $p(z')<\alpha$.
Under an observation model in which the reported intervals contain the latent ages almost surely, the
true allocation belongs to $S$, so this rejection event is a subset of rejection by the level-$\alpha$
exact-age test. It is therefore conservative. If containment can fail with probability $\delta$, the
direct size bound is instead $\alpha+\delta$; these geological ranges have no demonstrated joint
coverage. The maximisation resembles maximised-*p* constructions [@berger1994PValuesMaximized], but here
the intervals coarsen observations rather than form a confidence set for a nuisance parameter.
Enumerating all cutoff-inclusion states preserves the argument when the true state is included. A
passing witness is an admissible allocation, not an estimated chronology, evidence of model adequacy or
a ranking of histories. A coherent section chronology could remove a passing allocation but cannot
rescue an interval-wide failure if it contains the truth. A
separate brute-force permutation implementation (Codex) agreed on 720 fixed-$D$ decisions and 120 optimum
brackets, and Claude recomputed $D$ from the decisive witness files; the GPT-6 Pro follow-up review
independently checked small cases and all 48 saved witnesses.

<!-- table:interval -->
| Category | Units | Const. | PBDB | PBDB −plant | Decl. 25 | Decl. 10 | −plant × decl. 10 |
|--------|------------------:|-----:|-----:|----------:|-------:|-------:|----------------:|
| B2 | 48 guaranteed | 0.985 | 0.722 | 0.256 | 0.035* | 3e-06* | 0.045† |
| B2 | 49 (one straddling) | 0.994 | 0.667 | 0.217 | 0.049† | 6e-06* | 0.051 |
| B2 | 50 possible | 0.998 | 0.612 | 0.184 | 0.067 | 9e-06* | 0.057 |
| B0 +Oman | 76 guaranteed | 3e-07* | 9e-05* | 1e-06* | 0.002* | 5e-17* | 6e-08* |
| B0 +Oman | 77 (one straddling) | 2e-07* | 8e-05* | 8e-07* | 0.003* | 1e-16* | 9e-08* |
| B0 +Oman | 78 possible | 2e-07* | 7e-05* | 6e-07* | 0.004* | 3e-16* | 1e-07* |
<!-- /table:interval -->
**Table S7b.** Best attainable conditional-age diagnostic over all admissible allocations, main reading, Emsian cutoff: finite-sample *p* at the most favourable allocation. * no admissible allocation reaches *p* = 0.05, so the history fails this diagnostic for every age assignment within the recorded supports; † fails under the finite-sample reference but reaches 0.05 under the asymptotic one. Units: number inside the window, by inclusion of the units that straddle the cutoff (either of the two gives the same result). A failure is a conservative rejection only if the supports contain the true ages (see text); a pass is a possibility, not a fit (`models/f3/loop3/out/stage2_interval/`).

Under the finite-sample reference, for crown-member bodies the 10 Myr decline fails in every inclusion
state. The 25 Myr decline passes with all 50 possible units, falls just short with one straddling unit
(*p* = 0.049, which passes only asymptotically) and fails with the 48 guaranteed units. The plant-excluded
density times the 10 Myr decline passes with 49 or 50 units but not 48. For canonical land-plant bodies,
every history fails in every state under either reference.

### S5.3 Results and sensitivities

**Table labels.** B0 +Oman is the canonical land-plant body category; B0 -Oman excludes the
Ghaba-1 fragments; B1 is the E3-or-E5 polysporangiophyte category; B2 is crown vascular-plant
membership. Const. is constant intensity; PBDB is all-collection density; PBDB -plant removes
plant-matched collections; Decl. 25/10 denotes the exponential time constant in Myr. Indep. is
independent-uniform age allocation; shared q places every unit at a common within-range quantile.

<!-- table:primary -->
| Reading | Category | Units | Oldest | Const. | PBDB | PBDB −plant | Decl. 25 | Decl. 10 | −plant × decl. 10 |
|---------|-------:|-----:|-----:|-----:|-----:|----------:|-------:|-------:|----------------:|
| main | B0 +Oman | 76/78 | 452.8 | 455.19 | 456.62 | 456.09 | 465.21 | none | none |
| main | B1 | 69/71 | 432.9 | 434.65 | 436.68 | 435.98 | 437.57 | none | none |
| main | B2 | 48/50 | 426.7 | 428.84 | 428.88 | 428.45 | 431.63 | none | none |
| inclusive | B0 +Oman | 80/82 | 452.8 | 455.06 | 456.43 | 455.92 | 464.40 | none | none |
| inclusive | B1 | 73/75 | 445.2 | 447.37 | 448.53 | 448.07 | 453.76 | none | none |
| inclusive | B2 | 53/55 | 426.7 | 428.63 | 428.67 | 428.28 | 431.10 | none | 468.65 |
<!-- /table:primary -->
**Table S3.** Conservative 95% older bounds (Ma) by category, reading and recording history from the canonical inventory, in which B0 includes the Oman fragments (Table S3b compares B0 with and without them); Emsian cutoff. Units: guaranteed/possible; Oldest: oldest possible age. History abbreviations: Const., constant; PBDB, proportional to PBDB land and marginal-marine collection density; PBDB −plant, the same with plant-matched collections removed; Decl. 25 and Decl. 10, exponential decline into the past on 25 and 10 Myr timescales; −plant × decl. 10, their product. "None": no bound within the 469.4 Ma limit of the declared domain.

<!-- table:cutoffs -->
| Cutoff (Ma) | Units | Const. | PBDB | PBDB −plant | Decl. 25 | Decl. 10 | −plant × decl. 10 |
|-------------------|-----:|-----:|-----:|----------:|-------:|-------:|----------------:|
| Emsian (393.47) | 48 | 428.84 | 428.88 | 428.45 | 431.63 | none | none |
| Pragian (410.62) | 25 | 428.75 | 429.71 | 429.43 | 429.75 | 433.80 | 451.56 |
| Lochkovian (413.02) | 18 | 429.18 | 430.09 | 429.81 | 430.24 | 434.25 | 447.52 |
| Pridoli (419.62) | 13 | 428.53 | 428.54 | 428.35 | 428.92 | 429.80 | 429.55 |
<!-- /table:cutoffs -->
**Table S4.** Crown vascular-plant bounds (Ma) by younger cutoff, main reading. Abbreviations as in Table S3.

<!-- table:units -->
| B2 unit or source variant | Units | Constant | PBDB density | Decline 25 Myr |
|-----------------------------------|-----:|-------:|-----------:|-------------:|
| Individual collections/observations | 78 | 428.00 | 428.03 | 429.58 |
| Locality–age proxies (primary) | 48 | 428.84 | 428.88 | 431.63 |
| Whole localities | 47 | 428.89 | 428.93 | 431.75 |
| Region–stage cells | 19 | 432.38 | 432.16 | 442.78 |
| Wide-age records restored | 73 | 428.09 | 428.12 | 429.79 |
| Uncertain material restored | 54 | 428.60 | 428.63 | 431.01 |
| Low-confidence names omitted | 46 | 428.94 | 428.98 | 431.87 |
| Weak botanical source omitted | 48 | 428.84 | 428.88 | 431.63 |
| Kosov/Podolia links collapsed | 47 | 428.89 | 428.93 | 431.75 |
| Curated oldest-record set only | 15 | 434.05 | 434.62 | 450.50 |
<!-- /table:units -->
**Table S5.** Crown vascular-plant bounds under alternative units and source choices (main reading, Emsian cutoff). Region–stage cells use midpoint stage and are a deliberately coarse dependence diagnostic.

<!-- table:regions -->
| Region left out | Units | Oldest possible | Constant | PBDB density |
|-----------------------------|-----:|--------------:|-------:|-----------:|
| Gondwana Australia Antarctica | 44 | 425.0 | 427.22 | 427.33 |
| Gondwana South America | 47 | 426.7 | 428.89 | 428.87 |
| peri Gondwana Europe | 47 | 426.7 | 428.89 | 428.85 |
| Baltica | 45 | 426.7 | 428.99 | 431.80 |
| Avalonia | 44 | 426.7 | 429.04 | 428.95 |
| Kazakhstania | 44 | 426.7 | 429.04 | 429.08 |
| South China | 43 | 426.7 | 429.10 | 429.06 |
| multiple | 42 | 426.7 | 429.16 | 428.74 |
| Laurentia | 28 | 426.7 | 430.45 | 429.58 |
<!-- /table:regions -->
**Table S6.** Leave-one-region-out bounds for crown vascular-plant members, with PBDB exposure recomputed after the same omission. Regions are approximate modern country/state assignments.

**Shared timescale boundaries.** The bounds above take stage boundaries as fixed. Five deterministic
scenarios (`models/f3/loop3/timescale_sensitivity.py`) move every boundary in `data/timescale.csv` at once:
baseline; all one quoted uncertainty younger; all one older; and two alternating patterns, scaled to
0.7345 and 0.5610 of the quoted uncertainties so that stage order is kept. Each shifted boundary moves
curated stage-based endpoints, the cutoff, the analysis domain and the effort-stage widths together. A
PBDB numerical interval moves only when both of its endpoints match project boundaries (27 of 35 PBDB
crown-member units); otherwise its numbers are kept, because an equal number does not show that the
source used the ICS boundary. The maximum is compared three ways: the published 431.2 Ma held fixed; 431.2
Ma moved to the same fractional position between the shifted Homerian and Sheinwoodian bases; and Hooper
et al.'s rule reapplied on the current scale, the shifted Homerian base plus the 1.3 Myr uncertainty the
current table quotes for it (431.9 Ma at baseline, against the 431.2 Ma their GTS2012 value gives). The
constant-intensity bound stays younger than the maximum under all three comparisons in every scenario,
with margins of [−4.65]{.C50 .V088} to [−0.71]{.C50 .V089} Myr; the two collection-density histories also stay younger. The
25 Myr decline crosses in both directions. Scenarios with an older cutoff have 47 guaranteed units
because one PBDB support (393.47–399.5 Ma) keeps its numerical younger end. These are sensitivity
scenarios, not a probability distribution over geological ages.

<!-- table:timescale -->
| Scenario | Cutoff | Units | Const. | PBDB | PBDB −plant | Decl. 25 | 431.2 mapped | Source rule |
|-------------|-----:|-----:|-----:|-----:|----------:|-------:|-----------:|----------:|
| baseline | 393.47 | 48 | 428.84 | 428.88 | 428.45 | 431.63 | 431.20 | 431.90 |
| all younger | 392.48 | 48 | 427.31 | 427.53 | 427.08 | 429.98 | 429.93 | 430.60 |
| all older | 394.46 | 47 | 430.42 | 430.35 | 429.90 | 433.41 | 432.47 | 433.20 |
| alternating a | 394.20 | 47 | 430.01 | 429.05 | 428.78 | 432.96 | 430.72 | 430.95 |
| alternating b | 392.91 | 48 | 427.98 | 428.64 | 428.11 | 430.70 | 431.56 | 432.63 |
<!-- /table:timescale -->
**Table S6b.** Crown vascular-plant bounds (Ma) under shared boundary scenarios, main reading, Emsian cutoff (shifted with the scenario). Units: guaranteed. "431.2 mapped": the published maximum held at its fractional position in the shifted Homerian; "Source rule": shifted Homerian base plus its quoted 1.3 Myr uncertainty (`models/f3/loop3/out/stage2_timescale/`).

**Influential records.** Leave-group-out comparisons at the same unit rule and cutoff
(`models/f3/loop3/out/influential_taxa.csv`) remove the records that set the oldest ages. Under constant
intensity, removing the three Yea *Baragwanathia* units changes the crown-member bound by [−1.67]{.C52 .V090} Myr
(younger): the oldest age falls to the Bathurst Island 425.0 Ma support. Removing the five Bathurst Island
units changes it by [0.26]{.C52 .V091} Myr (older), because Yea remains oldest while the count falls. Removing
*C. barrandei* changes the polysporangiophyte bound by [−2.38]{.C52 .V092} Myr but canonical B0 by only [0.03]{.C52 .V093} Myr,
because the Oman unit sets B0's oldest age. Under other histories and readings the signs can change, since loss of count and loss
of the oldest record pull in opposite directions. A leave-out is a leverage diagnostic, not a
reidentification of any fossil.

<!-- table:shape -->
| Category | History | Nominal p, midpoint ages | Independent-uniform ages, 5–95% | Shared-quantile ages, 5–95% |
|--------|----------------:|-----------------------:|------------------------------:|--------------------------:|
| B0 +Oman | Const. | 5.5e-12 | 3.1e-13–4e-09 | 2.9e-12–1.2e-11 |
| B0 +Oman | PBDB | 7.5e-08 | 9.1e-09–4.1e-06 | 2.1e-09–1.6e-07 |
| B0 +Oman | PBDB −plant | 1.1e-10 | 9.4e-12–1.6e-08 | 2.5e-12–2.7e-10 |
| B0 +Oman | Decl. 25 | 6.3e-06 | 3.8e-06–0.00086 | 2e-16–0.00045 |
| B0 +Oman | Decl. 10 | 7.4e-20 | 1.2e-21–8.5e-17 | 1e-39–2.8e-16 |
| B0 +Oman | −plant × decl. 10 | 1.2e-08 | 1.1e-09–1.3e-07 | 4.6e-16–6.3e-08 |
| B0 -Oman | Const. | 0.0066 | 0.004–0.055 | 1.1e-09–0.0062 |
| B0 -Oman | PBDB | 0.02 | 0.0095–0.091 | 0.00033–0.022 |
| B0 -Oman | PBDB −plant | 0.0019 | 0.00074–0.03 | 4.4e-05–0.0047 |
| B0 -Oman | Decl. 25 | 1.2e-07 | 4.9e-09–3.2e-06 | 2e-21–1.9e-06 |
| B0 -Oman | Decl. 10 | 2.5e-20 | 4.3e-22–3.7e-17 | 1.4e-40–8.4e-17 |
| B0 -Oman | −plant × decl. 10 | 3.9e-09 | 3.2e-10–5.2e-08 | 1.7e-16–1.4e-08 |
| B1 | Const. | 0.006 | 0.0058–0.082 | 8.7e-09–0.0063 |
| B1 | PBDB | 0.017 | 0.011–0.14 | 0.00049–0.034 |
| B1 | PBDB −plant | 0.0014 | 0.00095–0.032 | 4.6e-05–0.0043 |
| B1 | Decl. 25 | 5.9e-07 | 5.6e-08–2.1e-05 | 1.6e-19–2e-05 |
| B1 | Decl. 10 | 1.6e-18 | 2.9e-20–5.1e-15 | 4.4e-37–1.4e-14 |
| B1 | −plant × decl. 10 | 1.7e-07 | 7.5e-09–1.2e-06 | 5.2e-15–4e-07 |
| B2 | Const. | 0.0085 | 0.056–0.71 | 3.1e-09–0.016 |
| B2 | PBDB | 0.0092 | 0.016–0.24 | 2.7e-05–0.058 |
| B2 | PBDB −plant | 8.6e-05 | 0.00022–0.019 | 2.2e-06–0.019 |
| B2 | Decl. 25 | 4.9e-06 | 4.9e-05–0.016 | 4.6e-16–0.0019 |
| B2 | Decl. 10 | 3.1e-13 | 1.6e-11–5.1e-07 | 3.5e-26–8e-07 |
| B2 | −plant × decl. 10 | 1.5e-05 | 0.001–0.042 | 5.9e-11–0.0064 |
<!-- /table:shape -->
**Table S7.** Within-record shape diagnostics (conditional-on-maximum Kolmogorov–Smirnov), main reading, under each declared age treatment. Ranges are the 5th–95th percentiles of nominal *p* across 256 age draws, not minimum-to-maximum ranges.

<!-- table:ages -->
| Category | History | Allocation | 5% | Median | 95% | Unbounded fraction |
|--------|-------:|---------:|-----:|-----:|-----:|-----------------:|
| B0 +Oman | Const. | indep. | 447.70 | 451.38 | 454.82 | 0.00 |
| B0 +Oman | PBDB | indep. | 448.82 | 452.47 | 456.20 | 0.00 |
| B0 +Oman | Decl. 25 | indep. | 453.81 | 459.13 | 464.39 | 0.00 |
| B0 +Oman | Const. | shared q | 447.67 | 451.19 | 454.74 | 0.00 |
| B0 +Oman | PBDB | shared q | 448.78 | 452.27 | 456.10 | 0.00 |
| B0 +Oman | Decl. 25 | shared q | 453.89 | 458.73 | 464.17 | 0.00 |
| B0 -Oman | Const. | indep. | 432.27 | 433.50 | 434.38 | 0.00 |
| B0 -Oman | PBDB | indep. | 432.04 | 433.84 | 436.06 | 0.00 |
| B0 -Oman | Decl. 25 | indep. | 434.48 | 435.91 | 436.97 | 0.00 |
| B0 -Oman | Const. | shared q | 432.23 | 433.27 | 434.35 | 0.00 |
| B0 -Oman | PBDB | shared q | 432.00 | 433.27 | 435.99 | 0.00 |
| B0 -Oman | Decl. 25 | shared q | 434.48 | 435.66 | 436.90 | 0.00 |
| B1 | Const. | indep. | 432.35 | 433.32 | 434.51 | 0.00 |
| B1 | PBDB | indep. | 432.10 | 433.31 | 436.33 | 0.00 |
| B1 | Decl. 25 | indep. | 434.79 | 435.93 | 437.35 | 0.00 |
| B1 | Const. | shared q | 432.36 | 433.40 | 434.48 | 0.00 |
| B1 | PBDB | shared q | 432.11 | 433.55 | 436.28 | 0.00 |
| B1 | Decl. 25 | shared q | 434.85 | 436.03 | 437.28 | 0.00 |
| B2 | Const. | indep. | 424.24 | 426.24 | 427.69 | 0.00 |
| B2 | PBDB | indep. | 425.05 | 426.64 | 427.80 | 0.00 |
| B2 | Decl. 25 | indep. | 426.13 | 428.43 | 430.19 | 0.00 |
| B2 | Const. | shared q | 421.58 | 424.10 | 427.03 | 0.00 |
| B2 | PBDB | shared q | 421.22 | 424.81 | 427.18 | 0.00 |
| B2 | Decl. 25 | shared q | 423.10 | 425.92 | 429.34 | 0.00 |
<!-- /table:ages -->
**Table S8.** Age-allocation sensitivity (Emsian cutoff, main reading). Quantiles across allocations are descriptive, not confidence bounds.

### S5.4 Recovery before the oldest record

After seeing that steep smooth declines fit poorly, we evaluated a complete stage-break grid: flat and
PBDB baselines; breaks at 419.62, 426.7 and 432.9 Ma; older multipliers 1, 0.5, 0.1 and 0.01; all
categories and both readings, with an additional B0 exclusion inventory (192 cells). The 426.7 Ma break coincides with the oldest possible main B2
record, so no main B2 unit's age support is changed and the within-record shape statistic is unchanged.
The grid is a retrospective sensitivity; the 0.05 rule supplies no nominal, simultaneous or
selection-adjusted confidence for it. The 432.9 Ma break is a null control when the bound lies younger.
No member was selected to match a clock (Table S9).

<!-- table:suppression -->
| Baseline | Break (Ma) | Older multiplier | Changes age support? | Older bound (Ma) | Midpoint shape p |
|------------|---------:|---------------:|-------------------:|---------------:|---------------:|
| constant | 419.62 | 1 | True | 428.84 | 0.00848 |
| constant | 419.62 | 0.5 | True | 430.52 | 0.00424 |
| constant | 419.62 | 0.1 | True | 444.00 | 0.00223 |
| constant | 419.62 | 0.01 | True | none | 0.00191 |
| constant | 426.7 | 1 | False | 428.84 | 0.00848 |
| constant | 426.7 | 0.5 | False | 430.98 | 0.00848 |
| constant | 426.7 | 0.1 | False | 448.10 | 0.00848 |
| constant | 426.7 | 0.01 | False | none | 0.00848 |
| constant | 432.9 | 1 | False | 428.84 | 0.00848 |
| constant | 432.9 | 0.5 | False | 428.84 | 0.00848 |
| constant | 432.9 | 0.1 | False | 428.84 | 0.00848 |
| constant | 432.9 | 0.01 | False | 428.84 | 0.00848 |
| PBDB density | 419.62 | 1 | True | 428.88 | 0.00918 |
| PBDB density | 419.62 | 0.5 | True | 430.60 | 0.0186 |
| PBDB density | 419.62 | 0.1 | True | 451.09 | 0.00729 |
| PBDB density | 419.62 | 0.01 | True | none | 0.00576 |
| PBDB density | 426.7 | 1 | False | 428.88 | 0.00918 |
| PBDB density | 426.7 | 0.5 | False | 430.98 | 0.00918 |
| PBDB density | 426.7 | 0.1 | False | 458.47 | 0.00918 |
| PBDB density | 426.7 | 0.01 | False | none | 0.00918 |
| PBDB density | 432.9 | 1 | False | 428.88 | 0.00918 |
| PBDB density | 432.9 | 0.5 | False | 428.88 | 0.00918 |
| PBDB density | 432.9 | 0.1 | False | 428.88 | 0.00918 |
| PBDB density | 432.9 | 0.01 | False | 428.88 | 0.00918 |
<!-- /table:suppression -->
**Table S9.** Retrospective stage-break grid for crown vascular-plant members, main reading (`models/f3/loop3/out/suppression_sensitivity.csv`).

**The age–intensity frontier.** The grid fixes multipliers and reads off bounds. The frontier inverts it:
for a candidate lineage age $T$ and an assumed delay $d$ before recoverable diagnostic bodies, what ratio
of earlier to later recording intensity puts the corresponding recoverability start $T-d$ exactly on the
95% bound? With constant later intensity, a step at the oldest possible age $A$,
fixed cutoff $c$ and $n$ guaranteed units, the earlier exposure needed is $(A-c)(0.05^{-1/n}-1)$, and the
ratio is that exposure divided by $T-d-A$ (`models/f3/loop3/frontier.py`). A ratio above one means no reduction is needed. Where
$T-d \le A$ the contour is undefined in this parameterisation (shown as —), which does not exclude the
combination, because the oldest fossil may be younger within its support. The step's position is chosen
from the data and the contour is not a fitted rate, a likelihood surface or a joint confidence region. The
delay and the earlier rate are not separately identifiable from positive records: a longer delay needs
less suppression for the same $T$.

<!-- table:frontier -->
| Units | Delay (Myr) | 431.2 Ma | 440 Ma | 444 Ma | 447 Ma | 452 Ma |
|----------------------|----------:|-------:|-----:|-----:|-----:|-----:|
| Locality–age (primary) | 0 | 0.476 | 0.161 | 0.124 | 0.105 | 0.085 |
| Locality–age (primary) | 5 | — | 0.258 | 0.174 | 0.140 | 0.105 |
| Locality–age (primary) | 10 | — | 0.648 | 0.293 | 0.208 | 0.140 |
| Locality–age (primary) | 20 | — | — | — | 7.133 | 0.404 |
| Region–stage | 0 | 1.261 | 0.427 | 0.328 | 0.280 | 0.224 |
| Region–stage | 5 | — | 0.684 | 0.461 | 0.371 | 0.280 |
| Region–stage | 10 | — | 1.720 | 0.777 | 0.551 | 0.371 |
| Region–stage | 20 | — | — | — | 18.917 | 1.071 |
| Curated oldest set | 0 | 1.632 | 0.552 | 0.425 | 0.362 | 0.290 |
| Curated oldest set | 5 | — | 0.885 | 0.597 | 0.480 | 0.362 |
| Curated oldest set | 10 | — | 2.226 | 1.006 | 0.713 | 0.480 |
| Curated oldest set | 20 | — | — | — | 24.486 | 1.386 |
<!-- /table:frontier -->
**Table S9b.** Retrospective age–intensity frontier for crown vascular-plant members, main reading, Emsian cutoff: earlier/later recording intensity at which each candidate lineage age lies on the conservative 95% bound, by unit treatment and assumed delay (`models/f3/loop3/out/frontier.csv`). Primary units: 48 guaranteed; region–stage: 19; curated: 15; oldest possible age 426.7 Ma in each.

### S5.5 Biological delay

Fixed delays of 0, 5, 10 and 20 Myr map the recoverability bound to a lineage bound and shift the
lineage domain by the same amount. A delay is an assumed mapping, not inferred from this record or
transferred from the spore comparison (Table S10).

<!-- table:delay -->
| Category | Assumed delay (Myr) | Recoverability bound | Lineage bound |
|--------|------------------:|-------------------:|------------:|
| B0 +Oman | 0 | 455.19 | 455.19 |
| B0 +Oman | 5 | 455.19 | 460.19 |
| B0 +Oman | 10 | 455.19 | 465.19 |
| B0 +Oman | 20 | 455.19 | 475.19 |
| B1 | 0 | 434.65 | 434.65 |
| B1 | 5 | 434.65 | 439.65 |
| B1 | 10 | 434.65 | 444.65 |
| B1 | 20 | 434.65 | 454.65 |
| B2 | 0 | 428.84 | 428.84 |
| B2 | 5 | 428.84 | 433.84 |
| B2 | 10 | 428.84 | 438.84 |
| B2 | 20 | 428.84 | 448.84 |
<!-- /table:delay -->
**Table S10.** Fixed-delay mapping, constant recovery, main reading.

### S5.6 Simulation checks

Each of 144 cells has 3,000 replicates (seed 20261101) at the reviewed unit counts and recoverability
endpoints of 432, 445 and 458.2 Ma. Each correctly specified history is checked with exact and
stage-censored dates. The checks then mismatch constant and steeply declining histories, repeat
underlying units two or four times, and impose 10 or 20 Myr delays with and without the correct
adjustment. Coverage counts no-bound outcomes as covering. Claim frequency and coverage among bounded
claims are reported separately, because 95% unconditional coverage does not imply 95% coverage after
selecting bounded outcomes. These runs verify the declared procedures and expose their failure modes.
They do not qualify the fossils (Table S11; all categories in `simulation_results.csv`).

<!-- table:simulation -->
| Scenario | True | Fitted | Ages | Dup. | True delay | Adj. | Claims | Coverage (95% CI) |
|-------------------------------|----------------:|----------------:|-------------:|-----:|---------:|-----:|-----:|------------------:|
| matched | Const. | Const. | exact | 1 | 0 | 0.0 | 1.000 | 0.955 (0.947–0.962) |
| matched | Const. | Const. | stage envelope | 1 | 0 | 0.0 | 1.000 | 1.000 (0.998–1.000) |
| matched | Const. | Const. | exact | 1 | 0 | 0.0 | 1.000 | 0.949 (0.941–0.957) |
| matched | Const. | Const. | stage envelope | 1 | 0 | 0.0 | 1.000 | 0.985 (0.980–0.989) |
| matched | Const. | Const. | exact | 1 | 0 | 0.0 | 1.000 | 0.945 (0.936–0.953) |
| matched | Const. | Const. | stage envelope | 1 | 0 | 0.0 | 1.000 | 0.983 (0.977–0.987) |
| matched | Decl. 25 | Decl. 25 | exact | 1 | 0 | 0.0 | 1.000 | 0.945 (0.936–0.952) |
| matched | Decl. 25 | Decl. 25 | stage envelope | 1 | 0 | 0.0 | 1.000 | 0.956 (0.948–0.963) |
| matched | Decl. 25 | Decl. 25 | exact | 1 | 0 | 0.0 | 1.000 | 0.958 (0.951–0.965) |
| matched | Decl. 25 | Decl. 25 | stage envelope | 1 | 0 | 0.0 | 1.000 | 0.990 (0.985–0.993) |
| matched | Decl. 25 | Decl. 25 | exact | 1 | 0 | 0.0 | 0.212 | 0.941 (0.932–0.949) |
| matched | Decl. 25 | Decl. 25 | stage envelope | 1 | 0 | 0.0 | 0.070 | 0.966 (0.959–0.972) |
| matched | Decl. 10 | Decl. 10 | exact | 1 | 0 | 0.0 | 0.139 | 0.950 (0.942–0.958) |
| matched | Decl. 10 | Decl. 10 | stage envelope | 1 | 0 | 0.0 | 0.078 | 0.998 (0.996–0.999) |
| matched | Decl. 10 | Decl. 10 | exact | 1 | 0 | 0.0 | 0.065 | 0.949 (0.940–0.956) |
| matched | Decl. 10 | Decl. 10 | stage envelope | 1 | 0 | 0.0 | 0.034 | 0.966 (0.959–0.972) |
| matched | Decl. 10 | Decl. 10 | exact | 1 | 0 | 0.0 | 0.053 | 0.950 (0.941–0.957) |
| matched | Decl. 10 | Decl. 10 | stage envelope | 1 | 0 | 0.0 | 0.032 | 0.968 (0.961–0.974) |
| matched | PBDB | PBDB | exact | 1 | 0 | 0.0 | 1.000 | 0.950 (0.942–0.958) |
| matched | PBDB | PBDB | stage envelope | 1 | 0 | 0.0 | 1.000 | 0.999 (0.998–1.000) |
| matched | PBDB | PBDB | exact | 1 | 0 | 0.0 | 1.000 | 0.957 (0.949–0.963) |
| matched | PBDB | PBDB | stage envelope | 1 | 0 | 0.0 | 1.000 | 0.967 (0.960–0.973) |
| matched | PBDB | PBDB | exact | 1 | 0 | 0.0 | 1.000 | 0.953 (0.945–0.960) |
| matched | PBDB | PBDB | stage envelope | 1 | 0 | 0.0 | 1.000 | 0.999 (0.998–1.000) |
| matched | PBDB −plant | PBDB −plant | exact | 1 | 0 | 0.0 | 1.000 | 0.954 (0.946–0.961) |
| matched | PBDB −plant | PBDB −plant | stage envelope | 1 | 0 | 0.0 | 1.000 | 1.000 (0.998–1.000) |
| matched | PBDB −plant | PBDB −plant | exact | 1 | 0 | 0.0 | 1.000 | 0.948 (0.939–0.955) |
| matched | PBDB −plant | PBDB −plant | stage envelope | 1 | 0 | 0.0 | 1.000 | 0.983 (0.977–0.987) |
| matched | PBDB −plant | PBDB −plant | exact | 1 | 0 | 0.0 | 1.000 | 0.952 (0.944–0.959) |
| matched | PBDB −plant | PBDB −plant | stage envelope | 1 | 0 | 0.0 | 1.000 | 0.954 (0.946–0.961) |
| matched | −plant × decl. 10 | −plant × decl. 10 | exact | 1 | 0 | 0.0 | 0.175 | 0.951 (0.943–0.958) |
| matched | −plant × decl. 10 | −plant × decl. 10 | stage envelope | 1 | 0 | 0.0 | 0.119 | 0.992 (0.988–0.995) |
| matched | −plant × decl. 10 | −plant × decl. 10 | exact | 1 | 0 | 0.0 | 0.069 | 0.954 (0.946–0.961) |
| matched | −plant × decl. 10 | −plant × decl. 10 | stage envelope | 1 | 0 | 0.0 | 0.049 | 0.951 (0.942–0.958) |
| matched | −plant × decl. 10 | −plant × decl. 10 | exact | 1 | 0 | 0.0 | 0.045 | 0.956 (0.948–0.962) |
| matched | −plant × decl. 10 | −plant × decl. 10 | stage envelope | 1 | 0 | 0.0 | 0.040 | 0.960 (0.953–0.967) |
| history mismatch | Const. | Decl. 10 | exact | 1 | 0 | 0.0 | 0.000 | 1.000 (0.999–1.000) |
| history mismatch | Const. | Decl. 10 | exact | 1 | 0 | 0.0 | 0.000 | 1.000 (0.999–1.000) |
| history mismatch | Const. | Decl. 10 | exact | 1 | 0 | 0.0 | 0.000 | 1.000 (0.999–1.000) |
| history mismatch | Decl. 10 | Const. | exact | 1 | 0 | 0.0 | 1.000 | 0.241 (0.226–0.257) |
| history mismatch | Decl. 10 | Const. | exact | 1 | 0 | 0.0 | 1.000 | 0.104 (0.094–0.116) |
| history mismatch | Decl. 10 | Const. | exact | 1 | 0 | 0.0 | 1.000 | 0.034 (0.028–0.041) |
| duplicated horizons | Const. | Const. | exact | 2 | 0 | 0.0 | 1.000 | 0.782 (0.767–0.797) |
| duplicated horizons | Const. | Const. | exact | 4 | 0 | 0.0 | 1.000 | 0.529 (0.511–0.546) |
| recoverability delay unadjusted | Const. | Const. | exact | 1 | 10 | 0.0 | 1.000 | 0.000 (0.000–0.001) |
| recoverability delay adjusted | Const. | Const. | exact | 1 | 10 | 10.0 | 1.000 | 0.947 (0.938–0.954) |
| recoverability delay unadjusted | Const. | Const. | exact | 1 | 20 | 0.0 | 1.000 | 0.000 (0.000–0.001) |
| recoverability delay adjusted | Const. | Const. | exact | 1 | 20 | 20.0 | 1.000 | 0.952 (0.943–0.959) |
<!-- /table:simulation -->
**Table S11.** Simulation results for crown vascular-plant counts. True and Fitted: generating and fitted recording histories (abbreviations as in Table S3); Dup.: duplication factor; True delay: imposed delay (Myr) between lineage origin and the start of recording; Adj.: delay adjustment applied in the fit; Claims: fraction of replicates giving a bound; Coverage: of the lineage or recording endpoint as targeted, with Wilson 95% interval.

### S5.7 Figures from the reviewed analysis

Figs S4–S6 are the reviewed analysis's own diagnostic figures (`models/f3/loop3/figures_reviewed.py`),
regenerated from the accepted tables: recovery bounds by category, the crown vascular-plant sensitivity
grid and the retrospective suppression grid.

### S5.8 Outside measures of the earlier/later ratio

The frontier (S5.4) gives the ratio of later to earlier finding rate at which a candidate ancestor age,
with zero delay, sits on the 95% limit. To judge whether such a ratio is large, three proxies were
defined before they were computed (`docs/plan-rulers.md`). For a proxy density *x*(*s*), the ratio is the
mean of *x* over 393.47–426.7 Ma divided by its mean over 426.7 Ma to the candidate age, time-weighted
within stages, approximated at 0.01 Myr steps (`models/f3/loop3/rulers.py`). *Rock* is the summed area of active North American
Macrostrat columns holding a non-marine unit at each age [@peters2018MacrostratPlatformGeological]; South
America is reported as a coarser secondary case. *Searching* is the PBDB land and marginal-marine
collection density already used as a recording history [@brook2026FrozenPaleobiologyDatabase]. *Spores*
is the share of Palynodata documents with a usable-age record that report a usable trilete record (not
flagged as reworked, caved, questionable or a synonym-list entry, and not in a rejected document or record
group), counting distinct Palynodata document IDs across regions [@white2008PalynodataDatafile2006]
(`data/spores/effort_global_by_stage.csv`). The last column inverts the closed form of S5.4: the largest
assumed independent-find count at which its numerical ratio equals the required finding-rate ratio.
This is an algebraic comparison, not evidence that the proxy supplies that finding-rate change. It
would represent the endpoint calculation if finding rate were proportional to that proxy throughout
both windows; that transfer is not estimated. Distinct database IDs can still refer to the same
publication, so this is not a fully deduplicated publication count; the bounded duplicate-entry check
is recorded in `docs/audits/2026-11-13-c56-independent-check.md`.

<!-- table:rulers -->
| Measure | 444 Ma | 452 Ma | Largest count matched (444 / 452 Ma) |
|---|--:|--:|--:|
| Rock: North America, non-marine column area | [3.29]{.C56 .V160} | [3.19]{.C56 .V161} | [20.4]{.C56 .V162} / [14.0]{.C56 .V163} |
| Rock: North America, non-marine or mixed area | [3.39]{.C56 .V164} | [3.42]{.C56 .V165} | 21.0 / 14.9 |
| Rock: North America, non-marine unit count | 1.80 | 2.23 | 11.8 / 10.2 |
| Rock: South America, non-marine or mixed area | [1.01]{.C56 .V166} | [0.78]{.C56 .V167} | 7.2 / 4.4 |
| Searching: PBDB land and marginal-marine collections | [1.35]{.C56 .V130} | [1.41]{.C56 .V131} | 9.2 / 7.0 |
| Searching: the same, plant-filter matches removed | [1.07]{.C56 .V168} | [1.12]{.C56 .V169} | 7.5 / 5.8 |
| Spores: share of Palynodata studies reporting triletes | [5.14]{.C56 .V170} | [7.10]{.C56 .V171} | [31.1]{.C56 .V172} / [29.4]{.C56 .V173} |
<!-- /table:rulers -->
**Table S14.** Outside measures: how many times scarcer each proxy was before the oldest crown
vascular-plant find than after it, for ancestors at 444 and 452 Ma with zero delay[]{.C56}.

The measures are rough and do not estimate the finding rate. The North American rock record is patchy: of 54
non-marine input units, 29 overlap 393.47–456 Ma; active columns hold none from 428.25 to 420.39 Ma or
from 445.2 to 443.1 Ma, and much of the later area is Early Devonian. Its ratio is therefore large for candidate ages
just older than the oldest find and settles near three from about 444 Ma; South American rock shows no decline. Collections are dominated by marine animals. The spore
measure is a share of indexed documents, not a count of spores or producers: its denominator includes
acritarch and chitinozoan studies that may not report spores, and changing geographic coverage, study
aims and the recognition of older triletes can move it independently of how common producers were.
Trilete spores were made by a wider group than crown vascular plants, and Palynodata's literature stops
in 2006. A first computation counted rejected record groups and synonym-list entries in the spore
numerator; Sol's review found this departure from the plan, and the corrected share raised the 444 and
452 Ma ratios from 4.98 and 6.67 to the values shown.
The measures bear on different factors (rock on preservation, searching on collection, spores on document
reporting, which producer prevalence affects among other factors); no product is formed.

### S5.9 Shapes of an early rise

For a fixed history with relative finding rate *r*(*s*) before the oldest find *A* and 1 after it, the
probability that all *n* finds are younger than *A*, given a start at *t*, is
$\{(A-c)/[(A-c)+R(t)]\}^n$ with $R(t)=\int_A^t r(s)\,ds$. An ancestor at *t* therefore fits the 95% limit
when $R(t)\le K=(A-c)(0.05^{-1/n}-1)$, whatever the earlier shape of *r* under the common later plateau;
the step of S5.4 is the case of constant
*r*. A linear rise from zero at *t* to 1 at *A* gives $R=(t-A)/2$ and reaches $t=A+2K$. An exponential rise
$r(s)=e^{-(s-A)/\tau}$ gives $R=\tau(1-e^{-(t-A)/\tau})$, which approaches $\tau$ as *t* grows: every
ancestor age fits once $\tau\le K$, equivalently when the doubling time is at most $K\ln 2$.
For $\tau>K$ the endpoint remains finite, $t=A-\tau\ln(1-K/\tau)$; finite-age thresholds and rounded
doubling times must not be substituted for the exact unlimited-age condition. Histories with the same
earlier integral have the same conditional-on-count likelihood when the later rate is held fixed;
the later fossil-age pattern can test that shared plateau but cannot distinguish these earlier
shapes. These are requirements for fitting, not estimates of spread, and the unlimited-age statement
is analytic extrapolation of this family beyond the data domain of S5.2. In
`models/f3/loop3/rise_shapes.py`, piecewise-constant histories verify the linear and exponential
integrals, `endpoint.known_cutoff_summary` additionally confirms the exponential endpoints at 444 and
452 Ma, and the absence of a finite endpoint for $\tau\le K$ follows analytically. The shapes were placed after seeing the record and carry no 95% status.

<!-- table:rises -->
| Independent finds | Allowance *K* (Myr at the later rate) | Linear rise reaches (Ma) | Doubling time, 444 Ma | 452 Ma | 500 Ma | Limit as *t* grows |
|--:|--:|--:|--:|--:|--:|--:|
| 48 | [2.14]{.C57 .V139} | [430.98]{.C57 .V140} | [1.48]{.C57 .V141} | [1.48]{.C57 .V142} | [1.48]{.C57 .V143} | [1.48]{.C57 .V123} |
| 24 | [4.42]{.C57 .V144} | [435.54]{.C57 .V145} | [3.13]{.C57 .V146} | [3.07]{.C57 .V147} | [3.06]{.C57 .V148} | [3.06]{.C57 .V149} |
| 19 | [5.68]{.C57 .V150} | [438.05]{.C57 .V151} | [4.17]{.C57 .V152} | [3.98]{.C57 .V153} | [3.93]{.C57 .V154} | [3.93]{.C57 .V124} |
| 15 | [7.35]{.C57 .V155} | [441.39]{.C57 .V156} | [5.84]{.C57 .V157} | [5.28]{.C57 .V158} | [5.09]{.C57 .V159} | [5.09]{.C57 .V125} |
<!-- /table:rises -->
**Table S15.** Early-rise shapes before the oldest crown vascular-plant find (main interpretation, Emsian
cutoff, zero delay). Doubling time is $\tau\ln 2$ in Myr.

For coarse context, the share of Palynodata documents reporting usable triletes (S5.8) changed from
[0.136]{.C57 .V174} in the Homerian to [0.183]{.C57 .V175} in the Gorstian, an equivalent doubling time of about
[6.6]{.C57 .V126} Myr between stage midpoints, and from [0.016]{.C57 .V176} in the Hirnantian to [0.089]{.C57 .V177}
in the Rhuddanian, about [1.0]{.C57 .V127} Myr. The first comparison spans the oldest find at the
Homerian–Gorstian boundary, so it is not a test of a rise confined to before *A*; placing the Gorstian
level at *A* instead would shorten it to about 4.6 Myr. The share is a reporting measure, not a finding
rate for crown vascular plants.

## S6. From specimens to nodes

The specimen-to-node pilot separates specimen observations, accepted event readings, encounter, trait
persistence and node interpretation (`data/pilot/`, `docs/pilot-traits.md`). We reused its
source-adjudicated combinations, Hooper et al.'s deposited crown-state outputs and the checked
stochastic-map analyses without rerunning them. Aperture (X21) and dispersal unit (X26) were modelled
separately, so their marginal supports do not define a joint ancestral phenotype. The X26 monad category
combines trilete and inaperturate monads; it is not an automatic absence of cryptospory.

For M2, a proximal trilete aperture is modal at the embryophyte crown across the deposited methods and
trees. X26 has a dyad-dominated alternative while X21 stays trilete-dominated, so no joint phenotype
probability follows. On the converged extant-tree runs, [77 of 3,382]{.C19} trilete starts depart along the
path to crown Tracheophyta: conditional persistence [0.977]{.C19} (Monte Carlo SE [0.0026]{.C19}). These trees put crown
Embryophyta at 508 Ma, not at Hooper et al.'s 457–450 Ma. Fixed-rate retention scenarios to 452.8 Ma give
an extant-tree median of [0.989]{.C20} (95% interval [0.895–0.995]{.C20}) from 459.1 Ma and [0.894]{.C20} ([0.332–0.956]{.C20}) from
515.5 Ma. These are model-conditional aperture retention scenarios, not observed survival, and they are
not multiplied into any coverage.

For M3, the *Cooksonia barrandei* holotype links trilete production and multiple sporangia directly, but
its tracheids are unknown[]{.C21}. The Irish Homerian material has a conditional sporangial interpretation and no
direct demonstration of the anatomy known from younger *C. pertoni*. A total-group or stem occurrence and
a crown assignment remain distinct. For M1, cryptospore persistence has not been assessed.

## S7. Analyses superseded during review

Analyses and wording were replaced after independent review. The record is kept so that readers can see what
changed and why.

**The Loop 3 body-record pilot** (`docs/loop3-pilot.md`, provisional, by Claude) reported logistic-ramp
limits of [452.6, 454.1 and 438.0]{.C35 .superseded} Ma for B0, B1 and B2. It read them as favouring the young clock, with a
15–25 Myr preservation lag. Codex's review found:

- stage collection totals passed where per-Myr density was required, counting stage duration twice. The
  unit correction alone moved B0's logistic limit from 452.57 to 436.78 Ma and flipped the selected
  capacity between grid boundaries;
- medians of imputed-age limits presented as 95% limits;
- false replacement of distinct PBDB localities through country, genus and age overlap;
- collection numbers treated as independent beds;
- a category gate that let names judged implausible into B1 and B2;
- two different papers sharing the source identifier `wang2026`.

All were repaired. The fixed-history endpoint calculation (S5.2) replaced the profiled ramp. Its numbers
and interpretation govern; the pilot's do not (`docs/audits/2026-11-01-loop3-methods-review.md`,
`docs/loop3-results.md`).

**The GPT-6 Pro review** (`docs/audits/2026-11-07-gpt6pro-triage.md`). An independent review of commit `60c406b`
found that the earlier drafts described the 515.5 Ma maximum as resting only on affinity, omitting the
published preservation-control argument; kept the Oman fragments out of the primary land-plant inventory;
described the recording rate as fossilisation alone; did not show that 18 of the 28 older Murzuq zeros
are younger than 459.1 Ma; and read shape diagnostics on allocated ages as rejections. All are corrected
here. The analyses it requested (interval feasibility, an age–intensity frontier, shared
timescale-boundary scenarios, Murzuq block dependence, influential-record checks and a public raw-input
rebuild) are reported in S2.5, S5.2–S5.4 and S8 (`docs/audits/2026-11-07-stage2-handoff.md`). Two of
their findings changed earlier statements: no admissible allocation rescues the 10 Myr decline, but some
rescue the 25 Myr decline, which earlier drafts had listed as fitting poorly; and the canonical rebuild's
executable membership test found that E4-only tracheid records had entered the polysporangiophyte
category (S5.1). The 5th–95th percentiles of independent allocations for constant intensity changed from
0.073–0.765 to 0.056–0.715 when the random streams were keyed to each analysis cell; this is a new Monte
Carlo sample, not a data change.

**The GPT-6 Pro follow-up review** (`docs/audits/2026-11-07-gpt6pro-review2-triage.md`) of commit
`342153a` found that the stage-2 admission repair had removed two records from B1 because they lacked an
E3 row, although E3 had never been enumerated for Ludlow and Pridoli records; both have published
branched fertile material and are restored (S5.1). It also found that the Yea entry in the pivotal-record
table listed sporangia that are not reported from the material claimed as Silurian; that the brief
labelled a conditional bound as an earliest start, drew the oldest finds as continuous records, and
compressed the spore-to-capsule interval to "within ten million years"; that the *C. barrandei* anchor
comparison mixed timescales; and that the interval search was reported on the asymptotic reference and
with a blanket statement that optimisation invalidates the tests. All are corrected, and the
finite-sample reference is now primary (S5.2).

**Review C wording** (`docs/audits/2026-11-05-review-c.md`, `docs/audits/2026-11-05-review-c-methods.md`).
The previous draft called the B0–spore separation a demonstrated, observed lag; applied the $\rho f \approx 0.09$
product to both Murzuq history classes when it holds for the constant class only; reported the QSIM
minimum ratios as percentages of all spores (0.307 as 31% rather than a 23.5% share); showed shape
diagnostics for one age treatment only; and presented the tenfold suppression and the 15–23 Myr delays as
if they were estimated. All are corrected here, and the Oman sensitivity was added.

**Loop 2 corrections** (`docs/loop2-close.md`, `docs/audits/2026-11-01-loop2-close-claude-response.md`)
fixed a misread H0c column, an overgeneralised exponent sensitivity, an unsupported circularity claim and
an overstated examination count in an earlier draft.

## S8. Reproduction and navigation

From the repository root:

```sh
make check-public       # public tests; no copyrighted text or private outputs needed
make reproduce-derived  # selected tables; declared optimiser tolerance
make rebuild-source     # restore the archived PBDB extract and rebuild inventories and results
uv run manuscript/figures.py
python3 manuscript/tables.py
uv run tools/refs.py build
make -C manuscript
python3 manuscript/package.py
```

The body-record analysis is reproduced by `models/f3/loop3/build_reviewed.py`, `analysis.py`,
`simulation.py`, `suppression_sensitivity.py` and `figures_reviewed.py`. Hash receipts bind their inputs
and outputs. Frozen Loop 1 and Loop 2 runs are retained without regeneration. Third-party deposits are
fetched by `data/external/scripts/deposits_fetch.py` and verified against `MANIFEST.tsv`.
`manuscript/claims.csv` links each main claim to its evidence and limits, and
`manuscript/value-bindings.csv` binds each quoted number of the strictly checked claims to one row and
field of its evidence. That check catches swapped or drifted values; it does not check what a sentence
means. The frozen PBDB all-taxa collections extract (27,830 collections) is archived under CC0 at
<https://doi.org/10.5281/zenodo.24028289>; `make fetch-pbdb` restores it and verifies its SHA-256.
`make check-public` restores/hash-checks that input before the tests. Reproduction requires byte
identity except for the Murzuq optimisation CSV, whose floating-point fields have absolute tolerance
$10^{-9}$ while its schema, row order, keys and categorical fields stay exact; receipts record both
reference and regenerated SHA-256 hashes. `make check-sources` reports the public thesis route
<https://etheses.whiterose.ac.uk/id/eprint/4475/> and expected hash even when the copyrighted PDF is
absent. The held source is the related 2013 thesis, not the 2011 abstract. Its SHA-256 is
`c0e3bf798fb3c27db0bf9cbb155396be5b4b8e003ee2228defb615a65abf3211`; the source check verifies it and
the byte count before checking the observation extraction. No source text is redistributed.
`makedoc.lock.json` pins the document builder.

## References
