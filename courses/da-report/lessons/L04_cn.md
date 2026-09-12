# 挑战 04：数字可回溯到输入

**判卷：** 客观——双套件 · **积分：** 10

`report.json` 里的每个指标都必须与 `results.json` 中的来源逐数相等。
本挑战回答的审计问题是：“这个数字从哪来的？”——答案是字段名，
不是一段解释。

`python verify.py starter --expect-failure` 现在必须退出非零；
`python verify.py solution` 必须全绿。

**检查点：** 两道门禁都过。用 `python verify.py progress` 取客观
认领码。
