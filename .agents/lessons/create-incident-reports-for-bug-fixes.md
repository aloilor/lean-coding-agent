# Create Incident Reports For Bug Fixes

## Mistake Pattern

I treated bug fixes as complete once the code change and verification were done, leaving no concise record of the symptom, impact, root cause, fix, checks, or follow-ups.

## Rule

For every bug fix, create an incident report. When a diagnosis agent runs, it owns the first draft; `code-reviewer` finalizes the report after the fix and verification, transcribing the confirmed facts from the implementer's report. For a small fix that ships without review, the main agent creates it. Keep durable incident reports in `docs/incidents/` unless the project defines a different committed incident-report location.
