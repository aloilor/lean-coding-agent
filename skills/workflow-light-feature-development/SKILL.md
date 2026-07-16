---
name: workflow-light-feature-development
description: Main-agent workflow for a clear, small, low-risk feature or change request. Use grill-with-docs to agree the approach, then have the main agent implement with TDD, verify, and self-review without subagents or coordination artifacts.
---

# Light Feature Development Workflow

Run this workflow only from the main agent. Do not spawn workflow subagents or create specifications, implementation reports, or review-pass artifacts. If the work crosses the light-feature boundary, stop and request user direction; do not escalate or switch workflows automatically.

## Workflow

1. **Plan with `$grill-with-docs`.** Inspect the code and project documentation before asking questions. Resolve material uncertainties and agree on behavior, scenarios, non-goals, implementation approach, and verification. Summarize the agreed plan concisely without creating a coordination artifact.
2. **Implement test-first.** Apply the coding skills `$engineering-standards` and `$tdd`. Drive each behavior through RED, GREEN, and REFACTOR, and keep the diff limited to the agreed plan and documentation state established during planning.
3. **Verify.** Run the focused tests after each behavior, then the relevant broader tests. Inspect the final diff for accidental or unrelated changes.
4. **Self-review.** Review the accepted plan, changed files, tests, and verification evidence for correctness, security, SOLID, DRY, YAGNI, KISS, and code smells. Fix every in-scope finding through the same TDD loop, rerun affected checks, and repeat until clean or a shared stop condition applies.

In the final response, identify the review as a main-agent self-review and report the implemented behavior, exact verification results, residual risks, and omissions.
