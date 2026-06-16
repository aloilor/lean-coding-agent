# Duplication And Refactoring

## Overview

Duplication and code smells are signals to inspect design. Refactor only when the change makes behavior clearer, safer, or easier to modify.

## Treat Duplication As A Design Smell

### Problem It Solves

Repeated business rules drift when one copy changes and another does not.

### How to Apply

Extract shared behavior when the repeated code represents the same concept. Do not abstract two similar lines before a real shared idea exists.

```typescript
// BAD: copied in many handlers
if (user.id !== invoice.ownerId || invoice.status === "paid") {
  throw new ForbiddenError();
}

// GOOD: one named policy
function assertCanEditInvoice(user: User, invoice: Invoice): void {
  if (user.id !== invoice.ownerId || invoice.status === "paid") {
    throw new ForbiddenError();
  }
}
```

### Detection Questions

- If this rule changes, how many places must be edited?
- Is the duplication repeated behavior or only similar syntax?
- Is there a clear name for the shared concept?

---

## Use Code Smells As Signals

### Problem It Solves

Smells like long functions, vague names, flag arguments, and deep nesting often point to hidden design problems.

### How to Apply

Investigate the smell first. Choose the smallest refactor that clarifies the underlying issue.

```typescript
// Smell: copied conditional policy
function assertCanDeleteProject(user: User, project: Project): void {
  if (!project.isOwnedBy(user)) throw new ForbiddenError();
  if (project.hasActiveBilling) throw new ActiveBillingError();
}
```

### Detection Questions

- What is the smell pointing at?
- Is the issue naming, function size, control flow, duplication, or boundaries?
- Can one small refactor clarify it?

---

## Refactor In Small Safe Steps

### Problem It Solves

Broad rewrites mix behavior changes with structure changes and become hard to review.

### How to Apply

Prefer mechanical, behavior-preserving steps: rename, extract function, replace nesting with guards, encapsulate direct mutation, run tests.

```typescript
// BEFORE
if (!request.user || request.user.role !== "admin") {
  throw new ForbiddenError();
}

// AFTER
assertAdminUser(request.user);
```

### Detection Questions

- Can this be improved with one small refactor?
- Are tests available for the behavior being preserved?
- Is this refactor separate from behavior changes?

---

## Avoid Premature Abstraction

### Problem It Solves

Bad abstractions create vague helpers, flags, and coupling that can be harder to remove than a little duplication.

### How to Apply

Wait until duplication reveals a shared concept. Name the abstraction after that concept.

```typescript
// BAD: one function hides separate operations
await updateInvoice(invoice, { recalculateTax: true, sendEmail: true });

// GOOD: separate intentions
await recalculateInvoiceTax(invoice);
await sendInvoiceUpdatedEmail(invoice);
```

### Detection Questions

- Is the abstraction named after a real shared concept?
- Does it need flags to recover meaning?
- Are callers likely to change in different directions?

---

## Practical Checks

- If this rule changes, how many places must be edited?
- What is the smell pointing at?
- Can the improvement be made as one small safe refactor?
- Is the abstraction clearer than the duplication it replaces?

---

## Quick Reference

| Rule | Good | Red Flag |
|------|------|----------|
| Duplication | Extract shared business rule | Copied policy across handlers |
| Code Smells | Investigate cause | Automatic rewrite because code is large |
| Small Refactors | Rename, extract, guard, test | Broad rewrite with behavior changes |
| Abstraction Timing | Shared concept is clear | Vague helper with flags |
