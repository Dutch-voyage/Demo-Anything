"""Command line interface for sviz."""

from __future__ import annotations

import json
import threading
import webbrowser
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer
import uvicorn

from .compiler import compile_trace
from .exporter import export_trace
from .loader import TraceLoadError, load_trace
from .models import TraceDocument, ViewerState
from .server import create_app
from .validation import TraceValidationError, validate_trace


app = typer.Typer(no_args_is_help=True, add_completion=False, help="Portable systems visualization IR tools.")


class ExportChoice(str, Enum):
    bundle = "bundle"
    json = "json"
    inline = "inline"
    standalone = "standalone"
    iframe = "iframe"


def _fail(message: str) -> None:
    typer.secho(message, fg=typer.colors.RED, err=True)


@app.command("validate")
def validate_command(
    traces: Annotated[list[Path], typer.Argument(exists=True, readable=True, help="Semantic YAML or JSON trace files")],
) -> None:
    """Validate one or more semantic traces."""

    failed = False
    for path in traces:
        try:
            trace = load_trace(path)
            report = validate_trace(trace)
        except TraceLoadError as error:
            failed = True
            _fail(str(error))
            continue
        if report.errors:
            failed = True
            typer.secho(f"{path}: invalid", fg=typer.colors.RED)
            for issue in report.issues:
                typer.echo(f"  {issue}")
        else:
            typer.secho(f"{path}: valid", fg=typer.colors.GREEN)
            for issue in report.warnings:
                typer.secho(f"  {issue}", fg=typer.colors.YELLOW)
    if failed:
        raise typer.Exit(code=1)


@app.command("schema")
def schema_command(
    output: Annotated[Path | None, typer.Option("--output", "-o", help="Write to a file instead of stdout")] = None,
) -> None:
    """Print the semantic IR JSON Schema."""

    rendered = json.dumps(TraceDocument.model_json_schema(by_alias=True), indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        typer.echo(str(output))
    else:
        typer.echo(rendered, nl=False)


@app.command("state-schema")
def state_schema_command(
    output: Annotated[Path | None, typer.Option("--output", "-o", help="Write to a file instead of stdout")] = None,
) -> None:
    """Print the persisted viewer-state JSON Schema."""

    rendered = json.dumps(ViewerState.model_json_schema(), indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        typer.echo(str(output))
    else:
        typer.echo(rendered, nl=False)


@app.command("compile")
def compile_command(
    trace_path: Annotated[Path, typer.Argument(exists=True, readable=True, help="Semantic trace to compile")],
    output: Annotated[Path | None, typer.Option("--output", "-o", help="Write JSON to a file")] = None,
) -> None:
    """Compile a trace into deterministic display JSON."""

    try:
        compiled = compile_trace(load_trace(trace_path))
    except (TraceLoadError, TraceValidationError) as error:
        _fail(str(error))
        raise typer.Exit(code=1) from error
    rendered = json.dumps(compiled, ensure_ascii=False, indent=2) + "\n"
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")
        typer.echo(str(output))
    else:
        typer.echo(rendered, nl=False)


@app.command("view")
def view_command(
    trace_path: Annotated[Path, typer.Argument(exists=True, readable=True, help="Semantic trace to view")],
    host: Annotated[str, typer.Option(help="Bind address")] = "127.0.0.1",
    port: Annotated[int, typer.Option(help="Bind port")] = 8000,
    open_browser: Annotated[bool, typer.Option("--open/--no-open", help="Open the viewer in the default browser")] = True,
    persist: Annotated[bool, typer.Option("--persist/--no-persist", help="Enable explicit viewer-state save and reload actions")] = True,
    state_file: Annotated[Path | None, typer.Option("--state-file", help="Override the default viewer-state file")] = None,
) -> None:
    """Start the local development viewer."""

    try:
        compiled = compile_trace(load_trace(trace_path))
    except (TraceLoadError, TraceValidationError) as error:
        _fail(str(error))
        raise typer.Exit(code=1) from error
    if not persist and state_file is not None:
        raise typer.BadParameter("--state-file cannot be combined with --no-persist")
    resolved_state_file = None
    if persist:
        resolved_state_file = state_file or (
            trace_path.parent / ".sviz" / f"{compiled['visualization_id']}.viewer-state.json"
        )
    url = f"http://{host}:{port}/"
    typer.echo(f"Viewing {trace_path} at {url}")
    if resolved_state_file is not None:
        typer.echo(f"Viewer state: {resolved_state_file}")
    else:
        typer.echo("Viewer persistence disabled")
    if open_browser:
        threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    uvicorn.run(create_app(compiled, resolved_state_file), host=host, port=port, log_level="info")


@app.command("export")
def export_command(
    trace_path: Annotated[Path, typer.Argument(exists=True, readable=True, help="Semantic trace to export")],
    output: Annotated[Path, typer.Option("--output", "-o", help="Output directory for bundle, file otherwise")] = Path("dist"),
    export_format: Annotated[ExportChoice, typer.Option("--format", "-f", help="Artifact format")] = ExportChoice.bundle,
) -> None:
    """Create portable JSON, inline, standalone, or iframe artifacts."""

    try:
        created = export_trace(trace_path, output, export_format.value)
    except (TraceLoadError, TraceValidationError) as error:
        _fail(str(error))
        raise typer.Exit(code=1) from error
    for path in created:
        typer.echo(str(path))


if __name__ == "__main__":  # pragma: no cover
    app()
