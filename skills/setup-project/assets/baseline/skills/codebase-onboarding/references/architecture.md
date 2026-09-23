# agent-context/architecture.md

Purpose: describe system shape and boundaries at a level useful before editing code.

## Quality Rules

- Prefer stable boundaries over implementation minutiae.
- Mark indirect conclusions as `Inferred from ...`.
- Include dependencies only when evidence exists in code, config, or docs.
- Do not prescribe new architecture.

## Template

```md
# Architecture

## Summary

Two to four sentences describing the architecture.

## System Boundaries

| Boundary | Responsibility | Evidence |
| --- | --- | --- |
| Web app | Serves user workflows. | `...` |

## Data Flow

1. User or system action.
2. Application boundary.
3. Persistence, integration, or output.

## Dependencies

| Dependency | Used For | Evidence |
| --- | --- | --- |
| Package or service | Purpose. | `package.json`, config, or code path |

## Constraints

- Constraint with evidence or `Inferred from ...`.

## Examples

- Example feature path: `...`.

## Open Questions

- Unknown.
```
