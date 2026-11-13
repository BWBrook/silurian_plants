# E2 dispersal-unit rule (addendum to the reporting rule)

Version 1, 1 November 2026. Drafted by Claude Opus 5.5 from Codex's replacement rule (Correspondence
2760), which supersedes Claude's first proposal in `studies/f3/docs/loop1-close.md` (613a154). Status: adopted
jointly on 1 November 2026, with Codex's clarification that indeterminate morphology needs affirmative
evidence before detection. It applies the frozen reporting
rule (`reporting-rule.md`) to event E2 and changes nothing in it. `reporting-rule.md` is
hash-bound in the 28 F3 qualification receipts and stays untouched. Any future E2 adapter must name
and consume this file and its version; no current outcome, code or receipt depends on it.

E2 is "first cryptospores accepted as embryophytic" (`studies/f3/docs/plan-f3.md`). A morphological cryptospore
label, from a source or from us, therefore does not by itself establish E2.

## Definition the rule rests on

Richardson et al. (1984) defined cryptospores as non-marine sporomorphs without visible haptotypic
features, including single grains or monads as well as permanent dyads and tetrads; Richardson (1988)
added hilate monads, the separated products of dyads. Edwards et al. (2014, New Phytologist 202:
50–78, pp.51–52) adopt Richardson (1988) because it is morphological and makes no affinity claim. A
hilum or envelope is therefore **not** a necessary condition for a cryptospore monad. The narrower
wording formerly on `taxa/ordovician-cryptospores.md` and pilot criterion C2 is corrected (Q5).

## Two axes, recorded separately

**Axis 1: morphology and producer evidence, as the source reports it.** Record configuration,
hilum/envelope state and evidence of dissociation separately where they overlap. The rows below
are evidence categories, not mutually exclusive taxonomic bins; uncertainty in any feature stays
explicit.

| Category | Example (Wellman et al. 2015, Table 1, p.115, and p.122) |
|---|---|
| permanent polyad: tetrad or dyad, naked or enveloped | *Tetrahedraletes*, *Velatitetras* |
| hilate monad | *Laevolancis divellomedium*, *Chelinohilates* |
| enveloped monad | none in Qusaiba-1 |
| alete monad without hilum or envelope | *Rugosphaera? cerebra*, which "appear[s] to be naked", a tight envelope not excluded (p.114) |
| demonstrated dissociated-polyad product | cf. *L. chibrikovae*: "a monad formed by physical dissociation of a permanent dyad", partner remains sometimes attached (p.122) |
| indeterminate grain | a grain the source does not identify to any of the above |

Pooled reports (colour groups, "cryptospores/spores" totals, percentage fractions) carry the list of
their constituent forms where the source gives it, and otherwise the category `pooled, constituents
unknown`.

**Axis 2: identity and embryophyte affinity under the named reading.** Each reading decides whether
the record's forms are accepted as embryophytic E2, with the record-specific evidence cited:
assignment to a taxon whose affinity the reading accepts, wall or ultrastructural evidence, in situ
or sporangial association, and evidence that excludes acritarch confusion (the ambiguity the formal
definitions sought to remove; Edwards et al. 2014, p.52).

## Mapping to outcomes

- **Detected** where a form passes both axes under that reading. Each identified morphology or
  demonstrated producer-evidence category can qualify; an indeterminate grain must first acquire
  affirmative evidence of a cryptospore morphology or producer link under that reading. In
  particular, an alete monad without hilum or envelope is accepted where the record-specific
  evidence supports both axes; the missing hilum or envelope alone does not make it unresolved.
- **Unresolved** where either axis remains undecided or undocumented under that reading. Disagreement
  between readings does not itself make each reading unresolved. An explicitly rejected identification
  can contribute to a zero only under the full-category reporting and other conditions of
  `reporting-rule.md`, qualification 3; rejection alone supplies no absence trial.
- **A wider reading detects a disputed record only if that reading explicitly accepts it**
  (`reporting-rule.md`, qualification 3). Selecting `inclusive` or `outlier` does not promote an
  unknown observation, a generic "spores" pool, an indeterminate grain or a missing sample link.
- **Pooled samples** count as detected only when their definition or constituents establish at
  least one form accepted under that reading, at that sample's scope.
- **Zeros** follow `reporting-rule.md` unchanged: explicit non-detection within its verified scope,
  or `not_reported` after the full-category reporting audit.

## Present effect

None on recorded outcomes. Claude's audit of the 147 E2 outcome rows and the sprint-2 ledgers
(1 November 2026, `studies/f3/docs/loop1-close.md`) found that every current E2 detection rests on a permanent
polyad or, at Paraguay AS1-2835, on the hilate *L. divellomedia*. That audit was a source and outcome
check, not a machine application of this rule, and it does not validate the rule for future
monad-only samples.
