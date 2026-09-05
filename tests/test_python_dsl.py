from __future__ import annotations

from pathlib import Path
import runpy

import pytest

from sviz import AuthoringError, Demo, compile_trace, load_trace, validate_trace
from sviz.server import component_source


ROOT = Path(__file__).parents[1]
build_demo = runpy.run_path(ROOT / "examples" / "python_dsl_minimal.py")["build_demo"]
build_first_demo = runpy.run_path(ROOT / "first_example.py")["build_demo"]
build_second_demo = runpy.run_path(ROOT / "second_example.py")["build_demo"]


def _view(compiled: dict, identifier: str) -> dict:
    return next(view for view in compiled["display"]["views"] if view["id"] == identifier)


def test_first_example_compiles_to_exactly_one_authored_view() -> None:
    demo = build_first_demo()
    trace = demo.to_trace()
    compiled = demo.compile()

    assert trace.view is None
    assert [(view.id, view.kind, view.roots) for view in trace.views] == [
        ("view-1", "spatial", ["plane-1"]),
    ]
    assert set(compiled["display"]) == {"views", "inspectors"}
    assert [view["id"] for view in compiled["display"]["views"]] == ["view-1"]
    rendered_view = _view(compiled, "view-1")
    shard_ids = [f"shard-{index}" for index in range(8)]
    assert [place["id"] for place in rendered_view["places"]] == [
        "plane-1",
        "group-1",
        *shard_ids,
    ]
    assert rendered_view["children"]["plane-1"] == ["group-1"]
    assert rendered_view["children"]["group-1"] == shard_ids
    for profile in ("wide", "narrow"):
        boxes = rendered_view["geometry"][profile]["places"]
        row = [boxes[identifier] for identifier in shard_ids]
        assert len({box["y"] for box in row}) == 1
        assert [box["x"] for box in row] == sorted(box["x"] for box in row)


def test_second_example_groups_elements_in_an_authored_horizontal_row() -> None:
    demo = build_second_demo()
    trace = demo.to_trace()
    compiled = demo.compile()

    places = {place.id: place for place in trace.places}
    assert places["group-1"].parent == "plane-1"
    assert places["group-1"].layout == "horizontal"
    assert places["element-1"].attrs == {
        "state": "ready",
        "slots": 1,
        "dsl_kind": "request",
    }
    assert places["element-2"].attrs == {
        **places["element-1"].attrs,
        "dsl_copied_from": "element-1",
    }
    assert places["element-3"].attrs == {
        **places["element-1"].attrs,
        "dsl_copied_from": "element-1",
    }
    assert [places[identifier].parent for identifier in ("element-1", "element-2", "element-3")] == [
        "group-1",
        "group-1",
        "group-1",
    ]

    view = _view(compiled, "view-1")
    assert view["children"]["group-1"] == ["element-1", "element-2", "element-3"]
    for profile in ("wide", "narrow"):
        boxes = view["geometry"][profile]["places"]
        row = [boxes[identifier] for identifier in view["children"]["group-1"]]
        assert len({box["y"] for box in row}) == 1
        assert [box["x"] for box in row] == sorted(box["x"] for box in row)


def test_copy_creates_an_independent_identity_and_does_not_copy_relationships() -> None:
    demo = Demo("copy-demo")
    view = demo.view("view")
    source_plane = view.plane("source-plane")
    destination_plane = view.plane("destination-plane")
    source = source_plane.element(
        "source",
        label="request",
        kind="request",
        attrs={"state": "ready", "limits": {"slots": 1}},
    )
    grouped_peer = source.copy("grouped-peer")
    source_plane.group("source-group", [source, grouped_peer])

    copied = source.copy("copied", into=destination_plane)

    assert copied is not source
    assert copied.id == "copied"
    assert copied.plane is destination_plane
    assert copied.label == source.label
    assert copied.kind == source.kind
    assert copied.attrs == source.attrs
    assert copied.attrs is not source.attrs
    assert copied.attrs["limits"] is not source.attrs["limits"]
    assert copied.copied_from is source
    assert copied.group is None

    copied.attrs["limits"]["slots"] = 2
    assert source.attrs["limits"]["slots"] == 1

    overridden = destination_plane.copy(
        "overridden",
        source,
        label="priority request",
        attrs={"state": "urgent"},
    )
    assert overridden.label == "priority request"
    assert overridden.kind == "request"
    assert overridden.attrs == {"state": "urgent", "limits": {"slots": 1}}

    places = {place.id: place for place in demo.to_trace().places}
    assert places["copied"].parent == "destination-plane"
    assert places["copied"].attrs["dsl_copied_from"] == "source"


def test_minimal_python_demo_lowers_to_existing_ir() -> None:
    demo = build_demo()
    trace = demo.to_trace()
    report = validate_trace(trace)

    assert report.ok, "\n".join(str(issue) for issue in report.issues)
    assert [item.id for item in trace.places[:2]] == [
        "buckets",
        "lanes",
    ]
    assert [(view.id, view.kind) for view in trace.views] == [
        ("schedule", "spatial"),
        ("round", "timeline"),
    ]
    assert trace.views[0].roots == ["buckets", "lanes"]
    assert trace.views[1].resources == ["scheduler", "worker"]


def test_compiler_preserves_element_edges_and_correspondence_metadata() -> None:
    compiled = build_demo().compile()
    routes = {item["id"]: item for item in _view(compiled, "schedule")["routes"]}
    marks = {item["id"]: item for item in _view(compiled, "round")["marks"]}

    assert routes["edge.reaches-frontier"]["from"] == "lane.0"
    assert routes["edge.reaches-frontier"]["to"] == "frontier.0"
    assert routes["edge.reaches-frontier"]["semantic_role"] == "edge"
    assert routes["equivalence.short-lane0"]["from"] == "bucket.short"
    assert routes["equivalence.short-lane0"]["to"] == "lane.0"
    assert routes["equivalence.short-lane0"]["semantic_role"] == "equivalence"
    assert marks["span.boundary"]["corresponds_to"] == [
        "lane.0",
        "edge.reaches-frontier",
        "equivalence.short-lane0",
    ]


def test_compilation_is_deterministic_and_generates_boundary_checkpoints() -> None:
    first = build_demo().compile()
    second = build_demo().compile()

    assert first == second
    assert [item["cursor"] for item in first["execution"]["checkpoints"]] == [
        0.0,
        1.0,
        2.0,
    ]
    assert first["execution"]["checkpoints"][0]["active_stages"] == [
        "span.boundary"
    ]
    assert first["execution"]["checkpoints"][1]["active_stages"] == [
        "span.reallocate"
    ]


def test_python_demo_can_emit_yaml_for_existing_commands(tmp_path: Path) -> None:
    path = build_demo().write(tmp_path / "demo.yaml")
    loaded = load_trace(path)

    assert validate_trace(loaded).ok
    assert compile_trace(loaded) == build_demo().compile()


def test_small_spatial_only_demo_needs_no_fake_timeline_objects() -> None:
    demo = Demo("spatial-only")
    view = demo.view("view")
    plane = view.plane("plane")
    plane.element("object")

    compiled = demo.compile()

    assert [view["id"] for view in compiled["display"]["views"]] == ["view"]
    assert _view(compiled, "view")["roots"] == ["plane"]


def test_dsl_rejects_ambiguous_edges_and_duplicate_identity() -> None:
    demo = Demo("invalid-demo")
    view = demo.view("view")
    left = view.plane("left")
    right = view.plane("right")
    first = left.element("first")
    second = left.element("second")
    other = right.element("other")

    with pytest.raises(AuthoringError, match="IDs are demo-global"):
        right.element("first")
    with pytest.raises(AuthoringError, match="ordinary edges must stay within"):
        view.edge("bad.edge", first, other)
    with pytest.raises(AuthoringError, match="different planes"):
        view.equivalence("bad.equivalence", first, second)
    with pytest.raises(AuthoringError, match="at least two"):
        left.group("bad.group", [first])
    with pytest.raises(AuthoringError, match="this plane"):
        left.group("bad.cross-plane", [first, other])
    left.group("valid.group", [first, second])
    third = left.element("third")
    with pytest.raises(AuthoringError, match="already belongs"):
        left.group("bad.overlap", [first, third])

    foreign_demo = Demo("foreign-demo")
    foreign_view = foreign_demo.view("foreign-view")
    foreign_plane = foreign_view.plane("foreign-plane")
    foreign = foreign_plane.element("foreign")
    with pytest.raises(AuthoringError, match="must belong to this demo"):
        left.copy("bad.copy", foreign)


def test_existing_capacity_validation_applies_to_python_spans() -> None:
    demo = Demo("overlap")
    view = demo.view("view")
    plane = view.plane("plane")
    element = plane.element("object")
    timeline = demo.timeline("timeline")
    lane = timeline.lane("lane", owner=plane, capacity=1)
    timeline.span(
        "span.first",
        lane=lane,
        start=0,
        duration=2,
        corresponds_to=[element],
    )
    timeline.span(
        "span.second",
        lane=lane,
        start=1,
        duration=2,
        corresponds_to=[element],
    )

    codes = {issue.code for issue in validate_trace(demo.to_trace()).errors}

    assert "resource-over-capacity" in codes


def test_serialized_span_correspondence_is_revalidated() -> None:
    trace = build_demo().to_trace()
    stage = trace.stages[0].model_copy(
        update={"attrs": {"corresponds_to": ["missing.object"]}}
    )
    invalid = trace.model_copy(update={"stages": [stage, *trace.stages[1:]]})

    codes = {issue.code for issue in validate_trace(invalid).errors}

    assert "unknown-reference" in codes


def test_renderer_supports_equivalence_and_cross_view_selection() -> None:
    source = component_source()

    assert "...this.displayViews" in source
    assert 'this.displayViews.find(view => view.id === this.view)' in source
    assert '{ id: "system", label: "System" }' not in source
    assert '{ id: "timeline", label: "Timeline" }' not in source
    assert "relatedSelection()" in source
    assert 'route.semantic_role === "equivalence"' in source
    assert "mark.corresponds_to" in source
    assert 'stroke-dasharray="${isEquivalence ? "7 5" : "none"}"' in source
