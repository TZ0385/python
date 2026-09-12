# Capstone task: verified analysis of a real dataset

**Points:** 200 · **Badge requirement:** Data Analysis Agent

End to end, with your agent as the tool: take
`dataset/orders.csv` (303 messy rows) through clean → explore → report.

## Required output

Your pipeline (any structure you choose) must write:

- `out/results.json` with keys:
  - `rows_total`, `duplicates_removed`, `rows_clean`
  - `total_revenue` (2 decimals), `avg_order_value` (2 decimals),
    `total_quantity`
  - `revenue_by_region` — `{region: total}` at 2 decimals
  - `top_category` — category with the highest total revenue
  - `first_date`, `last_date` — ISO dates
- `out/report.md` containing the sections `## Data quality`,
  `## Findings`, `## Appendix` and stating the verified total revenue.

## Data quality rules

Drop exact duplicates; drop rows with unparseable `amount`, unparseable
`date`, or blank `region`. Everything else stays.

## Verification

`python verify.py` checks `out/` against ground truth (tolerance 0.01)
and prints the capstone claim code on success. Reference implementation:
`solution/capstone.py` — look at it only after your own attempt.

Self-reported evidence, never a certificate.
