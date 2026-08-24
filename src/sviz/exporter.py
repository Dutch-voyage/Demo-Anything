"""Public portable-export interface."""

from __future__ import annotations

from pathlib import Path

from .next_exporter import DraftExportFormat, export_draft_trace


ExportFormat = DraftExportFormat


def export_trace(
    trace_path: str | Path,
    output: str | Path,
    export_format: ExportFormat = "bundle",
) -> list[Path]:
    return export_draft_trace(trace_path, output, export_format)
