"""Semantic validation for the draft IR."""

from __future__ import annotations

from collections import defaultdict
from typing import Iterable

import networkx as nx

from .next_models import DraftEffect, DraftStage, TraceDocument, resolved_views
from .validation import ValidationIssue, ValidationReport


def _add(
    issues: list[ValidationIssue],
    code: str,
    path: str,
    message: str,
    *,
    level: str = "error",
) -> None:
    issues.append(ValidationIssue(level=level, code=code, path=path, message=message))  # type: ignore[arg-type]


def _ref(
    issues: list[ValidationIssue],
    value: str | None,
    allowed: set[str],
    path: str,
    kind: str,
) -> None:
    if value is not None and value not in allowed:
        _add(issues, "unknown-reference", path, f"unknown {kind} {value!r}")


def _coordinates(trace: TraceDocument, stage: DraftStage) -> tuple[float, float]:
    if trace.time.mode == "timeline":
        assert stage.start is not None and stage.duration is not None
        return round(stage.start, 9), round(stage.start + stage.duration, 9)
    assert stage.step is not None
    return float(stage.step), float(stage.step + 1)


def _apply_effect(
    effect: DraftEffect,
    state: dict[str, dict[str, object]],
    issues: list[ValidationIssue],
    path: str,
) -> None:
    current = state.get(effect.materialization)
    if effect.action == "create":
        if current is not None:
            _add(issues, "materialization-already-present", path, f"creates existing materialization {effect.materialization!r}")
            return
        if effect.from_materialization is not None and effect.from_materialization not in state:
            _add(issues, "provenance-not-present", path, f"copy source {effect.from_materialization!r} is not present")
        state[effect.materialization] = {
            "entity": effect.entity,
            "place": effect.place,
            "provenance": effect.from_materialization,
            "updates": 0,
        }
    elif effect.action == "retire":
        if current is None:
            _add(issues, "materialization-not-present", path, f"retires absent materialization {effect.materialization!r}")
        else:
            state.pop(effect.materialization)
    elif effect.action == "place":
        if current is None:
            _add(issues, "materialization-not-present", path, f"places absent materialization {effect.materialization!r}")
        else:
            current["place"] = effect.place
    elif effect.action == "unplace":
        if current is None:
            _add(issues, "materialization-not-present", path, f"unplaces absent materialization {effect.materialization!r}")
        else:
            current["place"] = None
    elif effect.action == "update":
        if current is None:
            _add(issues, "materialization-not-present", path, f"updates absent materialization {effect.materialization!r}")
        else:
            current["updates"] = int(current.get("updates", 0)) + 1
    elif effect.action == "relate":
        if current is None:
            _add(issues, "materialization-not-present", path, f"relates absent materialization {effect.materialization!r}")
        if effect.to not in state:
            _add(issues, "materialization-not-present", path, f"relation target {effect.to!r} is not present")


def _validate_lifecycle(trace: TraceDocument, issues: list[ValidationIssue]) -> None:
    state = {
        item.id: {"entity": item.entity, "place": item.place, "provenance": None, "updates": 0}
        for item in trace.initial_materializations
    }
    starts: dict[float, list[tuple[int, DraftStage]]] = defaultdict(list)
    ends: dict[float, list[tuple[int, DraftStage]]] = defaultdict(list)
    for index, stage in enumerate(trace.stages):
        start, end = _coordinates(trace, stage)
        starts[start].append((index, stage))
        ends[end].append((index, stage))

    for coordinate in sorted(set(starts) | set(ends)):
        for index, stage in ends.get(coordinate, []):
            for effect_index, effect in enumerate(stage.effects):
                _apply_effect(effect, state, issues, f"stages.{index}.effects.{effect_index}")

        before = set(state)
        for index, stage in starts.get(coordinate, []):
            for materialization in stage.reads:
                if materialization not in before:
                    _add(
                        issues,
                        "materialization-not-present",
                        f"stages.{index}.reads",
                        f"reads absent materialization {materialization!r}",
                    )


def _descendants(trace: TraceDocument, owner: str) -> set[str]:
    children: dict[str, list[str]] = defaultdict(list)
    for place in trace.places:
        if place.parent:
            children[place.parent].append(place.id)
    result = {owner}
    pending = [owner]
    while pending:
        current = pending.pop()
        for child in children.get(current, []):
            if child not in result:
                result.add(child)
                pending.append(child)
    return result


def _validate_capacities(trace: TraceDocument, issues: list[ValidationIssue]) -> None:
    entity_by_id = {item.id: item for item in trace.entities}
    resource_by_id = {item.id: item for item in trace.resources}
    coordinates = sorted({value for stage in trace.stages for value in _coordinates(trace, stage)})
    emitted: set[tuple[str, str, float]] = set()

    for coordinate in coordinates:
        active = [stage for stage in trace.stages if _coordinates(trace, stage)[0] <= coordinate < _coordinates(trace, stage)[1]]
        claims: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        for stage in active:
            for claim in stage.claims:
                for dimension, amount in claim.amount.items():
                    claims[claim.resource][dimension] += amount
        for resource_id, dimensions in claims.items():
            resource = resource_by_id.get(resource_id)
            if resource is None:
                continue
            for dimension, amount in dimensions.items():
                capacity = resource.capacity.get(dimension)
                if capacity is None:
                    _add(
                        issues,
                        "unbounded-resource",
                        f"resources.{resource_id}",
                        f"resource does not declare {dimension!r} capacity",
                        level="warning",
                    )
                elif amount > capacity and (resource_id, dimension, coordinate) not in emitted:
                    emitted.add((resource_id, dimension, coordinate))
                    _add(
                        issues,
                        "resource-over-capacity",
                        f"resources.{resource_id}",
                        f"claims total {amount:g} {dimension} at {coordinate:g}, capacity is {capacity:g}",
                    )

    storage_resources = [item for item in trace.resources if item.kind == "storage"]
    if not storage_resources:
        return
    state = {
        item.id: {"entity": item.entity, "place": item.place, "provenance": None, "updates": 0}
        for item in trace.initial_materializations
    }
    end_stages: dict[float, list[DraftStage]] = defaultdict(list)
    for stage in trace.stages:
        end_stages[_coordinates(trace, stage)[1]].append(stage)

    def check_storage(coordinate: float) -> None:
        for resource in storage_resources:
            owned_places = _descendants(trace, resource.owner)
            used: dict[str, float] = defaultdict(float)
            for materialization in state.values():
                if materialization.get("place") not in owned_places:
                    continue
                entity = entity_by_id.get(str(materialization.get("entity")))
                if entity:
                    for dimension, amount in entity.quantity.items():
                        used[dimension] += amount
            for dimension, amount in used.items():
                capacity = resource.capacity.get(dimension)
                if capacity is not None and amount > capacity:
                    _add(
                        issues,
                        "storage-over-capacity",
                        f"resources.{resource.id}",
                        f"resident materializations use {amount:g} {dimension} at {coordinate:g}, capacity is {capacity:g}",
                    )

    check_storage(0)
    scratch_issues: list[ValidationIssue] = []
    for coordinate in sorted(end_stages):
        for stage in end_stages[coordinate]:
            for effect in stage.effects:
                _apply_effect(effect, state, scratch_issues, "storage-simulation")
        check_storage(coordinate)


def validate_draft_trace(trace: TraceDocument) -> ValidationReport:
    """Validate references, schedules, lifecycle, flows, and resource capacity."""

    issues: list[ValidationIssue] = []
    named_collections: list[tuple[str, Iterable[object]]] = [
        ("views", trace.views),
        ("places", trace.places),
        ("resources", trace.resources),
        ("links", trace.links),
        ("entities", trace.entities),
        ("operations", trace.operations),
        ("stages", trace.stages),
        ("flows", trace.flows),
        ("annotations", trace.annotations),
        ("checkpoints", trace.checkpoints),
    ]
    seen: dict[str, str] = {}
    for collection, values in named_collections:
        for index, value in enumerate(values):
            identifier = str(getattr(value, "id"))
            path = f"{collection}.{index}.id"
            if identifier in seen:
                _add(issues, "duplicate-id", path, f"{identifier!r} already used at {seen[identifier]}")
            else:
                seen[identifier] = path

    place_ids = {item.id for item in trace.places}
    resource_ids = {item.id for item in trace.resources}
    link_ids = {item.id for item in trace.links}
    entity_ids = {item.id for item in trace.entities}
    operation_ids = {item.id for item in trace.operations}
    stage_ids = {item.id for item in trace.stages}
    flow_ids = {item.id for item in trace.flows}
    checkpoint_ids = {item.id for item in trace.checkpoints}
    materialization_ids: set[str] = set()

    for index, item in enumerate(trace.initial_materializations):
        if item.id in seen or item.id in materialization_ids:
            conflict = seen.get(item.id, "an earlier initial materialization")
            _add(issues, "duplicate-id", f"initial_materializations.{index}.id", f"{item.id!r} conflicts with {conflict}")
        materialization_ids.add(item.id)
        _ref(issues, item.entity, entity_ids, f"initial_materializations.{index}.entity", "entity")
        _ref(issues, item.place, place_ids, f"initial_materializations.{index}.place", "place")

    place_graph = nx.DiGraph()
    place_graph.add_nodes_from(place_ids)
    for index, place in enumerate(trace.places):
        _ref(issues, place.parent, place_ids, f"places.{index}.parent", "place")
        if place.parent:
            place_graph.add_edge(place.parent, place.id)
    if not nx.is_directed_acyclic_graph(place_graph):
        _add(issues, "place-cycle", "places", "place hierarchy contains a cycle")

    for index, link in enumerate(trace.links):
        _ref(issues, link.from_place, place_ids, f"links.{index}.from", "place")
        _ref(issues, link.to_place, place_ids, f"links.{index}.to", "place")
        _ref(issues, link.resource, resource_ids, f"links.{index}.resource", "resource")
    for index, resource in enumerate(trace.resources):
        _ref(issues, resource.owner, place_ids | link_ids, f"resources.{index}.owner", "place or link")

    created_ids: set[str] = set()
    for index, stage in enumerate(trace.stages):
        _ref(issues, stage.operation, operation_ids, f"stages.{index}.operation", "operation")
        _ref(issues, stage.at, place_ids, f"stages.{index}.at", "place")
        _ref(issues, stage.link, link_ids, f"stages.{index}.link", "link")
        _ref(issues, stage.flow, flow_ids, f"stages.{index}.flow", "flow")
        for claim_index, claim in enumerate(stage.claims):
            _ref(issues, claim.resource, resource_ids, f"stages.{index}.claims.{claim_index}.resource", "resource")
            resource = next((item for item in trace.resources if item.id == claim.resource), None)
            if resource:
                for dimension in claim.amount:
                    if dimension not in resource.capacity:
                        _add(
                            issues,
                            "claim-dimension-mismatch",
                            f"stages.{index}.claims.{claim_index}.amount.{dimension}",
                            f"resource {resource.id!r} has no {dimension!r} capacity",
                        )
        for dependency in stage.after:
            _ref(issues, dependency, stage_ids, f"stages.{index}.after", "stage")
        for effect_index, effect in enumerate(stage.effects):
            path = f"stages.{index}.effects.{effect_index}"
            _ref(issues, effect.entity, entity_ids, f"{path}.entity", "entity")
            _ref(issues, effect.place, place_ids, f"{path}.place", "place")
            if effect.action == "create":
                if effect.materialization in materialization_ids | created_ids:
                    _add(issues, "duplicate-materialization", path, f"materialization {effect.materialization!r} is created more than once")
                created_ids.add(effect.materialization)

        if trace.time.mode == "timeline":
            if stage.start is None or stage.duration is None or stage.step is not None:
                _add(issues, "invalid-timing", f"stages.{index}", "timeline stages require start and duration only")
        elif stage.step is None or stage.start is not None or stage.duration is not None:
            _add(issues, "invalid-timing", f"stages.{index}", "step stages require step only")

    all_materializations = materialization_ids | created_ids
    all_semantic_ids = (
        place_ids
        | resource_ids
        | link_ids
        | entity_ids
        | operation_ids
        | stage_ids
        | flow_ids
        | all_materializations
    )
    for index, stage in enumerate(trace.stages):
        correspondence = stage.attrs.get("corresponds_to")
        if correspondence is None:
            continue
        if not isinstance(correspondence, list) or not all(
            isinstance(identifier, str) for identifier in correspondence
        ):
            _add(
                issues,
                "invalid-correspondence",
                f"stages.{index}.attrs.corresponds_to",
                "corresponds_to must be a list of semantic IDs",
            )
            continue
        for identifier in correspondence:
            _ref(
                issues,
                identifier,
                all_semantic_ids,
                f"stages.{index}.attrs.corresponds_to",
                "correspondence target",
            )
    for index, flow in enumerate(trace.flows):
        _ref(issues, flow.entity, entity_ids, f"flows.{index}.entity", "entity")
        for stage_id in flow.stages:
            _ref(issues, stage_id, stage_ids, f"flows.{index}.stages", "stage")
            stage = next((item for item in trace.stages if item.id == stage_id), None)
            if stage is not None and stage.flow != flow.id:
                _add(
                    issues,
                    "flow-membership-mismatch",
                    f"flows.{index}.stages",
                    f"stage {stage_id!r} belongs to {stage.flow!r}, not {flow.id!r}",
                )
    flow_by_id = {item.id: item for item in trace.flows}
    for index, stage in enumerate(trace.stages):
        if stage.flow and stage.flow in flow_by_id and stage.id not in flow_by_id[stage.flow].stages:
            _add(
                issues,
                "flow-membership-mismatch",
                f"stages.{index}.flow",
                f"flow {stage.flow!r} does not include stage {stage.id!r}",
            )
    for index, checkpoint in enumerate(trace.checkpoints):
        if trace.time.mode == "timeline" and checkpoint.at is None:
            _add(issues, "invalid-checkpoint", f"checkpoints.{index}", "timeline checkpoint requires at")
        if trace.time.mode == "steps" and checkpoint.step is None:
            _add(issues, "invalid-checkpoint", f"checkpoints.{index}", "step checkpoint requires step")
        for focus in checkpoint.focus:
            _ref(issues, focus, all_semantic_ids, f"checkpoints.{index}.focus", "semantic entity")
    for index, annotation in enumerate(trace.annotations):
        _ref(issues, annotation.anchor, all_semantic_ids, f"annotations.{index}.anchor", "semantic anchor")
        _ref(issues, annotation.checkpoint, checkpoint_ids, f"annotations.{index}.checkpoint", "checkpoint")

    for index, view in enumerate(resolved_views(trace)):
        prefix = f"views.{index}" if trace.views else "view"
        for field_name, values, allowed in (
            ("roots", view.roots, place_ids),
            ("draggable", view.draggable, place_ids),
            ("resources", view.resources, resource_ids),
            ("importance", view.importance, all_semantic_ids),
        ):
            for value in values:
                _ref(issues, value, allowed, f"{prefix}.{field_name}", field_name)

    dependency_graph = nx.DiGraph()
    dependency_graph.add_nodes_from(stage_ids)
    stage_by_id = {item.id: item for item in trace.stages}
    for stage in trace.stages:
        for dependency in stage.after:
            dependency_graph.add_edge(dependency, stage.id)
            if dependency in stage_by_id:
                predecessor_end = _coordinates(trace, stage_by_id[dependency])[1]
                stage_start = _coordinates(trace, stage)[0]
                if predecessor_end > stage_start + 1e-9:
                    _add(
                        issues,
                        "dependency-time-conflict",
                        f"stages.{stage.id}.after",
                        f"dependency {dependency!r} finishes at {predecessor_end:g}, after this stage starts at {stage_start:g}",
                    )
    if not nx.is_directed_acyclic_graph(dependency_graph):
        _add(issues, "dependency-cycle", "stages", "stage dependencies contain a cycle")

    if not issues or not any(issue.code == "invalid-timing" for issue in issues):
        _validate_lifecycle(trace, issues)
        _validate_capacities(trace, issues)
    return ValidationReport(tuple(issues))
