"""Orchestrates generators via Pub/Sub (DIP: depends on abstractions)."""
from __future__ import annotations

from typing import Protocol

from stock_school.core.bus import EventBus
from stock_school.core.events import GenerationFinished, GenerationStarted, SvgArtifactReady


class _RunnableGenerator(Protocol):
    generator_id: str

    def generate(self) -> dict[str, str]: ...

    def artifact_path(self, filename: str): ...


class GenerationPipeline:
    """Publisher: emits lifecycle events; subscribers handle side effects."""

    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def run(self, generator: _RunnableGenerator) -> int:
        self._bus.publish(GenerationStarted(generator_id=generator.generator_id))
        count = 0
        for filename, content in generator.generate().items():
            if not content:
                continue
            self._bus.publish(
                SvgArtifactReady(
                    generator_id=generator.generator_id,
                    path=generator.artifact_path(filename),
                    content=content,
                )
            )
            count += 1
        self._bus.publish(
            GenerationFinished(generator_id=generator.generator_id, artifact_count=count)
        )
        return count
