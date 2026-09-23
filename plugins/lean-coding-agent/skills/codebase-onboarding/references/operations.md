# agent-context/operations.md

Purpose: document runtime, deployment, monitoring, jobs, and operational procedures.

## Quality Rules

- Create this file only when operational evidence exists.
- Prefer deployment configs, CI workflows, environment docs, queue/job code, and runbooks.
- Do not invent environments or monitoring tools.
- Keep secrets and private values out of docs.

## Template

```md
# Operations

## Runtime Environments

| Environment | Purpose | Evidence |
| --- | --- | --- |

## Deployment

| Step / System | Purpose | Evidence |
| --- | --- | --- |

## Configuration

| Variable / Config | Purpose | Source |
| --- | --- | --- |

## Jobs / Queues

- Document background jobs, schedules, and queues from evidence.

## Monitoring

- Logs, metrics, alerts, or dashboards from evidence.

## Incident Checks

| Symptom | Check | Evidence |
| --- | --- | --- |

## Open Questions

- Unknown.
```
