# Example traces

The repository keeps two generated progressive examples and four complete
vNext examples. Each runs through the same semantic compiler and portable
renderer.

New authors should first read the
[IR authoring guide](../docs/ir-authoring-guide.md), then use these traces as
complete references for progressively richer lifecycle, resource, flow, and
timing patterns.

The root-level [`first_example.py`](../first_example.py) is a compact Python DSL
source: one authored view, one plane, and one horizontal group of shards. It generates
[`first_example.yaml`](first_example.yaml), whose compiled display contains
only the authored `view-1`—no synthetic System or Timeline view.

The root-level [`second_example.py`](../second_example.py) introduces two small
operations: copy an element's properties under new identities, then group the
elements while requesting a horizontal row. It generates
[`second_example.yaml`](second_example.yaml).

The [`python_dsl_minimal.py`](python_dsl_minimal.py) example uses the
experimental [Python authoring DSL](../docs/python-dsl-design.md) to declare
planes, elements, edges, equivalence, and timeline correspondence before
lowering to the same semantic IR.

- [FlashAttention-2](../docs/examples/flash-attention.md):
  [`flash_attention_vnext.yaml`](flash_attention_vnext.yaml)
- [DeepEP](../docs/examples/deep-ep.md):
  [`deepep_vnext.yaml`](deepep_vnext.yaml)
- [MLA prefill](../docs/examples/mla-prefill.md):
  [`mla_prefill_vnext.yaml`](mla_prefill_vnext.yaml)
- [MLA decode](../docs/examples/mla-decode.md):
  [`mla_decode_vnext.yaml`](mla_decode_vnext.yaml)

The complete guide index is [`docs/examples/README.md`](../docs/examples/README.md).
