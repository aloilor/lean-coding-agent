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

## Bug Fixing

When given a bug report, diagnose it before changing code. Show the user the symptom, evidence or likely root cause, proposed fix direction, and verification plan, then wait for explicit approval before every repair. The `workflow-bug-fixing` skill owns tiering and diagnosis routing. Small bugs need only a conversational diagnosis and approval summary; Medium and Full bugs use a durable incident report.

## Self-Improvement Loop

- Keep shared agent lessons in `.agents/lessons/`, one short descriptive file per lesson (e.g. `.agents/lessons/avoid-broad-git-add.md`). Never keep a single `lessons.md`.
- After a user correction, first update the authoritative agent prompt, workflow, guideline, project context, or other policy source when the rule belongs there. Create or update a lesson automatically only for a reusable agent-behavior mistake that has no better canonical owner; never duplicate established policy in lessons.
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
- Apply `engineering-standards` to every task that writes, generates, changes, fixes, refactors, debugs, or reviews code.
- Also use `tdd` for red-green-refactor, test strategy, selection, naming, AAA structure, and regression coverage; `refactor` for behavior-preserving restructuring; and `rest-api-design` for API contracts, endpoints, resource modeling, request/response shapes, validation errors, pagination, versioning, auth, docs, and contract tests.

## Workflows

Each workflow lives in its own `workflow-*` skill. The main agent routes the user's latest request to a workflow via the **Workflow Selection Rules** below, invokes that skill with the Skill tool, and orchestrates its steps. The shared rules in this section — subagent spawning, standard artifacts, tiering, and stop conditions — apply to every workflow and stay here rather than in any single skill.

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

For bug fixes, artifact depth follows the selected tier: Small uses no durable artifact; Medium uses an incident report plus concise implementation and review summaries at the standard paths; Full uses the complete incident, implementation report, gate evidence, and review-pass set. The user-approval gate applies to every tier and may be conversational for Small bugs.

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

### Static-Analysis Complexity Gate

For all development workflows — feature development, bug fixing, and refactoring — static-analysis complexity is a standing ratcheted acceptance criterion when the repo provides a deterministic gate (`scripts/quality-gate`, `composer quality`, PHPStan cognitive complexity, lint/static-analysis scripts, or equivalent).

- New code must stay under the configured complexity thresholds.
- Changed methods/classes/files must not introduce or worsen complexity violations.
- In-scope target methods/classes/files named by the request, specification, bug investigation, refactor brief, or implementation plan must have their reported complexity findings resolved before approval.
- Pre-existing unrelated findings outside the approved scope are reported or left to the ratchet baseline, not fixed opportunistically.
- "Improved but still over threshold" is incomplete for in-scope target code unless the user explicitly approved a partial-reduction objective.

The implementer must keep going until in-scope complexity findings are resolved or a Shared Stop Condition applies. The reviewer must `BLOCK` approval when the current static-analysis artifact still reports in-scope complexity violations.

### Workflow Selection Rules

Match the request to a row, then **invoke that workflow's skill** with the Skill tool and orchestrate it from the main agent. Each workflow's steps live in its skill; the shared rules above apply to all of them. When multiple rows match, use the most specific one that covers the requested outcome, and keep scope limited to what the user asked for.

| User input pattern | Invoke this skill | Rule |
| --- | --- | --- |
| Define, draft, clarify, or update requirements, acceptance criteria, contracts, or a feature specification before implementation. | `workflow-feature-specification` | Use when the deliverable is requirements or a specification, not production code. |
| Build, add, implement, or change product behavior for a feature. | `workflow-feature-development` | Use when code changes are expected and the requested behavior is externally observable. |
| Refactor, restructure, clean up, extract, rename, or simplify code while preserving behavior. | `workflow-refactor` | Use only when the outcome is internal structure change with no behavior change. If behavior changes too, treat it as feature work. |
| Code review, review, audit, or risk assessment without asking for edits. | `workflow-review` | Use when the deliverable is review findings, not code changes. |
| Bug, failing test, CI failure, runtime error, or regression. | `workflow-bug-fixing` | Diagnose and obtain explicit approval before every repair. Small bugs need no durable artifact; Medium and Full bugs require an incident report. |
| Direct question, small documentation edit, or narrow mechanical change. | Normal task execution (Small tier) | Do the smallest useful thing. Don't force workflows unless the change grows into a row above. |

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
