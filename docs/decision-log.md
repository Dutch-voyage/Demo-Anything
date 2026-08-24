# Design decision log

## 2026-08-24 — Enable persistence in the local viewer by default

**Status:** Implemented

### Decision

`sviz view` configures a file-backed state endpoint automatically while
retaining explicit Save/Reload actions. The default file lives in `.sviz/`
beside the trace and is not created until the first save. `--no-persist`
provides an explicit stateless mode. Annotation display numbers are scoped to
the current checkpoint so hidden annotations cannot make a visible list begin
at an unexplained number.

## 2026-08-24 — Persist reader edits as a separate viewer-state overlay

**Status:** Implemented

### Decision

Give every trace a stable top-level ID and compile a deterministic base digest.
Persist editable narratives, annotation overrides and tombstones, normalized
layout, and saved view in a separately versioned `0.1` viewer-state document.
The Web Component exposes snapshot import/export and explicit load/save through
a host-provided `state-src`; it never assumes a storage vendor.

Use revision numbers and `If-Match` for optimistic concurrency. The local
FastAPI viewer offers an atomic file-backed adapter by default, with
`--state-file` as a location override. This adapter is intended for development
and single-process deployments; production hosts replace the endpoint while
keeping the browser contract.

## 2026-08-24 — Keep reader content to narratives and pinned annotations

**Status:** Implemented

### Decision

Use one editable Markdown narrative per checkpoint as the primary explanation.
Keep annotations as pinned editorial objects only: every annotation references
a semantic anchor, may be scoped to one checkpoint, and has an explicit
`unresolved` or `resolved` status. Resolved pins remain visible so review
history is not mistaken for deleted content.

Narrative edits, locally created pins, and status switches are reader state;
they do not mutate compiled execution semantics. The portable component emits
`narrative-change` and `annotation-change` so a host can choose how to save
them. No automatic browser persistence is added in this change.

## 2026-08-24 — Split MLA into prefill and decode examples

**Status:** Implemented

### Decision

Use two step-mode examples for the absorbed MLA dataflow. Prefill starts with a
four-token hidden-state batch, creates separate `cKV` and positional `kR` cache
materializations, scores causally, reduces in latent space, and leaves a compact
cache. Decode starts from that cache, appends one `cKV` and one `kR` row, scores
the new query over all five positions, and produces one output.

Keep full per-head keys and values absent from the semantic model. Cache writes
are explicit copies with provenance, and the storage ledger derives BF16 cache
growth from 4,608 to 5,760 bytes. Use authored steps because the examples
explain architecture rather than claim a production kernel schedule. The same
places, resources, Timeline lanes, and renderer handle both phases.

## 2026-08-23 — Promote vNext and remove the earlier IR

**Status:** Implemented

### Decision

Keep only the semantic vNext pipeline and its FlashAttention-2 and DeepEP
examples. Promote `validate`, `schema`, `compile`, `view`, and `export` to the
root CLI and expose only `load_trace`, `validate_trace`, `compile_trace`, and
`export_trace` as the public Python workflow. Remove the earlier schema,
renderer, note shell, traces, compiled fixtures, exports, tests, and guides.

The surviving wire format remains explicitly versioned `0.2-draft`; promotion
of the interface does not claim schema stability.

## 2026-08-23 — Use DeepEP to prove fan-out, fan-in, and shared routes

**Status:** Implemented as a draft

### Decision

Use classical DeepEP's normal dispatch/expert/combine cycle as the second
complete vertical slice. Model logical tokens separately from their routed
materializations, keep source tokens resident during top-k fan-out, preserve
multi-leg flows, and use the dispatch handle as non-spatial coordination state.
Combine retires expert contributions and creates one restored output per source
token.

Concurrent transfers sharing one compiled link remain individually selectable,
but the System projection distributes their motion phases and shows one count
label for the route. This is a generic link-density policy: neither compilation
nor rendering branches on DeepEP, MoE, transport, or expert labels.

The mechanism boundary is recorded in [`deepep-mechanism.md`](deepep-mechanism.md)
and the source-to-display mapping in [`deepep-workflow.md`](deepep-workflow.md).

## 2026-08-23 — Keep sizing and routing in presentation state

**Status:** Implemented in the draft renderer

### Decision

Global object-shape scale, manual place size, and manual place position are
reader view state. They must never modify topology, timing, resource claims, or
materialization state. The portable component exposes a `shape-scale`
attribute, toolbar controls, accessible place resize handles, reset behavior,
and complete values in its `layout-change` event.

Compiled links continue to identify semantic endpoints. The renderer resolves
their actual ports after responsive fitting and manual layout changes. A route
may be direct only when its geometry is unobstructed and long enough to display
its label; otherwise it uses an exterior channel. Routes render with endpoint
clearance and a contrasting halo above place fills so intermediate shapes
cannot silently hide them. These decisions depend on current geometry rather
than workload names.

The compiler reserves dynamic edge bands from route count, and the renderer
spaces exterior lanes far enough apart for labels. An active route has one
label: either its structural name, its active stage, or a compact transfer
count. Readers can enable **Adjust edges** and drag or keyboard-adjust a route
handle. Per-edge offsets are presentation state, are included in
`layout-change`, and reset without modifying the compiled endpoints.

Timeline event labels follow the same presentation-state rule. A mark owns a
strict clip boundary and selects its label font and abbreviation from rendered
width. Very short marks remain visible, isolated capsules without inline text;
their complete semantic label stays available through selection and accessible
description rather than overflowing into adjacent events.

## 2026-08-23 — Use FlashAttention-2 as the first complete vertical slice

**Status:** Implemented as a draft

### Decision

Prove the new pipeline with one query tile and three streamed K/V tiles. Keep
the schema, compiler, server, commands, and Web Component independent until
more scenarios validate the abstractions.

The example must use explicit materializations and lifecycle effects, derive
shared-memory occupancy, expose prefetch/compute overlap, compile resource lanes,
share checkpoint and selection state across projections, and support manual
top-level place movement without changing semantics.

The renderer consumes only compiled concepts. It contains no FlashAttention
branches. The complete mapping and commands are recorded in
[`flash-attention-workflow.md`](flash-attention-workflow.md).

## 2026-08-23 — Rebuild around semantic execution and display compilation

**Status:** Accepted for the new implementation

### Context

The existing visualization is a prototype, not a base for incremental renderer
changes. It leaves lifecycle reconstruction, resource interpretation, event
summaries, and timeline packing in the browser. It also lacks a sufficient
identity model for copies, fan-out, fan-in, and multi-stage flows.

### Decision

Build the replacement around three separate artifacts:

1. a model definition for stable structure and meaning;
2. execution facts for one authored or observed run;
3. a view recipe for presentation intent.

Compilation produces a validated semantic graph, a cursor-independent execution
program, and deterministic system and timeline display plans. The renderer only
fits and draws those plans.

Adopt the following semantic distinctions:

- logical entity versus physical materialization;
- place and link versus resource and current claim;
- operation versus scheduled stage;
- structural link versus DAG-shaped flow;
- non-spatial coordination artifact versus resident object;
- metric observation versus derived resource ledger;
- semantic state versus reader view state.

Use explicit lifecycle effects: `create`, `place`, `unplace`, `retire`,
`update`, and `relate`. Copy creates a related destination materialization while
retaining the source. Move changes the placement of the same materialization.

Collections and representation policies handle scale. Manual dragging changes
display offsets only; it does not mutate topology or execution semantics.

Manual checkpoint stepping remains the default interaction. System and timeline
projections share semantic IDs, cursor, checkpoints, hierarchy state, and
selection.

The concise design contract and the first FlashAttention proof requirements are
recorded in [`ir-design.md`](ir-design.md).

### Consequences

- The earlier schema and renderer are replaced rather than migrated field by
  field.
- Source adapters target raw facts or semantic IR, never drawing primitives.
- Domain labels and tags remain data; the compiler and renderer do not branch on
  workload names.
- The compiled serialization will be finalized through complete examples,
  starting with FlashAttention.

## 2026-08-21 — Add a display-planning compilation layer

**Status:** Accepted

### Context

The visualization must generalize across scenario shape rather than workload
name. FlashAttention, scheduling, MoE, and resharding differ in topology,
cardinality, hierarchy, concurrency, timing, and density, but use the same IR
primitives. Letting the browser renderer infer semantics and layout directly
from those primitives makes behavior hard to test and encourages
scenario-specific branches.

### Decision

Use the following pipeline:

```text
Authored IR
  → semantic validation
  → cursor-independent state compilation
  → deterministic display planning
  → system and timeline projections
  → portable Web Component rendering
```

Responsibilities are separated as follows:

- The authored IR defines meaning: places, objects, links, activities, metrics,
  dependencies, quantity, hierarchy, resources, and authored time.
- Semantic validation checks references, lifecycle, timing, capacity, resource,
  and dependency invariants.
- State compilation derives explicit object lifecycle, event boundaries,
  capacity changes, resource ownership, metric changes, and human-readable
  event diffs at each authored cursor.
- The display planner chooses representation, aggregation, hierarchy expansion,
  stable geometry, label policy, route slots, timeline lanes, and density level.
- The system and timeline projections consume the same entity IDs, cursor,
  selection, and hierarchy state.
- The Web Component renders a display plan. It does not branch on workload
  names, labels, or domain-specific tags.

The display planner is deterministic and produces a versioned, JSON-serializable
plan that can be golden-tested without a browser. Optional presentation hints
may influence emphasis and layout, but cannot change trace semantics.

### Representation policy

When space or entity count changes, the planner changes representation instead
of shrinking text and controls indefinitely:

- places: full container, compact container, collapsed hierarchy, or summary;
- objects: labeled object, small stack, population, or aggregated flow;
- links: structural connection, capacity channel, parallel route slots, or
  aggregated flow;
- activities: local event, transfer event, checkpoint, interval, or concurrent
  event group;
- metrics: integrated into their target or inspector.

### Interaction invariants

- Stepping changes the shared global cursor.
- Selection reveals detail without changing time.
- Hierarchy expansion and focus affect presentation, not trace semantics.
- System and timeline views preserve the same cursor and selection.
- Individually rendered transfers retain visible object identity.

### Initial proof

Before integrating the new planner into the current renderer, exercise one
data-driven prototype with no renderer changes across:

1. one transfer;
2. multiple simultaneous transfers sharing a route;
3. fan-out followed by fan-in.

This proof establishes collision, route-slot, aggregation, and timeline-lane
rules before the compiled format is revised.
