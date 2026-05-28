# HTTP Semantics

## Methods

- `GET` for reads with no side effects.
- `POST` for creation or other non-idempotent operations.
- `PUT` for full replacement of a resource when the contract supports it.
- `PATCH` for partial updates.
- `DELETE` for logical or physical removal, with documented behavior.

Examples:

- `GET /products/{productId}` returns one product.
- `POST /products` creates a new product.
- `PUT /profiles/{profileId}` replaces the full profile representation.
- `PATCH /profiles/{profileId}` updates only selected fields.
- `DELETE /sessions/{sessionId}` revokes a session.

## Status Codes

- `200 OK` for successful reads or updates that return a body.
- `201 Created` for successful creation, with a `Location` header when useful.
- `202 Accepted` when work has been accepted but completes asynchronously.
- `204 No Content` when the operation succeeds without a response body.
- `400 Bad Request` for malformed input.
- `401 Unauthorized` when valid authentication is missing.
- `403 Forbidden` when the caller is authenticated but not allowed.
- `404 Not Found` when the resource does not exist or is not visible.
- `409 Conflict` for state conflicts or business constraints.
- `422 Unprocessable Entity` for semantic validation failures, if that is the project standard.
- `429 Too Many Requests` when the caller exceeds rate limits.

Examples:

- `POST /users` returns `201 Created` with `Location: /users/usr_123`.
- `PATCH /users/usr_123` returns `200 OK` with the updated resource.
- `DELETE /users/usr_123` returns `204 No Content` when no response body is needed.
- `POST /payments` may return `202 Accepted` if processing is asynchronous.
- `GET /admin/reports` returns `403 Forbidden` when the caller lacks permission.

## Idempotency

- `GET`, `PUT`, and `DELETE` should be idempotent.
- For critical `POST` endpoints, consider idempotency keys, especially for payments or retryable creation flows.

Example:

```http
POST /payments
Idempotency-Key: 7b0d90f2-7f4b-4b8f-a83a-194fb4f73ee5
```

## Consistency

- Do not mix different semantics for similar endpoints.
- Document edge cases such as upserts, asynchronous deletes, and partial update behavior.
- Declare request and response content types explicitly, with `application/json` as the default format unless there is a strong reason otherwise.

## Practical Checks

- Does the chosen method clearly describe what happens?
- Does the status code help the client react without special-case logic?
- Is automatic retry safe for this endpoint?
