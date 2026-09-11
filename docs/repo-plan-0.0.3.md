# FlyPython repository 0.0.3 update plan

Version: 0.0.3 (planning draft)
Updated: 2026-09-11
Chinese version: [repo-plan-0.0.3_cn.md](./repo-plan-0.0.3_cn.md)
Related: flypython.com `docs/product-and-growth-plan-0.0.3.md`

Status: planning document only. Nothing here is implemented. This plan keeps the
repository boundary from `AGENTS.md`: this repo owns reviewed content, runnable
evidence, and stable JSON contracts; the website owns presentation and
conversion. All new content ships English and Chinese in sync.

## 1. What the website's 0.0.3 direction requires from this repo

The site plan makes "agent-taught courses" the primary product line, adds a
Project Radar weekly, and turns this repo into the top-of-funnel channel
(4.1k stars). That requires five repo-side capabilities:

1. A `courses/` content type: agent-teachable folders with objective
   verification.
2. A structured Project Radar data source (per-project YAML, not a README
   table).
3. A discovery tool that produces review candidates without generating
   descriptions.
4. Contract updates: content-manifest, catalog export, schemas, llms files.
5. Referral overhaul of README/README_cn per `docs/REPO_TO_WEBSITE.md`.

## 2. `courses/` specification (new top-level directory)

Each course is one folder, assembled from existing guides/playbooks/examples
wherever possible:

```
courses/<slug>/
  COURSE.md            # metadata + teaching contract the agent reads first:
                       # audience, prerequisites, tool + version, lesson order,
                       # teaching style rules, when to stop, how to use
                       # verify.py, what the course does NOT cover
  lessons/
    L01.md  L01_cn.md  # objective, exercise, checkpoint, expected evidence
    ...
  scenario/            # data files for the chosen "skin" (same skills,
                       # relatable domain)
  TASK.md              # task contract (reuse templates/TASK_CONTRACT.md)
  starter/  solution/  # runnable pair
  verify.py            # objective pass/fail; stdlib-only where possible
  REVIEW.md            # maintainer run-through record: date, tool, version,
                       # deviations observed while the agent taught
```

Rules (to be added to `AGENTS.md` editorial standards):

- The agent teaches from these files; nothing requires a website, account, or
  video. `verify.py` is the completion evidence.
- Bilingual: `*_cn.md` ships with every English lesson in the same commit; a
  course is incomplete until both exist.
- `COURSE.md` must name the exact tool and version it was taught with
  (e.g. "Claude Code 2.x", "Codex CLI 0.x") plus `reviewed_on`; tool major
  releases trigger re-review.
- The REVIEW.md human run-through is screen-recorded when feasible: the
  recording doubles as the site's demo-video source material (see website
  plan §4.5).
- No invented outcomes, salaries, or "guaranteed to learn" claims.

First batch (assembled, not rewritten): C1 Claude Code × Python hands-on
(flagship, 3 scenario skins: Excel/report automation, data monitor, small API
tool); C2 Codex CLI; C3 AGENTS.md single-source; C4 verify-and-ship for
AI-generated code; C5 MCP server in Python. See the site plan §2.2.

## 3. Project Radar data model

Replace the table in `catalog/projects/README.md` with one YAML per project
(same authoring model as `catalog/resources/`):

```yaml
id: marimo
repo: marimo-team/marimo
url: https://github.com/marimo-team/marimo
category: notebooks          # controlled list, extend deliberately
status: rising               # new|rising|stable|major-update|experimental|archived
first_seen: 2026-09-02
reviewed_on: 2026-09-02
license: Apache-2.0
evidence:
  last_release: "…"
  release_cadence: "…"
  maintenance: "…"
ai_familiarity: low          # low|medium|high — covered by mainstream model
                             # training data? (the AI-era differentiator)
alternatives: [jupyter, quarto]
when_not_to_use: "…"
rationale: "…"               # human-written, per curation policy
risk: "…"
```

- `tools/render_readmes.py` regenerates the Radar table from YAML (same
  generated-block convention as the catalog index).
- New deterministic export `radar.json` + `schema/radar-v1.schema.json`,
  rather than expanding `catalog-v1` (which is consumed and pinned). Versioned
  the same way; website consumers pin a full commit.
- Migrate the existing 7 entries as the seed set.

## 4. `tools/radar_scan.py` (candidate discovery only)

- Inputs: GitHub Search API (recent `language:Python` repos by star velocity),
  PyPI release feeds for cataloged projects, top HN/r/Python posts.
- Output: `catalog/projects/candidates.json` — repo url, stars, recent
  release, license, first-seen date. **No descriptions, no status.** Humans
  write rationale/risk and choose status, per `AGENTS.md` and
  `CURATION_POLICY.md`.
- Read-only, rate-limited, no private endpoints (same constraints as
  `check_links.py`).

## 5. Contract and tooling updates

- `schema/content-manifest-v1.schema.json`: add `"course"` to `type`
  (schema bump requires a manifest regeneration and website-side pin update
  in the same deliberate step).
- `tools/build_content_manifest.py`: walk `courses/` like guides/playbooks;
  sha256 per locale file.
- New `tools/verify_courses.py` (mirrors `verify_examples.py`): checks folder
  contract — COURSE.md present, lesson EN/CN pairs aligned, verify.py runs
  against starter (expect failure) and solution (expect pass).
- `llms.txt` / `llms-full.txt`: add courses and radar sections; deep links to
  course folders and `radar.json`.
- `docs/CURATION_POLICY.md`: extend scope sentence to cover courses and radar
  entries; document `ai_familiarity` grading rules.
- `.github/ISSUE_TEMPLATE/`: add `course-feedback.yml` (report teaching
  drift / unclear lesson / verify mismatch) alongside project-proposal.
- GitHub housekeeping: keyword-bearing repo description and topics; first
  versioned Release so watchers get notified (supports the site plan's
  content cadence).

## 6. Referral overhaul (per `docs/REPO_TO_WEBSITE.md`)

- README/README_cn: top banner → `https://flypython.com/from-github`
  (only after that route exists and is verified in production; until then link
  the site root, per the doc's own rule).
- Per-guide/playbook/example footer: one contextual link to the matching site
  page — same-task continuation, not a generic banner.
- Repo description rewritten around the new positioning
  ("AI writes Python; we make it verifiable and deliverable" — final wording
  at implementation time).

## 7. Execution order

1. `courses/` spec + `verify_courses.py` + C1 folder (EN+CN) → manifest/schema
   updates in the same change.
2. Radar YAML migration + `radar.json` export + schema + README rendering.
3. `radar_scan.py` + first candidate list.
4. llms files, curation policy, issue template, repo description/topics.
5. README referral pass once `/from-github` is verified live.
6. Releases/tagging cadence starts with the first course drop.

## 8. TODO (continues site-plan numbering; all unverified)

- [ ] FP-325 `courses/` spec lands in `AGENTS.md` + this doc finalized;
  COURSE.md teaching contract reviewed.
- [ ] FP-326 C1 course folder complete (3 skins, verify.py both directions,
  EN+CN, REVIEW.md from a real run-through).
- [ ] FP-327 Manifest `type: "course"` + schema + `build_content_manifest.py`
  walk; website pin bump coordinated (single deliberate step, FP-224 rule).
- [ ] FP-328 `verify_courses.py` in the validation workflow + Makefile.
- [ ] FP-329 `catalog/projects/` → per-project YAML (7 seeds migrated) +
  `render_readmes.py` regeneration verified.
- [ ] FP-330 `radar.json` export + `schema/radar-v1.schema.json` +
  `export_catalog.py` extension; `--check` mode green.
- [ ] FP-331 `tools/radar_scan.py` merged with rate limits and no-description
  guarantee tested.
- [ ] FP-332 llms.txt / llms-full.txt courses+radar sections; deep links valid
  (website-side llms-links test stays green after pin bump).
- [ ] FP-333 `CURATION_POLICY.md` scope + `ai_familiarity` grading rules;
  `course-feedback.yml` issue template.
- [ ] FP-334 Repo description/topics/keywords; first GitHub Release.
- [ ] FP-335 README/README_cn banner + per-doc contextual footers, gated on
  verified `/from-github` route.
- [ ] FP-344 Dual LICENSE in place (MIT code / CC BY 4.0 content) in both
  repositories — prerequisite for course-folder distribution and FP-326.
- [ ] FP-350 Validators and schemas catch up to policy: `validate_catalog.py`
  + `catalog-v1`/`radar-v1` support radar lifecycle statuses and
  `ai_familiarity`; manifest schema gains `type: "course"`; CHANGELOG
  `[Unreleased]` cut into a `0.1.0` section at the first Release (FP-334).

## 9. Non-goals and risks

- This repo stays a content/evidence source: no website features, no paid
  content, no analytics, no keys in git.
- Course quality risk: agents drift from COURSE.md — mitigated by verify.py
  plus a recorded human run-through (REVIEW.md), not by promises.
- Radar volume risk: candidates are cheap, reviewed entries are not — the
  human review step is the deliberate bottleneck and must stay one.
- Pin discipline: every schema/manifest change pairs with a deliberate
  website pin bump; never a moving-branch dependency.
