from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from stock_school.render.candles import build_all_candle_svgs


@dataclass
class CandleSvgGenerator:
    output_dir: Path
    generator_id: str = "candles"

    def generate(self) -> dict[str, str]:
        return build_all_candle_svgs()

    def artifact_path(self, filename: str) -> Path:
        return self.output_dir / filename
