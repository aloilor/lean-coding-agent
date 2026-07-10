# Clean Code Rules

Use this as a routing map. Open a detail file only when the current task needs its examples or deeper questions.

## Core Rules

| Need | Rule | Details |
| --- | --- | --- |
| Naming | Use names that explain intent, domain meaning, and scope. | [naming-and-clarity.md](./naming-and-clarity.md) |
| Flow | Keep functions focused and prefer straightforward control flow over cleverness. | [functions-and-control-flow.md](./functions-and-control-flow.md) |
| Comments | Prefer self-explaining code; use comments for why, constraints, and surprises. | [inline-comments.md](./inline-comments.md) |
| Documentation | Document caller-facing contracts, edge cases, side effects, and failure modes. | [code-documentation.md](./code-documentation.md) |
| Duplication | Extract only when repeated code represents the same stable concept or business rule. | [duplication-and-refactoring.md](./duplication-and-refactoring.md) |
| Complexity | Reduce accidental complexity: change amplification, cognitive load, and hidden coupling. | [complexity.md](./complexity.md) |
| Smells | Treat smells as inspection signals, not automatic rewrite orders. | [code-smells.md](./code-smells.md) |

## Apply First

- Make behavior correct and verified.
- Express intent through clear names and obvious structure.
- Remove meaningful duplication when the shared concept is clear.
- Minimize concepts, branches, state, and moving parts.

## Stop And Reconsider

- Names hide domain meaning.
- A function mixes levels of detail or responsibilities.
- A comment explains obvious code instead of a non-obvious decision.
- Similar code is extracted before the shared concept is stable.
- Cleanup expands beyond the requested change.
