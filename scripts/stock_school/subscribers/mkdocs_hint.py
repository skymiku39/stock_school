"""Suggest MkDocs preview after generation (SRP: post-build guidance)."""
from __future__ import annotations

from stock_school.core.events import Event, PipelineCompleted


class MkdocsHintSubscriber:
    def on_event(self, event: Event) -> None:
        if isinstance(event, PipelineCompleted):
            print("\n提示：預覽網站 → uv run mkdocs serve")
