"""Public compilation interface for the semantic IR."""

from __future__ import annotations

from typing import Any

from .next_compiler import compile_draft_trace
from .next_models import TraceDocument


def compile_trace(trace: TraceDocument) -> dict[str, Any]:
    """Compile a semantic trace into deterministic execution and display plans."""

    return compile_draft_trace(trace)
