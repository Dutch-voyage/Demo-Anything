# Viewer-state persistence

`sviz` keeps compiled execution data immutable and stores reader edits in a
separate `0.1` viewer-state document. This lets a deployment change storage
systems without changing the renderer or semantic IR.

## Stored state

The overlay contains:

- checkpoint Markdown overrides;
- user or agent annotations and changes to authored annotations;
- tombstones for deleted authored annotations;
- shape scale, place offsets and sizes, and edge offsets;
- the explicitly saved projection and checkpoint;
- visualization ID, compiled-base digest, and state revision.

Selection, open editors, and playback state are not persisted.

## Local file-backed viewer

Run:

```bash
sviz view examples/mla_decode_vnext.yaml
```

Persistence is enabled by default. This example uses
`examples/.sviz/mla-decode.viewer-state.json`; the file is created only after
the first explicit save. Use `--state-file PATH` to override the location or
`--no-persist` to run without the state endpoint and Save/Reload controls.

The page loads `/api/state` and exposes **Save changes** after a narrative,
annotation, layout, projection, or checkpoint changes. Saving writes the JSON
file atomically. A stale revision receives HTTP `412`, and the component shows
a conflict instead of overwriting newer state.

Annotation numbers are local to the current checkpoint. Hidden annotations at
other checkpoints do not consume the visible numbering. Authored annotations
that are visible at the same checkpoint are numbered before newly pinned ones.

The file adapter is for development and single-process deployment. It does not
provide authentication, authorization, multi-process locking, or audit logs.

## Portable component API

Without a server, a host can own persistence directly:

```js
const visualization = document.querySelector("systems-viz-next");
const state = visualization.exportViewerState();

await saveStateElsewhere(state);
visualization.importViewerState(await loadStateElsewhere());
```

With an HTTP adapter:

```html
<systems-viz-next
  visualization-id="mla-decode"
  src="/compiled/mla-decode.json"
  state-src="/api/visualizations/mla-decode/state">
</systems-viz-next>
```

`loadViewerState()` performs `GET state-src`. `saveViewerState()` performs
`PUT state-src` with JSON and `If-Match: "revision-N"`. A successful response
must return the complete viewer-state document with its incremented revision.

The component emits `viewer-state-change`, `viewer-state-load`,
`viewer-state-save`, `viewer-state-conflict`, and `viewer-state-error`.

## Annotation collection for agents

The current in-browser state is available without inspecting Shadow DOM:

```js
const annotations = [...document.querySelectorAll("systems-viz-next")]
  .flatMap(element => element.getAnnotations({
    checkpoint: "all",
    status: "unresolved",
  }));
```

Results include visualization identity, annotation and anchor IDs, checkpoint,
anchor label, content, status, origin, and optional author ID. Deleted
annotations are absent.

## Production adapter requirements

A production endpoint should add authentication, access scopes, audit fields,
rate limits, durable transactions, and revision-aware writes. Personal layouts
should normally be stored separately from shared editorial narratives and
annotations. If a compiled base changes, preserve annotations with missing
anchors as orphaned review items until an editor reattaches them.
