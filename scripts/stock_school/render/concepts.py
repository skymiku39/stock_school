"""Synthetic concept-illustration SVGs (chips / fundamental / market charts).

These are educational diagrams with hand-crafted data, so they never depend on
TWSE network access and are always reproducible.
"""
from __future__ import annotations

from stock_school.render.svg_primitives import footer_note, svg_header, title_block
from stock_school.render.theme import DEFAULT_THEME

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

W, H = 640, 360


def _panel(x: int, y: int, w: int, h: int) -> str:
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fafafa" stroke="{BORDER}"/>'


def _polyline(points: list[tuple[float, float]], color: str, dash: str = "") -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    pts = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
    return f'<polyline fill="none" stroke="{color}" stroke-width="2"{dash_attr} points="{pts}"/>'


def institutional_cumulative_svg() -> str:
    price = [50, 51, 52, 51.5, 53, 54, 55, 56, 55.5, 57]
    cum = [200, 500, 850, 700, 1100, 1500, 1900, 2400, 2300, 2800]
    parts = title_block("法人累計買賣超圖（教學示意）", W, "累計線向上 = 近期淨買超")
    x0, y0, pw, ph = 56, 70, W - 112, 220
    parts.append(_panel(x0, y0, pw, ph))
    n = len(price)
    p_lo, p_hi = min(price) - 1, max(price) + 1
    ppts = [(x0 + pw * (i + 0.5) / n, y0 + ph * (p_hi - c) / (p_hi - p_lo)) for i, c in enumerate(price)]
    parts.append(_polyline(ppts, RED))
    c_hi = max(cum) * 1.1
    cpts = [(x0 + pw * (i + 0.5) / n, y0 + ph * (c_hi - c) / c_hi) for i, c in enumerate(cum)]
    parts.append(_polyline(cpts, BLUE, "5 3"))
    parts.append(f'<text x="{x0 + 4}" y="{y0 + 16}" font-size="10" fill="{RED}">— 股價</text>')
    parts.append(f'<text x="{x0 + 4}" y="{y0 + 30}" font-size="10" fill="{BLUE}">- - 法人累計買賣超</text>')
    parts.append(
        f'<text x="{x0 + pw - 188:.0f}" y="{y0 + ph - 10:.0f}" font-size="10" fill="{GRAY}">價漲 + 累計向上 = 籌碼一致</text>'
    )
    parts.append(footer_note(W, H, "教學示意 · 對照三大法人表 · 資料有 lag"))
    return svg_header("法人累計買賣超", W, H, "".join(parts))


def margin_balance_svg() -> str:
    margin = [120, 128, 135, 142, 150, 162, 158, 170, 180, 175]
    price = [50, 52, 53, 55, 57, 60, 58, 62, 64, 61]
    parts = title_block("融資餘額趨勢圖（教學示意）", W, "融資攀升 + 股價漲 = 散戶槓桿增加")
    x0, y0, pw, ph = 56, 70, W - 112, 220
    parts.append(_panel(x0, y0, pw, ph))
    n = len(margin)
    gap = pw / n
    mmax = max(margin) * 1.15
    for i, m in enumerate(margin):
        h = ph * 0.8 * m / mmax
        x = x0 + gap * i + gap * 0.2
        parts.append(
            f'<rect x="{x:.1f}" y="{y0 + ph - h:.1f}" width="{gap * 0.6:.1f}" '
            f'height="{h:.1f}" fill="{ORANGE}" opacity="0.6"/>'
        )
    p_lo, p_hi = min(price) - 2, max(price) + 2
    ppts = [(x0 + gap * (i + 0.5), y0 + ph * (p_hi - p) / (p_hi - p_lo)) for i, p in enumerate(price)]
    parts.append(_polyline(ppts, RED))
    parts.append(f'<text x="{x0 + 4}" y="{y0 + 16}" font-size="10" fill="{ORANGE}">▮ 融資餘額</text>')
    parts.append(f'<text x="{x0 + 4}" y="{y0 + 30}" font-size="10" fill="{RED}">— 股價</text>')
    parts.append(footer_note(W, H, "教學示意 · 融資急降 + 股價跌 = 留意斷頭"))
    return svg_header("融資餘額趨勢", W, H, "".join(parts))


def eps_trend_svg() -> str:
    quarters = ["Q1", "Q2", "Q3", "Q4", "Q1", "Q2", "Q3", "Q4"]
    eps = [1.1, 1.3, 1.2, 1.5, 1.6, 1.9, 2.1, 2.4]
    parts = title_block("季 EPS 趨勢圖（教學合成數據）", W, "一季一季是否成長")
    x0, y0, pw, ph = 56, 70, W - 112, 220
    parts.append(_panel(x0, y0, pw, ph))
    n = len(eps)
    gap = pw / n
    emax = max(eps) * 1.2
    for i, e in enumerate(eps):
        h = ph * 0.85 * e / emax
        x = x0 + gap * i + gap * 0.25
        parts.append(
            f'<rect x="{x:.1f}" y="{y0 + ph - h:.1f}" width="{gap * 0.5:.1f}" '
            f'height="{h:.1f}" fill="{BLUE}" opacity="0.5"/>'
        )
        parts.append(
            f'<text x="{x + gap * 0.25:.1f}" y="{y0 + ph - h - 4:.1f}" font-size="8" '
            f'fill="{GRAY}" text-anchor="middle">{e}</text>'
        )
    epts = [(x0 + gap * (i + 0.5), y0 + ph - ph * 0.85 * e / emax) for i, e in enumerate(eps)]
    parts.append(_polyline(epts, BLUE))
    for i, q in enumerate(quarters):
        parts.append(
            f'<text x="{x0 + gap * (i + 0.5):.1f}" y="{y0 + ph + 14:.1f}" font-size="8" '
            f'fill="{GRAY}" text-anchor="middle">{q}</text>'
        )
    parts.append(footer_note(W, H, "合成教學數據 · 看趨勢非單季"))
    return svg_header("季 EPS 趨勢", W, H, "".join(parts))


def profit_margins_svg() -> str:
    series = [
        ("毛利率", [42, 43, 44, 45, 46, 47], RED),
        ("營益率", [25, 26, 26, 28, 29, 30], BLUE),
        ("淨利率", [20, 21, 20, 22, 23, 24], GREEN),
    ]
    parts = title_block("三率趨勢圖（毛利率 / 營益率 / 淨利率，合成）", W, "本業競爭力與獲利能力")
    x0, y0, pw, ph = 56, 70, W - 112, 220
    parts.append(_panel(x0, y0, pw, ph))
    lo, hi = 15, 50
    n = len(series[0][1])
    for k, (label, values, color) in enumerate(series):
        pts = [(x0 + pw * (i + 0.5) / n, y0 + ph * (hi - v) / (hi - lo)) for i, v in enumerate(values)]
        parts.append(_polyline(pts, color))
        parts.append(f'<text x="{x0 + 4}" y="{y0 + 16 + k * 14}" font-size="10" fill="{color}">— {label}</text>')
    parts.append(footer_note(W, H, "合成教學數據 · 三率同揚較佳"))
    return svg_header("三率趨勢", W, H, "".join(parts))


def valuation_band_svg() -> str:
    price = [55, 58, 62, 60, 65, 70, 68, 72, 76, 74, 78, 80]
    parts = title_block("本益比河流圖（估值帶，教學示意）", W, "股價落在便宜 / 合理 / 昂貴帶")
    x0, y0, pw, ph = 56, 70, W - 112, 220
    lo, hi = 40, 95

    def y(v: float) -> float:
        return y0 + ph * (hi - v) / (hi - lo)

    parts.append(f'<rect x="{x0}" y="{y(95):.1f}" width="{pw}" height="{y(75) - y(95):.1f}" fill="#ffebee" opacity="0.7"/>')
    parts.append(f'<rect x="{x0}" y="{y(75):.1f}" width="{pw}" height="{y(55) - y(75):.1f}" fill="#e8f5e9" opacity="0.7"/>')
    parts.append(f'<rect x="{x0}" y="{y(55):.1f}" width="{pw}" height="{y(40) - y(55):.1f}" fill="#e3f2fd" opacity="0.7"/>')
    parts.append(f'<rect x="{x0}" y="{y0}" width="{pw}" height="{ph}" fill="none" stroke="{BORDER}"/>')
    parts.append(f'<text x="{x0 + pw - 56}" y="{y(86):.1f}" font-size="9" fill="{RED}">昂貴帶</text>')
    parts.append(f'<text x="{x0 + pw - 56}" y="{y(65):.1f}" font-size="9" fill="{GREEN}">合理帶</text>')
    parts.append(f'<text x="{x0 + pw - 56}" y="{y(47):.1f}" font-size="9" fill="{BLUE}">便宜帶</text>')
    n = len(price)
    pts = [(x0 + pw * (i + 0.5) / n, y(p)) for i, p in enumerate(price)]
    parts.append(_polyline(pts, PURPLE))
    parts.append(footer_note(W, H, "教學示意 · 估值帶隨 EPS 變動 · 非買賣訊號"))
    return svg_header("估值河流圖", W, H, "".join(parts))


def sector_performance_svg() -> str:
    sectors = [
        ("半導體", 2.8),
        ("金融", 1.2),
        ("航運", 0.4),
        ("生技", -0.6),
        ("傳產", -1.1),
        ("觀光", -2.3),
    ]
    parts = title_block("類股漲跌排行（教學示意）", W, "今日資金流向哪個類股")
    x0, y0, pw, ph = 120, 64, W - 200, 250
    rows = len(sectors)
    rh = ph / rows
    zero_x = x0 + pw * 0.45
    vmax = 3.0
    for i, (name, pct) in enumerate(sectors):
        cy = y0 + rh * i + rh * 0.5
        parts.append(
            f'<text x="{x0 - 8}" y="{cy + 4:.1f}" font-size="11" fill="{GRAY}" text-anchor="end">{name}</text>'
        )
        bw = (pw * 0.5) * abs(pct) / vmax
        if pct >= 0:
            parts.append(
                f'<rect x="{zero_x:.1f}" y="{cy - rh * 0.3:.1f}" width="{bw:.1f}" '
                f'height="{rh * 0.6:.1f}" fill="{RED}" opacity="0.8"/>'
            )
            parts.append(f'<text x="{zero_x + bw + 4:.1f}" y="{cy + 4:.1f}" font-size="10" fill="{RED}">+{pct:.1f}%</text>')
        else:
            parts.append(
                f'<rect x="{zero_x - bw:.1f}" y="{cy - rh * 0.3:.1f}" width="{bw:.1f}" '
                f'height="{rh * 0.6:.1f}" fill="{GREEN}" opacity="0.8"/>'
            )
            parts.append(
                f'<text x="{zero_x - bw - 4:.1f}" y="{cy + 4:.1f}" font-size="10" '
                f'fill="{GREEN}" text-anchor="end">{pct:.1f}%</text>'
            )
    parts.append(f'<line x1="{zero_x:.1f}" y1="{y0}" x2="{zero_x:.1f}" y2="{y0 + ph}" stroke="{BORDER}"/>')
    parts.append(footer_note(W, H, "教學示意 · 紅漲綠跌 · 先看類股再選股"))
    return svg_header("類股漲跌排行", W, H, "".join(parts))


def build_all_concept_svgs() -> dict[str, str]:
    """Return filename → SVG content for chips / fundamental / market illustrations."""
    return {
        "institutional-cumulative.svg": institutional_cumulative_svg(),
        "margin-balance.svg": margin_balance_svg(),
        "eps-trend.svg": eps_trend_svg(),
        "profit-margins.svg": profit_margins_svg(),
        "valuation-band.svg": valuation_band_svg(),
        "sector-performance.svg": sector_performance_svg(),
    }
