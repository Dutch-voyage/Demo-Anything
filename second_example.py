from __future__ import annotations

from pathlib import Path

from sviz import Demo


def build_demo() -> Demo:
    demo = Demo(
        identifier="second-example",
        title="copied elements in a horizontal group",
    )

    view = demo.view("view-1", label="view-1")
    plane = view.plane("plane-1", label="plane-1")

    element_1 = plane.element(
        "element-1",
        label="request",
        kind="request",
        attrs={"state": "ready", "slots": 1},
    )
    element_2 = element_1.copy("element-2")
    element_3 = element_1.copy("element-3")

    plane.group(
        "group-1",
        elements=[element_1, element_2, element_3],
        label="group-1",
        direction="horizontal",
    )

    return demo


if __name__ == "__main__":
    output = Path("examples/second_example.yaml")
    print(build_demo().write(output))
