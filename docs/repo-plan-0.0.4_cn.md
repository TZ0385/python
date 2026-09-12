# FlyPython 仓库 0.0.4 更新计划

版本：0.0.4（规划草稿）
更新日期：2026-09-12
英文正本：[repo-plan-0.0.4.md](./repo-plan-0.0.4.md)（治理以英文版为准）
关联：flypython.com `docs/product-and-growth-plan-0.0.4.md`

状态：仅规划文档。本文件所述内容均未实现。`AGENTS.md` 的仓库边界不变：
本仓库拥有经审核的内容、可运行的证据与稳定的 JSON 契约；网站拥有呈现
与转化。所有新内容中英同一次变更交付。

## 1. 主题：挑战/徽章层落在课程文件夹里

网站 0.0.4 计划在"Agent 授课"课程形态之上加一层"挑战与徽章"进阶层
——借鉴 PentesterLab 的徽章模型，但以**本地优先**实现：进度证据由
`verify.py` 写进学习者的文件夹，绝不写进服务器。让它成立的一切都归本
仓库所有：验证器行为、课程叙事、契约检查。

约束规则：

- 课程工具中无账号、无网络调用、无遥测。
- 徽章是自我报告的本地证据；工具输出绝不得出现认证式声明。
- 每条叙事或徽章文案中英同一次变更交付。
- `PROGRESS.json` 与 `BADGE.md` 是形状稳定（在课程契约中文档化）的
  版本化课程输出，网站与外部工具无需猜测即可渲染。

## 2. 工作项

### FP-411 `verify.py progress`（每门课程）

- 新子命令：`python verify.py progress` 读取当前实现状态，在
  `verify.py` 旁写出 `PROGRESS.json`：
  `{"course", "tool", "checkpoints": [{"id", "name", "status": "passed" |
  "open", "evidence_command", "recorded_on"}], "all_passed": bool}`。
- 检查点状态来自客观套件（每课的 starter 失败与 solution 通过），
  不来自自我评估。
- 仅用标准库；输出确定；可安全重复运行。

### FP-412 挑战叙事（COURSE.md + 课程）

- COURSE.md 增加徽章契约章节：课程徽章名（如"Verified Report Tool"）、
  五个检查点挑战、以及"自我报告的本地证据"的诚实表述。
- 课程标注为挑战（"挑战 01：复现故障"）；检查点小节写明它满足的徽章
  要求。
- 中英同一次提交；`reviewed_on` 更新；按 manifest 规则升级
  content_version。

### FP-413 徽章产物

- 当且仅当全部检查点通过时，`python verify.py progress --badge` 写出
  `BADGE.md`：徽章名、课程、工具 + 版本、日期、复现命令。自我报告的
  证据；明确不是证书。

### FP-414 Agent skill 打包（评估）

- 评估把课程摄取发布为 SKILL.md 兼容的 skill（OpenMAIC / Codex 工作
  台），遵循仓库模板约定。人工撰写；先留下真实试点记录再给建议。

### FP-415 `verify_courses.py` 扩展

- 扩展课程契约验证器：`PROGRESS.json`（如存在）按文档化形状校验；
  `BADGE.md` 仅在记录显示全部检查点通过时才允许存在；进度子命令
  纳入 CI 演练。

## 3. Non-goals

无账号、无服务端判题、无积分/排行榜/连续打卡、课程工具无网络访问、
无认证式措辞、无网站内容第二副本。网站用自己侧的课程数据渲染徽章
地图；本仓库不产出网站资产。

## 4. TODO（全部未验证）

- [ ] FP-411 全部五门课程的 `verify.py progress` + `PROGRESS.json` 契约。
- [ ] FP-412 徽章契约 + 挑战叙事，中英一次变更交付。
- [ ] FP-413 以"全部检查点通过"为门的 `BADGE.md` 生成。
- [ ] FP-414 SKILL.md 打包评估，附书面记录。
- [ ] FP-415 `verify_courses.py` 进度契约覆盖进 CI。

## 5. 执行顺序

1. FP-411 + FP-412 + FP-415 一次变更完成（契约、叙事、检查器）。
2. 进度契约稳定后做 FP-413。
3. 记录一次真实外部工具运行后再做 FP-414。

## 6. 自 0.0.3 结转（未完成）

- FP-326 备注：五次 Agent 实机授课记录仍待写入各课程 `REVIEW.md`
  （属于发布证据，不是内容阻塞项）。
- FP-327 发布步骤：网站 pin 在一次刻意变更中固定到本仓库发布 SHA。
- FP-334 仓库描述/话题 + 首个 GitHub Release；该 Release 时将
  CHANGELOG `[Unreleased]` 切为正式版本小节。
