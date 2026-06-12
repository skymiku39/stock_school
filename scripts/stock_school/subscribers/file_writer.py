"""Persist SVG artifacts to disk (SRP: I/O only)."""
from __future__ import annotations

from stock_school.core.events import Event, SvgArtifactReady


class FileWriterSubscriber:
    def on_event(self, event: Event) -> None:
        if not isinstance(event, SvgArtifactReady) or not event.content:
            return
        event.path.parent.mkdir(parents=True, exist_ok=True)
        event.path.write_text(event.content, encoding="utf-8")
