# Code Review: <name> — Pass <N>

<!-- Keep the core headings and scale detail to the task. Replace placeholders
and choices; remove drafting guidance from the completed review. Repeat the
finding block for confirmed findings only. Finding IDs stay stable across
passes: keep an earlier finding's ID and number new findings after the highest
existing ID. Use "Not applicable — <reason>" for conditional sections. Agent
instructions govern evidence requirements, scope, blocking decisions, and
verdicts. -->

## Verdict

Verdict: APPROVE | WARNING | BLOCK
Counts: CRITICAL <n>, HIGH <n>, MEDIUM <n>, LOW <n>
Reason: <brief justification and any required next action>

## Prior Findings

Pass 1: "Not applicable — first pass." Later passes: list every finding from
earlier passes.

| ID | Title | Status |
| --- | --- | --- |
| F-1 | <title> | Resolved / Still open / Regressed / Withdrawn |

## Findings

New and still-open findings, ordered by severity, or "No findings."

### F-1: [<severity>] <title>

- Location: <file:line>
- Trigger and incorrect outcome: <concrete failure>
- Evidence: <why existing validation, callers, tests, or guards do not prevent it>
- Impact and severity rationale: <consequence>
- Fix direction: <smallest responsible correction>
- Disposition: Blocking | Non-blocking
- Scope basis: <requirement, approved plan, incident, or review scope>
- Snippet (HIGH or CRITICAL only): <relevant code without secrets>

## Scope And Inputs

- Reviewed change: <commit, diff, or requested scope>
- Plan/specification: <link or not applicable>
- Implementation report: <link or not applicable>
- Incident investigation: <link or not applicable>
- Missing required inputs: <list or None>

## Review Coverage

Mark each audit Checked, Not applicable, or Incomplete. Explain every
Incomplete audit here; do not repeat it elsewhere.

### Security

Status: Checked | Not applicable | Incomplete

- Checked: <classes inspected, with paths and guards>
- Not applicable: <classes with reasons>
- Findings: <IDs or None>

### Specification Fidelity

Status: Checked | Not applicable | Incomplete

| Requirement | Implementation evidence | Verification evidence | Result |
| --- | --- | --- | --- |
| AC-1 | <location> | <test or check> | Satisfied / Gap / Unverified |
| New dependencies | <manifest changes> | <plan line> | Approved / Unapproved / None |
| Plan revisions | <deviations found> | <revision entry> | Approved / Unexplained / None |

If no originating contract applies, explain why this section is not applicable.

### Test-First And Refactor Evidence

Status: Checked | Not applicable | Incomplete

Describe the applicable failing assertion, GREEN result, refactor outcome, and
baseline and post-change verification evidence. Explain coverage gaps or
exemptions and link any findings by ID.

### Design Principles And Code Smells

Status: Checked | Not applicable | Incomplete

Describe the design contracts and structural smells inspected, with evidence.
When the plan supplies an implementation design, compare actual responsibility
ownership, contracts, dependencies, and main flow with it, and assess the
resulting design independently. Link confirmed in-scope risks by finding ID.

### Documentation

Status: Checked | Not applicable | Incomplete

In-scope developer documentation created or updated, or missing and stale
documents with finding IDs.

## Verification

Distinguish checks run by the reviewer from supplied results.
Record relevant outcomes and any verification gaps.

## Incident Finalization (conditional)

Bug-fixing workflows only: Finalized | Pending (verdict not APPROVE) | Blocked (draft missing)

## Remaining Risks And Out-Of-Scope Observations

Material uncertainty not captured as findings, and relevant observations about
untouched code. Do not turn unrelated debt into required repairs.

## Did Not Do

Review steps not performed that are not already marked Incomplete above, or
"No meaningful omissions."
