# Inline Comments

Inline comments should explain context the code cannot express clearly. First improve names and structure; then comment only on intent, constraints, tradeoffs, and surprising local behavior.

## Comment Rules

| Rule | Use | Red Flag |
| --- | --- | --- |
| Prefer self-explaining code first | Rename or extract before adding a comment that explains what code does. | `const d = 5000; // retry delay in milliseconds` |
| Explain why, not obvious what | Capture constraints, tradeoffs, and surprising behavior. | `i++ // increment i` |
| Keep comments accurate | Update or delete comments when behavior changes. | Timeout/comment mismatch, stale TODO, or old business rule. |
| Keep API docs separate | Use inline comments for local context, not public contract documentation. | A local comment tries to document caller-facing behavior. |

## Useful Comment Example

```typescript
async function normalizeVendorStatus(status: string): Promise<OrderStatus> {
  // The vendor sends "done" for both shipped and delivered orders.
  // Check tracking before marking an order delivered.
  if (status === "done") return resolveDoneStatusFromTracking();
  return mapVendorStatus(status);
}
```

## Checks

- Would a better name remove this comment?
- Does the comment explain a constraint, decision, or surprising behavior?
- Is it merely repeating the code?
- Did nearby behavior change without updating the comment?
- Can the comment be deleted because the code now explains itself?
