# 任务契约：从分析到报告（da-report）

只允许修改 `starter/report.py`。输入：
`scenario/analysis-pack/results.json`——一份经过验证的 EDA 摘要。

- `load_inputs(directory) -> dict`：读取 `results.json`。
- `build_report(inputs) -> dict` 返回 `{"title", "metrics", "sections"}`：
  - `metrics` 原样携带输入的 `rows_total`、`rows_clean`、
    `total_revenue`、`top_category`、`revenue_by_region`——报告里重新
    算出不同数字是缺陷，不是功能。
  - `sections` 是 `{"heading", "body"}` 的有序列表，按序包含
    `Data quality`、`Findings`、`Appendix`。
- `render_markdown(report) -> str`：输出 `# <title>`，然后按序输出
  各节的 `## <heading>`；关键数字以两位小数呈现（如 `33347.89`）。
- `write_report(report, markdown, out_dir)`：写出 `report.json`
  （UTF-8、缩进 2、末尾换行）和 `report.md`。
- `main()`：对随课数据包跑完整流程，写入 `out/`，打印一行确认，
  返回 0。

完成标准：`python verify.py starter` 退出 0，且
`python verify.py starter --expect-failure` 退出非零。
