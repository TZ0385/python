---
id: course-codex-cli
type: course
title: Hands-on with OpenAI Codex CLI
summary: The same verified Python workflow as the Claude Code course — task contract, bounded change, objective verify.py evidence — taught hands-on with the OpenAI Codex CLI instead.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# Hands-on with OpenAI Codex CLI

> TL;DR: download this folder, open it where you run `codex`, and say **"start
> lesson 1"**. You finish with a working report tool, a reproducible
> pass/fail command, and a workflow that transfers to any capable coding
> agent. This course reuses the scenario skins and code core of the Claude
> Code course — only the tool you drive changes.

## What you build

The same scenario report tool as the flagship course: messy CSV/JSON input,
invalid rows isolated instead of crashing, rounded aggregates, atomic report
writes. Three scenario skins ship with the folder — pick the domain you know:

| Skin | You are… | Data |
| --- | --- | --- |
| `scenario/excel-report/` | turning a weekly orders export into a region summary | `orders.csv` |
| `scenario/data-monitor/` | checking service latency numbers from your servers | `metrics.csv` |
| `scenario/api-tool/` | summarizing ticket data pulled from an internal API | `tickets.json` |

Same code, same nine tests, different agent at the wheel.

## Teaching contract (read this first, agent)

- **Audience:** a project owner who has working-with-AI experience and is
  stuck on reliability — not a Python beginner tutorial, not prompt tricks.
- **Prerequisites:** Python 3.11+ on PATH, the OpenAI Codex CLI installed
  and signed in, and the ability to run shell commands. Standard library
  only — nothing to install.
- **Tool:** taught and reviewed against Codex CLI 0.x (reviewed 2026-09-12);
  a Codex CLI major release triggers a course re-review.
- **Lesson order:** L01 → L05, one per session; never skip the checkpoint.
- **Teaching style:** work from the files in this folder. Quote the contract
  line you are satisfying. Smallest change per failing test group. No new
  dependencies, never edit `solution/`, ask before touching files the
  current lesson does not name. Respect the repository's AGENTS.md rules —
  they apply to you.
- **When to stop:** a lesson is done when its checkpoint command runs and
  the learner can explain what failed and why.
- **`verify.py`:** `python verify.py starter --expect-failure` must reproduce
  the listed failures; `python verify.py solution` must pass.
- **Honesty rules:** say what you did not verify; no production-ready
  claims; no promised outcomes.

## What this course does NOT cover

Installing Codex CLI, model selection, prompt engineering, multi-file
architecture, real `.xlsx` files, or deployment. The companion repository's
guides and playbooks cover those — link, don't improvise.

## Folder map

Same layout as the Claude Code course: `COURSE.md`/`COURSE_cn.md`, bilingual
`lessons/`, `scenario/` skins, `TASK.md`/`TASK_cn.md`, `starter/`,
`solution/`, `tests/`, `verify.py`, and `REVIEW.md`. The code contract is
identical — see `TASK.md`.

## Evidence and licensing

`REVIEW.md` records the run-through state with dates and tool versions.
Code is MIT-licensed; lesson prose is CC BY 4.0 (see repository `LICENSE`).
Teaching drift goes to the `course-feedback` issue form.
