# 综合项目任务：真实数据集的验证分析

**积分：** 200 · **徽章要求：** 数据分析 Agent

端到端跑一遍，Agent 是你的工具：把 `dataset/orders.csv`
（303 行脏数据）走完 清洗 → 探索 → 报告。

## 要求的产出

你的流水线（结构自定）必须写出：

- `out/results.json`，包含键：
  - `rows_total`、`duplicates_removed`、`rows_clean`
  - `total_revenue`（两位小数）、`avg_order_value`（两位小数）、
    `total_quantity`
  - `revenue_by_region`——`{region: 总额}`，两位小数
  - `top_category`——总收入最高的品类
  - `first_date`、`last_date`——ISO 日期
- `out/report.md`，包含 `## Data quality`、`## Findings`、
  `## Appendix` 三节，并写出已验证的总收入数字。

## 数据质量规则

删除完全重复行；删除 `amount` 不可解析、`date` 不可解析、或
`region` 为空的行。其余保留。

## 验证

`python verify.py` 用真值校验 `out/`（容差 0.01），通过时打印综合
项目认领码。参考实现：`solution/capstone.py`——自己尝试过之后再看。

自我报告的证据，绝非证书。
