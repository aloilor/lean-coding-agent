---
name: workflow-light-refactor
description: Light workflow for a clear, small, localized, low-risk behavior-preserving refactor.
---

# Light Refactor Workflow

The main agent owns planning: enter plan mode, run `$grill-with-docs`, and do not spawn `planner`. After explicit approval, spawn `implementer` and `code-reviewer`; both use the Luna model with high reasoning effort. Keep the light workflow free of durable coordination artifacts, and do not escalate to another workflow after it starts. If the work crosses the light-refactor boundary, requires a behavior change, or reveals a defect that needs repair, stop and request user direction without switching workflows automatically.

## Workflow

1. **Plan with plan mode and `$grill-with-docs`.** Inspect the complete code area, callers, tests, and project documentation before asking questions. Define the behavior to preserve, in-scope structure, non-goals, documentation impact, rollback risks, and focused verification. Summarize the accepted plan for the handoff without creating a coordination artifact, then obtain explicit user approval.
2. **Establish the baseline.** After approval, spawn `implementer` with the accepted plan. Apply `$engineering-standards`, `$refactor`, and the test-strategy guidance from `$tdd`. Run the focused tests before restructuring. If meaningful behavior is uncovered, add characterization tests that pass against the current implementation. Stop if the baseline fails unexpectedly; do not treat a failing baseline as refactor evidence.
3. **Refactor in green steps.** Make one small behavior-preserving structural change at a time and rerun the focused tests after each meaningful step. Keep the diff limited to the approved plan, avoid speculative abstractions, and update developer-facing documentation only where the new structure makes it stale.
4. **Review independently.** Spawn `code-reviewer` with the accepted plan, implementer handoff, changed files, tests, and verification evidence. The reviewer checks behavior drift, scope creep, missed tests, documentation staleness, unnecessary abstraction, and code smells, then returns `APPROVE`, `WARNING`, or `BLOCK` without editing code.
5. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer` and repeat the focused checks and review. Treat `WARNING` as actionable when tied to the plan, behavior drift, or a meaningful test gap. After approval, run the relevant broader tests, inspect the final diff, and perform the main-agent closeout review.

In the final response, identify the independent reviewer verdict and the main-agent closeout review. Report the preserved behavior, structural improvement, exact verification results, residual risks, and omissions.
