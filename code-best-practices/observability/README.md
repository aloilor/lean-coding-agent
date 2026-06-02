# Observability

This folder collects reusable observability best practices for understanding system behavior, detecting problems early, and making production issues diagnosable.

## Sources

- Google, [Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)
- OpenTelemetry, [Observability Primer](https://opentelemetry.io/docs/concepts/observability-primer/)
- OpenTelemetry, [Traces](https://opentelemetry.io/docs/concepts/signals/traces/)

## Contents

- [Logging](./logging.md): how to write structured logs with useful context and low noise.
- [Monitoring And Alerting](./monitoring-and-alerting.md): how to track service health, define useful metrics, and alert on actionable problems.
- [Tracing And Correlation](./tracing-and-correlation.md): how to connect logs, metrics, and traces across requests, jobs, and services.

## Core Rules

- Use logs for event detail, metrics for trends and thresholds, and traces for request flow.
- Start from user-visible signals such as latency, errors, and availability.
- Make telemetry structured and correlated with stable identifiers.
- Alert only on conditions that need action.
- Avoid collecting sensitive data unless it is truly necessary and properly protected.
