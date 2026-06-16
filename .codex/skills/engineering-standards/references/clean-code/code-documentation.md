# Code Documentation

## Overview

Documentation should help another engineer use code correctly without reading every implementation detail. Keep it close to the code, stable across refactors, and honest about side effects and failure modes.

## Document The Public Contract First

### Problem It Solves

Public code is easy to misuse when callers cannot see requirements, side effects, or errors.

### How to Apply

Document modules, classes, functions, endpoints, and commands that other engineers use directly.

```typescript
/**
 * Reserves inventory for every shippable item in an order.
 *
 * Throws `OutOfStockError` when at least one item cannot be reserved.
 * Writes reservation records and emits `inventory.reserved`.
 */
export async function reserveInventory(orderId: string): Promise<Reservation> {
  // ...
}
```

### Detection Questions

- Does the documentation tell callers how to use the code correctly?
- Are failure modes and side effects included?
- Are implementation details excluded unless they affect usage?

---

## Keep Documentation Close To The Code

### Problem It Solves

Distant docs become stale because maintainers forget to update them with code changes.

### How to Apply

Use docstrings or JSDoc for local public APIs, READMEs for module setup, and architecture docs for cross-module decisions.

```typescript
/**
 * Client for the billing provider's invoice endpoints.
 */
export class BillingInvoiceClient {
  // ...
}
```

### Detection Questions

- Is this documentation close enough to stay accurate?
- Should this be a local comment, API doc, README, or architecture note?
- Will future maintainers know where to update it?

---

## Write For The Reader's Next Question

### Problem It Solves

Docs that stop too early leave callers guessing about order, shape, constraints, or common mistakes.

### How to Apply

Start short, then answer the next question a caller is likely to ask.

```typescript
/**
 * Registers a callback that runs at most once for each message id.
 */
export function onMessageOnce(messageId: string, callback: MessageCallback): void {
  // ...
}
```

### Detection Questions

- What will the reader likely ask next?
- Would a short example answer faster than another paragraph?
- Is surprising behavior explicit?

---

## Prefer Stable Facts Over Temporary Narration

### Problem It Solves

Step-by-step implementation narration becomes stale after small refactors.

### How to Apply

Document behavior, contracts, and constraints that should remain true across implementation changes.

```typescript
/**
 * Retries only idempotent requests.
 */
export async function sendWithRetry(request: ApiRequest): Promise<ApiResponse> {
  // ...
}
```

### Detection Questions

- Is this fact stable across likely refactors?
- Is this describing behavior or implementation order?
- Would the doc stay true if helper functions changed?

---

## Explain Edge Cases And Failure Modes

### Problem It Solves

Edge cases and failure modes are where callers lose data, retry incorrectly, or report false success.

### How to Apply

Call out behavior the caller must recover from, retry, validate, or treat carefully. If an operation is destructive, expensive, asynchronous, eventually consistent, partially successful, or not idempotent, say so clearly.

```typescript
/**
 * Imports contacts and returns per-row failures.
 *
 * The import may partially succeed. Callers should inspect `failedRows`
 * before reporting success to the user.
 */
export async function importContacts(file: File): Promise<ContactImportResult> {
  // ...
}
```

### Detection Questions

- Does the caller need to recover, retry, validate, or avoid data loss?
- Is the operation destructive, expensive, asynchronous, or eventually consistent?
- Can this run more than once, and does it need to be idempotent?
- Are partial failures possible?

---

## Keep Examples Small And Honest

### Problem It Solves

Examples are often copied. Large or unrealistic examples teach the wrong shape.

### How to Apply

Use the smallest example that shows correct usage.

```typescript
const page = await listInvoices(customerId, { limit: 25, cursor });
```

### Detection Questions

- Is this the smallest useful example?
- Does it show real behavior?
- Would copying it lead to correct code?

---

## Use Consistent Structure

### Problem It Solves

Inconsistent docs make readers hunt for errors, examples, and side effects.

### How to Apply

Use a simple proportional structure: summary, inputs, return value or effects, errors, example.

```typescript
/**
 * Creates an invoice.
 *
 * Throws `EmptyInvoiceError` when no lines are provided.
 */
export function createInvoice(customer: Customer, lines: InvoiceLine[]): Invoice {
  // ...
}
```

### Detection Questions

- Do similar public APIs use a similar documentation shape?
- Is the template proportional to the code's importance?
- Can readers find errors and examples quickly?

---

## Remove Documentation That Lost Its Job

### Problem It Solves

Stale documentation is a bug because it makes readers trust the wrong thing.

### How to Apply

Delete docs that repeat obvious code, describe removed behavior, or explain an old API shape.

```typescript
// BAD: comment repeats the name
// Check if invoice needs review.
const requiresManualReview = invoice.total.greaterThan(reviewThreshold);

// GOOD
const requiresManualReview = invoice.total.greaterThan(reviewThreshold);
```

### Detection Questions

- Does this documentation still describe current behavior?
- Did clearer code remove the need for the doc?
- Is this doc helping a caller or preserving old noise?

---

## Practical Checks

- Can callers use the code safely without reading the implementation?
- Are side effects, failure modes, and edge cases clear where they matter?
- Is documentation close enough to the code to stay current?
- Are examples small, real, and copy-safe?
- Did you delete docs that no longer add value?

---

## Quick Reference

| Rule | Good | Red Flag |
|------|------|----------|
| Public Contract | Inputs, outputs, errors, effects | Callers must read implementation |
| Close To Code | JSDoc/docstring near API | Only in a stale wiki |
| Stable Facts | Behavior and constraints | Helper-by-helper narration |
| Edge Cases | Partial failure, idempotency, destructive operations | Hidden retry or data-loss risks |
| Examples | Small real usage | Huge toy setup |
| Cleanup | Delete stale docs | Old behavior kept "for context" |
