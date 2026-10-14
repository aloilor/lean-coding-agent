# CODING-STANDARDS.md Guide

Answers: which existing files to imitate, which boundaries and data or security rules apply, and what must never be done. Everything here is something tooling does not already catch.

Example values below illustrate shape and specificity. Never copy them into a project.

## Enforced By Tooling

One line naming the linters, formatters, and type checkers with their config files, so agents do not restate or second-guess them.

- **Look at:** `eslint.config.*`, `.eslintrc*`, `.prettierrc*`, `biome.json`, `ruff.toml`, `[tool.ruff]`, `tsconfig.json` (`strict`), `.editorconfig`, `rustfmt.toml`, `golangci.yml`, `.markdownlint*`.
- **Belongs:** tool names, config paths, and the fix command if one exists.
- Good: "`ruff` and `mypy --strict` (`pyproject.toml`). Fix formatting with `ruff format`."

## Follow These Examples

The single most useful section: which file to copy when adding a common kind of thing.

- **Look at:** the most recently added file of each recurring kind (`git log --diff-filter=A --name-only --format= -n 200`): endpoints, components, migrations, jobs, CLI commands, skills, tests. Compare it with older files of the same kind; when patterns differ, the newer one is usually current, but ask the user to confirm.
- **Belongs:** `<kind of change>: follow <path>`, plus the one or two idioms that file shows and agents tend to miss (error type, logging call, config access, registration step).
- **Drop:** kinds of change that happen once, and descriptions of what the example contains.
- Good: "New skill: follow `skills/lean-grill-with-docs/`; add `agents/openai.yaml` and a README entry."
- Bad: "Follow existing patterns in the codebase."

## Boundaries

Structural rules enforced only by convention.

- **Look at:** import-restriction lint rules, path aliases, workspace and package layout, `exports` fields, ADRs, `CODEOWNERS`, and comments like `do not import`, `internal`, `public API`.
- **Belongs:** forbidden dependency directions, public surfaces that must stay compatible, files or modules that are mirrors or snapshots of others.
- Good: "`skills/setup-lean-coding-agent/references/` holds copies of source files; edit the source, then sync."
- Bad: "Keep modules loosely coupled."

## Data And Security

Rules about persistent data, configuration, secrets, and user data.

- **Look at:** migration directories and their history, config loaders, `.env.example`, logging setup, auth middleware, security notes in `docs/` or `SECURITY.md`.
- **Belongs:** migration rules, the one sanctioned way to read config or secrets, PII and logging rules, auth requirements for new endpoints.
- Write `None.` when the project has no persistent data, secrets, or user data.

## Never

Operations that are forbidden here, each with what to do instead.

- **Look at:** `DO NOT`, `HACK`, `NOTE`, `WARNING` comments, reverted commits (`git log --grep revert -i`), PR template checklists, and user answers.
- **Belongs:** `<forbidden operation> → <what to do instead>`.
- Good: "Edit files under `src/generated/` → change `openapi.yaml` and run `pnpm gen:api`."
- Bad: "Never write bad code."

## Template

Write this structure exactly. Keep every heading; write `None.` under a heading with no facts.

```md
# Coding Standards

## Enforced By Tooling
<tools and config paths>. Their rules are not restated here.

## Follow These Examples
- <kind of change>: follow `<path>`; <idiom agents miss>.

## Boundaries
- <rule>

## Data And Security
- <rule>

## Never
- <forbidden operation> → <what to do instead>
```
