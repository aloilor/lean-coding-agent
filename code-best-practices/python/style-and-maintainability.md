# Style And Maintainability

## Let Tools Enforce The Baseline

- Follow the project's formatter, linter, and import-order rules instead of formatting by hand.
- Use four spaces for indentation, keep lines readable, and prefer one obvious layout style across the codebase.
- Keep imports at the top of the file unless a local import solves a real dependency or startup problem.

## Keep Functions Small And Purposeful

- A function should do one clear job.
- Split code when one function mixes validation, data access, formatting, and side effects.
- Keep file, network, and database operations near the edges so the core logic stays easy to test.

Good example:

```python
def build_invoice_rows(items: list[InvoiceItem]) -> list[dict[str, object]]:
    return [build_invoice_row(item) for item in items]
```

## Prefer Explicit Data Shapes

- Use named structures when the data has stable meaning.
- Prefer a `dataclass`, small class, or clear typed mapping over passing loose dictionaries everywhere.
- Keep related values together so call sites do not need to remember positional meaning.

Good example:

```python
from dataclasses import dataclass


@dataclass(slots=True)
class RetryPolicy:
    max_attempts: int
    backoff_seconds: float
```

## Add Type Hints Where They Clarify Contracts

- Add type hints to public functions, return values, and shared data structures.
- Use types to make inputs, outputs, and optional values obvious to readers and tools.
- Do not add noisy annotations to every short local variable when the meaning is already clear.

Good example:

```python
def load_user(user_id: str) -> User | None:
    ...
```

## Raise Precise Exceptions

- Raise the narrowest built-in exception that matches the problem, such as `ValueError`, `TypeError`, or `FileNotFoundError`.
- Use custom exceptions when the caller needs to distinguish one domain failure from another.
- Avoid broad `except Exception:` blocks unless you are adding context and re-raising, or you are handling a true process boundary.

Better:

```python
if quantity < 0:
    raise ValueError("quantity must be non-negative")
```

Avoid:

```python
if quantity < 0:
    raise Exception("bad quantity")
```

## Document Public Behavior, Not Obvious Code

- Write docstrings for public modules, classes, and functions when they expose behavior another engineer needs to use correctly.
- Explain constraints, side effects, important defaults, and non-obvious return behavior.
- Do not add comments that simply restate the next line of code.

Good example:

```python
def acquire_lock(key: str, timeout_seconds: float) -> None:
    """Block until the lock is acquired or raise TimeoutError."""
```

## Prefer The Standard Library First

- Reach for the standard library before adding a dependency for a small utility need.
- Prefer tools such as `pathlib`, `collections`, `itertools`, and context managers when they keep the code simpler.
- Add a third-party package when it clearly removes substantial complexity or maintenance risk.

## Test Behavior At The Boundary

- Test the observable behavior of functions and modules instead of their private implementation details.
- Cover invalid inputs, edge cases, and failure paths, not only the happy path.
- Keep most tests straightforward and use mocks mainly at process boundaries such as time, network, filesystem, or external services.

## Practical Checks

- Can I describe each function in one short sentence without using "and then" repeatedly?
- Would another engineer understand the main data shape without tracing five call sites?
- Do the type hints clarify a contract that matters to callers?
- Am I raising a precise exception and letting unexpected errors surface clearly?
- Do the tests prove behavior instead of locking the code to one internal implementation?
