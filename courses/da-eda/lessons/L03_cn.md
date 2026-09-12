# 挑战 03：清洗与统计

**判卷：** 客观——starter 套件 · **积分：** 10

在 `starter/eda.py` 里实现 `load_transactions`、`clean_transactions`、
`summarize`、`write_results`、`main`。把 `TASK.md` 当契约驱动你的
Agent；它写的每一行都要过目。

注意这几个经典 EDA 陷阱：

- `to_numeric` 不带 `errors="coerce"` 会在 `n/a` 上崩溃而不是计数。
- 先过滤再去重会漏掉脏行的完全重复。
- `groupby().sum()` 会悄悄丢掉 NaN——清洗*之前*就要数清楚。

**检查点：** `python verify.py starter` 退出 0——12 个测试全过。
用 `python verify.py progress` 打印认领码。
