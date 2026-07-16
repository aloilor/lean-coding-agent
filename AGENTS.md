# AGENTS.md

## Operating Principles

- **Simplest Responsible Solution** — choose the least complex approach that solves the request without creating an obvious future trap.
- **Root Causes** — diagnose before fixing; avoid temporary patches when the underlying problem is knowable.
- **Scoped Impact** — every changed line must trace to the request or a necessary supporting refactor. Mention unrelated debt instead of fixing it.
- **Settled Practice** — prefer standards, proven patterns, and established libraries when they fit; explain material deviations without cargo-cult citations.
- **Verification** — define success in checkable terms and loop until the relevant checks pass or a stop condition applies.
- **Explicit Omissions** — close every task with a brief `Did Not Do` note. State `No meaningful omissions` when none exist.

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
- Apply `engineering-standards` to every code-writing, generation, change, fix, refactor, debug, or review task, even when nearby style differs.
- Also apply `tdd` to test strategy and red-green-refactor work, `refactor` to behavior-preserving restructuring, and `rest-api-design` to API contracts and related tests or documentation.

## Workflows

Light workflows are executed entirely by the main agent; delegated workflows use their named subagents and artifacts.

### Always Spawn The Named Subagents

`workflow-light-feature-development` and `workflow-light-refactor` are main-agent-only: do not spawn workflow subagents for them. The main agent plans with `grill-with-docs`, implements, verifies, and self-reviews as directed by the applicable skill. `workflow-light-bug-fixing` is also main-agent-only and uses direct diagnosis, approval, TDD, verification, and self-review without `grill-with-docs`.

For every other workflow, when it names `planner`, `implementer`, `code-reviewer`, or `bug-diagnostician`, the main agent must spawn that subagent and must not perform its assigned work.

The main agent relays artifacts, enforces approval gates, runs broader final verification, and handles requests that are not assigned to a workflow.

### Subagent Runtime Verification

After spawning a subagent, compare its observed runtime model and reasoning effort with `model` and `model_reasoning_effort` in `.codex/agents/<subagent>.toml`.

Require every subagent response to begin with:

- `Runtime model: <model>`
- `Reasoning effort: <effort>`

Report the expected and observed values in the first progress update. Treat missing values as `unknown` and a failed match. On any mismatch, interrupt the subagent, discard its output, stop the workflow, and report the discrepancy. Do not retry or override the configuration.



### Standard Artifacts

Use these fixed paths rather than inventing alternatives. Light workflows create no coordination artifacts; delegated workflows use the applicable artifacts below.

| Artifact | Path | Owner |
| --- | --- | --- |
| Specification | `docs/spec/spec-<name>.md` | planner |
| Implementation plan | `.agents/implementation-plans/implementation-plan_YYYYMMDD_<name>.md` | planner |
| Refactor brief | `.agents/refactor-briefs/refactor-brief_YYYYMMDD_<name>.md` | planner |
| Implementation report | `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md` | implementer |
| Code review pass | `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md` | code-reviewer |
| Incident report (with Investigation section) | `docs/incidents/incident_YYYYMMDD_<name>.md` | diagnostician drafts; code-reviewer finalizes |

### Workflow Tiering

- **Small** — direct question, one-liner, documentation edit, or narrow mechanical change. Small non-bug work uses no workflow skill, subagents, or coordination artifacts.
- **Light feature** — a clear, small, localized, low-risk feature or change request with focused verification and no material architecture, public-contract, persistence, auth, security, privacy, or cross-module impact. The main agent performs the complete workflow without coordination artifacts.
- **Light refactor** — a clear, small, localized, low-risk behavior-preserving restructure with focused verification and no material architecture, public-contract, persistence, auth, security, privacy, or cross-module impact. The main agent performs the complete workflow without coordination artifacts.
- **Light bug** — a clearly understood Small-tier bug, failing test, runtime error, or regression with one localized root cause, focused reproduction, and no material architecture, public-contract, persistence, auth, security, privacy, data, production-like, user-facing, or cross-module impact. The main agent diagnoses, obtains explicit approval, repairs, verifies, and self-reviews without coordination artifacts.
- **Medium** — multiple connected changes where independent planning or review materially improves confidence, but architectural risk remains limited. A plan may replace a full specification.
- **Full** — complex product behavior, material API contracts, persistence, auth, security, privacy, cross-module architecture, or broad user-facing workflows. Use the complete workflow.

These tiers describe boundaries; they do not route requests automatically. If a light workflow crosses its boundary, stop and request direction without escalating or switching workflows. File count is only a signal; risk, ambiguity, and blast radius decide whether a feature, refactor, or bug fix qualifies as light. Bug fixes always require approval: Small is conversational; Medium adds an incident plus concise implementation and review artifacts; Full uses the complete artifact set and gate evidence.

### Shared Stop Conditions

Stop and report the failing check, actual error, attempts, and best hypothesis when:

- The same finding or failure remains after 3 informed fix attempts, or about 5 genuinely different attempts for an undiagnosed test failure.
- A fix requires changing the approved specification or expanding scope.
- Verification fails for an unknown reason.
- Success would require weakening a test, a broad rewrite, or a new dependency.

Never silently expand scope or force a green result.

### Subagent Routing

Use this table for subagents routed directly by the main agent. Subagents named by a workflow are routed only through that workflow.

| User request | Subagent | Boundary |
| --- | --- | --- |
| Create a commit, or otherwise commit the current changes | `committer` | Always route requests to commit through this subagent. Spawn with `fork_turns="none"`. |
