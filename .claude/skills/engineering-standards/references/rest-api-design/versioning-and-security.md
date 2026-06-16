# Versioning And Security

## Overview

API evolution and security are part of the contract. Design for compatibility first, then version only when a breaking change is truly necessary.

## Versioning

Do not version too early. First try to evolve the contract in a backward-compatible way.

When a breaking change is unavoidable, use one strategy consistently, such as `/v1` or documented header-based versioning.

## When To Version From Day One

Start with a version when the API is public, externally consumed, or expected to support long-lived clients.

Consider skipping explicit versioning when the API is internal, early-stage, and controlled by coordinated clients.

Examples:

- URI versioning: `/v1/users`
- Header versioning: `Accept: application/vnd.example.v1+json`
- Public API starting with a version: `/v1/payments`
- Internal service without an explicit version yet: `/orders`

## Backward Compatibility

Add fields in a non-breaking way. Do not change the meaning of existing fields.

Do not reuse enum values or statuses for different meanings.

## Authentication And Authorization

Define authentication and permissions as part of the contract, not as an implementation detail.

Use API keys for simple server-to-server access when appropriate. Use bearer tokens or OAuth 2.0 when user-scoped access, delegated permissions, consent, or scopes matter.

Validate authorization for every sensitive resource, not only at the endpoint level. Apply least privilege.

Examples:

- `Authorization: ApiKey sk_live_abc123`
- `Authorization: Bearer eyJhbGciOi...`

## Security Basics

Always use HTTPS.

Limit request rate, payload size, and abuse surface. Avoid predictable identifiers when they increase enumeration risk. Sanitize outputs and log safely, without unnecessary sensitive data.

Return useful rate-limit signals.

```http
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 1716912000
```

## Security Traceability

Generate or accept a `requestId` or `correlationId`, include it in logs and error responses, and propagate it to downstream services so sensitive operations can be traced.

Log enough security-relevant context to investigate authentication failures, authorization denials, rate limits, abuse patterns, and suspicious access without exposing secrets or unnecessary personal data.

## Practical Checks

- Is a new version truly necessary?
- Will this change break existing clients?
- Are authentication, authorization, rate limits, and logs part of endpoint review?
- Can operations trace a request across downstream services?
