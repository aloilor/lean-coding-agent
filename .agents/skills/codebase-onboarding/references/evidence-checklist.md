# Evidence Checklist

Use this checklist to gather facts before writing `agent-context/` docs. Read only what is relevant to the repo and requested depth.

## Repo Orientation

- `AGENTS.md`, `CLAUDE.md`, override files when present.
- `README.md`, `docs/`, `agent-context/`, `CONTRIBUTING.md`, `CHANGELOG.md`.
- Top-level structure from `rg --files` and directory listing.
- `.gitignore` for generated or local-only paths.

## Stack And Tooling

- JavaScript / TypeScript: `package.json`, lockfiles, `tsconfig*.json`, framework config.
- Python: `pyproject.toml`, `requirements*.txt`, `tox.ini`, `noxfile.py`.
- .NET: `*.sln`, `*.csproj`, `Directory.Build.props`.
- Java / Kotlin: `pom.xml`, `build.gradle*`, `settings.gradle*`.
- Go: `go.mod`, `go.work`.
- Rust: `Cargo.toml`.
- Containers: `Dockerfile`, `docker-compose*.yml`.

## Architecture Evidence

- Entry points: app bootstrap, server start, CLI main, worker main.
- Routing or handler files.
- Dependency injection or composition root.
- Database, queue, cache, auth, storage, and third-party integration code.
- Existing ADRs or architecture docs.

## Workflows Evidence

- Scripts in package/build files.
- `Makefile`, `justfile`, task runner config, CI workflows.
- Local setup docs.
- Release, deployment, or environment docs.
- Hook scripts and generated-artifact rules.

## Testing Evidence

- Test directories and naming patterns.
- Test runner config.
- Fixtures, factories, seed data, mocks, snapshots.
- CI test jobs.
- Existing testing docs or standards.

## Domain Evidence

- Existing glossary or domain docs.
- Product docs, feature docs, route names, model names, event names.
- Terms repeated in tests, schemas, API resources, or user-facing copy.

## Good Examples

Use examples like these in generated docs:

- Actual command: `npm test`, `pytest`, `dotnet test`, `go test ./...`.
- Actual path: `src/features/billing/`, `app/api/orders/route.ts`.
- Actual config: `package.json` script, `.github/workflows/ci.yml` job.
- Actual contract: endpoint path, event name, database table, queue name.

## Bad Examples

Avoid examples like these unless the repo really contains them:

- "Run the test suite" without a command.
- "Uses a database" without naming evidence.
- "Modern frontend architecture" without concrete boundaries.
- "Auth is secure" without auth flow evidence.
