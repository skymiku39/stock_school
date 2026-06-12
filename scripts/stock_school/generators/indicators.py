from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from stock_school.core.protocols import MarketDataSource
from stock_school.render.indicators import build_all_indicator_svgs


@dataclass
class IndicatorSvgGenerator:
    data_source: MarketDataSource
    output_dir: Path
    generator_id: str = "indicators"

    def generate(self) -> dict[str, str]:
        return build_all_indicator_svgs(self.data_source)

    def artifact_path(self, filename: str) -> Path:
        return self.output_dir / filename
