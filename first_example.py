from __future__ import annotations

from pathlib import Path

from sviz import Demo


def build_demo() -> Demo:
    demo = Demo(
        identifier="first-example",
        title="first example",
    )

    view = demo.view("view-1", label="view-1")

    plane_1 = view.plane("plane-1", label="plane-1")

    num_shards = 8

    plane_1.group("group-1", [plane_1.element(f"shard-{i}", label=f"shard-{i}") for i in range(num_shards)])

    return demo

if __name__ == "__main__":
    output = Path("examples/first_example.yaml")
    print(build_demo().write(output))
