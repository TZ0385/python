---
id: course-mcp-tools
type: course
title: Give your agent tools with MCP (Python)
summary: Build a stateless Model Context Protocol tool server in pure Python — JSON-RPC 2.0 dispatch, schema validation, error isolation, and the 2026-07-28 input_required round-trip — and learn where a real tool belongs.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# Give your agent tools with MCP (Python)

> TL;DR: download this folder, open it in your coding agent, and say
> **"start lesson 1"**. You finish with a working MCP tool server that
> implements the stateless 2026-07-28 specification — no initialize
> handshake, validated tool arguments, isolated handler failures, and the
> multi-round input_required flow — proven by a failing starter and a
> passing solution. Standard library only; no API key needed.

## What you build

The same reviewed MCP tool server contract the repository ships as a
runnable example, assembled into a course: a `MCPServer` class that answers
`tools/list` and `tools/call` directly, rejects bad requests with the right
JSON-RPC error codes, validates arguments against declared schemas, isolates
handler exceptions as structured `isError` results, and completes the
`input_required` round-trip. Sample request files under `scenario/requests/`
let you poke the wire format while you learn:

| File | What it exercises |
| --- | --- |
| `01-tools-list.json` | direct listing with no handshake |
| `02-echo-call.json` | a successful tools/call |
| `03-missing-argument.json` | argument validation failure |
| `04-removed-initialize.json` | the removed initialize method |

## Teaching contract (read this first, agent)

- **Audience:** developers who want their agent to call their own code
  safely — and want to understand the protocol instead of pasting a server
  scaffold.
- **Prerequisites:** Python 3.11+ on PATH, comfort reading JSON, and any
  coding agent (taught and reviewed with Claude Code 2.x; reviewed
  2026-09-12). Standard library only.
- **Lesson order:** L01 → L05; never skip the checkpoint.
- **Teaching style:** work from the files in this folder; quote the
  specification line you satisfy; smallest change per failing test group; no
  new dependencies; never edit `solution/`; ask before touching unnamed
  files.
- **When to stop:** a lesson is done when its checkpoint command runs and
  the learner can explain what failed and why.
- **`verify.py`:** `python verify.py starter --expect-failure` reproduces
  the listed failures; `python verify.py solution` passes the full suite.
- **Honesty rules:** this course builds the server side of the protocol; it
  does not certify any specific client's compliance. Say what you did not
  verify.

## What this course does NOT cover

Transports beyond plain JSON-RPC dicts (stdio/HTTP wiring), deployment, or
client-side configuration. The repository's MCP migration guide covers
moving existing servers to the 2026-07-28 specification.

## Folder map

`COURSE.md`/`COURSE_cn.md`, bilingual `lessons/`, `scenario/requests/`
wire samples, `TASK.md`/`TASK_cn.md` (the full server contract),
`starter/`, `solution/`, `tests/`, `verify.py`, `REVIEW.md`.

## Evidence and licensing

`REVIEW.md` records the run-through state. Code is MIT; prose is CC BY 4.0
(see repository `LICENSE`). Teaching drift goes to the `course-feedback`
issue form.
