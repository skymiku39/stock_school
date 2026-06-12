from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from stock_school.render.cases import build_all_case_svgs


@dataclass
class CaseSvgGenerator:
    output_dir: Path
    generator_id: str = "cases"

    def generate(self) -> dict[str, str]:
        return build_all_case_svgs()

    def artifact_path(self, filename: str) -> Path:
        return self.output_dir / filename
