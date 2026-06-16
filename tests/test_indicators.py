"""Indicator math and generator-guard tests (Phase A of the chart checklist)."""
from __future__ import annotations

import logging

from conftest import FakeDataSource, make_bars
from stock_school.indicators.calculator import IndicatorCalculator
from stock_school.render.indicators import build_all_indicator_svgs

calc = IndicatorCalculator()


def test_sma_basic() -> None:
    out = calc.sma([1, 2, 3, 4, 5], 3)
    assert out[:2] == [None, None]
    assert out[2] == 2.0
    assert out[4] == 4.0


def test_ema_seeds_with_sma() -> None:
    out = calc.ema([1, 2, 3, 4, 5], 3)
    assert out[1] is None
    assert out[2] == 2.0  # seed = SMA of first 3
    assert out[4] is not None and out[4] > out[2]


def test_rsi_stays_in_range() -> None:
    values = [float(v) for v in range(1, 40)]
    rsi = calc.rsi(values, 14)
    for v in rsi:
        if v is not None:
            assert 0.0 <= v <= 100.0
    # 一路上漲時 RSI 應偏高
    assert rsi[-1] is not None and rsi[-1] > 70


def test_macd_lengths_align() -> None:
    values = [float(v) for v in range(1, 60)]
    dif, sig, hist = calc.macd(values)
    assert len(dif) == len(sig) == len(hist) == len(values)


def test_indicator_guard_warns_on_insufficient_data(caplog) -> None:
    with caplog.at_level(logging.WARNING):
        files = build_all_indicator_svgs(FakeDataSource(count=10))
    assert files == {}
    assert any("指標 SVG 略過" in rec.message for rec in caplog.records)


def test_indicator_full_set_with_enough_data() -> None:
    files = build_all_indicator_svgs(FakeDataSource(count=45))
    assert "2330-ma.svg" in files
    assert "0050-market.svg" in files
    assert all(svg.startswith("<svg") for svg in files.values())


def test_make_bars_helper_is_deterministic() -> None:
    assert make_bars(5) == make_bars(5)
