"""Case-study SVG renderers (synthetic educational data)."""
from __future__ import annotations

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
closes = _calc.closes
sma = _calc.sma
macd = _calc.macd

T = DEFAULT_THEME
BLUE, BORDER, GRAY, GREEN, ORANGE, PURPLE, RED = (
    T.blue,
    T.border,
    T.gray,
    T.green,
    T.orange,
    T.purple,
    T.red,
)

W, H = 640, 380


def _bar(d: str, o: float, h: float, l: float, c: float, v: int = 3000) -> Bar:
    return Bar(d=d, open=o, high=h, low=l, close=c, volume=v * 1000)


def hammer_ma_bars() -> list[Bar]:
    """Decline to support + hammer at ~100 with MA20."""
    bars: list[Bar] = []
    price = 120.0
    for i in range(22):
        drift = -0.8 + (i % 3) * 0.15
        o = price
        c = price + drift
        h = max(o, c) + 0.6
        l = min(o, c) - 0.8
        bars.append(_bar(f"D{i - 21}", o, h, l, c, 2500 + i * 30))
        price = c
    # hammer: O101 H102 L96 C101.5 vol up
    bars.append(_bar("D0", 101, 102, 96, 101.5, 4200))
    return bars


def hammer_ma_svg() -> str:
    bars = hammer_ma_bars()
    c = closes(bars)
    ma20 = sma(c, 20)
    pad = ChartPad(top=44, bottom=36)
    lo = min(b.low for b in bars) - 2
    hi = max(b.high for b in bars) + 2
    parts = title_block("案例：低檔鎚子 + MA20（合成數據）", W, "B 公司 · 支撐 98～100 · 最後一根紅K鎚子")
    candle_parts, _, _ = draw_candles(bars, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    parts.append(
        draw_line_series(ma20, color=BLUE, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi)
    )
    # support zone
    y98 = pad.top + (H - pad.top - pad.bottom) * (hi - 98) / (hi - lo)
    y100 = pad.top + (H - pad.top - pad.bottom) * (hi - 100) / (hi - lo)
    parts.append(
        f'<rect x="48" y="{y100:.1f}" width="{W - 64}" height="{y98 - y100:.1f}" '
        f'fill="#fff3e0" opacity="0.5"/>'
    )
    parts.append(f'<text x="52" y="{y100 - 4:.1f}" font-size="9" fill="{ORANGE}">支撐區 98～100</text>')
    last = bars[-1]
    cx = 48 + (W - 64) * (len(bars) - 0.5) / len(bars)
    parts.append(f'<text x="{cx:.0f}" y="{pad.top + 12}" font-size="10" fill="{RED}" text-anchor="middle">鎚子</text>')
    parts.append(footer_note(W, H, "合成教學數據 · 非真實個股"))
    return svg_header("鎚子均線案例", W, H, "".join(parts))


def macd_divergence_bars() -> list[Bar]:
    """Uptrend with second price high > first, MACD weakening."""
    bars: list[Bar] = []
    # base rise 80 -> 100
    prices = [
        80, 82, 84, 83, 86, 88, 90, 89, 92, 94,
        96, 95, 98, 100, 99, 101, 103, 102, 104, 105,
        104, 103, 102,
    ]
    for i, c in enumerate(prices):
        o = c - 0.5 if i % 2 == 0 else c + 0.3
        h = max(o, c) + 0.8
        l = min(o, c) - 0.6
        vol = 3000 if i < 18 else 2200
        bars.append(_bar(f"D{i - len(prices)}", o, h, l, c, vol))
    return bars


def macd_divergence_svg() -> str:
    bars = macd_divergence_bars()
    c = closes(bars)
    dif, sig, hist = macd(c)
    price_h = int(H * 0.55)
    macd_h = H - price_h
    pad_p = ChartPad(top=44, bottom=6)
    pad_m = ChartPad(top=price_h + 6, bottom=32)
    lo = min(b.low for b in bars) - 1
    hi = max(b.high for b in bars) + 1
    parts = title_block("案例：MACD 頂背離（合成數據）", W, "F 公司 · 價格 100→105 新高 · DIF 未創高")
    candle_parts, _, _ = draw_candles(bars, width=W, height=price_h, pad=pad_p, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    # annotate peaks
    peaks = [13, 19]  # ~100 and ~105
    n = len(bars)
    gap = (W - 64) / n
    for idx, label in zip(peaks, ["高點1 ~100", "高點2 ~105"]):
        cx = 48 + gap * (idx + 0.5)
        cy = pad_p.top + 14
        parts.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="9" fill="{RED}" text-anchor="middle">{label}</text>')
    parts.append(f'<line x1="48" y1="{price_h}" x2="{W - 16}" y2="{price_h}" stroke="{BORDER}"/>')
    hvals = [h for h in hist if h is not None]
    dvals = [d for d in dif if d is not None]
    m_lo = min(hvals + dvals + [0]) * 1.2
    m_hi = max(hvals + dvals + [0]) * 1.2
    parts.append(
        draw_line_series(dif, color=BLUE, width=W, height=macd_h, pad=pad_m, y_lo=m_lo, y_hi=m_hi)
    )
    for idx, label in zip(peaks, ["DIF 2.5", "DIF 2.0↓"]):
        cx = 48 + gap * (idx + 0.5)
        parts.append(
            f'<text x="{cx:.1f}" y="{price_h + 20}" font-size="9" fill="{PURPLE}" text-anchor="middle">{label}</text>'
        )
    parts.append(
        f'<text x="52" y="{price_h + 36}" font-size="10" fill="{RED}">頂背離：價新高、MACD 未新高</text>'
    )
    parts.append(footer_note(W, H, "合成教學數據 · 背離是警訊非賣出指令"))
    return svg_header("MACD背離案例", W, H, "".join(parts))


def gap_breakout_bars() -> list[Bar]:
    bars: list[Bar] = []
    # 18 days consolidation 85-90
    import random
    random.seed(42)
    for i in range(18):
        base = 87 + (i % 4) * 0.5
        o = base + random.uniform(-0.5, 0.5)
        c = base + random.uniform(-1, 1)
        h = max(o, c) + random.uniform(0.2, 0.8)
        l = min(o, c) - random.uniform(0.2, 0.8)
        h = min(h, 90)
        l = max(l, 85)
        bars.append(_bar(f"D{i - 21}", o, h, l, c, 2800 + random.randint(0, 400)))
    # D-1
    bars.append(_bar("D-1", 89, 90, 87, 88, 3200))
    # D0 gap up
    bars.append(_bar("D0", 93, 96, 92, 95, 8500))
    bars.append(_bar("D+1", 94, 95, 88, 89, 6100))
    bars.append(_bar("D+2", 88, 90, 86, 87, 4800))
    return bars


def gap_breakout_svg() -> str:
    bars = gap_breakout_bars()
    pad = ChartPad(top=44, bottom=36)
    lo = 84
    hi = 97
    parts = title_block("案例：突破缺口 → 假突破（合成數據）", W, "整理 85～90 · D0 跳空 · D+2 回補缺口")
    candle_parts, _, _ = draw_candles(bars, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    # gap zone 90-92
    y90 = pad.top + (H - pad.top - pad.bottom) * (hi - 90) / (hi - lo)
    y92 = pad.top + (H - pad.top - pad.bottom) * (hi - 92) / (hi - lo)
    parts.append(
        f'<rect x="48" y="{y92:.1f}" width="{W - 64}" height="{y90 - y92:.1f}" '
        f'fill="#e3f2fd" opacity="0.6"/>'
    )
    parts.append(f'<text x="52" y="{y92 - 4:.1f}" font-size="9" fill="{BLUE}">缺口 90～92</text>')
    # consolidation box
    y85 = pad.top + (H - pad.top - pad.bottom) * (hi - 85) / (hi - lo)
    parts.append(
        f'<rect x="48" y="{y90:.1f}" width="{(W - 64) * 0.65:.1f}" height="{y85 - y90:.1f}" '
        f'fill="none" stroke="{GRAY}" stroke-dasharray="4 3"/>'
    )
    parts.append(f'<text x="100" y="{y85 + 14:.1f}" font-size="9" fill="{GRAY}">整理區</text>')
    n = len(bars)
    gap_w = (W - 64) / n
    for label, idx in [("D0 跳空", -3), ("回補", -1)]:
        cx = 48 + gap_w * (n + idx + 0.5)
        parts.append(
            f'<text x="{cx:.1f}" y="{pad.top + 12}" font-size="9" fill="{RED}" text-anchor="middle">{label}</text>'
        )
    parts.append(footer_note(W, H, "合成教學數據 · 突破需量+站穩"))
    return svg_header("假突破案例", W, H, "".join(parts))


def dca_drawdown_bars() -> list[Bar]:
    """Synthetic 0050-like long trend with drawdown for DCA illustration."""
    bars: list[Bar] = []
    import math
    for i in range(48):
        t = i / 47
        base = 140 + 25 * math.sin(t * 3.2) + 15 * t
        if 20 <= i <= 28:
            base -= (i - 20) * 1.2  # drawdown window
        o = base
        c = base + (0.4 if i % 2 else -0.3)
        h = max(o, c) + 0.8
        l = min(o, c) - 0.8
        bars.append(_bar(f"M{i}", o, h, l, c, 5000))
    return bars


def dca_drawdown_svg() -> str:
    bars = dca_drawdown_bars()
    pad = ChartPad(top=44, bottom=36)
    lo = min(b.low for b in bars) - 3
    hi = max(b.high for b in bars) + 3
    parts = title_block("0050 定期定額示意（合成長期走勢）", W, "▼ 標記為定額買進日 · 回檔時仍持續扣款")
    candle_parts, _, _ = draw_candles(bars, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    n = len(bars)
    gap = (W - 64) / n
    for i in range(0, n, 6):
        cx = 48 + gap * (i + 0.5)
        cy = pad.top + (H - pad.top - pad.bottom) * (hi - bars[i].close) / (hi - lo) + 12
        parts.append(f'<polygon points="{cx:.0f},{cy:.0f} {cx - 5:.0f},{cy - 10:.0f} {cx + 5:.0f},{cy - 10:.0f}" fill="{GREEN}"/>')
    parts.append(footer_note(W, H, "合成教學數據 · 閒錢定額 · 非保證獲利"))
    return svg_header("定額案例", W, H, "".join(parts))


def etf_vs_stock_svg() -> str:
    """Side by side volatility: single stock vs 0050-like smoother line."""
    import math
    parts = title_block("個股 vs ETF 波動示意（合成）", W, "左：單一個股 · 右：0050 類 ETF")
    pw = (W - 72) // 2
    for pi, (label, amp) in enumerate([("個股（集中風險）", 8), ("0050（分散大盤）", 3)]):
        x0 = 48 + pi * (pw + 16)
        y0, ph = 56, 240
        parts.append(f'<text x="{x0}" y="{y0 - 8}" font-size="11" font-weight="bold">{label}</text>')
        parts.append(f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="#fafafa" stroke="{BORDER}"/>')
        pts = []
        for i in range(30):
            v = 100 + amp * math.sin(i / 4) + (i * 0.3 if pi else i * 0.15)
            px = x0 + pw * (i + 0.5) / 30
            py = y0 + ph * 0.85 - (v - 90) / 40 * ph * 0.7
            pts.append(f"{px:.1f},{py:.1f}")
        color = RED if pi == 0 else BLUE
        parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="2" points="{" ".join(pts)}"/>')
    parts.append(footer_note(W, H, "合成示意 · ETF 波動通常較個股平滑"))
    return svg_header("ETF vs 個股", W, H, "".join(parts))


def build_all_case_svgs() -> dict[str, str]:
    """Return filename → SVG content for case-study assets."""
    return {
        "hammer-ma.svg": hammer_ma_svg(),
        "macd-divergence.svg": macd_divergence_svg(),
        "gap-breakout.svg": gap_breakout_svg(),
        "etf-dca-drawdown.svg": dca_drawdown_svg(),
        "etf-vs-stock.svg": etf_vs_stock_svg(),
    }
