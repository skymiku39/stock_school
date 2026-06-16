from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from stock_school.render.concepts import build_all_concept_svgs


@dataclass
class ConceptSvgGenerator:
    output_dir: Path
    generator_id: str = "concepts"

    def generate(self) -> dict[str, str]:
        return build_all_concept_svgs()

    def artifact_path(self, filename: str) -> Path:
        return self.output_dir / filename
