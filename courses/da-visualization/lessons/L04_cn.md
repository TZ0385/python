# 挑战 04：数字与图一致

**判卷：** 客观——双套件 · **积分：** 10

套件用数据集真值校验 `summary.json`（East 12334.94、North 14294.7、
South 11200.48、总计 37830.12、45 天）。图里呈现的数字和 JSON 不一致，
就是失败的图——JSON 才是可审计的那一层。

`python verify.py starter --expect-failure` 现在必须退出非零；
`python verify.py solution` 必须全绿。

**检查点：** 两道门禁都过。用 `python verify.py progress` 取客观
认领码。
