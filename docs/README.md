# Documentation map

`sviz` documentation follows the same path as the visualization pipeline:
understand the model, author a trace, verify the compiled result, and then
publish or persist the viewer.

## Start here

| Goal | Read |
| --- | --- |
| Understand what `sviz` does | [Project README](../README.md) |
| Learn the IR and write a first trace | [IR authoring guide](ir-authoring-guide.md) |
| Convert real code into a reviewed demo | [Code-to-demo user manual](user-manual.md) |
| Record evidence and gate reviews | [Example workbook template](example-workbook-template.md) |
| Understand compiler and renderer boundaries | [IR design](ir-design.md) |
| Check rendered text and element collisions | [Default-layout checking](layout-checking.md) |
| Embed or persist a visualization | [Persistence guide](persistence.md) |

## The complete authoring path

1. **Choose the question.** State what a reader should learn and bound one
   representative execution.
2. **Collect evidence.** Separate code or runtime facts from author assumptions.
3. **Model stable structure.** Define places, resources, links, entities,
   initial materializations, operations, and flows.
4. **Model execution.** Define resource-owning stages, explicit time,
   dependencies, reads, and lifecycle effects.
5. **Author the lesson.** Add checkpoints, Markdown narratives, focus targets,
   annotations, and a small view recipe.
6. **Validate and compile.** Reject invalid references, lifecycle, timing,
   capacity, and provenance before visual styling.
7. **Review both projections.** Inspect System for residency/topology and
   Timeline for order/overlap; fix meaning in the IR and reusable layout
   behavior in the compiler or renderer.
8. **Test and publish.** Add semantic regression tests, export the portable
   component, and optionally attach a viewer-state persistence adapter.

The [IR authoring guide](ir-authoring-guide.md) explains steps 3–6 at field
level. The [user manual](user-manual.md) turns all eight steps into nine
checkable quality gates for a production-quality example.

## Reference implementations

| Scenario | Mechanism | Source-to-IR workflow | Step-by-step visualization |
| --- | --- | --- | --- |
| FlashAttention-2 | — | [FA2 workflow](flash-attention-workflow.md) | [FA2 guide](examples/flash-attention.md) |
| DeepEP | [DeepEP mechanism](deepep-mechanism.md) | [DeepEP workflow](deepep-workflow.md) | [DeepEP guide](examples/deep-ep.md) |
| MLA prefill and decode | [MLA mechanism](mla-mechanism.md) | [MLA workflow](mla-workflow.md) | [MLA prefill](examples/mla-prefill.md) · [MLA decode](examples/mla-decode.md) |

All four traces are indexed in the [examples directory](../examples/README.md).

## Contracts and maintenance

- [IR design](ir-design.md) defines semantic boundaries and compilation rules.
- [Default-layout checking](layout-checking.md) defines the rendered overlap
  audit and CI integration.
- [Decision log](decision-log.md) records accepted design decisions.
- [`sviz-0.2-draft.schema.json`](../schema/sviz-0.2-draft.schema.json) is the
  machine-readable trace contract.
- [`sviz-viewer-state-0.1.schema.json`](../schema/sviz-viewer-state-0.1.schema.json)
  is the separate mutable reader-state contract.
- The tests assert validation, deterministic compilation, important snapshots,
  renderer capabilities, export portability, and persistence conflicts.
