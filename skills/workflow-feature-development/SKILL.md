---
name: workflow-feature-development
description: Workflow for feature and change requests, from small changes through complex externally observable behavior.
---

# Feature Development Workflow

Use this workflow for clear, small changes and complex or cross-cutting features. The approved plan records the requirements, scope, constraints, acceptance criteria, risks, and verification needed for the work. Every run produces the standard durable plan, implementation report, and review pass artifacts.

The main agent owns routing and planning. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. **Mandatory grill gate, then plan.** **Run `$grill-with-docs` first.** Do not write the plan, request approval, or implement until it has run. Inspect the code and project documentation, then save one plan at `.agents/plans/plan_YYYYMMDD_<name>.md`. The plan is the sole source of truth and includes behavior, scenarios, non-goals, contracts, constraints, acceptance criteria, implementation approach, risks, and verification. Obtain explicit user approval before implementation.
2. **Implement test-first.** After approval, spawn `implementer` with the approved plan. Apply `$engineering-standards` and `$tdd`; drive each behavior through RED, GREEN, and REFACTOR. The implementer records its TDD and verification evidence in `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md`.
3. **Review independently.** Spawn `code-reviewer` with the approved plan, implementation report, touched files, tests, and verification evidence. The reviewer checks correctness, security, test-first evidence, SOLID, DRY, YAGNI, KISS, and code smells, then records each pass under `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md` and returns `APPROVE`, `WARNING`, or `BLOCK`.
4. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer`, preserve the approved plan, rerun the relevant checks, and repeat review until `APPROVE` or a Shared Stop Condition triggers. Treat `WARNING` as actionable when tied to the plan, a likely bug, security/privacy, or a meaningful test gap.
5. **Close out.** Run the relevant focused and broader verification for the change, with broader checks whenever it touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows. Inspect the final diff and report residual risks and omissions.

In the final response, identify the artifact paths, independent reviewer verdict, and main-agent closeout review. Report the implemented behavior, exact verification results, residual risks, and omissions.
