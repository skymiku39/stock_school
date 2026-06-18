"""Verify chart assets stay complete (Phase A/B of the chart checklist)."""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from conftest import ASSETS_DIR, DOCS_DIR, FakeDataSource
from stock_school.generators.quotes import QuoteSvgGenerator
from stock_school.render.candles import build_all_candle_svgs
from stock_school.render.cases import build_all_case_svgs
from stock_school.render.concepts import build_all_concept_svgs
from stock_school.render.indicators import build_all_indicator_svgs

_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(\s*([^)\s]+)(?:\s+\"[^\"]*\")?\s*\)")
_INLINE_CODE_RE = re.compile(r"`[^`]*`")
_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_EXTERNAL_PREFIXES = ("http://", "https://", "//", "data:")

EXPECTED_INDICATOR_FILES = {
    "2330-ma.svg",
    "2330-macd.svg",
    "2330-rsi.svg",
    "2330-kd.svg",
    "2330-bollinger.svg",
    "2330-volume-price.svg",
    "line-compare.svg",
    "revenue-demo.svg",
    "0050-market.svg",
}

EXPECTED_QUOTE_FILES = {
    f"{code}-{kind}.svg"
    for code in ("2330", "0050")
    for kind in ("quote-screen", "daily-k", "intraday-demo", "volume")
}


def _disk_svgs(subdir: str) -> set[str]:
    return {p.name for p in (ASSETS_DIR / subdir).glob("*.svg")}


def test_candle_filenames_match_disk() -> None:
    assert set(build_all_candle_svgs()) == _disk_svgs("candles")


def test_case_filenames_match_disk() -> None:
    assert set(build_all_case_svgs()) == _disk_svgs("cases")


def test_concept_filenames_match_disk() -> None:
    assert set(build_all_concept_svgs()) == _disk_svgs("concepts")


def test_indicator_generator_keys() -> None:
    files = build_all_indicator_svgs(FakeDataSource(count=45))
    assert set(files) == EXPECTED_INDICATOR_FILES


def test_quote_generator_keys() -> None:
    gen = QuoteSvgGenerator(data_source=FakeDataSource(count=30), output_dir=Path("."))
    assert set(gen.generate()) == EXPECTED_QUOTE_FILES


@pytest.mark.parametrize("svg_path", sorted(ASSETS_DIR.rglob("*.svg")), ids=lambda p: p.name)
def test_svg_wellformed(svg_path: Path) -> None:
    content = svg_path.read_text(encoding="utf-8").strip()
    assert content.startswith("<svg"), f"{svg_path} 不是以 <svg 開頭"
    assert content.endswith("</svg>"), f"{svg_path} 不是以 </svg> 結尾"
    assert "viewBox" in content, f"{svg_path} 缺少 viewBox"
    assert "aria-label" in content, f"{svg_path} 缺少 aria-label"


def _markdown_image_targets() -> list[tuple[Path, str]]:
    targets: list[tuple[Path, str]] = []
    for md_path in DOCS_DIR.rglob("*.md"):
        in_fence = False
        for raw in md_path.read_text(encoding="utf-8").splitlines():
            if _FENCE_RE.match(raw):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            line = _INLINE_CODE_RE.sub("", raw)
            for match in _IMAGE_RE.finditer(line):
                href = match.group(1)
                if href.startswith(_EXTERNAL_PREFIXES):
                    continue
                target = href.split("#", 1)[0]
                if target:
                    targets.append((md_path, target))
    return targets


def test_markdown_images_exist() -> None:
    missing = []
    for md_path, target in _markdown_image_targets():
        resolved = (md_path.parent / target).resolve()
        if not resolved.exists():
            missing.append(f"{md_path.relative_to(DOCS_DIR)} → {target}")
    assert not missing, "以下圖片引用找不到檔案:\n" + "\n".join(missing)


def test_teaching_svgs_are_referenced() -> None:
    referenced: set[Path] = set()
    for md_path, target in _markdown_image_targets():
        referenced.add((md_path.parent / target).resolve())
    orphans = []
    for svg_path in ASSETS_DIR.rglob("*.svg"):
        if svg_path.name == "logo.svg":  # 主題用，非教學正文引用
            continue
        if svg_path.resolve() not in referenced:
            orphans.append(str(svg_path.relative_to(ASSETS_DIR)))
    assert not orphans, "以下教學 SVG 未被任何 Markdown 引用:\n" + "\n".join(orphans)
