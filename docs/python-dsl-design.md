# Python authoring DSL design

**Status:** implemented experiment (`v0`)  
**Audience:** authors building small, testable demonstrations in Python  
**Backend:** generic authored views in the `0.2-draft` semantic IR and compiled
display contract

## 1. Goal

The Python DSL lets an author describe objects and relationships without
designing coordinates:

```text
Python objects and references
  → normalized semantic IR
  → existing validation
  → automatic per-view layout and timeline planning
  → existing interactive renderer
```

The first implementation supports seven ideas:

1. create a spatial view containing one or more planes;
2. place stable elements on those planes without coordinates;
3. copy an element's properties under a new stable identity;
4. group existing elements with an authored ordering and layout intent;
5. connect elements within a plane using ordinary semantic edges;
6. relate elements on different planes using a special equivalence edge; and
7. create timeline spans that explicitly correspond to elements or edges.

This is an authoring frontend, not a parallel visualization engine. YAML and
Python lower to the same validated model and compiled display format. Authored
view identity survives normalization and compilation; the renderer creates its
tabs from `display.views` rather than assuming System and Timeline.

## 2. First acceptance case

[`first_example.py`](../first_example.py) is the starting contract:

```python
demo = Demo(identifier="first-example", title="first example")
view = demo.view("view-1", label="view-1")
plane = view.plane("plane-1", label="plane-1")
shards = [plane.element(f"shard-{i}") for i in range(8)]
plane.group("group-1", shards)
```

It must compile as exactly one view:

```text
Demo
└── view-1 (spatial view)
    └── plane-1
        └── group-1 (horizontal)
            ├── shard-0
            ├── …
            └── shard-7
```

There is no implied System view and no empty Timeline view. The normalized
YAML has `views: [{id: view-1, kind: spatial, roots: [plane-1]}]`; the compiled
JSON has the corresponding entry in `display.views`. The compiler supplies the
group and shard geometry that the Python source deliberately omits.

## 3. Smallest useful vocabulary

| Python concept | Meaning | Initial lowering |
| --- | --- | --- |
| `Demo` | Identity and metadata for one explanation | `TraceDocument` |
| `View` | A named spatial projection | `DraftView(kind="spatial")` and one `display.views[]` entry |
| `Plane` | A semantic region that owns elements | Root place |
| `Element` | A stable object on one plane | Child place |
| element copy | A new identity inheriting another element's properties | New child place with copy provenance |
| `Group` | Ordered containment plus layout intent | Nested place with `layout=horizontal` |
| `Edge` | A directed or undirected relation within one plane | Link |
| equivalence `Edge` | A symmetric cross-plane identity relation | Link with `semantic_role=equivalence` |
| `Timeline` | A named temporal projection | `DraftView(kind="timeline")` and one `display.views[]` entry |
| `Lane` | A capacity-bearing timeline row | Execution resource |
| `Span` | An interval on a lane | Operation plus stage |
| span correspondence | Elements or edges explained by a span | Normalized mark references |

Plane and element placement is intentionally absent. Authors may choose a
coarse layout policy such as `grid` or `network`, but the compiler determines
boxes and routes. Reader adjustments remain viewer state.

### Copying an element

`Element.copy()` creates a distinct element while inheriting the source label,
kind, and author-defined attributes:

```python
element_1 = plane.element(
    "element-1",
    label="request",
    kind="request",
    attrs={"state": "ready", "slots": 1},
)
element_2 = element_1.copy("element-2")
element_3 = element_1.copy("element-3")
```

The new ID is mandatory because identity is never copied. Attributes are deep
copied, so later mutation of a nested value on one element cannot alter the
other. Optional `label`, `kind`, and `attrs` arguments override inherited
properties; attribute overrides merge over the copied mapping. Copying into a
different plane is explicit:

```python
projected = element_1.copy("element-projected", into=other_plane)
# Equivalent spelling when the destination plane is the natural subject:
# projected = other_plane.copy("element-projected", element_1)
```

A copy is not automatically an equivalence. It records authoring provenance as
`dsl_copied_from`, but the author must use `view.equivalence()` when two marks
represent the same semantic subject across planes. Group membership and edges
are also not properties of one element, so they are never copied. This avoids
silently changing the graph when an author only intended to reuse a definition.

### Horizontal grouping

[`second_example.py`](../second_example.py) adds one operation to the first
acceptance case:

```python
element_1 = plane.element("element-1", kind="request")
element_2 = element_1.copy("element-2")
element_3 = element_1.copy("element-3")

row = plane.group(
    "group-1",
    elements=[element_1, element_2, element_3],
    direction="horizontal",
)
```

The operation groups existing handles; it does not replace them. Member order
is authored by the list, while positions and spacing are compiler output. The
normalized IR represents `group-1` as a place inside the plane, reparents the
three element places under it, and sets `layout: horizontal`. Both responsive
geometry profiles must keep the members on one row in the same order.

The initial operation deliberately supports only direct, non-nested groups of
at least two elements. A member can belong to only one group. All members must
come from the same plane. These constraints keep containment unambiguous while
vertical, grid, wrapping, nested, and overlapping groups remain future design
choices.

## 4. Richer authoring example

```python
from sviz import Demo

demo = Demo("bucket-lanes", title="Bucket demand and lane frontier")

view = demo.view("schedule")
buckets = view.plane("buckets", label="Completion buckets")
lanes = view.plane("lanes", label="Lane state")

short = buckets.element("bucket.short", label="Short debt: 2", kind="bucket")
lane0 = lanes.element("lane.0", label="Lane 0 · S-21", kind="lane")
frontier = lanes.element("frontier.0", label="Frontier f1", kind="frontier")

reaches = view.edge(
    "edge.reaches-frontier",
    lane0,
    frontier,
    label="reaches chunk boundary",
)
mapping = view.equivalence(
    "equivalence.short-lane0",
    short,
    lane0,
    label="bucket ↔ current lane",
)

timeline = demo.timeline("round", unit="ms")
worker = timeline.lane("worker", owner=lane0, label="Lane 0 worker")
timeline.span(
    "span.boundary",
    lane=worker,
    start=0,
    duration=1,
    kind="compute",
    at=lane0,
    corresponds_to=[lane0, reaches, mapping],
    label="Reach frontier",
)

compiled = demo.compile()
demo.write("/tmp/bucket-lanes.yaml")
```

`compile()` returns the same renderer-ready dictionary as
`sviz compile`. `write()` emits ordinary semantic YAML, so every existing CLI
command remains usable:

```bash
python examples/python_dsl_minimal.py /tmp/python-dsl-demo.yaml
sviz validate /tmp/python-dsl-demo.yaml
sviz view /tmp/python-dsl-demo.yaml
```

The complete executable example is
[`python_dsl_minimal.py`](../examples/python_dsl_minimal.py).

## 5. References instead of repeated string IDs

Methods return typed handles. Later declarations consume those handles:

```python
lane0 = lanes.element("lane.0")
frontier = lanes.element("frontier.0")
edge = view.edge("edge.advance", lane0, frontier)

timeline.span(
    "span.advance",
    lane=worker,
    start=0,
    duration=1,
    corresponds_to=[lane0, edge],
)
```

This catches foreign-demo references, cross-view references, and the wrong
kind of object when the graph is constructed. Stable string IDs remain in the
normalized IR and compiled output for serialization, selection, annotations,
and test assertions.

IDs are global within a demo. Reusing an ID for an element, edge, lane, span,
or generated operation fails immediately.

## 6. Edge semantics

### Ordinary edge

`view.edge()` connects two elements on the same plane. It describes a semantic
relationship such as dependency, adjacency, or progression. It may be directed
or undirected.

The v0 API deliberately rejects an ordinary edge across planes. Otherwise the
author could accidentally use a visual line to imply correspondence without
declaring its stronger meaning.

### Equivalence edge

`view.equivalence()` connects two elements on different planes. It means that
the two marks are projections of the same semantic subject, not merely nearby
or similarly colored objects.

Equivalence affects the renderer:

- it is drawn as a dashed, symmetric relation;
- selecting either endpoint highlights the relation and its counterpart; and
- a corresponding timeline span joins the same selection closure.

Equivalence does **not** establish independent verification. If both elements
were authored from the same value, the relation only checks cross-projection
consistency. Future evidence and assertion concepts should remain distinct.

Binary equivalence is sufficient for the first small cases. One-to-many and
partial correspondence need explicit cardinality and coverage before they are
added.

## 7. Timeline correspondence

A lane names the owner of scheduled capacity. A span names:

- its lane, start, and positive duration;
- a generic kind such as `compute`, `control`, `wait`, `sync`, or
  `state-change`;
- the spatial plane or element where the event acts;
- optional predecessor spans; and
- at least one corresponding element or edge.

For example, a frontier event can correspond to a lane object, its
lane-to-frontier edge, and the lane's cross-plane bucket equivalence. Selecting
the span then highlights those spatial marks. Selecting an equivalent spatial
element highlights the corresponding span when the reader switches to the
authored timeline view.

The DSL generates reader checkpoints at unique span boundaries. This keeps
micro-examples runnable without a second checkpoint API. Authored scene names,
narratives, state updates, and checkpoint merging belong in a later layer.

## 8. Compiler contract

`Demo.to_trace()` is the normalization boundary. After this method returns,
the Python builder is no longer special:

```text
View                 → DraftView(kind="spatial", roots=[...])
Plane                → DraftPlace(parent=None)
Group                → DraftPlace(parent=plane.id, layout="horizontal")
Element              → DraftPlace(parent=group.id or plane.id)
Element.copy()        → new DraftPlace with inherited properties and copy provenance
ordinary edge        → DraftLink(semantic_role="edge")
equivalence          → DraftLink(semantic_role="equivalence")
Lane                 → DraftResource(capacity={"slots": N})
Timeline             → DraftView(kind="timeline", resources=[...])
Span                 → DraftOperation + DraftStage
corresponds_to       → DraftStage.attrs["corresponds_to"]
span boundaries      → DraftCheckpoint[]
```

The display compiler emits an ordered `display.views` collection. A spatial
entry contains its roots, places, routes, and generated geometry; a timeline
entry contains its resources, lanes, and marks. The renderer derives tabs from
the entry IDs, labels, and kinds. It does not contain fixed System/Timeline tab
definitions.

The compiler preserves visible child-place endpoints rather than collapsing
every link to its root plane. It also copies `semantic_role` onto routes and
`corresponds_to` onto timeline marks. Those are generic display-plan facts; the
renderer does not inspect labels, workload names, or Python classes.

Existing hand-authored YAML examples still use the earlier singular `view`
recipe with `system_roots` and `timeline_resources`. An explicit input adapter
normalizes that recipe into two authored view entries named `system` and
`timeline`. New Python output uses `views` directly and does not pass through
that adapter.

Structural-only Python demos are valid. They need no fake entity, resource,
operation, or event. This is why those existing IR collections now default to
empty while places and checkpoints remain required.

## 9. Validation boundary

The Python layer rejects cheap authoring mistakes early:

- malformed or duplicate IDs;
- more than one spatial view or timeline in v0;
- copies whose source belongs to another demo;
- groups with fewer than two members, repeated members, cross-plane members,
  or members already owned by another group;
- ordinary edges that cross planes;
- equivalence edges whose endpoints share a plane;
- references owned by another demo;
- non-positive lane capacity or span duration;
- negative span starts; and
- dependencies that finish after a dependent span starts.

The shared semantic validator still owns graph-level checks:

- reference integrity after serialization;
- place and dependency cycles;
- timing shape;
- overlapping claims beyond lane capacity; and
- deterministic compilation.

Keeping both layers matters: builder checks make interactive authoring pleasant,
while IR validation protects generated or modified YAML and future automated
producers.

## 10. Testing with small cases

A useful Python-authored test should inspect semantic output, not pixels:

```python
compiled = build_demo().compile()

views = {view["id"]: view for view in compiled["display"]["views"]}
routes = {route["id"]: route for route in views["schedule"]["routes"]}
marks = {mark["id"]: mark for mark in views["round"]["marks"]}

assert routes["equivalence.short-lane0"]["semantic_role"] == "equivalence"
assert routes["equivalence.short-lane0"]["from"] == "bucket.short"
assert routes["equivalence.short-lane0"]["to"] == "lane.0"
assert "equivalence.short-lane0" in marks["span.boundary"]["corresponds_to"]
```

The repository tests also cover deterministic output, generated checkpoints,
YAML round trips, spatial-only demos, ambiguous edge rejection, and reuse of
the existing capacity validator.

## 11. Deliberate v0 limits

The first implementation is intentionally narrow:

- one spatial view authored through `Demo.view()`;
- one optional timeline view authored through `Demo.timeline()`;
- direct, non-nested horizontal groups only;
- direct elements only—no nested element hierarchy;
- binary equivalence only;
- static spatial elements—no scene-local value or lifecycle updates;
- numeric authored time with one unit;
- no collections, templates, style API, or manual coordinates;
- no automatic extraction from source code or traces; and
- no independent evidence, assertion, or disagreement plane yet.

These limits keep the authoring vocabulary testable. They are not promises that
the normalized IR should remain limited to these shapes.

## 12. Scaling path

The next capabilities should be added in semantic order:

1. **Scene state.** Add stable element properties and typed updates at event or
   checkpoint boundaries.
2. **Correspondence cardinality.** Generalize binary equivalence into typed
   one-to-one, one-to-many, many-to-one, and partial mappings with coverage.
3. **Evidence and assertions.** Distinguish authored equivalence from derived
   consistency, executable checks, measured observations, and disagreement.
4. **Collections.** Add declarative populations and repeat rules so automated
   producers do not instantiate thousands of Python objects.
5. **Multiple view kinds.** Support topology, dataflow, state, residency,
   comparison, model, and code projections through one normalized plane API.
6. **Extraction adapters.** Translate source APIs, runtime traces, paper
   specifications, and generated scenarios into the same builder or normalized
   IR.
7. **Layout intent.** Add constraints such as grouping, order, alignment, and
   importance—not absolute coordinates.

Every extension should preserve three properties demonstrated by v0: stable
semantic identity, deterministic normalized output, and tests that can fail
before a renderer is opened.
