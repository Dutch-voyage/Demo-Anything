# DeepEP visualization workflow

This is the second end-to-end test of the semantic IR. Read
[`deepep-mechanism.md`](deepep-mechanism.md) first for the mechanism and scope.
The authored schedule is explanatory rather than measured.

## Run it

```bash
.venv/bin/sviz validate examples/deepep_vnext.yaml
.venv/bin/sviz compile examples/deepep_vnext.yaml -o /tmp/deepep.json
.venv/bin/sviz view examples/deepep_vnext.yaml
.venv/bin/sviz export examples/deepep_vnext.yaml --format bundle -o dist/deepep
```

The viewer opens in the System projection. **Previous** and **Next** traverse
nine authored checkpoints; the Timeline projection shows the same cursor and
selection. Rank shapes can be dragged or resized without modifying the trace.
The default layout reserves separate lanes for the NVLink and RDMA routes. If a
host layout or manual place movement creates a new collision, enable **Adjust
edges** and drag a route handle; arrow keys provide precise adjustment.

## Source facts to IR

| Source-level fact | Authored IR definition |
| --- | --- |
| Expert-parallel ranks and resident experts | Places and initial materializations |
| Gate-selected top-2 routes | Token entity attributes plus dispatch stages |
| Layout/count calculation | Control stages claiming the coordination resource |
| Local route | State-change that creates an expert-input materialization |
| NVLink or RDMA leg | Transfer stage on a structural link with a bandwidth claim |
| Forwarded route | One flow containing two ordered transfer stages |
| Received grouping and dispatch handle | Sync stage that creates coordination materialization |
| Grouped expert GEMM | Compute stage reading received copies and creating contributions |
| Reverse exchange | Transfer stages that reuse the dispatch flow in reverse |
| Restore order and sum top-k results | Compute stage that creates final outputs and retires route state |

The original token is not moved during dispatch. Each selected expert gets a
new materialization with explicit provenance. This lets the same representation
handle top-1, top-k, duplication, multicast, or retry without changing the
renderer.

## IR to compiled display

Compilation derives three kinds of output:

- execution snapshots apply lifecycle effects at each checkpoint, list active
  stages, and calculate resource ledgers;
- the System plan contains stable rank geometry and the three structural links;
- the Timeline plan places every stage on a coordination, NVLink, RDMA, expert,
  or combine lane using authored microsecond coordinates.

The renderer makes only generic decisions. Resident materializations become
object chips inside their current place. Local stages become active bars.
Transfer stages become moving, selectable marks on their compiled link. When
several stages share a link, their marks are phase-separated and the link gets
one aggregate count label. Timeline labels fit, abbreviate, or move out of very
short marks according to available width.

## Checkpoint story

1. Inputs and experts are resident.
2. Layout completes and dispatch fans out local, NVLink, and RDMA copies.
3. Rail arrivals forward to their final ranks.
4. Receive counts and handles become ready.
5. Four experts compute in parallel.
6. Combine begins the reverse routes.
7. Forwarded results finish their RDMA leg.
8. Source ranks restore order and accumulate two contributions per token.
9. Temporary copies and handles are retired; only experts and final outputs remain.

## What this example proves

DeepEP adds the structural cases that FlashAttention did not: four peer places,
top-k fan-out, fan-in, concurrent transfers sharing a route, multi-leg flows,
and coordination state that is important but not itself a spatial transport.
All are expressed with the same semantic and display concepts; no workload name
or domain tag appears in renderer logic.
