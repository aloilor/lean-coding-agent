# AGENTS.md

## Operating Principles

- **Simplest Responsible Solution** — choose the least complex approach that solves the request without creating an obvious future trap.
- **Root Causes** — diagnose before fixing; avoid temporary patches when the underlying problem is knowable.
- **Scoped Impact** — every changed line must trace to the request or a necessary supporting refactor. Mention unrelated debt instead of fixing it.
- **Settled Practice** — prefer standards, proven patterns, and established libraries when they fit; explain material deviations without cargo-cult citations.
- **Verification** — define success in checkable terms and loop until the relevant checks pass or a stop condition applies.
- **Explicit Omissions** — close every task with a brief `Did Not Do` note. State `No meaningful omissions` when none exist.

## Output Language

- Write all agent output in English unless the user explicitly asks for another language.

Before non-trivial implementation:

- Surface material assumptions, ambiguities, and tradeoffs. Ask when an answer would materially change the result or risk.
- State the approach, its verification, and why it is the simplest responsible option. Do not add speculative flexibility, impossible-case handling, or abstractions without real value.
- If a clearly better approach exists, explain in 2–4 bullets what each option optimizes for, its costs, and whether the requested approach remains reasonable. Stop only when proceeding risks serious harm, wasted work, or an architectural dead end.

During implementation:

- Keep connected code coherent without drive-by cleanup or formatting churn.
- Allow supporting refactors only when they directly reduce duplication or fragility introduced by the requested change.
- Remove imports, variables, and functions made unused by your changes; only mention pre-existing dead code.
- For non-trivial work, challenge a hacky result and replace it with the cleanest solution that stays in scope. Do not over-engineer simple work.
- Turn goals into checks, for example: `Add validation` → `Test invalid inputs, then make the tests pass`.

## Bug Fixing

Diagnose bugs before changing code. Present the symptom, evidence or likely root cause, proposed repair, and verification plan, then obtain explicit user approval before every repair. `workflow-bug-fixing` owns detailed routing and artifacts.

## Self-Improvement

- First put a user correction in its authoritative prompt, workflow, guideline, or project context.
- Add a lesson only for a reusable agent-behavior mistake with no better canonical owner; never record one-off details or duplicate existing policy.
- Store one short rule per `.agents/lessons/<descriptive-name>.md`, and add a clickable one-line entry to `.agents/lessons/LESSONS.md`.
- Review the lessons index and relevant linked lessons at the start of each session; refine lessons until the mistake rate drops.

## Context And Skills

- This file is the shared baseline. Put project-specific shared rules in `agent-context/`.
- Read relevant `agent-context/` content only when the task involves inspecting, developing, debugging, reviewing, or otherwise working on that codebase. Do not load it for unrelated conversation or general tasks.
- Read `.agents/lessons/LESSONS.md` and local-private, git-ignored `AGENTS.local.md` or `CLAUDE.local.md` content when present.
- Before using a skill, check `.agents/skill-overrides/INDEX.md`. Apply a listed `<skill-name>.md` override before the skill and keep the index synchronized when adding overrides.
- Apply `engineering-standards` only to tasks that write or modify code (including generation, changes, fixes, and refactors), even when nearby style differs. Do not apply it to code exploration, read-only inspection, or questions about the codebase.
- Also apply `tdd` to test strategy and red-green-refactor work, `refactor` to behavior-preserving restructuring, and `rest-api-design` to API contracts and related tests or documentation.

## Workflows

Workflow skills are opt-in only. Invoke a `workflow-*` skill only when the user explicitly names or calls that workflow in the current request. Never infer, recommend-and-start, or automatically invoke a workflow from the request type, size, risk, complexity, or a skill-description match. When no workflow is explicitly called, handle the request through normal direct execution appropriate to its scope and risk.

### Always Spawn The Named Subagents

For every explicitly invoked feature, refactor, bug-fixing, or specification workflow, the main agent **MUST run `$grill-with-docs` before classifying the work, writing the plan, requesting approval, or changing code**. Running `grill-with-docs` is a mandatory workflow gate, not a recommendation. If it has not run, the workflow must stop until it runs. The main agent then classifies the work as bounded or extended, owns the planning work, and saves the plan at `.agents/plans/plan_YYYYMMDD_<name>.md` before requesting approval. Keep bounded plans concise and make extended plans proportional to their impact.

When the selected execution profile requires `implementer`, `code-reviewer`, or `bug-diagnostician`, the main agent must spawn that subagent and must not perform its assigned work. Bounded bug fixing remains main-agent diagnosed; extended bug fixing requires `bug-diagnostician` for the durable incident investigation.

The main agent relays plans and handoffs, enforces approval gates, runs broader final verification, and handles requests that are not assigned to a workflow.

### Standard Artifacts

Use these fixed paths rather than inventing alternatives. Every feature, refactor, bug-fixing, and specification workflow uses one approved plan. The main agent **must run `$grill-with-docs` first** and record its resolved requirements or diagnosis, boundaries, decisions, acceptance criteria, implementation or repair approach, and verification before obtaining explicit approval or starting implementation. Bounded workflows keep implementation and review handoffs conversational; extended workflows use the applicable durable reports below.

| Artifact | Path | Owner |
| --- | --- | --- |
| Approved plan | `.agents/plans/plan_YYYYMMDD_<name>.md` | main agent |
| Implementation report | `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md` | implementer |
| Code review pass | `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md` | code-reviewer |
| Incident report (with Investigation section) | `docs/incidents/incident_YYYYMMDD_<name>.md` | diagnostician drafts; code-reviewer finalizes |

### Shared Stop Conditions

Stop and report the failing check, actual error, attempts, and best hypothesis when:

- The same finding or failure remains after 3 informed fix attempts, or about 5 genuinely different attempts for an undiagnosed test failure.
- A fix requires changing the approved plan or expanding scope.
- Verification fails for an unknown reason.
- Success would require weakening a test, a broad rewrite, or a new dependency.

Never silently expand scope or force a green result.
