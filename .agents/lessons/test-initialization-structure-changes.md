# Test Initialization Structure Changes

## Mistake Pattern

Changing the project initializer to add, remove, move, or alter managed files or directories without updating its structural regression coverage can leave the documented initialization contract unverified.

## Rule

Whenever the initialization process changes the generated project structure, add or update a test that proves the new structural contract and its rerun behavior where ownership or idempotency matters. Rerun the focused initializer tests and the repository's broader applicable checks before completing the change.
