"""Verify installable package entry points."""
from __future__ import annotations

import importlib


def test_stock_school_package_importable() -> None:
    pkg = importlib.import_module("stock_school")
    assert pkg.__file__ is not None


def test_console_script_entry_points_registered() -> None:
    from importlib.metadata import entry_points

    names = {ep.name for ep in entry_points(group="console_scripts")}
    assert "stock-school-gen" in names
    assert "stock-school-links" in names
