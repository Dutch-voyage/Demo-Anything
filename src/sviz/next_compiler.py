"""Compile the draft semantic IR into deterministic execution and display plans."""

from __future__ import annotations

from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from typing import Any

from .next_models import DraftEffect, DraftStage, TraceDocument
from .next_validation import validate_draft_trace


def _coordinate(trace: TraceDocument, stage: DraftStage) -> tuple[float, float]:
    if trace.time.mode == "timeline":
        assert stage.start is not None and stage.duration is not None
        return round(stage.start, 9), round(stage.start + stage.duration, 9)
    assert stage.step is not None
    return float(stage.step), float(stage.step + 1)


def _checkpoint_coordinate(trace: TraceDocument, checkpoint: Any) -> float:
    return float(checkpoint.at if trace.time.mode == "timeline" else checkpoint.step)


def _apply(effect: DraftEffect, state: dict[str, dict[str, Any]]) -> None:
    if effect.action == "create":
        state[effect.materialization] = {
            "id": effect.materialization,
            "entity": effect.entity,
            "place": effect.place,
            "provenance": effect.from_materialization,
            "updates": 0,
            "attrs": dict(effect.attrs),
        }
    elif effect.action == "retire":
        state.pop(effect.materialization, None)
    elif effect.action == "place" and effect.materialization in state:
        state[effect.materialization]["place"] = effect.place
    elif effect.action == "unplace" and effect.materialization in state:
        state[effect.materialization]["place"] = None
    elif effect.action == "update" and effect.materialization in state:
        state[effect.materialization]["updates"] += 1
        state[effect.materialization]["attrs"].update(effect.attrs)
        if effect.write:
            state[effect.materialization]["last_write"] = effect.write
    elif effect.action == "relate" and effect.materialization in state:
        state[effect.materialization].setdefault("relations", []).append(
            {"to": effect.to, "kind": effect.relation}
        )


def _initial_state(trace: TraceDocument) -> dict[str, dict[str, Any]]:
    return {
        item.id: {
            "id": item.id,
            "entity": item.entity,
            "place": item.place,
            "provenance": None,
            "updates": 0,
            "attrs": dict(item.attrs),
        }
        for item in trace.initial_materializations
    }


def _state_at(trace: TraceDocument, cursor: float) -> dict[str, dict[str, Any]]:
    state = _initial_state(trace)
    completed = sorted(
        (stage for stage in trace.stages if _coordinate(trace, stage)[1] <= cursor),
        key=lambda stage: (_coordinate(trace, stage)[1], _coordinate(trace, stage)[0], stage.id),
    )
    for stage in completed:
        for effect in stage.effects:
            _apply(effect, state)
    return state


def _children(trace: TraceDocument) -> dict[str, list[str]]:
    result: dict[str, list[str]] = defaultdict(list)
    for place in trace.places:
        if place.parent:
            result[place.parent].append(place.id)
    return dict(result)


def _descendants(children: dict[str, list[str]], owner: str) -> set[str]:
    result = {owner}
    pending = [owner]
    while pending:
        current = pending.pop()
        for child in children.get(current, []):
            if child not in result:
                result.add(child)
                pending.append(child)
    return result


def _resource_ledgers(
    trace: TraceDocument,
    state: dict[str, dict[str, Any]],
    active: list[DraftStage],
) -> list[dict[str, Any]]:
    entity_by_id = {item.id: item for item in trace.entities}
    children = _children(trace)
    ledgers: list[dict[str, Any]] = []
    for resource in trace.resources:
        used: dict[str, float] = defaultdict(float)
        owners: list[str] = []
        if resource.kind == "storage":
            owned_places = _descendants(children, resource.owner)
            for materialization in state.values():
                if materialization.get("place") not in owned_places:
                    continue
                entity = entity_by_id[str(materialization["entity"])]
                for dimension, amount in entity.quantity.items():
                    used[dimension] += amount
                owners.append(str(materialization["id"]))
        else:
            for stage in active:
                for claim in stage.claims:
                    if claim.resource != resource.id:
                        continue
                    for dimension, amount in claim.amount.items():
                        used[dimension] += amount
                    owners.append(stage.id)
        ledgers.append(
            {
                "resource": resource.id,
                "label": resource.label or resource.id,
                "kind": resource.kind,
                "owner": resource.owner,
                "used": dict(used),
                "capacity": dict(resource.capacity),
                "owners": owners,
            }
        )
    return ledgers


def _event_tape(trace: TraceDocument) -> list[dict[str, Any]]:
    points = sorted({value for stage in trace.stages for value in _coordinate(trace, stage)})
    result: list[dict[str, Any]] = []
    for point in points:
        started = [stage.id for stage in trace.stages if _coordinate(trace, stage)[0] == point]
        finished = [stage.id for stage in trace.stages if _coordinate(trace, stage)[1] == point]
        effects = [
            {"stage": stage.id, **effect.model_dump(by_alias=True, exclude_none=True, mode="json")}
            for stage in trace.stages
            if _coordinate(trace, stage)[1] == point
            for effect in stage.effects
        ]
        result.append({"cursor": point, "started": started, "finished": finished, "effects": effects})
    return result


def _geometry(trace: TraceDocument) -> dict[str, Any]:
    children = _children(trace)
    roots = trace.view.system_roots

    wide_width = 1000.0
    route_slots_per_side = max(1, (len(trace.links) + 1) // 2)
    edge_band = max(76.0, 24.0 + route_slots_per_side * 32.0)
    root_height = 360.0
    wide_height = root_height + edge_band * 2.0
    gap = 20.0
    root_width = (wide_width - 40.0 - gap * (len(roots) - 1)) / max(1, len(roots))
    wide: dict[str, dict[str, float]] = {}
    for index, root in enumerate(roots):
        box = {"x": 20.0 + index * (root_width + gap), "y": edge_band, "w": root_width, "h": root_height}
        wide[root] = box
        nested = children.get(root, [])
        if nested:
            nested_gap = 10.0
            nested_height = (box["h"] - 62.0 - nested_gap * (len(nested) - 1)) / len(nested)
            for child_index, child in enumerate(nested):
                wide[child] = {
                    "x": box["x"] + 12.0,
                    "y": box["y"] + 44.0 + child_index * (nested_height + nested_gap),
                    "w": box["w"] - 24.0,
                    "h": nested_height,
                }

    narrow_width = 360.0
    narrow_side_band = min(80.0, max(28.0, 16.0 + route_slots_per_side * 18.0))
    narrow: dict[str, dict[str, float]] = {}
    y = 28.0
    for root in roots:
        nested = children.get(root, [])
        height = 188.0 if nested else 138.0
        # Keep an edge channel on both sides. Obstacle-aware routes use this
        # space when a direct connection would cross an intermediate place.
        box = {"x": narrow_side_band, "y": y, "w": narrow_width - narrow_side_band * 2.0, "h": height}
        narrow[root] = box
        if nested:
            nested_gap = 7.0
            nested_width = (box["w"] - 24.0 - nested_gap * (len(nested) - 1)) / len(nested)
            for child_index, child in enumerate(nested):
                narrow[child] = {
                    "x": box["x"] + 12.0 + child_index * (nested_width + nested_gap),
                    "y": box["y"] + 43.0,
                    "w": nested_width,
                    "h": box["h"] - 56.0,
                }
        y += height + 14.0

    return {
        "wide": {"canvas": {"width": wide_width, "height": wide_height}, "places": wide},
        "narrow": {"canvas": {"width": narrow_width, "height": y + 2.0}, "places": narrow},
    }


def _visible_root(place: str, roots: list[str], place_by_id: dict[str, Any]) -> str:
    current = place
    while current not in roots:
        parent = place_by_id[current].parent
        if parent is None:
            return current
        current = parent
    return current


def _display_plan(trace: TraceDocument) -> dict[str, Any]:
    place_by_id = {item.id: item for item in trace.places}
    resource_by_id = {item.id: item for item in trace.resources}
    roots = trace.view.system_roots
    children = _children(trace)
    visible_places = set(roots)
    for root in roots:
        visible_places.update(_descendants(children, root))

    system_places = [
        {
            "id": place.id,
            "label": place.label or place.id,
            "parent": place.parent,
            "role": place.role,
            "layout": place.layout,
        }
        for place in trace.places
        if place.id in visible_places
    ]
    routes = []
    for link in trace.links:
        if link.from_place not in place_by_id or link.to_place not in place_by_id:
            continue
        routes.append(
            {
                "id": link.id,
                "label": link.label or link.id,
                "from": _visible_root(link.from_place, roots, place_by_id),
                "to": _visible_root(link.to_place, roots, place_by_id),
                "directed": link.directed,
                "resource": link.resource,
            }
        )

    lanes = []
    for resource_id in trace.view.timeline_resources:
        resource = resource_by_id[resource_id]
        lanes.append(
            {
                "id": resource.id,
                "label": resource.label or resource.id,
                "kind": resource.kind,
                "owner": resource.owner,
            }
        )
    marks = []
    for stage in trace.stages:
        start, end = _coordinate(trace, stage)
        lane = next(
            (claim.resource for claim in stage.claims if claim.resource in trace.view.timeline_resources),
            stage.claims[0].resource if stage.claims else stage.at or "global",
        )
        marks.append(
            {
                "id": stage.id,
                "label": stage.label or stage.id,
                "operation": stage.operation,
                "kind": stage.kind,
                "lane": lane,
                "start": start,
                "end": end,
                "at": stage.at,
                "link": stage.link,
                "flow": stage.flow,
            }
        )

    # Pack overlapping intervals on the same semantic lane into deterministic
    # visual tracks. The renderer receives the decision instead of hiding
    # concurrent marks or inferring workload-specific grouping.
    track_ends: dict[str, list[float]] = defaultdict(list)
    for mark in sorted(marks, key=lambda item: (item["lane"], item["start"], item["end"], item["id"])):
        lane_tracks = track_ends[mark["lane"]]
        track = next(
            (index for index, previous_end in enumerate(lane_tracks) if previous_end <= mark["start"]),
            len(lane_tracks),
        )
        if track == len(lane_tracks):
            lane_tracks.append(mark["end"])
        else:
            lane_tracks[track] = mark["end"]
        mark["track"] = track
    for lane in lanes:
        lane["tracks"] = max(1, len(track_ends.get(lane["id"], [])))

    return {
        "system": {
            "roots": roots,
            "draggable": trace.view.draggable,
            "places": system_places,
            "children": children,
            "routes": routes,
            "geometry": _geometry(trace),
        },
        "timeline": {
            "lanes": lanes,
            "marks": marks,
            "start": min(0, min((mark["start"] for mark in marks), default=0)),
            "end": max((mark["end"] for mark in marks), default=0),
            "unit": trace.time.unit or "step",
        },
    }


def compile_draft_trace(trace: TraceDocument) -> dict[str, Any]:
    """Compile the vNext semantic document into renderer-ready JSON."""

    report = validate_draft_trace(trace)
    report.raise_for_errors()

    entity_by_id = {item.id: item for item in trace.entities}
    stage_by_id = {item.id: item for item in trace.stages}
    previous_state = _initial_state(trace)
    snapshots: list[dict[str, Any]] = []
    for checkpoint in sorted(trace.checkpoints, key=lambda item: _checkpoint_coordinate(trace, item)):
        cursor = _checkpoint_coordinate(trace, checkpoint)
        state = _state_at(trace, cursor)
        active = [
            stage for stage in trace.stages if _coordinate(trace, stage)[0] <= cursor < _coordinate(trace, stage)[1]
        ]
        previous_ids = set(previous_state)
        current_ids = set(state)
        changed = [
            identifier
            for identifier in current_ids & previous_ids
            if state[identifier].get("updates") != previous_state[identifier].get("updates")
        ]
        materializations = []
        for item in sorted(state.values(), key=lambda value: str(value["id"])):
            entity = entity_by_id[str(item["entity"])]
            materializations.append(
                {
                    **deepcopy(item),
                    "label": entity.label or entity.id,
                    "kind": entity.kind,
                    "quantity": dict(entity.quantity),
                }
            )
        snapshots.append(
            {
                "id": checkpoint.id,
                "cursor": cursor,
                "title": checkpoint.label or checkpoint.id,
                "detail": checkpoint.detail,
                "narrative": checkpoint.narrative if checkpoint.narrative is not None else checkpoint.detail or "",
                "focus": checkpoint.focus,
                "active_stages": [stage.id for stage in active],
                "active_flows": sorted({stage.flow for stage in active if stage.flow}),
                "materializations": materializations,
                "resource_ledgers": _resource_ledgers(trace, state, active),
                "changes": {
                    "created": sorted(current_ids - previous_ids),
                    "retired": sorted(previous_ids - current_ids),
                    "updated": sorted(changed),
                },
            }
        )
        previous_state = state

    source = trace.model_dump(by_alias=True, exclude_none=True, mode="json")
    base_revision = "sha256:" + hashlib.sha256(
        json.dumps(source, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()

    return {
        "format": "sviz-display",
        "format_version": "0.2-draft",
        "visualization_id": trace.id,
        "base_revision": base_revision,
        "title": trace.title,
        "description": trace.description,
        "source": source,
        "semantic": {
            "places": [item.model_dump(by_alias=True, exclude_none=True, mode="json") for item in trace.places],
            "resources": [item.model_dump(by_alias=True, exclude_none=True, mode="json") for item in trace.resources],
            "links": [item.model_dump(by_alias=True, exclude_none=True, mode="json") for item in trace.links],
            "entities": [item.model_dump(by_alias=True, exclude_none=True, mode="json") for item in trace.entities],
            "operations": [item.model_dump(by_alias=True, exclude_none=True, mode="json") for item in trace.operations],
            "stages": [item.model_dump(by_alias=True, exclude_none=True, mode="json") for item in trace.stages],
            "flows": [item.model_dump(by_alias=True, exclude_none=True, mode="json") for item in trace.flows],
            "stage_index": {
                identifier: stage.model_dump(by_alias=True, exclude_none=True, mode="json")
                for identifier, stage in stage_by_id.items()
            },
        },
        "content": {
            "annotations": [
                {
                    "id": annotation.id,
                    "title": annotation.label or annotation.id,
                    "body": annotation.body,
                    "anchor": annotation.anchor,
                    "checkpoint": annotation.checkpoint,
                    "status": annotation.status,
                    "origin": "authored",
                }
                for annotation in trace.annotations
            ],
        },
        "execution": {
            "mode": trace.time.mode,
            "unit": trace.time.unit,
            "events": _event_tape(trace),
            "checkpoints": snapshots,
        },
        "display": _display_plan(trace),
        "warnings": [
            {"code": issue.code, "path": issue.path, "message": issue.message}
            for issue in report.warnings
        ],
    }
