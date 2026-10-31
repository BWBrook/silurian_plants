# Two sprints to Loop 1's first empirical answers

**Draft v1**, Claude Opus 5.5, 31 October 2026, for Codex to critique and revise. Barry's instruction
(chat, 2026-10-31): "you and Codex agree on two sprints that would substantively advance the work,
after which you will counter-review each other's work, in a follow-up handshake." The order he set:
- Claude drafts; Codex critiques and revises.
- Claude runs sprint 1, then Codex runs sprint 2.
- Claude reviews and fixes sprint 2; Codex reviews and fixes sprint 1.
- Then the two reconcile.

## Where the work stands

F3 has a validated engine:
- stage-1 and stage-2 synthetic validation, the calibrated critical value and strict evidence
  checks;
- a frame screen with a conditional-qualification rule (`f3-shape.md`, "Frame screen and frame
  selection").

Seven candidate frames are inventoried with literal source reports (`data/units/`). Libya is mapped
to chart, appendix and prose. Persistence of trilete production is reproduced with measured
precision (`models/pilot-asr/`).

**No empirical F3 statement exists yet for any clock maximum.** Every recent tranche has
strengthened the machinery or the inventory by one step, then handed off. These sprints aim instead
at Loop 1's deliverable: compatibility statements for M2, M1 and M3 on real frames, each qualified on
its actual design, with the pivotal readings named (`plan-f3.md`, Loop 1, steps 4–6).

## Shape: sequential and dependent

Sprint 1 builds the real-design pipeline and uses it for M2. Sprint 2 applies that pipeline to M1
and M3, and assembles their frames. The pairing follows our strengths:
- sprint 1 is mostly statistical design and model code, Claude's lane;
- sprint 2 is mostly source-frame assembly, Codex's lane, plus applying a finished pipeline.

The dependency is real. Sprint 2 should not write its own estimator code, and sprint 1 cannot
assess M1 without frames that do not yet exist. Two isolated sprints would either duplicate the
pipeline or leave M1 without frames.

## Working rules for both sprints

- **Autonomy inside the sprint.** The sprinting agent may edit any file its sprint needs, including
  files the other agent normally owns. It records every such edit in the sprint audit, and the
  reviewer checks those edits first. Board posts happen at the start and the end only.
- **Pre-registration.** Before any declared design is screened or fitted, the sprint commits its
  design declarations:
  - frame and units;
  - reference membership;
  - sampling classes;
  - age allocation;
  - dependence;
  - reading and binary conversion;
  - targets.

  The commit hash is the timestamp. The fixed candidate list (`f3-shape.md`) is reported in full.
- **Acceptance comes from the existing contract.** That means the reporting rule
  (`data/units/reporting-rule.md`), the two-stage qualification on passing replicates
  (N1 = N2 = 1,000, cap of 20 attempts per pass, calibration target 0.955, floor 0.93), and the
  three reporting layers of `f3-shape.md`. Neither sprint changes the contract. A contract defect
  found mid-sprint is fixed as a declared amendment before any new real-data result, and the
  original is kept.
- **Compute.** Heavy qualification runs go to `nectar`, resized to `c3.3xlarge` for the tranche
  and returned to `c3.large` afterwards, with BLAS pinned to one thread.
- **Stop at the gold stamp,** a consult trigger (`plan-f3.md`) or a real blocker. A design that
  cannot be qualified is a result: a demonstrated limit, with the observation that would resolve it.
- **Independent check before handoff.** A fresh subagent audits the central claims: Sonnet for
  Claude, a bounded same-model reviewer for Codex.

## Sprint 1 (Claude): M2 on real frames, end to end

**Gold stamp.** For each declared M2 design: either a qualified empirical statement at 459.1 Ma and
older candidate origins, under main and every named reading, in the three layers; or a demonstrated
limit with the observation that would resolve it. The statements come with the readings that flip
them, and with a pipeline sprint 2 can run on new frames without new model code.

1. **Declare the M2 designs** (`models/f3/designs/`, one file each, committed before screening).
   - Libya H2 within well: Tanezzuft cuttings as reference, Hawaz cores and cuttings as older units,
     core and cutting as separate sampling classes, one well cluster.
   - Libya core-only, across wells, as a declared transport scenario. The 7287 ft prose-positive core
     is carried both ways.
   - Libya D1 and I3: declared, and expected to fail on productivity and caving.
   - Qusaiba as a positive reference with Borenshult's pre-Katian samples as older units, under a
     declared transport assumption.
   - Borenshult alone: already screened, so it is reported, not re-run.

   Binary conversion is applied by code in `models/f3/` that reads Codex's source-report tables
   under the named readings. Codex's tables themselves are not edited.
2. **Engine support for the real designs.**
   - several sampling classes with their own rates (core and cutting);
   - well or core clusters;
   - a caving rule, under which a cutting detection fixes the first appearance no older than its
     depth interval allows;
   - age allocation from formation-level stage assignments, with shared ages per formation.

   Each feature gets tests on the synthetic designs, and the stage-1 and stage-2 evidence is
   re-scored to show nothing earlier moved.
3. **Screen every declared design with the engine,** under its own structure, not the homogeneous
   shortcut. Report all of them.
4. **Qualify each passing design conditionally** on `nectar`: its simulated twin, with the screen
   in every replicate and passing-replicate counts.
5. **Run the qualified designs on the data.**
   - f\*(T) and the origin sets at f ∈ {1, 0.1, 0.01}, for main, inclusive and any design-specific
     readings.
   - Report the three layers: encounter intensity; biological translation, with the persistence
     and retention scenarios beside the verdict, not multiplied; and the node implication for
     459.1 Ma.
6. **Pivotal readings for M2.** Which readings flip a verdict:
   - the Borenshult triletes;
   - Libya 7287 ft;
   - the I3 marks within Cr3;
   - Qusaiba's core 56.

   Feed them to `questions.md` (Q1, Q2) and the value-of-information list.
7. **Write the M2 result note** (`docs/audits/`), with the AI roles recorded.

**Not in sprint 1:** M1 or M3 frames, the synthesis dataset release, and any new ASR work.

## Sprint 2 (Codex): M1 and M3 frames and results with the sprint-1 pipeline

**Gold stamp.** For M1 (515.5 Ma; E2, accepted embryophytic cryptospores): a qualified empirical
statement on at least one declared pre-Darriwilian design, or a demonstrated limit naming the
sampling that would resolve it. For M3 (431.2 Ma; E3, polysporangiophyte megafossils): a screened
statement of what the body-fossil frames can and cannot bound. Both come with pivotal readings and
value-of-information entries.

1. **Assemble the M1 frames.**
   - Pre-Darriwilian palynological sampling with complete sample reporting: the full Palynodata
     release (`data/external/local/spores/of_5793.zip`), and the Cambrian sources held (Strother
     2016; Wang et al. 2022).
   - The Argentine Dapingian (Rubinstein et al. 2010, 2011) with its dispute carried as readings.
   - The Saudi, Paraguay and Samphire frames already listed.
   - Inventory and event-map them as for Borenshult and Libya.
2. **Declare the M1 designs** in sprint 1's format and commit them before screening. Then screen,
   qualify conditionally and run, with the sprint-1 pipeline unchanged.
3. **M3.** Assess PBDB/GBDB Silurian collections in plant-bearing facies as frames, screen them,
   and state the limit. `plan-f3.md` already expects body-fossil events to be too thin for a
   qualified bound. The useful product is the number and kind of collections that would change
   that.
4. **Pivotal readings and value of information** for M1 and M3, feeding Q1, Q2 and Q5.
5. **Write the M1 and M3 result note** in `docs/audits/`.

**Not in sprint 2:** changes to the engine or the qualification contract. A needed pipeline change
is recorded for Claude's review and made as a declared amendment.

## Counter-review and reconciliation

- **Claude reviews sprint 2,** fixing what it finds, with the cross-ownership edits first. **Codex
  reviews sprint 1** the same way. Each review re-runs at least one qualification and one empirical
  result from the committed declarations.
- **Reconciliation** produces Loop 1's close (`plan-f3.md`, steps 5 and 6):
  - a memo on what holds under every reading for M2, M1 and M3, and what depends on which records;
  - what the record cannot tell apart, and the observation that would settle it;
  - a value-of-information ranking;
  - a structural-review entry.

  Disagreements go to Barry with both positions.

**Next candidate after this cycle:** the synthesis dataset release, contribution A. It needs
Barry's decision on release.
