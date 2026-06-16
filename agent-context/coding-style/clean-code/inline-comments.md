# Inline Comments

## Overview

Inline comments should explain context the code cannot express clearly. First make the code readable; then comment only on intent, constraints, tradeoffs, and surprising local behavior.

## Prefer Self-Explaining Code First

### Problem It Solves

Comments often become a patch over unclear names or tangled structure.

### How to Apply

Rename or extract before adding a comment that only explains what the code does.

```typescript
// BAD
const d = 5000; // retry delay in milliseconds

// GOOD
const retryDelayMs = 5000;
```

### Detection Questions

- Would a better name remove this comment?
- Would extracting a helper make the intent clear?
- Is the comment compensating for unclear code?

---

## Use Comments For Why, Not For Obvious What

### Problem It Solves

Obvious comments add noise and drift. Missing context makes surprising code look accidental.

### How to Apply

Comment on intent, constraints, and tradeoffs.

```typescript
async function normalizeVendorStatus(status: string): Promise<OrderStatus> {
  // The vendor sends "done" for both shipped and delivered orders.
  // Check tracking before marking an order delivered.
  if (status === "done") return resolveDoneStatusFromTracking();
  return mapVendorStatus(status);
}
```

### Detection Questions

- Does the comment explain why this code exists?
- Does it capture a constraint, tradeoff, or surprising behavior?
- Is it merely repeating the code?

---

## Keep Comments Accurate

### Problem It Solves

A wrong comment teaches the wrong mental model.

### How to Apply

Update comments when behavior changes. Delete comments that no longer add context.

```typescript
// Keep this timeout lower than the gateway timeout so callers receive our error shape.
const paymentTimeoutMs = 4500;
```

### Detection Questions

- Did nearby behavior change without updating the comment?
- Does the comment describe old behavior?
- Can the comment be deleted because the code now explains itself?

---

## Practical Checks

- Does the comment explain something the code cannot say clearly?
- Would better naming remove the need for the comment?
- Is every comment still accurate?
- Is this local implementation context rather than public API documentation?

---

## Quick Reference

| Rule | Good | Red Flag |
|------|------|----------|
| Self-Explaining First | Clear names | Comment explaining `x` |
| Why, Not What | Vendor constraint | `i++ // increment i` |
| Accuracy | Comment matches behavior | Timeout comment says 3s, code says 4.5s |
