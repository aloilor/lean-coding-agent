# Object-Oriented Design Rules

Use this as a routing map for object boundaries, SOLID checks, inheritance, polymorphism, patterns, and domain modeling. Open detail files only when the current task needs deeper guidance.

## Core Rules

| Need | Rule | Details |
| --- | --- | --- |
| Responsibilities | Ask what each unit knows, does, decides, and protects. | [object-oriented-design.md](./object-oriented-design.md) |
| Encapsulation | Keep behavior near the state and invariants it protects. | [object-oriented-design.md](./object-oriented-design.md) |
| Collaboration | Prefer telling collaborators what outcome is needed over pulling data out and deciding externally. | [object-oriented-design.md](./object-oriented-design.md) |
| Inheritance | Prefer composition unless a stable subtype contract is genuinely present. | [object-oriented-design.md](./object-oriented-design.md) |
| SOLID | Use SOLID as design questions, not ceremony mandates. | [solid-principles.md](./solid-principles.md) |
| Patterns | Use a pattern only when it clearly simplifies a real recurring design pressure. | [design-patterns.md](./design-patterns.md) |
| Domain modeling | Use value objects, entities, or aggregates only when they protect real domain rules. | [object-oriented-design.md](./object-oriented-design.md) |

## SOLID Questions

| Principle | Question |
| --- | --- |
| SRP | Does this have one clear reason to change? |
| OCP | Is extension safer than direct modification for this variation? |
| LSP | Can substitutes honor the same contract without surprising callers? |
| ISP | Do callers depend only on behavior they use? |
| DIP | Does high-level policy avoid depending on volatile details? |

## Stop And Reconsider

- A class is mostly getters and setters with behavior elsewhere.
- A subtype weakens or surprises the parent contract.
- A pattern name makes the design larger without reducing risk.
- A domain model uses value objects, entities, or aggregates where simple data would do.
