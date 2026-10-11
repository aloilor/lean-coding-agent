# docs/conventions/CODING-STANDARDS.md

Purpose: record coding rules an agent would break by following the code's surface.

## Quality Rules

- Include conventions that tooling does not enforce and existing code does not make obvious.
- Include boundaries and invariants, including API compatibility, data and migration, and security rules.
- Omit anything the linter, formatter, or type checker already enforces; name the tool instead.
- Each rule states what to do or avoid and its evidence or source.
- Do not invent rules. Record existing practice and what the user states.

## Template

```md
# Coding Standards

Enforced by tooling: `eslint`, `prettier`, `tsc --strict` (see their config). Rules below are not.

## Rules

- Rule an agent would otherwise break. Source: `path`, doc, or maintainer.
- `module-a` must not import from `module-b`. Source: `docs/adr/0003-boundaries.md`.

## Never

- Forbidden operation and what to do instead. Source: ...

## Open Questions

- Unknown.
```
