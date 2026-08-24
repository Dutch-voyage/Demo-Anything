# sviz example workbook template

Copy this file for each new example. It is the review record shared by the
author, automated agent, and reviewer. Do not mark a gate passed without
evidence.

## Example record

| Field | Value |
| --- | --- |
| Example name | `<name>` |
| Owner | `<person or agent>` |
| Reviewer | `<reviewer>` |
| Status | `not started / draft / blocked / passed` |
| Source repository and revision | `<URL/path and revision>` |
| Source path in scope | `<files/functions/modules>` |
| Representative input | `<input or scenario>` |
| Trace | `examples/<name>_vnext.yaml` |
| Guide | `docs/examples/<name>.md` |
| Test | `tests/test_<name>_pipeline.py` |
| Export | `dist/<name>/` |
| Last reviewed | `<date>` |

## Scoring scale

- **0 — Missing:** absent, contradicted, or unusable.
- **1 — Partial:** present but ambiguous, incomplete, or unsupported.
- **2 — Complete:** sufficient for the stated goal and credibly evidenced.
- **3 — Strong:** precise, economical, traceable, and independently reviewable.

Each gate requires every checklist item, no hidden blocker, and no rubric score
below 2.

---

## Gate 1 — Learning contract

### Brief

- **Audience:** `<who will use this>`
- **Assumed knowledge:** `<what they already understand>`
- **Primary question:** `<one question the demo must answer>`
- **Representative execution:** `<one bounded scenario>`
- **Timing provenance:** `measured / trace-derived / authored / steps`
- **Publishing target:** `<viewer, blog block, standalone, iframe>`
- **Target sizes:** `<minimum, default, maximum>`

### Required learning outcomes

1. `<observable outcome>`
2. `<observable outcome>`
3. `<observable outcome>`

### Explicit exclusions

- `<detail intentionally omitted>`
- `<detail intentionally omitted>`

### Acceptance observations

| Outcome | What must be visible | Checkpoint or view |
| --- | --- | --- |
| `<outcome>` | `<observable evidence>` | `<location>` |

### Checklist

- [ ] Primary question is singular and testable.
- [ ] Audience and assumed knowledge are explicit.
- [ ] Scenario and source boundaries are explicit.
- [ ] Required behaviors are observable.
- [ ] Exclusions and fidelity limits are explicit.
- [ ] Timing provenance is declared.
- [ ] Acceptance observations cover every learning outcome.

### Score

| Dimension | Score 0–3 | Evidence/reason |
| --- | ---: | --- |
| Goal clarity |  |  |
| Scope control |  |  |
| Audience fit |  |  |
| Acceptance quality |  |  |

**Gate status:** `<draft / blocked / passed>`
**Reviewer:** `<name>`
**Notes:** `<remaining concern>`

---

## Gate 2 — Source-evidence map

### Evidence table

| ID | Required behavior | Semantic claim | Source/runtime evidence | Confidence | Assumption? |
| --- | --- | --- | --- | --- | --- |
| E1 | `<goal behavior>` | `<what occurs>` | `<file:line, trace event, test, or log>` | `high/medium/low` | `no/yes` |

### Assumption and ambiguity ledger

| ID | Ambiguity or assumption | Why evidence is insufficient | Effect on conclusion | Owner | Resolution |
| --- | --- | --- | --- | --- | --- |
| A1 | `<unknown>` | `<gap>` | `<low/medium/high>` | `<name>` | `<decision or open>` |

### Checklist

- [ ] Every Gate 1 behavior has evidence.
- [ ] Structure, data, execution, transport, and lifecycle are covered.
- [ ] Concurrency and synchronization have evidence.
- [ ] Quantities and capacities include units and provenance.
- [ ] Copy, move, update, and retirement are distinguished.
- [ ] Assumptions are separate from observed facts.
- [ ] Another reviewer can locate the evidence.

### Score

| Dimension | Score 0–3 | Evidence/reason |
| --- | ---: | --- |
| Coverage |  |  |
| Traceability |  |  |
| Behavioral fidelity |  |  |
| Assumption discipline |  |  |

**Gate status:** `<draft / blocked / passed>`
**Reviewer:** `<name>`
**Notes:** `<remaining concern>`

---

## Gate 3 — Semantic structure and identity

### Mapping table

| Evidence IDs | Implementation concept | IR concept and ID | Why this abstraction fits |
| --- | --- | --- | --- |
| `<E1>` | `<buffer/rank/tensor/etc.>` | `<place/entity/resource/etc.>` | `<reason>` |

### Identity decisions

| Logical entity | Materializations | Initial place | Copy/move policy | Durable or temporary |
| --- | --- | --- | --- | --- |
| `<entity>` | `<ids>` | `<place>` | `<decision>` | `<lifetime>` |

### Checklist

- [ ] Places reflect semantic containment.
- [ ] Resources have owners, capacities, dimensions, and units.
- [ ] Links represent possible connectivity.
- [ ] Entities and concrete materializations are separated.
- [ ] Initial materializations completely define initial state.
- [ ] Operations are reader-meaningful and stages are implementation-level.
- [ ] Multi-stage transport is grouped into flows.
- [ ] IDs are stable and display-independent.
- [ ] View roots and importance match the learning contract.
- [ ] No required meaning depends only on labels or tags.

### Score

| Dimension | Score 0–3 | Evidence/reason |
| --- | ---: | --- |
| Abstraction fit |  |  |
| Identity accuracy |  |  |
| Structural completeness |  |  |
| Domain neutrality |  |  |

**Gate status:** `<draft / blocked / passed>`
**Reviewer:** `<name>`
**Notes:** `<remaining concern>`

---

## Gate 4 — Execution, lifecycle, and time

### Stage audit

| Stage | Evidence IDs | Time/step | Reads | Claims | Completion effects | Dependencies/flow |
| --- | --- | --- | --- | --- | --- | --- |
| `<stage>` | `<E1>` | `<start+duration or step>` | `<materializations>` | `<resource amounts>` | `<effects>` | `<after / flow>` |

### Boundary state audit

| Boundary | Finishes | Effects | Starts | Live materializations | Active claims |
| --- | --- | --- | --- | --- | --- |
| `<time/step>` | `<stages>` | `<state changes>` | `<stages>` | `<important state>` | `<resources>` |

### Checklist

- [ ] Every stage has exactly one timing form.
- [ ] Dependencies agree with timing.
- [ ] Every read exists at stage start.
- [ ] Creates name entity, place, and provenance when copied.
- [ ] Moves preserve identity; copies preserve the source.
- [ ] Updates use the intended write policy.
- [ ] Temporary materializations retire correctly.
- [ ] Claims use compatible resource dimensions.
- [ ] Concurrent claims represent intended overlap.
- [ ] Flow membership is bidirectionally consistent.
- [ ] Final state contains exactly the intended durable results.

### Score

| Dimension | Score 0–3 | Evidence/reason |
| --- | ---: | --- |
| Schedule fidelity |  |  |
| Lifecycle integrity |  |  |
| Resource fidelity |  |  |
| Flow continuity |  |  |

**Gate status:** `<draft / blocked / passed>`
**Reviewer:** `<name>`
**Notes:** `<remaining concern>`

---

## Gate 5 — Validation

### Command record

```bash
sviz validate examples/<name>_vnext.yaml
```

- **Date:** `<date>`
- **Source revision:** `<revision>`
- **Result:** `<exit status and summary>`

### Diagnostic disposition

| Error/warning/reviewer concern | Cause | Resolution | Verified by |
| --- | --- | --- | --- |
| `<diagnostic>` | `<cause>` | `<change or accepted limitation>` | `<test/reviewer>` |

### Checklist

- [ ] Validation exits successfully.
- [ ] Every warning has a written disposition.
- [ ] Every evidence row maps to IR or an explicit omission.
- [ ] No lifecycle meaning is hidden in labels or tags.
- [ ] Timing provenance is documented.
- [ ] Copy/move and initial/final states received a second review.

### Score

| Dimension | Score 0–3 | Evidence/reason |
| --- | ---: | --- |
| Structural validity |  |  |
| Semantic validity |  |  |
| Evidence agreement |  |  |
| Diagnostic closure |  |  |

**Gate status:** `<draft / blocked / passed>`
**Reviewer:** `<name>`
**Notes:** `<remaining concern>`

---

## Gate 6 — Compiled-state audit

### Command record

```bash
sviz compile examples/<name>_vnext.yaml -o /tmp/<name>.json
```

- **Repeated compilation identical:** `<yes/no>`
- **Regression test:** `tests/test_<name>_pipeline.py`

### Checkpoint state table

| Checkpoint | Expected live state | Expected active work | Resource ledger | Actual result | Test/assertion |
| --- | --- | --- | --- | --- | --- |
| `<id>` | `<materializations>` | `<stages/flows>` | `<peak claims>` | `<match/deviation>` | `<test>` |

### Checklist

- [ ] Compilation is deterministic.
- [ ] Initial and final snapshots match the learning contract.
- [ ] Every checkpoint has the expected materializations.
- [ ] Active stages and flows match the cursor.
- [ ] Copy/fan-out provenance is retained.
- [ ] Peak resource ledgers were independently checked.
- [ ] System roots and hierarchy are stable.
- [ ] Timeline marks cover all stages.
- [ ] Goal-critical states have regression assertions.
- [ ] Compilation contains no workload-name decisions.

### Score

| Dimension | Score 0–3 | Evidence/reason |
| --- | ---: | --- |
| State correctness |  |  |
| Accounting correctness |  |  |
| Determinism |  |  |
| Test strength |  |  |

**Gate status:** `<draft / blocked / passed>`
**Reviewer:** `<name>`
**Notes:** `<remaining concern>`

---

## Gate 7 — Checkpoint narrative

### Reader-step table

| Step | Cursor | Completed | Starts/remains active | State change | What to inspect | Goal outcome |
| ---: | ---: | --- | --- | --- | --- | --- |
| 1 | `<time/step>` | `<work>` | `<work>` | `<delta>` | `<visual focus>` | `<Gate 1 outcome>` |

### Checklist

- [ ] First checkpoint establishes initial state.
- [ ] Every learning outcome appears in the sequence.
- [ ] Each checkpoint adds one main insight.
- [ ] Parallel work is represented accurately.
- [ ] Focus IDs point to relevant semantic elements.
- [ ] Final checkpoint explains durable and retired state.
- [ ] Vocabulary matches the target audience.
- [ ] Timing claims retain their provenance label.

### Score

| Dimension | Score 0–3 | Evidence/reason |
| --- | ---: | --- |
| Narrative progression |  |  |
| Goal coverage |  |  |
| Cognitive economy |  |  |
| Visual direction |  |  |

**Gate status:** `<draft / blocked / passed>`
**Reviewer:** `<name>`
**Notes:** `<remaining concern>`

---

## Gate 8 — Visual and interaction QA

### Test matrix

| View | Checkpoint | Container | Interaction | Expected | Result/evidence |
| --- | --- | --- | --- | --- | --- |
| `System` | `<id>` | `<width×height>` | `<selection/drag/etc.>` | `<outcome>` | `<screenshot or note>` |
| `Timeline` | `<id>` | `<width×height>` | `<selection/keyboard>` | `<outcome>` | `<screenshot or note>` |

### Checklist

- [ ] Goal-critical elements are visible by default.
- [ ] Important edges, arrows, objects, and labels are unobstructed.
- [ ] Short Timeline labels remain inside their marks.
- [ ] Cursor and selection agree across projections.
- [ ] Transfers use the correct endpoints.
- [ ] Concurrent transfers are distinguishable or clearly aggregated.
- [ ] Dragging, resizing, shape scaling, and edge adjustment are reversible.
- [ ] Layout changes do not alter semantic execution.
- [ ] Narrow, default, and wide sizes are usable.
- [ ] Keyboard controls and focus labels are understandable.
- [ ] No workload-specific renderer branch was introduced.

### Score

| Dimension | Score 0–3 | Evidence/reason |
| --- | ---: | --- |
| Legibility |  |  |
| Cross-view coherence |  |  |
| Interaction quality |  |  |
| Responsive quality |  |  |
| Renderer generality |  |  |

**Gate status:** `<draft / blocked / passed>`
**Reviewer:** `<name>`
**Notes:** `<remaining concern>`

---

## Gate 9 — Documentation, export, and release

### Command record

```bash
sviz export examples/<name>_vnext.yaml --format bundle --output dist/<name>
```

### Export matrix

| Artifact | Environment tested | Result | Evidence |
| --- | --- | --- | --- |
| Compiled JSON | `<consumer>` | `<pass/fail>` | `<note>` |
| Inline component | `<host page>` | `<pass/fail>` | `<note>` |
| Standalone HTML | `<browser/offline>` | `<pass/fail>` | `<note>` |
| Iframe snippet | `<host page>` | `<pass/fail>` | `<note>` |

### Checklist

- [ ] Guide states purpose, audience, provenance, and omissions.
- [ ] Guide explains elements and every checkpoint.
- [ ] Commands are reproducible.
- [ ] Regression tests cover goal-critical states.
- [ ] Inline, standalone, and iframe exports were tested.
- [ ] Multiple components do not leak styles or state.
- [ ] Export has no unavailable local dependency.
- [ ] Trace, guide, tests, and export use the same revision.
- [ ] Remaining limitations are visible to readers or maintainers.

### Score

| Dimension | Score 0–3 | Evidence/reason |
| --- | ---: | --- |
| Documentation completeness |  |  |
| Reproducibility |  |  |
| Portability |  |  |
| Release integrity |  |  |

**Gate status:** `<draft / blocked / passed>`
**Reviewer:** `<name>`
**Notes:** `<remaining concern>`

---

## Final acceptance

| Quality | Score 0–3 | Best evidence | Remaining limitation |
| --- | ---: | --- | --- |
| User-goal alignment |  |  |  |
| Source fidelity |  |  |  |
| Semantic integrity |  |  |  |
| Explanatory quality |  |  |  |
| Visual clarity |  |  |  |
| Renderer generality |  |  |  |
| Reproducibility |  |  |  |

- [ ] Every gate passed.
- [ ] Every final quality scored at least 2.
- [ ] No unresolved assumption changes the primary conclusion.
- [ ] User or designated reviewer approved the primary learning outcome.

**Final status:** `<not ready / release-ready / reference-quality>`
**Approval:** `<name and date>`
**Summary:** `<why this example does or does not meet the original goal>`
