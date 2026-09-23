# SOLID Principles

Use SOLID as design questions for classes, modules, APIs, and architecture boundaries. The goal is lower change risk, not extra ceremony.

## Quick Reference

| Principle | Design Question | Red Flag | Safer Response |
| --- | --- | --- | --- |
| SRP - Single Responsibility | Does this unit have one clear reason to change? | One class changes for validation, persistence, formatting, and policy. | Split along responsibilities that change independently. |
| OCP - Open/Closed | Is extension safer than direct modification for this variation? | Every new case risks breaking stable existing behavior. | Put recurring variation behind a stable contract; otherwise prefer a direct tested edit. |
| LSP - Liskov Substitution | Can every subtype honor the same contract? | A subtype throws, ignores inputs, or weakens guarantees callers expect. | Fix the contract, use composition, or avoid the subtype relationship. |
| ISP - Interface Segregation | Do clients depend only on behavior they use? | Implementers have no-op methods or callers receive broad service objects. | Split interfaces by client need and keep contracts small. |
| DIP - Dependency Inversion | Does high-level policy avoid depending on volatile details? | Domain logic imports concrete databases, frameworks, or clients. | Depend on a narrow abstraction at the boundary and inject concrete details. |

## OCP Without Speculation

OCP is a risk-management heuristic. Use extension when variation is recurring, high-risk, or naturally behind a boundary. Do not create an interface, plugin system, or class hierarchy for a hypothetical future.

Direct modification is often the simplest responsible solution when:

- The behavior has one current implementation.
- The module is well tested and locally owned.
- The new branch is clearer than a new abstraction.

## LSP Contract Check

Before using inheritance or substitutable implementations, confirm:

- Preconditions are not stricter in the subtype.
- Postconditions and return shapes remain compatible.
- Exceptions and side effects do not surprise callers.
- Tests written against the base contract pass for each implementation.

## DIP Boundary Check

Introduce abstractions at volatile or external boundaries:

- Database, filesystem, network, queue, clock, payment, email, and framework edges.
- Cross-module contracts where policy must outlive implementation details.

Avoid abstractions that merely rename one concrete implementation without reducing volatility or test cost.
