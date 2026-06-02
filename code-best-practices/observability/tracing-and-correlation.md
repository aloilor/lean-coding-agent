# Tracing And Correlation

## Correlate Everything With Stable IDs

- Generate or accept a request ID at system boundaries and carry it through the whole flow.
- Use trace and span identifiers across services so one failing request can be reconstructed end to end.
- Return request IDs to clients when that helps support and debugging.

Example correlation headers:

```http
X-Request-ID: req_8f12
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
```

## Use Tracing For Request Flow

- Distributed tracing is most useful when work crosses service, queue, database, or third-party boundaries.
- Record the major spans that explain where time was spent and where failures happened.
- Do not try to trace every tiny in-process detail if it adds noise without helping diagnosis.

Example trace flow:

- API gateway receives `POST /checkout`
- checkout service validates cart
- payment service authorizes payment
- order service writes order
- email worker sends confirmation

## Connect Logs, Metrics, And Traces

- Add request IDs or trace IDs to logs whenever possible.
- Link dashboards and alerts to traces or log searches when your tooling supports it.
- Keep service names, operation names, and environment labels consistent across signals.

Example correlated log:

```json
{
  "service": "checkout-api",
  "event": "payment_authorization_failed",
  "requestId": "req_8f12",
  "traceId": "4bf92f3577b34da6a3ce929d0e0e4736"
}
```

## Sample Intentionally

- Full tracing is often too expensive at scale, so choose sampling deliberately.
- Keep enough coverage for slow, failed, or unusual requests even when general traffic is sampled.
- Review sampling strategy after incidents to make sure important paths are still visible.

## Trace Important Boundaries

- Trace external HTTP calls, database queries, queue publish and consume steps, and background job execution when they are material to system behavior.
- Capture duration, outcome, and key attributes that explain the operation.
- Avoid recording sensitive payloads just because tracing makes them easy to attach.

## Practical Checks

- Can I move from an alert to the relevant logs and traces quickly?
- Would one problematic request be diagnosable across service boundaries?
- Is sampling preserving the requests I care about most?
- Are trace attributes useful without exposing sensitive data?
