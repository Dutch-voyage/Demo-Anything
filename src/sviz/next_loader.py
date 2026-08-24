"""Loader for the draft semantic IR."""

from __future__ import annotations

import json
from pathlib import Path

import yaml
from pydantic import ValidationError

from .loader import TraceLoadError, _format_validation_error
from .next_models import TraceDocument


def load_draft_trace(path: str | Path) -> TraceDocument:
    """Load YAML or JSON into the vNext draft model."""

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
