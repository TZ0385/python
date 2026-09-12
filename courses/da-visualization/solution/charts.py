"""Data visualization — reviewed solution."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless: never require a display

import matplotlib.pyplot as plt
import pandas as pd

SCENARIO_DIR = Path(__file__).resolve().parent.parent / "scenario" / "sales-clean"
OUT_DIR = Path(__file__).resolve().parent.parent / "out"


def load_sales(path):
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    return df


def summary(df):
    by_region = df.groupby("region")["revenue"].sum().round(2)
    daily = df.groupby("date")["revenue"].sum().round(2)
    return {
        "revenue_by_region": {str(k): float(v) for k, v in by_region.items()},
        "daily_revenue": {k.date().isoformat(): float(v) for k, v in daily.items()},
        "grand_total": round(float(df["revenue"].sum()), 2),
    }


def revenue_by_region(df, dest):
    totals = df.groupby("region")["revenue"].sum().sort_index()
    fig, ax = plt.subplots()
    ax.bar(totals.index.astype(str), totals.values)
    ax.set_xlabel("Region")
    ax.set_ylabel("Total revenue")
    ax.set_title("Revenue by region")
    fig.savefig(dest, dpi=100)
    plt.close(fig)


def daily_revenue(df, dest):
    daily = df.groupby("date")["revenue"].sum().sort_index()
    fig, ax = plt.subplots()
    ax.plot(daily.index, daily.values)
    ax.set_xlabel("Date")
    ax.set_ylabel("Total revenue")
    ax.set_title("Daily revenue")
    fig.autofmt_xdate()
    fig.savefig(dest, dpi=100)
    plt.close(fig)


def revenue_histogram(df, dest):
    fig, ax = plt.subplots()
    ax.hist(df["revenue"], bins=20)
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Rows")
    ax.set_title("Revenue distribution")
    fig.savefig(dest, dpi=100)
    plt.close(fig)


def main(argv=None):
    df = load_sales(SCENARIO_DIR / "sales_daily.csv")
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    revenue_by_region(df, OUT_DIR / "revenue_by_region.png")
    daily_revenue(df, OUT_DIR / "daily_revenue.png")
    revenue_histogram(df, OUT_DIR / "revenue_histogram.png")
    (OUT_DIR / "summary.json").write_text(
        json.dumps(summary(df), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote 3 charts + summary.json to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
