# Incident Reports

Store durable incident investigations for extended bug fixes in this folder. Bounded bugs use a concise diagnosis and approval plan instead of a durable incident file.

Use `incident_YYYYMMDD_short_description.md`. The diagnostician drafts the Investigation section before implementation; the code reviewer confirms the final facts after repair and verification, trims Investigation to a durable summary, and finalizes Status, Root Cause, Fix, Verification, and Follow-ups.

## Canonical Template

```markdown
# Incident Report: [Short Name]

## Status

Draft from diagnosis — awaiting user approval and repair.

## Symptom

- [observable failure]

## Impact

- [affected users, workflows, data, security/privacy, or "unknown"]
- Severity: [low/medium/high/critical with brief rationale]

## Investigation

- Reproduction / evidence: [command, log, test, or check → result and key output summary; omit secrets]
- Areas involved: [`path/to/file.ext` → why it matters]
- Likely root cause: [fact-backed hypothesis]
- Material alternatives: [why less likely, or "none"]
- Fix recommendation: [smallest responsible repair direction and regression coverage]
- Verification plan: [pre-fix reproduction and post-fix checks]
- Unknowns / risks: [none, or concise uncertainty]

## Root Cause

- Pending confirmation — see Investigation.

## Fix

- Pending implementation.

## Verification

- Pending implementation.

## Follow-ups

- [none, or candidate follow-up]
```
