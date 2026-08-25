from __future__ import annotations

from pathlib import Path

from sviz import compile_trace, load_trace, validate_trace


ROOT = Path(__file__).parents[1]
EXAMPLE = ROOT / "examples" / "torch_all_to_all_single_vnext.yaml"
SYNC_MODE = ROOT / "examples" / "torch_all_to_all_sync_vnext.yaml"
ASYNC_MODE = ROOT / "examples" / "torch_all_to_all_async_shared_expert_vnext.yaml"


def _checkpoint(compiled: dict, checkpoint_id: str) -> dict:
    return next(
        item
        for item in compiled["execution"]["checkpoints"]
        if item["id"] == checkpoint_id
    )


def test_all_to_all_single_example_validates_without_warnings() -> None:
    report = validate_trace(load_trace(EXAMPLE))

    assert report.ok, "\n".join(str(issue) for issue in report.issues)
    assert not report.warnings


def test_sync_mode_isolated_trace_exposes_nccl_and_current_stream_wait() -> None:
    trace = load_trace(SYNC_MODE)
    report = validate_trace(trace)
    compiled = compile_trace(trace)
    overlap = _checkpoint(compiled, "sync_overlap")

    assert report.ok, "\n".join(str(issue) for issue in report.issues)
    assert not report.warnings
    assert {place.id for place in trace.places if place.parent == "sync_stream_pool"} == {
        "sync_current",
        "sync_nccl",
        "sync_shared",
    }
    assert set(overlap["active_stages"]) == {
        "sync_comm",
        "sync_current_wait",
        "sync_shared_expert_fc1",
    }
    assert [lane["id"] for lane in compiled["display"]["timeline"]["lanes"]] == [
        "sync_host_thread",
        "sync_current_stream",
        "sync_nccl_stream",
        "sync_shared_expert_stream",
        "sync_transport",
    ]


def test_async_mode_isolated_trace_exposes_shared_expert_overlap() -> None:
    trace = load_trace(ASYNC_MODE)
    report = validate_trace(trace)
    compiled = compile_trace(trace)
    overlap = _checkpoint(compiled, "async_overlap")
    join = _checkpoint(compiled, "async_join")

    assert report.ok, "\n".join(str(issue) for issue in report.issues)
    assert not report.warnings
    assert {place.id for place in trace.places if place.parent == "async_stream_pool"} == {
        "async_current",
        "async_nccl",
        "async_shared",
    }
    assert set(overlap["active_stages"]) == {
        "async_comm",
        "async_shared_expert_fc1",
        "async_current_model_work",
    }
    assert set(join["active_stages"]) == {"async_comm", "async_current_wait"}
    assert [lane["id"] for lane in compiled["display"]["timeline"]["lanes"]] == [
        "async_host_thread",
        "async_current_stream",
        "async_nccl_stream",
        "async_shared_expert_stream",
        "async_transport",
    ]


def test_all_to_all_single_compiles_control_path_and_grouped_exchange() -> None:
    compiled = compile_trace(load_trace(EXAMPLE))
    count_exchange = _checkpoint(compiled, "count_exchange")
    d2h = _checkpoint(compiled, "d2h")
    host_counts = _checkpoint(compiled, "host_counts")
    grouped = _checkpoint(compiled, "grouped_exchange")
    outputs = _checkpoint(compiled, "outputs")

    assert count_exchange["active_stages"] == ["exchange_counts"]
    assert set(d2h["active_stages"]) == {"d2h_counts0", "d2h_counts1"}
    assert set(host_counts["active_stages"]) == {"host_sync0", "host_sync1"}
    assert set(grouped["active_stages"]) == {
        "nccl_group0",
        "nccl_group1",
        "independent_compute0",
        "independent_compute1",
    }

    by_id = {item["id"]: item for item in outputs["materializations"]}
    assert {
        "chunk00.r0_input",
        "chunk01.r0_input",
        "chunk10.r1_input",
        "chunk11.r1_input",
    } <= by_id.keys()
    assert (
        by_id["chunk00.r0_output"]["place"],
        by_id["chunk00.r0_output"]["provenance"],
        by_id["chunk00.r0_output"]["attrs"]["output_offset"],
    ) == ("rank0_output", "chunk00.r0_input", 0)
    assert (
        by_id["chunk10.r0_output"]["place"],
        by_id["chunk10.r0_output"]["provenance"],
        by_id["chunk10.r0_output"]["attrs"]["output_offset"],
    ) == ("rank0_output", "chunk10.r1_input", 1)
    assert (
        by_id["chunk01.r1_output"]["place"],
        by_id["chunk01.r1_output"]["provenance"],
        by_id["chunk01.r1_output"]["attrs"]["output_offset"],
    ) == ("rank1_output", "chunk01.r0_input", 0)
    assert (
        by_id["chunk11.r1_output"]["place"],
        by_id["chunk11.r1_output"]["provenance"],
        by_id["chunk11.r1_output"]["attrs"]["output_offset"],
    ) == ("rank1_output", "chunk11.r1_input", 3)
