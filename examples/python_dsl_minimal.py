"""Minimal Python-authored demo with spatial and temporal correspondence."""

from __future__ import annotations

from pathlib import Path
import sys

from sviz import Demo


def build_demo() -> Demo:
    demo = Demo(
        "python-dsl-bucket-lanes",
        title="Bucket demand and lane frontier",
        description=(
            "A tiny Python-authored example connecting bucket objects, lane "
            "objects, and event spans without authored coordinates."
        ),
    )

    view = demo.view("schedule", label="Scheduling state")
    buckets = view.plane("buckets", label="Completion buckets")
    lanes = view.plane("lanes", label="Lane and frontier state")

    short = buckets.element("bucket.short", label="Short debt: 2", kind="bucket")
    long = buckets.element("bucket.long", label="Long debt: 6", kind="bucket")
    lane0 = lanes.element("lane.0", label="Lane 0 · S-21", kind="lane")
    frontier0 = lanes.element("frontier.0", label="Frontier f1", kind="frontier")
    lane1 = lanes.element("lane.1", label="Lane 1 · open", kind="lane")

    reaches = view.edge(
        "edge.reaches-frontier",
        lane0,
        frontier0,
        label="reaches chunk boundary",
    )
    short_mapping = view.equivalence(
        "equivalence.short-lane0",
        short,
        lane0,
        label="short bucket ↔ current lane",
    )
    long_mapping = view.equivalence(
        "equivalence.long-lane1",
        long,
        lane1,
        label="long bucket ↔ next lane",
    )

    timeline = demo.timeline("round", label="Scheduling round", unit="ms")
    scheduler = timeline.lane("scheduler", owner=lanes, label="Scheduler")
    worker = timeline.lane("worker", owner=lane0, label="Lane 0 worker")

    boundary = timeline.span(
        "span.boundary",
        lane=worker,
        start=0,
        duration=1,
        label="Reach frontier",
        kind="compute",
        at=lane0,
        corresponds_to=[lane0, reaches, short_mapping],
    )
    timeline.span(
        "span.reallocate",
        lane=scheduler,
        start=1,
        duration=1,
        label="Reallocate released lane",
        kind="control",
        at=lanes,
        after=[boundary],
        corresponds_to=[long, long_mapping, lane1],
    )
    return demo


if __name__ == "__main__":
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/tmp/python-dsl-demo.yaml")
    print(build_demo().write(output))
