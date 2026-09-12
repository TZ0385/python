# FlyPython repository 0.0.4 update plan

Version: 0.0.4 (planning draft, revision 2)
Updated: 2026-09-12 (rev 2 — supersedes the same-day local-first draft)
Chinese version: [repo-plan-0.0.4_cn.md](./repo-plan-0.0.4_cn.md)
Related: flypython.com `docs/product-and-growth-plan-0.0.4.md`

Status: planning document only. Nothing here is implemented. The repository
boundary from `AGENTS.md` holds: this repo owns reviewed content, runnable
evidence, and stable JSON contracts; the website owns presentation,
accounts, and conversion. All new content ships English and Chinese in sync.

Revision note: the first 0.0.4 draft proposed local-only progress artifacts
(`PROGRESS.json`, `BADGE.md`). The owner moved the 0.0.4 core to accounts,
server-recorded progress, and a leaderboard (Cloudflare D1 + Workers). This
revision refocuses the repo work on what the website needs from course
folders: **deterministic checkpoint claim codes** and the challenge
narrative. Local artifacts are dropped; the claim code is the contract.

## 1. Theme: checkpoint claim codes for server-recorded progress

The website records progress when a learner enters a claim code printed by
`verify.py` after a checkpoint's suite passes. This repo owns everything
that makes those codes trustworthy and stable:

- The code derives deterministically from `(course_id, checkpoint_id,
  evidence)` where evidence is the objective suite outcome — the same
  inputs always produce the same code, on any machine, offline.
- Codes are short and human-enterable (e.g. 8 chars of base32).
- Codes are spot-checkable, not tamper-proof; the framing everywhere is
  "self-reported evidence", never certification.
- No network access, no accounts, no telemetry in course tooling — the
  website side owns everything behind login.

## 2. Work items

### FP-411 Checkpoint claim codes (`verify.py`)

- New subcommand: `python verify.py progress` prints, per checkpoint, its
  id, name, pass state (derived from the objective suite), and — when
  passed — its claim code.
- Codes are stable across runs and platforms; the derivation (including
  any per-course salt constant) is documented in the course contract and
  reviewed like code.
- Stdlib only; deterministic output; safe to re-run.

### FP-412 Challenge narrative (COURSE.md + lessons)

- COURSE.md gains the badge contract section: course badge name (e.g.
  "Verified Report Tool"), the five checkpoint challenges, and the honest
  self-reported-evidence framing — now pointing at the website's recording
  flow.
- Lessons are labeled as challenges ("Challenge 01: reproduce the
  failure"); checkpoint sections name the badge requirement they satisfy
  and the claim step.
- EN+ZH in the same commit; `reviewed_on` and `content_version` bumped per
  manifest rules.

### FP-413 Badge contract alignment

- Each course's `COURSE.md` declares its badge metadata as structured
  front matter/fields (badge id, display name EN+ZH, requirement text) so
  the website can render badge maps and server records from course data —
  no hand-copied badge definitions on the site side.

### FP-414 Agent-skill packaging (evaluation)

- Evaluate publishing course ingestion as a SKILL.md-compatible skill
  (OpenMAIC / Codex workbenches), following the repository's template
  conventions. Human-authored; pilot recorded honestly before any
  recommendation.

### FP-415 `verify_courses.py` extension

- Extend the course-contract verifier: every checkpoint exposes a claim
  code; codes are deterministic (same inputs → same code across two runs
  and two platforms); format is validated; the progress subcommand is
  exercised in CI.

## 3. Non-goals

No accounts, no server-side judging in this repo, no network access from
course tooling, no certification language, no second copy of site content.
Anti-fraud design stays deliberately light (spot-checkable codes); heavy
anti-fraud is the website's concern and is out of scope here.

## 4. TODO (all unverified)

- [ ] FP-411 claim-code subcommand, all five courses, documented derivation.
- [ ] FP-412 badge contract + challenge narrative, EN+ZH, one change.
- [ ] FP-413 structured badge metadata for site rendering.
- [ ] FP-414 SKILL.md packaging evaluation with a written record.
- [ ] FP-415 `verify_courses.py` claim-code coverage in CI.

## 5. Execution order

1. FP-411 + FP-412 + FP-415 in one change (codes, narrative, checker),
   paired with the website's FP-401/FP-402 groundwork.
2. FP-413 once the website badge rendering shape is fixed.
3. FP-414 after one real external-tool run is recorded.

## 6. Carried forward from 0.0.3 (open)

- FP-326 note: five agent-taught run-throughs still to be recorded in each
  course's `REVIEW.md` (launch evidence, not a content blocker).
- FP-327 release step: website pin bump to this repo's release SHA in one
  deliberate step.
- FP-334 repo description/topics + first GitHub Release; CHANGELOG
  `[Unreleased]` cuts into a version section at that Release.
