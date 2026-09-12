# Task contract: exploratory data analysis (da-eda)

Change only `starter/eda.py`. The dataset is
`scenario/shop-export/transactions.csv` — a shop export with exact
duplicates, missing/unparseable amounts, and one bad date.

- `load_transactions(path) -> pandas.DataFrame`: reads the CSV.
- `clean_transactions(df) -> (clean_df, stats)`:
  - Drop exact duplicate rows, count them as `duplicates_removed`.
  - Parse `amount` to numeric; unparseable rows are removed and counted as
    `missing_amount`.
  - Parse `date`; unparseable rows are removed and counted as `bad_dates`.
  - `stats = {"duplicates_removed": int, "missing_amount": int,
    "bad_dates": int}`; clean rows keep parsed `amount` and `date`.
- `summarize(clean_df) -> dict` returns:
  - `rows_clean`, `total_revenue` (rounded to 2 decimals),
    `revenue_by_region` (each value rounded to 2 decimals),
    `top_category` (category with the highest total revenue),
    `first_date` / `last_date` (ISO `YYYY-MM-DD`).
- `write_results(results, dest)`: JSON, UTF-8, indent 2, trailing newline.
- `main(argv)`: runs on the shipped scenario CSV, merges `rows_total`,
  `duplicates_removed`, `missing_amount`, `bad_dates` into the results,
  writes `scenario/shop-export/results.json`, prints
  `rows_total=... rows_clean=...`, returns 0.

Done means `python verify.py starter` exits 0 with all twelve tests
passing, and `python verify.py starter --expect-failure` exits nonzero
because the starter no longer reproduces the unfinished state.
