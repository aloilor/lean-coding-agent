# agent-context/data.md

Purpose: document storage, schema, migration, and data ownership conventions.

## Quality Rules

- Create this file only when storage or data-model evidence exists.
- Prefer migrations, schemas, ORM models, seed scripts, and tests.
- Distinguish actual storage from inferred storage.
- Do not document hypothetical tables or collections.

## Template

```md
# Data

## Storage Overview

One paragraph describing persistence and data stores.

## Schemas

| Entity / Table / Collection | Purpose | Evidence |
| --- | --- | --- |

## Migrations

| Path / Tool | Purpose | Evidence |
| --- | --- | --- |

## Seed / Fixture Data

- Paths and usage rules.

## Data Ownership

- Ownership and boundary rules.

## Examples

- Example schema, migration, or seed command.

## Open Questions

- Unknown.
```
