---
name: workflow-bug-fixing
description: Orchestration workflow for bugs, failing tests, CI failures, runtime errors, or regressions. Coordinates diagnosis, approval, implementation, review, and tier-appropriate artifacts.
---

# Bug Fixing Workflow

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. `bug-diagnostician` investigates the failure and drafts the incident report.
2. Show the user the symptom, evidence or likely root cause, proposed fix direction, and verification plan. Wait for explicit approval before any implementation.
3. After approval, `implementer` applies `tdd` plus `engineering-standards`: reproduce the bug with an existing failing test or a focused regression test and observe RED; make the smallest root-cause fix; then refactor only while green. If automated reproduction is impractical, document why and record the strongest substitute evidence. Run broader verification and create the standard implementation report.
4. `code-reviewer` reviews the incident evidence, implementation report, verification, and affected code. The reviewer may inspect untouched code to establish impact, but only change-caused or explicitly approved in-scope findings become implementation work; ripple findings require scope approval and unrelated pre-existing debt stays out of scope. On `APPROVE`, the reviewer finalizes the incident report from the confirmed root cause, fix, and verification evidence and trims Investigation to a durable summary.

If the repair expands into feature-level behavior or contract work, stop and request user direction; do not switch workflows automatically.
