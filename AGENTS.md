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

- After any correction from the user, add a new lesson in the current project's `.codex/tasks/lessons/` folder
- Never keep a single `lessons.md`; create one short, descriptive file per lesson, such as `.codex/tasks/lessons/avoid-broad-git-add.md`
- In each lesson file, write the mistake pattern and the rule that should prevent the same mistake next time
- Ruthlessly iterate on these lessons until the mistake rate drops
- Review relevant lesson files at the start of each session for the current project


## Task Management

- The `.codex/tasks/` folder is project-local: use the `.codex/tasks/` directory inside the specific project you are working on, not this shared repo
- Plan First: Write the plan in the current project's daily task file, for example `.codex/tasks/todo_20260520.md`
- Use one task file per day: keep all tasks for that date in the same `.codex/tasks/todo_YYYYMMDD.md` file, and append new tasks to that existing file
- Each task entry must include `planned on: YYYY-MM-DD` and `ran on: YYYY-MM-DD`
- Verify Plan: Check in before starting implementation
- Track Progress: Mark items complete as you go
- Explain Changes: High-level summary at each step
- Document Results: Add a review section to the same project-local `.codex/tasks/todo_YYYYMMDD.md` file
- Capture Lessons: Store lessons in the current project's `.codex/tasks/lessons/` folder as separate files like `.codex/tasks/lessons/descriptive-lesson-name.md`


---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
