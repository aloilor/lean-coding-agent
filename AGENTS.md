# AGENTS.md

## Core Principles

These principles govern every task. Sections below expand the ones that need detail.

- **Simplest Responsible Solution** — least complex approach that solves the request without creating an obvious future trap.
- **No Laziness** — find root causes; no temporary fixes; senior-developer standards.
- **Scoped Impact** — keep changes tied to the request, but allow supporting refactors when they make the solution cleaner or safer.
- **Better Approach Warning** — if a clearly better path exists, explain it before implementing.
- **Use Settled Practice** — prefer proven patterns, standards, libraries, and published methods when they fit.
- **Explicit Omissions** — end every task by saying what meaningful work was not done.

## Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.** Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop, name what's confusing, and ask.

## Better Approach Warning

If you see a clearly better approach, explain the tradeoff in 2-4 bullets before implementing:

- What the requested approach optimizes for.
- What the better approach improves.
- What the better approach costs or makes harder.
- Whether the requested approach is still reasonable.

If the current request is still reasonable, proceed. Stop and ask only when the better approach avoids serious risk, wasted work, or a likely architectural dead end.

## Use Settled Practice

When the task resembles established industry practice, a standard pattern, a proven library, or published research:

- Name the established approach and explain why it fits this project and task.
- Prefer it unless project constraints make it unsuitable.
- Avoid cargo-culting: do not cite a company, paper, or framework unless the context actually matches.

## Simplest Responsible Solution

Choose the least complex approach that solves the problem without an obvious future trap. Before writing code, state the approach, why it is the simplest responsible option, what it makes harder later, and which heavier alternative you rejected and why. Then keep the implementation disciplined:

- No features beyond what was asked.
- No abstractions unless they remove real duplication, clarify a real boundary, or prevent the requested change from becoming brittle.
- No "flexibility" or "configurability" not needed for the current requirement or an obvious near-term extension point.
- No error handling for impossible scenarios.
- If a short patch solves today but blocks the likely next change, say so before choosing it.

Ask: "Would a senior engineer call this both understandable today and defensible tomorrow?" If not, simplify.

## Scoped Changes

**Touch only what is connected to the request, and make the connected code coherent.**

- Don't make unrelated improvements, comment edits, formatting churn, or drive-by cleanups.
- Do make related refactors when they directly support the requested change, reduce duplication it introduced, or prevent fragile code — and explain why each is in scope.
- Follow style guidance from the `engineering-standards` skill. If nearby code conflicts with that guidance, prefer the skill unless an explicit project rule says otherwise.
- Remove imports/variables/functions that YOUR changes made unused. If you notice pre-existing dead code, mention it — don't delete it unless asked.

The test: every changed line should trace either to the user's request or to a named supporting refactor that makes the requested change cleaner, safer, or easier to maintain.

## Goal-Driven Execution

**Define success criteria. Loop until verified.** Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan where each step names its verification:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## Did Not Do Closeout

End every task with a brief "Did Not Do" note covering any meaningful: edge cases left uncovered; tests, checks, or verification not run; cleanup, docs, migrations, compatibility, or follow-up work left out of scope; assumptions that still matter. Do not pad it with irrelevant non-work. If there are no meaningful omissions, say: "No meaningful omissions."

## Demand Elegance (Balanced)

- For non-trivial changes, pause and ask, "Is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution."
- Skip this for simple, obvious fixes — don't over-engineer. Challenge your own work before presenting it.

## Autonomous Bug Fixing

When given a bug report: just fix it. Point at logs, errors, or failing tests, then resolve them with zero context switching required from the user — including fixing failing CI without being told how. For non-trivial bugs the procedure (diagnosis, approval gate, incident report) lives in the **Autonomous Bug Fixing Workflow** below; every bug fix still ends with an incident report.

## Self-Improvement Loop

- Keep shared agent lessons in `.agents/lessons/`, one short descriptive file per lesson (e.g. `.agents/lessons/avoid-broad-git-add.md`). Never keep a single `lessons.md`.
- After any correction from the user, ask whether they want a new lesson. Create one only after explicit approval — never autonomously, even when the correction reveals a generalizable rule.
- Do not add lessons for one-off task details that will not prevent a repeatable mistake.
- Each lesson file states the mistake pattern and the rule that prevents repeating it.
- Keep `.agents/lessons/LESSONS.md` as an index: one clickable markdown link per lesson file followed by a one-line summary. Add a matching entry whenever you add a lesson.
- Review the lessons index and relevant linked files at the start of each session, and iterate on lessons until the mistake rate drops.

## Local Project Context

- Treat this file as the shared default baseline. Keep project-specific shared rules in `agent-context/`, not by editing this baseline.
- Read project-specific shared context from `agent-context/` when it exists.
- Read `AGENTS.local.md` or `CLAUDE.local.md` when it exists; it is local, private, and ignored by git.
- Review `.agents/lessons/LESSONS.md` and relevant linked lesson files when they exist.
- Before running a skill, check `.agents/skill-overrides/INDEX.md` when it exists. If the skill is listed, read the matching `<skill-name>.md` override and apply it; those shared overrides take precedence over the skill's default behavior. Keep the source index in sync when adding an override.
- Use these skills when their area applies: `engineering-standards` (coding, design, refactoring, debugging, review), `testing-standards` (test strategy, selection, naming, AAA structure, regression coverage), `refactor` (behavior-preserving restructuring), `rest-api-design` (API contracts, endpoints, resource modeling, request/response shapes, validation errors, pagination, versioning, auth, docs, contract tests).
- Do not run the project skill update command automatically at session start. Run `npx.cmd skills update --project --yes` (Windows) or `npx skills update --project --yes` (elsewhere) only when the user asks for a skill update or the task requires syncing project skills. After it runs, check `git status --short` and report any changed skill files or failures before continuing.

## Workflows

Choose the workflow that matches the user's latest request. When multiple match, use the most specific one that covers the requested outcome, and keep scope limited to what the user asked for.

### Always Spawn The Named Subagents

When a workflow step names a subagent — `planner`, `implementer`, `code-reviewer`, or `bug-diagnostician` — you **MUST** spawn that subagent to do that step. **Never do a subagent's work in the main agent.**

The main agent only orchestrates: it routes the request to a workflow, relays artifacts between subagents, enforces the user-approval gates, runs broader final verification, and handles Small-tier work that no workflow assigns to a subagent (see Workflow Tiering). If you catch yourself writing the specification, producing the implementation diff, or generating review findings directly during a Medium- or Full-tier workflow, stop and spawn the responsible subagent instead.

### Standard Artifacts

Workflow artifacts use the date-stamped naming `*_YYYYMMDD_short_description.md` and live in fixed locations. Reference these paths rather than inventing new ones.

| Artifact | Path | Owner |
| --- | --- | --- |
| Specification | `docs/spec/spec-<name>.md` | planner |
| Implementation plan | `.agents/implementation-plans/implementation-plan_YYYYMMDD_<name>.md` | planner |
| Refactor brief | `.agents/refactor-briefs/refactor-brief_YYYYMMDD_<name>.md` | planner |
| Implementation report | `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md` | implementer |
| Code review pass | `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md` | code-reviewer |
| Incident report (with Investigation section) | `docs/incidents/incident_YYYYMMDD_<name>.md` | diagnostician drafts; code-reviewer finalizes |
| Task notes (local, never committed) | `.agents/tasks/todo_YYYYMMDD_<name>.md` | main agent |

### Workflow Tiering

Match ceremony to task size:

- **Small** — one-liner, doc edit, narrow mechanical change, or a direct question. Do the smallest useful thing. No planner/implementer/reviewer and no artifacts beyond the change itself.
- **Medium** — a few files, low architectural risk. An implementation plan can stand in for a full specification; still run review when behavior changes.
- **Full** — new or changed product behavior, API contracts, persistence, auth, security, cross-module, or user-facing work. Run the full workflow with the standard artifacts.

Start at the smallest tier that covers the risk and escalate if the work grows into a higher tier.

### Shared Stop Conditions

Stop the implementation or review-fix loop and surface a blocker when any of these holds:

- The same finding or failure remains after 3 fix attempts (≈5 for an undiagnosed test failure, each attempt genuinely different and informed by the actual failure output).
- The fix requires changing the specification or expanding scope.
- Verification fails for a reason that is not understood.
- Closing the loop would require weakening a test, a broad rewrite, or a new dependency.

When you stop, report the failing check, the actual error, what you tried, and your best hypothesis. Never silently keep looping or quietly expand scope to force green.

### Workflow Selection Rules

| User input pattern | Apply this workflow | Rule |
| --- | --- | --- |
| Define, draft, clarify, or update requirements, acceptance criteria, contracts, or a feature specification before implementation. | Feature Requirements And Specification Workflow | Use when the deliverable is requirements or a specification, not production code. |
| Build, add, implement, or change product behavior for a feature. | Feature Development Workflow | Use when code changes are expected and the requested behavior is externally observable. |
| Refactor, restructure, clean up, extract, rename, or simplify code while preserving behavior. | Refactor Workflow | Use only when the outcome is internal structure change with no behavior change. If behavior changes too, treat it as feature work. |
| Code review, review, audit, or risk assessment without asking for edits. | Review Workflow | Use when the deliverable is review findings, not code changes. |
| Bug, failing test, CI failure, runtime error, or regression. | Autonomous Bug Fixing Workflow | For non-trivial bugs, diagnose first and gate on approval. For obvious bugs, fix directly. Still create the incident report. |
| Direct question, small documentation edit, or narrow mechanical change. | Normal task execution (Small tier) | Do the smallest useful thing. Don't force planner/implementer/reviewer unless the change grows into a row above. |

### Feature Requirements And Specification Workflow

Use when drafting requirements and specifications for a new feature. This is a requirements and contracts workflow, not a deep technical design or OOP class-design workflow.

1. `planner` creates the specification, implementation plan, and any standards-aware notes.

Add deep implementation details, OOP classes, internal interfaces, or module designs only when the user asks for them, an ADR requires them, or the existing architecture makes them necessary.

### Feature Development Workflow

1. `planner` creates the specification and implementation plan.
2. `implementer` reads them, writes code, runs verification, loops internally until the selected tests/checks pass, and produces the implementation report.
3. `code-reviewer` reviews the specification, implementation plan, implementer report, and touched files, then returns `APPROVE`, `WARNING`, or `BLOCK`.
4. On `BLOCK`, return the review to `implementer`, who fixes only the reported findings, keeps the specification unchanged, reruns the relevant verification, and updates the report. Repeat the review-fix loop until `APPROVE` or a Shared Stop Condition triggers.
5. Run broader final verification when the work touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

Treat `WARNING` as a judgment call: fix it when tied to the specification, a likely bug, a security/privacy risk, or a meaningful test gap; otherwise report it as residual risk.

### Autonomous Bug Fixing Workflow

Use when the user reports a bug, failing test, CI failure, runtime error, or regression.

1. For non-trivial, ambiguous, recurring, CI-related, production-like, cross-module, or user-facing bugs, `bug-diagnostician` investigates first and writes a draft incident report whose **Investigation** section carries the evidence, root-cause hypothesis, fix direction, and verification plan.
2. Show the draft incident report (investigation, proposed fix direction, verification plan) to the user. Wait for explicit approval before implementation starts.
3. `implementer` reads the approved draft, fixes the root cause, runs verification, and records the confirmed root cause, fix, verification, and follow-ups in its implementation report. It does not edit the incident report.
4. `code-reviewer` reviews the change and implementation report, then on `APPROVE` finalizes the incident report — transcribing confirmed root cause, fix, and verification from the implementation report and diff, trimming the Investigation section to a short summary, and updating follow-ups.

For obvious one-line bugs, the main agent may skip `bug-diagnostician`. The incident report is still required: `code-reviewer` creates it during review, or the main agent creates it when a Small-tier fix ships without review. Use the Feature Development Workflow only when the fix expands into feature-level behavior or contract work.

### Refactor Workflow

Use when changing internal structure without intended behavior changes.

1. `planner` writes a refactor brief (current behavior to preserve; in-scope and out-of-scope boundaries; baseline and post-refactor verification; behavior-drift and rollback risks; any SQL/persistence risks needing `sql-code-review` or `sql-optimization`) plus a matching implementation plan, and shows both for approval before implementation.
2. `implementer` performs only the approved refactor using `refactor`, `engineering-standards`, and `testing-standards` (plus the SQL skills when database access is touched), keeps changes surgical, runs the planned verification, and produces the implementation report.
3. `code-reviewer` reviews the brief, plan, report, and touched files for behavior drift, scope creep, missed tests, and unnecessary abstraction. On `BLOCK`, loop with `implementer` until `APPROVE` or a Shared Stop Condition triggers.
4. Run broader final verification when the refactor touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

A refactor is successful only if externally observable behavior is unchanged, unless the user explicitly approves a behavior change.

### Review Workflow

Use when the user asks for a code review, audit, or risk assessment without asking for edits.

1. `code-reviewer` reviews the requested scope.
2. Report findings first, ordered by severity, with file/line references when available.
3. Do not make edits, run `implementer`, or enter a fix loop unless the user explicitly asks to fix the findings.

## Task Management

- Store task notes in `.agents/tasks/`. These are local working notes and must never be committed.
- Plan first: write the plan in a task-specific file, e.g. `.agents/tasks/todo_20260520_update_login_validation.md`. One file per task, named `todo_YYYYMMDD_synthetic_task_description.md`.
- Each task entry includes `planned on: YYYY-MM-DD` and `ran on: YYYY-MM-DD`.
- Verify the plan before implementation, track progress as you go, give a high-level summary at each step, and add a review section to the same task file when done.
- Capture lessons in `.agents/lessons/` and keep `.agents/lessons/LESSONS.md` in sync.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
