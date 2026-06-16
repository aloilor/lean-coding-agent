# Functions And Control Flow

## Overview

Functions should do one clear job, and control flow should make the main path easy to scan. Prefer simple structure over clever expressions.

## Keep Functions Focused

### Problem It Solves

Large mixed functions are hard to test, review, reuse, and safely change.

### How to Apply

Separate validation, building, persistence, network calls, formatting, and response rendering when they are distinct responsibilities.

```typescript
// BAD
async function submitOrder(input: any) {
  if (!input.items?.length) throw new Error("bad");
  const total = input.items.reduce((sum: number, item: any) => sum + item.price, 0);
  const payment = await fetch("/charge", { method: "POST", body: JSON.stringify({ total }) });
  return { id: Math.random().toString(), total, payment };
}

// GOOD
async function submitOrder(request: OrderRequest): Promise<OrderReceipt> {
  validateOrderRequest(request);
  const order = buildOrder(request);
  const payment = await chargeOrder(order);
  return createReceipt(order, payment);
}
```

### Detection Questions

- Can the function be described in one sentence?
- Does it mix multiple kinds of work?
- Would extracting a block give that block a clear name?

---

## Prefer Guard Clauses Over Deep Nesting

### Problem It Solves

Deep nesting hides the normal path and makes edge cases harder to verify.

### How to Apply

Return or throw early for terminal cases. Keep the happy path left-aligned.

```typescript
function getPayAmount(employee: Employee): Money {
  if (employee.isDead) return deadAmount(employee);
  if (employee.isSeparated) return separatedAmount(employee);
  if (employee.isRetired) return retiredAmount(employee);
  return normalPayAmount(employee);
}
```

### Detection Questions

- Is the happy path visible without reading several nested blocks?
- Does each guard clause clearly end the current path?
- Did early returns clarify flow, or scatter behavior?

---

## Avoid Flag Arguments When They Change Meaning

### Problem It Solves

Flags make call sites unclear and often hide two different operations inside one function.

### How to Apply

Use separate named functions when a boolean or enum changes what the function means.

```typescript
// BAD
await sendEmail(user, true);

// GOOD
await sendPasswordResetEmail(user);
await sendWelcomeEmail(user);
```

### Detection Questions

- Does a boolean argument change the operation?
- Would two names make the call site clearer?
- Is the flag hiding separate workflows or tests?

---

## Prefer Straightforward Flow Over Cleverness

### Problem It Solves

Clever chains hide side effects and make behavior expensive to review.

### How to Apply

Split dense expressions when behavior matters. Keep side effects visible.

```typescript
// BAD
await Promise.all(invoices.filter(isOverdue).map(async (invoice) => markReminderSent(await sendPaymentReminder(invoice))));

// GOOD
const overdueInvoices = invoices.filter(isOverdue);

for (const invoice of overdueInvoices) {
  await sendPaymentReminder(invoice);
  markReminderSent(invoice);
}
```

### Detection Questions

- Is the main path obvious on first read?
- Are side effects hidden inside expressions that look like data transformation?
- Would splitting the expression make review safer?

---

## Practical Checks

- Can each function be described in one sentence?
- Is the happy path easy to find?
- Are flags hiding separate operations?
- Would simpler control flow make review safer?

---

## Quick Reference

| Rule | Good | Red Flag |
|------|------|----------|
| Focused Functions | One job per function | Validation, IO, formatting, and persistence mixed |
| Guard Clauses | Early terminal cases | Pyramid-shaped nesting |
| Flag Arguments | `sendWelcomeEmail()` | `sendEmail(user, false)` |
| Straight Flow | Visible side effects | Dense chained mutation |
