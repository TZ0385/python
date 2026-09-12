---
id: path-foundation-m0
type: path
title: The agent tool landscape
summary: Foundation path module 0 — orientation on Claude Code, Codex CLI, and Cursor; install one agent and observe its evidence habits.
lang: en-US
content_version: 1
status: reviewed
reviewed_on: 2026-09-12
---

# Module 0: The agent tool landscape

**Points:** 10 · **Type:** orientation · **Evidence:** self-attested

Before the hands-on courses, get your bearings: what the tools are, what they
have in common, and which one you will drive first.

## The landscape

Three agentic coding tools matter for this path:

| Tool | Where it runs | What it's good at |
| --- | --- | --- |
| **Claude Code** | terminal | long multi-step tasks, strong instruction following, reads `CLAUDE.md`/`AGENTS.md` |
| **Codex CLI** | terminal | open-source agent loop, sandboxed execution, reads `AGENTS.md` |
| **Cursor** | IDE | inline edits and chat inside an editor, good for people who live in a GUI |

They differ in interface, not in fundamentals. Every one of them: reads your
files, follows written instructions, edits code, runs commands, and — this is
the important part — **can be wrong in ways that look right**. That is why
this path spends so much effort on rules and verification, not on prompts.

## Your first task (no code)

1. Pick **one** of Claude Code or Codex CLI and install it following the
   official docs (linked from the course pages).
2. Open a terminal in an empty folder, start the agent, and ask it:
   "create a Python script that prints the current date, then run it."
3. Watch what it does: which files it creates, which commands it runs,
   what it reports back.
4. Ask it: "how do you know it works?" — notice whether it *shows evidence*
   or just *says it worked*. That gap is what the rest of this path is about.

## Checkpoint

You have finished this module when you can answer, in your own words:

- Which agent did you install, and how do you start it?
- What did it do when you asked for the date script — and what evidence did
  it give you that the script ran?

Self-attested checkpoint: when you can answer both, record it — module M0 of
the Foundation path is worth 10 points. Honest self-reporting is the rule of
this platform: nobody checks your answer, but nothing here is a certificate.
