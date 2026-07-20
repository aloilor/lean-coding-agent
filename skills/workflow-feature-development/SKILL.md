---
name: workflow-feature-development
description: Delegated orchestration workflow for complex features that add or change externally observable product behavior.
---

# Feature Development Workflow

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. The main agent enters Plan mode, runs `$grill-with-docs`, saves one plan at `.agents/plans/plan_YYYYMMDD_<name>.md`, and obtains explicit user approval. The plan is the sole planning source of truth and includes behavior, scenarios, non-goals, contracts, constraints, acceptance criteria, implementation approach, risks, and verification.
2. `implementer` reads the approved plan and implements test-first, applying `engineering-standards` throughout test creation, the smallest passing implementation, and refactoring while driving each behavior through the `tdd` skill's red-green-refactor loop. It then runs broader verification, loops internally until its selected tests and checks pass, and produces the implementation report with its TDD evidence.
3. `code-reviewer` reviews the approved plan, implementation report, and touched files; checks test-first evidence plus SOLID, DRY, YAGNI, KISS, security, correctness, and code-smell risks; then returns `APPROVE`, `WARNING`, or `BLOCK`. The reviewer may inspect untouched code to establish impact, but only change-caused or explicitly approved in-scope findings become implementation work; ripple findings require scope approval and unrelated pre-existing debt stays out of scope.
4. On `BLOCK`, return the review to `implementer`, who fixes only the reported findings, keeps the approved plan unchanged, reruns the relevant verification, and updates the report. Repeat the review-fix loop until `APPROVE` or a Shared Stop Condition triggers.
5. Run broader final verification when the work touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

Treat `WARNING` as a judgment call: fix it when tied to the approved plan, a likely bug, a security/privacy risk, or a meaningful test gap; otherwise report it as residual risk.
