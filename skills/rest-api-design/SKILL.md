---
name: rest-api-design
description: Use this skill when designing, reviewing, implementing, or changing REST APIs, HTTP endpoints, API contracts, resource models, request/response payloads, validation errors, pagination, versioning, authentication, authorization, CORS, deprecation, API documentation, or API contract tests. Applies this repo's REST API design standards through resource modeling, HTTP semantics, boundary validation, stable errors, query/response design, security, documentation, and operations guidance.
---

# REST API Design

Apply this repo's shared REST API standards when creating, changing, reviewing, or documenting HTTP APIs.

Use this skill for API contract decisions.

## Load The REST Baseline

Read this compact rule index first:

- `references/RULES.md`

Do not load every detailed reference file by default. Open only the files relevant to the API decision:

- `references/resource-modeling.md` for resources, URLs, identifiers, nesting, and payload shape.
- `references/http-semantics.md` for methods, status codes, idempotency, and endpoint behavior.
- `references/validation-and-errors.md` for boundary validation, error formats, and failure details.
- `references/querying-and-responses.md` for pagination, filtering, sorting, content types, CORS, and response size.
- `references/versioning-and-security.md` for compatibility, API versions, auth, authorization, rate limits, and traceability.
- `references/documentation-and-operations.md` for endpoint docs, examples, observability, deprecation, and contract tests.

## Design Workflow

When working on a REST API:

1. Model the domain resource before naming the endpoint.
2. Choose HTTP methods and status codes by semantic behavior, not controller convenience.
3. Define request, response, and error shapes as stable client-facing contracts.
4. Bound collections with pagination and clear query parameters.
5. Treat authentication, authorization, rate limits, payload limits, CORS, and trace IDs as part of the contract.
6. Preserve backward compatibility unless there is an explicit migration plan.
7. Keep endpoint documentation and examples aligned with implementation.
8. Add or update API contract tests when behavior, validation, auth, or documented examples change.

## Red Flags

- Action URLs where resources would be clearer.
- Inconsistent method, status, error, or response semantics across similar endpoints.
- Unbounded list responses.
- Database, framework, vendor, stack trace, or permission internals leaking to clients.
- Authorization checked only at route level when resource-level permissions matter.
- Breaking changes without a migration or deprecation plan.
- API docs that describe a different contract than the code implements.
