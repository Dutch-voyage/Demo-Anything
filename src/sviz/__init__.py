"""Public API for the Systems Visualization semantic IR."""

from .compiler import compile_trace
from .dsl import AuthoringError, Demo
from .exporter import export_trace
from .loader import TraceLoadError, load_trace
from .models import TraceDocument, ViewerState
from .validation import (
    TraceValidationError,
    ValidationIssue,
    ValidationReport,
    validate_trace,
)

__all__ = [
    "TraceDocument",
    "ViewerState",
    "AuthoringError",
    "Demo",
    "TraceLoadError",
    "TraceValidationError",
    "ValidationIssue",
    "ValidationReport",
    "compile_trace",
    "export_trace",
    "load_trace",
    "validate_trace",
]

__version__ = "0.2.0a1"
