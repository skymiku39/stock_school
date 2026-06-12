"""CLI entry — wires Pub/Sub bus, generators, and subscribers."""
from __future__ import annotations

import argparse
from pathlib import Path

from stock_school.core.bus import EventBus
from stock_school.core.events import PipelineCompleted
from stock_school.data.twse import TwseDataSource
from stock_school.generators.candles import CandleSvgGenerator
from stock_school.generators.cases import CaseSvgGenerator
from stock_school.generators.indicators import IndicatorSvgGenerator
from stock_school.generators.quotes import QuoteSvgGenerator
from stock_school.services.pipeline import GenerationPipeline
from stock_school.subscribers.console import ConsoleSubscriber
from stock_school.subscribers.file_writer import FileWriterSubscriber
from stock_school.subscribers.mkdocs_hint import MkdocsHintSubscriber

ASSETS = Path(__file__).resolve().parent.parent.parent / "docs" / "assets"


def _build_bus(*, hint_mkdocs: bool = False) -> EventBus:
    bus = EventBus()
    bus.subscribe_subscriber(ConsoleSubscriber())
    bus.subscribe_subscriber(FileWriterSubscriber())
    if hint_mkdocs:
        bus.subscribe_subscriber(MkdocsHintSubscriber())
    return bus


def _all_generators(data_source: TwseDataSource):
    return [
        QuoteSvgGenerator(data_source=data_source, output_dir=ASSETS / "quotes"),
        CandleSvgGenerator(output_dir=ASSETS / "candles"),
        IndicatorSvgGenerator(data_source=data_source, output_dir=ASSETS / "indicators"),
        CaseSvgGenerator(output_dir=ASSETS / "cases"),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Stock School SVG assets")
    parser.add_argument(
        "--only",
        choices=["quotes", "candles", "indicators", "cases"],
        help="Run a single generator",
    )
    parser.add_argument(
        "--hint-serve",
        action="store_true",
        help="After generation, print mkdocs serve hint",
    )
    args = parser.parse_args(argv)

    bus = _build_bus(hint_mkdocs=args.hint_serve)
    pipeline = GenerationPipeline(bus)
    data_source = TwseDataSource()
    generators = _all_generators(data_source)

    if args.only:
        generators = [g for g in generators if g.generator_id == args.only]

    total = 0
    for generator in generators:
        total += pipeline.run(generator)

    print(f"\nTotal: {total} SVG files → {ASSETS}")
    bus.publish(PipelineCompleted(total_artifacts=total))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
