"""Capstone reference pipeline — reviewed solution.

Reads dataset/orders.csv and writes out/results.json + out/report.md.
See TASK.md for the contract.
"""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATASET = ROOT / "dataset" / "orders.csv"
OUT_DIR = ROOT / "out"


def load_and_clean(path):
    df = pd.read_csv(path)
    stats = {"rows_total": int(len(df)),
             "duplicates_removed": int(df.duplicated().sum())}
    df = df.drop_duplicates().copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["region"] = df["region"].astype("string").str.strip()
    df.loc[df["region"].isin(["", "nan", "NaN", "<NA>"]), "region"] = pd.NA
    clean = df.dropna(subset=["amount", "date", "region"])
    stats["rows_removed"] = stats["rows_total"] - stats["duplicates_removed"] - len(clean)
    stats["rows_clean"] = int(len(clean))
    return clean, stats


def summarize(clean):
    by_region = clean.groupby("region")["amount"].sum().round(2)
    by_cat = clean.groupby("category")["amount"].sum()
    return {
        "total_revenue": round(float(clean["amount"].sum()), 2),
        "avg_order_value": round(float(clean["amount"].mean()), 2),
        "total_quantity": int(clean["quantity"].sum()),
        "revenue_by_region": {str(k): float(v) for k, v in by_region.items()},
        "top_category": str(by_cat.idxmax()),
        "first_date": clean["date"].min().date().isoformat(),
        "last_date": clean["date"].max().date().isoformat(),
    }


def render_report(results):
    lines = [
        "# Capstone analysis report",
        "",
        "## Data quality",
        f"{results['rows_clean']} of {results['rows_total']} rows survived "
        f"cleaning ({results['duplicates_removed']} duplicates, "
        f"{results['rows_removed']} invalid).",
        "",
        "## Findings",
        f"Total revenue {results['total_revenue']:.2f} over "
        f"{results['total_quantity']} units; top category "
        f"{results['top_category']}; period {results['first_date']} to "
        f"{results['last_date']}.",
        "",
        "## Appendix",
        "Numbers verified against the dataset by verify.py; prose is not verified.",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    clean, stats = load_and_clean(DATASET)
    results = {**stats, **summarize(clean)}
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "results.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUT_DIR / "report.md").write_text(render_report(results), encoding="utf-8")
    print(f"rows_clean={results['rows_clean']} total_revenue={results['total_revenue']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
