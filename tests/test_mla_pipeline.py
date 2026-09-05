from __future__ import annotations

from pathlib import Path

from sviz import compile_trace, load_trace, validate_trace
from sviz.server import component_source


ROOT = Path(__file__).parents[1]
PREFILL = ROOT / "examples" / "mla_prefill_vnext.yaml"
DECODE = ROOT / "examples" / "mla_decode_vnext.yaml"


def _compiled(path: Path) -> dict:
    return compile_trace(load_trace(path))


def _checkpoint(compiled: dict, checkpoint_id: str) -> dict:
    return next(item for item in compiled["execution"]["checkpoints"] if item["id"] == checkpoint_id)


def _view(compiled: dict, identifier: str) -> dict:
    return next(view for view in compiled["display"]["views"] if view["id"] == identifier)


def _materializations(checkpoint: dict) -> dict[str, dict]:
    return {item["id"]: item for item in checkpoint["materializations"]}


def _ledger(checkpoint: dict, resource_id: str) -> dict:
    return next(item for item in checkpoint["resource_ledgers"] if item["resource"] == resource_id)


def test_both_mla_examples_validate_without_warnings() -> None:
    for path in (PREFILL, DECODE):
        report = validate_trace(load_trace(path))
        assert report.ok, f"{path.name}:\n" + "\n".join(str(issue) for issue in report.issues)
        assert not report.warnings


def test_mla_examples_use_step_mode_and_shared_display_structure() -> None:
    prefill = _compiled(PREFILL)
    decode = _compiled(DECODE)

    assert prefill == _compiled(PREFILL)
    assert decode == _compiled(DECODE)
    assert prefill["execution"]["mode"] == decode["execution"]["mode"] == "steps"
    assert len(prefill["execution"]["checkpoints"]) == 8
    assert len(decode["execution"]["checkpoints"]) == 8
    assert len(_view(prefill, "timeline")["marks"]) == 10
    assert len(_view(decode, "timeline")["marks"]) == 10
    assert _view(prefill, "system")["roots"] == _view(decode, "system")["roots"] == [
        "input",
        "projection",
        "cache",
        "attention",
    ]
    expected_lanes = [
        "projection_compute",
        "cache_write",
        "score_compute",
        "softmax_pipe",
        "latent_reduce",
        "output_projection",
    ]
    assert [lane["id"] for lane in _view(prefill, "timeline")["lanes"]] == expected_lanes
    assert [lane["id"] for lane in _view(decode, "timeline")["lanes"]] == expected_lanes
    prefill_lanes = {lane["id"]: lane for lane in _view(prefill, "timeline")["lanes"]}
    assert prefill_lanes["projection_compute"]["tracks"] == 2
    assert prefill_lanes["cache_write"]["tracks"] == 2
    assert prefill_lanes["score_compute"]["tracks"] == 2


def test_concurrent_mla_marks_receive_distinct_timeline_tracks() -> None:
    for compiled in (_compiled(PREFILL), _compiled(DECODE)):
        marks = {item["id"]: item for item in _view(compiled, "timeline")["marks"]}
        assert marks[next(key for key in marks if key.startswith("project_") and "query" in key)]["track"] != marks[
            next(key for key in marks if key.startswith("compress_"))
        ]["track"]
        cache_marks = [item for item in marks.values() if item["lane"] == "cache_write"]
        assert {item["track"] for item in cache_marks} == {0, 1}


def test_prefill_projects_four_tokens_in_parallel_and_builds_two_cache_parts() -> None:
    compiled = _compiled(PREFILL)
    project = _checkpoint(compiled, "project")
    score = _checkpoint(compiled, "score")
    items = _materializations(score)

    assert set(project["active_stages"]) == {"project_prompt_query", "compress_prompt_kv"}
    assert _ledger(project, "projection_compute")["used"] == {"slots": 2.0}
    assert set(score["active_stages"]) == {"score_prompt_content", "score_prompt_position"}
    assert items["prompt.latent.cache"]["provenance"] == "prompt.latent.work"
    assert items["prompt.rope.cache"]["provenance"] == "prompt.rope.work"
    assert _ledger(score, "cache_bytes")["used"] == {"bytes": 4608.0}


def test_prefill_never_materializes_full_keys_or_values_and_leaves_decode_state() -> None:
    compiled = _compiled(PREFILL)
    entity_kinds = {item["kind"] for item in compiled["semantic"]["entities"]}
    done = _materializations(_checkpoint(compiled, "ready_for_decode"))

    assert "full-key-batch" not in entity_kinds
    assert "full-value-batch" not in entity_kinds
    assert set(done) == {"prompt.latent.cache", "prompt.rope.cache", "prompt.output"}
    assert done["prompt.latent.cache"]["quantity"] == {"bytes": 4096.0}
    assert done["prompt.rope.cache"]["quantity"] == {"bytes": 512.0}


def test_decode_appends_one_token_without_replacing_the_prefix() -> None:
    compiled = _compiled(DECODE)
    initial = _checkpoint(compiled, "prefix_ready")
    score = _checkpoint(compiled, "score_prefix")
    initial_items = _materializations(initial)
    score_items = _materializations(score)

    assert set(initial_items) == {"prefix.latent.cache", "prefix.rope.cache", "token4.input"}
    assert _ledger(initial, "cache_bytes")["used"] == {"bytes": 4608.0}
    assert {
        "prefix.latent.cache",
        "prefix.rope.cache",
        "token4.latent.cache",
        "token4.rope.cache",
    } <= set(score_items)
    assert score_items["token4.latent.cache"]["provenance"] == "token4.latent.work"
    assert score_items["token4.rope.cache"]["provenance"] == "token4.rope.work"
    assert _ledger(score, "cache_bytes")["used"] == {"bytes": 5760.0}


def test_decode_scores_and_reduces_directly_over_the_compressed_cache() -> None:
    compiled = _compiled(DECODE)
    score = _checkpoint(compiled, "score_prefix")
    reduce = _checkpoint(compiled, "reduce_latent")
    done = _materializations(_checkpoint(compiled, "next_token_ready"))

    assert set(score["active_stages"]) == {"score_decode_content", "score_decode_position"}
    assert reduce["active_stages"] == ["reduce_decode_latents"]
    assert set(done) == {
        "prefix.latent.cache",
        "prefix.rope.cache",
        "token4.latent.cache",
        "token4.rope.cache",
        "token4.output",
    }
    assert _ledger(_checkpoint(compiled, "next_token_ready"), "cache_bytes")["used"] == {
        "bytes": 5760.0
    }


def test_checkpoint_narrative_and_pinned_annotations_compile_as_content() -> None:
    compiled = _compiled(DECODE)
    score = _checkpoint(compiled, "score_prefix")
    annotations = {item["id"]: item for item in compiled["content"]["annotations"]}

    assert score["narrative"].startswith("## Read the compressed prefix directly")
    assert "**two score terms**" in score["narrative"]
    assert annotations["compressed-cache-question"] == {
        "id": "compressed-cache-question",
        "title": "Verify the cache representation",
        "body": "Does this step ever reconstruct a full per-head key or value tensor?",
        "anchor": "prefix.latent.cache",
            "checkpoint": "score_prefix",
            "status": "unresolved",
            "origin": "authored",
        }
    assert annotations["absorbed-score-note"]["status"] == "resolved"


def test_annotation_references_are_validated() -> None:
    trace = load_trace(DECODE)
    annotation = trace.annotations[0].model_copy(update={"anchor": "missing.anchor", "checkpoint": "missing-checkpoint"})
    invalid = trace.model_copy(update={"annotations": [annotation, *trace.annotations[1:]]})

    issues = validate_trace(invalid).errors
    assert {issue.path for issue in issues if issue.code == "unknown-reference"} >= {
        "annotations.0.anchor",
        "annotations.0.checkpoint",
    }


def test_renderer_supports_markdown_editing_and_annotation_state_events() -> None:
    source = component_source()

    assert "renderMarkdown" in source
    assert "data-narrative-input" in source
    assert 'CustomEvent("narrative-change"' in source
    assert "data-anchor-target" in source
    assert "data-pin-selection" in source
    assert 'role="switch"' in source
    assert "data-delete-annotation" in source
    assert 'emitAnnotationChange("delete", annotation)' in source
    assert 'CustomEvent("annotation-change"' in source


def test_renderer_contains_no_mla_specific_logic() -> None:
    source = component_source().lower()

    for workload_term in ("multi-head latent", "deepseek", "prefill", "decode", "ckv", "rope"):
        assert workload_term not in source
