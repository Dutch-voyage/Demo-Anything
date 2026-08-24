# DeepEP example

## Purpose

The example shows the classical high-throughput dispatch/expert/combine cycle
across four expert-parallel ranks on two nodes. Four source tokens use top-2
routing, so dispatch must create eight expert-input materializations and combine
must return two contributions per token.

Run it with:

```bash
.venv/bin/sviz view examples/deepep_vnext.yaml
```

The microsecond schedule and rail topology are explanatory, not measured
DeepEP performance.

## What the elements mean

- Each rank owns one resident expert: E0 through E3.
- T0/T1 originate on rank 0; T2/T3 originate on rank 2.
- NVLink connects ranks within a node; one RDMA rail connects the two nodes.
- Local routes create copies without a link. Remote routes use one or two
  transfer stages.
- Route maps and dispatch handles are coordination materializations, not token
  payloads.
- Bandwidth, layout, expert-compute, and combine lanes expose concurrency and
  capacity claims.

## Step-by-step walkthrough

| Step | Cursor | What happens | What to observe |
| ---: | ---: | --- | --- |
| 1 | 0.0 µs | Tokens and experts are resident while four layout stages run. | Origins are preserved and each rank prepares receive counts/routing metadata. |
| 2 | 0.4 µs | Dispatch begins: two local copies, two NVLink routes, and four RDMA legs run together. | The RDMA edge shows four distinct moving transfers and a four-channel resource claim. |
| 3 | 1.2 µs | Direct routes have arrived; T1 and T3 continue from rail ranks over NVLink. | Rail materializations make the two-leg flows explicit rather than pretending they are one hop. |
| 4 | 1.7 µs | Every rank has two expert-input copies and resolves its receive-ready state. | Rail copies retire; final expert copies and routing metadata remain. |
| 5 | 1.9 µs | E0–E3 run grouped expert GEMMs in parallel. | Four expert slots are claimed and all dispatch handles stay live for combine. |
| 6 | 3.0 µs | Expert inputs become output contributions and reverse transfers begin. | Local contributions stay put; NVLink, direct RDMA, and first forwarding legs run concurrently. |
| 7 | 3.5 µs | Forwarded O1/O3 contributions cross RDMA while direct RDMA returns continue. | The shared RDMA route again carries four active transfers. |
| 8 | 4.3 µs | Source ranks restore token order and accumulate two expert contributions per token. | Combine stages run on ranks 0 and 2 while ranks 1 and 3 release routing state. |
| 9 | 4.9 µs | The round trip is complete. | Only four resident experts and final O0–O3 outputs remain. |

The mechanism itself is introduced in [`../deepep-mechanism.md`](../deepep-mechanism.md),
and the detailed source-to-display mapping is in
[`../deepep-workflow.md`](../deepep-workflow.md).
