# Naming And Clarity

## Overview

Names should make the code's intent obvious. A reader should not need to reverse-engineer several lines of implementation to understand what a value, function, class, or module means.

## Use Names That Explain Intent

### Problem It Solves

Vague names make reviewers guess. Bugs hide when `data`, `result`, `item`, or `handle()` could mean almost anything.

### How to Apply

Use names that describe the role in the current context.

```typescript
// BAD
const x = calc(invoice);
await gateway.run(customer, x);

// GOOD
const outstandingBalance = calculateOutstandingBalance(invoice);
await paymentGateway.charge(customer, outstandingBalance);
```

### Detection Questions

- Would a new teammate understand the name without reading the implementation?
- Would a better name remove a nearby explanatory comment?
- Is the name specific enough for how far it travels?

---

## Prefer Domain Language

### Problem It Solves

Domain code becomes hard to validate when it uses technical or generic words instead of business language.

### How to Apply

Use product and business terms for business behavior. Save technical names for technical concerns.

```typescript
// BAD
await reservation.update({ status: 2 });
await gateway.call("charge", data);

// GOOD
await reservation.confirm({ confirmedBy: currentUser.id });
await paymentGateway.charge(customer, invoice.totalDue);
```

### Detection Questions

- Does the name match the product or business process?
- Would this name still make sense if the database schema changed?
- Is a framework, transport, or storage term leaking into domain code?

---

## Keep Scope Small

### Problem It Solves

Short vague names become dangerous when they live too long or travel too far.

### How to Apply

Use short names only for tiny obvious scopes. Use more precise names for public APIs, module variables, and long-lived values.

```typescript
// Fine in a tiny loop
for (const row of rows) importRow(row);

// Better for a wider scope
const taxableLineTotal = invoice.lines
  .filter((line) => line.isTaxable)
  .reduce((total, line) => total + line.amount, 0);
```

### Detection Questions

- How far from its definition will this name be read?
- Is the name precise enough for that distance?
- Is a short name clear because of scope, or only because you just wrote it?

---

## Prefer Code That Reads Like A Story

### Problem It Solves

Dense blocks force readers to understand low-level details before they can understand the workflow.

### How to Apply

Use names and small helpers so the main path reads as a sequence of intentions.

```typescript
function payInvoice(invoice: Invoice, customer: Customer): Promise<Receipt> {
  validateInvoiceCanBePaid(invoice);
  const balance = calculateOutstandingBalance(invoice);
  return chargeCustomer(customer, balance);
}
```

### Detection Questions

- Can the main flow be understood by reading only function and variable names?
- Would extracting a helper give a complex block a useful name?
- Are names describing intent instead of mechanics?

---

## Practical Checks

- Would a new teammate understand the names without extra explanation?
- Does domain code use domain words?
- Are long-lived names more precise than short-lived names?
- Does the main flow read as clear intentions?

---

## Quick Reference

| Rule | Good | Red Flag |
|------|------|----------|
| Intent | `outstandingBalance` | `x`, `tmp`, `data` |
| Domain Language | `invoice.cancel()` | `invoice.updateStatus("x")` |
| Scope | Precise public names | Vague long-lived locals |
| Story | `validate -> calculate -> charge` | `check -> calc -> run` |
