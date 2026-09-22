---
name: workflow-refactor
description: Workflow for behavior-preserving restructuring, from local cleanup through complex refactors.
---

# Code Refactoring Workflow

Use this workflow for clear, small, localized refactors and complex behavior-preserving restructuring. The approved plan records the behavior and contracts to preserve, scope, risks, documentation impact, and verification needed for the work. Every run produces the standard durable plan, implementation report, and review pass artifacts.

The main agent owns routing and planning. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. **Mandatory grill gate, then plan.** Enter Plan mode and **run `$grill-with-docs` first**. This step is mandatory; do not write the plan, request approval, or implement until it has run. Inspect the complete code area, callers, tests, and project documentation, then save one plan at `.agents/plans/plan_YYYYMMDD_<name>.md`. Record current behavior and contracts to preserve, boundaries, baseline and post-refactor verification, behavior-drift and rollback risks, documentation impact, and resolved constraints. Obtain explicit user approval before implementation. If the work reveals behavior change, stop and request user direction; do not switch workflows automatically.
2. **Establish the baseline and refactor in green steps.** After approval, spawn `implementer` with the approved plan. Apply `$engineering-standards`, `$refactor`, and the test-strategy guidance from `$tdd`. Run focused tests before restructuring; add characterization tests when behavior to preserve is uncovered. Make one small behavior-preserving change at a time and rerun focused tests after each meaningful step. The implementer records its TDD, baseline, documentation, and verification evidence in `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md`.
3. **Review independently.** Spawn `code-reviewer` with the approved plan, implementation report, touched files, tests, and verification evidence. The reviewer checks behavior drift, scope creep, missed tests, unnecessary abstraction, code smells, and documentation staleness. Missing or stale required documentation is a `BLOCK`. Each review pass is recorded under `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md`.
4. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer`, preserve the approved plan, rerun focused checks, and repeat review until `APPROVE` or a Shared Stop Condition triggers. Treat `WARNING` as actionable when tied to the plan, behavior drift, or a meaningful test gap. Run broader final verification whenever shared behavior, API contracts, persistence, auth, security, or user-facing workflows are touched.

In the final response, identify the artifact paths, independent reviewer verdict, and main-agent closeout review. Report the preserved behavior, structural improvement, exact verification results, residual risks, and omissions.
