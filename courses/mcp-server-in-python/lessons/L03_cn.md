---
id: course-mcp-tools-l03
type: course
title: "校验与错误隔离"
summary: "参数是不可信输入：先校验再执行，绝不让处理函数打断传输。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# 校验与错误隔离

## 目标

参数是不可信输入：先校验再执行，绝不让处理函数打断传输。

## 课程内容

两条边界让工具服务变得安全：按声明的 inputSchema 校验必填参数（缺参变成结构化结果而不是异常），并包裹每个处理函数，让它的失败返回 isError 而不是断开连接。03-missing-argument.json 在线路上演示了第一条边界。

## 练习

- 把每个校验测试对应到它锚定的契约行
- 问：如果处理函数抛出 InputRequired 会怎样？（下一课。）

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
