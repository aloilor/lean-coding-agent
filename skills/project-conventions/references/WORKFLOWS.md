# docs/conventions/WORKFLOWS.md

Purpose: record commands and workflow traps an agent would not infer from the stack defaults.

## Quality Rules

- Do not invent commands. Take them from package files, Makefiles, CI, existing docs, or the user.
- Omit commands that are the stack default and work as-is (`npm install`, `cargo build`). If all of them are, say so in one line.
- Include required flags, env vars, services, ordering, and generated-file rules.
- Record review, commit, and release rules only when they are not already in `AGENTS.md`, `CONTRIBUTING.md`, or similar.

## Template

```md
# Workflows

Standard commands for the stack apply unless listed here.

## Commands

| Task | Command | Why it is non-obvious | Source |
| --- | --- | --- | --- |
| Regenerate API client | `pnpm gen:api` | Required after editing `openapi.yaml`; CI fails otherwise. | `.github/workflows/ci.yml` |

## Traps

- Symptom or mistake -> cause -> what to do instead.

## Review And Release

- Rules not already documented elsewhere.

## Open Questions

- Unknown.
```
