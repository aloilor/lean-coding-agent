# AGENTS.md

## Core Principles

- Simplicity First: Make every change as simple as possible. Impact minimal code.
- No Laziness: Find root causes. No temporary fixes. Senior developer standards.
- Minimal Impact: Changes should only touch what's necessary. Avoid introducing bugs.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

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

## 5. Demand Elegance (Balanced)

- For non-trivial changes: pause and ask, "Is there a more elegant way?"
- If a fix feels hacky: "Knowing everything I know now, implement the elegant solution."
- Skip this for simple, obvious fixes - don't over-engineer
- Challenge your own work before presenting it

## 6. Autonomous Bug Fixing

- When given a bug report: just fix it. Don’t ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching is required from the user
- Go fix failing CI tests without being told how

## 7. Self-Improvement Loop

- Keep shared agent lessons in `.agents/lessons/`
- After any correction from the user, add one new lesson file in `.agents/lessons/`
- Handle lesson capture autonomously when the correction reveals a generalizable agent behavior rule
- If the correction is ambiguous, task-specific, or preference-like, ask before writing a lesson
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
- Read `AGENTS.local.md` when it exists; it is local, private, and ignored by git.
- Keep project-specific shared rules in `agent-context/`, not by editing the copied baseline.
- At the start of every session, when `skills-lock.json` exists, automatically run the project skill update command from the repo root: use `npx.cmd skills update --project --yes` on Windows and `npx skills update --project --yes` elsewhere. After it runs, check `git status --short`; report any changed skill files or update failures before continuing.

## Feature Requirements And Specification Workflow

Use this workflow when drafting requirements and specifications for a new feature. This is a requirements and contracts workflow, not a deep technical design or OOP class design workflow.

1. `grill-with-docs`: Provide enough context first, including what the user wants, who it is for, rough scope, and relevant repo docs. Challenge the idea against existing repo docs and context. Check whether it conflicts with existing rules, misses requirements, duplicates an existing pattern, or has edge cases implied by the repo.
2. `create-specification`: Convert the clarified inputs into implementable requirements and contracts, such as behavior, inputs, outputs, data formats, validation rules, APIs, persistence rules, and test criteria.

Only add deep implementation details, OOP classes, internal interfaces, or module designs when the user asks for them, an ADR requires them, or the existing architecture makes them necessary.

## Feature Development Loop

For feature implementation work:

1. `planner` creates the specification.
2. `implementer` reads the specification, writes code, runs verification, loops internally until the selected tests/checks pass, and produces a shared implementation report.
3. `code-reviewer` reviews the planner specification plus the implementer report and touched files.
4. If `code-reviewer` returns `BLOCK`, `implementer` reads the shared review file, fixes only those findings, reruns verification, and returns updated touched files.
5. Repeat the review-fix loop until `code-reviewer` returns `APPROVE`, or stop on the documented blocker conditions.
6. Run broader final verification when the work touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

## Refactor Workflow

Use this workflow when changing internal structure without intended behavior changes.

1. `planner` writes a refactor brief using `refactor`, `engineering-standards`, and `testing-standards`:
   - Current behavior to preserve.
   - Files, modules, or boundaries in scope.
   - Files, modules, or boundaries out of scope.
   - Verification plan, including baseline checks when feasible.
   - Rollback risks or behavior-drift risks.
   - SQL, persistence, query performance, indexing, pagination, batching, execution-plan, or database access risks that require `sql-code-review` or `sql-optimization`.
2. `implementer` performs only the approved refactor using `refactor`, `engineering-standards`, and `testing-standards`; when SQL or database access is touched, also use `sql-code-review`, and use `sql-optimization` for query performance, indexes, pagination, batching, execution plans, or database load.
3. `implementer` keeps changes surgical, runs the planned verification, and produces a shared implementation report.
4. `code-reviewer` reviews the refactor brief plus the implementer report and touched files with `engineering-standards`, `testing-standards`, and `refactor` for behavior drift, scope creep, missed tests, and unnecessary abstraction. Use `sql-code-review` and `sql-optimization` when the touched files include the SQL or database concerns listed above.
5. If `code-reviewer` returns `BLOCK`, `implementer` reads the shared review file, fixes only those findings, reruns relevant verification, and returns updated touched files.
6. Repeat the review-fix loop until `code-reviewer` returns `APPROVE`, or stop on the documented blocker conditions.
7. Run broader final verification when the refactor touches shared behavior, API contracts, persistence, auth, security, or user-facing workflows.

A refactor is successful only if externally observable behavior is unchanged, unless the user explicitly approves a behavior change.

## Review Fix Loop

For implementation work that uses `planner`, `implementer`, and `code-reviewer`:

1. Run `implementer` from the approved specification.
2. Pass the planner specification and implementer-touched files to `code-reviewer`.
3. If `code-reviewer` returns findings, send the review report back to `implementer`.
4. `implementer` must fix only the reported findings, rerun relevant verification, and update its touched file list.
5. Run `code-reviewer` again with the same specification and updated touched files.
6. Repeat until `code-reviewer` returns `APPROVE`.

Automatically loop on `BLOCK`. Treat `WARNING` as a judgment call: fix it when the finding is tied to the specification, a likely bug, a security/privacy risk, or a meaningful test gap; otherwise report it as residual risk.

Stop and surface a blocker when:

- The same finding remains after 3 fix attempts.
- The fix requires changing the specification or expanding scope.
- Verification fails for a reason that is not understood.
- Fixing would require weakening tests or hiding a failure.

## Task Management

- Store task notes in the current tool's project-local tasks folder: use `.codex/tasks/` when working in Codex, and `.claude/tasks/` when working in Claude Code
- Files inside `.codex/tasks/` or `.claude/tasks/` are local working notes and should never be committed
- Plan First: Write the plan in a task-specific file in the current project's tasks folder, for example `.codex/tasks/todo_20260520_update_login_validation.md` or `.claude/tasks/todo_20260520_update_login_validation.md`
- Create one task file per task: name it `todo_YYYYMMDD_synthetic_task_description.md`, using the run date and a short lowercase description of the task or feature with words separated by underscores
- Each task entry must include `planned on: YYYY-MM-DD` and `ran on: YYYY-MM-DD`
- Verify Plan: Check in before starting implementation
- Track Progress: Mark items complete as you go
- Explain Changes: High-level summary at each step
- Document Results: Add a review section to the same project-local task file
- Capture Lessons: Store each lesson in `.agents/lessons/` and keep `.agents/lessons/LESSONS.md` in sync


---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
