"""Quote-screen SVG renderers."""
from __future__ import annotations

from stock_school.domain.bar import Bar
from stock_school.render.svg_primitives import svg_header
from stock_school.render.theme import DEFAULT_THEME, Theme


def daily_k_svg(
    bars: list[Bar],
    *,
    code: str,
    name: str,
    width: int = 640,
    height: int = 320,
    theme: Theme = DEFAULT_THEME,
) -> str:
    if not bars:
        return svg_header(f"{code} 日K（無資料）", width, height, "")

    pad_l, pad_r, pad_t, pad_b = 48, 16, 36, 40
    chart_w = width - pad_l - pad_r
    chart_h = height - pad_t - pad_b
    lo = min(b.low for b in bars)
    hi = max(b.high for b in bars)
    span = hi - lo or 1
    n = len(bars)
    gap = chart_w / n
    body_w = max(gap * 0.55, 2)

    def y_price(p: float) -> float:
        return pad_t + chart_h * (hi - p) / span

    parts = [
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{pad_l}" y="22" font-size="14" font-weight="bold" fill="{theme.black}">'
        f"{code} {name} — 日 K（近 {n} 個交易日，TWSE）</text>",
        f'<line x1="{pad_l}" y1="{pad_t + chart_h}" x2="{width - pad_r}" y2="{pad_t + chart_h}" stroke="{theme.border}"/>',
    ]
    for i in range(5):
        p = lo + span * i / 4
        y = y_price(p)
        parts.append(
            f'<line x1="{pad_l}" y1="{y:.1f}" x2="{width - pad_r}" y2="{y:.1f}" stroke="#eeeeee"/>'
        )
        parts.append(
            f'<text x="{pad_l - 6}" y="{y + 4:.1f}" font-size="10" text-anchor="end" fill="{theme.gray}">{p:.0f}</text>'
        )

    for i, b in enumerate(bars):
        cx = pad_l + gap * i + gap / 2
        bull = b.close >= b.open
        color = theme.red if bull else theme.black
        y_h, y_l = y_price(b.high), y_price(b.low)
        y_o, y_c = y_price(b.open), y_price(b.close)
        parts.append(
            f'<line x1="{cx:.1f}" y1="{y_h:.1f}" x2="{cx:.1f}" y2="{y_l:.1f}" stroke="{color}" stroke-width="1"/>'
        )
        top, bot = min(y_o, y_c), max(y_o, y_c)
        h = max(bot - top, 1)
        parts.append(
            f'<rect x="{cx - body_w / 2:.1f}" y="{top:.1f}" width="{body_w:.1f}" height="{h:.1f}" fill="{color}"/>'
        )

    last = bars[-1]
    prev = bars[-2] if len(bars) > 1 else last
    chg = last.close - prev.close
    pct = chg / prev.close * 100 if prev.close else 0
    clr = theme.red if chg >= 0 else theme.green
    parts.append(
        f'<text x="{width - pad_r}" y="22" font-size="12" text-anchor="end" fill="{clr}">'
        f"收 {last.close:.2f}  ({chg:+.2f}, {pct:+.2f}%)</text>"
    )
    parts.append(
        f'<text x="{pad_l}" y="{height - 8}" font-size="10" fill="{theme.gray}">'
        f"資料：TWSE 日行情 · 教學用 · 非即時</text>"
    )
    return svg_header(f"{code} {name} 日K", width, height, "".join(parts))


def intraday_demo_svg(
    *,
    code: str,
    name: str,
    prev_close: float,
    width: int = 640,
    height: int = 280,
    theme: Theme = DEFAULT_THEME,
) -> str:
    pad_l, pad_r, pad_t, pad_b = 48, 16, 36, 36
    cw, ch = width - pad_l - pad_r, height - pad_t - pad_b
    pts = [
        0, 0.4, 0.55, 0.35, 0.2, 0.15, 0.25, 0.3, 0.22, 0.18,
        0.12, 0.08, 0.05, 0.1, 0.15, 0.2, 0.28, 0.35, 0.42, 0.38,
        0.45, 0.52, 0.48, 0.55, 0.6, 0.58, 0.62,
    ]
    amp = prev_close * 0.012
    base = prev_close
    prices = [base + (p - 0.3) * amp * 2 for p in pts]
    lo, hi = min(prices), max(prices)
    span = hi - lo or 1

    def xy(i: int, price: float) -> tuple[float, float]:
        x = pad_l + cw * i / (len(pts) - 1)
        y = pad_t + ch * (hi - price) / span
        return x, y

    avg_prices = []
    s = 0.0
    for i, p in enumerate(prices):
        s += p
        avg_prices.append(s / (i + 1))

    line = " ".join(f"{xy(i, p)[0]:.1f},{xy(i, p)[1]:.1f}" for i, p in enumerate(prices))
    avg_line = " ".join(f"{xy(i, p)[0]:.1f},{xy(i, p)[1]:.1f}" for i, p in enumerate(avg_prices))
    y_ref = pad_t + ch * (hi - prev_close) / span

    parts = [
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{pad_l}" y="22" font-size="14" font-weight="bold" fill="{theme.black}">'
        f"{code} {name} — 分時走勢（教學示意）</text>",
        f'<line x1="{pad_l}" y1="{y_ref:.1f}" x2="{width - pad_r}" y2="{y_ref:.1f}" '
        f'stroke="#999" stroke-dasharray="4 3"/>',
        f'<text x="{width - pad_r}" y="{y_ref - 4:.1f}" font-size="9" text-anchor="end" fill="{theme.gray}">昨收 {prev_close:.0f}</text>',
        f'<polyline fill="none" stroke="{theme.red}" stroke-width="2" points="{line}"/>',
        f'<polyline fill="none" stroke="{theme.orange}" stroke-width="1.5" stroke-dasharray="5 3" points="{avg_line}"/>',
        f'<text x="{pad_l + 4}" y="{pad_t + 14}" font-size="10" fill="{theme.red}">■ 成交價</text>',
        f'<text x="{pad_l + 84}" y="{pad_t + 14}" font-size="10" fill="{theme.orange}">- - 均價</text>',
        f'<text x="{pad_l}" y="{height - 10}" font-size="10" fill="{theme.gray}">09:00 ─────────────── 13:30（非即時 tick 重播）</text>',
    ]
    return svg_header(f"{code} 分時示意", width, height, "".join(parts))


def quote_screen_svg(
    *,
    code: str,
    name: str,
    last: Bar,
    prev: Bar,
    width: int = 720,
    height: int = 420,
    theme: Theme = DEFAULT_THEME,
) -> str:
    chg = last.close - prev.close
    pct = chg / prev.close * 100 if prev.close else 0
    clr = theme.red if chg >= 0 else theme.green
    spread = max(last.close * 0.001, 0.5)
    bids = [(last.close - spread * i, 100 + i * 37) for i in range(1, 6)]
    asks = [(last.close + spread * i, 88 + i * 41) for i in range(1, 6)]

    parts = [
        f'<rect width="{width}" height="{height}" fill="#fafafa"/>',
        f'<rect x="0" y="0" width="{width}" height="72" fill="#ffffff" stroke="{theme.border}"/>',
        f'<text x="16" y="28" font-size="18" font-weight="bold" fill="{theme.black}">{code} {name}</text>',
        f'<text x="16" y="58" font-size="28" font-weight="bold" fill="{clr}">{last.close:.2f}</text>',
        f'<text x="130" y="58" font-size="16" fill="{clr}">{chg:+.2f} ({pct:+.2f}%)</text>',
        f'<text x="320" y="32" font-size="11" fill="{theme.gray}">開 {last.open:.2f}</text>',
        f'<text x="320" y="50" font-size="11" fill="{theme.gray}">高 {last.high:.2f}</text>',
        f'<text x="400" y="32" font-size="11" fill="{theme.gray}">低 {last.low:.2f}</text>',
        f'<text x="400" y="50" font-size="11" fill="{theme.gray}">昨收 {prev.close:.2f}</text>',
        f'<text x="480" y="32" font-size="11" fill="{theme.gray}">單量 —</text>',
        f'<text x="480" y="50" font-size="11" fill="{theme.gray}">總量 {last.volume // 1000:,} 張</text>',
        f'<rect x="12" y="84" width="460" height="220" fill="#ffffff" stroke="{theme.border}"/>',
        f'<text x="24" y="108" font-size="12" fill="{theme.gray}">圖表區（可切換 分時 / 日K / 量價）</text>',
        f'<text x="24" y="128" font-size="10" fill="{theme.gray}">→ 見本頁下方 {code} 範例圖</text>',
        f'<rect x="488" y="84" width="220" height="220" fill="#ffffff" stroke="{theme.border}"/>',
        f'<text x="500" y="104" font-size="12" font-weight="bold" fill="{theme.black}">五檔報價（示意）</text>',
    ]
    y0 = 124
    parts.append(f'<text x="500" y="{y0}" font-size="10" fill="{theme.gray}">委賣</text>')
    parts.append(f'<text x="620" y="{y0}" font-size="10" fill="{theme.gray}">張數</text>')
    for i, (px, vol) in enumerate(reversed(asks)):
        y = y0 + 18 + i * 18
        parts.append(f'<text x="500" y="{y}" font-size="11" fill="{theme.green}">{px:.2f}</text>')
        parts.append(f'<text x="620" y="{y}" font-size="11" fill="{theme.gray}">{vol}</text>')
    parts.append(f'<line x1="492" y1="{y0 + 100}" x2="704" y2="{y0 + 100}" stroke="{theme.border}"/>')
    parts.append(f'<text x="500" y="{y0 + 118}" font-size="10" fill="{theme.gray}">委買</text>')
    for i, (px, vol) in enumerate(bids):
        y = y0 + 136 + i * 18
        parts.append(f'<text x="500" y="{y}" font-size="11" fill="{theme.red}">{px:.2f}</text>')
        parts.append(f'<text x="620" y="{y}" font-size="11" fill="{theme.gray}">{vol}</text>')
    parts.append(f'<rect x="12" y="312" width="696" height="96" fill="#ffffff" stroke="{theme.border}"/>')
    parts.append(f'<text x="24" y="332" font-size="12" font-weight="bold" fill="{theme.black}">分時成交明細（Tick，示意）</text>')
    ticks = [
        ("13:24:05", last.close, 2, "外"),
        ("13:23:58", last.close - spread, 1, "內"),
        ("13:23:41", last.close - spread, 3, "外"),
        ("13:23:12", last.close - spread * 2, 1, "內"),
    ]
    for i, (t, px, lots, side) in enumerate(ticks):
        y = 352 + i * 14
        sc = theme.red if side == "外" else theme.green
        parts.append(f'<text x="24" y="{y}" font-size="10" fill="{theme.gray}">{t}</text>')
        parts.append(f'<text x="100" y="{y}" font-size="10" fill="{theme.black}">{px:.2f}</text>')
        parts.append(f'<text x="160" y="{y}" font-size="10" fill="{theme.gray}">{lots}</text>')
        parts.append(f'<text x="190" y="{y}" font-size="10" fill="{sc}">{side}</text>')
    return svg_header(f"{code} 報價畫面示意", width, height, "".join(parts))


def volume_bars_svg(
    bars: list[Bar], *, code: str, name: str, width: int = 640, height: int = 120, theme: Theme = DEFAULT_THEME
) -> str:
    if not bars:
        return ""
    pad_l, pad_r, pad_t, pad_b = 48, 16, 24, 24
    cw = width - pad_l - pad_r
    ch = height - pad_t - pad_b
    vmax = max(b.volume for b in bars) or 1
    n = len(bars)
    gap = cw / n
    parts = [
        f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
        f'<text x="{pad_l}" y="16" font-size="12" font-weight="bold" fill="{theme.black}">{code} 成交量（近 {n} 日）</text>',
    ]
    for i, b in enumerate(bars):
        bull = b.close >= b.open
        color = theme.red if bull else theme.black
        h = ch * b.volume / vmax
        x = pad_l + gap * i + gap * 0.2
        w = gap * 0.6
        y = pad_t + ch - h
        parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{color}" opacity="0.85"/>')
    parts.append(
        f'<line x1="{pad_l}" y1="{pad_t + ch}" x2="{width - pad_r}" y2="{pad_t + ch}" stroke="{theme.border}"/>'
    )
    return svg_header(f"{code} 量柱", width, height, "".join(parts))
