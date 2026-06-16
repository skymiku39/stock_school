"""Indicator reference SVG renderers."""
from __future__ import annotations

import logging

from stock_school.core.protocols import MarketDataSource
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
rsi = _calc.rsi
stochastic = _calc.stochastic
bollinger = _calc.bollinger

T = DEFAULT_THEME
BLUE, BORDER, GRAY, GREEN, ORANGE, PURPLE, RED, TEAL = (
    T.blue,
    T.border,
    T.gray,
    T.green,
    T.orange,
    T.purple,
    T.red,
    T.teal,
)

CODE, NAME = "2330", "台積電"
W, H = 640, 360

MIN_BARS = 30

logger = logging.getLogger(__name__)


def ma_svg(bars) -> str:
    c = closes(bars)
    ma5, ma20, ma60 = sma(c, 5), sma(c, 20), sma(c, 60)
    pad = ChartPad(top=44, bottom=32)
    lo = min(b.low for b in bars)
    hi = max(b.high for b in bars)
    parts = title_block(f"{CODE} {NAME} — 均線 MA5 / MA20 / MA60", W, "TWSE 日 K · 教學用")
    candle_parts, _, _ = draw_candles(bars, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    for series, color, label in [
        (ma5, ORANGE, "MA5"),
        (ma20, BLUE, "MA20"),
        (ma60, PURPLE, "MA60"),
    ]:
        parts.append(
            draw_line_series(series, color=color, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi)
        )
    lx = W - 150
    for i, (color, label) in enumerate([(ORANGE, "MA5"), (BLUE, "MA20"), (PURPLE, "MA60")]):
        parts.append(
            f'<text x="{lx}" y="{54 + i * 14}" font-size="10" fill="{color}">— {label}</text>'
        )
    parts.append(footer_note(W, H, "資料：TWSE · 非即時 · 交叉需搭配量價確認"))
    return svg_header(f"{CODE} 均線", W, H, "".join(parts))


def macd_svg(bars) -> str:
    c = closes(bars)
    dif, sig, hist = macd(c)
    price_h = int(H * 0.58)
    macd_h = H - price_h
    pad_p = ChartPad(top=44, bottom=8)
    pad_m = ChartPad(top=price_h + 8, bottom=28)
    lo = min(b.low for b in bars)
    hi = max(b.high for b in bars)
    parts = title_block(f"{CODE} {NAME} — MACD (12, 26, 9)", W, "上：日 K · 下：DIF / Signal / 柱狀")
    candle_parts, _, _ = draw_candles(bars, width=W, height=price_h, pad=pad_p, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    parts.append(
        f'<line x1="48" y1="{price_h}" x2="{W - 16}" y2="{price_h}" stroke="{BORDER}"/>'
    )
    hvals = [h for h in hist if h is not None]
    dvals = [d for d in dif if d is not None] + [s for s in sig if s is not None]
    m_lo = min(hvals + dvals + [0]) * 1.1
    m_hi = max(hvals + dvals + [0]) * 1.1
    if m_lo == m_hi:
        m_lo, m_hi = -1, 1
    n = len(bars)
    gap = (W - 48 - 16) / n
    zero_y = pad_m.top + (macd_h - pad_m.top - pad_m.bottom) * (m_hi - 0) / (m_hi - m_lo)
    parts.append(
        f'<line x1="48" y1="{zero_y:.1f}" x2="{W - 16}" y2="{zero_y:.1f}" '
        f'stroke="#ccc" stroke-dasharray="3 3"/>'
    )
    for i, h in enumerate(hist):
        if h is None:
            continue
        cx = 48 + gap * (i + 0.5)
        y0 = zero_y
        y1 = pad_m.top + (macd_h - pad_m.top - pad_m.bottom) * (m_hi - h) / (m_hi - m_lo)
        color = RED if h >= 0 else GREEN
        top, bot = min(y0, y1), max(y0, y1)
        parts.append(
            f'<rect x="{cx - gap * 0.25:.1f}" y="{top:.1f}" width="{gap * 0.5:.1f}" '
            f'height="{max(bot - top, 1):.1f}" fill="{color}" opacity="0.7"/>'
        )
    parts.append(
        draw_line_series(dif, color=BLUE, width=W, height=macd_h, pad=pad_m, y_lo=m_lo, y_hi=m_hi)
    )
    parts.append(
        draw_line_series(
            sig, color=ORANGE, width=W, height=macd_h, pad=pad_m, y_lo=m_lo, y_hi=m_hi, dash="4 3"
        )
    )
    parts.append(
        f'<text x="{W - 140}" y="{price_h + 18}" font-size="10" fill="{BLUE}">— DIF</text>'
    )
    parts.append(
        f'<text x="{W - 140}" y="{price_h + 32}" font-size="10" fill="{ORANGE}">- - Signal</text>'
    )
    parts.append(footer_note(W, H, "資料：TWSE · 非即時"))
    return svg_header(f"{CODE} MACD", W, H, "".join(parts))


def rsi_svg(bars) -> str:
    c = closes(bars)
    r = rsi(c, 14)
    price_h = int(H * 0.62)
    rsi_h = H - price_h
    pad_p = ChartPad(top=44, bottom=8)
    pad_r = ChartPad(top=price_h + 8, bottom=28)
    lo = min(b.low for b in bars)
    hi = max(b.high for b in bars)
    parts = title_block(f"{CODE} {NAME} — RSI (14)", W, "70 超買 / 30 超賣參考線")
    candle_parts, _, _ = draw_candles(bars, width=W, height=price_h, pad=pad_p, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    parts.append(
        f'<line x1="48" y1="{price_h}" x2="{W - 16}" y2="{price_h}" stroke="{BORDER}"/>'
    )
    for level, label in [(70, "70"), (50, "50"), (30, "30")]:
        y = pad_r.top + (rsi_h - pad_r.top - pad_r.bottom) * (100 - level) / 100
        parts.append(
            f'<line x1="48" y1="{y:.1f}" x2="{W - 16}" y2="{y:.1f}" '
            f'stroke="#ddd" stroke-dasharray="4 3"/>'
        )
        parts.append(f'<text x="52" y="{y - 3:.1f}" font-size="9" fill="{GRAY}">{label}</text>')
    parts.append(
        draw_line_series(r, color=PURPLE, width=W, height=rsi_h, pad=pad_r, y_lo=0, y_hi=100)
    )
    parts.append(footer_note(W, H, "資料：TWSE · 強勢股可長期 >70"))
    return svg_header(f"{CODE} RSI", W, H, "".join(parts))


def kd_svg(bars) -> str:
    k_line, d_line = stochastic(bars)
    price_h = int(H * 0.62)
    kd_h = H - price_h
    pad_p = ChartPad(top=44, bottom=8)
    pad_k = ChartPad(top=price_h + 8, bottom=28)
    lo = min(b.low for b in bars)
    hi = max(b.high for b in bars)
    parts = title_block(f"{CODE} {NAME} — KD (9, 3, 3)", W, "80 超買 / 20 超賣")
    candle_parts, _, _ = draw_candles(bars, width=W, height=price_h, pad=pad_p, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    parts.append(
        f'<line x1="48" y1="{price_h}" x2="{W - 16}" y2="{price_h}" stroke="{BORDER}"/>'
    )
    for level in (80, 20):
        y = pad_k.top + (kd_h - pad_k.top - pad_k.bottom) * (100 - level) / 100
        parts.append(
            f'<line x1="48" y1="{y:.1f}" x2="{W - 16}" y2="{y:.1f}" '
            f'stroke="#ddd" stroke-dasharray="4 3"/>'
        )
    parts.append(
        draw_line_series(k_line, color=BLUE, width=W, height=kd_h, pad=pad_k, y_lo=0, y_hi=100)
    )
    parts.append(
        draw_line_series(
            d_line, color=ORANGE, width=W, height=kd_h, pad=pad_k, y_lo=0, y_hi=100, dash="4 3"
        )
    )
    parts.append(footer_note(W, H, "資料：TWSE · K 較敏感、D 較平滑"))
    return svg_header(f"{CODE} KD", W, H, "".join(parts))


def bollinger_svg(bars) -> str:
    c = closes(bars)
    mid, up, lo_b = bollinger(c, 20, 2.0)
    pad = ChartPad(top=44, bottom=32)
    lo = min(b.low for b in bars)
    hi = max(b.high for b in bars)
    for s in up + lo_b:
        if s is not None:
            lo = min(lo, s)
            hi = max(hi, s)
    parts = title_block(f"{CODE} {NAME} — 布林通道 (20, 2)", W, "中軌 = MA20")
    candle_parts, _, _ = draw_candles(bars, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    for series, color, dash in [(up, TEAL, ""), (mid, GRAY, "4 3"), (lo_b, TEAL, "")]:
        parts.append(
            draw_line_series(
                series, color=color, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi, dash=dash
            )
        )
    parts.append(footer_note(W, H, "資料：TWSE · 觸軌需看趨勢方向"))
    return svg_header(f"{CODE} 布林", W, H, "".join(parts))


def volume_price_svg(bars) -> str:
    price_h = int(H * 0.68)
    vol_h = H - price_h
    pad_p = ChartPad(top=44, bottom=8)
    pad_v = ChartPad(top=price_h + 8, bottom=28)
    lo = min(b.low for b in bars)
    hi = max(b.high for b in bars)
    parts = title_block(f"{CODE} {NAME} — 量價圖", W, "上：日 K · 下：成交量（紅漲黑跌）")
    candle_parts, _, _ = draw_candles(bars, width=W, height=price_h, pad=pad_p, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    parts.append(
        f'<line x1="48" y1="{price_h}" x2="{W - 16}" y2="{price_h}" stroke="{BORDER}"/>'
    )
    vmax = max(b.volume for b in bars) or 1
    n = len(bars)
    gap = (W - 48 - 16) / n
    ch = vol_h - pad_v.top - pad_v.bottom
    for i, b in enumerate(bars):
        bull = b.close >= b.open
        color = RED if bull else "#212121"
        h = ch * b.volume / vmax
        x = 48 + gap * i + gap * 0.2
        y = pad_v.top + ch - h
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{gap * 0.6:.1f}" '
            f'height="{h:.1f}" fill="{color}" opacity="0.85"/>'
        )
    parts.append(footer_note(W, H, "資料：TWSE · 價漲量增 / 價漲量縮對照閱讀"))
    return svg_header(f"{CODE} 量價", W, H, "".join(parts))


def line_compare_svg(bars) -> str:
    """Line vs bar vs candle on same closes (last 15 bars)."""
    tail = bars[-15:]
    c = closes(tail)
    lo, hi = min(c), max(c)
    span = hi - lo or 1
    panel_w = (W - 64) // 3
    parts = title_block("線圖 vs 美國線 vs K 線（同一組收盤，教學示意）", W)
    labels = ["線圖（收盤價）", "美國線", "K 線"]
    for pi, label in enumerate(labels):
        x0 = 48 + pi * (panel_w + 8)
        y0, ph = 50, 200
        parts.append(
            f'<text x="{x0}" y="{y0 - 6}" font-size="11" font-weight="bold" fill="#212121">{label}</text>'
        )
        parts.append(
            f'<rect x="{x0}" y="{y0}" width="{panel_w}" height="{ph}" '
            f'fill="#fafafa" stroke="{BORDER}"/>'
        )
        n = len(tail)
        if pi == 0:
            pts = []
            for i, cl in enumerate(c):
                px = x0 + panel_w * (i + 0.5) / n
                py = y0 + ph * (hi - cl) / span
                pts.append(f"{px:.1f},{py:.1f}")
            parts.append(
                f'<polyline fill="none" stroke="{BLUE}" stroke-width="2" points="{" ".join(pts)}"/>'
            )
        elif pi == 1:
            for i, b in enumerate(tail):
                cx = x0 + panel_w * (i + 0.5) / n
                y_h = y0 + ph * (hi - b.high) / span
                y_l = y0 + ph * (hi - b.low) / span
                y_o = y0 + ph * (hi - b.open) / span
                y_c = y0 + ph * (hi - b.close) / span
                parts.append(
                    f'<line x1="{cx:.1f}" y1="{y_h:.1f}" x2="{cx:.1f}" y2="{y_l:.1f}" stroke="#666"/>'
                )
                parts.append(
                    f'<line x1="{cx - 4:.1f}" y1="{y_o:.1f}" x2="{cx:.1f}" y2="{y_o:.1f}" stroke="#666"/>'
                )
                parts.append(
                    f'<line x1="{cx:.1f}" y1="{y_c:.1f}" x2="{cx + 4:.1f}" y2="{y_c:.1f}" stroke="#666"/>'
                )
        else:
            bw = max(panel_w / n * 0.55, 2)
            for i, b in enumerate(tail):
                cx = x0 + panel_w * (i + 0.5) / n
                color = RED if b.close >= b.open else "#212121"
                y_h = y0 + ph * (hi - b.high) / span
                y_l = y0 + ph * (hi - b.low) / span
                y_o = y0 + ph * (hi - b.open) / span
                y_c = y0 + ph * (hi - b.close) / span
                parts.append(
                    f'<line x1="{cx:.1f}" y1="{y_h:.1f}" x2="{cx:.1f}" y2="{y_l:.1f}" stroke="{color}"/>'
                )
                top, bot = min(y_o, y_c), max(y_o, y_c)
                parts.append(
                    f'<rect x="{cx - bw / 2:.1f}" y="{top:.1f}" width="{bw:.1f}" '
                    f'height="{max(bot - top, 1):.1f}" fill="{color}"/>'
                )
    parts.append(footer_note(W, H, f"資料：{CODE} TWSE 近 15 日 · 教學用"))
    return svg_header("線圖比較", W, H, "".join(parts))


def revenue_demo_svg() -> str:
    """Synthetic monthly revenue from revenue-turn case."""
    months = ["M-3", "M-2", "M-1", "M0"]
    revenue = [2800, 2650, 2720, 3100]
    yoy = [-5.0, -8.2, -6.0, 2.0]
    max_r = max(revenue)
    parts = title_block("月營收柱狀 + YoY 折線（教學合成數據）", W, "案例：營收轉折")
    base_y, ch = 260, 180
    gap = (W - 96) / len(months)
    for i, (m, r) in enumerate(zip(months, revenue)):
        x = 48 + gap * i + gap * 0.25
        h = ch * r / max_r
        y = base_y - h
        parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{gap * 0.5:.1f}" height="{h:.1f}" fill="{BLUE}" opacity="0.85"/>'
        )
        parts.append(
            f'<text x="{x + gap * 0.25:.1f}" y="{base_y + 16:.1f}" font-size="10" '
            f'text-anchor="middle" fill="{GRAY}">{m}</text>'
        )
        parts.append(
            f'<text x="{x + gap * 0.25:.1f}" y="{y - 6:.1f}" font-size="9" '
            f'text-anchor="middle" fill="{GRAY}">{r}</text>'
        )
    y_min, y_max = min(yoy), max(yoy)
    y_span = y_max - y_min or 1
    pts = []
    for i, v in enumerate(yoy):
        px = 48 + gap * (i + 0.5)
        py = 120 + 80 * (y_max - v) / y_span
        pts.append(f"{px:.1f},{py:.1f}")
    parts.append(
        f'<polyline fill="none" stroke="{ORANGE}" stroke-width="2" points="{" ".join(pts)}"/>'
    )
    for i, v in enumerate(yoy):
        px = 48 + gap * (i + 0.5)
        py = 120 + 80 * (y_max - v) / y_span
        parts.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3" fill="{ORANGE}"/>')
        parts.append(
            f'<text x="{px:.1f}" y="{py - 8:.1f}" font-size="9" text-anchor="middle" fill="{ORANGE}">{v:+.1f}%</text>'
        )
    parts.append(f'<text x="52" y="110" font-size="10" fill="{ORANGE}">— YoY%</text>')
    parts.append(footer_note(W, H, "合成教學數據 · 見營收轉折案例"))
    return svg_header("月營收示意", W, H, "".join(parts))


def market_index_svg(bars) -> str:
    """Use 0050 bars as market proxy."""
    pad = ChartPad(top=44, bottom=32)
    lo = min(b.low for b in bars)
    hi = max(b.high for b in bars)
    c = closes(bars)
    ma20 = sma(c, 20)
    parts = title_block("0050 元大台灣50 — 大盤代理走勢", W, "加權指數常用類似日 K 閱讀")
    candle_parts, _, _ = draw_candles(bars, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi)
    parts.extend(candle_parts)
    parts.append(
        draw_line_series(ma20, color=BLUE, width=W, height=H, pad=pad, y_lo=lo, y_hi=hi, dash="4 3")
    )
    parts.append(footer_note(W, H, "資料：TWSE · 0050 追蹤台灣50"))
    return svg_header("0050 大盤", W, H, "".join(parts))


def build_all_indicator_svgs(data_source: MarketDataSource) -> dict[str, str]:
    """Return filename → SVG content for indicator assets."""
    bars = data_source.fetch_bars(CODE, months=8, tail=45)
    if len(bars) < MIN_BARS:
        logger.warning(
            "指標 SVG 略過：%s 僅取得 %d 根 K 線（需 >= %d），可能因 TWSE 無回應或假日無資料",
            CODE,
            len(bars),
            MIN_BARS,
        )
        return {}
    files = {
        "2330-ma.svg": ma_svg(bars),
        "2330-macd.svg": macd_svg(bars),
        "2330-rsi.svg": rsi_svg(bars),
        "2330-kd.svg": kd_svg(bars),
        "2330-bollinger.svg": bollinger_svg(bars),
        "2330-volume-price.svg": volume_price_svg(bars),
        "line-compare.svg": line_compare_svg(bars),
        "revenue-demo.svg": revenue_demo_svg(),
    }
    bars_50 = data_source.fetch_bars("0050", months=6, tail=40)
    if bars_50:
        files["0050-market.svg"] = market_index_svg(bars_50)
    else:
        logger.warning("0050 大盤 SVG 略過：TWSE 無回應，將沿用既有檔案")
    return files
