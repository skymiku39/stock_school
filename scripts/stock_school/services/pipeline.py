"""Orchestrates generators via Pub/Sub (DIP: depends on abstractions)."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from stock_school.core.bus import EventBus
from stock_school.core.events import (
    GenerationError,
    GenerationFinished,
    GenerationStarted,
    PipelineCompleted,
    SvgArtifactReady,
)
from stock_school.core.protocols import SvgGenerator


@dataclass
class PipelineResult:
    """Structured outcome of a pipeline run."""

    total_artifacts: int = 0
    error_count: int = 0

    @property
    def success(self) -> bool:
        return self.error_count == 0


class GenerationPipeline:
    """Publisher: emits lifecycle events; subscribers handle side effects."""

    def __init__(self, bus: EventBus) -> None:
        self._bus = bus

    def run(self, generator: SvgGenerator) -> tuple[int, int]:
        """Run a single generator. Returns (artifact_count, error_count)."""
        gid = generator.generator_id
        self._bus.publish(GenerationStarted(generator_id=gid))
        try:
            artifacts = generator.generate()
        except Exception as exc:  # noqa: BLE001 — surface via bus, not crash CLI
            self._bus.publish(
                GenerationError(
                    generator_id=gid,
                    message=str(exc),
                    cause=exc,
                )
            )
            self._bus.publish(GenerationFinished(generator_id=gid, artifact_count=0))
            return 0, 1

        count = 0
        for filename, content in artifacts.items():
            if not content:
                continue
            self._bus.publish(
                SvgArtifactReady(
                    generator_id=gid,
                    path=generator.artifact_path(filename),
                    content=content,
                )
            )
            count += 1

        errors = 0
        if count == 0:
            self._bus.publish(
                GenerationError(
                    generator_id=gid,
                    message="未產出任何 SVG（可能因資料不足或外部 API 無回應）",
                )
            )
            errors = 1

        self._bus.publish(GenerationFinished(generator_id=gid, artifact_count=count))
        return count, errors

    def run_all(
        self,
        generators: list[SvgGenerator],
        *,
        output_dir: Path | None = None,
    ) -> PipelineResult:
        total_artifacts = 0
        total_errors = 0
        for g in generators:
            artifacts, errors = self.run(g)
            total_artifacts += artifacts
            total_errors += errors
        self._bus.publish(
            PipelineCompleted(total_artifacts=total_artifacts, output_dir=output_dir)
        )
        return PipelineResult(
            total_artifacts=total_artifacts,
            error_count=total_errors,
        )
