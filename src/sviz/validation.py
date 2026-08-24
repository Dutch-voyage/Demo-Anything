"""Public validation types and semantic validation interface."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .next_models import TraceDocument


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    level: Literal["error", "warning"]
    code: str
    path: str
    message: str

    def __str__(self) -> str:
        return f"{self.level.upper()} {self.path}: {self.message} [{self.code}]"


@dataclass(frozen=True, slots=True)
class ValidationReport:
    issues: tuple[ValidationIssue, ...]

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.level == "error")

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.level == "warning")

    @property
    def ok(self) -> bool:
        return not self.errors

    def raise_for_errors(self) -> None:
        if self.errors:
            raise TraceValidationError(self)


class TraceValidationError(ValueError):
    def __init__(self, report: ValidationReport) -> None:
        self.report = report
        super().__init__("\n".join(str(issue) for issue in report.errors))


def validate_trace(trace: TraceDocument) -> ValidationReport:
    """Validate references, schedule, lifecycle, flows, and capacity."""

    from .next_validation import validate_draft_trace

    return validate_draft_trace(trace)
