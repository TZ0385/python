# 任务契约：数据可视化（da-visualization）

只允许修改 `starter/charts.py`。输入：
`scenario/sales-clean/sales_daily.csv`——干净的长表数据
（date、region、revenue；135 行，45 天，3 个地区）。

- `load_sales(path) -> DataFrame`，`date` 列已解析为日期。
- `summary(df) -> dict`：
  - `revenue_by_region`——各地区总额，两位小数。
  - `daily_revenue`——每日总额（ISO 日期键），两位小数。
  - `grand_total`——两位小数。
- `revenue_by_region(df, dest)`——柱状图 PNG 写到 `dest`。
- `daily_revenue(df, dest)`——折线图 PNG 写到 `dest`。
- `revenue_histogram(df, dest)`——直方图 PNG 写到 `dest`。
- `main()`——写出 `out/revenue_by_region.png`、`out/daily_revenue.png`、
  `out/revenue_histogram.png` 与 `out/summary.json`（UTF-8、缩进 2、
  末尾换行）；打印一行确认；返回 0。

约束：只用 matplotlib Agg 后端（不需要显示器）；图必须*由数据生成*，
绝不许硬编码。验证检查 PNG 文件存在且有效、summary.json 的数字与
数据集一致——它不评价图好不好看。

完成标准：`python verify.py starter` 退出 0，且
`python verify.py starter --expect-failure` 退出非零。
