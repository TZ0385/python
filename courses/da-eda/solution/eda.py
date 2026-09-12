"""Exploratory data analysis — reviewed solution."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

SCENARIO_DIR = Path(__file__).resolve().parent.parent / "scenario" / "shop-export"


def load_transactions(path):
    return pd.read_csv(path)


def clean_transactions(df):
    stats = {"duplicates_removed": int(df.duplicated().sum()),
             "missing_amount": 0, "bad_dates": 0}
    df = df.drop_duplicates().copy()
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    stats["missing_amount"] = int(df["amount"].isna().sum())
    clean = df.dropna(subset=["amount"])
    stats["bad_dates"] = int(clean["date"].isna().sum())
    return clean.dropna(subset=["date"]), stats


def summarize(clean_df):
    revenue_by_region = (
        clean_df.groupby("region")["amount"].sum().round(2).to_dict()
    )
    top_category = clean_df.groupby("category")["amount"].sum().idxmax()
    return {
        "rows_total": None,  # filled by main from the raw frame
        "rows_clean": int(len(clean_df)),
        "total_revenue": round(float(clean_df["amount"].sum()), 2),
        "revenue_by_region": {k: float(v) for k, v in revenue_by_region.items()},
        "top_category": str(top_category),
        "first_date": clean_df["date"].min().date().isoformat(),
        "last_date": clean_df["date"].max().date().isoformat(),
    }


def write_results(results, dest):
    dest = Path(dest)
    dest.write_text(json.dumps(results, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def main(argv=None):
    raw = load_transactions(SCENARIO_DIR / "transactions.csv")
    clean, stats = clean_transactions(raw)
    results = summarize(clean)
    results.update({
        "rows_total": int(len(raw)),
        "duplicates_removed": stats["duplicates_removed"],
        "missing_amount": stats["missing_amount"],
        "bad_dates": stats["bad_dates"],
    })
    write_results(results, SCENARIO_DIR / "results.json")
    print(f"rows_total={results['rows_total']} rows_clean={results['rows_clean']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
