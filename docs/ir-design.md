# Systems Visualization IR — design draft

**Status:** Implemented contract, versioned `0.2-draft`
**Scope:** Authored educational visualizations and sampled execution traces

The first two implementations are described in
[`flash-attention-workflow.md`](flash-attention-workflow.md) and
[`deepep-workflow.md`](deepep-workflow.md).

## 1. Goal

The system converts code, traces, or authored examples into portable,
interactive explanations of system structure and execution.

Users describe facts and meaning. The compiler derives state and display
plans. The renderer draws those plans without knowing the workload domain.

```text
code, trace, or authored example
  → raw facts
  → semantic IR
  → validation
  → execution compilation
  → display planning
  → system, timeline, and narrative projections
  → portable renderer
```

The same renderer must handle FlashAttention, collective communication,
schedulers, memory movement, distributed routing, and other structures without
branches on workload names or tags.

## 2. Three authoring artifacts

The design separates three kinds of input.

### Model definition

Defines stable meaning and structure:

- place hierarchy and topology;
- logical entity types;
- capacities and resources;
- operation and flow definitions;
- static relationships.

### Execution facts

Defines one authored or observed run:

- operation and stage instances;
- start/end times or authored steps;
- materialization lifecycle effects;
- resource claims;
- quantities and metric samples.

Facts may be hand-authored, emitted by an instrumentation SDK, or translated
from an existing trace.

### View recipe

Defines presentation intent without changing semantics:

- initial projection and focus;
- preferred grouping and hierarchy expansion;
- important entities and resources;
- checkpoint density;
- aggregation and label preferences.

Small examples may place all three artifacts in one file. They remain separate
conceptually and in the compiled output.

## 3. Semantic concepts

| Concept | Scope | Default representation |
| --- | --- | --- |
| Logical entity | Stable identity and meaning | Inspector identity or lineage root |
| Materialization | One concrete resident or in-flight instance | Object, stack, population, or payload |
| Place | Hierarchical containment or execution location | Container |
| Link | Possible adjacency or transport path | Structural edge or channel |
| Resource | Capacity domain such as bytes, bandwidth, slots, or engines | Meter or timeline lane |
| Operation | User-meaningful work | Narrative and selection group |
| Stage | Scheduled, resource-owning part of an operation | Timeline interval and active system mark |
| Flow | Correlated DAG of transport stages | Route or route bundle |
| Collection | Group of similar entities or materializations | Stack, count, or flow band |
| Coordination artifact | Non-spatial persistent state such as a plan or handle | Inspector item or phase connector |
| Relation | Dependency, provenance, membership, or derivation | On-demand highlight |
| Metric | Observed numeric value | Meter, counter, sparkline, or inspector value |

Concept boundaries are strict:

- a place is not a resource;
- a link is not current traffic;
- a logical entity is not a physical copy;
- an operation is not necessarily one scheduled interval;
- a flow is not necessarily one direct transfer;
- an event is not automatically a visible dot.

## 4. Identity and lifecycle

Logical identity is separated from physical materialization.

For example, a K tile in HBM and its copy in shared memory are two
materializations of one logical entity. A token routed to two experts has one
logical identity and two routed materializations.

The lifecycle effect algebra is:

- `create`: introduce a materialization, optionally with provenance;
- `place`: make a materialization resident in a place;
- `unplace`: remove residency without retiring identity;
- `retire`: end a materialization's lifetime;
- `update`: change state while preserving identity;
- `relate`: create provenance, membership, dependency, or another relation.

Convenience operations compile to this algebra:

```text
copy(source, destination)
  = retain source
  + create destination materialization
  + relate destination to source

move(materialization, destination)
  = unplace source
  + place the same materialization at destination
```

Production, consumption, assembly, accumulation, replacement, and selection
must be expressed through explicit lifecycle effects and write policies. The
compiler never guesses copy versus move from an arrow.

## 5. Operations, stages, and flows

An operation describes what the user believes is happening. A stage describes
where and when part of that operation runs and which resources it owns.

One operation may contain several stages. For example, a remote dispatch can
contain pack, RDMA transfer, NVLink forwarding, and receive stages.

A flow correlates materialization movement across stages. Its shape is a DAG,
which permits:

- sequential routes;
- fan-out and fan-in;
- local and remote branches;
- joins, retries, and alternate paths;
- chunked or pipelined execution.

Operations and flows are selection scopes. Stages are the atomic scheduling and
resource-accounting units.

## 6. Authored time and compiled events

The author chooses one time mode:

- `timeline`: stages provide numeric start and duration;
- `steps`: stages provide authored integer steps, and stages sharing a step are
  parallel.

The compiler does not invent missing timing. It derives event boundaries from
the supplied schedule and creates deterministic snapshots and deltas.

At a shared boundary, ordering is:

1. finish stages;
2. apply completion effects;
3. release resources;
4. start stages;
5. claim resources.

A checkpoint is a reader-facing cursor stop over one or more event boundaries.
The compiler may suggest checkpoints; the author may merge, hide, name, or
explain them. Manual stepping uses checkpoints, not animation frames.

### Reader content

Each checkpoint may carry an authored Markdown `narrative`. Plain `detail`
text remains a fallback for existing traces. The compiled checkpoint preserves
the Markdown source; editing it in the viewer changes reader state, not
execution state. The renderer supports headings, paragraphs, emphasis, links,
inline and fenced code, lists, and blockquotes without loading a network
dependency.

An `annotation` is an editorial pin with an ID, semantic `anchor`, optional
checkpoint scope, title, body, and `unresolved` or `resolved` status. Pins are
not activities, dependencies, or metrics. They remain attached to their
semantic anchors as layouts move or resize, and resolved pins remain visible.
The browser may create and edit local pins; hosts receive explicit
`narrative-change` and `annotation-change` events if they want to persist those
reader edits. Annotation changes report `create`, `update`, `status`, or
`delete`; deletion removes the local pin immediately without changing the
compiled source document.

Persisted reader state is a separate versioned overlay. It records narrative
overrides, annotation additions and overrides, authored-annotation tombstones,
normalized place and edge layout, and an explicitly saved projection and
checkpoint. It identifies the immutable compiled base by visualization ID and
content digest. The overlay never changes lifecycle, timing, topology, or
resource semantics.

## 7. Resources and metrics

A resource has a capacity, unit, owner, and optional scheduling policy. A stage
claims resource quantities over its interval.

Examples include:

- shared-memory bytes owned by a place;
- transfer bandwidth owned by a link;
- copy-engine slots owned by a device;
- compute slots owned by an execution unit.

The compiler builds a resource ledger at every event boundary by aggregating
claims and resident materialization quantities. Capacity violations are
semantic validation errors or explicit oversubscription states.

Metrics are observations. They do not replace resource claims. When occupancy
can be derived from lifecycle and quantity, it should be compiled rather than
authored again as a metric.

## 8. Collections and scale

Large scenarios are represented by collections rather than thousands of small
marks. Collections preserve:

- membership or a reproducible membership rule;
- quantity and units;
- grouping keys;
- representative or selected members;
- source and destination distributions where relevant.

The display planner chooses among individual objects, stacks, populations, and
aggregated flows using cardinality, concurrency, hierarchy, available space,
and the view recipe. It never chooses based on workload names.

## 9. Compilation products

### Validated semantic graph

Contains normalized identities, hierarchy, topology, operations, stages,
flows, lifecycle effects, dependencies, quantities, and resource definitions.

### Execution program

Contains an ordered `views` collection. Each entry has stable authored
identity and a rendering kind such as `spatial` or `timeline`, plus the
kind-specific plan. It also contains:

- ordered events;
- materialization lifetimes and residency;
- active stages and flows;
- resource ledgers;
- collection membership;
- metrics;
- state deltas and deterministic snapshots.

It contains no coordinates or renderer-specific markup.

### Display plan

Contains:

- representation choice and aggregation;
- initial hierarchy expansion;
- stable place and object slots;
- route geometry and parallel route slots;
- timeline lanes and row packing;
- label priority;
- inspector-only elements;
- responsive policies for supported container profiles.

All view plans share semantic IDs, cursor positions, selection, and checkpoint
definitions. The renderer derives tabs from this collection; it does not
invent a fixed pair of projections.

## 10. Renderer and interaction boundary

The renderer receives compiled display plans and handles only:

- responsive pixel fitting;
- drawing and interpolation;
- hit testing, focus, and selection styling;
- cursor navigation;
- accessibility behavior.

It does not reconstruct lifecycle, aggregate resources, assign timeline lanes,
or infer workload meaning.

Reader interaction state is separate from semantic state:

- cursor;
- selection;
- expanded/collapsed hierarchy;
- selected projection;
- manual place offsets;
- edited checkpoint narratives;
- local annotations and annotation status;
- note position and size.

Dragging a place changes only its display offset. Children move with their
parent, links reconnect to the new boundary, and execution semantics remain
unchanged. Explicitly saved view state may restore these offsets later.

## 11. Code-to-IR workflow

The standard workflow is:

1. State the question the visualization should answer.
2. Identify places, entities, resources, operations, and important flows.
3. Choose hand authoring, SDK instrumentation, or a trace adapter.
4. Emit plain, append-only execution facts.
5. Apply mapping rules that group low-level facts and attach lifecycle meaning.
6. Validate identities, lifecycle, topology, timing, dependencies, and capacity.
7. Compile events, deltas, snapshots, flow state, and resource ledgers.
8. Review compiler-proposed checkpoints and add concise narrative where needed.
9. Apply authored view definitions and compile an ordered collection of view
   plans.
10. Preview every rendered mark with provenance back to its semantic concept and
    source facts.

Static code analysis can suggest call structure and dependencies. Runtime
instrumentation supplies concrete instances, branches, quantities, and timing.
Authored mapping is still required for meaning that code does not express, such
as logical identity, copy semantics, grouping, and teaching intent.

## 12. Validation requirements

The compiler validates:

- unique and resolvable IDs;
- acyclic place hierarchy and dependencies;
- valid stage timing for the selected time mode;
- valid materialization lifecycle and residency;
- legal copy, move, update, retirement, and provenance effects;
- flow continuity across topology;
- dependency ordering;
- aggregate resource capacity;
- compatible concurrent writes and merge policies;
- collection quantities and membership;
- metric target and unit consistency.

Diagnostics name the semantic entity, source fact, and mapping rule involved.

## 13. FlashAttention proof target

The first complete proof will model one FlashAttention forward tile with
several streamed K/V tiles.

It must demonstrate:

- HBM, shared memory, register/accumulator state, and compute resources;
- HBM-to-shared-memory copies that retain HBM materializations;
- QK, online-softmax, and PV stages grouped into tile-iteration operations;
- prefetch and compute overlap;
- temporary score/probability lifecycles;
- derived shared-memory occupancy;
- double-buffer reuse and release;
- output normalization and store;
- shared checkpoints across system and timeline projections;
- draggable top-level places as presentation-only state.

The example is an authored explanatory schedule, not an instruction-level CUDA
trace. Kernel fences, warp synchronization, and individual memory instructions
remain inspectable details rather than default lanes.

## 14. Resolved design problems

| Problem | Decision |
| --- | --- |
| Copy and move looked identical | Separate logical entities from materializations and compile explicit lifecycle effects |
| Fan-out could not preserve identity | Represent flows as DAGs and create related materializations per branch |
| Places and utilization were conflated | Separate places, links, resources, claims, and metrics |
| Browser code inferred semantics | Compile execution state and display plans before rendering |
| System and timeline views diverged | Share semantic IDs, cursor, checkpoints, and selection |
| Large cases produced tiny unreadable marks | Compile collections and representation levels instead of shrinking indefinitely |
| Fixed layouts did not fit every scenario | Use deterministic initial planning plus responsive policies and manual place offsets |
| Automatic playback obscured authored teaching steps | Make semantic checkpoint stepping the default |
| Floating embeds mixed host and trace state | Keep note and saved view state outside execution semantics |
| Domain-specific examples threatened renderer generality | Permit domain labels, but forbid renderer branches on labels or tags |

## 15. Deferred decisions

The following are intentionally outside the first proof:

- automatic extraction of meaning from arbitrary source code;
- instruction-level GPU simulation;
- production-scale trace ingestion and performance diagnosis;
- automatic multilevel semantic zoom;
- collaborative or account-synchronized saved views;
- custom domain renderers in the generic core;
- a final concrete serialization schema for every compiled concept.

The FlashAttention proof should refine the serialization schema without
weakening these boundaries.
