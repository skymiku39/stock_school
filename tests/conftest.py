"""Shared test fixtures and helpers.

提供測試共用的路徑常數與一個離線、確定性的 ``FakeDataSource``，
讓圖表／指標測試不需連線 TWSE 即可重現。
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from stock_school.domain.bar import Bar

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
ASSETS_DIR = DOCS_DIR / "assets"

_BASE_DATE = date(2024, 1, 1)


def make_bars(n: int) -> list[Bar]:
    """產生 ``n`` 根確定性的 OHLCV K 線（不依賴亂數或網路）。"""
    bars: list[Bar] = []
    price = 100.0
    for i in range(n):
        delta = ((i * 7) % 9) - 4  # 介於 -4~4 的固定鋸齒波動
        open_ = price
        close = round(price + delta, 2)
        high = round(max(open_, close) + 1.5, 2)
        low = round(min(open_, close) - 1.5, 2)
        volume = 10_000 + (i % 5) * 1_000
        day = (_BASE_DATE + timedelta(days=i)).isoformat()
        bars.append(Bar(d=day, open=open_, high=high, low=low, close=close, volume=volume))
        price = close if close > 1 else 1.0
    return bars


class FakeDataSource:
    """離線替身，符合 ``MarketDataSource`` 協定（LSP：可替換 TwseDataSource）。"""

    def __init__(self, *, count: int = 45) -> None:
        self._count = count

    def fetch_bars(self, stock_no: str, *, months: int = 4, tail: int = 30) -> list[Bar]:
        bars = make_bars(self._count)
        return bars[-tail:]
