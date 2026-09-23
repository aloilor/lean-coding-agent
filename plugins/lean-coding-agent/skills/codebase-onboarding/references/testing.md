# agent-context/testing.md

Purpose: make verification expectations explicit.

## Quality Rules

- Use actual test commands from repo evidence.
- Distinguish unit, integration, end-to-end, lint, typecheck, and smoke checks when visible.
- Document fixture and test-data conventions only when evidence exists.
- Include what to run for common change types.

## Template

```md
# Testing

## Test Stack

| Layer | Tooling | Evidence |
| --- | --- | --- |
| Unit | `...` | `package.json`, config, or test files |

## Commands

| Purpose | Command | Evidence |
| --- | --- | --- |
| Run all tests | `...` | `package.json` |

## Test Locations

| Path | Test Type | Notes |
| --- | --- | --- |

## Naming And Structure

- Describe conventions found in existing tests.

## Fixtures And Test Data

- Describe fixture locations and cleanup rules.

## Verification Expectations

- Which checks to run for docs, frontend, API, database, or shared logic changes.

## Open Questions

- Unknown.
```
