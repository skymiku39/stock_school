"""Stock School chart generation — SOLID + Pub/Sub architecture."""

from stock_school.core.bus import EventBus
from stock_school.core.events import Event, GenerationFinished, GenerationStarted, SvgArtifactReady

__all__ = [
    "Event",
    "EventBus",
    "GenerationFinished",
    "GenerationStarted",
    "SvgArtifactReady",
]
