# Plan: <name>

Status: Draft | Awaiting approval | Approved
Workflow: <workflow>
Approval: <actual user approval reference, or Pending>

<!-- Keep the core headings and scale detail to the task. Replace placeholders
and choices; remove drafting guidance from the completed plan. Use
"Not applicable — <reason>" for conditional sections. Record approval only
after the main agent confirms actual user approval. -->

## Objective And Requirements

Describe the intended outcome and the requirements it must satisfy.
Link the originating request, specification, or incident when available.

## Evidence And Decisions

- Relevant code, documentation, or investigation evidence.
- Resolved user decisions and their rationale.
- Assumptions and unresolved questions.
- Grill outcome.

## Scope And Boundaries

- Included work.
- Non-goals.
- Constraints and behavior that must remain unchanged.

## Acceptance Criteria

Give each criterion a stable ID and an observable outcome.

| ID | Criterion | Verification |
| --- | --- | --- |
| AC-1 | <observable outcome> | <test or check> |

## Approach

Ordered implementation steps, with affected areas and links to acceptance
criteria. Include only the design detail needed to proceed.

## Implementation Design

Scale the design to the work. Name the actual modules, classes, or functions
that own important responsibilities; do not introduce classes solely to fill
the table or specify every private method.

### Responsibilities And Boundaries

| Component | Action | Responsibility | Dependencies |
| --- | --- | --- | --- |
| <module, class, or function and relevant path> | Add / Modify / Reuse | <specific responsibility and rules it owns> | <direct dependencies> |

### Main Flow

Describe how the components collaborate for the main scenario.
Include failure paths when they affect the design.

### Contracts And Preserved Behavior

Describe the important inputs, outputs, errors, and invariants.
Identify existing behavior and interfaces that must stay compatible.

### Design Rationale

Explain material design choices:

- Why each new component is necessary.
- How the structure avoids duplicating rules or mixing responsibilities.
- Why existing components can or cannot be reused.
- Any justified complexity or tradeoffs.

Routine implementation details remain the implementer's choice. Changes to
approved responsibility ownership, public contracts, or dependency direction
require a plan revision and explicit user approval before implementation.

## Risks And Alternatives

Material risks, mitigations, and alternatives considered.
Include rollback considerations when relevant.

## Workflow-Specific Requirements

Include only the applicable workflow details:

- Feature: relevant scenarios.
- Refactor: preserved behavior and baseline verification.
- Bug fix: incident evidence, root cause, and repair contract.
- Planning only: expected handoff and deferred implementation.

## Verification

Relevant commands or manual checks, expected results, and applicable stop
conditions.

## Did Not Do

Explicit omissions, or "No meaningful omissions."
