---
id: course-agent-rules-l01
type: course
title: "量化你已经存在的漂移"
summary: "对三个场景仓库运行检查器，把漂移读成测试失败，而不是一种感觉。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# 量化你已经存在的漂移

## 目标

对三个场景仓库运行检查器，把漂移读成测试失败，而不是一种感觉。

## 课程内容

运行 `python starter/rules_check.py scenario/drifted`——它说一切正常。这正是 bug：三个文件对同一行为各执一词，却没有任何东西察觉。然后运行验证器：

## 练习

- 把 `verify.py --expect-failure` 里的每个具名失败对应到一类真实漂移：无真源、无指针识别、无漂移报告
- 打开 `scenario/drifted/.cursorrules`，找出与 AGENTS.md 矛盾的规则

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
