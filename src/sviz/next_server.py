"""Development server for the semantic compiled renderer."""

from __future__ import annotations

from html import escape
from importlib.resources import files
import json
from pathlib import Path
import threading
from typing import Any

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, Response

from .viewer_state import ViewerState, empty_viewer_state


def next_component_source() -> str:
    return files("sviz").joinpath("static/systems-viz-next.js").read_text(encoding="utf-8")


def next_viewer_html(title: str, visualization_id: str = "", *, persistent: bool = False) -> str:
    persistence = ' state-src="/api/state"' if persistent else ""
    identity = f' visualization-id="{escape(visualization_id, quote=True)}"' if visualization_id else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)} · sviz</title>
  <style>
    :root {{ color-scheme: light dark; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; min-height: 100vh; padding: 18px; background: #eceef3; font-family: ui-sans-serif, system-ui, sans-serif; }}
    main {{ width: min(1180px, 100%); height: calc(100vh - 36px); min-height: 620px; margin: 0 auto; }}
    systems-viz-next {{ height: 100%; }}
    @media (prefers-color-scheme: dark) {{ body {{ background: #0d1015; }} }}
    @media (max-width: 620px) {{ body {{ padding: 8px; }} main {{ height: auto; min-height: 680px; }} }}
  </style>
  <script type="module" src="/assets/systems-viz-next.js"></script>
</head>
<body>
  <main><systems-viz-next src="/api/trace" theme="auto"{identity}{persistence}></systems-viz-next></main>
</body>
</html>"""


class ViewerStateStore:
    """Small file-backed adapter for development and single-process deployment."""

    def __init__(self, compiled: dict[str, Any], path: Path) -> None:
        self.compiled = compiled
        self.path = path
        self.lock = threading.Lock()
        self.state = self._load()

    def _load(self) -> ViewerState:
        if not self.path.exists():
            return empty_viewer_state(self.compiled)
        state = ViewerState.model_validate_json(self.path.read_text(encoding="utf-8"))
        if state.visualization_id != self.compiled["visualization_id"]:
            raise ValueError(
                f"viewer state belongs to {state.visualization_id!r}, expected {self.compiled['visualization_id']!r}"
            )
        return state

    @property
    def etag(self) -> str:
        return f'"revision-{self.state.revision}"'

    def save(self, proposed: ViewerState, if_match: str | None) -> ViewerState:
        with self.lock:
            if if_match != self.etag:
                raise HTTPException(status_code=412, detail="viewer state revision conflict")
            if proposed.visualization_id != self.compiled["visualization_id"]:
                raise HTTPException(status_code=409, detail="visualization ID mismatch")
            self.state = proposed.model_copy(
                update={
                    "revision": self.state.revision + 1,
                    "base_revision": self.compiled["base_revision"],
                }
            )
            self.path.parent.mkdir(parents=True, exist_ok=True)
            temporary = self.path.with_name(f".{self.path.name}.tmp")
            temporary.write_text(
                json.dumps(self.state.model_dump(mode="json"), ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            temporary.replace(self.path)
            return self.state


def create_next_app(compiled: dict[str, Any], state_path: str | Path | None = None) -> FastAPI:
    app = FastAPI(title="sviz viewer", docs_url=None, redoc_url=None)
    store = ViewerStateStore(compiled, Path(state_path)) if state_path is not None else None

    @app.get("/", response_class=HTMLResponse)
    def index() -> str:
        return next_viewer_html(
            compiled["title"],
            compiled["visualization_id"],
            persistent=store is not None,
        )

    @app.get("/api/trace", response_class=JSONResponse)
    def trace() -> dict[str, Any]:
        return compiled

    @app.get("/assets/systems-viz-next.js")
    def component() -> Response:
        return Response(next_component_source(), media_type="text/javascript", headers={"Cache-Control": "no-store"})

    if store is not None:
        @app.get("/api/state", response_class=JSONResponse)
        def viewer_state() -> JSONResponse:
            return JSONResponse(store.state.model_dump(mode="json"), headers={"ETag": store.etag, "Cache-Control": "no-store"})

        @app.put("/api/state", response_class=JSONResponse)
        def save_viewer_state(
            proposed: ViewerState,
            if_match: str | None = Header(default=None, alias="If-Match"),
        ) -> JSONResponse:
            saved = store.save(proposed, if_match)
            return JSONResponse(saved.model_dump(mode="json"), headers={"ETag": store.etag, "Cache-Control": "no-store"})

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app
