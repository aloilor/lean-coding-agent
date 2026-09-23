# Inline Comments

Inline comments should explain context the code cannot express clearly. First improve names and structure; then comment only on intent, constraints, tradeoffs, and surprising local behavior.

## Comment Rules

| Rule | Use | Red Flag |
| --- | --- | --- |
| Prefer self-explaining code first | Rename or extract before adding a comment that explains what code does. | A comment only gives a vague value or operation a clearer name. |
| Explain why, not obvious what | Capture constraints, tradeoffs, and surprising behavior. | A comment merely narrates the operation beside it. |
| Keep comments accurate | Update or delete comments when behavior changes. | Timeout/comment mismatch, stale TODO, or old business rule. |
| Keep API docs separate | Use inline comments for local context, not public contract documentation. | A local comment tries to document caller-facing behavior. |

## Checks

- Would a better name remove this comment?
- Does the comment explain a constraint, decision, or surprising behavior?
- Is it merely repeating the code?
- Did nearby behavior change without updating the comment?
- Can the comment be deleted because the code now explains itself?
