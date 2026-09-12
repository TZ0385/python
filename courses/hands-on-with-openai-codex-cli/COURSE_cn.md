---
id: course-codex-cli
type: course
title: OpenAI Codex CLI 实战
summary: 与 Claude Code 课程相同的已验证 Python 工作流——任务契约、最小变更、客观 verify.py 证据——改用 OpenAI Codex CLI 完成实战。
lang: zh-CN
content_version: 2
status: reviewed
reviewed_on: 2026-09-12
badge:
  id: course-codex-cli
  name_en: Reproduce with Codex in the loop
  name_zh: Codex 协同复现
  requires: 全部五个检查点认领通过（L01–L05）
course_id: course-codex-cli
---

# OpenAI Codex CLI 实战

> 摘要：下载本文件夹，在你运行 `codex` 的地方打开，说一句 **“开始第 1 课”**。
> 课程结束时你会得到一个可运行的报表工具、一条可复现的通过/失败命令，
> 以及可迁移到任何编码 Agent 的工作流。本课程复用 Claude Code 课程的场景
> 皮肤与代码核心——变的只是你驱动的工具。

## 你将做出什么

与旗舰课程相同的场景报表工具：混乱的 CSV/JSON 输入、无效行隔离而非
崩溃、聚合舍入、原子写报告。文件夹附带三个场景皮肤——选你熟悉的领域：

| 皮肤 | 你的角色 | 数据 |
| --- | --- | --- |
| `scenario/excel-report/` | 把每周订单导出变成区域销售摘要 | `orders.csv` |
| `scenario/data-monitor/` | 检查来自服务器的服务延迟数据 | `metrics.csv` |
| `scenario/api-tool/` | 汇总从内部 API 拉取的工单数据 | `tickets.json` |

同一份代码、同一套九个测试，换一个 Agent 掌舵。

## 教学契约（Agent 请先阅读本节）

- **受众：** 有 AI 协作经验、卡在可靠性上的项目所有者——不是 Python
  入门教程，也不是提示词工程课。
- **前置条件：** PATH 中有 Python 3.11+，已安装并登录 OpenAI Codex CLI，
  能运行 shell 命令。只用标准库——无需安装任何包。
- **工具：** 以 Codex CLI 0.x 完成教学与审核（审核日期 2026-09-12）；
  Codex CLI 主版本更新会触发课程复审。
- **课程顺序：** L01 → L05，每次一课；绝不跳过检查点。
- **教学风格：** 从本文件夹的文件出发。引用你正在满足的契约原文。每个
  失败测试组做最小变更。不新增依赖，不修改 `solution/`，改动当前课程
  未授权的文件前先询问。遵守仓库 AGENTS.md 的规则——它同样约束你。
- **何时停止：** 检查点命令运行通过、且学习者能说清什么失败了、为什么。
- **`verify.py`：** `python verify.py starter --expect-failure` 必须复现
  列出的失败；`python verify.py solution` 必须通过。
- **诚实规则：** 说明哪些没验证过；不宣称生产可用；不承诺结果。

## 本课程不涉及的内容

Codex CLI 安装、模型选择、提示工程、多文件架构、真正的 `.xlsx` 文件、
部署。这些在配套仓库的指南与手册里——链接过去，不要现场发挥。


## 徽章契约

- 徽章：**让 Codex 进环，先复现故障徽章**（徽章 id `course-codex-cli`）——认领全部五个检查点后获得。
- 挑战：L01–L05 检查点各 10 分；五项全部在 flypython.com 认领后另加 50 分课程徽章奖励。
- 证据：`python verify.py progress` —— L03（边界修改）与 L04（验证与审查）由测试套件客观判定；L01/L02/L05 为学习者自报。
- 提交：每个通过的检查点会打印确定性认领码，在 flypython.com 上记入你的账号。这是自我报告的证据，绝不是证书。

## 文件夹结构


与 Claude Code 课程相同的布局：`COURSE.md`/`COURSE_cn.md`、双语
`lessons/`、`scenario/` 皮肤、`TASK.md`/`TASK_cn.md`、`starter/`、
`solution/`、`tests/`、`verify.py`、`REVIEW.md`。代码契约完全一致——
见 `TASK.md`。

## 证据与许可

`REVIEW.md` 记录带日期与工具版本的试跑状态。代码采用 MIT 许可；课程
文字采用 CC BY 4.0（见仓库 `LICENSE`）。教学偏差请走 `course-feedback`
issue 表单。
