---
name: workflow-light-bug-fixing
description: Light workflow for a clearly understood, localized, low-risk bug.
---

# Light Bug Fixing Workflow

The main agent owns diagnosis and planning: enter Plan mode, run `$grill-with-docs`, save one concise plan at `.agents/plans/plan_YYYYMMDD_<name>.md`, and do not spawn `bug-diagnostician`. After explicit approval, spawn `implementer` and `code-reviewer`; both use the Luna model with high reasoning effort. Keep implementation and review handoffs conversational. If the bug is not clearly understood, localized, and low risk, stop and request user direction without escalating or switching workflows automatically.

## Workflow

1. **Plan and diagnose with Plan mode and `$grill-with-docs`.** Inspect the relevant code, callers, tests, project context, and documentation. Define the symptom, evidence, likely root cause, impact, proposed repair, verification, and non-goals. Confirm the bug is narrow, reproducible, localized, low risk, and free of ambiguous, recurring, CI-related, production-like, user-facing, cross-module, security/privacy-sensitive, or data-affecting impact. Save the concise diagnosis and repair contract at `.agents/plans/plan_YYYYMMDD_<name>.md`, show it to the user, and obtain explicit approval before changing production or test code.
2. **Reproduce and fix test-first.** After approval, spawn `implementer` with the approved plan path. Apply `$engineering-standards` and `$tdd`. Prefer an existing failing test; otherwise add the smallest focused regression test and observe RED. If automated reproduction is impractical, record why and capture the strongest substitute evidence. Make the smallest root-cause change that turns the regression test GREEN, and refactor only while green.
3. **Review independently.** Spawn `code-reviewer` with the approved plan path, implementer handoff, changed files, tests, and verification evidence. The reviewer checks root-cause correctness, regression coverage, security, scope, and code smells, then returns `APPROVE`, `WARNING`, or `BLOCK` without editing code.
4. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer` and repeat the focused regression test and review. Treat `WARNING` as actionable when tied to the repair plan, a likely bug, security/privacy, or a meaningful test gap. After approval, run the relevant broader checks, inspect the final diff, and perform the main-agent closeout review.

In the final response, identify the work as a light bug fix, include the independent reviewer verdict and main-agent closeout review, and report the confirmed root cause, repair, exact verification results, residual risks, and omissions.
