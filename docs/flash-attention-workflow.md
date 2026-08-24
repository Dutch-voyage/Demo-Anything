# FlashAttention vertical slice

This example is the first complete implementation of the semantic IR workflow. It
models one FlashAttention-2 query tile streamed across three K/V tiles.

## Run it

```bash
.venv/bin/sviz validate examples/flash_attention_vnext.yaml
.venv/bin/sviz compile examples/flash_attention_vnext.yaml \
  --output /tmp/flash-attention.json
.venv/bin/sviz view examples/flash_attention_vnext.yaml
.venv/bin/sviz export examples/flash_attention_vnext.yaml \
  --format bundle --output dist/flash-attention
```

The viewer defaults to authored checkpoint stepping. Its IR, selected compiled
checkpoint, System projection, and Timeline projection are inspectable in the
same component.

## Workflow represented by the files

| Workflow stage | Implementation |
| --- | --- |
| Semantic definition and execution facts | `examples/flash_attention_vnext.yaml` |
| Structural model | `src/sviz/next_models.py` |
| YAML/JSON ingestion | `src/sviz/next_loader.py` |
| Semantic validation | `src/sviz/next_validation.py` |
| Execution and display compilation | `src/sviz/next_compiler.py` |
| Portable renderer | `src/sviz/static/systems-viz-next.js` |
| Local development shell | `src/sviz/next_server.py` |
| Public commands | `sviz validate/schema/compile/view` |
| Portable export | `sviz export` |

## Source process to semantic IR

The example represents this authored code-level process:

1. Copy Q, K0, and V0 from HBM into shared-memory slots.
2. Compute QK0 while prefetching K1/V1 into the alternate buffer.
3. Update the online-softmax maximum and normalization sum.
4. Compute P0V0 and create the output accumulator.
5. Repeat with K1/V1 while refilling the released buffer with K2/V2.
6. Accumulate the remaining PV products.
7. Normalize the accumulator, copy the result to HBM, and release local state.

The mapping is generic:

- Q, K, V, scores, probabilities, online state, and output are logical entities;
- HBM, shared-memory slots, execution units, and registers are places;
- HBM values and local copies are separate materializations;
- loads and stores are transfer stages grouped into flows;
- QK, softmax, PV, and normalization are compute stages grouped into operations;
- shared-memory bytes and execution pipelines are resources;
- create, update, and retire effects define lifecycle precisely.

## Compilation

The compiler produces:

- 20 exact event boundaries;
- 16 reader-facing checkpoints;
- materialization residency and provenance at every checkpoint;
- active stages and flows;
- a derived resource ledger, including shared-memory occupancy;
- state changes since the previous checkpoint;
- stable wide and narrow place geometry;
- route definitions and draggable place IDs;
- five resource-oriented timeline lanes and 19 scheduled marks.

No FlashAttention term is interpreted by the renderer. Labels remain data.

## Visual behavior

The System projection shows current residency, active computation, transfer
motion, copy lineage, and derived shared-memory occupancy. HBM, shared memory,
and SM execution have draggable headers. Pointer or keyboard movement changes
manual display offsets; nested places move with their parent and routes
reconnect. Corner handles resize each top-level place, while the **Shape size**
control scales object chips, labels, and moving transfer marks between 70% and
140%. **Reset layout** restores compiled placement and sizing.

Links are routed from compiler-defined endpoints using the current geometry.
The renderer uses a direct route only when it has enough clear space for its
label. Otherwise it selects an exterior routing channel around intermediate
places. Endpoint gaps, contrasting halos, and an edge layer above place fills
keep routes and arrowheads visible after responsive reflow, dragging, or
resizing. These rules inspect geometry only; they do not inspect domain labels.

The Timeline projection uses compiler-assigned resource lanes. Checkpoint and
selection state are shared with the System projection. There is no automatic
playback. Each event is an isolated, selectable capsule. Its inline label is
fitted from the capsule's rendered width: the renderer chooses a 10, 9, or
8-pixel font, preserves the semantic label when it fits, truncates it when a
useful fragment fits, and hides inline text for very short events. Every label
is clipped to its capsule, so it cannot cover a neighboring event. The full
name and authored interval remain available through the accessible tooltip,
selection, and checkpoint footer.

The IR and Compiled views expose why every visible mark exists. Manual offsets,
place scales, global shape scale, selection, and cursor are view state and never
modify semantic execution. A `layout-change` event reports all three layout
values so a host can save them explicitly.

## Fidelity boundary

This is an authored explanatory schedule, not an instruction-level CUDA trace.
It preserves the important algorithmic facts—copy retention, tiled QK/softmax/PV
ordering, double-buffer reuse, overlap, accumulation, normalization, and
cleanup—while omitting individual instructions, fences, and warp-level timing.

New examples should reuse this compiler and renderer while the format remains
explicitly versioned as `0.2-draft`.
