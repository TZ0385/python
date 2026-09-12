---
id: course-mcp-tools-l01
type: course
title: "MCP 到底是什么（2026-07-28）"
summary: "一个面向工具的无状态 JSON-RPC 2.0 接口——无握手、无会话、版本放在 _meta 里。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# MCP 到底是什么（2026-07-28）

## 目标

一个面向工具的无状态 JSON-RPC 2.0 接口——无握手、无会话、版本放在 _meta 里。

## 课程内容

读 TASK.md，然后双向运行验证器。2026-07-28 规范移除了 initialize 握手与会话：服务端直接响应 tools/list 与 tools/call，每个请求通过 _meta 自报协议版本。边读边手动试 scenario/requests/ 里的线路样本。

## 练习

- 先预测 04-removed-initialize.json 的响应，再对照 TASK.md
- 把 starter 的每个预期失败对应到一条规范

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
