# Create Incident Reports For Bug Fixes

## Mistake Pattern

I treated bug fixes as complete once the code change and verification were done, leaving no concise record of the symptom, impact, root cause, fix, checks, or follow-ups.

## Rule

For every bug fix, create an incident report. When a diagnosis agent runs, it owns the first draft; the implementer owns the final report after the fix and verification. Keep durable incident reports in `docs/incidents/` unless the project defines a different committed incident-report location.
