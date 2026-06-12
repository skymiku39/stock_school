"""Quote-screen SVG generator (OCP: extend stocks without changing pipeline)."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from stock_school.core.protocols import MarketDataSource
from stock_school.render.quotes import (
    daily_k_svg,
    intraday_demo_svg,
    quote_screen_svg,
    volume_bars_svg,
)


@dataclass
class QuoteSvgGenerator:
    data_source: MarketDataSource
    output_dir: Path
    generator_id: str = "quotes"
    stocks: dict[str, str] = field(
        default_factory=lambda: {"2330": "台積電", "0050": "元大台灣50"}
    )

    def generate(self) -> dict[str, str]:
        files: dict[str, str] = {}
        for code, name in self.stocks.items():
            bars = self.data_source.fetch_bars(code, months=4, tail=30)
            if len(bars) < 2:
                continue
            last, prev = bars[-1], bars[-2]
            files[f"{code}-quote-screen.svg"] = quote_screen_svg(
                code=code, name=name, last=last, prev=prev
            )
            files[f"{code}-daily-k.svg"] = daily_k_svg(bars, code=code, name=name)
            files[f"{code}-intraday-demo.svg"] = intraday_demo_svg(
                code=code, name=name, prev_close=prev.close
            )
            vol = volume_bars_svg(bars, code=code, name=name)
            if vol:
                files[f"{code}-volume.svg"] = vol
        return files

    def artifact_path(self, filename: str) -> Path:
        return self.output_dir / filename
