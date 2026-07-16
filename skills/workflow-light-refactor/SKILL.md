---
name: workflow-light-refactor
description: Main-agent workflow for a clear, small, localized, low-risk refactor. Preserve externally observable behavior; use for narrow restructuring, extraction, renaming, cleanup, or simplification with focused verification and no material architecture, public-contract, persistence, auth, security, privacy, or cross-module impact.
---

# Light Refactor Workflow

Run this workflow only from the main agent. Do not spawn workflow subagents, create refactor briefs, implementation plans, implementation reports, or review-pass artifacts, or escalate to another workflow after this workflow starts. If the work crosses the light-refactor boundary, requires a behavior change, or reveals a defect that needs repair, stop and request user direction without switching workflows automatically.

## Workflow

1. **Plan with `$grill-with-docs`.** Inspect the complete code area, callers, tests, and project documentation before asking questions. Define the behavior to preserve, in-scope structure, non-goals, documentation impact, rollback risks, and focused verification. Summarize the agreed plan concisely without creating a coordination artifact.
2. **Establish the baseline.** Apply `$engineering-standards`, `$refactor`, and the test-strategy guidance from `$tdd`. Run the focused tests before restructuring. If meaningful behavior is uncovered, add characterization tests that pass against the current implementation. Stop if the baseline fails unexpectedly; do not treat a failing baseline as refactor evidence.
3. **Refactor in green steps.** Make one small behavior-preserving structural change at a time and rerun the focused tests after each meaningful step. Keep the diff limited to the agreed plan, avoid speculative abstractions, and update developer-facing documentation only where the new structure makes it stale.
4. **Verify.** Run the relevant broader tests. Inspect the final diff for behavior drift, accidental changes, stale in-scope documentation, and unrelated cleanup.
5. **Self-review.** Review the accepted plan, changed files, tests, and verification evidence for preserved behavior, scope control, security, SOLID, DRY, YAGNI, KISS, and code smells. Fix every in-scope finding through another green refactor step, rerun affected checks, and repeat until clean or a shared stop condition applies.

In the final response, identify the review as a main-agent self-review and report the preserved behavior, structural improvement, exact verification results, residual risks, and omissions.
