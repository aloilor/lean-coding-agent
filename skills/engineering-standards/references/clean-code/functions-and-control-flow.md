# Functions And Control Flow

Functions should do one clear job, and control flow should make the main path easy to scan. Prefer simple structure over clever expressions.

## Function And Flow Rules

| Rule | Use | Red Flag |
| --- | --- | --- |
| Keep functions focused | Separate validation, building, persistence, network calls, formatting, and rendering when they are distinct responsibilities. | One function mixes several kinds of work or cannot be described in one sentence. |
| Prefer guard clauses | Return or throw early for terminal cases so the normal path stays visible. | Pyramid-shaped nesting hides the main path. |
| Avoid meaning-changing flags | Split behavior when a boolean or enum changes what the function fundamentally does. | `sendEmail(user, false)` forces callers to remember hidden meaning. |
| Prefer straightforward flow | Split dense expressions when behavior, ordering, or side effects matter. | Side effects hide inside chains that look like data transformation. |

## Examples

```typescript
async function submitOrder(request: OrderRequest): Promise<OrderReceipt> {
  validateOrderRequest(request);
  const order = buildOrder(request);
  const payment = await chargeOrder(order);
  return createReceipt(order, payment);
}
```

```typescript
function getPayAmount(employee: Employee): Money {
  if (employee.isDead) return deadAmount(employee);
  if (employee.isSeparated) return separatedAmount(employee);
  if (employee.isRetired) return retiredAmount(employee);
  return normalPayAmount(employee);
}
```

```typescript
const overdueInvoices = invoices.filter(isOverdue);

for (const invoice of overdueInvoices) {
  await sendPaymentReminder(invoice);
  markReminderSent(invoice);
}
```

## Checks

- Can the function be described in one sentence?
- Does it mix multiple kinds of work?
- Is the happy path visible without reading several nested blocks?
- Are flags hiding separate workflows or tests?
- Would simpler control flow make review safer?
