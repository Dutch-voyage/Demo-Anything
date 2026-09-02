# Designing corresponding views that explain and verify

Use this guide when one claim needs two coordinated views: for example, code
and a runtime timeline, a measured trace and a resource map, or a paper model
and an observed result. The goal is not simply to make two pictures agree. The
goal is to make their relationship explicit enough that a reader can decide
whether the claim follows, and can see what would disprove it.

This is design guidance, not a proposal to change the current `sviz` IR or
renderer.

## The core test

Two projections of one authored calculation can establish **cross-projection
consistency**: the same inputs and rules produced compatible outputs. They do
not provide independent empirical verification. A bar and a timeline both
computed from `payload / assumed_bandwidth` will agree even when the bandwidth
assumption is wrong.

Genuine verification needs at least one of these:

- an independent evidence source, such as a measured event, counter, log, or
  separately sourced specification; or
- an executable semantic assertion that can fail, such as “every receive used
  by expert compute has completed in the same epoch.”

One view commonly acts as the **grounding (basis) plane** and the other as an
**explanatory (consequence) plane**. The grounding plane states the evidence or
model being reasoned from. The explanatory plane adds a mechanism or
consequence. It must not merely rescale the grounding plane.

Keep three axes independent:

| Axis | Example values | Question answered |
| --- | --- | --- |
| Plane type | code, timeline, topology, resource, residency, dataflow, state, comparison, model | How is the information projected? |
| Epistemic role | grounding, explanatory, corroborating, counterfactual | What job does this plane perform in the argument? |
| Provenance | source-linked code, measured trace, runtime event, paper specification, authored model, explanatory assumption | Where did each fact come from? |

A timeline can be grounding when it is measured and explanatory when it is
derived. A topology can likewise be either. Do not infer role or trust from
visual form.

## The verification ladder

Each rung adds a stronger check; higher rungs do not erase the need to label
provenance and assumptions.

| Rung | What it establishes | Example | What it does not establish |
| --- | --- | --- | --- |
| 1. Shared identity | Both views refer to the same semantic things | Selecting `buffer.rx.7` highlights it in both planes | That either view is correct |
| 2. Derived consistency | A declared transformation was applied consistently | Payload equals retained elements times encoded bits plus declared overhead | That the inputs or transformation match reality |
| 3. Executable assertion | A semantic contract is checked and may visibly fail | Compute cannot start before all of its required chunks are ready | Independent empirical support |
| 4. Independent evidence | A separately obtained observation can corroborate or falsify the explanation | Instrumented receive events are compared with predicted readiness | That every unmeasured assumption is true |

Use precise language in titles and captions: “consistent with,” “asserted by,”
“predicted by,” and “observed in” mean different things. Reserve “verified by”
for an actual assertion or independent comparison and state which one.

## Correspondence is a semantic contract

Coordination by color, position, or shared ID is useful interaction, but it is
not yet correspondence. Define the relation between planes before drawing it.

| Contract field | Authoring question |
| --- | --- |
| Stable identity | Which entity, operation, event, resource, or state has the same identity in both planes? |
| Measure transformation | What typed rule converts a grounding value into an explanatory value, including units and overheads? |
| Causal or dependency path | Which ordered dependencies justify the claimed consequence? |
| Cardinality and coverage | Is the relation one-to-one, one-to-many, many-to-one, or many-to-many, and which members may be absent? |
| Scene applicability | In which scenario and scene does the relation hold? When does it start or expire? |
| Granularity | Is correspondence per request, rank, expert, chunk, buffer, epoch, or aggregate? |
| Assumptions | Which capacities, policies, ordering rules, or counterfactual choices are not observed facts? |
| Expected disagreement | What mismatch is possible, how is it rendered, and what assertion or evidence would expose it? |

For example, a source call may map one-to-many to enqueue, copy, and completion
events. Coverage must say whether an optimized-away call or a sampled event is
allowed to have no partner. A buffer ID reused across epochs is not stable
identity unless the epoch participates in the key.

Write the relationship as a reviewable sentence:

> For every required receive chunk in epoch *e*, map the source-declared
> destination buffer to the measured completion event with the same buffer and
> epoch; dependent compute may begin after all chunks in its declared input set
> are complete. Missing, duplicate, late, or cross-epoch matches are failures.

That sentence carries more meaning than a coordinated highlight alone.

## An eight-step authoring workflow

### 1. State the claim and decision

Complete both prompts:

- **Claim:** What mechanism or consequence does the pair explain?
- **Reader decision:** What should a reader be able to accept, reject, compare,
  or investigate after five seconds and after a deeper inspection?

“Show communication” is too broad. “Decide whether expert compute waits on a
whole phase or only on its required chunks” is testable.

### 2. Identify truth sources and provenance

Inventory each fact before choosing marks. Useful provenance classes include:

- source-linked code;
- measured trace or counter;
- runtime event or event log;
- paper formula or specification;
- authored model;
- explanatory assumption; and
- counterfactual scenario.

Record a source locator where one exists, and label modeled or assumed values
in the view itself. A paper specification is authoritative about what the
paper states, not evidence that a particular runtime behaved that way. An
authored calculation can ground a hypothetical comparison, but cannot become a
measurement by being drawn as a timeline.

### 3. Choose plane types from the question

Do not default to a generic “System” canvas. Pick the smallest pair that makes
the decision possible:

| Plane | Best question |
| --- | --- |
| Code | Which source call, API contract, branch, or ownership rule initiated this? |
| Timeline | In what order did work, readiness, waiting, and overlap occur? |
| Topology | Through which endpoints and paths could or did traffic move? |
| Resource | Who owned finite links, engines, queues, SMs, or buffers, and when? |
| Residency | Where did each materialization live, and when was it valid or reusable? |
| Dataflow | Which values and dependencies produced the downstream value? |
| State | Which transitions were legal, observed, missing, or out of order? |
| Comparison | Which invariant dimensions and outcome dimensions differ by scenario? |
| Model | Which formulas, policy choices, assumptions, or predicted bounds apply? |

Prefer a code–timeline pair for an asynchronous API question, a trace–resource
pair for contention, and a model–measurement pair for a paper claim. Add a
third view only if a distinct question cannot be answered by inspection or a
detail panel.

### 4. Define identity, ordering, scenarios, and coordination

Define semantic keys before scene-local labels. Include an epoch, request, or
generation when storage and handles are reused. State whether ordering is
source order, enqueue order, dependency order, timestamp order, or a partial
order; they are not interchangeable.

Keep scenario parameters separate from invariants. A precision policy may
change while route identity, token counts, and destinations remain fixed.
Declare those invariants so a comparison cannot silently change the workload.

Selection and focus should coordinate by stable semantic identity and relation:

- selection answers “where else does this exact thing appear?”;
- related highlighting answers “what produced or consumes this thing?”; and
- scene focus answers “which causal step matters now?”

Do not manufacture a shared ID for different objects merely to synchronize
their colors.

### 5. Define typed correspondences and executable assertions

For every cross-plane relation, record the types at both ends, cardinality,
coverage, transformation or dependency, scene scope, and failure behavior.
Examples include:

- `source-call -> runtime-event[1..n]` via an enqueue/complete relation;
- `transfer-event -> resource-claim[1..n]` via route allocation;
- `paper-term[n] -> measured-series[0..n]` via a unit-normalized observation;
- `materialization -> consumer[n]` via read dependencies.

Turn important claims into checks. Useful assertions include conservation of
payload, legal state transitions, balanced create/retire lifecycles, capacity
limits, required-input readiness, epoch agreement, and scenario invariants.
Render failures at both endpoints and on the relation; do not hide them in a
validation console.

### 6. Model resources, readiness, and the downstream consumer

Before claiming time or latency, name:

1. the owner of each buffer, lane, queue, link, engine, or execution slot;
2. the event that makes each required input ready;
3. the synchronization scope—global, rank-local, expert-local, chunk-local, or
   resource-local;
4. the downstream consumer and its exact required-input set; and
5. competing work that shares the resource.

A transfer ending is only meaningful relative to a readiness contract and a
consumer. A blank gap is not automatically a wait, and an API return is not
automatically device completion.

### 7. Design a short causal scene sequence

Use a small number of scenes. Each scene should introduce one causal step while
preserving semantic identity across the sequence. A reliable pattern is:

1. establish invariant structure and evidence;
2. expose the relevant payload or event;
3. show resource allocation and readiness;
4. reveal the dependent consumer and critical path; and
5. compare the alternative or display disagreement.

Change scenario parameters explicitly; do not replace `route.e2` with a new
look-alike object between scenes. Keep prior context muted rather than deleting
the identities a reader is tracking.

### 8. Validate communication and failure visibility

Run a five-second test with someone who did not author the view: can they name
the grounding plane, the claimed consequence, and whether the data is measured
or modeled? Then check:

- keyboard selection, meaningful focus order, text alternatives, and
  non-color-only distinctions;
- readable units, labels, patterns, and contrast at supported sizes;
- responsive reflow without changing identity, ordering, or apparent
  causality;
- visible missing, duplicate, stale, out-of-range, and contradictory mappings;
  and
- an explicit empty/error state instead of silently dropping unmatched data.

## Synchronization and critical paths

A completed dependency DAG always has at least one maximum-duration path from
the chosen start boundary to the chosen completion boundary. That is the
critical path for those boundaries. It does **not** follow that “the largest
logical edge determines latency” in every execution model.

Choose the readiness contract first:

- **Whole-buffer or barrier.** When the contract requires every relevant edge
  to finish before the next phase, phase completion may be
  `max(edge.end)`. State the participating set and barrier scope.
- **Rank-local.** Each rank waits only for the inputs its next operation
  requires. Different ranks can become ready at different times; an invented
  global maximum exaggerates the dependency.
- **Per-expert or per-chunk streaming.** Readiness and compute overlap at that
  finer granularity. Layer latency is the maximum communication-plus-compute
  dependency path to the defined layer output, not merely the longest
  transfer.
- **Shared transport or execution resources.** With shared NICs, NVLink paths,
  queues, or communication SMs, contention can make aggregate injection or
  receive volume, queue order, or overall resource makespan the bottleneck.
  Several modest logical edges may serialize on one physical resource.

Async execution does not remove readiness dependencies. It can reduce host or
global synchronization and hide work behind independent useful work. For one
dependency, the exposed wait can be reasoned about as:

```text
exposed wait = max(0, communication_ready - useful_overlap)
```

The terms need a shared time origin and a declared consumer. For a DAG, compute
the dependency paths with actual readiness and resource constraints rather
than applying that scalar expression independently and summing the results.

Payload balancing generally reduces work before readiness, critical-tail
exposure, resource occupancy and interference, congestion, and backpressure.
It does not necessarily reduce the fixed cost of a synchronization primitive.
Distinguish less work arriving at a barrier from a cheaper barrier.

## Worked example: precision-aware expert traffic

This example uses the PACE concept to show the design method. It makes no claim
about a particular transport implementation. A fine-grained, SM-driven MoE
transport is one possible execution setting; its real contract must still come
from source documentation or measurements.

### Grounding plane: routes, counts, and precision

Hold four expert-route groups, `E0`–`E3`, fixed across scenarios. The grounding
plane shows each route identity, routed item count, precision allocation, and
resulting payload. Payload is a typed derivation, including any declared
packing or metadata overhead—not just a rectangle width.

```text
payload_i = count_i × retained_bits_i / 8 + metadata_i + padding_i
```

Declare rounding, grouping, encoding, and padding rules rather than assuming
the expression alone is byte-exact.

```text
fixed route/count ── retained bits + encoding rule ──> payload
       │                                                │
       └──────── scenario-invariant identity ───────────┘
```

Use three explicitly labeled scenarios:

- **Uniform floor:** all groups use the low-bit floor.
- **Uniform wider:** all groups use the same wider precision.
- **PACE allocation:** precision is pruned on traffic that affects the
  critical tail while lighter traffic retains additional precision, subject to
  the stated policy and accuracy model.

The grounding view should make unchanged routing obvious: `E0` remains `E0`,
with the same route and item count, in all three scenarios. Precision and
payload may change. If counts or routes change, the comparison no longer
isolates precision allocation and must say so.

### Explanatory plane: communication and dependency

The second plane must show an actual modeled or observed schedule: resource
ownership, queueing, transfers, readiness events, dependent expert compute,
and the chosen completion boundary. The required causal chain is:

```text
retained bits → payload → resource schedule → readiness event
              → dependent compute → critical path
```

`bytes / constant bandwidth` may be a declared service-time assumption inside
an illustrative model. It is not, by itself, communication completion: it
omits queueing, sharing, startup, receiver work, backpressure, readiness scope,
and the consumer. Label an illustrative schedule prominently as **modeled—not
measured** and show its assumptions beside it.

Each uniform-precision scenario should expose its critical traffic and
downstream wait, not only differently sized bars. The PACE scenario should
show all of the following:

- pruning on the critical traffic;
- retained precision on lighter traffic;
- changed readiness and critical path relative to uniform wider precision when
  the modeled allocation produces that improvement;
- unchanged route identities and counts.

Under a floor-frontier policy, PACE **may** improve modeled accuracy at the
same makespan as the uniform low-bit floor while reducing makespan relative to
the uniform wider-bit baseline. This conclusion is conditional: it requires
the allocated payloads to fit the floor scenario's actual critical-path or
resource frontier, while the added bits improve the declared accuracy
objective. It is not guaranteed by payload totals alone.

### What can falsify the explanation

Render disagreement if any of these occur:

- measured readiness order or completion exceeds the modeled bound;
- the assumed bottleneck resource is idle while an unmodeled resource stalls;
- dependent compute starts before the model says its inputs are ready, showing
  that the assumed readiness scope was too broad;
- dependent compute waits after all modeled inputs are ready, revealing a
  missing dependency or resource;
- routing or counts differ between scenarios advertised as invariant; or
- independent quality measurements do not improve under the PACE allocation.

An assertion can check route/count invariance, payload derivation, resource
capacity, and readiness-before-consume. Instrumented events or counters are
still required to test whether the illustrative schedule matches a runtime.

## Reusable scenario patterns

### Source-code API and runtime timeline

The source plane is authoritative about calls, parameters, buffer declarations,
and the documented API contract. A runtime timeline maps each call to enqueue,
return, device work, completion, and first dependent use. It can verify an
asynchronous return and a late wait only when events come from independent
instrumentation or when an executable assertion checks the contract.

Track buffer and lane ownership plus epochs. A fast host return does not prove
useful overlap; show the independent work that occupies the interval. A
completion in epoch 8 cannot satisfy a consumer in epoch 9 simply because the
same buffer address was reused.

Principal failures include a wait earlier than claimed, use before completion,
wrong-lane work, cross-epoch matching, and reuse before the prior consumer
releases ownership.

### Measured trace timeline and topology/resource view

Here the measured trace is the evidence. The explanatory plane projects events
onto links, engines, SMs, queues, buffers, or residency intervals. Declare how
trace IDs map to resources and how multiplexed or sampled events affect
coverage.

The pair can reveal contention, serialization, head-of-line blocking, or
buffer residency that a flat timeline obscures. It fails when events map to no
resource, one exclusive event maps to conflicting owners, resource capacity is
exceeded, or predicted contention is absent from the trace.

### Paper/model comparison and measured or counterfactual result

Use the grounding plane to show formulas, specification terms, parameter
ranges, and assumptions with source locators. The corresponding plane may be:

- a measured result, which independently tests a prediction; or
- a counterfactual result, which explores the model but is not evidence of
  real behavior.

Normalize units and experimental conditions before relating terms to series.
Visually separate measurements, derived values, interpolations, and unsupported
assumptions. Failure signals include observations outside a stated bound,
missing parameter coverage, unit or condition mismatches, and a conclusion
that depends on an unsupported assumption.

### Optional extensions

- **State machine and event log:** map each log record to a legal transition;
  flag missing, duplicate, impossible, or out-of-order transitions.
- **Dataflow and residency:** map produced values to materializations and their
  consumers; flag reads before creation, use after retirement, unwanted
  aliases, capacity excess, or an unexplained copy.

## Scenario matrix

| Task | Recommended pair | Grounding source | Correspondence relation | Principal failure signal |
| --- | --- | --- | --- | --- |
| Code/API behavior | Code + runtime timeline | Source-linked calls and API contract | Call to enqueue/return/complete/use events, including buffer, lane, and epoch | Early use, late or wrong-lane event, premature reuse |
| System process | Dataflow or topology + resource/timeline | Authored dependency model or runtime events | Operation/flow to claims, readiness, and consumers | Capacity violation, missing dependency, unexplained wait |
| Trace diagnosis | Measured timeline + topology/resource | Instrumented trace and counters | Event to physical path, engine, queue, buffer, or SM | Unmapped event, ownership conflict, absent/present contention mismatch |
| Paper idea | Model/comparison + measured result | Cited formula or specification plus independent experiment | Term/prediction to unit-normalized observation | Bound violation, condition mismatch, missing coverage |
| Future scenario | Model/comparison + counterfactual | Declared authored model and scenario parameters | Parameter change to predicted consequence | Assumption violation or scenario changes an invariant |
| PACE concept | Route/payload grounding + communication/dependency | Fixed routes/counts and declared precision policy | Bits to payload to resource/readiness/consumer path | Changed routing, readiness mismatch, or no quality gain |
| Stateful protocol | State machine + event log | Specification and observed records | Record to legal epoch-scoped transition | Missing, duplicate, or illegal transition |

## Good and bad mini-examples

### Async API

**Bad:** A source call highlights a same-colored device bar. The gap after the
call is labeled “overlap,” and the last bar is labeled “synchronized.”

**Good:** `call.42` maps to an enqueue and device completion in epoch 7. The
timeline shows the independent kernel that overlaps it, the buffer owner, the
first consumer, and the event on which that consumer waits. An assertion flags
use before completion or cross-epoch matching.

### Payload and latency

**Bad:** The second view redraws each payload bar with its width divided by a
constant and calls the result completion time.

**Good:** Payload feeds a labeled service-time assumption, then a shared-NIC
queue and receive resource, then per-chunk readiness and dependent compute.
Modeled marks are visually distinct from measured events. Queue delay or a
readiness mismatch can make the two disagree.

### Paper claim

**Bad:** A paper equation and a smooth curve share colors, with no units,
parameter range, or indication that the curve was generated from the equation.

**Good:** Terms map to a derived prediction with units and an applicability
range. Separately measured points retain error bars and experiment provenance.
Residuals outside the declared tolerance appear as visible correspondence
failures.

### Trace and resource

**Bad:** Timeline lanes are named after devices, but there is no ownership or
capacity relation and omitted trace events disappear silently.

**Good:** Every event has zero or more explicitly permitted resource mappings;
exclusive claims are checked against capacity, sampling gaps are marked, and
unmapped events remain visible in an “unresolved” lane.

## Anti-patterns

- **Arbitrary coordinated shapes:** matching color or geometry implies a
  relationship whose type and failure conditions are undeclared.
- **Text-only semantics:** captions claim causality, readiness, or ownership
  that the data model and marks cannot inspect or validate.
- **Rescaled duplicate charts:** both planes encode the same authored number
  under a deterministic scale and add no mechanism or consequence.
- **Invented global barriers:** all ranks wait on a global maximum even though
  each consumer has a smaller required-input set.
- **Timelines without consumers or readiness:** transfer endpoints appear, but
  nothing defines when data is usable or which work depends on it.
- **Hidden provenance:** predictions, assumptions, interpolations, and measured
  observations use indistinguishable marks.
- **Identity replacement between scenes:** objects are deleted and recreated
  for each scenario, making coordinated selection and invariant review
  impossible.
- **Payload-as-latency:** bytes divided by nominal bandwidth is presented as an
  observed completion time.
- **Aggregate-only explanation:** totals hide skew, critical tails, queueing,
  and per-consumer readiness.
- **Invisible disagreement:** unmatched or contradictory items are dropped,
  recolored as normal, or reported only outside the view.

## Review checklist

Before review, confirm:

- [ ] The claim and reader decision fit in one sentence each.
- [ ] Grounding and explanatory roles are labeled independently of plane type.
- [ ] Every fact is marked as sourced, measured, derived, modeled, assumed, or
      counterfactual, with a locator where applicable.
- [ ] The explanatory plane adds a mechanism or consequence.
- [ ] Correspondences declare identity, transformation or dependency,
      cardinality, coverage, scene scope, granularity, and assumptions.
- [ ] At least one important relation has an assertion or independent evidence
      that can falsify it.
- [ ] Resource ownership, queueing, readiness scope, and the downstream
      consumer are explicit for every time claim.
- [ ] The critical path uses declared start/completion boundaries and the right
      barrier, rank, expert, or chunk granularity.
- [ ] Scenario parameters change without silently changing invariants.
- [ ] Scenes preserve stable identities and introduce one causal step each.
- [ ] Selection, focus, and relation highlighting work without relying only on
      color.
- [ ] Missing, duplicate, stale, and contradictory mappings are visible.
- [ ] The pair passes five-second, keyboard, contrast, reflow, and narrow-screen
      checks.

## Acceptance rubric

Score each row from 0 to 2: **0** missing or misleading, **1** present but
ambiguous or incomplete, **2** explicit and testable. A publishable pair
should score 2 on the first five rows, have no 0, and score at least 16/20.

| Criterion | A score of 2 means |
| --- | --- |
| Claim and decision | A reader can state what the pair claims and decide what action or conclusion follows. |
| Epistemic clarity | The reader can explain why alignment alone is not verification and distinguish facts, derivations, assumptions, and observations. |
| Plane choice | The pair fits the code, system, trace, paper, or counterfactual question without a generic catch-all canvas. |
| Semantic correspondence | Types, identities, transformation/dependency, cardinality, coverage, scope, granularity, and assumptions are inspectable. |
| Falsifiability | A named assertion or independent evidence can visibly disagree with the explanatory view. |
| Mechanism | The explanatory plane adds causal, resource, state, residency, or outcome information rather than rescaling the grounding plane. |
| Synchronization | Ownership, readiness boundary, consumer, overlap, and critical-path endpoints are explicit. |
| Scenario integrity | Invariants remain stable; changed parameters and provenance are obvious. |
| Scenes and coordination | Stable identities survive scenes; selection and focus expose exact and related items accessibly. |
| Communication quality | Five-second comprehension, responsive layout, accessibility, and disagreement states pass review. |

## Implications for a future generic DSL

These practices suggest capabilities a future generic visualization language
may need; they are design requirements to explore, not an implementation RFC:

- typed plane roles and provenance, independent of visual plane type;
- typed correspondence with explicit cardinality, coverage, granularity, and
  scene applicability;
- validated derivations, assumptions, units, and executable assertions;
- first-class resource ownership, readiness events, consumer dependencies, and
  synchronization scope;
- distinct barrier, aggregate/resource-makespan, and dependency-path marks;
- scene-scoped relations that preserve semantic identity across scenarios;
- coordinated exact selection, related-item focus, and accessible highlighting;
- visible disagreement, missing evidence, uncertainty, and invalid-relation
  rendering; and
- normalized intermediate representation so facts and relationships remain
  inspectable across renderers.

The durable abstraction is not “two canvases.” It is two explicitly sourced
semantic projections connected by relations that state how they may agree—and
how they can fail.
