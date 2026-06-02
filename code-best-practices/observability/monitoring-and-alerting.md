# Monitoring And Alerting

## Start With User-Facing Signals

- Monitor latency, error rate, throughput, and availability before lower-level technical counters.
- Treat saturation signals such as queue depth, CPU pressure, and connection pool exhaustion as supporting indicators.
- Start from what users feel, not only what infrastructure exposes.

## Define Useful Metrics

- Use counters for totals, gauges for current values, and histograms for distributions such as latency.
- Track both system metrics and business metrics when both matter to service health.
- Keep metric names and labels consistent so dashboards and alerts are easier to reuse.

Example metric set:

- `http_requests_total`
- `http_request_duration_ms`
- `job_failures_total`
- `queue_depth`
- `checkout_success_rate`

## Use SLOs And Error Budgets Carefully

- Define service-level objectives for user-visible behaviors that matter.
- Use error budgets to decide when reliability work should take priority over feature work.
- Do not invent SLOs for everything. Focus on the few signals that represent real service quality.

Example SLO:

- `99.9%` of `POST /payments` requests complete successfully in under `500 ms` over 30 days

## Alert On Actionable Symptoms

- Alert on symptoms that require action, such as sustained error spikes or unacceptable latency.
- Prefer symptom-based alerts over shallow infrastructure thresholds when possible.
- Add enough time windowing and deduplication to avoid noisy flapping alerts.
- Route each alert to a clear owner and link it to a runbook when practical.

Example actionable alerts:

- `5xx rate > 5% for 10 minutes`
- `p95 checkout latency > 2 seconds for 15 minutes`
- `queue depth growing continuously for 20 minutes`

## Keep Dashboards Focused

- Maintain a small overview dashboard for service health and a deeper dashboard for diagnosis.
- Show current status, recent trends, and the main dependencies that can explain a failure.
- Remove charts that nobody uses during incidents or reviews.

Example overview dashboard panels:

- request rate
- error rate
- p95 latency
- queue depth
- dependency health

## Practical Checks

- Would these metrics tell me quickly whether users are affected?
- Does every alert correspond to a real action someone should take?
- Are latency and error metrics measured in a way that matches user experience?
- Do the dashboards help with diagnosis instead of just showing a wall of charts?
