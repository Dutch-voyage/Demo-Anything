# sviz

`sviz` is a domain-neutral semantic IR, compiler, and portable Web Component
for authored systems visualizations. The repository now contains only the
vNext pipeline.

The IR describes places, resources, links, logical entities, physical
materializations, operations, flows, stages, lifecycle effects, and authored
checkpoints. A deterministic compiler derives an ordered collection of authored
views; the renderer creates its tabs from that collection and contains no
workload-specific branches. Existing YAML traces using the earlier
`system_roots`/`timeline_resources` recipe are adapted at the compiler boundary.

## Quick start

```bash
python3.12 -m venv .venv
.venv/bin/pip install -e '.[dev]'

.venv/bin/sviz validate examples/flash_attention_vnext.yaml examples/deepep_vnext.yaml
.venv/bin/sviz compile examples/flash_attention_vnext.yaml -o /tmp/flash-attention.json
.venv/bin/sviz view examples/flash_attention_vnext.yaml
.venv/bin/sviz export examples/flash_attention_vnext.yaml --format bundle -o dist/flash
```

The viewer is checkpoint-first: **Previous** and **Next** advance through
authored teaching moments. It does not autoplay. Places can be dragged and
resized, object shapes can be rescaled, and edge routes can be adjusted when a
compiled default needs help. Each checkpoint also has an editable Markdown
narrative. Readers can attach pinned annotations to selected visual elements
and switch each pin between unresolved and resolved without hiding it. Opening
an annotation also exposes its title, body, and delete action. **Check layout**
audits every checkpoint in every authored spatial and timeline view at the
default scale using the browser's rendered bounds; see the
[`layout-checking guide`](docs/layout-checking.md).

## Examples

- [`first_example.py`](first_example.py) authors one generic view containing a
  compiler-positioned horizontal group of shards.
- [`second_example.py`](second_example.py) copies one element into two new
  identities, then groups all three into a compiler-arranged horizontal row.
- [`flash_attention_vnext.yaml`](examples/flash_attention_vnext.yaml) models a
  complete FlashAttention-2 tile with copies, overlapping work, shared-memory
  occupancy, online-softmax state, and cleanup.
- [`deepep_vnext.yaml`](examples/deepep_vnext.yaml) models top-2 dispatch,
  forwarding, parallel expert work, reverse transfers, and combine across four
  ranks.
- [`mla_prefill_vnext.yaml`](examples/mla_prefill_vnext.yaml) builds and
  consumes a four-token compressed MLA prompt cache.
- [`mla_decode_vnext.yaml`](examples/mla_decode_vnext.yaml) appends one token
  and attends directly over the growing compressed cache.

The guides are indexed in [`docs/examples`](docs/examples/README.md). The FA2
and DeepEP source-to-display workflows are documented in
[`docs/flash-attention-workflow.md`](docs/flash-attention-workflow.md) and
[`docs/deepep-workflow.md`](docs/deepep-workflow.md).

## Documentation

Start with the [`documentation map`](docs/README.md). To create another
example:

1. Learn the concepts and YAML fields in the
   [`IR authoring guide`](docs/ir-authoring-guide.md).
2. Follow the checkable stage-gate process in the
   [`code-to-demo user manual`](docs/user-manual.md).
3. Copy the [`example workbook template`](docs/example-workbook-template.md)
   to record evidence, assumptions, checks, and review scores.

The short pipeline is: define the learning goal, collect evidence, model
structure and execution, author checkpoints, validate, inspect compiled state,
review each authored view, test, and export. Semantic facts belong in the IR;
reusable display planning belongs in the compiler; reader-specific placement
and content edits belong in viewer state.

For small Python-authored experiments, begin with
[`first_example.py`](first_example.py): one real view, one plane, and one
compiler-arranged shard group. The [`Python DSL design`](docs/python-dsl-design.md)
then introduces semantic edges, cross-plane equivalence, and corresponding
timeline spans; [`python_dsl_minimal.py`](examples/python_dsl_minimal.py) is the
richer executable example.

## Commands

- `sviz validate TRACE...` validates references, timing, lifecycle,
  provenance, dependencies, and resource capacity.
- `sviz schema` prints the vNext JSON Schema.
- `sviz state-schema` prints the persisted viewer-state JSON Schema.
- `sviz compile TRACE` emits deterministic display JSON.
- `sviz view TRACE` serves the local viewer.
- `sviz view TRACE --no-persist` serves it without Save/Reload controls.
- `sviz export TRACE` creates JSON, inline, standalone, iframe, or bundle
  artifacts.

## Embedding

The framework-neutral `<systems-viz-next>` element consumes the compiled JSON
from `src` or an inline `application/vnd.sviz+json` script. `sviz export`
packages the component with the data, so the result works without the Python
server or a Node build.

```html
<systems-viz-next src="flash-attention.json" theme="auto"></systems-viz-next>
```

The local viewer enables explicit persistence by default and stores state under
`.sviz/` beside the trace. Portable embeddings without `state-src` keep edits
local to the component instance. A host can persist them with
`exportViewerState()` and `importViewerState()`, or provide `state-src` and call
`saveViewerState()`. See the [persistence guide](docs/persistence.md).

## Python API

```python
from sviz import compile_trace, load_trace, validate_trace

trace = load_trace("examples/flash_attention_vnext.yaml")
report = validate_trace(trace)
report.raise_for_errors()
compiled = compile_trace(trace)
```

Or construct a small demo directly:

```python
from sviz import Demo

demo = Demo("hello")
view = demo.view("main")
plane = view.plane("objects")
plane.element("hello.object", label="Hello")
compiled = demo.compile()
```

The checked-in [`schema/sviz-0.2-draft.schema.json`](schema/sviz-0.2-draft.schema.json)
and [`schema/sviz-viewer-state-0.1.schema.json`](schema/sviz-viewer-state-0.1.schema.json)
are generated from the same Pydantic models used by the loader and persistence
adapter. The IR contract and accepted architecture decisions are recorded in
[`docs/ir-design.md`](docs/ir-design.md) and
[`docs/decision-log.md`](docs/decision-log.md).
