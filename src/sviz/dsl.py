"""Small, typed Python authoring frontend for sviz.

The DSL deliberately describes identity and relationships, not coordinates.
It lowers to the existing semantic IR so validation, compilation, serving, and
export remain shared with YAML-authored demos.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal, Mapping, Sequence

import yaml

from .compiler import compile_trace
from .next_models import (
    ID_PATTERN,
    DraftCheckpoint,
    DraftClaim,
    DraftLink,
    DraftOperation,
    DraftPlace,
    DraftResource,
    DraftStage,
    DraftTime,
    DraftView as DraftViewDefinition,
    TraceDocument,
)


PlaneLayout = Literal["hierarchy", "memory", "grid", "queue", "network", "horizontal"]
SpanKind = Literal["compute", "control", "wait", "sync", "state-change"]
TimeUnit = Literal["ns", "us", "ms", "s"]


class AuthoringError(ValueError):
    """Raised when the Python authoring graph is inconsistent."""


def _copied(mapping: Mapping[str, Any] | None) -> dict[str, Any]:
    return dict(mapping or {})


@dataclass(slots=True, eq=False)
class Element:
    """A stable object that belongs to exactly one spatial plane."""

    id: str
    plane: Plane
    label: str
    kind: str = "object"
    attrs: dict[str, Any] = field(default_factory=dict)
    group: Group | None = field(default=None, init=False, repr=False)
    copied_from: Element | None = field(default=None, init=False, repr=False)

    def copy(
        self,
        identifier: str,
        *,
        into: Plane | None = None,
        label: str | None = None,
        kind: str | None = None,
        attrs: Mapping[str, Any] | None = None,
    ) -> Element:
        """Create a distinct element that inherits this element's properties."""

        return (into or self.plane).copy(
            identifier,
            self,
            label=label,
            kind=kind,
            attrs=attrs,
        )


@dataclass(slots=True, eq=False)
class Group:
    """An ordered semantic group whose members share one layout intent."""

    id: str
    plane: Plane
    label: str
    direction: Literal["horizontal"]
    members: tuple[Element, ...]
    attrs: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, eq=False)
class Edge:
    """A semantic connection between two elements."""

    id: str
    view: View
    source: Element
    target: Element
    label: str
    directed: bool
    semantic_role: Literal["edge", "equivalence"]
    attrs: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, eq=False)
class Lane:
    """A semantic timeline lane backed by a capacity-bearing resource."""

    id: str
    timeline: Timeline
    owner: Plane | Element
    label: str
    capacity: int = 1
    attrs: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True, eq=False)
class Span:
    """A scheduled interval with explicit correspondence targets."""

    id: str
    timeline: Timeline
    lane: Lane
    label: str
    start: float
    duration: float
    kind: SpanKind
    at: Plane | Element
    corresponds_to: tuple[Element | Edge, ...]
    after: tuple[Span, ...] = ()
    attrs: dict[str, Any] = field(default_factory=dict)

    @property
    def end(self) -> float:
        return self.start + self.duration


@dataclass(slots=True, eq=False)
class Plane:
    """A compiler-laid-out spatial plane containing elements."""

    id: str
    view: View
    label: str
    layout: PlaneLayout = "grid"
    attrs: dict[str, Any] = field(default_factory=dict)
    elements: list[Element] = field(default_factory=list, init=False)
    groups: list[Group] = field(default_factory=list, init=False)

    def element(
        self,
        identifier: str,
        *,
        label: str | None = None,
        kind: str = "object",
        attrs: Mapping[str, Any] | None = None,
    ) -> Element:
        """Add an object to this plane without specifying coordinates."""

        self.view.demo._register(identifier, "element")
        element = Element(
            id=identifier,
            plane=self,
            label=label or identifier,
            kind=kind,
            attrs=_copied(attrs),
        )
        self.elements.append(element)
        return element

    def copy(
        self,
        identifier: str,
        source: Element,
        *,
        label: str | None = None,
        kind: str | None = None,
        attrs: Mapping[str, Any] | None = None,
    ) -> Element:
        """Copy an element into this plane under a new stable identity.

        Label, kind, and author-defined attributes are inherited. Explicit
        attributes are merged over a deep copy of the source attributes.
        Containment and edges are relationships, so they are not copied.
        """

        if not isinstance(source, Element) or source.plane.view.demo is not self.view.demo:
            raise AuthoringError("copied element must belong to this demo")
        copied_attrs = deepcopy(source.attrs)
        if attrs is not None:
            copied_attrs.update(deepcopy(dict(attrs)))
        copied = self.element(
            identifier,
            label=source.label if label is None else label,
            kind=source.kind if kind is None else kind,
            attrs=copied_attrs,
        )
        copied.copied_from = source
        return copied

    def group(
        self,
        identifier: str,
        elements: Sequence[Element],
        *,
        label: str | None = None,
        direction: Literal["horizontal"] = "horizontal",
        attrs: Mapping[str, Any] | None = None,
    ) -> Group:
        """Group existing elements and preserve their authored row order."""

        members = tuple(elements)
        if direction != "horizontal":
            raise AuthoringError("the initial group operation supports horizontal layout only")
        if len(members) < 2:
            raise AuthoringError("a group requires at least two elements")
        if len({id(element) for element in members}) != len(members):
            raise AuthoringError("a group cannot contain the same element more than once")
        for element in members:
            if not isinstance(element, Element) or element.plane is not self:
                raise AuthoringError("group members must be elements from this plane")
            if element.group is not None:
                raise AuthoringError(
                    f"element {element.id!r} already belongs to group {element.group.id!r}"
                )
        self.view.demo._register(identifier, "group")
        group = Group(
            id=identifier,
            plane=self,
            label=label or identifier,
            direction=direction,
            members=members,
            attrs=_copied(attrs),
        )
        for element in members:
            element.group = group
        self.groups.append(group)
        return group


@dataclass(slots=True, eq=False)
class View:
    """A named spatial view containing compiler-laid-out planes."""

    id: str
    demo: Demo
    label: str
    attrs: dict[str, Any] = field(default_factory=dict)
    planes: list[Plane] = field(default_factory=list, init=False)
    edges: list[Edge] = field(default_factory=list, init=False)

    def plane(
        self,
        identifier: str,
        *,
        label: str | None = None,
        layout: PlaneLayout = "grid",
        attrs: Mapping[str, Any] | None = None,
    ) -> Plane:
        """Create a semantic plane; the compiler owns its placement."""

        self.demo._register(identifier, "plane")
        plane = Plane(
            id=identifier,
            view=self,
            label=label or identifier,
            layout=layout,
            attrs=_copied(attrs),
        )
        self.planes.append(plane)
        return plane

    def edge(
        self,
        identifier: str,
        source: Element,
        target: Element,
        *,
        label: str | None = None,
        directed: bool = True,
        attrs: Mapping[str, Any] | None = None,
    ) -> Edge:
        """Connect two elements within one plane."""

        return self._add_edge(
            identifier,
            source,
            target,
            label=label,
            directed=directed,
            semantic_role="edge",
            attrs=attrs,
        )

    def equivalence(
        self,
        identifier: str,
        left: Element,
        right: Element,
        *,
        label: str | None = None,
        attrs: Mapping[str, Any] | None = None,
    ) -> Edge:
        """Relate corresponding elements from two different planes."""

        return self._add_edge(
            identifier,
            left,
            right,
            label=label,
            directed=False,
            semantic_role="equivalence",
            attrs=attrs,
        )

    def _add_edge(
        self,
        identifier: str,
        source: Element,
        target: Element,
        *,
        label: str | None,
        directed: bool,
        semantic_role: Literal["edge", "equivalence"],
        attrs: Mapping[str, Any] | None,
    ) -> Edge:
        self.demo._require_elements(source, target, view=self)
        if semantic_role == "edge" and source.plane is not target.plane:
            raise AuthoringError(
                "ordinary edges must stay within one plane; use equivalence() across planes"
            )
        if semantic_role == "equivalence" and source.plane is target.plane:
            raise AuthoringError("equivalence endpoints must belong to different planes")
        self.demo._register(identifier, semantic_role)
        edge = Edge(
            id=identifier,
            view=self,
            source=source,
            target=target,
            label=label or identifier,
            directed=directed,
            semantic_role=semantic_role,
            attrs=_copied(attrs),
        )
        self.edges.append(edge)
        return edge


@dataclass(slots=True, eq=False)
class Timeline:
    """The optional temporal view of a demo."""

    id: str
    demo: Demo
    label: str
    unit: TimeUnit
    attrs: dict[str, Any] = field(default_factory=dict)
    lanes: list[Lane] = field(default_factory=list, init=False)
    spans: list[Span] = field(default_factory=list, init=False)

    def lane(
        self,
        identifier: str,
        *,
        owner: Plane | Element,
        label: str | None = None,
        capacity: int = 1,
        attrs: Mapping[str, Any] | None = None,
    ) -> Lane:
        """Create a timeline lane owned by a spatial plane or element."""

        self.demo._require_spatial(owner)
        if capacity < 1:
            raise AuthoringError("lane capacity must be at least 1")
        self.demo._register(identifier, "timeline lane")
        lane = Lane(
            id=identifier,
            timeline=self,
            owner=owner,
            label=label or identifier,
            capacity=capacity,
            attrs=_copied(attrs),
        )
        self.lanes.append(lane)
        return lane

    def span(
        self,
        identifier: str,
        *,
        lane: Lane,
        start: float,
        duration: float,
        corresponds_to: Sequence[Element | Edge],
        label: str | None = None,
        kind: SpanKind = "control",
        at: Plane | Element | None = None,
        after: Sequence[Span] = (),
        attrs: Mapping[str, Any] | None = None,
    ) -> Span:
        """Add a timeline interval tied to spatial objects or edges."""

        if lane.timeline is not self:
            raise AuthoringError("span lane belongs to a different timeline")
        if start < 0:
            raise AuthoringError("span start must be non-negative")
        if duration <= 0:
            raise AuthoringError("span duration must be positive")
        if kind not in {"compute", "control", "wait", "sync", "state-change"}:
            raise AuthoringError(f"unsupported span kind {kind!r}")
        if not corresponds_to:
            raise AuthoringError("span correspondence must name at least one element or edge")
        targets = tuple(corresponds_to)
        for target in targets:
            self.demo._require_correspondence_target(target)
        predecessors = tuple(after)
        for predecessor in predecessors:
            if predecessor.timeline is not self:
                raise AuthoringError("span dependency belongs to a different timeline")
            if predecessor.end > start:
                raise AuthoringError(
                    f"span {predecessor.id!r} ends after dependent span {identifier!r} starts"
                )
        location = at or lane.owner
        self.demo._require_spatial(location)
        self.demo._register(identifier, "event span")
        operation_id = f"operation.{identifier}"
        self.demo._register(operation_id, "generated operation")
        span = Span(
            id=identifier,
            timeline=self,
            lane=lane,
            label=label or identifier,
            start=float(start),
            duration=float(duration),
            kind=kind,
            at=location,
            corresponds_to=targets,
            after=predecessors,
            attrs=_copied(attrs),
        )
        self.spans.append(span)
        return span


class Demo:
    """Root builder for a small auto-laid-out spatial and temporal demo."""

    def __init__(
        self,
        identifier: str,
        *,
        title: str | None = None,
        description: str | None = None,
    ) -> None:
        self.id = identifier
        self.title = title or identifier
        self.description = description
        self._identifiers: dict[str, str] = {}
        self._register(identifier, "demo")
        self._view: View | None = None
        self._timeline: Timeline | None = None

    def view(
        self,
        identifier: str,
        *,
        label: str | None = None,
        attrs: Mapping[str, Any] | None = None,
    ) -> View:
        """Create the v0 spatial view. Only one is supported initially."""

        if self._view is not None:
            raise AuthoringError("the initial Python DSL supports one spatial view")
        self._register(identifier, "view")
        self._view = View(identifier, self, label or identifier, _copied(attrs))
        return self._view

    def timeline(
        self,
        identifier: str,
        *,
        label: str | None = None,
        unit: TimeUnit = "ms",
        attrs: Mapping[str, Any] | None = None,
    ) -> Timeline:
        """Create the optional temporal view. Only one is supported in v0."""

        if self._timeline is not None:
            raise AuthoringError("the initial Python DSL supports one timeline")
        self._register(identifier, "timeline")
        self._timeline = Timeline(identifier, self, label or identifier, unit, _copied(attrs))
        return self._timeline

    def to_trace(self) -> TraceDocument:
        """Lower the authoring graph to the existing validated semantic IR."""

        view = self._view
        if view is None or not view.planes:
            raise AuthoringError("define a spatial view with at least one plane")
        if not any(plane.elements for plane in view.planes):
            raise AuthoringError("define at least one element")

        places = [
            DraftPlace(
                id=plane.id,
                label=plane.label,
                role="group",
                layout=plane.layout,
                attrs={**plane.attrs, "dsl_view": view.id, "dsl_kind": "plane"},
            )
            for plane in view.planes
        ]
        places.extend(
            DraftPlace(
                id=group.id,
                label=group.label,
                parent=plane.id,
                role="group",
                layout=group.direction,
                attrs={**group.attrs, "dsl_kind": "group"},
            )
            for plane in view.planes
            for group in plane.groups
        )
        places.extend(
            DraftPlace(
                id=element.id,
                label=element.label,
                parent=element.group.id if element.group else plane.id,
                role="group",
                layout="hierarchy",
                attrs={
                    **element.attrs,
                    "dsl_kind": element.kind,
                    **(
                        {"dsl_copied_from": element.copied_from.id}
                        if element.copied_from
                        else {}
                    ),
                },
            )
            for plane in view.planes
            for element in plane.elements
        )
        links = [
            DraftLink(
                id=edge.id,
                label=edge.label,
                from_place=edge.source.id,
                to_place=edge.target.id,
                directed=edge.directed,
                attrs={
                    **edge.attrs,
                    "semantic_role": edge.semantic_role,
                    "source_plane": edge.source.plane.id,
                    "target_plane": edge.target.plane.id,
                },
            )
            for edge in view.edges
        ]

        timeline = self._timeline
        lanes = timeline.lanes if timeline else []
        spans = timeline.spans if timeline else []
        resources = [
            DraftResource(
                id=lane.id,
                label=lane.label,
                owner=lane.owner.id,
                kind="execution",
                capacity={"slots": float(lane.capacity)},
                attrs={**lane.attrs, "dsl_timeline": timeline.id if timeline else ""},
            )
            for lane in lanes
        ]
        operations = [
            DraftOperation(
                id=f"operation.{span.id}",
                label=span.label,
                kind="authored-event",
                attrs={"dsl_timeline": timeline.id if timeline else ""},
            )
            for span in spans
        ]
        stages = [
            DraftStage(
                id=span.id,
                label=span.label,
                operation=f"operation.{span.id}",
                kind=span.kind,
                at=span.at.id,
                claims=[DraftClaim(resource=span.lane.id, amount={"slots": 1.0})],
                after=[predecessor.id for predecessor in span.after],
                start=span.start,
                duration=span.duration,
                attrs={
                    **span.attrs,
                    "dsl_timeline": timeline.id if timeline else "",
                    "corresponds_to": [target.id for target in span.corresponds_to],
                },
            )
            for span in spans
        ]
        checkpoints = self._checkpoints(spans)

        return TraceDocument(
            version="0.2-draft",
            id=self.id,
            title=self.title,
            description=self.description,
            time=(
                DraftTime(mode="timeline", unit=timeline.unit)
                if timeline
                else DraftTime(mode="steps")
            ),
            places=places,
            resources=resources,
            links=links,
            entities=[],
            operations=operations,
            stages=stages,
            checkpoints=checkpoints,
            views=[
                DraftViewDefinition(
                    id=view.id,
                    label=view.label,
                    kind="spatial",
                    roots=[plane.id for plane in view.planes],
                    draggable=[plane.id for plane in view.planes],
                    importance=[
                        edge.id
                        for edge in view.edges
                        if edge.semantic_role == "equivalence"
                    ],
                    attrs=view.attrs,
                ),
                *(
                    [
                        DraftViewDefinition(
                            id=timeline.id,
                            label=timeline.label,
                            kind="timeline",
                            resources=[lane.id for lane in lanes],
                            attrs=timeline.attrs,
                        )
                    ]
                    if timeline and lanes
                    else []
                ),
            ],
        )

    def compile(self) -> dict[str, Any]:
        """Validate and compile this demo into renderer-ready JSON."""

        return compile_trace(self.to_trace())

    def to_dict(self) -> dict[str, Any]:
        """Return the lowered semantic IR as ordinary Python data."""

        return self.to_trace().model_dump(by_alias=True, exclude_none=True, mode="json")

    def write(self, path: str | Path) -> Path:
        """Write lowered YAML that can be used by all existing ``sviz`` commands."""

        destination = Path(path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(
            yaml.safe_dump(self.to_dict(), sort_keys=False, allow_unicode=True),
            encoding="utf-8",
        )
        return destination

    def _checkpoints(self, spans: Sequence[Span]) -> list[DraftCheckpoint]:
        if not self._timeline:
            return [
                DraftCheckpoint(
                    id="checkpoint.initial",
                    label="Initial state",
                    step=1,
                    narrative="Inspect the authored planes, elements, and semantic edges.",
                )
            ]
        points = sorted({0.0, *(span.start for span in spans), *(span.end for span in spans)})
        result: list[DraftCheckpoint] = []
        for index, point in enumerate(points):
            checkpoint_id = f"checkpoint.auto.{index}"
            if checkpoint_id in self._identifiers:
                raise AuthoringError(
                    f"identifier {checkpoint_id!r} is reserved for generated checkpoints"
                )
            starting = [span for span in spans if span.start == point]
            ending = [span for span in spans if span.end == point]
            focus = list(
                dict.fromkeys(
                    identifier
                    for span in [*starting, *ending]
                    for identifier in [span.id, *(target.id for target in span.corresponds_to)]
                )
            )
            if point == 0 and not starting:
                title = "Initial state"
                narrative = "Inspect the authored planes before the first event span."
            elif starting:
                labels = ", ".join(span.label for span in starting)
                title = labels
                narrative = f"Starting: {labels}. Select a span to inspect its corresponding objects and edges."
            else:
                labels = ", ".join(span.label for span in ending)
                title = f"After {labels}"
                narrative = f"Completed: {labels}. The spatial view preserves the same object identities."
            result.append(
                DraftCheckpoint(
                    id=checkpoint_id,
                    label=title,
                    at=point,
                    narrative=narrative,
                    focus=focus,
                )
            )
        return result

    def _register(self, identifier: str, kind: str) -> None:
        if not ID_PATTERN.fullmatch(identifier):
            raise AuthoringError(
                f"invalid {kind} identifier {identifier!r}; identifiers must start with a letter"
            )
        previous = self._identifiers.get(identifier)
        if previous:
            raise AuthoringError(
                f"identifier {identifier!r} is already used by {previous}; IDs are demo-global"
            )
        self._identifiers[identifier] = kind

    def _require_elements(self, *elements: Element, view: View) -> None:
        for element in elements:
            if not isinstance(element, Element) or element.plane.view is not view:
                raise AuthoringError("edge endpoints must be elements from this view")

    def _require_spatial(self, value: Plane | Element) -> None:
        if isinstance(value, Plane):
            valid = value.view.demo is self
        elif isinstance(value, Element):
            valid = value.plane.view.demo is self
        else:
            valid = False
        if not valid:
            raise AuthoringError("spatial reference belongs to a different demo")

    def _require_correspondence_target(self, value: Element | Edge) -> None:
        if isinstance(value, Element):
            self._require_spatial(value)
        elif not isinstance(value, Edge) or value.view.demo is not self:
            raise AuthoringError("span correspondence target belongs to a different demo")


__all__ = [
    "AuthoringError",
    "Demo",
    "Edge",
    "Element",
    "Group",
    "Lane",
    "Plane",
    "Span",
    "Timeline",
    "View",
]
