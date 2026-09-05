from __future__ import annotations

from pathlib import Path

from sviz import compile_trace, load_trace, validate_trace
from sviz.server import component_source


ROOT = Path(__file__).parents[1]
EXAMPLE = ROOT / "examples" / "deepep_vnext.yaml"


def _compiled() -> dict:
    return compile_trace(load_trace(EXAMPLE))


def _checkpoint(compiled: dict, checkpoint_id: str) -> dict:
    return next(item for item in compiled["execution"]["checkpoints"] if item["id"] == checkpoint_id)


def _view(compiled: dict, identifier: str) -> dict:
    return next(view for view in compiled["display"]["views"] if view["id"] == identifier)


def _materialization_ids(checkpoint: dict) -> set[str]:
    return {item["id"] for item in checkpoint["materializations"]}


def _ledger(checkpoint: dict, resource_id: str) -> dict:
    return next(item for item in checkpoint["resource_ledgers"] if item["resource"] == resource_id)


def test_deepep_validates_without_warnings() -> None:
    report = validate_trace(load_trace(EXAMPLE))

    assert report.ok, "\n".join(str(issue) for issue in report.issues)
    assert not report.warnings


def test_deepep_compilation_is_deterministic_and_domain_neutral() -> None:
    first = _compiled()

    assert first == _compiled()
    assert len(first["execution"]["events"]) == 12
    assert len(first["execution"]["checkpoints"]) == 9
    assert len(_view(first, "timeline")["marks"]) == 34
    assert _view(first, "system")["roots"] == ["rank0", "rank1", "rank2", "rank3"]
    assert [lane["id"] for lane in _view(first, "timeline")["lanes"]] == [
        "route_layout",
        "nvlink_bw",
        "rdma_bw",
        "expert_compute",
        "combine_work",
    ]


def test_dispatch_fanout_preserves_origins_and_creates_eight_expert_copies() -> None:
    grouped = _checkpoint(_compiled(), "grouped")
    ids = _materialization_ids(grouped)

    assert {"t0.origin", "t1.origin", "t2.origin", "t3.origin"} <= ids
    assert {
        "t0.e0",
        "t0.e2",
        "t1.e1",
        "t1.e3",
        "t2.e0",
        "t2.e2",
        "t3.e1",
        "t3.e3",
    } <= ids
    assert "t1.rail2" not in ids
    assert "t3.rail0" not in ids


def test_forwarding_and_shared_route_capacity_are_explicit() -> None:
    compiled = _compiled()
    dispatch = _checkpoint(compiled, "dispatch")
    forwarding = _checkpoint(compiled, "forwarding")
    reverse = _checkpoint(compiled, "reverse_forward")

    assert _ledger(dispatch, "rdma_bw")["used"] == {"channels": 4.0}
    assert set(forwarding["active_stages"]) == {"dispatch_t1_e3", "dispatch_t3_e1"}
    assert {"t1.rail2", "t3.rail0"} <= _materialization_ids(forwarding)
    assert _ledger(reverse, "rdma_bw")["used"] == {"channels": 4.0}
    assert set(reverse["active_stages"]) == {
        "return_o0_e2",
        "return_o2_e0",
        "return_o1_origin",
        "return_o3_origin",
    }


def test_experts_run_in_parallel_with_live_routing_handles() -> None:
    experts = _checkpoint(_compiled(), "experts")

    assert set(experts["active_stages"]) == {
        "expert0_compute",
        "expert1_compute",
        "expert2_compute",
        "expert3_compute",
    }
    assert _ledger(experts, "expert_compute")["used"] == {"slots": 4.0}
    assert {"handle0.ready", "handle1.ready", "handle2.ready", "handle3.ready"} <= _materialization_ids(experts)


def test_combine_retires_route_state_and_leaves_one_output_per_token() -> None:
    done = _checkpoint(_compiled(), "done")

    assert _materialization_ids(done) == {
        "expert0.resident",
        "expert1.resident",
        "expert2.resident",
        "expert3.resident",
        "o0.final",
        "o1.final",
        "o2.final",
        "o3.final",
    }
    outputs = [item for item in done["materializations"] if item["id"].endswith(".final")]
    assert all(item["quantity"] == {"tokens": 1.0, "bytes": 7168.0} for item in outputs)


def test_renderer_groups_shared_link_motion_without_workload_branches() -> None:
    source = component_source().lower()

    assert "data-active-transfer-count" in source
    assert "concurrent transfers" in source
    assert "manual_edge_offsets" in source
    assert "adjust edge routes" in source
    assert "deepep" not in source
    assert "expert-dispatch" not in source
