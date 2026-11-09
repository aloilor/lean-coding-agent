# Coding Standards Grill Guide

Find out how code here should be written and which code deserves imitation. This is the area where the repo is least trustworthy: agents copy what they see, so the goal is to name what is worth copying and what is not.

Examples below show the shape of a useful line. Never copy them into a project.

## Coding Style

Cover what tooling does not enforce. Learn what is enforced first and leave those rules out, because the tool already catches them.

- **Ask about:** naming beyond language defaults, error handling (throw or return, where errors are caught), when to extract a function or abstraction, comments, type strictness and escape hatches, async patterns, banned idioms, file and module organization.
- **Look at:** linter, formatter, and type-checker config; places where recent files disagree; review comments; `CONTRIBUTING`.
- Useful: "Services return `Result`; only controllers turn errors into HTTP responses."
- Useful: "Don't add an interface for a single implementation."
- Obvious: "Keep functions small and readable."

## Architecture Boundaries

Record what may depend on what, not what the layout looks like, and leave out boundaries a tool already enforces. Code that crosses a boundary may be what's wrong, so ask which side is intended.

- **Ask about:** which layers or modules may call which, internals other modules must not reach into, where a new feature or shared helper belongs, boundaries the code breaks today.
- **Look at:** imports between top-level modules, especially ones running against the usual direction; dependency-lint config; package manifests in a monorepo.
- Useful: "Only `billing/` writes to the ledger tables; other modules call `billing/service`."
- Obvious: "Keep concerns separated."

## Exemplars

Excellent code to mimic, one or two per recurring kind of code: endpoint, service, component, job, migration.

1. Ask the user first which modules they are proud of. People know this better than git history does.
2. Add candidates from the scan. Recency and frequency only tell you what is common, so read the code and judge it: clear boundaries, honest error handling, small surface, good tests.
3. Show a short excerpt of each candidate and say why it is good. Ask whether this is the code to mimic.
4. Record confirmed exemplars as kind of code, path, symbol, and what to imitate. Skip pasted snippets, which go stale and cost tokens, and line numbers, which shift.
5. If nothing qualifies for a kind of code, write nothing rather than lowering the bar.

- Useful: "New endpoint: mimic `createOrder` in `src/api/orders/create.ts`, especially how it validates once at the boundary."

## Code To Avoid Copying

The inverse of exemplars, and often the more valuable half.

- **Ask about:** legacy areas, abandoned patterns, code that works but should not spread, migrations in progress and which side is current.
- **Look at:** directories with old patterns next to newer ones, `TODO`, `HACK`, and `DEPRECATED` comments, reverted commits.
- Useful: "`src/legacy-users/` hand-writes SQL; don't copy it and don't migrate it unless asked."

## Generated Files

- **Ask about:** what is generated or mirrored, what to edit instead, how to regenerate.
- **Look at:** `DO NOT EDIT` and `@generated` headers, codegen config, sync scripts.
- Useful: "Edit `openapi.yaml`, not `src/generated/`; regenerate with `pnpm gen:api`."

## Dependencies

- **Ask about:** who may add one, preferred and banned libraries, what justifies a new one, version pinning.
- **Look at:** manifests, lockfile policy, overlapping libraries that suggest an unfinished migration.
- Useful: "Use `date-fns`; `moment` remains only in `src/reports/`."

## Data Access And Schema

Only when the project has a data store. This covers how queries and schema changes are written; how migrations roll out belongs to deployment.

- **Ask about:** the sanctioned way to query (ORM, query builder, raw SQL), who opens and owns transactions, table and column naming, required columns, indexing expectations, soft or hard deletes.
- **Look at:** models and schema files, recent migrations, query helpers and the code that bypasses them.
- Useful: "Open transactions only in service methods; repositories never commit."
- Useful: "Queries on `orders` go through `activeOrders()`, which excludes soft-deleted rows."

## Secrets, PII, And Logging

- **Ask about:** the one sanctioned way to read config and secrets, what must never be logged, how user data is handled.
- **Look at:** config loaders, `.env.example`, logging setup, `SECURITY.md`.
- Useful: "Read config only through `settings`; never log request bodies from `/auth`."

## Authorization And Input Trust

Only when the project has users or accepts untrusted input. A missed check here looks like working code, so name where each check must happen.

- **Ask about:** where permission checks live, how tenants are isolated, where input is validated and what later code may assume, how uploads and other untrusted content are handled.
- **Look at:** auth middleware and guards, endpoints that skip them, validation schemas, `SECURITY.md`.
- Useful: "Every route declares `requirePermission()`; a check inside a service does not replace it."
- Useful: "Every query on tenant data filters by `tenantId` from the session, never from the request body."

## API Design And Compatibility

Only when the repo exposes an API, whether to other services or to its own clients.

- **Ask about:** error format, pagination, idempotency of writes, naming and versioning, whether internal APIs follow the same rules. For consumers outside the repo, also ask what counts as public, how long old behavior stays, and how removal is announced.
- **Look at:** API schemas, error helpers, handlers that disagree with each other, versioned paths.
- Useful: "Errors return `{ code, message }`; new list endpoints use cursor pagination. Offset pagination in `/v1/` stays, but don't copy it."

## Performance, Accessibility, And I18n

Only when the scan shows they apply. Record concrete requirements, not aspirations.

- Useful: "All user-facing strings go through `t()`."

## What Agents May Do Alone

- **Ask about:** adding dependencies, changing public APIs, changing the database schema, changing permission checks, editing generated or vendored code, large refactors.
