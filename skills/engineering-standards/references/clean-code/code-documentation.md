# Code Documentation

Documentation should help the next caller or maintainer use, change, debug, or operate behavior correctly. Prefer clear code first; document what names and types cannot make obvious.

## Document Caller Contracts

For public APIs, exported functions, shared modules, scripts, and durable interfaces, document the facts callers rely on:

- Purpose and expected inputs.
- Return values or outputs.
- Constraints, units, ordering, and idempotency.
- Side effects such as persistence, network calls, retries, emitted events, or file writes.
- Failure modes, validation errors, partial failures, and recovery expectations.
- One small honest example when usage is non-obvious.

Skip contract docs when the name, type, and local scope already answer the caller's next question.

## Keep Documentation Close

Put documentation where maintainers will update it with the behavior:

- Function or method docs for callable contracts.
- Module docs for shared concepts and constraints.
- README or `agent-context/` docs for project workflows and architecture.
- Inline comments only for local non-obvious decisions.

## Prefer Stable Facts

Document behavior, constraints, and tradeoffs. Avoid temporary narration such as "first we loop over the items" when the code already says that.

Useful comments explain:

- Why an unusual choice exists.
- Which external constraint forced a shape.
- Which invariant must not be broken.
- Why a simpler-looking alternative is unsafe.

## Examples

Keep examples small, realistic, and copy-safe:

- Show the minimum inputs needed.
- Avoid fake options that do not work.
- Include the edge case only when it changes correct use.
- Update or delete examples when behavior changes.

## Remove Documentation That Lost Its Job

Delete or rewrite docs that are stale, obvious, misleading, or duplicating better nearby documentation. A wrong comment is worse than no comment.

## Quick Checks

- Would a caller know how to use this without reading the implementation?
- Are constraints, side effects, and failure modes visible where they matter?
- Is the documentation stable enough to survive small implementation changes?
- Did this change make an existing comment or example inaccurate?
