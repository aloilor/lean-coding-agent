# Naming And Clarity

## Use Names That Explain Intent

- Prefer names that tell the reader what the value or function means.
- A name should save the reader from guessing.
- If a variable name needs a comment to explain it, the name is usually weak.

Good examples:

- `area` instead of `a`
- `totalPrice` instead of `tp`
- `markAsPaid()` instead of `setStatus("paid")`

Avoid:

- `data`
- `tmp`
- `handleStuff()`

## Prefer Domain Language

- Use names from the business domain when the code models business behavior.
- Keep technical names for technical concerns.
- A domain object should sound like the problem space, not like the storage layer.

Good examples:

- `invoice.cancel()`
- `reservation.confirm()`
- `paymentGateway.charge()`

## Keep Scope Small

- Small scopes make names easier to understand.
- A short-lived variable can have a shorter name than a value used across a whole file, but it still should not be vague.
- The larger the scope, the more precise the name should be.

## Prefer Code That Reads Like A Story

- Good names reduce the need for explanatory comments.
- A reader should be able to scan the function and understand the flow from the names alone.
- Prefer extracting a small function with a good name over leaving a complex block inline.

Good example:

```ts
const outstandingBalance = calculateOutstandingBalance(invoice);
```

Avoid:

```ts
const x = calc(invoice);
```

## Practical Checks

- Would a new teammate understand this name without extra explanation?
- Does the name describe intent instead of implementation trivia?
- If I renamed the storage layer, would this domain name still make sense?
