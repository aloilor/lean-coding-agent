# Feature Specification Template

Copy the template below. Keep every section heading, the section order, and the ID prefixes exactly as written so that all specifications in a project share one shape and can be compared, reviewed, and approved consistently.

## Variants

| Section | Full | Lean |
| --- | --- | --- |
| Feature | Required | Required |
| Objective | Required | Required |
| User Stories | Required | Required |
| Scope | Required | Required |
| Out of Scope | Required | Required |
| Actors and Permissions | Required | Omit |
| Preconditions | Required | Omit |
| Functional Requirements | Required | Required |
| Business Rules | Required | Omit |
| Error Handling and Edge Cases | Required | Omit |
| Acceptance Criteria | Required | Required |
| UI / UX Reference | Required | Omit |
| Non-Functional Requirements | Required | Omit |
| Dependencies and Assumptions | Required | Omit |
| Open Questions | Required | Required |
| Approval | Required | Required |

In the full variant, a section with genuinely nothing to say keeps its heading and states `None.` with a one-line reason, so the reader knows it was considered. In the lean variant, fold the most important rules or edge cases into Functional Requirements instead of adding sections.

## Field Conventions

- **ID:** `FEAT-NNN`, zero-padded to three digits, unique within the project.
- **Version:** `MAJOR.MINOR`, starting at `1.0`. Minor for clarifications, major for scope or behavior changes.
- **Status:** one of `Draft` (open questions remain), `Proposed` (ready for client review), `Approved`, `Superseded`.
- **ID prefixes:** `US-` user story, `FR-` functional requirement, `BR-` business rule, `EC-` edge case, `AC-` acceptance criterion, `NFR-` non-functional requirement, `OQ-` open question. Number sequentially from 1 within each prefix.
- **Titles:** every FR, EC, AC, and NFR has a short title after an em dash: `FR-4 — File name`. Open questions use the question itself as the title. BRs and USs may omit titles.

## Template

````markdown
# Feature Specification — {Feature Name}

## Feature

- **ID:** FEAT-{NNN}
- **Name:** {Feature Name}
- **Version:** 1.0
- **Status:** Draft

## Objective

{One or two sentences: who can do what, and what outcome it enables.}

## User Stories

**US-1**
As a {role}, I want to {capability} so that {benefit}.

**US-2**
As a {role}, I want to {capability} so that {benefit}.

## Scope

The feature includes:

- {included capability};
- {included capability}.

## Out of Scope

The following are not included in this feature:

- {excluded capability a reader might reasonably assume is included};
- {excluded capability}.

## Actors and Permissions

The feature is available to:

- {Role};
- {Role}.

{Statement of what users without permission can and cannot do.}

## Preconditions

- {Condition that must hold before the feature can be used.}
- {Condition.}

## Functional Requirements

**FR-1 — {Title}**
The system shall {single, verifiable behavior}.

**FR-2 — {Title}**
When {trigger}, the system shall {behavior}.

**FR-3 — {Title}**
The {output} shall include:

- {item};
- {item}, when applicable.

## Business Rules

**BR-1**
{Rule that constrains behavior regardless of screen or entry point.}

**BR-2**
{Rule.}

## Error Handling and Edge Cases

**EC-1 — {Title}**
If {failure or unusual condition}, {expected system behavior and what the user sees}.

**EC-2 — {Title}**
{Boundary, limit, or unusual input} shall {expected behavior}.

## Acceptance Criteria

**AC-1 — {Title}**

- **Given** {initial context}
- **When** {action}
- **Then** {observable outcome}
- **And** {additional outcome}

**AC-2 — {Title}**

- **Given** {initial context}
- **When** {action}
- **Then** {observable outcome}

## UI / UX Reference

- {Where the feature appears and how it is triggered.}
- {Reference to approved designs, or "No designs are attached."}
- Any mockups attached to this specification are considered illustrative unless explicitly marked as binding.

## Non-Functional Requirements

**NFR-1 — Performance**
{Measurable target, with the conditions under which it applies.}

**NFR-2 — Security**
{Measurable or verifiable security requirement.}

**NFR-3 — {Compatibility | Accessibility | Availability | Backward compatibility | ...}**
{Requirement.}

## Dependencies and Assumptions

- {Existing capability, data, or service this feature relies on.}
- {Assumption made while writing this specification that the client should confirm.}

## Open Questions

**OQ-1 — {Decision the client must make?}**
Recommended: {the answer this spec is written for}, because {reason}. Affects: {FR-n, AC-n}.

**OQ-2 — {Decision?}**
Recommended: {answer}, because {reason}. Affects: {IDs}.

All open questions must be resolved before the feature is considered approved for development.

## Approval

By approving this specification, the client confirms that the scope, expected behavior, and acceptance criteria described above represent the agreed requirements for FEAT-{NNN} — {Feature Name}.

- **Client representative:** ______________________
- **Date:** ______________________
- **Approved version:** ______________________
- **Signature / Approval reference:** ______________________
````

## Section Guidance

- **Objective** — the outcome, not the mechanism. "Allow authorized users to generate a PDF of an invoice so it can be downloaded, printed, or shared", not "Add a PDF button".
- **User Stories** — 1–5 stories for the roles that matter. Context only; never the sole source of a requirement.
- **Scope / Out of Scope** — Out of Scope is the anti-dispute section. Name adjacent features, automation, history/versioning, customization, and notifications that a reader might assume.
- **Actors and Permissions** — every role that can use the feature, plus what happens for everyone else.
- **Functional Requirements** — one behavior each, `shall`, concrete formats and examples. Lists of required content belong here.
- **Business Rules** — constraints that hold everywhere: calculations, consistency with other screens, data-ownership rules, authorization rules.
- **Error Handling and Edge Cases** — failures, missing optional data, limits, special characters, concurrency, duplicates, expired or revoked state.
- **Acceptance Criteria** — Given/When/Then, observable outcomes only. Cover the success path, each permission boundary, each business-relevant edge case, and failure behavior.
- **UI / UX Reference** — placement and triggers; state whether mockups are binding.
- **Non-Functional Requirements** — measurable targets. `should` is acceptable for performance targets; security requirements use `shall`.
- **Dependencies and Assumptions** — what must already exist, and assumptions the client should confirm.
- **Open Questions** — client decisions only, each with a recommended answer, the reason, and the IDs it affects. The rest of the spec is written as if every recommendation is accepted, so the client confirms or overrides rather than designs. When none remain, write `None.` and say how earlier questions were resolved. While any remain, Status stays `Draft`.
- **Approval** — keep the wording; it is what makes the document a sign-off artifact.
