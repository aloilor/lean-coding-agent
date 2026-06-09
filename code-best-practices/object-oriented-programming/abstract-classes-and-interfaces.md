# Abstract Classes And Interfaces

## Start Concrete By Default

- A plain concrete class is usually the right starting point.
- Do not introduce an interface or abstract base class only because "we might need it later".
- Extract an abstraction when you have a real second implementation, a stable extension point, or a clear boundary that callers should depend on.

Good example:

```ts
class TaxCalculator {
  calculate(order: Order): number { ... }
}
```

- If there is only one implementation and no real variation yet, a concrete class is simpler.

Avoid:

- Creating `ITaxCalculator` and `BaseTaxCalculator` on day one when only one class exists and nothing needs to vary yet.

## When To Use An Interface

- Use an interface when callers need a contract, not a shared implementation.
- Use it when multiple classes should be interchangeable behind the same role.
- Use it when unrelated classes need to expose the same capability.
- Use it to keep business logic depending on behavior instead of infrastructure details.

Good example:

```ts
interface PaymentGateway {
  charge(amount: number): void;
}
```

- `StripePaymentGateway` and `FakePaymentGateway` can both satisfy the same contract.

More examples:

- `NotificationSender` implemented by `EmailSender` and `SmsSender`.
- `UserRepository` implemented by `PostgresUserRepository` and `InMemoryUserRepository`.

Use an interface when:

- You expect multiple implementations with the same behavior contract.
- Callers should not know or care which implementation they receive.
- The types sharing the contract are not naturally part of one inheritance family.

Avoid:

- Adding an interface that only mirrors one class with no real variation or boundary.
- Using interfaces as decoration for every class in the codebase.

Concrete avoid example:

```ts
interface UserService {
  createUser(data: CreateUserData): User;
}

class DefaultUserService implements UserService {
  createUser(data: CreateUserData): User { ... }
}
```

- If there is only one implementation and no architectural reason for the boundary, this adds ceremony without value.

## When To Use An Abstract Class

- Use an abstract class when several closely related types share both a contract and reusable behavior.
- Use it when the base class should enforce common rules, state handling, or a shared algorithm shape.
- Use it when subclasses are truly specialized versions of the same concept.

Good example:

```ts
abstract class ReportExporter {
  export(report: Report): string {
    this.validate(report);
    return this.render(report);
  }

  protected validate(report: Report) { ... }
  protected abstract render(report: Report): string;
}
```

- The base class keeps the common workflow, while subclasses provide the format-specific part.

More examples:

- A `Shape` base class that stores shared geometry data and requires each subtype to implement `area()`.
- A `Job` base class that provides retry and logging hooks while subclasses define the actual work.

Use an abstract class when:

- Subclasses need shared code, not only a shared method list.
- The base type owns state or invariants that every subtype must preserve.
- The extension model is intentionally narrow and controlled.

Avoid:

- Using an abstract class only to reuse a few helper methods between unrelated types.
- Forcing subclasses into a hierarchy when composition would be simpler.
- Creating a base class when subclasses need to disable inherited behavior or ignore inherited state.

Concrete avoid example:

```ts
abstract class Animal {
  abstract fly(): void;
}

class Dog extends Animal {
  fly(): void {
    throw new Error("Not supported");
  }
}
```

- If a subtype has to break the parent contract, the hierarchy is wrong.

## Interface Vs Abstract Class

- Choose an interface when you need a role.
- Choose an abstract class when you need a family with shared behavior.
- Choose a concrete class when you do not yet need either.

In simple terms:

- Interface: "these types can all do this".
- Abstract class: "these types are all versions of this and share part of how it works".
- Concrete class: "we only need one straightforward implementation right now".

## Common Pattern

- It is normal to use both together.
- Let callers depend on an interface, and let one branch of implementations share code through an abstract class behind that interface.

Example:

```ts
interface NotificationSender {
  send(message: Message): void;
}

abstract class BaseEmailSender implements NotificationSender {
  send(message: Message): void {
    this.validate(message);
    this.deliver(message);
  }

  protected validate(message: Message) { ... }
  protected abstract deliver(message: Message): void;
}
```

- The interface defines the role seen by callers.
- The abstract class helps related implementations share logic internally.

## Practical Checks

- Am I adding an abstraction for a real need, or only for future speculation?
- Do callers need a contract, or do subclasses need shared code and state?
- Are these types truly one family, or just separate classes with a similar method?
- Would composition be simpler than introducing a base class?
- If I removed the abstraction, would the design become clearer instead of weaker?
