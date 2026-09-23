# agent-context/folder-structure.md

Purpose: explain important directories and files, not every path.

## Quality Rules

- Document paths that affect navigation, ownership, generated output, or common edits.
- Avoid listing every file.
- Include evidence for non-obvious claims.
- Call out local-only and ignored paths.

## Template

```md
# Folder Structure

## Overview

One paragraph describing the repo shape.

## Important Paths

| Path | Purpose | Notes / Evidence |
| --- | --- | --- |
| `src/` | Application source. | Inferred from source files. |
| `tests/` | Automated tests. | Contains `*.test.*` files. |

## Generated Or Ignored Paths

| Path | Why It Exists | Commit Policy |
| --- | --- | --- |
| `.codex/tasks/` | Local Codex task notes. | Do not commit. |

## Ownership And Boundaries

- `path/`: owner or boundary if known, otherwise `Unknown`.

## Examples

- To find route handlers, inspect `...`.

## Open Questions

- Unknown.
```
