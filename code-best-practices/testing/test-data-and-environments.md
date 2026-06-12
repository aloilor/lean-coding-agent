# Test Data And Environments

## Use Realistic Data Safely

- Use data that matches production shapes, limits, optional fields, encodings, and relationships.
- Do not use production personal data unless it is legally allowed, minimized, and properly anonymized.
- Prefer synthetic or anonymized fixtures for repeatable tests.
- Include edge cases that real data tends to expose, such as empty names, long strings, time zones, and missing optional values.

## Keep State Isolated

- Reset databases, queues, caches, and files between tests that mutate shared state.
- Prefer unique IDs, temporary resources, transactions, or disposable containers over shared named records.
- Avoid tests that depend on execution order.
- Design integration tests to run safely in parallel.

## Control Time And Randomness

- Inject clocks instead of reading system time deep inside business logic.
- Fix random seeds when randomness is part of the test.
- Test time zones, daylight saving changes, expiration windows, and clock skew when they affect behavior.

Good pattern:

```text
create_order(now=fixed_time)
```

Avoid:

```text
create_order()  # internally reads the current wall clock
```

## Own External Boundaries

- Use contract tests for external APIs, events, and service-to-service messages.
- Stub third-party services when the test is about your code's reaction, not the provider itself.
- Run a small number of live dependency checks on a schedule or pre-release path when real integration risk matters.
- Record enough request and response detail to diagnose contract drift without leaking secrets.

## Keep Environments Close Enough

- Run tests against the same schema migrations, feature flag defaults, and important configuration shape as production.
- Keep environment differences explicit when exact parity is impossible.
- Seed only the data a test needs so failures are easier to understand.
- Clean up temporary cloud resources, accounts, topics, buckets, and credentials automatically.

## Practical Checks

- Could this test fail because another test left state behind?
- Does the fixture resemble real input without exposing sensitive data?
- Are time, randomness, and external services controlled enough for repeatable results?
- Can integration tests run in parallel without shared names, ports, accounts, or records?
- Are environment differences documented where they affect confidence?
