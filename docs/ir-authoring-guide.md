# IR authoring guide

This is the practical manual for understanding the `sviz` IR and defining a
trace that the generic compiler can turn into System, Timeline, narrative, and
inspector views. It describes version `0.2-draft`.

For the broader process of investigating code, reviewing evidence, and scoring
example quality, continue with the [code-to-demo user manual](user-manual.md).

## 1. The mental model

An `sviz` trace is not drawing instructions. It is a small semantic account of
one execution:

```text
stable structure + one execution + teaching checkpoints + view hints
    → semantic validation
    → deterministic state snapshots and display plans
    → System, Timeline, narrative, and inspector projections
```

Keep four layers distinct:

| Layer | Defines | Must not define |
| --- | --- | --- |
| Structure | identity, containment, topology, capacity | current traffic or pixel coordinates |
| Execution | time, reads, resource claims, lifecycle changes | visual animation instructions |
| Teaching | checkpoints, explanations, focus, review pins | hidden semantic mutations |
| View recipe | initial roots, lanes, importance, draggable places | workload-specific rendering behavior |

The compiler reconstructs the state at every checkpoint. The renderer receives
that compiled state and chooses generic visual primitives. Neither component
should infer workload meaning from names such as “FlashAttention” or “DeepEP.”

## 2. Concepts and their automatic displays

| IR concept | Meaning | System projection | Timeline / inspector |
| --- | --- | --- | --- |
| `place` | Container or execution location | Nested container | Stage grouping and metadata |
| `resource` | Capacity owned by a place or link | Capacity meter | Lane and claim accounting |
| `link` | Possible transport adjacency | Structural edge | Transfer route metadata |
| `entity` | Stable logical identity | Lineage identity | Quantity and attributes |
| `materialization` | One concrete resident copy | Object, stack, or population | Residency and provenance |
| `operation` | Reader-meaningful work | Selection group | Groups its scheduled stages |
| `stage` | Atomic scheduled work and resource ownership | Active operation or transfer | Interval or step mark |
| `flow` | Correlated transfer-stage DAG | Highlighted route or bundle | Transfer grouping |
| `effect` | Lifecycle change at stage completion | Creates, moves, updates, or removes objects | State delta |
| `checkpoint` | Authored reader stop | Global reconstructed state | Cursor, narrative, and focus |
| `annotation` | Editorial note on a semantic anchor | Pinned marker | Review content and status |

One semantic item may appear in several projections. Selection uses its stable
ID, so the System view, Timeline, narrative, and inspector stay connected.

## 3. The distinctions that matter most

### Entity versus materialization

An entity answers “what logical thing is this?” A materialization answers
“which physical copy is resident where?” A tensor in HBM and its shared-memory
copy are one entity and two materializations.

### Place versus resource

A place contains or executes things. A resource limits concurrent use. Shared
memory may be a place; `smem_bytes` is its storage capacity. A network link is
topology; `rdma_channels` is capacity owned by that link.

### Operation versus stage

An operation names work at the reader's level. A stage is the scheduled unit
with a place or link, time, dependencies, reads, effects, and resource claims.
One “dispatch token” operation can contain pack, network transfer, forwarding,
and receive stages.

### Link versus flow

A link says traffic *can* travel between two places. A flow correlates the
specific stage or stages that carried one logical transfer, including
multi-hop, fan-out, and fan-in paths.

### Copy versus move

Copy and move change identity differently:

```yaml
# Copy: source remains; a destination materialization is created with provenance.
effects:
  - action: create
    materialization: tile.smem
    entity: tile
    place: smem
    from: tile.hbm
```

```yaml
# Move: the same materialization leaves one place and enters another.
effects:
  - {action: unplace, materialization: request.0}
  - {action: place, materialization: request.0, place: running_queue}
```

Never use an arrow, function name, or transfer stage alone to guess this
choice. It affects provenance, quantities, capacity, and every later snapshot.

## 4. A minimal complete trace

This example copies one block from a source store to a destination store in one
authored step. It is deliberately small, but it contains every layer needed for
automatic visualization.

```yaml
version: "0.2-draft"
id: minimal-copy
title: Minimal copy
description: One block is copied while the source remains resident.

time:
  mode: steps

places:
  - {id: system, label: System, role: group, layout: hierarchy}
  - {id: source, label: Source store, parent: system, role: storage, layout: memory}
  - {id: destination, label: Destination store, parent: system, role: storage, layout: memory}

resources:
  - id: copy_slot
    label: Copy channel
    owner: source_to_destination
    kind: bandwidth
    capacity: {channels: 1}

links:
  - id: source_to_destination
    label: Copy path
    from: source
    to: destination
    directed: true
    resource: copy_slot

entities:
  - id: block
    label: Data block
    kind: data-block
    quantity: {bytes: 1024}

initial_materializations:
  - {id: block.source, entity: block, place: source}

operations:
  - {id: copy_block, label: Copy the block, kind: copy}

stages:
  - id: copy_block.transfer
    label: Transfer source to destination
    operation: copy_block
    kind: transfer
    link: source_to_destination
    flow: block_copy
    reads: [block.source]
    claims:
      - {resource: copy_slot, amount: {channels: 1}}
    effects:
      - action: create
        materialization: block.destination
        entity: block
        place: destination
        from: block.source
    step: 1

flows:
  - id: block_copy
    label: Block copy
    entity: block
    stages: [copy_block.transfer]

checkpoints:
  - id: copying
    label: Copying
    step: 1
    narrative: The source block remains while the copy channel is active.
    focus: [block.source, source_to_destination]
  - id: copied
    label: Copied
    step: 2
    narrative: The destination copy now exists and retains source provenance.
    focus: [block.source, block.destination]

views:
  - id: structure
    label: System
    kind: spatial
    roots: [source, destination]
    draggable: [source, destination]
    importance: [block, block_copy]
  - id: execution
    label: Timeline
    kind: timeline
    resources: [copy_slot]
```

What the compiler derives:

- at `copying`, `block.source` is resident and the transfer stage owns the copy
  channel;
- when the stage completes, its `create` effect introduces
  `block.destination` with provenance from `block.source`;
- at `copied`, both materializations exist;
- the System view shows two stores and a directed copy path;
- the Timeline view uses the `copy_slot` lane;
- the narrative and focus list direct the reader to the relevant evidence.

## 5. Define a real trace in dependency order

Author in the following order. Each section introduces IDs used by later
sections.

### 5.1 Header and time

Use a stable document `id`, a reader-facing `title`, and one explicit time
mode:

- `steps` for known ordering without credible duration;
- `timeline` for numeric `start` and `duration`, with one of `ns`, `us`, `ms`,
  or `s` as `unit`.

Stages sharing a step are parallel. Timeline overlap must be authored
numerically. The compiler does not invent missing time.

### 5.2 Places

Define semantic containment, not screen boxes. Valid roles are `group`,
`storage`, `buffer`, `executor`, `register`, and `queue`. Layout hints are
`hierarchy`, `memory`, `grid`, `queue`, `network`, and `horizontal`.

Use `horizontal` on a semantic group whose direct children must form an
ordered row. The list order of the child places is stable authoring intent;
coordinates and spacing remain compiler output.

Use `parent` only for real containment. Put only meaningful roots in a spatial
view's `roots`; the renderer can still show their descendants.

### 5.3 Resources and links

A resource has an `owner`, generic `kind`, and one or more capacity dimensions.
Claims must use the same dimensions. Keep units in dimension names such as
`bytes`, `channels`, or `slots`.

A link defines `from`, `to`, direction, and optionally its capacity resource.
Do not create one link per transfer event; repeated traffic reuses topology.

### 5.4 Entities and initial materializations

Give every logical value an entity and its intrinsic quantity. Use
materializations for concrete copies and residency. Initial materializations
must completely describe what exists before authored work changes state.

Prefer stable IDs that encode identity, not position, color, or checkpoint.
For example, `token.3.rank1` is useful; `orange_box_left` is not.

### 5.5 Operations, stages, and flows

For each reader-meaningful operation, split implementation work into stages
only where scheduling, location, resource ownership, or lifecycle differs.

Every stage provides:

- one generic `kind`: `compute`, `transfer`, `control`, `wait`, `sync`, or
  `state-change`;
- `at` for non-transfer work or `link` for transfers;
- `step`, or both `start` and `duration`, matching the document time mode;
- optional `after`, `reads`, `claims`, `effects`, and `flow`.

Resource claims last for the complete stage interval. Lifecycle effects happen
at completion. Use `after` for semantic dependency, not merely because two
stages happen to be written in order.

Lifecycle actions are:

| Action | Result |
| --- | --- |
| `create` | Introduce a materialization; `from` records copy provenance. |
| `place` | Make the same materialization resident at a place. |
| `unplace` | Remove its current residency without retiring identity. |
| `update` | Preserve identity while applying `replace`, `accumulate`, `assemble`, or `select`. |
| `retire` | End the materialization's lifetime. |
| `relate` | Add an explicit semantic relation to another item. |

### 5.6 Checkpoints, narratives, and annotations

Checkpoints are teaching moments, not animation frames. Add the initial state,
goal-critical transitions, important overlap or capacity moments, and the final
state. Each checkpoint should explain one new insight and focus semantic IDs
that are visible in at least one projection.

`narrative` supports Markdown. An annotation is an editorial pin with an
`anchor`, optional checkpoint, title, body, and `resolved` or `unresolved`
status. It is not execution state.

### 5.7 Authored views

Each entry in `views` has a stable `id`, reader-facing `label`, and `kind`.
The initial kinds are `spatial` and `timeline`:

- `roots`: top-level containers for a spatial view;
- `draggable`: places readers may reposition in that spatial view;
- `resources`: ordered lane IDs for a timeline view;
- `importance`: semantic IDs to emphasize;

The compiler preserves the authored view ID and label in `display.views`. The
renderer generates its tabs from that ordered collection. Existing repository
traces using the singular `view` recipe with `system_roots` and
`timeline_resources` remain supported through a legacy-input adapter, but new
documents should use `views`.

Do not encode coordinates or execution meaning here. Reader-adjusted positions,
sizes, edge routes, narrative edits, and annotation edits belong to the
separate viewer-state overlay.

## 6. Validate, inspect, and publish

Run the loop from the repository root:

```bash
sviz validate examples/<name>_vnext.yaml
sviz compile examples/<name>_vnext.yaml -o /tmp/<name>.json
sviz view examples/<name>_vnext.yaml
sviz export examples/<name>_vnext.yaml --format bundle --output dist/<name>
```

Review in this order:

1. **Validation:** resolve schema, reference, timing, lifecycle, dependency,
   flow, provenance, and capacity errors.
2. **Compiled JSON:** inspect initial/final materializations, checkpoint
   snapshots, active stages, flows, resource ledgers, spatial roots, and
   timeline lanes.
3. **Spatial views:** verify containment, residency, topology, flow routes,
   capacity, and selection.
4. **Timeline views:** verify order, overlap, wait/sync work, labels, and lane
   ownership.
5. **Narrative:** verify every step directs the reader to visible evidence.
6. **Responsive and interaction QA:** check narrow/wide containers, dragging,
   resizing, edge adjustment, keyboard control, and reset.

Fix a problem at the layer that owns it:

| Problem | Change |
| --- | --- |
| Wrong identity, time, lifecycle, dependency, or quantity | Trace IR |
| Repeated domain-neutral placement or routing failure | Compiler/display planner |
| Generic label fitting, hit target, accessibility, or responsive failure | Renderer |
| One reader's preferred placement, scale, narrative, or review note | Viewer state |

Never add workload-name, label, or tag branches to the renderer.

## 7. Completeness checklist

Before calling a trace complete:

- [ ] The reader question and fidelity boundary are written down.
- [ ] Every important claim has source/runtime evidence or a labeled assumption.
- [ ] Entity/materialization, place/resource, link/flow, and operation/stage
      distinctions are correct.
- [ ] Copy, move, update, and retirement semantics are explicit.
- [ ] Initial and final materializations are complete.
- [ ] Timing provenance is stated; parallel work is represented as parallel.
- [ ] Claims and resident quantities do not silently exceed capacity.
- [ ] Checkpoints form a concise step-by-step explanation.
- [ ] Validation passes and repeated compilation is deterministic.
- [ ] System and Timeline views agree at every goal-critical checkpoint.
- [ ] The renderer contains no scenario-specific branch.
- [ ] A reader guide, semantic tests, and portable export are included.

For a scored review with evidence requirements and pass conditions, use the
[nine-gate user manual](user-manual.md) and copy the
[workbook template](example-workbook-template.md).

## 8. Guidance for automated agents

An agent should first produce an evidence map, then a semantic draft, then a
validated trace. It should stop and ask when an ambiguity changes the learning
goal, identity, copy/move meaning, timing provenance, or scenario boundary.

The agent may infer syntactic references and deterministic compiler output. It
must not silently infer semantic meaning from names, invent measured timing,
or solve a one-scenario visual defect with workload-specific rendering code.
Its completion report should include validation results, test results, visual
observations, assumptions, and unresolved limitations.
