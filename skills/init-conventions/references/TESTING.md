# TESTING.md Guide

Answers: what must pass before work is done, how to run one test quickly, what tests need to run, and how tests are written here. Verification commands live only in this file; `WORKFLOWS.md` does not repeat them.

Example values below illustrate shape and specificity. Never copy them into a project.

## Definition Of Done

The ordered commands that must pass before work is complete, matching what CI enforces.

- **Look at:** CI workflow files (`.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, ...), pre-commit and pre-push hooks (`.githooks/`, `.husky/`, `.pre-commit-config.yaml`), scripts in `package.json`, `Makefile`, `justfile`, `pyproject.toml`, `Taskfile.yml`, and testing commands in the README or `CONTRIBUTING.md`.
- **Belongs:** the exact command lines CI runs, in CI order, including required flags. Then run them.
- **Drop:** CI steps that only build artifacts, deploy, or publish (they belong in `WORKFLOWS.md`).
- Good: `` 2. `npm run check-skill-overrides` `` (CI fails when mirrored copies drift).
- Bad: "Run the test suite and make sure linting passes."

## Fast Loop

How to run the smallest useful scope while iterating.

- **Look at:** test runner config (`vitest.config.*`, `jest.config.*`, `pytest.ini`, `[tool.pytest]`, `go.mod`, `Cargo.toml`), how scripts invoke the runner, workspace layout for per-package commands.
- **Belongs:** one row per scope that differs from the full run: one file, one test by name, one package. Run at least one.
- **Drop:** scopes the runner's defaults make obvious when the full-suite command already shows the pattern.
- Good: `` | One file | `node --test tests/setup-project.test.mjs` | ``
- Bad: `` | One file | `run the test runner on the file` | ``

## Prerequisites

What must exist before tests pass.

- **Look at:** `docker-compose*.yml`, `.env.example`, global test setup files, CI `services:` and `env:` blocks, failures from running the commands above.
- **Belongs:** services, env var names, seed or fixture commands, required tool versions, and their order.
- Good: "Start Postgres with `docker compose up -d db` before `pnpm test:integration`; it reads `DATABASE_URL`."
- Write `None.` when the commands passed from a clean checkout.

## Writing Tests

How tests are written here, where it differs from the stack's habits.

- **Look at:** the three most recently added test files (`git log --diff-filter=A --name-only --format= -- '*test*' | head`), shared helpers, factories, fixtures, mock directories, and test-related review comments in `CONTRIBUTING.md` or PR templates.
- **Belongs:** where new tests go when it is not next to the source, which test type to write for which change, the mocking policy, helpers and factories to reuse, snapshot update rules.
- **Drop:** naming rules the existing files make obvious, and generic advice ("test edge cases").
- Good: "Never mock the database; use `withTestDb()` from `tests/support/db.ts`."
- Bad: "Tests should be isolated and deterministic."

## Traps

Mistakes that cost someone time already.

- **Look at:** `git log --oneline -n 100 --grep 'fix' --grep 'flak' --grep 'skip' --grep 'test'`, skipped or retried tests (`.skip`, `xit`, `@pytest.mark.xfail`, `retry`), CI retry settings, and failures from running the commands.
- **Belongs:** `symptom → cause → what to do instead`.
- Good: "`node --test tests/` fails with a module error → it treats the directory as one file → pass the glob `tests/*.test.mjs`."

## Template

Write this structure exactly. Keep every heading; write `None.` under a heading with no facts.

```md
# Testing

## Definition Of Done
Run in order; all must pass before work is complete.
1. `<command>`

## Fast Loop
| Scope | Command |
| --- | --- |
| <scope> | `<command>` |

## Prerequisites
- <fact>

## Writing Tests
- <fact>

## Traps
- <symptom> → <cause> → <what to do instead>
```
