# Functions And Control Flow

## Keep Functions Focused

- A function should do one small job.
- If a function is mixing validation, formatting, persistence, and side effects, it is probably doing too much.
- Extract small pieces when a block has its own clear purpose.

Good example:

```ts
function printOwing(invoice: Invoice) {
  printBanner();
  const outstanding = calculateOutstanding(invoice);
  printDetails(invoice, outstanding);
}
```

## Prefer Guard Clauses Over Deep Nesting

- Return early when a condition ends the main path.
- Guard clauses reduce indentation and make the happy path easier to read.
- Use them to flatten code, not to scatter exits randomly.

Good example:

```ts
function getPayAmount() {
  if (isDead) return deadAmount();
  if (isSeparated) return separatedAmount();
  if (isRetired) return retiredAmount();
  return normalPayAmount();
}
```

Avoid:

- Deeply nested `if` blocks that hide the main flow.

## Avoid Flag Arguments When They Change Meaning

- A boolean flag that changes behavior often hides two different operations inside one function.
- Prefer two clearly named functions when the caller is choosing between different actions.

Good examples:

- `regularBook(customer)`
- `premiumBook(customer)`

Avoid:

- `book(customer, true)`
- `book(customer, false)`

## Prefer Straightforward Flow Over Cleverness

- Write the code the next reader can scan quickly.
- Avoid dense conditionals, magical short names, and control flow that depends on subtle side effects.
- Clarity is usually more valuable than saving a few lines.

## Practical Checks

- Can I describe this function in one sentence?
- Is the main path obvious on first read?
- Would splitting this function make the names explain the logic better?
