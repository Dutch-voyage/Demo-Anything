"""YAML and JSON loading for semantic sviz traces."""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from pydantic import ValidationError

from .next_models import TraceDocument


class TraceLoadError(ValueError):
    """Raised when a trace cannot be decoded or parsed into the IR model."""

    def __init__(self, source: Path, message: str) -> None:
        self.source = source
        self.detail = message
        super().__init__(f"{source}: {message}")


def _format_validation_error(error: ValidationError) -> str:
    lines: list[str] = []
    for item in error.errors(include_url=False):
        path = ".".join(str(part) for part in item["loc"])
        lines.append(f"{path or '<root>'}: {item['msg']}")
    return "\n".join(lines)


def load_trace(path: str | Path) -> TraceDocument:
    """Load YAML or JSON into the semantic IR model."""

    source = Path(path)
    try:
        text = source.read_text(encoding="utf-8")
    except OSError as error:
        raise TraceLoadError(source, str(error)) from error

    try:
        data = json.loads(text) if source.suffix.lower() == ".json" else yaml.safe_load(text)
    except (json.JSONDecodeError, yaml.YAMLError) as error:
        raise TraceLoadError(source, f"invalid syntax: {error}") from error

    if not isinstance(data, dict):
        raise TraceLoadError(source, "the document root must be a mapping")

    try:
        return TraceDocument.model_validate(data)
    except ValidationError as error:
        raise TraceLoadError(source, _format_validation_error(error)) from error
