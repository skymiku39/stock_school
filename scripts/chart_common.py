"""Backward-compatible shim — import from stock_school package."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from stock_school.data.twse import TwseDataSource
from stock_school.domain.bar import Bar
from stock_school.indicators.calculator import IndicatorCalculator
from stock_school.render.svg_primitives import (
    ChartPad,
    draw_candles,
    draw_line_series,
    footer_note,
    svg_header,
    title_block,
)
from stock_school.render.theme import DEFAULT_THEME

_calc = IndicatorCalculator()
fetch_bars = lambda stock_no, months=8, tail=60: TwseDataSource().fetch_bars(
    stock_no, months=months, tail=tail
)
fetch_recent_bars = lambda stock_no, months=4: TwseDataSource().fetch_bars(
    stock_no, months=months, tail=30
)
closes = _calc.closes
sma = _calc.sma
ema = _calc.ema
ema_series = _calc.ema_series
macd = _calc.macd
rsi = _calc.rsi
stochastic = _calc.stochastic
bollinger = _calc.bollinger

T = DEFAULT_THEME
RED = T.red
GREEN = T.green
BLACK = T.black
GRAY = T.gray
BORDER = T.border
BLUE = T.blue
ORANGE = T.orange
PURPLE = T.purple
TEAL = T.teal

__all__ = [
    "Bar",
    "BLACK",
    "BLUE",
    "BORDER",
    "ChartPad",
    "GRAY",
    "GREEN",
    "ORANGE",
    "PURPLE",
    "RED",
    "TEAL",
    "bollinger",
    "closes",
    "draw_candles",
    "draw_line_series",
    "ema",
    "ema_series",
    "fetch_bars",
    "fetch_recent_bars",
    "footer_note",
    "macd",
    "rsi",
    "sma",
    "stochastic",
    "svg_header",
    "title_block",
]
