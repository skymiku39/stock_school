"""EventBus and GenerationPipeline unit tests."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from stock_school.core.bus import EventBus
from stock_school.core.events import (
    Event,
    GenerationError,
    GenerationFinished,
    GenerationStarted,
    PipelineCompleted,
    SvgArtifactReady,
)
from stock_school.services.pipeline import GenerationPipeline


@dataclass
class _StubGenerator:
    output_dir: Path
    generator_id: str = "stub"
    artifacts: dict[str, str] | None = None
    fail: bool = False

    def generate(self) -> dict[str, str]:
        if self.fail:
            raise RuntimeError("boom")
        return self.artifacts if self.artifacts is not None else {"a.svg": "<svg></svg>"}

    def artifact_path(self, filename: str) -> Path:
        return self.output_dir / filename


class _RecordingSubscriber:
    def __init__(self) -> None:
        self.events: list[Event] = []

    def on_event(self, event: Event) -> None:
        self.events.append(event)


def test_event_bus_mro_dispatches_base_handlers(tmp_path: Path) -> None:
    bus = EventBus()
    recorder = _RecordingSubscriber()
    bus.subscribe_subscriber(recorder)
    bus.publish(GenerationStarted(generator_id="x"))
    assert len(recorder.events) == 1
    assert isinstance(recorder.events[0], GenerationStarted)


def test_pipeline_emits_lifecycle_events(tmp_path: Path) -> None:
    bus = EventBus()
    recorder = _RecordingSubscriber()
    bus.subscribe_subscriber(recorder)
    pipeline = GenerationPipeline(bus)
    gen = _StubGenerator(output_dir=tmp_path, artifacts={"ok.svg": "<svg>x</svg>"})

    count = pipeline.run(gen)

    assert count == 1
    types = [type(e) for e in recorder.events]
    assert types == [
        GenerationStarted,
        SvgArtifactReady,
        GenerationFinished,
    ]
    ready = recorder.events[1]
    assert isinstance(ready, SvgArtifactReady)
    assert ready.path == tmp_path / "ok.svg"


def test_pipeline_publishes_error_on_exception(tmp_path: Path) -> None:
    bus = EventBus()
    recorder = _RecordingSubscriber()
    bus.subscribe_subscriber(recorder)
    pipeline = GenerationPipeline(bus)
    gen = _StubGenerator(output_dir=tmp_path, fail=True)

    count = pipeline.run(gen)

    assert count == 0
    assert any(isinstance(e, GenerationError) for e in recorder.events)
    assert recorder.events[-1].__class__ is GenerationFinished


def test_pipeline_publishes_error_on_empty_output(tmp_path: Path) -> None:
    bus = EventBus()
    recorder = _RecordingSubscriber()
    bus.subscribe_subscriber(recorder)
    pipeline = GenerationPipeline(bus)
    gen = _StubGenerator(output_dir=tmp_path, artifacts={})

    count = pipeline.run(gen)

    assert count == 0
    errors = [e for e in recorder.events if isinstance(e, GenerationError)]
    assert len(errors) == 1
    assert "未產出" in errors[0].message


def test_pipeline_run_all_publishes_completed(tmp_path: Path) -> None:
    bus = EventBus()
    recorder = _RecordingSubscriber()
    bus.subscribe_subscriber(recorder)
    pipeline = GenerationPipeline(bus)
    gens = [
        _StubGenerator(output_dir=tmp_path, generator_id="a"),
        _StubGenerator(output_dir=tmp_path, generator_id="b"),
    ]

    total = pipeline.run_all(gens, output_dir=tmp_path)

    assert total == 2
    completed = [e for e in recorder.events if isinstance(e, PipelineCompleted)]
    assert len(completed) == 1
    assert completed[0].total_artifacts == 2
    assert completed[0].output_dir == tmp_path


def test_file_writer_subscriber_writes_artifact(tmp_path: Path) -> None:
    from stock_school.subscribers.file_writer import FileWriterSubscriber

    sub = FileWriterSubscriber()
    target = tmp_path / "nested" / "chart.svg"
    sub.on_event(
        SvgArtifactReady(
            generator_id="stub",
            path=target,
            content='<svg viewBox="0 0 1 1" aria-label="t"></svg>',
        )
    )
    assert target.read_text(encoding="utf-8").startswith("<svg")


def test_console_arrow_falls_back_to_ascii_on_legacy_codepage(monkeypatch) -> None:
    import io

    from stock_school.subscribers import console

    class _Cp950Stream(io.StringIO):
        encoding = "cp950"

    monkeypatch.setattr(console.sys, "stdout", _Cp950Stream())
    assert console._safe_arrow() == "->"


def test_console_arrow_uses_unicode_on_utf8(monkeypatch) -> None:
    import io

    from stock_school.subscribers import console

    class _Utf8Stream(io.StringIO):
        encoding = "utf-8"

    monkeypatch.setattr(console.sys, "stdout", _Utf8Stream())
    assert console._safe_arrow() == "→"
