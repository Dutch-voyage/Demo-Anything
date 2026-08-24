# MLA prefill and decode visualization workflow

This document applies the [`code-to-demo user manual`](user-manual.md) to the
two MLA examples. The mechanism is defined in
[`mla-mechanism.md`](mla-mechanism.md).

## Gate 1: learning contracts

### Prefill

**Primary question:** How does a multi-token prompt build and consume MLA's
compressed cache without retaining full K/V tensors?

The reader must be able to identify:

- batched query and KV projection;
- separate `cKV` and `kR` cache regions;
- content and position score paths;
- causal normalization;
- latent reduction before value up-projection;
- the persistent state handed to decode.

### Decode

**Primary question:** How does one new token append to and attend over an
existing MLA prefix cache?

The reader must be able to identify:

- one-token projection versus four-token resident prefix state;
- append rather than replacement;
- direct scoring over five compressed rows;
- persistent cache growth by 1,152 BF16 bytes;
- one latent reduction and one output.

Both examples target readers who understand ordinary attention and KV caching
but have not yet internalized MLA's content/position split or absorption.

## Gate 2: source-evidence map

| Evidence | Source fact | Semantic claim |
| --- | --- | --- |
| DeepSeek-V2 report, MLA section | Keys and values share a low-rank latent `cKV`; up-projections can be absorbed | Cache content is a compressed latent rather than persistent full K/V |
| DeepSeek-V3 `MLA.forward`, query branch | Query is projected and split into content and RoPE parts | `qC` and `qR` are separate temporary entities |
| DeepSeek-V3 `MLA.forward`, KV branch | Joint projection yields normalized `cKV` and rotated `kR` | Cache has distinct content and positional materializations |
| DeepSeek-V3 optimized cache writes | `kv_cache` and `pe_cache` receive the current sequence range | Prefill creates four rows; decode appends one row |
| DeepSeek-V3 optimized score equations | Content and positional dot products are added | Two parallel score stages feed one normalization stage |
| DeepSeek-V3 optimized value equations | Weights reduce `kv_cache`, then the value slice of `wkv_b` expands the result | Latent context precedes value up-projection |
| FlashMLA support matrix | Production kernels distinguish prefill/decode and MLA execution modes | Demo schedule is semantic, not a universal kernel-level schedule |

Primary links:

- [DeepSeek-V2 technical report](https://arxiv.org/abs/2405.04434)
- [DeepSeek-V3 reference inference implementation](https://github.com/deepseek-ai/DeepSeek-V3/blob/main/inference/model.py)
- [FlashMLA](https://github.com/deepseek-ai/FlashMLA)

## Gate 3: semantic mapping

| Mechanism | IR representation |
| --- | --- |
| Input hidden states | Initial materializations in `input` |
| Query and KV projection branches | Child places under `projection` and parallel compute stages |
| `cKV` and `kR` cache arrays | Separate entities, materializations, child places, and byte quantities |
| Cache append | Transfer flow that copies a work product to cache and retires the work product |
| Absorbed content query | Compute stage creating a temporary in `score_path` |
| Content and position dot products | Parallel compute stages sharing `score_compute` capacity |
| Mask and softmax | One normalization stage |
| Probability-weighted `cKV` sum | `latent_reduce` stage and latent-context materialization |
| Value/output expansion | Final output-projection stage |

The same places, resource lanes, and seven authored execution steps are used in
both examples. This makes phase differences semantic rather than stylistic.

## Gate 4: execution decisions

- Time mode is `steps` because no measured kernel trace is being claimed.
- Stages sharing a step express intended logical concurrency.
- Cache writes are copies with provenance; projection work products retire.
- Prefill starts with an empty cache and creates four-token cache populations.
- Decode starts with those populations and creates separate one-token append
  materializations.
- Full per-head key and value entities are deliberately absent.
- Cache storage is derived from entity byte quantities rather than authored as
  a separate metric.

## Gates 5 and 6: validation and compilation checks

Run:

```bash
.venv/bin/sviz validate \
  examples/mla_prefill_vnext.yaml \
  examples/mla_decode_vnext.yaml

.venv/bin/sviz compile examples/mla_prefill_vnext.yaml -o /tmp/mla-prefill.json
.venv/bin/sviz compile examples/mla_decode_vnext.yaml -o /tmp/mla-decode.json
.venv/bin/pytest tests/test_mla_pipeline.py
```

Regression checks establish:

- both traces validate without warnings and compile deterministically;
- both use the same System roots and Timeline lanes;
- prefill projection and score paths expose parallel stages;
- prefill derives 4,608 cache bytes and leaves only cache plus output;
- decode preserves prefix materializations, appends two new cache parts, and
  derives 5,760 cache bytes;
- neither trace defines persistent full-key or full-value entities;
- renderer source contains no MLA, DeepSeek, prefill, decode, `cKV`, or RoPE
  branches.

## Gate 7: checkpoint narrative

Both examples use the same reader rhythm:

1. establish initial input and cache state;
2. project query and compressed KV paths;
3. write cache while absorbing the content query;
4. compute content and position scores;
5. normalize;
6. reduce cached values in latent space;
7. up-project output;
8. inspect persistent final state.

The phase contrast is visible at the first, cache-write, score, and final
checkpoints: prefill handles a four-token batch and creates the prefix, whereas
decode handles one token and grows the prefix.

## Gate 8: visual acceptance

Each demo must show, at default and narrow sizes:

- four stable top-level places: input, projection, cache, and attention;
- separate query/KV projection and `cKV`/`kR` cache children;
- unobstructed cache-write routes;
- six readable resource lanes;
- selection shared between System and Timeline projections;
- reversible place drag, resize, shape scale, edge adjustment, and reset.

Any repeated placement failure must be corrected through generic geometry or
display-planning rules, not workload-specific renderer code.

## Gate 9: release commands

```bash
.venv/bin/sviz export examples/mla_prefill_vnext.yaml \
  --format bundle --output dist/mla-prefill
.venv/bin/sviz export examples/mla_decode_vnext.yaml \
  --format bundle --output dist/mla-decode
```

The maintained source artifacts are the two traces, their two reader guides,
this evidence/workflow document, and `tests/test_mla_pipeline.py`. Generated
bundles are reproducible and do not need to be checked in.
