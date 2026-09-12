# Task contract: from analysis to report (da-report)

Change only `starter/report.py`. Input:
`scenario/analysis-pack/results.json` — a verified EDA summary.

- `load_inputs(directory) -> dict`: read `results.json`.
- `build_report(inputs) -> dict` returns `{"title", "metrics", "sections"}`:
  - `metrics` carries `rows_total`, `rows_clean`, `total_revenue`,
    `top_category`, `revenue_by_region` **unchanged** from the inputs —
    a report that recomputes differently is a bug, not a feature.
  - `sections` is an ordered list of `{"heading", "body"}` containing
    `Data quality`, `Findings`, `Appendix` in that order.
- `render_markdown(report) -> str`: emits `# <title>`, then
  `## <heading>` per section in order; key numbers appear formatted with
  two decimals (e.g. `33347.89`).
- `write_report(report, markdown, out_dir)`: writes `report.json`
  (UTF-8, indent 2, trailing newline) and `report.md`.
- `main()`: runs the whole pipeline on the shipped scenario pack, writes
  to `out/`, prints a one-line confirmation, returns 0.

Done means `python verify.py starter` exits 0 and
`python verify.py starter --expect-failure` exits nonzero.
