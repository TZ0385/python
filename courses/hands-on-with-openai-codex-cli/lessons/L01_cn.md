---
id: course-codex-cli-l01
type: course
title: "第 1 课：让 Codex 进环，先复现故障"
summary: "双向运行验证器，把每个失败测试对应到真实故障，并学会如何把文件夹交给 Codex。"
lang: zh-CN
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# 第 1 课：让 Codex 进环，先复现故障

## 目标

双向运行验证器，把每个失败测试对应到真实故障，并学会如何把文件夹交给 Codex。

## 课程内容

在课程文件夹里运行 `codex`，说“开始第 1 课”。Codex 会先读 COURSE.md——教学契约约束它能碰什么。然后你自己运行客观验证命令：

## 练习

- `test_load_json_records_returns_list_of_dicts` —— 只认 CSV；API 皮肤直接崩溃
- `test_invalid_records_are_isolated_with_reasons` —— 一个空单元格让整次运行中止
- `test_group_totals_are_rounded_to_two_decimals` —— `0.1 + 0.2` 打印出 `0.30000000000000004`
- `test_write_report_creates_missing_parent_directories` —— 新建输出目录写不进去

## 检查点

`python verify.py starter --expect-failure` 复现列出的失败、`python verify.py solution` 通过——并且你不看资料也能说出四个缺失行为。

## 预期证据

命令输出记录与你的回答。第 4 课会再次用到。
