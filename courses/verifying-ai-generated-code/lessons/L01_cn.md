---
id: course-verify-ship-l01
type: course
title: "“能跑”不是证据"
summary: "看着 starter 给零测试的项目和有失败的项目都盖章放行——然后想要更好的东西。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# “能跑”不是证据

## 目标

看着 starter 给零测试的项目和有失败的项目都盖章放行——然后想要更好的东西。

## 课程内容

运行 `python starter/ship_check.py scenario/green-project`，再跑 `.../no-tests`——都是退出 0。一个不会失败的绿色检查只是装饰。运行验证器，看看你要构建的七个行为：

## 练习

- 把每个预期失败对应到真实缺口：解析计数、零测试判定、未验证清单、原子写入、退出码
- 打开 scenario/red-project/tests，找出写错的断言

## 检查点

本课的命令运行通过，并且你能用自己的话说清什么失败了、为什么。

## 预期证据

命令输出记录与你的回答。
