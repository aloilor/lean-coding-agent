# agent-context/workflows.md

Purpose: preserve executable project workflows.

## Quality Rules

- Do not invent commands.
- Prefer commands from package files, Makefiles, CI, or existing docs.
- Include verification steps when the repo provides them.
- Keep deployment and release sections evidence-backed.
- When a reviewer-owned quality gate exists, document its exact command, stable script contracts, configuration files, ownership, and the latest operational status of every check. Mark skips and pending policy decisions explicitly.

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

## Reviewer-Owned Quality Gate

| Check | Command | Configuration | Status | Evidence / Pending Decision |
| --- | --- | --- | --- | --- |
| Example | `...` | `...` | operational-pass / operational-fail / skipped / pending-approval | `...` |

## Release / Deployment

- Document only if repo evidence exists.

## Troubleshooting

| Symptom | Likely Cause | Check |
| --- | --- | --- |

## Open Questions

- Unknown.
```
