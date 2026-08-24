# MLA decode example

## Purpose

This example starts from the four-token prefill cache and follows one new token
through an absorbed MLA decode step. The reader should see append-only cache
growth, direct scoring over compressed prefix rows, and latent reduction before
the output projection.

Run it with:

```bash
.venv/bin/sviz view examples/mla_decode_vnext.yaml
```

The example uses authored steps, not measured FlashMLA timing. See
[`../mla-mechanism.md`](../mla-mechanism.md) for the mechanism and exclusions.

## What the elements mean

- **Prefix cKV[0:4]** and **prefix kR[0:4]** are the persistent output of
  prefill.
- **H[4]** is the new token's hidden state.
- **cKV[4]** and **kR[4]** are newly appended cache materializations with
  provenance from projection work products.
- **qC[4] · WUK** is the content query transformed for direct latent-cache
  scoring.
- The two score paths read five rows each: four prefix rows plus the new row.
- The latent value path produces one 512-element context and only then expands
  it to the output dimension.

## Step-by-step walkthrough

| Step | What happens | What to observe |
| ---: | --- | --- |
| 0 | Four compressed prefix rows and one new hidden state are resident. | The cache ledger starts at 4,608 bytes; no full K/V prefix exists. |
| 1 | Query and compressed-KV projections run for one token. | Prefix cache objects remain unchanged while two projection slots are active. |
| 2 | `cKV[4]` and `kR[4]` begin appending while `qC[4]` is absorbed. | Cache writes preserve the four-token prefix instead of replacing it. |
| 3 | The new query scores all five content and positional rows. | Cache occupancy is 5,760 bytes and both score paths are active. |
| 4 | Five combined scores become one attention distribution. | Temporary score parts retire when normalized weights appear. |
| 5 | Five `cKV` rows reduce to one latent context. | Value expansion has not happened yet. |
| 6 | Value and output projections produce the new hidden state. | All five cache rows remain resident while output projection runs. |
| 7 | The decode step completes. | Prefix rows, appended rows, and one output remain; all query and score temporaries are gone. |

## Expected final state

- original four-token `cKV` and `kR` cache materializations;
- one appended `cKV[4]` row of 1,024 bytes;
- one appended `kR[4]` row of 128 bytes;
- one decode output;
- 5,760 total compressed-cache bytes.

The source-to-IR evidence and gate review are recorded in
[`../mla-workflow.md`](../mla-workflow.md).
