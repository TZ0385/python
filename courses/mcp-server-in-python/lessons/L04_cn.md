---
id: course-mcp-tools-l04
type: course
title: "input_required 多轮交互"
summary: "工具可以在调用中途向客户端提问——先返回问题，客户端带答案重试后完成。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# input_required 多轮交互

## 目标

工具可以在调用中途向客户端提问——先返回问题，客户端带答案重试后完成。

## 课程内容

这是 2026-07-28 对服务端发起 elicitation 的替代：处理函数抛出 InputRequired(requests)；服务端返回 resultType 为 "input_required" 及问题；客户端带 params.inputResponses 重试同一调用；处理函数完成。实现它，然后像工程师一样验证：验证器双向、完整套件、以及每处改动都有测试逼着的 diff 审查。

## 练习

- 运行任何命令之前，先在纸上手推一遍完整往返
- 写下三行证据笔记：已验证 / 未验证 / 已知局限

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
