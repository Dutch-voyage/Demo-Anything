from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote

import yaml

from sviz import validate_trace
from sviz.models import TraceDocument


ROOT = Path(__file__).parents[1]
AUTHORING_GUIDE = ROOT / "docs" / "ir-authoring-guide.md"


def test_minimal_trace_in_authoring_guide_is_valid() -> None:
    guide = AUTHORING_GUIDE.read_text(encoding="utf-8")
    match = re.search(
        r"## 4\. A minimal complete trace.*?```yaml\n(.*?)\n```",
        guide,
        re.DOTALL,
    )

    assert match is not None
    trace = TraceDocument.model_validate(yaml.safe_load(match.group(1)))
    report = validate_trace(trace)

    assert report.ok, "\n".join(str(issue) for issue in report.issues)


def test_local_markdown_links_resolve() -> None:
    documents = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
    missing: list[str] = []

    for document in documents:
        source = document.read_text(encoding="utf-8")
        for raw_target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", source):
            target = raw_target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            relative_path = unquote(target.split("#", maxsplit=1)[0])
            if relative_path and not (document.parent / relative_path).exists():
                missing.append(f"{document.relative_to(ROOT)} -> {relative_path}")

    assert not missing, "Missing local Markdown targets:\n" + "\n".join(missing)
