---
id: course-verify-ship-l03
type: course
title: "按测试逐组构建 ship check"
summary: "解析、判定、未验证清单、原子写入、退出码——一次一组失败测试。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# 按测试逐组构建 ship check

## 目标

解析、判定、未验证清单、原子写入、退出码——一次一组失败测试。

## 课程内容

对 Agent 说：“按 TASK.md 修改 starter/ship_check.py，一次只处理一组失败测试：先解析，再判定，再未验证清单，再原子写入，最后 CLI 退出码。每组之后给我看 diff。”

## 练习

- 每组之后运行 PYTHONPATH=starter python -m unittest discover -s tests -v
- 绝不允许为了过测试而弱化判定

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
