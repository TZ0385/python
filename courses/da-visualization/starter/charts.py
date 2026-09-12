"""Data visualization — starter (deliberately unfinished).

Contract: see TASK.md. Produce the three spec'd charts and summary.json
in out/ using matplotlib (Agg backend — no display required).
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

SCENARIO_DIR = Path(__file__).resolve().parent.parent / "scenario" / "sales-clean"
OUT_DIR = Path(__file__).resolve().parent.parent / "out"


def load_sales(path):
    """Read the daily-sales CSV into a DataFrame with a parsed date column."""
    raise NotImplementedError


def summary(df):
    """Return {"revenue_by_region": {region: float}, "daily_revenue":
    {date: float}, "grand_total": float} — every value rounded to 2."""
    raise NotImplementedError


def revenue_by_region(df, dest):
    """Bar chart of total revenue per region -> PNG at dest."""
    raise NotImplementedError


def daily_revenue(df, dest):
    """Line chart of total revenue per day -> PNG at dest."""
    raise NotImplementedError


def revenue_histogram(df, dest):
    """Histogram of row-level revenue values -> PNG at dest."""
    raise NotImplementedError


def main(argv=None):
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
