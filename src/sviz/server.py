"""Public development-server interface."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI

from .next_server import create_next_app, next_component_source, next_viewer_html


def component_source() -> str:
    return next_component_source()


def viewer_html(title: str, visualization_id: str = "", *, persistent: bool = False) -> str:
    return next_viewer_html(title, visualization_id, persistent=persistent)


def create_app(compiled: dict[str, Any], state_path: str | Path | None = None) -> FastAPI:
    return create_next_app(compiled, state_path)
