---
name: workflow-refactor
description: Workflow for behavior-preserving restructuring, from bounded local cleanup through complex refactors.
---

# Refactor Workflow

Use this workflow for clear, small, localized refactors and complex behavior-preserving restructuring. The approved plan records the execution profile:

- **Bounded:** localized, low-risk restructuring with conversational implementation and review handoffs.
- **Extended:** shared or cross-module structure, persistence, auth or security boundaries, public contracts, or other work that needs durable handoffs, documentation review, and broader verification.

The main agent owns routing and planning. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. **Plan and classify.** Enter Plan mode, run `$grill-with-docs`, inspect the complete code area, callers, tests, and project documentation, classify the request as bounded or extended, and save one plan at `.agents/plans/plan_YYYYMMDD_<name>.md`. Record current behavior and contracts to preserve, boundaries, baseline and post-refactor verification, behavior-drift and rollback risks, documentation impact, and resolved constraints. Obtain explicit user approval before implementation. If the work reveals behavior change, stop and request user direction; do not switch workflows automatically.
2. **Establish the baseline and refactor in green steps.** After approval, spawn `implementer` with the approved plan. Apply `$engineering-standards`, `$refactor`, and the test-strategy guidance from `$tdd`. Run focused tests before restructuring; add characterization tests when behavior to preserve is uncovered. Make one small behavior-preserving change at a time and rerun focused tests after each meaningful step. Extended work produces an implementation report and updates in-scope developer documentation so it matches the new structure.
3. **Review independently.** Spawn `code-reviewer` with the approved plan, implementer handoff, touched files, tests, and verification evidence. The reviewer checks behavior drift, scope creep, missed tests, unnecessary abstraction, code smells, and documentation staleness. Missing or stale required documentation is a `BLOCK`. Extended work also records each review pass under `.agents/code-reviews/`.
4. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer`, preserve the approved plan, rerun focused checks, and repeat review until `APPROVE` or a Shared Stop Condition triggers. Treat `WARNING` as actionable when tied to the plan, behavior drift, or a meaningful test gap. Run broader final verification for extended work and whenever shared behavior, API contracts, persistence, auth, security, or user-facing workflows are touched.

In the final response, identify the execution profile, independent reviewer verdict, and main-agent closeout review. Report the preserved behavior, structural improvement, exact verification results, residual risks, and omissions.
