from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient
from typer.testing import CliRunner

from sviz import compile_trace, export_trace, load_trace, validate_trace
from sviz.cli import app
from sviz.models import TraceDocument, ViewerState
from sviz.server import component_source, create_app


ROOT = Path(__file__).parents[1]
EXAMPLE = ROOT / "examples" / "flash_attention_vnext.yaml"


def _compiled() -> dict:
    return compile_trace(load_trace(EXAMPLE))


def _checkpoint(compiled: dict, checkpoint_id: str) -> dict:
    return next(item for item in compiled["execution"]["checkpoints"] if item["id"] == checkpoint_id)


def test_flash_attention_validates_without_warnings() -> None:
    report = validate_trace(load_trace(EXAMPLE))

    assert report.ok, "\n".join(str(issue) for issue in report.issues)
    assert not report.warnings


def test_checked_in_schema_matches_models() -> None:
    expected = TraceDocument.model_json_schema(by_alias=True)
    checked_in = json.loads((ROOT / "schema" / "sviz-0.2-draft.schema.json").read_text())

    assert checked_in == expected


def test_checked_in_viewer_state_schema_matches_models() -> None:
    expected = ViewerState.model_json_schema()
    checked_in = json.loads((ROOT / "schema" / "sviz-viewer-state-0.1.schema.json").read_text())

    assert checked_in == expected


def test_compiler_builds_deterministic_execution_and_display_plans() -> None:
    first = _compiled()
    second = _compiled()

    assert first == second
    assert first["format"] == "sviz-display"
    assert first["format_version"] == "0.2-draft"
    assert first["visualization_id"] == "flash-attention-v2-tile"
    assert first["base_revision"].startswith("sha256:")
    assert len(first["execution"]["events"]) == 20
    assert len(first["execution"]["checkpoints"]) == 16
    assert first["display"]["system"]["roots"] == ["hbm", "smem", "compute"]
    assert [lane["id"] for lane in first["display"]["timeline"]["lanes"]] == [
        "copy_engine",
        "tensor_core",
        "softmax_pipe",
        "global_store",
        "lifecycle",
    ]
    narrow_places = first["display"]["system"]["geometry"]["narrow"]["places"]
    for root in first["display"]["system"]["roots"]:
        box = narrow_places[root]
        assert box["x"] >= 24
        assert box["x"] + box["w"] <= 336

    wide = first["display"]["system"]["geometry"]["wide"]
    root_top = min(wide["places"][root]["y"] for root in first["display"]["system"]["roots"])
    root_bottom = max(
        wide["places"][root]["y"] + wide["places"][root]["h"]
        for root in first["display"]["system"]["roots"]
    )
    assert root_top >= 76
    assert wide["canvas"]["height"] - root_bottom >= 76


def test_copy_lineage_retains_hbm_source_and_creates_smem_materialization() -> None:
    snapshot = _checkpoint(_compiled(), "first_qk")
    by_id = {item["id"]: item for item in snapshot["materializations"]}

    assert by_id["q.hbm"]["place"] == "hbm"
    assert by_id["q.smem"]["place"] == "smem_q"
    assert by_id["q.smem"]["provenance"] == "q.hbm"


def test_prefetch_overlap_and_smem_occupancy_are_compiled() -> None:
    snapshot = _checkpoint(_compiled(), "overlap_prefetch")
    smem = next(item for item in snapshot["resource_ledgers"] if item["resource"] == "smem_bytes")

    assert set(snapshot["active_stages"]) == {"qk0", "load_v1"}
    assert smem["used"] == {"bytes": 131072.0}
    assert smem["capacity"] == {"bytes": 131072.0}
    assert set(smem["owners"]) == {"q.smem", "k0.buf0", "v0.buf0", "k1.buf1"}


def test_output_copy_precedes_local_cleanup() -> None:
    release = _checkpoint(_compiled(), "release_local")
    done = _checkpoint(_compiled(), "done")
    release_ids = {item["id"] for item in release["materializations"]}
    done_ids = {item["id"] for item in done["materializations"]}

    assert {"output.acc", "output.hbm"} <= release_ids
    assert "output.acc" not in done_ids
    assert "output.hbm" in done_ids
    assert {"q.hbm", "k0.hbm", "v0.hbm", "k1.hbm", "v1.hbm", "k2.hbm", "v2.hbm"} <= done_ids


def test_resource_over_capacity_is_reported() -> None:
    trace = load_trace(EXAMPLE)
    load_q = trace.stages[0]
    oversized = load_q.claims[0].model_copy(update={"amount": {"channels": 2}})
    changed = load_q.model_copy(update={"claims": [oversized]})
    invalid = trace.model_copy(update={"stages": [changed, *trace.stages[1:]]})

    codes = {issue.code for issue in validate_trace(invalid).errors}
    assert "resource-over-capacity" in codes


def test_missing_copy_source_is_reported() -> None:
    trace = load_trace(EXAMPLE)
    load_q = trace.stages[0]
    effect = load_q.effects[0].model_copy(update={"from_materialization": "missing.source"})
    changed = load_q.model_copy(update={"effects": [effect]})
    invalid = trace.model_copy(update={"stages": [changed, *trace.stages[1:]]})

    codes = {issue.code for issue in validate_trace(invalid).errors}
    assert "provenance-not-present" in codes


def test_server_uses_portable_component() -> None:
    compiled = _compiled()
    client = TestClient(create_app(compiled))

    page = client.get("/")
    trace = client.get("/api/trace")
    component = client.get("/assets/systems-viz-next.js")

    assert page.status_code == 200
    assert '<systems-viz-next src="/api/trace"' in page.text
    assert trace.json() == compiled
    assert 'customElements.define("systems-viz-next"' in component.text
    assert "data-drag-place" in component.text
    assert "data-resize-place" in component.text
    assert "data-scale-up" in component.text
    assert "shape-scale" in component.text
    assert "place_scales" in component.text
    assert "routeConnection" in component.text
    assert "data-edge-halo" in component.text
    assert "data-toggle-edge-edit" in component.text
    assert "data-drag-edge" in component.text
    assert 'data-select="${escapeText(place.id)}"' in component.text
    assert 'data-select="${escapeText(route.id)}"' in component.text
    assert 'data-select="${escapeText(ledger.resource)}"' in component.text
    assert "this.dragState = { id, moved: false }" in component.text
    assert "edge_offsets" in component.text
    assert "fitTimelineLabel" in component.text
    assert "data-label-fit" in component.text
    assert "timeline-label-" in component.text
    assert "clip-path" in component.text
    assert "cursor-change" in component.text
    assert "getAnnotations(options = {})" in component.text
    assert "exportViewerState()" in component.text
    assert "importViewerState(input" in component.text
    assert "saveViewerState()" in component.text
    assert "state-src" in component.text
    assert "viewer-state-conflict" in component.text
    assert "auditCurrentLayout()" in component.text
    assert "checkDefaultLayout(options = {})" in component.text
    assert 'new CustomEvent("layout-check"' in component.text
    assert "data-layout-item" in component.text
    assert "data-layout-label" in component.text
    assert "data-check-layout" in component.text
    assert "this.visibleAnnotations().findIndex" in component.text
    assert component.headers["cache-control"] == "no-store"


def test_file_backed_viewer_state_roundtrip_and_conflict(tmp_path: Path) -> None:
    compiled = _compiled()
    state_path = tmp_path / "flash.viewer-state.json"
    client = TestClient(create_app(compiled, state_path))

    page = client.get("/")
    initial = client.get("/api/state")
    proposed = initial.json()
    proposed["narrative_overrides"] = {"start": "## Persisted narrative"}
    proposed["layout"]["shape_scale"] = 1.2

    saved = client.put("/api/state", json=proposed, headers={"If-Match": initial.headers["etag"]})
    stale = client.put("/api/state", json=proposed, headers={"If-Match": initial.headers["etag"]})

    assert 'visualization-id="flash-attention-v2-tile"' in page.text
    assert 'state-src="/api/state"' in page.text
    assert initial.status_code == 200
    assert initial.json()["revision"] == 0
    assert initial.headers["etag"] == '"revision-0"'
    assert saved.status_code == 200
    assert saved.json()["revision"] == 1
    assert saved.headers["etag"] == '"revision-1"'
    assert stale.status_code == 412
    assert state_path.exists()

    reloaded = TestClient(create_app(compiled, state_path)).get("/api/state")
    assert reloaded.json()["narrative_overrides"] == {"start": "## Persisted narrative"}
    assert reloaded.json()["layout"]["shape_scale"] == 1.2


def test_renderer_contains_no_flash_attention_specific_logic() -> None:
    source = component_source().lower()

    assert "flashattention" not in source
    assert "softmax0" not in source
    assert "qk0" not in source


def test_cli_validate_compile_and_schema(tmp_path: Path) -> None:
    runner = CliRunner()
    output = tmp_path / "compiled.json"

    validate_result = runner.invoke(app, ["validate", str(EXAMPLE)])
    compile_result = runner.invoke(app, ["compile", str(EXAMPLE), "-o", str(output)])
    schema_result = runner.invoke(app, ["schema"])
    state_schema_result = runner.invoke(app, ["state-schema"])

    assert validate_result.exit_code == 0, validate_result.output
    assert compile_result.exit_code == 0, compile_result.output
    assert json.loads(output.read_text())["format"] == "sviz-display"
    assert json.loads(schema_result.output)["title"] == "TraceDocument"
    assert json.loads(state_schema_result.output)["title"] == "ViewerState"


def test_view_enables_file_backed_persistence_by_default(tmp_path: Path, monkeypatch) -> None:
    trace_path = tmp_path / EXAMPLE.name
    trace_path.write_text(EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8")
    served_apps = []

    def capture_run(application, **_kwargs) -> None:
        served_apps.append(application)

    monkeypatch.setattr("sviz.cli.uvicorn.run", capture_run)
    runner = CliRunner()

    persistent = runner.invoke(app, ["view", str(trace_path), "--no-open"])
    stateless = runner.invoke(app, ["view", str(trace_path), "--no-open", "--no-persist"])

    default_state = tmp_path / ".sviz" / "flash-attention-v2-tile.viewer-state.json"
    assert persistent.exit_code == 0, persistent.output
    assert f"Viewer state: {default_state}" in persistent.output
    assert "/api/state" in {route.path for route in served_apps[0].routes}
    assert not default_state.exists()
    assert stateless.exit_code == 0, stateless.output
    assert "Viewer persistence disabled" in stateless.output
    assert "/api/state" not in {route.path for route in served_apps[1].routes}


def test_bundle_is_portable_and_self_contained(tmp_path: Path) -> None:
    created = export_trace(EXAMPLE, tmp_path, "bundle")

    assert {path.name for path in created} == {
        "flash_attention_vnext.json",
        "flash_attention_vnext.inline.html",
        "flash_attention_vnext.standalone.html",
        "flash_attention_vnext.iframe.html",
    }
    standalone = (tmp_path / "flash_attention_vnext.standalone.html").read_text()
    inline = (tmp_path / "flash_attention_vnext.inline.html").read_text()

    assert "systems-viz-next" in standalone
    assert "systems-viz-next" in inline
    assert "sviz-display" in standalone
    assert 'visualization-id="flash-attention-v2-tile"' in standalone
    assert 'visualization-id="flash-attention-v2-tile"' in inline
    assert 'src="/assets/' not in standalone
    assert "fetch(" in standalone  # component supports src, while this export uses inline data


def test_only_vnext_examples_and_schema_are_kept() -> None:
    assert {path.name for path in (ROOT / "examples").glob("*.yaml")} == {
        "deepep_vnext.yaml",
        "flash_attention_vnext.yaml",
        "mla_decode_vnext.yaml",
        "mla_prefill_vnext.yaml",
    }
    assert {path.name for path in (ROOT / "schema").glob("*.json")} == {
        "sviz-0.2-draft.schema.json",
        "sviz-viewer-state-0.1.schema.json",
    }
