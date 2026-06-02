# Logging

## Log Structured Events

- Prefer structured logs over free-form text so tools can query them reliably.
- Keep field names stable across services and environments.
- Include machine-readable values for status, duration, identifiers, and event type.

Example log shape:

```json
{
  "timestamp": "2026-06-02T10:15:00Z",
  "level": "INFO",
  "service": "billing-api",
  "event": "invoice_created",
  "requestId": "req_8f12",
  "durationMs": 34
}
```

## Include Stable Context

- Add request, trace, job, tenant, or user identifiers when they help debugging.
- Prefer stable IDs over names that can change or contain sensitive data.
- Keep the same key names across services so log searches stay predictable.

Example useful context:

- `requestId`: ties all logs from one API request together
- `traceId`: connects logs to distributed traces
- `jobId`: groups logs from one background job run
- `tenantId`: helps isolate tenant-specific incidents in multi-tenant systems

## Use Levels Consistently

- Use `DEBUG` for temporary or development-focused detail.
- Use `INFO` for normal lifecycle events and successful operations worth recording.
- Use `WARN` for unusual conditions that the system recovered from.
- Use `ERROR` for failures that need investigation or affect behavior.

## Log Boundaries And Outcomes

- Log incoming requests, background job starts and finishes, retries, external API calls, and important state changes.
- Log the outcome and the small amount of context needed to explain it.
- Avoid repeating the same failure at multiple layers unless each layer adds distinct value.

Example boundary events:

- `payment_retry_scheduled`
- `email_delivery_failed`
- `inventory_sync_started`
- `inventory_sync_completed`

## Avoid Sensitive Or Noisy Logs

- Do not log secrets, access tokens, raw passwords, or unnecessary personal data.
- Be careful with request and response bodies, especially on authentication, billing, and user-content paths.
- Avoid high-volume logs inside tight loops unless they are sampled or truly needed.

Example safer logging choice:

- Log `userId`, `requestId`, and `validationErrors`
- Do not log full JWTs, raw credit card data, or complete request bodies by default

## Practical Checks

- Can I filter these logs reliably by service, request, or event type?
- Would the logs explain both the failure and the surrounding context?
- Am I logging anything sensitive or unnecessarily expensive?
- Are log levels consistent enough that alerts and dashboards can trust them?
