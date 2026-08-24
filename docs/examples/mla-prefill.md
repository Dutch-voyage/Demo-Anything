# MLA prefill example

## Purpose

This example shows how four prompt tokens pass through one absorbed MLA layer
and leave a compressed cache ready for autoregressive decode. The reader should
see that content and positional cache rows are separate, full K/V tensors are
not persistent materializations, and value reduction occurs before value
up-projection.

Run it with:

```bash
.venv/bin/sviz view examples/mla_prefill_vnext.yaml
```

The example uses authored steps, not measured kernel timing. See
[`../mla-mechanism.md`](../mla-mechanism.md) for the mechanism and fidelity
boundary.

## What the elements mean

- **Prompt hidden states** hold the four input vectors.
- **Query path** creates content queries `qC` and RoPE queries `qR`.
- **KV compression path** creates one 512-element `cKV` row and one
  64-element positional `kR` row per token.
- **Compressed KV cache** stores `cKV` and `kR` in separate regions.
- **Score path** adds content and positional score contributions and applies
  causal softmax.
- **Latent value path** reduces cached `cKV` rows before the value and output
  projections.

## Step-by-step walkthrough

| Step | What happens | What to observe |
| ---: | --- | --- |
| 0 | Four prompt hidden states enter; the cache is empty. | Only `prompt.input` exists. |
| 1 | Query projection and joint KV compression run in parallel. | Both projection slots are active over the same four-token input. |
| 2 | Four `cKV` rows and four `kR` rows start copying into the cache while `qC` is absorbed. | Two cache-write channels and one score-compute slot are active together. |
| 3 | Content and positional score paths run in parallel. | `prompt.latent.cache` and `prompt.rope.cache` coexist; full K/V objects do not appear. |
| 4 | Score parts are added, causally masked, and normalized. | Ten allowed causal token pairs become one attention-weight object. |
| 5 | Attention weights reduce cached `cKV` rows. | One latent context per prompt token appears before value expansion. |
| 6 | Value and output projections run. | The compact cache remains resident while prompt outputs are produced. |
| 7 | Prefill completes and temporary state is gone. | Four outputs plus 4,608 bytes of compressed cache remain. |

## Expected final state

- `prompt.latent.cache`: 4,096 bytes;
- `prompt.rope.cache`: 512 bytes;
- `prompt.output`: four output hidden states;
- no prompt query, score, weight, or latent-context temporary.

The source-to-IR evidence and gate review are recorded in
[`../mla-workflow.md`](../mla-workflow.md).
