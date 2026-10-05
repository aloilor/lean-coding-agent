# Code Review: <name> — Pass <N>

<!-- Keep the core headings and scale detail to the task. Replace placeholders
and choices; remove drafting guidance from the completed review. Repeat the
finding block for confirmed findings only; use "No findings" when appropriate.
Use "Not applicable — <reason>" for conditional sections. Agent instructions
govern evidence requirements, scope, blocking decisions, and verdicts. -->

## Findings

Order by severity. If there are none, state "No findings."

### F-1: [<severity>] <title>

- Location: <file:line>
- Trigger and incorrect outcome: <concrete failure>
- Evidence: <why existing validation, callers, tests, or guards do not prevent it>
- Impact and severity rationale: <consequence>
- Fix direction: <smallest responsible correction>
- Disposition: Blocking | Non-blocking
- Scope basis: <requirement, approved plan, incident, or review scope>

For HIGH or CRITICAL findings, include the relevant snippet without exposing
secrets.

## Scope And Inputs

- Reviewed change: <commit, diff, or requested scope>
- Plan/specification: <link or not applicable>
- Implementation report: <link or not applicable>
- Incident investigation: <link or not applicable>
- Missing required inputs: <list or None>

## Review Coverage

### Security

Status: Checked | Not applicable | Incomplete

Describe the applicable security checks, inspected paths and guards, and
supporting evidence. Explain exclusions or incomplete checks and link any
confirmed vulnerabilities to their finding IDs.

### Specification Fidelity

Status: Checked | Not applicable | Incomplete

| Requirement | Implementation evidence | Verification evidence | Result |
| --- | --- | --- | --- |
| AC-1 | <location> | <test or check> | Satisfied / Gap / Unverified |

If no originating contract applies, explain why this section is not applicable.
Link omissions, contradictions, or unexplained deviations to their finding IDs.

### Test-First And Refactor Evidence

Status: Checked | Not applicable | Incomplete

Describe the applicable failing assertion, GREEN result, refactor outcome, and
baseline and post-change verification evidence. Explain coverage gaps or
exemptions and link any findings by ID.

### Design Principles And Code Smells

Status: Checked | Not applicable | Incomplete

Describe the applicable design contracts and structural smells inspected,
with evidence supporting the assessment. Explain exclusions or incomplete
checks and link confirmed in-scope risks to their finding IDs.
When the plan supplies an implementation design, compare actual responsibility
ownership, contracts, dependencies, and main flow with it. Distinguish approved
revisions from unexplained deviations; assess the resulting design independently.

## Verification

Distinguish checks run by the reviewer from supplied results.
Record relevant outcomes and any verification gaps.

## Remaining Risks And Limitations

State material uncertainty and relevant out-of-scope observations.
Do not turn unrelated debt into required repairs.

## Did Not Do

Explicit omissions, or "No meaningful omissions."

## Verdict

Counts: CRITICAL <n>, HIGH <n>, MEDIUM <n>, LOW <n>
Verdict: APPROVE | WARNING | BLOCK
Reason: <brief justification and any required next action>
