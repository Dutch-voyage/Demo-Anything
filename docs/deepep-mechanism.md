# DeepEP working mechanism

## Scope

This note uses **classical DeepEP** to mean the archived V1 normal-kernel path
for training and inference prefill. That path uses high-throughput expert-
parallel dispatch and combine kernels across NVLink and RDMA. The current V2
implementation keeps the same dispatch/expert/combine contract but replaces
the original NVSHMEM-oriented interface with a unified `ElasticBuffer` and the
NCCL Gin backend.

The first visualization models the mechanism, not a benchmark result or an
instruction-accurate kernel trace.

## The problem DeepEP solves

An MoE gate selects several experts for each input token. Experts are sharded
across expert-parallel ranks, so the selected token copies must reach the ranks
that own those experts and their results must return to the token's original
rank and order.

DeepEP supplies the two communication halves:

```text
origin tokens + top-k routing
  -> dispatch layout
  -> dispatch / permutation / all-to-all
  -> tokens grouped by local expert
  -> expert computation
  -> combine / reverse all-to-all / reduction
  -> outputs in original token order
```

This is not a move of the original token. A top-k route creates several logical
copies for expert computation. Combine later gathers the corresponding expert
outputs and reduces them into one result per original token.

## Normal-kernel process

### 1. Gate and layout

The model supplies hidden states, `topk_idx`, and `topk_weights`. Before the V1
normal dispatch, `get_dispatch_layout` derives the token counts per destination
rank, per RDMA rank, and per expert, plus rank-membership information. The
layout lets the communication kernel size receive regions and lets the expert
GEMM know how many tokens belong to each local expert.

### 2. Dispatch

`Buffer.dispatch` sends each selected token representation, routing index, and
weight to the expert owner. It returns received tensors grouped for local
experts, per-expert receive counts, an opaque routing handle, and an overlap
event.

Within one node the transport uses NVLink. Across nodes, the normal kernels
compose the scale-up NVLink domain with the scale-out RDMA domain and are
optimized for asymmetric-domain forwarding. A concrete deployment may use a
rail GPU as an intermediate forwarding point; that routing detail is a
transport policy, not a change to the token's semantic destination.

The original token remains at its source. Each selected expert receives a
materialized route copy.

### 3. Expert computation

After the dispatch event is ready, each rank runs its local grouped expert
GEMMs using the received token grouping and counts. This computation is outside
DeepEP itself; DeepEP produces and consumes the layouts used by the expert
kernels.

### 4. Combine

`Buffer.combine` consumes expert outputs and the dispatch handle. The handle
encodes enough routing information to reverse the communication, return expert
contributions to their source ranks, restore original token order, and combine
the top-k contributions. In the forward pass this is the MoE output; in the
backward pass, dispatch and combine exchange roles.

### 5. Overlap

Normal dispatch and combine can return asynchronous completion events and
accept a preceding event. The application may overlap independent compute with
communication, but it must wait before consuming received tensors. V1 normal
dispatch can involve a host wait when the number of received tokens was not
known in advance.

## Normal versus low-latency mode

| Concern | V1 normal kernels | V1 low-latency kernels |
| --- | --- | --- |
| Intended workload | Training and prefill | Small-batch decoding |
| Transport emphasis | NVLink plus RDMA forwarding | Pure-RDMA latency path |
| Main objective | Throughput and controllable SM use | End-to-end latency |
| Receive behavior | Layout/count-driven dispatch | Hook can defer receive completion |
| First demo | Included | Deferred |

V2 unifies high-throughput and low-latency calls behind `ElasticBuffer`, but
that API refactor does not change the basic semantic cycle described above.

## First visualization boundary

The demo uses four expert-parallel ranks across two nodes, one expert per rank,
four source tokens, and top-2 routing. It deliberately includes:

- a local expert route;
- an intra-node NVLink route;
- a cross-node RDMA route;
- a two-leg RDMA-plus-NVLink forwarded route;
- parallel expert computation;
- the reverse combine routes and final top-2 accumulation;
- the dispatch handle and per-rank receive-ready state.

Authored microsecond values are explanatory, not measured DeepEP timings. The
two-hop rail route is a representative topology chosen to expose the transport
boundary; it is not a claim that every DeepEP deployment uses the same physical
hop sequence.

## Sources

- [DeepEP V1 archived documentation](https://github.com/deepseek-ai/DeepEP/blob/main/docs/legacy.md)
- [Current DeepEP V2 README](https://github.com/deepseek-ai/DeepEP/blob/main/README.md)
- [DeepSeek-V3 technical report](https://arxiv.org/abs/2412.19437)
