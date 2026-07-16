---
name: workflow-light-bug-fixing
description: Main-agent workflow for a clearly understood Small-tier bug, failing test, runtime error, or regression with one localized root cause and focused verification. Use when the repair has no material architecture, public-contract, persistence, auth, security, privacy, data, production-like, user-facing, or cross-module impact.
---

# Light Bug Fixing Workflow

Run this workflow only from the main agent. Do not spawn workflow subagents or create incident reports, implementation reports, implementation plans, or review-pass artifacts. If the bug crosses the Small-tier boundary, stop and request user direction without escalating or switching workflows automatically.

## Workflow

1. **Diagnose before repair.** Inspect the relevant code, callers, tests, project context, and documentation. Define the symptom, evidence, likely root cause, impact, proposed repair, verification, and non-goals. Confirm the bug is narrow, reproducible, localized, low risk, and free of ambiguous, recurring, CI-related, production-like, user-facing, cross-module, security/privacy-sensitive, or data-affecting impact. Present the diagnosis and wait for explicit approval before changing production or test code.

2. **Reproduce and fix test-first.** Apply `$engineering-standards` and `$tdd`. Prefer an existing failing test; otherwise add the smallest focused regression test and observe RED. If automated reproduction is impractical, record why and capture the strongest substitute evidence. Make the smallest root-cause change that turns the regression test GREEN, and refactor only while green.

3. **Verify.** Run the focused regression test after the fix, then the relevant broader checks. Inspect the final diff for accidental, unrelated, or undocumented changes, and remove anything made unused by the repair.

4. **Self-review.** Review the approved diagnosis, changed files, tests, callers, and verification evidence for root-cause correctness, scope control, security, SOLID, DRY, YAGNI, KISS, and code smells. Fix every in-scope finding through the same red-green loop, rerun affected checks, and repeat until clean or a shared stop condition applies.

In the final response, identify the work as a Small-tier light bug fix and the review as a main-agent self-review. Report the confirmed root cause, repair, exact verification results, residual risks, and omissions.
