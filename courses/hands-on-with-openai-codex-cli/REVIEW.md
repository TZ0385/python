# Maintainer run-through record

## 2026-09-12 — contract verification (mechanical)

- Environment: macOS (arm64), Python 3.13; repository clean checkout on
  branch `feat/0.0.3-courses-and-radar`.
- The code core is the reviewed Claude Code course core reused per the 0.0.3
  plan §2.2 ("reuse C1 skins"): same starter/solution/tests contract.
- Commands and results:
  - `python verify.py starter --expect-failure` — exit 0; all seven expected
    failure names reproduced.
  - `python verify.py solution` — exit 0; 9/9 tests pass.
  - All three skins exercised end to end by the shared suite.
- Not verified in this pass: teaching quality with a live Codex CLI session.

## Pending before the public course drop

- One full agent-taught run-through with Codex CLI 0.x ("start lesson 1"
  through the Lesson 5 checkpoint), recording observed deviations from
  COURSE.md here; the recording doubles as demo-video source material.

## Deviation log

(none recorded yet — first agent-taught run-through pending)
