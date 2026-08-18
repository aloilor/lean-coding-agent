---
name: workflow-bug-fixing
description: Workflow for bugs, failing tests, CI failures, runtime errors, and regressions, from bounded repairs through extended investigations.
---

# Bug Fixing Workflow

Use this workflow for clearly understood local bugs and failures that need investigation before repair. The approved plan records the execution profile:

- **Bounded:** clear, localized, low-risk bugs with a main-agent diagnosis and conversational handoffs.
- **Extended:** ambiguous, recurring, CI-related, production-like, user-facing, cross-module, security/privacy-sensitive, data-affecting, or otherwise consequential failures requiring a durable incident investigation.

The main agent owns routing, planning, approval, and closeout. Follow the shared scaffolding in `AGENTS.md` — **Always Spawn The Named Subagents**, **Standard Artifacts**, and **Shared Stop Conditions** — and never run this workflow from a subagent.

## Steps

1. **Mandatory grill gate, then diagnose and classify.** Enter Plan mode and **run `$grill-with-docs` first**. This step is mandatory; do not diagnose, classify, write the plan, request approval, or repair until it has run. Then inspect the relevant code, callers, tests, project context, and documentation, and classify the failure as bounded or extended. For bounded bugs, the main agent records the symptom, evidence, likely root cause, impact, proposed repair, verification, and non-goals in `.agents/plans/plan_YYYYMMDD_<name>.md`. For extended bugs, spawn `bug-diagnostician` to investigate and draft `docs/incidents/incident_YYYYMMDD_<name>.md`; consolidate its evidence into the approved plan.
2. **Approve before repair.** Show the user the symptom, evidence or likely root cause, proposed repair direction, impact, and verification plan. Obtain explicit approval before changing production or test code.
3. **Reproduce and fix test-first.** After approval, spawn `implementer` with the approved plan and, when applicable, the incident investigation. Apply `$engineering-standards` and `$tdd`; prefer an existing failing test, otherwise add the smallest focused regression test and observe RED. Make the smallest root-cause change that turns the regression test GREEN, then refactor only while green. Extended work produces an implementation report.
4. **Review independently.** Spawn `code-reviewer` with the approved plan, implementer handoff, changed files, tests, and verification evidence. The reviewer checks root-cause correctness, regression coverage, security, scope, and code smells. Extended work also records each review pass under `.agents/code-reviews/`; on `APPROVE`, the reviewer finalizes the incident report from confirmed evidence.
5. **Resolve and verify.** On `BLOCK`, send only the concrete findings back to `implementer`, preserve the approved plan, rerun the focused regression test, and repeat review until `APPROVE` or a Shared Stop Condition triggers. Treat `WARNING` as actionable when tied to the repair plan, a likely bug, security/privacy, or a meaningful test gap. Run relevant broader checks, inspect the final diff, and perform the main-agent closeout review.

If the repair expands into feature-level behavior or contract work, stop and request user direction; do not switch workflows automatically.

In the final response, identify the execution profile, independent reviewer verdict, and main-agent closeout review. Report the confirmed root cause, repair, exact verification results, residual risks, and omissions.
