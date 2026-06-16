# HTTP Semantics

## Overview

Use HTTP methods, status codes, and idempotency rules consistently. Clients should be able to infer what happened and what is safe to retry.

## Methods

Use methods according to their meaning:

- `GET` for reads with no side effects.
- `POST` for creation or other non-idempotent operations.
- `PUT` for full replacement when the contract supports replacement.
- `PATCH` for partial updates.
- `DELETE` for logical or physical removal with documented behavior.

Examples:

- `GET /products/{productId}` returns one product.
- `POST /products` creates a product.
- `PUT /profiles/{profileId}` replaces the full profile representation.
- `PATCH /profiles/{profileId}` updates selected fields.
- `DELETE /sessions/{sessionId}` revokes a session.

## Status Codes

Use status codes that help clients react correctly:

- `200 OK` for successful reads or updates with a body.
- `201 Created` for successful creation.
- `202 Accepted` for asynchronous work.
- `204 No Content` for success without a body.
- `400 Bad Request` for malformed input.
- `401 Unauthorized` for missing or invalid authentication.
- `403 Forbidden` for authenticated callers without permission.
- `404 Not Found` for resources that do not exist or are not visible.
- `409 Conflict` for state conflicts.
- `422 Unprocessable Entity` for semantic validation failures when that is the project standard.
- `429 Too Many Requests` for rate limits.

## Idempotency

`GET`, `PUT`, and `DELETE` should be idempotent. For critical retryable `POST` operations, especially payments or creation flows, support idempotency keys.

```http
POST /payments
Idempotency-Key: 7b0d90f2-7f4b-4b8f-a83a-194fb4f73ee5
```

## Consistency

Do not mix different semantics for similar endpoints. Document edge cases such as upserts, asynchronous deletes, and partial update behavior.

Declare request and response content types explicitly, with `application/json` as the default unless there is a strong reason otherwise.

## Practical Checks

- Does the chosen method clearly describe what happens?
- Does the status code help the client react without special-case logic?
- Is automatic retry safe for this endpoint?
- Are unusual behaviors such as upsert, async delete, or partial update documented?
