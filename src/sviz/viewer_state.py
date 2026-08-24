"""Versioned mutable state for persisted visualization content and layouts."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from .next_models import ID_PATTERN, Identifier


class ViewerStateModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ViewerPoint(ViewerStateModel):
    x: float = 0
    y: float = 0


class ViewerAnnotation(ViewerStateModel):
    id: Identifier
    title: str
    body: str
    anchor: Identifier
    checkpoint: Identifier | None = None
    status: Literal["unresolved", "resolved"] = "unresolved"
    origin: Literal["authored", "user", "agent"] = "user"
    author_id: str | None = None

    @field_validator("id", "anchor", "checkpoint")
    @classmethod
    def validate_identifier(cls, value: str | None) -> str | None:
        if value is not None and not ID_PATTERN.fullmatch(value):
            raise ValueError("must be a valid semantic identifier")
        return value


class ViewerLayout(ViewerStateModel):
    shape_scale: float = Field(default=1, ge=0.7, le=1.4)
    place_offsets: dict[Identifier, ViewerPoint] = Field(default_factory=dict)
    place_scales: dict[Identifier, float] = Field(default_factory=dict)
    edge_offsets: dict[Identifier, ViewerPoint] = Field(default_factory=dict)
    collapsed_places: list[Identifier] = Field(default_factory=list)

    @field_validator("place_offsets", "place_scales", "edge_offsets")
    @classmethod
    def validate_mapping_ids(cls, value: dict[str, object]) -> dict[str, object]:
        for identifier in value:
            if not ID_PATTERN.fullmatch(identifier):
                raise ValueError(f"invalid semantic identifier {identifier!r}")
        return value

    @field_validator("place_scales")
    @classmethod
    def validate_place_scales(cls, value: dict[str, float]) -> dict[str, float]:
        for identifier, scale in value.items():
            if not 0.65 <= scale <= 1.75:
                raise ValueError(f"place scale for {identifier!r} must be between 0.65 and 1.75")
        return value


class SavedViewerView(ViewerStateModel):
    projection: Literal["ir", "compiled", "system", "timeline"] = "system"
    checkpoint: Identifier | None = None


class ViewerState(ViewerStateModel):
    version: Literal["0.1"] = "0.1"
    visualization_id: Identifier
    base_revision: str
    revision: int = Field(default=0, ge=0)
    narrative_overrides: dict[Identifier, str] = Field(default_factory=dict)
    annotations: list[ViewerAnnotation] = Field(default_factory=list)
    deleted_annotation_ids: list[Identifier] = Field(default_factory=list)
    layout: ViewerLayout = Field(default_factory=ViewerLayout)
    saved_view: SavedViewerView = Field(default_factory=SavedViewerView)

    @field_validator("visualization_id")
    @classmethod
    def validate_visualization_id(cls, value: str) -> str:
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("must be a valid identifier")
        return value

    @field_validator("narrative_overrides")
    @classmethod
    def validate_checkpoint_ids(cls, value: dict[str, str]) -> dict[str, str]:
        for identifier in value:
            if not ID_PATTERN.fullmatch(identifier):
                raise ValueError(f"invalid checkpoint identifier {identifier!r}")
        return value

    @model_validator(mode="after")
    def validate_annotation_sets(self) -> "ViewerState":
        annotation_ids = [annotation.id for annotation in self.annotations]
        if len(annotation_ids) != len(set(annotation_ids)):
            raise ValueError("annotation IDs must be unique")
        if len(self.deleted_annotation_ids) != len(set(self.deleted_annotation_ids)):
            raise ValueError("deleted annotation IDs must be unique")
        if set(annotation_ids) & set(self.deleted_annotation_ids):
            raise ValueError("an annotation cannot be present and deleted")
        return self


def empty_viewer_state(compiled: dict[str, object]) -> ViewerState:
    """Create an empty persisted overlay for one compiled visualization."""

    return ViewerState(
        visualization_id=str(compiled["visualization_id"]),
        base_revision=str(compiled["base_revision"]),
    )
