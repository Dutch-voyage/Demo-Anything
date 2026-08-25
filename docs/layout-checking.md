# Default-layout checking

The renderer includes a browser-native layout audit because real font metrics,
SVG transforms, responsive scaling, and clipping cannot be verified reliably
from compiled coordinates alone.

## Reader action

Select **Check layout** in the visualization header. The audit temporarily
renders every checkpoint in both System and Timeline at:

- shape scale `100%`;
- zero manual place offsets;
- place scale `100%`;
- zero manual edge offsets.

It then restores the reader's current projection, checkpoint, and layout. The
check does not mark viewer state as dirty or save anything.

The header reports **Layout clean** or the number of unique overlaps. Hover the
failure status to read the first affected checkpoint and semantic IDs; the same
details are included in its accessible label.

## What is checked

Errors fail the audit:

- text intersecting other visible text;
- sibling place boxes intersecting;
- materializations, meters, or active-stage shapes intersecting within a place;
- Timeline marks intersecting on the same lane and track;
- text extending outside its owning shape;
- edge-label text intersecting a visual element.

Shortened or hidden labels are warnings rather than overlap errors. Their full
text remains available through the element's accessible label or SVG title.
The returned report keeps warnings so stricter hosts may reject them.

The result is specific to the component's current host width. Resizing the host
invalidates the displayed result and requires a new check.

## Component API

Audit the currently rendered System or Timeline projection synchronously:

```js
const visualization = document.querySelector("systems-viz-next");
const current = visualization.auditCurrentLayout();
```

Audit all checkpoints in both projections at default layout:

```js
const report = await visualization.checkDefaultLayout();

if (report.status !== "pass") {
  console.table(report.issues.filter(issue => issue.severity === "error"));
}
```

Limit a check when investigating one state:

```js
await visualization.checkDefaultLayout({
  projections: ["system"],
  checkpoints: "current",
});
```

The component emits a composed `layout-check` event containing the complete
report. A host page with several blocks can collect results without inspecting
Shadow DOM:

```js
const reports = await Promise.all(
  [...document.querySelectorAll("systems-viz-next")]
    .map(element => element.checkDefaultLayout()),
);

const failures = reports.flatMap(report =>
  report.issues.filter(issue => issue.severity === "error"),
);
```

## CI use

Run the same public method from a real browser after the component has loaded.
For example, in Playwright:

```js
const report = await page.locator("systems-viz-next").evaluate(
  element => element.checkDefaultLayout(),
);

expect(report.status, JSON.stringify(report.issues, null, 2)).toBe("pass");
```

Repeat the check at each supported container width. The maintained examples are
reviewed at the normal desktop width and at a 360-pixel viewport. Keep label
truncation policy separate from overlap acceptance so dense scenarios can
remain legible without making the component unbounded.
