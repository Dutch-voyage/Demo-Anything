# Multi-head Latent Attention mechanism

## Scope

These examples explain one **absorbed inference** formulation of DeepSeek's
Multi-head Latent Attention (MLA). The goal is to make two phase-specific facts
clear:

- **Prefill** processes a prompt batch and leaves a compact cache for later
  generation.
- **Decode** appends one compact cache row and reads the growing prefix without
  reconstructing a persistent full per-head K/V cache.

The examples cover one attention layer and use four prompt tokens followed by
one decode token. They use authored steps rather than measured timing.

## Primary evidence

The [DeepSeek-V2 technical report](https://arxiv.org/abs/2405.04434) introduces
joint low-rank KV compression. It defines a per-token latent vector `cKV` and
explains that the key up-projection can be absorbed into the query path while
the value up-projection can be applied after attention reduction.

The optimized branch of the official
[`DeepSeek-V3/inference/model.py`](https://github.com/deepseek-ai/DeepSeek-V3/blob/main/inference/model.py)
provides the concrete source process used here:

1. Project `q`, split it into content `qC` and positional `qR`, and apply RoPE
   to `qR`.
2. Project the input to compressed `cKV` and a separate positional key `kR`.
3. Normalize and store `cKV` in `kv_cache`; store rotated `kR` in `pe_cache`.
4. Transform `qC` with the key up-projection weights.
5. Add the content score `qC_absorbed · cKV` and the positional score
   `qR · kR`.
6. Apply the mask and softmax.
7. Reduce attention weights directly over `cKV`.
8. Apply the value up-projection and output projection to the reduced latent
   context.

The current official [FlashMLA repository](https://github.com/deepseek-ai/FlashMLA)
contains distinct prefill and decode kernels and supports different physical
MLA modes depending on hardware and kernel. Consequently, these demos explain
the semantic absorbed dataflow; they are not a claim that every production
prefill kernel executes this exact physical schedule.

## The two cache components

The compressed cache has two semantically different parts:

| Cache part | Purpose | Illustrated BF16 size per token |
| --- | --- | ---: |
| `cKV` | Shared compressed content used by both the key and value paths | 512 elements = 1,024 bytes |
| `kR` | Decoupled positional key used by the RoPE score path | 64 elements = 128 bytes |
| Total | Persistent state per layer and token | 576 elements = 1,152 bytes |

For four prompt tokens, the example therefore stores 4,608 bytes. After one
decode append, it stores 5,760 bytes. These byte counts are explanatory BF16
quantities derived from the dimensions used in the reference implementation;
they exclude allocation metadata, paging, alignment, quantization scales, and
other runtime overhead.

## Prefill process

Prefill accepts a multi-token hidden-state batch. Query projection and joint KV
compression can be treated as parallel branches over the same batch.

The prompt's `cKV` and `kR` rows are appended to their cache regions. Attention
then constructs two score contributions: content queries read `cKV`, and
rotated positional queries read `kR`. After causal masking and softmax, the
weighted reduction occurs in latent space. Only the reduced latent contexts
pass through the value and output projections.

The persistent result is:

- four cached `cKV` rows;
- four cached `kR` rows;
- four layer outputs.

Temporary queries, partial scores, weights, and latent contexts are retired.

## Decode process

Decode begins with the prompt cache already resident and one new hidden state.
Only that token is projected. Its `cKV` and `kR` rows are appended rather than
replacing or moving the four prefix rows.

The new query reads all five content rows and all five positional rows. The
resulting five attention weights reduce the five `cKV` rows to one latent
context, which is then up-projected to one output.

The persistent result is:

- the original four `cKV` and `kR` rows;
- one newly appended `cKV` and `kR` row;
- one decode output.

## Copy and identity decisions

Projection work products and cache rows are separate materializations. Cache
append is modeled as copy followed by retirement of the temporary projection
result:

```text
temporary cKV[4]
  → create cached cKV[4] with provenance
  → retire temporary cKV[4]
```

The prefix cache is never updated in place in the decode example. A distinct
new cache-row materialization makes append-only growth visible and lets the
resource ledger derive the increase in cache bytes.

## Deliberate omissions

The demos do not model:

- individual attention heads or GPU warps;
- tensor-parallel collectives;
- paged-cache block tables and scheduler metadata;
- fused-kernel tiles, pipeline stages, or measured latency;
- FP8 cache encoding or dequantization;
- sparse token selection;
- multiple transformer layers.

Those details can be added as separate examples without changing the semantic
distinctions used here.
