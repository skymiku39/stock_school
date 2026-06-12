"""TWSE market data source (SRP: only fetching/parsing)."""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from datetime import date

from stock_school.domain.bar import Bar

UA = {"User-Agent": "StockSchool/1.0 (educational; +https://github.com/stock-school)"}


class TwseDataSource:
    """Concrete MarketDataSource — replaceable without touching renderers."""

    def fetch_month(self, stock_no: str, year: int, month: int) -> list[Bar]:
        url = (
            "https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY"
            f"?response=json&date={year}{month:02d}01&stockNo={stock_no}"
        )
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        rows = payload.get("data") or []
        bars: list[Bar] = []
        for row in rows:
            if len(row) < 7 or not str(row[0]).strip()[0].isdigit():
                continue
            bars.append(
                Bar(
                    d=row[0].replace("/", "-"),
                    volume=int(str(row[1]).replace(",", "")),
                    open=float(str(row[3]).replace(",", "")),
                    high=float(str(row[4]).replace(",", "")),
                    low=float(str(row[5]).replace(",", "")),
                    close=float(str(row[6]).replace(",", "")),
                )
            )
        return bars

    def fetch_bars(self, stock_no: str, *, months: int = 4, tail: int = 30) -> list[Bar]:
        today = date.today()
        all_bars: list[Bar] = []
        y, m = today.year, today.month
        for _ in range(months):
            try:
                all_bars.extend(self.fetch_month(stock_no, y, m))
            except (urllib.error.URLError, json.JSONDecodeError, ValueError):
                pass
            m -= 1
            if m == 0:
                m = 12
                y -= 1
        seen: set[str] = set()
        ordered: list[Bar] = []
        for b in reversed(all_bars):
            if b.d not in seen:
                seen.add(b.d)
                ordered.append(b)
        return ordered[-tail:]
