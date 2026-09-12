---
id: path-da-capstone
type: path
title: "综合项目：真实数据集的验证分析"
summary: 数据分析路线综合项目——在 orders.csv 上端到端完成清洗、探索与报告，verify.py 校验数字。
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# 综合项目：真实数据集的验证分析

**积分：** 200 · **类型：** 项目 · **证据：** 客观验证（`verify.py`）

数据分析路线的收官挑战。本路线教过的一切——读脏导出、按计数清洗、
产出可核查数字、写出可回溯指标的报告——在
`capstone/dataset/orders.csv` 上端到端用一遍。

## 怎么做

在 `paths/data-analysis/capstone/` 下工作。契约见 `TASK.md`
（中文 `TASK_cn.md`）：你的流水线写出含规定键的 `out/results.json`
和含必需章节的 `out/report.md`，然后 `python verify.py` 用真值校验
数字并打印综合项目认领码。

让 Agent 干繁琐的活——解析、聚合、渲染——并把契约摆在它面前。
solution 文件夹供维护者审核；第一次尝试不要抄它。

## 检查点

`python verify.py` 退出 0 → 认领码计入数据分析路线徽章（200 分）。
自我报告的证据，绝非证书。
