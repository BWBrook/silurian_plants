# Table S17 and Interpretation: focused acceptance review

Codex, 15 November 2026. Requested by Barry following Claude's Board 158
message 3437; revision checked at `49c8cb0`. This is a wording and navigation
review, with no new analysis, result, claim or value-binding change.

## Decision

**The shortened Conditions paragraph and reordered Interpretation pass.** The
conditions removed from the former Discussion remain represented in Table S17
and its supporting sections. Nominal lower 95% bounds can remain in Results (h):
the main Conditions paragraph explicitly states the absence of calibrated
confidence for choices made after seeing the data. The comparison still uses the
whole period after A, including the late Silurian.

The new demographic sentence is conditional on populations filling available
habitat rapidly. It therefore illustrates what would follow under that premise,
without estimating ancient net growth or ruling slow growth out. The inherited
trigger sentence retains prompt spread, recognisable crown bodies and finding at
the later rate before drawing the young-ancestor inference; its “otherwise”
keeps an older ancestor possible. The three condensed fossil cautions and the
preservation alternative retain the distinctions checked on 14 November.

One word was added: the doubling-time comparison now says **exponential** rises.
This keeps the 1.5–5.8 Myr range tied to the tested family rather than all possible
histories. The Abstract, Results (h) heading and short Conditions paragraph are
otherwise unchanged.

## Table S17

An independent row-by-row trace checked all 34 condition rows against the main
article, supplement and implementation. Every named section exists. The affected
cells and a common locator note were repaired:

- Locate the base age/independence assumptions in S2.2, with the sensitivities
  still pointing to S2.3/S2.5.
- Point the count sensitivity to figure 3a and calibration examples to S5.6.
- Include Results (d), where the rule of three is introduced, among its applications.
- Distinguish calibrated confidence from the nominal levels of retrospective
  step/rise and combined-measure calculations.
- Identify exchangeability as stated in the table and stage shuffling as the
  implementation, rather than implying that exchangeability was tested.
- Add Methods (h), which defines the binomial allocation probability.
- Identify collection density as a rough searching proxy, the exponential
  family as examined, and the rate lower bounds as not establishing a plateau.
- Clarify the article/supplement reference conventions and the loop3 base for
  script/output paths; name the membership table and its B2/main subset.

The full matrix is in `2026-11-15-s17-pointer-review.md`. The parent compared the
old Conditions text, checked the affected source passages and implementation,
and integrated the repairs. The independent reviewer accepted the final pointers
and wording. No scientific condition was removed or empirically validated by
collecting it into the table.

## Verification

The claims ledger and value bindings are byte-identical to `2a8ded3`; no analysis
code or numerical output changed. Claims and all-profile manuscript lint/citation
checks pass: 60 cited, 58 supported and two superseded, zero errors or warnings.
No numerical rerun or additional unit test was warranted for this edit. The
article and supplement were rebuilt and the affected pages inspected, including
all pages of Table S17. Package/dependency manifests were refreshed and their
hashes checked. Companion products remain for the agreed later pass. No question
or adopted scientific interpretation changes, and no release or submission occurs.
