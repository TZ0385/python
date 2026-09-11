# Maintainer run-through record

## 2026-09-12 — contract verification (mechanical)

- Environment: macOS (arm64), Python 3.13; repository clean checkout on
  branch `feat/0.0.3-courses-and-radar`.
- Commands and results:
  - `python verify.py starter --expect-failure` — exit 0; all seven expected
    failure names reproduced (JSON loading, unsupported suffix, row
    isolation, rounding, parent directories, scenario report, CLI summary).
  - `python verify.py solution` — exit 0; 9/9 tests pass.
  - All three skins exercised end to end through `run_scenario` in the test
    suite (`excel-report`, `data-monitor`, `api-tool`); report totals and
    group sums recomputed by hand against the scenario data files.
- Not verified in this pass: teaching quality with a live agent session.

## Pending before the public course drop

- One full agent-taught run-through with Claude Code 2.x ("start lesson 1"
  through Lesson 5 checkpoint), recording observed deviations from
  COURSE.md here. This recording doubles as the demo-video source material
  per the 0.0.3 plan §4.5.
- Course status remains `reviewed` for content and code; the agent-teaching
  sample is tracked as launch evidence, not a content blocker.

## Deviation log

(none recorded yet — first agent-taught run-through pending)
