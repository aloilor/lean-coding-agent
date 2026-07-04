---
name: workflow-bug-fixing
description: Orchestration workflow for a reported bug, failing test, CI failure, runtime error, or regression. For non-trivial bugs spawns bug-diagnostician (diagnose plus approval gate), then implementer, then code-reviewer. Medium-tier and larger fixes end with an incident report; genuinely trivial one-liners skip it. Invoke from the main agent for defect fixes.
---

# Autonomous Bug Fixing Workflow

Use when the user reports a bug, failing test, CI failure, runtime error, or regression.

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, **Workflow Tiering**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. For non-trivial, ambiguous, recurring, CI-related, production-like, cross-module, or user-facing bugs, `bug-diagnostician` investigates first and writes a draft incident report whose **Investigation** section carries the evidence, root-cause hypothesis, fix direction, and verification plan.
2. Show the draft incident report (investigation, proposed fix direction, verification plan) to the user. Wait for explicit approval before implementation starts.
3. `implementer` reads the approved draft, fixes the root cause, runs verification and any repo-provided deterministic quality gate, applies the Static-Analysis Complexity Gate from `AGENTS.md`, and records the confirmed root cause, fix, verification, gate result, and follow-ups in its implementation report. It does not edit the incident report.
4. `code-reviewer` reviews the change, implementation report, deterministic gate artifact, and complexity gate outcome, then on `APPROVE` finalizes the incident report — transcribing confirmed root cause, fix, and verification from the implementation report and diff, trimming the Investigation section to a short summary, and updating follow-ups.

For obvious one-line bugs, the main agent may skip `bug-diagnostician`. Incident reports are required for Medium-tier and larger fixes — `code-reviewer` finalizes the report during review — but genuinely trivial one-line (Small-tier) fixes skip the incident report entirely. Use the `workflow-feature-development` skill only when the fix expands into feature-level behavior or contract work.
