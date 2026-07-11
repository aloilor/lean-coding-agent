---
name: workflow-bug-fixing
description: Orchestration workflow for a reported bug, failing test, CI failure, runtime error, or regression. Owns bug tiering, diagnosis routing, the mandatory approval gate, implementation, review, and tier-appropriate artifacts.
---

# Bug Fixing Workflow

Use when the user reports a bug, failing test, CI failure, runtime error, or regression.

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, **Workflow Tiering**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. Classify the bug using `AGENTS.md` tiering. The main agent diagnoses Small bugs in conversation. For Medium or Full bugs—and whenever the failure is ambiguous, recurring, CI-related, production-like, cross-module, security/privacy-sensitive, data-affecting, or user-facing—`bug-diagnostician` investigates and drafts the incident report.
2. Show the user the symptom, evidence or likely root cause, proposed fix direction, and verification plan. Wait for explicit approval before any implementation, regardless of tier.
3. After approval, the main agent handles Small repairs; Medium and Full repairs go to `implementer`. Apply `tdd` plus `engineering-standards`: reproduce the bug with an existing failing test or a focused regression test and observe RED; make the smallest root-cause fix; then refactor only while green. If automated reproduction is impractical, document why and record the strongest substitute evidence. Run broader verification.
4. Medium and Full changes go to `code-reviewer`, which runs the repository's deterministic quality gate after inventorying the diff and uses the fresh findings during review. The reviewer may inspect untouched code to establish impact, but only change-caused or explicitly approved in-scope findings become implementation work; ripple findings require scope approval and unrelated pre-existing debt stays out of scope. On `APPROVE`, the reviewer finalizes the incident report from the confirmed root cause, fix, and verification evidence and trims Investigation to a durable summary.

## Artifacts By Tier

- **Small:** conversational diagnosis, proposed repair, verification plan, and user approval; no durable incident, implementation report, or review pass.
- **Medium:** durable incident plus concise implementation and review summaries at the standard paths.
- **Full:** durable incident, implementation report, deterministic-gate evidence, and review passes at all standard paths.

Use `workflow-feature-development` only when the repair expands into feature-level behavior or contract work.
