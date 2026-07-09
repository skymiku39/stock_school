"""Console logging subscriber (SRP: observability only)."""
from __future__ import annotations

from stock_school.core.events import (
    Event,
    GenerationError,
    GenerationFinished,
    GenerationStarted,
    PipelineCompleted,
    SvgArtifactReady,
)


class ConsoleSubscriber:
    def on_event(self, event: Event) -> None:
        if isinstance(event, GenerationStarted):
            print(f"[start] {event.generator_id}")
        elif isinstance(event, SvgArtifactReady):
            print(f"  → {event.path.name}")
        elif isinstance(event, GenerationFinished):
            print(f"[done] {event.generator_id} ({event.artifact_count} files)")
        elif isinstance(event, GenerationError):
            print(f"[error] {event.generator_id}: {event.message}")
        elif isinstance(event, PipelineCompleted):
            dest = f" → {event.output_dir}" if event.output_dir else ""
            print(f"\nTotal: {event.total_artifacts} SVG files{dest}")
