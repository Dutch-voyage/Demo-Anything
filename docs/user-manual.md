# User manual: code implementation to visualized demo

This manual describes how a person or automated agent turns a code path into a
complete `sviz` example. It is organized as nine stage gates. Every gate has a
required artifact, a checklist, a rubric, and a pass condition.

Use the copyable [`example-workbook-template.md`](example-workbook-template.md)
to record the work and review results.

## 1. What this workflow produces

A complete example contains five connected artifacts:

1. A **learning contract** stating what the reader should understand.
2. An **evidence map** connecting source code or runtime evidence to semantic
   claims.
3. A **vNext trace** containing the semantic model, execution facts,
   checkpoints, and initial view recipe.
4. A **portable interactive demo** compiled and rendered by the generic
   `sviz` pipeline.
5. A **reader guide** explaining every checkpoint and the intended visual
   observation.

```text
goal and audience
  → source/runtime evidence
  → semantic structure
  → execution and lifecycle
  → validation
  → compiled snapshots and display plans
  → checkpoint narrative
  → visual QA
  → portable release
```

The process is deliberately not automatic source-code drawing. Static analysis
and traces can identify calls, durations, dependencies, and quantities, but the
author still supplies meaning: identity, copy versus move, grouping, scope, and
teaching intent.

## 2. Inputs required from the user

Before work starts, provide as many of these as possible:

- the source repository, revision, and code path in scope;
- one representative input or execution scenario;
- the intended audience and their expected prior knowledge;
- one primary question the visualization must answer;
- behaviors that must be visible, such as overlap, queueing, fan-out, capacity,
  reuse, or cleanup;
- behaviors that may be omitted;
- the timing source: measured, trace-derived, authored explanatory timing, or
  ordered steps;
- the desired publishing form and target container sizes;
- access needed to run code, tests, profilers, or trace collectors.

If measured timing is unavailable, use step mode or clearly label a timeline as
authored and explanatory. Never present invented timing as a measurement.

## 3. Quality scale and gate rule

Score every rubric dimension from 0 to 3:

| Score | Meaning |
| ---: | --- |
| 0 | Missing, contradicted, or unusable. |
| 1 | Present but incomplete, ambiguous, or mostly unsupported. |
| 2 | Complete enough for the stated goal, with credible evidence. |
| 3 | Precise, traceable, economical, and independently reviewable. |

A gate passes when:

- every required checklist item is checked;
- no known blocker is hidden;
- every rubric dimension scores at least 2;
- the reviewer records evidence or a short reason for each score.

A score is not a substitute for judgment. A machine-valid trace can still fail
the goal-alignment or explanatory-quality gates.

## Gate 1: establish the learning contract

### Objective

Turn a broad request such as “visualize this kernel” into one testable reader
outcome and a bounded scenario.

### Procedure

1. Name one primary audience.
2. Write one primary question in the reader's language.
3. Write three to seven observable learning outcomes.
4. Select one representative execution and define its boundaries.
5. List important exclusions so low-level detail does not consume the demo.
6. Define how a reviewer will know the demo answered the question.

### Required artifact

A one-page learning contract in the example workbook.

### Completion checklist

- [ ] One primary question is stated.
- [ ] Audience and assumed knowledge are stated.
- [ ] The source path and scenario boundaries are explicit.
- [ ] Required behaviors are observable rather than aspirational.
- [ ] Exclusions and fidelity limits are explicit.
- [ ] Timing provenance is declared.
- [ ] Success can be judged by someone other than the author.

### Rubric

| Dimension | What a score of 2 or better requires |
| --- | --- |
| Goal clarity | One question can be answered by inspecting the finished demo. |
| Scope control | Included and excluded behavior defines a feasible vertical slice. |
| Audience fit | Labels, detail, and expected knowledge match a named reader. |
| Acceptance quality | Observable success criteria cover the important learning outcomes. |

**Pass condition:** the reviewer can explain what the demo must teach without
reading the implementation plan.

## Gate 2: build the source-evidence map

### Objective

Establish what the implementation actually does before choosing visual
elements.

### Procedure

Inspect the relevant code and, when possible, execute the selected scenario.
Capture:

- structural facts: devices, ranks, memory regions, queues, buffers, and
  execution units;
- data facts: logical values, concrete copies, quantities, and ownership;
- behavioral facts: operations, dependencies, waits, synchronization, and
  concurrent work;
- transport facts: local copies, direct links, forwarding, fan-out, and fan-in;
- lifecycle facts: creation, placement, update, reuse, and retirement;
- resource facts: storage, bandwidth, execution slots, and coordination
  capacity;
- timing facts: start, duration, step, or ordering evidence.

For every important claim, record a source location, trace record, log, test,
or explicit author assumption. Do not mix observed facts and assumptions in the
same column.

### Required artifact

An evidence table and an assumption ledger.

### Completion checklist

- [ ] Every required behavior from Gate 1 has supporting evidence.
- [ ] Important code regions and runtime phases are covered.
- [ ] Concurrency and synchronization are supported by evidence.
- [ ] Quantities and capacities include units and provenance.
- [ ] Copy, move, update, and retirement claims are distinguished.
- [ ] Unknowns and author assumptions are listed separately.
- [ ] Evidence is precise enough for another reviewer to find it.

### Rubric

| Dimension | What a score of 2 or better requires |
| --- | --- |
| Coverage | Evidence covers every goal-critical behavior. |
| Traceability | Major claims point to reproducible source or runtime evidence. |
| Behavioral fidelity | Ordering, concurrency, and lifecycle match the selected execution. |
| Assumption discipline | Unsupported claims are labeled and do not masquerade as measurements. |

**Pass condition:** every visualized semantic claim can be traced to evidence or
an explicitly approved assumption.

## Gate 3: define semantic structure and identity

### Objective

Translate evidence into stable domain-neutral concepts before authoring time.

### Procedure

Map implementation facts to the vNext IR:

| Implementation fact | IR concept |
| --- | --- |
| Device, rank, memory, buffer, queue, executor | `place` |
| Storage, bandwidth, execution, coordination limit | `resource` |
| Possible transport adjacency | `link` |
| Tensor, token, request, message, shard | logical `entity` |
| One resident physical copy | `materialization` |
| Reader-meaningful unit of work | `operation` |
| Scheduled resource-owning phase | `stage` |
| Correlated sequence or branch of transfers | `flow` |
| Initial presentation intent | `view` recipe |

Resolve the following distinctions explicitly:

- logical entity versus concrete materialization;
- place versus resource;
- structural link versus current traffic;
- operation versus scheduled stage;
- spatial payload versus coordination state;
- copy versus move.

Copy retains the source and creates a destination materialization with
provenance. Move changes the placement of the same materialization. An arrow is
not sufficient evidence for either interpretation.

### Required artifact

The structural portion of the trace: time mode, places, resources, links,
entities, initial materializations, operations, flows, and initial view recipe.

### Completion checklist

- [ ] Every top-level place has a clear semantic role.
- [ ] The place hierarchy reflects containment, not visual convenience.
- [ ] Every resource has an owner, dimensions, units, and capacity.
- [ ] Links describe possible connectivity rather than individual transfers.
- [ ] Logical entities are separated from their physical copies.
- [ ] Initial materializations fully describe state at the initial cursor.
- [ ] Operations use reader-facing meaning; stages retain implementation detail.
- [ ] Flows group related transfer stages, including multi-hop paths.
- [ ] IDs are stable, readable, and independent of display coordinates.
- [ ] The view recipe emphasizes the Gate 1 learning goal.

### Rubric

| Dimension | What a score of 2 or better requires |
| --- | --- |
| Abstraction fit | The model is neither instruction noise nor an empty high-level cartoon. |
| Identity accuracy | Copies, origins, outputs, and temporary state remain distinguishable. |
| Structural completeness | Required topology, capacities, entities, and operations are represented. |
| Domain neutrality | Domain terms appear as data; core concepts keep generic meanings. |

**Pass condition:** the structure can describe the scenario without relying on
renderer-specific shapes or workload-specific rendering rules.

## Gate 4: author execution, lifecycle, and time

### Objective

Make the selected execution reconstructable at every reader cursor.

### Procedure

For each stage, author:

- its operation and generic stage kind;
- execution place or transfer link;
- exact `start` and `duration`, or an integer `step`;
- dependencies through `after`;
- materializations read;
- resource claims for the complete active interval;
- flow membership for transfer stages;
- completion effects.

Use lifecycle effects deliberately:

- `create` for a new materialization, optionally with `from` provenance;
- `place` and `unplace` for movement of the same identity;
- `update` with a write policy for persistent state;
- `retire` when a materialization ceases to exist;
- `relate` for an explicit semantic relation.

Author an initial checkpoint, important transition checkpoints, and a final
checkpoint. A checkpoint is a teaching moment, not automatically every event
boundary.

### Required artifact

A complete vNext YAML trace.

### Completion checklist

- [ ] Every stage has exactly one valid timing form.
- [ ] Dependencies agree with the authored schedule.
- [ ] Every read is present when its stage starts.
- [ ] Every created materialization has entity and place.
- [ ] Copy provenance is explicit and preserves its source.
- [ ] Moves preserve materialization identity.
- [ ] Updates state the intended write policy where relevant.
- [ ] Temporary state is retired at the correct boundary.
- [ ] Claims use dimensions declared by their resources.
- [ ] Concurrent claims represent intended overlap.
- [ ] Flow membership is consistent in both the flow and its stages.
- [ ] The final state contains exactly the intended durable results.

### Rubric

| Dimension | What a score of 2 or better requires |
| --- | --- |
| Schedule fidelity | Ordering and overlap match evidence or labeled authored intent. |
| Lifecycle integrity | Every object has a coherent origin, residency history, and end state. |
| Resource fidelity | Claims and capacities explain important contention or concurrency. |
| Flow continuity | Local, direct, multi-hop, fan-out, and fan-in paths retain identity. |

**Pass condition:** a reviewer can manually simulate the trace from its initial
state to its final state without guessing hidden mutations.

## Gate 5: pass structural and semantic validation

### Objective

Use machine checks to reject internally inconsistent traces before visual
review.

### Procedure

Run:

```bash
sviz validate examples/<name>_vnext.yaml
```

Resolve all errors. Review warnings rather than suppressing them. Current
validation covers identifier uniqueness, references, hierarchy and dependency
cycles, timing form, dependency timing, flow membership, lifecycle presence,
copy provenance, resource dimensions, concurrent claims, and storage capacity.

Also perform a manual semantic review against the evidence map; validation can
prove consistency but cannot prove the chosen abstraction answers the user's
question.

### Required artifact

A clean validation result recorded with the source revision and trace hash or
review date.

### Completion checklist

- [ ] `sviz validate` exits successfully.
- [ ] No warning is ignored without a written disposition.
- [ ] Every Gate 2 evidence row maps to at least one IR item or an explicit omission.
- [ ] No lifecycle meaning is encoded only in a label or tag.
- [ ] Timing provenance remains visible in the example description or guide.
- [ ] A second reader has checked the copy/move and initial/final state decisions.

### Rubric

| Dimension | What a score of 2 or better requires |
| --- | --- |
| Structural validity | Schema and reference constraints pass. |
| Semantic validity | Lifecycle, dependencies, flows, and capacity are internally coherent. |
| Evidence agreement | The valid trace still matches the source-evidence map. |
| Diagnostic closure | Every tool warning and reviewer concern has a disposition. |

**Pass condition:** the trace is both machine-valid and manually reconciled
with the evidence—not merely parseable.

## Gate 6: inspect compilation and state reconstruction

### Objective

Verify the compiler derived the correct execution snapshots before judging
visual appearance.

### Procedure

Run:

```bash
sviz compile examples/<name>_vnext.yaml -o /tmp/<name>.json
```

Inspect the compiled initial state, every checkpoint, and the final state.
Check materialization residency, provenance, active stages and flows, resource
ledgers, state deltas, System roots, link routes, Timeline lanes, and marks.

Compile twice and compare the outputs. Compilation must be deterministic.

### Required artifact

A checkpoint audit in the workbook and, for maintained examples, automated
assertions for the most important states.

### Completion checklist

- [ ] Two compilations of the same trace are identical.
- [ ] Initial and final snapshots match the learning contract.
- [ ] Every checkpoint has the expected live materializations.
- [ ] Active stages and flows match the authored cursor.
- [ ] Provenance survives copies and fan-out.
- [ ] Resource ledgers match independent calculations at peak moments.
- [ ] System roots and hierarchy are stable.
- [ ] Timeline lanes and marks cover every authored stage.
- [ ] No compiler output depends on workload names or domain tags.
- [ ] Goal-critical snapshots have regression tests.

### Rubric

| Dimension | What a score of 2 or better requires |
| --- | --- |
| State correctness | Snapshots reconstruct initial, transition, and final state correctly. |
| Accounting correctness | Resource and quantity ledgers agree with the authored execution. |
| Determinism | Repeated compilation produces identical semantic and display plans. |
| Test strength | Assertions cover the failures that would invalidate the teaching goal. |

**Pass condition:** compiled state is trustworthy without using the renderer as
a debugging oracle.

## Gate 7: design the checkpoint narrative

### Objective

Turn correct state transitions into a coherent step-by-step explanation.

### Procedure

For every checkpoint, write:

1. what completed since the previous checkpoint;
2. what begins or remains active;
3. what materialization or resource state changed;
4. what the reader should inspect;
5. how this moment advances the primary learning goal.

Merge checkpoints that add no distinct semantic insight. Add a checkpoint when
an important transition would otherwise be skipped. Keep continuous playback
out of the explanation; the default interaction is deliberate Previous/Next
navigation.

### Required artifact

A checkpoint table in the reader guide and concise `narrative`/`focus` data in
the trace. `narrative` accepts Markdown; use `detail` only for a short plain-text
fallback. Add checkpoint-scoped annotations only for questions or review notes
that must remain pinned to a specific semantic element.

### Completion checklist

- [ ] The first checkpoint establishes the initial state.
- [ ] Every required behavior from Gate 1 appears in at least one checkpoint.
- [ ] Each step communicates one main transition or comparison.
- [ ] Parallel work is described as parallel, not serialized in prose.
- [ ] Focus IDs refer to the most relevant semantic elements.
- [ ] The final checkpoint states what remains and what was retired.
- [ ] Labels and explanations use vocabulary appropriate for the audience.
- [ ] Timing claims distinguish measurement from authored explanation.
- [ ] Every annotation anchor is visibly represented in at least one projection.
- [ ] Annotation status communicates review state, not execution state.

### Rubric

| Dimension | What a score of 2 or better requires |
| --- | --- |
| Narrative progression | Each checkpoint adds a meaningful, ordered insight. |
| Goal coverage | Together, the checkpoints answer the primary question. |
| Cognitive economy | The sequence omits redundant cursors and avoids detail overload. |
| Visual direction | Every explanation tells the reader what visible evidence to inspect. |

**Pass condition:** a target reader can follow the story using only Previous,
Next, and the checkpoint explanations.

## Gate 8: perform visual and interaction QA

### Objective

Confirm that correct compiled information is legible, connected, responsive,
and usable through the generic renderer.

### Procedure

Run:

```bash
sviz view examples/<name>_vnext.yaml
```

Review every checkpoint in both System and Timeline projections. Test default,
narrow, and wide containers. Exercise selection, keyboard navigation, place
dragging, place resizing, shape rescaling, edge adjustment, Markdown editing,
pin creation, annotation status switching, and layout reset.

Run **Check layout** at each supported host width. It audits every checkpoint
in System and Timeline at the unmodified 100% layout. Record the returned
report, including shortened-label warnings, in the visual QA artifact. See
[`layout-checking.md`](layout-checking.md) for the browser and CI APIs.

Fix problems at the correct layer:

- incorrect meaning or state → trace;
- repeated scenario-independent placement failure → compiler/display planner;
- pixel fitting, hit testing, or accessibility failure → renderer;
- one reader's preferred position or scale → presentation state or view recipe.

Never fix one workload by branching on its name, label, or tag in the renderer.

### Required artifact

A visual QA record with screenshots or concise observations for representative
checkpoints and sizes.

### Completion checklist

- [ ] All goal-critical elements are visible at the default layout.
- [ ] No important edge, arrowhead, object, or label is unintentionally hidden.
- [ ] Short Timeline marks do not leak text into neighboring events.
- [ ] The default-layout checker reports no overlap errors at each supported width.
- [ ] Selection is consistent across System and Timeline views.
- [ ] Transfers connect the correct semantic endpoints.
- [ ] Parallel transfers remain distinguishable or clearly aggregated.
- [ ] Manual placement and size changes do not modify execution semantics.
- [ ] Reset restores the compiled layout.
- [ ] Narrow and wide containers remain usable.
- [ ] Keyboard focus and controls have understandable labels.
- [ ] No scenario-specific renderer branch was introduced.

### Rubric

| Dimension | What a score of 2 or better requires |
| --- | --- |
| Legibility | Important shapes, edges, labels, and states can be read at target sizes. |
| Cross-view coherence | Cursor, selection, identity, and timing agree in both projections. |
| Interaction quality | Navigation and layout adjustment are predictable and reversible. |
| Responsive quality | The demo remains useful across declared host sizes. |
| Renderer generality | Fixes use semantic or geometry policies reusable by other scenarios. |

**Pass condition:** the target reader can locate every piece of visual evidence
needed to answer the Gate 1 question.

## Gate 9: document, export, and release

### Objective

Package a reproducible example that works outside the development viewer.

### Procedure

Write a guide containing purpose, fidelity boundary, element mapping,
checkpoint walkthrough, and source-to-IR notes. Then run:

```bash
sviz export examples/<name>_vnext.yaml \
  --format bundle \
  --output dist/<name>
```

Test the inline snippet, standalone offline page, and iframe fallback. Record
the command and source revision used to regenerate them.

### Required artifact

A reviewed trace, guide, tests, and verified portable bundle.

### Completion checklist

- [ ] The guide states purpose, audience, timing provenance, and omissions.
- [ ] The guide explains visual elements and every checkpoint.
- [ ] Validation and compilation commands are reproducible.
- [ ] Regression tests cover goal-critical semantic states.
- [ ] Inline export works in a host page.
- [ ] Standalone export works without the development server.
- [ ] Iframe fallback loads correctly.
- [ ] Multiple components do not leak state or styles.
- [ ] Exported files contain no unavailable local dependencies.
- [ ] The final workbook records reviewer scores and unresolved limitations.

### Rubric

| Dimension | What a score of 2 or better requires |
| --- | --- |
| Documentation completeness | A new reader can understand elements, steps, and fidelity limits. |
| Reproducibility | Another person or agent can validate, compile, view, and export it. |
| Portability | Supported export forms work in their intended environments. |
| Release integrity | Trace, guide, tests, and exports describe the same revision. |

**Pass condition:** a reviewer who did not author the example can reproduce and
use the demo from the checked-in instructions.

## 4. Final acceptance rubric

In addition to passing all nine gates, score the finished example across these
critical qualities:

| Quality | Release requirement |
| --- | --- |
| User-goal alignment | The primary question is answered through visible evidence. |
| Source fidelity | Important behavior is supported by code, runtime evidence, or labeled assumptions. |
| Semantic integrity | Identity, topology, dependencies, resources, and lifecycle are coherent. |
| Explanatory quality | Checkpoints form a concise, comprehensible story. |
| Visual clarity | System and Timeline views remain legible and mutually consistent. |
| Generality | The example requires no workload-specific renderer behavior. |
| Reproducibility | Validation, compilation, tests, and export can be repeated. |

The example is **release-ready** when every gate passes and every final quality
scores at least 2. It is **reference-quality** when the average final score is
at least 2.6 and no assumption materially affects the primary conclusion.

## 5. Operating rules for automated agents

An automated agent following this manual should:

1. Preserve source evidence and assumptions separately.
2. Ask for direction when an ambiguity changes identity, lifecycle, timing
   meaning, scope, or the user's primary conclusion.
3. Prefer step mode when credible numeric timing is unavailable.
4. Never infer copy or move from a function name or arrow alone.
5. Inspect compiled snapshots before visual styling.
6. Change the trace for semantic errors, the compiler for reusable planning
   errors, and the renderer only for generic rendering behavior.
7. Never add workload-name, label, or tag branches to the renderer.
8. Keep manual dragging, resizing, shape scale, and edge offsets out of
   execution semantics.
9. Record validation output, test results, visual observations, and remaining
   limitations in the workbook.
10. Stop claiming completion if any required gate is unreviewed.

## 6. Useful references

- [`README.md`](README.md): documentation map and recommended reading order.
- [`ir-authoring-guide.md`](ir-authoring-guide.md): field-level IR concepts,
  minimal trace, and authoring loop.
- [`ir-design.md`](ir-design.md): semantic boundaries and compiler contract.
- [`example-workbook-template.md`](example-workbook-template.md): copyable gate
  checklists and score sheets.
- [`flash-attention-workflow.md`](flash-attention-workflow.md): first complete
  source-to-display example.
- [`deepep-workflow.md`](deepep-workflow.md): fan-out, multi-hop flow, shared
  route, and fan-in example.
- [`../schema/sviz-0.2-draft.schema.json`](../schema/sviz-0.2-draft.schema.json):
  current machine-readable trace schema.
- [`../schema/sviz-viewer-state-0.1.schema.json`](../schema/sviz-viewer-state-0.1.schema.json):
  persisted narrative, annotation, layout, and saved-view schema.
- [`persistence.md`](persistence.md): local file-backed viewing and the portable
  component persistence API.
- [`../examples/flash_attention_vnext.yaml`](../examples/flash_attention_vnext.yaml)
  and [`../examples/deepep_vnext.yaml`](../examples/deepep_vnext.yaml): complete
  trace references.
