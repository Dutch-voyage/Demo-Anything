# Visualization example guides

Each guide explains the scenario, its semantic-IR mapping, the System and
Timeline projections, and every authored reader checkpoint.

| Case | Trace | Timing | Guide |
| --- | --- | --- | --- |
| FlashAttention-2 | [`flash_attention_vnext.yaml`](../../examples/flash_attention_vnext.yaml) | 16 checkpoints in microseconds | [`flash-attention.md`](flash-attention.md) |
| DeepEP | [`deepep_vnext.yaml`](../../examples/deepep_vnext.yaml) | 9 checkpoints in microseconds | [`deep-ep.md`](deep-ep.md) |
| MLA prefill | [`mla_prefill_vnext.yaml`](../../examples/mla_prefill_vnext.yaml) | 8 authored steps | [`mla-prefill.md`](mla-prefill.md) |
| MLA decode | [`mla_decode_vnext.yaml`](../../examples/mla_decode_vnext.yaml) | 8 authored steps | [`mla-decode.md`](mla-decode.md) |

All examples make copies, provenance, resources, and lifecycle changes
explicit. The reader moves through named checkpoints; a stage may stay active
across multiple checkpoints.
