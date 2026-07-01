# Code Smells

Code smells are signals to inspect design. They are not automatic rewrite commands. First understand why the smell exists, then choose the smallest behavior-preserving improvement that is in scope and verifiable.

## Smell Table

| Smell | What It Suggests | Safer Response |
| --- | --- | --- |
| Long method | Mixed responsibilities or hidden levels of detail. | Extract named steps only when it clarifies the main path. |
| Large class | Too many reasons to change. | Split by responsibility, lifecycle, or invariant boundary. |
| Long parameter list | Missing concept or scattered configuration. | Introduce a value object/options object only when parameters travel together. |
| Data clumps | Repeated groups of values with shared meaning. | Model the group when it has rules or behavior. |
| Primitive obsession | Domain concepts are carried by raw strings/numbers. | Wrap primitives when units, validation, or invariants matter. |
| Feature envy | Behavior lives away from the data or invariant it uses. | Move behavior toward the owner of the decision. |
| Message chain | Callers know too much about object internals. | Ask the nearer object for the outcome instead of walking the graph. |
| Inappropriate intimacy | Modules depend on private details of each other. | Move behavior, narrow contracts, or introduce a boundary. |
| Switch/type branching | Behavior varies by type. | Use polymorphism, strategy, or a dispatch table when branches are growing or volatile. |
| Divergent change | One unit changes for unrelated reasons. | Split responsibilities along change boundaries. |
| Shotgun surgery | One small behavior change touches many places. | Centralize the rule or create a clearer boundary. |
| Duplicate code | Repeated knowledge or behavior. | Extract only when it is the same stable concept. |
| Speculative generality | Abstractions, hooks, or config have no current user. | Delete or inline unused flexibility. |
| Dead code | Behavior no one calls or verifies. | Remove when safe; mention pre-existing dead code if out of scope. |
| Lazy class | A wrapper adds no behavior, invariant, or boundary. | Inline unless it represents a useful contract. |

## Response Checklist

1. Identify the smell and the concrete maintenance risk.
2. Confirm the behavior that must not change.
3. Choose the smallest in-scope refactor that reduces the risk.
4. Verify with tests, focused checks, or a clear manual inspection.
5. Stop before cleanup expands beyond the task.

## When Not To Refactor

- The smell is unrelated to the user's request.
- You cannot verify behavior preservation.
- The refactor would require changing the agreed specification.
- A local duplication is clearer than a premature abstraction.

Smells should sharpen judgment, not replace it.
