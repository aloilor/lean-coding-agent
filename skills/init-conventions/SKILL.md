---
name: init-conventions
description: "Initialize or refresh docs/conventions/CODING-STANDARDS.md, TESTING.md, and WORKFLOWS.md with repo-specific facts an agent needs to work correctly: verified commands, example files to follow, boundaries, forbidden operations, generated files, and traps. Gathers evidence from the repo, runs the commands it records, and interviews the user for what the repo cannot show. Use whenever the user wants to create, fill, initialize, update, or refresh project conventions, coding standards, testing docs, or docs/conventions/, or after setting up the Lean Coding Agent baseline in a project."
---

# Init Conventions

Write three files under `docs/conventions/` that tell an agent what is specific to this repo: the commands that prove work is done, the files to imitate, the lines not to cross, and the traps others already hit. `AGENTS.md` already tells agents when to read them; do not edit `AGENTS.md` or `CLAUDE.md`.

| File | Answers | Guide and template |
| --- | --- | --- |
| `docs/conventions/TESTING.md` | What must pass before I'm done? How do I run one test? What do tests need? How are tests written here? | [references/TESTING.md](references/TESTING.md) |
| `docs/conventions/CODING-STANDARDS.md` | Which file do I copy? Which boundaries, data, and security rules apply? What must I never do? | [references/CODING-STANDARDS.md](references/CODING-STANDARDS.md) |
| `docs/conventions/WORKFLOWS.md` | How do I set up, regenerate, commit, and release? Which docs must change with the code? What breaks CI? | [references/WORKFLOWS.md](references/WORKFLOWS.md) |

Project terms live in `GLOSSARY.md` and decisions in `adr/`, both owned by `lean-grill-with-docs`. Do not restate them; a rule may cite an ADR.

## Why Output Goes Generic, And How To Avoid It

Convention docs fail when an agent fills headings with what is usually true for the stack: "write unit tests", "follow SOLID", "use meaningful names". Those lines cost tokens on every read and change nothing. They appear when a section is filled from general knowledge instead of evidence. So:

- **Every fact starts from evidence or the user.** Each reference file lists where to look for each section. A section with no evidence and no user answer is written as `None.`, never padded.
- **Apply the swap test.** If a line would still be true pasted into another repo with the same stack, delete it. A surviving line names something only this repo has: a path, a command with its flags, a symbol, a config key, a decision.
- **Run commands before recording them.** A command that ran is a fact; a command that looks right is a guess.

## What Belongs

Keep a fact when all three hold:

1. **Specific.** It passes the swap test.
2. **Actionable.** An agent would run it, imitate it, or avoid something because of it.
3. **Confirmed.** Code, config, CI, docs, git history, a command run, or the user backs it. Otherwise write it with `(inferred: <evidence>)`, for example `(inferred: only used in .github/workflows/ci.yml; not run locally)`.

Copy facts that already exist in the README, `CONTRIBUTING.md`, or `docs/` into the right section, condensed to the fact itself. These files are the one place an agent reads to work correctly; a link costs another read and is easy to skip.

Leave out directory maps, tech-stack tables, architecture overviews, endpoint or schema inventories, and rules the linter, formatter, or type checker already enforces (name the tool instead).

## Process

1. **Read what exists.** `docs/conventions/` (including `GLOSSARY.md` and `adr/`), `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, the README, `docs/`, and `.github/`. If the three files exist, follow **Refresh** below. If a legacy `agent-context/` folder exists, treat its content as candidates and tell the user it can be deleted once migrated.
2. **Gather evidence, file by file.** Read each reference file before working on its doc and work through its "Look at" lists with `rg --files`, `rg`, `git log`, and targeted reads. Note each candidate with its evidence. Do not read every file in the repo.
3. **Verify commands.** Run every Definition Of Done command and at least one Fast Loop command per test runner. Also run setup or generation commands when they are safe and fast. Skip commands that deploy, publish, push, write to shared or remote state, or need credentials or services you do not have; record those as `(inferred: ...)`. When a command fails, find out why: a missing service, env var, or ordering requirement becomes a Prerequisite or Trap. Do not fix the repo.
4. **Interview.** Ask the user about every gap the repo cannot answer, as many questions as needed. Before asking, check that the repo really cannot answer it. Ask in rounds grouped by file, number the questions, and give each one a candidate answer from your evidence, worded so "yes" accepts it. For example: "`src/api/orders/` and `src/api/legacy-users/` handle errors differently. Is `orders/` the pattern new endpoints should follow?" Typical repo-invisible facts: which of two coexisting patterns is current, rules reviewers enforce, forbidden operations, past incidents, flaky tests, deploy and release constraints. If the user declines, keep the evidence-backed facts and mark the rest `(inferred: ...)` or drop them.
5. **Filter.** Apply the three checks in "What Belongs" to every candidate. Delete failures instead of rewording them into something vaguer.
6. **Write.** Use each reference's template exactly: every heading present, `None.` under empty ones, bullets and tables instead of prose. Aim for one screen per file (about 60 lines). If a file grows beyond that, cut the least actionable facts first.
7. **Report in chat.** List what was added, removed, and marked inferred, commands that failed, and questions still open. Open questions stay in the report, not in the files.

## Refresh

When the files already exist, re-check each fact: rerun the recorded commands, confirm referenced paths and example files still exist, and look for evidence added since the files last changed (`git log -1 --format=%cs -- docs/conventions/`). Keep confirmed facts and remove stale ones. Before removing a fact a person wrote that you cannot disprove, ask.

## Rules

- **Document, don't legislate.** Record existing practice and what the user states. Do not invent rules, thresholds, or architecture.
- **Trust code over docs.** When docs and code disagree, record what the code does and report the conflict.
- **Keep secrets out.** Name env vars and config keys, never values.
