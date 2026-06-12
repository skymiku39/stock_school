"""Domain events for the generation pipeline (Pub/Sub payloads)."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Event:
    """Base event — all bus messages inherit from this."""

    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True)
class GenerationStarted(Event):
    """Publisher signals a generator batch is starting."""

    generator_id: str = ""


@dataclass(frozen=True)
class SvgArtifactReady(Event):
    """Publisher produced one SVG artifact."""

    generator_id: str = ""
    path: Path = field(default_factory=Path)
    content: str = ""


@dataclass(frozen=True)
class GenerationFinished(Event):
    """Publisher completed a generator batch."""

    generator_id: str = ""
    artifact_count: int = 0


@dataclass(frozen=True)
class GenerationError(Event):
    """Publisher or subscriber reported a failure."""

    generator_id: str = ""
    message: str = ""
    cause: Any = None


@dataclass(frozen=True)
class PipelineCompleted(Event):
    """All requested generators finished."""

    total_artifacts: int = 0
