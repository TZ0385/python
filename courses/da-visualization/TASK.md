# Task contract: data visualization (da-visualization)

Change only `starter/charts.py`. Input:
`scenario/sales-clean/sales_daily.csv` — clean long-format data
(date, region, revenue; 135 rows, 45 days, 3 regions).

- `load_sales(path) -> DataFrame` with a parsed `date` column.
- `summary(df) -> dict`:
  - `revenue_by_region` — total per region, 2 decimals.
  - `daily_revenue` — total per ISO date, 2 decimals.
  - `grand_total` — 2 decimals.
- `revenue_by_region(df, dest)` — bar chart PNG at `dest`.
- `daily_revenue(df, dest)` — line chart PNG at `dest`.
- `revenue_histogram(df, dest)` — histogram PNG at `dest`.
- `main()` — writes `out/revenue_by_region.png`, `out/daily_revenue.png`,
  `out/revenue_histogram.png`, and `out/summary.json` (UTF-8, indent 2,
  trailing newline); prints a one-line confirmation; returns 0.

Constraints: matplotlib Agg backend only (no display); charts must be
generated *from the data*, never hardcoded. Verification checks that the
PNG files exist and are valid, and that summary.json's numbers match the
dataset — it does not judge how the charts look.

Done means `python verify.py starter` exits 0 and
`python verify.py starter --expect-failure` exits nonzero.
