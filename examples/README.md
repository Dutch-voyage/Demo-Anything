# Example traces

The repository keeps seven vNext examples. Each runs through the same semantic
compiler and portable renderer.

New authors should first read the
[IR authoring guide](../docs/ir-authoring-guide.md), then use these traces as
complete references for progressively richer lifecycle, resource, flow, and
timing patterns.

- [FlashAttention-2](../docs/examples/flash-attention.md):
  [`flash_attention_vnext.yaml`](flash_attention_vnext.yaml)
- [DeepEP](../docs/examples/deep-ep.md):
  [`deepep_vnext.yaml`](deepep_vnext.yaml)
- [MLA prefill](../docs/examples/mla-prefill.md):
  [`mla_prefill_vnext.yaml`](mla_prefill_vnext.yaml)
- [MLA decode](../docs/examples/mla-decode.md):
  [`mla_decode_vnext.yaml`](mla_decode_vnext.yaml)
- [`torch.distributed.all_to_all_single`](../docs/examples/torch-all-to-all-single.md):
  [`torch_all_to_all_single_vnext.yaml`](torch_all_to_all_single_vnext.yaml)
- [`all_to_all_single(async_op=False)`](../docs/examples/torch-all-to-all-sync.md):
  [`torch_all_to_all_sync_vnext.yaml`](torch_all_to_all_sync_vnext.yaml)
- [`all_to_all_single(async_op=True)` with shared-expert overlap](../docs/examples/torch-all-to-all-async-shared-expert.md):
  [`torch_all_to_all_async_shared_expert_vnext.yaml`](torch_all_to_all_async_shared_expert_vnext.yaml)

The complete guide index is [`docs/examples/README.md`](../docs/examples/README.md).
