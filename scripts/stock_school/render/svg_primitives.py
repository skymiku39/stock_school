"""Low-level SVG building blocks (SRP: drawing only)."""
from __future__ import annotations

from dataclasses import dataclass

from stock_school.domain.bar import Bar
from stock_school.render.theme import DEFAULT_THEME, Theme


@dataclass
class ChartPad:
    left: int = 48
    right: int = 16
    top: int = 36
    bottom: int = 28


def svg_header(title: str, w: int, h: int, body: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{title}">'
        f"<title>{title}</title>{body}</svg>"
    )


def _x(i: int, n: int, pad: ChartPad, width: int) -> float:
    cw = width - pad.left - pad.right
    return pad.left + cw * (i + 0.5) / n


def _y(v: float, lo: float, hi: float, pad: ChartPad, height: int) -> float:
    ch = height - pad.top - pad.bottom
    span = hi - lo or 1
    return pad.top + ch * (hi - v) / span


def draw_candles(
    bars: list[Bar],
    *,
    width: int,
    height: int,
    pad: ChartPad | None = None,
    y_lo: float | None = None,
    y_hi: float | None = None,
    theme: Theme = DEFAULT_THEME,
) -> tuple[list[str], float, float]:
    pad = pad or ChartPad()
    lo = y_lo if y_lo is not None else min(b.low for b in bars)
    hi = y_hi if y_hi is not None else max(b.high for b in bars)
    n = len(bars)
    gap = (width - pad.left - pad.right) / n
    bw = max(gap * 0.55, 2)
    parts: list[str] = []
    for i, b in enumerate(bars):
        cx = _x(i, n, pad, width)
        bull = b.close >= b.open
        color = theme.red if bull else theme.black
        y_h = _y(b.high, lo, hi, pad, height)
        y_l = _y(b.low, lo, hi, pad, height)
        y_o = _y(b.open, lo, hi, pad, height)
        y_c = _y(b.close, lo, hi, pad, height)
        parts.append(
            f'<line x1="{cx:.1f}" y1="{y_h:.1f}" x2="{cx:.1f}" y2="{y_l:.1f}" '
            f'stroke="{color}" stroke-width="1"/>'
        )
        top, bot = min(y_o, y_c), max(y_o, y_c)
        h = max(bot - top, 1)
        parts.append(
            f'<rect x="{cx - bw / 2:.1f}" y="{top:.1f}" width="{bw:.1f}" '
            f'height="{h:.1f}" fill="{color}"/>'
        )
    return parts, lo, hi


def draw_line_series(
    series: list[float | None],
    *,
    color: str,
    width: int,
    height: int,
    pad: ChartPad,
    y_lo: float,
    y_hi: float,
    stroke_width: float = 1.5,
    dash: str = "",
) -> str:
    n = len(series)
    pts: list[str] = []
    for i, v in enumerate(series):
        if v is None:
            continue
        pts.append(f"{_x(i, n, pad, width):.1f},{_y(v, y_lo, y_hi, pad, height):.1f}")
    if len(pts) < 2:
        return ""
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<polyline fill="none" stroke="{color}" stroke-width="{stroke_width}"'
        f'{dash_attr} points="{" ".join(pts)}"/>'
    )


def title_block(title: str, width: int, subtitle: str = "", theme: Theme = DEFAULT_THEME) -> list[str]:
    parts = [
        f'<rect width="{width}" height="100%" fill="#ffffff"/>',
        f'<text x="48" y="22" font-size="14" font-weight="bold" fill="{theme.black}">{title}</text>',
    ]
    if subtitle:
        parts.append(f'<text x="48" y="38" font-size="10" fill="{theme.gray}">{subtitle}</text>')
    return parts


def footer_note(width: int, height: int, text: str, theme: Theme = DEFAULT_THEME) -> str:
    return f'<text x="48" y="{height - 8}" font-size="10" fill="{theme.gray}">{text}</text>'
