---
name: workflow-feature-development
description: Orchestration workflow for building, adding, implementing, or changing externally observable product behavior with code. Spawns planner, then implementer (test-first TDD), then code-reviewer subagents through the spec then implement then review-fix loop. Invoke from the main agent when a feature's behavior change ships as production code.
---

# Feature Development Workflow

Use when code changes are expected and the requested behavior is externally observable.

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, **Workflow Tiering**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. `planner` creates the specification and implementation plan.
2. `implementer` reads them and implements test-first, applying `engineering-standards` throughout test creation, the smallest passing implementation, and refactoring while driving each behavior through the `tdd` skill's red-green-refactor loop. It then runs broader verification, loops internally until its selected tests and checks pass, and produces the implementation report with its TDD evidence.
3. `code-reviewer` reviews the specification, implementation plan, implementer report, and touched files; after inventorying the diff it runs the deterministic quality gate and uses the fresh artifact and complexity outcome alongside test-first evidence and SOLID, DRY, YAGNI, KISS, and code-smell design checks, then returns `APPROVE`, `WARNING`, or `BLOCK`.
4. On `BLOCK`, return the review to `implementer`, who fixes only the reported findings, keeps the specification unchanged, reruns the relevant verification, and updates the report. Repeat the review-fix loop until `APPROVE` or a Shared Stop Condition triggers.
5. Run broader final verification when the work touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

Treat `WARNING` as a judgment call: fix it when tied to the specification, a likely bug, a security/privacy risk, or a meaningful test gap; otherwise report it as residual risk.
