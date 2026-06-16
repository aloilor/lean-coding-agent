# Validation And Errors

## Overview

Validate at the boundary and return stable error responses. Clients should know what failed, whether they can fix it, and how to trace it.

## Input Validation

Validate shape, types, ranges, and business constraints before work begins.

Fail early with clear messages and identifiable fields. Reject unknown fields when the contract should stay strict and predictable.

```json
{
  "email": "not-an-email",
  "age": -1
}
```

## Error Format

Use one stable error format across the API.

```json
{
  "code": "validation_failed",
  "message": "Request validation failed.",
  "details": [
    {
      "field": "email",
      "message": "Must be a valid email address."
    }
  ],
  "requestId": "req_7f2b1c"
}
```

Include at least:

- `code`: stable machine-readable identifier.
- `message`: short human-readable description.
- `details`: optional field-level validation errors.
- `requestId`: tracing identifier for support and operations.

## Error Design Principles

Do not expose stack traces, SQL errors, vendor internals, or infrastructure details.

Separate technical failures from domain errors. Keep application error codes stable; messages may evolve, codes should not.

Return all practical validation errors in one response instead of forcing clients through fix-one-error-at-a-time loops.

## Response Consistency

Use consistent field names, enum values, and nullability rules.

Avoid ambiguous responses such as `success: true` without useful context. If a field is optional, document when it may be missing or `null`.

## Practical Checks

- Can clients distinguish validation, authorization, conflict, and server errors?
- Can support trace the request with `requestId`?
- Will the error contract survive internal refactors?
- Are field names, enum values, and nullability rules consistent?
