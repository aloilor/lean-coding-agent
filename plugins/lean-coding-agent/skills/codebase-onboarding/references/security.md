# agent-context/security.md

Purpose: document auth, authorization, secrets, sensitive data, and compliance constraints.

## Quality Rules

- Create this file only when security evidence exists.
- Avoid exposing secrets or private values.
- Prefer auth middleware, permission checks, config names, and existing docs.
- Mark gaps as open questions rather than assuming safety.

## Template

```md
# Security

## Authn / Authz

| Mechanism | Purpose | Evidence |
| --- | --- | --- |

## Secrets

| Secret / Config Name | Purpose | Source |
| --- | --- | --- |

## Sensitive Data

- Data types and handling rules from evidence.

## Threat Notes

- Known risks, assumptions, or controls.

## Compliance

- Compliance constraints from evidence.

## Open Questions

- Unknown.
```
