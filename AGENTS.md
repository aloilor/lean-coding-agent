# AGENTS.md

## Core Principles

- Simplest Responsible Solution: Prefer the least complex approach that solves the request without creating an obvious future trap.
- No Laziness: Find root causes. No temporary fixes. Senior developer standards.
- Scoped Impact: Keep changes tied to the request, but allow supporting refactors when they make the solution cleaner or safer.
- Better Approach Warning: If a clearly better path exists, explain it before implementing.
- Use Settled Practice: Prefer proven patterns, standards, libraries, and published methods when they fit the task.
- Explicit Omissions: End every task by saying what meaningful work was not done.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Better Approach Warning

**If you see a clearly better approach, say so before implementing.**

Explain the tradeoff in 2-4 bullets:
- What the requested approach optimizes for.
- What the better approach improves.
- What the better approach costs or makes harder.
- Whether the requested approach is still reasonable.

If the current request is still reasonable, proceed. Stop and ask only when the better approach avoids serious risk, wasted work, or a likely architectural dead end.

## 3. Use Settled Practice

**Do not reinvent settled solutions without a reason.**

When the task resembles established industry practice, a standard pattern, a proven library, or published research:
- Name the established approach.
- Explain why it fits this project and task.
- Prefer the established approach unless project constraints make it unsuitable.
- Avoid cargo-culting: do not cite a company, paper, or framework unless the context actually matches.

## 4. Simplest Responsible Solution

**Choose the least complex approach that solves the problem without creating an obvious future trap.**

Before writing code, state:
- The approach you are taking.
- Why it is the simplest responsible option.
- What this approach makes harder later.
- Which heavier alternative you rejected and why.

Then keep the implementation disciplined:
- No features beyond what was asked.
- No abstractions unless they remove real duplication, clarify a real boundary, or prevent the requested change from becoming brittle.
- No "flexibility" or "configurability" that is not needed for the current requirement or an obvious near-term extension point.
- No error handling for impossible scenarios.
- If a short patch solves today but blocks the likely next change, say so before choosing it.

Ask yourself: "Would a senior engineer call this both understandable today and defensible tomorrow?" If not, simplify or choose the cleaner small design.

## 5. Scoped Changes

**Touch only what is connected to the request, and make the connected code coherent.**

When editing existing code:
- Don't make unrelated improvements, comment edits, formatting churn, or drive-by cleanups.
- Do make related refactors when they directly support the requested change, reduce duplication introduced by the change, or prevent awkward/fragile code.
- Explain why each supporting refactor is in scope.
- Follow style guidance from the `engineering-standards` skill when available. If nearby code conflicts with that guidance, prefer the skill unless an explicit project rule says otherwise.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace either to the user's request or to a named supporting refactor that makes the requested change cleaner, safer, or easier to maintain.

## 6. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 7. Did Not Do Closeout

**End every task by stating what you did not do.**

In the final response, include a brief "Did Not Do" note that mentions any meaningful:
- Edge cases left uncovered.
- Tests, checks, or broader verification not run.
- Cleanup, docs, migrations, compatibility work, or follow-up work left out of scope.
- Assumptions that still matter after the change.

Do not pad this section with irrelevant non-work. If there are no meaningful omissions, say: "No meaningful omissions."

## 8. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask, "Is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution."
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

## 9. Autonomous Bug Fixing

- When given a bug report: just fix it. Don’t ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching is required from the user
- Go fix failing CI tests without being told how
- For non-trivial, ambiguous, recurring, CI-related, production-like, cross-module, or user-facing bugs, run `bug-diagnostician` before `implementer`. The diagnostician writes `.agents/bug-diagnoses/bug-diagnosis_YYYYMMDD_short_description.md` and drafts `docs/incidents/incident_YYYYMMDD_short_description.md`. Show both to the user and wait for explicit approval before implementation starts.
- For every bug fix, create a concise incident report. The diagnostician owns the first draft when diagnosis runs; the implementer owns the final incident report after the fix and verification. Include symptom, impact, root cause, fix, verification, and follow-ups.

## 10. Self-Improvement Loop

- Keep shared agent lessons in `.agents/lessons/`
- After any correction from the user, ask whether they want a new lesson before creating or updating lesson files.
- Create a lesson only after the user explicitly approves adding it.
- Do not handle lesson capture autonomously, even when the correction reveals a generalizable agent behavior rule.
- Do not add lessons for one-off task details that will not prevent a repeatable mistake
- Never keep a single `lessons.md`; create one short, descriptive file per lesson, such as `.agents/lessons/avoid-broad-git-add.md`
- Keep a `LESSONS.md` index in `.agents/lessons/` that lists every lesson file with a short title and one-line summary
- When adding a new lesson file, also add a matching entry to `.agents/lessons/LESSONS.md`
- Populate each index entry as a markdown link to the lesson file followed by a brief summary of the rule or mistake pattern
- In each lesson file, write the mistake pattern and the rule that should prevent the same mistake next time
- Ruthlessly iterate on these lessons until the mistake rate drops
- Review the shared lessons index and the relevant linked lesson files at the start of each session for the current project

## Local Project Context

- Treat this file as the shared default baseline.
- Read project-specific shared context from `agent-context/` when it exists.
- When available, use the `engineering-standards` skill for reusable coding, design, refactoring, debugging, and review guidance.
- When available, use the `testing-standards` skill for test strategy, test selection, test naming, Arrange-Act-Assert structure, regression coverage, and testing changes or bug fixes.
- When available, use the `refactor` skill for behavior-preserving internal restructuring and code-smell driven improvements.
- When available, use the `rest-api-design` skill for REST API contracts, endpoints, resource modeling, request/response shapes, validation errors, pagination, versioning, auth, documentation, and API contract tests.
- Review `.agents/lessons/LESSONS.md` and any relevant linked lesson files when they exist.
- Read `AGENTS.local.md` or `CLAUDE.local.md` when it exists; it is local, private, and ignored by git.
- Keep project-specific shared rules in `agent-context/`, not by editing the copied baseline.
- Do not run the project skill update command automatically at the start of every session. Run `npx.cmd skills update --project --yes` on Windows or `npx skills update --project --yes` elsewhere only when the user asks for a skill update or the current task directly requires syncing project skills. After it runs, check `git status --short`; report any changed skill files or update failures before continuing.

## Workflows

Use this section to choose the right workflow from the user's latest request. When multiple rows match, use the most specific workflow that covers the requested outcome, and keep the scope limited to what the user asked for.

### Workflow Selection Rules

| User input pattern | Apply this workflow | Rule |
| --- | --- | --- |
| User asks to define, draft, clarify, or update requirements, acceptance criteria, contracts, or a feature specification before implementation. | Feature Requirements And Specification Workflow | Use this when the deliverable is requirements or a specification, not production code. |
| User asks to build, add, implement, or change product behavior for a feature. | Feature Development Workflow | Use this when code changes are expected and the requested behavior is externally observable. |
| User asks to refactor, restructure, clean up, extract, rename, or simplify code while preserving behavior. | Refactor Workflow | Use this only when the intended outcome is internal structure change with no behavior change. If behavior changes are requested too, treat it as feature work. |
| User asks for a code review, review, audit, or risk assessment without asking for edits. | Review Workflow | Use this when the deliverable is review findings, not code changes. |
| User reports a bug, failing test, CI failure, runtime error, or regression. | Autonomous Bug Fixing | For non-trivial bugs, use `bug-diagnostician` first to create a diagnosis report and incident draft, show them to the user, and wait for explicit approval before `implementer` fixes the root cause and finalizes the incident report. For obvious bugs, fix directly and still create the incident report. Use Feature Development Workflow only when the fix expands into feature-level behavior or contract work. |
| User asks a direct question, requests a small documentation edit, or asks for a narrow mechanical change. | Normal task execution | Do the smallest useful thing. Do not force planner, implementer, or code-reviewer workflows unless the change grows into one of the rows above. |

### Feature Requirements And Specification Workflow

Use this workflow when drafting requirements and specifications for a new feature. This is a requirements and contracts workflow, not a deep technical design or OOP class design workflow.

1. `planner`: Create the requirements, specification, and standards-aware implementation plan artifact.

Only add deep implementation details, OOP classes, internal interfaces, or module designs when the user asks for them, an ADR requires them, or the existing architecture makes them necessary.

### Feature Development Workflow

For feature implementation work:

1. `planner` creates the specification and standards-aware implementation plan artifact.
2. `implementer` reads the specification and implementation plan artifact, writes code, runs verification, loops internally until the selected tests/checks pass, and produces a shared implementation report.
3. `code-reviewer` reviews the planner specification, implementation plan artifact, implementer report, and touched files.
4. If `code-reviewer` returns `BLOCK`, give the review report back to `implementer`. `implementer` fixes only the reported findings, keeps the original specification unchanged, reruns the relevant verification, and updates the implementation report with the new touched files and test results.
5. Send the updated implementation report and touched files back to `code-reviewer`. Repeat this review-fix loop until `code-reviewer` returns `APPROVE`, or stop on the blocker conditions below.
6. Run broader final verification when the work touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

Treat `WARNING` as a judgment call: fix it when the finding is tied to the specification, a likely bug, a security/privacy risk, or a meaningful test gap; otherwise report it as residual risk.

Stop and surface a blocker when:

- The same finding remains after 3 fix attempts.
- The fix requires changing the specification or expanding scope.
- Verification fails for a reason that is not understood.
- Fixing would require weakening tests or hiding a failure.

### Autonomous Bug Fixing Workflow

Use this workflow when the user reports a bug, failing test, CI failure, runtime error, or regression.

1. For non-trivial, ambiguous, recurring, CI-related, production-like, cross-module, or user-facing bugs, `bug-diagnostician` investigates first and writes `.agents/bug-diagnoses/bug-diagnosis_YYYYMMDD_short_description.md`.
2. `bug-diagnostician` also creates a draft incident report at `docs/incidents/incident_YYYYMMDD_short_description.md` with symptom, impact, draft root cause, and candidate follow-ups.
3. Show the diagnosis report, proposed fix direction, verification plan, and incident draft to the user. Wait for explicit approval before implementation starts.
4. `implementer` reads the approved diagnosis report and incident draft, fixes the root cause, runs verification, creates or updates the implementation report, and finalizes the incident report with confirmed root cause, fix, verification, and follow-ups.
5. `code-reviewer` reviews the code change, implementation report, diagnosis report when one exists, and final incident report for consistency with the evidence and verification.

For obvious one-line bugs, the main agent may skip `bug-diagnostician`, but the implementer or main agent still creates the final incident report.

### Refactor Workflow

Use this workflow when changing internal structure without intended behavior changes.

1. `planner` writes a refactor brief under `.agents/refactor-briefs/refactor-brief_YYYYMMDD_feature_name.md` using `refactor`, `engineering-standards`, and `testing-standards`:
   - Current behavior to preserve.
   - Files, modules, or boundaries in scope.
   - Files, modules, or boundaries out of scope.
   - Verification plan, including baseline checks when feasible.
   - Rollback risks or behavior-drift risks.
   - SQL, persistence, query performance, indexing, pagination, batching, execution-plan, or database access risks that require `sql-code-review` or `sql-optimization`.
2. `planner` writes a matching implementation plan under `.agents/implementation-plans/implementation-plan_YYYYMMDD_feature_name.md` and shows both artifacts to the user for approval before implementation starts.
3. `implementer` performs only the approved refactor using `refactor`, `engineering-standards`, and `testing-standards`; when SQL or database access is touched, also use `sql-code-review`, and use `sql-optimization` for query performance, indexes, pagination, batching, execution plans, or database load.
4. `implementer` keeps changes surgical, runs the planned verification, and produces a shared implementation report.
5. `code-reviewer` reviews the refactor brief plus the implementation plan, implementer report, and touched files with `engineering-standards`, `testing-standards`, and `refactor` for behavior drift, scope creep, missed tests, and unnecessary abstraction. Use `sql-code-review` and `sql-optimization` when the touched files include the SQL or database concerns listed above.
6. If `code-reviewer` returns `BLOCK`, `implementer` reads the shared review file, fixes only those findings, reruns relevant verification, and returns updated touched files.
7. Repeat the review-fix loop until `code-reviewer` returns `APPROVE`, or stop on the same blocker conditions listed in Feature Development Workflow.
8. Run broader final verification when the refactor touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

A refactor is successful only if externally observable behavior is unchanged, unless the user explicitly approves a behavior change.

### Review Workflow

Use this workflow when the user asks for a code review, audit, or risk assessment without asking for edits.

1. `code-reviewer` reviews the requested scope.
2. Report findings first, ordered by severity, with file/line references when available.
3. Do not make edits, run `implementer`, or enter a fix loop unless the user explicitly asks to fix the findings.

## Task Management

- Store task notes in `.agents/tasks/`
- Files inside `.agents/tasks/` are local working notes and should never be committed
- Plan First: Write the plan in a task-specific file in `.agents/tasks/`, for example `.agents/tasks/todo_20260520_update_login_validation.md`
- Create one task file per task: name it `todo_YYYYMMDD_synthetic_task_description.md`, using the run date and a short lowercase description of the task or feature with words separated by underscores
- Each task entry must include `planned on: YYYY-MM-DD` and `ran on: YYYY-MM-DD`
- Verify Plan: Check in before starting implementation
- Track Progress: Mark items complete as you go
- Explain Changes: High-level summary at each step
- Document Results: Add a review section to the same project-local task file
- Capture Lessons: Store each lesson in `.agents/lessons/` and keep `.agents/lessons/LESSONS.md` in sync


---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
