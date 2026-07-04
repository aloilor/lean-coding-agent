---
name: workflow-refactor
description: Orchestration workflow for behavior-preserving restructuring — refactor, restructure, clean up, extract, rename, or simplify code with no intended behavior change. Spawns planner (refactor brief), then implementer, then code-reviewer subagents. Invoke from the main agent; if behavior changes too, use workflow-feature-development instead.
---

# Refactor Workflow

Use when changing internal structure without intended behavior changes.

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, **Workflow Tiering**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. `planner` writes a refactor brief (current behavior to preserve; in-scope and out-of-scope boundaries; baseline and post-refactor verification; behavior-drift and rollback risks; any SQL/persistence risks needing `sql-code-review` or `sql-optimization`) plus a matching implementation plan, and shows both for approval before implementation.
2. `implementer` performs only the approved refactor using `refactor`, `engineering-standards`, and `tdd` (plus the SQL skills when database access is touched). Where the behavior to preserve has no test coverage, it first adds characterization tests that pin current behavior, then keeps changes surgical, runs the planned verification, and produces the implementation report.
3. `code-reviewer` reviews the brief, plan, report, and touched files for behavior drift, scope creep, missed tests, and unnecessary abstraction. On `BLOCK`, loop with `implementer` until `APPROVE` or a Shared Stop Condition triggers.
4. Run broader final verification when the refactor touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

A refactor is successful only if externally observable behavior is unchanged, unless the user explicitly approves a behavior change.
