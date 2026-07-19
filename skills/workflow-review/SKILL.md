---
name: workflow-review
description: Orchestration workflow for code reviews, audits, or risk assessments.
---

# Review Workflow

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. `code-reviewer` reviews the requested scope.
2. Report findings first, ordered by severity, with file/line references when available.
3. Do not make edits, run `implementer`, or enter a fix loop unless the user explicitly asks to fix the findings.
