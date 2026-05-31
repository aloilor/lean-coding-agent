# SOLID

## Single Responsibility Principle

- A module should have one reason to change.
- Group code that changes for the same reason, and separate code that changes for different reasons.
- Do not mix business rules, persistence, presentation, and formatting logic in the same class.

Good example:

- `PayrollCalculator` computes pay.
- `HoursReportFormatter` formats output.
- `PayrollRepository` persists payroll data.

Avoid:

- One `EmployeeService` class that calculates pay, renders HTML, and saves database rows.

## Open-Closed Principle

- Design modules so new behavior can be added without repeatedly editing stable code.
- Prefer adding a new implementation behind an abstraction over growing `if/else` trees in shared code.
- Use this to protect stable business logic from volatile details.

Good example:

```ts
interface PaymentMethod {
  charge(amount: number): void;
}
```

- Add `CardPayment` and `WirePayment` implementations instead of rewriting the checkout flow for each method.

Avoid:

```ts
if (paymentType === "card") {
  ...
} else if (paymentType === "wire") {
  ...
} else if (paymentType === "paypal") {
  ...
}
```

## Liskov Substitution Principle

- If `Child` is a subtype of `Parent`, code written for `Parent` should still work with `Child`.
- A subtype should not surprise callers or break the normal behavior of the parent type.
- If callers need `instanceof` checks or special cases for one subtype, the design is probably wrong.

Good example:

- Every `NotificationSender` still sends a notification when `send()` is called.
- Callers can treat `EmailSender` and `SmsSender` the same way.

Avoid:

- A `ReadOnlyFile` subtype of `File` that breaks when code calls `write()`.
- A subtype that forces callers to add `if (x instanceof SpecialCase)` checks.

## Interface Segregation Principle

- Keep interfaces small.
- A client should depend only on the methods it actually uses.
- If different callers need different parts, split the interface.

Good example:

```ts
interface UserReader {
  getById(id: string): User;
}

interface UserWriter {
  save(user: User): void;
}
```

Avoid:

- A single `UserService` interface with dozens of methods used by every caller.

## Dependency Inversion Principle

- Business logic should not depend directly on low-level details like databases or HTTP clients.
- Depend on interfaces or abstractions instead.
- Keep infrastructure code at the edges.

Good example:

```ts
class InvoiceService {
  constructor(private readonly gateway: InvoiceGateway) {}
}
```

- `InvoiceService` depends on `InvoiceGateway`, while `PostgresInvoiceGateway` depends on that abstraction.

Avoid:

- Business logic importing ORM models or HTTP clients directly.

## Practical Checks

- Does each class have one clear reason to change?
- Can new behavior be added by extension more often than by rewriting stable code?
- Can every implementation be used through its abstraction without surprises?
- Are interfaces sized to actual client needs?
- Do business rules depend on abstractions instead of infrastructure details?
