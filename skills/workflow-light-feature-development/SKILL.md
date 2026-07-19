---
name: workflow-light-feature-development
description: Light workflow for a clear, small, low-risk feature or change request.
---

# Light Feature Development Workflow

The main agent owns planning: enter plan mode, run `$grill-with-docs`, and do not spawn `planner`. After explicit approval, spawn `implementer` and `code-reviewer`; both use the Luna model with high reasoning effort. Keep the light workflow free of durable coordination artifacts. If the work crosses the light-feature boundary, stop and request user direction; do not escalate or switch workflows automatically.

## Workflow

1. **Plan with plan mode and `$grill-with-docs`.** Inspect the code and project documentation before asking questions. Resolve material uncertainties and agree on behavior, scenarios, non-goals, implementation approach, and verification. Summarize the accepted plan for the handoff without creating a coordination artifact, then obtain explicit user approval.
2. **Implement test-first.** After approval, spawn `implementer` with the accepted plan. Apply `$engineering-standards` and `$tdd`; drive each behavior through RED, GREEN, and REFACTOR, and keep the diff limited to the approved plan and documentation state established during planning.
3. **Review independently.** Spawn `code-reviewer` with the accepted plan, implementer handoff, changed files, tests, and verification evidence. The reviewer checks correctness, security, SOLID, DRY, YAGNI, KISS, and code smells, then returns `APPROVE`, `WARNING`, or `BLOCK` without editing code.
4. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer` and repeat the focused checks and review. Treat `WARNING` as actionable when tied to the plan, a likely bug, security/privacy, or a meaningful test gap. After approval, run the relevant broader tests and inspect the final diff. The main agent performs the final closeout review.

In the final response, identify the independent reviewer verdict and the main-agent closeout review. Report the implemented behavior, exact verification results, residual risks, and omissions.
