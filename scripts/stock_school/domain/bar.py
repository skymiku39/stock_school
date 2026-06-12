from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Bar:
    d: str
    open: float
    high: float
    low: float
    close: float
    volume: int
