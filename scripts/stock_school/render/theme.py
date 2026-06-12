"""Visual theme tokens (台股慣例：紅漲綠跌)."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Theme:
    red: str = "#e53935"
    green: str = "#00897b"
    black: str = "#212121"
    gray: str = "#666666"
    light: str = "#f5f5f5"
    border: str = "#dddddd"
    blue: str = "#1565c0"
    orange: str = "#ff9800"
    purple: str = "#7b1fa2"
    teal: str = "#00897b"


DEFAULT_THEME = Theme()
