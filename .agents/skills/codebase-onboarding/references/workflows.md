# agent-context/workflows.md

Purpose: preserve executable project workflows.

## Quality Rules

- Do not invent commands.
- Prefer commands from package files, Makefiles, CI, or existing docs.
- Include verification steps when the repo provides them.
- Keep deployment and release sections evidence-backed.

## Template

```md
# Workflows

## Setup

| Step | Command / Action | Evidence |
| --- | --- | --- |
| Install dependencies | `...` | `package.json` |

## Run Locally

| Task | Command | Notes |
| --- | --- | --- |
| Start app | `...` | Unknown if not documented. |

## Build

| Task | Command | Evidence |
| --- | --- | --- |

## Review And Commit

- Branch, PR, commit, or review rules from repo docs.

## Release / Deployment

- Document only if repo evidence exists.

## Troubleshooting

| Symptom | Likely Cause | Check |
| --- | --- | --- |

## Open Questions

- Unknown.
```
