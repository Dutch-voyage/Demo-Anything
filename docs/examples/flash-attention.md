# FlashAttention examples

## Purpose

The canonical example follows one FlashAttention-2 query tile through three
K/V tiles. It demonstrates durable versus temporary materializations,
double-buffer reuse, online-softmax state, resource overlap, output-copy
semantics, and cleanup.

Run it with:

```bash
.venv/bin/sviz view examples/flash_attention_vnext.yaml
```

The authored timings explain ordering and overlap; they are not benchmark
measurements.

## What the elements mean

- **HBM** holds durable Q, K, V, and the final output.
- **Shared memory** contains a Q slot and alternating KV buffers 0 and 1.
- **Tensor core**, **online softmax**, and **registers** are execution and local
  state places.
- A chip such as `k1.buf1` is a physical materialization of a logical tile.
- Copy stages create destination materializations without deleting HBM inputs.
- The resource lanes are copy engine, tensor core, softmax pipeline, global
  store, and lifecycle.

## Step-by-step walkthrough

| Step | Cursor | What happens | What to observe |
| ---: | ---: | --- | --- |
| 1 | 0.0 µs | Q and three K/V pairs are resident in HBM. | Nothing local exists yet; HBM is the durable source. |
| 2 | 0.6 µs | The Q copy has completed and K0 starts loading into KV buffer 0. | `q.smem` coexists with `q.hbm`, demonstrating copy rather than move. |
| 3 | 1.4 µs | K0 and V0 are ready; `Q × K0ᵀ` begins. | Buffer 0 is full and the tensor-core lane becomes active. |
| 4 | 2.0 µs | QK0 continues while V1 is prefetched into buffer 1. | Copy-engine and tensor-core claims overlap; shared-memory occupancy reaches its authored peak. |
| 5 | 2.4 µs | QK0 completes and online softmax 0 starts. | K0 is retired, score state `s0.reg` appears, and V1 is ready. |
| 6 | 2.8 µs | Softmax produces P0 and `P0 × V0` begins. | Running online-softmax state is updated; temporary score state is replaced by probability state. |
| 7 | 3.7 µs | The first PV finishes and `Q × K1ᵀ` begins. | `output.acc` is created; P0 and V0 retire, freeing buffer 0 for K2/V2. |
| 8 | 4.7 µs | QK1 finishes and online softmax 1 begins. | K2/V2 are already in reused buffer 0 while K1 retires. |
| 9 | 5.1 µs | P1 is formed and `P1 × V1` begins. | The existing output accumulator will be updated rather than replaced. |
| 10 | 6.0 µs | The second PV completes and `Q × K2ᵀ` begins. | `output.acc` records an update; buffer 1 becomes free. |
| 11 | 7.0 µs | The last QK finishes and online softmax 2 begins. | K2 retires and the final score materialization appears. |
| 12 | 7.4 µs | P2 is formed and the last PV begins. | Online-softmax state has incorporated all three tiles. |
| 13 | 8.3 µs | The last PV completes and final normalization starts. | P2 and V2 retire; only the accumulator and running normalization state remain locally. |
| 14 | 8.8 µs | Normalization finishes and the global-store copy starts. | The normalized accumulator remains in registers while it is being copied. |
| 15 | 9.4 µs | `output.hbm` has been created and local cleanup runs. | Source and destination coexist, making output copy semantics explicit. |
| 16 | 9.6 µs | Block-local Q, online state, and accumulator retire. | HBM retains all original inputs plus the new normalized output. |

For the source-to-IR and compiler mapping, see
[`../flash-attention-workflow.md`](../flash-attention-workflow.md).
