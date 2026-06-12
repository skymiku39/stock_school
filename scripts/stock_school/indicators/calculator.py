"""Technical indicator math (SRP: pure calculations, no I/O)."""
from __future__ import annotations

from stock_school.domain.bar import Bar


class IndicatorCalculator:
    @staticmethod
    def closes(bars: list[Bar]) -> list[float]:
        return [b.close for b in bars]

    @staticmethod
    def sma(values: list[float], period: int) -> list[float | None]:
        out: list[float | None] = [None] * len(values)
        for i in range(period - 1, len(values)):
            out[i] = sum(values[i - period + 1 : i + 1]) / period
        return out

    @staticmethod
    def ema(values: list[float], period: int) -> list[float | None]:
        out: list[float | None] = [None] * len(values)
        if len(values) < period:
            return out
        k = 2 / (period + 1)
        start = sum(values[:period]) / period
        out[period - 1] = start
        prev = start
        for i in range(period, len(values)):
            prev = values[i] * k + prev * (1 - k)
            out[i] = prev
        return out

    @classmethod
    def ema_series(cls, values: list[float | None], period: int) -> list[float | None]:
        nums = [v for v in values if v is not None]
        if not nums:
            return [None] * len(values)
        full = cls.ema(nums, period)
        out: list[float | None] = [None] * len(values)
        j = 0
        for i, v in enumerate(values):
            if v is not None and j < len(full):
                out[i] = full[j]
                j += 1
        return out

    @classmethod
    def macd(
        cls, values: list[float], fast: int = 12, slow: int = 26, signal: int = 9
    ) -> tuple[list[float | None], list[float | None], list[float | None]]:
        ef = cls.ema(values, fast)
        es = cls.ema(values, slow)
        dif: list[float | None] = [None] * len(values)
        for i in range(len(values)):
            if ef[i] is not None and es[i] is not None:
                dif[i] = ef[i] - es[i]  # type: ignore[operator]
        dif_nums = [d if d is not None else 0.0 for d in dif]
        sig = cls.ema_series(dif_nums, signal)
        hist: list[float | None] = [None] * len(values)
        for i in range(len(values)):
            if dif[i] is not None and sig[i] is not None:
                hist[i] = dif[i] - sig[i]  # type: ignore[operator]
        return dif, sig, hist

    @classmethod
    def rsi(cls, values: list[float], period: int = 14) -> list[float | None]:
        out: list[float | None] = [None] * len(values)
        if len(values) <= period:
            return out
        gains: list[float] = []
        losses: list[float] = []
        for i in range(1, len(values)):
            d = values[i] - values[i - 1]
            gains.append(max(d, 0))
            losses.append(max(-d, 0))
        avg_g = sum(gains[:period]) / period
        avg_l = sum(losses[:period]) / period
        out[period] = 100 - 100 / (1 + avg_g / avg_l) if avg_l else 100.0
        for i in range(period, len(gains)):
            avg_g = (avg_g * (period - 1) + gains[i]) / period
            avg_l = (avg_l * (period - 1) + losses[i]) / period
            out[i + 1] = 100 - 100 / (1 + avg_g / avg_l) if avg_l else 100.0
        return out

    @classmethod
    def stochastic(
        cls, bars: list[Bar], k_period: int = 9, k_smooth: int = 3, d_smooth: int = 3
    ) -> tuple[list[float | None], list[float | None]]:
        rsv: list[float | None] = [None] * len(bars)
        for i in range(k_period - 1, len(bars)):
            window = bars[i - k_period + 1 : i + 1]
            hi = max(b.high for b in window)
            lo = min(b.low for b in window)
            if hi == lo:
                rsv[i] = 50.0
            else:
                rsv[i] = (bars[i].close - lo) / (hi - lo) * 100
        k_line = cls._smooth(rsv, k_smooth)
        d_line = cls._smooth(k_line, d_smooth)
        return k_line, d_line

    @staticmethod
    def _smooth(values: list[float | None], period: int) -> list[float | None]:
        out: list[float | None] = [None] * len(values)
        for i in range(period - 1, len(values)):
            chunk = [v for v in values[i - period + 1 : i + 1] if v is not None]
            if len(chunk) == period:
                out[i] = sum(chunk) / period
        return out

    @classmethod
    def bollinger(
        cls, values: list[float], period: int = 20, k: float = 2.0
    ) -> tuple[list[float | None], list[float | None], list[float | None]]:
        mid = cls.sma(values, period)
        up: list[float | None] = [None] * len(values)
        lo: list[float | None] = [None] * len(values)
        for i in range(period - 1, len(values)):
            chunk = values[i - period + 1 : i + 1]
            m = mid[i]
            if m is None:
                continue
            var = sum((x - m) ** 2 for x in chunk) / period
            std = var**0.5
            up[i] = m + k * std
            lo[i] = m - k * std
        return mid, up, lo
