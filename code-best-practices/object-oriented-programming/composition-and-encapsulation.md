# Composition And Encapsulation

## Favor Composition Over Inheritance

- Composition means building an object by giving it other objects to work with, instead of inheriting behavior from a parent class.
- In simple terms: "has a" is often safer than "is a".
- Use inheritance only when one type is really a specialized version of another.
- If you just want to reuse behavior, composition is usually safer.
- It is often better to wrap an object than to subclass it.

Good example:

```ts
class InstrumentedSet<T> {
  constructor(private readonly inner: Set<T>) {}
}
```

- The wrapper can add logic without depending on the internal behavior of `Set`.

More examples:

```ts
class ReportService {
  constructor(
    private readonly repository: ReportRepository,
    private readonly formatter: ReportFormatter
  ) {}
}
```

- `ReportService` uses other objects to do its work instead of inheriting from them.

```ts
class OrderService {
  constructor(private readonly paymentGateway: PaymentGateway) {}
}
```

- `OrderService` has a `PaymentGateway`. It does not need to extend one.

```ts
class CachedUserReader {
  constructor(private readonly inner: UserReader) {}
}
```

- The wrapper can add caching without changing the original reader.

Avoid:

- Subclassing a collection just to reuse code when a wrapper would do the job more safely.

Concrete avoid example:

```ts
class LoggedSet<T> extends Set<T> {
  add(value: T) {
    console.log("adding", value);
    return super.add(value);
  }
}
```

- This ties your class to `Set` internals when a wrapper would usually be safer.

## Hide Internal Representation

- Do not expose raw internal state when callers only need the object to do something.
- Let the object decide how its state can change.
- This helps the object protect its own rules and makes the internals easier to change later.

What this means:

- Callers should ask the object to perform an action, not reach inside and change its fields directly.
- The object should be the place where validation and invariants live.
- If every caller can change internal values freely, the object cannot protect itself.

Good example:

```ts
class Account {
  deposit(amount: number) { ... }
  withdraw(amount: number) { ... }
}
```

- Callers do not edit `balance` directly. They use methods that can enforce the rules.

More examples:

```ts
class ShoppingCart {
  addItem(productId: string, quantity: number) { ... }
  removeItem(productId: string) { ... }
}
```

- Callers do not push directly into an internal `items` array.

```ts
class Thermostat {
  setTemperature(value: number) { ... }
}
```

- The object can reject invalid temperatures instead of letting callers assign any value they want.

Avoid:

```ts
class Account {
  public balance: number;
}
```

- If callers can change `balance` directly, the object cannot protect its own rules.

Concrete avoid example:

```ts
class ShoppingCart {
  public items: CartItem[] = [];
}
```

- Now any caller can add invalid items, duplicate items, or negative quantities without going through cart rules.

## Prefer Stable Abstractions

- Expose what the object does, not how it stores data.
- Name methods after business behavior.
- Do not make callers depend on your internal data structure.

What this means:

- Callers should use actions like `addItem()` or `cancel()` instead of reaching into internal arrays, maps, or fields.
- If callers depend on the internal structure, even a small refactor can break many places.
- A stable abstraction gives callers a clear business-level API while keeping storage details private.

Good example:

- `cart.addItem(productId, quantity)` instead of exposing `cart.items.push(...)`.

More examples:

- `team.addMember(userId)` instead of `team.members.push(userId)`.
- `order.markAsPaid()` instead of `order.status = "paid"`.

Concrete example:

```ts
class Team {
  addMember(userId: string) { ... }
}
```

- The object can decide whether duplicates are allowed, whether the team is full, or whether the user is already present.

```ts
class Order {
  markAsPaid() { ... }
}
```

- The object can check whether the order was already canceled or already paid before changing its state.

Avoid:

- Exposing `team.members` or `order.status` and making every caller manage the rules by hand.

## Use Inheritance Narrowly

- Inheritance works best when the base class was clearly designed to be extended.
- If a subclass has to rely on hidden superclass behavior, the design is fragile.
- If a subclass has to turn inherited behavior off, the hierarchy is probably wrong.

## Practical Checks

- Am I using inheritance for subtyping, or only for code reuse?
- Would a wrapper or collaborator reduce coupling better than a subclass?
- Does this class protect its own rules, or are callers managing them manually?
- If I changed the internal data structure, would most callers remain unaffected?
