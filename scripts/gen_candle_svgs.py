"""Backward-compatible entry — delegates to Pub/Sub pipeline."""
from __future__ import annotations

from stock_school.cli import main

if __name__ == "__main__":
    raise SystemExit(main(["--only", "candles"]))
