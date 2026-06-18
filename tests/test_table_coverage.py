"""看表章節 A 級結構檢查。

對齊 docs/STYLE-GUIDE.md 的「看表頁 A 模板」：每個 03-tables 教學頁
（index 除外）必須包含「在哪裡看到」「閱讀步驟」「常見誤」「讀完請做」
「手算／導覽練習」等關鍵小節，避免出現「標題寫怎麼看、內容卻是速查」的退化。
"""
from __future__ import annotations

from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TABLES_DIR = REPO_ROOT / "docs" / "03-tables"

REQUIRED_MARKERS = {
    "在哪裡看到": ("在哪裡看到", "在哪裡看"),
    "閱讀步驟": ("閱讀步驟", "怎麼讀", "閱讀方法", "閱讀順序", "先做這三件事"),
    "常見誤區": ("## 常見誤區", "## 常見誤解", "## 陷阱"),
    "讀完請做": ("讀完請做", "讀完接著", "延伸案例"),
    "手算或導覽練習": ("## 手算一例", "## 導覽練習一例"),
}


def _table_pages() -> list[Path]:
    return sorted(p for p in TABLES_DIR.glob("*.md") if p.name != "index.md")


@pytest.mark.parametrize("page", _table_pages(), ids=lambda p: p.name)
def test_table_page_follows_a_grade_template(page: Path):
    text = page.read_text(encoding="utf-8")
    missing = [
        name
        for name, variants in REQUIRED_MARKERS.items()
        if not any(v in text for v in variants)
    ]
    assert not missing, f"{page.name} 缺少 A 模板區塊：{missing}"
