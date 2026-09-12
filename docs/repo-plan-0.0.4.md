# FlyPython repository 0.0.4 update plan

Version: 0.0.4 (planning draft)
Updated: 2026-09-12
Chinese version: [repo-plan-0.0.4_cn.md](./repo-plan-0.0.4_cn.md)
Related: flypython.com `docs/product-and-growth-plan-0.0.4.md`

Status: planning document only. Nothing here is implemented. The repository
boundary from `AGENTS.md` holds: this repo owns reviewed content, runnable
evidence, and stable JSON contracts; the website owns presentation and
conversion. All new content ships English and Chinese in sync.

## 1. Theme: the challenge/badge layer lives in course folders

The 0.0.4 site plan adds a "challenges and badges" progression layer over
the agent-taught course format — learned from PentesterLab's badge model but
implemented **local-first**: progress evidence is written by `verify.py` into
the learner's folder, never to a server. This repo owns everything that makes
that real: the verifier behavior, the course narrative, and the contract
checks.

Binding rules:

- No accounts, no network calls, no telemetry in any course tooling.
- Badges are self-reported local evidence; tooling must never print
  certification-style claims.
- Every narrative or badge string ships EN+ZH in the same change.
- `PROGRESS.json` and `BADGE.md` are versioned course outputs with a stable
  shape (documented in the course contract), so the website and external
  tools can render them without guessing.

## 2. Work items

### FP-411 `verify.py progress` (every course)

- New subcommand: `python verify.py progress` reads the current
  implementation state and writes `PROGRESS.json` next to `verify.py`:
  `{"course", "tool", "checkpoints": [{"id", "name", "status": "passed" |
  "open", "evidence_command", "recorded_on"}], "all_passed": bool}`.
- Checkpoint status derives from the objective suite (starter-fails and
  solution-passes per lesson), not from self-assessment.
- Stdlib only; deterministic output; safe to re-run.

### FP-412 Challenge narrative (COURSE.md + lessons)

- COURSE.md gains a badge contract section: course badge name (e.g.
  "Verified Report Tool"), the five checkpoint challenges, and the honest
  self-reported-evidence framing.
- Lessons are labeled as challenges ("Challenge 01: reproduce the failure");
  checkpoint sections name the badge requirement they satisfy.
- EN+ZH in the same commit; `reviewed_on` bumped; content_version bump per
  manifest rules.

### FP-413 Badge artifact

- `python verify.py progress --badge` writes `BADGE.md` when — and only
  when — all checkpoints pass: badge name, course, tool + version, dates,
  and the replay commands. Self-reported evidence; explicitly not a
  certificate.

### FP-414 Agent-skill packaging (evaluation)

- Evaluate publishing course ingestion as a SKILL.md-compatible skill
  (OpenMAIC / Codex workbenches), following the repository's template
  conventions. Human-authored; pilot recorded honestly before any
  recommendation.

### FP-415 `verify_courses.py` extension

- Extend the course-contract verifier: `PROGRESS.json` (when present)
  validates against the documented shape; `BADGE.md` may exist only when
  the record shows all checkpoints passed; the progress subcommand is
  exercised in CI.

## 3. Non-goals

No accounts, no server-side judging, no points/leaderboards/streaks, no
network access from course tooling, no certification language, no second
copy of site content. The website renders badge maps from its own course
data; this repo does not ship site assets.

## 4. TODO (all unverified)

- [ ] FP-411 `verify.py progress` + `PROGRESS.json` contract, all five
      courses.
- [ ] FP-412 badge contract + challenge narrative, EN+ZH, one change.
- [ ] FP-413 `BADGE.md` generation gated on all-checkpoints-passed.
- [ ] FP-414 SKILL.md packaging evaluation with a written record.
- [ ] FP-415 `verify_courses.py` progress-contract coverage in CI.

## 5. Execution order

1. FP-411 + FP-412 + FP-415 in one change (contract, narrative, checker).
2. FP-413 once the progress contract is stable.
3. FP-414 after one real external-tool run is recorded.

## 6. Carried forward from 0.0.3 (open)

- FP-326 note: five agent-taught run-throughs still to be recorded in each
  course's `REVIEW.md` (launch evidence, not a content blocker).
- FP-327 release step: website pin bump to this repo's release SHA in one
  deliberate step.
- FP-334 repo description/topics + first GitHub Release; CHANGELOG
  `[Unreleased]` cuts into a version section at that Release.
