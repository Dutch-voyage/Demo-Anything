"""Portable exports for the semantic compiled renderer."""

from __future__ import annotations

import json
from html import escape
from pathlib import Path
from typing import Literal

from .next_compiler import compile_draft_trace
from .next_loader import load_draft_trace
from .next_server import next_component_source


DraftExportFormat = Literal["bundle", "json", "inline", "standalone", "iframe"]


def _safe_json(data: dict) -> str:
    return (
        json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        .replace("&", "\\u0026")
        .replace("<", "\\u003c")
        .replace(">", "\\u003e")
    )


def draft_inline_snippet(compiled: dict) -> str:
    return f"""<!-- sviz semantic visualization -->
<script type="module">
{next_component_source()}
</script>
<systems-viz-next visualization-id="{escape(compiled['visualization_id'], quote=True)}" theme="auto" style="height:720px;min-height:620px">
  <script type="application/vnd.sviz+json">{_safe_json(compiled)}</script>
</systems-viz-next>
"""


def draft_standalone_html(compiled: dict) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(compiled["title"])}</title>
  <style>
    :root {{ color-scheme: light dark; }}
    * {{ box-sizing: border-box; }}
    html, body {{ margin: 0; min-height: 100%; }}
    body {{ padding: 12px; background: #eceef3; }}
    systems-viz-next {{ height: calc(100vh - 24px); min-height: 620px; }}
    @media (prefers-color-scheme: dark) {{ body {{ background: #0d1015; }} }}
    @media (max-width: 620px) {{ systems-viz-next {{ height: auto; min-height: 680px; }} }}
  </style>
</head>
<body>
{draft_inline_snippet(compiled)}
</body>
</html>
"""


def draft_iframe_snippet(standalone_name: str, title: str) -> str:
    return f"""<iframe
  src="{escape(standalone_name, quote=True)}"
  title="{escape(title, quote=True)}"
  loading="lazy"
  style="width:100%;height:740px;border:0;border-radius:12px"
></iframe>
"""


def export_draft_trace(
    trace_path: str | Path,
    output: str | Path,
    export_format: DraftExportFormat = "bundle",
) -> list[Path]:
    source = Path(trace_path)
    destination = Path(output)
    compiled = compile_draft_trace(load_draft_trace(source))
    created: list[Path] = []

    def write(path: Path, content: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        created.append(path)

    rendered_json = json.dumps(compiled, ensure_ascii=False, indent=2) + "\n"
    if export_format == "bundle":
        destination.mkdir(parents=True, exist_ok=True)
        json_path = destination / f"{source.stem}.json"
        inline_path = destination / f"{source.stem}.inline.html"
        standalone_path = destination / f"{source.stem}.standalone.html"
        iframe_path = destination / f"{source.stem}.iframe.html"
        write(json_path, rendered_json)
        write(inline_path, draft_inline_snippet(compiled))
        write(standalone_path, draft_standalone_html(compiled))
        write(iframe_path, draft_iframe_snippet(standalone_path.name, compiled["title"]))
    elif export_format == "json":
        write(destination, rendered_json)
    elif export_format == "inline":
        write(destination, draft_inline_snippet(compiled))
    elif export_format == "standalone":
        write(destination, draft_standalone_html(compiled))
    elif export_format == "iframe":
        standalone_path = destination.with_name(f"{destination.stem}.standalone.html")
        write(standalone_path, draft_standalone_html(compiled))
        write(destination, draft_iframe_snippet(standalone_path.name, compiled["title"]))
    else:  # pragma: no cover
        raise ValueError(f"unknown export format {export_format!r}")
    return created
