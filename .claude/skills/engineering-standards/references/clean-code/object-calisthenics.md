# Object Calisthenics

## Overview

Object Calisthenics are practice constraints for improving object-oriented design. Use them to notice overly procedural code, weak encapsulation, and objects that carry too many responsibilities.

These rules can be relaxed. They do not need to be enforced at all times.

Do not treat them as universal production laws or review blockers. They are most useful as refactoring prompts, review questions, and practice exercises.

## One Level Of Indentation Per Method

### Problem It Solves

Deep nesting hides the main path and usually means one function is doing too much.

### How to Apply

Extract named helpers, use guard clauses, and let collections or domain objects handle details.

```typescript
// BAD
function process(orders: Order[]) {
  for (const order of orders) {
    if (order.isValid()) {
      for (const item of order.items) {
        if (item.inStock) {
          processItem(item);
        }
      }
    }
  }
}

// GOOD
function process(orders: Order[]) {
  orders.filter((order) => order.isValid()).forEach(processOrder);
}

function processOrder(order: Order) {
  order.items.filter((item) => item.inStock).forEach(processItem);
}
```

### Detection Questions

- Is the happy path buried under nested blocks?
- Would a helper name explain a nested block better?
- Is the nesting showing missing domain behavior?

---

## Prefer Guard Clauses When Clearer

### Problem It Solves

`else` often keeps finished paths alive and makes the normal flow harder to scan.

### How to Apply

Use early returns, guard clauses, or polymorphism when they make the paths clearer.

```typescript
// BAD
function getDiscount(user: User): number {
  if (user.isPremium) {
    return 20;
  } else {
    return 0;
  }
}

// GOOD
function getDiscount(user: User): number {
  if (user.isPremium) return 20;
  return 0;
}
```

### Detection Questions

- Can the first branch return or throw and end the path?
- Would removing `else` make the main path clearer?
- Is a conditional hiding a polymorphic domain decision?

---

## Wrap Primitives And Strings When They Have Meaning

### Problem It Solves

Primitive values can carry domain meaning without validation, units, or behavior.

### How to Apply

Wrap primitives when they represent important domain concepts, rules, or units. Do not wrap every primitive mechanically.

```typescript
// BAD
function createUser(email: string, age: number) {}

// GOOD
class Email {
  constructor(private readonly value: string) {
    if (!value.includes("@")) throw new InvalidEmail();
  }
}

class Age {
  constructor(private readonly value: number) {
    if (value < 0 || value > 150) throw new InvalidAge();
  }
}

function createUser(email: Email, age: Age) {}
```

### Detection Questions

- Does this primitive have business rules or units?
- Could callers accidentally pass the wrong string or number?
- Would a value object make invalid state harder to create?

---

## Use First-Class Collections

### Problem It Solves

Raw collections invite callers to mutate internals and duplicate collection rules.

### How to Apply

Create a collection object when the collection has behavior, invariants, or repeated operations.

```typescript
// BAD
class Order {
  items: OrderItem[] = [];
  customerId: string;
}

// GOOD
class OrderItems {
  constructor(private readonly items: OrderItem[] = []) {}

  add(item: OrderItem): void {
    this.items.push(item);
  }

  total(): Money {
    return this.items.reduce((sum, item) => sum.add(item.total()), Money.zero());
  }
}
```

### Detection Questions

- Are callers directly mutating an internal list?
- Are collection rules copied across several places?
- Does the collection have behavior worth naming?

---

## Avoid Deep Object Chains

### Problem It Solves

Long object chains couple callers to internal structure.

### How to Apply

Ask the object you know to do the work or expose the needed behavior.

```typescript
// BAD
const city = order.customer.address.city;

// GOOD
const city = order.getShippingCity();
```

### Detection Questions

- Is the caller reaching through several objects?
- Would a method on the immediate object better express the need?
- Would an internal structure change ripple through callers?

---

## Do Not Abbreviate

### Problem It Solves

Abbreviations make names harder to search, pronounce, and understand.

### How to Apply

Use full words unless the abbreviation is a standard domain term.

```typescript
// BAD
const custRepo = new CustRepo();
const ord = new Ord();

// GOOD
const customerRepository = new CustomerRepository();
const order = new Order();
```

### Detection Questions

- Can the name be spoken clearly in a review?
- Is the abbreviation standard in this domain?
- Would search results be better with the full name?

---

## Keep Entities Small

### Problem It Solves

Large classes and methods often hide multiple responsibilities.

### How to Apply

Use size limits as warning lights, not as absolute rules. If a class or method is large, look for separate responsibilities, nested flow, duplication, or missing names.

Practical practice limits:

- Methods around 10 lines.
- Classes around 50 lines.
- Files around 100 lines.

### Detection Questions

- Can the method or class be summarized without using "and"?
- Is size coming from one cohesive concept or several mixed concerns?
- Would extraction improve names and tests?

---

## Prefer Few Instance Variables

### Problem It Solves

Many fields often mean an object is storing multiple concepts.

### How to Apply

Look for natural groups and extract value objects or collaborators when the grouping has meaning.

```typescript
// BAD
class Order {
  id: string;
  customerId: string;
  items: Item[];
  total: number;
  status: string;
}

// GOOD
class Order {
  constructor(
    private readonly id: OrderId,
    private readonly details: OrderDetails
  ) {}
}
```

### Detection Questions

- Do the fields form smaller natural concepts?
- Are some fields always passed or changed together?
- Is the class doing more than one job?

---

## Avoid Getter And Setter Data Bags

### Problem It Solves

Getter/setter-heavy objects make callers own the behavior and can leave invariants unprotected.

### How to Apply

Expose behavior, not just data. Tell objects what to do and let them enforce their own rules.

```typescript
// BAD
if (account.getBalance() >= amount) {
  account.setBalance(account.getBalance() - amount);
}

// GOOD
const result = account.withdraw(amount);
```

### Detection Questions

- Are callers pulling data out only to make decisions for the object?
- Would a behavior method protect invariants better?
- Is this object a domain object or a plain data transfer shape?

---

## Practical Checks

- Is this rule revealing a design smell, or am I applying it mechanically?
- Would following the rule make the code clearer for the next maintainer?
- Is this production code allowed to bend the exercise constraint for readability?
- Does the refactor preserve behavior and improve names, tests, or boundaries?
- Is relaxing the rule simpler and clearer in this specific case?

## Quick Reference

| Rule | Useful Pressure | Overuse Risk |
|------|-----------------|--------------|
| One indentation level | Extract hidden steps | Too many tiny helpers |
| Guard clauses | Clear terminal paths | Awkward early returns |
| Wrap primitives | Protect domain meaning | Ceremony for simple values |
| First-class collections | Encapsulate collection rules | Wrapper with no behavior |
| Shallow object chains | Reduce coupling | Pass-through methods everywhere |
| No abbreviations | Searchable names | Overlong names |
| Small entities | Find mixed concerns | Arbitrary line-count policing |
| Few fields | Find missing concepts | Artificial object splitting |
| No getter/setter data bags | Move behavior to data owner | Hiding simple DTO fields |
