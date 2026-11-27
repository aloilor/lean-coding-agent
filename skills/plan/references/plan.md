# Plan: <name>

Workflow: planning | feature | refactor | bug-fixing
Status: Draft | Awaiting approval | Approved (<actual user approval reference>)

<!-- Keep the core headings and scale detail to the task. Replace placeholders
and choices; remove drafting guidance from the completed plan. Sections marked
"(conditional)" may be "Not applicable — <reason>". Set Status to Approved only
after the main agent confirms actual user approval and Open Questions is "None". -->

## Objective And Requirements

Describe the intended outcome and the requirements it must satisfy.
Link the originating request, specification, or incident when available.
For bug fixes, state the confirmed root cause and the repair contract here.

## Evidence And Decisions

- Relevant code, documentation, or investigation evidence.
- Resolved user decisions and their rationale.
- Assumptions.
- Grill outcome.

## Open Questions

Unresolved decisions that block approval, or "None".

## Scope And Boundaries

- Included work.
- Non-goals.
- Constraints. Preserved behavior belongs in Contracts And Preserved Behavior.
- New dependencies: None | <package and why existing code or libraries do not suffice>

## Acceptance Criteria

Give each criterion a stable ID and an observable outcome.

| ID | Criterion | Verification |
| --- | --- | --- |
| AC-1 | <observable outcome> | <test name or V-ID> |

## Approach

Ordered build steps with affected areas, each tagged with the acceptance
criteria it serves, for example: `1. Add the parser for X in <path> (AC-1, AC-3)`.

## Implementation Design (conditional)

Scale the design to the work. Name the actual modules, classes, or functions
that own important responsibilities; do not introduce classes solely to fill
the table or specify every private method.

### Responsibilities And Boundaries

| Component | Action | Responsibility | Dependencies |
| --- | --- | --- | --- |
| <module, class, or function and relevant path> | Add / Modify / Reuse | <specific responsibility and rules it owns> | <direct dependencies> |

### Main Flow (conditional)

Describe how the components collaborate at runtime for the main scenario,
including failure paths that affect the design. Omit when the Approach and
responsibilities already make it obvious.

### Contracts And Preserved Behavior

Describe the important inputs, outputs, errors, and invariants.
Identify existing behavior and interfaces that must stay unchanged or compatible.

### Design Rationale

Explain material design choices:

- Why each new component is necessary.
- How the structure avoids duplicating rules or mixing responsibilities.
- Why existing components can or cannot be reused.
- Any justified complexity or tradeoffs.

Routine implementation details remain the implementer's choice. Changes to
approved responsibility ownership, public contracts, dependency direction, or
new dependencies require a plan revision and explicit user approval before
implementation.

## Risks And Alternatives (conditional)

Material risks, mitigations, and alternatives considered.
Include rollback considerations when relevant.

## Workflow-Specific Requirements (conditional)

Include only details not already covered above:

- Feature: relevant scenarios.
- Refactor: baseline verification to capture before restructuring.
- Planning only: expected handoff and deferred implementation.

## Verification

| ID | Command or manual check | Expected result |
| --- | --- | --- |
| V-1 | <command> | <result> |

## Revisions

| Date | Change | Approval |
| --- | --- | --- |
| <YYYY-MM-DD> | Initial draft | Pending |

## Did Not Do

Planning omissions such as areas not investigated or decisions deferred, or
"No meaningful omissions." Non-goals belong in Scope And Boundaries.
