"""Console logging subscriber (SRP: observability only)."""
from __future__ import annotations

import sys

from stock_school.core.events import (
    Event,
    GenerationError,
    GenerationFinished,
    GenerationStarted,
    PipelineCompleted,
    SvgArtifactReady,
)


def _safe_arrow() -> str:
    """Use the Unicode arrow only on UTF-8 terminals; ASCII fallback elsewhere.

    Legacy code pages such as cp950 can *encode* U+2192 but render it as
    mojibake, so encodability is not a reliable signal — the terminal encoding
    family is.
    """
    encoding = (getattr(sys.stdout, "encoding", None) or "utf-8").lower()
    is_utf8 = encoding.replace("-", "") in {"utf8", "utf16", "utf32"}
    return "→" if is_utf8 else "->"


class ConsoleSubscriber:
    def on_event(self, event: Event) -> None:
        if isinstance(event, GenerationStarted):
            print(f"[start] {event.generator_id}")
        elif isinstance(event, SvgArtifactReady):
            print(f"  {_safe_arrow()} {event.path.name}")
        elif isinstance(event, GenerationFinished):
            print(f"[done] {event.generator_id} ({event.artifact_count} files)")
        elif isinstance(event, GenerationError):
            print(f"[error] {event.generator_id}: {event.message}")
        elif isinstance(event, PipelineCompleted):
            dest = f" {_safe_arrow()} {event.output_dir}" if event.output_dir else ""
            print(f"\nTotal: {event.total_artifacts} SVG files{dest}")
