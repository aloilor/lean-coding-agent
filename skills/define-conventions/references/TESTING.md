# Testing Grill Guide

Find out how testing works today and how the team wants it to work. Where those differ, write the target and scope it, so agents know what new tests should do without rewriting old ones.

Examples below show the shape of a useful line. Never copy them into a project.

## What Must Pass

- **Ask about:** what must pass before work counts as done, what CI does not cover but people are expected to run, whether a red CI blocks merging.
- **Look at:** CI workflows, git hooks, test scripts in manifests.
- Useful: "`test:integration` must pass before merge, though CI skips it."
- Obvious: "Run the tests before committing."

## How Tests Should Be Written

- **Ask about:** which kind of test a given change needs, mocking policy, where tests live when not next to the source, helpers and factories to reuse, snapshot rules, coverage expectations, what is deliberately not tested.
- **Look at:** recent test files, shared helpers and fixtures, mock directories. If tests disagree, show the split and ask which is the target.
- Useful: "Never mock the database in new tests; use `withTestDb()`. Older mocked tests in `tests/unit/orders/` stay until touched."
- Obvious: "Tests should be isolated and deterministic."

## Test Exemplars

Confirm one or two excellent test files the same way as code exemplars: ask the user first, show an excerpt, say why it is good, then record kind of test, path, and what to imitate.

## Test Environments

- **Ask about:** what tests need to run (services, env var names, seed data), shared test environments and who may use them, how to run one test quickly when it is not obvious from the runner.
- **Look at:** `docker-compose*`, `.env.example`, global setup files, CI `services:` and `env:` blocks.
- Useful: "Start Postgres with `docker compose up -d db` first; integration tests read `DATABASE_URL`."

## Local Setup Traps

Problems that block someone from getting code running and tested.

- **Ask about:** what new contributors get stuck on, required tool versions, one-time steps that are not in the setup script.
- **Look at:** version files, bootstrap scripts, devcontainer config, setup-related fix commits.
- Useful: "Run `git config core.hooksPath .githooks` once, or mirrored files drift."

## Flaky Tests And Traps

- **Ask about:** known flaky tests, how they are handled, failures that mislead.
- **Look at:** skipped or retried tests, CI retry settings, `fix` and `flaky` commits.
- Useful: "`checkout.spec` fails when run in parallel; rerun it with `--workers=1` before investigating."

## What Agents May Do Alone

- **Ask about:** updating snapshots, skipping or deleting tests, touching shared test databases, running slow or expensive suites.
