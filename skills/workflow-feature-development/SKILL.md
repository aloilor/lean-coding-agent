---
name: workflow-feature-development
description: Workflow for feature and change requests, from bounded low-risk work through complex externally observable behavior.
---

# Feature Development Workflow

Use this workflow for clear, small changes and complex or cross-cutting features. The approved plan records the execution profile:

- **Bounded:** clear, small, localized, low-risk work with conversational implementation and review handoffs.
- **Extended:** complex behavior, public contracts, persistence, auth or security, cross-module impact, user-facing workflows, or other work that needs durable handoffs and broader verification.

The main agent owns routing and planning. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. **Plan and classify.** Enter Plan mode, run `$grill-with-docs`, inspect the code and project documentation, classify the request as bounded or extended, and save one plan at `.agents/plans/plan_YYYYMMDD_<name>.md`. The plan is the sole source of truth. For bounded work, keep it concise; for extended work, include behavior, scenarios, non-goals, contracts, constraints, acceptance criteria, implementation approach, risks, and verification. Obtain explicit user approval before implementation.
2. **Implement test-first.** After approval, spawn `implementer` with the approved plan. Apply `$engineering-standards` and `$tdd`; drive each behavior through RED, GREEN, and REFACTOR. Bounded work uses a conversational handoff. Extended work also produces `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md` with its TDD and verification evidence.
3. **Review independently.** Spawn `code-reviewer` with the approved plan, implementer handoff, touched files, tests, and verification evidence. The reviewer checks correctness, security, test-first evidence, SOLID, DRY, YAGNI, KISS, and code smells, then returns `APPROVE`, `WARNING`, or `BLOCK`. Extended work also records each review pass under `.agents/code-reviews/`.
4. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer`, preserve the approved plan, rerun the relevant checks, and repeat review until `APPROVE` or a Shared Stop Condition triggers. Treat `WARNING` as actionable when tied to the plan, a likely bug, security/privacy, or a meaningful test gap.
5. **Close out.** Run broader final verification for extended work and whenever the change touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows. Inspect the final diff and report residual risks and omissions.

In the final response, identify the execution profile, independent reviewer verdict, and main-agent closeout review. Report the implemented behavior, exact verification results, residual risks, and omissions.
