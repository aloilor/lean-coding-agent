# Implementation Report: <name>

Source: <approved plan, incident report, or direct request>
Last updated for: Initial implementation | Review pass <N> fixes

<!-- Keep the core headings and scale detail to the task. Replace placeholders
and choices; remove drafting guidance from the completed report. Use
"Not applicable — <reason>" for conditional sections. Update this report on
every implementation and review-fix pass. -->

## Acceptance Criteria Status

| ID | Status | Evidence |
| --- | --- | --- |
| AC-1 | Done / Partial / Not done | <test, check, or reason> |

## Changes

| File | Purpose |
| --- | --- |
| <path> | <why it changed> |

New dependencies: None | <packages, matching the plan's approved list>

## Design Conformance

How the implemented components match the plan's implementation design, and any
explicitly approved revisions. Report unapproved drift as a blocker instead of
recording it here.

## Test-First Evidence

| Behavior | RED assertion observed | GREEN result | Refactor |
| --- | --- | --- | --- |
| <behavior or AC ID> | <failing assertion> | <passing test> | <structural change or None> |

Exemptions: <non-behavioral or characterization-test exemptions with reasons, or None>

## Verification

| Command or check | Result |
| --- | --- |
| <command> | Pass / Fail / Not run — <reason> |

## Bug Fix Details (conditional)

- Confirmed root cause: <cause>
- Fix: <repair>
- Follow-ups: <items or None>
- Draft incident: <docs/incidents/incident_YYYYMMDD_<name>.md>

## Review-Fix History (conditional)

| Pass | Finding ID | Resolution |
| --- | --- | --- |
| <N> | F-1 | <change made and verification> |

## Residual Risks And Did Not Do

Residual risks, manual checks, skipped tests, and explicit omissions, or
"No meaningful omissions."
