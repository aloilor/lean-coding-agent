---
name: workflow-refactor
description: Orchestration workflow for behavior-preserving restructuring.
---

# Refactor Workflow

Orchestrated by the main agent. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. The main agent enters Plan mode and runs `$grill-with-docs` to challenge the restructuring against the project's domain language and documented decisions, then saves one plan at `.agents/plans/plan_YYYYMMDD_<name>.md`. The plan records current behavior and contracts to preserve; in-scope and out-of-scope boundaries; baseline and post-refactor verification; behavior-drift and rollback risks; SQL or persistence risks needing `sql-code-review` or `sql-optimization`; developer-facing documentation to create or update; and every resolved constraint, scenario, non-goal, tradeoff, and decision. The main agent obtains explicit approval before implementation. If the work reveals behavior change, stop and request user direction; do not switch workflows automatically.
2. `implementer` performs only the approved refactor using `refactor`, `engineering-standards`, and `tdd` (plus the SQL skills when database access is touched). Where the behavior to preserve has no test coverage, it first adds characterization tests that pin current behavior, then keeps changes surgical and runs the planned verification. In the same change it creates or updates the developer-facing docs so they match the new structure without inventing or altering behavior claims. It then produces the implementation report, recording the created or updated docs.
3. `code-reviewer` reviews the approved plan, report, and touched files, then checks behavior drift, scope creep, missed tests, unnecessary abstraction, and whether in-scope documentation matches the new structure without introducing new behavior claims. The reviewer may inspect untouched code to establish impact, but only change-caused or explicitly approved in-scope findings become implementation work; ripple findings require scope approval and unrelated pre-existing debt stays out of scope. Missing or stale in-scope documentation is a `BLOCK`. On `BLOCK`, loop with `implementer` until `APPROVE` or a Shared Stop Condition triggers.
4. Run broader final verification when the refactor touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

A refactor is successful only if externally observable behavior is unchanged, the reviewer approves the change, and the in-scope developer-facing documentation has been created or updated to match the new structure, unless the user explicitly approves a behavior change.
