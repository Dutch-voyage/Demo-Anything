# `all_to_all_single(async_op=True)` with shared-expert overlap

## Purpose

This isolated trace shows a useful asynchronous schedule: routed-token
all-to-all communication overlaps independent shared-expert FC1 computation.

View it with:

```bash
.venv/bin/sviz view examples/torch_all_to_all_async_shared_expert_vnext.yaml
```

The microsecond durations are authored for explanation and are not benchmark
results.

## Schedule

```python
work = dist.all_to_all_single(
    routed_output,
    routed_tokens,
    async_op=True,
)
with torch.cuda.stream(shared_expert_stream):
    shared_expert_fc1(local_tokens)
independent_model_work()  # current stream; does not consume routed_output
work.wait()
consume(routed_output)
```

The collective returns a `Work` handle after submission. NCCL occupies the
ProcessGroupNCCL stream while shared-expert FC1 occupies a dedicated CUDA
stream. Because completion has not yet been joined, the model/current stream
also remains available for independent work. `work.wait()` is placed after
that work in current-stream order.

For CUDA collectives, `work.wait()` normally establishes stream ordering; it
is not an unconditional host-side `cudaDeviceSynchronize()`.

## Resource interpretation

- **CUDA stream pool** groups all three stream executors, so the System view
  exposes the stream count and operation placement at a glance.
- **Host submission thread** creates and later waits on the `Work` handle.
- **Model/current CUDA stream** executes independent work, then carries the
  explicit wait before consuming routed tokens.
- **ProcessGroupNCCL stream** clearly shows when the collective owns NCCL
  execution resources.
- **Shared-expert CUDA stream** executes FC1 independently from both.
- **NCCL peer transport** shows the data-movement interval independently from
  stream occupancy.

Shared-expert/NCCL overlap can also exist with `async_op=False` because those
operations use separate streams. The additional benefit of `async_op=True` is
control over where the model/current stream joins communication completion.
Useful overlap still requires independent work and enough hardware resources
for communication and computation to make progress together.
