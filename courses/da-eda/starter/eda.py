"""Exploratory data analysis — starter (deliberately unfinished).

Contract: see TASK.md. Implement the functions below so the test suite
passes and results.json matches the reviewed summary of the dataset.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

SCENARIO_DIR = Path(__file__).resolve().parent.parent / "scenario" / "shop-export"


def load_transactions(path):
    """Read the transactions CSV into a DataFrame."""
    raise NotImplementedError


def clean_transactions(df):
    """Return (clean_df, stats).

    - Drop exact duplicate rows.
    - Parse ``amount`` to numeric; rows that do not parse are removed and
      counted as ``missing_amount``.
    - Parse ``date``; rows that do not parse are removed and counted as
      ``bad_dates``.
    stats = {"duplicates_removed": int, "missing_amount": int, "bad_dates": int}
    clean_df keeps original columns plus parsed ``amount`` and ``date``.
    """
    raise NotImplementedError


def summarize(clean_df):
    """Build the results dict described in TASK.md."""
    raise NotImplementedError


def write_results(results, dest):
    """Write results as JSON (UTF-8, indent 2, trailing newline)."""
    raise NotImplementedError


def main(argv=None):
    raise NotImplementedError


if __name__ == "__main__":
    raise SystemExit(main())
