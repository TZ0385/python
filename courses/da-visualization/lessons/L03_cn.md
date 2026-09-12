# 挑战 03：三张图与摘要

**判卷：** 客观——starter 套件 · **积分：** 10

在 `starter/charts.py` 里实现契约。驱动 Agent 时的要点：

- `matplotlib.use("Agg")` 必须在导入 pyplot *之前*执行，否则在没有
  显示器的机器上直接崩。
- 在未解析的字符串列上 `groupby("date")` 会按字典序排——先解析日期。
- 测试检查 PNG 魔数：不是真 PNG 的文件会失败。

**检查点：** `python verify.py starter` 退出 0。用
`python verify.py progress` 取认领码。
