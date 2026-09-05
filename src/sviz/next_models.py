"""Draft semantic IR used by the new compiled visualization pipeline."""

from __future__ import annotations

import re
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


ID_PATTERN = re.compile(r"^[A-Za-z][A-Za-z0-9_.-]*$")
Identifier = str
Scalar = str | int | float | bool
DimensionMap = dict[str, float]


def _dimensions(value: DimensionMap, name: str) -> DimensionMap:
    for dimension, amount in value.items():
        if not ID_PATTERN.fullmatch(dimension):
            raise ValueError(f"{name} dimension {dimension!r} is not a valid identifier")
        if amount < 0:
            raise ValueError(f"{name}.{dimension} must be non-negative")
    return value


class DraftModel(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)


class Named(DraftModel):
    id: Identifier
    label: str | None = None
    attrs: dict[str, Any] = Field(default_factory=dict)
    tags: dict[str, Scalar] = Field(default_factory=dict)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("must start with a letter and contain only letters, numbers, '.', '_' or '-'")
        return value


class DraftTime(DraftModel):
    mode: Literal["timeline", "steps"]
    unit: Literal["ns", "us", "ms", "s"] | None = None

    @model_validator(mode="after")
    def validate_unit(self) -> "DraftTime":
        if self.mode == "timeline" and self.unit is None:
            raise ValueError("timeline mode requires a unit")
        if self.mode == "steps" and self.unit is not None:
            raise ValueError("steps mode must not define a unit")
        return self


class DraftPlace(Named):
    parent: Identifier | None = None
    role: Literal["group", "storage", "buffer", "executor", "register", "queue"] = "group"
    layout: Literal[
        "hierarchy",
        "memory",
        "grid",
        "queue",
        "network",
        "horizontal",
    ] = "hierarchy"
    capacity: DimensionMap = Field(default_factory=dict)

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, value: DimensionMap) -> DimensionMap:
        return _dimensions(value, "capacity")


class DraftResource(Named):
    owner: Identifier
    kind: Literal["storage", "bandwidth", "execution", "coordination"]
    capacity: DimensionMap

    @field_validator("capacity")
    @classmethod
    def validate_capacity(cls, value: DimensionMap) -> DimensionMap:
        if not value:
            raise ValueError("resource capacity must not be empty")
        return _dimensions(value, "capacity")


class DraftLink(Named):
    from_place: Identifier = Field(alias="from")
    to_place: Identifier = Field(alias="to")
    directed: bool = False
    resource: Identifier | None = None


class DraftEntity(Named):
    kind: str
    quantity: DimensionMap = Field(default_factory=dict)

    @field_validator("quantity")
    @classmethod
    def validate_quantity(cls, value: DimensionMap) -> DimensionMap:
        return _dimensions(value, "quantity")


class DraftMaterialization(DraftModel):
    id: Identifier
    entity: Identifier
    place: Identifier
    label: str | None = None
    attrs: dict[str, Any] = Field(default_factory=dict)

    @field_validator("id")
    @classmethod
    def validate_id(cls, value: str) -> str:
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("invalid materialization identifier")
        return value


LifecycleAction = Literal["create", "place", "unplace", "retire", "update", "relate"]
WritePolicy = Literal["replace", "accumulate", "assemble", "select"]


class DraftEffect(DraftModel):
    action: LifecycleAction
    materialization: Identifier
    entity: Identifier | None = None
    place: Identifier | None = None
    from_materialization: Identifier | None = Field(default=None, alias="from")
    to: Identifier | None = None
    relation: str | None = None
    write: WritePolicy | None = None
    attrs: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_shape(self) -> "DraftEffect":
        if self.action == "create" and (self.entity is None or self.place is None):
            raise ValueError("create effects require entity and place")
        if self.action == "place" and self.place is None:
            raise ValueError("place effects require place")
        if self.action == "relate" and (self.to is None or self.relation is None):
            raise ValueError("relate effects require to and relation")
        if self.write is not None and self.action != "update":
            raise ValueError("write policy is only valid for update effects")
        return self


class DraftClaim(DraftModel):
    resource: Identifier
    amount: DimensionMap

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: DimensionMap) -> DimensionMap:
        if not value:
            raise ValueError("claim amount must not be empty")
        return _dimensions(value, "claim")


StageKind = Literal["compute", "transfer", "control", "wait", "sync", "state-change"]


class DraftOperation(Named):
    kind: str


class DraftStage(Named):
    operation: Identifier
    kind: StageKind
    at: Identifier | None = None
    link: Identifier | None = None
    flow: Identifier | None = None
    reads: list[Identifier] = Field(default_factory=list)
    effects: list[DraftEffect] = Field(default_factory=list)
    claims: list[DraftClaim] = Field(default_factory=list)
    after: list[Identifier] = Field(default_factory=list)
    start: float | None = None
    duration: float | None = None
    step: int | None = None

    @model_validator(mode="after")
    def validate_shape(self) -> "DraftStage":
        if self.kind == "transfer" and self.link is None:
            raise ValueError("transfer stages require a link")
        if self.kind != "transfer" and self.link is not None:
            raise ValueError("link is only valid for transfer stages")
        if self.kind != "transfer" and self.at is None:
            raise ValueError("non-transfer stages require at")
        if self.start is not None and self.start < 0:
            raise ValueError("start must be non-negative")
        if self.duration is not None and self.duration < 0:
            raise ValueError("duration must be non-negative")
        if self.step is not None and self.step < 1:
            raise ValueError("step must be at least 1")
        return self


class DraftFlow(Named):
    entity: Identifier | None = None
    stages: list[Identifier]

    @field_validator("stages")
    @classmethod
    def stages_not_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("flow stages must not be empty")
        return value


class DraftCheckpoint(Named):
    at: float | None = None
    step: int | None = None
    detail: str | None = None
    narrative: str | None = None
    focus: list[Identifier] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_coordinate(self) -> "DraftCheckpoint":
        if (self.at is None) == (self.step is None):
            raise ValueError("checkpoint requires exactly one of at or step")
        return self


class DraftAnnotation(Named):
    anchor: Identifier
    checkpoint: Identifier | None = None
    body: str = Field(min_length=1)
    status: Literal["unresolved", "resolved"] = "unresolved"


class DraftViewRecipe(DraftModel):
    """Legacy two-projection recipe accepted for existing YAML traces."""

    system_roots: list[Identifier]
    draggable: list[Identifier] = Field(default_factory=list)
    timeline_resources: list[Identifier]
    importance: list[Identifier] = Field(default_factory=list)
    show_source: bool = True
    show_compiled: bool = True


class DraftView(Named):
    """One authored view in the generic display collection."""

    kind: Literal["spatial", "timeline"]
    roots: list[Identifier] = Field(default_factory=list)
    resources: list[Identifier] = Field(default_factory=list)
    draggable: list[Identifier] = Field(default_factory=list)
    importance: list[Identifier] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_shape(self) -> "DraftView":
        if self.id in {"ir", "compiled"}:
            raise ValueError("view IDs 'ir' and 'compiled' are reserved for inspectors")
        if self.kind == "spatial":
            if not self.roots:
                raise ValueError("spatial views require at least one root plane")
            if self.resources:
                raise ValueError("resources are only valid on timeline views")
        else:
            if not self.resources:
                raise ValueError("timeline views require at least one resource")
            if self.roots or self.draggable:
                raise ValueError("roots and draggable are only valid on spatial views")
        return self


class TraceDocument(DraftModel):
    version: Literal["0.2-draft"]
    id: Identifier
    title: str
    description: str | None = None
    time: DraftTime
    places: list[DraftPlace]
    resources: list[DraftResource] = Field(default_factory=list)
    links: list[DraftLink] = Field(default_factory=list)
    entities: list[DraftEntity] = Field(default_factory=list)
    initial_materializations: list[DraftMaterialization] = Field(default_factory=list)
    operations: list[DraftOperation] = Field(default_factory=list)
    stages: list[DraftStage] = Field(default_factory=list)
    flows: list[DraftFlow] = Field(default_factory=list)
    annotations: list[DraftAnnotation] = Field(default_factory=list)
    checkpoints: list[DraftCheckpoint]
    views: list[DraftView] = Field(default_factory=list)
    view: DraftViewRecipe | None = None

    @field_validator("places", "checkpoints")
    @classmethod
    def collection_not_empty(cls, value: list[Any]) -> list[Any]:
        if not value:
            raise ValueError("collection must not be empty")
        return value

    @field_validator("id")
    @classmethod
    def validate_document_id(cls, value: str) -> str:
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("must be a valid identifier")
        return value

    @model_validator(mode="after")
    def validate_view_contract(self) -> "TraceDocument":
        if bool(self.views) == (self.view is not None):
            raise ValueError("define exactly one of generic views or the legacy view recipe")
        return self


def resolved_views(trace: TraceDocument) -> list[DraftView]:
    """Return canonical views, adapting legacy System/Timeline recipes on input."""

    if trace.views:
        return trace.views
    assert trace.view is not None
    legacy = trace.view
    views = [
        DraftView(
            id="system",
            label="System",
            kind="spatial",
            roots=legacy.system_roots,
            draggable=legacy.draggable,
            importance=legacy.importance,
        )
    ]
    if legacy.timeline_resources:
        views.append(
            DraftView(
                id="timeline",
                label="Timeline",
                kind="timeline",
                resources=legacy.timeline_resources,
                importance=legacy.importance,
            )
        )
    return views
