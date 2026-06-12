"""Candlestick pattern SVG renderers."""
from __future__ import annotations

from collections.abc import Callable

W, H, CX = 80, 120, 40


def svg_wrap(body: str, title: str = "") -> str:
    t = f'<title>{title}</title>' if title else ""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{title}">{t}'
        f'<rect width="{W}" height="{H}" fill="none"/>'
        f"{body}</svg>"
    )


def wick(y1: float, y2: float, color: str = "#666") -> str:
    return f'<line x1="{CX}" y1="{y1}" x2="{CX}" y2="{y2}" stroke="{color}" stroke-width="2"/>'


def body(y_top: float, y_bot: float, color: str) -> str:
    h = max(y_bot - y_top, 2)
    return (
        f'<rect x="{CX-12}" y="{y_top}" width="24" height="{h}" '
        f'fill="{color}" stroke="{color}" stroke-width="1"/>'
    )


def candle(
    *,
    open_y: float,
    close_y: float,
    high_y: float,
    low_y: float,
    bull: bool,
    title: str,
) -> str:
    color = "#e53935" if bull else "#212121"
    y_top = min(open_y, close_y)
    y_bot = max(open_y, close_y)
    parts = [wick(high_y, low_y), body(y_top, y_bot, color)]
    return svg_wrap("".join(parts), title)


def structure() -> str:
    parts = [
        wick(15, 105),
        body(35, 75, "#e53935"),
        '<text x="52" y="18" font-size="9" fill="#666">高</text>',
        '<text x="52" y="40" font-size="9" fill="#666">收</text>',
        '<text x="52" y="78" font-size="9" fill="#666">開</text>',
        '<text x="52" y="108" font-size="9" fill="#666">低</text>',
        '<text x="4" y="58" font-size="8" fill="#888">實體</text>',
        '<text x="4" y="28" font-size="8" fill="#888">上影</text>',
        '<text x="4" y="95" font-size="8" fill="#888">下影</text>',
    ]
    return svg_wrap("".join(parts), "K棒結構")


PATTERNS: dict[str, tuple] = {
    "big-red": (30, 90, 15, 95, True, "大紅K"),
    "mid-red": (45, 80, 25, 90, True, "中紅K"),
    "small-red": (52, 68, 35, 82, True, "小紅K"),
    "big-black": (30, 90, 15, 95, False, "大黑K"),
    "mid-black": (45, 80, 25, 90, False, "中黑K"),
    "small-black": (52, 68, 35, 82, False, "小黑K"),
    "inverted-hammer-red": (70, 78, 12, 80, True, "倒鎚紅K"),
    "inverted-hammer-black": (70, 78, 12, 80, False, "倒鎚黑K"),
    "hammer-red": (42, 50, 40, 95, True, "紅K鎚子"),
    "hammer-black": (50, 58, 48, 95, False, "黑K鎚子"),
    "spinning-red": (48, 58, 20, 90, True, "紡錘紅K"),
    "spinning-black": (48, 58, 20, 90, False, "紡錘黑K"),
    "doji": (55, 57, 18, 88, True, "十字線"),
    "dragonfly": (20, 22, 20, 92, True, "T字線"),
    "gravestone": (20, 22, 20, 92, False, "倒T字線"),
    "flat": (50, 52, 48, 54, True, "一字線"),
}


def doji_svg(title: str) -> str:
    parts = [
        wick(18, 88),
        '<line x1="28" y1="56" x2="52" y2="56" stroke="#e53935" stroke-width="3"/>',
    ]
    return svg_wrap("".join(parts), title)


def flat_svg(title: str) -> str:
    parts = [wick(50, 52), body(50, 52, "#e53935")]
    return svg_wrap("".join(parts), title)


def combo_wrap(body: str, title: str, width: int = 200) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {H}" '
        f'role="img" aria-label="{title}"><title>{title}</title>'
        f'<rect width="{width}" height="{H}" fill="none"/>'
        f"{body}</svg>"
    )


def combo_candle(cx: int, open_y: float, close_y: float, high_y: float, low_y: float, bull: bool) -> str:
    color = "#e53935" if bull else "#212121"
    y_top = min(open_y, close_y)
    y_bot = max(open_y, close_y)
    return (
        wick(high_y, low_y, "#666").replace(f'x1="{CX}"', f'x1="{cx}"').replace(f'x2="{CX}"', f'x2="{cx}')
        + body(y_top, y_bot, color).replace(f'x="{CX-12}"', f'x="{cx-12}"')
    )


def engulfing_bull() -> str:
    parts = [
        combo_candle(50, 45, 80, 25, 90, False),
        combo_candle(130, 30, 75, 15, 95, True),
    ]
    return combo_wrap("".join(parts), "看漲吞噬")


def engulfing_bear() -> str:
    parts = [
        combo_candle(50, 30, 75, 15, 95, True),
        combo_candle(130, 45, 80, 25, 90, False),
    ]
    return combo_wrap("".join(parts), "看跌吞噬")


def morning_star() -> str:
    parts = [
        combo_candle(40, 30, 85, 20, 95, False),
        combo_candle(100, 52, 58, 48, 62, True),
        combo_candle(160, 30, 70, 20, 90, True),
    ]
    return combo_wrap("".join(parts), "晨星")


def evening_star() -> str:
    parts = [
        combo_candle(40, 30, 70, 20, 90, True),
        combo_candle(100, 52, 58, 48, 62, False),
        combo_candle(160, 45, 85, 35, 95, False),
    ]
    return combo_wrap("".join(parts), "暮星")


COMBOS: dict[str, Callable[[], str]] = {
    "engulfing-bull": engulfing_bull,
    "engulfing-bear": engulfing_bear,
    "morning-star": morning_star,
    "evening-star": evening_star,
}


def build_all_candle_svgs() -> dict[str, str]:
    """Return filename → SVG content for all candle assets."""
    files: dict[str, str] = {"structure.svg": structure()}
    for name, args in PATTERNS.items():
        if name == "doji":
            files[f"{name}.svg"] = doji_svg(args[5])
        elif name == "flat":
            files[f"{name}.svg"] = flat_svg(args[5])
        else:
            files[f"{name}.svg"] = candle(
                open_y=args[0],
                close_y=args[1],
                high_y=args[2],
                low_y=args[3],
                bull=args[4],
                title=args[5],
            )
    for name, fn in COMBOS.items():
        files[f"{name}.svg"] = fn()
    return files
