# docs/conventions/TESTING.md

Purpose: make the exact verification commands and test traps explicit.

## Quality Rules

- Use actual commands from repo evidence.
- Name the command to run for each change type only when it differs from running the whole suite.
- Record setup the tests need (services, env vars, fixtures) and known flaky or slow suites.
- Omit test-file naming and locations when existing tests make them obvious.

## Template

```md
# Testing

## Commands

| Purpose | Command | Source |
| --- | --- | --- |
| Run all tests | `...` | `package.json` |

## Verification By Change Type

- Change type: command or check to run.

## Traps

- Required services, env vars, flaky suites, or snapshot rules.

## Open Questions

- Unknown.
```
