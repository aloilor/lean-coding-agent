# Validation And Errors

## Input Validation

- Always validate shape, types, ranges, and business constraints at the boundary.
- Fail early with clear messages and identifiable fields.
- Do not accept unknown fields when the contract should stay strict and predictable.

Example invalid request:

```json
{
  "email": "not-an-email",
  "age": -1
}
```

## Error Format

- Return one stable error format across the API.
- Include at least:
  - `code`: a stable machine-readable identifier.
  - `message`: a short human-readable description.
  - `details`: optional field-level validation errors.
  - `requestId`: an identifier useful for tracing and support.

Example error response:

```json
{
  "code": "validation_failed",
  "message": "Request validation failed.",
  "details": [
    {
      "field": "email",
      "message": "Must be a valid email address."
    },
    {
      "field": "age",
      "message": "Must be greater than or equal to 0."
    }
  ],
  "requestId": "req_7f2b1c"
}
```

## Error Design Principles

- Do not expose stack traces or infrastructure details to clients.
- Separate technical failures from domain errors.
- Use stable application error codes; messages may evolve, codes should not.
- Return all validation errors in one response when practical, instead of forcing clients into fix-one-error-at-a-time loops.

## Response Consistency

- Keep naming consistent for fields, enums, and nested structures.
- Avoid ambiguous responses such as `success: true` without context.
- If a field is optional, document when it may be missing or `null`.

## Practical Checks

- Can a client easily distinguish validation, authorization, and conflict errors?
- Can support or operations trace the request using `requestId`?
- Will the error remain useful even after internal refactors?
