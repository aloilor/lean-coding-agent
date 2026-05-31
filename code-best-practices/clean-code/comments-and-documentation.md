# Comments And Documentation

## Prefer Self-Explaining Code First

- Use names and structure to explain what the code does before reaching for comments.
- Comments are not a substitute for clear code.
- The best comment is often removing the need for the comment.

Good example:

```ts
const retryDelayMs = 5000;
```

Avoid:

```ts
const d = 5000; // retry delay in milliseconds
```

## Use Comments For Why, Not For Obvious What

- Comments are most useful when they explain intent, constraints, or unusual decisions.
- Use them for business rules, historical context, tricky tradeoffs, or non-obvious safety requirements.
- Do not narrate code that already reads clearly.

Good examples:

- Why this retry is capped
- Why a fallback exists
- Why a weird vendor behavior is handled this way

Avoid:

- `i++ // increment i`
- `saveUser(); // save the user`

## Keep Comments Accurate

- A wrong comment is worse than no comment.
- Update comments when you change the code.
- Delete comments that repeat old behavior or describe code that no longer exists.

## Document Public Contracts Clearly

- Public APIs, modules, and important classes should explain how to use them.
- Focus on inputs, outputs, side effects, and constraints.
- Keep docs close to the code they describe.

## Practical Checks

- Does this comment explain something the code cannot say clearly on its own?
- Would better naming remove the need for this comment?
- If this code changed tomorrow, would the comment become stale?
