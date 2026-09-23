# agent-context/README.md

Purpose: index the available project context and tell agents where to start.

## Quality Rules

- Keep this file short.
- Link every context file that exists.
- Mark missing or incomplete files as `Missing` or `Partial`.
- Do not duplicate the detailed content from the linked files.

## Template

```md
# Agent Context

This folder contains shared project-specific context for agents working in this repo.

## Start Here

1. Read `folder-structure.md` to understand where things live.
2. Read `architecture.md` to understand boundaries and data flow.
3. Read `workflows.md` and `testing.md` before changing code.
4. Read `domain.md` for project-specific language.

## Files

| File | Purpose | Status |
| --- | --- | --- |
| `folder-structure.md` | Important directories and ownership notes. | Current |
| `architecture.md` | System shape, boundaries, and dependencies. | Current |
| `workflows.md` | Setup, build, run, review, and release workflows. | Current |
| `testing.md` | Test commands, frameworks, and expectations. | Current |
| `domain.md` | Domain glossary and preferred terms. | Current |

## Open Questions

- Unknown.
```

## Example

```md
| `api.md` | API contracts and endpoint conventions. | Partial |
```
