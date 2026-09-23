# Duplication And Refactoring

Duplication and smells are prompts to inspect design, not permission for broad rewrites. Refactor only when the change is in scope, behavior-preserving, and verifiable.

## Duplication Judgment

| Signal | Usually Extract | Usually Tolerate |
| --- | --- | --- |
| Business rule | The same policy, invariant, permission, calculation, or validation appears in multiple places. | Rules look similar but are owned by different domains or change for different reasons. |
| Syntax | The same code shape hides the same concept and has a clear name. | The code only looks alike and an abstraction would need a vague name. |
| Bug risk | A future fix would need to be made in several places. | Copies are local, obvious, and cheaper to read than an indirection. |
| Callers | Callers want one named operation. | Callers would need flags or options to recover different meanings. |

## Safer Refactoring Steps

Prefer small mechanical moves:

- Rename for intent.
- Extract a named function around one concept.
- Replace deep nesting with guard clauses when it clarifies the main path.
- Move behavior toward the data or invariant it protects.
- Encapsulate direct mutation that can break rules.
- Run the relevant check after each meaningful step.

Avoid mixing refactors with behavior changes unless the behavior change is the requested work and the refactor is needed to make it safe.

## Checks

- If this rule changes, how many places must be edited?
- Is this repeated knowledge or only similar syntax?
- Is there a clear domain name for the extraction?
- Would the abstraction remove risk or just add indirection?
- Can the refactor be reviewed and verified independently?
