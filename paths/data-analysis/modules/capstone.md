---
id: path-da-capstone
type: path
title: "Capstone: verified analysis of a real dataset"
summary: Data Analysis path capstone — end-to-end clean, explore, and report on orders.csv with verify.py checking the numbers.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# Capstone: verified analysis of a real dataset

**Points:** 200 · **Type:** project · **Evidence:** objective (`verify.py`)

The final challenge of the Data Analysis path. Everything the path taught —
loading messy exports, cleaning with counted removals, summarizing with
checkable numbers, reporting with traceable metrics — applied end to end
on `capstone/dataset/orders.csv`.

## What to do

Work in `paths/data-analysis/capstone/`. The contract is `TASK.md`
(`TASK_cn.md` for 中文): your pipeline writes `out/results.json` with the
specified keys and `out/report.md` with the required sections, then
`python verify.py` checks the numbers against ground truth and prints the
capstone claim code.

Use your agent for the boring parts — parsing, aggregation, rendering —
and keep the contract in front of it. The solution folder exists for
maintainer review; do not copy it for your first attempt.

## Checkpoint

`python verify.py` exits 0 → claim code recorded against the Data
Analysis path badge (200 points). Self-reported evidence, never a
certificate.
