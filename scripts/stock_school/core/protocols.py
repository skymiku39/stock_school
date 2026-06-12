"""Abstract contracts (DIP + ISP)."""
from __future__ import annotations

from pathlib import Path
from typing import Protocol, runtime_checkable

from stock_school.core.events import Event
from stock_school.domain.bar import Bar


@runtime_checkable
class EventSubscriber(Protocol):
    """Subscribe to events — single responsibility per subscriber."""

    def on_event(self, event: Event) -> None: ...


@runtime_checkable
class MarketDataSource(Protocol):
    """Fetch OHLCV bars without coupling renderers to TWSE."""

    def fetch_bars(self, stock_no: str, *, months: int, tail: int) -> list[Bar]: ...


@runtime_checkable
class SvgGenerator(Protocol):
    """Produce named SVG artifacts (OCP: add generators without changing bus)."""

    @property
    def generator_id(self) -> str: ...

    def generate(self) -> dict[str, str]:
        """Return mapping of filename → SVG content."""
        ...
