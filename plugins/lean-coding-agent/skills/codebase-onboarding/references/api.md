# agent-context/api.md

Purpose: document API contracts and endpoint conventions when the repo exposes an API.

## Quality Rules

- Create this file only when API evidence exists.
- Prefer actual routes, handlers, schemas, and docs.
- Include request and response examples only from code, tests, or docs.
- Do not invent auth, pagination, or error formats.

## Template

```md
# API

## API Overview

One paragraph describing the API surface.

## Resource Model

| Resource | Meaning | Evidence |
| --- | --- | --- |

## Endpoints

| Method | Path | Purpose | Evidence |
| --- | --- | --- | --- |

## Request / Response Shapes

- Include JSON examples or schema snippets from evidence.

## Validation And Errors

- Error format and validation behavior from evidence.

## Auth

- Authentication and authorization behavior from evidence.

## Pagination

- Pagination behavior from evidence.

## Examples

- Example request or handler path.

## Open Questions

- Unknown.
```
