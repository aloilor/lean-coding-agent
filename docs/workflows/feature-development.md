# Feature Development Workflow

Use this workflow for a feature or behavior change, from a small change through a cross-cutting feature. It establishes an approved plan, test-first implementation, independent review, and main-agent verification.

## Process

1. Run `grill-with-docs`, inspect the relevant code and documentation, then write a plan at `.agents/plans/plan_YYYYMMDD_<name>.md`. Get explicit user approval before implementation.
2. After approval, have the implementer work test-first through RED, GREEN, and REFACTOR. Record implementation and verification evidence in `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md`.
3. Have the code reviewer assess the change independently and record each pass at `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md`.
4. Resolve concrete `BLOCK` findings with the implementer and repeat focused checks and review. Address `WARNING` findings when they identify a plan issue, likely bug, security or privacy risk, or meaningful test gap.
5. The main agent runs relevant closeout verification, inspects the final diff, and reports behavior, verification, and residual risks.

## Artifacts

- Approved plan: `.agents/plans/plan_YYYYMMDD_<name>.md`
- Implementation report: `.agents/implementation-reports/implementation_YYYYMMDD_<name>.md`
- One or more review passes: `.agents/code-reviews/review_YYYYMMDD_<name>_pass_N.md`

## Flow

```mermaid
flowchart TD
    A[Feature request] --> B[Planner]
    B --> C[grill-with-docs]
    C --> D[Implementation plan]
    D --> E[User approval]
    E --> F[Implementer]
    F --> G[RED: write one failing behavior test]
    G --> H[GREEN: simplest code that passes]
    H --> I[REFACTOR: apply engineering-standards]
    I --> J[Run focused verification]
    J --> K{More behaviors to cover?}
    K -->|Yes, next slice| G
    K -->|No| L[Implementation report with TDD evidence]
    L --> M[Code reviewer]
    M --> N{Review result}
    N -->|APPROVE| O[Main-agent closeout]
    N -->|BLOCK| F
    N -->|WARNING| P{Tied to plan, bug, security, or test gap?}
    P -->|Yes| F
    P -->|No| O
```

Canonical instructions: [workflow-feature-development](../../skills/workflow-feature-development/SKILL.md).
