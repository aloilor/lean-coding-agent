# Versioning And Security

## Versioning

- Do not version too early; first try to evolve the contract in a backward-compatible way.
- When a breaking change is unavoidable, use one consistent strategy across the project, for example `/v1`.
- Do not introduce multiple active versions without a clear deprecation policy.
- If header-based versioning is chosen instead of URI versioning, use it consistently and document it clearly.

## When To Version From Day One

- Do not assume every new API must start with an explicit version.
- Start with a version such as `/v1` when the API is public, externally consumed, or expected to support long-lived clients.
- Consider skipping an explicit version at first when the API is internal, early-stage, and controlled by a small number of coordinated clients.
- If you do version from day one, define what counts as a breaking change and how deprecation will work.

Examples:

- URI versioning: `/v1/users`
- Header versioning: `Accept: application/vnd.example.v1+json`
- Public API starting with a version: `/v1/payments`
- Internal service without an explicit version yet: `/orders`

## Backward Compatibility

- Add new fields in a non-breaking way.
- Do not change the meaning of existing fields.
- Do not reuse enums or statuses for different meanings.

## Authentication And Authorization

- Define authentication and permissions as part of the contract, not as an implementation detail.
- Use API keys for simple server-to-server access where appropriate.
- Use bearer tokens or OAuth 2.0 flows when user-scoped access and delegated permissions matter.
- Rule of thumb:
  - Same app, simple API: bearer token auth may be enough.
  - Third-party apps, delegated permissions, user consent, scopes: use OAuth 2.0.
- Validate authorization for every sensitive resource, not only at the endpoint level.
- Apply the principle of least privilege.

Examples:

- `Authorization: ApiKey sk_live_abc123`
- `Authorization: Bearer eyJhbGciOi...`

## Security Basics

- Always use HTTPS.
- Limit rate, payload size, and abuse surface.
- Do not expose predictable identifiers when they increase enumeration risk.
- Sanitize outputs and log safely, without unnecessary sensitive data.
- Return clear rate-limit headers and `429` responses when limits are exceeded.

Example rate-limit headers:

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716912000
```

## Observability

- Plan from the start to generate or accept a `requestId` or `correlationId`, include it in logs and error responses, and propagate it to downstream services.
- Log meaningful events for audit and debugging.
- Track baseline metrics for latency, errors, and saturation.

## Practical Checks

- Is a new version truly necessary?
- Will this change break existing clients?
- Are security concerns part of the endpoint review?
