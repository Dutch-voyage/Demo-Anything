# `torch.distributed.all_to_all_single` example

## Purpose

This example explains how a variable-split, two-rank
`all_to_all_single` moves from GPU routing counts to consumable output. It
includes the control path hidden by equal splits:

- exchange send counts while they are device-resident;
- copy send/receive split vectors to host;
- synchronize before Python consumes those vectors;
- hand data from the current CUDA stream to ProcessGroupNCCL;
- let NCCL manage grouped peer operations;
- delay `Work.wait()` so independent CUDA work can overlap.

The ordered steps are explanatory, not measured NCCL timing.

View the trace with:

```bash
.venv/bin/sviz view examples/torch_all_to_all_single_vnext.yaml
```

On a machine with two CUDA GPUs and PyTorch installed, run the matching code:

```bash
torchrun --standalone --nproc-per-node=2 \
  examples/torch_all_to_all_single.py
```

## Concrete data layout

Routing produces uneven destination-major chunks:

```text
rank 0 input: [0 | 1, 2, 3]      send splits: [1, 3]
rank 1 input: [10, 11 | 12, 13]  send splits: [2, 2]
```

After exchanging one count per peer:

```text
rank 0 receive splits: [1, 2]
rank 1 receive splits: [3, 2]
```

The payload collective produces source-major outputs:

```text
rank 0 output: [0 | 10, 11]
rank 1 output: [1, 2, 3 | 12, 13]
```

## Count exchange and D2H synchronization

The runnable example first uses a small device-side count exchange:

```python
dist.all_to_all_single(recv_counts_gpu, send_counts_gpu)
```

The payload API requires Python split sequences, so the device vectors must
become host values:

```python
input_split_sizes = send_counts_gpu.cpu().tolist()
output_split_sizes = recv_counts_gpu.cpu().tolist()
```

The copies may start asynchronously, but `.tolist()` cannot finish until the
D2H data is ready. That makes this a host-visible synchronization point. It is
an application/PyTorch API consequence, not a requirement of the physical
payload transfer itself.

## Async stream management

The payload call requests asynchronous ProcessGroupNCCL work:

```python
work = dist.all_to_all_single(
    output_tensor,
    input_tensor,
    output_split_sizes=output_split_sizes,
    input_split_sizes=input_split_sizes,
    async_op=True,
)

# Enqueued before the communication dependency is joined.
independent.square_()
work.wait()
```

Conceptually, ProcessGroupNCCL:

1. orders its communication stream after input-producing work on the current
   CUDA stream, normally using CUDA events;
2. enqueues NCCL communication and returns a `Work` handle;
3. lets the caller enqueue independent work before waiting;
4. joins NCCL completion to the consumer stream when `work.wait()` is used.

The exact use of current versus private streams is PyTorch-version dependent.
`async_op=True` creates an overlap opportunity; it does not guarantee useful
overlap if `wait()` is called immediately or if communication and compute
contend for the same hardware resources.

## NCCL owns the grouped transfers

For variable splits, ProcessGroupNCCL calculates per-peer addresses and counts,
then issues the equivalent of:

```cpp
ncclGroupStart();
for (int peer = 0; peer < world_size; ++peer) {
    ncclSend(send_ptr[peer], send_count[peer], ..., peer, comm, stream);
    ncclRecv(recv_ptr[peer], recv_count[peer], ..., peer, comm, stream);
}
ncclGroupEnd();
```

PyTorch constructs the group, but NCCL manages matching, channels, transport
protocols, kernel launch, and progress. The trace therefore shows one grouped
NCCL stage per rank rather than claiming a particular channel-by-channel
schedule.

This differs from the equal-split path on PyTorch builds using NCCL 2.28 or
newer, which may call native `ncclAlltoAll` and may select a CE implementation
when its symmetric-window and topology requirements are satisfied.

## Checkpoint walkthrough

1. GPU routing counts and destination-major inputs are resident.
2. NCCL exchanges one count per peer.
3. Send/receive vectors move to pinned host memory.
4. Host synchronization creates the split-list API arguments.
5. ProcessGroupNCCL establishes producer-to-communication stream ordering.
6. NCCL grouped peer operations progress while independent work is enqueued.
7. `Work.wait()` joins communication completion to each consumer stream.
8. Variable-size outputs are visible in source-rank order.

## Fidelity boundary

The trace models observable data semantics and documented control boundaries.
It does not claim measured timing, a fixed number of NCCL channels, or one
specific NCCL protocol. ProcessGroupNCCL and the installed NCCL version choose
those details at runtime.
