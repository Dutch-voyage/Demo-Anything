# `all_to_all_single(async_op=False)`

## Purpose

This isolated trace shows the synchronous API contract without treating it as a
device-wide blocking call.

View it with:

```bash
.venv/bin/sviz view examples/torch_all_to_all_sync_vnext.yaml
```

The microsecond durations are authored for explanation and are not benchmark
results.

## Schedule

```python
# Capture producer readiness before the collective installs its current-stream
# completion dependency.
shared_expert_stream.wait_stream(torch.cuda.current_stream())
dist.all_to_all_single(output, routed_tokens, async_op=False)
with torch.cuda.stream(shared_expert_stream):
    shared_expert_fc1(local_tokens)
consume(output)
```

ProcessGroupNCCL still submits the transfer to its NCCL CUDA stream. Before the
call returns, PyTorch establishes the dependency needed to make `output` safe
for subsequent work on the current CUDA stream. The CPU may continue before
the GPU transfer physically finishes.

Shared-expert FC1 is submitted to a dedicated CUDA stream whose producer
dependency was established before the collective call. It can therefore run
concurrently with NCCL even though the model/current stream is waiting.

## Resource interpretation

- **CUDA stream pool** groups all three stream executors, so the System view
  exposes the stream count and each operation's placement at a glance.
- **Host submission thread** shows that Python can return before device
  completion.
- **Current CUDA stream** carries the implicit completion dependency and then
  resumes routed-token work after NCCL.
- **ProcessGroupNCCL stream** is occupied only while NCCL communication is
  active.
- **Shared-expert CUDA stream** executes FC1 independently from both.
- **NCCL peer transport** exposes the concurrent data-movement interval.

This is why `async_op=False` does not forbid shared-expert overlap. Its
limitation is narrower: the caller cannot place additional model/current-stream
work before the completion join that PyTorch installed internally.
