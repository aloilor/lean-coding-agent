---
name: workflow-review
description: Orchestration workflow for a code review, audit, or risk assessment when the deliverable is findings and NOT edits. Spawns the code-reviewer subagent and reports findings by severity without entering a fix loop. Invoke from the main agent when the user asks to review without asking for changes.
---

# Review Workflow

Use when the user asks for a code review, audit, or risk assessment without asking for edits.

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, **Workflow Tiering**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. `code-reviewer` reviews the requested scope.
2. Report findings first, ordered by severity, with file/line references when available.
3. Do not make edits, run `implementer`, or enter a fix loop unless the user explicitly asks to fix the findings.
