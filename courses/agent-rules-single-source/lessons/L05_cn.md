---
id: course-agent-rules-l05
type: course
title: "把这套方法带回你的仓库"
summary: "一个 AGENTS.md，其余全是瘦指针，一旦破坏检查就失败。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# 把这套方法带回你的仓库

## 目标

一个 AGENTS.md，其余全是瘦指针，一旦破坏检查就失败。

## 课程内容

在你自己的仓库里：把 AGENTS.md 写成（或修剪成）唯一规则真源，把其他规则文件替换为瘦指针，把 rules_check.py 和它的测试命令加进 CI。工作流才是产品；检查器只是护栏。

## 练习

- 在干净检出上运行检查器，证明它不依赖你的机器

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
