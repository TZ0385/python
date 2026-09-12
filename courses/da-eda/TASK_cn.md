# 任务契约：探索性数据分析（da-eda）

只允许修改 `starter/eda.py`。数据集是
`scenario/shop-export/transactions.csv`——一份商店导出，含完全重复行、
缺失/不可解析的金额、以及一条坏日期。

- `load_transactions(path) -> pandas.DataFrame`：读取 CSV。
- `clean_transactions(df) -> (clean_df, stats)`：
  - 删除完全重复的行，数量记入 `duplicates_removed`。
  - 把 `amount` 解析为数值；解析失败的行移除并记入 `missing_amount`。
  - 把 `date` 解析为日期；解析失败的行移除并记入 `bad_dates`。
  - `stats = {"duplicates_removed": int, "missing_amount": int,
    "bad_dates": int}`；清洗后的行保留解析好的 `amount` 与 `date`。
- `summarize(clean_df) -> dict` 返回：
  - `rows_clean`、`total_revenue`（保留两位小数）、
    `revenue_by_region`（每个值保留两位小数）、
    `top_category`（总收入最高的品类）、
    `first_date` / `last_date`（ISO `YYYY-MM-DD`）。
- `write_results(results, dest)`：JSON，UTF-8，缩进 2，末尾换行。
- `main(argv)`：处理随课附带的场景 CSV，把 `rows_total`、
  `duplicates_removed`、`missing_amount`、`bad_dates` 合并进结果，
  写出 `scenario/shop-export/results.json`，打印
  `rows_total=... rows_clean=...`，返回 0。

完成的标准：`python verify.py starter` 退出 0 且全部 12 个测试通过；
`python verify.py starter --expect-failure` 退出非零——因为 starter
已不再处于未完成状态。
