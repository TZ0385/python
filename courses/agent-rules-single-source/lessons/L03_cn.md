---
id: course-agent-rules-l03
type: course
title: "按测试驱动一次有边界的变更"
summary: "让 starter 依次识别真源、指针、副本与漂移——一次一组失败测试。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# 按测试驱动一次有边界的变更

## 目标

让 starter 依次识别真源、指针、副本与漂移——一次一组失败测试。

## 课程内容

对 Agent 说：“按 TASK.md 修改 starter/rules_check.py，一次只处理一组失败测试：先指针识别，再真源要求，再副本/漂移分类，最后 CLI 退出码。每组之后给我看 diff。”

## 练习

- 每组之后运行 PYTHONPATH=starter python -m unittest discover -s tests -v
- 拒绝任何触碰 tests/、solution/ 或 scenario/ 的改动

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
