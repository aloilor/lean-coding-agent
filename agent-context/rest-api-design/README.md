# REST API Design

## Overview

REST APIs are contracts. Design URLs, methods, payloads, errors, security, documentation, and operations so clients can integrate without guessing or writing special-case logic.

## Contents

- [Resource Modeling](./resource-modeling.md)
- [HTTP Semantics](./http-semantics.md)
- [Validation And Errors](./validation-and-errors.md)
- [Querying And Responses](./querying-and-responses.md)
- [Versioning And Security](./versioning-and-security.md)
- [Documentation And Operations](./documentation-and-operations.md)

## Core Rules

- Model URLs around resources, not actions.
- Use HTTP semantics consistently and predictably.
- Return structured and stable error responses.
- Support pagination, filtering, sorting, and search on collection endpoints where they matter.
- Version only when a breaking change is truly necessary.
- Treat authentication, authorization, observability, docs, and tests as part of the API design.
- Use Documentation And Operations as the canonical home for operational observability; Versioning And Security covers security traceability.

## Quick Reference

| Area | One-Liner | Red Flag |
|------|-----------|----------|
| Resources | URLs are nouns | `/createUser`, `/deleteOrder` |
| Methods | HTTP method matches behavior | `POST` for every operation |
| Status Codes | Codes guide client action | Always returning `200` |
| Errors | Stable shape and codes | Stack traces or changing error shapes |
| Collections | Pagination and clear query params | Unbounded list responses |
| Versioning | Version breaking contracts | Versions added without policy |
| Security | Auth, authz, limits, HTTPS | Endpoint-only permission checks |
| Operations | Docs, logs, tests stay current | Docs drift from real behavior |
