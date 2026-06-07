# Code Documentation

## Document The Public Contract First

- Document modules, classes, functions, endpoints, and commands that other engineers are expected to use directly.
- Focus first on what callers need to know: inputs, outputs, side effects, failure modes, and important constraints.
- Keep internal implementation notes out of public-facing API documentation unless they affect correct usage.

Good documentation answers questions like:

- What does this component do?
- What inputs are required or optional?
- What can it return or change?
- What assumptions or limits matter to callers?

## Keep Documentation Close To The Code

- Put documentation near the code it describes when possible so it changes with the implementation.
- Prefer code-adjacent docs for public functions, exported types, and reusable modules.
- Use higher-level docs such as `README.md` files when the topic spans multiple files or explains how pieces fit together.

- Code comments are better for local intent.
- API docs are better for usage contracts.
- READMEs are better for setup, workflows, and architecture overviews.

## Write For The Reader's Next Question

- Start with the shortest explanation that lets another engineer use the code correctly.
- Prefer examples when the API shape, expected order, or common mistakes are easier to understand from a concrete case.
- Explain unusual behavior explicitly, especially when the default expectation would be wrong.

Better example topics:

- Why retries stop after a certain count
- Why a parameter must be passed in UTC
- Why a callback runs only once

## Prefer Stable Facts Over Temporary Narration

- Document behavior, contracts, and constraints that are likely to stay true across refactors.
- Avoid step-by-step descriptions of the current implementation unless that detail is part of the contract.
- If the docs mostly describe how the code is currently written, they will become stale faster than the code changes.

Prefer:

- "Returns cached results for five minutes."
- "Requires an authenticated user."
- "Retries only idempotent requests."

Avoid:

- "Loops through the array and sets a flag."
- "Calls helper A, then helper B, then helper C."

## Explain Edge Cases And Failure Modes

- Document surprising edge cases where correct use depends on special handling.
- Call out failure behavior when the caller needs to recover, retry, validate, or avoid data loss.
- If an operation is destructive, expensive, asynchronous, or eventually consistent, say so clearly.

Examples:

- A function throws on invalid state instead of returning `null`
- An API accepts partial success and returns per-item errors
- A background job may run more than once and must be idempotent

## Keep Examples Small And Honest

- Use the smallest example that shows correct usage.
- Keep examples aligned with real behavior and valid names from the current codebase when practical.
- Update or remove examples when the underlying API changes.

Better example qualities:

- Short enough to scan quickly
- Complete enough to compile or be copied with minor edits
- Focused on the main success path or the main failure path

## Use Consistent Structure

- Keep similar docs in a similar shape so readers know where to look.
- A simple structure usually works well: summary, parameters or inputs, return value or effects, errors, and example.
- Do not force a long template onto tiny functions that only need one or two sentences.

## Remove Documentation That Lost Its Job

- Delete documentation that repeats obvious code, explains removed behavior, or describes an old API shape.
- If better naming or extraction made a paragraph unnecessary, remove it instead of preserving extra noise.
- Treat stale documentation as a bug because it teaches readers the wrong thing.

## Practical Checks

- Does this documentation help a caller use the code correctly without reading the full implementation?
- Is the documentation close enough to the code that future changes are likely to update both together?
- Did I document stable behavior and constraints instead of temporary implementation steps?
- Are edge cases, side effects, and failure modes clear where they matter?
- Would a short example reduce ambiguity more than another paragraph?
